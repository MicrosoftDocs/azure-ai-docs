---
title: Monitor model deployments in Azure AI model inference
description: Learn how to use Azure Monitor tools like Log Analytics to capture and analyze metrics and data logs for your Azure AI model inference.
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 4/30/2025
---

# Monitor model deployments in Azure AI model inference

When you have critical applications and business processes that rely on Azure resources, you need to monitor and get alerts for your system. The Azure Monitor service collects and aggregates metrics and logs from every component of your system, including Azure AI model inference model deployments. You can use this information to view availability, performance, and resilience, and get notifications of issues.

This document explains how you can use metrics and logs to monitor model deployments in Azure AI model inference.

## Prerequisites

To use monitoring capabilities for model deployments in Azure AI model inference, you need the following:

* An Azure AI services resource. For more information, see [Create an Azure AI Services resource](quickstart-create-resources.md).

    > [!TIP]
    > If you are using Serverless API Endpoints and you want to take advantage of monitoring capabilities explained in this document, [migrate your Serverless API Endpoints to Azure AI model inference](quickstart-ai-project.md).

* At least one model deployment.

* Access to diagnostic information for the resource.

## Metrics

Azure Monitor collects metrics from Azure AI model inference automatically. **No configuration is required**. These metrics are:

* Stored in the Azure Monitor time-series metrics database.
* Lightweight and capable of supporting near real-time alerting.
* Used to track the performance of a resource over time.

### Viewing metrics

Azure Monitor metrics can be queried using multiple tools, including:

#### Azure AI Foundry portal

You can view metrics within Azure AI Foundry portal. To view them, follow these steps:

