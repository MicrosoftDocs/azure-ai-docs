---
title: "Customize a Model with Azure OpenAI in Microsoft Foundry Models and Microsoft Foundry"
titleSuffix: Azure OpenAI
description: Learn how to create your own custom model with Azure OpenAI by using the Microsoft Foundry portal.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 11/11/2024
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom:
  - build-2025
---

There are two unique fine-tuning experiences in the Microsoft Foundry portal:

* [Hub or project view](https://ai.azure.com/?cid=learnDocs): Supports fine-tuning models from multiple providers, such as Azure OpenAI, Meta Llama, and Microsoft Phi.
* [Azure OpenAI-centric view](https://ai.azure.com/resource/overview): Supports only fine-tuning Azure OpenAI models, but has support for additional features like the [Weights & Biases (W&B) preview integration](../how-to/weights-and-biases-integration.md). If you're only fine-tuning Azure OpenAI models, we recommend this experience.

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

# [Azure OpenAI](#tab/azure-openai)

[!INCLUDE [Foundry resource view fine-tuning](../includes/fine-tuning-studio.md)]

# [Hub/Project](#tab/hub)

[!INCLUDE [Foundry project fine-tuning](../includes/fine-tuning-openai-in-ai-studio.md)]

---
