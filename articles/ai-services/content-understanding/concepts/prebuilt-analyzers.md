---
title: Azure AI Content Understanding Prebuilt analyzers
titleSuffix: Azure AI services
description: Learn about prebuilt analyzers, their scenarios, customization options, billing, roadmap in Azure AI Content Understanding.
author: laujan
ms.author: admaheshwari
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
---

# Prebuilt analyzers in Azure AI Content Understanding

Azure AI Content Understanding prebuilt analyzers are ready-to-use tools designed to streamline common content processing tasks. They support scenarios such as content ingestion for search and retrieval-augmented generation (RAG) workflows, and intelligent document processing (IDP) for extracting data from invoices or analyzing call center recordings. You can also [customize these analyzers](../tutorial/create-custom-analyzer.md) to extract more fields or refine outputs to better fit your specific workflow requirements.

## Prebuilt analyzers for content ingestion

Azure AI Content Understanding offers prebuilt analyzers that extract raw content with layout as markdown and perform essential semantic analysis, simplifying common content ingestion tasks. These capabilities enhance retrieval quality for downstream applications such as retrieval-augmented generation (RAG).

##### `prebuilt-documentAnalyzer`

* Extracts text and layout details from documents and images.
* Produces a concise summary of the document content.

##### `prebuilt-imageAnalyzer`

* Generates a descriptive caption for the image.

##### `prebuilt-audioAnalyzer`

* Extracts transcripts from audio files.
* Performs speaker diarization to distinguish among different speakers.
* Provides a summary of the audio content.

##### `prebuilt-videoAnalyzer`

* Extracts transcripts from video files.
* Identifies keyframes and camera shots.
* Divides/segments the video into meaningful sections.
* Generates a summary for each video segment.


## Prebuilt analyzers for intelligent document processing

Content Understanding also includes prebuilt analyzers designed for specialized industry scenarios, enabling extraction of structured data from invoices and analysis of call center transcripts.

##### `prebuilt-invoice`

* Extracts text and document layout as markdown from documents and images.
* Extracts structured data from invoices, including invoice number, date, vendor, total amount, and line items. Supports various invoice formats and languages, enabling automated data capture for accounts payable processes and related scenarios.

##### `prebuilt-callCenter`

* Extracts transcripts from audio files.
* Distinguishes between speakers and assigns them to customer or agent roles.
* Analyzes call center transcripts to generate summaries, determine customer sentiment, identify discussion topics, and more.

## Next steps

* [Try out prebuilt analyzers using REST API](../quickstart/use-rest-api.md).
* [Customize prebuilt analyzers](../tutorial/create-custom-analyzer.md).
