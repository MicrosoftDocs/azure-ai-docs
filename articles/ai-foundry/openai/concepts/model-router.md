---
title: Model router for Microsoft Foundry concepts
titleSuffix: Azure OpenAI
description: Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 09/10/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: conceptual
ms.custom:
  - build-2025
monikerRange: 'foundry-classic || foundry'

---

# Model router for Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Model router for Microsoft Foundry is a deployable AI model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. You deploy model router like any other Foundry model. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. Thus, it delivers high performance while saving on compute costs where possible, all packaged as a single model deployment.

> [!NOTE]
> You do not need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments will get invoked by Model router if they're selected for routing.

::: moniker range="foundry-classic"
> [!TIP]
> The [Microsoft Foundry (new)](../../what-is-azure-ai-foundry.md#microsoft-foundry-portals) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation](?view=foundry&preserve-view=true) to see the latest features.
::: moniker-end

## How model router works

Model router is a trained language model that analyzes your prompts in real time to decide on the most suitable large language model (LLM) to route to based on the complexity, reasoning, task type, and other attributes of the prompts. It does not store your prompts. Moreover, it routes to only eligible models based on your access and deployment types, honoring data zone boundaries. 
- In the default `Balanced` mode, it considers all underlying models within a small quality range, for example 1-2% compared with the highest quality model for that prompt, and picks the most cost-effective model.
- When the `Cost` routing mode is selected, it considers a larger quality band, for example 5-6% range compared with the highest quality model for that prompt, and chooses the most cost-effective model. 
- For the `Quality` routing mode, it picks the highest quality rated model for the prompt, ignoring the cost basis.

## Why use model router?

Model router intelligently selects the best underlying model for a given prompt to optimize costs while maintaining quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single deployment and chat experience that combines the best features from all of the underlying chat models.

::: moniker range="foundry"

The latest version, `2025-11-18` adds several capabilities:
1. Support Global Standard and Data Zone Standard deployments.
1. Adds support for new models: `grok-4`, `grok-4-fast-reasoning`, `DeepSeek-V3.1`, `gpt-oss-120b`, `Llama-4-Maverick-17B-128E-Instruct-FP8`, `gpt-4o`, `gpt-4o-mini`, `claude-haiku-4-5`, `claude-opus-4-1`, and `claude-sonnet-4-5`.
1. Quick deploy or Custom deploy with **routing mode** and **model subset** options.
1. **Routing mode**: Optimize the routing logic for your needs. Supported options: `Quality`, `Cost`, `Balanced` (default).
1. **Model subset**: Select your preferred models to create your model subset for routing.
1. Support for agentic scenarios including tools so you can now use it in the Foundry Agent service.

::: moniker-end

## Versioning 

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed&mdash;only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Manage models](/azure/ai-foundry/openai/how-to/working-with-models?tabs=powershell#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.


## Underlying models
With the `2025-11-18` version, Model Router adds nine new models including Anthropic's Claude, DeepSeek, Llama, Grok models to support a total of 18 models available for routing your prompts.

|Model router version|Underlying models| Underlying model version
|:---:|:---|:----:|
|`2025-11-18`| `gpt-4.1` </br> `gpt-4.1-mini` </br> `gpt-4.1-nano` </br> `o4-mini` <br> `gpt-5-nano` <br> `gpt-5-mini` <br> `gpt-5` <br> `gpt-5-chat` <br> `Deepseek-v3.1` <br> `gpt-oss-120b` <br> `llama4-maverick-instruct` <br> `grok-4` <br> `grok-4-fast` <br> `gpt-4o` <br> `gpt-4o-mini` <br> `claude-haiku-4-5` <br> `claude-opus-4-1` <br> `claude-sonnet-4-5` | `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> N/A <br> N/A <br> N/A <br> N/A <br> N/A <br> `2024-11-20` <br> `2024-07-18` <br> `2025-10-01` <br> `2025-08-05` <br> `2025-09-29` |
|`2025-08-07`| `gpt-4.1` </br> `gpt-4.1-mini` </br> `gpt-4.1-nano` </br> `o4-mini` </br> `gpt-5` <br> `gpt-5-mini` <br> `gpt-5-nano` <br> `gpt-5-chat` | `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` <br> `2025-08-07` |
|`2025-05-19`| `gpt-4.1` </br>`gpt-4.1-mini` </br>`gpt-4.1-nano` </br>`o4-mini`  |  `2025-04-14` <br> `2025-04-14` <br> `2025-04-14` <br> `2025-04-16` |

::: moniker range="foundry"

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don’t set one, your deployment defaults to the `balanced` mode.

Available routing modes:

| Mode | Description |
|------|-----------|
| Balanced (default) | Considers both cost and quality dynamically. Perfect for general-purpose scenarios |
| Quality | Prioritizes for maximum accuracy. Best for complex reasoning or critical outputs |
| Cost | Prioritizes for more cost savings. Ideal for high-volume, budget-sensitive workloads |

## Model subset

The latest version of model router supports model subsets: For custom deployments, you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics.

When new base models become available, they're not included in your selection unless you explicitly add them to your deployment's inclusion list.

::: moniker-end


## Limitations

### Resource limitations

| Region | Deployment types supported |
|------|-----------|
| East US 2 | Global Standard, Data zone Standard |
| Sweden Central | Global Standard, Data zone Standard  |

Also see the [Models](../concepts/models.md#model-router) page for the region availability and deployment types for model router.

### Rate limits

| Model                               | Deployment Type  | Default RPM   | Default TPM   | Enterprise and MCA-E RPM    | Enterprise and MCA-E TPM     |
|:-----------------------------------:|------------------:|:--------------:|:--------------:|:----------------------------|:-----------------------------:|
| `model-router` <br> `(2025-11-18)` | DataZoneStandard | 150           | 150,000       | 300                         | 300,000                      |
| `model-router` <br> `(2025-11-18)` | GlobalStandard   | 250           | 250,000       | 400                         | 400,000                      |

Also see [Quotas and limits](/azure/ai-foundry/openai/quotas-limits) for rate limit information.

::: moniker range="foundry"

To overcome the limits on context window and parameters, use the Model subset feature to select your models for routing that support your desired properties.

::: moniker-end

> [!NOTE]
> The context window limit listed on the [Models](../concepts/models.md#model-router) page is the limit of the smallest underlying model. Other underlying models are compatible with larger context windows, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model, otherwise the call will fail. To shorten the context window, you can do one of the following:
> - Summarize the prompt before passing it to the model
> - Truncate the prompt into more relevant parts
> - Use document embeddings and have the chat model retrieve relevant sections: see [Azure AI Search](/azure/search/search-what-is-azure-search) 

Model router accepts image inputs for [Vision enabled chats](/azure/ai-foundry/openai/how-to/gpt-with-vision) (all of the underlying models can accept image input), but the routing decision is based on the text input only.

Model router doesn't process audio input.

## Billing information

Starting November 2025, the model router usage will be charged for input prompts at the rate listed on the pricing page.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
