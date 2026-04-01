---
title: "How to use model router for Microsoft Foundry (classic)"
description: "Learn how to use the model router in Azure OpenAI to select the best model for your task. (classic)"
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

ROBOTS: NOINDEX, NOFOLLOW
---

# Use model router for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/model-router.md)

Model router for Microsoft Foundry is a deployable AI chat model that selects the best large language model (LLM) to respond to a prompt in real time. It uses different preexisting models to deliver high performance and save on compute costs, all in one model deployment. To learn more about how model router works, its advantages, and limitations, see the [Model router concepts guide](../concepts/model-router.md).

Use model router through the Chat Completions API like you'd use a single base model such as GPT-5. Follow the same steps as in the [Chat completions guide](/azure/ai-foundry/openai/how-to/chatgpt).

> [!TIP]
> The [Microsoft Foundry (new)](../../what-is-foundry.md#microsoft-foundry-portals) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation]() to see the latest features.
[!INCLUDE [model-router-supported](../../../foundry/openai/includes/model-router-supported.md)]

## Deploy a model router model

Model router is packaged as a single Foundry model that you deploy. Start by following the steps in the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource). 

In the **Create new deployment**, find `model-router` in the **Models** list and select it.

> [!NOTE]
> Your deployment settings apply to all underlying chat models that model router uses.
> - Don't deploy the underlying chat models separately. Model router works independently of your other deployed models.
> - Select a content filter when you deploy the model router model or apply a filter later. The content filter applies to all content passed to and from the model router; don't set content filters for each underlying chat model.
> - Your tokens-per-minute rate limit setting applies to all activity to and from the model router; don't set rate limits for each underlying chat model.

[!INCLUDE [model-router 1](../../../foundry/openai/includes/how-to-model-router-1.md)]

## Test model router in the playground

In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), go to your model router deployment on the **Models + endpoints** page and select it to open the model playground. In the playground, enter messages and see the model's responses. Each response shows which underlying model the router selected.

> [!IMPORTANT]
> You can set the `Temperature` and `Top_P` parameters to the values you prefer (see the [concepts guide](/azure/ai-foundry/openai/concepts/prompt-engineering?tabs=chat#temperature-and-top_p-parameters)), but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it ignores the `Temperature` and `Top_P` input parameters.
>
> The parameters `stop`, `presence_penalty`, `frequency_penalty`, `logit_bias`, and `logprobs` are similarly dropped for o-series models but used otherwise.

> [!IMPORTANT]
> Starting with the `2025-11-18` version, the `reasoning_effort` parameter (see the [Reasoning models guide](/azure/ai-foundry/openai/how-to/reasoning?tabs=python-secure#reasoning-effort)) is now **supported** in model router. If the model router selects a reasoning model for your prompt, it will use your `reasoning_effort` input value with the underlying model.

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
[!INCLUDE [model-router 2](../../../foundry/openai/includes/how-to-model-router-2.md)]
