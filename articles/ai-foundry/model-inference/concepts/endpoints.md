---
title: Endpoints for Azure AI Foundry Models
titleSuffix: Azure AI Foundry
description: Learn about the Azure AI Foundry Models endpoint
author: msakande
manager: scottpolly
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
ms.author: mopeakande
ms.custom: ignite-2024, github-universe-2024
ms.reviewer: fasantia
reviewer: santiagxf
---

# Endpoints for Azure AI Foundry Models

Azure AI Foundry Models allows customers to consume the most powerful models from flagship model providers using a single endpoint and credentials. This means that you can switch between models and consume them from your application without changing a single line of code.

The article explains how models are organized inside of the service and how to use the inference endpoint to invoke them.

## Deployments

Azure AI Foundry makes models available using the **deployment** concept. **Deployments** are a way to give a model a name under certain configurations. Then, you can invoke such model configuration by indicating its name on your requests.

Deployments capture:

> [!div class="checklist"]
> * A model name
> * A model version
> * A provisioning/capacity type<sup>1</sup>
> * A content filtering configuration<sup>1</sup>
> * A rate limiting configuration<sup>1</sup>

<sup>1</sup> Configurations may vary depending on the selected model.

An Azure AI Foundry resource can have as many model deployments as needed and they don't incur in cost unless inference is performed for those models. Deployments are Azure resources and hence they're subject to Azure policies.

To learn more about how to create deployments see [Add and configure model deployments](../how-to/create-model-deployments.md).

## Endpoints

Azure AI Foundry Services (formerly known Azure AI Services) expose multiple endpoints depending on the type of work you're looking for:

> [!div class="checklist"]
> * Azure AI inference endpoint (usually with the form `https://<resource-name>.services.ai.azure.com/models`)
> * Azure OpenAI endpoint (usually with the form `https://<resource-name>.openai.azure.com`)

The **Azure AI inference endpoint** allows customers to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. All the models support this capability. This endpoint follows the [Azure AI Model Inference API](.././reference/reference-model-inference-api.md). 

The **Azure OpenAI API** exposes the full capabilities of OpenAI models and supports more features like assistants, threads, files, and batch inference. Non-OpenAI models may also be exposed in this route.

To learn more about how to apply the **Azure OpenAI endpoint** see [Azure OpenAI in Azure AI Foundry Models documentation](../../../ai-services/openai/overview.md).

## Using Azure AI inference endpoint

The inference endpoint routes requests to a given deployment by matching the parameter `name` inside of the request to the name of the deployment. This means that *deployments work as an alias of a given model under certain configurations*. This flexibility allows you to deploy a given model multiple times in the service but under different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a Meta-llama-3.2-8b-instruct model by indicating such name in the parameter 'model' inside of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, then such deployment can be invoked as:

[!INCLUDE [code-create-chat-client](../includes/code-create-chat-client.md)]

For a chat model, you can create a request as follows:

[!INCLUDE [code-create-chat-completion](../includes/code-create-chat-completion.md)]

If you specify a model name that doesn't match any given model deployment, you get an error that the model doesn't exist. You can control which models are available for users by creating model deployments as explained at [add and configure model deployments](../how-to/create-model-deployments.md).

## Key-less authentication

Models deployed to Azure AI Foundry Models in Azure AI Services support key-less authorization using Microsoft Entra ID. Key-less authorization enhances security, simplifies the user experience, reduces operational complexity, and provides robust compliance support for modern development. It makes it a strong choice for organizations adopting secure and scalable identity management solutions.

To use key-less authentication, [configure your resource and grant access to users](../how-to/configure-entra-id.md) to perform inference. Once configured, then you can authenticate as follows:

[!INCLUDE [code-create-chat-client-entra](../includes/code-create-chat-client-entra.md)]

## Limitations

* Azure OpenAI Batch can't be used with the Foundry Models endpoint. You have to use the dedicated deployment URL as explained at [Batch API support in Azure OpenAI documentation](../../../ai-services/openai/how-to/batch.md#api-support).
* Real-time API isn't supported in the inference endpoint. Use the dedicated deployment URL.

## Next steps

- [Models](models.md)
- [Deployment types](deployment-types.md)
