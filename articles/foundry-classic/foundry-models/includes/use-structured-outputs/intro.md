---
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 05/29/2025
ms.reviewer: fasantia
reviewer: santiagxf
ms.author: mopeakande
author: msakande
ms.custom: include
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

Free-form outputs of language models can be difficult to parse by software applications. Structured outputs, like JSON, provide a clear format that software applications can read and process. This article explains how to use structured outputs to generate specific JSON schemas with the chat completions API for models deployed in Microsoft Foundry Models.

The following list describes typical scenarios where structured outputs are useful:

* You need to extract specific information from a prompt and such information can be described as a schema with specific keys and types.
* You need to parse information contained in the prompts.
* You're using the model to control a workflow in your application where you can benefit from more rigid structures.
* You're using the model as a zero-shot or few-shot learner.

## Prerequisites

To use structured outputs with chat completions models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A chat completions model deployment with JSON and structured outputs support. If you don't have one, read [Add and configure Foundry Models](../../how-to/create-model-deployments.md).

    * You can check which models support structured outputs by checking the column **Response format** in the [Models](../../concepts/models-sold-directly-by-azure.md) article.

    * This article uses `gpt-4o`.