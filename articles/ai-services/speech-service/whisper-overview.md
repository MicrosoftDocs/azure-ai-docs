---
title: The Whisper model from OpenAI
titleSuffix: Foundry Tools
description: In this article, you learn about the Whisper model from OpenAI that you can use for speech to text and speech translation.
author: PatrickFarley
reviewer: patrickfarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 10/21/2025
ms.author: pafarley
ms.reviewer: pafarley
#Customer intent: As a developer, I want to learn about the Whisper model from OpenAI that I can use for speech to text and speech translation.
---

# What is the Whisper model?

The Whisper model is a speech to text model from OpenAI that you can use to transcribe or translate audio files. The model is trained on a large dataset of English audio and text. 
- The model is optimized for transcribing audio files that contain speech in English. 
- The model can also be used to translate audio files that contain speech in other languages. The output of the transcription is English text.

Whisper models are available via the Azure OpenAI in Microsoft Foundry Models or via Azure Speech in Foundry Tools. The features differ for those offerings. In [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model), Whisper is just one of several models that you can use for speech to text.

You might ask:

- Is the Whisper Model a good choice for my scenario, or is an Azure Speech model better? What are the API comparisons between the two types of models?

- If I want to use the Whisper Model, should I use it via the Azure OpenAI or via Azure Speech ? What are the scenarios that guide me to use one or the other?

## Whisper model or Azure Speech models

Either the Whisper model or the Azure Speech models are appropriate depending on your scenarios. If you decide to use Azure Speech, you can choose from several models, including the Whisper model. The following table compares options with recommendations about where to start.

| Scenario | Whisper model | Azure Speech models |
|---------|---------------|------------------------|
| Real-time transcriptions, captions, and subtitles for audio and video. | Not available | Recommended |
| Transcriptions, captions, and subtitles for prerecorded audio and video. | The Whisper model via [Azure OpenAI](../../ai-foundry/openai/whisper-quickstart.md) is recommended for fast processing of individual audio files. The Whisper model via [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model) is recommended for batch processing of large files. For more information, see [Whisper model via Azure Speech batch transcription or via Azure OpenAI?](#whisper-model-via-azure-speech-or-via-azure-openai) | Recommended for batch processing of large files, diarization, and word level timestamps. |
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

## Whisper model via Azure Speech or via Azure OpenAI?

If you decide to use the Whisper model, you have two options. You can choose whether to use the Whisper Model via [Azure OpenAI](../../ai-foundry/openai/whisper-quickstart.md) or via [Azure Speech (batch transcription)](./batch-transcription-create.md#use-a-whisper-model). In either case, the readability of the transcribed text is the same. 

Whisper Model via Azure OpenAI might be best for:
- Quickly transcribing audio files one at a time.
- Translate audio from other languages into English. You can input mixed language audio and the output is in English. 
- Provide a prompt to the model to guide the output.
- Supported file formats: mp3, mp4, mpweg, mpga, m4a, wav, and webm.
- Only ASCII character supported for filename.

Whisper Model via Azure Speech batch transcription might be best for:
- Transcribing files larger than 25MB (up to 1GB). The file size limit for the Azure OpenAI Whisper model is 25 MB.
- Transcribing large batches of audio files.
- Diarization to distinguish between the different speakers participating in the conversation. The Speech service provides information about which speaker was speaking a particular part of transcribed speech. The Whisper model via Azure OpenAI doesn't support diarization.
- Word-level timestamps
- Supported file formats: mp3, wav, and ogg.

Regional support is another consideration. 
- For the current list of regions where the Whisper model is available, see the [Speech service regions table](regions.md?tabs=stt).

## Related content

- [Use Whisper models via the Azure Speech batch transcription API](./batch-transcription-create.md#use-a-whisper-model)
- [Try the speech to text quickstart for Whisper via Azure OpenAI](../../ai-foundry/openai/whisper-quickstart.md)
- [Try the real-time speech to text quickstart via Azure Speech](./get-started-speech-to-text.md)
