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

## Model subset

The latest version of model router supports model subsets: For custom deployments, you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics.

When new base models become available, they're not included in your selection unless you explicitly add them to your deployment's inclusion list.

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

Starting November 2025, the model router usage will be charged for input prompts at the rate listed on the pricing page.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
