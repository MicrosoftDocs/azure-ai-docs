---
title: Add and configure models to Azure AI services
titleSuffix: Azure AI services
description: Learn how to add and configure new models to the Azure AI model's inference endpoint in Azure AI services.
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/01/2024
ms.custom: ignite-2024, github-universe-2024
manager: nitinme
author: mrbullwinkle
ms.author: fasantia 
recommendations: false
---

# Add and configure models to Azure AI services

You can decide and configure which models are available for inference in the Azure AI services resource model's inference endpoint. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.

In this article, you will learn how to add a new model to the Azure AI model inference service in Azure AI services.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you are using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI Models in AI Services](quickstart-github-models.md) if that's your case.
* An Azure AI services resource. See [Create an Azure AI Services resource](../../multi-service-resource.md??context=/azure/ai-services/model-inference/context/context) for more details.


## Add a models

[!INCLUDE [add-model-deployments](../includes/add-model-deployments.md)]

## Use the model

Deployed models in Azure AI services can be consumed using the [Azure AI model's inference endpoint](../concepts/endpoints.md) for the resource.

To use it:

1. Get the Azure AI model's inference endpoint URL and keys from the **deployment page** or the **Overview** page. If you are using Microsoft Entra ID authentication, you don't need a key.

    :::image type="content" source="../media/add-model-deployments/models-deploy-endpoint-url.png" alt-text="An screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/add-model-deployments/models-deploy-endpoint-url.png":::

2. When constructing your request, indicate the parameter `model` and insert the model deployment name you have created.

    [!INCLUDE [code-create-chat-completion](../includes/code-create-chat-completion.md)]

3. When using the endpoint, you can change the `model` parameter to any available model deployment in your resource.

Additionally, Azure OpenAI models can be consumed using the [Azure OpenAI service endpoint](../../openai/supported-languages.md) in the resource. This endpoint is exclusive for each model deployment and has its own URL.

## Model deployment customization

When creating model deployments, you can configure additional settings including content filtering and rate limits. To configure this settings, select the option **Customize** in the deployment wizard.

> [!NOTE]
> Configurations may vary depending on the model you are deploying.

## Next steps

* [Develop applications using Azure AI model inference service in Azure AI services](../supported-languages.md)