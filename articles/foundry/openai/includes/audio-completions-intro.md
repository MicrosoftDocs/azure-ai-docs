---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 1/21/2025
---

Audio-enabled models introduce the audio modality into the existing `/chat/completions` API. The audio model expands the potential for AI applications in text and voice-based interactions and audio analysis. Modalities supported in `gpt-4o-audio-preview` and `gpt-4o-mini-audio-preview` models include: text, audio, and text + audio.

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

The following OpenAI models support audio generation:

| Model | Audio generation? | Primary Use |
| -- | -- | -- |
|`gpt-4o-audio-preview` | ✔️ | Chat completions with spoken output |
|`gpt-4o-mini-tts` | ✔️ | Fast, scalable text-to-speech |
|`gpt-4o-mini-audio-preview` | ✔️ | Asynchronous audio generation |
|`gpt-realtime` | ✔️ | Real‑time interactive voice |
|`gpt-realtime-mini` | ✔️ | Low‑latency audio streaming |
|`tts-1` / `tts-1-hd` | ✔️ | General‑purpose speech synthesis |

For information about region availability, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md).

> [!NOTE]
> The [Realtime API](../realtime-audio-quickstart.md) uses the same underlying GPT-4o audio model as the completions API, but is optimized for low-latency, real-time audio interactions.

## Input requirements

The following voices are supported for audio out: Alloy, Ash, Ballad, Coral, Echo, Sage, Shimmer, Verse, Marin, and Cedar.

The following audio output formats are supported: wav, mp3, flac, opus, pcm16, and aac.

The maximum audio file size is 20 MB.


## API support

Support for audio completions was first added in API version `2025-01-01-preview`. 
