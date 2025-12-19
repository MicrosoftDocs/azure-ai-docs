---
title: What is Azure Content Understanding in Foundry Tools?
titleSuffix: Foundry Tools
description: Learn about Azure Content Understanding in Foundry Tools solutions, processes, workflows, use-cases, and field extractions.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 12/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - ignite-2024-understanding-release
  - build-2025
# customer intent: As a user, I want to learn more about Content Understanding solutions.
---

# What is Azure Content Understanding in Foundry Tools?

> [!NOTE]
> Content Understanding is now a generally available (GA) service with the release of the `2025-11-01` API version. For details, see [What's New](whats-new.md).

Azure Content Understanding in Foundry Tools is an [**Foundry Tool**](../what-are-ai-services.md) that's available as part of the [Microsoft Foundry Resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal. It uses generative AI to process and ingest many types of content, including documents, images, videos, and audio, into a user-defined output format. Content Understanding offers a streamlined process to reason over large amounts of unstructured data, accelerating time-to-value by generating an output that you can integrate into automation and analytical workflows.

Content Understanding is now a generally available (GA) service with the release of the `2025-11-01` API version. It's now available in a broader range of [regions](language-region-support.md). For details on the updates in the GA release, see the Content Understanding [What's New](whats-new.md) page. 

:::image type="content" source="media/overview/content-understanding-framework-2025.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="media/overview/content-understanding-framework-2025.png" :::

## Why use Content Understanding?

Content Understanding accelerates time to value by enabling straight-through processing of unstructured data with confidence scores, minimizing manual review, and reducing operational costs. Key benefits include:

* **Simplify and streamline workflows**. Content Understanding standardizes the extraction and classification of content, structure, and insights from various content types into a unified process.

* **Simplify field extraction**. Content Understanding's field extraction makes it easier to generate structured output from unstructured content. Define a schema to extract, classify, or generate field values with no complex prompt engineering.

* **Enhance accuracy**. Content Understanding employs multiple AI models to analyze and cross-validate information simultaneously, resulting in more accurate and reliable results.

* **Confidence scores and grounding**. Content Understanding ensures the accuracy of extracted values while minimizing the cost of human review.

* **Classify content types**. Content Understanding enables you to classify your document types to streamline your ability to process content. This feature is now available in a unified approach in the Analyze API.

* **Industry-specific prebuilt analyzers**. Content Understanding includes prebuilt analyzers designed for industry-specific scenarios including tax preparation, procurement document processing, contract analysis, call center analytics, media analysis, and much more.

## Content Understanding use cases

* **Intelligent document processing (IDP)**. Content Understanding enables intelligent document processing by converting unstructured documents into structured data with high accuracy. Confidence scores and grounding capabilities ensure data quality while minimizing manual review and reducing operational costs. For example, automate invoice processing, contract analysis, and claims management by extracting and validating fields from complex documents.

* **Agentic applications**. Content Understanding turns messy, multimodal file inputs into predictable, standardized inputs. It delivers clean markdown representations for reasoning and knowledge workflows, ensuring clarity and context for downstream tasks. When structured data is required, it provides schema-aligned key-value fields with confidence scores and grounding, enabling agents to automate decisions with accuracy and auditability.

* **Search and retrieval-augmented generation (RAG)**. Content Understanding enables ingestion of content of any modality into a search index, with extensive support for figure description and analysis to make your data more accessible. The Content Understanding service offers multiple prebuilt analyzers that are fine-tuned to give you the best outputs for your RAG search scenarios.

* **Robotic process automation (RPA)**. Content Understanding integrates seamlessly with RPA workflows by providing structured data extracted from various content types. This capability enables end-to-end automation of business processes that require content understanding, such as order processing, customer onboarding, and regulatory compliance workflows.

* **Analytics and reporting**: Content Understanding's extracted field outputs enhance analytics and reporting, allowing businesses to gain valuable insights, conduct deeper analysis, and make informed decisions based on accurate reports.

* **Optimize workflow through classification**: Content Understanding's classification feature enables you to categorize the documents first, before routing it to the associated analyzer for extraction.

## Industry-specific applications

