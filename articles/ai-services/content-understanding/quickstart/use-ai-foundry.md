---
title: "Use Azure AI Content Understanding Analyzer templates in the Azure AI Foundry"
titleSuffix: Azure AI services
description: Learn how to use Content Understanding Analyzer templates in Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/19/2025
---

# Use Azure AI Content Understanding in the Azure AI Foundry

In this quickstart, you learn how to create a custom task and build your first analyzer using the Azure AI Foundry. The Azure AI Foundry is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. You also learn how to share your project with other users.

[Azure AI Foundry](../../../ai-foundry/index.yml) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. Azure AI Content Understanding is a new generative [Azure AI Service](../../what-are-ai-services.md) that analyzes files from varied modalities and extracts structured output in a user-defined field format. 

Input sources include document, video, image, and audio data. This guide shows you how to build and test a Content Understanding analyzer in the AI Foundry. You can then utilize the extracted data in any app or process you build using a simple REST API call. Content Understanding analyzers are fully customizable. You can create an analyzer by building your own schema from scratch or by using a suggested analyzer template offered to address common scenarios across each data type.

:::image type="content" source="../media/quickstarts/ai-foundry-overview.png" alt-text="Screenshot of the Content Understanding workflow in the Azure AI Foundry.":::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

* An [Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md) created in one of the following supported regions: `westus`, `swedencentral`, or `australiaeast`. A project is used to organize your work and save state while building customized AI apps.

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

* If your organization requires you to customize the security of storage resources, refer to [Azure AI services API access keys](../../../ai-foundry/concepts/encryption-keys-portal.md) to create resources that meet your organizations requirements through the Azure portal. To learn how to utilize customer managed keys, refer to [Encrypt data using customer-managed keys](../../../ai-foundry/concepts/encryption-keys-portal.md). 

## Create a custom task

Follow these steps to create a custom task in the Azure AI Foundry. This task will be used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. Choose a task type. The type of task that you create depends on what data you plan to bring in.
* [Single-file task:](#single-file-task-standard-mode) A single-file task utilizes Content Understanding Standard mode and allows you to bring in one file to create your analyzer:
* [Multi-file task:](#multi-file-task-pro-mode) A multi-file task utilizes Content Understanding Pro mode and allows you to bring in multiple files to create your analyzer. You can also bring in a set of reference data that the service can use to perform multi-step reasoning and make conclusions about your data. To learn more about the difference between Content Understanding Standard and Pro mode, check out [Azure AI Content Understanding pro and standard modes](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first task analyzer

Now that everything is configured to get started, we can walk through, step-by-step, how to build your first analyzer. 

### Single-file task (Standard mode)

When you create a single-file Content Understanding task, you'll start by building your field schema. The schema is the customizable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document, but you can bring in any type of data and the steps remain the same. [Compare the output of this invoice analysis use case to the output of a Content Understanding Pro invoice analysis scenario](). For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).


1. Upload a sample file of an invoice document or any other data relevant to your scenario.

   :::image type="content" source="../media/quickstart/upload-data.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service suggests analyzer templates based on your content type. Check out [Analyzer templates offered with Content Understanding](../concepts/analyzer-templates.md) for a full list of all templates offered for each modality. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](../concepts/analyzer-templates.md) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

1. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.

1. Select **Save**.

   :::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add more data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.

### Multi-file task (Pro mode)

When you create a multi-file Content Understanding task, you'll start by building your field schema. The schema is the customizable framework that guides the analyzer to extract the preferred insights from your data.

In this example, the schema is created to extract key fields from an invoice document, but you can bring in any document based data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload one or multiple sample files of invoice documents or any other document data relevant to your scenario.

   :::image type="content" source="../media/quickstart/upload-test-data.png" alt-text="Screenshot of upload step in user experience.":::

2. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.
  
   :::image type="content" source="../media/quickstart/add-fields.png" alt-text="Screenshot of upload step in user experience.":::

  
3. Select **Save**.

   :::image type="content" source="../media/quickstart/save-schema.png" alt-text="Screenshot of completed schema.":::

4. Upload one or more pieces of reference data for the service to analyze. Adding reference data allows the model to compare and apply multi-step reasoning to your test data in order to infer conclusions about that data.

   :::image type="content" source="../media/quickstart/reference-data.png" alt-text="Screenshot of completed schema.":::

5.  Run analysis on your data. Kicking off analysis generates an output on your test files based on the schema that you just created, and applies predictions by comparing that output to your reference data.

   :::image type="content" source="../media/quickstart/prediction.png" alt-text="Screenshot of completed schema.":::

6.  Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/quickstart/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. When you select the analyzer you just created, you can view sample code to get started with implenting this in code.

   :::image type="content" source="../media/quickstart/view-code.png" alt-text="Screenshot of completed schema.":::

Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.

## Sharing your project

In order to share and manage access to the project you created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-find-management-center.png" alt-text="Screenshot of where to find management center.":::


You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/cu-management-center.png" alt-text="Screenshot of Project users section of management center.":::


   :::image type="content" source="../media/analyzer-template/sample-code.png" alt-text="Screenshot of analyzer sample code.":::

## Next steps

 * Learn more about creating and using [analyzer templates](../concepts/analyzer-templates.md) in the Azure AI Foundry.
