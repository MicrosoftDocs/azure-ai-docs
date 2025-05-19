---
title: Azure OpenAI in Azure AI Foundry Models audio
titleSuffix: Azure OpenAI
description: Learn about the audio capabilities of Azure OpenAI.
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 4/15/2025
ms.custom: template-concept
manager: nitinme
---

# Audio capabilities in Azure OpenAI in Azure AI Foundry Models

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by the audio models such as Whisper in Azure OpenAI. 

Audio models in Azure OpenAI are available via the `realtime`, `completions`, and `audio` APIs. The audio models are designed to handle a variety of tasks, including speech recognition, translation, and text to speech.

For information about the available audio models per region in Azure OpenAI, see the [audio models](models.md?tabs=standard-audio#standard-deployment-regional-models-by-endpoint), [standard models by endpoint](models.md?tabs=standard-audio#standard-deployment-regional-models-by-endpoint), and [global standard model availability](models.md?tabs=standard-audio#global-standard-model-availability) documentation.

## GPT-4o audio Realtime API

GPT-4o real-time audio is designed to handle real-time, low-latency conversational interactions, making it a great fit for support agents, assistants, translators, and other use cases that need highly responsive back-and-forth with a user. For more information on how to use GPT-4o real-time audio, see the [GPT-4o real-time audio quickstart](../realtime-audio-quickstart.md) and [how to use GPT-4o audio](../how-to/realtime-audio.md).

## GPT-4o audio completions

GPT-4o audio completion is designed to generate audio from audio or text prompts, making it a great fit for generating audio books, audio content, and other use cases that require audio generation. The GPT-4o audio completions model introduces the audio modality into the existing `/chat/completions` API. For more information on how to use GPT-4o audio completions, see the [audio generation quickstart](../audio-completions-quickstart.md).

## Audio API

The audio models via the `/audio` API can be used for speech to text, translation, and text to speech. To get started with the audio API, see the [Whisper quickstart](../whisper-quickstart.md) for speech to text.

> [!NOTE]
> To help you decide whether to use Azure AI Speech or Azure OpenAI, see the [Azure AI Speech batch transcription](../../speech-service/batch-transcription-create.md), [What is the Whisper model?](../../speech-service/whisper-overview.md), and [OpenAI text to speech voices](../../speech-service/openai-voices.md#openai-text-to-speech-voices-via-azure-or-via-azure-ai-speech) guides.

## Related content

- [Audio models](models.md#audio-models)
- [Whisper quickstart](../whisper-quickstart.md)
- [Audio generation quickstart](../audio-completions-quickstart.md)
- [GPT-4o real-time audio quickstart](../realtime-audio-quickstart.md)
