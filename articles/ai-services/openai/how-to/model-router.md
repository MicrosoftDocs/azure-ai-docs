---
title: How to use model router for Azure AI Foundry (preview)
titleSuffix: Azure OpenAI Service
description: Learn how to use the model router in Azure OpenAI Service to select the best model for your task.
author: PatrickFarley
ms.author: pafarley 
#customer intent: 
ms.service: azure-ai-openai
ms.topic: how-to
ms.date: 04/17/2025
manager: nitinme
---

# Use model router for Azure AI Foundry (preview)

Model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. It uses a combination of preexisting models to provide high performance while saving on compute costs where possible. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](../concepts/model-router.md).

You can access model router through the Completions API just as you would use a single base model like GPT-4.

## Deploy a model router model

Model router is packaged as a single OpenAI model that you deploy. Follow the steps in the [resource deployment guide](/azure/ai-services/openai/how-to/create-resource), and in the **Create new deployment** step, find `model-router` in the **Models** list. Select it, and then complete the rest of the deployment steps.

> [!NOTE]
> Consider that your deployment settings apply to all underlying chat models that model router uses.
> - You don't need to deploy the underlying chat models separately. Model router works independently of your other deployed models.
> - You select a content filter when you deploy the model router model (or you can apply a filter later). The content filter is applied to all activity to and from the model router: you don't set content filters for each of the underlying chat models.
> - Your tokens-per-minute rate limit setting is applied to all activity to and from the model router: you don't set rate limits for each of the underlying chat models.

## Use model router in chats

You can use model router through the [chat completions API](/azure/ai-services/openai/chatgpt-quickstart) in the same way you'd use other OpenAI chat models. Set the `model` parameter to the name of our model router deployment, and set the `messages` parameter to the messages you want to send to the model.

In the [Azure AI Foundry portal](https://ai.azure.com/), you can navigate to your model router deployment on the **Models + endpoints** page and select it to enter the model playground. In the playground experience, you can enter messages and see the model's responses. Each response message shows which underlying model was selected to respond.


> [!IMPORTANT]
> You can set the `Temperature` and `Top_P` parameters to the values you prefer (see the [concepts guide](/azure/ai-services/openai/concepts/prompt-engineering?tabs=chat#temperature-and-top_p-parameters)), but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it ignores the `Temperature` and `Top_P` input parameters.
>
> The parameters `stop`, `presence_penalty`, `frequency_penalty`, `logit_bias`, and `logprobs` are similarly dropped for o-series models but used otherwise.

> [!IMPORTANT]
> The `reasoning_effort` parameter (see the [Reasoning models guide](/azure/ai-services/openai/how-to/reasoning?tabs=python-secure#reasoning-effort)) isn't supported in model router. If the model router selects a reasoning model for your prompt, it also selects a `reasoning_effort` input value based on the complexity of the prompt.

### Output format 

The JSON response you receive from a model router model looks like the following.

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

You can monitor the performance of your model router deployment in Azure monitor (AzMon) in the Azure portal. 

1. Go to the **Monitoring** -> **Metrics** page for your Azure OpenAI resource in the Azure portal. 
1. Filter by the deployment name of your model router model.
1. Optionally, split up the metrics by underlying models.


### Monitor costs

You can monitor the costs of model router, which is the sum of the costs incurred by the underlying models.
1. Visit the **Resource Management** -> **Cost analysis** page in the Azure portal.
1. If needed, filter by Azure resource.
1. Then, filter by deployment name: Filter by "Tag", select **Deployment** as the type of the tag, and then select your model router deployment name as the value.

