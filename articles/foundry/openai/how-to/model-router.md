---
title: "How to use model router for Microsoft Foundry"
description: "Learn how to use the model router in Azure OpenAI to select the best model for your task."
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 03/18/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.custom:
  - classic-and-new
  - build-2025
  - doc-kit-assisted
# customer intent:
ai-usage: ai-assisted
---

# Use model router for Microsoft Foundry
Model router for Microsoft Foundry is a deployable AI chat model that selects the best large language model (LLM) to respond to a prompt in real time. It uses different preexisting models to deliver high performance and save on compute costs, all in one model deployment. To learn more about how model router works, its advantages, and limitations, see the [Model router concepts guide](../concepts/model-router.md).

Use model router through the Chat Completions API like you'd use a single base model such as GPT-5. Follow the same steps as in the [Chat completions guide](/azure/ai-foundry/openai/how-to/chatgpt).

[!INCLUDE [model-router-supported](../includes/model-router-supported.md)]

## Deploy a model router model

Model router is packaged as a single Foundry model that you deploy. Start by following the steps in the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource). 

In the model catalog, find `model-router` in the **Models** list and select it. Choose **Default settings** for the **Balanced** routing mode and route between all supported models. To enable more configuration options, choose **Custom settings**.

:::image type="content" source="media/working-with-models/model-router-deploy.png" alt-text="Screenshot of model router deploy screen.":::

> [!NOTE]
> Your deployment settings apply to all underlying chat models that model router uses.
> - Don't deploy the underlying chat models separately. Model router works independently of your other deployed models.
> - Select a content filter when you deploy the model router model or apply a filter later. The content filter applies to all content passed to and from the model router; don't set content filters for each underlying chat model.
> - Your tokens-per-minute rate limit setting applies to all activity to and from the model router; don't set rate limits for each underlying chat model.

### Select a routing mode

> [!NOTE]
> Changes to the routing mode can take up to five minutes to take effect.

Use the **Routing mode** dropdown to select a routing profile. This sets the routing logic for your deployment.

:::image type="content" source="media/working-with-models/model-router-routing-mode.png" alt-text="Screenshot of model router routing mode selection.":::

**When to use each mode:**
- **Balanced** (default): Most workloads. Optimizes cost while maintaining quality.
- **Quality**: Critical tasks like legal review, medical summaries, or complex reasoning.
- **Cost**: High-volume, budget-sensitive workloads like content classification or simple Q&A.

### Select your model subset

> [!NOTE]
> Changes to the model subset can take up to five minutes to take effect.

The latest version of model router supports custom subsets: you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics. 

In the model router deployment pane, select **Route to a subset of models**. Then select the underlying models you want to enable.

:::image type="content" source="media/working-with-models/model-router-model-subset.png" alt-text="Screenshot of model router subset selection.":::

> [!IMPORTANT]
> To include models by Anthropic (Claude) in your model router deployment, you need to deploy them yourself to your Foundry resource. See [Deploy and use Claude models](/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude).

> [!NOTE]
> You must select at least one model for routing. If no models are selected, the deployment uses the default model set for your routing mode.

New models introduced later are excluded by default until explicitly added.

## Test model router with the Completions API

You can use model router through the [chat completions API](/azure/ai-foundry/openai/chatgpt-quickstart) in the same way you'd use other OpenAI chat models. Set the `model` parameter to the name of our model router deployment, and set the `messages` parameter to the messages you want to send to the model.

## Test model router in the playground

In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), go to your model router deployment on the **Models + endpoints** page and select it to open the model playground. In the playground, enter messages and see the model's responses. Each response shows which underlying model the router selected.

> [!IMPORTANT]
> You can set the `Temperature` and `Top_P` parameters to the values you prefer (see the [concepts guide](/azure/ai-foundry/openai/concepts/prompt-engineering?tabs=chat#temperature-and-top_p-parameters)), but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it ignores the `Temperature` and `Top_P` input parameters.
>
> The parameters `stop`, `presence_penalty`, `frequency_penalty`, `logit_bias`, and `logprobs` are similarly dropped for o-series models but used otherwise.

> [!IMPORTANT]
> Starting with the `2025-11-18` version, the `reasoning_effort` parameter (see the [Reasoning models guide](/azure/ai-foundry/openai/how-to/reasoning?tabs=python-secure#reasoning-effort)) is now **supported** in model router. If the model router selects a reasoning model for your prompt, it will use your `reasoning_effort` input value with the underlying model.

## Connect model router to a Foundry agent

If you've created an AI agent in Foundry, you can connect your model router deployment to be used as the agent's base model. Select it from the **model** dropdown menu in the agent playground. Your agent will have all the tools and instructions you've configured for it, but the underlying model that processes its responses will be selected by model router.

> [!IMPORTANT]
> If you use Agent service tools in your flows, only OpenAI models will be used for routing.

### Output format 

The JSON response you receive from a model router model is identical to the standard chat completions API response. Note that the `"model"` field reveals which underlying model was selected to respond to the prompt.

The following example response was generated using API version `2025-11-18`:

```json
{
  "choices": [
    {
      "content_filter_results": {
        "hate": {
          "filtered": "False",
          "severity": "safe"
        },
        "protected_material_code": {
          "detected": "False",
          "filtered": "False"
        },
        "protected_material_text": {
          "detected": "False",
          "filtered": "False"
        },
        "self_harm": {
          "filtered": "False",
          "severity": "safe"
        },
        "sexual": {
          "filtered": "False",
          "severity": "safe"
        },
        "violence": {
          "filtered": "False",
          "severity": "safe"
        }
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": "None",
      "message": {
        "content": "I'm doing well, thank you! How can I assist you today?",
        "refusal": "None",
        "role": "assistant"
      }
    }
  ],
  "created": 1745308617,
  "id": "xxxx-yyyy-zzzz",
  "model": "gpt-4.1-nano-2025-04-14",
  "object": "chat.completion",
  "prompt_filter_results": [
    {
      "content_filter_results": {
        "hate": {
          "filtered": "False",
          "severity": "safe"
        },
        "jailbreak": {
          "detected": "False",
          "filtered": "False"
        },
        "self_harm": {
          "filtered": "False",
          "severity": "safe"
        },
        "sexual": {
          "filtered": "False",
          "severity": "safe"
        },
        "violence": {
          "filtered": "False",
          "severity": "safe"
        }
      },
      "prompt_index": 0
    }
  ],
  "system_fingerprint": "xxxx",
  "usage": {
    "completion_tokens": 15,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens": 21,
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    },
    "total_tokens": 36
  }
}
```

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