---
title: Create and improve your custom analyzer in Content Understanding Studio
titleSuffix: Foundry Tools
description: Create custom analyzers and apply in context learning to improve them using Content Understanding Studio
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

# Create and improve your custom analyzer in Content Understanding Studio

Content Understanding Studio lets you build content analyzers that extract content and fields tailored to your needs. Follow these steps to create a custom analyzer in Content Understanding Studio.

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal, created in a [supported region](/azure/ai-services/content-understanding/language-region-support).
  * This resource is listed under **Foundry** > **Foundry** in the portal.
* [!INCLUDE [foundry-model-deployment-setup](../includes/foundry-model-deployment-setup.md)]

## Log in to Content Understanding Studio

Go to the [Content Understanding Studio portal](https://aka.ms/cu-studio) and sign in using your credentials to get started. If you're familiar with the classic Azure Document Intelligence in Foundry Tools Studio experience, Content Understanding extends the same content and field extraction across all modalities—document, image, video, and audio. Select the option to try the new Content Understanding experience to access multimodal capabilities.

## Create your custom analyzer

1.	**Start with a new project**: To get started with creating your custom analyzer, select `Create project` on the home page. 

2.	**Select your project type**: In this guide, we will select the option to `Extract content and fields with a custom schema`. To learn more about classifying and routing your data, check out [How to classify and route data with Content Understanding](./classification-content-understanding-studio.md).

3.	**Create your project**: Give your project a friendly name and select `Create`.  

4.	**Upload sample data**: Now that your project is configured, you can get started with building your custom analyzer. Upload a sample of your data to the tool, and Content Understanding will classify your data and recommend analyzer templates to give you a starting point.

:::image type="content" source="../media/quickstarts/cu-studio-suggested-templates.png" alt-text="Screenshot of suggested Content Understanding templates." lightbox="../media/quickstarts/cu-studio-suggested-templates.png" :::

5.	**Select a scenario template**: Select a template that best fits your scenario needs. You have the option to customize all schema fields to your specific needs in the next step. 

6.	**Leverage suggested fields**: If your scenario requires custom fields, you can leverage the AI suggestion feature to analyze your data and suggest a full schema with fields that you may be interested in extracting. The tool allows you to keep the suggestions that fit and discard the ones that don't. 

:::image type="content" source="../media/quickstarts/cu-studio-schema-suggestion.png" alt-text="Screenshot of suggested schemas using AI suggestion tool." lightbox="../media/quickstarts/cu-studio-schema-suggestion.png" :::

7.	**Define your schema**: Review the schema fields that were suggested or were part of the template. If there are additional fields that you want to add or change, you can utilize the edit features to refine the schema fields. Note that you can easily go back to refine your schema after testing and after you build your initial analyzer. Once you complete your changes, select `Save`.

8.	**Test your schema**: Once you feel your schema is ready for testing, select `run analysis` to see the output of the schema on your data. You can optionally upload additional pieces of sample data for testing to see how the schema performs. 

9.	**Iterate on your schema**: Repeat steps 6-8 as needed to improve the output of your schema. 

10.	**Optional: In-context learning (documents only)**: To further improve the quality of the output of your schema, you can enable in-context learning. This step lets you bring in a knowledge base of data for the model to reference.

To get started, upload your training data to a blob storage account. Select the **Knowledge** tab and select the blob storage container that contains the training dataset of sample documents. Based on the analyzer you defined, the model assigns labels to your documents. Validate the training data by reviewing and correcting any labels with incorrect output, and add any missing output.

11.	**Build your analyzer**: Once you're satisfied with the output from your analyzer, select **Build analyzer** at the top of the page. Give the analyzer a name and select **Build**.

12. **Use your analyzer**: After your analyzer is built, select **Jump to analyzer list** to view the full list of built analyzers. Select the analyzer you created to see a code sample with a key and endpoint. You can use the analyzer endpoint in your own application via the REST API.

## Next steps

* Learn how to [classify and route your data using Content Understanding Studio](./classification-content-understanding-studio.md).
* Learn more about [best practices for Azure Content Understanding](../concepts/best-practices.md).



