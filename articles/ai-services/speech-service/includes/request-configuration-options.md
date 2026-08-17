---
manager: xkang
author: Rena Liu
ms.author: renaliu
ms.service: azure-speech-llm
ms.topic: include
ms.date: 08/04/2026
ai-usage: ai-assisted
---

## Request configuration options

Here are some property options to configure a transcription when you call the [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe) operation.

| Property | Description | Required or optional |
|----------|-------------|----------------------|
| `channels` | The list of zero-based indices of the channels to be transcribed separately. Up to two channels are supported unless diarization is enabled. By default, the fast transcription API merges all input channels into a single channel and then performs the transcription. If this isn't desirable, channels can be transcribed independently without merging.<br/><br/>If you want to transcribe the channels from a stereo audio file separately, you need to specify `[0,1]`, `[0]`, or `[1]`. Otherwise, stereo audio is merged to mono and only a single channel is transcribed.<br/><br/>If the audio is stereo and diarization is enabled, then you can't set the `channels` property to `[0,1]`. The Speech service doesn't support diarization of multiple channels.<br/><br/>For mono audio, the `channels` property is ignored, and the audio is always transcribed as a single channel.| Optional |
| `diarization` | The diarization configuration. Diarization is the process of recognizing and separating multiple speakers in one audio channel. For example, specify `"diarization": {"maxSpeakers": 2, "enabled": true}`. Then the transcription file contains `speaker` entries (such as `"speaker": 0` or `"speaker": 1`) for each transcribed phrase. | Optional |
| `locales` | The list of locales that should match the expected locale of the audio data to transcribe.<br/><br/>If you know the locale of the audio file, you can specify it to improve transcription accuracy and minimize the latency. If a single locale is specified, that locale is used for transcription.<br/><br/>But if you're not sure about the locale, you can specify multiple locales to use language identification. Language identification might be more accurate with a more precise list of candidate locales.<br/><br/>If you don't specify any locale, then the Speech service will use the latest multi-lingual model to identify the locale and transcribe continuously.<br/><br/> You can get the latest supported languages via the [Transcriptions - List Supported Locales](/rest/api/speechtotext/transcriptions/list-supported-locales) REST API (API version 2024-11-15 or later). For more information about locales, see the [Speech service language support](../../language-support.md?tabs=stt) documentation.| Optional but recommended if you know the expected locale. |
| `phraseList` |Phrase list is a list of words or phrases provided ahead of time to help improve their recognition. Adding a phrase to a phrase list increases its importance, thus making it more likely to be recognized. For example, specify `phraseList":{"phrases":["Contoso","Jessie","Rehaan"]}`. Phrase List is supported via API version 2025-10-15. For more information, see [Improve recognition accuracy with phrase list](../improve-accuracy-phrase-list.md#implement-phrase-list-in-fast-and-llm-speech-transcription). | Optional |
| `profanityFilterMode` |Specifies how to handle profanity in recognition results. Accepted values are `None` to disable profanity filtering, `Masked` to replace profanity with asterisks, `Removed` to remove all profanity from the result, or `Tags` to add profanity tags. The default value is `Masked`. | Optional |
