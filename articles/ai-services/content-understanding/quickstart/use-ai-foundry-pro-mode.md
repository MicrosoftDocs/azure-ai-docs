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

# Create an Azure AI Content Understanding multi-file task in the Azure AI Foundry portal

In this quickstart, you will learn how to use the Content Understanding service in the Azure AI Foundry portal to create a multi-file task. The Azure AI Foundry is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. 

A few terms to know before getting started:
* **Task**: Your Content Understanding task is the top-level structure that all of your Content Understanding related work falls under. This guide will offer a step by step introduction to creating your field schema.
* **Field schema**: A field schema is the definition of all of the outputs that you want to extract or generate from your data. Content Understanding offers several prebuilt schemas and they are all fully customizable to meet your business needs. This quickstart will offer guidance to help you build the schema that is right for your scenario.
* **Analyzer**: The Content Understanding analyzer allows you to call the field schema you define as an API call in your own solution. You can build as many analyzers as needed within your task.
* **Reference data**: Reference data includes documents that can aid in providing context that references the service at inference time. For example, if you're looking to analyze invoices to ensure they're consistent with a contractual agreement, you can supply the invoice and other relevant documents (for example, a purchase order) as inputs, and supply the contract files as reference data. The service applies reasoning to validate the input documents according to your schema, which might be to identify discrepancies to flag for further review.
* **Multi-step reasoning**: Multi-step reasoning takes data analysis a step further than extracting and aggregating structured data and allows you to draw conclusions on that data, minimizing the need for human review.

This guide will show you how to build and test a Content Understanding analyzer in the AI Foundry. You can then utilize the analyzer in any app or process you build using a simple REST API call, allowing you to extract meaningful outputs on your data at scale. Content Understanding analyzers are fully customizable. You can create an analyzer by building your own schema from scratch or by using a suggested analyzer template offered to address common scenarios across each data type.

:::image type="content" source="../media/overview/component-overview-updated.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="media/overview/component-overview-updated.png" :::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

* An [Azure AI Foundry hub-based project](../../../ai-foundry/how-to/create-projects.md) created in one of the following supported regions: `westus`, `swedencentral`, or `australiaeast`. A project is used to organize your work and save state while building customized AI apps. You can create a project from the home page of AI Foundry, or the [Content Understanding landing page](aka.ms/cu-landing).

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

## Create a custom task

Follow these steps to create a custom task in the Azure AI Foundry. This task will be used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. Choose a task type. The type of task that you create depends on what data you plan to bring in. This guide will help you build a multi-file task utilizing Content Understanding Pro mode, but if you're interested in creating a single-file task utilizing Standard mode, refer to [Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal](./use-ai-foundry.md). For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Creating your multi-file task powered by Content Understanding Pro mode

When you create a multi-file Content Understanding task, you'll start by building your field schema. The schema is the customizable framework that guides the analyzer to extract the preferred insights from your data.

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
