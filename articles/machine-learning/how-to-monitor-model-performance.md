---
title: Monitor model performance in production
titleSuffix: Azure Machine Learning
description: See how to monitor models that you deploy to production in Azure Machine Learning. Find out how to use out-of-box, advanced, and custom monitoring.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: mlops
ms.topic: how-to
author: s-polly
ms.author: scottpolly
ms.reviewer: jturuk
ms.date: 02/11/2026
ms.custom: devplatv2, devx-track-azurecli, update-code5, dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to see how to monitor the models that I deploy to production in Azure Machine Learning so that I can maintain the models and improve their performance.
---

# Monitor the performance of models deployed to production

[!INCLUDE [dev v2](includes/machine-learning-dev-v2.md)]

In Azure Machine Learning, use model monitoring to continuously track the performance of machine learning models in production. Model monitoring provides a broad view of monitoring signals and alerts you to potential problems. When you monitor signals and performance metrics of models in production, you can critically evaluate the inherent risks of your models. You can also identify hidden problems that might adversely affect your business.

In this article, you learn how to perform the following tasks:

- Set up out-of-box and advanced monitoring for models that you deploy to Azure Machine Learning online endpoints
- Monitor performance metrics for models in production
- Monitor models that you deploy outside Azure Machine Learning or models that you deploy to Azure Machine Learning batch endpoints
- Set up custom signals and metrics to use in model monitoring
- Interpret monitoring results
- Integrate Azure Machine Learning model monitoring with Azure Event Grid

## Prerequisites

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [Basic prerequisites for the Azure CLI](includes/machine-learning-cli-prereqs.md)]

# [Python SDK](#tab/python)

[!INCLUDE [Basic prerequisites for the Python SDK](includes/machine-learning-sdk-v2-prereqs.md)]

# [Studio](#tab/azure-studio)

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) before you begin.

