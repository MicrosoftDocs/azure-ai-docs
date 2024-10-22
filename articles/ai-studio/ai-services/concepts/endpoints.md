---
title: Model inference endpoint in Azure AI services
titleSuffix: Azure AI services
description: Learn about the model inference endpoint in Azure AI services
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-studio
ms.topic: concept
ms.date: 10/11/2024
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Model inference endpoint in Azure AI Services

Azure AI inference service in Azure AI services allow customers to consume the most powerful models from flagship model providers using a single endpoint and credentials. This means that you can switch between models and consume them from your application without changing a single line of code.

The article explains how models are organized inside of the service and how to use the inference endpoint to invoke them.

## Deployments

Azure AI model inference service make models available using the **deployment** concept. **Deployments** are a way to give a model a name under certain configurations. Then, you can invoke such model configuration by indicating its name on your requests.

Deployments capture:

> [!div class="checklist"]
> * A model name
> * A model version
> * A provisioning/capacity type<sup>1</sup>
> * A content filtering configuration<sup>1</sup>
> * A rate limiting configuration<sup>1</sup>

<sup>1</sup> Configurations may vary depending on the model you have selected.

An Azure AI services resource can have as many model deployments as needed and they don't incur in cost unless inference is performed for those models. Deployments are Azure resources and hence they are subject to Azure policies.

To learn more about how to create deployments see [Add and configure model deployments](../how-to/create-model-deployments.md).

## Azure AI inference endpoint

The Azure AI inference endpoint allow customers to use a single endpoint with the same authentication and schema to generate inference for the deployed models in the resource. This endpoint follows the [Azure AI model inference API](../../reference/reference-model-inference-api.md) which is supported by all the models in Azure AI model inference service.

You can see the endpoint URL and credentials in the **Overview** section:

:::image type="content" source="../media/overview/overview-endpoint-and-key.png" alt-text="An screenshot showing how to get the URL and key associated with the resource." lightbox="../media/overview/overview-endpoint-and-key.png":::

### Routing

The inference endpoint routes requests to a given deployment by matching the parameter `name` inside of the request to the name of the deployment. This means that *deployments work as an alias of a given model under certain configurations*. This flexibility allow you to deploy a given model multiple times in the service but under different configurations if needed.

:::image type="content" source="../media/endpoint/endpoint-routing.png" alt-text="An illustration showing how routing works for a Meta-llama-3.2-8b-instruct model by indicating such name in the parameter 'model' inside of the payload request." lightbox="../media/endpoint/endpoint-routing.png":::

For example, if you create a deployment named `Mistral-large`, then such deployment can be invoked as:

[!INCLUDE [code-create-chat-completion](../../includes/code-create-chat-completion.md)]

> [!TIP]
> Deployment routing is not case sensitive.

### SDKs

The Azure AI inference endpoint is supported by the **Azure AI inference SDK**, which is available in multiple languages. See [supported languages](../supported-languages.md) for details.

## Azure OpenAI inference endpoint

Azure OpenAI models deployed to AI services also support the Azure OpenAI API. This API exposes the full capabilities of OpenAI models and support additional features like assistants, threads, files, and batch inference.

Azure OpenAI inference endpoints are used per-deployment and they have they own URL that is associated with only one deployment. However, the same authentication mechanism can be used to consume it. Learn more in the reference page for [Azure OpenAI API](../../openai/reference.md)

:::image type="content" source="../media/endpoint/endpoint-openai.png" alt-text="An illustration showing how Azure OpenAI deployments contain a single URL for each deployment." lightbox="../media/endpoint/endpoint-openai.png":::

Each deployment has a URL that is the concatenations of the **Azure OpenAI** base URL and the route `/deployments/<model-deployment-name>`.

> [!IMPORTANT]
> There is no routing mechanism for the Azure OpenAI endpoint, as each URL is exclusive for each model deployment.

### SDKs

The Azure OpenAI endpoint is supported by the **OpenAI SDK (`AzureOpenAI` class)** and **Azure OpenAI SDKs**, which are available in multiple languages. See [supported languages](../supported-languages.md) for details. 


## Next steps

- [Models](models.md)
- [Deployment types](deployment-types.md)