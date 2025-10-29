﻿---
title: Endpoints for Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn how to access and use Azure AI Foundry Models endpoints for secure model inference, flexible deployments, and keyless authentication.
author: msakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 08/25/2025
ms.author: mopeakande
ms.custom: ignite-2024, github-universe-2024
ms.reviewer: fasantia
reviewer: santiagxf
ai-usage: ai-assisted

#CustomerIntent: As a developer using Azure AI Foundry Models, I want to understand how to access and use Foundry Model endpoints so that I can integrate models into my applications with secure authentication and flexible deployment options.
---

# Endpoints for Azure AI Foundry Models

Azure AI Foundry Models enables you to access the most powerful models from leading model providers through a single endpoint and set of credentials. This capability lets you switch between models and use them in your application without changing any code.

This article explains how the Azure AI Foundry services (formerly known as Azure AI Services) organize models and how to use the inference endpoint to access them.

## Deployments

Azure AI Foundry uses **deployments** to make models available. **Deployments** give a model a name and set specific configurations. You can access a model by using its deployment name in your requests.

A deployment includes:

* A model name
* A model version
* A provisioning or capacity type<sup>1</sup>
* A content filtering configuration<sup>1</sup>
* A rate limiting configuration<sup>1</sup>

<sup>1</sup> These configurations can change depending on the selected model.

An Azure AI Foundry resource can have many model deployments. You only pay for inference performed on model deployments. Deployments are Azure resources, so they're subject to Azure policies.

For more information about creating deployments, see [Add and configure model deployments](../../model-inference/how-to/create-model-deployments.md).

## Endpoints

Azure AI Foundry services provide multiple endpoints depending on the type of work you want to perform:

* [Azure AI inference endpoint](#azure-ai-inference-endpoint)
* [Azure OpenAI inference endpoint](#azure-openai-inference-endpoint)


## Azure AI inference endpoint

The **Azure AI inference endpoint**, usually of the form `https://<resource-name>.services.ai.azure.com/models`, enables you to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. All Foundry Models support this capability. This endpoint follows the [Azure AI Model Inference API](../../model-inference/reference/reference-model-inference-api.md), which supports the following modalities:

* Text embeddings
* Image embeddings
* Chat completions


### Routing

The inference endpoint routes requests to a specific deployment by matching the `name` parameter in the request to the name of the deployment. This setup means that *deployments work as an alias for a model under certain configurations*. This flexibility lets you deploy a model multiple times in the service but with different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a model by indicating the model name in the 'model' parameter of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, you can invoke that deployment as follows:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

For a chat model, you can create a request as follows:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

If you specify a model name that doesn't match any model deployment, you get an error that the model doesn't exist. You control which models are available to users by creating model deployments. For more information, see [add and configure model deployments](../../model-inference/how-to/create-model-deployments.md).


## Azure OpenAI inference endpoint

The **Azure OpenAI API** exposes the full capabilities of OpenAI models and supports more features like assistants, threads, files, and batch inference. You might also access non-OpenAI models through this route.

Azure OpenAI endpoints, usually of the form `https://<resource-name>.openai.azure.com`, work at the deployment level and each deployment has its own associated URL. However, you can use the same authentication mechanism to consume the deployments. For more information, see the reference page for [Azure OpenAI API](../../openai/reference.md).

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that's formed by concatenating the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

[!INCLUDE [code-create-openai-client](../includes/code-create-openai-client.md)]

[!INCLUDE [code-create-openai-chat-completion](../includes/code-create-openai-chat-completion.md)]

For more information about how to use the **Azure OpenAI endpoint**, see [Azure OpenAI in Azure AI Foundry Models documentation](../../openai/overview.md).

## Keyless authentication

Models deployed to Azure AI Foundry Models in Azure AI services support keyless authorization by using Microsoft Entra ID. Keyless authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. It makes keyless authorization a strong choice for organizations adopting secure and scalable identity management solutions.

To use keyless authentication, [configure your resource and grant access to users](../../model-inference/how-to/configure-entra-id.md) to perform inference. After you configure the resource and grant access, authenticate as follows:

[!INCLUDE [code-create-chat-client-entra](../../foundry-models/includes/code-create-chat-client-entra.md)]

## Limitations

* You can't use Azure OpenAI Batch with the Foundry Models endpoint. You have to use the dedicated deployment URL as explained in [Batch API support in Azure OpenAI documentation](../../../ai-services/openai/how-to/batch.md#api-support).
* Real-time API isn't supported in the inference endpoint. Use the dedicated deployment URL.

## Related content

- [Foundry Models and capabilities](models.md)
- [Deployment types in Azure AI Foundry Models](deployment-types.md)
- [What is Azure OpenAI in Azure AI Foundry Models?](../../openai/overview.md)

