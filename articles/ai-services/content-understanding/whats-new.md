---
title: What's new in Content Understanding?
titleSuffix: Azure AI services
description: Learn the latest updates to the Content Understanding API.
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.date: 05/19/2025
ms.author: lajanuar
ms.custom:
  - references_regions
---

# What's new in Azure AI Content Understanding?

Azure AI Content Understanding service is updated on an ongoing basis. Bookmark this page to stay up to date with release notes, feature enhancements, and our newest documentation.

## May 2025
The Azure AI Content Understanding **`2025-05-01-preview`** REST API is now available. This update introduces the following updates and enhanced capabilities:

* **Modes for documents**: With the **`2025-05-01-preview`** release, we introduce two modes: `standard` and `pro`. Content Understanding pro mode adds reasoning, support for multiple input documents, the ability to configure an external knowledge base for linking and validation. These features enable agentic processes for automating complex tasks requiring human effort. The `pro` mode is currently limited to the document analyzer, enables reasoning capabilities that can infer complicated outputs given multiple reference documents (for example, insurance policy documents) and multiple input documents (for example, forms and supporting documents that are case-specific)

* **Document modality improvements** :

  * Improvements in content extraction:
      * Support for table spanning multiple pages getting extracted as a single logical table. 
      * Selection mark support for checkmark and radio buttons as unicode characters.
      * Bar code extraction as part of the default content extraction along with `OCR`.
      * Support for embedded figures in Markdown as base64 string format output.
  * Confidence score improvements with better grounding results for extractive fields. 
  * New file format support extended for following document types `.rtf`,`.txt`,`.xml`,`.json`, `.msg`,`.eml`,`.csv`, and `.xlsx`.
  * Classification API for documents only. This API supports classifying and splitting a single file containing multiple documents  with optional routing to field extraction analyzers.

* **Video Modality improvements**:

  * Support for whole video fields.
  * Support for video chapters via segmentation.
  * Support for face identification on extracted face thumbnails. The identity enhances the description and downstream tasks like search and retrieval.
  * Support for disabling face blurring in analyzer configuration.

* **Audio Modality improvements**: Support for multi-speaker call center role detection to allow detection of multiple speakers.

* **Face API preview**: Detection, recognition, and enrollment of faces.

* **Billing Changes**: New simpler pricing model that lowers costs from the **2024-12-01-preview** REST API across all modalities.
  
* **User experience improvements**: To improve latency issues, the UX experience is refreshed with ease-of-use and quick try-out experience as part of [Azure AI Foundry](https://aka.ms/cu-landing)

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
