---
title: "Model router for Microsoft Foundry concepts (classic)"
description: "Learn about the model router feature in Azure OpenAI in Microsoft Foundry Models. (classic)"
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 03/18/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: concept-article
ms.custom:
  - classic-and-new
  - build-2025
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted

ROBOTS: NOINDEX, NOFOLLOW
---

# Model router for Microsoft Foundry (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/concepts/model-router.md)

Model router is a trained language model that intelligently routes your prompts in real time to the most suitable large language model (LLM). You deploy model router like any other Foundry model. Thus, it delivers high performance while saving on costs, reducing latencies, and increasing responsiveness, while maintaining comparable quality, all packaged as a single model deployment.

> [!NOTE]
> You do not need to separately deploy the supported LLMs for use with model router, with the exception of the Claude models. To use model router with your Claude models, first deploy them from the model catalog. The deployments are invoked by model router if they're selected for routing.

To try model router quickly, follow [How to use model router](../how-to/model-router.md). After you deploy model router, send a request to the deployment. Model router selects an underlying model for each request based on your routing settings.

> [!TIP]
> The [Microsoft Foundry (new)](../../what-is-foundry.md) portal offers enhanced configuration options for model router. [Switch to the Microsoft Foundry (new) documentation]() to see the latest features.

[!INCLUDE [model-router 1](../../../foundry/openai/includes/concepts-model-router-1.md)]

## Routing mode

With the latest version, if you choose custom deployment, you can select the **routing mode** to optimize for quality or cost while maintaining a baseline level of performance. Setting a routing mode is optional, and if you don't set one, your deployment defaults to the Balanced mode.

Available routing modes:

| Mode | Description |
|------|-----------|
| Balanced (default) | Considers both cost and quality dynamically. Perfect for general-purpose scenarios |
| Quality | Prioritizes for maximum accuracy. Best for complex reasoning or critical outputs |
| Cost | Prioritizes for more cost savings. Ideal for high-volume, budget-sensitive workloads |

## Model subset

The latest version of model router supports model subsets: For custom deployments, you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics.

When new base models become available, they're not included in your selection unless you explicitly add them to your deployment's inclusion list.

## Automatic failover

Model router now includes built-in automatic failover. When using the default deployment to route to all supported models, model router transparently redirects the request to the next most appropriate model, so transient issues with any single model don't disrupt your application. Failover is enabled by default — no additional configuration is required.

For custom deployment configurations:

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal documentation** - [For the new features, switch to the new Foundry portal](../../../foundry/openai/concepts/model-router.md)
- Your selected routing mode (Balanced, Cost, or Quality) continues to apply during failover.
- Your configured model subset also works as your fallback set to prevent your prompts getting processed by unapproved models. Therefore, be sure to select model subsets with atleast two models to benefit from the fallback capability.

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

To overcome the limits on context window and parameters, use the Model subset feature to select your models for routing that support your desired properties.

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

Model router usage is charged for input prompts at the rate listed on the pricing page.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
