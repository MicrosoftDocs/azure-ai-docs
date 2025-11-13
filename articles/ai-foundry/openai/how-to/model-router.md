---
title: How to use model router for Microsoft Foundry
description: Learn how to use the model router in Azure OpenAI to select the best model for your task.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 09/02/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom:
  - build-2025
# customer intent:
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted


---

# Use model router for Microsoft Foundry


Model router for Microsoft Foundry is a deployable AI chat model that selects the best large language model (LLM) to respond to a prompt in real time. It uses different preexisting models to deliver high performance and save on compute costs, all in one model deployment. To learn more about how model router works, its advantages, and limitations, see the [Model router concepts guide](../concepts/model-router.md).

Use model router through the Completions API like you'd use a single base model such as GPT-4. Follow the same steps as in the [Chat completions guide](/azure/ai-foundry/openai/how-to/chatgpt).

## Deploy a model router model

Model router is packaged as a single Foundry model that you deploy. Start by following the steps in the [resource deployment guide](/azure/ai-foundry/openai/how-to/create-resource). 

::: moniker range="foundry-classic"
In the **Create new deployment** step, find `model-router` in the **Models** list and select it. 
::: moniker-end

::: moniker range="foundry"
In the **Create new deployment** step, find `model-router` in the **Models** list and select it. To enable more configuration options, toggle the **Customize my deployment** switch on.
::: moniker-end

> [!NOTE]
> Your deployment settings apply to all underlying chat models that model router uses.
> - Don't deploy the underlying chat models separately. Model router works independently of your other deployed models.
> - Select a content filter when you deploy the model router model or apply a filter later. The content filter applies to all content passed to and from the model router; don't set content filters for each underlying chat model.
> - Your tokens-per-minute rate limit setting applies to all activity to and from the model router; don't set rate limits for each underlying chat model.## Use model router in chats

::: moniker range="foundry"

## Select a routing profile

Use the **Routing mode** dropdown to select a routing profile. This sets the default routing profile for your deployment, but you can still override it at request time. See the [concepts guide](../how-to/model-router.md) for more information.

You can also set the routing profile programmatically. The allowed values are `balanced`, `quality`, and `cost`. If you don't specify a profile, the service defaults to `balanced`.


#### [Azure CLI](#tab/cli)

Set mode at deployment time:

```bash
az resource create \
  --resource-group <rg-name> \
  --namespace Microsoft.CognitiveServices \
  --parent accounts/<account-name> \
  --resource-type deployments \
  --name <deployment-name> \
  --api-version 2024-03-01-preview \
  --properties '{
    "sku": { "name": "GlobalStandard", "capacity": 10 },
    "properties": {
      "model": {
        "format": "OpenAI",
        "name": "ModelRouter",
        "version": "2025-02-26-preview"
      },
      "routing": {
        "mode": "quality"
      }
    }
  }'
```

Update an existing deployment’s mode:

```bash
az resource update \
  --resource-group <rg-name> \
  --namespace Microsoft.CognitiveServices \
  --parent accounts/<account-name> \
  --resource-type deployments \
  --name <deployment-name> \
  --api-version 2024-03-01-preview \
  --set properties.routing.mode=cost
```

#### [ARM-style JSON body](#tab/arm)

```json
{
  "sku": { "name": "GlobalStandard", "capacity": 10 },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "ModelRouter",
      "version": "2025-02-26-preview"
    },
    "routing": {
      "mode": "balanced"
    }
  }
}
```
---

### Per-request override (data plane)

Add the `model-router-mode` header to a request to override the deployment’s default for that single call.

#### Request example

```
POST /v1/chat/completions HTTP/1.1
Authorization: Bearer <token>
Content-Type: application/json
model-router-mode: cost

{
  "messages": [
    { "role": "user", "content": "Summarize this article." }
  ]
}
```

### Response headers

The router returns the header:

```
model-router-effective-mode: cost
```

This echoes the effective mode after merging deployment defaults and any valid override.

### Validation and errors

