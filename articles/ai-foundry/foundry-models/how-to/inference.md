---
title: How to use the Azure AI Foundry Models inference endpoints to consume models
titleSuffix: Azure AI Foundry
description: Learn how to use the Azure AI Foundry Models inference endpoint to consume models
manager: scottpolly
author: msakande
reviewer: santiagxf
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
ms.author: mopeakande
ms.reviewer: fasantia
---

# Use Foundry Models

Once you have [deployed a model in Azure AI Foundry](../../model-inference/how-to/create-model-deployments.md), you can consume its capabilities via Azure AI Foundry APIs. There are two different endpoints and APIs to use models in Azure AI Foundry Models.

## Models inference endpoint

The models inference endpoint (usually with the form `https://<resource-name>.services.ai.azure.com/models`) allows customers to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. This endpoint follows the [Azure AI Model Inference API](../../model-inference/reference/reference-model-inference-api.md) which all the models in Foundry Models support. It supports the following modalities:

* Text embeddings
* Image embeddings
* Chat completions

### Routing

The inference endpoint routes requests to a given deployment by matching the parameter `name` inside of the request to the name of the deployment. This means that *deployments work as an alias of a given model under certain configurations*. This flexibility allows you to deploy a given model multiple times in the service but under different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a Meta-llama-3.2-8b-instruct model by indicating such name in the parameter 'model' inside of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, then such deployment can be invoked as:

[!INCLUDE [code-create-chat-client](../../model-inference/includes/code-create-chat-client.md)]

[!INCLUDE [code-create-chat-completion](../../model-inference/includes/code-create-chat-completion.md)]

> [!TIP]
> Deployment routing isn't case sensitive.


## Azure OpenAI inference endpoint

Azure AI Foundry also support the Azure OpenAI API. This API exposes the full capabilities of OpenAI models and supports additional features like assistants, threads, files, and batch inference. Non-OpenAI models can also be used for compatible functionalities.

Azure OpenAI endpoints (usually with the form `https://<resource-name>.openai.azure.com`) work at the deployment level and they have their own URL that is associated with each of them. However, the same authentication mechanism can be used to consume them. Learn more in the reference page for [Azure OpenAI API](../../../ai-services/openai/reference.md)

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that is the concatenations of the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

[!INCLUDE [code-create-openai-client](../../model-inference/includes/code-create-openai-client.md)]

[!INCLUDE [code-create-openai-chat-completion](../../model-inference/includes/code-create-openai-chat-completion.md)]


## Next steps

* [Use embedding models](../../model-inference/how-to/use-embeddings.md)
* [Use chat completion models](../../model-inference/how-to/use-chat-completions.md)
