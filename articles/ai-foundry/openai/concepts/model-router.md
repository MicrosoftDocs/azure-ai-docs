---
title: Model router for Microsoft Foundry concepts
titleSuffix: Azure OpenAI
description: Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 02/10/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.custom:
  - build-2025
  - dev-focus
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'

---

# Model router for Microsoft Foundry

[!INCLUDE [version-banner](../../includes/version-banner.md)]

Model router is a trained language model that intelligently routes your prompts in real time to the most suitable large language model (LLM). You deploy model router like any other Foundry model. Thus, it delivers high performance while saving on costs, reducing latencies, and increasing responsiveness, while maintaining comparable quality, all packaged as a single model deployment.

> [!NOTE]
> You do not need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments are invoked by model router if they're selected for routing.

To try model router quickly, follow [How to use model router](../how-to/model-router.md). After you deploy model router, send a request to the deployment. Model router selects an underlying model for each request based on your routing settings.

::: moniker range="foundry-classic"
> [!TIP]
> The [Microsoft Foundry (new)](../../what-is-foundry.md) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation](?view=foundry&preserve-view=true) to see the latest features.
::: moniker-end


## How model router works
As a trained language model, model router analyzes your prompts in real time based on complexity, reasoning, task type, and other attributes. It does not store your prompts. It routes only to eligible models based on your access and deployment types, honoring data zone boundaries.

> [!IMPORTANT]
> The effective context window is limited by the smallest underlying model. For larger contexts, use [model subset](#model-subset) to select models that support your requirements.

- In Balanced mode (default), it considers all underlying models within a small quality range (for example, 1% to 2% compared with the highest-quality model for that prompt) and picks the most cost-effective model.
- In Cost mode, it considers a larger quality band (for example, 5% to 6% compared with the highest-quality model for that prompt) and chooses the most cost-effective model.
- In Quality mode, it picks the highest quality rated model for the prompt, ignoring the cost.

## Why use model router?

Model router optimizes costs and latencies while maintaining comparable quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single deployment and chat experience that combines the best features from all of the underlying chat models.

::: moniker range="foundry"

The latest version, `2025-11-18` adds several capabilities:
1. Support Global Standard and Data Zone Standard deployments.
1. Adds support for new models: `grok-4`, `grok-4-fast-reasoning`, `DeepSeek-V3.1`, `gpt-oss-120b`, `Llama-4-Maverick-17B-128E-Instruct-FP8`, `claude-haiku-4-5`, `claude-opus-4-1`, and `claude-sonnet-4-5`.
1. Quick deploy or Custom deploy with **routing mode** and **model subset** options.
1. **Routing mode**: Optimize the routing logic for your needs. Supported options: `Quality`, `Cost`, `Balanced` (default).
1. **Model subset**: Select your preferred models to create your model subset for routing.
1. Support for agentic scenarios including tools so you can now use it in the Foundry Agent Service.

::: moniker-end

## Versioning 

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed&mdash;only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Model updates](../how-to/working-with-models.md#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

[!INCLUDE [model-router-supported](../includes/model-router-supported.md)]

::: moniker range="foundry"

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don’t set one, your deployment defaults to the Balanced mode.

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
| East US 2 | Global Standard, Data Zone Standard |
| Sweden Central | Global Standard, Data Zone Standard |

Also see [Azure OpenAI in Microsoft Foundry models](../../foundry-models/concepts/models-sold-directly-by-azure.md) for current region availability.

### Rate limits

| Model                               | Deployment Type  | Default RPM   | Default TPM   | Enterprise and MCA-E RPM    | Enterprise and MCA-E TPM     |
|:-----------------------------------:|------------------:|:--------------:|:--------------:|:----------------------------|:-----------------------------:|
| `model-router` <br> `(2025-11-18)` | DataZoneStandard | 150           | 150,000       | 300                         | 300,000                      |
| `model-router` <br> `(2025-11-18)` | GlobalStandard   | 250           | 250,000       | 400                         | 400,000                      |

Also see [Quotas and limits](../quotas-limits.md) for rate limit information.

::: moniker range="foundry"

To overcome the limits on context window and parameters, use the Model subset feature to select your models for routing that support your desired properties.

::: moniker-end

> [!NOTE]
> The context window limit listed for model router is the limit of the smallest underlying model. Other underlying models are compatible with larger context windows, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model. To review context windows for the underlying models, see [Azure OpenAI in Microsoft Foundry models](../../foundry-models/concepts/models-sold-directly-by-azure.md).
>
> To shorten the context window, you can do one of the following:
> - Summarize the prompt before passing it to the model
> - Truncate the prompt into more relevant parts
> - Use document embeddings and have the chat model retrieve relevant sections. For more information, see [What is Azure AI Search?](../../../search/search-what-is-azure-search.md)

Model router accepts image inputs for [Vision enabled chats](../how-to/gpt-with-vision.md) (all of the underlying models can accept image input), but the routing decision is based on the text input only.

Model router doesn't process audio input.

## Troubleshooting

| Issue | Resolution |
|-------|------------|
| Deployment fails | Verify your Foundry resource is in East US 2 or Sweden Central. |
| Claude models not routing | Ensure Claude models are deployed separately before enabling in model router. |
| Context exceeded error | Reduce prompt size or use model subset to select models with larger context windows. |
| Unexpected model selection | Review your routing mode setting (Balanced, Cost, Quality) and model subset configuration. |

For detailed deployment troubleshooting, see [How to use model router](../how-to/model-router.md).

## Billing information

Starting November 2025, the model router usage will be charged for input prompts at the rate listed on the pricing page.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
