---
title: Azure AI Content Understanding audio overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding audio solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.date: 03/18/2025
ms.custom: ignite-2024-understanding-release
---


# Content Understanding audio solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Content Understanding audio analyzers enable transcription and diarization of conversational audio, extracting structured fields such as summaries, sentiments, and key topics. Customize an audio analyzer template to your business needs using [Azure AI Foundry portal](https://ai.azure.com/) to start generating results.

Here are common scenarios for using Content Understanding with conversational audio data:

* Gain customer insights through summarization and sentiment analysis.
* Assess and verify call quality and compliance in call centers.
* Create automated summaries and metadata for podcast publishing.

## Audio analyzer capabilities

:::image type="content" source="../media/audio/overview/workflow-diagram.png" lightbox="../media/audio/overview/workflow-diagram.png" alt-text="Illustration of Content Understanding audio workflow.":::

Content Understanding serves as a cornerstone for Media Asset Management solutions, enabling the following capabilities for audio files:
  
### Content extraction

* **Transcription**. Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request.

* **`Diarization`**. Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers.

* **Speaker role detection**. Identifies agent and customer roles within contact center call data.

* **Language detection**. Automatically detects the language in the audio or uses specified language/locale hints.

### Field extraction

Field extraction allows you to extract structured data from audio files, such as summaries, sentiments, and mentioned entities from call logs. You can begin by customizing a suggested analyzer template or creating one from scratch.

## Key Benefits
Content Understanding offers advanced audio capabilities, including:

* **Customizable data extraction**. Tailor the output to your specific needs by modifying the field schema, allowing for precise data generation and extraction.

* **Generative models**. Utilize generative AI models to specify in natural language the content you want to extract, and the service generates the desired output.

* **Integrated pre-processing**. Benefit from built-in preprocessing steps like transcription, diarization, and role detection, providing rich context for generative models.

* **Scenario adaptability**. Adapt the service to your requirements by generating custom fields and extract relevant data.

## Content Understanding audio analyzer templates

Content Understanding offers customizable audio analyzer templates:

* **Post-call analysis**. Analyze call recordings to generate conversation transcripts, call summaries, sentiment assessments, and more.

* **Conversation analysis**. Generate transcriptions, summaries, and sentiment assessments from conversation audio recordings.

Start with a template or create a custom analyzer to meet your specific business needs.

## Input requirements
For a detailed list of supported audio formats, refer to our [Service limits and codecs](../service-limits.md) page.

## Supported languages and regions

For a complete list of supported regions, languages, and locales, see our [Language and region support](../language-region-support.md)) page.

## Data privacy and security

Developers using Content Understanding should review Microsoft's policies on customer data. For more information, visit our [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy) page.

## Next steps

* Try processing your audio content using Content Understanding in [**Azure AI Foundry portal**](https://aka.ms/cu-landing).
* Learn how to analyze audio content [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code sample: [**audio content extraction**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/content_extraction.ipynb).
* Review code sample: [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
