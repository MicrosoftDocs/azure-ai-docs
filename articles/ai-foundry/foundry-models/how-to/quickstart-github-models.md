---
title: Upgrade from GitHub Models to Microsoft Foundry Models
titleSuffix: Microsoft Foundry for GitHub
description: Learn how to upgrade from GitHub Models to Microsoft Foundry Models for production-ready AI applications with enhanced features.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/09/2026
ms.custom: ignite-2024, github-universe-2024, pilot-ai-workflow-jan-2026
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

The playground and free API usage for GitHub Models are [rate limited](https://docs.github.com/en/github-models/use-github-models/prototyping-with-ai-models#rate-limits) by requests per minute, requests per day, tokens per request, and concurrent requests. If you get rate limited, you need to wait for the rate limit that you hit to reset before you can make more requests.

## Prerequisites

You need:

- A GitHub account with access to [GitHub Models](https://docs.github.com/en/github-models/).
- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin. Alternatively, you can wait until you're ready to deploy your model to production, at which point you'll be prompted to create or update your Azure account to a standard account.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](configure-marketplace.md). [Foundry Models sold directly by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.
 

## Upgrade to Foundry Models

The rate limits for the playground and free API usage help you experiment with models and develop your AI application. When you're ready to bring your application to production, use a key and endpoint from a paid Azure account. You don't need to change anything else in your code.

> [!NOTE]
> GitHub Models are free with rate limits. After you upgrade to Foundry Models, usage is billed to your Azure subscription based on the [deployment type](../concepts/deployment-types.md) you choose.

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

1.  You're taken to [Foundry > GitHub](https://ai.azure.com/GitHub) and land on the home page in a Foundry project.

    > [!TIP]
    > If you land in the Foundry (classic) experience, toggle the **New Foundry** switcher in the upper-right navigation to switch to the new Foundry experience.

1. Follow the steps in [Deploy a model](deploy-foundry-models.md#deploy-a-model) to deploy the model of your choice, test it in the Playground, and inference the deployed model with code.

1. Verify the deployment works by sending a test prompt in the Playground. If you receive a response, your model is ready to use from code.


> [!IMPORTANT]
> Unlike GitHub Models where all the models are already configured, the Foundry Tools resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](./create-model-deployments.md) to your resource.

## Explore additional features

Foundry Models supports features that aren't available in GitHub Models:

* **[Model catalog](https://ai.azure.com/explore/models)** — Browse, compare, and evaluate models from Azure, partners, and the open-source community.
* **[Keyless authentication](configure-entra-id.md)** — Use Microsoft Entra ID for token-based authentication without managing API keys.
* **[Content filtering](../concepts/content-filter.md)** — Configure content safety filters for your deployments.
* **Rate limiting** — Set custom rate limits for specific models in your resource.
* **[Deployment types](../concepts/deployment-types.md)** — Choose from multiple deployment SKUs such as pay-per-token, provisioned, and batch.

## Troubleshoot common issues

| Issue | Resolution |
| --- | --- |
| Model not available in your region | Check the model's region availability on its [model catalog page](https://ai.azure.com/explore/models) and choose a supported region. |
| Authentication error after key swap | Verify you copied the correct key from the Foundry portal. Select **Project settings** > **Keys and endpoints** to view your keys. |
| Rate limit errors after upgrade | Foundry Models rate limits depend on your [deployment type](../concepts/deployment-types.md). Scale up or choose a higher-throughput deployment. |

## Related content

* [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md)
* [Create model deployments](create-model-deployments.md)
* [Deployment types for Foundry Models](../concepts/deployment-types.md)
