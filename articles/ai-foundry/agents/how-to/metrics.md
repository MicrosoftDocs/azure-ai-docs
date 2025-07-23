---
title: Monitor Azure AI Foundry Agent Service
description: Start here to learn how to use Azure Monitor to capture and analyze metrics for your Azure AI Foundry Agent Service.
ms.date: 07/23/2025
ms.custom: horz-monitor, subject-monitoring
ms.topic: conceptual
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
---

# Monitor Azure AI Foundry Agent Service

[!INCLUDE [horz-monitor-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-intro.md)]

Monitoring is available for agents in a [standard agent setup](../concepts/standard-agent-setup.md).

> [!IMPORTANT]
> Monitoring support is currently limited to Azure AI Foundry hubs. Azure AI Foundry projects are not supported.

## Dashboards

Azure AI Foundry Agent Service provides out-of-box dashboards. There are two key dashboards to monitor your resource: 

- The metrics dashboard in the AI Foundry resource view 
- The dashboard in the overview pane within the Azure portal 

To access the monitoring dashboards, sign in to the [Azure portal](https://portal.azure.com) and then select **Monitoring** in the left navigation menu, then click **Metrics**.


:::image type="content" source="../media/monitoring/dashboard.png" alt-text="Screenshot that shows out-of-box dashboards for a resource in the Azure portal." lightbox="../media/monitoring/dashboard.png" border="false":::

## Azure monitor platform metrics

Azure Monitor provides platform metrics for most services. These metrics are:

* Individually defined for each namespace.
* Stored in the Azure Monitor time-series metrics database.
* Lightweight and capable of supporting near real-time alerting.
* Used to track the performance of a resource over time.
* Collection: Azure Monitor collects platform metrics automatically. No configuration is required.

For a list of all metrics it's possible to gather for all resources in Azure Monitor, see [Supported metrics in Azure Monitor](/azure/azure-monitor/platform/metrics-supported).

## Azure AI Foundry Agent Service metrics
Azure AI Foundry Agent Service has commonality with a subset of Azure AI services. Here's a list of currently available metrics on Azure Monitor:

| Metric              | Description                                                                             | Name in REST API         | Unit        | Aggregation                            | Dimensions                                                      | Time Grains| DS Export |
|---------------------|-----------------------------------------------------------------------------------------|--------------------------|-------------|----------------------------------------|-----------------------------------------------------------------|-----------|
| Agent Events        | Number of events (create, delete, update) for AI Agents in this project                 | `AgentEvents`            | Count       | Average, Maximum, Minimum, Total (Sum) | `EventType`                                                     | PT1M      | No |
| Indexed Files Read  | Number of indexed files read by AI agents via file search in this project               | `AgentIndexedFilesRead`  | Count       | Average, Maximum, Minimum, Total (Sum) | `ErrorCode`, `Status`, `VectorStoreId`, `AgentId`               | PT1M      | No |
| Runs                | Number of runs by AI Agents in this project                                             | `AgentRuns`              | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `RunStatus`, `StatusCode`, `StreamType`, `ThreadId`  | PT1M      | No |
| User Message Events | Number of events (create, update delete) for user messages to AI Agents in this project | `AgentUserMessageEvents` | Count       | Average, Maximum, Minimum, Total (Sum) | `EventType`, `AgentId`, `ThreadId`                              | PT1M      | No |
| Thread Events       | Number of events (create, delete) for AI Agent threads in this project                  | `AgentThreadEvents`      | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `EventType`                                          | PT1M      | No |
| Input Tokens        | Number of prompt tokens processed (input) by AI Agents in this project                  | `AgentInputTokens`       | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ModelName`, `ModelVersion`                          | PT1M      | No |
| Output Tokens       | Number of tokens generated (output) by AI Agents in this project                        | `AgentOutputTokens`      | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ModelName`, `ModelVersion`                          | PT1M      | No |
| Total Tokens        | Sum of tokens processed (input) and generated (output) by AI Agents in this project     | `AgentTotalTokens`       | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ModelName`, `ModelVersion`                          | PT1M      | No |
| Tool Calls          | Number of tool calls made by AI Agents in this project                                  | `AgentToolCalls`         | Count       | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ToolName`                                           | PT1M      | No |

## Analyze monitoring data

There are many tools for analyzing monitoring data.

### Azure Monitor tools

Azure Monitor supports the [metrics explorer](/azure/azure-monitor/essentials/metrics-getting-started), a tool in the Azure portal that allows you to view and analyze metrics for Azure resources. For more information, see Analyze metrics with Azure Monitor metrics explorer.

## Azure Monitor export tools

You can get data out of Azure Monitor into other tools by using the [REST API for metrics](/rest/api/monitor/operation-groups) to extract metric data from the Azure Monitor metrics database. The API supports filter expressions to refine the data retrieved. For more information, see [Azure Monitor REST API reference](/rest/api/monitor/filter-syntax).

To get started with the REST API for Azure Monitor, see [Azure monitoring REST API walkthrough](/azure/azure-monitor/essentials/rest-api-walkthrough).

## Alerts

Azure Monitor alerts proactively notify you when specific conditions are found in your monitoring data. Alerts allow you to identify and address issues in your system before your customers notice them. For more information, see Azure Monitor alerts.

There are many sources of common alerts for Azure resources. [The Azure Monitor Baseline Alerts (AMBA)](https://aka.ms/amba) site provides a semi-automated method of implementing important platform metric alerts, dashboards, and guidelines. The site applies to a continually expanding subset of Azure services, including all services that are part of the Azure Landing Zone (ALZ).

The common alert schema standardizes the consumption of Azure Monitor alert notifications. For more information, see [Common alert schema](/azure/azure-monitor/alerts/alerts-common-schema).

[Metric alerts](/azure/azure-monitor/alerts/alerts-types#metric-alerts) evaluate resource metrics at regular intervals. Metric alerts can also apply multiple conditions and dynamic thresholds.

Every organization's alerting needs vary and can change over time. Generally, all alerts should be actionable and have a specific intended response if the alert occurs. If an alert doesn't require an immediate response, the condition can be captured in a report rather than an alert. Some use cases might require alerting anytime certain error conditions exist. In other cases, you might need alerts for errors that exceed a certain threshold for a designated time period.

Depending on what type of application you're developing with your use of Azure AI Foundry Agent Service, [Azure Monitor Application Insights](/azure/azure-monitor/overview) might offer more monitoring benefits at the application layer.

### Azure AI Foundry Agent Service alert rules

You can set alerts for any metric listed in the [monitoring data reference](../reference/monitor-service.md).

[!INCLUDE [horz-monitor-advisor-recommendations](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-advisor-recommendations.md)]

## Related content

- See [Monitoring data reference](../reference/monitor-service.md) for a reference of the metrics and other important values created for Azure AI Foundry Agent Service.
- See [Monitoring Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource) for general details on monitoring Azure resources.