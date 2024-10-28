---
title: Add and configure models to Azure AI services
titleSuffix: Azure AI services
description: Learn how to add and configure new models to the Azure AI model's inference endpoint in Azure AI services.
ms.service: azure-ai-studio
ms.topic: how-to
author: sdgilley
manager: scottpolly
ms.date: 10/24/2024
ms.author: sgilley
ms.reviewer: fasantia
recommendations: false
---

# Add and configure models to Azure AI services

You can decide and configure which models are available for inference in the Azure AI services resource model's inference endpoint. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.

In this article, you learn how to add a new model to the Azure AI model inference service in Azure AI services.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Learn more at [Upgrade from GitHub Models to Azure AI Models in AI Services](quickstart-github-models.md).
* An Azure AI services resource. For more information, see [Create an Azure AI Services resource](../../../ai-services/multi-service-resource.md??context=/azure/ai-studio/context/context).


## Add a model

[!INCLUDE [add-model-deployments](../../includes/ai-services/add-model-deployments.md)]

## Use the model

Deployed models in Azure AI services can be consumed using the [Azure AI model's inference endpoint](../concepts/endpoints.md) for the resource.

To use it:

1. Get the Azure AI model's inference endpoint URL and keys from the **deployment page** or the **Overview** page. If you're using Microsoft Entra ID authentication, you don't need a key.

    :::image type="content" source="../../media/ai-services/add-model-deployments/models-deploy-endpoint-url.png" alt-text="A screenshot showing how to get the URL and key associated with the deployment." lightbox="../../media/ai-services/add-model-deployments/models-deploy-endpoint-url.png":::

2. Use the model inference endpoint URL and the keys from before when constructing your client. The following example uses the Azure AI Inference package:

    [!INCLUDE [code-create-chat-client](../../includes/ai-services/code-create-chat-client.md)]

3. When constructing your request, indicate the parameter `model` and insert the model deployment name you created.
    
    [!INCLUDE [code-create-chat-completion](../../includes/ai-services/code-create-chat-completion.md)]

> [!TIP]
> When using the endpoint, you can change the `model` parameter to any available model deployment in your resource.

Additionally, Azure OpenAI models can be consumed using the [Azure OpenAI service endpoint](../../../ai-services/openai/supported-languages.md) in the resource. This endpoint is exclusive for each model deployment and has its own URL.

## Model deployment customization

When creating model deployments, you can configure other settings including content filtering and rate limits. To configure more settings, select the option **Customize** in the deployment wizard.

> [!NOTE]
> Configurations may vary depending on the model you're deploying.

## Next steps

* [Develop applications using Azure AI model inference service in Azure AI services](../concepts/endpoints.md)