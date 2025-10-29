---
title: Voice live API language support
titleSuffix: Azure AI services
description: Learn about the languages supported by Voice live API and how to configure them.
manager: nitinme
author: goergenj
ms.author: jagoerge
ms.service: azure-ai-speech
ms.topic: conceptual
ms.date: 9/26/2025
ms.custom: languages
# Customer intent: As a developer, I want to learn about which languages are supported by the Voice live API and how to configure them.
---

# Voice live API supported languages

## Introduction

The Voice live API supports multiple languages and configuration options. In this document, you learn which languages the Voice live API supports and how to configure them.

## [Speech input](#tab/speechinput)

Depending on which model is being used voice live speech input is processed either by one of the multimodal models (for example, `gpt-realtime`, `gpt-4o-mini-realtime-preview`, and `phi4-mm-realtime`) or by `azure speech to text` models.

### Azure speech to text supported languages

Azure speech to text is used for all configuration where a non-multimodal model is being used and for speech input transcriptions with `phi4-mm-realtime`.
It supports all languages documented on the [Language and voice support for the Speech service - Speech to text](./language-support.md?tabs=stt) tab.

There are three options for voice live language processing:
- Automatic multilingual configuration using multilingual model (default)
- Single language configuration
- Multilingual configuration using up to 10 defined languages

The current multi-lingual model supports the following languages:
- Chinese (China) [zh-CN]
- English (Australia) [en-AU]
- English (Canada) [en-CA]
- English (India) [en-IN]
- English (United Kingdom) [en-GB]
- English (United States) [en-US]
- French (Canada) [fr-CA]
- French (France) [fr-FR]
- German (Germany) [de-DE]
- Hindi (India) [hi-IN]
- Italian (Italy) [it-IT]
- Japanese (Japan) [ja-JP]
- Korean (Korea) [ko-KR]
- Spanish (Mexico) [es-MX]
- Spanish (Spain) [es-ES]

To use **Automatic multilingual configuration using multilingual model** no extra configuration is required. If you do add the `language` string to the session`session.update` message, make sure to leave it empty.

```json
{
    "session": {
        "input_audio_transcription": {
            "model": "azure-speech",
            "language": ""
        }
}
```

> [!NOTE]
> The multilingual model generates results for unsupported languages, if no language is defined. In these cases transcription, quality is low. Ensure to configure defined languages, if you're setting up application with languages unsupported by the multilingual model.

To configure a single or multiple languages not supported by the multimodal model, you must add them to the `language` string in the session`session.update` message. A maximum of 10 languages are supported.

```json
{
    "session": {
        "input_audio_transcription": {
            "model": "azure-speech",
            "language": "en-US,fr-FR,de-DE"
        }
}
```

### gpt-realtime and gpt-4o-mini-realtime-preview supported languages

While the underlying model was trained on 98 languages, OpenAI only lists the languages that exceeded <50% word error rate (WER) which is an industry standard benchmark for speech to text model accuracy. The model returns results for languages not listed but the quality will be low.

The following languages are supported by `gpt-realtime` and `gpt-4o-mini-realtime-preview`:
- Afrikaans
- Arabic
- Armenian
- Azerbaijani
- Belarusian
- Bosnian
- Bulgarian
- Catalan
- Chinese
- Croatian
- Czech
- Danish
- Dutch
- English
- Estonian
- Finnish
- French
- Galician
- German
- Greek
- Hebrew
- Hindi
- Hungarian
- Icelandic
- Indonesian
- Italian
- Japanese
- Kannada
- Kazakh
- Korean
- Latvian
- Lithuanian
- Macedonian
- Malay
- Marathi
- Maori
- Nepali
- Norwegian
- Persian
- Polish
- Portuguese
- Romanian
- Russian
- Serbian
- Slovak
- Slovenian
- Spanish
- Swahili
- Swedish
- Tagalog
- Tamil
- Thai
- Turkish
- Ukrainian
- Urdu
- Vietnamese
- Welsh

Multimodal models don't require a language configuration for the general processing. If you configure input audio transcription, you can provide the transcription models with a language hint to improve transcription quality. In this case you need to add the `language`string to the session`session.update` message.

```json
{
    "session": {
        "input_audio_transcription": {
            "model": "gpt-4o-transcribe",
            "language": "English, German, French"
        }
}
```

> [!NOTE]
> Multimodal gpt models only support the following transcription models: `whisper-1`, `gpt-4o-transcribe`, and `gpt-4o-mini-transcribe`.

### phi4-mm-realtime supported languages

The following languages are supported by `phi4-mm-realtime`:
- Chinese
- English
- French
- German
- Italian
- Japanese
- Portuguese
- Spanish

Multimodal models don't require a language configuration for the general processing. If you configure input audio transcription for `phi4-mm-realtime` you need to use the same configuration as for all non-mulitmodal model configuration where `azure-speech` is used for transcription as described.

> [!NOTE]
> Multimodal phi models only support the following transcription models: `azure-speech`.

## [Speech output](#tab/speechoutput)

Depending on which model is being used voice live speech output is processed either by one of the multimodal OpenAI voices integrated into `gpt-realtime` and `gpt-4o-mini-realtime-preview` or by `azure text to speech` voices.

### Azure text to speech supported languages

Azure text to speech is used by default for all configuration where a non-multimodal OpenAI model is being used and can be configured in all configurations manually.
It supports all voices documented on the [Language and voice support for the Speech service - Text to speech](./language-support.md?tabs=tts) tab.

The following types of voices are supported:
- Monolingual voices
- Multilingual voices
- Custom voices

The supported language is tied to the voice used. To configure specific Azure text to speech voices, you need to add the `voice` configuration to the session`session.update` message.

```json
{
    "session": {
        "voice": {
            "name": "en-US-Ava:DragonHDLatestNeural",
            "type": "azure-standard",
            "temperature": 0.8,
        }
    }
}
```

For more information, see how to configure [Audio output through Azure text to speech](./voice-live-how-to.md#audio-output-through-azure-text-to-speech).

If *Multilingual Voices* are used, the language output can optionally be controlled by setting specific SSML tags. You can learn more about SSML tags in the [Customize voice and sound with SSML](./speech-synthesis-markup-voice.md#lang-examples) how to.

## Related content

- Learn more about [How to use the Voice live API](./voice-live-how-to.md)
- Try out the [Voice live API quickstart](./voice-live-quickstart.md)
- See the [Voice live API reference](./voice-live-api-reference.md)
