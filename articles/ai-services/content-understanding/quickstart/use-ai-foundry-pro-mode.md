---
title: "Create an Azure AI Content Understanding multi-file task in the Azure AI Foundry portal"
titleSuffix: Azure AI services
description: Create an Azure AI Content Understanding multi-file task in the Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/29/2025
---

# Try out Azure AI Content Understanding on multiple files in the Azure AI Foundry portal

This quickstart shows you how to use the Content Understanding service in the Azure AI Foundry portal to extract structured information from your data. Azure AI Foundry enables you to build and deploy generative AI applications and APIs responsibly.

Suppose you have document files and you want to automatically extract key information from them, while also comparing to reference data to infer conclusions from your files. With Content Understanding, you can create a task to organize your data processing, define a field schema that specifies the information to extract or generate, and then build an analyzer that will apply reasoning to your data to output key inferences and conclusions. The analyzer becomes an API endpoint that you can integrate into your applications or workflows.

In this guide, you'll walk through building and testing an analyzer for your scenario. You can start from scratch or use suggested templates for common use cases.

:::image type="content" source="../media/overview/component-overview-updated.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="media/overview/component-overview-updated.png" :::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

* An [Azure AI Foundry hub-based project](../../../ai-foundry/how-to/create-projects.md) created in one of the following [supported regions](../service-limits.md): `westus`, `swedencentral`, or `australiaeast`. A project is used to organize your work and save state while building customized AI apps. You can create a project from the [home page of AI Foundry](https://aka.ms/foundry-home-page), or the [Content Understanding landing page](https://aka.ms/cu-landing).

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

## Create your multi-file task powered by Content Understanding Pro mode

Follow these steps to create a custom task in the Azure AI Foundry. This task will be used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. In this guide, you will select a `multi-file task` utilizing Content Understanding Pro mode, but if you're interested in creating a single-file task utilizing Standard mode, refer to [Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal](./use-ai-foundry.md). For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first analyzer

When you create a multi-file Content Understanding task, you'll start by uploading one or more samples of data and building your field schema. The schema is the customizable framework that guides the analyzer to extract the preferred insights from your data.

In this example, the schema is created to extract key fields from an invoice document, but you can bring in any document based data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload one or multiple sample files of invoice documents or any other document data relevant to your scenario.

   :::image type="content" source="../media/quickstarts/upload-test-data.png" alt-text="Screenshot of upload step in user experience.":::

2. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.
  
   :::image type="content" source="../media/quickstarts/add-fields.png" alt-text="Screenshot of upload step in user experience.":::

  
3. Once you feel that the schema is ready to test, select **Save**. You can always come back and make changes if needed.

   :::image type="content" source="../media/quickstarts/save-schema.png" alt-text="Screenshot of completed schema.":::

4. Upload one or more documents for reference data for the service to analyze. Adding reference data allows the model to compare and apply multi-step reasoning to your test data in order to infer conclusions about that data.

   :::image type="content" source="../media/quickstarts/reference-data.png" alt-text="Screenshot of completed schema.":::

5.  Run analysis on your data. Kicking off analysis generates an output on your test files based on the schema that you just created, and applies predictions by comparing that output to your reference data.

   :::image type="content" source="../media/quickstarts/prediction.png" alt-text="Screenshot of completed schema.":::

6.  Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/quickstarts/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. When you select the analyzer you just created, you can view sample code to get started with implenting this in code.

   :::image type="content" source="../media/quickstarts/view-code.png" alt-text="Screenshot of completed schema.":::

Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.


## Sharing your project

In order to share and manage access to the project you created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of where to find management center.":::


You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/management-center.png" alt-text="Screenshot of Project users section of management center.":::

## Next steps

 * Learn more about 
