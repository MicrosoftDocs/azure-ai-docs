---
title: Use the fast transcription API - Speech service
titleSuffix: Foundry Tools
description: Learn how to use Azure Speech in Foundry Tools for fast transcriptions, where you submit audio get the transcription results faster than real-time.
manager: nitinme
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 01/31/2026
zone_pivot_groups: fast-transcription-quickstart
# Customer intent: As a user who implements audio transcription, I want create transcriptions as quickly as possible.
---

# Use the fast transcription API with Azure Speech in Foundry Tools 

Fast transcription API is used to transcribe audio files with returning results synchronously and faster than real-time. Use fast transcription in the scenarios that you need the transcript of an audio recording as quickly as possible with predictable latency, such as: 

- Quick audio or video transcription, subtitles, and edit. 
- Meeting notes
- Voicemail

Unlike the batch transcription API, fast transcription API only produces transcriptions in the display (not lexical) form. The display form is a more human-readable form of the transcription that includes punctuation and capitalization.

> [!TIP]
> You can also use the latest LLM-powered speech transcription and speech translation with [LLM speech](./llm-speech.md).

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](includes/common/transcription-rest-api.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/common/transcription-sdk-python.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK quickstart](includes/common/transcription-sdk-java.md)]

::: zone-end

## Related content

- [Fast transcription REST API reference](/rest/api/speechtotext/transcriptions/transcribe)
- [Speech to text supported languages](./language-support.md?tabs=stt)
- [Batch transcription](./batch-transcription.md)
