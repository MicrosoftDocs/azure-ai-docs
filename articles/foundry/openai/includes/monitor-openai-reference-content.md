---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include, classic-and-new
---

[!INCLUDE [horz-monitor-ref-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-intro.md)]

See [Monitor Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md) for details on the data you can collect for Azure OpenAI in Microsoft Foundry Models and how to use it.

[!INCLUDE [horz-monitor-ref-metrics-intro](~/reusable-content/ce-skilling/azure/includes/azure-monitor/horizontals/horz-monitor-ref-metrics-intro.md)]

### Supported metrics for Microsoft.CognitiveServices/accounts

Here are the most important metrics we think you should monitor for Azure OpenAI. Later in this article is a longer list of all available metrics for this namespace which contains more details on metrics in this shorter list. _Please see below list for most up to date information. We're working on refreshing the tables in the following sections._

> [!IMPORTANT]
> Don't confuse the metrics in this section with the legacy `Latency` metric listed under **Cognitive Services - HTTP Requests** later in this article. The legacy `Latency` metric isn't designed for Azure OpenAI workloads and produces misleading results when used to diagnose Azure OpenAI latency. For Azure OpenAI latency monitoring, use **Time to Response** (`AzureOpenAITimeToResponse`), **Time to Last Byte** (`AzureOpenAITTLTInMS`), **Time Between Tokens** (`AzureOpenAINormalizedTBTInMS`), or **Normalized Time to First Byte** (`AzureOpenAINormalizedTTFTInMS`). For guidance on interpreting these metrics, see [Performance and latency](../how-to/latency.md).

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

#### Quick reference: Key metrics by use case

Use this table to find the right metric for a specific monitoring goal. For end-to-end guidance on interpreting these metrics, see [Performance and latency](../how-to/latency.md).

| I want to monitor... | Use this metric | REST API name |
| --- | --- | --- |
| Overall response time | Time to Last Byte | `AzureOpenAITTLTInMS` |
| First-token responsiveness (streaming) | Time to Response | `AzureOpenAITimeToResponse` |
| Token generation speed | Time Between Tokens | `AzureOpenAINormalizedTBTInMS` |
| First-token efficiency normalized by prompt size | Normalized Time to First Byte | `AzureOpenAINormalizedTTFTInMS` |
| Output token volume per request | Generated Completion Tokens | `GeneratedTokens` |
| Input token volume per request | Processed Prompt Tokens | `ProcessedPromptTokens` |
| PTU capacity utilization | Provisioned-managed Utilization V2 | `AzureOpenAIProvisionedManagedUtilizationV2` |
| Request volume and errors | Azure OpenAI Requests | `AzureOpenAIRequests` |

> [!TIP]
> Always pair a latency metric with a token count metric. A latency increase without a corresponding token increase might indicate a real issue. A latency increase with a proportional token increase is expected behavior.

> [!WARNING]
> The metrics under **Cognitive Services - HTTP Requests** later in this article are legacy Cognitive Services metrics and aren't designed for Azure OpenAI workloads. In particular, the `Latency` metric in that category isn't the same as the Azure OpenAI latency metrics (Time to Response, Time to Last Byte, Time Between Tokens, Normalized Time to First Byte). Using the legacy `Latency` metric for Azure OpenAI troubleshooting produces misleading results. Use the Azure OpenAI metrics listed in this section instead.

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

- See [Monitor Azure OpenAI](../../../foundry-classic/openai/how-to/monitor-openai.md) for a description of monitoring Azure OpenAI.
- See [Monitor Azure resources with Azure Monitor](/azure/azure-monitor/essentials/monitor-azure-resource) for details on monitoring Azure resources.
