---
title: Azure AI Content Understanding video overview
titleSuffix: Azure AI services
description: Learn how to use Azure AI Content Understanding video solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 10/24/2024
---

# Use Content Understanding video solutions overview (preview)

Azure AI Content Understanding lets you extract and customize video metadata for seamless integration into your systems or workflows. Content Understanding helps efficiently manage, categorize, retrieve, and build workflows for video assets. Content Understanding can enhance your media asset library, support workflows such as highlight generation, categorize content, and facilitate applications like retrieval-augmented generation (`RAG`). The video content extraction capabilities of Content Understanding offer the following advantages:

* **Video transcription**. Convert speech within a video into text transcripts that can be searched and analyzed. Transcription data is also used as grounding for generating customizable metadata.

* **Shot and Key frame extraction**. Identify different scenes or shots in a video and segment the content for detailed analysis. The detected scenes and shots are available as separate metadata and are also used as grounding data for further metadata customization.

* **Face Grouping**. Recognize and group faces appearing in a video, which can be used for indexing or compliance purposes. The grouped face data is available as metadata and is used as grounding for generating customized metadata fields.

* **Generating fields**. Field generation allows you to define custom metadata fields to extract from your videos by describing them in the schema definition.

## Key benefits

Content Understanding provides a specific set of capabilities for video including:

* **Customization**. Unlike traditional video analysis services, Content Understanding enables you to customize the metadata you want to generate. By modifying the schema, you can tailor the output to match your specific scenario.

* **Segment-based context aware analysis**. By analyzing video segments rather than video frames Content Understanding is able to identify actions, events, topics, and themes in a way that frame-based tools have difficulty achieving.

* **Generative Models**. By using generative AI models, you can describe in natural language what content you want to extract, and Content Understanding generates that metadata.

*    **Integrated preprocessing**. Content Understanding performs several preprocessing steps, such as transcription and scene detection, to provide rich context to AI generative models.

*    **Scenario adaptability**. Whether you need to generate highlights, categorize content for streaming platforms, or identify key moments in a tutorial, the service can adapt to your needs by generating custom fields to extract the correct grounding data.

## Content Understanding video use case industries

* **Broadcast Media and Entertainment**. Manage large libraries of shows, movies, and clips by generating detailed metadata for each asset.

* **Education and E-Learning**. Index and retrieve specific moments in educational videos or lectures.

* **Corporate Training**. Organize training videos by key topics, scenes, or important moments.

* **Marketing and Advertising**. Analyze promotional videos to extract product placements, brand appearances, and key messages.

## Content Understanding video scenarios

* **Media Asset Libraries**. Enhance your media library with detailed metadata for better searchability and organization.

* **Highlight Generation**. Automatically create highlights or summaries of videos based on scene descriptions and key moments.

* **Content Categorization and Compliance**. Categorize videos for streaming platforms, deciding where specific content airs.

* **Retrieval-augmented generation (`RAG`) applications**. Enable applications that can answer user questions with specific video moments by indexing content at a granular level.

## Next steps

Get started using Content Understanding video APIs with our [**how to guide**](how-to/set-up-manage-video-assets.md) for a managing media assets scenario.