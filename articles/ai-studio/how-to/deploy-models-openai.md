---
title: How to deploy Azure OpenAI models with Azure AI Studio
titleSuffix: Azure AI Studio
description: Learn how to deploy Azure OpenAI models with Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ai-learning-hub
ms.topic: how-to
ms.date: 5/21/2024
ms.reviewer: fasantia
ms.author: mopeakande
author: msakande
---

# How to deploy Azure OpenAI models with Azure AI Studio

In this article, you learn to create Azure OpenAI model deployments in [Azure AI Studio](https://ai.azure.com). 

Azure OpenAI Service offers a diverse set of models with different capabilities and price points. Model availability varies by region. To learn more about the details of each model see [Azure OpenAI Service models](../../ai-services/openai/concepts/models.md).

After you deploy Azure OpenAI models in Azure AI Studio, you can consume the deployments in playgrounds or code. 

## Deploy an Azure OpenAI model from the model catalog

> [!TIP]
> You can use Azure OpenAI Service in AI Studio without creating a project or a connection. If you're only using Azure OpenAI Service, we recommend working outside of a project. Instead of deploying from the model catalog, follow the steps in the [Deploy from the Azure OpenAI Service page](#deploy-from-the-azure-openai-service-page) section. 

Follow the steps below to deploy an Azure OpenAI model such as `gpt-4o-mini` to a real-time endpoint from the AI Studio [model catalog](./model-catalog-overview.md). You need a project to deploy an Azure OpenAI Service model from the model catalog.

1. Go to the [AI Studio home page](https://ai.azure.com).
1. Select the tile that says **Model catalog and benchmarks**. 

    :::image type="content" source="../media/explore/ai-studio-home-model-catalog.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select the model catalog tile." lightbox="../media/explore/ai-studio-home-model-catalog.png":::

    If you don't see this tile, you can also go directly to the [Azure AI model catalog page](https://ai.azure.com/explore/models) in AI Studio.

1. From the **Collections** dropdown, select **Azure OpenAI**. 

    :::image type="content" source="../media/deploy-monitor/catalog-filter-azure-openai.png" alt-text="A screenshot showing how to filter by Azure OpenAI models in the catalog." lightbox="../media/deploy-monitor/catalog-filter-azure-openai.png"::: 

1. Select a model such as `gpt-4o-mini` from the Azure OpenAI collection.
1. Select **Deploy** to open the deployment window. 
1. Select the project where you want to use the deployed model. If you don't have a project, you can create one.
1. Follow the wizard to deploy the model. 

## Deploy from the Azure OpenAI Service page

You can use Azure OpenAI Service in AI Studio without creating a project or a connection. If you're only using Azure OpenAI Service, we recommend working outside of a project as described in this section. 

1. Go to the [AI Studio home page](https://ai.azure.com) and make sure you're signed in with the Azure subscription that has your Azure OpenAI Service resource (with or without model deployments.)
1. Find the tile that says **Focused on Azure OpenAI Service?** and select **Let's go**. 

    :::image type="content" source="../media/azure-openai-in-ai-studio/home-page.png" alt-text="Screenshot of the home page in Azure AI Studio with the option to select Azure OpenAI Service." lightbox="../media/azure-openai-in-ai-studio/home-page.png":::

    If you don't see this tile, you can also go directly to the [Azure OpenAI Service page](https://ai.azure.com/resource/overview) in AI Studio.

1. You should see your existing Azure OpenAI Service resources (with any existing deployments). In case your subscription has multiple Azure OpenAI Service resources, you can use the selector or go to **All resources** to see all your resources.

    :::image type="content" source="../media/ai-services/azure-openai-studio-select-resource.png" alt-text="Screenshot of the Azure OpenAI Service resources page in Azure AI Studio." lightbox="../media/ai-services/azure-openai-studio-select-resource.png":::

1. Select **Deployments** > **+ Deploy model** > **Deploy base model** to open the deployment window. 
1. Select the model that you want to deploy.
1. Follow the wizard to deploy the model.

You can create a new deployment or view existing deployments. For more information about deploying Azure OpenAI models, see [Deploy Azure OpenAI models to production](../how-to/deploy-models-openai.md).

## Inferencing the Azure OpenAI model

To perform inferencing on the deployed model, you can use the playground or code samples. The playground is a web-based interface that allows you to interact with the model in real-time. You can use the playground to test the model with different prompts and see the model's responses. 

For more examples of how to consume the deployed model in your application, see the following Azure OpenAI quickstarts:

- [Get started using Azure OpenAI Assistants](../../ai-services/openai/assistants-quickstart.md?context=/azure/ai-studio/context/context)
- [Chat quickstart](../../ai-services/openai/chatgpt-quickstart.md)

## Regional availability and quota limits of a model

For Azure OpenAI models, the default quota for models varies by model and region. Certain models might only be available in some regions. For more information on availability and quota limits, see [Azure OpenAI Service quotas and limits](/azure/ai-services/openai/quotas-limits).

## Quota for deploying and inferencing a model

For Azure OpenAI models, deploying and inferencing consumes quota that is assigned to your subscription on a per-region, per-model basis in units of Tokens-per-Minute (TPM). When you sign up for Azure AI Studio, you receive default quota for most of the available models. Then, you assign TPM to each deployment as it is created, thus reducing the available quota for that model by the amount you assigned. You can continue to create deployments and assign them TPMs until you reach your quota limit. 

Once you reach your quota limit, the only way for you to create new deployments of that model is to:

- Request more quota by submitting a [quota increase form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR4xPXO648sJKt4GoXAed-0pURVJWRU4yRTMxRkszU0NXRFFTTEhaT1g1NyQlQCN0PWcu).
- Adjust the allocated quota on other model deployments to free up tokens for new deployments on the [Azure OpenAI Portal](https://oai.azure.com/portal).

To learn more about quota, see [Azure AI Studio quota](./quota.md) and [Manage Azure OpenAI Service quota](../../ai-services/openai/how-to/quota.md?tabs=rest).

## Related content

- [Azure OpenAI Service models](../../ai-services/openai/concepts/models.md)
- [Where to use Azure OpenAI Service in AI Studio](../ai-services/where-to-use-ai-services.md)
