---
title: Monitor Azure AI Agent Service
description: Start here to learn how to use Azure Monitor tools like Log Analytics to capture and analyze metrics and data logs for your Azure AI Agent Service.
ms.date: 03/20/2025
ms.custom: horz-monitor, subject-monitoring
ms.topic: conceptual
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
---

# Monitor Azure AI Agent Service

[!INCLUDE [horz-monitor-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-intro.md)]

Monitoring is available for agents in a [standard agent setup](../quickstart.md?pivots=programming-language-csharp#choose-basic-or-standard-agent-setup).

## Dashboards

Azure AI Agent Service provides out-of-box dashboards. There are two key dashboards to monitor your resource: 

- The metrics dashboard in the AI Foundry resource view 
- The dashboard in the overview pane within the Azure portal 

To access the monitoring dashboards, sign in to the [Azure portal](https://portal.azure.com) and then select **Monitoring** in the left navigation menu, then click **Metrics**.


:::image type="content" source="../media/monitoring/dashboard.png" alt-text="Screenshot that shows out-of-box dashboards for a resource in the Azure portal." lightbox="../media/monitoring/dashboard.png" border="false":::


## Data collection and routing in Azure Monitor

Azure AI Agent Service collects the same kinds of monitoring data as other Azure resources. You can configure Azure Monitor to generate data in activity logs, resource logs, virtual machine logs, and platform metrics. For more information, see [Monitoring data from Azure resources](/azure/azure-monitor/essentials/monitor-azure-resource#monitoring-data-from-azure-resources).

Platform metrics and the Azure Monitor activity log are collected and stored automatically. This data can be routed to other locations by using a diagnostic setting. Azure Monitor resource logs aren't collected and stored until you create a diagnostic setting and then route the logs to one or more locations.

When you create a diagnostic setting, you specify which categories of logs to collect. For more information about creating a diagnostic setting by using the Azure portal, the Azure CLI, or PowerShell, see [Create diagnostic setting to collect platform logs and metrics in Azure](/azure/azure-monitor/platform/diagnostic-settings).

Keep in mind that using diagnostic settings and sending data to Azure Monitor Logs has other costs associated with it. For more information, see [Azure Monitor Logs cost calculations and options](/azure/azure-monitor/logs/cost-logs).

The metrics and logs that you can collect are described in the following sections.

[!INCLUDE [horz-monitor-resource-types](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-resource-types.md)]

For more information about the resource types, see the [monitoring data reference](../reference/monitor-service.md).

[!INCLUDE [horz-monitor-data-storage](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-data-storage.md)]

[!INCLUDE [horz-monitor-platform-metrics](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-platform-metrics.md)]

Azure AI Agent Service has commonality with a subset of Azure AI services. For a list of available metrics for Azure AI Agent Service, see the [monitoring data reference](../reference/monitor-service.md#metrics).

[!INCLUDE [horz-monitor-analyze-data](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-analyze-data.md)]

### Configure diagnostic settings

All of the metrics are exportable with [diagnostic settings in Azure Monitor](/azure/azure-monitor/essentials/diagnostic-settings). To analyze logs and metrics data with Azure Monitor Log Analytics queries, you need to configure diagnostic settings for your Azure resource and your Log Analytics workspace.

:::image type="content" source="../media/monitoring/diagnostic-settings.png" alt-text="Screenshot that shows how to open the Diagnostic setting page for a resource in the Azure portal." lightbox="../media/monitoring/diagnostic-settings.png":::

After you configure the diagnostic settings, you can work with metrics and log data for your resource in your Log Analytics workspace.

[!INCLUDE [horz-monitor-external-tools](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-external-tools.md)]

## Alerts

Azure Monitor alerts proactively notify you when specific conditions are found in your monitoring data. Alerts allow you to identify and address issues in your system before your customers notice them. For more information, see Azure Monitor alerts.

There are many sources of common alerts for Azure resources. [The Azure Monitor Baseline Alerts (AMBA)](https://aka.ms/amba) site provides a semi-automated method of implementing important platform metric alerts, dashboards, and guidelines. The site applies to a continually expanding subset of Azure services, including all services that are part of the Azure Landing Zone (ALZ).

The common alert schema standardizes the consumption of Azure Monitor alert notifications. For more information, see [Common alert schema](/azure/azure-monitor/alerts/alerts-common-schema).

[Metric alerts](/azure/azure-monitor/alerts/alerts-types#metric-alerts) evaluate resource metrics at regular intervals. Metrics can be platform metrics, custom metrics, logs from Azure Monitor converted to metrics, or Application Insights metrics. Metric alerts can also apply multiple conditions and dynamic thresholds.

Every organization's alerting needs vary and can change over time. Generally, all alerts should be actionable and have a specific intended response if the alert occurs. If an alert doesn't require an immediate response, the condition can be captured in a report rather than an alert. Some use cases might require alerting anytime certain error conditions exist. In other cases, you might need alerts for errors that exceed a certain threshold for a designated time period.

Depending on what type of application you're developing with your use of Azure AI Agent Service, [Azure Monitor Application Insights](/azure/azure-monitor/overview) might offer more monitoring benefits at the application layer.

### Azure AI Agent service alert rules

You can set alerts for any metric listed in the [monitoring data reference](../reference/monitor-service.md).

[!INCLUDE [horz-monitor-advisor-recommendations](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-advisor-recommendations.md)]

## Related content

- See [Monitoring data reference](../reference/monitor-service.md) for a reference of the metrics and other important values created for Azure AI Agent Service.
- See [Monitoring Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource) for general details on monitoring Azure resources.