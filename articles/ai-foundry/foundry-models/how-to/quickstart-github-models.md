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

In this article, you learn to develop a generative AI application by starting from GitHub Models and then upgrade your experience by deploying an Azure AI Services resource with Azure AI Foundry Models.

[GitHub Models](https://docs.github.com/en/github-models/) are useful when you want to find and experiment with AI models for free as you develop a generative AI application. When you're ready to bring your application to production, upgrade your experience by deploying an Azure AI Services resource in an Azure subscription and start using Foundry Models. You don't need to change anything else in your code.

The playground and free API usage for GitHub Models are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

## Prerequisites

To complete this tutorial, you need:

- A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. Alternatively, you can wait until you're ready to deploy your model to production, at which point you'll be prompted to create or update your Azure account to a standard account.
- [Models from partners and community](../../concepts/models.md#models-from-partners-and-community) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../../how-to/configure-marketplace.md). [Models sold directly by Azure](../../concepts/models.md#models-sold-directly-by-azure) don't have this requirement.
 

## Upgrade to Azure AI Foundry Models

The rate limits for the playground and free API usage help you experiment with models and develop your AI application. When you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To get the key and endpoint:

1. Go to [GitHub Models](https://github.com/marketplace/models) and select a model to land on its playground. This article uses Mistral Large 24.11.

1. Select **Use this model** from the playground

1. In the playground for your model, select **Use this model**. This action opens up a window to "Get started with Models in your codebase".

1. In the "Configure authentication" step, select **Get Azure AI key** from the "Azure AI" section.

    :::image type="content" source="../media/quickstart-github-models/github-models-get-production-key.png" alt-text="A screenshot showing how to get the Azure AI production key from the playground of a GitHub Model." lightbox="../media/quickstart-github-models/github-models-get-production-key.png":::

1. The Azure AI Foundry homepage opens up if you're already signed in to your Azure account, otherwise you land on the Azure AI Foundry sign in page.

1. If you're not yet signed in to your Azure account, select **Sign in to get started** to open the sign in window.

    - If you don't have an Azure account, select **Create one** and follow the steps to create a paid account. 

    - Alternatively, if you have an existing account, sign in. If your existing account is a free account, you first have to upgrade to a standard plan. 
    
    - Return to the model's playground and select **Get Azure AI key** again. This time, you land on the Azure AI Foundry homepage.

1. Go to the "Explore models and capabilities" section of the homepage to search for and select the **Mistral Large 24.11** model. This action opens up the model card where you can see the model's details.

1. Select **Use this model** to deploy the model to your account. This process begins by creating an Azure AI Foundry project to use for your deployment.

1. When your deployment is ready, the endpoint's target URI and API key appear in the deployment's details page. Use these values in your code to use the model in your production environment.


## Use the new endpoint

You can use any of the supported SDKs to get predictions from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Foundry SDK

For more details and examples, see [supported languages and SDKs](../supported-languages.md). The following example shows how to use the Azure AI Foundry SDK with the newly deployed model:

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
