---
title: Create and improve your custom analyzer in Content Understanding Studio
titleSuffix: Azure AI services
description: Create custom analyzers and apply in context learning to improve them using Content Understanding Studio
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 10/30/2025
ms.service: azure-ai-content-understanding
ms.topic: how-to
ms.custom:
  - ignite-2024-understanding-release
  - references_regions
  - ignite-2025
---

# Create and improve your custom analyzer in Content Understanding Studio

Content Understanding Studio enables you to build powerful content analyzers that extract content and fields tailored to the specific needs of your scenario. Follow the steps below to create your own custom analyzer in Content Understanding Studio.

## Prerequisites
To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Log in to Content Understanding Studio
Navigate to the [Content Understanding Studio portal](https://aka.ms/cu-studio) and sign in using your credentials to get started. You may recognize the classic Azure AI Document Intelligence Studio experience; Content Understanding extends the same content and field extraction that you are familiar with in Document Intelligence across all modalities - document, image, video, and audio. Select the option to try out the new Content Understanding experience to get all of the multimodal capabilities of the service. 

## Create your custom analyzer

1.	**Start with a new project**: To get started with creating your custom analyzer, select `Create project` on the home page. 

2.	**Select your project type**: In this guide, we will select the option to `Extract content and fields with a custom schema`. To learn more about classifying and routing your data, check out [How to classify and route data with Content Understanding](./classification-content-understanding-studio.md).

3.	**Create your project**: Give your project a friendly name and select `Create`.  

4.	**Upload sample data**: Now that your project is configured, you can get started with building your custom analyzer. Upload a sample of your data to the tool, and Content Understanding will classify your data and recommend analyzer templates to give you a starting point.

<!--[Insert photo of recommended templates]-->

5.	**Select a scenario template**: Select a template that best fits your scenario needs. If there is not a template to start with, select the option to create a new analyzer.

6.	**Leverage suggested fields**: If creating from scratch, you can leverage the AI suggestion feature to analyze your data and suggest a full schema with fields that you may be interested in extracting. 

<!--[Insert photo of suggested schema fields.]-->

7.	**Define your schema**: Review the schema fields that were suggested or were part of the template. If there are additional fields that you want to add or change, you can utilize the edit features to refine the schema fields. Note that you can easily go back to refine your schema after testing and after you build your initial analyzer. Once you complete your changes, select `Save`.

8.	**Test your schema**: Once you feel your schema is ready for testing, select `run analysis` to see the output of the schema on your data. You can optionally upload additional pieces of sample data for testing to see how the schema performs. 

9.	**Iterate on your schema**: Repeat steps 6-8 as needed to improve the output of your schema. 

10.	**Optional step: In-context learning (documents only)**: To further improve the quality of the output of your schema, you have the option to enable in-context learning. This step will enable you to bring in a knowledge base of data for the model to reference and learn from.

To get started, you will need to upload your training data to a blob storage account. Select the “Knowledge” tab and select the blob storage container containing the training dataset of sample documents. Based on the analyzer you just defined, the model will assign labels to your document. Validate that training data by reviewing and correcting any labels that have provided an incorrect output, or add any missing output. 

<!--[Insert photo of in-context learning]-->

11.	**Build your analyzer**: Once you’re satisfied with the output from your analyzer, select the `Build analyzer` button at the top of the page. Give the analyzer a name and select `Save`. 

12. **Use your analyzer**: Now you have an analyzer endpoint that you can utilize in your own application via the REST API. This has been a walkthrough of how to use Content Understanding Studio to build a custom analyzer. 

## Next steps
* Learn how to [classify and route your data using Content Understanding Studio](./classification-content-understanding-studio.md)
* Learn more about [Best practices for Azure AI Content Understanding](../concepts/best-practices.md) 



