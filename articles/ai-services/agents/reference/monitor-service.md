---
title: Monitoring data reference for Azure AI Foundry Agent Service
description: This article contains important reference material you need when you monitor Azure AI Foundry Agent Service by using Azure Monitor.
ms.date: 03/24/2025
ms.custom: horz-monitor, subject-monitoring
ms.topic: reference
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
---

# Azure AI Foundry Agent Service monitoring data reference

[!INCLUDE [horz-monitor-ref-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-intro.md)]

See [Monitor Azure AI Foundry Agent Service](../how-to/metrics.md) for details on the data you can collect on your agents.

## Metrics

Here are the most important metrics we think you should monitor for Azure AI Foundry Agent Service. Later in this article is a longer list of all available metrics which contains more details on metrics in this shorter list. _See the below list for most up to date information. We're working on refreshing the tables in the following sections._

- [Runs](#category-agents)
- [Indexed files](#category-agents)
<!-- - Indexed files -->

## Supported metrics

This section lists all the automatically collected platform metrics for this service. These metrics are also part of the global list of [all platform metrics supported in Azure Monitor](/azure/azure-monitor/reference/supported-metrics/metrics-index#supported-metrics-per-resource-type).

[!INCLUDE [horz-monitor-ref-metrics-tableheader](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-tableheader.md)]
[!INCLUDE [Microsoft.MachineLearningServices/workspaces](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/metrics/microsoft-machinelearningservices-workspaces-metrics-include.md)]

## Category: Agents


|Metric  |Name in REST API  |Unit  | Aggregation | Dimension | Time grains | DS Export |
|---------|---------|---------|---------|---------|---------|---------|
|Runs <br>  The number of runs in a given timeframe.     | `Runs`        | Count        | Total (sum), Average, Minimum, Maximum, Count        | `ResourceId`, `ProjectId`, `AgentId`, `StreamType`, `Region`, `StatusCode (successful, clienterrors, server errors)`, `RunStatus (started, completed, failed, cancelled, expired)` | PT1M | Yes |
|Indexed files <br> Number of files indexed for file search    |  `IndexedFiles`       | Count        |  Count, Average, Minimum, Maximum       | `ResourceId`, `ProjectId`, `VectorStoreId`, `StreamType`, `Region`, `Status`, `ErrorCode` | PT1M | Yes |


## Related content

- See [Monitor Azure AI Foundry Agent Service](../how-to/metrics.md) for a description of monitoring Azure AI Foundry Agent Service.
- See [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource) for details on monitoring Azure resources.
