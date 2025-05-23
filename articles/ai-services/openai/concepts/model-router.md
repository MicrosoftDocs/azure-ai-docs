---
title: Model router for Azure AI Foundry (preview) concepts
titleSuffix: Azure OpenAI
description: Learn about the model router feature in Azure OpenAI in Azure AI Foundry Models.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 05/08/2025
ms.custom: 
manager: nitinme
---

# Model router for Azure AI Foundry (preview)

Model router for Azure AI Foundry is a deployable AI chat model that is trained to select the best large language model (LLM) to respond to a given prompt in real time. By evaluating factors like query complexity, cost, and performance, it intelligently routes requests to the most suitable model. Thus, it delivers high performance while saving on compute costs where possible, all packaged as a single model deployment.

## Why use model router?

Model router intelligently selects the best underlying model for a given prompt to optimize costs while maintaining quality. Smaller and cheaper models are used when they're sufficient for the task, but larger and more expensive models are available for more complex tasks. Also, reasoning models are available for tasks that require complex reasoning, and non-reasoning models are used otherwise. Model router provides a single deployment and chat experience that combines the best features from all of the underlying chat models.

## Versioning 

Each version of model router is associated with a specific set of underlying models and their versions. This set is fixed&mdash;only newer versions of model router can expose new underlying models.

If you select **Auto-update** at the deployment step (see [Manage models](/azure/ai-services/openai/how-to/working-with-models?tabs=powershell#model-updates)), then your model router model automatically updates when new versions become available. When that happens, the set of underlying models also changes, which could affect the overall performance of the model and costs.

## Underlying models

|Model router version|Underlying models (version)|
|---|---|
|`2025-05-19`|GPT-4.1 (`2025-04-14`)</br>GPT-4.1-mini (`2025-04-14`)</br>GPT-4.1-nano (`2025-04-14`) </br>o4-mini (`2025-04-16`) |


## Limitations

### Resource limitations

See the [Models](../concepts/models.md#model-router) page for the region availability and deployment types for model router.

### Technical limitations

See [Quotas and limits](/azure/ai-services/openai/quotas-limits) for rate limit information.

> [!NOTE]
> The context window limit listed on the [Models](../concepts/models.md#model-router) page is the limit of the smallest underlying model. Other underlying models are compatible with larger context windows, which means an API call with a larger context will succeed only if the prompt happens to be routed to the right model, otherwise the call will fail. To shorten the context window, you can do one of the following:
> - Summarize the prompt before passing it to the model
> - Truncate the prompt into more relevant parts
> - Use document embeddings and have the chat model retrieve relevant sections: see [Azure AI Search](/azure/search/search-what-is-azure-search) 

Model router accepts image inputs for [Vision enabled chats](/azure/ai-services/openai/how-to/gpt-with-vision) (all of the underlying models can accept image input), but the routing decision is based on the text input only.

Model router doesn't process audio input.

## Billing information

When you use model router today, you're only billed for the use of the underlying models as they're recruited to respond to prompts: the model routing function itself doesn't incur any extra charges. Starting August 1, the model router usage will be charged as well.

You can monitor the costs of your model router deployment in the Azure portal.

## Next step

> [!DIV class="nextstepaction"]
> [How to use model router](../how-to/model-router.md)