Some common industry-specific applications for Content Understanding include:

|Application|Description|
|:---------|:----------|
|Tax automation| Tax preparation companies can use Content Understanding to generate a unified view of information from various documents and create comprehensive tax returns.|
|Mortgage application processing|Analyze supplementary supporting documentation and mortgage applications to determine whether a prospective home buyer provided all the necessary documentation to secure a mortgage.|
|Invoice contract verification|Review invoices and contractual agreements with clients carefully. Apply a multi-step reasoning process to analyze the data. Ensure that conclusions, such as validating the consistency between the invoice and the contract, are accurate and thorough.|
|Retrieval-augmented generation (RAG) ingestion| Organizations can enhance their RAG workflows by extracting comprehensive information from documents that would otherwise be missed. Figure descriptions capture information from charts, diagrams, and visualizations, making them searchable. Layout analysis preserves document structure including tables, sections, and hierarchies. Annotation detection captures handwritten notes, underlines, and strikeouts.|
|Post-call analytics| Businesses and call centers can generate insights from call recordings to track key performance indicators (KPIs), improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.|
|Media asset management| Software and media vendors can use Content Understanding to extract richer, targeted information from videos for media asset management solutions.|
|Enhanced customer support| Businesses with support channels can utilize Content Understanding for RAG search to enhance the quality of responses based on data from prior customer issues and feedback.|


## Key components of Content Understanding

The Content Understanding framework processes unstructured content through multiple stages, transforming inputs into structured, actionable outputs. The following table describes each component from left to right as shown in the diagram:

:::image type="content" source="media/overview/content-understanding-framework-2025.png" alt-text="Diagram showing the Content Understanding framework with inputs flowing through analyzers to structured output." lightbox="media/overview/content-understanding-framework-2025.png" :::

