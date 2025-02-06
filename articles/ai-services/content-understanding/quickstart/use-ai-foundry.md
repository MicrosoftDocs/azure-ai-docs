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
[The Azure AI Foundry](https://ai.azure.com/) is a comprehensive platform for developing and deploying generative AI applications and APIs responsibly. Azure AI Content Understanding is a new generative AI-based [Azure AI Service](../../what-are-ai-services.md) that analyzes files of any modality (documents, images, videos, and audio) and extracts structured output in user-defined field formats. This guide shows you how to use Content Understanding to build an analyzer, which is a tool that allows you to extract exactly the insights that you need from your data, no matter the type. Content Understanding analyzers are fully customizable, and can be created by building your own schema from scratch or by using a suggested analyzer template which is offered to address common scenarios across each data type.

  :::image type="content" source="../media/quickstarts/ai-foundry-overview.png" alt-text="Screenshot of the Content Understanding workflow in the Azure AI Foundry.":::

## Prerequisites

To get started, make sure you have the following:

* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free/) before you begin.

* You need permissions to create an Azure AI Foundry hub or have one created for you.

  * If your role is **Contributor** or **Owner**, you can proceed with creating your own hub.

  * If your role is **Azure AI Developer**, the hub must already be created before you can complete this quickstart. Your user role must be **Azure AI Developer**, **Contributor**, or **Owner** on the hub. For more information, see [hubs](../../../ai-studio/concepts/ai-resources.md) and [Azure AI roles](../../../ai-studio/concepts/rbac-ai-studio.md).

 > [!NOTE] Your AI Hub must be in one of the following supported regions: westus, swedencentral, australiaeast

 >[!IMPORTANT] If your organization requires you to customize the security or storage resources, the AI Foundry currently does not support resource creation that meets these standards. Please refer to [Azure AI services API access keys](../../../ai-studio/concepts/ai-resources.md#azure-ai-services-api-access-keys) to create resources that meet your organizations requirements through the Azure portal. Policy enforced in Azure on the hub scope applies to all projects managed under it.

## Create your first Content Understanding project in the AI Foundry

In order to try out [the Content Understanding service in the AI Foundry](https://ai.azure.com/explore/aiservices/vision/contentunderstanding), you have to create a Content Understanding project. You can access Content Understanding from:

* The [AI Foundry home page](https://ai.azure.com/https://ai.azure.com/explore/aiservices)
   :::image type="content" source="../media/quickstarts/foundry-home-page.png" alt-text="Screenshot of the AI Foundry home page.":::

* The [AI Services landing page]()
   :::image type="content" source="../media/quickstarts/cu-ai-services-landing-page.png" alt-text="Screenshot of the AI Services landing page in AI Foundry.":::

Once on the Content Understanding page, select `Create a new Content Understanding Project`, shown below:

   :::image type="content" source="../media/quickstarts/cu-landing-page.png" alt-text="Screenshot of Content Understanding page.":::

 > [!NOTE] The Content Understanding project type is separate from the Generative AI project type, also available in the AI Foundry.

Follow the steps in the project creation wizard, and start by selecting the Hub that you already created. When the hub was created, it should have provisioned an AI Services resource, as well as a blob storage container, and these will be selected by default. You can alternatively create one using the wizard.

 >[!IMPORTANT] If your organization requires you to customize the security or storage resources, the AI Foundry currently does not support resource creation that meets these standards. Please refer to [Azure AI services API access keys](../../../ai-studio/concepts/ai-resources.md#azure-ai-services-api-access-keys) to create resources that meet your organizations requirements through the Azure portal. Policy enforced in Azure on the hub scope applies to all projects managed under it.

 Once you complete the setup steps, select `Create project`.

 ## Sharing your content understanding project

In order to share and manage access to the Content Understanding project you just created, navigate to the Management Center, found at the bottom of the navigation for your project:

  :::image type="content" source="../media/quickstarts/cu-find-management-center.png" alt-text="Screenshot of where to find management center.":::


You can manage the users and their individual roles here:

   :::image type="content" source="../media/quickstarts/cu-management-center.png" alt-text="Screenshot of "Project users" section of management center.":::

## Build your first analyzer

Now that everything is configured to get started, the following is a setep-by-step walkthrough of how to build your first analyzer, starting with building the schema. The schema is the customziable framework that allows the analyzer to extract insights from your data. In this example, the schema is created to extract key data from an invoice document, but you can bring in any type of data and the steps to follow will remain the same. For a complete list of supported file types, see [input file limits](../service-limits.md#input-file-limits).

1. Upload a sample file of an invoice document or any other data relevant to your scenario.

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

## Next steps

 * In this quickstart, you learned how to create a Content Understanding analyzer using the Azure AI Foundry. To use the Content Understanding [REST API](/rest/api/contentunderstanding/operation-groups?view=rest-contentunderstanding-2024-12-01-preview&preserve-view=true), see the [REST API quickstart](use-rest-api.md).

