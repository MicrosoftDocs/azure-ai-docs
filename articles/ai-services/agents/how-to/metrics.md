---
title: Monitor Azure AI Foundry Agent Service
description: Start here to learn how to use Azure Monitor to capture and analyze metrics for your Azure AI Foundry Agent Service.
ms.date: 03/20/2025
ms.custom: horz-monitor, subject-monitoring
ms.topic: conceptual
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
---

# Monitor Azure AI Foundry Agent Service

[!INCLUDE [horz-monitor-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-intro.md)]

Monitoring is available for agents in a [standard agent setup](../how-to/).

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

Azure AI Foundry Agent Service has commonality with a subset of Azure AI services. For a list of available metrics for Azure AI Foundry Agent Service, see the [monitoring data reference](../reference/monitor-service.md#metrics).

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