|Component|Description|
|:---------|:----------|
|**Inputs** |The source content that Content Understanding processes. Supports multiple modalities including Documents, Images, Video, Audio. Learn more about [input file types](service-limits.md#input-file-limits).|
|**Analyzer**|The core component that defines how your content is processed. It configures content extraction settings, field extraction schema, and model deployments. Once configured, the analyzer consistently applies these settings to all incoming data. Content Understanding offers prebuilt analyzers for common scenarios and supports custom analyzers tailored to your needs. Learn more about [analyzers](concepts/analyzer-reference.md), [prebuilt analyzers](concepts/prebuilt-analyzers.md), and [custom analyzers](tutorial/create-custom-analyzer.md).|
|**Content extraction**|Transforms unstructured input into normalized, structured text and metadata. Extracts text using optical character recognition (OCR), identifies selection marks and barcodes, detects formulas, and recognizes layout elements like paragraphs, sections, and tables. For audio and video, transcribes speech and identifies key visual elements. Learn more about [content extraction](document/overview.md#content-extraction).|
|**Segmentation**|Divides documents or videos into logical sections for targeted processing. Configured using the `enableSegment` property in the analyzer schema. Enables breaking content into meaningful chunks, such as splitting a document by document type or dividing a video into scenes. Learn more about [segmentation and classification](concepts/classifier.md).|
|**Field extraction**|Generates structured key-value pairs based on your defined schema. See [service limits](service-limits.md) for supported field types. Fields can be generated via three methods:</br></br> &bullet; **Extract**: Directly extract values as they appear in the input content (supported for documents only), such as dates from receipts or item details from invoices.</br></br>&bullet; **Classify**: Classify content from a predefined set of categories, such as call sentiment or chart type, and route it to the correct analyzer for analysis.</br></br>&bullet; **Generate**: Generate values freely from input data, such as summarizing an audio conversation or creating scene descriptions from videos. </br></br>Learn more about [field extraction](document/overview.md#field-extraction).|
|**Confidence scores**|Provides reliability estimates from 0 to 1 for each extracted field value. High scores indicate accurate data extraction, enabling straight-through processing in automation workflows. Enabled using the `estimateFieldSourceAndConfidence` setting in document analyzers. Learn more about [confidence scores](document/overview.md#field-extraction).|
|**Grounding**|Identifies the specific regions in the content where each value was extracted or generated. Source grounding allows users in automation scenarios to quickly verify the correctness of field values by tracing them back to their origin in the source content. Enabled using the `estimateFieldSourceAndConfidence` setting in document analyzers. Learn more about [grounding](document/overview.md#field-extraction).|
|**Contextualization**|Content Understanding's processing layer that prepares context for generative models and post-processes their output. Includes output normalization and formatting, source grounding calculation, confidence score computation, and context engineering to optimize model usage. Learn more about [contextualization](pricing-explainer.md#contextualization-tokens).|
|**Foundry models**|The Foundry large language models (LLMs) and embeddings models that power generative capabilities. You bring your own deployments of supported generative models and text-embedding models for training examples. Content Understanding uses these models for field extraction, figure analysis, and other AI-powered features. Learn more about [models and deployments](concepts/models-deployments.md).|
|**Structured output** |The final result is supplied in your chosen format. Content can be output as Markdown for search and retrieval scenarios, or as structured JSON matching your defined schema for automation and analytics workflows.|

## Content Understanding experiences
Content Understanding is a Foundry service. To use Content Understanding, you must create a Foundry Azure Resource. Content Understanding Studio complements the Foundry experience for customers that need advanced capabilities. For a more detailed breakdown of each service, check out [Feature Comparison: Content Understanding in Foundry vs Content Understanding Studio](foundry-vs-content-understanding-studio.md).

* **Content Understanding in Foundry (new) portal (coming soon)**: The Foundry NextGen portal offers the ability to build advanced, comprehensive agentic workflows with the Content Understanding Tool.
* **Content Understanding Studio**: A complementary UX experience, Content Understanding Studio enables a smooth transition for customers transitioning from Document Intelligence. It offers an experience optimized for analyzer performance improvement including improving custom analyzers using data labeling techniques. It also supports building classification-based custom analyzers.

## Responsible AI

Content Understanding is designed to guard against processing harmful content, such as graphic violence and gore, hateful speech and bullying, exploitation, abuse, and more. The service leverages the standard Foundry infrastructure, including the Azure AI Content Safety, integrating content safety results into the Content Understanding output. For more information and a full list of prohibited content, see the [**Transparency note**](/azure/ai-foundry/responsible-ai/content-understanding/transparency-note) and the [**Code of Conduct**](https://aka.ms/AI-CoC).

### Modified content filtering

Content Understanding supports modified content filtering for approved customers. The subscription IDs (identifiers) with approved modified content filtering impact Content Understanding output. By default, Content Understanding employs a content filtering system that identifies specific risk categories for potentially harmful content in both submitted prompts and generated outputs. Modified content filtering allows the system to annotate rather than block potentially harmful output, giving you the ability to determine how to handle potentially harmful content. For more information on content filter types, see [Content filter types](../openai/concepts/content-filter.md#content-filter-types).

> [!IMPORTANT]
>
> * Apply for modified content filters by using this form: [Azure OpenAI Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR).
> * For more information, see [**Content filtering**](../../ai-foundry/openai/concepts/content-filter.md).

## Face capabilities

Content Understanding provides face description capabilities that can generate detailed textual descriptions of faces in video and image content. When enabled, the generative model describes facial attributes such as facial hair, facial expression, and can identify prominent people or celebrities. Learn more about [face description in video processing](video/overview.md#face-description-fields).


## Data privacy and security
Developers using the Content Understanding service should review Microsoft's policies on customer data. For more information, visit the [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page.

> [!IMPORTANT]
> If you're using Microsoft products or services to process Biometric Data, you're responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate, and required under applicable Data Protection Requirements. "Biometric Data" has the meaning articulated in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and privacy for Face](/azure/ai-foundry/responsible-ai/face/data-privacy-security).

## Get started

Our quickstart guides help you quickly start using the Content Understanding service:

* [**Microsoft Foundry portal Quickstart**](quickstart/use-ai-foundry.md)
* [**Content Understanding Studio quickstart**](quickstart/content-understanding-studio.md)
* [**Rest API Quickstart**](quickstart/use-rest-api.md)

