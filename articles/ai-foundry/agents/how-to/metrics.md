---
title: Monitor Foundry Agent Service with Azure Monitor
description: Learn how to use Azure Monitor to view, analyze, and alert on platform metrics for Foundry Agent Service, including Log Analytics export and KQL queries.
ms.date: 02/03/2026
ms.custom: horz-monitor, subject-monitoring, pilot-ai-workflow-jan-2026
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# Monitor Foundry Agent Service with Azure Monitor

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [horz-monitor-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-intro.md)]

Monitoring is available for agents in a [standard agent setup](../concepts/standard-agent-setup.md).

[!INCLUDE [Feature preview](../../openai/includes/preview-feature.md)]

> [!IMPORTANT]
> Monitoring support is currently limited to Microsoft Foundry hubs. Foundry projects aren't supported.
>
> To learn about Foundry hubs and projects, see [What is Microsoft Foundry?](../../what-is-foundry.md) and [Migrate from hub-based to Foundry projects](../../how-to/migrate-project.md).

> [!NOTE]
> If you're using a Foundry project, use Foundry monitoring instead of Azure Monitor metrics.
>
> See [Monitor AI Agents with the Agent Monitoring Dashboard (preview)](../../default/observability/how-to/how-to-monitor-agents-dashboard.md).

## Prerequisites

- An agent running in a [standard agent setup](../concepts/standard-agent-setup.md).
- Access to the Azure resource you want to monitor. To view metrics, you need the **Monitoring Reader** role or equivalent permissions.
- To export metrics to Log Analytics or create alerts, you need the **Monitoring Contributor** role or equivalent permissions to create diagnostic settings and alert rules in your Azure subscription.

## Dashboards

Foundry Agent Service provides out-of-the-box dashboards. There are two key dashboards to monitor your resource:

- The metrics dashboard on the Foundry resource page.
- The dashboard in the overview pane in the Azure portal.

