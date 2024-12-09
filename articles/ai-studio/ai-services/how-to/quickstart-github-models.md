---
title: Upgrade from GitHub Models to Azure AI model inference in Azure AI Services
titleSuffix: Azure AI Services
description: Learn how to upgrade your endpoint from GitHub Models to Azure AI Models in AI Services
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/01/2024
ms.custom: github-universe-2024
manager: nitinme
author: mrbullwinkle
ms.author: fasantia 
recommendations: false
---

# Upgrade from GitHub Models to the Azure AI model inference service

If you want to develop a generative AI application, you can use [GitHub Models](https://docs.github.com/en/github-models/) to find and experiment with AI models for free. The playground and free API usage are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

Once you're ready to bring your application to production, you can upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using the Azure AI model inference service. You don't need to change anything else in your code.

The following article explains how to get started from GitHub Models in Azure AI Models for Azure AI services.

## Prerequisites

To complete this tutorial, you need:

* A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).

* An Azure subscription. If you don't have one, you are prompted to create or update your Azure account to a pay as you go account when you're ready to deploy your model to production.

## Upgrade to Azure AI Services

The rate limits for the playground and free API usage are intended to help you experiment with models and develop your AI application. Once you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To obtain the key and endpoint:

1. In the playground for your model, select **Get API key**.

1. Select **Get production key**.

1. If you don't have an Azure account, select Create my account and follow the steps to create one.

1. If you have an Azure account, select **Sign back in**.

1. If your existing account is a free account, you first have to upgrade to a Pay as you go plan. Once you upgrade, go back to the playground and select **Get API key** again, then sign in with your upgraded account.

1. Once you've signed in to your Azure account, you're taken to [Azure AI Foundry](https://ai.azure.com). 

1. At the top of the page, select **Go to your GitHub AI resource** to go to Azure AI Foundry / Github](https://ai.azure.com/github). It might take one or two minutes to load your initial model details in AI Foundry portal.

1. The page is loaded with your model's details. Select the **Create a Deployment** button to deploy the model to your account.

1. Once it's deployed, your model's API Key and endpoint are shown in the Overview. Use these values in your code to use the model in your production environment.

    :::image type="content" source="../../media/ai-services/add-model-deployments/models-deploy-endpoint-url.png" alt-text="A screenshot showing how to get the URL and key associated with the deployment." lightbox="../../media/ai-services/add-model-deployments/models-deploy-endpoint-url.png":::

At this point, the model you selected is ready to consume. 

> [!TIP]
> Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. See [Routing](../concepts/endpoints.md#routing) concept page to learn how Azure AI Services route deployments.

## Upgrade your code to use the new endpoint

Once your Azure AI Services resource is configured, you can start consuming it from your code. You need the endpoint URL and key for it, which can be found in the **Overview** section:

:::image type="content" source="../../media/ai-services/overview/overview-endpoint-and-key.png" alt-text="A screenshot showing how to get the URL and key associated with the resource." lightbox="../../media/ai-services/overview/overview-endpoint-and-key.png":::

You can use any of the supported SDKs to get predictions out from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference SDK

See the [supported languages and SDKs](../concepts/endpoints.md#azure-ai-inference-endpoint) section for more details and examples. The following example shows how to use the Azure AI model inference SDK with the newly deployed model:

[!INCLUDE [code-create-chat-client](../../includes/ai-services/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../../includes/ai-services/code-create-chat-completion.md)]

## Explore more features

Azure AI model inference supports more features not available in GitHub Models, including:

* [Explore the model catalog](https://ai.azure.com/github/models) to see other models not available in GitHub Models.
* Configure [content filtering](../../concepts/content-filtering.md).
* Configure rate limiting (for specific models).
* Explore more [deployment SKUs (for specific models)](../concepts/deployment-types.md).
* Configure [private networking](../../../ai-services/cognitive-services-virtual-networks.md?context=/azure/ai-studio/context/context).

## Got troubles?

See the [FAQ section](../faq.yml) to explore more help.

## Next steps

* [Add more models](create-model-deployments.md) to your endpoint.
* [Explore the model catalog](https://ai.azure.com/github/models) in Azure AI Foundry portal.