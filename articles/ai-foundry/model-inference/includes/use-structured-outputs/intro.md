---
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: include
ms.date: 1/31/2025
ms.author: fasantia
author: santiagxf
---

[!INCLUDE [Feature preview](~/reusable-content/ce-skilling/azure/includes/ai-studio/includes/feature-preview.md)]

When working with software, it's more challenging to parse free-form text outputs coming from language models. Structured outputs, like JSON, provide a clear format that software routines can read and process. This article explains how to use structured outputs to generate specific JSON schemas with the chat completions API with models deployed in Azure AI Foundry Models.

Typical scenarios of structured outputs include:

> [!div class="checklist"]
> * You need to extract specific information from a prompt and such information can be described as an schema with specific keys and types.
> * You need to parse information contained in the prompts.
> * You are using the model to control a workflow in your application where you can benefit from more rigid structures.
> * You are using the model as a zero-shot or few-shot learner.

## Prerequisites

To use structured outputs with chat completions models in your application, you need:

[!INCLUDE [how-to-prerequisites](../how-to-prerequisites.md)]

* A chat completions model deployment with JSON and structured outputs support. If you don't have one read [Add and configure Foundry Models](../../how-to/create-model-deployments.md).

    * You can check which models support structured outputs by checking the column **Response format** in the [Models](../../concepts/models.md) article.

    * This article uses `gpt-4o`.