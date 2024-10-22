---
title: Upgrade from GitHub Models to Azure AI model inference in Azure AI Services
titleSuffix: Azure AI Services
description: Learn how to upgrade your endpoint from GitHub Models to Azure AI Models in AI Services
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/01/2024
ms.custom: ignite-2024, github-universe-2024
manager: nitinme
author: mrbullwinkle
ms.author: fasantia 
recommendations: false
---

# Upgrade from GitHub Models to Azure AI model inference in Azure AI Services

If you want to develop a generative AI application, you can use [GitHub Models](https://docs.github.com/en/github-models/) to find and experiment with AI models for free. The playground and free API usage are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you will need to wait for the rate limit that you hit to reset before you can make more requests.

Once you are ready to bring your application to production, you can upgrade your experience by deploying an AI services resource in an Azure subscription and start using the Azure AI Models service. You don't need to change anything else in your code.

The following article explains how to get started from GitHub Models in Azure AI Models for Azure AI services.

## Prerequisites

To complete this tutorial, you need:

* A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
* An Azure subscription. If you don't have one, you are prompted to create or update your Azure account to a pay as you go account when you're ready to deploy your model to production.

## Upgrade to Azure AI Services

The rate limits for the playground and free API usage are intended to help you experiment with models and develop your AI application. Once you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To obtain the key and endpoint:

1. In the playground for your model, select **Get API key**.

2. Select **Get production key**.

3. If you don't have an Azure account, select Create my account and follow the steps to create one.

4. If you have an Azure account, select **Sign back in**.

5. If your existing account is a free account, you first have to upgrade to a Pay as you go plan. Once you upgrade, go back to the playground and select **Get API key** again, then sign in with your upgraded account.

6. Once you've signed in to your Azure account, you see [Azure AI Studio | GitHub](https://ai-azure.com/GitHub). It might take 1-2 minutes to load the studio with your initial model details.

7. The page is loaded with your model's details. Select the **Deploy** button to deploy the model to your account.

8. Once it's deployed, your model's API Key and endpoint are shown in the Overview. Use these values in your code to use the model in your production environment.

    :::image type="content" source="../media/add-model-deployments/models-deploy-endpoint-url.png" alt-text="An screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/add-model-deployments/models-deploy-endpoint-url.png":::

At this point, the model you selected will be ready to consume. 

> [!TIP]
> Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. See [Routing](../concepts/endpoints.md#routing) concept page to learn how Azure AI Services route deployments.

## Add more models

[!INCLUDE [add-model-deployments](../includes/add-model-deployments.md)]

## Upgrade your code to use the new endpoint

Once your Azure AI Services resource is configured, you can start consuming it from your code. You will need the endpoint URL and key for it, which can be found in the **Overview** section:

:::image type="content" source="../media/overview/overview-endpoint-and-key.png" alt-text="An screenshot showing how to get the URL and key associated with the resource." lightbox="../media/overview/overview-endpoint-and-key.png":::

You can use any of the supported SDKs to get predictions out from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference SDK

See the [supported languages and SDKs](../supported-languages.md) section for more details and examples. The following example shows how to use the Azure AI model inference SDK with the newly deployed model:

[!INCLUDE [code-create-chat-client](../includes/code-create-chat-client.md)]

## Explore additional features

Azure AI services resource supports additional features not available in GitHub Models, including:

* [Explore the model catalog](https://ai.azure.com/github/models) to see additional models not available in GitHub Models.
* Configure [content filtering](content-filters.md).
* Configure rate limiting (for specific models).
* Configure Microsoft Entra ID support for [key-less access](role-based-access-control.md).
* Explore additional [deployment SKUs (for specific models)](../concepts/deployment-types.md).
* Configure [private networking](../../cognitive-services-virtual-networks.md?context=/azure/ai-services/openai/context/context).

## Got troubles?

See the [FAQ section](../faq.yml) to explore more help.

## Next steps

* [Explore the model catalog](https://ai.azure.com/github/models) in Azure AI studio.