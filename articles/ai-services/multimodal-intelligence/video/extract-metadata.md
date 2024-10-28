---
title: Azure AI Multimodal Intelligence extract metadata for media asset management
titleSuffix: Azure AI services
description: Learn how to use Azure AI Multimodal Intelligence to extract metadata for media asset management
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 10/24/2024
---

# Use Multimodal Intelligence to extract metadata for media asset management

Azure AI Multimodal Intelligence enables you to extract rich metadata from your videos, customize the metadata fields according to your needs, and integrate that data into your existing  systems or workflows. Efficiently managing, categorizing, retrieving, and building workflows for video assets requires detailed video metadata. Media asset management (`MAM`) is essential for organizations that handle and process large volumes of video content. Although it can be challenging to implement, `MAM` is an effective tool for organizing and storing digital assets. Multimodal Intelligence enables you to automatically generate specific metadata for your video assets, such as descriptions of each shot, shot types, brands seen, and more. This metadata can be customized to your specific needs by defining the schema. Multimodal Intelligence can be used to enhance your media asset library, support workflows like highlight generation, categorize content, and facilitate applications like retrieval-augmented generation (`RAG`). The Multimodal Intelligence video content extraction capabilities and enable access to the following benefits:

* **Video transcription**. Convert speech within a video into text transcripts that can be searched and analyzed. Transcription data is also used as grounding for generating customizable metadata.

* **Shot and Key frame extraction**. Identify different scenes or shots in a video and segment the content for detailed analysis. The detected scenes and shots are available as separate metadata and are also used as grounding data for further metadata customization.

* **Face Grouping**. Recognize and group faces appearing in a video, which can be used for indexing or compliance purposes. The grouped face data is available as metadata and is used as grounding for generating customized metadata fields.

* **Generating fields**. Field generation allows you to define custom metadata fields to extract from your videos by describing them in the schema definition.

## Key benefits

Multimodal Intelligence provides a specific set of capabilities for video including:

* **Customization**. Unlike traditional video analysis services, Multimodal Intelligence enables you to customize the metadata you want to generate. By modifying the schema, you can tailor the output to match your specific scenario.

* **Segment-based context aware analysis**. By analyzing video segments rather than video frames Multimodal intelligence is able to identify actions, events, topics, and themes in a way that frame-based tools have difficulty achieving.

* **Generative Models**. By using generative AI models, you can describe in natural language what content you want to extract, and Multimodal Intelligence generates that metadata.

*    **Integrated preprocessing**. Multimodal Intelligence performs several preprocessing steps, such as transcription and scene detection, to provide rich context to AI generative models.

*    **Scenario adaptability**. Whether you need to generate highlights, categorize content for streaming platforms, or identify key moments in a tutorial, the service can adapt to your needs by generating custom fields to extract the correct grounding data.

## Multimodal Intelligence video use case industries

* **Broadcast Media and Entertainment**. Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.

* **Education and E-Learning**. Index and retrieve specific moments in educational videos or lectures.

* **Corporate Training**. Organize training videos by key topics, scenes, or important moments.

* **Marketing and Advertising**. Analyze promotional videos to extract product placements, brand appearances, and key messages.

## Multimodal Intelligence video scenarios

* **Media Asset Libraries**. Enhance your media library with detailed metadata for better searchability and organization.

* **Highlight Generation**. Automatically create highlights or summaries of videos based on scene descriptions and key moments.

* **Content Categorization and Compliance**. Categorize videos for streaming platforms, deciding where specific content airs.

* **Retrieval-augmented generation (`RAG`) applications**. Enable applications that can answer user questions with specific video moments by indexing content at a granular level.

# Next steps
Follow this [**how to guide**](how-to/set-up-video-assets-mam.md) to get started with using Multimodal Intelligence APIs for this scenario. 