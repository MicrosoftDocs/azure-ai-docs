---
title: include file
description: include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include, classic-and-new
---

> [!IMPORTANT]
> GitHub Models was retired on July 30, 2026. The playground, model catalog, inference API, and bring your own key (BYOK) support are no longer available to any customer. For more information, see [GitHub Models](https://docs.github.com/en/github-models/) in the GitHub documentation.
>
> If your application still calls the GitHub Models inference endpoint, migrate it to Microsoft Foundry Models by following the steps in this article. GitHub Models was a separate service from GitHub Copilot and is unrelated to GitHub Copilot.

In this article, you learn how to move a generative AI application from the retired GitHub Models service to Microsoft Foundry Models by deploying a Foundry Tools resource in an Azure subscription. Both services use the same inference API, so you typically only need to change the endpoint and credentials in your code.

## Prerequisites

You need:

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) to begin.
- [Foundry Models from partners and community](../concepts/models-from-partners.md) require access to **Azure Marketplace**. Ensure you have the [permissions required to subscribe to model offerings](../concepts/models-from-partners.md#permissions-required-to-subscribe-to-models-from-partners-and-community). [Foundry Models sold by Azure](../concepts/models-sold-directly-by-azure.md) don't have this requirement.

## Migrate to Foundry Models

Unlike GitHub Models, which was free with rate limits, Foundry Models usage is billed to your Azure subscription based on the [deployment type](../concepts/deployment-types.md) you choose.

To replace your GitHub Models endpoint and token with a Foundry Models endpoint and key:

1. Sign in to the [Foundry portal](https://ai.azure.com) with your Azure account.

    > [!TIP]
    > If you land in the Foundry (classic) experience, toggle the **New Foundry** switcher in the upper-right navigation to switch to the new Foundry experience.

1. Follow the steps in [Deploy a model](../how-to/deploy-foundry-models.md#deploy-a-model) to deploy the model of your choice, test it in the Playground, and inference the deployed model with code.

1. On the Foundry homepage, copy the **API key** and **Project endpoint**, and use them in place of the GitHub Models endpoint and personal access token in your application.

1. Verify the migration works by sending a test prompt from the Playground or from your code. If you receive a response, your model is ready to use.

> [!IMPORTANT]
> Unlike GitHub Models, where all the models were already configured, the Foundry Tools resource allows you to control which models are available in your endpoint and under which configuration. Add as many models as you plan to use before indicating them in the `model` parameter. Learn how to [add more models](../how-to/create-model-deployments.md) to your resource.

## Use your Foundry models in the IDE

The GitHub Models playground is no longer available. To experiment with models from your editor instead, add your Foundry deployment to Visual Studio Code as a bring your own key (BYOK) language model:

1. In Visual Studio Code, open the model picker in the Chat view and select **Manage Language Models** (gear icon), or run the **Chat: Manage Language Models** command from the Command Palette.

1. Select **Add Models**, and then select **Azure** from the provider list.

1. Enter a group name for the models, and then enter the endpoint URL and API key that you copied from the Foundry portal.

1. Select the model from the model picker in chat.

Alternatively, select **Install Model Providers** in the Language Models editor and install the [Foundry Toolkit for VS Code](https://aka.ms/AIToolkit) extension, which adds Foundry's cloud-hosted and local models to the model picker.

For more information, see [Language models in Visual Studio Code](https://code.visualstudio.com/docs/agent-customization/language-models#_add-a-model-from-a-built-in-provider).

## Explore additional features

Foundry Models supports features that GitHub Models didn't offer:

* **[Model catalog](https://ai.azure.com/explore/models)** — Browse, compare, and evaluate models from Azure, partners, and the open-source community.
* **[Keyless authentication](../how-to/configure-entra-id.md)** — Use Microsoft Entra ID for token-based authentication without managing API keys.
* **[Content filtering](../../../foundry-classic/foundry-models/concepts/content-filter.md)** — Configure content safety filters for your deployments.
* **Rate limiting** — Set custom rate limits for specific models in your resource.
* **[Deployment types](../concepts/deployment-types.md)** — Choose from multiple deployment SKUs such as pay-per-token, provisioned, and batch.

## Troubleshoot common issues

| Issue | Resolution |
| --- | --- |
| Requests to the GitHub Models endpoint fail | The GitHub Models inference API was retired on July 30, 2026. Point your application at a Foundry Models endpoint as described in this article. |
| Model not available in your region | Check the model's region availability by selecting **View availability** in the **Quick facts** section of its model card. Switch to a project in a supported region. |
| Authentication error after key swap | Verify you copied the correct key from the Foundry portal. On the Foundry homepage, copy the **API key** and **Project endpoint** to view your key and endpoint. |
| Rate limit errors after migrating | Foundry Models rate limits depend on your [deployment type](../concepts/deployment-types.md). Scale up or choose a higher-throughput deployment. |

## Related content

* [Deploy Microsoft Foundry Models in the Foundry portal](../how-to/deploy-foundry-models.md)
* [Create model deployments](../how-to/create-model-deployments.md)
* [Deployment types for Foundry Models](../concepts/deployment-types.md)
