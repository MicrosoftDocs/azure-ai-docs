---
title: Model monitoring in production
titleSuffix: Azure Machine Learning
description: Learn about monitoring the performance of models deployed to production on Azure Machine Learning, including lookback windows, monitoring signals, and metrics.
services: machine-learning
author: s-polly
ms.author: scottpolly
ms.service: azure-machine-learning
ms.subservice: mlops
ms.reviewer: jturuk
ms.topic: concept-article
ms.date: 01/27/2026
ms.custom: devplatv2, FY25Q1-Linter
#Customer intent: As a data scientist, I want to understand Azure Machine Learning monitoring so I can keep my machine learning models fresh and performant.
---

# Azure Machine Learning model monitoring

Model monitoring is the last step in the machine learning end-to-end lifecycle. This step tracks model performance in production and analyzes the performance from both data science and operational perspectives. In this article, you learn about model monitoring in Azure Machine Learning, the signals and metrics you can monitor, and recommended practices for model monitoring.

Unlike traditional software systems, machine learning system behavior doesn't only depend on rules specified in code, but is also learned from data. Data distribution changes, training-serving skew, data quality problems, shifts in environments, and consumer behavior changes can all cause a model to become stale.

When a model becomes stale, its performance can degrade to the point that it fails to add business value or starts to cause serious compliance problems in highly regulated environments. Therefore, it's important to monitor model performance.

## How Azure Machine Learning model monitoring works

To implement monitoring, Azure Machine Learning acquires monitoring signals by performing statistical computations on streamed production inference data and reference data. Production inference data refers to the model's input and output data collected in production. Reference data can be historical training, validation, or ground truth data.

Each monitoring signal has one or more metrics. You can set thresholds for these metrics to trigger alerts about model or data anomalies via Azure Machine Learning or Azure Event Grid. When you receive alerts, you can use Azure Machine Learning studio to analyze or troubleshoot monitoring signals for continuous model quality improvement.

Azure Machine Learning uses the following process to handle a built-in monitoring signal, such as data drift, for a model in production:

- First, Azure Machine Learning calculates the statistical distribution of the feature's value in the training data. This distribution is the baseline distribution for the feature.

- Next, Azure Machine Learning calculates the statistical distribution of the feature's latest values recorded in production.

- Azure Machine Learning then performs a statistical test or calculates a distance score to compare the distribution of the feature's latest values in production with the baseline distribution. If the test statistic or distance score between the two distributions exceeds a user-specified threshold, Azure Machine Learning identifies the anomaly and notifies the user.

### Set up and use model monitoring

To use model monitoring in Azure Machine Learning:

First, **enable production inference data collection.**
- If you deploy a model to an Azure Machine Learning online endpoint, you can enable production inference data collection by using Azure Machine Learning [model data collection](concept-data-collection.md).
- If you deploy a model outside of Azure Machine Learning or to an Azure Machine Learning batch endpoint, you're responsible for collecting production inference data that you can then use for Azure Machine Learning model monitoring.

Next, **set up model monitoring.** You can use Azure Machine Learning SDK/CLI 2.0 or the studio UI to easily set up model monitoring. During setup, you can specify your preferred monitoring signals and customize metrics and thresholds for each signal.

Finally, **view and analyze model monitoring results.** Once you set up model monitoring, Azure Machine Learning runs a monitoring job on your specified schedule. Each run computes and evaluates metrics for all selected monitoring signals and triggers alert notifications when any specified threshold is exceeded. You can follow the link in the alert notification to view and analyze monitoring results in your Azure Machine Learning workspace.

## Capabilities of model monitoring 

Azure Machine Learning provides the following capabilities for continuous model monitoring:

- **Built-in monitoring signals** for tabular data, including data drift, prediction drift, data quality, feature attribution drift, and model performance.
- **Out-of-box model monitoring for online endpoints**. If you deploy your model to production in an online endpoint, Azure Machine Learning collects production inference data automatically and uses it for continuous monitoring.
- **Multiple monitoring signals** in one monitoring setup. For each monitoring signal, you can select your preferred metrics and alert threshold.
- **Choice of reference data for comparison**. For monitoring signals, you can set reference data using training data or recent past production data.
- **Top N features for data drift or data quality monitoring**. If you use training data as the reference data, you can define data drift or data quality signals layered over feature importance.
- **Ability to define custom monitoring signals**. If the built-in monitoring signals aren't suitable for your business scenario, you can define your own monitoring signal with a custom monitoring signal component.
- **Flexibility to use production inference data from any source**. If you deploy models outside of Azure Machine Learning or deploy models to batch endpoints, you can still collect production inference data yourself to use in Azure Machine Learning model monitoring.

