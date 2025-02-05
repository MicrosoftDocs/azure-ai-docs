---
title: Azure AI Content Understanding Capabilities Overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding Capabilities.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 02/03/2025
ms.custom: 2025-understanding-release
---

# Content Understanding Capabilities (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Content Understanding offers a streamlined process and various capabilities to reason over large amounts of unstructured data, accelerating time-to-value by generating an output that can be integrated into analytical workflows and retrieval augmented generation (RAG) applications.

## Key Capabilities of Content Understanding

### Multimodal Data Ingestion
Content Understanding processes a variety of data types, including documents, text, images, audio, and video, converting them into a structured format for efficient analysis. This service offers a comprehensive solution, eliminating the need to manage separate Azure resources for each type of data—speech, vision, and document processing. By integrating these functionalities, Content Understanding simplifies workflows, reduces operational complexity, and enhances efficiency.

### Content Extraction
Content extraction focuses on extracting general information from the input content. For example, content extraction can be used to extract all printed or handwritten text, perform layout analysis to identify paragraphs, sections, and tables, and recognize barcode within a document.


#### Add-on capabilities of content extraction
Content Understanding supports more sophisticated analysis capabilities. Use the add-on features to extend the results to include more features extracted from your content. Some add-on features incur an extra cost. These optional features can be enabled and disabled depending on the scenario.

To explore the content extraction and add-on capabilities for each modality, select a modality from the tabs below.

# [Document](#tab/document)

|Content Extraction|Add-on Capabilities|
|--------|-------------|
|&bullet; **Optical Character Recognition (OCR)**: Extract printed and handwritten text from documents in various file formats, converting it into structured data. </br>|  &bullet; **Layout**:Extracts layout information such as paragraphs, sections, tables, and more.. </br>&bullet; **Barcode**:  Identifies and decodes all barcodes in the documents. </br> &bullet; **Formula**: Recognizes all identified mathematical equations from the documents. </br> |

# [Image](#tab/image)

|Content Extraction|Add-on Capabilities|
|--------|-------------|
|&bullet; **Image Analysis**: Analyze images to extract structured fields. </br>&bullet; **Defect detection**:  Identify potential defects and their severities in defect scenarios </br> &bullet; **Retail Inventory Management**: Identify and extract retail products fields product on shelves and retail scenarios. </br>| N/A |

# [Audio](#tab/audio)

|Content Extraction|Add-on Capabilities|
|--------|-------------|
|&bullet; **Transcription**:Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request. </br>&bullet; **Diarization**:  Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers. </br> &bullet;  **Speaker role detection**: Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers. <br> &bullet; **Language detection**: Automatically detects the language in the audio or uses specified language/locale hints. </br>| N/A |

# [Video](#tab/video)

|Content Extraction|Add-on Capabilities|
|--------|-------------|
|&bullet; **Transcription**: Converts speech to structured, searchable text via Azure AI Speech, allowing users to specify recognition languages. </br>&bullet; **Shot Detection**:  Identifies segments of the video aligned with shot boundaries where possible, allowing for precise editing and repackaging of content with breaks exactly on shot boundaries. </br> &bullet; **Key Frame Extraction**: Extracts key frames from videos to represent each shot completely, ensuring each shot has enough key frames to enable Field Extraction to work effectively.</br> | **Face Grouping**: Grouped faces appearing in a video to extract one representative face image for each person and provides segments where each one is present. The grouped face data is available as metadata and can be used to generate customized metadata fields.This feature is limited access and involves face identification and grouping; customers need to register for access at Face Recognition. |

----
### Information Extraction Using Schemas
Schemas play a crucial role in Content understanding by providing a structured framework for extracting and organizing information from various data types. [Field extraction](#1-field-extraction), [grounding and confidence scores](#2-grounding-and-confidence-scores) are some of the key reasons why schemas are powerful.

#### 1. Field Extraction
Schemas enable the extraction of structured data from unstructured data using generative AI to generate, classify or extract data from the input content. For instance, field extraction can identify the invoice amount in a document, capture names mentioned in an audio file, or generate a summary of a video.  [Learn more and follow a quickstart guide to build a schema and extract fields.](../quickstart/use-ai-foundry.md#build-a-schema)

Generation methods differ by modality type. To learn more about the supported generation methods for each modality, select a modality from the tabs below.

----
# [Document](#tab/document)

|Supported generation methods|
|--------------|
|**Extract**: In document, users can extract field values from input content, such as dates from receipts or item details from invoices. |

# [Image](#tab/image)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In images, users can derive values from the input content, such as generating titles, descriptions, and summaries for figures and charts. <br> &bullet; **Classify**: In images, users can categorize elements from the input content, such as identifying different types of charts like histograms, bar graphs, etc.<br> |

# [Audio](#tab/audio)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In audio, users can derive values from the input content, such as conversation summaries and topics. <br> &bullet; **Classify**: In audio, users can categorize values from the input content, such as determining the sentiment of a conversation (positive, neutral, or negative).<br> |

# [Video](#tab/video)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In video, users can derive values from the input content, such as summaries of video segments and product characteristics. <br> &bullet; **Classify**: In video, users can categorize values from the input content, such as determining the sentiment of conversations (positive, neutral, or negative). <br>|

-------
#### 2. Grounding and Confidence Scores

Content Understanding ensures that the results from field and content extraction are accurately grounded to the input content and provide confidence scores for the extracted data, making automation and validation more reliable.

### Analyzers
Analyzers serve as the fundamental element of Content Understanding. They enable clients to set up content extraction configurations and field extraction schemas. Once established, the analyzer reliably applies these settings to all incoming data for processing. 

#### Prebuilt and Customizable Analyzers
Each modality offers suggested analyzer templates tailored to common scenarios, with some templates providing prebuilt schemas.

These suggested templates serve as a starting point, allowing users to customize them to fit specific needs and extract relevant data. This approach simplifies data extraction without requiring specialized AI skills, such as prompt engineering. [Learn more about analyzer templates](../quickstart/use-ai-foundry.md#analyzer-templates)

#### Training Analyzers

If you want to further boost the performance for field extraction, training is possible with zero-shot capabilities when provided with a few labeled samples. Note: This feature is available to document scenario now.


## Input requirements
For detailed information on supported input document formats, refer to our [Service quotas and limits](../service-limits.md) page.

## Supported languages and regions
For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

## Data privacy and security
Developers using Content Understanding should review Microsoft's policies on customer data. For more information, visit our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) page.

## Next step
* Try processing your document content using Content Understanding in [Azure ](https://ai.azure.com/).
* Learn to analyze content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Take a look at our [**glossary**](../glossary.md)


