---
title: Monitoring data reference for Azure OpenAI
description: This article contains important reference material you need when you monitor Azure OpenAI in Microsoft Foundry Models by using Azure Monitor.
ms.date: 11/26/2025
ms.custom: horz-monitor, subject-monitoring
ms.topic: reference
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-foundry
monikerRange: 'foundry-classic || foundry'
ms.subservice: azure-ai-foundry-openai
---

# Azure OpenAI monitoring data reference

[!INCLUDE [horz-monitor-ref-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-intro.md)]

See [Monitor Azure OpenAI](./how-to/monitor-openai.md) for details on the data you can collect for Azure OpenAI in Microsoft Foundry Models and how to use it.

[!INCLUDE [horz-monitor-ref-metrics-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-intro.md)]

### Supported metrics for Microsoft.CognitiveServices/accounts

Here are the most important metrics we think you should monitor for Azure OpenAI. Later in this article is a longer list of all available metrics for this namespace which contains more details on metrics in this shorter list. _Please see below list for most up to date information. We're working on refreshing the tables in the following sections._

- Azure OpenAI Requests
- Active Tokens
- Generated Completion Tokens
- Processed FineTuned Training Hours
- Processed Inference Tokens
- Processed Prompt Tokens
- Provisioned-managed Utilization V2
- Prompt Token Cache Match Rate
- Time to Response
- Time Between Tokens
- Time to Last Byte
- Normalized Time to First Byte
- Tokens per Second

You can also monitor Content Safety metrics that are used by other related services. 
- Blocked Volume
- Harmful Volume Detected
- Potential Abusive User Count
- Safety System Event
- Total Volume Sent for Safety Check 

> [!NOTE]
> The **Provisioned-managed Utilization** metric is now deprecated and is no longer recommended. This metric has been replaced by the **Provisioned-managed Utilization V2** metric.
> Tokens per Second, Time to Response, Time Between Tokens are currently not available for Standard deployments. 

Cognitive Services metrics have the category **Cognitive Services - HTTP Requests** in the following table. These metrics are legacy metrics that are common to all resources of this type. Microsoft no longer recommends that you use these metrics with Azure OpenAI.

The following table lists the metrics available for the Microsoft.CognitiveServices/accounts resource type.

[!INCLUDE [horz-monitor-ref-metrics-tableheader](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-tableheader.md)]

[!INCLUDE [Microsoft.CognitiveServices/account](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/metrics/microsoft-cognitiveservices-accounts-metrics-include.md)]

[!INCLUDE [horz-monitor-ref-metrics-dimensions-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-dimensions-intro.md)]

[!INCLUDE [horz-monitor-ref-metrics-dimensions](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-dimensions.md)]

- ApiName
- FeatureName
- ModelDeploymentName
- ModelName
- ModelVersion
- OperationName
- Region
- StatusCode
- StreamType
- UsageChannel

[!INCLUDE [horz-monitor-ref-resource-logs](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-resource-logs.md)]

### Supported resource logs for Microsoft.CognitiveServices/accounts

[!INCLUDE [<ResourceType/namespace>](~/reusable-content/ce-skilling/azure/includes/azure-monitor/reference/logs/microsoft-cognitiveservices-accounts-logs-include.md)]

[!INCLUDE [horz-monitor-ref-logs-tables](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-logs-tables.md)]

### Azure OpenAI microsoft.cognitiveservices/accounts

- [AzureActivity](/azure/azure-monitor/reference/tables/azureactivity#columns)
- [AzureMetrics](/azure/azure-monitor/reference/tables/azuremetrics#columns)
- [AzureDiagnostics](/azure/azure-monitor/reference/tables/azurediagnostics#columns)

[!INCLUDE [horz-monitor-ref-activity-log](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-activity-log.md)]

- [AI + machine learning resource provider operations](/azure/role-based-access-control/resource-provider-operations#microsoftsearch)

## Related content

- See [Monitor Azure OpenAI](./how-to/monitor-openai.md) for a description of monitoring Azure OpenAI.
- See [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource) for details on monitoring Azure resources.