## Best practices for model monitoring

Each machine learning model and its use cases are unique. Therefore, model monitoring is unique for each situation. The following list describes recommended best practices for model monitoring.

- **Start model monitoring immediately after you deploy a model to production.**
- **Work with data scientists who are familiar with the model to set up monitoring.** Data scientists who have insight into the model and its use cases can recommend monitoring signals and metrics and set the right alert thresholds for each metric to avoid alert fatigue.
- **Include multiple monitoring signals in your setup.** With multiple monitoring signals, you get both broad and granular monitoring views. For example, you can combine data drift and feature attribution drift signals to get early warnings about model performance problems.
- **Use appropriate reference data as the comparison baseline.** For reference data used as the comparison baseline, you can use recent past production data or historical data, such as training or validation data. For more meaningful comparison, use training data as the comparison baseline for data drift and data quality. Use validation data as the comparison baseline for prediction drift.
- **Specify monitoring frequency based on production data growth over time**. For example, if your production model has heavy daily traffic and the daily data accumulation is sufficient, set the monitoring frequency to daily. Otherwise, consider a weekly or monthly monitoring frequency based on the growth of your production data over time.
- **Monitor top N features or a feature subset.** If you use training data as the comparison baseline, you can easily configure data drift monitoring or data quality monitoring for the top N important features. For models that have a large number of features, consider monitoring a subset of those features to reduce computation cost and monitoring noise.
- **Use the model performance signal when you have access to ground truth data.** If you have access to ground truth data, also called actuals, based on your machine learning application, use the model performance signal to compare the ground truth data to model output. This comparison provides an objective view of model performance in production.

## Lookback window size and offset

The *lookback window size* is the duration of time in ISO 8601 format for your production or reference data window. The *lookback window offset* is the duration of time to offset the end of your data window from the date of your monitoring run.

For example, your model in production has a monitor set to run on January 31 at 3:15 PM UTC. A production data lookback window size of `P7D` or seven days and a data lookback window offset of `P0D` or zero days means the monitor uses production data from January 24 at 3:15 PM UTC up until January 31 at 3:15 PM UTC, the time your monitor runs.

For the reference data, if you set the lookback window offset to `P7D` or seven days, the reference data window ends right before the production data window starts, so that there's no overlap. You can then set your reference data lookback window size to be as large as you like.

For example, if you set the reference data lookback window size to `P24D` or 24 days, the reference data window includes data from January 1 at 3:15 PM UTC up until January 24 at 3:15 PM UTC. The following diagram illustrates this example.

:::image type="content" source="media/how-to-monitor-models/monitoring-period.png" alt-text="A diagram showing the lookback window size and offset for reference and production data." border="false" lightbox="media/how-to-monitor-models/monitoring-period.png"::: 

In some cases, it might be useful to set the lookback window offset for your production data to a number greater than zero days. For example, if your monitor is scheduled to run weekly on Mondays at 3:15 PM UTC, but you don't want to use data from the weekend in your monitoring run, you can use a lookback window size of `P5D` or five days and a lookback window offset of `P2D` or two days. Your data window then starts on the prior Monday at 3:15 PM UTC and ends on Friday at 3:15 PM UTC.

In practice, you should ensure that the reference data window and the production data window don't overlap. As shown in the following figure, you can ensure nonoverlapping windows by making sure that the reference data lookback window offset, `P10D` or 10 days in this example, is greater or equal to the sum of the production data lookback window size and its lookback window offset, seven days total in this example.

:::image type="content" source="media/how-to-monitor-models/lookback-overlap.png" alt-text="A diagram showing nonoverlapping reference data and production data windows." border="false" lightbox="media/how-to-monitor-models/lookback-overlap.png":::

With Azure Machine Learning model monitoring, you can use smart defaults for your lookback window size and lookback window offset, or you can customize them to meet your needs. Both rolling windows and fixed windows are supported.