| Condition | HTTP status | Error code | Notes |
|-----------|-------------|-----------|-------|
| Unsupported `model-router-mode` value | 400 | `invalidRoutingMode` | Value not in balanced/quality/cost |
| Per-request overrides disabled (deployment policy) | 400 | `headerNotAllowed` | Remove header or enable overrides |
| Case variation | 200 | — | Value normalized internally (`Quality` → `quality`) |

(Confirm whether per-request overrides can be disabled by policy and link to policy doc when available.) [TO VERIFY]



### Troubleshooting

| Symptom | Possible cause | Action |
|---------|----------------|--------|
| 400 `invalidRoutingMode` | Typo in header value | Use `balanced`, `quality`, or `cost` |
| 400 `headerNotAllowed` | Overrides disabled | Remove header or enable overrides at deployment |
| Higher cost than expected in `balanced` | Narrow candidate pool still dominated by top-cost model | Test `cost` mode; verify quality tolerance |
| Quality drop larger than expected in `cost` mode | Domain differs from internal tuning set | Re-evaluate; consider `balanced` or `quality` for that segment |

## Select your model subset

The latest version of model router supports custom subsets: you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics. See the [concepts guide](../how-to/model-router.md) for more information.

In the model router deployment pane, select **Route to a subset of models**. Then select the underlying models you want to enable. Selections apply to all requests to this deployment by default. 

If you're deploying programmatically, you can specify your model subset by setting the `routing.models` contents in the request body.

```json
{
  "sku": {
    "name": "GlobalStandard",
    "capacity": 10
  },
  "properties": {
    "model": {
      "format": "OpenAI",
      "name": "ModelRouter",
      "version": "2025-02-26-preview"
    },
    "routing": {
      "mode": "balanced",
      "models": [
        {
          "format": "OpenAI",
          "name": "babbage",
          "version": "1"
        },
        {
          "format": "OpenAI",
          "name": "ada",
          "version": "1"
        }
      ]
    }
  }
}
```

New models introduced later are excluded by default until explicitly added.

::: moniker-end



## Test model router with the Completions API

You can use model router through the [chat completions API](/azure/ai-foundry/openai/chatgpt-quickstart) in the same way you'd use other OpenAI chat models. Set the `model` parameter to the name of our model router deployment, and set the `messages` parameter to the messages you want to send to the model.

## Test model router in the playground

In the [Foundry portal](https://ai.azure.com/?cid=learnDocs), go to your model router deployment on the **Models + endpoints** page and select it to open the model playground. In the playground, enter messages and see the model's responses. Each response shows which underlying model the router selected.

> [!IMPORTANT]
> You can set the `Temperature` and `Top_P` parameters to the values you prefer (see the [concepts guide](/azure/ai-foundry/openai/concepts/prompt-engineering?tabs=chat#temperature-and-top_p-parameters)), but note that reasoning models (o-series) don't support these parameters. If model router selects a reasoning model for your prompt, it ignores the `Temperature` and `Top_P` input parameters.
>
> The parameters `stop`, `presence_penalty`, `frequency_penalty`, `logit_bias`, and `logprobs` are similarly dropped for o-series models but used otherwise.

> [!IMPORTANT]
> The `reasoning_effort` parameter (see the [Reasoning models guide](/azure/ai-foundry/openai/how-to/reasoning?tabs=python-secure#reasoning-effort)) isn't supported in model router. If the model router selects a reasoning model for your prompt, it also selects a `reasoning_effort` input value based on the complexity of the prompt.

::: moniker range="foundry"

## Connect model router to a Foundry agent

If you've created an AI agent in Foundry, you can connect your model router deployment to be used as the agent's base model. Select it from the **model** dropdown menu in the agent playground. Your agent will have all the tools and instructions you've configured for it, but the underlying model that processes its responses will be selected by model router.

::: moniker-end




### Output format 

The JSON response you receive from a model router model is identical to the standard chat completions API response. Note that the `"model"` field reveals which underlying model was selected to respond to the prompt.

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

