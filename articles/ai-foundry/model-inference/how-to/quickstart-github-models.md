---
title: Upgrade from GitHub Models to Azure AI model inference
titleSuffix: Azure AI Foundry for GitHub
description: Learn how to upgrade your endpoint from GitHub Models to Azure AI model inference
ms.service: azure-ai-model-inference
ms.topic: how-to
ms.date: 1/21/2025
ms.custom: ignite-2024, github-universe-2024
manager: nitinme
author: santiagxf
ms.author: fasantia 
recommendations: false
---

# Upgrade from GitHub Models to Azure AI model inference

If you want to develop a generative AI application, you can use [GitHub Models](https://docs.github.com/en/github-models/) to find and experiment with AI models for free. The playground and free API usage are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

Once you're ready to bring your application to production, you can upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using Azure AI model inference service. You don't need to change anything else in your code.

The following article explains how to get started from GitHub Models and deploy an Azure AI Services resource with Azure AI model inference.

## Prerequisites

To complete this tutorial, you need:

* A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
* An Azure subscription. If you don't have one, you're prompted to create or update your Azure account to a pay as you go account when you're ready to deploy your model to production.

## Upgrade to Azure AI model inference

The rate limits for the playground and free API usage are intended to help you experiment with models and develop your AI application. Once you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To obtain the key and endpoint:

1. Got to [GitHub Models](https://github.com/marketplace/models) and select the model you're interested in.

1. In the playground for your model, select **Get API key**.

2. Select **Get production key**.

    :::image type="content" source="../media/quickstart-github-models/github-models-upgrade.gif" alt-text="An animation showing how to upgrade GitHub Models to get a production ready resource." lightbox="../media/quickstart-github-models/github-models-upgrade.gif":::

3. If you don't have an Azure account, select Create my account and follow the steps to create one.

4. If you have an Azure account, select **Sign back in**.

5. If your existing account is a free account, you first have to upgrade to a Pay as you go plan. Once you upgrade, go back to the playground and select **Get API key** again, then sign in with your upgraded account.

6. Once you've signed in to your Azure account, you're taken to [Azure AI Foundry > GitHub](https://ai.azure.com/GitHub). It might take one or two minutes to load your initial model details in AI Foundry.

7. The page is loaded with your model's details. Select the **Deploy** button to deploy the model to your account.

8. Once it's deployed, your model's API Key and endpoint are shown in the Overview. Use these values in your code to use the model in your production environment.

At this point, the model you selected is ready to consume.

## Upgrade your code to use the new endpoint

Once your Azure AI Services resource is configured, you can start consuming it from your code. To consume the Azure AI Services resource, you need the endpoint URL and key, which are available in the **Overview** section:

:::image type="content" source="../media/overview/overview-endpoint-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the resource." lightbox="../media/overview/overview-endpoint-and-key.png":::

You can use any of the supported SDKs to get predictions out from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference SDK

See the [supported languages and SDKs](../supported-languages.md) section for more details and examples. The following example shows how to use the Azure AI model inference SDK with the newly deployed model:

[!INCLUDE [code-create-chat-client](../includes/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../includes/code-create-chat-completion.md)]

Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. See [Routing](../concepts/endpoints.md#routing) concept page to learn how Azure AI Services route deployments.

> [!IMPORTANT]
> As opposite to GitHub Models where all the models are already configured, the Azure AI Services resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](create-model-deployments.md) to your resource.

## Explore additional features

Azure AI model inference supports additional features not available in GitHub Models, including:

* [Explore the model catalog](https://ai.azure.com/github/models) to see additional models not available in GitHub Models.
* Configure [key-less authentication](configure-entra-id.md).
* Configure [content filtering](configure-content-filters.md).
* Configure rate limiting (for specific models).
* Explore additional [deployment SKUs (for specific models)](../concepts/deployment-types.md).
* Configure [private networking](../../../ai-services/cognitive-services-virtual-networks.md?context=/azure/ai-services/openai/context/context).

## Got troubles?

See the [FAQ section](../faq.yml) to explore more help.

## Next steps

* [Explore the model catalog](https://ai.azure.com/github/models) in Azure AI Foundry portal.
* [Add more models](create-model-deployments.md) to your endpoint.
