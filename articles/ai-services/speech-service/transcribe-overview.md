---
title: Transcription models from OpenAI
titleSuffix: Foundry Tools
description: In this article, you learn about OpenAI transcription models that you can use for speech to text and speech translation.
author: PatrickFarley
reviewer: patrickfarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: concept-article
ms.custom: dev-focus
ms.date: 07/27/2026
ai-usage: ai-assisted
ms.author: pafarley
ms.reviewer: pafarley
#Customer intent: As a developer, I want to learn about OpenAI transcription models that I can use for speech to text and speech translation.
---

# What are OpenAI transcription models?

OpenAI transcription models are speech-to-text models that you can use to transcribe audio files in English or translate audio from other languages into English.

You can access transcription models through Azure OpenAI in Microsoft Foundry Models or through Azure Speech in Foundry Tools. The features differ for those offerings. In [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model), the OpenAI transcription model is one of several models that you can use for speech-to-text.

## Choose a workflow

- **Offline (file-based)**: Upload a complete prerecorded file and receive one completed transcript.
- **Realtime (streaming)**: Stream audio continuously and receive transcript updates while audio is still in progress.

## Offline transcription workflow

For offline transcription in Foundry Models, use the Audio API transcription path (`POST /v1/audio/transcriptions`). Current model IDs include `whisper` and `gpt-transcribe`.

The Audio API transcription path is the HTTP route for file-based transcription. Depending on the endpoint format that you use, the route is either `/audio/transcriptions` (deployment-style endpoints) or `/openai/v1/audio/transcriptions` (v1 endpoints).

To get started with offline workflows, see:
- [Speech-to-text quickstart via Azure OpenAI transcription models](../../foundry/openai/whisper-quickstart.md)
- [Batch transcription with transcription models via Azure Speech](./batch-transcription-create.md#use-a-whisper-model)

### Offline language hints

For offline transcription, set a language hint when you know the expected language. Language hints can improve stability for short or noisy audio.

The following example shows the `language` form field with a transcription request:

```bash
curl $AZURE_OPENAI_ENDPOINT/openai/deployments/YourDeploymentName/audio/transcriptions?api-version=2025-03-01-preview \
 -H "api-key: $AZURE_OPENAI_API_KEY" \
 -H "Content-Type: multipart/form-data" \
 -F file="@./sample.wav" \
 -F language="en"
```

If you use the v1 endpoint format, call `POST /openai/v1/audio/transcriptions`.

## Realtime transcription workflow

`gpt-transcribe` is an offline transcription model and isn't a Realtime API model. For real-time streaming transcription, use GPT Realtime Transcribe or GPT Live Transcribe models.

Get started with realtime workflows:
- [Real-time speech-to-text quickstart via Azure Speech](./get-started-speech-to-text.md)

## Compare offline and realtime transcription

Use offline and realtime transcription for different workloads.

| Area | Offline transcription (`gpt-transcribe`) | Realtime transcription (`gpt-realtime-whisper`, `gpt-live-transcribe`) |
|---|---|---|
| API interaction model | One HTTP request per file, then one response. | Long-lived realtime session with streaming events. |
| Audio input pattern | Upload a complete prerecorded file. | Stream audio chunks from a live source. |
| Result pattern | Returns a completed transcript after processing. | Returns incremental transcript updates as audio arrives. |
| Latency profile | Better for file workflows where end-to-end latency isn't critical. | Better for low-latency live scenarios such as captions and monitoring. |
| Typical scenarios | Prerecorded media processing, post-call transcription, and async pipelines. | Live captions, voice agents, and interactive real-time experiences. |

## Transcription models vs. Azure Speech models

Choose the model that best fits your scenario. The following table summarizes recommendations. If you use Azure Speech, you can choose from several models, including OpenAI transcription models.

| Scenario | OpenAI transcription model | Azure Speech models |
|---------|---------------|------------------------|
| Real-time transcriptions, captions, and subtitles for audio and video. | Not available | Recommended |
| Transcriptions, captions, and subtitles for prerecorded audio and video. | The transcription model via [Azure OpenAI](../../foundry/openai/whisper-quickstart.md) is recommended for fast processing of individual audio files. The transcription model via [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model) is recommended for batch processing of large files. For more information, see [Transcription models via Azure Speech batch transcription or via Azure OpenAI?](#transcription-models-via-azure-speech-or-via-azure-openai) | Recommended for batch processing of large files, diarization, and word-level timestamps. |
| Transcript of phone call recordings and analytics such as call summary, sentiment, key topics, and custom insights. | Available | Recommended |
| Real-time transcription and analytics to assist call center agents with customer questions. | Not available | Recommended |
| Transcript of meeting recordings and analytics such as meeting summary, meeting chapters, and action item extraction. | Available | Recommended |
| Real-time text entry and document generation through voice dictation. | Not available | Recommended |
| Contact center voice agent: Call routing and interactive voice response for call centers.​ | Available | Recommended |
| Voice assistant: Application specific voice assistant for a set-top box, mobile app, in-car, and other scenarios. | Available | Recommended |
| Pronunciation assessment: Assess the pronunciation of a speaker's voice. | Not available | Recommended |
| Translate live audio from one language to another. | Not available | Recommended via the [speech translation API](./speech-translation.md). |
| Translate prerecorded audio from other languages into English. | Recommended | Also available via the [speech translation API](./speech-translation.md). |
| Translate prerecorded audio into languages other than English. | Not available | Recommended via the [speech translation API](./speech-translation.md). |



## Transcription models via Azure Speech or via Azure OpenAI?

If you decide to use a transcription model, you have two options. You can choose whether to use a transcription model via [Azure OpenAI](../../foundry/openai/whisper-quickstart.md) or via [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model). In either case, the readability of the transcribed text is the same.

Transcription models via Azure OpenAI might be best for:
- Quickly transcribing audio files one at a time.
- Translate audio from other languages into English. You can input mixed language audio and the output is in English. 
- Provide a prompt to the model to guide the output.
- Supported file formats: mp3, mp4, mpeg, mpga, m4a, wav, and webm.
- Only ASCII character supported for filename.

Transcription models via Azure Speech batch transcription might be best for:
- Transcribing files larger than 25 MB (up to 1 GB). The file size limit for the Azure OpenAI transcription model is 25 MB.
- Transcribing large batches of audio files.
- Diarization to distinguish between the different speakers participating in the conversation. The Speech service provides information about which speaker was speaking a particular part of transcribed speech. The transcription model via Azure OpenAI doesn't support diarization.
- Word-level timestamps.
- Supported file formats: mp3, wav, and ogg.

Regional support is another consideration.
- For the current list of regions where the transcription model is available, see the [Speech service regions table](regions.md?tabs=stt).

## Related content

- [Use transcription models via the Azure Speech batch transcription API](./batch-transcription-create.md#use-a-whisper-model)
- [Try the speech-to-text quickstart for transcription models via Azure OpenAI](../../foundry/openai/whisper-quickstart.md)
- [Try the real-time speech-to-text quickstart via Azure Speech](./get-started-speech-to-text.md)
