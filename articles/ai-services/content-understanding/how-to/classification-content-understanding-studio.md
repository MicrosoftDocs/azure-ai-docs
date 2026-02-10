---
title: Classify and route your data using Content Understanding Studio
titleSuffix: Foundry Tools
description: Learn about how to classify and route your data using Content Understanding Studio
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Classify and route your data using Content Understanding Studio

Content Understanding Studio enables you to create custom classification workflows that route your data to the right analyzer. With routing, you can send multiple data streams through the same pipeline and ensure your data is routed to the best analyzer.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal, created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
  * This resource is listed under **Foundry** > **Foundry** in the portal.
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Sign in to Content Understanding Studio

Go to the [Content Understanding Studio portal](https://aka.ms/cu-studio) and sign in with your credentials. If you're familiar with the classic Azure Document Intelligence in Foundry Tools Studio experience, Content Understanding extends the same content and field extraction across all modalities—document, image, video, and audio. Select the option to try the new Content Understanding experience to access multimodal capabilities.

## Create your custom categories

Custom categories let you route your data to a specific analyzer so you get the best output based on the type of data. In this guide, you learn how to classify invoice documents based on the client that provided them. Documents for different clients might have a different structure depending on the unique business agreement in place. This classification workflow ensures that the documents are analyzed with the correct context. To successfully route your data, you might want to create custom analyzers to route to depending on your scenario. For more information on building custom analyzers, see [Create and improve your custom analyzer in Content Understanding Studio](./customize-analyzer-content-understanding-studio.md).

1.	**Start with a new project**: To get started with creating your custom classification workflow, select **Create project** on the home page. 

1.	**Select your project type**: For this scenario, select the option to `Classify and route with custom categories`. To learn more about creating custom analyzers for content and field extraction, see [Create and improve your custom analyzer in Content Understanding Studio](./customize-analyzer-content-understanding-studio.md).

1.	**Upload your data**: To get started with classifying, upload a piece of sample data.

1.	**Create routing rules**: Under the **Routing rules** tab, select `Add category`. Give the category a name and description, and select an analyzer to correspond to that route. For example, if you're analyzing invoices from multiple clients that each require custom schemas, you can route to the custom analyzer that was built for that specific invoice type. The tool allows you to preview the schema for each analyzer to ensure you have the right one.

    :::image type="content" source="../media/quickstarts/classify-define-routes.png" alt-text="Screenshot of routes UX for classification." lightbox="../media/quickstarts/classify-define-routes.png" :::

1.	**Test your classification workflow**: When your custom routing rules are ready for testing, select **Run analysis** to see the output of the rules on your data. You can optionally upload additional pieces of sample data for testing to see how it performs with multiple different rules.

    :::image type="content" source="../media/quickstarts/classify-test.png" lightbox="../media/quickstarts/classify-test.png" alt-text="Screenshot of Content Understanding Studio with the Test button highlighted.":::

1. **Build your classification analyzer**: When you’re satisfied with the output, select the **Build analyzer** button at the top of the page. Give the analyzer a name and select **Save**.

1. **Use your classification analyzer**: Now you have an analyzer endpoint that you can use in your own application via the REST API.

## Next steps

* Learn more about [best practices for Azure Content Understanding in Foundry Tools](../concepts/best-practices.md).

