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

The Content Understanding service is continuously updated. Bookmark this page to stay informed about the latest features and samples.

## April 2025

The Content Understanding **2024-12-01-preview** REST API is now available. This update for preview API introduces the following updates and enhanced capabilities:

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
