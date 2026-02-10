---
title: Upgrade from GitHub Models to Microsoft Foundry Models
titleSuffix: Microsoft Foundry for GitHub
description: Learn how to upgrade from GitHub Models to Microsoft Foundry Models for production-ready AI applications with enhanced features.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 12/05/2025
ms.custom: ignite-2024, github-universe-2024
author: msakande   
ms.author: mopeakande
recommendations: false
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
#CustomerIntent: As a developer using GitHub Models, I want to learn how to upgrade my endpoint to Microsoft Foundry Models so that I can access enhanced features and capabilities for my AI applications.
---

# Upgrade from GitHub Models to Microsoft Foundry Models

[!INCLUDE [version-banner](../../includes/version-banner.md)]

In this article, you learn to develop a generative AI application by starting from GitHub Models and then upgrade your experience by deploying a Foundry Tools resource with Microsoft Foundry Models.

[GitHub Models](https://docs.github.com/en/github-models/) are useful when you want to find and experiment with AI models for free as you develop a generative AI application. When you're ready to bring your application to production, upgrade your experience by deploying a Foundry Tools resource in an Azure subscription and start using Foundry Models. You don't need to change anything else in your code.

The playground and free API usage for GitHub Models are [rate limited](https://docs.github.com/en/github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

## Prerequisites

To complete this tutorial, you need:

- A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. Alternatively, you can wait until you're ready to deploy your model to production, at which point you'll be prompted to create or update your Azure account to a standard account.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.
 

## Upgrade to Foundry Models

The rate limits for the playground and free API usage help you experiment with models and develop your AI application. When you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

To get the key and endpoint:

1. Go to [GitHub Models](https://github.com/marketplace/models) and select a model to land on its playground. This article uses Mistral Medium 3 (25.05).

1. Type in some prompts or use some of the suggested prompts to interact with the model in the playground.

1. Select **Use this model** from the playground. This action opens up a window to "Get started with Models in your codebase".

1. In the "Configure authentication" step, select **Get Microsoft Foundry key** from the "Azure AI" section.

    :::image type="content" source="../media/quickstart-github-models/github-models-get-production-key.png" alt-text="A screenshot showing how to get the Azure AI production key from the playground of a GitHub Model." lightbox="../media/quickstart-github-models/github-models-get-production-key.png":::

1. If you're already signed in to your Azure account, skip this step. However, if you don't have an Azure account or you're not signed in to your account, follow these steps:

    1. If you don't have an Azure account, select **Create my account** and follow the steps to create one.

    1. Alternatively, if you have an Azure account, select **Sign back in**. If your existing account is a free account, you first have to upgrade to a standard plan. 

    1. Return to the model's playground and select **Get Microsoft Foundry key** again. 

    1. Sign in to your Azure account.

1.  You're taken to [Foundry > GitHub](https://ai.azure.com/GitHub) and land on the home page in a Foundry project. The Foundry experience that opens up depends on the one you last used, either: 

    1. You might land in the Foundry (new) experience. Notice the **New Foundry** toggle is on in the upper-right navigation.
    
        :::image type="icon" source="../../media/version-banner/new-foundry.png" border="false":::

    1.  Alternatively, you might land in the Foundry (classic) experience. Notice the **New Foundry** toggle is off in the upper-right navigation. 
    
        :::image type="icon" source="../../media/version-banner/classic-foundry.png" border="false":::

1. Toggle the **New Foundry** switcher if you prefer to switch to a different Foundry experience.

1. Follow the steps in [Deploy a model](deploy-foundry-models.md#deploy-a-model) to deploy the model of your choice, test it in the Playground, and inference the deployed model with code.


> [!IMPORTANT]
> Unlike GitHub Models where all the models are already configured, the Foundry Tools resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](./create-model-deployments.md) to your resource.

## Explore additional features

Foundry Models supports extra features that aren't available in GitHub Models, including:

* The Model catalog
* Keyless authentication with Microsoft Entra ID
* Content filtering
* Rate limiting for specific models
* Additional [deployment SKUs for specific models](../../foundry-models/concepts/deployment-types.md).

## Next Step

* [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md)
