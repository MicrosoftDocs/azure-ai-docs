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

# Use Content Understanding analyzer templates in Azure AI Foundry
[Azure AI Foundry](https://ai.azure.com/) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. This guide will show you how to use Content Understanding to build an analyzer, either by creating your own schema from scratch or by using a suggested analyzer template.

## Steps to create a Content Understanding analyzer

Azure AI Foundry allows you to create a Content Understanding analyzer tailored to your specific needs. An analyzer can extract data from your content based on your scenario.

Follow these steps to create your own analyzer:

1. Upload a sample data file.
2. Choose an analyzer template or create your own schema from scratch.
3. Customize the schema to match your specific scenario.
4. Test the analyzer with your data to ensure its accuracy.
5. Build the analyzer and integrate it into your applications.

## Build a schema
Here's an example of building a schema to extract key data from an invoice document. 

1. Upload a sample video file of a soccer game or any other data relevant to your scenario.
![Image of step 1 in defining schema]()

2. Content Understanding suggests analyzer templates based on your content type. For this example, select "Start from scratch" to build a schema tailored to the soccer game scenario, then click "Create".
![Image of selecting "start from scratch" in defining schema]()

3. Add fields to your schema:
   - Specify clear and simple field names.  - Example fields: "vendorname," "items," "price." 
   - Indicate the value type for each field (e.g., strings, dates, numbers, lists, groups). Learn more about [supported field types]().
   - *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.
   - *[Optional]* Specify the method to generate the value for each field. Learn more about [generation methods]().

   
4. Click "Save".
![Image of creating the custom schema]()

5. Content Understanding generates the output based on your schema. Test the analyzer's accuracy on additional data or make changes to the schema if needed.
![Image of testing schema]()

6. Once you are satisfied with the quality, click "Build analyzer". This action will create an analyzer that you can integrate into your applications. You will receive an analyzer ID, which you can use to call this analyzer from your code.
![Image of built analyzer]()

## Analyzer templates 
Analyzer templates give you a head start by allowing you to build your analyzer without creating schemas from scratch.  They are fully customizable, allowing you to adjust any fields in the schemas to better fit your needs. 

The analyzer templates below are available for use in the [Azure AI Foundry Content Understanding experience]().

### Document analyzer templates

Below are some of our document analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Document analysis |Analyze documents to extract text, layout, structured fields, and more.| [Code sample]() |
|Text analysis |Analyze texts to extract structured fields.| [Code sample]() |

:::image type="content" source="../media/analyzertemplate/image_doc_templates.png" alt-text="Screenshot of document analyzer template.":::

### Image analyzer templates
Below are some of our image analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Image analysis |Analyze images to extract structured fields.| [Code sample]() |
|Retail inventory management |Retail inventory management for monitoring of products on shelves.| [Code sample]() |
|Defect detection |Identify potential defects in provided images of metal plates.| [Code sample]() |

:::image type="content" source="../media/analyzertemplate/image_doc_templates.png" alt-text="Screenshot of image analyzer template.":::

### Audio analyzer templates
Below are some of our audio analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Audio transcription |Transcribe audio recordings.| [Code sample]() |
|Conversation summarization |Transcribe conversations and extract summaries.| [Code sample]() |
|Post call analytics |Analyze call center conversations to extract transcripts, summaries, sentiment, and more.| [Code sample]() |


:::image type="content" source="../media/analyzertemplate/audio_templates.png" alt-text="Screenshot of audio analyzer template.":::

### Video analyzer templates
Below are some of our video analyzer templates.

|Template| Description| Code sample |
| ----|----|----|
|Video shot analysis |Analyze videos to extract transcript and structured fields for each shot.| [Code sample]() |
|Media asset management |Extract structured information from marketing videos, news content, broadcast media, television episodes, and film archives.| [Code sample]() |
|Advertising |Advertising analysis and moderation.| [Code sample]() |


:::image type="content" source="../media/analyzertemplate/video_templates.png" alt-text="Screenshot of video analyzer template.":::

## Next steps
* In this quickstart, you learned how to create an analyzer in AI Foundry. To call our REST APIs, try our [API quickstart](use-rest-api.md).
* Explore more analyzer templates in our [GitHub repository]().
