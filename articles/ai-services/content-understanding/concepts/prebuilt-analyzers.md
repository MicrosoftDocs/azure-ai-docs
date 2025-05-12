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

## Overview

Azure AI Content Understanding employs analyzers to derive structured insights from unstructured content, spanning documents, images, audio, and video files. Its prebuilt analyzers are ready-to-use solutions tailored for common content processing tasks, including document ingestion, search indexing, and retrieval-augmented generation (`RAG`).

These analyzers streamline trial experiences and can be adapted by extending their functionality to meet specific workflow requirements. Key offerings include:

* **[Content parsers](#content-parsers-for-search-and-ingestion)** for general search and ingestion scenarios.
* **[Scenario-specific predefined analyzers](#scenario-specific-predefined-analyzers)** for targeted use cases like invoices or call center transcripts.
* **[Inheritance from prebuilt analyzers](#inheritance-and-customizing-prebuilt-analyzers)** to customize configuration and fields.

## Content parsers for search and ingestion

To streamline common content ingestion scenarios, Azure AI Content Understanding offers general purpose **prebuilt content analyzers**. These analyzers extract text, layout, and metadata from various content types.


| Analyzer                  | Description                                                                 | Supported File Types |
|:-------------------------|:-----------------------------------------------------------------------------|:--------------------|
| `prebuilt-documentAnalyzer` | Extracts text, layout, and metadata using `OCR` for images and rendered files. Users can customize prebuilt content analyzers to modify configuration and add/remove fields. | `.pdf`, `.tiff`, `image`, `.docx`, `.rtf`, `.html`, `.md`, `.json`, `.xml`, `.csv`, `.tsv`, and `.txt` |
| `prebuilt-imageAnalyzer`    | Generates a descriptive caption of an image and `OCR` is conceptually disabled. Users refine the description and/or add new fields by creating analyzer with baseAnalyzerId=prebuilt-imageAnalyzer.  | image                |
| `prebuilt-audioAnalyzer`    | Produces a transcript, speaker diarization, and a summary for audio files. Users can add new fields by creating analyzer with baseAnalyzerId=prebuilt-audioAnalyzer.  | audio                |
| `prebuilt-videoAnalyzer`    | Extracts keyframes, transcript, and video segmentation. Segmentation is enabled by default. Users can disable/customize segmentation by creating an analyzer with baseAnalyzerId=prebuilt-videoAnalyzer and changing segmentationMode property.                | video                |

Analyzers are optimized for `RAG` ingestion and search workflows, offering default behaviors suitable for indexing and summarizing large volumes of content.

> [!NOTE]
>
> * Currently, `OCR` is supported for `.pdf` and `.tiff` image files. Content elements from such files include span properties and bounding boxes via their source properties.
> * For unsupported files, contents are extracted digitally. Content elements from these files include span properties to indicate their position in the returned markdown.
> * There are no prebuilt models for `agentic` mode. Instead, users can create an analyzer with mode=pro starting from any document base analyzer to test out `agentic` behavior.

## Scenario-specific predefined analyzers

In addition to general content analyzers, Azure AI Content Understanding provides **prebuilt analyzers for specific business scenarios**  to target common scenarios. They can be further customized by setting them as the `baseAnalyzerId`:

| Analyzer             | Description                                                     | Supported File Types |
|:--------------------|:----------------------------------------------------------------|:--------------------|
| `prebuilt-callCenter` | Extracts summary, sentiment, topics, and insights from call center transcripts. | audio |
| `prebuilt-invoice`    | Extracts structured fields such as InvoiceId, Date, and Vendor from invoices. | `.pdf`, `.tiff`, and `image` files.|

These analyzers bundle best practices and hidden configurations to deliver accurate extractions for their intended use cases while simplifying deployment by abstracting internal implementation details.


## Inheritance and customizing prebuilt analyzers

With the **`2025-05-01-preview`**, any prebuilt analyzer can be inherited using `baseAnalyzerId` to create a custom analyzer. Inheritance allows for modification of existing fields, descriptions, types, and methods. Additionally, configuration settings such as `enableFormula`, `segmentationMode`, and others can be customized.

***Example***


### Inherit from prebuilt document analyzer

```json
{
  "baseAnalyzerId": "prebuilt-documentAnalyzer",
  "fields": [
    { "name": "InvoiceId", "type": "string", "method": "regex" },
    { "name": "TotalAmount", "type": "currency", "method": "extractive" }
  ],
  "configuration": {
    "enableFormula": true,
    "tableFormat": "markdown"
  }
}
```

> [!IMPORTANT]
> With the `2025-05-01-preview`, modifying a field description overwrites the internal refined description, potentially reducing extraction quality.
> The `baseAnalyzerId` must be a prebuilt analyzer. Custom analyzers can't currently inherit from other custom analyzers.

## Analyzer details and configurations

* **Document Analyzer**: Uses `OCR` for `.pdf`,`.tiff`, and `image` files.
* **Image Analyzer**: Doesn't use `OCR`but generates image descriptions.
* **Audio Analyzer**: Returns transcript and summary extraction.
* **Video Analyzer**: Returns keyframes, transcript, and segmentation.
* **Call Center Analyzer**: Summarizes and extracts insights from audio. Supports audio text.
* **Invoice Analyzer**: Returns structured field extraction from invoices. Supports `.pdf`, `.tiff`, and `image` files.


## Billing and limits

* **Documents**: Billing is calculated per page, slide, or sheet. For`.docx`, `.rtf`, `.html`, `.md`, `.msg`, `.eml`, `.json`, `.xml`, `.csv`, `.tsv`, and `.txt`, we count every 3k `UTF16 `characters as a page. Field extraction has a `fixed-per-1k` page rate
* **Images**: There's no cost for image content extraction, however, generating a description invokes image field extraction charges.
* **Audio/Video**: Billing is calculated on a per hour basis with 1-minute granularity. Charges are calculated for both audio/video content extraction and field extraction.
* Maximum field limit: Currently there are 90 user-defined fields with 100 total to include reserved fields.

## Next steps

* [Analyzer templates](analyzer-templates.md)
* [Analyzers overview](analyzers-overview.md)


