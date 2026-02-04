---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/21/2025
---

The `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` models introduce the audio modality into the existing `/chat/completions` API. The audio model expands the potential for AI applications in text and voice-based interactions and audio analysis. Modalities supported in `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` models include:  text, audio, and text + audio.

Here's a table of the supported modalities with example use cases:

| Modality input | Modality output | Example use case |
| --- | --- | --- |
| Text | Text + audio | Text to speech, audio book generation |
| Audio | Text + audio | Audio transcription, audio book generation |
| Audio | Text | Audio transcription |
| Text + audio | Text + audio | Audio book generation |
| Text + audio | Text | Audio transcription |

By using audio generation capabilities, you can achieve more dynamic and interactive AI applications. Models that support audio inputs and outputs allow you to generate spoken audio responses to prompts and use audio inputs to prompt the model. 

## Supported models

Currently only `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` version: `2024-12-17` supports audio generation.

For more information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).

Currently the following voices are supported for audio out: Alloy, Echo, and Shimmer.

The maximum audio file size is 20 MB.

> [!NOTE]
> The [Realtime API](../realtime-audio-quickstart.md) uses the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions.

## API support

Support for audio completions was first added in API version `2025-01-01-preview`. 
