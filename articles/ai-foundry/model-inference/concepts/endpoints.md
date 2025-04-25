---
title: Model inference endpoint in Azure AI services
titleSuffix: Azure AI Foundry
description: Learn about the model inference endpoint in Azure AI services
author: santiagxf
manager: nitinme
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Model inference endpoint in Azure AI Services

Azure AI model inference in Azure AI services allows customers to consume the most powerful models from flagship model providers using a single endpoint and credentials. This means that you can switch between models and consume them from your application without changing a single line of code.

The article explains how models are organized inside of the service and how to use the inference endpoint to invoke them.

## Deployments

Azure AI model inference makes models available using the **deployment** concept. **Deployments** are a way to give a model a name under certain configurations. Then, you can invoke such model configuration by indicating its name on your requests.

Deployments capture:

> [!div class="checklist"]
> * A model name
> * A model version
> * A provisioning/capacity type<sup>1</sup>
> * A content filtering configuration<sup>1</sup>
> * A rate limiting configuration<sup>1</sup>

<sup>1</sup> Configurations may vary depending on the selected model.

An Azure AI services resource can have as many model deployments as needed and they don't incur in cost unless inference is performed for those models. Deployments are Azure resources and hence they're subject to Azure policies.

To learn more about how to create deployments see [Add and configure model deployments](../how-to/create-model-deployments.md).

## Azure AI inference endpoint

The Azure AI inference endpoint allows customers to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. This endpoint follows the [Azure AI model inference API](.././reference/reference-model-inference-api.md) which all the models in Azure AI model inference support. It support the following modalities:

* Text embeddings
* Image embeddings
* Chat completions

You can see the endpoint URL and credentials in the **Overview** section:

:::image type="content" source="../media/overview/overview-endpoint-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the resource." lightbox="../media/overview/overview-endpoint-and-key.png":::

### Routing

The inference endpoint routes requests to a given deployment by matching the parameter `name` inside of the request to the name of the deployment. This means that *deployments work as an alias of a given model under certain configurations*. This flexibility allows you to deploy a given model multiple times in the service but under different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a Meta-llama-3.2-8b-instruct model by indicating such name in the parameter 'model' inside of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, then such deployment can be invoked as:

[!INCLUDE [code-create-chat-client](../includes/code-create-chat-client.md)]

[!INCLUDE [code-create-chat-completion](../includes/code-create-chat-completion.md)]

> [!TIP]
> Deployment routing isn't case sensitive.

### SDKs

The Azure AI model inference endpoint is supported by multiple SDKs, including the **Azure AI Inference SDK**, the **Azure AI Foundry SDK**, and the **Azure OpenAI SDK**; which are available in multiple languages. Multiple integrations are also supported in popular frameworks like LangChain, LangGraph, Llama-Index, Semantic Kernel, and AG2. See [supported programming languages and SDKs](../supported-languages.md) for details.

## Azure OpenAI inference endpoint

Azure OpenAI models deployed to AI services also support the Azure OpenAI API. This API exposes the full capabilities of OpenAI models and supports additional features like assistants, threads, files, and batch inference.

Azure OpenAI inference endpoints work at the deployment level and they have their own URL that is associated with each of them. However, the same authentication mechanism can be used to consume them. Learn more in the reference page for [Azure OpenAI API](../../../ai-services/openai/reference.md)

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that is the concatenations of the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

> [!IMPORTANT]
> There's no routing mechanism for the Azure OpenAI endpoint, as each URL is exclusive for each model deployment.

### SDKs

The Azure OpenAI endpoint is supported by the **OpenAI SDK (`AzureOpenAI` class)** and **Azure OpenAI SDKs**, which are available in multiple languages. See [supported languages](../supported-languages.md#azure-openai-models) for details. 


## Next steps

- [Models](models.md)
- [Deployment types](deployment-types.md)
