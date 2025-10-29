---
title: Azure AI Content Understanding audio overview
titleSuffix: Azure AI services
description: Learn about Azure AI Content Understanding audio solutions
author: PatrickFarley 
ms.author: jagoerge
manager: nitinme
ms.date: 05/19/2025
ms.service: azure-ai-content-understanding
ms.topic: overview
ms.custom:
  - build-2025
---

# Azure AI Content Understanding audio solutions (preview)

> [!IMPORTANT]
> * Azure AI Content Understanding is available in preview. Public preview releases provide early access to features that are in active development.
> * Features, approaches, and processes can change or have limited capabilities, before General Availability (GA).
> * For more information, *see* [**Supplemental Terms of Use for Microsoft Azure Previews**](https://azure.microsoft.com/support/legal/preview-supplemental-terms).

Audio analyzers enable transcription and diarization of conversational audio, extracting structured fields such as summaries, sentiments, and key topics. Customize an audio analyzer template to your business needs using [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) to start generating results.

Here are common scenarios for conversational audio data processing:

* Gain customer insights through summarization and sentiment analysis.
* Assess and verify call quality and compliance in call centers.
* Create automated summaries and metadata for podcast publishing.

## Audio analyzer capabilities

:::image type="content" source="../media/audio/overview/workflow-diagram.png" lightbox="../media/audio/overview/workflow-diagram.png" alt-text="Illustration of Content Understanding audio capabilities.":::

Content Understanding serves as a cornerstone for Speech Analytics solutions, enabling the following capabilities for audio files:

### Content extraction

Audio content extraction is the process of transcribing audio files. This process includes separating transcriptions by speaker and can involve optional features like role detection to update speaker results to meaningful speaker roles. It can also involve detailed results including word-level timestamps.

#### Language handling
We support different options to handle language processing during transcription.

The following table provides an overview of the options controlled via the 'locales' configuration:

|Locale setting|File size|Supported processing|Supported locales|Result latency|
|--|--|--|--|--|
|**auto or empty**|≤ 300 MB and/or ≤ 2 hours|Multilingual transcription|`de-DE`, `en-AU`,` en-CA`, `en-GB`, `en-IN`, `en-US`, `es-ES`, `es-MX`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, and `zh-CN`|Near-real-time|
|**auto or empty**|> 300 MB and >2 HR ≤ 4 hours|Multilingual transcription|`en-US`, `es-ES`, `es-MX`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `zh-CN`|Regular|
|**single locale**|≤ 1 GB and/or ≤ 4 hours|Single language transcription|All supported locales[^1]|&bullet; ≤ 300 MB and/or ≤ 2 hours: Near-real-time<br>&bullet; > 300 MB and >2 HR ≤ 4 hours: Regular|
|**multiple locales**|≤ 1 GB and/or ≤ 4 hours|Single language transcription (based on language detection)|All supported locales[^1]|&bullet; ≤ 300 MB and/or ≤ 2 hours: Near-real-time<br>&bullet; > 300 MB and >2 HR ≤ 4 hours: Regular|

[^1]: Content Understanding supports the full set of [Azure AI Speech Speech to text languages](../../speech-service/language-support.md).
For languages with Fast transcriptions support and for files ≤ 300 MB and/or ≤ 2 hours, transcription time is reduced substantially.

* **Transcription**. Converts conversational audio into searchable and analyzable text-based transcripts in WebVTT format. Customizable fields can be generated from transcription data. Sentence-level and word-level timestamps are available upon request.

* **Diarization**. Distinguishes between speakers in a conversation, attributing parts of the transcript to specific speakers.

* **Speaker role detection**. Identifies agent and customer roles within contact center call data.

* **Multilingual transcription**. Generates multilingual transcripts, applying language/locale per phrase. Deviating from language detection this feature is enabled when no language/locale is specified or language is set to `auto`.

> [!NOTE]
> When Multilingual transcription is used, any files with unsupported locales produce a result based on the closest supported locale, which is likely incorrect. This result is a known
> behavior. Avoid transcription quality issues by ensuring that you configure locales when not using a multilingual transcription supported locale!

* **Language detection**. Automatically detects the dominant language/locale which is used to transcribe the file. Set multiple languages/locales to enable language detection.

### Field extraction

Field extraction allows you to extract structured data from audio files, such as summaries, sentiments, and mentioned entities from call logs. You can begin by customizing a suggested analyzer template or creating one from scratch.

## Key benefits

Advanced audio capabilities, including:

* **Customizable data extraction**. Tailor the output to your specific needs by modifying the field schema, allowing for precise data generation and extraction.

* **Generative models**. Utilize generative AI models to specify in natural language the content you want to extract, and the service generates the desired output.

* **Integrated pre-processing**. Benefit from built-in preprocessing steps like transcription, diarization, and role detection, providing rich context for generative models.

* **Scenario adaptability**. Adapt the service to your requirements by generating custom fields and extract relevant data.

## Prebuilt audio analyzers

The prebuilt analyzers allow extracting valuable insights into audio content without the need to create an analyzer setup.

All audio analyzers generate transcripts in standard WEBVTT format separated by speaker.

> [!NOTE]
> 
> Prebuilt analyzers are set to use multilingual transcription and `returnDetails` enabled.

The following prebuilt analyzers are available:

**Post-call analysis (prebuilt-callCenter)**. Analyze call recordings to generate:

* conversation transcripts with speaker role detection result
* call summary
* call sentiment
* top five articles mentioned
* list of companies mentioned
* list of people (name and title/role) mentioned
* list of relevant call categories

**Example result:**
```json
{
  "id": "bc36da27-004f-475e-b808-8b8aead3b566",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-callCenter",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-05-06T22:53:28Z",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Audio: 00:00.000 => 00:32.183\n\nTranscript\n```\nWEBVTT\n\n00:00.080 --> 00:00.640\n<v Agent>Good day.\n\n00:00.960 --> 00:02.240\n<v Agent>Welcome to Contoso.\n\n00:02.560 --> 00:03.760\n<v Agent>My name is John Doe.\n\n00:03.920 --> 00:05.120\n<v Agent>How can I help you today?\n\n00:05.440 --> 00:06.320\n<v Agent>Yes, good day.\n\n00:06.720 --> 00:08.160\n<v Agent>My name is Maria Smith.\n\n00:08.560 --> 00:11.280\n<v Agent>I would like to inquire about my current point balance.\n\n00:11.680 --> 00:12.560\n<v Agent>No problem.\n\n00:12.880 --> 00:13.920\n<v Agent>I am happy to help.\n\n00:14.240 --> 00:16.720\n<v Agent>I need your date of birth to confirm your identity.\n\n00:17.120 --> 00:19.600\n<v Agent>It is April 19th, 1988.\n\n00:20.000 --> 00:20.480\n<v Agent>Great.\n\n00:20.800 --> 00:24.160\n<v Agent>Your current point balance is 599 points.\n\n00:24.560 --> 00:26.160\n<v Agent>Do you need any more information?\n\n00:26.480 --> 00:27.200\n<v Agent>No, thank you.\n\n00:27.600 --> 00:28.320\n<v Agent>That was all.\n\n00:28.720 --> 00:29.280\n<v Agent>Goodbye.\n\n00:29.680 --> 00:30.320\n<v Agent>You're welcome.\n\n00:30.640 --> 00:31.840\n<v Agent>Goodbye at Contoso.\n```",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "Maria Smith contacted Contoso to inquire about her current point balance. After confirming her identity with her date of birth, the agent, John Doe, informed her that her balance was 599 points. Maria did not require any further assistance, and the call concluded politely."
          },
          "Topics": {
            "type": "array",
            "valueArray": [
              {
                "type": "string",
                "valueString": "Point balance inquiry"
              },
              {
                "type": "string",
                "valueString": "Identity confirmation"
              },
              {
                "type": "string",
                "valueString": "Customer service"
              }
            ]
          },
          "Companies": {
            "type": "array",
            "valueArray": [
              {
                "type": "string",
                "valueString": "Contoso"
              }
            ]
          },
          "People": {
            "type": "array",
            "valueArray": [
              {
                "type": "object",
                "valueObject": {
                  "Name": {
                    "type": "string",
                    "valueString": "John Doe"
                  },
                  "Role": {
                    "type": "string",
                    "valueString": "Agent"
                  }
                }
              },
              {
                "type": "object",
                "valueObject": {
                  "Name": {
                    "type": "string",
                    "valueString": "Maria Smith"
                  },
                  "Role": {
                    "type": "string",
                    "valueString": "Customer"
                  }
                }
              }
            ]
          },
          "Sentiment": {
            "type": "string",
            "valueString": "Positive"
          },
          "Categories": {
            "type": "array",
            "valueArray": [
              {
                "type": "string",
                "valueString": "Business"
              }
            ]
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 32183,
        "transcriptPhrases": [
          {
            "speaker": "Agent",
            "startTimeMs": 80,
            "endTimeMs": 640,
            "text": "Good day.",
            "words": []
          }, ...
          {
            "speaker": "Customer",
            "startTimeMs": 5440,
            "endTimeMs": 6320,
            "text": "Yes, good day.",
            "words": []
          }, ...
        ]
      }
    ]
  }
}
```

**Conversation analysis (prebuilt-audioAnalyzer)**. Analyze recordings to generate:
- conversation transcripts
- conversation summary

**Example result:**
```json
{
  "id": "9624cc49-b6b3-4ce5-be6c-e895d8c2484d",
  "status": "Succeeded",
  "result": {
    "analyzerId": "prebuilt-audioAnalyzer",
    "apiVersion": "2025-05-01-preview",
    "createdAt": "2025-05-06T23:00:12Z",
    "stringEncoding": "utf8",
    "warnings": [],
    "contents": [
      {
        "markdown": "# Audio: 00:00.000 => 00:32.183\n\nTranscript\n```\nWEBVTT\n\n00:00.080 --> 00:00.640\n<v Speaker 1>Good day.\n\n00:00.960 --> 00:02.240\n<v Speaker 1>Welcome to Contoso.\n\n00:02.560 --> 00:03.760\n<v Speaker 1>My name is John Doe.\n\n00:03.920 --> 00:05.120\n<v Speaker 1>How can I help you today?\n\n00:05.440 --> 00:06.320\n<v Speaker 1>Yes, good day.\n\n00:06.720 --> 00:08.160\n<v Speaker 1>My name is Maria Smith.\n\n00:08.560 --> 00:11.280\n<v Speaker 1>I would like to inquire about my current point balance.\n\n00:11.680 --> 00:12.560\n<v Speaker 1>No problem.\n\n00:12.880 --> 00:13.920\n<v Speaker 1>I am happy to help.\n\n00:14.240 --> 00:16.720\n<v Speaker 1>I need your date of birth to confirm your identity.\n\n00:17.120 --> 00:19.600\n<v Speaker 1>It is April 19th, 1988.\n\n00:20.000 --> 00:20.480\n<v Speaker 1>Great.\n\n00:20.800 --> 00:24.160\n<v Speaker 1>Your current point balance is 599 points.\n\n00:24.560 --> 00:26.160\n<v Speaker 1>Do you need any more information?\n\n00:26.480 --> 00:27.200\n<v Speaker 1>No, thank you.\n\n00:27.600 --> 00:28.320\n<v Speaker 1>That was all.\n\n00:28.720 --> 00:29.280\n<v Speaker 1>Goodbye.\n\n00:29.680 --> 00:30.320\n<v Speaker 1>You're welcome.\n\n00:30.640 --> 00:31.840\n<v Speaker 1>Goodbye at Contoso.\n```",
        "fields": {
          "Summary": {
            "type": "string",
            "valueString": "Maria Smith contacted Contoso to inquire about her current point balance. John Doe assisted her by confirming her identity using her date of birth and informed her that her balance was 599 points. Maria expressed no further inquiries, and the conversation concluded politely."
          }
        },
        "kind": "audioVisual",
        "startTimeMs": 0,
        "endTimeMs": 32183,
        "transcriptPhrases": [
          {
            "speaker": "Speaker 1",
            "startTimeMs": 80,
            "endTimeMs": 640,
            "text": "Good day.",
            "words": []
          }, ...
          {
            "speaker": "Speaker 2",
            "startTimeMs": 5440,
            "endTimeMs": 6320,
            "text": "Yes, good day.",
            "words": []
          }, ...
        ]
      }
    ]
  }
}
```

You can also customize prebuilt analyzers for more fine-grained control of the output by defining custom fields. Customization allows you to use the full power of generative models to extract deep insights from the audio. For example, customization allows you to:

* Generate other insights.
* Control the language of the field extraction output.
* Configure the transcription behavior.

## Conversational Knowledge Mining Solution Accelerator
For an end-2-end quickstart for Speech Analytics solutions, refer to the [Conversation knowledge mining solution accelerator](https://aka.ms/Conversational-Knowledge-Mining).

Gain actionable insights from large volumes of conversational data by identifying key themes, patterns, and relationships. By using Azure AI Foundry, Azure AI Content Understanding, Azure OpenAI in Azure AI Foundry Models, and Azure AI Search, this solution analyzes unstructured dialogue and maps it to meaningful, structured insights.

Capabilities such as topic modeling, key phrase extraction, speech-to-text transcription, and interactive chat enable users to explore data naturally and make faster, more informed decisions.

Analysts working with large volumes of conversational data can use this solution to extract insights through natural language interaction. It supports tasks like identifying customer support trends, improving contact center quality, and uncovering operational intelligence—enabling teams to spot patterns, act on feedback, and make informed decisions faster.

## Input requirements

For a detailed list of supported audio formats, *see* [Service limits and codecs](../service-limits.md).

## Supported languages and regions

For a complete list of supported regions, languages, and locales, see [Language and region support](../language-region-support.md).

## Data privacy and security

Developers using this service should review Microsoft's policies on customer data. For more information, *see* [Data, protection, and privacy](https://www.microsoft.com/trust-center/privacy).

## Next steps

* Try processing your audio content in the [**Azure AI Foundry portal**](https://aka.ms/cu-landing).
* Learn how to analyze audio content with [**analyzer templates**](../quickstart/use-ai-foundry.md).
* Review code samples: 
  * [**audio content extraction**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/blob/main/notebooks/content_extraction.ipynb).
  * [**analyzer templates**](https://github.com/Azure-Samples/azure-ai-content-understanding-python/tree/main/analyzer_templates).
