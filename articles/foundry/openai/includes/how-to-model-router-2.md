---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Monitor model router metrics

### Monitor performance

Monitor the performance of your model router deployment in Azure Monitor (AzMon) in the Azure portal.

1. Go to the **Monitoring** > **Metrics** page for your Azure OpenAI resource in the Azure portal.
1. Filter by the deployment name of your model router model.
1. Split the metrics by underlying models if needed.

### Monitor costs

You can monitor the costs of model router, which is the sum of the costs incurred by the underlying models.
1. Visit the **Resource Management** -> **Cost analysis** page in the Azure portal.
1. If needed, filter by Azure resource.
1. Then, filter by deployment name: Filter by "Tag", select **Deployment** as the type of the tag, and then select your model router deployment name as the value.

## Troubleshoot model router

### Common issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Rate limit exceeded | Too many requests to model router deployment | Increase tokens-per-minute quota or implement retry with exponential backoff |
| Unexpected model selection | Routing logic selected different model than expected | Review routing mode settings; consider using model subset to constrain options |
| High latency | Router overhead plus underlying model processing | Use Cost mode for latency-sensitive workloads; smaller models respond faster |
| Claude model not routing | Claude models require separate deployment | Deploy Claude models from model catalog before enabling in subset |

### Error codes

For API error codes and troubleshooting, see the [Azure OpenAI REST API reference](../../../foundry-classic/openai/reference.md).

## Next steps

- [Model router concepts](../concepts/model-router.md) - Learn how routing modes work
- [Quotas and limits](../quotas-limits.md) - Rate limits for model router
- [Create an agent](../../../foundry-classic/agents/quickstart.md) - Use model router with Foundry agents
