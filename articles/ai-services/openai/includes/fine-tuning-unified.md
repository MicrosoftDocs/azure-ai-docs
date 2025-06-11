---
title: "Customize a model with Azure OpenAI in Azure AI Foundry Models and Azure AI Foundry"
titleSuffix: Azure OpenAI
description: Learn how to create your own custom model with Azure OpenAI by using the Azure AI Foundry portal.
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 11/11/2024
ms.service: azure-ai-openai
ms.topic: include
ms.custom:
  - build-2025
---

There are two unique fine-tuning experiences in the Azure AI Foundry portal:

* [Hub/Project view](https://ai.azure.com/?cid=learnDocs) - supports fine-tuning models from multiple providers including Azure OpenAI, Meta Llama, Microsoft Phi, etc.
* [Azure OpenAI centric view](https://ai.azure.com/resource/overview) - only supports fine-tuning Azure OpenAI models, but has support for additional features like the [Weights & Biases (W&B) preview integration](../how-to/weights-and-biases-integration.md). 

If you are only fine-tuning Azure OpenAI models, we recommend the Azure OpenAI centric fine-tuning experience which is available by navigating to [https://ai.azure.com/resource/overview](https://ai.azure.com/resource/overview). 

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

# [Azure OpenAI](#tab/azure-openai)

[!INCLUDE [Azure AI Foundry resource view fine-tuning](../includes/fine-tuning-studio.md)]

# [Hub/Project](#tab/hub)

[!INCLUDE [Azure AI Foundry project fine-tuning](../includes/fine-tuning-openai-in-ai-studio.md)]

---
