---
title: "Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal"
titleSuffix: Azure AI services
description: Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/19/2025
---

# Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal

In this quickstart, you will learn how to use the Content Understanding service in the Azure AI Foundry portal to create a single-file task which will allow you to generate structured outputs from your video, audio, image and document data. The Azure AI Foundry is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. 

A few terms to know before getting started:
* **Task**: Your Content Understanding task is the top-level structure that all of your Content Understanding related work falls under. This guide will offer a step by step introduction to creating your field schema.
* **Field schema**: A field schema is the definition of all of the outputs that you want to extract or generate from your data. Content Understanding offers several prebuilt schemas and they are all fully customizable to meet your business needs. This quickstart will offer guidance to help you build the schema that is right for your scenario.
* **Analyzer**: The Content Understanding analyzer allows you to call the field schema you define as an API call in your own solution. You can build as many analyzers as needed within your task.

This guide will show you how to build and test a Content Understanding analyzer in the AI Foundry. You can then utilize the analyzer in any app or process you build using a simple REST API call, allowing you to extract meaningful outputs on your data at scale. Content Understanding analyzers are fully customizable. You can create an analyzer by building your own schema from scratch or by using a suggested analyzer template offered to address common scenarios across each data type.

:::image type="content" source="../media/overview/component-overview-updated.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="media/overview/component-overview-updated.png" :::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

* An [Azure AI Foundry hub-based project](../../../ai-foundry/how-to/create-projects.md) created in one of the following supported regions: `westus`, `swedencentral`, or `australiaeast`. A project is used to organize your work and save state while building customized AI apps. You can create a project from the home page of AI Foundry, or the [Content Understanding landing page](aka.ms/cu-landing).

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

## Create your single-file task powered by Content Understanding Standard mode

Follow these steps to create a custom task in the Azure AI Foundry. This task will be used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. In this guide, you will select a single-file task utilizing Content Understanding Standard mode, but if you're interested in creating a multi-file task utilizing Pro mode, refer to [Create an Azure AI Content Understanding multi-file task in the Azure AI Foundry portal
](./use-ai-foundry-pro-mode.md). For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first analyzer

Now that everything is configured to get started, we can walk through how to build your first analyzer. 

When you create a single-file Content Understanding task, you'll start by uploading a sample of your data and building your field schema. The schema is the customizable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document, but you can bring in any type of data and the steps remain the same. [Compare the output of this invoice analysis use case to the output of a Content Understanding Pro invoice analysis scenario](). For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

   :::image type="content" source="../media/quickstarts/upload-data.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service suggests analyzer templates based on your content type. Check out [Analyzer templates offered with Content Understanding](../concepts/analyzer-templates.md) for a full list of all templates offered for each modality. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](../concepts/analyzer-templates.md) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

1. Next, you can add fields to your schema to reflect all of the outputs you want to generate. 

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.
  
      For best practices on how to define your field schema, refer to [best practices for Azure AI Content Understanding](./best-practices.md).

1. Once you feel that the schema is ready to test, select **Save**. You can always come back and make changes if needed.

   :::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add more data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.

## Sharing your project

In order to share and manage access to the project you created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of where to find management center.":::

You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/management-center.png" alt-text="Screenshot of Project users section of management center.":::

## Next steps

 * Learn more about creating and using [analyzer templates](../concepts/analyzer-templates.md) in the Azure AI Foundry.
