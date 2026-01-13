---
title: Track Experiments and Models by Using MLflow
titleSuffix: Azure Machine Learning
description:  Learn how to use MLflow to log metrics and artifacts from machine learning experiments and runs in Azure Machine Learning workspaces.
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.service: azure-machine-learning
ms.subservice: mlops
ms.date: 10/17/2025
ms.topic: how-to
ms.custom: mlflow, devx-track-azurecli, cliv2, devplatv2, update-code, FY25Q1-Linter
ms.devlang: azurecli
#Customer intent: As a data scientist, I want to know how to track my machine learning experiments and models with MLflow so I can use MLflow for tracking in Azure Machine Learning.
---

# Track experiments and models by using MLflow

*Tracking* is the process of saving relevant information about experiments. In this article, you learn how to use MLflow for tracking experiments and runs in Azure Machine Learning workspaces.

Some methods available in the MLflow API might not be available when you're using Azure Machine Learning. For details about supported and unsupported operations, see [Support matrix for querying runs and experiments](how-to-track-experiments-mlflow.md#support-matrix-for-querying-runs-and-experiments). You can also learn about supported MLflow functionalities in Azure Machine Learning from the article [MLflow and Azure Machine Learning](concept-mlflow.md).

> [!NOTE] 
> - To track experiments running on Azure Databricks, see [Track Azure Databricks machine learning experiments with MLflow and Azure Machine Learning](how-to-use-mlflow-azure-databricks.md).
> - To track experiments running on Azure Synapse Analytics, see [Track Azure Synapse Analytics ML experiments with MLflow and Azure Machine Learning](how-to-use-mlflow-azure-synapse.md).

## Prerequisites

- Have an Azure subscription and the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

- To run Azure CLI and Python commands, install [Azure CLI v2](how-to-configure-cli.md) and the [Azure Machine Learning SDK v2 for Python](/python/api/overview/azure/ai-ml-readme). The `ml` extension for Azure CLI installs automatically the first time you run an Azure Machine Learning CLI command.

[!INCLUDE [mlflow-prereqs](includes/machine-learning-mlflow-prereqs.md)]

## Configure the experiment

MLflow organizes information in experiments and runs. Runs are called *jobs* in Azure Machine Learning. By default, runs log to an automatically created experiment named **Default**, but you can configure which experiment to track.

# [Notebooks](#tab/interactive)

For interactive training, such as in a Jupyter notebook, use the MLflow command `mlflow.set_experiment()`. For example, the following code snippet configures an experiment:

```python
experiment_name = 'hello-world-example'
mlflow.set_experiment(experiment_name)
```

# [Jobs](#tab/jobs)

To submit jobs by using the Azure Machine Learning CLI or SDK, set the experiment name by using the `experiment_name` property of the job. You don't need to configure the experiment name in your training script.

:::code language="yaml" source="~/azureml-examples-main/cli/jobs/basics/hello-world-org.yml" highlight="8" range="1-9":::

---

## Configure the run

Azure Machine Learning tracks training jobs in what MLflow calls *runs*. Use runs to capture all the processing that your job performs.

# [Notebooks](#tab/interactive)

When you work interactively, MLflow starts tracking your training routine as soon as you log information that requires an active run. For instance, if MLflow's autologging functionality is enabled, MLflow tracking starts when you log a metric or parameter, or start a training cycle.

However, it's usually helpful to start the run explicitly, especially if you want to capture the total time for your experiment in the **Duration** field. To start the run explicitly, use `mlflow.start_run()`.

Whether you start the run manually or not, you eventually need to stop the run, so that MLflow knows that your experiment run is done and can mark the run's status as **Completed**. To stop a run, use `mlflow.end_run()`.

The following code starts a run manually and ends it at the end of the notebook:

```python
mlflow.start_run()

# Your code

mlflow.end_run()
```

It's best to start runs manually so you don't forget to end them. You can use the context manager paradigm to help you remember to end the run.

```python
with mlflow.start_run() as run:
    # Your code
```

When you start a new run by using `mlflow.start_run()`, it can be useful to specify the `run_name` parameter, which later translates to the name of the run in the Azure Machine Learning user interface. This practice helps you identify the run more quickly.

```python
with mlflow.start_run(run_name="hello-world-example") as run:
    # Your code
```

# [Jobs](#tab/jobs)

Azure Machine Learning jobs allow you to submit long-running training or inference routines as isolated and reproducible executions.

### Create a training routine that has tracking

When you work with jobs, you typically include all your training logic as files in a folder, such as *src*. One of the files is a Python file with your training code entry point.

In your training routine, you can use the MLflow SDK to track any metric, parameter, artifact, or model. For examples, see [Log metrics, parameters, and files with MLflow](how-to-log-view-metrics.md).

The following example shows a *hello_world.py* training routine that adds logging:

:::code language="python" source="~/azureml-examples-main/cli/jobs/basics/src/hello-mlflow.py" highlight="9-10,12":::

The previous code example doesn't use `mlflow.start_run()`. If this line is used, MLflow reuses the current active run. Therefore, you don't need to remove `mlflow.start_run()` if you migrate code to Azure Machine Learning.

### Ensure that your job's environment has MLflow installed

