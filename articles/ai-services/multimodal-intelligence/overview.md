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



Azure AI Multimodal Intelligence (Multimodal Intelligence) is a cloud-based solution within [**Azure AI services**](../what-are-ai-services.md), designed to process/ingest various data modalities such as documents, images, videos, and audio into customizable output formats using Generative AI, Larger Language models (LLM), and Small Language Models (SLM) within a unified workflow.

Built on the success of Document Intelligence, Multimodal Intelligence offers a streamlined process to reason over large amounts of unstructured data, build customizable workflows, ultimately accelerating time-to-value (TTV), while varied AI models.

:::image type="content" source="media/overview/multimodal-intelligence-process.png" alt-text="Screenshot of accepted media input files.":::

### Benefits of using Multimodal Intelligence

* **Simplified and streamlined workflows**. Multimodal Intelligence simplifies data extraction from mixed modality and unstructured content by eliminating the need for separate workflows.

   :::image type="content" source="media/overview/multimodal-intelligence-workflow.png" alt-text="Screenshot comparing Multimodal Intelligence workflows.":::

* **Efficiency and Cost Reduction**. Automating the ingestion and analysis of large amounts of data from varied sources reduces the cost associated with building Generative AI automation solutions.

* **Enhanced Accuracy**. Multimodal Intelligence uses multiple data modalities to simultaneously analyze and cross-validate information, leading to more accurate and reliable results.

### Multimodal Intelligence use cases

*    **Business leaders and c-suite executives**. Decision makers gain actionable insights from Multimodal Intelligence solutions. Generative
AI powered results and high confidence scores lead to enlightened data-driven decisions and minimize the need for human review.

*    **Developers**. Computer application and system professionals can address enterprise-specific use cases by creating customized workflows using various input data types and deployed custom models.

*    **Subject matter experts**: Domain  and subject matter experts benefit from streamlined output, enhanced automation, and high confidence scores.

## Features and capabilities
|Capability|Description|
|:---------|:----------|
|Diverse modality processing|Multimodal Intelligence intakes document, image, audio, video, and mixed media input and converts it into a structured format easily analyzed and further processed by other services and applications.|
|High-level schema extraction|Users can define the structure and the schema of the extracted results or use a predefined schema for specific schema values: </br></br>&bullet; **Extracted (explicit)**. Values like the name of the product in a recording or the brand/logo from a video are examples of extracted values.</br></br>&bullet; **Inferred (implicit)**. Inferred values aren't explicitly present in the content but can be determined based on the content. The sum of all line items in an invoice or the end date of a contract given a start date and duration are examples of inferred values.</br></br>&bullet; **Abstracted (tacit)**. Abstracted values are generated based on the content of the input. Examples include summaries, outlines, recaps are examples of abstracted values.
|Comprehensive content extraction and analysis| Multimodal Intelligence is equipped with the capability to automatically identify and extract pertinent information from diverse file types. This functionality is available for certain file formats, including documents, audio, and video. The service can analyze data within these files and extract text, key-value pairs, tables, and structure from documents, as well as transcriptions from video and audio files. <br> <br> The primary objective is to transform unstructured data into structured, actionable information that can be readily accessed and utilized.|
|Grounded results for higher accuracy|Multimodal Intelligence ensures that responses are anchored to your input files, leading to higher precision in extracted values. The source information is pivotal to assessing groundedness, serving as the foundation for both grounding and accuracy. A grounded response adheres strictly to the provided information, avoiding any speculation or fabrication. |
|Highly precise confidence scores|Multimodal Intelligence ensures accuracy across contexts for extracted fields. A confidence score from 0 to 100 measures the statistical certainty of the result's reliability. High scores indicate precise data extraction, enabling straight-through processing (STP) in automation workflows.|
|Precise and efficient extraction of modality-specific details for secondary processing scenarios| Users can extract specific content that is suitable for secondary scenarios like Large Language Model (LLM) processing.|

## Scenarios
Common scenarios for Azure AI multimodal intelligence service include:

|Use|Scenario|Scenario Quickstart|
|--------|-------|-------|
|Call center post-call analytics| Businesses and call center operators can generate insights from call recordings to track key KPIs to improve product experience, generate business insights, create differentiated customer experiences, and answer queries faster and more accurately.| [**Post call analytics Quickstart**](audio/how-to/set-up-post-call-analytics.md) |
|Marketing automation digital asset management| Independent software and media vendors that build media asset management solutions can use Multimodal Intelligence to extract richer, targeted content from images and videos.| [**Media asset management Quickstart**](video/how-to/set-up-manage-video-assets.md)|
|Tax processing automation| Tax preparing companies can use the extended capabilities of Multimodal Intelligence to generate a unified view of information from different documents and generate comprehensive tax returns.| Quick start|
Chart Understanding| Businesses can significantly enhance chart understanding by automating the analysis and interpretation of various types of charts and diagrams using Multimodal Intelligence. This capability is useful in several downstream use cases.| Quickstart |

## Responsible AI
At Microsoft, we prioritize advancing AI with a people-first approach. Generative models in Azure AI Multimodal Intelligence have great potential but can produce incorrect or harmful content without careful design. For more information, *see* [Microsoft Responsible AI dashboard](/azure/machine-learning/concept-responsible-ai-dashboard?view=azureml-api-2), [Adopt responsible and trusted AI principles](/azure/cloud-adoption-framework/strategy/responsible-ai), and follow our [**Empowering responsible AI practices**](https://www.microsoft.com/ai/responsible-ai) guidance.

## Data privacy and security

As with all the Azure AI services, developers using the Multimodal Intelligence service should be aware of Microsoft's policies on customer data. See our **Data, Privacy and Security** page to learn more.

## Getting started
Before you get started using Multimodal Intelligence, you need an [**Azure AI services multi-service resource**](how-to/create-multi-service-resource.md). The multi-service resource enables access to multiple Azure AI services with a single set of credentials.

We provide quickstart guides designed to help you begin utilizing Multimodal Intelligence service swiftly:

* **[**Rest API Quickstart**](quickstart/rest-api.md)**
* **Azure AI Studio Quickstart**





