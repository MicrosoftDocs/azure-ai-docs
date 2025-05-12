---
title: Azure AI Content Understanding analyzers overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding analyzers.
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 05/11/2025
---

# Content Understanding analyzers overview (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Azure AI Content Understanding is an advanced generative AI service designed to process and interpret vast quantities of unstructured data with precision. It delivers powerful capabilities that shorten the time needed to extract meaningful insights, accelerating value realization. By producing outputs that seamlessly integrate into analytical workflows and Retrieval-Augmented Generation (`RAG`) applications, it empowers data-driven decision-making, enhances automation, and drives overall productivity improvements.

## Analyzers

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

## Multimodal Data Ingestion

Azure AI Content Understanding offers an integrated solution for handling various data types—documents, text, images, audio, and video—via a sophisticated AI pipeline that converts unstructured content into structured, actionable formats. This streamlined approach simplifies operations by removing the need to manage separate Azure resources for speech, vision, and document processing.

The service employs a customizable dual-pipeline architecture that combines [content extraction](#content-extraction) and [field extraction](#field-extraction) capabilities. Content extraction provides foundational structuring of raw data, while field extraction applies schema-based analysis to derive specific insights. This integrated approach streamlines workflows, reduces operational overhead, and enables sophisticated analysis across multiple modalities through a single, cohesive interface.

## Content extraction

Content extraction in Azure AI Content Understanding is a powerful feature that transforms unstructured data into structured data, powering advanced AI processing capabilities. It identifies and structures text and other elements from your content. The structured data enables efficient downstream processing while maintaining contextual relationships in the source content.

Content extraction provides foundational data that grounds the generative capabilities of Field Extraction, offering essential context about the input content. Users find content extraction invaluable for converting diverse data formats into a structured format. This capability excels in scenarios requiring:

* Document digitization, indexing, and retrieval by structure (can be extended for RAG)
* Audio/video transcription
* Metadata generation at scale

 Content Understanding enhances its core extraction capabilities through optional add-on features that provide deeper content analysis. These add-ons can extract ancillary elements like layout information, speaker roles, and face grouping. While some add-ons can incur added costs, they can be selectively enabled based on your specific requirements to optimize both functionality and cost-efficiency. The modular nature of these add-on features allows for customized processing pipelines tailored to your use case.

The following section details the content extraction capabilities and optional add-on features available for each supported modality. Select your target modality from the following tabs and view its specific capabilities.

|Modality| Content extraction & Add-on analyzers|
|-------------|-------------|
|**Documents** |&bullet; **`Optical Character Recognition (OCR)`**: Extract printed and handwritten text, identify barcodes, mathematical equations, and formula from documents in various file formats, converting it into structured data.</br> &bullet; **`Layout`**: Extracts layout information such as paragraphs, sections, and tables. It also expands **cross table support** for tables that span multiple pages. You may also choose to flatten tables into bullet lists for simpler downstream processing.</br> &bullet; **`Selection Mark`**: Extract details from checkboxes or radio buttons using Unicode characters.|
| **Audio** | &bullet; **`Transcription`**: Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request.</br> &bullet; **`Diarization`**:  Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers. </br>  &bullet; **`Language detection`**: Automatically detects the language spoken in the audio to be processed.</br> &bullet;  **`Speaker role detection`**: Identifies speaker roles based on diarization results and replaces generic labels like "Speaker 1" with specific role names, such as "Agent" or "Customer."|
| **Video** | &bullet; **`Transcription`**: Converts speech to structured, searchable text via Azure AI Speech, allowing users to specify recognition languages.</br>&bullet; **`Shot Detection`**:  Identifies segments of the video aligned with shot boundaries where possible, allowing for precise editing and repackaging of content with breaks exactly on shot boundaries.</br>&bullet; **`Key Frame Extraction`**: Extracts key frames from videos to represent each shot completely, ensuring each shot has enough key frames to enable Field Extraction to work effectively.</br>&bullet; **`Face Grouping`**: Grouped faces appearing in a video to extract one representative face image for each person and provides segments where each one is present. The grouped face data is available as metadata and can be used to generate customized metadata fields. This feature is limited access and involves face identification, description, and grouping; customers need to register for access at `Face Recognition`.</br>&bullet; **`Segmentation`**: Segment the video based on detected shots for highlighting reels or cohesive scene summary using segmentation property|

> [!NOTE]
> **Image**: Content extraction for images is currently not fully supported. The image modality currently supports field extraction capabilities only. 

### Field extraction
Field extraction in Content Understanding uses generative AI models to define schemas that extract, infer, or abstract information from various data types into structured outputs. This capability is powerful because by defining schemas with natural language field descriptions, it eliminates the need for complex prompt engineering, making it accessible for users to create standardized outputs. It helps users to get the streamlined output with zero-shot method without prelabeling.

Field extraction is optimized for scenarios requiring:

* Consistent metadata extraction across content types
* Workflow automation with structured output
* Compliance monitoring and validation

The value lies in its ability to handle multiple content types (text, audio, video, images) while maintaining accuracy and scalability through AI-powered schema extraction and confidence scoring.

Each modality supports specific generation approaches optimized for that content type. We support the following methods across modalities.
> [!NOTE]
> Extract method is only supported for documents for now. To learn more about modality support, *see* [field schema limits](service-limits.md#Field-schema-limits) page.
>
> There's a distinction between digital documents (PDFs, DOCX, etc.) and text documents (plain text, markdown, HTML) in terms of content extraction capabilities.

&bullet; **Extract**: With documents, users can extract raw field values from input content, such as dates from receipts or item details from invoices.

:::image type="content" source="../media/capabilities/document-extraction.gif" alt-text="Illustration of Document extraction method workflow.":::

&bullet; **Generate**: Generative method help user extend generative capabilities to infer details from the content. Users have the flexibility to input content for a wide array of applications. This task involves a range of activities. It includes crafting concise summaries and calculating taxes based on document contents. Additionally, it entails generating eye-catching titles, descriptions, and highlights for images. Other aspects include identifying key topics and summarizing audio conversations, as well as segmenting and analyzing distinct portions of videos. Finally, the task involves extracting product features highlighted in video content.

:::image type="content" source="../media/capabilities/chart-analysis.gif" alt-text="Illustration of Image Generation and Classification workflow.":::

&bullet;  **Classify**: The classify method enables users to categorize values extracted from input content. Users can, for example, compile different document types, such as tax forms like 1099, 1098, and W2, into a single PDF. They can also distinguish between chart types, such as histograms and bar graphs, within images, or analyze the sentiment (positive, neutral, or negative) of conversations in audio and video files.

:::image type="content" source="../media/capabilities/audio-analysis.gif" alt-text="Illustration of audio generation and classification workflow.":::

:::image type="content" source="../media/capabilities/media-asset.gif" alt-text="Illustration of Video generation and classification workflow.":::

Follow our quickstart guide [to build your first schema](../quickstart/use-ai-foundry.md#build-your-first-analyzer).

### Grounding and confidence scores
> [!NOTE]
> These metrics are currently only available for extract method in documents.

Content Understanding ensures that the results from field and content extraction are precisely aligned with the input content. It also provides confidence scores for the extracted data, enhancing the reliability of automation and validation processes.

### Analysis mode

With the `2025-05-01-preview`, we introduce two modes, `pro` and `standard`. Azure AI Content Understanding `pro` mode is designed for intricate use cases requiring advanced, multi-step reasoning capabilities, excelling in deep understanding, and complex decision-making by using both input content and reference data to draw key conclusions, thus reducing the need for human review and enhancing productivity. It offers dynamic task management, supports multiple input documents, and integrates reference datasets to enhance workflows. However, its capabilities are currently confined to document-based data. In contrast, `standard` mode offers structured insights extraction across all data types, optimized for lower cost and latency without data inferencing, ideal for scenarios needing exact insights without complex reasoning, such as structuring data for RAG search workflows, integrating with Microsoft Fabric, analyzing advertising videos, segmenting video footage, and extracting critical data points from sports games. 

### Data processing location

The data processing location refers to the geographical region where your content is analyzed and processed. This feature allows you to specify the region where your data can be processed, ensuring compliance with data residency requirements and optimizing performance based on your needs:

   1. **Data Residency Compliance**: Many organizations have strict regulations regarding where their data can be stored and processed. By specifying the processing location, you can ensure that your content is handled in compliance with local data residency laws.

   1. **Scalability and Capacity**: Choosing a global processing location enables greater capacity and potentially lower latencies. Selection is beneficial for high-volume data processing scenarios where performance and scalability are critical.

#### Supported processing locations

Azure AI Content Understanding supports three processing locations:

**Geography**: This option allows you to process content within the same Azure geography as the Azure AI Services resource. It ensures that your data remains within the chosen geography, complying with regional data residency requirements.

**Data Zone**: This option allows the content to be processed within the broader data zone associated with the current Azure AI Services resource. For example, when processing location is set to data zone, analysis performed using a resource in Sweden Central may be processed anywhere in the European Union, providing greater capacity and potentially lower latencies.

**Global**: This option allows your content to be processed in any available region worldwide, providing access to the greatest capacity and potentially lower latencies.

***Example Use Cases***

1. **Document Analysis**: A financial institution in the European Union (`EU`) needs to analyze customer documents while ensuring compliance with EU data residency regulations. Specifying the `EU` as the processing location enables the institution to meet regulatory requirements while using Azure AI Content Understanding.

1. **Video Content Analysis**: A media company with a global audience wants to analyze video content for metadata extraction and tagging. Choosing a global processing location enables optimization of performance and scalability, ensuring efficient processing of large volumes of video data.

To learn more, *see* [Azure OpenAI Deployment Data processing Locations](../../openai/how-to/deployment-types.ms#azure-openai-deployment-data-processing-locations).

## Next steps

* For guidance on optimizing your Content Understanding implementations, including schema design tips, see our detailed [Best practices guide](best-practices.md).
* For detailed information on supported input document formats, refer to our [Service quotas and limits](../service-limits.md) page.
* For a detailed list of supported languages and regions, visit our [Language and region support](../language-region-support.md) page.
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
* Take a look at our [**glossary**](../glossary.md)
* Refer to our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) policy.


