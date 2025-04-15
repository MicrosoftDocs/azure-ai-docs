---
title: What's new in Content Understanding?
titleSuffix: Azure AI services
description: Learn the latest updates to the Content Understanding API.
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.date: 04/14/2025
ms.author: lajanuar
ms.custom:
  - references_regions, ignite-2024-understanding-release
---

# What's new in Azure AI Content Understanding?

The Content Understanding service is continuously updated. Bookmark this page to stay informed about the latest features and samples.

## May 2025

The Content Understanding **2025-05-01-preview** REST API is now available. This preview API introduces the following updates and enhanced capabilities:

* **General improvements**. The total number of fields supported across all modalities is now 50 by default. For the document modality specifically, this limit can be extended up to 100 fields. To request an increase from 50 to 100 fields for the document modality, contact us at `cu_contact@microsoft.com`.
* **Normalization support**. Document normalization is expanded from the US region to [all supported regions](language-region-support.md#language-support).
* **Prebuilt invoice template**. The invoice template is now customizable. Once you select the invoice template, you can access a predefined list of fields that can be tailored to your specific needs by adding or removing fields.
* **Enhanced generative and classification fields support**. Now, you can define generative and classification fields to produce zero-shot outputs for documents through the REST endpoint. This capability allows you to generate summaries, infer results, and classify a single document into multiple files it may contain. Also, you can utilize multiple analyzers to process individual files independently. 
* **Generative and classification fields**
  * Both generative and classify fields are now supported.
  * You can now utilize the REST endpoint to define generative and classification fields with zero-shot outputs for documents. This feature enables you to generate summaries, infer results, and classify individual documents across multiple files.
  * Multiple analyzers can be invoked to process individual files.
* **Field and language support**
  * Expanded support for Tier 1 and Tier 2 languages.
  * Increased maximum number of fields supported.
* **Video modality**
  * Improvements include object field reordering and the option to disable face blurring via generative fields.
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
