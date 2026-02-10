---
title: How to customize Voice Live input and output
titleSuffix: Foundry Tools
description: Learn how to use the Voice Live API with customized models.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 10/05/2025
ms.custom: custom speech, custom voice, custom avatar, fine-tuning
# Customer intent: As a developer, I want to learn how to use custom models with the Voice Live API for real-time voice agents.
---

# How to customize Voice Live input and output

Voice Live provides multiple options to optimize performance and quality by using custom models. The following customization options are currently available:

- Speech input customization:
    - Phrase-list: A lightweight just-in-time customization based on a list of words or phrases provided as part of the session configuration to help improve recognition quality. To learn more, see [Improve recognition accuracy with phrase list](./improve-accuracy-phrase-list.md).
    - Custom Speech: With custom speech, you can evaluate and improve the accuracy of speech recognition for your applications and products and fine-tune the recognition quality to your business needs. See [What is custom speech?](./custom-speech-overview.md) to learn more.
- Speech output customization:
    - Custom lexicon: Custom lexicon allows you to easily customize pronunciation for both standard Azure text to speech voices and custom voices to improve speech synthesis accuracy for your use case. See [custom lexicon for text to speech](./speech-synthesis-markup-pronunciation.md#custom-lexicon) to learn more.
    - Custom voice: Custom voice lets you create a one-of-a-kind, customized, synthetic voice for your applications. With custom voice, you can build a highly natural-sounding voice for your brand or characters by providing human speech samples as fine-tuning data. See [What is custom voice?](./custom-neural-voice.md) to learn more.
    - Custom avatar: Custom text to speech avatar allows you to create a customized, one-of-a-kind synthetic talking avatar for your application. With custom text to speech avatar, you can build a unique and natural-looking avatar for your product or brand by providing video recording data of your selected actors. See [What is custom text to speech avatar?](./text-to-speech-avatar/what-is-custom-text-to-speech-avatar.md) to learn more.

## Speech input customization

### Phrase list

Use phrase list for lightweight just-in-time customization on audio input. To configure phrase list, you can set the phrase_list in the `session.update` message.

```json
{
    "session": {
        "input_audio_transcription": {
            "model": "azure-speech",
            "phrase_list": ["Neo QLED TV", "TUF Gaming", "AutoQuote Explorer"]
        }
    }
}
```

> [!NOTE]
> Phrase list currently doesn't support gpt-realtime, gpt-4o-mini-realtime, and phi4-mm-realtime. To learn more about phrase list, see [phrase list for speech to text](./improve-accuracy-phrase-list.md).

### Custom speech configuration

You can use the custom_speech field to specify your custom speech models. This field is defined as a dictionary, where each key represents a locale code and each value corresponds to the `Model ID` of the custom speech model. For more information about custom speech, see [What is custom speech?](./custom-speech-overview.md).

Voice Live supports using a combination of base models and custom models as long as each type is unique per locale with a maximum of 10 languages specified in total.

Example session configuration with custom speech models. In this example when the detected language is English, the base model is used and, when the detected language is Chinese, the custom speech model is used.

```json
{
  "session": {
    "input_audio_transcription": {
      "model": "azure-speech",
      "language": "en",
      "custom_speech": {
        "zh-CN": "847cb03d-7f22-4b11-444-e1be1d77bf17"
      }
    }
  }
}
```

> [!NOTE]
> In order to use a custom speech model with Voice Live API, the model must be available on the same Microsoft Foundry resource you are using to call the Voice Live API. If you trained the model on a different Microsoft Foundry or Azure Speech in Foundry Tools resource you have to copy the model to the resource you are using to call the Voice Live API.
> You pay separately for custom speech training and model hosting. 

## Speech output customization

### Custom lexicon

Use the `custom_lexicon_url` string property to customize pronunciation for both standard Azure text to speech voices and custom voices. To learn more about how to format the custom lexicon (the same as Speech Synthesis Markup Language (SSML)), see [custom lexicon for text to speech](./speech-synthesis-markup-pronunciation.md#custom-lexicon).

```json
{
  "voice": {
    "name": "en-US-Ava:DragonHDLatestNeural",
    "type": "azure-standard",
    "temperature": 0.8, // optional
    "custom_lexicon_url": "<custom lexicon url>"
  }
}
```

### Azure custom voices

You can use a custom voice for audio output. For information about how to create a custom voice, see [What is custom voice](./custom-neural-voice.md).

```json
{
  "voice": {
    "name": "en-US-CustomNeural",
    "type": "azure-custom",
    "endpoint_id": "your-endpoint-id", // a guid string
    "temperature": 0.8 // optional, value range 0.0-1.0, only take effect when using HD voices
  }
}
```

> [!IMPORTANT]
> Custom voice access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

> [!NOTE]
> In order to use a custom voice model with Voice Live API, the model must be available on the same Microsoft Foundry resource you are using to call the Voice Live API. If you trained the model on a different Microsoft Foundry or Azure Speech resource you have to copy the model to the resource you are using to call the Voice Live API.
> You pay separately for custom voice training and model hosting.
> For more information on supported regions, see [Speech service supported regions](./regions.md?tabs=tts).


### Azure custom avatar

[Text to speech avatar](./text-to-speech-avatar/what-is-text-to-speech-avatar.md) converts text into a digital video of a photorealistic human (either a standard avatar or a [custom text to speech avatar](./text-to-speech-avatar/what-is-custom-text-to-speech-avatar.md)) speaking with a natural-sounding voice.

The configuration for a custom avatar doesn't differ from the configuration of a standard avatar. Refer to [How to use the Voice Live API - Azure text to speech avatar](./voice-live-how-to.md#azure-text-to-speech-avatar) for a detailed example.

> [!IMPORTANT]
> Custom text to speech avatar access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

> [!NOTE]
> In order to use a custom voice model with Voice Live API, the model must be available on the same Microsoft Foundry resource you are using to call the Voice Live API. If you trained the model on a different Microsoft Foundry or Azure Speech resource you have to copy the model to the resource you are using to call the Voice Live API.
> You pay separately for custom avatar training and model hosting. 
> For more information on supported regions, see [Speech service supported regions](./regions.md?tabs=ttsavatar).

> [!NOTE]
> Custom photo avatar (PREVIEW) training isn't yet available as a self-service option and currently requires a manual offline process.

## Related content

- Try out the [Voice Live API quickstart](./voice-live-quickstart.md)
- Learn more about [How to use the Voice Live API](./voice-live-how-to.md)
