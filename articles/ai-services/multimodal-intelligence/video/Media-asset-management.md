---
title: Azure AI Multimodal Intelligence Video Metadata for Media Asset Management Overview
titleSuffix: Azure AI services
description: Learn how to set up a post-call analytics workflow
author: laujan
ms.author: jfilcik
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/24/2024
---

# Video Metadata for Media Asset Management Overview

> [!IMPORTANT]
>
> * Azure AI Multimodal Intelligence is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).


# Overview

Media Asset Management (MAM) is essential for organizations that deal with large volumes of video content. Efficiently managing, categorizing, retrieving, and building workflows for video assets requires detailed video metadata. Azure AI Multimodal Intelligence enables you to automatically generate specific metadata for your video assets, such as descriptions of each shot, shot types, brands seen and more. This metadata can be customized to your specific needs by just defining the schema. It can be used to enhance your media asset library, supporting workflows like highlight generation, content categorization, and Retrieval-Augmented Generation (RAG) applications.

By leveraging Azure's Multimodal Intelligence APIs, you can extract rich metadata from your videos, customize the metadata fields according to your needs, and integrate this data into your existing MAM systems or workflows.

# Multimodal Intelligence features for Media Asset Management
Recognizing that metadata serves as the cornerstone of a Media Asset Management (MAM) solution, obtaining accurate metadata is critical. It is in this context that Multimodal Intelligence (MMI) proves indispensable.


The Multimodal Intelligence API enables several capabilities for video files.
* Extracting content: 
* **Transcription**: Converts speech within the video into text, providing transcripts that can be searched and analyzed. This transcription data is also used as grounding for generating customizable metadata.
Shot and Key frame extraction: Identifies different scenes or shots in the video, segmenting the content for detailed analysis. The detected scenes and shots are available as separate metadata and are also used as grounding data for further metadata customization.
* **Face Grouping**: Recognizes and groups faces appearing in the video, which can be used for indexing or compliance purposes. The grouped face data is available as metadata and is used as grounding for generating customized metadata fields.
* Generating fields:
* **Field generation**: Allows you to define custom metadata fields to extract from your videos by simply describing them in the schema definition.

## Key Benefits 
Multimodal Intelligence provides a specific set of capabilities for video including:

* **Highly Customizable**: Unlike traditional video analysis services, the Multimodal Intelligence API allows you to customize the metadata you want to generate. By modifying the schema, you can tailor the output to match your specific use cases.
Segment-based context aware analysis: By analyzing video segments rather than frames Multimodal intelligence is able to identify actions, events, topics, and themes in a way that frame-based tools have difficulty doing. 

* **Generative Models**: Leveraging generative AI models, you can describe in natural language what content you want to extract, and the service will generate that metadata.

* **Integrated Pre-processing**: The service performs several pre-processing steps, such as transcription and scene detection, to provide rich context to the generative models.

* **Adaptable to Various Scenarios**: Whether you need to generate highlights, categorize content for streaming platforms, or identify key moments in a tutorial, the service can adapt to your needs by generating custom fields to extract the right grounding data.

## Use Cases and Industries

**Industries**:
* **Broadcast Media and Entertainment**: Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.

* **Education and E-Learning**: Index and retrieve specific moments in educational videos or lectures.
Corporate Training: Organize training videos by key topics, scenes, or important moments.
Marketing and Advertising: Analyze promotional videos to extract product placements, brand appearances, and key messages.

## Use Cases:
* **Media Asset Libraries**: Enhance your media library with detailed metadata for better searchability and organization. 
* **Highlight Generation**: Automatically create highlights or summaries of videos based on scene descriptions and key moments. 
* **Content Categorization & Compliance**: Categorize videos for streaming platforms, deciding where specific content will air. 
* **RAG Applications: Enable applications** that can answer user questions with specific video moments by indexing content at a granular level.

# Next steps
In this section of this article, you learn how to create a media asset management workflow with Multimodal Intelligence service. 
