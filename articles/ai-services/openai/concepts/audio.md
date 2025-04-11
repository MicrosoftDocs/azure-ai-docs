---
title: Azure OpenAI Service audio
titleSuffix: Azure OpenAI
description: Learn about the audio capabilities of Azure OpenAI Service.
author: eric-urban
ms.author: eur
ms.service: azure-ai-openai
ms.topic: conceptual 
ms.date: 4/15/2025
ms.custom: template-concept
manager: nitinme
---

# Audio capabilities in Azure OpenAI Service

> [!IMPORTANT]
> The content filtering system isn't applied to prompts and completions processed by the audio models such as Whisper in Azure OpenAI Service. Learn more about the [Audio API in Azure OpenAI](models.md?tabs=standard-audio#standard-models-by-endpoint).


### GPT-4o audio models

The GPT 4o audio models are part of the GPT-4o model family and support either low-latency, "speech in, speech out" conversational interactions or audio generation. 
- GPT-4o real-time audio is designed to handle real-time, low-latency conversational interactions, making it a great fit for support agents, assistants, translators, and other use cases that need highly responsive back-and-forth with a user. For more information on how to use GPT-4o real-time audio, see the [GPT-4o real-time audio quickstart](../realtime-audio-quickstart.md) and [how to use GPT-4o audio](../how-to/realtime-audio.md).
- GPT-4o audio completion is designed to generate audio from audio or text prompts, making it a great fit for generating audio books, audio content, and other use cases that require audio generation. The GPT-4o audio completions model introduces the audio modality into the existing `/chat/completions` API. For more information on how to use GPT-4o audio completions, see the [audio generation quickstart](../audio-completions-quickstart.md).

> [!CAUTION]
> We don't recommend using preview models in production. We will upgrade all deployments of preview models to either future preview versions or to the latest stable GA version. Models that are designated preview don't follow the standard Azure OpenAI model lifecycle.

To use GPT-4o audio, you need [an Azure OpenAI resource](../how-to/create-resource.md) in one of the [supported regions](#global-standard-model-availability).

When your resource is created, you can [deploy](../how-to/create-resource.md#deploy-a-model) the GPT-4o audio model. 

Details about maximum request tokens and training data are available in the following table.

|  Model ID  | Description | Max Request (tokens) | Training Data (up to)  |
|---|---|---|---|
|`gpt-4o-mini-audio-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for audio and text generation. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-mini-realtime-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-audio-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for audio and text generation. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-realtime-preview` (2024-12-17) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |
|`gpt-4o-realtime-preview` (2024-10-01) <br> **GPT-4o audio** | **Audio model** for real-time audio processing. |Input: 128,000  <br> Output: 4,096 | Oct 2023 |

To compare the availability of GPT-4o audio models across all regions, see the [models table](#global-standard-model-availability).

### Audio API

The audio models via the `/audio` API can be used for speech to text, translation, and text to speech. 

#### Speech to text models

|  Model ID  | Description | Max Request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |
| `gpt-4o-transcribe` | Speech to text powered by GPT-4o. | 25 MB|
| `gpt-4o-mini-transcribe` | Speech to text powered by GPT-4o mini. | 25 MB|

You can also use the Whisper model via Azure AI Speech [batch transcription](../../speech-service/batch-transcription-create.md) API. Check out [What is the Whisper model?](../../speech-service/whisper-overview.md) to learn more about when to use Azure AI Speech vs. Azure OpenAI Service. 

#### Speech translation models

|  Model ID  | Description | Max Request (audio file size) |
| ----- | ----- | ----- |
| `whisper` | General-purpose speech recognition model. | 25 MB |

#### Text to speech models (Preview)

|  Model ID  | Description |
|  --- | :--- |
| `tts` | Text to speech optimized for speed. |
| `tts-hd` | Text to speech optimized for quality.|
| `gpt-4o-mini-tts` | Text to speech model powered by GPT-4o mini. |

You can also use the OpenAI text to speech voices via Azure AI Speech. To learn more, see [OpenAI text to speech voices via Azure OpenAI Service or via Azure AI Speech](../../speech-service/openai-voices.md#openai-text-to-speech-voices-via-azure-openai-service-or-via-azure-ai-speech) guide. 

For more information see [Audio models region availability](?tabs=standard-audio#standard-models-by-endpoint) in this article.


## Related content

