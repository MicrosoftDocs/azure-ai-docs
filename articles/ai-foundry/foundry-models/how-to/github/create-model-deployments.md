---
title: Add and configure models to Azure AI Foundry Models
titleSuffix: Azure AI Foundry for GitHub
description: Learn how to add and configure new models to the Foundry Models endpoint in Azure AI Foundry for GitHub.
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 05/19/2025
ms.custom: ignite-2024, github-universe-2024
manager: scottpolly
author: ssalgadodev
ms.author: ssalgado
recommendations: false
ms.reviewer: fasantia
reviewer: santiagxf
---

# Add and configure models from Azure AI Foundry Models

You can decide and configure which models are available for inference in the Azure AI services resource model's inference endpoint. When a given model is configured, you can then generate predictions from it by indicating its model name or deployment name on your requests. No further changes are required in your code to use it.


In this article, you learn how to add a new model from Azure AI Foundry Models.

## Prerequisites

To complete this article, you need:

* An Azure subscription. If you're using [GitHub Models](https://docs.github.com/en/github-models/), you can upgrade your experience and create an Azure subscription in the process. Read [Upgrade from GitHub Models to Azure AI Foundry Models](../../../model-inference/how-to/quickstart-github-models.md) if it's your case.
* An Azure AI services resource. For more information, see [Create an Azure AI Foundry resource](../../../model-inference/how-to/quickstart-create-resources.md).


## Add a model

[!INCLUDE [add-model-deployments](../../../foundry-models/includes/github/add-model-deployments.md)]

## Use the model

Deployed models in Azure AI Foundry Models can be consumed using the [Azure AI model's inference endpoint](../../../model-inference/concepts/endpoints.md) for the resource.

To use it:

1. Get the Azure AI model's inference endpoint URL and keys from the **deployment page** or the **Overview** page. If you're using Microsoft Entra ID authentication, you don't need a key.

2. When constructing your request, indicate the parameter `model` and insert the model deployment name you created.

    [!INCLUDE [code-create-chat-completion](../../../foundry-models/includes/code-create-chat-completion.md)]

3. When using the endpoint, you can change the `model` parameter to any available model deployment in your resource.

Additionally, Azure OpenAI models can be consumed using the [Azure OpenAI in Azure AI Foundry Models endpoint](../../../../ai-services/openai/supported-languages.md) in the resource. This endpoint is exclusive for each model deployment and has its own URL.

## Model deployment customization

When creating model deployments, you can configure additional settings including content filtering and rate limits. Select the option **Customize** in the deployment wizard to configure it.

> [!NOTE]
> Configurations may vary depending on the model you're deploying.

## Related content

* [Develop applications using Azure AI Foundry Models](../../../model-inference/supported-languages.md)

