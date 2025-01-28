---
title: "Use Azure AI Content Understanding Analyzer templates in Azure AI Foundry portal"
titleSuffix: Azure AI services
description: Learn how to use Content Understanding Analyzer templates in Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# Use Content Understanding in Azure AI Foundry portal
[Azure AI Foundry portal](https://ai.azure.com/) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. This guide shows you how to use Content Understanding and build an analyzer, either by creating your own schema from scratch or by using a suggested analyzer template.

  :::image type="content" source="../media/quickstarts/ai-foundry-overview.png" alt-text="Screenshot of the Content Understanding workflow in the Azure AI Foundry.":::

## Steps to create a Content Understanding analyzer

Azure AI Foundry portal enables you to build a Content Understanding analyzer tailored to your specific needs. An analyzer can extract data from your content based on your scenario.

Follow these steps to create your own analyzer:

1. Upload a sample data file.

1. Select an analyzer template or build your own schema from scratch.

1. Customize the schema to fit your specific scenario.

1. Test the analyzer on your data and validate its accuracy.

1. Build the analyzer to integrate it into your applications.

## Build a schema

To follow is an example of building an analyzer to extract key data from an invoice document:

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of upload step in user experience.":::

1. Content Understanding suggests analyzer templates based on your content type. For this example, select **Document analysis** and build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See Analyzer templates for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

1. Add fields to your schema:

    * Specify clear and simple field names. Example fields: **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-type-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * *[Optional]* Specify the method to generate the value for each field.

1. Select **Save**.

   :::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

1. Content Understanding generates the output based on your schema. Test the analyzer's accuracy on added data or make changes to the schema if needed.

   :::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality, select **Build analyzer**. This action creates an analyzer that you can integrate into your applications. You also receive an analyzer ID, which you can use to call the analyzer from your code.

   :::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

## Analyzer templates

Content Understanding analyzer templates give you a head start by allowing you to build your analyzer without creating schemas from scratch. They're fully customizable, allowing you to adjust any fields in the schemas to better fit your needs.

The following analyzer templates are available for use in the [Azure AI Foundry portal Content Understanding experience](https://ai.azure.com/).

# [Document](#tab/document)

|Template| Description|
| ----|----|----|
|Document analysis |Analyze documents to extract text, layout, structured fields, and more.|
|Text analysis |Analyze texts and extract structured fields.|

   :::image type="content" source="../media/analyzer-template/image-templates.png" alt-text="Screenshot of document analyzer template.":::

# [Image](#tab/image)

|Template| Description|
| ----|----|----|
|Image analysis |Analyze images and extract structured fields.|
|Retail inventory management |Retail inventory management for monitoring of products on shelves.|
|Defect detection |Identify potential defects in provided images of metal plates.|

   :::image type="content" source="../media/analyzer-template/image-templates.png" alt-text="Screenshot of image analyzer template.":::

# [Audio](#tab/audio)

|Template| Description|
| ----|----|----|
|Audio transcription |Transcribe audio recordings.|
|Conversation summarization |Transcribe conversations and extract summaries.|
|Post call analytics |Analyze call center conversations to extract transcripts, summaries, sentiment, and more.|


   :::image type="content" source="../media/analyzer-template/audio-templates.png" alt-text="Screenshot of audio analyzer template.":::

# [Video](#tab/video)

|Template| Description|
| ----|----|----|
|Video shot analysis |Analyze videos to extract transcript and structured fields for each shot.|
|Media asset management |Extract structured information from marketing videos, news content, broadcast media, television episodes, and film archives.|
|Advertising |Advertising analysis and moderation.|


   :::image type="content" source="../media/analyzer-template/video-templates.png" alt-text="Screenshot of video analyzer template.":::

---

## Next steps

 * In this quickstart, you learned how to create an analyzer in Azure portal. To use [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true), *see* the [REST API quickstart](use-rest-api.md).

