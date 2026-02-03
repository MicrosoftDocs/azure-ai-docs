---
title: Set up AutoML with Python (v2)
titleSuffix: Azure Machine Learning
description: Learn how to set up an AutoML training run for tabular data with the Azure Machine Learning CLI and Python SDK v2.
ms.author: scottpolly
author: s-polly
ms.reviewer: sooryar
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: automl
ms.date: 08/29/2025
ms.topic: how-to
ms.custom: devx-track-python, automl, sdkv2
show_latex: true
#customer intent: As a data scientist, I want to use the Azure Machine Learning SDK to set up AutoML.
---

# Set up AutoML training for tabular data with the Azure Machine Learning CLI and Python SDK

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In this article, learn how to set up an AutoML training job with the [Azure Machine Learning Python SDK v2](/python/api/overview/azure/ml/intro). AutoML picks an algorithm and hyperparameters for you and generates a model ready for deployment. This article provides details of the various options that you can use to configure AutoML experiments.

If you prefer a no-code experience, you can also [set up no-code AutoML training for tabular data with the studio UI](how-to-use-automated-ml-for-ml-models.md).

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure Machine Learning workspace. If you don't have one, see [Create resources to get started](quickstart-create-resources.md).

# [Python SDK](#tab/python)

To use the **SDK** information, install the Azure Machine Learning [SDK v2 for Python](https://aka.ms/sdk-v2-install).

You can install the SDK in two ways:

- Create a compute instance, which already has the latest Azure Machine Learning Python SDK and is configured for ML workflows. For more information, see [Create an Azure Machine Learning compute instance](how-to-create-compute-instance.md).
- Install the SDK on your local machine.

# [Azure CLI](#tab/azurecli)

To use the **CLI** information, install the [Azure CLI and extension for machine learning](how-to-configure-cli.md).

---

## Set up your workspace 

To connect to a workspace, you need to provide a subscription, resource group, and workspace.

# [Python SDK](#tab/python)

The workspace details go into the `MLClient` from `azure.ai.ml` to connect to your Azure Machine Learning workspace.

The following example uses the default Azure authentication with the default workspace configuration or configuration from a `config.json` file in the folder structure. If it finds no `config.json`, you need to manually provide the subscription ID, resource group, and workspace when you create the `MLClient`.

```Python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient

credential = DefaultAzureCredential()
ml_client = None
try:
    ml_client = MLClient.from_config(credential)
except Exception as ex:
    print(ex)
    # Enter details of your Azure Machine Learning workspace
    subscription_id = "<SUBSCRIPTION_ID>"
    resource_group = "<RESOURCE_GROUP>"
    workspace = "<AZUREML_WORKSPACE_NAME>"
    ml_client = MLClient(credential, subscription_id, resource_group, workspace)

```

# [Azure CLI](#tab/azurecli)

In the CLI, start by signing into your Azure account. If your account is associated with multiple subscriptions, you need to [set the subscription](/cli/azure/manage-azure-subscriptions-azure-cli#change-the-active-subscription).

```azurecli
az login
```

You can also set default values to avoid typing these values into every CLI command:

```azurecli
az configure --defaults group=<RESOURCE_GROUP> workspace=<AZUREML_WORKSPACE_NAME> location=<LOCATION>
```

For more information, see [CLI setup](how-to-configure-cli.md#set-up).

---

<a name="data-source-and-format"></a>

## Specify data source and format

To provide training data in SDK v2, you need to upload it to the cloud through an *MLTable*.

Requirements for loading data into an MLTable:

- Data must be in tabular form.
- The value to predict, *target column*, must be in the data.

Training data must be accessible from the remote compute. AutoML v2 (Python SDK and CLI/YAML) accepts MLTable data assets (v2). For backwards compatibility, it also supports v1 Tabular Datasets from v1, a registered Tabular Dataset, through the same input dataset properties. We recommend that you use MLTable, available in v2. In this example, the data is stored at the local path, *./train_data/bank_marketing_train_data.csv*.

# [Python SDK](#tab/python)

You can create an MLTable using the [mltable Python SDK](/python/api/mltable/mltable) as in the following example:

```python
import mltable

paths = [
    {'file': './train_data/bank_marketing_train_data.csv'}
]

train_table = mltable.from_delimited_files(paths)
train_table.save('./train_data')
```

This code creates a new file, *./train_data/MLTable*, which contains the file format and loading instructions.

# [Azure CLI](#tab/azurecli)

The following YAML code defines an MLTable that is placed in a local folder or a remote folder in the cloud, along with the data file. The data file is a *.csv* or Parquet file. In this case, write the YAML text to the local file, *./train_data/MLTable*.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/MLTable.schema.json

paths:
  - file: ./bank_marketing_train_data.csv
transformations:
  - read_delimited:
        delimiter: ','
        encoding: 'ascii'
```

---

Now the *./train_data* folder has the MLTable definition file plus the data file, *bank_marketing_train_data.csv*.

For more information on MLTable, see [Working with tables in Azure Machine Learning](how-to-mltable.md).

### Training, validation, and test data

You can specify separate *training data and validation data sets*. You must provide training data to the `training_data` parameter in the factory function of your AutoML job.

If you don't explicitly specify a `validation_data` or `n_cross_validation` parameter, AutoML applies default techniques to determine how to do validation. This determination depends on the number of rows in the dataset assigned to your `training_data` parameter.

| Training&nbsp;data&nbsp;size | Validation technique |
|:---|:-----|
| **Larger&nbsp;than&nbsp;20,000&nbsp;rows** | AutoML applies training and validation data split. The default takes 10% of the initial training data set as the validation set. AutoML then uses that validation set for metrics calculation. |
| **Smaller&nbsp;than&nbsp;or&nbsp;equal&nbsp;to&nbsp;20,000&nbsp;rows** | AutoML applies cross-validation approach. The default number of folds depends on the number of rows. <br> **If the dataset is fewer than 1,000 rows**, AutoML uses ten folds. <br> **If the rows are equal to or between 1,000 and 20,000**, AutoML uses three folds. |

## Compute to run experiment

AutoML jobs with the Python SDK v2 (or CLI v2) are currently only supported on Azure Machine Learning remote compute cluster or compute instance. For more information about creating compute with the Python SDKv2 or CLIv2, see [train models with Azure Machine Learning CLI, SDK, and REST API](./how-to-train-model.md).

## Configure your experiment settings

You can use several options to configure your AutoML experiment. These configuration parameters are set in your task method. You can also set job training settings and [exit criteria](#exit-criteria) with the `training` and `limits` settings.

The following example shows the required parameters for a classification task that specifies accuracy as the [primary metric](#primary-metric) and five cross-validation folds.

# [Python SDK](#tab/python)

```python
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import automl, Input

# note that this is a code snippet -- you might have to modify the variable values to run it successfully

# make an Input object for the training data
my_training_data_input = Input(
    type=AssetTypes.MLTABLE, path="./data/training-mltable-folder"
)

# configure the classification job
classification_job = automl.classification(
    compute=my_compute_name,
    experiment_name=my_exp_name,
    training_data=my_training_data_input,
    target_column_name="y",
    primary_metric="accuracy",
    n_cross_validations=5,
    enable_model_explainability=True,
    tags={"my_custom_tag": "My custom value"}
)

# Limits are all optional
classification_job.set_limits(
    timeout_minutes=600, 
    trial_timeout_minutes=20, 
    max_trials=5,
    enable_early_termination=True,
)

# Training properties are optional
classification_job.set_training(
    blocked_training_algorithms=["logistic_regression"], 
    enable_onnx_compatible_models=True
)
```

# [Azure CLI](#tab/azurecli)

```yml
$schema: https://azuremlsdk2.blob.core.windows.net/preview/0.0.1/autoMLJob.schema.json
type: automl

experiment_name: <my_exp_name>
description: A classification AutoML job
task: classification

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:<my_compute_name>
primary_metric: accuracy  
target_column_name: y
n_cross_validations: 5
enable_model_explainability: True

tags:
    <my_custom_tag>: <My custom value>

limits:
    timeout_minutes: 600 
    trial_timeout_minutes: 20 
    max_trials: 5
    enable_early_termination: True

training:
    blocked_training_algorithms: ["logistic_regression"] 
    enable_onnx_compatible_models: True
```

---

### Select your machine learning task type

Before you can submit your AutoML job, determine the kind of machine learning problem that you want to solve. This problem determines which function your job uses and what model algorithms it applies.

AutoML supports different task types:

- Tabular data based tasks

  - classification
  - regression
  - forecasting

- Computer vision tasks, including

  - Image Classification
  - Object Detection

- Natural language processing tasks, including

  - Text classification
  - Entity Recognition

 For more information, see [task types](concept-automated-ml.md#when-to-use-automl-classification-regression-forecasting-computer-vision-and-nlp). For more information on setting up forecasting jobs, see [set up AutoML to train a time-series forecasting model](how-to-auto-train-forecast.md).

### Supported algorithms

AutoML tries different models and algorithms during the automation and tuning process. As a user, you don't need to specify the algorithm.

The task method determines the list of algorithms or models to apply. To further modify iterations with the available models to include or exclude, use the `allowed_training_algorithms` or `blocked_training_algorithms` parameters in the `training` configuration of the job.

In the following table, explore the supported algorithms per machine learning task.

| Classification | Regression | Time Series Forecasting |
|:-- |:-- |:--|
| [Logistic Regression](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-logisticregression)* | [Elastic Net](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-elasticnet)* | [AutoARIMA](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.forecasting#azureml-train-automl-constants-supportedmodels-forecasting-autoarima) |
| [Light GBM](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-lightgbmclassifier)* | [Light GBM](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-lightgbmregressor)* | [Prophet](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-automl-core-shared-constants-supportedmodels-forecasting-prophet) |
| [Gradient Boosting](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-gradientboosting)* | [Gradient Boosting](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-gradientboostingregressor)* | [Elastic Net](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net) |
| [Decision Tree](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-decisiontree)* |[Decision Tree](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-decisiontreeregressor)* |[Light GBM](https://lightgbm.readthedocs.io/en/latest/index.html) |
| [K Nearest Neighbors](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-knearestneighborsclassifier)* |[K Nearest Neighbors](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-knearestneighborsregressor)* | K Nearest Neighbors |
| [Linear SVC](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-linearsupportvectormachine)* |[LARS Lasso](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-lassolars)* | [Decision Tree](https://scikit-learn.org/stable/modules/tree.html#regression) |
| [Support Vector Classification (SVC)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-supportvectormachine)* |[Stochastic Gradient Descent (SGD)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-sgdregressor)* | [Arimax](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-automl-core-shared-constants-supportedmodels-forecasting-arimax) |
| [Random Forest](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-randomforest)* | [Random Forest](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-randomforestregressor) | [LARS Lasso](https://scikit-learn.org/stable/modules/linear_model.html#lars-lasso) |
| [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* | [Extremely Randomized Trees](https://scikit-learn.org/stable/modules/ensemble.html#extremely-randomized-trees)* |
| [Xgboost](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-xgboostclassifier)* |[Xgboost](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.regression#azureml-train-automl-constants-supportedmodels-regression-xgboostregressor)* | [Random Forest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests) |
| [Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html#bernoulli-naive-bayes)* | [Xgboost](https://xgboost.readthedocs.io/en/latest/parameter.html)  | [TCNForecaster](concept-automl-forecasting-deep-learning.md#introduction-to-tcnforecaster) |
| [Stochastic Gradient Descent (SGD)](/python/api/azureml-train-automl-client/azureml.train.automl.constants.supportedmodels.classification#azureml-train-automl-constants-supportedmodels-classification-sgdclassifier)* |[Stochastic Gradient Descent (SGD)](https://scikit-learn.org/stable/modules/sgd.html#regression) | [Gradient Boosting](https://scikit-learn.org/stable/modules/ensemble.html#regression) |
||| [ExponentialSmoothing](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-automl-core-shared-constants-supportedmodels-forecasting-exponentialsmoothing) |
||| [SeasonalNaive](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-train-automl-constants-supportedmodels-forecasting-seasonalnaive) |
||| [Average](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-train-automl-constants-supportedmodels-forecasting-average) |
||| [Naive](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-train-automl-constants-supportedmodels-forecasting-naive) |
||| [SeasonalAverage](/python/api/azureml-automl-core/azureml.automl.core.shared.constants.supportedmodels.forecasting#azureml-train-automl-constants-supportedmodels-forecasting-seasonalaverage) |

With other algorithms:

- [Image Classification Multi-class Algorithms](how-to-auto-train-image-models.md#supported-model-architectures)
- [Image Classification Multi-label Algorithms](how-to-auto-train-image-models.md#supported-model-architectures)
- [Image Object Detection Algorithms](how-to-auto-train-image-models.md#supported-model-architectures)
- [NLP Text Classification Multi-label Algorithms](how-to-auto-train-nlp-models.md#language-settings)
- [NLP Text Named Entity Recognition (NER) Algorithms](how-to-auto-train-nlp-models.md#language-settings)

For example notebooks of each task type, see [automl-standalone-jobs](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs).

### Primary metric

The `primary_metric` parameter determines the metric to use during model training for optimization. The task type that you choose determines the metrics that you can select.

Choosing a primary metric for AutoML to optimize depends on many factors. We recommend your primary consideration be to choose a metric that best represents your business needs. Then consider if the metric is suitable for your dataset profile, including data size, range, and class distribution. The following sections summarize the recommended primary metrics based on task type and business scenario.

To learn about the specific definitions of these metrics, see [evaluate AutoML experiment results](how-to-understand-automated-ml.md).

#### Metrics for classification multi-class scenarios

These metrics apply for all classification scenarios, including tabular data, images or computer-vision, and natural language processing text (NLP-Text).

Threshold-dependent metrics, like `accuracy`, `recall_score_weighted`, `norm_macro_recall`, and `precision_score_weighted` might not optimize as well for datasets that are small, have large class skew (class imbalance), or when the expected metric value is very close to 0.0 or 1.0. In those cases, `AUC_weighted` can be a better choice for the primary metric. After AutoML completes, you can choose the winning model based on the metric best suited to your business needs.

| Metric | Example use cases |
| ------ | ------- |
| `accuracy` | Image classification, Sentiment analysis, Churn prediction |
| `AUC_weighted` | Fraud detection, Image classification, Anomaly detection/spam detection |
| `average_precision_score_weighted` | Sentiment analysis |
| `norm_macro_recall` | Churn prediction |
| `precision_score_weighted` |  |

#### Metrics for classification multi-label scenarios

For text classification multi-label, currently 'Accuracy' is the only primary metric supported.

For image classification multi-label, the primary metrics supported are defined in the `ClassificationMultilabelPrimaryMetrics` enum.

#### Metrics for NLP Text Named Entity Recognition scenarios

For NLP text Named Entity Recognition (NER), currently 'Accuracy' is the only primary metric supported.

#### Metrics for regression scenarios

`r2_score`, `normalized_mean_absolute_error`, and `normalized_root_mean_squared_error` all try to minimize prediction errors. `r2_score` and `normalized_root_mean_squared_error` both minimize average squared errors while `normalized_mean_absolute_error` minimizes the average absolute value of errors. Absolute value treats errors at all magnitudes alike and squared errors have a much larger penalty for errors with larger absolute values. Depending on whether larger errors should be punished more or not, you can choose to optimize squared error or absolute error.

The main difference between `r2_score` and `normalized_root_mean_squared_error` is how they're normalized and their meanings. `normalized_root_mean_squared_error` is root mean squared error normalized by range and can be interpreted as the average error magnitude for prediction. `r2_score` is mean squared error normalized by an estimate of variance of data. It's the proportion of variation that the model can capture.

> [!NOTE]
> `r2_score` and `normalized_root_mean_squared_error` also behave similarly as primary metrics. If a fixed validation set is applied, these two metrics are optimizing the same target, mean squared error, and are optimized by the same model. When only a training set is available and cross-validation is applied, they would be slightly different as the normalizer for `normalized_root_mean_squared_error` is fixed as the range of training set, but the normalizer for `r2_score` would vary for every fold as it's the variance for each fold.

If the rank, instead of the exact value, is of interest, `spearman_correlation` can be a better choice. It measures the rank correlation between real values and predictions.

AutoML doesn't currently support any primary metrics that measure *relative* difference between predictions and observations. The metrics `r2_score`, `normalized_mean_absolute_error`, and `normalized_root_mean_squared_error` are all measures of absolute difference. For example, if a prediction differs from an observation by 10 units, these metrics compute the same value if the observation is 20 units or 20,000 units. In contrast, a percentage difference, which is a relative measure, gives errors of 50% and 0.05%, respectively. To optimize for relative difference, you can run AutoML with a supported primary metric and then select the model with the best `mean_absolute_percentage_error` or `root_mean_squared_log_error`. These metrics are undefined when any observation values are zero, so they might not always be good choices.

| Metric | Example use cases |
|:------ |:------- |
| `spearman_correlation` | |
| `normalized_root_mean_squared_error` | Price prediction (house/product/tip), Review score prediction |
| `r2_score` | Airline delay, Salary estimation, Bug resolution time |
| `normalized_mean_absolute_error` |  |

#### Metrics for Time Series Forecasting scenarios

The recommendations are similar to the recommendations for regression scenarios.

| Metric | Example use cases |
|:------ |:------- |
| `normalized_root_mean_squared_error` | Price prediction (forecasting), Inventory optimization, Demand forecasting |
| `r2_score` | Price prediction (forecasting), Inventory optimization, Demand forecasting |
| `normalized_mean_absolute_error` | |

#### Metrics for Image Object Detection scenarios

For image Object Detection, the primary metrics supported are defined in the `ObjectDetectionPrimaryMetrics` enum.

#### Metrics for Image Instance Segmentation scenarios

For image Instance Segmentation scenarios, the primary metrics supported are defined in the `InstanceSegmentationPrimaryMetrics` enum.

### Data featurization

In every AutoML experiment, your data is automatically transformed to numbers and vectors of numbers. The data is also scaled and normalized to help algorithms that are sensitive to features that are on different scales. These data transformations are called *featurization*.

> [!NOTE]
> AutoML featurization steps, such as feature normalization, handling missing data, and converting text to numeric, become part of the underlying model. When you use the model for predictions, the same featurization steps applied during training are applied to your input data automatically.

When you configure AutoML jobs, you can enable or disable the `featurization` settings.

The following table shows the accepted settings for featurization.

| Featurization Configuration | Description |
|:------------- |:------------- |
| `"mode": 'auto'` | Indicates that, as part of preprocessing, [data guardrails and featurization steps](./v1/how-to-configure-auto-features.md#featurization) are done automatically. This value is the default setting. |
| `"mode": 'off'` | Indicates featurization step shouldn't be done automatically. |
| `"mode":`&nbsp;`'custom'` | Indicates you should use customized featurization step. |

The following code shows how to provide custom featurization in this case for a regression job.

# [Python SDK](#tab/python)

```python
from azure.ai.ml.automl import ColumnTransformer

transformer_params = {
    "imputer": [
        ColumnTransformer(fields=["CACH"], parameters={"strategy": "most_frequent"}),
        ColumnTransformer(fields=["PRP"], parameters={"strategy": "most_frequent"}),
    ],
}
regression_job.set_featurization(
    mode="custom",
    transformer_params=transformer_params,
    blocked_transformers=["LabelEncoding"],
    column_name_and_types={"CHMIN": "Categorical"},
)
```

# [Azure CLI](#tab/azurecli)

```yml
$schema: https://azuremlsdk2.blob.core.windows.net/preview/0.0.1/autoMLJob.schema.json
type: automl

experiment_name: <my_exp_name>
description: A classification AutoML job
task: classification

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:<my_compute_name>
primary_metric: accuracy  
target_column_name: y
n_cross_validations: 5
enable_model_explainability: True

featurization:
    mode: custom
    column_name_and_types:
        CHMIN: Categorical
    blocked_transformers: ["label_encoder"]
    transformer_params:
        imputer:
            - fields: ["CACH", "PRP"]
            parameters:
                strategy: most_frequent

limits:
    # limit settings

training:
    # training settings
```

---

### Exit criteria

You can define a few options in the `set_limits()` function to end your experiment before the job completes.

| Criteria | description |
|:----|:----|
| No&nbsp;criteria | If you don't define any exit parameters, the experiment continues until no further progress is made on your primary metric. |
| `timeout` | Defines how long, in minutes, your experiment should continue to run. If not specified, the default job's total timeout is six days (8,640 minutes). To specify a timeout less than or equal to 1 hour (60 minutes), make sure your dataset's size isn't greater than 10,000,000 (rows times column) or an error results. <br><br> This timeout includes setup, featurization, and training runs but doesn't include the ensembling and model explainability runs at the end of the process since those actions need to happen after all the trials (children jobs) are done. |
| `trial_timeout_minutes` | Maximum time in minutes that each trial (child job) can run for before it terminates. If not specified, AutoML uses a value of 1 month or 43200 minutes. |
| `enable_early_termination`| Whether to end the job if the score isn't improving in the short term. |
| `max_trials` | The maximum number of trials/runs each with a different combination of algorithm and hyper-parameters to try during a job. If not specified, the default is 1,000 trials. If you use `enable_early_termination`, AutoML might use fewer trials. |
| `max_concurrent_trials` | The maximum number of trials (children jobs) that would run in parallel. It's a good practice to match this number with the number of nodes your cluster. |

## Run experiment

Submit the experiment to run and generate a model.

> [!NOTE]
> If you run an experiment with the same configuration settings and primary metric multiple times, you might see variation in each experiment's final metrics score and generated models. The algorithms that AutoML employs have inherent randomness that can cause slight variation in the models output by the experiment and the recommended model's final metrics score, like accuracy. You also might see results with the same model name, but different hyper-parameters used.

> [!WARNING]
> If you have set rules in firewall or Network Security Group over your workspace, verify that required permissions are given to inbound and outbound network traffic as defined in [configure inbound and outbound network traffic](how-to-access-azureml-behind-firewall.md).

With the `MLClient` created in the prerequisites, you can run the following command in the workspace.

# [Python SDK](#tab/python)

```python

# Submit the AutoML job
returned_job = ml_client.jobs.create_or_update(
    classification_job
)  # submit the job to the backend

print(f"Created job: {returned_job}")

# Get a URL for the status of the job
returned_job.services["Studio"].endpoint

```

# [Azure CLI](#tab/azurecli)

In following CLI command, the job YAML configuration is at the path, *./automl-classification-job.yml*:

```azurecli
run_id=$(az ml job create --file automl-classification-job.yml -w <Workspace> -g <Resource Group> --subscription <Subscription>)
```

You can use the stored run ID to return information about the job. The `--web` parameter opens the Azure Machine Learning studio web UI where you can drill into details on the job:

```azurecli
az ml job show -n $run_id --web
```

---

### Multiple child runs on clusters

You can run AutoML experiment child runs on a cluster that is already running another experiment. The timing depends on how many nodes the cluster has and if those nodes are available to run a different experiment.

Each node in the cluster acts as an individual virtual machine (VM) that can accomplish a single training run. For AutoML, this means a child run. If all the nodes are busy, AutoML queues a new experiment. If free nodes are available, the new experiment runs child runs in parallel in the available nodes or virtual machines.

To help manage child runs and when they can run, we recommend that you create a dedicated cluster per experiment, and match the number of `max_concurrent_iterations` of your experiment to the number of nodes in the cluster. This way, you use all the nodes of the cluster at the same time with the number of concurrent child runs and iterations that you want.

Configure `max_concurrent_iterations` in the `limits` configuration. If it isn't configured, then by default only one concurrent child run/iteration is allowed per experiment. For a compute instance, you can set `max_concurrent_trials` to be the same as number of cores on the compute instance virtual machine.

## Explore models and metrics

AutoML offers options for you to monitor and evaluate your training results.

- For definitions and examples of the performance charts and metrics provided for each run, see [evaluate AutoML experiment results](how-to-understand-automated-ml.md).

- To get a featurization summary and understand what features were added to a particular model, see [featurization transparency](./v1/how-to-configure-auto-features.md#featurization-transparency).

From the Azure Machine Learning UI at the model's page, you can also view the hyper-parameters used when you train a particular model and also view and customize the internal model's training code used.

## Register and deploy models

After you test a model and confirm you want to use it in production, you can register it for later use.

> [!TIP]
> For registered models, you can use one-click deployment by using the [Azure Machine Learning studio](https://ml.azure.com). See [deploy your model](how-to-use-automated-ml-for-ml-models.md#deploy-your-model).

## Use AutoML in pipelines

To use AutoML in your machine learning operations workflows, you can add AutoML Job steps to your [Azure Machine Learning Pipelines](./how-to-create-component-pipeline-python.md). This approach allows you to automate your entire workflow by hooking up your data preparation scripts to AutoML. Then register and validate the resulting best model.

This code is a [sample pipeline](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/1h_automl_in_pipeline/automl-classification-bankmarketing-in-pipeline) with an AutoML classification component and a command component that shows the resulting output. The code references the inputs (training and validation data) and the outputs (best model) in different steps.

# [Python SDK](#tab/python)

``` python
# Define pipeline
@pipeline(
    description="AutoML Classification Pipeline",
    )
def automl_classification(
    classification_train_data,
    classification_validation_data
):
    # define the automl classification task with automl function
    classification_node = classification(
        training_data=classification_train_data,
        validation_data=classification_validation_data,
        target_column_name="y",
        primary_metric="accuracy",
        # currently need to specify outputs "mlflow_model" explictly to reference it in following nodes 
        outputs={"best_model": Output(type="mlflow_model")},
    )
    # set limits and training
    classification_node.set_limits(max_trials=1)
    classification_node.set_training(
        enable_stack_ensemble=False,
        enable_vote_ensemble=False
    )

    command_func = command(
        inputs=dict(
            automl_output=Input(type="mlflow_model")
        ),
        command="ls ${{inputs.automl_output}}",
        environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu:latest"
    )
    show_output = command_func(automl_output=classification_node.outputs.best_model)


pipeline_job = automl_classification(
    classification_train_data=Input(path="./training-mltable-folder/", type="mltable"),
    classification_validation_data=Input(path="./validation-mltable-folder/", type="mltable"),
)

# set pipeline level compute
pipeline_job.settings.default_compute = compute_name

# submit the pipeline job
returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name
)
returned_pipeline_job

# ...
# Note that this is a snippet from the bankmarketing example you can find in our examples repo -> https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/1h_automl_in_pipeline/automl-classification-bankmarketing-in-pipeline

```

For more examples on how to include AutoML in your pipelines, see the [examples repository](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/1h_automl_in_pipeline/).

# [Azure CLI](#tab/azurecli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

description: AutoML Classification Pipeline
experiment_name: <exp_name>

# set the default compute for the pipeline steps
settings:
    default_compute: azureml:<my_compute>

# pipeline inputs
inputs:
    classification_train_data:
        type: mltable
        path: "./train_data"
    classification_validation_data:
        type: mltable
        path: "./valid_data"

jobs:
    # Configure the automl training node of the pipeline 
    classification_node:
        type: automl
        task: classification
        primary_metric: accuracy
        target_column_name: y
        training_data: ${{parent.inputs.classification_train_data}}
        validation_data: ${{parent.inputs.classification_validation_data}}
        training:
            max_trials: 1
        limits:
            enable_stack_ensemble: False
            enable_vote_ensemble: False
        outputs:
            best_model:
                type: mlflow_model

    show_output:
        type: command
        inputs:
            automl_output: ${{parent.jobs.classification_node.outputs.best_model}}
        environment: "AzureML-sklearn-0.24-ubuntu18.04-py37-cpu:latest"
        command: >-
            ls ${{inputs.automl_output}}
        
```

Now, you launch the pipeline run using the following command. The pipeline configuration is at the path *./automl-classification-pipeline.yml*.

```azurecli
> run_id=$(az ml job create --file automl-classification-pipeline.yml -w <Workspace> -g <Resource Group> --subscription <Subscription>)
> az ml job show -n $run_id --web
```

---

<a name="automl-at-scale-distributed-training"></a>

## Use AutoML at scale: distributed training

For large data scenarios, AutoML supports distributed training for a limited set of models:

| Distributed algorithm | Supported tasks | Data size limit (approximate) |
|:--|:--|:--  |
| [LightGBM](https://lightgbm.readthedocs.io/en/latest/Parallel-Learning-Guide.html) | Classification, regression | 1 TB |
| [TCNForecaster](concept-automl-forecasting-deep-learning.md#introduction-to-tcnforecaster) | Forecasting | 200 GB |

Distributed training algorithms automatically partition and distribute your data across multiple compute nodes for model training.

> [!NOTE]
> Cross-validation, ensemble models, ONNX support, and code generation are not currently supported in the distributed training mode. Also, AutoML can make choices such as restricting available featurizers and sub-sampling data used for validation, explainability, and model evaluation.

### Distributed training for classification and regression

To use distributed training for classification or regression, set the `training_mode` and `max_nodes` properties of the job object.

| Property | Description |
|:-- |:-- |
| training_mode | Indicates training mode: `distributed` or `non_distributed`. Defaults to `non_distributed`. |
| max_nodes | The number of nodes to use for training by each trial. This setting must be greater than or equal to 4. |

The following code sample shows an example of these settings for a classification job:

# [Python SDK](#tab/python)

```python
from azure.ai.ml.constants import TabularTrainingMode

# Set the training mode to distributed
classification_job.set_training(
    allowed_training_algorithms=["LightGBM"],
    training_mode=TabularTrainingMode.DISTRIBUTED
)

# Distribute training across 4 nodes for each trial
classification_job.set_limits(
    max_nodes=4,
    # other limit settings
)
```

# [Azure CLI](#tab/azurecli)

```yml
# Set the training mode to distributed
training:
    allowed_training_algorithms: ["LightGBM"]
    training_mode: distributed

# Distribute training across 4 nodes for each trial
limits:
    max_nodes: 4
```

---

> [!NOTE]
> Distributed training for classification and regression tasks doesn't currently support multiple concurrent trials. Model trials run sequentially with each trial using `max_nodes` nodes. The `max_concurrent_trials` limit setting is currently ignored.

### Distributed training for forecasting

To learn how distributed training works for forecasting tasks, see [forecasting at scale](concept-automl-forecasting-at-scale.md#distributed-dnn-training-preview). To use distributed training for forecasting, you need to set the `training_mode`, `enable_dnn_training`, `max_nodes`, and optionally the `max_concurrent_trials` properties of the job object.

| Property | Description |
|:-- |:--|
| training_mode | Indicates training mode; `distributed` or `non_distributed`. Defaults to `non_distributed`. |
| enable_dnn_training | Flag to enable deep neural network models. |
| max_concurrent_trials | This value is the maximum number of trial models to train in parallel. Defaults to 1. |
| max_nodes | The total number of nodes to use for training. This setting must be greater than or equal to 2. For forecasting tasks, each trial model is trained using $\text{max}\left(2, \text{floor}( \text{max\_nodes} / \text{max\_concurrent\_trials}) \right)$ nodes. |

The following code sample shows an example of these settings for a forecasting job:

# [Python SDK](#tab/python)

```python
from azure.ai.ml.constants import TabularTrainingMode

# Set the training mode to distributed
forecasting_job.set_training(
    enable_dnn_training=True,
    allowed_training_algorithms=["TCNForecaster"],
    training_mode=TabularTrainingMode.DISTRIBUTED
)

# Distribute training across 4 nodes
# Train 2 trial models in parallel => 2 nodes per trial
forecasting_job.set_limits(
    max_concurrent_trials=2,
    max_nodes=4,
    # other limit settings
)
```

# [Azure CLI](#tab/azurecli)

```yml
# Set the training mode to distributed
training:
    allowed_training_algorithms: ["TCNForecaster"]
    training_mode: distributed

# Distribute training across 4 nodes
# Train 2 trial models in parallel => 2 nodes per trial
limits:
    max_concurrent_trials: 2
    max_nodes: 4
```

---

For samples of full configuration code, see previous sections on [configuration](#configure-your-experiment-settings) and [job submission](#run-experiment).

## Related content

- Learn more about [how and where to deploy a model](./how-to-deploy-online-endpoints.md).
- Learn more about [how to set up AutoML to train a time-series forecasting model](./how-to-auto-train-forecast.md).
