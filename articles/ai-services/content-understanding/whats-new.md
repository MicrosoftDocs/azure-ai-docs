---
title: What's new in Content Understanding?
titleSuffix: Azure AI services
description: Learn the latest updates to the Content Understanding API.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 11/01/2025
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.custom:
  - references_regions
  - build-2025
---

# What's new in Azure AI Content Understanding?

Azure AI Content Understanding service is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

## November 2025

Azure AI Content Understanding is now Generally Available with API version `2025-11-01`. The release brings production readiness plus customer-driven enhancements across model choice, management, and security.

### Choose the right generative model for every workload

- Connect Content Understanding to an Azure AI Foundry deployment for large language models and embeddings so you control quality, latency, and cost.
- Initial support includes GPT-4.1, GPT-4o family models, and embeddings such as `text-embedding-3-large`. Learn how to [configure your LLM deployment](quickstart/use-ai-foundry.md).
- Select a deployment type—Global, DataZone, or Regional—or use Provisioned Throughput Units (PTUs) to reserve capacity for predictable, high-volume workloads. For Global and DataZone, data at rest remains in your customer-designated geography; only the processing location differs.

### Manage analyzers with more precision

- **Optimize performance and reduce costs** with granular control over field extraction. Enable confidence scores and source grounding only for the fields where you need validation and traceability using the `estimateFieldSourceAndConfidence` setting. This selective approach reduces response payload sizes and lowers processing costs by computing confidence metrics only when required. Confidence scores are now consistently available across all extraction methods—whether using extract, generative, or classify—giving you uniform quality metrics regardless of how fields are processed. Learn how to [enable confidence scores for field extraction](document/overview.md#field-extraction).
- **Simplify analyzer development** with intelligent defaults and streamlined workflows. The extraction method is now optional. Content Understanding automatically selects the best approach for each field, reducing configuration complexity. This intelligent behavior makes it easier to build and maintain analyzers without deep knowledge of extraction techniques.
- **Categorization expands support** with `categorization` property now supports up to 200 categories up from 50, enabling precise classification and routing of diverse document types within a single analyzer—no separate classifier required. 
- **Analyzer lifecycle APIs** extend to support copy, delete, replace, and explicit result deletion give you complete control over analyzer versions and data retention for compliance and privacy requirements. See [Migrate projects from preview to GA](how-to/migration-preview-to-ga.md) for guidance.

### RAG analyzers

RAG analyzers are optimized for retrieval-augmented generation scenarios, extracting content with layout as markdown and performing semantic analysis to enhance retrieval quality for downstream applications.

- **Documents**: `prebuilt-documentAnalyzer` extracts paragraphs, tables, and figure descriptions from documents, enables textual descriptions of images, charts, and diagrams, captures hand-written annotations, generates content summaries, and supports a wide range of file formats including PDF, images, Office documents, and text files.
- **Multimodal support**: Extends to video, image, and audio with `prebuilt-videoAnalyzer` for transcript extraction and segment-based summaries with automatic scene detection, `prebuilt-imageAnalyzer` for visual content descriptions and insights, and `prebuilt-audioAnalyzer` for conversation transcription with speaker diarization and multilingual support.

Review the full analyzer catalog in [Prebuilt analyzers in Azure AI Content Understanding](concepts/prebuilt-analyzers.md).

### Domain-specific prebuilt analyzers for industry workloads

Domain-specific prebuilt analyzers are tailored for industry scenarios, enabling automated extraction of structured data from specialized document types without custom training.

- **Finance and tax**: Extract key data from financial statements, tax forms, W-2s, 1099s, and other tax documents with tuned schemas that capture amounts, dates, tax identifiers, and financial entities.
- **Procurement and contracts**: Process purchase orders, contracts, and procurement documents to extract vendor information, line items, pricing, terms, and contractual obligations.
- **Mortgage and lending**: Automate extraction from mortgage applications, loan documents, and lending forms, capturing borrower details, property information, loan terms, and financial disclosures.
- **Identity verification**: Process passports, driver's licenses, ID cards, and other identity documents with `prebuilt-idDocument`, extracting personal information, document numbers, and verification details. Categorization lets you send specific sections—such as passport pages—to purpose-built analyzers during a single run.
- **Utilities, billing, and more**: Extract structured data from utility bills, invoices, and billing statements across industries, capturing account information, usage details, and payment data.

Explore the domain-specific analyzer lineup and usage guidance in [Prebuilt analyzers in Azure AI Content Understanding](concepts/prebuilt-analyzers.md#vertical-analyzers).

### Enterprise security and governance

- General availability includes Microsoft Entra ID, managed identities, customer-managed keys, virtual networks, and private endpoints.
- These controls keep sensitive content in your Azure boundary and help you meet compliance requirements. Learn more in [Secure access to Content Understanding](concepts/managed-identities-entra-id.md).

### Other improvements

- `prebuilt-read` and `prebuilt-layout` analyzers now expose key Document Intelligence capabilities inside Content Understanding.
- `prebuilt-layoutWithFigures` extends layout extraction with figure detection and analysis, extracting charts, diagrams, and images with their context.
- Review the full analyzer catalog in [Prebuilt analyzers in Azure AI Content Understanding](concepts/prebuilt-analyzers.md).
- Use the `range` parameter to analyze specific pages or segments and reduce token consumption.
- Choose HTML or Markdown table output to match downstream processing requirements.
- Categorization lets you send sections—such as passport pages within `prebuilt-idDocument`—to purpose-built analyzers during a single run.

### Region expansion and availability

- Content Understanding is now supported in 14 regions worldwide, providing greater geographic coverage and improved data residency options. See the [language and region support documentation](language-region-support.md) for the detailed list of available regions.
- Content Understanding is available in both [Azure AI Foundry portal](https://ai.azure.com) (coming soon) for integrated AI workflows and Content Understanding Studio for more advanced scenarios, as well as through the REST API for programmatic access.

### Breaking changes

- Managed capacity for the preview generative models is retired. Now to use Content Understand you always bring your own Foundry large language model and embedding deployments.
- Dedicated classifier APIs are deprecated because classification now lives inside the analyzer API as the categorization feature.
- Video segmentation can now be done using the categorization capability unifying the API for splitting files across document and video analyzers.
- The preview API (`2025-05-01-preview`) doesn't carry forward Pro mode for cross-file analysis or the person directory with Face API integration.

## October 2025
Azure AI Content Understanding preview version introduces the following updates:

* Azure AI Content Understanding now has increased field count support (1,000) for all modalities.
* The API response body now inclues input, output, and contextualization tokens consumed as part of the tokens object. Check out the quickstart article for more information.

## May 2025

The Azure AI Content Understanding [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) REST API is now available. This update introduces the following updates and enhanced capabilities:

### Processing modes

With the [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) release, we introduce two modes: `standard` and `pro`. The default mode for all analyzers is `standard`.

Content Understanding pro mode adds reasoning, support for multiple input documents, the ability to configure an external knowledge base for linking, enrichment, and validation. These features automate complex tasks by extending field extraction capabilities to cover scenarios that previously required custom code or human effort.

The `pro` mode is currently limited to documents as inputs, with support other types of content types coming soon! Common challenges that the pro mode addresses are aggregating a schema across content from different input files, validating results across documents, and using external knowledge to generate an output schema. Learn more about the [pro mode](concepts/standard-pro-modes.md).

### AI Foundry experience

With this release, the following updates are now available to the Content Understanding experience in Azure AI Foundry:

* Added support for creating both `standard` mode and `pro` mode tasks in the existing Content Understanding experience. Now with pro mode, you have the ability to bring in your own reference data and create a task that executes multi-step reasoning on your data. Read more about the two different task types in [Use Azure AI Content Understanding in the Azure AI Foundry](./quickstart/use-ai-foundry.md).
* Try-out experiences are now available for general document analysis and invoice analysis. Try out these prebuilt features on your own data and start getting insights without having to create a custom task. 

### Document classification and splitting

This release introduces a new [classification API](concepts/classifier.md). This API supports classifying and logically splitting a single file containing multiple documents with optional routing to field extraction analyzers. You can create a custom classifier to split and classify a file into multiple logical documents and route the individual documents to a downstream field extraction model in a single API call.

### Improvements to document processing

* Added support for extracting table spanning multiple pages as a single logical table. Learn more about [structure extraction updates in documents](document/elements.md).
* Selection mark support for checkmark and radio buttons as unicode characters. Learn more about [structure extraction updates in documents](document/elements.md).
* Barcode extraction as part of the default content extraction along with `OCR`. Learn more about [structure extraction updates in documents](document/elements.md).
* Confidence score improvements with better grounding results for extractive fields.
* New file format support extended for following document types: `docx`, `xslx`, `pptx`, `msg`, `eml`, `rtf`, `html`, `md`, and `xml`.

### Improvements to video processing

* Added support for whole video fields. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
* Added support for video chapters via segmentation. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
* Added support for face identification on extracted face thumbnails. The identity enhances the description and downstream tasks like search and retrieval. Learn more about [face detection in videos](video/overview.md#content-extraction---grouping-and-identification)
* Added support for disabling face blurring in analyzer configuration. Learn more about [video processing improvements](video/overview.md#field-extraction--face-description).

* ### Improvements to audio processing

* Added additional locales for audio transcription. Learn more about [audio capabilities](audio/overview.md).
* Added support for multilingual audio processing. Learn more about [language handling improvements in audio](audio/overview.md#language-handling).
* Increased maximum supported file-size to ≤ 1 GB and length of ≤ 4 hours. Learn more about [audio service limits](service-limits.md).

### Face API

This release adds new face detection and recognition capabilities to Content Understanding. You can create a directory of faces and persons. The directory can be used to recognize the faces in the processed content. Learn more about [detecting and recognizing faces](face/overview.md).


## April 2025

**2024-12-01-preview** REST API introduces the following updates and enhanced capabilities:

* **General improvements**. For all modality, to request an increase from current limits, contact us at `cu_contact@microsoft.com`.
* **Prebuilt invoice template**. The invoice template is now customizable. Once you select the invoice template, you can access a predefined list of fields that can be tailored to your specific needs by adding or removing fields.
* **Generative and classification fields**
  * Both generative and classify fields are now supported for documents modality.
  * You can now utilize the REST endpoint/Studio to define generative and classification fields with zero-shot outputs for documents. This feature enables you to generate summaries, infer results, and classify individual documents across multiple files.
  * Multiple analyzers can be invoked to process individual files.
* **Video modality**
  * Latency improvement for video processing resulting in 50% lower latency.
  * Expanded output types to add support for `Object` and `Arrays`
  * Added support for video files provided via S3 presigned URL ingestion
  * Improved video segmentation to semantically segment especially when no shot edits exist in the video
* **Audio modality**
  * API now supports the field type: `group`.
* **Text modality**
  * API support for the field type: `group`.
* **User experience improvements**
  * Added functionality to download and upload schema configurations during schema definition.
  * Enhanced file labeling and analyzer building processes.
  * Add download code samples for quick setup added.

## November 2024

Welcome! The Azure AI Content Understanding API version `2024-12-01-preview` is now in public preview. This version allows you to generate a structured representation of content tailored to specific tasks from various modalities or formats. Content Understanding uses a defined schema to extract content suitable for processing by large language models and subsequent applications.