All Azure Machine Learning curated environments already have MLflow installed. However, if you use a custom environment, create a *conda.yml* file that has the dependencies you need, and reference the environment in your job.

:::code language="yaml" source="~/azureml-examples-main/sdk/python/using-mlflow/deploy/environment/conda.yaml" highlight="7-8" range="1-12":::

### Configure the job name

Use the Azure Machine Learning jobs parameter `display_name` to configure the name of the run.

1. Use the `display_name` property to configure the job.

    # [Azure CLI](#tab/cli)

    To configure the job, create a YAML file with your job definition in a *job.yml* file outside of the *src* directory.

    :::code language="yaml" source="~/azureml-examples-main/cli/jobs/basics/hello-world-org.yml" highlight="7" range="1-9":::

    # [Python SDK](#tab/python)

    ```python
    from azure.ai.ml import command, Environment

    command_job = command(
        code="src",
        command="echo "hello world",
        environment=Environment(image="library/python:latest"),
        compute="cpu-cluster",
        display_name="hello-world-example"
    )
    ```

1. Be sure that you don't use `mlflow.start_run(run_name="")` in your training routine.

### Submit the job

1. The workspace is the top-level resource for Azure Machine Learning, providing a centralized place to work with all the Azure Machine Learning artifacts you create. Connect to the Azure Machine Learning workspace.

    # [Azure CLI](#tab/cli)
   
    ```azurecli
    az account set --subscription <subscription>
    az configure --defaults workspace=<workspace> group=<resource-group> location=<location>
    ```
   
    # [Python SDK](#tab/python)
   
    1. Import the required libraries:
   
        ```python
        from azure.ai.ml import MLClient
        from azure.identity import DefaultAzureCredential
        ```
   
    2. Configure workspace details and get a handle to the workspace:
   
        ```python
        subscription_id = "<subscription>"
        resource_group = "<resource-group>"
        workspace = "<workspace>"
        
        ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
        ```

1. Open a terminal and use the following code to submit the job. Jobs that use MLflow and run on Azure Machine Learning automatically log any tracking information to the workspace.

   # [Azure CLI](#tab/cli)

   Use the Azure Machine Learning CLI [to submit your job](how-to-train-model.md).

   ```azurecli
   az ml job create -f job.yml --web
   ```

   # [Python SDK](#tab/python)

   Use the Python SDK [to submit your job](how-to-train-model.md).

   ```python
   returned_job = ml_client.jobs.create_or_update(command_job)
   returned_job.studio_url
   ```

1. Monitor job progress in Azure Machine Learning studio.

---

## Enable MLflow autologging

You can [log metrics, parameters, and files with MLflow](how-to-log-view-metrics.md) manually, and you can also rely on MLflow's automatic logging capability. Each machine learning framework supported by MLflow determines what to track automatically.

To enable [automatic logging](https://mlflow.org/docs/latest/tracking.html#automatic-logging), insert the following code before your training code:

```python
mlflow.autolog()
```

## View metrics and artifacts in your workspace

The metrics and artifacts from MLflow logging are tracked in your workspace. You can view and access them in Azure Machine Learning studio or access them programmatically by using the MLflow SDK.

To view metrics and artifacts in the studio:

1. On the **Jobs** page in your workspace, select the experiment name.
1. On the experiment details page, select the **Metrics** tab.
1. Select logged metrics to render charts on the right side of the page. You can customize the charts by applying smoothing, changing the color, or plotting multiple metrics on a single graph. You can also resize and rearrange the layout.
1. After you create the view that you want, save it for future use and share it with your teammates by using a direct link.

   :::image type="content" source="media/how-to-log-view-metrics/metrics.png" alt-text="Screenshot of the metrics view that shows the list of metrics and the charts created from the metrics." lightbox="media/how-to-log-view-metrics/metrics.png"::: 

To access or query metrics, parameters, and artifacts programmatically by using the MLflow SDK, use [mlflow.get_run()](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.get_run).

```python
import mlflow

run = mlflow.get_run("<RUN_ID>")

metrics = run.data.metrics
params = run.data.params
tags = run.data.tags

print(metrics, params, tags)
```

> [!TIP]
> The preceding example returns only the last value of a given metric. To retrieve all the values of a given metric, use the `mlflow.get_metric_history` method. For more information on retrieving metrics values, see [Get params and metrics from a run](how-to-track-experiments-mlflow.md#get-params-and-metrics-from-a-run).

To download artifacts you logged, such as files and models, use [mlflow.artifacts.download_artifacts()](https://www.mlflow.org/docs/latest/python_api/mlflow.artifacts.html#mlflow.artifacts.download_artifacts).

```python
mlflow.artifacts.download_artifacts(run_id="<RUN_ID>", artifact_path="helloworld.txt")
```

For more information about how to retrieve or compare information from experiments and runs in Azure Machine Learning by using MLflow, see [Query and compare experiments and runs with MLflow](how-to-track-experiments-mlflow.md).

## Related content

* [Deploy MLflow models](how-to-deploy-mlflow-models.md)
* [Manage models with MLflow](how-to-manage-models-mlflow.md)
* [Using MLflow (Jupyter Notebooks)](https://github.com/Azure/azureml-examples/tree/main/sdk/python/using-mlflow)
