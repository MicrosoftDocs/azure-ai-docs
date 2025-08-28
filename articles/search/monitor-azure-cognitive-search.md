---
title: Monitor Azure AI Search
description: Start here to learn how to monitor Azure AI Search.
ms.date: 07/25/2025
ms.update-cycle: 365-days
ms.custom: horz-monitor
ms.topic: concept-article
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
---

# Monitor Azure AI Search

[!INCLUDE [horz-monitor-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-intro.md)]

[!INCLUDE [horz-monitor-resource-types](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-resource-types.md)]

For more information about the resource types for Azure AI Search, see [Azure AI Search monitoring data reference](monitor-azure-cognitive-search-data-reference.md).

[!INCLUDE [horz-monitor-data-storage](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-data-storage.md)]

[!INCLUDE [horz-monitor-platform-metrics](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-platform-metrics.md)]
In Azure AI Search, platform metrics measure query performance, indexing volume, and skillset invocation. For a list of available metrics for Azure AI Search, see [Azure AI Search monitoring data reference](monitor-azure-cognitive-search-data-reference.md#metrics).

To learn how to analyze query and index performance, see [Analyze performance in Azure AI Search](search-performance-analysis.md).

[!INCLUDE [horz-monitor-resource-logs](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-resource-logs.md)]

For the available resource log categories, their associated Log Analytics tables, and the logs schemas for Azure AI Search, see [Azure AI Search monitoring data reference](monitor-azure-cognitive-search-data-reference.md#resource-logs).

[!INCLUDE [horz-monitor-activity-log](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-activity-log.md)]

In Azure AI Search, activity logs reflect control plane activity such as service creation and configuration, or API key usage or management. Entries often include **Get Admin Key**, one entry for every call that [provided an admin API key](search-security-api-keys.md) on the request. There are no details about the call itself, just a notification that the admin key was used.

API keys can be disabled for data plane operations, such as creating or querying an index, but on the control plane they're used in the Azure portal to return service information. Control plane operations can request API keys so you continue to see key-related requests in the Activity log even if you disable key-based authentication.

The following screenshot shows Azure AI Search activity log signals you can configure in an alert.

:::image type="content" source="media/search-monitor-usage/activity-log-signals.png" alt-text="Screenshot of the activity log signals that can be used in an alert." border="true":::

For other entries, see the [Management REST API reference](/rest/api/searchmanagement/) for control plane activity that might appear in the log.

[!INCLUDE [horz-monitor-analyze-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-analyze-data.md)]

[!INCLUDE [horz-monitor-external-tools](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-external-tools.md)]

[!INCLUDE [horz-monitor-kusto-queries](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-kusto-queries.md)]

The following queries can get you started. See [Analyze performance in Azure AI Search](search-performance-analysis.md) for more examples and guidance specific to search service.

#### List metrics by name

Return a list of metrics and the associated aggregation. The query is scoped to the current search service over the time range that you specify.

```kusto
AzureMetrics
| project MetricName, Total, Count, Maximum, Minimum, Average
```

#### List operations by name

Return a list of operations and a count of each one.

```kusto
AzureDiagnostics
| summarize count() by OperationName
```

[!INCLUDE [horz-monitor-alerts](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-alerts.md)]

### Azure AI Search alert rules

The following table lists common and recommended alert rules for Azure AI Search. On a search service, throttling or query latency that exceeds a given threshold are the most commonly used alerts, but you might also want to be notified if a search service is deleted.

| Alert type | Condition | Description  |
|:---|:---|:---|
| Search Latency (metric alert) | Whenever the average search latency is greater than a user-specified threshold (in  seconds) | Send an SMS alert when average query response time exceeds the threshold. |
| Throttled search queries percentage (metric alert) | Whenever the total throttled search queries percentage is greater than or equal to a user-specified threshold | Send an SMS alert when dropped queries begin to exceed the threshold.|
| Delete Search Service (activity log alert) | Whenever the Activity Log has an event with Category='Administrative', Signal name='Delete Search Service (searchServices)', Level='critical' | Send an email if a search service is deleted in the subscription. |

[!INCLUDE [horz-monitor-advisor-recommendations](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-advisor-recommendations.md)]

## Related content

- [Azure AI Search monitoring data reference](monitor-azure-cognitive-search-data-reference.md)
- [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource)
- [Monitor queries](search-monitor-queries.md)
- [Monitor indexer-based indexing](search-monitor-indexers.md)
- [Visualize resource logs](search-monitor-logs-powerbi.md)
- [Analyze performance in Azure AI Search](search-performance-analysis.md)
- [Tips for better performance](search-performance-tips.md)