### Customize lookback window size

You have the flexibility to select a lookback window size for both the production data and the reference data.

- By default, the lookback window size for production data is your monitoring frequency. All data collected in the monitoring period before the monitoring job runs is included in the lookback window. Use the `production_data.data_window.lookback_window_size` property to adjust the rolling data window for production data.

- By default, the lookback window for the reference data is the full dataset. Use the `reference_data.data_window.lookback_window_size` property to adjust the reference lookback window size.

To specify a fixed data window for the reference data, use the properties `reference_data.data_window.window_start_date` and `reference_data.data_window.window_end_date`.

### Customize lookback window offset

You can select a lookback window offset for your data window for both the production data and the reference data. Use the offset for granular control over the data your monitor uses. The offset applies only to the rolling data windows.

- By default, the offset for production data is `P0D` or zero days. Modify this offset by using the `production_data.data_window.lookback_window_offset` property.

- By default, the offset for reference data is two times the `production_data.data_window.lookback_window_size`. This setting ensures that there's enough reference data for statistically meaningful monitoring results. Modify this offset by using the `reference_data.data_window.lookback_window_offset` property.

## Monitoring signals and metrics

Azure Machine Learning model monitoring supports the following monitoring signals and metrics.

[!INCLUDE [machine-learning-preview-items-disclaimer](includes/machine-learning-preview-items-disclaimer.md)]

|Monitoring signal | Description | Metrics | Model tasks or supported data format | Production data | Reference data |
|--|--|--|--|--|--|
| Data drift | Tracks changes in the distribution of a model's input data by comparing the distribution to the model's training data or recent production data. | Jensen-Shannon Distance, Population Stability Index, Normalized Wasserstein Distance, Two-Sample Kolmogorov-Smirnov Test, Pearson's Chi-Squared Test | Classification (tabular data), Regression (tabular data) | Production data: Model inputs | Recent past production data or training data |
| Prediction drift | Tracks changes in the distribution of a model's predicted outputs by comparing the distribution to validation data, labeled test data, or recent production data. | Jensen-Shannon Distance, Population Stability Index, Normalized Wasserstein Distance, Chebyshev Distance, Two-Sample Kolmogorov-Smirnov Test, Pearson's Chi-Squared Test | Classification (tabular data), Regression (tabular data) | Production data: Model outputs | Recent past production data or validation data |
| Data quality | Tracks the data integrity of a model's input by comparing it to the model's training data or recent production data. The data quality checks include checking for null values, type mismatch, or out-of-bounds values. | Null value rate, Data type error rate, Out-of-bounds rate | Classification (tabular data), Regression (tabular data) | Production data: Model inputs | Recent past production data or training data |
| Feature attribution drift (preview) | Based on the contribution of features to predictions, also known as feature importance. Feature attribution drift tracks feature importance during production by comparing it with feature importance during training.| Normalized discounted cumulative gain | Classification (tabular data), Regression (tabular data) | Production data: Model inputs and outputs | Training data (required) |
| Model performance: Classification (preview) | Tracks the objective performance of a model's output in production by comparing it to collected ground truth data. | Accuracy, Precision, and Recall | Classification (tabular data) | Production data: Model outputs | Ground truth data (required) |
| Model performance: Regression (preview) | Tracks the objective performance of a model's output in production by comparing it to collected ground truth data. | Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE) | Regression (tabular data) | Production data: Model outputs | Ground truth data (required) |
|[Generative AI: Generation safety and quality](prompt-flow/how-to-monitor-generative-ai-applications.md) (preview)|Evaluates generative AI applications for safety and quality, using GPT-assisted metrics.| Groundedness, Relevance, Fluency, Similarity, Coherence| Questions & Answers | Prompt, completion, context, and annotation template |N/A|

### Data quality metrics

The data quality monitoring signal tracks the integrity of a model's input data by calculating the following three metrics:

- Null value rate
- Data type error rate
- Out-of-bounds rate

Azure Machine Learning model monitoring supports up to 0.00001 precision for calculations of the null value rate, data type error rate, and out-of-bounds rate.

#### Null value rate

The null value rate is the rate of null values in the model input for each feature. For example, if the monitoring production data window contains 100 rows, and the value for the `temperature` feature is null for 10 of those rows, the null value rate for `temperature` is 10%.

