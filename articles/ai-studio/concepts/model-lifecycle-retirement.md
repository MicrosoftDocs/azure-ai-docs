---
title: Deprecation and retirement for models in Azure AI model catalog
titleSuffix: Azure AI Foundry
description: Learn about the lifecycle stages, deprecation, and retirement for models in the Azure AI model catalog.
manager: scottpolly
ms.service: azure-ai-studio
ms.topic: concept-article
ms.date: 11/22/2024
ms.author: mopeakande
author: msakande
ms.reviewer: kritifaujdar
reviewer: fkriti

#Customer intent: As a data scientist, I want to learn about the lifecycle of models that are available in the model catalog.
---

# Model deprecation and retirement in Azure AI model catalog

Models in the model catalog are continually refreshed with newer and more capable models. As part of this process, model providers might deprecate and retire their older models, and you might need to update your applications to use a newer model. This document communicates information about the model lifecycle and deprecation timelines and explains how you're informed of model lifecycle stages.

> [!IMPORTANT]
> This article describes deprecation and retirement only for models that can be deployed to __serverless APIs__, not managed compute. To learn more about the differences between deployment to serverless APIs and managed computes, see [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md).

> [!NOTE]
> Azure OpenAI models in the model catalog are provided through Azure OpenAI Service. For information about Azure Open AI model deprecation and retirement, see the [Azure OpenAI service product documentation](/azure/ai-services/openai/concepts/model-retirements).

## Model lifecycle stages

Models in the model catalog belong to one of these stages:

- Preview
- Generally available
- Legacy
- Deprecated
- Retired

### Preview

Models labeled _Preview_ are experimental in nature. A model's weights, runtime, and API schema can change while the model is in preview. Models in preview aren't guaranteed to become generally available. Models in preview have a _Preview_ label next to their name in the model catalog.  

### Generally available

This stage is the default model stage. Models that don't include a lifecycle label next to their name are generally available and suitable for use in production environments. In this stage, model weights and APIs are fixed. However, model containers or runtimes with vulnerabilities might get patched, but patches won't affect model outputs.  
 
### Legacy

Models labeled _Legacy_ are intended for deprecation. You should plan to move to a different model, such as a new, improved model that might be available in the same model family. While a model is in the legacy stage, existing deployments of the model continue to work, and you can create new deployments of the model until the deprecation date.

### Deprecated

Models labeled _Deprecated_ are no longer available for new deployments. You can't create any new deployments for the model; however, existing deployments continue to work until the retirement date.

### Retired

Models labeled _Retired_ are no longer available for use. You can't create new deployments, and attempts to use existing deployments return `<return code>` errors.


## Notifications

- Models are labeled as _Legacy_ and remain in the legacy state for at least 30 days before being moved to the deprecated state. During this notification period, you may create new deployments as you prepare for deprecation and retirement.

- Models are labeled _Deprecated_ and remain in the deprecated state for at least 90 days before being moved to the retired state. During this notification period, you can migrate any existing deployments to newer or replacement models.

- Members of the _owner_, _contributor_, _reader_, monitoring contributor_, and _monitoring reader_ roles for each Azure subscription with a serverless API model deployment receive a notification when a model deprecation is announced. The notification contains the dates when the model enters legacy, deprecated, and retired states. The notification might provide information about possible replacement model options, if applicable.



| Model provider | Model | Legacy date | Deprecation date | Retirement date | Suggested replacement model |
| ---- | ---- | ---- | --- | ---- | --- |
| Mistral AI | [Mistral-large](https://aka.ms/azureai/landing/Mistral-Large) | December 15, 2024 | January 15, 2025 | April 15, 2025 | [Mistral-large-2407](https://aka.ms/azureai/landing/Mistral-Large-2407) |

## Related content

- [Model catalog and collections in Azure AI Foundry portal](../how-to/model-catalog-overview.md)
- [Data, privacy, and security for use of models through the model catalog in Azure AI Foundry portal](../how-to/concept-data-privacy.md)