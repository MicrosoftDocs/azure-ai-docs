---
title: What's new in model router in Microsoft Foundry Models?
description: Learn about the latest news and features updates for Azure model router.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.date: 02/10/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: whats-new
monikerRange: 'foundry-classic || foundry'

---

# What's new in model router in Microsoft Foundry Models?

This article provides a summary of the latest releases and major documentation updates for Azure model router, including new supported models, routing features, and deployment options.

[!INCLUDE [version-banner](../includes/version-banner.md)]

## November 2025

### Anthropic models added

Version `2025-11-18` of model router adds support for three Anthropic models: `claude-haiku-4-5`, `claude-opus-4-1`, and `claude-sonnet-4-5`. To include these in your model router deployment, you need to first deploy them yourself to your Foundry resource (see [Deploy and use Claude models](/azure/ai-foundry/foundry-models/how-to/use-foundry-models-claude?view=foundry&tabs=python)). Then enable them with [model subset configuration](/azure/ai-foundry/openai/how-to/model-router?view=foundry) in your model router deployment.


### Model router GA version

A new model router model is now available. Version `2025-11-18` includes support for all underlying models in previous versions, as well as 10 new language models. 

It also includes new features that make it more versatile and effective.
- **Routing profiles** let you skew model router's choices to optimize for quality or cost while maintaining a baseline level of performance.
- Model router supports **custom subsets**: you can specify which underlying models to include in routing decisions. This gives you more control over cost, compliance, and performance characteristics.
- Model router supports **Global Standard** and **Data Zone Standard** deployment types in East US 2 and Sweden Central regions.

For more information on model router and its capabilities, see the [Model router concepts guide](../openai/concepts/model-router.md).

## August 2025

### New version of model router (preview)

- Model router now supports GPT-5 series models.

- Model router for Microsoft Foundry is a deployable AI chat model that automatically selects the best underlying chat model to respond to a given prompt. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](../openai/concepts/model-router.md). To use model router with the Completions API, follow the [How-to guide](../openai/how-to/model-router.md).

## May 2025

### Model router (preview)

Model router for Foundry is a deployable AI chat model that automatically selects the best underlying chat model to respond to a given prompt. For more information on how model router works and its advantages and limitations, see the [Model router concepts guide](../openai/concepts/model-router.md). To use model router with the Completions API, follow the [How-to guide](../openai/how-to/model-router.md).