---
title: Azure AI Content Understanding Capabilities Overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding Capabilities.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/19/2025
ms.custom: 2025-understanding-release
---

# Content Understanding Capabilities (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Content Understanding provides an advanced approach to processing and interpreting vast amounts of unstructured data. It offers various capabilities that accelerate time-to-value, reducing the time required to derive meaningful insights. By generating outputs that seamlessly integrate into analytical workflows and Retrieval-Augmented Generation (RAG) applications, it enhances data-driven decision-making and boosts overall productivity.

## Overview of Key Capabilities in Content Understanding

### Multimodal Data Ingestion

Content Understanding delivers a unified solution for processing diverse data types - documents, text, images, audio, and video - through an intelligent pipeline that transforms unstructured content into structured, analyzable formats. This consolidated approach eliminates the complexity of managing separate Azure resources for speech, vision, and document processing.

The service employs a customizable dual-pipeline architecture that combines [content extraction](#content-extraction) and [field extraction](#field-extraction) capabilities. Content extraction provides foundational structuring of raw data, while field extraction applies schema-based analysis to derive specific insights. This integrated approach streamlines workflows, reduces operational overhead, and enables sophisticated analysis across multiple modalities through a single, cohesive interface.

### Content Extraction

Content extraction in Content Understanding is a powerful feature that transforms unstructured data into structured data, powering advanced AI processing capabilities. The structured data enables efficient downstream processing while maintaining contextual relationships in the source content.

Content extraction provides foundational data that grounds the generative capabilities of Field Extraction, offering essential context about the input content. Users find content extraction invaluable for converting diverse data formats into a structured format. This capability excels in scenarios requiring:

* Document digitization, indexing, and retrieval by structure
* Audio/video transcription
* Metadata generation at scale

Content Understanding enhances its core extraction capabilities through optional add-on features that provide deeper content analysis. These add-ons can extract ancillary elements like layout information, speaker roles, and face grouping. While some add-ons can incur added costs, they can be selectively enabled based on your specific requirements to optimize both functionality and cost-efficiency. The modular nature of these add-on features allows for customized processing pipelines tailored to your use case.

The following section details the content extraction capabilities and optional add-on features available for each supported modality. Select your target modality from the following tabs and view its specific capabilities.

# [Document](#tab/document)

|Content Extraction|Add-on Capabilities|
|-------------|-------------|
|&bullet; **`Optical Character Recognition (OCR)`**: Extract printed and handwritten text from documents in various file formats, converting it into structured data. </br>|  &bullet; **`Layout`**: Extracts layout information such as paragraphs, sections, and tables</br> &bullet; **`Barcode`**:  Identifies and decodes all barcodes in the documents.</br> &bullet; **`Formula`**: Recognizes all identified mathematical equations from the documents. </br> |

# [Image](#tab/image)
> [!NOTE]
> Content extraction for images is currently not fully supported. The image modality currently supports field extraction capabilities only.

# [Audio](#tab/audio)

|Content Extraction|Add-on Capabilities|
|-------------|-------------|
|&bullet; **`Transcription`**: Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request.</br> &bullet; **`Diarization`**:  Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers. </br>  &bullet; **`Language detection`**: Automatically detects the language spoken in the audio to be processed.</br>| &bullet;  **`Speaker role detection`**: Identifies speaker roles based on diarization results and replaces generic labels like "Speaker 1" with specific role names, such as "Agent" or "Customer." </br>|

# [Video](#tab/video)

|Content Extraction|Add-on Capabilities|
|-------------|-------------|
|&bullet; **`Transcription`**: Converts speech to structured, searchable text via Azure AI Speech, allowing users to specify recognition languages. </br>&bullet; **`Shot Detection`**:  Identifies segments of the video aligned with shot boundaries where possible, allowing for precise editing and repackaging of content with breaks exactly on shot boundaries.</br> &bullet; **`Key Frame Extraction`**: Extracts key frames from videos to represent each shot completely, ensuring each shot has enough key frames to enable Field Extraction to work effectively.</br> | &bullet; **`Face Grouping`**: Grouped faces appearing in a video to extract one representative face image for each person and provides segments where each one is present. The grouped face data is available as metadata and can be used to generate customized metadata fields. This feature is limited access and involves face identification and grouping; customers need to register for access at Face Recognition. |

----
### Field Extraction
Field extraction in Content Understanding uses generative AI models to define schemas that extract, infer, or abstract information from various data types into structured outputs. This capability is powerful because by defining schemas with natural language field descriptions it eliminates the need for complex prompt engineering, making it accessible for users to create standardized outputs.

Field extraction is optimized for scenarios requiring:

* Consistent metadata extraction across content types
* Workflow automation with structured output
* Compliance monitoring and validation

The value lies in its ability to handle multiple content types (text, audio, video, images) while maintaining accuracy and scalability through AI-powered schema extraction and confidence scoring.

Each modality supports specific generation approaches optimized for that content type. Review the following tabs to understand the generation capabilities and methods available for your target modality.

# [Document](#tab/document)

|Supported generation methods|
|--------------|
|&bullet; **Extract**: In document, users can extract field values from input content, such as dates from receipts or item details from invoices. |

:::image type="content" source="../media/capabilities/document-extraction.gif" alt-text="Illustration of Document extraction method workflow.":::

# [Image](#tab/image)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In images, users can derive values from the input content, such as generating titles, descriptions, and summaries for figures and charts. <br> &bullet; **Classify**: In images, users can categorize elements from the input content, such as identifying different types of charts like histograms, bar graphs, etc.<br> |

:::image type="content" source="../media/capabilities/chart-analysis.gif" alt-text="Illustration of Image Generation and Classification workflow.":::

# [Audio](#tab/audio)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In audio, users can derive values from the input content, such as conversation summaries and topics. <br> &bullet; **Classify**: In audio, users can categorize values from the input content, such as determining the sentiment of a conversation (positive, neutral, or negative).<br> |

:::image type="content" source="../media/capabilities/audio-analysis.gif" alt-text="Illustration of Audio Generation and Classification workflow.":::

# [Video](#tab/video)

|Supported generation methods|
|--------------|
|&bullet; **Generate**: In video, users can derive values from the input content, such as summaries of video segments and product characteristics. <br> &bullet; **Classify**: In video, users can categorize values from the input content, such as determining the sentiment of conversations (positive, neutral, or negative). <br>|

:::image type="content" source="../media/capabilities/media-asset.gif" alt-text="Illustration of Video Generation and Classification workflow.":::

-------


Follow our quickstart guide [to build your first schema](../quickstart/use-ai-foundry.md#build-your-first-analyzer).

#### Grounding and Confidence Scores

Content Understanding ensures that the results from field and content extraction are precisely aligned with the input content. It also provides confidence scores for the extracted data, enhancing the reliability of automation and validation processes.

### Analyzers

Analyzers are the core processing units in Content Understanding that define how your content should be processed and what insights should be extracted. Think of an analyzer as a custom pipeline that combines:

* Content extraction configurations - determining what foundational elements to extract.
* Field extraction schemas - specifying what insights to generate from the content.

Key benefits of analyzers include:

* **Consistency**: Analyzers ensure uniform processing across all content by applying the same extraction rules and schemas, delivering reliable and predictable results.

* **Scalability**: Once configured, analyzers can handle large volumes of content through API integration, making them ideal for production scenarios.

* **Reusability**: A single analyzer can be reused across multiple workflows and applications, reducing development overhead.

* **Customization**: Start with prebuilt templates. You can then enhance their functionality with analyzers that can be fully customized to match your specific business requirements and use cases.

For example, you might create an analyzer for processing customer service calls that combines audio transcription (content extraction) with sentiment analysis and topic classification (field extraction). This analyzer can then consistently process thousands of calls, providing structured insights for your customer experience analytics.

To get started, you can follow our guide for [building your first analyzer](../concepts/analyzer-templates.md).

### Best Practices

For guidance on optimizing your Content Understanding implementations, including schema design tips, see our detailed [Best practices guide](best-practices.md). This guide helps you maximize the value of Content Understanding while avoiding common pitfalls.

### Input requirements
For detailed information on supported input document formats, refer to our [Service quotas and limits](../service-limits.md) page.

### Supported languages and regions
For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.

### Data privacy and security
Developers using Content Understanding should review Microsoft's policies on customer data. For more information, visit our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) page.

## Next steps

* Try processing your document content using Content Understanding in [**Azure AI Foundry**](https://ai.azure.com/).
* Learn to analyze content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Take a look at our [**glossary**](../glossary.md)


