---
title: "Endpoints for Microsoft Foundry Models (classic)"
description: "Learn how to access and use Microsoft Foundry Models endpoints for secure model inference, flexible deployments, and keyless authentication. (classic)"
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 11/21/2025
ms.author: mopeakande
ms.custom:
  - build-2025
  - classic-and-new
ai-usage: ai-assisted

#CustomerIntent: As a developer using Microsoft Foundry Models, I want to understand how to access and use Foundry Model endpoints so that I can integrate models into my applications with secure authentication and flexible deployment options.
ROBOTS: NOINDEX, NOFOLLOW
---

# Endpoints for Microsoft Foundry Models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/foundry-models/concepts/endpoints.md)

[!INCLUDE [endpoints 1](../../../foundry/foundry-models/includes/concepts-endpoints-1.md)]

## Endpoints

Foundry services provide multiple endpoints depending on the type of work you want to perform:

* [Azure AI inference endpoint](#azure-ai-inference-endpoint)
* [Azure OpenAI inference endpoint](#azure-openai-inference-endpoint)

## Azure AI inference endpoint

> [!NOTE]
> The Azure AI Inference SDK samples in this section remain fully functional. However, for new projects, we recommend using the [Azure OpenAI endpoint](#azure-openai-inference-endpoint) with the OpenAI SDK. For migration guidance, see [Migrate from Azure AI Inference SDK to OpenAI SDK](../../how-to/model-inference-to-openai-migration.md).

The **Azure AI inference endpoint**, usually of the form `https://<resource-name>.services.ai.azure.com/models`, enables you to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. All Foundry Models support this capability. This endpoint follows the [Azure AI Model Inference API](/rest/api/aifoundry/modelinference), which supports the following modalities:

* Text embeddings
* Image embeddings
* Chat completions

### Routing

The inference endpoint routes requests to a specific deployment by matching the `name` parameter in the request to the name of the deployment. This setup means that *deployments work as an alias for a model under certain configurations*. This flexibility lets you deploy a model multiple times in the service but with different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a model by indicating the model name in the 'model' parameter of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, you can invoke that deployment as follows:

[!INCLUDE [code-create-chat-client](../../../foundry/foundry-models/includes/code-create-chat-client.md)]

For a chat model, you can create a request as follows:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

If you specify a model name that doesn't match any model deployment, you get an error that the model doesn't exist. You control which models are available to users by creating model deployments. For more information, see [add and configure model deployments](../how-to/create-model-deployments.md).

[!INCLUDE [endpoints 2](../../../foundry/foundry-models/includes/concepts-endpoints-2.md)]

## Limitations

* You can't use Azure OpenAI Batch with the Foundry Models endpoint. You have to use the dedicated deployment URL as explained in [Batch API support in Azure OpenAI documentation](../../openai/how-to/batch.md).
* Real-time API isn't supported in the inference endpoint. Use the dedicated deployment URL.

[!INCLUDE [endpoints 3](../../../foundry/foundry-models/includes/concepts-endpoints-3.md)]
