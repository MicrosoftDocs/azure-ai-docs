---
title: Set Up AutoML for Time-Series Forecasting
titleSuffix: Azure Machine Learning
description: Set up Azure Machine Learning automated machine learning (AutoML) to train time-series forecasting models by using the Azure Machine Learning CLI and Python SDK.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.reviewer: sooryar
ms.service: azure-machine-learning
ms.subservice: automl
ms.topic: how-to
ms.custom: automl, sdkv2, build-2023, devx-track-python, devx-track-azurecli
ms.date: 01/23/2026
show_latex: true
#customer intent: As a data scientist, I want to train time-series forecasting models and understand the options available for training them by using AutoML.
---

# Set up AutoML to train a time-series forecasting model by using the SDK and CLI

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

Automated machine learning (AutoML) in Azure Machine Learning uses standard machine learning models together with well-known time-series models to create forecasts. This approach incorporates historical information about the target variable with user-provided features in the input data and automatically engineered features. Model search algorithms help to identify models with the best predictive accuracy. For more information, see [forecasting methodology](concept-automl-forecasting-methods.md) and [model sweeping and selection](concept-automl-forecasting-sweeping.md).

This article describes how to set up AutoML for time-series forecasting with Machine Learning by using the [Azure Machine Learning Python SDK](/python/api/overview/azure/ai-ml-readme) and the [Azure CLI](how-to-configure-cli.md). The process includes preparing data for training and configuring time-series parameters in a [forecasting job (class reference)](/python/api/azure-ai-ml/azure.ai.ml.automl.forecastingjob). You then train, inference, and evaluate models by using components and pipelines.

