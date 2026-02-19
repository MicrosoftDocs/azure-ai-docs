---
title: Hyperparameter tuning a model (v2)
titleSuffix: Azure Machine Learning
description: Discover how to define search spaces, choose sampling algorithms, and configure early termination policies for hyperparameter tuning in Azure ML.
#customer intent: As a data scientist, I want to automate hyperparameter tuning using Azure Machine Learning so that I can optimize model performance efficiently.
ms.author: scottpolly
author: s-polly
ms.reviewer: sooryar
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: training
ms.date: 09/15/2025
ms.topic: how-to
---


# Hyperparameter tuning a model (v2)

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]


In this article, you learn how to automate efficient hyperparameter tuning with the Azure Machine Learning SDK v2 and CLI v2 using the [SweepJob](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjob) class.

- Define the parameter search space
- Choose a sampling algorithm
- Set the optimization objective
- Configure an early termination policy
- Set sweep job limits
- Submit the experiment
- Visualize training jobs
- Select the best configuration

## What is hyperparameter tuning?

**Hyperparameters** are adjustable settings that control model training. For neural networks, for example, you choose the number of hidden layers and the number of nodes per layer. Model performance depends heavily on these values.

**Hyperparameter tuning** (or **hyperparameter optimization**) is the process of finding the hyperparameter configuration that yields the best performance. This process is often computationally expensive and manual.

Azure Machine Learning lets you automate hyperparameter tuning and run experiments in parallel to efficiently optimize hyperparameters.


## Define the search space

Tune hyperparameters by exploring the range of values defined for each hyperparameter.