To access the monitoring dashboards, sign in to the [Azure portal](https://portal.azure.com), select your Agent Service resource, and then select **Monitoring** > **Metrics**.

:::image type="content" source="../media/monitoring/dashboard.png" alt-text="Screenshot that shows out-of-the-box dashboards for a resource in the Azure portal." lightbox="../media/monitoring/dashboard.png" border="false":::

## Data collection and routing in Azure Monitor

Azure Monitor collects platform metrics automatically for Azure resources. Platform metrics are stored in the Azure Monitor metrics database and are suitable for near real-time charts and metric alerts.

If you want to query metrics in Log Analytics, build workbooks, export to external systems, or retain data longer, configure diagnostic settings to route metrics to other destinations. For more information, see [Monitoring data from Azure resources](/azure/azure-monitor/essentials/monitor-azure-resource#monitoring-data-from-azure-resources) and [Create diagnostic settings to collect platform logs and metrics in Azure](/azure/azure-monitor/essentials/diagnostic-settings).

Platform metrics are retained for 93 days by default. If you route metrics to Log Analytics, retention depends on your workspace configuration.

Routing metrics to Log Analytics can increase costs. For more information, see [Azure Monitor Logs cost calculations and options](/azure/azure-monitor/logs/cost-logs).

## Azure Monitor platform metrics

Azure Monitor provides platform metrics for most services. These metrics are:

- Individually defined for each namespace.
- Stored in the Azure Monitor time-series metrics database.
- Lightweight and capable of supporting near real-time alerting.
- Used to track the performance of a resource over time.
- Collected automatically by Azure Monitor (no configuration required).

For a list of all metrics it's possible to gather for all resources in Azure Monitor, see [Supported metrics in Azure Monitor](/azure/azure-monitor/essentials/metrics-supported).

## Agent Service metrics

Agent Service shares a subset of metrics with other Foundry components. The following metrics are currently available in Azure Monitor:

| Metric | Name in REST API | Unit | Aggregation | Dimensions | Time grain |
|---|---|---:|---|---|---|
| Agents | `AgentEvents` | Count | Average, Maximum, Minimum, Total (Sum) | `EventType` | PT1M |
| Indexed files | `AgentIndexedFilesRead` | Count | Average, Maximum, Minimum, Total (Sum) | `ErrorCode`, `Status`, `VectorStoreId`, `AgentId` | PT1M |
| Runs | `AgentRuns` | Count | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `RunStatus`, `StatusCode`, `StreamType`, `ThreadId` | PT1M |
| Messages | `AgentUserMessageEvents` | Count | Average, Maximum, Minimum, Total (Sum) | `EventType`, `AgentId`, `ThreadId` | PT1M |
| Threads | `AgentThreadEvents` | Count | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `EventType` | PT1M |
| Tokens | `AgentTotalTokens` | Count | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ModelName`, `ModelVersion` | PT1M |
| Tool calls | `AgentToolCalls` | Count | Average, Maximum, Minimum, Total (Sum) | `AgentId`, `ToolName` | PT1M |

For metric definitions, see [Monitoring data reference](../reference/monitor-service.md).

## Analyze monitoring data

### Use Metrics Explorer in the Azure portal

Azure Monitor supports [Metrics Explorer](/azure/azure-monitor/essentials/metrics-getting-started), which lets you view and analyze metrics for Azure resources.

Common analysis tasks include:

- Filtering a chart by a dimension (for example, by `AgentId`).
- Splitting a chart by a dimension (for example, by `RunStatus` or `ToolName`).
- Changing the time range and aggregation to match your investigation needs.

### Verify you're receiving metrics

If you don't see data right away, confirm that metrics are flowing before you start deeper analysis:

- Generate activity for your agent (for example, create a run and send a few messages).
- In Metrics Explorer, chart at least one metric (for example, `AgentRuns`) for your Agent Service resource.
- If you exported metrics to Log Analytics, wait a few minutes for ingestion, and then run a basic `AzureMetrics` query.

### Export metrics with diagnostic settings

If you want to query metrics in Log Analytics or export them to other systems, configure diagnostic settings for the Agent Service resource and route metrics to one or more destinations.

To configure diagnostic settings in the Azure portal:

1. In the [Azure portal](https://portal.azure.com), open the Agent Service resource.
1. Under **Monitoring**, select **Diagnostic settings**.
1. Create a diagnostic setting and choose to export metrics to your destination (for example, a Log Analytics workspace).
1. Save the diagnostic setting.

After you save the setting, it appears in the **Diagnostic settings** list for the resource. Metrics typically begin flowing to the destination within a few minutes.

For more information, see [Create diagnostic settings to collect platform logs and metrics in Azure](/azure/azure-monitor/essentials/diagnostic-settings).

### Query metrics with Log Analytics (KQL)

After you route metrics to a Log Analytics workspace, you can query them with KQL.

The following query returns a sample of metric records:

```kusto
AzureMetrics
| take 100
| project TimeGenerated, MetricName, Total, Count, Maximum, Minimum, Average, TimeGrain, UnitName, ResourceId, Tags
```

To focus on Agent Service runs:

```kusto
AzureMetrics
| where MetricName == "AgentRuns"
| take 100
| project TimeGenerated, Total, ResourceId
```

For query fundamentals, see [Kusto Query Language (KQL) overview](/kusto/query/).

## Create alerts

Azure Monitor alerts notify you when conditions are met in your monitoring data. For more information, see [Alerts in Azure Monitor](/azure/azure-monitor/alerts/alerts-overview).

To create a metric alert rule:

1. In the [Azure portal](https://portal.azure.com), open the Agent Service resource.
1. Select **Monitoring** > **Alerts**.
1. Select **Create** > **Alert rule**.
1. Under **Condition**, select a metric (for example, `AgentRuns`).
1. If needed, use dimensions (for example, `RunStatus` or `StatusCode`) to scope the alert.
1. Configure the action group, severity, and evaluation frequency.
1. Select **Create**.

After you create the rule, it appears in the **Alert rules** list. The rule becomes active immediately and evaluates based on the frequency you configured.

For application-layer observability, see [Monitor your generative AI applications (preview)](../../how-to/monitor-applications.md).

## Troubleshooting

### No data appears in Metrics Explorer

- Confirm you're viewing the correct Agent Service resource.
- Expand the time range (for example, last 24 hours).
- Generate new activity (for example, create a run) and refresh the chart.
- Confirm you have permissions to view monitoring data for the resource.

### No data appears in Log Analytics

- Confirm you created diagnostic settings for the Agent Service resource and selected the correct destination.
- Wait a few minutes for ingestion, and then rerun your query.
- Confirm you have permissions to query the Log Analytics workspace.

## Next steps

- If you're using a Foundry project, see [Monitor AI Agents with the Agent Monitoring Dashboard (preview)](../../default/observability/how-to/how-to-monitor-agents-dashboard.md).
- For end-to-end debugging, see [Trace and observe AI agents in Foundry (preview)](../../how-to/develop/trace-agents-sdk.md).
- For metric definitions, see [Monitoring data reference](../reference/monitor-service.md).