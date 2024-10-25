---
title: What is Azure AI Multimodal Intelligence?
titleSuffix: Azure AI services
description: Learn about Azure AI Multimodal Intelligence solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/09/2024
---

# What is Azure AI Multimodal Intelligence?

:::image type="content" source="media/overview/media-input.png" alt-text="Screenshot of accepted media input files.":::

Azure AI Multimodal Intelligence is a cloud-based solution within [**Azure AI services**](../what-are-ai-services.md), designed to process various data modalities such as documents, images, videos, and audio within a unified workflow. Integrating these diverse modalities enables Multimodal Intelligence to deliver more extensive, efficient, and accurate results compared to single modality processing. Utilizing the Multimodal Intelligence service, provides you with access to the following benefits:

* [**Comprehensive content extraction and analysis**](#features-and-capabilities)

* [**Diverse modality processing**](#features-and-capabilities).

* [**High-level schema extraction**](#features-and-capabilities).

* [**Grounded results for higher accuracy**](#features-and-capabilities)

* [**Enhanced data-input alignment framework**](#features-and-capabilities)

* [**Precise and efficient extraction of modality-specific details for secondary processing scenarios**](#features-and-capabilities).


## Features and capabilities

|Capability|Description|
|:---------|:----------|
|Comprehensive content extraction and analysis|&bullet; **Synchronous**. Process a given document and return the result in the same REST API call.</br></br>&bullet; **Long-running operations (LRO)**. Process larger documents and return an operation location where user can poll for the result.</br></br>&bullet; **Batch**. Process a a set of documents from a blob and write the results to a blob.|
|Diverse modality processing|Multimodal Intelligence intakes document, image, audio, video, and mixed media input and converts it into a structured format easily analyzed and further processed by other services and applications.|
|High-level schema extraction|Users can define the structure and the schema of the extracted results or use a predefined schema for specific schema values: </br></br>&bullet; **Extracted (explicit)**. Values like the name of the product in a recording or the brand/logo from a video are examples of extracted values.</br></br>&bullet; **Inferred (implicit)**. Inferred values aren't explicitly present in the content but can be determined based on the content. The sum of all line items in an invoice or the end date of a contract given a start date and duration are examples of inferred values.</br></br>&bullet; **Abstracted (tacit)**. Abstracted values are generated based on the content of the input. Examples include summaries, outlines, recaps are examples of abstracted values.
|Grounded results for higher accuracy|Multimodal Intelligence ensures that responses are anchored to your input files, leading to higher precision in extracted values. The source information is pivotal to assessing groundedness, serving as the foundation for both grounding and accuracy. A grounded response adheres strictly to the provided information, avoiding any speculation or fabrication. |
|Highly precise confidence scores|The Multimodal Intelligence enhanced data-input alignment framework ensures a high level of certainty and accuracy across various contexts. A confidence score, ranging from 0 to 1, quantifies the likelihood by assessing the statistical certainty that the extracted result is accurate, correct, and reliable. High confidence scores signify precise data extraction. Accurate extraction scores facilitate straight-through processing (STP) in automation workflows.|
|Precise and efficient extraction of modality-specific details for secondary processing scenarios| Users can extract specific content that is suitable for secondary scenarios like Large Language Model (LLM) processing.|

## Scenarios
Common scenarios for Azure AI multimodal intelligence service includes:

|Use|Scenario|Scenario Quickstart|
|--------|-------|-------|
|Call center post-call analytics| Businesses and call center operators can generate insights from call recordings to track key KPIs to improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.| [**Post call analytics Quickstart**](speech/how-to/set-up-post-call-analytics.md) |
|Marketing automation digital asset management| Independent software and media vendors that build media asset management solutions can use Multimodal Intelligence to extract richer, targeted content from images and videos.| [**Media asset management Quickstart**](video/how-to/set-up-video-assets-mam.md)|
|Tax processing automation| Tax preparing companies can use the extended capabilities of Multimodal Intelligence to generate a unified view of information from different documents and generate comprehensive tax returns.| Quick start|
Chart Understanding| Businesses can significantly enhance chart understanding by automating the analysis and interpretation of various types of charts and diagrams using Multimodal Intelligence. This capability is particularly useful in several downstream use cases.| Quickstart | 

## Pricing

Pricing tiers (and the amount you're billed) are based on the number of transactions that you send by using your authentication information. Each pricing tier specifies the:

* Maximum number of allowed transactions per second (TPS).
* Service features enabled within the pricing tier.
* Cost for a predefined number of transactions. Going above this number causes an extra charge, as specified in the [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services) for your service.

## Getting started
Before you get started using Multimodal Intelligence, you need an [**Azure AI services multi-service resource**](how-to/create-multi-service-resource.md). The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

We provide quickstart guides designed to help you begin utilizing Multimodal Intelligence service swiftly:

* **Rest API Quickstart**
* **Azure AI Studio Quickstart**