Azure Machine Learning supports calculating the null value rate for all feature data types.

#### Data type error rate

During each monitoring run, Azure Machine Learning model monitoring infers the data type for each feature from the reference data. The data type error rate is the rate of data type differences between the current production data window and the reference data.

For example, if the data type for the `temperature` feature is inferred to be `IntegerType` from the reference data, but in the production data window, 10 out of 100 values for `temperature` aren't `IntegerType` but are strings, the data type error rate for `temperature` is  10%.

Azure Machine Learning supports calculating the data type error rate for the following data types that are available in PySpark: `ShortType`, `BooleanType`, `BinaryType`, `DoubleType`, `TimestampType`, `StringType`, `IntegerType`, `FloatType`, `ByteType`, `LongType`, and `DateType`. If the data type for a feature isn't in this list, Azure Machine Learning model monitoring still runs, but doesn't compute the data type error rate for that feature.

#### Out-of-bounds rate

During each monitoring run, Azure Machine Learning model monitoring determines the acceptable range or set for each feature from the reference data. The out-of-bounds rate is the rate of values for each feature that fall outside of the appropriate range or set determined by the reference data.

- For numerical features, the appropriate range is the numerical interval between the minimum and maximum values in the reference dataset, such as `[0, 100]`.
- For categorical features, such as `color`, the appropriate range is a set of all values contained in the reference dataset, such as `[red, yellow, green]`.

For example, if you have a numerical `temperature` feature where all values in the reference dataset fall within the range `[37, 77]`, but 10 out of 100 values for `temperature` in the production data window fall outside the range `[37, 77]`, the out-of-bounds rate for `temperature` is 10%.

Azure Machine Learning supports calculating the out-of-bounds rate for the following data types that are available in PySpark: `StringType`, `IntegerType`, `DoubleType`, `ByteType`, `LongType`, and `FloatType`. If the data type for a feature isn't in this list, Azure Machine Learning model monitoring still runs, but doesn't compute the out-of-bounds rate for that feature.

## Model monitoring integration with Azure Event Grid

By using events generated by Azure Machine Learning model monitoring runs, you can set up event-driven applications, processes, or continuous integration/continuous delivery (CI/CD) workflows with [Azure Event Grid](how-to-use-event-grid.md). When your model monitor detects drift, data quality problems, or model performance degradation, you can track these events with Event Grid and take action programmatically.

For example, if the accuracy of your classification model in production dips below a certain threshold, you can use Event Grid to begin a retraining job that uses collected ground truth data. For more information about integrating Azure Machine Learning with Event Grid, see [Monitor performance of models deployed to production](how-to-monitor-model-performance.md).

## Model monitoring authentication options

Azure Machine Learning model monitoring supports both credential-based and credential-less authentication to the datastore with the collected production inference data from your model. To configure credential-less authentication, follow these steps:

1. Create a User-Assigned Managed Identity (UAMI) and attach it to your Azure Machine Learning workspace.
1. Grant the UAMI [proper permissions](how-to-identity-based-service-authentication.md#user-assigned-managed-identity) to access your datastore.
1. Update the value of the workspace level property `systemDatastoresAuthMode` to `'identity'`.

Alternatively, add credentials to the datastore where your production inference data is stored.

For more information about credential-less authentication with Azure Machine Learning, see [User-assigned managed identity](how-to-identity-based-service-authentication.md#user-assigned-managed-identity).

## Model monitoring limitations

Azure Machine Learning model monitoring has the following limitations:

- It doesn't support the `AllowOnlyApprovedOutbound` managed virtual network isolation setting. For more information about managed virtual network isolation in Azure Machine Learning, see [Workspace Managed Virtual Network Isolation](how-to-managed-network.md).

- It depends on `Spark` to compute metrics over large-scale datasets. Because `MLTable` isn't well-supported by `Spark`, avoid using `MLTable` whenever possible with model monitoring jobs. Only basic `MLTable` files have guaranteed support. For complex or custom operations, consider using the `Spark` API directly in your code.

## Related content

- [Model data collection](concept-data-collection.md)
- [Collect production inference data](how-to-collect-production-data.md)
- [Model monitoring for generative AI applications](prompt-flow/how-to-monitor-generative-ai-applications.md)