1. Go to [Azure AI Foundry portal](https://ai.azure.com).

1. Navigate to your model deployment by selecting **Deployments**, and then select the name of the deployment you want to see metrics about.

1. Select the tab **Metrics**.

1. You can see a high level view of the most common metrics you may be interested about.

    :::image type="content" source="../media/monitor-models/deployment-metrics.png" alt-text="Screenshot showing the metrics displayed for model deployments in Azure AI Foundry portal." lightbox="../media/monitor-models/deployment-metrics.png":::

1. To slice, filter, or view model details about the metrics you can **Open in Azure Monitor**, where you have more advanced options.

    :::image type="content" source="../media/monitor-models/deployment-metrics-azmonitor.png" alt-text="Screenshot showing the option to open model deployment metrics in Azure Monitor." lightbox="../media/monitor-models/deployment-metrics-azmonitor.png":::

1. Use [Metrics explorer](#metrics-explorer) to analyze the metrics.

#### Metrics explorer

[Metrics explorer](/azure/azure-monitor/fundamentals/getting-started) is a tool in the Azure portal that allows you to view and analyze metrics for Azure resources. For more information, see Analyze metrics with Azure Monitor metrics explorer.

To use Azure Monitor, follow these steps:

1. Go to [Azure portal](https://portal.azure.com).

1. On the search box type and select **Monitor**.

1. Select **Metrics** in the left navigation bar.

1. On **Select scope**, select the resources you want to monitor. You can select either one resource or select a resource group or subscription. If that's the case, ensure you select **Resource types** as **Azure AI Services**.

1. The metric explorer shows. Select the [metrics](#metrics-reference) that you want to explore. The following example shows the number of requests made to the model deployments in the resource.

    :::image type="content" source="../media/monitor-models/azmon-add-metric.png" alt-text="Screenshot showing how to add a new metric to the chart." lightbox="../media/monitor-models/azmon-add-metric.png":::

    > [!IMPORTANT]
    > Metrics in category **Azure OpenAI** contains metrics for Azure OpenAI models in the resource. Category **Models** contains all the models available in the resource, including Azure OpenAI, DeepSeek, Phi, etc. We recommend switching to this new set of metrics.

1. You can add as many metrics as needed to either the same chart or to a new chart.

1. If you need, you can filter metrics by any of the available dimensions of it.

    :::image type="content" source="../media/monitor-models/azmon-add-filter.png" alt-text="Screenshot showing how to apply a filter to a metric." lightbox="../media/monitor-models/azmon-add-filter.png":::

1. It is useful to break down specific metrics by some of the dimensions. The following example shows how to break down the number of requests made to the resource by model by using the option **Add splitting**:

    :::image type="content" source="../media/monitor-models/azmon-add-splitting.png" alt-text="Screenshot showing how to split the metric by a given dimension." lightbox="../media/monitor-models/azmon-add-splitting.png":::

1. You can save your dashboards at any time to avoid having to configure them each time.


#### Kusto query language (KQL)

If you [configure diagnostic settings](#configure-diagnostic-settings) to send metrics to Log Analytics, you can use the Azure portal to query and analyze log data by using the Kusto query language (KQL). 

To query metrics, follow these steps:

1. Ensure you have [configure diagnostic settings](#configure-diagnostic-settings).

1. Go to [Azure portal](https://portal.azure.com).

1. Locate the Azure AI Services resource you want to query.

1. In the left navigation bar, navigate to **Monitoring** > **Logs**.

1. Select the Log Analytics workspace that you configured with diagnostics.

1. From the Log Analytics workspace page, under Overview on the left pane, select Logs. The Azure portal displays a Queries window with sample queries and suggestions by default. You can close this window.

1. To examine the Azure Metrics, use the table `AzureMetrics` for your resource, and run the following query:

    ```kusto
    AzureMetrics
    | take 100
    | project TimeGenerated, MetricName, Total, Count, Maximum, Minimum, Average, TimeGrain, UnitName
    ```

    > [!NOTE]
    > When you select **Monitoring** > **Logs** in the menu for your resource, Log Analytics opens with the query scope set to the current resource. The visible log queries include data from that specific resource only. To run a query that includes data from other resources or data from other Azure services, select **Logs** from the **Azure Monitor** menu in the Azure portal. For more information, see [Log query scope and time range in Azure Monitor Log Analytics](/azure/azure-monitor/logs/scope) for details.
    

#### Other tools

Tools that allow more complex visualization include:

* [Workbooks](/azure/azure-monitor/visualize/workbooks-overview), customizable reports that you can create in the Azure portal. Workbooks can include text, metrics, and log queries.
* [Grafana](/azure/azure-monitor/visualize/grafana-plugin), an open platform tool that excels in operational dashboards. You can use Grafana to create dashboards that include data from multiple sources other than Azure Monitor.
* [Power BI](/azure/azure-monitor/logs/log-powerbi), a business analytics service that provides interactive visualizations across various data sources. You can configure Power BI to automatically import log data from Azure Monitor to take advantage of these visualizations.

### Metrics reference

The following categories of metrics are available:

#### Models - Requests

| Metric | Internal name | Unit | Aggregation | Dimensions |
|--------|---------------|------|-------------|------------|
| **Model Availability Rate**<br /><br />Availability percentage with the following calculation: (Total Calls - Server Errors)/Total Calls. Server Errors include any HTTP responses >=500. | `ModelAvailabilityRate` | Percent | Minimum, Maximum, Average | `ApiName`, `OperationName`, `Region`, `StreamType`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Model Requests**<br /><br />Number of calls made to the model inference API over a period of time that resulted in a service error (>500). | `ModelRequests ` | Count | Total (Sum) | `ApiName`, `OperationName`, `Region`, `StreamType`, `ModelDeploymentName`, `ModelName`, `ModelVersion`, `StatusCode` |
| **Model Requests Service Errors**<br /><br />Number of calls made to the model inference API over a period of time that resulted in a service error (>500). | `ModelRequestsServiceErrors` | Total (Count) | `ApiName`, `OperationName`, `Region`, `StreamType`, `ModelDeploymentName`, `ModelName`, `ModelVersion`, `StatusCode` |

#### Models - Latency

| Metric | Internal name | Unit | Aggregation | Dimensions |
|--------|---------------|------|-------------|------------|
| **Time To Response**<br /><br />Recommended latency (responsiveness) measure for streaming requests. Applies to PTU and PTU-managed deployments. Calculated as time taken for the first response to appear after a user sends a prompt, as measured by the API gateway. This number increases as the prompt size increases and/or cache hit size reduces. Note: this metric is an approximation as measured latency is heavily dependent on multiple factors, including concurrent calls and overall workload pattern. In addition, it does not account for any client-side latency that may exist between your client and the API endpoint. Please refer to your own logging for optimal latency tracking. | `TimeToResponse` | Milliseconds | Maximum, Minimum, Average | `ApiName`, `OperationName`, `Region`, `StreamType`, `ModelDeploymentName`, `ModelName`, `ModelVersion`, `StatusCode` |
| **Normalized Time Between Tokens**<br /><br />For streaming requests; model token generation rate, measured in milliseconds. Applies to PTU and PTU-managed deployments. | `NormalizedTimeBetweenTokens` | Milliseconds | Maximum, Minimum, Average |  `ApiName`, `OperationName`, `Region`, `StreamType`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |

#### Models - Usage

| Metric | Internal name | Unit | Aggregation | Dimensions |
|--------|---------------|------|-------------|------------|
| **Input Tokens**<br /><br /> Number of prompt tokens processed (input) on a model. Applies to PTU, PTU-managed and Pay-as-you-go deployments. | `InputTokens` | Count | Total (Sum) | `ApiName`, `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Output Tokens**<br /><br /> Number of tokens generated (output) from a model. Applies to PTU, PTU-managed and Pay-as-you-go deployments. | `OutputTokens` | Count | Total (Sum) | `ApiName`, `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Total Tokens**<br /><br /> Number of inference tokens processed on a model. Calculated as prompt tokens (input) plus generated tokens (output). Applies to PTU, PTU-managed and Pay-as- you-go deployments. | `TotalTokens` | Count | Total (Sum) | `ApiName`, `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Tokens Cache Match Rate**<br /><br /> Percentage of prompt tokens that hit the cache. Applies to PTU and PTU-managed deployments. | `TokensCacheMatchRate` | Percentage | Average | `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Provisioned Utilization**<br /><br /> Utilization % for a provisoned-managed deployment, calculated as (PTUs consumed / PTUs deployed) x 100. When utilization is greater than or equal to 100%, calls are throttled and error code 429 returned. | `TokensCacheMatchRate ` | Percentage | Average | `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Provisioned Consumed Tokens**<br /><br /> Total tokens minus cached tokens over a period of time. Applies to PTU and PTU-managed deployments. | `ProvisionedConsumedTokens` | Count | Total (Sum) | `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Audio Input Tokens**<br /><br /> Number of audio prompt tokens processed (input) on a model. Applies to PTU-managed model deployments. | `AudioInputTokens` | Count | Total (Sum) | `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |
| **Audio Output Tokens**<br /><br /> Number of audio prompt tokens generated (output) on a model. Applies to PTU-managed model deployments. | `AudioOutputTokens` | Count | Total (Sum) | `Region`, `ModelDeploymentName`, `ModelName`, `ModelVersion` |


## Logs

Resource logs provide insight into operations that were done by an Azure resource. Logs are generated automatically, but you must route them to Azure Monitor logs to save or query by [configuring a diagnostic setting](#configure-diagnostic-settings). Logs are organized in categories when you create a diagnostic setting, you specify which categories of logs to collect.


## Configure diagnostic settings

All of the metrics are exportable with diagnostic settings in Azure Monitor. To analyze logs and metrics data with Azure Monitor Log Analytics queries, you need to configure diagnostic settings for your Azure AI Services resource. You need to perform this operation on each resource.

:::image type="content" source="../media/monitor-models/azmon-diagnostic.png" alt-text="Screenshot showing how to configure diagnostic logging in a resource.png":::

There's a cost for collecting data in a Log Analytics workspace, so only collect the categories you require for each service. The data volume for resource logs varies significantly between services.

