---
title: Azure AI Content Understanding Capabilities Overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding Capabilities.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 02/25/2025
ms.custom: 2025-understanding-release
---

# Content Understanding Capabilities (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding is a gen-AI based service that takes an advanced approach to processing and interpreting vast amounts of unstructured data. It offers various capabilities that accelerate time-to-value, reducing the time required to derive meaningful insights. By generating outputs that seamlessly integrate into analytical workflows and Retrieval-Augmented Generation (RAG) applications, it enhances data-driven decision-making, automation and boosts overall productivity.

## Overview of Key Capabilities in Content Understanding

### Multimodal Data Ingestion

Azure AI Content Understanding delivers a unified solution for processing diverse data types - documents, text, images, audio, and video - through an intelligent AI pipeline that transforms unstructured content into structured, analyzable formats. This consolidated approach eliminates the complexity of managing separate Azure resources for speech, vision, and document processing.

The service employs a customizable dual-pipeline architecture that combines [content extraction](#content-extraction) and [field extraction](#field-extraction) capabilities. Content extraction provides foundational structuring of raw data, while field extraction applies schema-based analysis to derive specific insights. This integrated approach streamlines workflows, reduces operational overhead, and enables sophisticated analysis across multiple modalities through a single, cohesive interface.

### Analyzers

Analyzers are the core processing units in Content Understanding that define how your content should be processed and what insights should be extracted. Think of an analyzer as a custom pipeline that combines:

* Content extraction configurations - determining what foundational elements to extract.
* Field extraction schemas - specifying how to get the fields(extract/generate/classify) from the content.

:::image type="content" source="../concepts/analyzer-architecture.png" alt-text="Screenshot of Analyzer architecture.":::

Key benefits of analyzers include:

* **Consistency**: Analyzers ensure uniform processing across all content by applying the same extraction rules and schemas, delivering reliable and predictable results.

* **Scalability**: Once configured, analyzers can handle large volumes of content through API integration, making them ideal for production scenarios.

* **Reusability**: A single analyzer can be reused across multiple workflows and applications, reducing development overhead.

* **Customization**: Start with prebuilt templates. You can then enhance their functionality with analyzers that can be fully customized to match your specific business requirements and use cases.

For example, you might create an analyzer for processing customer service calls that combines audio transcription (content extraction) with sentiment analysis and topic classification (field extraction). This analyzer can then consistently process thousands of calls, providing structured insights for your customer experience analytics.

To get started, you can follow our guide for [building your first analyzer](../concepts/analyzer-templates.md).


### Content Extraction

Content extraction in Azure AI Content Understanding is a powerful feature that transforms unstructured data into structured data, powering advanced AI processing capabilities. It identifies and structures text and other elements from your content. The structured data enables efficient downstream processing while maintaining contextual relationships in the source content. 

Content extraction provides foundational data that grounds the generative capabilities of Field Extraction, offering essential context about the input content. Users find content extraction invaluable for converting diverse data formats into a structured format. This capability excels in scenarios requiring:

* Document digitization, indexing, and retrieval by structure (can be extended for RAG)
* Audio/video transcription
* Metadata generation at scale

 Content Understanding enhances its core extraction capabilities through optional add-on features that provide deeper content analysis. These add-ons can extract ancillary elements like layout information, speaker roles, and face grouping. While some add-ons can incur added costs, they can be selectively enabled based on your specific requirements to optimize both functionality and cost-efficiency. The modular nature of these add-on features allows for customized processing pipelines tailored to your use case.

The following section details the content extraction capabilities and optional add-on features available for each supported modality. Select your target modality from the following tabs and view its specific capabilities.

|Modality| Content extraction & Add-on Capabilities|
|-------------|-------------|
|Documents |&bullet; **`Optical Character Recognition (OCR)`**: Extract printed and handwritten text, identify barcodes, mathematical equations and formula (will be part of default OCR capability soon) from documents in various file formats, converting it into structured data. </br> &bullet; **`Layout`**: Extracts layout information such as paragraphs, sections, and tables. It also expands **cross table support** for tables that span multiple pages. You may also choose to flatten tables into bullet lists for simpler downstream processing.</br> &bullet; **`Selection Mark`**: Extract details from checkboxes or radio buttons using Unicode characters. </br>
| Audio | &bullet; **`Transcription`**: Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request.</br> &bullet; **`Diarization`**:  Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers. </br>  &bullet; **`Language detection`**: Automatically detects the language spoken in the audio to be processed.</br> &bullet;  **`Speaker role detection`**: Identifies speaker roles based on diarization results and replaces generic labels like "Speaker 1" with specific role names, such as "Agent" or "Customer." </br> |
| Video | &bullet; **`Transcription`**: Converts speech to structured, searchable text via Azure AI Speech, allowing users to specify recognition languages. </br>  &bullet; **`Shot Detection`**:  Identifies segments of the video aligned with shot boundaries where possible, allowing for precise editing and repackaging of content with breaks exactly on shot boundaries.</br>  &bullet; **`Key Frame Extraction`**: Extracts key frames from videos to represent each shot completely, ensuring each shot has enough key frames to enable Field Extraction to work effectively.</br>  &bullet; **`Face Grouping`**: Grouped faces appearing in a video to extract one representative face image for each person and provides segments where each one is present. The grouped face data is available as metadata and can be used to generate customized metadata fields. This feature is limited access and involves face identification, description and grouping; customers need to register for access at Face Recognition. </br> &bullet; **`Segmentation`**: Segment the video based on detected shots for highlighting reels or cohesive scene summary using segmentation property </br>|

> [!NOTE]
> Image : Content extraction for images is currently not fully supported. The image modality currently supports field extraction capabilities only. Capabilities like Face detection, Face identification and OCR for images will be available shortly. 

----
### Field Extraction
Field extraction in Content Understanding uses generative AI models to define schemas that extract, infer, or abstract information from various data types into structured outputs. This capability is powerful because by defining schemas with natural language field descriptions, it eliminates the need for complex prompt engineering, making it accessible for users to create standardized outputs. It helps users to get the streamlined output with zero-shot method without labelling to start with. 

Field extraction is optimized for scenarios requiring:

* Consistent metadata extraction across content types
* Workflow automation with structured output
* Compliance monitoring and validation

The value lies in its ability to handle multiple content types (text, audio, video, images) while maintaining accuracy and scalability through AI-powered schema extraction and confidence scoring.

Each modality supports specific generation approaches optimized for that content type. We support the following methods across modalities. 
> [!NOTE]
> Extract method is only supported for documents for now. Support for other modalities will be added in the future release.To learn more on modality support, please refer to [field schema limits](service-limits.md#Field-schema-limits) page. </br>
> There’s a distinction between Digital Documents (PDFs, DOCX, etc.) and Text Documents (plain text, markdown, HTML) in terms of content extraction capabilities. 

&bullet; **Extract**: In document, users can extract raw field values from input content, such as dates from receipts or item details from invoices.

:::image type="content" source="../media/capabilities/document-extraction.gif" alt-text="Illustration of Document extraction method workflow.":::

&bullet; **Generate**: Generative method help user extend generative capabilites to infer details from the content. For example, users can derive the input content, such as generating summary, infering tax values from documents, generating titles, descriptions, and summaries for figures in images, conversation summaries and topics from audio, video segments and product characteristics from videos. 

:::image type="content" source="../media/capabilities/chart-analysis.gif" alt-text="Illustration of Image Generation and Classification workflow.":::

&bullet;  **Classify**: Classify method helps user categorize value from input content. For examples, users can categorize elements like multiple doc types within a single pdf (tax form 1099, 1098, W2) in dcouments, identifying different types of charts like histograms, bar graphs, etc in images, determining the sentiment of a conversation (positive, neutral, or negative) in audio and video files. 

:::image type="content" source="../media/capabilities/audio-analysis.gif" alt-text="Illustration of Audio Generation and Classification workflow.":::

:::image type="content" source="../media/capabilities/media-asset.gif" alt-text="Illustration of Video Generation and Classification workflow.":::

Follow our quickstart guide [to build your first schema](../quickstart/use-ai-foundry.md#build-your-first-analyzer).

### Grounding and Confidence Scores
> [!NOTE]
> This is currently only available for extract method in documents. 

Content Understanding ensures that the results from field and content extraction are precisely aligned with the input content. It also provides confidence scores for the extracted data, enhancing the reliability of automation and validation processes.

### Analysis Mode
With preview.2, we have introducted 2 modes, Pro and Standard. Azure AI Content Understanding Pro Mode is designed for intricate use cases requiring advanced, multi-step reasoning capabilities, excelling in deep understanding and complex decision-making by leveraging both input content and reference data to draw key conclusions, thereby reducing the need for human review and enhancing productivity. It supports dynamic task handling, multiple input documents, and reference dataset integration for enriched workflows, currently limited to document data but expanding to other modalities soon. In contrast, Standard Mode offers structured insights extraction across all data types, optimized for lower cost and latency without data inferencing, ideal for scenarios needing exact insights without complex reasoning, such as structuring data for RAG search workflows, integrating with Microsoft Fabric, analyzing advertising videos, segmenting video footage, and extracting critical datapoints from sports games. Learn more about [more capabilities](../articles/ai-services/content-understanding/concepts/standard-vs-pro.md) in each mode. 

### Processing Location
#### What is Processing Location?
Processing location refers to the geographical region where your content is analyzed and processed. This feature allows you to specify the region where your data can be processed, ensuring compliance with data residency requirements and optimizing performance based on your needs.

#### Why is Processing Location Important?

1. **Data Residency Compliance**: Many organizations have strict regulations regarding where their data can be stored and processed. By specifying the processing location, you can ensure that your content is handled in compliance with local data residency laws.

2. **Scalability and Capacity**: By choosing a global processing location, you can access greater capacity and potentially lower latencies. This is beneficial for high-volume data processing scenarios where performance and scalability are critical.

#### Supported Processing Locations

Azure AI Content Understanding supports three processing locations:

**Geography**: This option allows you to process content within the same Azure geography as the Azure AI Services resource. It ensures that your data remains within the chosen geography, complying with regional data residency requirements.

**Data Zone**: This option allows the content to be processed within the broader data zone associated with the current Azure AI Services resource. For example, when processing location is set to data zone, analysis performed using a resource in Sweden Central may be processed anywhere in the European Union, providing greater capacity and potentially lower latencies.

**Global**: This option allows your content to be processed in any available region worldwide, providing access to the greatest capacity and potentially lower latencies.

**Example Use Cases**

1. **Document Analysis**: A financial institution in the European Union needs to analyze customer documents while ensuring compliance with EU data residency regulations. By specifying the EU as the processing location, the institution can meet regulatory requirements while leveraging Azure AI Content Understanding.

2. **Video Content Analysis**: A media company with a global audience wants to analyze video content for metadata extraction and tagging. By choosing a global processing location, the company can optimize performance and scalability, ensuring efficient processing of large volumes of video data.

Learn about about [Azure OpenAI Deployment Data Processing Locations](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/deployment-types#azure-openai-deployment-data-processing-locations).

## Next steps

* For guidance on optimizing your Content Understanding implementations, including schema design tips, see our detailed [Best practices guide](best-practices.md). 
* For detailed information on supported input document formats, refer to our [Service quotas and limits](../service-limits.md) page.
* For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page..
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Take a look at our [**glossary**](../glossary.md)
* Refer to our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) policy.


