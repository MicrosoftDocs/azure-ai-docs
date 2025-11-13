---
title: How to deploy Azure OpenAI in Foundry Models with Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Learn how to deploy and use Azure OpenAI models in Microsoft Foundry, including model region availability and quota management.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: how-to
ms.date: 09/15/2025
ms.reviewer: fasantia
ms.author: mopeakande
manager: nitinme
author: msakande
ai-usage: ai-assisted

#CustomerIntent: As a developer or data scientist, I want to deploy and interact with Azure OpenAI in Foundry Models using the Foundry portal so that I can build, test, and integrate advanced AI capabilities into my applications efficiently and securely.
---

# How to deploy Azure OpenAI models with Microsoft Foundry

In this article, you learn how to create deployments for Azure OpenAI in Microsoft Foundry Models, using the Foundry portal.

Azure OpenAI in Foundry Models offers a diverse set of models with different capabilities and price points. When you deploy Azure OpenAI models in the Foundry portal, you can consume the deployments by using prompt flow or another tool. Model availability varies by region. For more information about the details of each model, see [Azure OpenAI models](../openai/concepts/models.md).

To modify and interact with an Azure OpenAI model in the [Foundry](https://ai.azure.com/?cid=learnDocs) playground, you first need to deploy a base Azure OpenAI model to your project. After you deploy the model and make it available in your project, you can consume its REST API endpoint as-is or customize it further with your own data and other components, such as embeddings and indexes.  

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions don't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [[!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]](create-projects.md).

## Deploy an Azure OpenAI model from the model catalog

Follow the steps in this section to deploy an Azure OpenAI model, such as `gpt-4o-mini`, to a real-time endpoint from the Foundry portal [model catalog](./model-catalog-overview.md):

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. In the **Collections** filter, select **Azure OpenAI**.
    
    :::image type="content" source="../media/deploy-monitor/catalog-filter-azure-openai.png" alt-text="A screenshot showing how to filter by Azure OpenAI models in the catalog." lightbox="../media/deploy-monitor/catalog-filter-azure-openai.png":::

1. Select a model such as `gpt-4o-mini` from the Azure OpenAI collection.
1. Select **Use this model** to open the deployment window.
1. Select the resource that you want to deploy the model to. If you don't have a resource, create one.
1. Specify the deployment name and modify other default settings depending on your requirements.
1. Select **Deploy**.
1. Go to the deployment details page. Select **Open in playground**.
1. Select **View Code** to get code samples that you can use to consume the deployed model in your application.

## Deploy an Azure OpenAI model from your project

You can also start deployment from your project in Foundry portal.

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Go to your project in Foundry portal.
1. From the left sidebar of your project, go to **My assets** > **Models + endpoints**.
1. Select **+ Deploy model** > **Deploy base model**.
1. Search for and select a model such as `gpt-4o-mini` from the list of models.
1. Select **Confirm** to open the deployment window.
1. Specify the deployment name and modify other default settings depending on your requirements.
1. Select **Deploy**.
1. Go to the deployment details page. Select **Open in playground**.
1. Select **View Code** to get code samples that you can use to consume the deployed model in your application.

## Inferencing the Azure OpenAI model

To perform inferencing on the deployed model, use the playground or code samples. The playground is a web-based interface that lets you interact with the model in real-time. Use the playground to test the model with different prompts and see the model's responses.

For more examples of how to consume the deployed model in your application, see the [Get started using chat completions with Azure OpenAI in Foundry Models quickstart](../openai/chatgpt-quickstart.md).

## Regional availability and quota limits of a model

For Azure OpenAI models, the default quota for models varies by model and region. Certain models might only be available in some regions. For more information on availability and quota limits, see [Azure OpenAI quotas and limits](/azure/ai-foundry/openai/quotas-limits).

## Quota for deploying and inferencing a model

For Azure OpenAI models, deploying and inferencing consume quota that Azure assigns to your subscription on a per-region, per-model basis in units of Tokens-per-Minute (TPM). When you sign up for Foundry, you receive default quota for most of the available models. Then, you assign TPM to each deployment as you create it, which reduces the available quota for that model. You can continue to create deployments and assign them TPMs until you reach your quota limit.

When you reach your quota limit, you can only create new deployments of that model if you:

- Request more quota by submitting a [quota increase form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pUMFE1Rk9CU084RjA0TUlVSUlMWEQzVkJDNCQlQCN0PWcu).
- Adjust the allocated quota on other model deployments to free up tokens for new deployments on the [Azure OpenAI Portal](https://oai.azure.com/portal).

For more information about quota, see [Foundry quota](./quota.md) and [Manage Azure OpenAI quota](../../ai-services/openai/how-to/quota.md?tabs=rest).

## Related content

- Learn more about what you can do in [Foundry](../what-is-azure-ai-foundry.md)
- Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml)
