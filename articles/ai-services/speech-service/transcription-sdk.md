---
title: About the Speech Transcription SDK - Speech service
titleSuffix: Foundry Tools
description: The Speech Transcription software development kit (SDK) exposes the LLM Speech and Fast Transcription capabilities of the Speech Service, making it easier to develop high quality transcription applications.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 01/13/2026
ms.author: pafarley
#Customer intent: As a developer, I want to learn about the Speech Transcription SDK.
---

# What is the Speech Transcription SDK?

The Speech Transcription software development kit (SDK) exposes the LLM Speech and Fast Transcription capabilities of the Speech Service, making it easier to develop high quality transcription applications.
The Speech Transcription SDK is available [in many programming languages](#supported-languages) and across platforms. The Speech Transcription SDK is ideal for near-real-time and non-real-time scenarios, by using local device captured audio, files, and Azure Blob Storage data.

In some cases, you can't or shouldn't use the [Speech Transcription SDK](./transcription-sdk.md). In those cases, you can use real-time streaming via WebSockets or REST APIs to access the Speech service. For example use the [Speech SDK](speech-sdk.md) for real-time streaming, or use the [Speech to text REST API](rest-speech-to-text.md) for [batch transcription](batch-transcription.md) of high-volume processing and [custom speech](custom-speech-overview.md) model management.

## Supported languages

The Speech Transcription SDK supports the following languages and platforms:

| Programming language | Reference | Platform support |
|----------------------|-----------|------------------|
| Java | [Java](/java/api/overview/azure/ai-speech-transcription-readme) | Android, Windows, Linux, macOS |
| Python | [Python](/python/api/overview/azure/ai-transcription-readme) | Windows, Linux, macOS |

## Code samples

Speech Transcription SDK code samples are available in the documentation and GitHub. 

### Docs samples

At the top of documentation pages that contain samples use the options to select your programming language.

:::image type="content" source="./media/sdk/pivot-programming-languages-speech-sdk.png" alt-text="Screenshot showing how to select a programming language in the documentation.":::

If a sample isn't available in your preferred programming language, you can select another programming language to get started and learn about the concepts, or see the reference and samples linked from the beginning of the article.

### GitHub samples

You can find samples for each programming language in the respective GitHub repositories.

| Programming language | Samples Repository |
|----------------------|--------------------|
| Java | [Java Samples](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/transcription/azure-ai-speech-transcription/src/samples/java/com/azure/ai/speech/transcription/README.md) |
| Python | [Python Samples](https://github.com/Azure/azure-sdk-for-python/tree/azure-ai-transcription_1.0.0b2/sdk/cognitiveservices/azure-ai-transcription/samples) |

## Help options

The developer community can use the [Stack Overflow](https://stackoverflow.com/questions/tagged/azure-speech) forums to ask and answer questions about Azure Cognitive Speech and other services. Microsoft monitors the forums and replies to questions that the community didn't yet answer. To make sure that Microsoft sees your question, tag it with 'azure-speech'.

You can suggest an idea or report a bug by creating an issue on GitHub.

See also [Foundry Tools support and help options](../cognitive-services-support-options.md?context=/azure/ai-services/speech-service/context/context) to get support, stay up-to-date, give feedback, and report bugs for Foundry Tools.

## Next steps

* [Try the Fast Transcription API](./fast-transcription-create.md)
- [Try LLM Speech API](./llm-speech.md)
