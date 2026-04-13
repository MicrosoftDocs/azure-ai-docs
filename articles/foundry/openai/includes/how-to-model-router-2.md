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

## Resources

The following open-source repositories demonstrate model router in different scenarios. Each repo is on GitHub — learn, fork, and extend to accelerate your learning. Most samples require an existing model router deployment; see [Deploy a model router model](#deploy-a-model-router-model) to get started.

| **Resource** | **Learn** | **Extend** |
|---|---|---|
| [Model Router Capabilities Interactive Demo](https://github.com/leestott/router-demo-app/) (Python) | Compare Balanced, Cost, and Quality routing modes with custom prompts. View live benchmark data for cost savings, latency, and routing distribution. | Add your own prompt sets, integrate with your CI pipeline, or connect to your deployment for A/B testing. |
| [Routed Models Distribution Analysis](https://github.com/guygregory/ModelRouter-Distribution) (Python) | Run batches of prompts across routing profiles and model subsets. See which models the router selects and in what proportions. | Plug in representative prompt logs to evaluate tradeoffs before adopting a routing policy at scale. |
| [Multi-team sceanrios with Quality & Cost benchmarking](https://github.com/microsoft/aitour26-LTG153-automate-model-selection-with-microsoft-foundry-model-router) (Python, workshop) | Deploy model router, run benchmarks against fixed-model deployments, and analyze cost and latency optimization in a multi-team enterprise scenario. | Swap in your own models, prompts, and routing profiles to benchmark against your workload patterns. |
| [On-Call Copilot Multi-Agent Demo](https://github.com/leestott/On-Call-Copilot-Multi-Agent) (Python) | See how model router dynamically selects the right model per agent step — a fast, low-cost model for classification and a reasoning model for root-cause analysis. | Adapt the multi-agent architecture, agent roles, and escalation paths for your own operations or support scenarios. |

> [!IMPORTANT]
> These samples are intended for learning and experimentation only and are not production-ready. Before deploying any code derived from these repositories, review it against your organization's security, compliance, and responsible AI policies. See the [Microsoft Responsible AI principles](https://www.microsoft.com/ai/responsible-ai) for guidance.

## Next steps

- [Model router concepts](../concepts/model-router.md) - Learn how routing modes work
- [Quotas and limits](../quotas-limits.md) - Rate limits for model router
- [Create an agent](../../../foundry-classic/agents/quickstart.md) - Use model router with Foundry agents
