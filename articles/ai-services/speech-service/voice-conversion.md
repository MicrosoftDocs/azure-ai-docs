---
title: What is voice conversion?
titleSuffix: Foundry Tools
description: Learn about voice conversion in Azure Speech in Foundry Tools.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 01/30/2026
ms.custom: references_regions
---

# What is voice conversion? (Preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Voice conversion is the process of transforming the voice characteristics of given audio to a target voice speaker. After voice conversion, the resulting audio reserves the source audio's linguistic content and prosody while the voice timbre sounds like the target speaker.

There are three reasons users need voice conversion functionality:

- Voice conversion can replicate your content using a different voice identity while maintaining the original prosody and emotion. For instance, in education, teachers can record themselves reading stories, and voice conversion can deliver these stories using a predesigned cartoon character's voice. This method preserves the expressiveness of the teacher's reading while incorporating the unique timbre of the cartoon character's voice.
- Another application is multilingual dubbing. When localized content is read by different voices, voice conversion can transform them into a uniform voice, ensuring a consistent experience across all languages while keeping the most localized voice characters.
- Voice conversion enhances control over the expressiveness of a voice. By transforming various speaking styles, such as adopting a unique tone or conveying exaggerated emotions, a voice gains greater versatility in expression and can be more dynamic in different scenarios.

## Key capabilities

Voice conversion (or voice changer or speech to speech conversion) is built on state-of-the-art generative models and offers high-quality voice conversion. It delivers the following core capabilities:

| Capability | Description |
|------------|-------------|
| **High speaker similarity**   | Captures the timbre and vocal identity of the target speaker.<br>Generates audio that accurately matches the target voice. |
| **Prosody preservation**      | Maintains rhythm, stress, and intonation of source audio.<br>Preserves expressive and emotional qualities. |
| **High audio fidelity**       | Generates realistic, natural-sounding audio.<br>Minimizes artifacts.                                      |
| **Multilingual support**      | Enables multilingual voice conversion.<br>Supports 91 locales (same as standard text to speech locale support).<br>See [supported voices for voice conversion](./language-support.md?tabs=tts#voice-conversion) for the complete list. |

## Use voice conversion

You can use Azure Speech in Foundry Tools voice conversion with either the Speech SDK or text to speech REST APIs.

Use the `<mstts:voiceconversion>` tag via Speech Synthesis Markup Language (SSML) to specify the source audio URL and the target voice for the conversion. For a complete list of supported target voices, see [supported voices for voice conversion](./language-support.md?tabs=tts#voice-conversion).

### Example SSML

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice xml:lang="en-US" xml:gender="Female" name="en-US-AvaMultilingualNeural">
        <mstts:voiceconversion url="https://your.blob.core.windows.net/sourceaudio.wav"/>
    </voice>
</speak>
```

For details about the SSML structure and usage, see the [Speech Synthesis Markup Language (SSML) reference](./speech-synthesis-markup-voice.md#voice-conversion-element) documentation.

## Related content

- [Text to speech overview](./text-to-speech.md)
- [Speech synthesis markup voice](./speech-synthesis-markup-voice.md)
