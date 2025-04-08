---
title: What's new in Content Understanding?
titleSuffix: Azure AI services
description: Learn the latest updates to the Content Understanding API.
author: laujan
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: whats-new
ms.date: 11/19/2024
ms.author: lajanuar
ms.custom:
  - references_regions, ignite-2024-understanding-release
---

# What's new in Azure AI Content Understanding?

The Content Understanding service is continuously updated. Bookmark this page to stay informed about the latest features and samples.

## March 2024
With March release in preview.1, we have launched support for: 
* Prebuilt-invoice template: You can now use invoice as a template and customize the out of the box invoice template per your use case. It is part of document modality, once you select the invoice template, you can automatically get the list of all the predefined fields. You can customize bu adding or deleting any existing fields. 
* Support for generative and classify fields as API : Now, you can define generative and classification fields with zero-shot outputs for documents via REST endpoint which can generate summaries or infer results and classify a single documents into multiple files that it may contain. You can further call multiple analyzers to process individual files. Support in UX coming soon.
* Maximum number of Fields & Language Support : We are expanding support of tier 1 languages and tier 2 support, along with expanding the total number of fields to be 50 for all modalities (default) and upto 100 for documents. In order to increase the limit, please reach out on cu_contact@microsoft.com.
* Normalization support for documents: Normalization support added for all regions expanding from US region.
* Video modality improvements: We have added improvements for object field reordering, disabling face blurring through generative fields.
* Audio modality improvements: We have enabled transcription as an input for speech and added object support. 
* UX improvements: We have added support to download schema and upload schema configurations while defining schema, improvements in labeling the files and while building the analyzer, ability to download the code samples to get started. 

## November 2024
Welcome! The Azure AI Content Understanding API version `2024-12-01-preview` is now in public preview. This version allows you to generate a structured representation of content tailored to specific tasks from various modalities or formats. Content Understanding uses a defined schema to extract content suitable for processing by large language models and subsequent applications.
