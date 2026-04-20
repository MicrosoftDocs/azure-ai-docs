---
title: Use the LLM Speech API - Speech Service
titleSuffix: Foundry Tools
description: Learn how to use Azure Speech with the latest LLM-powered speech model for transcription and translation.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/15/2025
zone_pivot_groups: llm-speech-quickstart
# Customer intent: As a user who implements audio transcription, I want create transcriptions as quickly as possible.
---

# LLM Speech for speech transcription and translation (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

LLM Speech is an API in Microsoft Foundry. It's powered by a speech model that's enhanced by a large language model (LLM). LLM Speech delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It uses GPU acceleration for ultra-fast inference, making it ideal for a wide range of scenarios. For example, use LLM Speech to generate captions and subtitles from audio files, summarize meeting notes, assist call center agents, and transcribe voicemails.

[!INCLUDE [transcription-features](includes/transcription-features.md)]

::: zone pivot="ai-foundry"

[!INCLUDE [Foundry portal](includes/common/llm-speech-ai-foundry.md)]

::: zone-end

::: zone pivot="programming-language-rest"

[!INCLUDE [REST API quickstart](includes/common/llm-speech-rest-api.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK quickstart](includes/common/llm-speech-sdk-python.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# SDK quickstart](includes/common/llm-speech-sdk-csharp.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript SDK quickstart](includes/common/llm-speech-sdk-javascript.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Java SDK quickstart](includes/common/llm-speech-sdk-java.md)]

::: zone-end

[!INCLUDE [error-handling](includes/quickstarts/speech-to-text-basics/error-handling.md)]

## Related content

- [LLM Speech REST API reference](/rest/api/speechtotext/transcriptions/transcribe)
- [Fast transcription](fast-transcription-create.md)