For a low-code experience, see [Tutorial: Forecast demand with automated machine learning](tutorial-automated-ml-forecast.md). The tutorial provides a time-series forecasting example that uses AutoML in [Azure Machine Learning studio](https://ml.azure.com/).

## Prerequisites

- An Azure Machine Learning workspace. For more information, see [Create workspace resources](quickstart-create-resources.md).
- The ability to start AutoML training jobs. For more information, see [Set up AutoML training for tabular data with the Azure Machine Learning CLI and Python SDK](how-to-configure-auto-train.md).

## Prepare training and validation data

Input data for AutoML forecasting must contain a valid time series in tabular format. Each variable must have its own corresponding column in the data table. AutoML requires at least two columns: a *time* column to represent the time axis and a *target* column for the quantity to forecast. Other columns can serve as predictors. For more information, see [How AutoML uses your data](concept-automl-forecasting-methods.md#how-automl-uses-your-data).

> [!IMPORTANT]
> When you train a model for forecasting future values, ensure that all features used in training can also be used when running predictions for your intended horizon.
>
> Consider a feature for current stock price, which can increase training accuracy. If you forecast with a long horizon, you might not be able to accurately predict future stock values that correspond to future time-series points. This approach can reduce model accuracy.

AutoML forecasting jobs require that your training data is represented as an `MLTable` object. An `MLTable` object specifies a data source and steps for loading the data. For more information and use cases, see [Working with tables](how-to-mltable.md).

For the following example, assume that your training data is contained in a CSV file in a local directory: *./train_data/timeseries_train.csv*.

> [!TIP]
> For complete working examples with sample datasets, see the [AutoML Forecasting Sample Notebooks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs) in the Azure Machine Learning examples repository. The [energy demand forecasting notebook](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs/automl-forecasting-task-energy-demand) includes sample training data you can use to follow along.

# [Python SDK](#tab/python)

You can create an `MLTable` object by using the [mltable Python SDK member](/python/api/mltable/mltable):

```python
import mltable

paths = [
    {'file': './train_data/timeseries_train.csv'}
]

train_table = mltable.from_delimited_files(paths)
train_table.save('./train_data')
```

This code creates a new file, *./train_data/MLTable*, that contains the file format and loading instructions.

To start the training job, define an input data object by using the Python SDK:

```python
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import Input

# Training MLTable defined locally, with local data to be uploaded.
my_training_data_input = Input(
    type=AssetTypes.MLTABLE, path="./train_data"
)
```

# [Azure CLI](#tab/cli)

You can define a new `MLTable` object by copying the following YAML snippet to a new file, *./train_data/MLTable*.

```yml
$schema: https://azuremlschemas.azureedge.net/latest/MLTable.schema.json

type: mltable
paths:
    - file: ./timeseries_train.csv

transformations:
    - read_delimited:
        delimiter: ','
        encoding: ascii
```

Begin building the YAML configuration for the AutoML job with the training data specified as shown in the following example:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

# Training data MLTable for the AutoML job.
training_data:
    path: "./train_data"
    type: mltable

validation_data:
    # Optional validation data.

compute: # Compute for training job.
primary_metric: # Primary metric.  

target_column_name: # Target column name.
n_cross_validations: # Cross-validation setting.

limits:
    # Limit settings.

forecasting:
    # Forecasting-specific settings.

training:
    # Training settings. 
```

You'll add more detail to this configuration in subsequent sections of this article. In this example, the location is *./automl-forecasting-job.yml*.

---

You specify [validation data](concept-automated-ml.md#training-validation-and-test-data) in a similar way. Create an `MLTable` object and specify a validation data input. Alternatively, if you don't supply validation data, AutoML automatically creates cross-validation splits from your training data to use for model selection. For more information, see the following resources:

- [Select forecasting models](./concept-automl-forecasting-sweeping.md#model-selection-in-automl)
- [Set training data length requirements](./concept-automl-forecasting-methods.md#data-length-requirements)
- [Prevent overfitting with cross-validation](concept-manage-ml-pitfalls.md#prevent-overfitting)

## Create compute to run the experiment

AutoML uses Azure Machine Learning compute, which is a fully managed compute resource, to run the training job. 

# [Python SDK](#tab/python)

The following example creates a compute cluster named `cpu-cluster`.

[!notebook-python[] (~/azureml-examples-main/sdk/python/jobs/configuration.ipynb?name=create-cpu-compute)]

# [Azure CLI](#tab/cli)

Create a new compute named `cpu-compute` by using the following Azure CLI command:

```azurecli
az ml compute create -n cpu-compute --type amlcompute --min-instances 0 --max-instances 4
```

Reference the compute in the job definition, as shown in the following example:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

# Set training data MLTable for the AutoML job.
training_data:
    path: "./train_data"
    type: mltable

# Set compute for the training job to use. 
compute: azureml:cpu-compute

primary_metric: # Primary metric.  

target_column_name: # Target column name.
n_cross_validations: # Cross-validation setting.

limits:
    # Limit settings.

forecasting:
    # Forecasting-specific settings.

training:
    # Training settings.
```

---

## Configure the experiment

The following example shows how to configure the experiment.

# [Python SDK](#tab/python)

Use the [AutoML factory functions](/python/api/azure-ai-ml/azure.ai.ml.automl#azure-ai-ml-automl-forecasting) to configure forecasting jobs in the Python SDK. The following example shows how to create a [forecasting job](/python/api/azure-ai-ml/azure.ai.ml.automl.forecastingjob) by setting the [primary metric](how-to-configure-auto-train.md#primary-metric) and set limits on the training run:

```python
from azure.ai.ml import automl

# Set forecasting variables.
# As needed, modify the variable values to run the snippet successfully.
forecasting_job = automl.forecasting(
    compute="cpu-cluster",
    experiment_name="sdk-v2-automl-forecasting-job",
    training_data=my_training_data_input,
    target_column_name=target_column_name,
    primary_metric="normalized_root_mean_squared_error",
    n_cross_validations="auto",
)

# Set optional limits.
forecasting_job.set_limits(
    timeout_minutes=120,
    trial_timeout_minutes=30,
    max_concurrent_trials=4,
)
```

# [Azure CLI](#tab/cli)

Configure general properties of the AutoML job, including:

- The [primary metric](how-to-configure-auto-train.md#primary-metric).
- The name of the target column in the training data.
- The cross-validation settings.
- Resource limits on the job.

For more information, see the [forecasting command job YAML schema](reference-automated-ml-forecasting.md), [training parameters](reference-automated-ml-forecasting.md#training), and [limits](reference-automated-ml-forecasting.md#limits).

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:cpu-compute

# Settings for primary metric, target/label column name, cross validation.
primary_metric: normalized_root_mean_squared_error
target_column_name: <target_column_name>
n_cross_validations: auto

# Settings for training job limits on time, concurrency, and others.
limits:
    timeout_minutes: 120
    trial_timeout_minutes: 30
    max_concurrent_trials: 4

forecasting:
    # Forecasting-specific settings.

training:
    # Training settings.
```

---

### Forecast job settings

Forecasting tasks have many settings that are specific to forecasting. The most basic of these settings are the name of the time column in the training data and the forecast horizon.

# [Python SDK](#tab/python)

Use the [ForecastingJob](/python/api/azure-ai-ml/azure.ai.ml.automl.forecastingjob#azure-ai-ml-automl-forecastingjob-set-forecast-settings) methods to configure these settings:

```python
# Forecasting-specific configuration.
forecasting_job.set_forecast_settings(
    time_column_name=time_column_name,
    forecast_horizon=24
)
```

# [Azure CLI](#tab/cli)

Configure these settings in the `forecasting` section of the job YAML configuration:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:cpu-compute

primary_metric: normalized_root_mean_squared_error
target_column_name: <target_column_name>
n_cross_validations: auto

limits:
    timeout_minutes: 120
    trial_timeout_minutes: 30
    max_concurrent_trials: 4

# Forecasting-specific settings.
# Set the horizon to 24 for this example. The horizon generally depends on the business scenario.
forecasting:
    time_column_name: <time_column_name>
    forecast_horizon: 24

training:
    # Training settings.
```

---

The time column name is a required setting. Generally, set the forecast horizon according to your prediction scenario. If your data contains multiple time series, specify the names of the *time series ID* columns. When you group these columns, they define the individual series. For example, suppose you have data that consists of hourly sales from different stores and brands. The following sample shows how to set the time series ID columns, assuming that the data contains columns named *store* and *brand*:

# [Python SDK](#tab/python)

```python
# Forecasting-specific configuration.
# Add time series IDs for store and brand.
forecasting_job.set_forecast_settings(
    ...,  # Other settings.
    time_series_id_column_names=['store', 'brand']
)
```

# [Azure CLI](#tab/cli)

```yml
# Forecasting-specific settings.
# Add time series IDs for store and brand.
forecasting:
    # Other settings.
    time_series_id_column_names: ["store", "brand"]
```

---

If you don't specify time series ID columns, AutoML tries to automatically detect them in your data.

The other settings are optional and described in the following section.

### Optional forecasting job settings

Optional configurations are available for forecasting tasks, such as enabling deep learning and specifying a target rolling-window aggregation. A complete list of parameters is available in the [reference documentation](reference-automated-ml-forecasting.md#forecasting).

#### Model search settings

Two optional settings control the model space where AutoML searches for the best model: `allowed_training_algorithms` and `blocked_training_algorithms`. To restrict the search space to a given set of model classes, use the `allowed_training_algorithms` parameter, as shown in the following example:

# [Python SDK](#tab/python)

```python
# Only search ExponentialSmoothing and ElasticNet models.
forecasting_job.set_training(
    allowed_training_algorithms=["ExponentialSmoothing", "ElasticNet"]
)
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:cpu-compute

primary_metric: normalized_root_mean_squared_error
target_column_name: <target_column_name>
n_cross_validations: auto

limits:
    timeout_minutes: 120
    trial_timeout_minutes: 30
    max_concurrent_trials: 4

forecasting:
    time_column_name: <time_column_name>
    forecast_horizon: 24

# Training settings.
# Only search ExponentialSmoothing and ElasticNet models.
training:
    allowed_training_algorithms: ["ExponentialSmoothing", "ElasticNet"]
    # Other training settings.
```

---

In this scenario, the forecasting job searches *only* over Exponential Smoothing and Elastic Net model classes. To remove a given set of model classes from the search space, use `blocked_training_algorithms`, as shown in the following example:

# [Python SDK](#tab/python)

```python
# Search over all model classes except Prophet.
forecasting_job.set_training(
    blocked_training_algorithms=["Prophet"]
)
```

# [Azure CLI](#tab/cli)

```yml
# Training settings.
# Search over all model classes except Prophet.
training:
    blocked_training_algorithms: ["Prophet"]
    # Other training settings.
```

---

The job searches over all model classes *except* Prophet. For a list of forecasting model names that are accepted in `allowed_training_algorithms` and `blocked_training_algorithms`, see [training properties](reference-automated-ml-forecasting.md#training). You can apply either but not both `allowed_training_algorithms` and `blocked_training_algorithms` to a training run.

#### Enable learning for deep neural networks

AutoML ships with a custom deep neural network (DNN) model named `TCNForecaster`. This model is a [temporal convolutional network](https://arxiv.org/abs/1803.01271) (TCN), that applies common imaging task methods to time-series modeling. One-dimensional "causal" convolutions form the backbone of the network and enable the model to learn complex patterns over long durations in the training history. For more information, see [Introduction to TCNForecaster](./concept-automl-forecasting-deep-learning.md#introduction-to-tcnforecaster).

:::image type="content" source="media/how-to-auto-train-forecast/tcn-basic.png" alt-text="Diagram that shows the major components of the AutoML TCNForecaster model." border="false" lightbox="media/how-to-auto-train-forecast/tcn-basic.png":::

TCNForecaster often achieves higher accuracy than standard time-series models when there are thousands of observations or more in the training history. However, it also takes longer to train and sweep over TCNForecaster models because of their higher capacity.

You can enable the TCNForecaster in AutoML by setting the `enable_dnn_training` flag in the training configuration, as shown in the following example:

# [Python SDK](#tab/python)

```python
# Include TCNForecaster models in the model search.
forecasting_job.set_training(
    enable_dnn_training=True
)
```

# [Azure CLI](#tab/cli)

```yml
# Training settings.
# Include TCNForecaster models in the model search.
training:
    enable_dnn_training: true
    # Other training settings.
```

---

By default, TCNForecaster training is limited to a single compute node and a single GPU, if available, per model trial. For large data scenarios, distribute each TCNForecaster trial over multiple cores, GPUs, and nodes. For more information and code samples, see [distributed training](how-to-configure-auto-train.md#distributed-training-for-forecasting).

To enable DNN for an AutoML experiment created in Azure Machine Learning studio, see the [task type settings in the studio UI article](how-to-use-automated-ml-for-ml-models.md#create-and-run-experiment).

> [!NOTE]
> - When you enable DNN for experiments created by using the SDK, [best model explanations](./v1/how-to-machine-learning-interpretability-automl.md) are disabled.
> - DNN support for forecasting in automated machine learning isn't supported for runs initiated in Azure Databricks.
> - Use GPU compute types when you enable DNN training.

#### Lag and rolling-window features

Recent values of the target are often impactful features in a forecasting model. Accordingly, AutoML can create time-lagged and rolling-window aggregation features to potentially improve model accuracy.

Consider an energy demand forecasting scenario where weather data and historical demand are available. The following table shows the resulting feature engineering that occurs when window aggregation is applied over the most recent three hours. Columns for *minimum*, *maximum*, and *sum* are generated on a sliding window of three hours based on the defined settings. For instance, for the observation valid on September 8, 2017, 4:00 AM, the maximum, minimum, and sum values are calculated by using the *demand values* for September 8, 2017, 1:00 AM to 3:00 AM. This window of three hours shifts along to populate data for the remaining rows. For more information and examples, see [Lag features for time-series forecasting in AutoML](concept-automl-forecasting-lags.md).

:::image type="content" source="./media/how-to-auto-train-forecast/target-roll.png" alt-text="A table with data that shows the target rolling window. The values in the Demand column are highlighted." border="false" lightbox="./media/how-to-auto-train-forecast/target-roll.png":::

You can enable lag and rolling-window aggregation features for the target by setting the rolling-window size and the lag orders you want to create. The window size is three in the previous example. You can also enable lags for features by using the `feature_lags` setting. In the following example, set all of these settings to `auto` to instruct AutoML to automatically determine settings by analyzing the correlation structure of your data:

# [Python SDK](#tab/python)

```python
forecasting_job.set_forecast_settings(
    ...,  # Other settings.
    target_lags='auto', 
    target_rolling_window_size='auto',
    feature_lags='auto'
)
```

# [Azure CLI](#tab/cli)

```yml
# Forecasting-specific settings.
# Auto configure lags and rolling-window features.
forecasting:
    target_lags: auto
    target_rolling_window_size: auto
    feature_lags: auto
    # Other settings.
```

---

#### Short series handling

AutoML considers a time series a *short series* if the series doesn't have enough data points to conduct the train and validation phases of model development. For more information, see [training data length requirements](concept-automl-forecasting-methods.md#data-length-requirements).

AutoML has several actions it can take for short series. You can configure these actions by using the `short_series_handling_config` setting. The default value is `auto`. The following table describes the settings:

| Setting | Description | Notes |
| --- | --- |--|
| `auto` | The default value for short series handling. | - If all series are short, pad the data. <br> - If not all series are short, drop the short series. |
| `pad`  | If the `short_series_handling_config = pad` setting is used, AutoML adds random values to each short series it finds. AutoML pads the target column with white noise. | You can use the following column types with the specified padding: <br> - Object columns - pad with `NaN`s. <br> - Numeric columns - pad with 0 (zero). <br> - Boolean/logic columns - pad with `False`. |
| `drop` | If the `short_series_handling_config = drop` setting is used, AutoML drops the short series. It doesn't use the short series for training or prediction. | Predictions for these series return `NaN`. |
| `None` | No series is padded or dropped. | |

The following example sets the short series handling so that all short series are padded to the minimum length:

# [Python SDK](#tab/python)

```python
forecasting_job.set_forecast_settings(
    ...,  # Other settings.
    short_series_handling_config='pad'
)
```

# [Azure CLI](#tab/cli)

```yml
# Forecasting-specific settings.
# Auto configure lags and rolling-window features.
forecasting:
    short_series_handling_config: pad
    # Other settings.
```

---

> [!CAUTION]
> Padding can affect the accuracy of the resulting model because it introduces artificial data to avoid training failures. If many of the series are short, you might also see some impact in explainability results.

#### Frequency and target data aggregation

Use the frequency and data aggregation options to avoid failures caused by irregular data. Your data is irregular if it doesn't follow a set cadence in time, like hourly or daily. Point-of-sales data is a good example of irregular data. In these scenarios, AutoML can aggregate your data to a desired frequency and then build a forecasting model from the aggregates.

Set the `frequency` and `target_aggregate_function` options to handle irregular data. The frequency option accepts [Pandas DateOffset strings](https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects) as input. The following table shows supported values for the aggregation function:

| Function | Description |
| --- | --- |
| `sum`  | Sum of target values |
| `mean` | Mean or *average* of target values |
| `min`  | Minimum value of a target |
| `max`  | Maximum value of a target |

AutoML applies aggregation for the following columns:

| Column | Aggregation method |
| --- | --- |
| Numerical predictors    | AutoML uses the `sum`, `mean`, `min`, and `max` functions. It generates new columns. Each column name includes a suffix that identifies the name of the aggregation function applied to the column values. |
| Categorical predictors  | AutoML uses the value of the `forecast_mode` parameter to aggregate the data. It's the most prominent category in the window. For more information, see the descriptions of the parameter in the [Many-models pipeline](#many-models-pipeline) and [HTS pipeline](#hts-pipeline) sections. |
| Data predictors         | AutoML uses the minimum target value (`min`), maximum target value (`max`), and `forecast_mode` parameter settings to aggregate the data. |
| Target                  | AutoML aggregates the values according to the specified operation. Typically, the `sum` function is appropriate for most scenarios. |

The following example sets the frequency to hourly and the aggregation function to summation:

# [Python SDK](#tab/python)

```python
# Aggregate the data to hourly frequency.
forecasting_job.set_forecast_settings(
    ...,  # Other settings.
    frequency='H',
    target_aggregate_function='sum'
)
```

# [Azure CLI](#tab/cli)

```yml
# Forecasting-specific settings.
# Auto-configure lags and rolling-window features.
forecasting:
    frequency: H
    target_aggregate_function: sum
    # Other settings.
```

---

#### Custom cross-validation settings

Two customizable settings control cross-validation for forecasting jobs. Customize the number of folds by using the `n_cross_validations` parameter. Configure the [cv_step_size](/python/api/azure-ai-ml/azure.ai.ml.automl.forecastingjob#azure-ai-ml-automl-forecastingjob-set-forecast-settings) parameter to define the time offset between folds. For more information, see [forecasting model selection](concept-automl-forecasting-sweeping.md#model-selection-in-automl).

By default, AutoML sets both settings automatically based on characteristics of your data. Advanced users might want to set them manually. For example, suppose you have daily sales data and you want your validation setup to consist of five folds with a seven-day offset between adjacent folds. The following code sample shows how to set these values:

# [Python SDK](#tab/python)

```python
from azure.ai.ml import automl

# Create a job with five CV folds.
forecasting_job = automl.forecasting(
    ...,  # Other training parameters.
    n_cross_validations=5,
)

# Set the step size between folds to seven days.
forecasting_job.set_forecast_settings(
    ...,  # Other settings.
    cv_step_size=7
)
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:cpu-compute

primary_metric: normalized_root_mean_squared_error
target_column_name: <target_column_name>
n_cross_validations: auto

# Use five CV folds.
n_cross_validations: 5

# Set the step size between folds to seven days.
forecasting:
    cv_step_size: 7
    # Other settings.

limits:
    # Limit settings.

training:
    # Training settings.
```

---

### Custom featurization

By default, AutoML augments training data with engineered features to increase the accuracy of the models. For more information, see [Automated feature engineering](./concept-automl-forecasting-methods.md#automated-feature-engineering). You can customize some of the preprocessing steps by using the [featurization](reference-automated-ml-forecasting.md#featurization) configuration of the forecasting job.

The following table lists the supported customizations for forecasting:

| Customization | Description | Options |
| --- | --- | --- |
| Column purpose update        | Override the autodetected feature type for the specified column. | `categorical`, `dateTime`, `numeric` |
| Transformer parameter update | Update the parameters for the specified imputer. | `{"strategy": "constant", "fill_value": <value>}`, `{"strategy": "median"}`, `{"strategy": "ffill"}` |

For example, suppose you have a retail demand scenario where the data includes prices, an `on sale` flag, and a product type. The following example shows how you can set customized types and imputers for these features:

# [Python SDK](#tab/python)

```python
from azure.ai.ml.automl import ColumnTransformer

# Customize imputation methods for price and is_on_sale features.
# Median value imputation for price, constant value of zero for is_on_sale.
transformer_params = {
    "imputer": [
        ColumnTransformer(fields=["price"], parameters={"strategy": "median"}),
        ColumnTransformer(fields=["is_on_sale"], parameters={"strategy": "constant", "fill_value": 0}),
    ],
}

# Set the featurization.
# Ensure product_type feature is interpreted as categorical.
forecasting_job.set_featurization(
    mode="custom",
    transformer_params=transformer_params,
    column_name_and_types={"product_type": "Categorical"},
)
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

experiment_name: cli-v2-automl-forecasting-job
description: A time-series forecasting AutoML job
task: forecasting

training_data:
    path: "./train_data"
    type: mltable

compute: azureml:cpu-compute

primary_metric: normalized_root_mean_squared_error
target_column_name: <target_column_name>
n_cross_validations: auto

# Customize imputation methods for price and is_on_sale features.
# Median value imputation for price, constant value of zero for is_on_sale.
featurization:
    mode: custom
    column_name_and_types:
        product_type: Categorical
    transformer_params:
        imputer:
            - fields: ["price"]
            parameters:
                strategy: median
            - fields: ["is_on_sale"]
            parameters:
                strategy: constant
                fill_value: 0

forecasting:
    # Forecasting-specific settings.

limits:
    # Limit settings.

training:
    # Training settings.
```

---

If you use Azure Machine Learning studio for your experiment, see [Configure featurization settings in the studio](how-to-use-automated-ml-for-ml-models.md#customize-featurization).

## Submit the forecasting job

After you configure all settings, you're ready to run the forecasting job. The following example demonstrates this process.

# [Python SDK](#tab/python)

```python
# Submit the AutoML job.
returned_job = ml_client.jobs.create_or_update(
    forecasting_job
)

print(f"Created job: {returned_job}")

# Get a URL for the job in the studio UI.
returned_job.services["Studio"].endpoint
```

# [Azure CLI](#tab/cli)

In the following Azure CLI command, the job YAML configuration is in the current working directory at the path *./automl-forecasting-job.yml*. If you run the command from a different directory, change the path accordingly.

```azurecli
run_id=$(az ml job create --file automl-forecasting-job.yml)
```

Use the stored run ID to return information about the job. The `--web` parameter opens the Azure Machine Learning studio web UI, where you can see details about the job:

```azurecli
az ml job show -n $run_id --web
```

---

After you submit the job, AutoML provisions compute resources, applies featurization and other preparation steps to the input data, and begins sweeping over forecasting models. For more information, see [Forecasting methodology in AutoML](concept-automl-forecasting-methods.md) and [Model sweeping and selection for forecasting in AutoML](concept-automl-forecasting-sweeping.md).

## Orchestrate training, inference, and evaluation by using components and pipelines

Your machine learning workflow probably requires more than just training. Inference, or retrieving model predictions on newer data, and evaluation of model accuracy on a test set with known target values are other common tasks that you can orchestrate in Azure Machine Learning along with training jobs. To support inference and evaluation tasks, Azure Machine Learning provides [components](concept-component.md), which are self-contained pieces of code that do one step in an Azure Machine Learning [pipeline](concept-ml-pipelines.md).

# [Python SDK](#tab/python)

The following example retrieves component code from a client registry:

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Get credential to access azureml registry.
try:
    credential = DefaultAzureCredential()
    # Check if token can be obtained successfully.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential in case DefaultAzureCredential fails.
    credential = InteractiveBrowserCredential()

# Create client to access assets in azureml-preview registry.
ml_client_registry = MLClient(
    credential=credential,
    registry_name="azureml-preview"
)

# Create client to access assets in azureml registry.
ml_client_metrics_registry = MLClient(
    credential=credential,
    registry_name="azureml"
)

# Get inference component from registry.
inference_component = ml_client_registry.components.get(
    name="automl_forecasting_inference",
    label="latest"
)

# Get component to compute evaluation metrics from registry.
compute_metrics_component = ml_client_metrics_registry.components.get(
    name="compute_metrics",
    label="latest"
)
```

Next, define a factory function that creates pipelines orchestrating training, inference, and metric computation. For more information, see [Configure the experiment](#configure-the-experiment).

```python
from azure.ai.ml import automl
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.dsl import pipeline

@pipeline(description="AutoML Forecasting Pipeline")
def forecasting_train_and_evaluate_factory(
    train_data_input,
    test_data_input,
    target_column_name,
    time_column_name,
    forecast_horizon,
    primary_metric='normalized_root_mean_squared_error',
    cv_folds='auto'
):
    # Configure training node of pipeline.
    training_node = automl.forecasting(
        training_data=train_data_input,
        target_column_name=target_column_name,
        primary_metric=primary_metric,
        n_cross_validations=cv_folds,
        outputs={"best_model": Output(type=AssetTypes.MLFLOW_MODEL)},
    )

    training_node.set_forecasting_settings(
        time_column_name=time_column_name,
        forecast_horizon=max_horizon,
        frequency=frequency,
        # Other settings.
        ... 
    )
    
    training_node.set_training(
        # Training parameters.
        ...
    )
    
    training_node.set_limits(
        # Limit settings.
        ...
    )

    # Configure inference node to make rolling forecasts on test set.
    inference_node = inference_component(
        test_data=test_data_input,
        model_path=training_node.outputs.best_model,
        target_column_name=target_column_name,
        forecast_mode='rolling',
        step=1
    )

    # Configure metrics calculation node.
    compute_metrics_node = compute_metrics_component(
        task="tabular-forecasting",
        ground_truth=inference_node.outputs.inference_output_file,
        prediction=inference_node.outputs.inference_output_file,
        evaluation_config=inference_node.outputs.evaluation_config_output_file
    )

    # Return dictionary with evaluation metrics and raw test set forecasts.
    return {
        "metrics_result": compute_metrics_node.outputs.evaluation_result,
        "rolling_fcst_result": inference_node.outputs.inference_output_file
    }
```

Define train and test data inputs contained in local folders *./train_data* and *./test_data*.

```python
my_train_data_input = Input(
    type=AssetTypes.MLTABLE,
    path="./train_data"
)

my_test_data_input = Input(
    type=AssetTypes.URI_FOLDER,
    path='./test_data',
)
```

Finally, construct the pipeline, set its default compute, and submit the job:

```python
pipeline_job = forecasting_train_and_evaluate_factory(
    my_train_data_input,
    my_test_data_input,
    target_column_name,
    time_column_name,
    forecast_horizon
)

# Set pipeline-level compute.
pipeline_job.settings.default_compute = compute_name

# Submit pipeline job.
returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name
)
returned_pipeline_job
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

description: AutoML Forecasting Pipeline
experiment_name: cli-v2-automl-forecasting-pipeline

# Set default compute for pipeline steps.
settings:
    default_compute: cpu-compute

# Pipeline inputs.
inputs:
    train_data_input:
        type: mltable
        path: "./train_data"
    test_data_input:
        type: uri_folder
        path: "./test_data"
    target_column_name: <target column name>
    time_column_name: <time column name>
    forecast_horizon: <forecast horizon>
    primary_metric: normalized_root_mean_squared_error
    cv_folds: auto

# Set pipeline outputs.
# Output the evaluation metrics and raw test set rolling forecasts.
outputs: 
    metrics_result:
        type: uri_file
        mode: upload
    rolling_fcst_result:
        type: uri_file
        mode: upload

jobs:
  # Configure automl training node of pipeline.
    training_node:
        type: automl
        task: forecasting
        primary_metric: ${{parent.inputs.primary_metric}}
        target_column_name: ${{parent.inputs.target_column_name}}
        training_data: ${{parent.inputs.train_data_input}}
        n_cross_validations: ${{parent.inputs.cv_folds}}
        training:
            # Training settings.
        forecasting:
            time_column_name: ${{parent.inputs.time_column_name}}
            forecast_horizon: ${{parent.inputs.forecast_horizon}}
            # Other forecasting-specific settings.
        limits:
            # Limit settings.
        outputs:
            best_model:
                type: mlflow_model

    # Configure inference node to make rolling forecasts on test set.
    inference_node:
        type: command
        component: azureml://registries/azureml-preview/components/automl_forecasting_inference
        inputs:
            target_column_name: ${{parent.inputs.target_column_name}}
            forecast_mode: rolling
            step: 1
            test_data: ${{parent.inputs.test_data_input}}
            model_path: ${{parent.jobs.training_node.outputs.best_model}}
        outputs:
            inference_output_file: ${{parent.outputs.rolling_fcst_result}}
            evaluation_config_output_file:
                type: uri_file

    # Configure metrics calculation node.
    compute_metrics:
        type: command
        component: azureml://registries/azureml/compute_metrics
        inputs:
            task: "tabular-forecasting"
            ground_truth: ${{parent.jobs.inference_node.outputs.inference_output_file}}
            prediction: ${{parent.jobs.inference_node.outputs.inference_output_file}}
            evaluation_config: ${{parent.jobs.inference_node.outputs.evaluation_config_output_file}}
        outputs:
            evaluation_result: ${{parent.outputs.metrics_result}}
```

AutoML requires training data in [MLTable format](#prepare-training-and-validation-data).

Start the pipeline run by using the following command. The pipeline configuration is at the path *./automl-forecasting-pipeline.yml*:

```yml
run_id=$(az ml job create --file automl-forecasting-pipeline.yml -w <Workspace> -g <Resource Group> --subscription <Subscription>)
```

---

After you submit the run request, the pipeline runs AutoML training, rolling-evaluation inference, and metric calculation in sequence. You can monitor and inspect the run in the studio UI. When the run completes, you can download the rolling forecasts and the evaluation metrics to the local working directory:

# [Python SDK](#tab/python)

```python
# Download metrics JSON.
ml_client.jobs.download(returned_pipeline_job.name, download_path=".", output_name='metrics_result')

# Download rolling forecasts.
ml_client.jobs.download(returned_pipeline_job.name, download_path=".", output_name='rolling_fcst_result')
```

# [Azure CLI](#tab/cli)

```azurecli
az ml job download --name $run_id --download-path . --output-name metrics_result
az ml job download --name $run_id --download-path . --output-name rolling_fcst_result
```

---

You can review the output at the following locations:

- Metrics: *./named-outputs/metrics_results/evaluationResult/metrics.json*
- Forecasts: *./named-outputs/rolling_fcst_result/inference_output_file* (JSON Lines format).

For more information on rolling evaluation, see [Inference and evaluation of forecasting models](concept-automl-forecasting-evaluation.md).

## Forecast at scale: Many models

The many-models components in AutoML enable you to train and manage millions of models in parallel. For more information, see [Many models](concept-automl-forecasting-at-scale.md#many-models).

### Many-models training configuration

The many-models training component accepts a YAML-format configuration file of AutoML training settings. The component applies these settings to each AutoML instance it starts. The YAML file has the same specification as the [Forecasting command job](reference-automated-ml-forecasting.md), plus the `partition_column_names` and `allow_multi_partitions` parameters.

| Parameter | Description |
| --- | --- |
| `partition_column_names` | Column names in the data that, when grouped, define the data partitions. The many-models training component starts an independent training job on each partition. |
| `allow_multi_partitions` | An optional flag that allows training one model per partition when each partition contains more than one unique time series. The default value is `false`. |

Here's a sample YAML configuration:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

description: A time-series forecasting job config
compute: azureml:<cluster-name>
task: forecasting
primary_metric: normalized_root_mean_squared_error
target_column_name: sales
n_cross_validations: 3

forecasting:
  time_column_name: date
  time_series_id_column_names: ["state", "store"]
  forecast_horizon: 28

training:
  blocked_training_algorithms: ["ExtremeRandomTrees"]

limits:
  timeout_minutes: 15
  max_trials: 10
  max_concurrent_trials: 4
  max_cores_per_trial: -1
  trial_timeout_minutes: 15
  enable_early_termination: true
  
partition_column_names: ["state", "store"]
allow_multi_partitions: false
```

In subsequent examples, the configuration is stored at the path *./automl_settings_mm.yml*.

### Many models pipeline

Next, define a factory function that creates pipelines for the orchestration of many models training, inference, and metric computation. The following table describes the parameters for this factory function:

| Parameter | Description |
| --- | --- |
| `max_nodes`                        | Number of compute nodes to use in the training job. |
| `max_concurrency_per_node`         | Number of AutoML processes to run on each node. The total concurrency of a many-models job is `max_nodes` * `max_concurrency_per_node`. |
| `parallel_step_timeout_in_seconds` | Many models component timeout, specified in number of seconds. |
| `retrain_failed_models`            | Flag to enable retraining for failed models. This value is useful if you did previous many-models runs that resulted in failed AutoML jobs on some data partitions. When you enable this flag, many models only runs training jobs for previously failed partitions. |
| `forecast_mode`                    | Inference mode for model evaluation. Valid values are `recursive` (default) and `rolling`. For more information, see [Inference and evaluation of forecasting models](concept-automl-forecasting-evaluation.md) and the [ManyModelsInferenceParameters Class](/python/api/azureml-train-automl-runtime/azureml.train.automl.runtime.manymodelsinferenceparameters#parameters) reference. |
| `step`                             | Step size for rolling forecast. The default is `1`. For more information, see [Inference and evaluation of forecasting models](concept-automl-forecasting-evaluation.md) and the [ManyModelsInferenceParameters Class](/python/api/azureml-train-automl-runtime/azureml.train.automl.runtime.manymodelsinferenceparameters#parameters) reference.|

The following example demonstrates a factory method for constructing many-models training and model evaluation pipelines:

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Get credential to access azureml registry.
try:
    credential = DefaultAzureCredential()
    # Check whether token can be obtained.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential if DefaultAzureCredential fails.
    credential = InteractiveBrowserCredential()

# Get many-models training component.
mm_train_component = ml_client_registry.components.get(
    name='automl_many_models_training',
    version='latest'
)

# Get many-models inference component.
mm_inference_component = ml_client_registry.components.get(
    name='automl_many_models_inference',
    version='latest'
)

# Get component to compute evaluation metrics.
compute_metrics_component = ml_client_metrics_registry.components.get(
    name="compute_metrics",
    label="latest"
)

@pipeline(description="AutoML Many Models Forecasting Pipeline")
def many_models_train_evaluate_factory(
    train_data_input,
    test_data_input,
    automl_config_input,
    compute_name,
    max_concurrency_per_node=4,
    parallel_step_timeout_in_seconds=3700,
    max_nodes=4,
    retrain_failed_model=False,
    forecast_mode="rolling",
    forecast_step=1
):
    mm_train_node = mm_train_component(
        raw_data=train_data_input,
        automl_config=automl_config_input,
        max_nodes=max_nodes,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        retrain_failed_model=retrain_failed_model,
        compute_name=compute_name
    )

    mm_inference_node = mm_inference_component(
        raw_data=test_data_input,
        max_nodes=max_nodes,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        optional_train_metadata=mm_train_node.outputs.run_output,
        forecast_mode=forecast_mode,
        step=forecast_step,
        compute_name=compute_name
    )

    compute_metrics_node = compute_metrics_component(
        task="tabular-forecasting",
        prediction=mm_inference_node.outputs.evaluation_data,
        ground_truth=mm_inference_node.outputs.evaluation_data,
        evaluation_config=mm_inference_node.outputs.evaluation_configs
    )

    # Return metrics results from rolling evaluation.
    return {
        "metrics_result": compute_metrics_node.outputs.evaluation_result
    }
```

Construct the pipeline with the factory function. The training and test data are in the local folders *./data/train* and *./data/test*. Finally, set the default compute and submit the job as shown in the following example:

```python
pipeline_job = many_models_train_evaluate_factory(
    train_data_input=Input(
        type="uri_folder",
        path="./data/train"
    ),
    test_data_input=Input(
        type="uri_folder",
        path="./data/test"
    ),
    automl_config=Input(
        type="uri_file",
        path="./automl_settings_mm.yml"
    ),
    compute_name="<cluster name>"
)
pipeline_job.settings.default_compute = "<cluster name>"

returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name,
)
ml_client.jobs.stream(returned_pipeline_job.name)
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

description: AutoML Many Models Forecasting Pipeline
experiment_name: cli-v2-automl-mm-forecasting-pipeline

# Set default compute for pipeline steps.
settings:
    default_compute: azureml:cpu-compute

# Set pipeline inputs.
inputs:
    train_data_input:
        type: uri_folder
        path: "./train_data"
        mode: direct
    test_data_input:
        type: uri_folder
        path: "./test_data"
    automl_config_input:
        type: uri_file
        path: "./automl_settings_mm.yml"
    max_nodes: 4
    max_concurrency_per_node: 4
    parallel_step_timeout_in_seconds: 3700
    forecast_mode: rolling
    step: 1
    retrain_failed_model: False

# Set pipeline outputs.
# Output the evaluation metrics and raw test set rolling forecasts.
outputs: 
    metrics_result:
        type: uri_file
        mode: upload

jobs:
    # Configure AutoML many-models training component.
    mm_train_node:
        type: command
        component: azureml://registries/azureml-preview/components/automl_many_models_training
        inputs:
            raw_data: ${{parent.inputs.train_data_input}}
            automl_config: ${{parent.inputs.automl_config_input}}
            max_nodes: ${{parent.inputs.max_nodes}}
            max_concurrency_per_node: ${{parent.inputs.max_concurrency_per_node}}
            parallel_step_timeout_in_seconds: ${{parent.inputs.parallel_step_timeout_in_seconds}}
            retrain_failed_model: ${{parent.inputs.retrain_failed_model}}
        outputs:
            run_output:
                type: uri_folder

    # Configure inference node to make rolling forecasts on test set.
    mm_inference_node:
        type: command
        component: azureml://registries/azureml-preview/components/automl_many_models_inference
        inputs:
            raw_data: ${{parent.inputs.test_data_input}}
            max_concurrency_per_node: ${{parent.inputs.max_concurrency_per_node}}
            parallel_step_timeout_in_seconds: ${{parent.inputs.parallel_step_timeout_in_seconds}}
            forecast_mode: ${{parent.inputs.forecast_mode}}
            step: ${{parent.inputs.step}}
            max_nodes: ${{parent.inputs.max_nodes}}
            optional_train_metadata: ${{parent.jobs.mm_train_node.outputs.run_output}}
        outputs:
            run_output:
                type: uri_folder
            evaluation_configs:
                type: uri_file
            evaluation_data:
                type: uri_file

    # Configure metrics calculation node.
    compute_metrics:
        type: command
        component: azureml://registries/azureml/components/compute_metrics
        inputs:
            task: "tabular-forecasting"
            ground_truth: ${{parent.jobs.mm_inference_node.outputs.evaluation_data}}
            prediction: ${{parent.jobs.mm_inference_node.outputs.evaluation_data}}
            evaluation_config: ${{parent.jobs.mm_inference_node.outputs.evaluation_configs}}
        outputs:
            evaluation_result: ${{parent.outputs.metrics_result}}
```

You start the pipeline job with the following command. The many-models pipeline configuration is at the path *./automl-mm-forecasting-pipeline.yml*.

```azurecli
az ml job create --file automl-mm-forecasting-pipeline.yml -w <Workspace> -g <Resource Group> --subscription <Subscription>
```

---

After the job finishes, you can download the evaluation metrics locally by using the procedure in the [single training run pipeline](#orchestrate-training-inference-and-evaluation-by-using-components-and-pipelines).

For a more detailed example, see the [Demand Forecasting by Using Many Models notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1k_demand_forecast_pipeline/aml-demand-forecast-mm-pipeline/aml-demand-forecast-mm-pipeline.ipynb).

#### Training considerations for a many-models run

- The many-models training and inference components conditionally partition your data according to the `partition_column_names` setting. This process results in each partition being in its own file. The process can be slow or fail when you have a lot of data. Manually partition your data before you run many-models training or inference.

- During many-models training, models are automatically registered in the workspace, so you don't need to register models manually. Models are named based on the partition on which they were trained, and these names aren't customizable. Tags also aren't customizable. These properties are used to automatically detect models during inference.

- Deploying individual models isn't scalable, but you can use `PipelineComponentBatchDeployment` to make the deployment process easier. For an example, see the [Demand Forecasting by Using Many Models notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1k_demand_forecast_pipeline/aml-demand-forecast-mm-pipeline/aml-demand-forecast-mm-pipeline.ipynb). 

- During inference, appropriate models (the latest version) are automatically selected based on the partition sent in the inference data. By default, when you use `training_experiment_name`, the latest model is used, but you can override this behavior to select models from a particular training run by also providing `train_run_id`.

> [!NOTE]
> The default parallelism limit for a many-models run in a subscription is 320. If your workload requires a higher limit, contact Microsoft support.

## Forecast at scale: Hierarchical time series

The hierarchical time series (HTS) components in AutoML enable you to train a large number of models on data that's in a hierarchical structure. For more information, see [Hierarchical time series forecasting](concept-automl-forecasting-at-scale.md#hierarchical-time-series-forecasting).

### HTS training configuration

The HTS training component accepts a YAML format configuration file of AutoML training settings. The component applies these settings to each AutoML instance it runs. This YAML file has the same specification as the [Forecasting command job](reference-automated-ml-forecasting.md), but it includes other parameters that are related to the hierarchy information:

| Parameter | Description |
| --- | --- |
| `hierarchy_column_names`  | A list of column names in the data that define the hierarchical structure of the data. The order of the columns in this list determines the hierarchy levels. The degree of aggregation decreases with the list index. That is, the last column in the list defines the leaf, or most disaggregated, level of the hierarchy. |
| `hierarchy_training_level` | The hierarchy level to use for forecast model training. |

Here's a sample YAML configuration:

```yml
$schema: https://azuremlschemas.azureedge.net/latest/autoMLForecastingJob.schema.json
type: automl

description: A time-series forecasting job config
compute: azureml:cluster-name
task: forecasting
primary_metric: normalized_root_mean_squared_error
log_verbosity: info
target_column_name: sales
n_cross_validations: 3

forecasting:
  time_column_name: "date"
  time_series_id_column_names: ["state", "store", "SKU"]
  forecast_horizon: 28

training:
  blocked_training_algorithms: ["ExtremeRandomTrees"]

limits:
  timeout_minutes: 15
  max_trials: 10
  max_concurrent_trials: 4
  max_cores_per_trial: -1
  trial_timeout_minutes: 15
  enable_early_termination: true
  
hierarchy_column_names: ["state", "store", "SKU"]
hierarchy_training_level: "store"
```

In subsequent examples, the configuration is stored at the path *./automl_settings_hts.yml*.

### HTS pipeline

Next, define a factory function that creates pipelines for the orchestration of HTS training, inference, and metric computation. The following table describes the parameters for this factory function:

| Parameter | Description |
| --- | --- |
| `forecast_level`                   | The level of the hierarchy for which to retrieve forecasts. |
| `allocation_method`                | The allocation method to use when forecasts are disaggregated. Valid values are `proportions_of_historical_average` and `average_historical_proportions`. |
| `max_nodes`                        | The number of compute nodes to use in the training job. |
| `max_concurrency_per_node`         | The number of AutoML processes to run on each node. The total concurrency of an HTS job is `max_nodes` * `max_concurrency_per_node`. |
| `parallel_step_timeout_in_seconds` |The many-models component timeout, specified in seconds. |
| `forecast_mode`                    | The inference mode for model evaluation. Valid values are `recursive` and `rolling`. For more information, see [Inference and evaluation of forecasting models](concept-automl-forecasting-evaluation.md) and the [HTSInferenceParameters Class](/python/api/azureml-train-automl-runtime/azureml.train.automl.runtime.htsinferenceparameters#parameters) reference. |
| `step`                             | The step size for rolling forecast. The default is `1`. For more information, see [Inference and evaluation of forecasting models](concept-automl-forecasting-evaluation.md) and the [HTSInferenceParameters Class](/python/api/azureml-train-automl-runtime/azureml.train.automl.runtime.htsinferenceparameters#parameters) reference. |

# [Python SDK](#tab/python)

```python
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential

# Get credential to access azureml registry.
try:
    credential = DefaultAzureCredential()
    # Check whether token can be obtained.
    credential.get_token("https://management.azure.com/.default")
except Exception as ex:
    # Fall back to InteractiveBrowserCredential if DefaultAzureCredential fails.
    credential = InteractiveBrowserCredential()

# Get HTS training component.
hts_train_component = ml_client_registry.components.get(
    name='automl_hts_training',
    version='latest'
)

# Get HTS inference component.
hts_inference_component = ml_client_registry.components.get(
    name='automl_hts_inference',
    version='latest'
)

# Get component to compute evaluation metrics.
compute_metrics_component = ml_client_metrics_registry.components.get(
    name="compute_metrics",
    label="latest"
)

@pipeline(description="AutoML HTS Forecasting Pipeline")
def hts_train_evaluate_factory(
    train_data_input,
    test_data_input,
    automl_config_input,
    max_concurrency_per_node=4,
    parallel_step_timeout_in_seconds=3700,
    max_nodes=4,
    forecast_mode="rolling",
    forecast_step=1,
    forecast_level="SKU",
    allocation_method='proportions_of_historical_average'
):
    hts_train = hts_train_component(
        raw_data=train_data_input,
        automl_config=automl_config_input,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        max_nodes=max_nodes
    )
    hts_inference = hts_inference_component(
        raw_data=test_data_input,
        max_nodes=max_nodes,
        max_concurrency_per_node=max_concurrency_per_node,
        parallel_step_timeout_in_seconds=parallel_step_timeout_in_seconds,
        optional_train_metadata=hts_train.outputs.run_output,
        forecast_level=forecast_level,
        allocation_method=allocation_method,
        forecast_mode=forecast_mode,
        step=forecast_step
    )
    compute_metrics_node = compute_metrics_component(
        task="tabular-forecasting",
        prediction=hts_inference.outputs.evaluation_data,
        ground_truth=hts_inference.outputs.evaluation_data,
        evaluation_config=hts_inference.outputs.evaluation_configs
    )

    # Return metrics results from rolling evaluation.
    return {
        "metrics_result": compute_metrics_node.outputs.evaluation_result
    }
```

Construct the pipeline by using the factory function. The training and test data are in the local folders *./data/train* and *./data/test*. Finally, set the default compute and submit the job as shown in the following example:

```python
pipeline_job = hts_train_evaluate_factory(
    train_data_input=Input(
        type="uri_folder",
        path="./data/train"
    ),
    test_data_input=Input(
        type="uri_folder",
        path="./data/test"
    ),
    automl_config=Input(
        type="uri_file",
        path="./automl_settings_hts.yml"
    )
)
pipeline_job.settings.default_compute = "cluster-name"

returned_pipeline_job = ml_client.jobs.create_or_update(
    pipeline_job,
    experiment_name=experiment_name,
)
ml_client.jobs.stream(returned_pipeline_job.name)
```

# [Azure CLI](#tab/cli)

```yml
$schema: https://azuremlschemas.azureedge.net/latest/pipelineJob.schema.json
type: pipeline

description: AutoML Many Models Forecasting Pipeline
experiment_name: cli-v2-automl-mm-forecasting-pipeline

# Set the default compute for pipeline steps.
settings:
    default_compute: azureml:cpu-compute

# Set pipeline inputs.
inputs:
    train_data_input:
        type: uri_folder
        path: "./train_data"
        mode: direct
    test_data_input:
        type: uri_folder
        path: "./test_data"
    automl_config_input:
        type: uri_file
        path: "./automl_settings_hts.yml"
    max_concurrency_per_node: 4
    parallel_step_timeout_in_seconds: 3700
    max_nodes: 4
    forecast_mode: rolling
    step: 1
    allocation_method: proportions_of_historical_average
    forecast_level: # forecast level

# Set pipeline outputs.
# Output evaluation metrics and raw test set rolling forecasts.
outputs: 
    metrics_result:
        type: uri_file
        mode: upload

jobs:
    # Configure AutoML many-models training component.
    hts_train_node:
        type: command
        component: azureml://registries/azureml-preview/components/automl_hts_training
        inputs:
            raw_data: ${{parent.inputs.train_data_input}}
            automl_config: ${{parent.inputs.automl_config_input}}
            max_nodes: ${{parent.inputs.max_nodes}}
            max_concurrency_per_node: ${{parent.inputs.max_concurrency_per_node}}
            parallel_step_timeout_in_seconds: ${{parent.inputs.parallel_step_timeout_in_seconds}}
        outputs:
            run_output:
                type: uri_folder


    # Configure inference node to make rolling forecasts on test set.
    hts_inference_node:
        type: command
        component: azureml://registries/azureml-preview/components/automl_hts_inference
        inputs:
            raw_data: ${{parent.inputs.test_data_input}}
            max_concurrency_per_node: ${{parent.inputs.max_concurrency_per_node}}
            parallel_step_timeout_in_seconds: ${{parent.inputs.parallel_step_timeout_in_seconds}}
            forecast_mode: ${{parent.inputs.forecast_mode}}
            step: ${{parent.inputs.step}}
            max_nodes: ${{parent.inputs.max_nodes}}
            optional_train_metadata: ${{parent.jobs.hts_train_node.outputs.run_output}}
            forecast_level: ${{parent.inputs.forecast_level}}
            allocation_method: ${{parent.inputs.allocation_method}}
        outputs:
            run_output:
                type: uri_folder
            evaluation_configs:
                type: uri_file
            evaluation_data:
                type: uri_file

    # Configure metrics calculation node.
    compute_metrics:
        type: command
        component: azureml://registries/azureml/components/compute_metrics
        inputs:
            task: "tabular-forecasting"
            ground_truth: ${{parent.jobs.hts_inference_node.outputs.evaluation_data}}
            prediction: ${{parent.jobs.hts_inference_node.outputs.evaluation_data}}
            evaluation_config: ${{parent.jobs.hts_inference_node.outputs.evaluation_configs}}
        outputs:
            evaluation_result: ${{parent.outputs.metrics_result}}
```

You start the pipeline job by using the following command. The many-models pipeline configuration is at the path *./automl-hts-forecasting-pipeline.yml*.

```azurecli
az ml job create --file automl-hts-forecasting-pipeline.yml -w <Workspace> -g <Resource Group> --subscription <Subscription>
```

---

After the job finishes, you can download the evaluation metrics locally by using the procedure in the [single training run pipeline](#orchestrate-training-inference-and-evaluation-by-using-components-and-pipelines).

For a more detailed example, see the [Demand Forecasting Using HTS notebook](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/pipelines/1k_demand_forecast_pipeline/aml-demand-forecast-hts-pipeline/aml-demand-forecast-hts.ipynb).

#### Training considerations for an HTS run

The HTS training and inference components conditionally partition your data according to the `hierarchy_column_names` setting so that each partition is in its own file. This process can be slow or fail when you have a lot of data. Manually partition your data before you run HTS training or inference.

> [!NOTE]
> The default parallelism limit for an HTS run in a subscription is 320. If your workload requires a higher limit, you can contact Microsoft support.

## Forecast at scale: Distributed DNN training

As described earlier in this article, you can [enable learning for deep neural networks (DNN)](#enable-learning-for-deep-neural-networks). To learn how distributed training works for DNN forecasting tasks, see [Distributed deep neural network training (preview)](concept-automl-forecasting-at-scale.md#distributed-dnn-training-preview). 

For scenarios that require large amounts of data, distributed training with AutoML is available for a limited set of models. You can find more information and code samples in [AutoML at scale: Distributed training](how-to-configure-auto-train.md#automl-at-scale-distributed-training).

## Explore example notebooks

Detailed code samples that demonstrate advanced forecasting configurations are available in the [AutoML Forecasting Sample Notebooks](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/automl-standalone-jobs) GitHub repository. Here are some of the example notebooks:

- [Create demand forecasting pipeline (HTS and many models)](https://github.com/Azure/azureml-examples/tree/main/sdk/python/jobs/pipelines/1k_demand_forecast_pipeline)
- [Train TCNForecaster (DNN) model on GitHub dataset](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-forecasting-github-dau/auto-ml-forecasting-github-dau.ipynb)
- [Forecast with holiday detection and featurization (bike-share dataset)](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-forecasting-task-bike-share/auto-ml-forecasting-bike-share.ipynb)
- [Configure lags and rolling-window aggregation manually](https://github.com/Azure/azureml-examples/blob/main/sdk/python/jobs/automl-standalone-jobs/automl-forecasting-task-energy-demand/automl-forecasting-task-energy-demand-advanced.ipynb)

## Related content

- [Deploy an AutoML model to an online endpoint](how-to-deploy-automl-endpoint.md)
- [Model interpretability with the Python SDK](./v1/how-to-machine-learning-interpretability-automl.md)
- [Choose a modeling configuration](how-to-automl-forecasting-faq.md#what-modeling-configuration-should-i-use)
