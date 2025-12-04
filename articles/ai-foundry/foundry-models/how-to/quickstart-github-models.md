---
title: Upgrade from GitHub Models to Microsoft Foundry Models
titleSuffix: Microsoft Foundry for GitHub
description: Learn how to upgrade from GitHub Models to Microsoft Foundry Models for production-ready AI applications with enhanced features.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 09/30/2025
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
recommendations: false
#CustomerIntent: As a developer using GitHub Models, I want to learn how to upgrade my endpoint to Microsoft Foundry Models so that I can access enhanced features and capabilities for my AI applications.
---

# Upgrade from GitHub Models to Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

In this article, you learn to develop a generative AI application by starting from GitHub Models and then upgrade your experience by deploying a Foundry Tools resource with Microsoft Foundry Models.

[GitHub Models](https://docs.github.com/en/github-models/) are useful when you want to find and experiment with AI models for free as you develop a generative AI application. When you're ready to bring your application to production, upgrade your experience by deploying a Foundry Tools resource in an Azure subscription and start using Foundry Models. You don't need to change anything else in your code.

The playground and free API usage for GitHub Models are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

[!INCLUDE [migrate-model-inference-to-v1-openai](../../includes/migrate-model-inference-to-v1-openai.md)]

## Prerequisites

To complete this tutorial, you need:

- A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. Alternatively, you can wait until you're ready to deploy your model to production, at which point you'll be prompted to create or update your Azure account to a standard account.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.
 

## Upgrade to Foundry Models

The rate limits for the playground and free API usage help you experiment with models and develop your AI application. When you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To get the key and endpoint:

1. Go to [GitHub Models](https://github.com/marketplace/models) and select a model to land on its playground. This article uses Mistral Large 24.11.

1. Type in some prompts or use some of the suggested prompts to interact with the model in the playground.

1. Select **Use this model** from the playground. This action opens up a window to "Get started with Models in your codebase".

1. In the "Configure authentication" step, select **Get Azure AI key** from the "Azure AI" section.

    :::image type="content" source="../media/quickstart-github-models/github-models-get-production-key.png" alt-text="A screenshot showing how to get the Azure AI production key from the playground of a GitHub Model." lightbox="../media/quickstart-github-models/github-models-get-production-key.png":::

1. If you're already signed in to your Azure account, skip this step. However, if you don't have an Azure account or you're not signed in to your account, follow these steps:

    1. If you don't have an Azure account, select **Create my account** and follow the steps to create one.

    1. Alternatively, if you have an Azure account, select **Sign back in**. If your existing account is a free account, you first have to upgrade to a standard plan. 

    1. Return to the model's playground and select **Get Azure AI key** again. 

    1. Sign in to your Azure account.
    
1.  You're taken to [Foundry > GitHub](https://ai.azure.com/GitHub), and the page loads with your model's details. It might take one or two minutes to load your model details in Foundry.

1. For [Foundry Models from partners and community](../concepts/models-from-partners.md), you need to subscribe to Azure Marketplace. This requirement applies to Mistral-Large-2411, for example. Select **Agree and Proceed** to accept the terms.

1. Select the **Deploy** button to deploy the model to your account.

1. When your deployment is ready, you land on your project's **Overview** page, where you can see the Foundry project's endpoint. 

1. To get the specific model's endpoint URL and API key, go to the **Models + endpoints** tab in the left pane of the Foundry portal and select the deployed model. The endpoint's target URI and API key are visible on the deployment's details page. Use these values in your code to use the model in your production environment.

    :::image type="content" source="../media/quickstart-github-models/deployment-endpoint-and-key.png" alt-text="Screenshot showing how to get the URL and key associated with the deployment." lightbox="../media/quickstart-github-models/deployment-endpoint-and-key.png":::

## Use the new endpoint

To use your deployed model with code, you need the model's endpoint URL and key, which you saw in the previous section. You can use any of the supported SDKs to get predictions from the endpoint. The following SDKs are officially supported:

* OpenAI SDK
* Azure OpenAI SDK
* Azure AI Inference SDK

For more details and examples, see [supported languages and SDKs](../supported-languages.md). The following example shows how to use the Azure AI Inference SDK with the newly deployed model:

[!INCLUDE [code-create-chat-client](../../foundry-models/includes/code-create-chat-client.md)]

Generate your first chat completion:

[!INCLUDE [code-create-chat-completion](../../foundry-models/includes/code-create-chat-completion.md)]

Use the parameter `model="<deployment-name>` to route your request to this deployment. *Deployments work as an alias of a given model under certain configurations*.

> [!IMPORTANT]
> Unlike GitHub Models where all the models are already configured, the Foundry Tools resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](../../model-inference/how-to/create-model-deployments.md) to your resource.

## Explore additional features

Foundry Models supports extra features that aren't available in GitHub Models, including:

* [Explore the model catalog](https://ai.azure.com/github/models) to see more models.
* Configure [key-less authentication](../../model-inference/how-to/configure-entra-id.md).
* Configure [content filtering](../../model-inference/how-to/configure-content-filters.md).
* Configure rate limiting for specific models.
* Explore additional [deployment SKUs for specific models](../../model-inference/concepts/deployment-types.md).
* Configure [private networking](../../../ai-services/cognitive-services-virtual-networks.md?context=/azure/ai-foundry/openai/context/context).

## Troubleshooting

For more help, see the [FAQ section](../../foundry-models/faq.yml).

## Related content

* [Explore the model catalog](https://ai.azure.com/github/models) in Foundry portal.
* [Add more models](../../model-inference/how-to/create-model-deployments.md) to your endpoint.
