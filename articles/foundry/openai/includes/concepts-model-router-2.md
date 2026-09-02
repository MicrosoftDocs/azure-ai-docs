---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/01/2026
ms.custom: include
ai-usage: ai-assisted
---

## Model subset

The latest version of model router supports model subsets: You can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics.

When new base models become available, they're not included in your selection unless you explicitly add them to your deployment's inclusion list.

## Automatic failover

Model router now includes built-in automatic failover. When using the default deployment to route to all supported models, model router transparently redirects the request to the next most appropriate model, so transient issues with any single model don't disrupt your application. Failover is enabled by default — no additional configuration is required.

For custom deployment configurations:
- Your selected routing mode (Balanced, Cost, or Quality) continues to apply during failover.
- Your configured model subset also works as your fallback set to prevent your prompts from getting processed by unapproved models. Therefore, be sure to select model subsets with at least two models to benefit from the fallback capability.

To inspect ordered model attempts and determine whether fallback occurred for an individual Chat Completions request, see [Monitor model router](../how-to/monitor-model-router.md).

## Prompt caching

Model router supports prompt caching because requests are processed by the underlying models that support it. When model router delegates a request to a model that supports prompt caching, cached tokens are used automatically — no extra configuration is needed.

Cache behavior depends on which underlying model the router selects for a given request. Because routing decisions might vary, caching benefits apply only when the same model handles consecutive requests with overlapping prompt prefixes.

For details on how prompt caching works and which models support it, see [Prompt caching](../how-to/prompt-caching.md).

## Limitations

To overcome the limits on context window and parameters, use the Model subset feature to select your models for routing that support your desired properties.

> [!NOTE]
> The context window limit listed for model router is the limit of the smallest underlying model. Other underlying models are compatible with larger context windows, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model. To review context windows for the underlying models, see [Azure OpenAI in Microsoft Foundry models](../../foundry-models/concepts/models-sold-directly-by-azure.md).
>
> To shorten the context window, you can do one of the following:
> - Summarize the prompt before passing it to the model
> - Truncate the prompt into more relevant parts
> - Use document embeddings and have the chat model retrieve relevant sections. For more information, see [What is Azure AI Search?](../../../search/search-what-is-azure-search.md)

### Quota tiers

Model router limits scale with your subscription's usage tier. For information on how tiers work, see [Quota tiers](../quotas-limits.md#quota-tiers).

| Tier   | GlobalStandard RPM | GlobalStandard TPM | DataZoneStandard RPM | DataZoneStandard TPM |
|:-------|-------------------:|-------------------:|---------------------:|---------------------:|
| Tier 1 | 1,000              | 1,000,000          | 300                  | 300,000              |
| Tier 2 | 2,000              | 2,000,000          | 670                  | 670,000              |
| Tier 3 | 4,000              | 4,000,000          | 1,000                | 1,000,000            |
| Tier 4 | 7,000              | 7,000,000          | 2,000                | 2,000,000            |
| Tier 5 | 10,000             | 10,000,000         | 3,000                | 3,000,000            |
| Tier 6 | 15,000             | 15,000,000         | 4,000                | 4,000,000            |

For other rate limit information, see [Quotas and limits](../quotas-limits.md).

Model router accepts image inputs for [Vision enabled chats](../how-to/gpt-with-vision.md) (all of the underlying models can accept image input), but the routing decision is based on the text input only.

Model router doesn't process audio input.

## Troubleshooting

| Issue | Resolution |
| ------- | ------------ |
| Deployment fails | Verify your Foundry resource is in a [supported region](../concepts/model-router.md#supported-regions). |
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