Hyperparameters can be discrete or continuous, and can have a value distribution expressed with a [parameter expression](reference-yaml-job-sweep.md#parameter-expressions).

### Discrete hyperparameters

Discrete hyperparameters are specified as a `Choice` among discrete values. `Choice` can be:

* one or more comma-separated values
* a `range` object
* any arbitrary `list` object

```Python
from azure.ai.ml.sweep import Choice

command_job_for_sweep = command_job(
    batch_size=Choice(values=[16, 32, 64, 128]),
    number_of_hidden_layers=Choice(values=range(1,5)),
)
```

References:
- [Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)

In this case, `batch_size` takes one of [16, 32, 64, 128] and `number_of_hidden_layers` takes one of [1, 2, 3, 4].

The following advanced discrete hyperparameters can also be specified using a distribution:

* `QUniform(min_value, max_value, q)` - Returns a value like round(Uniform(min_value, max_value) / q) * q
* `QLogUniform(min_value, max_value, q)` - Returns a value like round(exp(Uniform(min_value, max_value)) / q) * q
* `QNormal(mu, sigma, q)` - Returns a value like round(Normal(mu, sigma) / q) * q
* `QLogNormal(mu, sigma, q)` - Returns a value like round(exp(Normal(mu, sigma)) / q) * q

### Continuous hyperparameters 

Continuous hyperparameters are specified as a distribution over a continuous range of values:

* `Uniform(min_value, max_value)` - Returns a value uniformly distributed between min_value and max_value
* `LogUniform(min_value, max_value)` - Returns a value drawn according to exp(Uniform(min_value, max_value)) so that the logarithm of the return value is uniformly distributed
* `Normal(mu, sigma)` - Returns a real value that's normally distributed with mean mu and standard deviation sigma
* `LogNormal(mu, sigma)` - Returns a value drawn according to exp(Normal(mu, sigma)) so that the logarithm of the return value is normally distributed

An example of a parameter space definition:

```Python
from azure.ai.ml.sweep import Normal, Uniform

command_job_for_sweep = command_job(   
    learning_rate=Normal(mu=10, sigma=3),
    keep_probability=Uniform(min_value=0.05, max_value=0.1),
)
```

References:
- [Normal](/python/api/azure-ai-ml/azure.ai.ml.sweep.normal)
- [Uniform](/python/api/azure-ai-ml/azure.ai.ml.sweep.uniform)

This code defines a search space with two parameters - `learning_rate` and `keep_probability`. `learning_rate` has a normal distribution with mean value 10 and a standard deviation of 3. `keep_probability` has a uniform distribution with a minimum value of 0.05 and a maximum value of 0.1.

For the CLI, use the [sweep job YAML schema](./reference-yaml-job-sweep.md) to define the search space:
```YAML
    search_space:
        conv_size:
            type: choice
            values: [2, 5, 7]
        dropout_rate:
            type: uniform
            min_value: 0.1
            max_value: 0.2
```

## Sampling the hyperparameter space

Specify the sampling method for the hyperparameter space. Azure Machine Learning supports:

* Random sampling
* Grid sampling
* Bayesian sampling

### Random sampling

Random sampling supports discrete and continuous hyperparameters, and supports early termination of low-performing jobs. Many users start with random sampling to identify promising regions, then refine.

In random sampling, values are drawn uniformly (or via the specified random rule) from the defined search space. After creating your command job, use `sweep` to define the sampling algorithm. 

```Python
from azure.ai.ml.entities import CommandJob
from azure.ai.ml.sweep import RandomSamplingAlgorithm, SweepJob, SweepJobLimits

   command_job = CommandJob(
       inputs=dict(kernel="linear", penalty=1.0),
       compute=cpu_cluster,
       environment=f"{job_env.name}:{job_env.version}",
       code="./scripts",
       command="python scripts/train.py --kernel $kernel --penalty $penalty",
       experiment_name="sklearn-iris-flowers",
   )

   sweep = SweepJob(
       sampling_algorithm=RandomSamplingAlgorithm(seed=999, rule="sobol", logbase="e"),
       trial=command_job,
       search_space={"ss": Choice(type="choice", values=[{"space1": True}, {"space2": True}])},
       inputs={"input1": {"file": "top_level.csv", "mode": "ro_mount"}},  # type:ignore
       compute="top_level",
       limits=SweepJobLimits(trial_timeout=600),
   )
```
References: 
- [CommandJob](/python/api/azure-ai-ml/azure.ai.ml.entities.commandjob)
- [RandomSamplingAlgorithm](/python/api/azure-ai-ml/azure.ai.ml.sweep.randomsamplingalgorithm)
- [SweepJob](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjob)
- [SweepJobLimits](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjoblimits)
- [Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)

#### Sobol
Sobol is a quasi-random sequence that improves space-filling and reproducibility. Provide a seed and set `rule="sobol"` on `RandomSamplingAlgorithm`.

```Python
from azure.ai.ml.sweep import  RandomSamplingAlgorithm

sweep_job = command_job_for_sweep.sweep(
    compute="cpu-cluster",
    sampling_algorithm = RandomSamplingAlgorithm(seed=123, rule="sobol"),
    ...
)
```
References: 
[RandomSamplingAlgorithm](/python/api/azure-ai-ml/azure.ai.ml.sweep.randomsamplingalgorithm)

### Grid sampling

Grid sampling supports discrete hyperparameters. Use grid sampling if you can budget to exhaustively search over the search space. Supports early termination of low-performance jobs.

Grid sampling does a simple grid search over all possible values. Grid sampling can only be used with `choice` hyperparameters. For example, the following space has six samples:

```Python
from azure.ai.ml.sweep import Choice

command_job_for_sweep = command_job(
    batch_size=Choice(values=[16, 32]),
    number_of_hidden_layers=Choice(values=[1,2,3]),
)

sweep_job = command_job_for_sweep.sweep(
    compute="cpu-cluster",
    sampling_algorithm = "grid",
    ...
)
```
References: 
[Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)

### Bayesian sampling

Bayesian sampling (Bayesian optimization) selects new samples based on prior results to improve the primary metric efficiently.

Bayesian sampling is recommended if you have enough budget to explore the hyperparameter space. For best results, we recommend a maximum number of jobs greater than or equal to 20 times the number of hyperparameters being tuned. 

The number of concurrent jobs has an impact on the effectiveness of the tuning process. A smaller number of concurrent jobs may lead to better sampling convergence, since the smaller degree of parallelism increases the number of jobs that benefit from previously completed jobs.

Bayesian sampling supports `choice`, `uniform`, and `quniform` distributions.

```Python
from azure.ai.ml.sweep import Uniform, Choice

command_job_for_sweep = command_job(   
    learning_rate=Uniform(min_value=0.05, max_value=0.1),
    batch_size=Choice(values=[16, 32, 64, 128]),
)

sweep_job = command_job_for_sweep.sweep(
    compute="cpu-cluster",
    sampling_algorithm = "bayesian",
    ...
)
```
References: 
- [Uniform](/python/api/azure-ai-ml/azure.ai.ml.sweep.uniform)
- [Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)


## <a name="specify-objective-to-optimize"></a> Specify the objective of the sweep

Define the objective of your sweep job by specifying the primary metric and goal you want hyperparameter tuning to optimize. Each training job is evaluated for the primary metric. The early termination policy uses the primary metric to identify low-performance jobs.

* `primary_metric`: The name of the primary metric needs to exactly match the name of the metric logged by the training script
* `goal`: It can be either `Maximize` or `Minimize` and determines whether the primary metric will be maximized or minimized when evaluating the jobs. 

```Python
from azure.ai.ml.sweep import Uniform, Choice

command_job_for_sweep = command_job(   
    learning_rate=Uniform(min_value=0.05, max_value=0.1),
    batch_size=Choice(values=[16, 32, 64, 128]),
)

sweep_job = command_job_for_sweep.sweep(
    compute="cpu-cluster",
    sampling_algorithm = "bayesian",
    primary_metric="accuracy",
    goal="Maximize",
)
```
References: 
- [Uniform](/python/api/azure-ai-ml/azure.ai.ml.sweep.uniform)
- [Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)

This sample maximizes "accuracy".

### <a name="log-metrics-for-hyperparameter-tuning"></a>Log metrics for hyperparameter tuning

Your training script **must** log the primary metric with the exact name expected by the sweep job.

Log the primary metric in your training script with the following sample snippet:

```Python
import mlflow
mlflow.log_metric("accuracy", float(val_accuracy))
```
References: 
[mlflow.log_metric](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.log_metric)

The training script calculates the `val_accuracy` and logs it as the primary metric "accuracy". Each time the metric is logged, it's received by the hyperparameter tuning service. It's up to you to determine the frequency of reporting.

For more information on logging values for training jobs, see [Enable logging in Azure Machine Learning training jobs](how-to-log-view-metrics.md).

## <a name="early-termination"></a> Specify early termination policy

End poorly performing jobs early to improve efficiency.

You can configure the following parameters that control when a policy is applied:

* `evaluation_interval`: the frequency of applying the policy. Each time the training script logs the primary metric counts as one interval. An `evaluation_interval` of 1 will apply the policy every time the training script reports the primary metric. An `evaluation_interval` of 2 will apply the policy every other time. If not specified, `evaluation_interval` is set to 0 by default.
* `delay_evaluation`: delays the first policy evaluation for a specified number of intervals. This is an optional parameter that avoids premature termination of training jobs by allowing all configurations to run for a minimum number of intervals. If specified, the policy applies every multiple of evaluation_interval that is greater than or equal to delay_evaluation. If not specified, `delay_evaluation` is set to 0 by default.

Azure Machine Learning supports the following early termination policies:
* [Bandit policy](#bandit-policy)
* [Median stopping policy](#median-stopping-policy)
* [Truncation selection policy](#truncation-selection-policy)
* [No termination policy](#no-termination-policy-default)


### Bandit policy

[Bandit policy](/python/api/azure-ai-ml/azure.ai.ml.sweep.banditpolicy) uses a slack factor or amount plus evaluation interval. It ends a job when its primary metric falls outside the allowed slack from the best job.

Specify the following configuration parameters:

* `slack_factor` or `slack_amount`: Allowed difference from the best job. `slack_factor` is a ratio; `slack_amount` is an absolute value.

    For example,  consider a Bandit policy applied at interval 10. Assume that the best performing job at interval 10 reported a primary metric is 0.8 with a goal to maximize the primary metric. If the policy specifies a `slack_factor` of 0.2, any training jobs whose best metric at interval 10 is less than 0.66 (0.8/(1+`slack_factor`)) will be terminated.
* `evaluation_interval`: (optional) the frequency for applying the policy
* `delay_evaluation`: (optional) delays the first policy evaluation for a specified number of intervals



```Python
from azure.ai.ml.sweep import BanditPolicy
sweep_job.early_termination = BanditPolicy(slack_factor = 0.1, delay_evaluation = 5, evaluation_interval = 1)
```
References: 
[BanditPolicy](/python/api/azure-ai-ml/azure.ai.ml.sweep.banditpolicy)

In this example, the early termination policy is applied at every interval when metrics are reported, starting at evaluation interval 5. Any jobs whose best metric is less than (1/(1+0.1) or 91% of the best performing jobs will be terminated.

### Median stopping policy

[Median stopping](/python/api/azure-ai-ml/azure.ai.ml.sweep.medianstoppingpolicy) is an early termination policy based on running averages of primary metrics reported by the jobs. This policy computes running averages across all training jobs and stops jobs whose primary metric value is worse than the median of the averages.

This policy takes the following configuration parameters:
* `evaluation_interval`: the frequency for applying the policy (optional parameter).
* `delay_evaluation`: delays the first policy evaluation for a specified number of intervals (optional parameter).


```Python
from azure.ai.ml.sweep import MedianStoppingPolicy
sweep_job.early_termination = MedianStoppingPolicy(delay_evaluation = 5, evaluation_interval = 1)
```
References: 
[MedianStoppingPolicy](/python/api/azure-ai-ml/azure.ai.ml.sweep.medianstoppingpolicy)

In this example, the early termination policy is applied at every interval starting at evaluation interval 5. A job is stopped at interval 5 if its best primary metric is worse than the median of the running averages over intervals 1:5 across all training jobs.

### Truncation selection policy

[Truncation selection](/python/api/azure-ai-ml/azure.ai.ml.sweep.truncationselectionpolicy) cancels a percentage of lowest performing jobs at each evaluation interval. Jobs are compared using the primary metric. 

This policy takes the following configuration parameters:

* `truncation_percentage`: the percentage of lowest performing jobs to terminate at each evaluation interval. An integer value between 1 and 99.
* `evaluation_interval`: (optional) the frequency for applying the policy
* `delay_evaluation`: (optional) delays the first policy evaluation for a specified number of intervals
* `exclude_finished_jobs`: specifies whether to exclude finished jobs when applying the policy


```Python
from azure.ai.ml.sweep import TruncationSelectionPolicy
sweep_job.early_termination = TruncationSelectionPolicy(evaluation_interval=1, truncation_percentage=20, delay_evaluation=5, exclude_finished_jobs=true)
```
References: 
[TruncationSelectionPolicy](/python/api/azure-ai-ml/azure.ai.ml.sweep.truncationselectionpolicy)

In this example, the early termination policy is applied at every interval starting at evaluation interval 5. A job terminates at interval 5 if its performance at interval 5 is in the lowest 20% of performance of all jobs at interval 5 and will exclude finished jobs when applying the policy.

### No termination policy (default)

If no policy is specified, the hyperparameter tuning service lets all training jobs execute to completion.

```Python
sweep_job.early_termination = None
```
References: 
[SweepJob](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjob)

### Picking an early termination policy

* For a conservative policy that provides savings without terminating promising jobs, consider a Median Stopping Policy with `evaluation_interval` 1 and `delay_evaluation` 5. These are conservative settings that can provide approximately 25%-35% savings with no loss on primary metric (based on our evaluation data).
* For more aggressive savings, use Bandit Policy with a smaller allowable slack or Truncation Selection Policy with a larger truncation percentage.

## Set limits for your sweep job

Control your resource budget by setting limits for your sweep job.

* `max_total_trials`: Maximum number of trial jobs. Must be an integer between 1 and 1000.
* `max_concurrent_trials`: (optional) Maximum number of trial jobs that can run concurrently. If not specified, max_total_trials number of jobs launch in parallel. If specified, must be an integer between 1 and 1000.
* `timeout`: Maximum time in seconds the entire sweep job is allowed to run. Once this limit is reached the system cancels the sweep job, including all its trials.
* `trial_timeout`: Maximum time in seconds each trial job is allowed to run. Once this limit is reached the system cancels the trial. 

>[!NOTE] 
>If both max_total_trials and timeout are specified, the hyperparameter tuning experiment terminates when the first of these two thresholds is reached.

>[!NOTE] 
>The number of concurrent trial jobs is gated on the resources available in the specified compute target. Ensure that the compute target has the available resources for the desired concurrency.

```Python
sweep_job.set_limits(max_total_trials=20, max_concurrent_trials=4, timeout=1200)
```
References: 
[SweepJob.set_limits](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjob#azure_ai_ml_sweep_SweepJob_set_limits)

This code configures the hyperparameter tuning experiment to use a maximum of 20 total trial jobs, running four trial jobs at a time with a timeout of 1,200 seconds for the entire sweep job.

## Configure hyperparameter tuning experiment

To configure your hyperparameter tuning experiment, provide the following:
* The defined hyperparameter search space
* Your sampling algorithm
* Your early termination policy
* Your objective
* Resource limits
* CommandJob or CommandComponent
* SweepJob

SweepJob can run a hyperparameter sweep on the Command or Command Component. 

> [!NOTE]
>The compute target used in `sweep_job` must have enough resources to satisfy your concurrency level. For more information on compute targets, see [Compute targets](concept-compute-target.md).

Configure your hyperparameter tuning experiment:

```Python
from azure.ai.ml import MLClient
from azure.ai.ml import command, Input
from azure.ai.ml.sweep import Choice, Uniform, MedianStoppingPolicy
from azure.identity import DefaultAzureCredential

# Create your base command job
command_job = command(
    code="./src",
    command="python main.py --iris-csv ${{inputs.iris_csv}} --learning-rate ${{inputs.learning_rate}} --boosting ${{inputs.boosting}}",
    environment="AzureML-lightgbm-3.2-ubuntu18.04-py37-cpu@latest",
    inputs={
        "iris_csv": Input(
            type="uri_file",
            path="https://azuremlexamples.blob.core.windows.net/datasets/iris.csv",
        ),
        "learning_rate": 0.9,
        "boosting": "gbdt",
    },
    compute="cpu-cluster",
)

# Override your inputs with parameter expressions
command_job_for_sweep = command_job(
    learning_rate=Uniform(min_value=0.01, max_value=0.9),
    boosting=Choice(values=["gbdt", "dart"]),
)

# Call sweep() on your command job to sweep over your parameter expressions
sweep_job = command_job_for_sweep.sweep(
    compute="cpu-cluster",
    sampling_algorithm="random",
    primary_metric="test-multi_logloss",
    goal="Minimize",
)

# Specify your experiment details
sweep_job.display_name = "lightgbm-iris-sweep-example"
sweep_job.experiment_name = "lightgbm-iris-sweep-example"
sweep_job.description = "Run a hyperparameter sweep job for LightGBM on Iris dataset."

# Define the limits for this sweep
sweep_job.set_limits(max_total_trials=20, max_concurrent_trials=10, timeout=7200)

# Set early stopping on this one
sweep_job.early_termination = MedianStoppingPolicy(
    delay_evaluation=5, evaluation_interval=2
)
```
References: 
- [MLClient](/python/api/azure-ai-ml/azure.ai.ml.mlclient) 
- [command](/python/api/azure-ai-ml/azure.ai.ml.dsl#azure_ai_ml_dsl_command)
- [Input](/python/api/azure-ai-ml/azure.ai.ml.input)
- [Choice](/python/api/azure-ai-ml/azure.ai.ml.sweep.choice)
- [Uniform](/python/api/azure-ai-ml/azure.ai.ml.sweep.uniform)
- [MedianStoppingPolicy](/python/api/azure-ai-ml/azure.ai.ml.sweep.medianstoppingpolicy)
- [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

The `command_job` is invoked as a function so you can apply parameter expressions. The `sweep` function is configured with `trial`, sampling algorithm, objective, limits, and compute. The snippet comes from the sample notebook [Run hyperparameter sweep on a Command or CommandComponent](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb). In this sample, `learning_rate` and `boosting` are tuned. Early stopping is driven by a `MedianStoppingPolicy`, which stops a job whose primary metric is worse than the median of running averages across all jobs (see [MedianStoppingPolicy reference](/python/api/azure-ai-ml/azure.ai.ml.sweep.medianstoppingpolicy)).

To see how the parameter values are received, parsed, and passed to the training script to be tuned, refer to this [code sample](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/lightgbm/iris/src/main.py)

> [!Important]
> Every hyperparameter sweep job restarts the training from scratch, including rebuilding the model and _all the data loaders_. You can minimize 
> this cost by using an Azure Machine Learning pipeline or manual process to do as much data preparation as possible prior to your training jobs. 

## Submit hyperparameter tuning experiment

After you define your hyperparameter tuning configuration, [submit the job](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure-ai-ml-mlclient-create-or-update):

```Python
# submit the sweep
returned_sweep_job = ml_client.create_or_update(sweep_job)
# get a URL for the status of the job
returned_sweep_job.services["Studio"].endpoint
```
References: 
- [MLClient.create_or_update](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure_ai_ml_mlclient_create_or_update) 
- [SweepJob](/python/api/azure-ai-ml/azure.ai.ml.sweep.sweepjob)

## Visualize hyperparameter tuning jobs

Visualize hyperparameter tuning jobs in [Azure Machine Learning studio](https://ml.azure.com). For details, see [View job records in the studio](how-to-log-view-metrics.md#view-the-experiment-in-the-web-portal).

- **Metrics chart**: This visualization tracks the metrics logged for each hyperdrive child job over the duration of hyperparameter tuning. Each line represents a child job, and each point measures the primary metric value at that iteration of runtime.  

    :::image type="content" source="media/how-to-tune-hyperparameters/hyperparameter-tuning-metrics.png" alt-text="Hyperparameter tuning metrics chart":::

- **Parallel Coordinates Chart**: This visualization shows the correlation between primary metric performance and individual hyperparameter values. The chart is interactive via movement of axes (select and drag by the axis label), and by highlighting values across a single axis (select and drag vertically along a single axis to highlight a range of desired values). The parallel coordinates chart includes an axis on the rightmost portion of the chart that plots the best metric value corresponding to the hyperparameters set for that job instance. This axis is provided in order to project the chart gradient legend onto the data in a more readable fashion.

    :::image type="content" source="media/how-to-tune-hyperparameters/hyperparameter-tuning-parallel-coordinates.png" alt-text="Hyperparameter tuning parallel coordinates chart":::

- **2-Dimensional Scatter Chart**: This visualization shows the correlation between any two individual hyperparameters along with their associated primary metric value.

    :::image type="content" source="media/how-to-tune-hyperparameters/hyperparameter-tuning-2-dimensional-scatter.png" alt-text="Hyparameter tuning 2-dimensional scatter chart":::

- **3-Dimensional Scatter Chart**: This visualization is the same as 2D but allows for three hyperparameter dimensions of correlation with the primary metric value. You can also select and drag to reorient the chart to view different correlations in 3D space.

    :::image type="content" source="media/how-to-tune-hyperparameters/hyperparameter-tuning-3-dimensional-scatter.png" alt-text="Hyparameter tuning 3-dimensional scatter chart":::


## Find the best trial job

After all tuning jobs complete, retrieve the best trial outputs:

```Python
# Download best trial model output
ml_client.jobs.download(returned_sweep_job.name, output_name="model")
```
References:
- [MLClient.jobs](/python/api/azure-ai-ml/azure.ai.ml.mlclient#azure_ai_ml_mlclient_jobs)

You can use the CLI to download all default and named outputs of the best trial job and logs of the sweep job.
```
az ml job download --name <sweep-job> --all
```

Optionally, download only the best trial output:
```
az ml job download --name <sweep-job> --output-name model
```   
    
## References

- [Hyperparameter tuning example](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/single-step/lightgbm/iris/src/main.py)
- [CLI (v2) sweep job YAML schema](reference-yaml-job-sweep.md#parameter-expressions)

## Next steps
* [Track an experiment](how-to-log-view-metrics.md)
* [Deploy a trained model](how-to-deploy-online-endpoints.md)
