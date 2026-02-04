---
title: Azure OpenAI in Microsoft Foundry Models audio
titleSuffix: Azure OpenAI
description: Learn about the audio capabilities of Azure OpenAI.
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article 
ms.date: 11/21/2025
ms.custom: template-concept
manager: nitinme
---

# Audio capabilities in Azure OpenAI in Microsoft Foundry Models

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]


Audio models in Azure OpenAI are available via the `realtime`, `completions`, and `audio` APIs, and support speech recognition, translation, and text to speech.

For information about the available audio models per region in Azure OpenAI, see the [audio models](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio), [standard models by endpoint](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio), and [global standard model availability](../../foundry-models/concepts/models-sold-directly-by-azure.md?tabs=standard-audio) documentation.

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by audio models in Azure OpenAI, such as Whisper.

## GPT-4o audio Realtime API

GPT real-time audio supports real-time, low-latency conversational interactions for scenarios that require responsive bidirectional audio exchange. For more information on how to use GPT real-time audio, see the [GPT real-time audio quickstart](../realtime-audio-quickstart.md) and [how to use GPT-4o audio](../how-to/realtime-audio.md).

## GPT-4o audio completions

GPT-4o audio completion generates audio outputs from audio or text prompts. The GPT-4o audio completions model introduces the audio modality into the existing `/chat/completions` API. For more information on how to use GPT-4o audio completions, see the [audio generation quickstart](../audio-completions-quickstart.md).

## Audio API

The audio models via the `/audio` API can be used for speech to text, translation, and text to speech. To get started with the audio API, see the [Whisper quickstart](../whisper-quickstart.md) for speech to text.

> [!NOTE]
> To help you decide whether to use Azure Speech in Foundry Tools or Azure OpenAI, see the [Azure Speech batch transcription](../../../ai-services/speech-service/batch-transcription-create.md), [What is the Whisper model?](../../../ai-services/speech-service/whisper-overview.md), and [OpenAI text to speech voices](../../../ai-services/speech-service/openai-voices.md#openai-text-to-speech-voices-via-azure-openai-or-via-azure-speech) guides.

## Related content

- [Audio models](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models)
- [Whisper quickstart](../whisper-quickstart.md)
- [Audio generation quickstart](../audio-completions-quickstart.md)
- [GPT real-time audio quickstart](../realtime-audio-quickstart.md)