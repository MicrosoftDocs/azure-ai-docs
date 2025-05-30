---
title: "Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal"
titleSuffix: Azure AI services
description: Create an Azure AI Content Understanding single-file task in the Azure AI Foundry portal
author: laujan
manager: nitinme
ms.author: kabrow
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/19/2025
---

# Quickstart: Use Content Understanding with a single file

This quickstart shows you how to use the Content Understanding service in the [**Azure AI Foundry portal**](https://ai.azure.com/explore/aiservices/vision/contentunderstanding) to extract structured information from your data. Azure AI Foundry enables you to build and deploy generative AI applications and APIs responsibly.
 
Suppose you have files—such as documents, images, audio, or video—and you want to automatically extract key information from them. With Content Understanding, you can create a task to organize your data processing, define a field schema that specifies the information to extract or generate, and then build an analyzer. The analyzer becomes an API endpoint that you can integrate into your applications or workflows.
 
In this guide, we walk you through building and testing an analyzer for your scenario. You can start from scratch or use suggested templates for common use cases.

:::image type="content" source="../media/overview/component-overview-updated.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="../media/overview/component-overview-updated.png" :::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/).

* An [Azure AI Foundry hub-based project](../../../ai-foundry/how-to/create-projects.md) created in one of the following [supported regions](../service-limits.md): `westus`, `swedencentral`, or `australiaeast`. A project is used to organize your work and save state while building customized AI apps. You can create a project from the [home page of AI Foundry](https://aka.ms/foundry-home-page), or the [Content Understanding landing page](https://aka.ms/cu-landing).

[!INCLUDE [hub based project required](../../../ai-foundry/includes/uses-hub-only.md)]

## Create your single-file task powered by Content Understanding Standard mode

Follow these steps to create a custom task in the Azure AI Foundry. This task is used to build your first analyzer.

1. Go to the **Home** page of [Azure AI Foundry](https://ai.azure.com).
1. Select your hub based project. You might need to select **View all resources** to see your project.
1. Select **Content Understanding** from the left navigation pane.
1. Select **+ Create**.
2. In this guide, you create a `Single-file task` utilizing Content Understanding Standard mode, but if you're interested in creating a multi-file task utilizing Pro mode, refer to [Create an Azure AI Content Understanding multi-file task in the Azure AI Foundry portal](./use-ai-foundry-pro-mode.md). For more information on which mode is right for your scenario, check out [Azure AI Content Understanding pro and standard modes](../concepts/standard-pro-modes.md).
1. Enter a name for your task. Optionally, enter a description and change other settings.
1. Select **Create**.

## Create your first analyzer

Now that everything is configured to get started, we can walk through how to build your first analyzer. 

When you create a single-file Content Understanding task, you start by uploading a sample of your data and building your field schema. The schema is the customizable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document, but you can bring in any type of data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload a [sample file of an invoice document](https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf) or any other data relevant to your scenario.

   :::image type="content" source="../media/quickstarts/upload-data.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service suggests analyzer templates based on your content type. Check out [Analyzer templates offered with Content Understanding](../concepts/analyzer-templates.md) for a full list of all templates offered for each modality. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](../concepts/analyzer-templates.md) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/quickstarts/invioce-template.png" alt-text="Screenshot of analyzer templates.":::

1. Next, you can add fields to your schema to reflect all of the outputs you want to generate. 

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-schema-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.
  
      For best practices on how to define your field schema, refer to [best practices for Azure AI Content Understanding](../concepts//best-practices.md). It may take a few minutes to build out your schema.

1. Once you feel that the schema is ready to test, select **Save**. You can always come back and make changes if needed.

   :::image type="content" source="../media/quickstarts/define-invoice-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add more data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/quickstarts/test-invoice.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/quickstarts/build-invoice-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.

## Sharing your project

In order to share and manage access to the project you created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of where to find management center.":::

You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/management-center.png" alt-text="Screenshot of Project users section of management center.":::

## Next steps

 * Learn more about creating and using [analyzer templates](../concepts/analyzer-templates.md) in the Azure AI Foundry.
