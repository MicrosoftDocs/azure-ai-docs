---
title: What's new in Content Understanding?
titleSuffix: Azure AI services
description: Learn the latest updates to the Content Understanding API.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.custom:
  - references_regions
  - build-2025
---

# What's new in Azure AI Content Understanding?

Azure AI Content Understanding service is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

## May 2025

The Azure AI Content Understanding [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) REST API is now available. This update introduces the following updates and enhanced capabilities:

### Processing modes

With the [**`2025-05-01-preview`**](/rest/api/contentunderstanding/content-analyzers?view=rest-contentunderstanding-2025-05-01-preview&preserve-view=true) release, we introduce two modes: `standard` and `pro`.
The default mode for all analyzers is `standard`.
Content Understanding pro mode adds reasoning, support for multiple input documents, the ability to configure an external knowledge base for linking, enrichment, and validation.
These features automate complex tasks by extending field extraction capabilities to cover scenarios that previously required custom code or human effort.

The `pro` mode is currently limited to documents as inputs, with support other types of content types coming soon!
Common challenges that the pro mode addresses are aggregating a schema across content from different input files, validating results across documents, and using external knowledge to generate an output schema.
Learn more about the [pro mode](concepts/standard-pro-modes.md).

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
