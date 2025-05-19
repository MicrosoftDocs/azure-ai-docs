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

* **Processing modes**: With the **`2025-05-01-preview`** release, we introduce two modes: `standard` and `pro`. The default mode for all analyzers is `standard`. Content Understanding pro mode adds reasoning, support for multiple input documents, the ability to configure an external knowledge base for linking, enrichment, and validation. These features enable automating complex tasks to extend field extraction capabilities to include tasks that required custom code or human effort. The `pro` mode is currently limited to documents as inputs. Common challenges that the pro mode addresses include aggregating a schema across content from different input files. It also involves validating results across documents. Additionally, it uses external knowledge, such as guidelines, standard operating procedures, and other context, to generate an output schema. Learn more about the [pro mode](concepts/standard-pro-modes.md).

* **Improvements to document processing** :

  * **Document classification and splitting** with a [Classification API](concepts/classifier.md). This API supports classifying and logical splitting a single file containing multiple documents with optional routing to field extraction analyzers. The API enables you to define a workflow to classify and split a file into multiple logical documents and route the individual documents to a downstream field extraction model in a single API call.
  * Improvements in **content extraction**:
      * Added support for extracting table spanning multiple pages as a single logical table. Learn more about [structure extraction updates in documents](document/elements.md).
      * Selection mark support for checkmark and radio buttons as unicode characters. Learn more about [structure extraction updates in documents](document/elements.md).
      * Bar code extraction as part of the default content extraction along with `OCR`. Learn more about [structure extraction updates in documents](document/elements.md).
      * Support for embedded figures in Markdown as base64 string format output. Learn more about [structure extraction updates in documents](document/elements.md).
  * Improvements in **field extraction**
      * Confidence score improvements with better grounding results for extractive fields.
      * New file format support extended for following document types `.rtf`,`.txt`,`.xml`,`.json`, `.msg`,`.eml`,`.csv`, and `.xlsx`.


* **Improvements to video processing**:

  * Added Support for whole video fields. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
  * Added Support for video chapters via segmentation. Learn more about [video processing improvements](video/overview.md#segmentation-mode).
  * Added Support for face identification on extracted face thumbnails. The identity enhances the description and downstream tasks like search and retrieval. Learn more about [face detection in videos](video/overview.md#content-extraction---grouping-and-identification)
  * Added Support for disabling face blurring in analyzer configuration. Learn more about [video processing improvements](video/overview.md#field-extraction--face-description).

* **Improvements in audio processing**:

  * Support for multi-speaker call center role detection to allow detection of multiple speakers.

* **Face API preview**:

This release adds new face detection and recognition capabilities to Content Understanding. You can create a database of faces and recognize the faces in the processed content.
* Detection, recognition, and enrollment of faces. Learn more about [detecting and recognizing faces](face/overview.md).

* **Billing Changes**:

  * New simpler pricing model that lowers processing costs when compared to the **2024-12-01-preview** REST API across many of the features. Learn more about the [updated pricing model](https://azure.microsoft.com/pricing/details/content-understanding/)

* **User experience improvements**:

  The [Azure AI Foundry](https://ai.azure.com/) experience continues to improve with a streamlined project creation flow, improved performance experience, and a try-out experience. Get started with Content Understanding in the [Azure AI Foundry](https://aka.ms/cu-landing) today.

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
