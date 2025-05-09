---
title: Video retrieval deprecation notice
titleSuffix: Azure AI services
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-vision
ms.topic: include
ms.date: 03/21/2025
ms.collection: "ce-skilling-fresh-tier2, ce-skilling-ai-copilot"
ms.update-cycle: 365-days
ms.author: pafarley
---

> [!IMPORTANT]
> On 30 June 2025, Azure AI Vision Video Retrieval will be retired. The decision to retire this feature is part of our ongoing effort to improve and simplify and improve the features offered for video processing. Migrate to Azure AI Content Understanding and Azure AI Search to benefit from their additional capabilities.
>
> **Video processing: Video Retrieval vs Azure AI Content Understanding**
>
>|Feature |	Video Retrieval for video description |	Azure AI Content Understanding|
>|---|---|---|
Video Length Supported|Optimized for short videos, up to ~3 minutes|Supports short & long videos, up to 4 hours|
>|Frame Processing|Up to 20 frames|Batch processing, sampling shot-by-shot sampled across entire video|
>|Content Extraction Pre-Processing|Transcription|Transcription, Shot identification, Face grouping|
>|Structured Output Support|Not supported|Supports schema-conforming structured outputs|
>|Data types|Video supported|Video, images, documents, and speech supported|
>|Pricing|Variable Token-based|Fixed cost per minute of video processed|
> 
> To migrate to Content Understanding for video summaries and descriptions, we'd recommend reviewing the [Azure AI Content Understanding](/azure/ai-services/content-understanding/video/overview) documentation.
>
>
> **Video Search: Video Retrieval vs. Azure AI Search and Content Understanding**
>
>|Feature |	Video Retrieval for video search |	Azure AI Search and Content Understanding|
>|---|---|---|
|Visual Embedding type|Frame-based Image Embeddings|Video description text embeddings|
|Content Extraction Pre-Processing|Transcription, OCR|Transcription, Shot identification, Face grouping|
|People & Object search support|Strong support|Strong support|
|Action and Event support|Limited|Strong support|
|Customization|None|Content Understanding analyzer can be customized to focus using the fields and field descriptions|
>
> To start building the search use case with Content Understanding, we recommend starting with this [sample](https://aka.ms/Content-Understanding-Video-Search) which shows how to use Azure AI Search to search videos.
>
> To avoid service disruptions, migrate by 30 June 2025.

