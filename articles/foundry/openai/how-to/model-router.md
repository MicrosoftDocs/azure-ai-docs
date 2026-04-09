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

[!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]

Use the **Routing mode** dropdown to select a routing profile. This sets the routing logic for your deployment.

:::image type="content" source="media/working-with-models/model-router-routing-mode.png" alt-text="Screenshot of model router routing mode selection.":::

**When to use each mode:**
- **Balanced** (default): Most workloads. Optimizes cost while maintaining quality.
- **Quality**: Critical tasks like legal review, medical summaries, or complex reasoning.
- **Cost**: High-volume, budget-sensitive workloads like content classification or simple Q&A.

> [!NOTE]
> Changes to the routing mode can take up to five minutes to take effect.

### Select your model subset

[!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]


The latest version of model router supports custom subsets: you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics. 

In the model router deployment pane, select **Route to a subset of models**. Then select the underlying models you want to enable. You must select at least one model for routing. If no models are selected, the deployment uses the default model set for your routing mode.

:::image type="content" source="media/working-with-models/model-router-model-subset.png" alt-text="Screenshot of model router subset selection.":::

New models introduced later are excluded by default until explicitly added.


> [!IMPORTANT]
> To include models by Anthropic (Claude) in your model router deployment, you need to deploy them yourself to your Foundry resource. See [Deploy and use Claude models](/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude).


> [!NOTE]
> Changes to the model subset can take up to five minutes to take effect.


[!INCLUDE [model-router 1](../includes/how-to-model-router-1.md)]

## Test model router in the playground

In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), go to your model router deployment on the **Models + endpoints** page and select it to open the model playground. In the playground, enter messages and see the model's responses. Each response shows which underlying model the router selected.

> [!IMPORTANT]
> You can set the `Temperature` and `Top_P` parameters to the values you prefer (see the [concepts guide](/azure/ai-foundry/openai/concepts/prompt-engineering?tabs=chat#temperature-and-top_p-parameters)), but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it ignores the `Temperature` and `Top_P` input parameters.
>
> The parameters `stop`, `presence_penalty`, `frequency_penalty`, `logit_bias`, and `logprobs` are similarly dropped for o-series models but used otherwise.

> [!IMPORTANT]
> Starting with the `2025-11-18` version, the `reasoning_effort` parameter (see the [Reasoning models guide](/azure/ai-foundry/openai/how-to/reasoning?tabs=python-secure#reasoning-effort)) is now **supported** in model router. If the model router selects a reasoning model for your prompt, it will use your `reasoning_effort` input value with the underlying model.

## Connect model router to a Foundry agent

[!INCLUDE [version-sign-in](../../includes/version-sign-in.md)]


If you've created an AI agent in Foundry, you can connect your model router deployment to be used as the agent's base model. Select it from the **model** dropdown menu in the agent playground. Your agent will have all the tools and instructions you've configured for it, but the underlying model that processes its responses will be selected by model router.

> [!IMPORTANT]
> If you use Agent service tools in your flows, only OpenAI models will be used for routing.

### Output format 

The JSON response you receive from a model router model is identical to the standard chat completions API response. Note that the `"model"` field reveals which underlying model was selected to respond to the prompt.

The following example response was generated using API version `2025-11-18`:

```json

{
    "success": true,
    "data": {
        "choices": [
            {
                "content_filter_results": {
                    "hate": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "protected_material_code": {
                        "filtered": false,
                        "detected": false
                    },
                    "protected_material_text": {
                        "filtered": false,
                        "detected": false
                    },
                    "self_harm": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "sexual": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "violence": {
                        "filtered": false,
                        "severity": "safe"
                    }
                },
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null,
                "message": {
                    "annotations": [],
                    "content": "Charismatic and bold—combining brash showmanship and poetic wit with fierce competitiveness, moral conviction, and unwavering activism.",
                    "refusal": null,
                    "role": "assistant"
                }
            }
        ],
        "created": 1774543376,
        "id": "xxxx-yyyy-zzzz",
        "model": "gpt-5-mini-2025-08-07",
        "object": "chat.completion",
        "prompt_filter_results": [
            {
                "prompt_index": 0,
                "content_filter_results": {
                    "hate": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "jailbreak": {
                        "filtered": false,
                        "detected": false
                    },
                    "self_harm": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "sexual": {
                        "filtered": false,
                        "severity": "safe"
                    },
                    "violence": {
                        "filtered": false,
                        "severity": "safe"
                    }
                }
            }
        ],
        "system_fingerprint": null,
        "usage": {
            "completion_tokens": 163,
            "completion_tokens_details": {
                "accepted_prediction_tokens": 0,
                "audio_tokens": 0,
                "reasoning_tokens": 128,
                "rejected_prediction_tokens": 0
            },
            "prompt_tokens": 3254,
            "prompt_tokens_details": {
                "audio_tokens": 0,
                "cached_tokens": 3200
            },
            "total_tokens": 3417
        }
    }
}

```

[!INCLUDE [model-router 2](../includes/how-to-model-router-2.md)]
