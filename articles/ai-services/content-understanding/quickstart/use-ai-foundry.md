---
title: "Use Azure AI Content Understanding Analyzer templates in Azure AI Foundry"
titleSuffix: Azure AI services
description: Learn how to use Content Understanding Analyzer templates in Azure AI Foundry
author: laujan
manager: nitinme
ms.service: azure
ms.topic: quickstart
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# Use Content Understanding in Azure AI Foundry
[Azure AI Foundry](https://ai.azure.com/) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. This guide will show you how to use Content Understanding to build an analyzer, either by creating your own schema from scratch or by using a suggested analyzer template.

## Steps to create a Content Understanding analyzer

Azure AI Foundry enables you to build a Content Understanding analyzer tailored to your specific needs. An analyzer can extract data from your content based on your scenario.

Follow these steps to create your own analyzer:

1. Upload a sample data file.
2. Select an analyzer template or build your own schema from scratch.
3. Customize the schema to fit your specific scenario.
4. Test the analyzer on your data to validate its accuracy.
5. Build the analyzer to integrate it into your applications.

## Build a schema
Here's an example of building an analyzer to extract key data from an invoice document. 

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

:::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of upload step in user experience.":::

2. Content Understanding suggests analyzer templates based on your content type. For this example, select "Document analysis" to build your own schema tailored to the invoice scenario, then click "Create". When using your own data, select the analyzer template that best fits your needs, or create your own. See Analyzer templates for a full list of available templates.

:::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

3. Add fields to your schema:
   - Specify clear and simple field names.  - Example fields: "vendorname," "items," "price." 
   - Indicate the value type for each field (e.g., strings, dates, numbers, lists, groups). Learn more about [supported field types]().
   - *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.
   - *[Optional]* Specify the method to generate the value for each field. Learn more about [generation methods]().
   
4. Click "Save".
:::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

5. Content Understanding generates the output based on your schema. Test the analyzer's accuracy on additional data or make changes to the schema if needed.
:::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

6. Once you are satisfied with the quality, click "Build analyzer". This action will create an analyzer that you can integrate into your applications. You will receive an analyzer ID, which you can use to call this analyzer from your code.

:::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

## Analyzer templates 
Analyzer templates give you a head start by allowing you to build your analyzer without creating schemas from scratch.  They are fully customizable, allowing you to adjust any fields in the schemas to better fit your needs. 

The analyzer templates below are available for use in the [Azure AI Foundry Content Understanding experience]().

### Document analyzer templates

Below are some of our document analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Document analysis |Analyze documents to extract text, layout, structured fields, and more.| [Code sample]() |
|Text analysis |Analyze texts to extract structured fields.| [Code sample]() |

:::image type="content" source="../media/analyzer-template/image_doc_templates.png" alt-text="Screenshot of document analyzer template.":::

### Image analyzer templates
Below are some of our image analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Image analysis |Analyze images to extract structured fields.| [Code sample]() |
|Retail inventory management |Retail inventory management for monitoring of products on shelves.| [Code sample]() |
|Defect detection |Identify potential defects in provided images of metal plates.| [Code sample]() |

:::image type="content" source="../media/analyzer-template/image_doc_templates.png" alt-text="Screenshot of image analyzer template.":::

### Audio analyzer templates
Below are some of our audio analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Audio transcription |Transcribe audio recordings.| [Code sample]() |
|Conversation summarization |Transcribe conversations and extract summaries.| [Code sample]() |
|Post call analytics |Analyze call center conversations to extract transcripts, summaries, sentiment, and more.| [Code sample]() |


:::image type="content" source="../media/analyzer-template/audio_templates.png" alt-text="Screenshot of audio analyzer template.":::

### Video analyzer templates
Below are some of our video analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Video shot analysis |Analyze videos to extract transcript and structured fields for each shot.| [Code sample]() |
|Media asset management |Extract structured information from marketing videos, news content, broadcast media, television episodes, and film archives.| [Code sample]() |
|Advertising |Advertising analysis and moderation.| [Code sample]() |


:::image type="content" source="../media/analyzer-template/video_templates.png" alt-text="Screenshot of video analyzer template.":::

## Next steps
* In this quickstart, you learned how to create an analyzer in AI Foundry. To call our REST APIs, try our [API quickstart](use-rest-api.md).
* Explore more analyzer templates in our [GitHub repository]().
