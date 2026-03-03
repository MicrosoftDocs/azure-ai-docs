---
title: Game development with Azure Speech in Foundry Tools - Speech service
titleSuffix: Foundry Tools
description: Concepts for game development with Azure Speech in Foundry Tools.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 02/25/2026
ms.author: pafarley
ai-usage: ai-assisted
---

# Game development with Azure Speech in Foundry Tools

Azure Speech enhances various gaming scenarios, both in-game and out-of-game.

Speech features to consider for flexible and interactive game experiences include:

- Synthesize audio from text or display text from audio to make conversations accessible to all players.
- Improve accessibility for players who can't read text in a particular language, including young players who don't yet read or write. Players can listen to storylines and instructions in their preferred language.
- Create game avatars and nonplayable characters (NPCs) that can initiate or participate in conversations during gameplay.
- Use standard voices to provide highly natural out-of-the-box voices across a large portfolio of languages and voices.
- Use custom voices to create a voice that stays on-brand with consistent quality and speaking style. You can add emotions, accents, nuances, laughter, and other paralinguistic sounds and expressions.
- Prototype game dialogue to reduce the time and cost of production and get the game to market sooner. You can rapidly swap lines of dialogue and listen to variations in real time to iterate on game content.

You can use the [Speech SDK](speech-sdk.md) or [Speech CLI](spx-overview.md) for real-time, low-latency speech to text, text to speech, language identification, and speech translation. You can also use the [Batch transcription API](batch-transcription.md) to transcribe prerecorded speech to text. To synthesize a large volume of text input (long and short) to speech, use the [Batch synthesis API](batch-synthesis.md).

For information about locale and regional availability, see [Language and voice support](language-support.md) and [Region support](regions.md).

## Text to speech

Convert text messages to audio using [text to speech](text-to-speech.md) for scenarios such as game dialogue prototyping, greater accessibility, or nonplayable character (NPC) voices. Text to speech includes [standard voice](language-support.md?tabs=tts#standard-voices) and [custom voice](language-support.md?tabs=tts#professional-voice) features. Standard voice provides highly natural out-of-the-box voices across a large portfolio of languages and voices. Custom voice is a self-service tool for creating a highly natural custom voice.

Consider the following capabilities when you enable text to speech in your game:

- **Voices and languages** - A large portfolio of [locales and voices](language-support.md?tabs=tts#supported-languages) is supported. You can also [specify multiple languages](speech-synthesis-markup-voice.md#adjust-speaking-languages) for text to speech output. For [custom voice](custom-neural-voice.md), you can [choose to create](professional-voice-train-voice.md?tabs=neural#choose-a-training-method) different languages from single-language training data.
- **Emotional styles** - [Emotional tones](language-support.md?tabs=tts#voice-styles-and-roles), such as cheerful, angry, sad, excited, hopeful, friendly, unfriendly, terrified, shouting, and whispering. You can [adjust the speaking style](speech-synthesis-markup-voice.md#use-speaking-styles-and-roles), style degree, and role at the sentence level.
- **Visemes** - You can use visemes during real-time synthesis to control the movement of 2D and 3D avatar models so that mouth movements match synthetic speech precisely. For more information, see [Get facial position with viseme](how-to-speech-synthesis-viseme.md).
- **SSML fine-tuning** - With Speech Synthesis Markup Language (SSML), you can customize text to speech output with richer voice tuning options. For more information, see [Speech Synthesis Markup Language (SSML) overview](speech-synthesis-markup.md).
- **Audio outputs** - Each standard voice model is available at 24 kHz and high-fidelity 48 kHz. If you select a 48-kHz output format, the high-fidelity voice model at 48 kHz is invoked accordingly. Other sample rates can be obtained through upsampling or downsampling during synthesis. For example, 44.1 kHz is downsampled from 48 kHz. Each audio format incorporates a bitrate and encoding type. For more information, see the [supported audio formats](rest-text-to-speech.md?tabs=streaming#audio-outputs). For more information on 48-kHz high-quality voices, see [this blog post](https://techcommunity.microsoft.com/t5/ai-cognitive-services-blog/azure-neural-tts-voices-upgraded-to-48khz-with-hifinet2-vocoder/ba-p/3665252).

For an example, see the [text to speech quickstart](get-started-text-to-speech.md).

## Speech to text

You can use [speech to text](speech-to-text.md) to display text from the spoken audio in your game. For an example, see the [Speech to text quickstart](get-started-speech-to-text.md).

## Language identification

With [language identification](language-identification.md), you can detect the language of the chat string submitted by the player.

## Speech translation

Players in the same game session often speak different languages and might appreciate receiving both the original message and its translation. You can use [speech translation](speech-translation.md) to translate text between languages so players across the world can communicate in their native language.

For an example, see the [Speech translation quickstart](get-started-speech-translation.md).

> [!NOTE]
> In addition to the Speech service, you can also use the [Translator service](../translator/translator-overview.md). To perform real-time text translation between supported source and target languages, see [Text translation](../translator/text-translation-overview.md).

## Next steps

* [Azure gaming documentation](/gaming/azure/)
* [Text to speech quickstart](get-started-text-to-speech.md)
* [Speech to text quickstart](get-started-speech-to-text.md)
* [Speech translation quickstart](get-started-speech-translation.md)
