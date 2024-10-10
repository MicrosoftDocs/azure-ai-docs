---
title: What is Azure AI Multimodal Intelligence?
titleSuffix: Azure AI services
description: Learn about Multimodal Intelligence solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: TODO
ms.topic: overview
ms.date: 10/09/2024
#Customer intent: As a developer of content management software, I want to find out whether Azure AI Multimodal Intelligence is the right solution for my moderation needs.
---

# What is Azure AI Multimodal Intelligence?

:::image type="content" source="media/overview/media-input.png" alt-text="Screenshot of accepted media input files.":::

Multimodal Intelligence is a cloud-based data solution capable of processing both structured and unstructured content across various formats, such as documents, images, videos, and audio. The service employs a predefined schema to transform content into a task-specific structured representation. This schema can be either prebuilt for common scenarios or customized by the user. Large language models (LLMs) to improve operations, support data-driven decision-making, and drive innovation. Downstream applications use structured output for retrieval augmented generation (RAG) frameworks, developing specialized AI and machine learning models, or creating autonomous workflows. The solution is compatible with both single-modality and multi-modal scenarios.

## Service features

* **Diverse modality processing**. The service intakes document, image, audio, video, and mixed media input and converts it into a structured format easily analyzed and further processed by other services and applications.

* **High-level schema extraction**. Users can define the structure and the schema of the extracted results or use a predefined schema for specific scenarios. Schema values can be as follows:

  * **Extracted (explicit)**. Values like the name of the product in a recording or the brand/logo from a video are examples of extracted values.

  * **Inferred (implicit)**. Inferred values aren't explicitly present in the content but can be determined based on the content. The sum of all line items in an invoice or the end date of a contract given a start date and duration are examples of inferred values.

  * **Abstracted (tacit)**. Abstracted values are generated based on the content of the input. Examples include summaries, outlines, recaps are examples of abstracted values.

## Multimodal Intelligence use cases

|Use|Scenario|
|--------|-------|
|Tax processing automation| Tax preparing companies can use the extended capabilities of Multimodal Intelligence to generate a unified view of information from different documents and generate comprehensive tax returns.|
|Call center post-call analytics| Businesses and call center operators can generate insights from call recordings to track key KPIs to improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.
|Marketing automation digital asset management| Independent software and media vendors that build media asset management solutions can use Multimodal Intelligence to extract richer, targeted content from images and videos.|



## Supported input formats

|Content modality|File extension|
|------------|----------|
|Text document|.txt, .md|
|Visual document|.pdf, .tiff, .jpeg|
|Markup Document|.html, .docx|
|Image|.jpeg, .gif, .tiff|
|Audio|.wav|
|Video|.mp4|
|Structured|.json, .csv|




## Next steps


