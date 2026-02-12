---
title: What's new in Content Understanding?
titleSuffix: Foundry Tools
description: Learn the latest updates to the Content Understanding API.
author: PatrickFarley 
ms.author: pafarley
manager: nitinme
ms.date: 01/29/2026
ai-usage: ai-assisted
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.custom:
  - references_regions
  - build-2025
---

# What's new in Azure Content Understanding in Foundry Tools?

The Azure Content Understanding service in Foundry Tools is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and new documentation.

> [!NOTE]
> Content Understanding is now a Generally Available (GA) service with the release of the `2025-11-01` API version.

## January 2026

- **Foundry (new) availability**: The new Read and Layout models are now available directly in the Foundry (new) portal.
- **Read and Layout rebuilt analyzers**: The Read and Layout prebuilt models no longer require specifying a model (LLM). They also no longer require your Foundry resource to be configured with a model. Content Understanding can use them even if no model is defined in `contentunderstanding/defaults`.
- **Updated GitHub samples**: New and refreshed samples are now available, including updated [Python](https://github.com/Azure-Samples/azure-ai-content-understanding-python) and [.NET](https://github.com/Azure-Samples/azure-ai-content-understanding-dotnet) samples. Other samples have also been updated.

## December 2025

- **Read and Layout update**: The Read and Layout prebuilt models no longer require specifying a model (LLM). They also no longer require your Foundry resource to be configured with a model. Content Understanding runs them even if no model is defined in `contentunderstanding/defaults`.
- **Updated GitHub samples**: New and refreshed samples are now available, including updated [Python](https://github.com/Azure-Samples/azure-ai-content-understanding-python) and [.NET](https://github.com/Azure-Samples/azure-ai-content-understanding-dotnet) samples. Other samples have also been updated.
- **Foundry NextGen availability**: The new Read and Layout models are now available directly in the Foundry New portal.

## November 2025

Azure Content Understanding in Foundry Tools is now Generally Available with API version `2025-11-01`. The release brings production readiness plus customer-driven enhancements across model choice, management, and security.

### Flexibility to choose the right generative AI model for every workload

- Connect Content Understanding to a Microsoft Foundry model deployment for generative AI so you can control quality, latency, and cost. You can choose either pay-as-you-go or Provisioned Throughput Unit (PTU) deployments for your Foundry model. See what models are [currently supported](concepts/models-deployments.md#supported-models). To try it, see [How to build a custom analyzer in Content Understanding Studio](how-to/customize-analyzer-content-understanding-studio.md).
- Model selection gives you the flexibility to optimize your Foundry model deployment with settings like type (Global, DataZone, or Regional) and Provisioned Throughput Units (PTUs) to reserve capacity for predictable, high-volume workloads. For details see [Deployment types for Foundry Models](../../ai-foundry/foundry-models/concepts/deployment-types.md).
- Transparent pricing model provides clear visibility into costs across content extraction, contextualization, and generative model usage. Content Understanding only charges for content extraction (per page/minute) and contextualization. Generative features directly use your Foundry model deployment incurring standard token-based charges. Learn more in the [Pricing explainer](pricing-explainer.md).

### Analyzer updates

- **Optimize performance and reduce costs** with granular control over field extraction. Enable confidence scores and source grounding only for the fields where you need validation and traceability using the `estimateSourceAndConfidence` configuration setting. This selective approach reduces response payload sizes and lowers processing costs and latency by computing confidence metrics only when required. Confidence scores are only supported for document files.
- **Classification is now integrated** with the analyzer API, which supports classification using the `contentCategories` property. The number of supported categories expands from 50 to 200, enabling precise classification and routing of diverse [file types](/azure/ai-services/content-understanding/service-limits#input-file-limits) within a single analyzer—no separate classifier required. See [Build a robotic process automation solution](tutorial/robotic-process-automation.md) for an example.
- **Analyzer lifecycle APIs** extend to support copy, delete, and replace to give you complete control over analyzer versions. See [Migrate projects from preview to GA](how-to/migration-preview-to-ga.md) for guidance.
- **Delete analyze results**: You can now explicitly delete analyzer results after you retrieve them, giving you control over data retention for compliance and privacy requirements. See [Delete analyze response](/rest/api/contentunderstanding/content-analyzers/get-result-file?view=rest-contentunderstanding-2025-11-01&preserve-view=true).

### RAG analyzers

RAG analyzers are optimized for retrieval-augmented generation scenarios. They extract content with layout as markdown and perform semantic analysis to enhance retrieval quality for downstream applications.

- **Documents**: `prebuilt-documentSearch` extracts paragraphs, tables, and figure descriptions from documents. It enables textual descriptions of images, charts, and diagrams. It captures hand-written annotations, generates content summaries, and supports a [wide range of file formats](/azure/ai-services/content-understanding/service-limits#input-file-limits) including PDF, images, Office documents, and text files.
- **Multimodal support**: Extends to video, image, and audio with `prebuilt-videoSearch` for transcript extraction and segment-based summaries with automatic scene detection, `prebuilt-imageSearch` for visual content descriptions and insights, and `prebuilt-audioSearch` for conversation transcription with speaker diarization and multilingual support.

Review the full analyzer catalog in [Prebuilt analyzers in Content Understanding](concepts/prebuilt-analyzers.md).

### Domain-specific prebuilt analyzers for industry workloads

Domain-specific prebuilt analyzers are tailored for industry scenarios. They enable automated extraction of structured data from specialized document types without custom training.

- **Finance and tax**: Extract key data from financial statements, tax forms, W-2s, 1099s, and other tax documents with tuned schemas that capture amounts, dates, tax identifiers, and financial entities. See [finance and tax](concepts/prebuilt-analyzers.md#domain-specific-analyzers).
- **Procurement and contracts**: Process purchase orders, contracts, and procurement documents to extract vendor information, line items, pricing, terms, and contractual obligations. See [ legal and business documents](concepts/prebuilt-analyzers.md#domain-specific-analyzers).
- **Mortgage and lending**: Automate extraction from mortgage applications, loan documents, and lending forms, capturing borrower details, property information, loan terms, and financial disclosures. See [mortgage and lending](concepts/prebuilt-analyzers.md#domain-specific-analyzers).
- **Identity verification**: Process passports, driver's licenses, ID cards, and other identity documents with `prebuilt-idDocument`, extracting personal information, document numbers, and verification details. Categorization lets you send specific sections - such as passport pages - to purpose-built analyzers during a single run. See [identity documents](concepts/prebuilt-analyzers.md#domain-specific-analyzers).
- **Utilities, billing, and more**: Extract structured data from utility bills, invoices, and billing statements across industries, capturing account information, usage details, and payment data.

Explore the domain-specific analyzer lineup and usage guidance in [Prebuilt analyzers in Content Understanding](concepts/prebuilt-analyzers.md#domain-specific-analyzers).

### Content extraction

- **Content annotations** - `digital PDF` inputs support annotations to provide more metadata on the document. The metadata can identify spans of content that have annotations like highlight, underline, strikethrough, and more. 
- **Multi-page tables and output formats** - You can choose the table output format between HTML or Markdown to align with your application needs. Tables are also multipage by default. The service returns multipage tables as a single table object.
- **Hyperlink extraction** - The service now extracts hyperlinks embedded within documents as a URL.
- **Figure extraction** - The service can now extract figures and charts as either chart.js or mermaid.js syntax depending on the types, along with its description.

### Field extraction

- **Confidence scores are now consistently available across all extraction methods for documents**—whether you use extract, generative, or classify—giving you uniform quality metrics regardless of how you process fields. Confidence scores are only supported for document modality. Learn how to [enable confidence scores for field extraction](document/overview.md#field-extraction).
- **Simplified schema definition** with intelligent defaults and streamlined workflows. The extraction method is now optional. Content Understanding automatically selects the best approach for each field, reducing configuration complexity. This intelligent behavior makes it easier to build and maintain analyzers without deep knowledge of extraction techniques.
- **Added support for complex types like objects**: Define an object, for example a customer object with contained fields of name, address, and phone.
### Enterprise security and governance

- General availability includes Microsoft Entra ID, managed identities, customer-managed keys, virtual networks, and private endpoints.
- These controls keep sensitive content in your Azure boundary and help you meet compliance requirements. Learn more in [Secure access to Content Understanding](concepts/secure-communications.md).

### Other improvements

- `prebuilt-read` and `prebuilt-layout` analyzers now bring key Document Intelligence capabilities to Content Understanding. See [Prebuilt analyzers](concepts/prebuilt-analyzers.md).
- `prebuilt-layoutWithFigures` extends layout extraction with figure detection and analysis, extracting and summarizing charts, diagrams, and images with their context. See [Prebuilt analyzers](concepts/prebuilt-analyzers.md).
- When analyzing content, you can now provide a **page range** to only analyze specific pages of the input document.
- Segmentation and classification (`contentCategories`) let you send sections to purpose-built analyzers during a single run. For example, `prebuilt-idDocument` classifies pages and routes them to specific analyzers (such as passport and driver's license analyzers), each with their own schemas—all within a single run.

### Region expansion and availability

- Content Understanding is now supported in 14 regions worldwide, providing greater geographic coverage, and improved data residency options. See the [language and region support documentation](language-region-support.md) for the detailed list of available regions.
- Content Understanding is available in [Content Understanding Studio](https://aka.ms/cu-studio) and through the REST API for programmatic access.

### Breaking changes

- Managed capacity for the preview generative models is retired. To use Content Understanding, you always bring your own Foundry large language model and embedding deployments.
- Dedicated classifier APIs are deprecated because classification now lives inside the analyzer API as the `contentCategories` feature.
- Video segmentation can now be done using the `contentCategories` capability, unifying the API for splitting files across document and video analyzers.
- The preview API (`2025-05-01-preview`) doesn't carry forward Pro mode for cross-file analysis or the person directory with Face API integration.

## October 2025
Content Understanding preview version introduces the following updates:

* Content Understanding now has increased field count support (1,000) for all modalities.
* The API response body now includes input, output, and contextualization tokens consumed as part of the tokens object. Check out the quickstart article for more information.

## May 2025

The Azure Content Understanding [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) REST API is now available. This update introduces the following updates and enhanced capabilities:

### Processing modes

With the [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) release, two modes are introduced: `standard` and `pro`. The default mode for all analyzers is `standard`.

Content Understanding pro mode adds reasoning, support for multiple input documents, and the ability to configure an external knowledge base for linking, enrichment, and validation. These features automate complex tasks by extending field extraction capabilities to cover scenarios that previously required custom code or human effort.

The `pro` mode (preview) is currently limited to documents as inputs, with support for other types of content coming soon. Common challenges that the pro mode addresses are aggregating a schema across content from different input files, validating results across documents, and using external knowledge to generate an output schema. Learn more about the [pro mode (preview)](concepts/standard-pro-modes.md).

### Foundry experience

With this release, the following updates are now available to the Content Understanding experience in Microsoft Foundry:

* Added support for creating both `standard` mode and `pro` mode tasks in the existing Content Understanding experience. Now by using pro mode, you can bring in your own reference data and create a task that executes multistep reasoning on your data. Read more about the two different task types in [Create Content Understanding Standard and Pro tasks in the Foundry (classic) portal](./how-to/content-understanding-foundry-classic.md).
* Try-out experiences are now available for general document analysis and invoice analysis. Try out these prebuilt features on your own data and start getting insights without having to create a custom task. 

### Document classification and splitting

This release introduces a new [classification API](concepts/classifier.md). This API supports classifying and logically splitting a single file containing multiple documents with optional routing to field extraction analyzers. You can create a custom classifier to split and classify a file into multiple logical documents and route the individual documents to a downstream field extraction model in a single API call.

### Improvements to document processing

* Added support for extracting table spanning multiple pages as a single logical table. Learn more about [structure extraction updates in documents](document/elements.md).
* Selection mark support for checkmark and radio buttons as Unicode characters. Learn more about [structure extraction updates in documents](document/elements.md).
* Barcode extraction as part of the default content extraction along with `OCR`. Learn more about [structure extraction updates in documents](document/elements.md).
* Confidence score improvements with better grounding results for extractive fields.
* New file format support extended for following document types: `docx`, `xslx`, `pptx`, `msg`, `eml`, `rtf`, `html`, `md`, and `xml`.

### Improvements to video processing

* Added support for whole video fields. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
* Added support for video chapters via segmentation. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
* Added support for face identification on extracted face thumbnails. The identity enhances the description and downstream tasks like search and retrieval.
* Added support for disabling face blurring in analyzer configuration. Learn more about [video processing improvements](video/overview.md#face-description-fields).

### Improvements to audio processing

* Added more locales for audio transcription. Learn more about [audio capabilities](audio/overview.md).
* Added support for multilingual audio processing. Learn more about [language handling improvements in audio](audio/overview.md#language-handling).
* Increased maximum supported file size to 1 GB and length to 4 hours. Learn more about [audio service limits](service-limits.md).

### Face API (preview)

This release adds new face detection and recognition capabilities to Content Understanding. You can create a directory of faces and persons. Use the directory to recognize the faces in the processed content. Learn more about [detecting and recognizing faces](face/overview.md).


## April 2025

**2024-12-01-preview** REST API introduces the following updates and enhanced capabilities:

* **General improvements**. For all modalities, to request an increase from current limits, contact `cu_contact@microsoft.com`.
* **Prebuilt invoice template**. The invoice template is now customizable. Once you select the invoice template, you can access a predefined list of fields that you can tailor to your specific needs by adding or removing fields.
* **Generative and classification fields**
  * Both generative and classification fields are now supported for documents modality.
  * You can now use the REST endpoint or Studio to define generative and classification fields with zero-shot outputs for documents. This feature enables you to generate summaries, infer results, and classify individual documents across multiple files.
  * You can invoke multiple analyzers to process individual files.
* **Video modality**
  * Latency improvement for video processing resulting in 50% lower latency.
  * Expanded output types to add support for `Object` and `Arrays`.
  * Added support for video files provided via S3 presigned URL ingestion.
  * Improved video segmentation to semantically segment especially when no shot edits exist in the video.
* **Audio modality**
  * API now supports the field type: `group`.
* **Text modality**
  * API support for the field type: `group`.
* **User experience improvements**
  * Added functionality to download and upload schema configurations during schema definition.
  * Enhanced file labeling and analyzer building processes.
  * Added download code samples for quick setup.

## November 2024

Welcome! The Azure Content Understanding API version `2024-12-01-preview` is now in public preview. This version allows you to generate a structured representation of content tailored to specific tasks from various modalities or formats. Content Understanding uses a defined schema to extract content suitable for processing by large language models and subsequent applications.
