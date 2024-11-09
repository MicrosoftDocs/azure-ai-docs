---
title: What is Azure AI Content Understanding?
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---

# What is Azure AI Content Understanding?

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding is a new Generative AI based [**Azure AI Service**](../what-are-ai-services.md), designed to process/ingest content of any types (documents, images, videos, and audio) into a user-defined output format.

Content Understanding offers a streamlined process to reason over large amounts of unstructured data, accelerating time-to-value by generating an output that can be integrated into automation and analytical workflows.

:::image type="content" source="media/overview/cu-overview.png" alt-text="Screenshot of Content Understanding overview.":::

## Why process with Content Understanding?

* **Simplify and streamline workflows**. Content Understanding standardizes the extraction of content, structure, and insights from various content types into a unified process.

* **Simplify field extraction**. Content Understanding's field extraction makes it easier to generate structured output from unstructured content. Define a schema to extract, classify, or generate field values with no complex prompt engineering

* **Enhance accuracy**. Content Understanding employs multiple AI models to analyze and cross-validate information simultaneously, resulting in more accurate and reliable results.

## Content Understanding use cases

* **Automation**. Content Understanding supports automation scenarios by converting unstructured content into structured data, which can be integrated into various workflows and applications. Confidence scores minimize human review and lower costs. For example, automate procurement and payment processes by extracting fields from invoices.

* **Search and retrieval augmented generation (RAG)**. Content Understanding enables ingestion of content of any modality into the search index. The structured output representation improves the relevance for RAG scenarios.

* **Analytics and reporting**: Content Understanding's extracted field outputs enhance analytics and reporting, allowing businesses to gain valuable insights, conduct deeper analysis, and make informed decisions based on accurate reports.

## Applications
Common applications for Content Understanding include:

|Application|Description|Quickstart|
|:---------|:----------|:----------|
|Post-call analytics| Businesses and call centers can generate insights from call recordings to track key KPIs, improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.| [**Post-call analytics quickstart**](quickstart/use-ai-foundry.md) |
|Media asset management| Software and media vendors can use Content Understanding to extract richer, targeted information from videos for media asset management solutions.| [**Media asset management quickstart**](quickstart/use-ai-foundry.md) |
|Tax automation| Tax preparation companies can use Content Understanding to generate a unified view of information from various documents and create comprehensive tax returns.| [**Tax automation quickstart**](quickstart/use-ai-foundry.md) | 
|Chart understanding| Businesses can enhance chart understanding by automating the analysis and interpretation of various types of charts and diagrams using Content Understanding.| [**Chart understanding quickstart**](quickstart/use-ai-foundry.md) |

See [Quickstart](quickstart/use-ai-foundry.md) for more examples.

## Capabilities

:::image type="content" source="media/overview/component_overview.png" alt-text="Screenshot of Content Understanding components.":::

|Capability|Description|
|:---------|:----------|
|Content extraction | Content Understanding recognizes content from documents, images, audio, and video for easy analysis and further processing.|
|Add-ons| Content Understanding add-ons enhance content extraction by incorporating additional elements like barcodes, tables, and detected faces.|
|Field extraction|Choose from a list of supported field types like strings, numbers and tables. See [service limits](service-limits.md) for a complete list of field types supported. Fields can be generated via one of the following methods:</br></br>&bullet; **Extract**: Directly extract values as they appear in the input content, such as extracting dates from receipts or item details from invoices.</br></br>&bullet; **Classify**: Classify content from a predefined set of categories, such as determining call sentiment or chart type.</br></br>&bullet; **Generate**: Generate values freely from input data, such as summarizing an audio conversation or generating scene descriptions from videos.|
|Grounding Source| Content Understanding identifies the specific regions in the content where the value was generated from. This allows users in automation scenarios to quickly verify the correctness of the field values, leading to higher confidence in the extracted data. |
|Confidence Score | Content Understanding provides confidence scores from 0 to 1 to estimate the reliability of the results. High scores indicate accurate data extraction, enabling straight-through processing in automation workflows.|


## Responsible AI
 Azure AI Content Understanding is designed to guard against processing harmful content. For more information, *see* our [**Transparency Note**]() and our [**Code of Conduct**](/legal/cognitive-services/openai/code-of-conduct).

## Data privacy and security
Developers using the Content Understanding service should review Microsoft's policies on customer data. For more information, visit our [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page.

> [!IMPORTANT]
> If you are using Microsoft products or services to process Biometric Data, you are responsible for: (i) providing notice to data subjects, including with respect to retention periods and destruction; (ii) obtaining consent from data subjects; and (iii) deleting the Biometric Data, all as appropriate and required under applicable Data Protection Requirements. "Biometric Data" will have the meaning set forth in Article 4 of the GDPR and, if applicable, equivalent terms in other data protection requirements. For related information, see [Data and Privacy for Face](/legal/cognitive-services/face/data-privacy-security).

## Getting started
Our quickstart guides help you quickly start using the Content Understanding service:

* [**Azure AI Foundry Quickstart**](quickstart/use-ai-foundry.md)
* [**Rest API Quickstart**](quickstart/use-rest-api.md)





