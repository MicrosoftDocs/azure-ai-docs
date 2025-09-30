---
title: Upgrade from GitHub Models to Azure AI Foundry Models
titleSuffix: Azure AI Foundry for GitHub
description: Learn how to upgrade from GitHub Models to Azure AI Foundry Models for production-ready AI applications with enhanced features.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/30/2025
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
recommendations: false
#CustomerIntent: As a developer using GitHub Models, I want to learn how to upgrade my endpoint to Azure AI Foundry Models so that I can access enhanced features and capabilities for my AI applications.
---

# Upgrade from GitHub Models to Azure AI Foundry Models

In this article, learn to develop a generative AI application by starting from GitHub Models and then deploying upgrading your experience by deploying an Azure AI Services resource with Azure AI Foundry Models.

[GitHub Models](https://docs.github.com/en/github-models/) are useful when you want to find and experiment with AI models for free as you develop a generative AI application. When you're ready to bring your application to production, upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using Azure AI Foundry Models service. You don't need to change anything else in your code.

The playground and free API usage for GitHub Models are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

## Prerequisites

To complete this tutorial, you need:

* A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
* An Azure subscription. If you don't have one, you're prompted to create or update your Azure account to a Standard account when you're ready to deploy your model to production.

## Upgrade to Azure AI Foundry Models

The rate limits for the playground and free API usage help you experiment with models and develop your AI application. When you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To get the key and endpoint:

1. Go to [GitHub Models](https://github.com/marketplace/models) and select the model you're interested in.

1. In the playground for your model, select **Get API key**.

1. Select **Get production key**.

    :::image type="content" source="../media/quickstart-github-models/github-models-upgrade.gif" alt-text="An animation showing how to upgrade GitHub Models to get a production ready resource." lightbox="../media/quickstart-github-models/github-models-upgrade.gif":::

1. If you don't have an Azure account, select **Create my account** and follow the steps to create one.

1. If you have an Azure account, select **Sign back in**.

1. If your existing account is a free account, you first have to upgrade to a Standard plan. Once you upgrade, go back to the playground and select **Get API key** again, then sign in with your upgraded account.

1. When you sign in to your Azure account, you're taken to [Azure AI Foundry > GitHub](https://ai.azure.com/GitHub). It might take one or two minutes to load your initial model details in AI Foundry.

1. The page loads with your model's details. Select the **Deploy** button to deploy the model to your account.

1. When it's deployed, your model's API Key and endpoint appear in the Overview. Use these values in your code to use the model in your production environment.

At this point, the model you selected is ready to consume.

## Upgrade your code to use the new endpoint

After you configure your Azure AI Services resource, you can start using it from your code. To use the Azure AI Services resource, you need the endpoint URL and key, which you can find in the **Overview** section:

:::image type="content" source="../media/overview/overview-endpoint-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the resource." lightbox="../media/overview/overview-endpoint-and-key.png":::

You can use any of the supported SDKs to get predictions from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference SDK

For more details and examples, see the [supported languages and SDKs](../supported-languages.md) section. The following example shows how to use the Azure AI Foundry Models SDK with the newly deployed model:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*. See [Routing](inference.md#routing) concept page to learn how Azure AI Services route deployments.

> [!IMPORTANT]
> Unlike GitHub Models where all the models are already configured, the Azure AI Services resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](../../model-inference/how-to/create-model-deployments.md) to your resource.

## Explore additional features

Azure AI Foundry Models supports additional features that aren't available in GitHub Models, including:

* [Explore the model catalog](https://ai.azure.com/github/models) to see more models.
* Configure [key-less authentication](../../model-inference/how-to/configure-entra-id.md).
* Configure [content filtering](../../model-inference/how-to/configure-content-filters.md).
* Configure rate limiting for specific models.
* Explore additional [deployment SKUs for specific models](../../model-inference/concepts/deployment-types.md).
* Configure [private networking](../../../ai-services/cognitive-services-virtual-networks.md?context=/azure/ai-foundry/openai/context/context).

## Troubleshooting

See the [FAQ section](../../foundry-models/faq.yml) for more help.

## Related content

* [Explore the model catalog](https://ai.azure.com/github/models) in Azure AI Foundry portal.
* [Add more models](../../model-inference/how-to/create-model-deployments.md) to your endpoint.
