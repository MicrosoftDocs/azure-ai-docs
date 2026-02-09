---
title: Language and Voice Support for Azure Speech
titleSuffix: Foundry Tools
description: Learn about language and voice support in Azure Speech for speech to text, text to speech, speech translation, and more. Learn which features support each locale.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 12/19/2025
ms.author: pafarley
ms.custom: references_regions, build-2024
#Customer intent: As a developer, I want to learn about the languages that Azure Speech supports so that I can decide how to use the features in my application.
---

# Language and voice support for Azure Speech

The following tables summarize language support for [speech to text](speech-to-text.md), [text to speech](text-to-speech.md), [pronunciation assessment](how-to-pronunciation-assessment.md), [speech translation](speech-translation.md), and more features of Azure Speech. Use them to check whether your target language and locale are available for each Azure Speech capability.

You can also see the list of locales and voices supported for each specific region or endpoint:

- [Speech SDK](speech-sdk.md)
- [Speech-to-text REST API](rest-speech-to-text.md)
- [Speech-to-text REST API for short audio](rest-speech-to-text-short.md)
- [Text-to-speech REST API](rest-text-to-speech.md#get-a-list-of-voices)

## Supported languages

Language support varies by functionality in Azure Speech.

> [!NOTE]
> See the [speech containers](speech-container-overview.md#available-speech-containers) and [embedded speech](embedded-speech.md#models-and-voices) documentation for their supported languages.

Choose a feature:

# [Speech to text](#tab/stt)

The table in this section summarizes the locales supported for [real-time transcription](speech-to-text.md#real-time-transcription), [fast transcription](speech-to-text.md#fast-transcription), and [batch transcription](speech-to-text.md#batch-transcription).

[!INCLUDE [Language support include](includes/language-support/stt.md)]


> [!TIP]
> To build and run samples in Visual Studio Code, try the [Azure Speech Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit).

# [Text to speech](#tab/tts)

The table in this section summarizes the locales and voices that text to speech supports. For details, see the table footnotes.

More remarks for text-to-speech locales are included in the [Voice styles and roles](#voice-styles-and-roles), [Standard voices](#standard-voices), [Professional voice](#professional-voice), and [Personal voice](#personal-voice) sections in this article.

> [!TIP]
> To determine the right voice for your business needs, check the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery).
>
> To build and run samples in Visual Studio Code, try the [Azure Speech Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit).


[!INCLUDE [Language support include](includes/language-support/tts.md)]


## Multilingual voices

Voices with names that include `MultilingualNeural`, `DragonHDLatestNeural`, or `DragonHDOmniLatestNeural` support multiple languages. These voices enable expressive speech synthesis across languages, which helps reduce language barriers and support inclusive global communication.

`DragonHDLatestNeural` and `DragonHDOmniLatestNeural` are neural high‑definition (HD) voices that are based on large language models (LLMs). They can understand the semantic content of the input text, automatically detect emotional cues, and adjust speaking style and tone in real time to better match the sentiment. HD voices maintain a consistent voice persona with their non‑HD (neural) counterparts while providing enhanced capabilities through improved contextual understanding.

`MultilingualNeural` voices represent an earlier generation of multilingual technology. They offer high naturalness but don't have the same level of contextual awareness as HD voices.

The following table lists all supported speaking languages for each multilingual voice. If a voice doesn't support the language of the input text, Azure Speech doesn't return synthesized audio. The table is sorted in descending order by the number of supported languages.

The locale prefix indicates the voice's primary locale. For example, for the voice `en‑US‑AndrewMultilingualNeural`, the locale prefix is `en‑US`, which is the first segment of the voice name.

[!INCLUDE [Language support include](includes/language-support/multilingual-voices.md)]

## Multi-talker voices

Multi-talker voices enable natural, dynamic conversations with multiple distinct speakers. This innovation enhances the realism of synthesized dialogues by preserving contextual flow, emotional consistency, and natural speech patterns.

Use this capability to generate engaging, podcast-style speech or conversational exchanges with seamless transitions between speakers. Unlike single-talker models, which synthesize each turn in isolation, multi-talker voices maintain coherence across dialogue. This coherence helps ensure a more authentic and immersive listening experience.

[!INCLUDE [Language support include](includes/language-support/multi-talker.md)]

For more information about how to use multi-talker voices via Speech Synthesis Markup Language (SSML), see [Multi-talker voice example](speech-synthesis-markup-voice.md#multi-talker-voice-example).

## Voice styles and roles

In some cases, you can adjust the speaking style to express emotions like cheerfulness, empathy, and calm. All standard voices with speaking styles and multi-style custom voices support adjustment of style degree. You can optimize the voice for scenarios like customer service, newscast, and voice assistant. With roles, the same voice can act as a different age and gender.

To learn how you can configure and adjust voice styles and roles, see [Use speaking styles and roles](speech-synthesis-markup-voice.md#use-speaking-styles-and-roles).

Use the following table to determine supported styles and roles for each voice.

[!INCLUDE [Language support include](includes/language-support/voice-styles-and-roles.md)]

## Visemes

This table lists all the locales supported for [viseme](speech-synthesis-markup-voice.md#viseme-element). For more information about viseme, see [Get facial position with viseme](how-to-speech-synthesis-viseme.md) and [Viseme element](speech-synthesis-markup-voice.md#viseme-element). 

[!INCLUDE [Language support include](includes/language-support/viseme.md)]

## Standard voices

Each standard voice supports a specific language and dialect, identified by locale. You can try the demo and hear the voices in the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery).

> [!IMPORTANT]
> Pricing varies for standard voice and custom voice. For more information, see the [Azure Speech in Foundry Tools pricing](https://azure.microsoft.com/pricing/details/speech/) page.

Each standard voice model is available at 24 kHz and high-fidelity 48 kHz. You can get other sample rates through upsampling or downsampling when synthesizing.

## Professional voice

Use [professional voice fine-tuning](./professional-voice-create-project.md) to create synthetic voices that are rich in speaking styles. You can create a unique brand voice in multiple languages and styles by using a small set of recording data. Multi-style custom voices support adjustment of style degree.

Select the right locale that matches the data for your professional voice fine-tuning. For example, if the recording data is spoken in English with a British accent, select `en-GB`.

By using the cross-lingual feature, you can transfer your custom voice model to speak a second language. For example, with the `zh-CN` data, you can create a voice that speaks `en-AU` or any of the languages with cross-lingual support.

For the cross-lingual feature, we categorize locales into two tiers:

- A tier that includes source languages that support the cross-lingual feature
- A tier that comprises locales designated as target languages for cross-lingual transfer

The following table distinguishes locales that function as both cross-lingual sources and targets from locales that are eligible solely as target locales for cross-lingual transfer.

[!INCLUDE [Language support include](includes/language-support/tts-cnv.md)]


## Personal voice

[Personal voice](personal-voice-overview.md) is a feature for creating a voice that sounds like you or your users. The following table summarizes the supported locales for personal voice.

[!INCLUDE [Language support include](includes/language-support/personal-voice.md)]


## Voice conversion

[Voice conversion](voice-conversion.md) is a feature for transforming the voice characteristics of audio to a target voice speaker. The following table summarizes the supported locales for voice conversion. Each language is available in all [voice conversion regions](regions.md#regions).

[!INCLUDE [Language support include](includes/language-support/voice-conversion.md)]

# [Pronunciation assessment](#tab/pronunciation-assessment)

The table in this section summarizes the 33 supported locales for pronunciation assessment. Each language is available in all [speech-to-text regions](regions.md#regions). The latest update extends support from English to 32 more languages and quality enhancements to existing features, including accuracy, fluency, and miscue assessment. You should specify the language that you're learning or practicing improving pronunciation. The default language is `en-US`.

If you know your target learning language, [set the locale](how-to-pronunciation-assessment.md#get-pronunciation-assessment-results) accordingly. For example, if you're learning British English, you should specify the language as `en-GB`. If you're teaching a broader language, such as Spanish, and you're uncertain about which locale to select, you can run various accent models (`es-ES`, `es-MX`) to determine the one that achieves the highest score to suit your specific scenario.

If you're interested in languages not listed in the following table, fill out [this intake form](https://aka.ms/speechpa/intake) for further assistance.

[!INCLUDE [Language support include](includes/language-support/pronunciation-assessment.md)]

# [Speech translation](#tab/speech-translation)

> [!TIP]
> To build and run samples on Visual Studio Code, try the [Azure Speech Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit).

### Real-time speech translation

The table in this section summarizes the supported locales for speech translation. Speech translation supports various languages for speech-to-speech and speech-to-text translation. The available target languages depend on whether the translation target is speech or text.

[!INCLUDE [Language support include](includes/language-support/speech-translation.md)]

#### Translate-from language

To set the language for input speech recognition, specify the full locale with a dash (`-`) separator. See the [speech-to-text language table](?tabs=stt#supported-languages). All languages are supported, except `jv-ID` and `wuu-CN`. The default language is `en-US` if you don't specify a language.

#### Translate-to-text language

To set the translation target language, you usually specify only the language code that precedes the locale dash (`-`) separator. For example, use `es` for Spanish (Spain) instead of `es-ES`. The default language is `en` if you don't specify a language.

### Video translation

The table in this section summarizes the supported locales for [video translation](./video-translation-overview.md). Video translation supports various languages for standard (platform) voice and personal voice. The available source and target languages depend on whether the translation source is standard or personal voice.

[!INCLUDE [Language support include](includes/language-support/video-translation.md)]

# [Language identification](#tab/language-identification)

The table in this section summarizes the supported locales for [language identification](language-identification.md).

> [!IMPORTANT]
> Language Identification compares speech at the language level, such as English and German. Don't include multiple locales of the same language in your candidate list.

[!INCLUDE [Language support include](includes/language-support/language-identification.md)]

# [Custom keyword](#tab/custom-keyword)

The following table summarizes the supported locales for custom keyword and keyword verification.

[!INCLUDE [Language support include](includes/language-support/custom-keyword.md)]

---

## Related content

- [Region support](regions.md)
