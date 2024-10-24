---
title: Azure AI Multimodal Intelligence speech overview
titleSuffix: Azure AI services
description: Learn about Azure AI Multimodal Intelligence speech solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 10/24/2024
---


# Azure AI Multimodal Intelligence speech solutions overview (preview)

> [!IMPORTANT]
>
> * Azure AI Multimodal Intelligence is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Multimodal Intelligence speech capabilities can help you transcribe and diarize conversational audio. The feature can also help you generate enhanced outputs like summaries, special industry record formats, captioning data. Multimodal Intelligence speech and audio capabilities enable you to extract valuable information such as key topics, sentiment, and more. To get started, use one of the provided out-of-box prebuilt extraction schemas and start generating results. You can also customize Multimodal Intelligence capabilities to meet your business needs as necessary.

Here are some of the common use cases for Multimodal Intelligence on conversational audio data:

* Get customer insights through summarization and sentiment.

* Generate Call Center call analytics results.

* Create a redacted version of the transcript with personally identifiable information (`PII`) removed.

* Analyze recordings to find valuable information like most desired topics.

## Multimodal Intelligence in AI Studio

AI studio enables you to set up, test, and manage Multimodal Intelligence solutions. You can use prebuilt schemas that can be customized to analyze your audio transcripts to easily generate results matching your specific business needs. A typical use case is to automatically process files uploaded into a blob storage account and write the analytics results back to it. Based on the single file analysis, you can then easily index and add these results to a database or an Azure AI Search Index to easily generate more cross-recording insights and dashboards.

* Get insights from audio recordings of meetings, calls, and conversations. Review insights from summaries, sentiment results, action items, meeting notes, and `PII` redacted transcripts.

* Customize the results according to your specific needs and scenarios to modify the output of the workflow.

* Test and deploy customized workflows easily and quickly, without having to write any code or use any external tools.

* Access and manage your Multimodal Intelligence projects and resources in one place, along with other AI services that you use in AI Studio.

 You can use the AI Studio UI to manage speech analytics projects and resources.

* You might prefer to use AI studio for Multimodal Intelligence because it offers a user-friendly interface and an easy-to-use setup experience to generate insights from audio data. You can also test and deploy different versions of the output schema directly in AI studio.

* Developers can use the SDK and APIs to process data at scale in production and to integrate Multimodal Intelligence into Azure Pipelines as needed.

## Multimodal Intelligence speech workflow

The following diagram provides a high-level overview of a typical Multimodal Intelligence Speech processing workflow.

  :::image type="content" source="../media/speech/overview/workflow-diagram.png" alt-text="Illustration of Multimodal Intelligence speech workflow.":::

A typical Multimodal IntelligenceSpeech workflow consists of the following steps:

1. You send audio or transcription files to the Multimodal IntelligenceAPI wither as single file or providing settings to process from a connected blob storage account.

1. Multimodal IntelligenceContent Extraction generates a conversation transcript incl. speaker separation in webVTT format and optionally recognizes speaker roles or names to replace generic 'Speaker n' results.

1. The Multimodal IntelligenceField Extraction then generates added insights based on the generated conversation transcript.

1. The Multimodal Intelligence service returns an audio file results containing the conversation transcript including added generated insights in JSON format. The results are either directly returned from the API or can be written into a connected blob storage account.

## Multimodal IntelligenceSpeech prebuilt scenarios

**Multimodal Intelligence provides the following customizable prebuilt scenario templates:
**
* **Post call analytics** [LINK TO 'How to']. Analyze call recordings and generate outputs such as conversation transcript, call summary, sentiment assessment and more.

* **Conversation summarization** [LINK TO 'How to']. Generate transcriptions from conversation audio recordings, generate a summary, and assess sentiment.

 You can start with any prebuilt scenario or start from scratch to get started and customize as needed to meet your business needs.

## Audio format support and input requirements

**Multimodal Intelligence speech capabilities supports multiple audio formats and codecs, such as**:

* `WAV`
* `MP3`
* `OPUS/OGG`
* `FLAC`
* `WMA`
* `AAC`
* `ALAW` in `WAV` container
* `MULAW` in `WAV` container
* `AMR`
* `WebM`
* `M4A`
* `SPEEX`

**Multimodal Intelligence speech capability operation limits**

|Attribute|Limit|
|-----|-----|
|Time|Maximum of 2 hours in length|
|Size|Maximum of 200 MB in size|
|Speakers|Maximum number of 36 speakers|


## Region and language support

**The following regions support Multimodal Intelligence speech capabilities**:

* West US

* East US

* West Europe

* Sweden Central

* SouthEast Asia

* Australia East

**Multimodal Intelligence speech capabilities supports the following languages and locales**: 

|Language|Language code and locale|
|--------|-------------|
|Arabic |&bullet; `ar-AE` (United Arab Emirates)</br>&bullet; `ar-BH`(Bahrain)</br>&bullet; `ar-DZ` (Algeria)</br>&bullet; `ar-EG` (Egypt)</br>&bullet; `ar-IL` (Israel)</br>&bullet; `ar-IQ` (Iraq)</br>&bullet; `ar-JO` (Jordan)</br>&bullet; `ar-KW` (Kuwait) </br>&bullet; `ar-LB` (Lebanon)</br>&bullet; `ar-LY` (Libya)</br>&bullet; `ar-MA` (Morocco)</br>&bullet; `ar-OM` (Oman)</br>&bullet; `ar-PS` (Palestinian Authority)</br>&bullet; `ar-QA` (Qatar)</br>&bullet; `ar-SY` (Syria)</br>&bullet; `ar-TN` (Tunisia)</br>&bullet; `ar-YE` (Yemen) |
|Chinese Simplified|&bullet; `zh-cn` (Mandarin, Simplified)</br>&bullet; `zh-HK`(Cantonese, Traditional)</br>&bullet;  `zh-TW`(Taiwanese Mandarin, Traditional)|
|Czech |`cs-CZ` (Czechia)|
|Danish |`da-DK` (Denmark)|
|English|&bullet; `en-AU` (Australia)</br>&bullet; `en-CA` (Canada)</br>&bullet; `en-GB` (United Kingdom)</br>&bullet;  `en-IN` (India)</br>&bullet; `en-US` (United States)|
|Finnish |`fi-FI` (Finland)|
|French|&bullet; `fr-CA` (Canada)</br>&bullet; fr-FR (France)|
|German|&bullet; `de-DE` (Germany)|
|German |`de-AT` (Austria)|
|German |`de-CH` (Switzerland)|
|Greek |`el-GR` (Greece)|
|Hebrew |`he-IL` (Israel)|
|Indonesian |`id-ID` (Indonesia)|
|Italian|&bullet; `it-IT` (Italy)|
|Japanese|&bullet; `ja-JP` (Japan)|
|Polish |`pl-PL` (Poland)|
|Portuguese|&bullet; `pt-BR` (Brazil)|
|Portuguese |`pt-PT` (Portugal)|
|Punjabi |`pa-IN` (India)|
|Russian |`ru-RU` (Russia)|
|Spanish|&bullet; `es-ES` (Spain)</br>&bullet; `es-MX` (Mexico) |
|Spanish |`es-US` (United States)|
|Swedish |`sv-SE` (Sweden)|
|Turkish |`tr-TR` (Türkiye)|
|Ukrainian |`uk-UA` (Ukraine)|

