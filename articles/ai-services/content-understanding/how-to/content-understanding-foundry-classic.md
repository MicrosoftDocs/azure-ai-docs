---
title: Create Content Understanding Standard and Pro tasks in the Azure AI Foundry Classic portal
titleSuffix: Azure AI services
description: Utilize the Foundry classic portal to create Content Understanding custom tasks
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

# Create Content Understanding Standard and Pro tasks in the Azure AI Foundry Classic portal

Suppose you have files—such as documents, images, audio, or video—and you want to automatically extract key information from them. With Content Understanding, you can create a task to organize your data processing, define a field schema that specifies the information to extract or generate, and then build an analyzer. The analyzer becomes an API endpoint that you can integrate into your applications or workflows. 

This guide shows you how to utilize  Content Understanding Standard and Pro modes in the Azure AI Foundry Classic portal to build and test a custom analyzer that extracts structured information from your data. 

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

* An [Azure AI Foundry hub-based project](../../../ai-foundry/how-to/create-projects.md) created in one of the following [supported regions](../service-limits.md): `westus`, `swedencentral`, or `australiaeast`. Use a project to organize your work and save state while building customized AI apps. You can create a project from the [home page of AI Foundry](https://aka.ms/foundry-home-page), or the [Content Understanding landing page](https://aka.ms/cu-landing).

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

# [Standard mode](#tab/standard)

## Create your single-file task powered by Content Understanding Standard mode

Follow these steps to create a custom task in the Azure AI Foundry. Use this task to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
1. Select to create a `Single-file task` utilizing Content Understanding Standard mode. For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes (preview)](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first analyzer

Now that everything is configured, you can build your first analyzer. 

When you create a single-file Content Understanding task, you start by uploading a sample of your data and building your field schema. The schema is the customizable framework that allows the analyzer to extract insights from your data. In this example, you create the schema to extract key data from an invoice document, but you can bring in any type of data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload a [sample file of an invoice document](https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf) or any other data relevant to your scenario.

   :::image type="content" source="../media/quickstarts/upload-data.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service suggests analyzer templates based on your content type. Check out [Analyzer templates offered with Content Understanding](../concepts/analyzer-templates.md) for a full list of all templates offered for each modality. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](../concepts/analyzer-templates.md) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/quickstarts/invioce-template.png" alt-text="Screenshot of analyzer templates.":::

1. Next, add fields to your schema to reflect all of the outputs you want to generate. 

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.
  
      For best practices on how to define your field schema, refer to [best practices for Azure AI Content Understanding](../concepts//best-practices.md). It might take a few minutes to build out your schema.

1. When your schema is ready to test, select **Save**. You can always come back and make changes if needed.

   :::image type="content" source="../media/quickstarts/define-invoice-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add more data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/quickstarts/test-invoice.png" alt-text="Screenshot of schema testing step.":::

1. When you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/quickstarts/build-invoice-analyzer.png" alt-text="Screenshot of built analyzer.":::

You've successfully built your first Content Understanding analyzer and are ready to start extracting insights from your data. Check out [Quickstart: Azure AI Content Understanding REST APIs](../quickstart/use-rest-api.md) to utilize the REST API to call your analyzer.

# [Pro mode](#tab/pro)

## Create your multi-file task powered by Content Understanding Pro mode

Follow these steps to create a custom task in the Azure AI Foundry. This task is used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. Select to create a `Multi-file task` utilizing Content Understanding Pro mode. For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes (preview)](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first analyzer

To create a multi-file Content Understanding task, start by uploading one or more samples of data and building your field schema. The schema is the customizable framework that guides the analyzer to extract the preferred insights from your data.

In this example, the schema is created to extract key fields from an invoice document, but you can bring in any document based data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload one or multiple sample files of invoice documents or any other document data relevant to your scenario.

   :::image type="content" source="../media/quickstarts/upload-test-data.png" alt-text="Screenshot of upload step in user experience." lightbox="../media/quickstarts/upload-test-data.png":::

2. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.

   :::image type="content" source="../media/quickstarts/add-fields.png" alt-text="Screenshot of create schema step in user experience." lightbox="../media/quickstarts/add-fields.png":::


3. Once you feel that the schema is ready to test, select **Save**. You can always come back and make changes if needed.

   :::image type="content" source="../media/quickstarts/save-schema.png" alt-text="Screenshot of completed schema."  lightbox="../media/quickstarts/save-schema.png":::

4. Upload one or more documents for reference data for the service to analyze. Adding reference data allows the model to compare and apply multi-step reasoning to your test data in order to infer conclusions about that data.

   :::image type="content" source="../media/quickstarts/reference-data.png" alt-text="Screenshot of user adding reference data." lightbox="../media/quickstarts/reference-data.png":::

5.  Run analysis on your data. Kicking off analysis generates an output on your test files based on the schema that you created, and applies predictions by comparing that output to your reference data.

   :::image type="content" source="../media/quickstarts/prediction.png" alt-text="Screenshot of user running analysis on their data." lightbox="../media/quickstarts/prediction.png":::

6.  Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/quickstarts/build-analyzer.png" alt-text="Screenshot of built analyzer." lightbox="../media/quickstarts/build-analyzer.png":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. You can select the analyzer you created and view sample code to get started.

   :::image type="content" source="../media/quickstarts/view-code.png" alt-text="Screenshot of sample code." lightbox="../media/quickstarts/view-code.png":::

Check out [Quickstart: Azure AI Content Understanding REST APIs](../quickstart/use-rest-api.md) to utilize the REST API to call your analyzer.

---

## Sharing your project

To share the project you created and manage access, go to the Management Center. You can find it at the bottom of the navigation pane for your project:

  :::image type="content" source="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of where to find management center.":::

In the Management Center, you can manage users and assign individual roles:

   :::image type="content" source="../media/quickstarts/management-center.png" alt-text="Screenshot of Project users section of management center.":::


## Next steps

 * Learn how to call the REST API at [Quickstart: Azure AI Content Understanding REST APIs](../quickstart/use-rest-api.md)
