---
title: Azure AI Content Understanding audio overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding audio solutions
author: laujan
ms.author: lajanuar
manager: nitinme
ms.service: azure
ms.topic: overview
ms.date: 11/19/2024
ms.custom: ignite-2024-understanding-release
---


# Content Understanding audio solutions (preview)

> [!IMPORTANT]
>
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes may change or have constrained capabilities, prior to General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Content Understanding audio capabilities enable you to transcribe and diarize conversational audio. It can generate enhanced outputs like summaries, special industry record formats, captioning data. Content Understanding audio and audio capabilities enable you to extract valuable information such as key topics, sentiment, and more. To get started, use one of the provided out-of-box prebuilt extraction schemas and start generating results. You can also customize Content Understanding capabilities to meet your business needs as necessary.

Here are some of the common scenarios for Content Understanding extracted conversational audio data:

* Get customer insights through summarization and sentiment.

* Generate contact center call analytics results.

* Assess and verify contact center call quality and compliance for improved processing coverage.

* Generate automated summaries and metadata for podcast platform publishing.

* Create a redacted version of the transcript with personal data removed.

* Analyze recordings to find valuable information like most desired topics.

* Generate rich outputs based on conversational audio such as dictated documents.

## Content Understanding in AI Studio

AI studio enables you to set up, test, and manage Content Understanding solutions. You can use prebuilt schemas that can be customized to analyze your audio transcripts to easily generate results matching your specific business needs. A typical scenario is to automatically process files uploaded into a blob storage account and write the analytics results back to it. Based on the single file analysis, you can then easily index and add these results to a database or an Azure AI Search Index to easily generate more cross-recording insights and dashboards.

* Get insights from audio recordings of meetings, calls, and conversations. Review insights from summaries, sentiment results, action items, meeting notes, and `PII` redacted transcripts.

* Customize the results according to your specific needs and scenarios to modify the output of the workflow.

* Test and deploy customized workflows easily and quickly, without having to write any code or use any external tools.

* Access and manage your Content Understanding projects and resources in one place, along with other AI services that you use in AI Studio.

You can use the AI Studio to manage audio analytics projects and resources.

* Content Understanding in AI studio offers a user-friendly interface and a seamless setup experience to generate insights from audio data. You can also test and deploy different versions of the output schema directly in AI studio.

* Developers can use the `SDK`s and `REST API`s to process data at scale in production and integrate Content Understanding into Azure Pipelines as needed.

## Content Understanding features for audio processing

Content Understanding is serves as a cornerstone for Media Asset Management solutions and enables the following capabilities for audio files:

* **Extracting content**:

   * **Transcription**. Convert audio within conversational audio files into text-based transcripts that can be searched and analyzed. This transcription data is also used as grounding for generating customizable fields.

   * **Diarization**. Speaker diarization distinguishes between the speakers participating in a conversation. The Content Understanding service provides information about which part of a transcribed conversation is attributed to a particular speaker.

   * **Speaker Role Detection**. Detect and identify agent and customer speaker roles within contact center call data.

   * **Supported languages**. Content Understanding audio capabilities support automatic language detection for [**supported languages**](../language-region-support.md#language-support). The feature is automatically active if no locale or multiple locales are selected.

  * **Supported audio formats**. Content Understanding audio capabilities support a broad variety of [audio file formats and codes](../language-region-support.md).

  * **Audio transcription detailed output**. The complete output from the audio transcription process is returned including, if needed, sentence-level and word-level-timestamps.

* **Generating fields**:

   * **Field generation**. Content Understanding enables you to define custom fields and extract and generate data from your audio by including them in the schema definition.

  * **Multi-language results**. Content Understanding can generate field schema results in multiple languages when you include a field description in the desired output language.

  * **Support for `generate` and `classify` methods for field extraction**. Customize your output formats using user-specified extraction methods.

## Content Understanding audio workflow

The following diagram provides a high-level overview of a typical Content Understanding Audio processing workflow.

  :::image type="content" source="../media/audio/overview/workflow-diagram.png" lightbox="../media/audio/overview/workflow-diagram.png" alt-text="Illustration of Content Understanding audio workflow.":::

A typical Content Understanding Audio workflow consists of the following steps:

1. You send audio or transcription files to the Content UnderstandingAPI wither as single file or providing settings to process from a connected blob storage account.

1. Content UnderstandingContent Extraction generates a conversation transcript incl. speaker separation in webVTT format and optionally recognizes speaker roles or names to replace generic 'Speaker n' results.

1. The Content UnderstandingField Extraction then generates added insights based on the generated conversation transcript.

1. The Content Understanding service returns an audio file results containing the conversation transcript including added generated insights in JSON format. The results are either directly returned from the API or can be written into a connected blob storage account.

## Content Understanding prebuilt audio scenarios

Content Understanding provides the following customizable prebuilt scenario templates:

* **Post call analytics**. Analyze call recordings and generate outputs such as conversation transcript, call summary, sentiment assessment and more.

* **Conversation summarization**. Generate transcriptions from conversation audio recordings, generate a summary, and assess sentiment.

 You can start with any prebuilt scenario or start from scratch to get started and customize as needed to meet your business needs.

## Audio format support and input requirements

For a complete list of  Content Understanding supported audio formats, *see* our [Service limits and codecs](../service-limits.md) page.

## Supported regions, languages, and locales

For a complete list of supported regions, languages, and locales, see our [Language and region support](../language-region-support.md)) page.


## Content Understanding audio capability limits

|Attribute|Limit|
|-----|-----|
|Time|Maximum of 2 hours in length|
|Size|Maximum of 200 MB in size|
|Speakers|Maximum number of 36 speakers|

## Key Benefits

Content Understanding provides a specific set of capabilities for audio including:

* **Highly customizable data extraction**. Unlike traditional audio analysis services, Content Understanding allows you to customize the data you want to generate or extract. By modifying the schema, you can tailor the output to match your specific use cases.

* **Generative Models**. You can use our generative AI models to describe in natural language what content you want to extract, and the service generates that output.

* **Integrated Pre-processing**. The service performs several preprocessing steps, such as transcription, diarization and role detection, to provide rich context to the generative models.

* **Scenarios adaptability**. The service can adapt to your needs by generating custom fields to extract the right data.

## Data privacy and security

As with all the Azure AI services, developers using the Content Understanding service should be aware of Microsoft's policies on customer data. See our [**Data, protection and privacy**](https://www.microsoft.com/trust-center/privacy) page to learn more.

## Next steps

To get started using Content Understanding audio capabilities, try our [post-call analytics prebuilt scenario template](../prebuilt-template/post-call-analytics.md).

