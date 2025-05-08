---
title: "Use Azure AI Content Understanding Analyzer templates in the Azure AI Foundry"
titleSuffix: Azure AI services
description: Learn how to use Content Understanding Analyzer templates in Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 05/19/2025
ms.custom: ignite-2024-understanding-release
---

# Use Content Understanding in the Azure AI Foundry

[The Azure AI Foundry](https://aka.ms/cu-landing) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. Azure AI Content Understanding is a new generative [Azure AI Service](../../what-are-ai-services.md) that analyzes files from varied modalities and extracts structured output in a user-defined field format. Input sources include document, video, image, and audio data. This guide shows you how to build and test a Content Understanding analyzer in the AI Foundry. You can then utilize the extracted data in any app or process you build using a simple REST API call. Content Understanding analyzers are fully customizable. You can create an analyzer by building your own schema from scratch or by using a suggested analyzer template offered to address common scenarios across each data type.

  :::image type="content" source="../media/quickstarts/ai-foundry-overview.png" alt-text="Screenshot of the Content Understanding workflow in the Azure AI Foundry.":::

## Prerequisites

To get started, make sure you have the following resources and permissions:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/) before you begin.

* An Azure AI Foundry project created in one of the following supported regions: westus, swedencentral, or australiaeast. If you're creating a project for the first time, *see* [How to create an Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md) to learn more. It's important to note you need the proper permissions to create a project, or your admin may create one for you.

> [!IMPORTANT]
> If your organization requires you to customize the security of storage resources, refer to [Azure AI services API access keys](../../../ai-foundry/concepts/encryption-keys-portal.md) to create resources that meet your organizations requirements through the Azure portal. To learn how to utilize customer managed keys, refer to [(Preview) Service-side storage of encrypted data when using customer-managed keys](../../../ai-foundry/concepts/encryption-keys-portal.md#preview-service-side-storage-of-encrypted-data-when-using-customer-managed-keys). 

## Create your first Content Understanding project in the AI Foundry portal

> [!NOTE]
> The Content Understanding project type is separate from the Generative AI project type, also available in the AI Foundry portal.

In order to try out [the Content Understanding service in the AI Foundry portal](https://aka.ms/cu-landing), you have to create a Content Understanding project. You can access Content Understanding from:

* The [AI Foundry home page](https://ai.azure.com/)

   :::image type="content" source="../media/quickstarts/foundry-home-page.png" lightbox="../media/quickstarts/foundry-home-page.png" alt-text="Screenshot of the AI Services landing page in AI Foundry.":::
   

* The [AI Foundry AI Services landing page](https://ai.azure.com/explore/aiservices)

   :::image type="content" source="../media/quickstarts/ai-services-landing-page.png" lightbox="../media/quickstarts/ai-services-landing-page.png" alt-text="Screenshot of the AI Services landing page.":::

Once on the Content Understanding page, select `Create a new Content Understanding Project`:

   :::image type="content" source="../media/quickstarts/cu-landing-page.png" lightbox="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of Content Understanding page.":::

Follow the steps in the project creation wizard. Once you complete the setup steps, select `Create project`.

## Sharing your content understanding project

In order to share and manage access to the Content Understanding project you created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-find-management-center.png" alt-text="Screenshot of where to find management center.":::


You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/cu-management-center.png" alt-text="Screenshot of Project users section of management center.":::

## Build your first analyzer

Now that everything is configured to get started, we can walk through, step-by-step, how to build your first analyzer, starting with building the schema. The schema is the customizable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document, but you can bring in any type of data and the steps remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service suggests analyzer templates based on your content type. Check out [Analyzer templates offered with Content Understanding](../concepts/analyzer-templates.md) for a full list of all templates offered for each modality. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](../concepts/analyzer-templates.md) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

1. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-type-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * Specify the method to generate the value for each field.

1. Select **Save**.

   :::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add more data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data. Check out [Quickstart: Azure AI Content Understanding REST APIs](./use-rest-api.md) to utilize the REST API to call your analyzer.


## Next steps

 * In this quickstart, you learned how to create a Content Understanding analyzer using the Azure AI Foundry. To use the Content Understanding [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true), see the [REST API quickstart](use-rest-api.md).

