---
title: Azure OpenAI model router (preview) concepts
titleSuffix: Azure OpenAI
description: Learn about the model router feature in Azure OpenAI Service.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 05/08/2025
ms.custom: 
manager: nitinme
---

# Azure OpenAI model router (preview)

Azure OpenAI model router is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. 

## Why use model router?

Model router intelligently selects the best underlying model for a given prompt to optimize costs while maintaining quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single chat experience that combines the best features from all of the underlying chat models.

## Versioning 

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed&mdash;only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Manage models](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

## Underlying models

|Model router version|Underlying models (version)|
|---|---|
|`2025-04-15`|GPT-4.1 (`2025-04-14`)</br>GPT-4.1-mini (`2025-04-14`)</br>GPT-4.1-nano (`2025-04-14`) </br>o4-mini (`2025-04-16`) |


## Limitations

See [Quotas and limits](/azure/ai-services/openai/quotas-limits).

Model router doesn't process input images or audio.

## Billing information

When you use Azure OpenAI model router, you're only billed for the use of the underlying models as they're recruited to respond to prompts. The model router itself doesn't incur any extra charges.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
