---
title: What is Azure AI Content Understanding?
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding solutions, processes, workflows, use-cases, and field extractions.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 06/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - ignite-2024-understanding-release
  - build-2025
# customer intent: As a user, I want to learn more about Content Understanding solutions.
---

# What is Azure AI Content Understanding (preview)?

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding is a new Generative AI based [**Azure AI Service**](../what-are-ai-services.md), designed to process/ingest content of any types (documents, images, videos, and audio) into a user-defined output format.

Content Understanding offers a streamlined process to reason over large amounts of unstructured data, accelerating time-to-value by generating an output that can be integrated into automation and analytical workflows.

:::image type="content" source="media/overview/component-overview-updated.png" alt-text="Screenshot of Content Understanding overview, process, and workflow." lightbox="media/overview/component-overview-updated.png" :::

## Why process with Content Understanding?

* **Simplify and streamline workflows**. Azure AI Content Understanding standardizes the extraction and classification of content, structure, and insights from various content types into a unified process.

* **Simplify field extraction**. Content Understanding's field extraction makes it easier to generate structured output from unstructured content. Define a schema to extract, classify, or generate field values with no complex prompt engineering

* **Enhance accuracy**. Content Understanding employs multiple AI models to analyze and cross-validate information simultaneously, resulting in more accurate and reliable results.

* **Confidence scores & grounding**. Content Understanding ensures the accuracy of extracted values while minimizing the cost of human review.

## Content Understanding use cases

* **Automation**. Content Understanding supports automation scenarios by converting unstructured content into structured data, which can be integrated into various workflows and applications. Confidence scores minimize human review and lower costs. For example, automate procurement and payment processes by extracting fields from invoices.

* **Search and retrieval-augmented generation (RAG)**. Content Understanding enables ingestion of content of any modality into the search index. The structured output representation improves the relevance for RAG scenarios.

* **Analytics and reporting**: Content Understanding's extracted field outputs enhance analytics and reporting, allowing businesses to gain valuable insights, conduct deeper analysis, and make informed decisions based on accurate reports.

* **Optimize workflow through classification**: Content Understanding's classification feature enables you to categorize the documents first, before routing it to the associated analyzer for extraction.

## Applications

Common applications for Content Understanding include:

|Application|Description|
|:---------|:----------|
|Post-call analytics| Businesses and call centers can generate insights from call recordings to track key KPIs, improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.|
|Media asset management| Software and media vendors can use Content Understanding to extract richer, targeted information from videos for media asset management solutions.|
|Tax automation| Tax preparation companies can use Content Understanding to generate a unified view of information from various documents and create comprehensive tax returns.|
|Chart understanding| Businesses can enhance chart understanding by automating the analysis and interpretation of various types of charts and diagrams using Content Understanding.|
|Mortgage application processing|Analyze supplementary supporting documentation and mortgage applications to determine whether a prospective home buyer provided all the necessary documentation to secure a mortgage.|
|Invoice contract verification|Review invoices and contractual agreements with clients carefully. Apply a multi-step reasoning process to analyze the data. Ensure that conclusions, such as validating the consistency between the invoice and the contract, are accurate and thorough.|

## Components

:::image type="content" source="media/overview/pro-components.png" lightbox="media/overview/pro-components.png"alt-text="Screenshot of Content Understanding pro components.":::

|Component|Description|
|:---------|:----------|
|Analyzer|The analyzer is the core component of Content Understanding. It allows customers to configure content extraction settings and field extraction schema. Once configured, the analyzer consistently applies these settings to process all incoming data.|
|Content extraction|With content extraction, you specify the types of information to identify and extract from incoming content. You can target text (such as optical character recognition (OCR) results), selection marks, barcodes, formulas, and layout elements like paragraphs, sections, and tables. This approach lets you focus on extracting the most relevant information for your needs.|
|Field extraction|Field extraction allows users to define the structure and schema of the desired fields to extract from input files. See [service limits](service-limits.md) for a complete list of field types supported. Fields can be generated via one of the following methods:</br></br> &bullet; **Extract**: Directly extract values as they appear in the input content, such as dates from receipts or item details from invoices.</br></br>&bullet; **Classify**: Classify content from a predefined set of categories, such as call sentiment or chart type.</br></br>&bullet; **Generate**: Generate values freely from input data, such as summarizing an audio conversation or creating scene descriptions from videos.|
|Grounding source| Content Understanding identifies the specific regions in the content where the value was generated from. Source grounding allows users in automation scenarios to quickly verify the correctness of the field values, leading to higher confidence in the extracted data. |
|Confidence score | Content Understanding provides confidence scores from 0 to 1 to estimate the reliability of the results. High scores indicate accurate data extraction, enabling straight-through processing in automation workflows.|

## Responsible AI

 Azure AI Content Understanding is designed to guard against processing harmful content, such as graphic violence and gore, hateful speech and bullying, exploitation, abuse, and more. For more information and a full list of prohibited content, *see* our [**Transparency note**](/legal/cognitive-services/content-understanding/transparency-note?toc=/azure/ai-services/content-understanding/toc.json&bc=/azure/ai-services/content-understanding/breadcrumb/toc.json) and our [**Code of Conduct**](https://aka.ms/AI-CoC).

### Modified content filtering

Content Understanding now supports modified content filtering for approved customers. The subscription IDs with approved modified content filtering impacts Content Understanding output. By default, Content Understanding employs a content filtering system that identifies specific risk categories for potentially harmful content in both submitted prompts and generated outputs. Modified content filtering allows the system to annotate rather than block potentially harmful output, giving you the ability to determine how to handle potentially harmful content. For more information on content filter types, *see* [Content filter types](../openai/concepts/content-filter.md#content-filter-types).

> [!IMPORTANT]
>
> * Apply for modified content filters via this form: [Azure OpenAI Limited Access Review: Modified Content Filters](https://ncv.microsoft.com/uEfCgnITdR).
> * For more information, *see* [**Content filtering**](../openai/concepts/content-filter.md).

## Face capabilities

The Face capabilities feature in Content Understanding is a limited Access service and registration is required for access. Face grouping and identification feature in Content Understanding is limited based on eligibility and usage criteria. Face service is only available to Microsoft managed customers and partners. Use the [Face Recognition intake form](https://aka.ms/facerecognition) to apply for access. For more information, see [Microsoft's Limited Access Policy](../../ai-services/cognitive-services-limited-access.md).


## Data privacy and security
Developers using the Content Understanding service should review Microsoft's policies on customer data. For more information, visit our [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page.

> [!IMPORTANT]
> If you're using Microsoft products or services to process Biometric Data, you're responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate, and required under applicable Data Protection Requirements. "Biometric Data" has the meaning articulated in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and privacy for Face](/legal/cognitive-services/face/data-privacy-security).

## Getting started

Our quickstart guides help you quickly start using the Content Understanding service:

* [**Azure AI Foundry portal Quickstart**](quickstart/use-ai-foundry.md)
* [**Rest API Quickstart**](quickstart/use-rest-api.md)