* An Azure Machine Learning workspace. For steps for creating a workspace, see [Create the workspace](quickstart-create-resources.md#create-the-workspace).

* An Azure Machine Learning compute instance. For steps for creating a compute instance, see [Create a compute instance](quickstart-create-resources.md#create-a-compute-instance).

---

* A user account that has at least one of the following Azure role-based access control (Azure RBAC) roles:

  * An Owner role for the Azure Machine Learning workspace
  * A Contributor role for the Azure Machine Learning workspace
  * A custom role that has `Microsoft.MachineLearningServices/workspaces/onlineEndpoints/*` permissions

  For more information, see [Manage access to Azure Machine Learning workspaces](how-to-assign-roles.md).

* For monitoring an Azure Machine Learning managed online endpoint or Kubernetes online endpoint:

  * A model that's deployed to the Azure Machine Learning online endpoint. Managed online endpoints and Kubernetes online endpoints are supported. For instructions for deploying a model to an Azure Machine Learning online endpoint, see [Deploy and score a machine learning model by using an online endpoint](how-to-deploy-online-endpoints.md).

  * Data collection enabled for your model deployment. You can enable data collection during the deployment step for Azure Machine Learning online endpoints. For more information, see [Collect production data from models deployed for real-time inferencing](how-to-collect-production-data.md).

* For monitoring a model that's deployed to an Azure Machine Learning batch endpoint or deployed outside Azure Machine Learning:

  * A means to collect production data and register it as an Azure Machine Learning data asset
  * A means to update the registered data asset continuously for model monitoring
  * (Recommended) Registration of the model in an Azure Machine Learning workspace, for lineage tracking

## Configure a serverless Spark compute pool

Schedule model monitoring jobs to run on serverless Spark compute pools. The following Azure Virtual Machines instance types are supported:

- Standard_E4s_v3
- Standard_E8s_v3
- Standard_E16s_v3
- Standard_E32s_v3
- Standard_E64s_v3

To specify a virtual machine instance type when you follow the procedures in this article, take the following steps:

# [Azure CLI](#tab/azure-cli)

When you use the Azure CLI to create a monitor, use a YAML configuration file. In that file, set the `create_monitor.compute.instance_type` value to the type that you want to use.

# [Python SDK](#tab/python)

When you use the Python SDK to create a monitor, use `azure.ai.ml.entities.ServerlessSparkCompute` to create a compute instance. When you call that method, set the `instance_type` parameter to the type that you want to use.

# [Studio](#tab/azure-studio)

When you use Azure Machine Learning studio to add a monitor, the Basic settings page opens. Under **Virtual machine size**, select the type that you want to use.

---

## Set up out-of-box model monitoring

Consider a scenario in which you deploy your model to production in an Azure Machine Learning online endpoint and enable [data collection](how-to-collect-production-data.md) at deployment time. In this case, Azure Machine Learning collects production inference data and automatically stores it in Azure Blob Storage. You can use Azure Machine Learning model monitoring to continuously monitor this production inference data.

You can use the Azure CLI, the Python SDK, or the studio for an out-of-box setup of model monitoring. The out-of-box model monitoring configuration provides the following monitoring capabilities:

* Azure Machine Learning automatically detects the production inference data asset that's associated with an Azure Machine Learning online deployment and uses the data asset for model monitoring.
* The comparison reference data asset is set as the recent, past production inference data asset.
* Monitoring setup automatically includes and tracks the following built-in monitoring signals: data drift, prediction drift, and data quality. For each monitoring signal, Azure Machine Learning uses:
  * The recent, past production inference data asset as the comparison reference data asset.
  * Smart default values for metrics and thresholds.
* A monitoring job is configured to run on a regular schedule. That job acquires monitoring signals and evaluates each metric result against its corresponding threshold. By default, when any threshold is exceeded, Azure Machine Learning sends an alert email to the user who set up the monitor.

To set up out-of-box model monitoring, take the following steps.

# [Azure CLI](#tab/azure-cli)

In the Azure CLI, use `az ml schedule` to schedule a monitoring job.

1. Create a monitoring definition in a YAML file. For a sample out-of-box definition, see the following YAML code, which is also available in the [azureml-examples repository](https://github.com/Azure/azureml-examples/blob/main/cli/monitoring/out-of-box-monitoring.yaml).

    Before you use this definition, adjust the values to fit your environment. For `endpoint_deployment_id`, use a value in the format `azureml:<endpoint-name>:<deployment-name>`.

    :::code language="yaml" source="~/azureml-examples-main/cli/monitoring/out-of-box-monitoring.yaml":::

1. Run the following command to create the model:

    ```azurecli
    az ml schedule create -f ./out-of-box-monitoring.yaml
    ```

# [Python SDK](#tab/python)

Use code similar to the following sample. Replace the placeholders with appropriate values:

| Placeholder | Description | Example |
| --- | --- | --- |
| \<subscription-ID\> | The ID of your subscription | aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e |
| \<resource-group-name\> | The name of the resource group that contains your workspace | my-resource-group |
| \<workspace-name\> | The name of your workspace | my-workspace |
| \<endpoint-name\> | The name of the endpoint to monitor | credit-default |
| \<deployment-name\> | The name of the deployment to monitor | main |
| \<email-address-1\> and \<email-address-2\> | Email addresses to use for notifications | `abc@example.com` |
| \<frequency-unit\> | The monitoring frequency unit | day |
| \<interval\> | The interval between jobs, expressed in the frequency unit | 1 |
| \<start-hour\> | The hour to start monitoring, on a 24-hour clock | 3 |
| \<start-minutes\> | The minutes after the specified hour to start monitoring | 15 |

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import MLClient
from azure.ai.ml.entities import (
    AlertNotification,
    MonitoringTarget,
    MonitorDefinition,
    MonitorSchedule,
    RecurrencePattern,
    RecurrenceTrigger,
    ServerlessSparkCompute
)

# Get a handle to the workspace.
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<subscription-ID>",
    resource_group_name="<resource-group-name>",
    workspace_name="<workspace-name>",
)

# Create the compute instance.
spark_compute = ServerlessSparkCompute(
    instance_type="standard_e4s_v3",
    runtime_version="3.4"
)

# Specify your online endpoint deployment.
monitoring_target = MonitoringTarget(
    ml_task="classification",
    endpoint_deployment_id="azureml:<endpoint-name>:<deployment-name>"
)

# Create an alert notification object.
alert_notification = AlertNotification(
    emails=['<email-address-1>', '<email-address-2>']
)

# Create the monitor definition.
monitor_definition = MonitorDefinition(
    compute=spark_compute,
    monitoring_target=monitoring_target,
    alert_notification=alert_notification
)

# Specify the schedule frequency.
recurrence_trigger = RecurrenceTrigger(
    frequency="<frequency-unit>",
    interval=<interval>,
    schedule=RecurrencePattern(hours=<start-hour>, minutes=<start-minutes>)
)

# Create the monitoring schedule.
model_monitor = MonitorSchedule(
    name="credit_default_monitor_basic",
    trigger=recurrence_trigger,
    create_monitor=monitor_definition
)

# Schedule the monitoring job.
poller = ml_client.schedules.begin_create_or_update(model_monitor)
created_monitor = poller.result()
```

# [Studio](#tab/azure-studio)

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Manage**, select **Monitoring**, and then select **Add**.

    :::image type="content" source="media/how-to-monitor-models/add-model-monitoring.png" alt-text="Screenshot of an Azure Machine Learning studio workspace Monitoring page, with the Monitoring and Add buttons highlighted and a few monitors visible." lightbox="media/how-to-monitor-models/add-model-monitoring.png":::

1. On the Basic settings page, enter the following information:
    - Under **(Optional) Select model**, select the model that you want to monitor.
    - Under **(Optional) Select deployment with data collection enabled**, select the deployment that you want to monitor. Azure Machine Learning automatically populates this list if the model is deployed to an Azure Machine Learning online endpoint.
    - Under **(Optional) Select training data**, select the training data to use as the comparison reference.
    - Under **Monitor name**, enter a name for the monitoring, or keep the default name.
    - Under **Virtual machine size**, use the default size.
    - Under **Time zone**, select your time zone. 
    - For scheduling, select **Recurrence** or **Cron expression**.
    - For recurrence scheduling, specify the repeat frequency, day, and time. For cron expression scheduling, enter a cron expression for a monitoring run.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-basic-setup.png" alt-text="Screenshot of the Basic settings page for model monitoring, with settings like the name, model, and deployment filled in." lightbox="media/how-to-monitor-models/model-monitoring-basic-setup.png":::

1. Select **Next**.

1. On the following pages, select **Next**:
    - Configure data asset
    - Select monitoring signals

1. On the Notifications page, enter the email address that you want to use to receive notifications, and then select **Next**.

1. On the Review monitoring details page, review the settings, and then select **Create**.

---

## Set up advanced model monitoring

Azure Machine Learning provides many capabilities for continuous model monitoring. For a comprehensive list of this functionality, see [Capabilities of model monitoring](concept-model-monitoring.md#capabilities-of-model-monitoring). In many cases, you need to set up model monitoring that supports advanced monitoring tasks. The following section provides a few examples of advanced monitoring:

* The use of multiple monitoring signals for a broad view
* The use of historical model training data or validation data as the comparison reference data asset
* Monitoring of the *N* most important features and individual features

### Configure feature importance

Feature importance represents the relative importance of each input feature to a model's output. For example, temperature might be more important to a model's prediction than elevation. When you turn on feature importance, you can provide visibility into which features you don't want drifting or having data quality problems in production. 

To turn on feature importance with any of your signals, such as data drift or data quality, provide:

- Your training data asset as the `reference_data` data asset.
- The `reference_data.data_column_names.target_column` property, which is the name of your model's output column, or prediction column. 
 
After you turn on feature importance, you see a feature importance for each feature that you monitor in Azure Machine Learning studio.

Turn alerts on or off for each signal by setting the `alert_enabled` property when you use the Python SDK or the Azure CLI.

Use the Azure CLI, the Python SDK, or the studio to set up advanced model monitoring.

# [Azure CLI](#tab/azure-cli)

1. Create a monitoring definition in a YAML file. For a sample advanced definition, see the following YAML code, which is also available in the [azureml-examples repository](https://github.com/Azure/azureml-examples/blob/main/cli/monitoring/advanced-model-monitoring.yaml).

    Before you use this definition, adjust the following settings and any others to meet the needs of your environment:

    - For `endpoint_deployment_id`, use a value in the format `azureml:<endpoint-name>:<deployment-name>`.
    - For `path` in reference input data sections, use a value in the format `azureml:<reference-data-asset-name>:<version>`.
    - For `target_column`, use the name of the output column that contains values that the model predicts, such as `DEFAULT_NEXT_MONTH`.
    - For `features`, list the features like `SEX`, `EDUCATION`, and `AGE` that you want to use in an advanced data quality signal.
    - Under `emails`, list the email addresses that you want to use for notifications.

    :::code language="yaml" source="~/azureml-examples-main/cli/monitoring/advanced-model-monitoring.yaml":::

1. Run the following command to create the model:

    ```azurecli
    az ml schedule create -f ./advanced-model-monitoring.yaml
    ```

# [Python SDK](#tab/python)

To set up advanced model monitoring, use code similar to the following sample. Replace the placeholders with appropriate values:

| Placeholder | Description | Example |
| --- | --- | --- |
| \<subscription-ID\> | The ID of your subscription | aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e |
| \<resource-group-name\> | The name of the resource group that contains your workspace | my-resource-group |
| \<workspace-name\> | The name of your workspace | my-workspace |
| \<endpoint-name\> | The name of the endpoint to monitor | credit-default |
| \<deployment-name\> | The name of the deployment to monitor | main |
| \<production-data-asset-name\> | The name of the data asset that contains production data | credit-default-main-model_inputs |
| \<reference-data-asset-name\> | The name of the data asset that contains reference data | credit-default-reference |
| \<target-column\> | The name of the output column that contains values that the model predicts | DEFAULT_NEXT_MONTH |
| \<feature-1\>, \<feature-2\>, and \<feature-3\> | The features that you want to use in an advanced data quality signal | AGE |
| \<email-address-1\> and \<email-address-2\> | Email addresses to use for notifications | `abc@example.com` |
| \<frequency-unit\> | The monitoring frequency unit | day |
| \<interval\> | The interval between jobs, expressed in the frequency unit | 1 |
| \<start-hour\> | The hour to start monitoring, on a 24-hour clock | 3 |
| \<start-minutes\> | The minutes after the specified hour to start monitoring | 15 |

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import Input, MLClient
from azure.ai.ml.constants import (
    MonitorDatasetContext,
)
from azure.ai.ml.entities import (
    AlertNotification,
    BaselineDataRange,
    DataDriftSignal,
    DataQualitySignal,
    PredictionDriftSignal,
    DataDriftMetricThreshold,
    DataQualityMetricThreshold,
    FeatureAttributionDriftMetricThreshold,
    FeatureAttributionDriftSignal,
    PredictionDriftMetricThreshold,
    NumericalDriftMetrics,
    CategoricalDriftMetrics,
    DataQualityMetricsNumerical,
    DataQualityMetricsCategorical,
    MonitorFeatureFilter,
    MonitoringTarget,
    MonitorDefinition,
    MonitorSchedule,
    RecurrencePattern,
    RecurrenceTrigger,
    ServerlessSparkCompute,
    ReferenceData,
    ProductionData
)

# Get a handle to the workspace.
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<subscription-ID>",
    resource_group_name="<resource-group-name>",
    workspace_name="<workspace-name>",
)

# Create a compute instance.
spark_compute = ServerlessSparkCompute(
    instance_type="standard_e4s_v3",
    runtime_version="3.4"
)

# Specify the online deployment if you have one.
monitoring_target = MonitoringTarget(
    ml_task="classification",
    endpoint_deployment_id="azureml:<endpoint-name>:<deployment-name>"
)

# Specify a look-back window size and offset to use. Omit this line to use the default values, which are listed in the documentation.
data_window = BaselineDataRange(lookback_window_size="P1D", lookback_window_offset="P0D")

# Set up the production data.
production_data = ProductionData(
    input_data=Input(
        type="uri_folder",
        path="azureml:<production-data-asset-name>:1"
    ),
    data_window=data_window,
    data_context=MonitorDatasetContext.MODEL_INPUTS,
)

# Set up the training data to use as a reference data asset.
reference_data_training = ReferenceData(
    input_data=Input(
        type="mltable",
        path="azureml:<reference-data-asset-name>:1"
    ),
    data_column_names={
        "target_column":"<target-column>"
    },
    data_context=MonitorDatasetContext.TRAINING,
)

# Create an advanced data drift signal.
features = MonitorFeatureFilter(top_n_feature_importance=10)

metric_thresholds = DataDriftMetricThreshold(
    numerical=NumericalDriftMetrics(
        jensen_shannon_distance=0.01
    ),
    categorical=CategoricalDriftMetrics(
        pearsons_chi_squared_test=0.02
    )
)

advanced_data_drift = DataDriftSignal(
    reference_data=reference_data_training,
    features=features,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Create an advanced prediction drift signal.
metric_thresholds = PredictionDriftMetricThreshold(
    categorical=CategoricalDriftMetrics(
        jensen_shannon_distance=0.01
    )
)

advanced_prediction_drift = PredictionDriftSignal(
    reference_data=reference_data_training,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Create an advanced data quality signal.
features = ['<feature-1>', '<feature-2>', '<feature-3>']

metric_thresholds = DataQualityMetricThreshold(
    numerical=DataQualityMetricsNumerical(
        null_value_rate=0.01
    ),
    categorical=DataQualityMetricsCategorical(
        out_of_bounds_rate=0.02
    )
)

advanced_data_quality = DataQualitySignal(
    reference_data=reference_data_training,
    features=features,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Create a feature attribution drift signal.
metric_thresholds = FeatureAttributionDriftMetricThreshold(normalized_discounted_cumulative_gain=0.9)

feature_attribution_drift = FeatureAttributionDriftSignal(
    reference_data=reference_data_training,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Put all monitoring signals in a dictionary.
monitoring_signals = {
    'data_drift_advanced':advanced_data_drift,
    'data_quality_advanced':advanced_data_quality,
    'feature_attribution_drift':feature_attribution_drift,
}

# Create an alert notification object.
alert_notification = AlertNotification(
    emails=['<email-address-1>', '<email-address-2>']
)

# Create the monitor definition.
monitor_definition = MonitorDefinition(
    compute=spark_compute,
    monitoring_target=monitoring_target,
    monitoring_signals=monitoring_signals,
    alert_notification=alert_notification
)

# Specify the schedule frequency.
recurrence_trigger = RecurrenceTrigger(
    frequency="<frequency-unit>",
    interval=<interval>,
    schedule=RecurrencePattern(hours=<start-hour>, minutes=<start-minutes>)
)

# Create the monitoring schedule.
model_monitor = MonitorSchedule(
    name="credit_default_monitor_advanced",
    trigger=recurrence_trigger,
    create_monitor=monitor_definition
)

# Schedule the monitoring job.
poller = ml_client.schedules.begin_create_or_update(model_monitor)
created_monitor = poller.result()
```

# [Studio](#tab/azure-studio)

To set up advanced monitoring, complete the steps in the following sections.

### Configure basic settings

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Manage**, select **Monitoring**, and then select **Add**.

1. On the Basic settings page, enter the information as described earlier in [Set up out-of-box model monitoring](#set-up-out-of-box-model-monitoring).

### Add data assets

1. On the Basic settings page, after you configure the settings, select **Next**. The **Configure data asset** page of the **Advanced settings** section opens.

1. If you don't see the data asset that you want to use as a reference data asset, select **Add**. Then enter the settings for your data asset. Use the model training data as the comparison reference data asset for data drift and data quality. Use the model validation data as the comparison reference data asset for prediction drift.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-advanced-configuration-data.png" alt-text="Screenshot of the Configure data asset page, with a few data assets listed in a table and the Add button highlighted." lightbox="media/how-to-monitor-models/model-monitoring-advanced-configuration-data.png":::

### Edit data drift settings

1. On **Configure data asset**, after you add data assets, select **Next**. The **Select monitoring signals** page opens. If you're using an Azure Machine Learning online deployment, you see some monitoring signals. The data drift, data quality, and prediction drift signals use recent, past production data as the comparison reference data asset and use smart default values for metrics and thresholds.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-monitoring-signals.png" alt-text="Screenshot of the Select monitoring signals page. Three default monitoring signals and buttons for adding, editing, and deleting signals are visible." lightbox="media/how-to-monitor-models/model-monitoring-monitoring-signals.png":::

1. Next to the data drift signal, select **Edit**.

1. In the **Edit Signal** window, take the following steps to configure the data drift signal:
    1. In step 1:
        1. For the production data asset, select your model input data asset.
        1. Select the look-back window size that you want to use.
    1. In step 2:
        1. For the reference data asset, select your training data asset.
        1. Select the target, or output, column.
    1. In step 3, select **Top N features** to monitor drift for the *N* most important features. Or select specific features if you want to monitor drift for a specific set.
    1. In step 4, select the metric and threshold that you want to use for numerical features.
    1. In step 5, select the metric and threshold that you want to use for categorical features.
    1. Select **Save**.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configure-signals.png" alt-text="Screenshot of the Edit Signal page for the data drift signal. Five steps are visible that provide a way to configure various settings." lightbox="media/how-to-monitor-models/model-monitoring-configure-signals.png":::

### Add a feature attribution drift signal

1. On **Select monitoring signals**, select **Add**.

1. In **Edit Signal**, select **Feature attribution drift (PREVIEW)**, and then take the following steps to configure the feature attribution drift signal:

    1. In step 1:
        1. Select the production data asset that has your model input data.
        1. Select the look-back window size that you want to use.
    1. In step 2:
        1. Select the production data asset that has your model output data.
        1. Select the common column to use to join the production data and the output data. If you use the [data collector](how-to-collect-production-data.md) to collect data, select **correlationid**.
    1. (Optional) If you use the data collector to collect your input and output data in a format that joins them together, take the following steps:
        1. In step 1, for the production data asset, select the joined data asset. 
        1. In step 2, select **Remove** to remove step 2 from the configuration panel.  
    1. In step 3:
        1. For the reference data asset, select your training data asset.
        1. Select the target, or output, column for your training data asset.
    1. In step 4, select the metric and threshold that you want to use.
    1. Select **Save**.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configure-feature-attribution-drift.png" alt-text="Screenshot of the Edit Signal page. The Feature attribution drift tab is highlighted, and four steps provide a way to configure various settings." lightbox="media/how-to-monitor-models/model-monitoring-configure-feature-attribution-drift.png":::

### Finish the configuration

1. On **Select monitoring signals**, finish configuring your monitoring signals, and then select **Next**.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configured-signals.png" alt-text="Screenshot of the Select monitoring signals page, with three default signals and the feature attribution drift signal visible." lightbox="media/how-to-monitor-models/model-monitoring-configured-signals.png":::

1. On **Notifications**, turn on notifications for each signal, and then select **Next**.

1. On **Review monitoring details**, review your settings.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-advanced-configuration-review.png" alt-text="Screenshot of the Review monitoring details page. The basic settings, three configured data assets, and four configured signals are visible." lightbox="media/how-to-monitor-models/model-monitoring-advanced-configuration-review.png":::

1. Select **Create** to create your advanced model monitor.

---

## Set up model performance monitoring

When you use Azure Machine Learning model monitoring, you can track the performance of your models in production by calculating their performance metrics. The following model performance metrics are currently supported:

- For classification models:
  - Precision
  - Accuracy
  - Recall
- For regression models:
  - Mean absolute error (MAE)
  - Mean squared error (MSE)
  - Root mean squared error (RMSE)

### Prerequisites for model performance monitoring

* Output data for the production model (the model's predictions) with a unique ID for each row. If you use the [Azure Machine Learning data collector](how-to-collect-production-data.md) to collect production data, a correlation ID is provided for each inference request for you. The data collector also offers the option of logging your own unique ID from your application.

  > [!NOTE]
  >
  > For Azure Machine Learning model performance monitoring, use the [Azure Machine Learning data collector](how-to-collect-production-data.md) to log your unique ID in its own column.

* Ground truth data (actuals) with a unique ID for each row. The unique ID for a given row should match the unique ID for the model output data for that particular inference request. This unique ID is used to join your ground truth data asset with the model output data.

  If you don't have ground truth data, you can't perform model performance monitoring. Ground truth data is encountered at the application level, so it's your responsibility to collect it as it becomes available. You should also maintain a data asset in Azure Machine Learning that contains this ground truth data.

* (Optional) A prejoined tabular data asset with model output data and ground truth data already joined together.

### Requirements for model performance monitoring when you use the data collector

Azure Machine Learning generates a correlation ID when you meet the following criteria:

- You use the [Azure Machine Learning data collector](concept-data-collection.md) to collect production inference data.
- You don't supply your own unique ID for each row as a separate column.

The logged JSON object includes the generated correlation ID. However, the data collector [batches rows](how-to-collect-production-data.md#data-collector-batching) that are sent within short time intervals of each other. Batched rows fall within the same JSON object. Within each object, all rows have the same correlation ID.

To differentiate between the rows in a JSON object, Azure Machine Learning model performance monitoring uses indexing to determine the order of the rows within the object. For example, if a batch contains three rows and the correlation ID is `test`, the first row has an ID of `test_0`, the second row has an ID of `test_1`, and the third row has an ID of `test_2`. To match your ground truth data asset unique IDs with the IDs of your collected production inference model output data, apply an index to each correlation ID appropriately. If your logged JSON object only has one row, use `correlationid_0` as the `correlationid` value.

To avoid using this indexing, log your unique ID in its own column. Put that column within the pandas data frame that the [Azure Machine Learning data collector](how-to-collect-production-data.md) logs. In your model monitoring configuration, you can then specify the name of this column to join your model output data with your ground truth data. As long as the IDs for each row in both data assets are the same, Azure Machine Learning model monitoring can perform model performance monitoring.

### Example workflow for monitoring model performance

To understand the concepts associated with model performance monitoring, consider the following example workflow. It applies to a scenario in which you deploy a model to predict whether credit card transactions are fraudulent:

1. Configure your deployment to use the data collector to collect the model's production inference data (input and output data). Store the output data in a column called `is_fraud`.
1. For each row of the collected inference data, log a unique ID. The unique ID can come from your application, or you can use the `correlationid` value that Azure Machine Learning uniquely generates for each logged JSON object.
1. When the ground truth (or actual) `is_fraud` data is available, log and map each row to the same unique ID that you logged for the corresponding row in the model's output data.
1. Register a data asset in Azure Machine Learning, and use it to collect and maintain the ground truth `is_fraud` data.
1. Create a model performance monitoring signal that uses the unique ID columns to join the model's production inference and ground truth data assets.
1. Compute the model performance metrics.

# [Azure CLI](#tab/azure-cli)

After you satisfy the [prerequisites for model performance monitoring](#prerequisites-for-model-performance-monitoring), take the following steps to set up model monitoring:

1. Create a monitoring definition in a YAML file. The following sample specification defines model monitoring with production inference data. Before you use this definition, adjust the following settings and any others to meet the needs of your environment:

    - For `endpoint_deployment_id`, use a value in the format `azureml:<endpoint-name>:<deployment-name>`.
    - For each `path` value in an input data section, use a value in the format `azureml:<data-asset-name>:<version>`.
    - For the `prediction` value, use the name of the output column that contains values that the model predicts.
    - For the `actual` value, use the name of the ground truth column that contains the actual values that the model tries to predict.
    - For the `correlation_id` values, use the names of the columns that you use to join the output data and the ground truth data.
    - Under `emails`, list the email addresses that you want to use for notifications.

    ```yml
    # model-performance-monitoring.yaml
    $schema:  http://azureml/sdk-2-0/Schedule.json
    name: model_performance_monitoring
    display_name: Credit card fraud model performance
    description: Credit card fraud model performance

    trigger:
      type: recurrence
      frequency: day
      interval: 7 
      schedule: 
        hours: 10
        minutes: 15
  
    create_monitor:
      compute: 
        instance_type: standard_e8s_v3
        runtime_version: "3.4"
      monitoring_target:
        ml_task: classification
        endpoint_deployment_id: azureml:loan-approval-endpoint:loan-approval-deployment

      monitoring_signals:
        fraud_detection_model_performance: 
          type: model_performance 
          production_data:
            input_data:
              path: azureml:credit-default-main-model_outputs:1
              type: mltable
            data_column_names:
              prediction: is_fraud
              correlation_id: correlation_id
          reference_data:
            input_data:
              path: azureml:my_model_ground_truth_data:1
              type: mltable
            data_column_names:
              actual: is_fraud
              correlation_id: correlation_id
            data_context: ground_truth
          alert_enabled: true
          metric_thresholds: 
            tabular_classification:
              accuracy: 0.95
              precision: 0.8
      alert_notification: 
          emails: 
            - abc@example.com
    ```

1. Run the following command to create the model:

    ```azurecli
    az ml schedule create -f ./model-performance-monitoring.yaml
    ```

# [Python SDK](#tab/python)

After you satisfy the [prerequisites for model performance monitoring](#prerequisites-for-model-performance-monitoring), use the following Python code to set up model monitoring. First replace the following placeholders with appropriate values:

| Placeholder | Description | Example |
| --- | --- | --- |
| \<subscription-ID\> | The ID of your subscription | aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e |
| \<resource-group-name\> | The name of the resource group that contains your workspace | my-resource-group |
| \<workspace-name\> | The name of your workspace | my-workspace |
| \<production-data-asset-name\> | The name of the data asset that contains production data | credit-default-main-model_inputs |
| \<production-target-column\> | The name of the production column that contains values that the model predicts | DEFAULT_NEXT_MONTH |
| \<production-join-column\> | The name of the production column to use to join the production and ground truth data | correlationid |
| \<ground-truth-data-asset-name\> | The name of the data asset that contains ground truth data | credit-ground-truth |
| \<ground-truth-target-column\> | The name of the ground truth column that contains actual data that the model tries to predict | ground_truth|
| \<ground-truth-join-column\> | The name of the ground truth column to use to join the production and ground truth data | correlationid |
| \<email-address-1\> and \<email-address-2\> | Email addresses to use for notifications | `abc@example.com` |
| \<frequency-unit\> | The monitoring frequency unit | day |
| \<interval\> | The interval between jobs, expressed in the frequency unit | 1 |
| \<start-hour\> | The hour to start monitoring, on a 24-hour clock | 3 |
| \<start-minutes\> | The minutes after the specified hour to start monitoring | 15 |

```python
from azure.identity import DefaultAzureCredential
from azure.ai.ml import Input, MLClient
from azure.ai.ml.constants import (
    MonitorDatasetContext,
)
from azure.ai.ml.entities import (
    AlertNotification,
    BaselineDataRange,
    ModelPerformanceMetricThreshold,
    ModelPerformanceSignal,
    ModelPerformanceClassificationThresholds,
    MonitoringTarget,
    MonitorDefinition,
    MonitorSchedule,
    RecurrencePattern,
    RecurrenceTrigger,
    ServerlessSparkCompute,
    ReferenceData,
    ProductionData
)

# Get a handle to the workspace.
ml_client = MLClient(
    DefaultAzureCredential(),
    subscription_id="<subscription-ID>",
    resource_group_name="<resource-group-name>",
    workspace_name="<workspace-name>",
)

# Create a compute instance.
spark_compute = ServerlessSparkCompute(
    instance_type="standard_e4s_v3",
    runtime_version="3.4"
)

# Specify the type of the model task.
monitoring_target = MonitoringTarget(
    ml_task="classification",
)

# Specify production data that the model data collector generates. 
production_data = ProductionData(
    input_data=Input(
        type="uri_folder",
        path="azureml:<production-data-asset-name>:1"
    ),
    data_column_names={
        "target_column": "<production-target-column>",
        "join_column": "<production-join-column>"
    },
    data_window=BaselineDataRange(
        lookback_window_offset="P0D",
        lookback_window_size="P10D",
    )
)

# Specify the ground truth reference data.
reference_data_ground_truth = ReferenceData(
    input_data=Input(
        type="mltable",
        path="azureml:<ground-truth-data-asset-name>:1"
    ),
    data_column_names={
        "target_column": "<ground-truth-target-column>",
        "join_column": "<ground-truth-join-column>"
    },
    data_context=MonitorDatasetContext.GROUND_TRUTH_DATA,
)

# Create the model performance signal.
metric_thresholds = ModelPerformanceMetricThreshold(
    classification=ModelPerformanceClassificationThresholds(
        accuracy=0.50,
        precision=0.50,
        recall=0.50
    ),
)

model_performance = ModelPerformanceSignal(
    production_data=production_data,
    reference_data=reference_data_ground_truth,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Put all monitoring signals in a dictionary.
monitoring_signals = {
    'model_performance':model_performance,
}

# Create an alert notification object.
alert_notification = AlertNotification(
    emails=['<email-address-1>', '<email-address-2>']
)

# Set up the monitor definition.
monitor_definition = MonitorDefinition(
    compute=spark_compute,
    monitoring_target=monitoring_target,
    monitoring_signals=monitoring_signals,
    alert_notification=alert_notification
)

# Specify the schedule frequency.
recurrence_trigger = RecurrenceTrigger(
    frequency="<frequency-unit>",
    interval=<interval>,
    schedule=RecurrencePattern(hours=<start-hour>, minutes=<start-minutes>)
)

# Create the monitoring schedule.
model_monitor = MonitorSchedule(
    name="credit_default_model_performance",
    trigger=recurrence_trigger,
    create_monitor=monitor_definition
)

# Schedule the monitoring job.
poller = ml_client.schedules.begin_create_or_update(model_monitor)
created_monitor = poller.result()
```

# [Studio](#tab/azure-studio)

To set up model performance monitoring, complete the steps in the following sections.

### Configure basic settings

1. In [Azure Machine Learning studio](https://ml.azure.com), go to your workspace.

1. Under **Manage**, select **Monitoring**, and then select **Add**.

1. On the Basic settings page, enter the information as described earlier in [Set up out-of-box model monitoring](#set-up-out-of-box-model-monitoring).

### Add data assets

1. On the Basic settings page, select **Next** to open the Configure data asset page of the **Advanced settings** section.

1. Select **Add**, and then add the data asset that you want to use as the ground truth data asset. The ground truth data asset must have a unique ID column. Also, the values in the unique ID column of the ground truth data asset and the model output data asset must match. You can join these data assets together before metric computation occurs.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configure-data-asset.png" alt-text="Screenshot of the Configure data asset page. Two configured data assets are visible, and the Add button is highlighted." lightbox="media/how-to-monitor-models/model-monitoring-configure-data-asset.png":::

1. If you don't see your model output data asset in the list of added data assets, select **Add**, and then add it.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-added-ground-truth-data-asset.png" alt-text="Screenshot of the Configure data asset page. Ground truth, input, and output data assets are visible. Output and ground truth assets are highlighted." lightbox="media/how-to-monitor-models/model-monitoring-added-ground-truth-data-asset.png":::

### Add a performance monitoring signal

1. On **Configure data asset**, select **Next**. The **Select monitoring signals** page opens. If you're using an Azure Machine Learning online deployment, you see a list of monitoring signals.

1. Delete any monitoring signals that you see on the page. The focus of this section is to create a model performance monitoring signal.

1. Select **Add**.

1. In the **Edit Signal** window, select **Model performance (PREVIEW)**, and then take the following steps to configure the model performance signal:

    1. In step 1:
        1. For the production data asset, select your model output data asset.
        1. Select an appropriate target column, for example, `DEFAULT_NEXT_MONTH`.
        1. Select the look-back window size and offset that you want to use.
    1. In step 2:
        1. For the reference data asset, select your ground truth data asset.
        1. Select the target column, for example, `ground_truth`.
        1. Select the column to use for the join with the model output data asset, for example, `correlationid`. Both data assets should contain that column, and it should contain a unique ID for each row in the data asset.
    1. In step 3, select the performance metrics that you want to use, and specify their respective thresholds.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configure-model-performance.png" alt-text="Screenshot of the Edit Signal page. The Model performance tab is open, and three steps are visible that provide a way to configure various settings." lightbox="media/how-to-monitor-models/model-monitoring-configure-model-performance.png":::

1. Select **Save**. On the **Select monitoring signals** page, the model performance signal is visible.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-configured-model-performance-signal.png" alt-text="Screenshot of the Select monitoring signals page. A configured model performance signal is visible." lightbox="media/how-to-monitor-models/model-monitoring-configured-model-performance-signal.png":::

### Finish the configuration

1. On **Select monitoring signals**, select **Next**.

1. On **Notifications**, turn on notifications for the model performance signal, and then select **Next**.

1. On **Review monitoring settings**, review your settings.

    :::image type="content" source="media/how-to-monitor-models/model-monitoring-review-monitoring-details.png" alt-text="Screenshot of the Review monitoring details page. The basic settings, three configured data assets, and one configured performance signal are visible." lightbox="media/how-to-monitor-models/model-monitoring-review-monitoring-details.png":::

1. Select **Create** to create your model performance monitor.

---

## Set up model monitoring for production data

You can monitor models that you deploy to Azure Machine Learning batch endpoints or models you deploy outside Azure Machine Learning. If you don't have a deployment but you have production data, use the data to perform continuous model monitoring. To monitor these models, you must be able to:

* Collect production inference data from models deployed in production.
* Register the production inference data as an Azure Machine Learning data asset, and ensure continuous updates of the data.
* Provide a custom data preprocessing component and register it as an Azure Machine Learning component if you don't use the [data collector](how-to-collect-production-data.md) to collect data. Without this custom data preprocessing component, the Azure Machine Learning model monitoring system can't process your data into a tabular form that supports time windowing.

Your custom preprocessing component must have the following input and output signatures:

| Input or output | Signature name | Type | Description | Example value |
|---|---|---|---|---|
| input | `data_window_start` | literal, string | The data window start time in ISO8601 format | 2023-05-01T04:31:57.012Z |
| input | `data_window_end` | literal, string | The data window end time in ISO8601 format | 2023-05-01T04:31:57.012Z |
| input | `input_data` | uri_folder | The collected production inference data, which is registered as an Azure Machine Learning data asset | azureml:myproduction_inference_data:1 |
| output | `preprocessed_data` | mltable | A tabular data asset that matches a subset of the reference data schema | |

For an example of a custom data preprocessing component, see [custom_preprocessing in the azuremml-examples GitHub repo](https://github.com/Azure/azureml-examples/tree/main/cli/monitoring/components/custom_preprocessing).

For instructions on registering an Azure Machine Learning component, see [Register component in your workspace](how-to-create-component-pipelines-ui.md#register-a-component-in-your-workspace) .

After you register your production data and preprocessing component, you can set up model monitoring.

# [Azure CLI](#tab/azure-cli)

1. Create a monitoring definition YAML file that's similar to the following example. Before you use this definition, adjust the following settings and any other settings to meet the needs of your environment:

    - For `endpoint_deployment_id`, use a value in the format `azureml:<endpoint-name>:<deployment-name>`.
    - For `pre_processing_component`, use a value in the format `azureml:<component-name>:<component-version>`. Specify the exact version, such as `1.0.0`, not `1`.
    - For each `path`, use a value in the format `azureml:<data-asset-name>:<version>`.
    - For the `target_column` value, use the name of the output column that contains values that the model predicts.
    - Under `emails`, list the email addresses that you want to use for notifications.

    :::code language="yaml" source="~/azureml-examples-main/cli/monitoring/model-monitoring-with-collected-data.yaml":::

1. Run the following command to create the model.

    ```azurecli
    az ml schedule create -f ./model-monitoring-with-collected-data.yaml
    ```

# [Python SDK](#tab/python)

Use a script that's similar to the following Python code to set up model monitoring. First, replace the following placeholders with appropriate values:

| Placeholder | Description | Example |
| --- | --- | --- |
| \<subscription-ID\> | The ID of your subscription | aaaa0a0a-bb1b-cc2c-dd3d-eeeeee4e4e4e |
| \<resource-group-name\> | The name of the resource group that contains your workspace | my-resource-group |
| \<workspace-name\> | The name of your workspace | my-workspace |
| \<production-data-asset-name\> | The name of the data asset that contains production data | my_model_production_data |
| \<preprocessing-component-name\> | The name of your preprocessing component | production_data_preprocessing |
| \<training-data-asset-name\> | The name of the training data asset that you want to use as a reference data asset | my_model_training_data |
| \<email-address-1\> and \<email-address-2\> | Email addresses to use for notifications | `abc@example.com` |
| \<frequency-unit\> | The monitoring frequency unit | day |
| \<interval\> | The interval between jobs, expressed in the frequency unit | 1 |
| \<start-hour\> | The hour to start monitoring, on a 24-hour clock | 3 |
| \<start-minutes\> | The minutes after the specified hour to start monitoring | 15 |

```python
from azure.identity import InteractiveBrowserCredential
from azure.ai.ml import Input, MLClient
from azure.ai.ml.constants import (
    MonitorDatasetContext
)
from azure.ai.ml.entities import (
    AlertNotification,
    DataDriftSignal,
    DataQualitySignal,
    DataDriftMetricThreshold,
    DataQualityMetricThreshold,
    NumericalDriftMetrics,
    CategoricalDriftMetrics,
    DataQualityMetricsNumerical,
    DataQualityMetricsCategorical,
    MonitorFeatureFilter,
    MonitoringTarget,
    MonitorDefinition,
    MonitorSchedule,
    RecurrencePattern,
    RecurrenceTrigger,
    ServerlessSparkCompute,
    ReferenceData,
    ProductionData
)

# Get a handle to the workspace.
subscription_id = "<subscription-ID>"
resource_group = "<resource-group-name>"
workspace = "<workspace-name>"
ml_client = MLClient(
   InteractiveBrowserCredential(),
   subscription_id,
   resource_group,
   workspace
)

# Specify the compute instance.
spark_compute = ServerlessSparkCompute(
    instance_type="standard_e4s_v3",
    runtime_version="3.4"
)

# Specify the target data asset (the production data asset).
production_data = ProductionData(
    input_data=Input(
        type="uri_folder",
        path="azureml:<production-data-asset-name>:1"
    ),
    data_context=MonitorDatasetContext.MODEL_INPUTS,
    pre_processing_component="azureml:<preprocessing-component-name>:1.0.0"
)

# Specify the training data to use as a reference data asset.
reference_data_training = ReferenceData(
    input_data=Input(
        type="mltable",
        path="azureml:<training-data-asset-name>:1"
    ),
    data_context=MonitorDatasetContext.TRAINING
)

# Create an advanced data drift signal.
features = MonitorFeatureFilter(top_n_feature_importance=20)
metric_thresholds = DataDriftMetricThreshold(
    numerical=NumericalDriftMetrics(
        jensen_shannon_distance=0.01
    ),
    categorical=CategoricalDriftMetrics(
        pearsons_chi_squared_test=0.02
    )
)

advanced_data_drift = DataDriftSignal(
    production_data=production_data,
    reference_data=reference_data_training,
    features=features,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Create an advanced data quality signal.
features = ['feature_A', 'feature_B', 'feature_C']
metric_thresholds = DataQualityMetricThreshold(
    numerical=DataQualityMetricsNumerical(
        null_value_rate=0.01
    ),
    categorical=DataQualityMetricsCategorical(
        out_of_bounds_rate=0.02
    )
)

advanced_data_quality = DataQualitySignal(
    production_data=production_data,
    reference_data=reference_data_training,
    features=features,
    metric_thresholds=metric_thresholds,
    alert_enabled=True
)

# Put all monitoring signals in a dictionary.
monitoring_signals = {
    'data_drift_advanced': advanced_data_drift,
    'data_quality_advanced': advanced_data_quality
}

# Create an alert notification object.
alert_notification = AlertNotification(
    emails=['<email-address-1>', '<email-address-2>']
)

# Set up the monitor definition.
monitor_definition = MonitorDefinition(
    compute=spark_compute,
    monitoring_signals=monitoring_signals,
    alert_notification=alert_notification
)

# Specify the schedule frequency.
recurrence_trigger = RecurrenceTrigger(
    frequency="<frequency-unit>",
    interval=<interval>,
    schedule=RecurrencePattern(hours=<start-hour>, minutes=<start-minutes>)
)

# Create the monitoring schedule.
model_monitor = MonitorSchedule(
    name="fraud_detection_model_monitoring_advanced",
    trigger=recurrence_trigger,
    create_monitor=monitor_definition
)

# Schedule the monitoring job.
poller = ml_client.schedules.begin_create_or_update(model_monitor)
created_monitor = poller.result()

```

# [Studio](#tab/azure-studio)

The studio currently doesn't support configuring monitoring for models that are deployed outside Azure Machine Learning. See the Azure CLI or Python SDK tabs instead. 

After you use the Azure CLI or the Python SDK to configure monitoring, you can view the monitoring results in the studio. For more information about interpreting monitoring results, see [Interpret monitoring results](#interpret-monitoring-results).

---

## Set up model monitoring with custom signals and metrics

When you use Azure Machine Learning model monitoring, you can define a custom signal and implement any metric to monitor your model. You can register your custom signal as an Azure Machine Learning component. When your model monitoring job runs on its specified schedule, it computes the metrics that you define within your custom signal, just as it does for the data drift, prediction drift, and data quality prebuilt signals.

To set up a custom signal to use for model monitoring, first define the custom signal and register it as an Azure Machine Learning component. The Azure Machine Learning component must have the following input and output signatures.

### Component input signature

The component input data frame should contain the following items:

- An `mltable` structure that contains the processed data from the preprocessing component.
- Any number of literals, each representing an implemented metric as part of the custom signal component. For example, if you implement the `std_deviation` metric, you need an input for `std_deviation_threshold`. Generally, one input with the name `<metric-name>_threshold` exists per metric.

| Signature name | Type | Description | Example value |
|---|---|---|---|
| `production_data` | mltable | A tabular data asset that matches a subset of the reference data schema | |
| `std_deviation_threshold` | literal, string | The respective threshold for the implemented metric | 2 |

### Component output signature

The component output port uses the following signature:

| Signature name | Type | Description |
|---|---|---|
| `signal_metrics` | mltable | The mltable structure that contains the computed metrics. For the schema of this signature, see the next section, [signal_metrics schema](#signal_metrics-schema). |
  
#### signal_metrics schema

The component output data frame contains four columns: `group`, `metric_name`, `metric_value`, and `threshold_value`.

| Signature name | Type | Description | Example value |
|---|---|---|---|
| `group` | literal, string | The top-level logical grouping to apply to the custom metric | TRANSACTIONAMOUNT |
| `metric_name` | literal, string | The name of the custom metric | std_deviation |
| `metric_value` | numerical | The value of the custom metric | 44,896.082 |
| `threshold_value` | numerical | The threshold for the custom metric | 2 |

The following table shows example output from a custom signal component that computes the `std_deviation` metric:

| group | metric_value | metric_name | threshold_value |
|---|---|---|---|
| TRANSACTIONAMOUNT | 44,896.082 | std_deviation | 2 |
| LOCALHOUR | 3.983 | std_deviation | 2 |
| TRANSACTIONAMOUNTUSD | 54,004.902 | std_deviation | 2 |
| DIGITALITEMCOUNT | 7.238 | std_deviation | 2 |
| PHYSICALITEMCOUNT | 5.509 | std_deviation | 2 |

To see an example of a custom signal component definition and metric computation code, see [custom_signal in the azureml-examples repo](https://github.com/Azure/azureml-examples/tree/main/cli/monitoring/components/custom_signal).

For instructions on registering an Azure Machine Learning component, see [Register component in your workspace](how-to-create-component-pipelines-ui.md#register-a-component-in-your-workspace) .

# [Azure CLI](#tab/azure-cli)

After you create and register your custom signal component in Azure Machine Learning, take the following steps to set up model monitoring:

1. Create a monitoring definition in a YAML file that's similar to the following example. Before you use this definition, adjust the following settings and any others to meet the needs of your environment:

    - For `component_id`, use a value in the format `azureml:<custom-signal-name>:1.0.0`.
    - For `path` in the input data section, use a value in the format `azureml:<production-data-asset-name>:<version>`.
    - For `pre_processing_component`:
      - If you use the [data collector](how-to-collect-production-data.md) to collect your data, you can omit the `pre_processing_component` property.
      - If you don't use the data collector and want to use a component to preprocess production data, use a value in the format `azureml:<custom-preprocessor-name>:<custom-preprocessor-version>`.
    - Under `emails`, list the email addresses that you want to use for notifications.

    ```yml
    # custom-monitoring.yaml
    $schema:  http://azureml/sdk-2-0/Schedule.json
    name: my-custom-signal
    trigger:
      type: recurrence
      frequency: day # Possible frequency values include "minute," "hour," "day," "week," and "month."
      interval: 7 # Monitoring runs every day when you use the value 1.
    create_monitor:
      compute:
        instance_type: "standard_e4s_v3"
        runtime_version: "3.4"
      monitoring_signals:
        customSignal:
          type: custom
          component_id: azureml:my_custom_signal:1.0.0
          input_data:
            production_data:
              input_data:
                type: uri_folder
                path: azureml:my_production_data:1
              data_context: test
              data_window:
                lookback_window_size: P30D
                lookback_window_offset: P7D
              pre_processing_component: azureml:custom_preprocessor:1.0.0
          metric_thresholds:
            - metric_name: std_deviation
              threshold: 2
      alert_notification:
        emails:
          - abc@example.com
    ```

1. Run the following command to create the model:

    ```azurecli
    az ml schedule create -f ./custom-monitoring.yaml
    ```

# [Python SDK](#tab/python)

The Python SDK currently doesn't support monitoring for custom signals. See the Azure CLI tab instead.

# [Studio](#tab/azure-studio)

The studio currently doesn't support monitoring for custom signals. See the Azure CLI tab instead.

---

## Interpret monitoring results

After you configure your model monitor and the first run finishes, view the results in Azure Machine Learning studio.

1. In the studio, under **Manage**, select **Monitoring**. In the **Monitoring** page, select the name of your model monitor to see its overview page. This page shows the monitoring model, endpoint, and deployment. It also provides detailed information about configured signals. The following image shows a monitoring overview page that includes data drift and data quality signals.

    :::image type="content" source="media/how-to-monitor-models/monitoring-dashboard.png" alt-text="Screenshot of the monitoring page for a model, with Monitoring highlighted. Information about fail and pass rates is visible for two signals." lightbox="media/how-to-monitor-models/monitoring-dashboard.png":::

1. Look in the **Notifications** section of the overview page. In this section, you can see the feature for each signal that breaches the configured threshold for its respective metric.

1. In the **Signals** section, select **data_drift** to see detailed information about the data drift signal. On the details page, you can see the data drift metric value for each numerical and categorical feature that your monitoring configuration includes. If your monitor has more than one run, you see a trend line for each feature.

    :::image type="content" source="media/how-to-monitor-models/data-drift-details-page.png" alt-text="Screenshot that shows detailed information about the data drift signal, including a feature data drift chart and a feature breakdown." lightbox="media/how-to-monitor-models/data-drift-details-page.png":::

1. On the details page, select the name of an individual feature. A detailed view opens that shows the production distribution compared to the reference distribution. You can also use this view to track drift over time for the feature.

    :::image type="content" source="media/how-to-monitor-models/data-drift-individual-feature.png" alt-text="Screenshot that shows detailed information about a feature, including a histogram and a chart that shows drift over time." lightbox="media/how-to-monitor-models/data-drift-individual-feature.png":::

1. Return to the monitoring overview page. In the **Signals** section, select **data_quality** to view detailed information about this signal. On this page, you can see the null value rates, out-of-bounds rates, and data type error rates for each feature that you monitor.

    :::image type="content" source="media/how-to-monitor-models/data-quality-details-page.png" alt-text="Screenshot that shows detailed information about the data quality signal, including fail and pass rates and a feature breakdown." lightbox="media/how-to-monitor-models/data-quality-details-page.png":::

Model monitoring is a continuous process. When you use Azure Machine Learning model monitoring, you can configure multiple monitoring signals to obtain a broad view into the performance of your models in production.

## Integrate Azure Machine Learning model monitoring with Event Grid

When you use [Event Grid](how-to-use-event-grid.md), you can configure events that Azure Machine Learning model monitoring generates to trigger applications, processes, and CI/CD workflows. You can consume events through various event handlers, such as Azure Event Hubs, Azure Functions, and Azure Logic Apps. When your monitors detect drift, you can take action programmatically, such as by running a machine learning pipeline to retrain a model and redeploy it.

To integrate Azure Machine Learning model monitoring with Event Grid, take the steps in the following sections.

### Create a system topic

If you don't have an Event Grid system topic to use for monitoring, create one. For instructions, see [Create, view, and manage Event Grid system topics in the Azure portal](/azure/event-grid/create-view-manage-system-topics).

### Create an event subscription

1. In the Azure portal, go to your Azure Machine Learning workspace.

1. Select **Events**, and then select **Event Subscription**.

    :::image type="content" source="./media/how-to-monitor-models/add-event-subscription.png" alt-text="Screenshot that shows the Event page of an Azure Machine Learning workspace. Events and Event Subscription are highlighted.":::

1. Next to **Name**, enter a name for your event subscription, such as **MonitoringEvent**.

1. Under **Event Types**, select only **Run status changed**. 

    > [!WARNING]
    >
    > Select only **Run status changed** for the event type. Don't select **Dataset drift detected**, which applies to data drift v1, not Azure Machine Learning model monitoring.

1. Select the **Filters** tab. Under **Advanced Filters**, select **Add new filter**, and then enter the following values:

    - Under **Key**, enter `data.RunTags.azureml_modelmonitor_threshold_breached`.
    - Under **Operator**, select **String contains**.
    - Under **Value**, enter **has failed due to one or more features violating metric thresholds**.

    :::image type="content" source="media/how-to-monitor-models/add-advanced-filter.png" alt-text="Screenshot of the Create Event Description page in the Azure portal. The Filters tab and the values under Key, Operator, and Value are highlighted." lightbox="media/how-to-monitor-models/add-advanced-filter.png":::

    When you use this filter, events are generated when the run status of any monitor in your Azure Machine Learning workspace changes. The run status can change from completed to failed or from failed to completed.

    To filter at the monitoring level, select **Add new filter** again, and then enter the following values:

    - Under **Key**, enter `data.RunTags.azureml_modelmonitor_threshold_breached`.
    - Under **Operator**, select **String contains**.
    - Under **Value**, enter the name of a monitor signal that you want to filter events for, such as **credit_card_fraud_monitor_data_drift**. The name that you enter must match the name of your monitoring signal. Any signal that you use in filtering should have a name in the format `<monitor-name>_<signal-description>` that includes the monitor name and a description of the signal.

1. Select the **Basics** tab. Configure the endpoint that you want to serve as your event handler, such as Event Hubs.

1. Select **Create** to create the event subscription.

### View events

After you capture events, you can view them on the event handler endpoint page:

:::image type="content" source="media/how-to-monitor-models/events-on-endpoint-page.png" alt-text="Screenshot of an event subscription page that uses an Event Hubs endpoint and an Azure Machine Learning workspace topic. A chart is visible." lightbox="media/how-to-monitor-models/events-on-endpoint-page.png":::

You can also view events in the Azure Monitor **Metrics** tab: 

:::image type="content" source="media/how-to-monitor-models/events-in-azure-monitor-metrics-tab.png" alt-text="Screenshot of the Monitor metrics page. A line chart shows a total of three events in the past hour." lightbox="media/how-to-monitor-models/events-in-azure-monitor-metrics-tab.png":::

## Related content

- [Data collection from models in production](concept-data-collection.md)
- [CLI (v2) schedule YAML schema for model monitoring (preview)](reference-yaml-monitor.md)
- [Model monitoring for generative AI applications (preview)](./prompt-flow/how-to-monitor-generative-ai-applications.md)
