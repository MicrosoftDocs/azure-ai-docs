---
title: How to deploy Azure OpenAI models with Azure AI Foundry
titleSuffix: Azure AI Foundry
description: Learn how to deploy Azure OpenAI models with Azure AI Foundry.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
  - ignite-2024
ms.topic: how-to
ms.date: 11/05/2024
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# How to deploy Azure OpenAI models with Azure AI Foundry

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this article, you learn to create Azure OpenAI model deployments in Azure AI Foundry portal.

Azure OpenAI in Azure AI Foundry Models offers a diverse set of models with different capabilities and price points. When you deploy Azure OpenAI models in Azure AI Foundry portal, you can consume the deployments, using prompt flow or another tool. Model availability varies by region. To learn more about the details of each model see [Azure OpenAI models](../../ai-services/openai/concepts/models.md).

To modify and interact with an Azure OpenAI model in the [Azure AI Foundry](https://ai.azure.com) playground, first you need to deploy a base Azure OpenAI model to your project. Once the model is deployed and available in your project, you can consume its REST API endpoint as-is or customize further with your own data and other components (embeddings, indexes, and more).  

## Prerequisites

- An Azure subscription with a valid payment method. Free or trial Azure subscriptions won't work. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go) to begin.

- An [Azure AI Foundry project](create-projects.md).

## Deploy an Azure OpenAI model from the model catalog

Follow the steps below to deploy an Azure OpenAI model such as `gpt-4o-mini` to a real-time endpoint from the Azure AI Foundry portal [model catalog](./model-catalog-overview.md):

[!INCLUDE [open-catalog](../includes/open-catalog.md)]

4. In the **Collections** filter, select **Azure OpenAI**.

    :::image type="content" source="../media/deploy-monitor/catalog-filter-azure-openai.png" alt-text="A screenshot showing how to filter by Azure OpenAI models in the catalog." lightbox="../media/deploy-monitor/catalog-filter-azure-openai.png":::

1. Select a model such as `gpt-4o-mini` from the Azure OpenAI collection.
1. Select **Deploy** to open the deployment window.
1. Select the resource that you want to deploy the model to. If you don't have a resource, you can create one.
1. Specify the deployment name and modify other default settings depending on your requirements.
1. Select **Deploy**.
1. You land on the deployment details page. Select **Open in playground**.
1. Select **View Code** to obtain code samples that can be used to consume the deployed model in your application.

## Deploy an Azure OpenAI model from your project

Alternatively, you can initiate deployment by starting from your project in Azure AI Foundry portal.

1. Go to your project in Azure AI Foundry portal.
1. From the left sidebar of your project, go to **My assets** > **Models + endpoints**.
1. Select **+ Deploy model** > **Deploy base model**.
1. In the **Collections** filter, select **Azure OpenAI**.
1. Select a model such as `gpt-4o-mini` from the Azure OpenAI collection.
1. Select **Confirm** to open the deployment window.
1. Specify the deployment name and modify other default settings depending on your requirements.
1. Select **Deploy**.
1. You land on the deployment details page. Select **Open in playground**.
1. Select **View Code** to obtain code samples that can be used to consume the deployed model in your application.

## Inferencing the Azure OpenAI model

To perform inferencing on the deployed model, you can use the playground or code samples. The playground is a web-based interface that allows you to interact with the model in real-time. You can use the playground to test the model with different prompts and see the model's responses.

For more examples of how to consume the deployed model in your application, see the following Azure OpenAI quickstarts:

- [Get started with Assistants and code interpreter in the playground](../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Chat quickstart](../../ai-services/openai/chatgpt-quickstart.md)

## Regional availability and quota limits of a model

For Azure OpenAI models, the default quota for models varies by model and region. Certain models might only be available in some regions. For more information on availability and quota limits, see [Azure OpenAI quotas and limits](/azure/ai-services/openai/quotas-limits).

## Quota for deploying and inferencing a model

For Azure OpenAI models, deploying and inferencing consume quota that is assigned to your subscription on a per-region, per-model basis in units of Tokens-per-Minute (TPM). When you sign up for Azure AI Foundry, you receive default quota for most of the available models. Then, you assign TPM to each deployment as it is created, thus reducing the available quota for that model by the amount you assigned. You can continue to create deployments and assign them TPMs until you reach your quota limit.

Once you reach your quota limit, the only way for you to create new deployments of that model is to:

- Request more quota by submitting a [quota increase form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pURVJWRU4yRTMxRkszU0NXRFFTTEhaT1g1NyQlQCN0PWcu).
- Adjust the allocated quota on other model deployments to free up tokens for new deployments on the [Azure OpenAI Portal](https://oai.azure.com/portal).

To learn more about quota, see [Azure AI Foundry quota](./quota.md) and [Manage Azure OpenAI quota](../../ai-services/openai/how-to/quota.md?tabs=rest).

## Related content

- Learn more about what you can do in [Azure AI Foundry](../what-is-azure-ai-foundry.md)
- Get answers to frequently asked questions in the [Azure AI FAQ article](../faq.yml)
