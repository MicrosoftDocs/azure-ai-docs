---
title: "Use Azure AI Content Understanding Analyzer templates in the Azure AI Foundry"
titleSuffix: Azure AI services
description: Learn how to use Content Understanding Analyzer templates in Azure AI Foundry portal
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: quickstart
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# Use Content Understanding in the Azure AI Foundry
[The Azure AI Foundry](https://ai.azure.com/) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. This guide shows you how to use Content Understanding to build an analyzer, which is a tool that allows you to extract exactly the insights that you need from your data, no matter the type. Content Understanding analyzers can be created by building your own schema from scratch or by using a suggested analyzer template which is offered to address common scenarios across each data type.

  :::image type="content" source="../media/quickstarts/ai-foundry-overview.png" alt-text="Screenshot of the Content Understanding workflow in the Azure AI Foundry.":::

## Create a Content Understanding project in the AI Foundry

In order to try out [the Content Understanding service in the AI Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding), you have to create a Content Understanding project. You can also access Content Understanding from:

* The AI Foundry home page
   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of the AI Foundry home page.":::

* The AI Services landing page
   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of the AI Services landing page in AI Foundry.":::


Once on the Content Understanding page, select `Create a new Content Understanding Project`, shown below:

   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of Content Understanding page.":::

There are a few requirements to creating a project, including the following:

* An Azure AI Hub with an AI Services multi-service resource connected

[NOTE] Your AI Hub must be in the following supported regions: westus, swedencentral, australiaeast
* An Azure blob storage account (by default it will create a new one for you)

Once you complete the setup steps, select `Create project`.

## Steps to create a Content Understanding analyzer

Azure AI Foundry portal enables you to build a Content Understanding analyzer tailored to your specific needs. An analyzer can extract data from your content based on your scenario.

Follow these steps to create your own analyzer:

1. **Upload a sample data file:** Upload a data file that is representative of the data you are interested in extracting insights from. This allows the model to classify your data and recommend relevant scenario templates that may fit your needs, such as call-center analytics or video shot extraction.

1. **Select an analyzer template or build your own schema from scratch:** Once the service recommends templates, you have the option of selecting one that fits your needs or building one from scratch.

1. **Customize the schema to fit your specific scenario:** Make any necessary changes or build your schema from scratch to include exactly the fields that your scenario requires. An example field might be "Summarize the video, highlighting the backgrounds and vehicles that are present in each scene." 

1. **Test the analyzer on your data and validate its accuracy:** Try out the schema on your data file, or add additional data to test the performance.

1. **Build the analyzer to integrate it into your applications:** A built analyzer can be consumed in your own application, applying the schema that you just created. 

## Analyzer templates offered with Content Understanding

Content Understanding analyzer templates give you a head start by allowing you to build your analyzer without creating schemas from scratch. They're fully customizable, allowing you to adjust any fields in the schemas to better fit your needs. Learn more about the analyzer templates offered for each modality by viewing the tabs below.

The following analyzer templates are available for use in the [Azure AI Foundry Content Understanding experience](https://ai.azure.com/).

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


## Build your first analyzer

The following is an example of how to build a schema, which is the customziable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document:

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

[Add a note about the data types supported]

   :::image type="content" source="../media/analyzer-template/define-schema-upload.png" alt-text="Screenshot of upload step in user experience.":::

1. Next, the Content Understanding service will suggest analyzer templates based on your content type. For this example, select **Document analysis** to build your own schema tailored to the invoice scenario. When using your own data, select the analyzer template that best fits your needs, or create your own. See [Analyzer templates](#analyzer-templates) for a full list of available templates.

1. Select **Create**.

   :::image type="content" source="../media/analyzer-template/define-schema-template-selection.png" alt-text="Screenshot of analyzer templates.":::

1. Add fields to your schema:

    * Specify clear and simple field names. Some example fields might include **vendorName**, **items**, **price**.

    * Indicate the value type for each field (strings, dates, numbers, lists, groups). To learn more, *see* [supported field types](../service-limits.md#field-type-limits).

    * *[Optional]* Provide field descriptions to explain the desired behavior, including any exceptions or rules.

    * *[Optional]* Specify the method to generate the value for each field.

1. Select **Save**.

   :::image type="content" source="../media/analyzer-template/define-schema.png" alt-text="Screenshot of completed schema.":::

1. With the completed schema, Content Understanding now generates the output on your sample data. At this step, you can add additional data to test the analyzer's accuracy or make changes to the schema if needed.

   :::image type="content" source="../media/analyzer-template/test-analyzer.png" alt-text="Screenshot of schema testing step.":::

1. Once you're satisfied with the quality of your output, select **Build analyzer**. This action creates an analyzer ID that you can integrate into your own applications, allowing you to call the analyzer from your code.

   :::image type="content" source="../media/analyzer-template/build-analyzer.png" alt-text="Screenshot of built analyzer.":::

Now you've successfully built your first Content Understanding analyzer, and are ready to start extracting insights from your data.

## Next steps

 * In this quickstart, you learned how to create a Content Understanding analyzer using the Azure AI Foundry. To use the Content Understanding [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true), see the [REST API quickstart](use-rest-api.md).

