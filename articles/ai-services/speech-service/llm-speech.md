---
title: Use the LLM-speech API - Speech service
titleSuffix: Foundry Tools
description: Learn how to use Azure Speech in Foundry Tools for LLM-speech, where you can leverage the latest LLM-powered speech model for transcription and translation
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/15/2025
zone_pivot_groups: llm-speech-quickstart
# Customer intent: As a user who implements audio transcription, I want create transcriptions as quickly as possible.
---

# LLM speech for speech transcription and translation (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

LLM speech is powered by a large-language-model-enhanced speech model that delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It uses GPU acceleration for ultra-fast inference, making it ideal for a wide range of scenarios including generating captions and subtitles from audio files, summarizing meeting notes, assisting call center agents, transcribing voicemails, and more.

The LLM speech API currently supports the following speech tasks:
- `transcribe`
- `translate`

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](includes/common/llm-speech-rest-api.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/common/llm-speech-sdk-python.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK quickstart](includes/common/llm-speech-sdk-java.md)]

::: zone-end

> [!NOTE]
> Speech service is an elastic service. If you receive 429 error code (too many requests), please follow the [best practices to mitigate throttling during autoscaling](speech-services-quotas-and-limits.md#general-best-practices-to-mitigate-throttling-during-autoscaling).

## Related content

- [LLM speech REST API reference](/rest/api/speechtotext/transcriptions/transcribe)
- [Fast transcription](fast-transcription-create.md)
