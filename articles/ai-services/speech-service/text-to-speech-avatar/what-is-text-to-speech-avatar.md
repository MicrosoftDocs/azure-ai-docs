---
title: Text to speech avatar overview - Speech service
titleSuffix: Foundry Tools
description: Get an overview of the Text to speech avatar feature of speech service, which allows users to create synthetic videos featuring avatars speaking based on text input.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 10/21/2025
ms.author: pafarley
author: PatrickFarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.custom: references_regions
---

# What is Text to speech avatar?

Text to speech avatar converts text into a digital video of a photorealistic human (either a standard avatar or a [custom text to speech avatar](#custom-text-to-speech-avatar)) speaking with a natural-sounding voice. The text to speech avatar video can be synthesized asynchronously or in real time. Developers can build applications integrated with text to speech avatar through an API, or use Text to speech avatar in Foundry to create video content without coding.

With text to speech avatar's advanced models, the feature empowers users to deliver life-like and high-quality synthetic talking avatar videos for various applications while adhering to [responsible AI practices](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

> [!TIP]
> To convert text to speech with a no-code approach, try the [Text to speech avatar tool in Speech Studio](https://speech.microsoft.com/portal/talkingavatar).

## Avatar capabilities

Text to speech avatar capabilities include:

- Converts text into a digital video of a photorealistic human speaking with natural-sounding voices powered by Azure AI text to speech.
-  Provides a collection of standard avatars, see [Standard avatars](./standard-avatars.md) for a full list of supported standard avatars.
- Azure AI text to speech generates the voice of the avatar. For more information, see [Avatar voice and language](#avatar-voice-and-language).
- Synthesizes text to speech avatar video asynchronously with the [batch synthesis API](./batch-synthesis-avatar.md) or in [real-time](./real-time-synthesis-avatar.md).
- Use Text to speech avatar tool in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs) or in [Speech Studio](https://speech.microsoft.com/portal/talkingavatar) for creating video content without coding.
- Enables real-time avatar conversations through the [live chat avatar tool](https://speech.microsoft.com/portal/livechat) in Speech Studio.
- Create voice agent with avatar in [Voice Live](../voice-live.md) 

With text to speech avatar's advanced neural network models and Photo avatar's VASA-1 models, the feature empowers you to deliver lifelike and high-quality synthetic talking avatar videos for various applications while adhering to responsible AI practices.

## Avatar voice and language

You can choose from a range of standard voices for the avatar. The language support for text to speech avatar is the same as the language support for text to speech. For details, see [Language and voice support for the Speech service](../language-support.md?tabs=tts). Standard text to speech avatars can be accessed through the [Speech Studio portal](https://speech.microsoft.com/portal/talkingavatar) or via API.

The voice in the synthetic video could be an Azure Speech in Foundry Tools standard voice or the [custom voice](../custom-neural-voice.md) of voice talent selected by you.

## Avatar type
- Video Avatar: The avatar is generated using a fine tuned model with a video recording for fine tuning. It supports half-body and full-body representations.
- Photo Avatar (preview): The avatar is created from a single input image as prompt and is limited to a head-only representation.


## Avatar video output

For video avatar, both batch synthesis and real-time synthesis resolution are 1920 x 1080 by default, while user can choose to train 4K resolution custom avatars, and the frames per second (FPS) rate is 25. For batch synthesis, the codec can be h264, hevc, or av1 if the format is `mp4` and can be vp9 or av1 if the format is `webm`; only `vp9` can contain an alpha channel. For real-time synthesis, the codec is h264. Video bitrate can be configured in the request for both batch synthesis and real-time synthesis; the default value is 2,000,000; more detailed configurations can be found in the sample code.
Photo avatar 's resolution is 512x512 for both batch synthesis and real-time synthesis.

Video Avatar

|                  | Batch synthesis   | Real-time synthesis |
|------------------|-------------------|----------------------|
| **Resolution**   | 1920 x 1080/3840 x 2160    | 1920 x 1080/3840 x 2160          |
| **FPS**          | 25                | 25                   |
| **Codec**        | h264/hevc/vp9/av1 | h264                 |


Photo Avatar (preview)

|                  | Batch synthesis   | Real-time synthesis |
|------------------|-------------------|----------------------|
| **Resolution**   | 512x512      | 512x512    |
| **FPS**          | 25                | 25                   |
| **Codec**        | h264/hevc/vp9 | h264                 |


## Custom text to speech avatar

You can create custom text to speech avatars that are unique to your product or brand. For custom video avatar, all it takes to get started is taking 10 minutes of video recordings; and for custom photo avatar, it only needs one photo.  If you're also fine-tuning a professional voice for the actor, the avatar can be highly realistic. 

Voice sync for avatar is trained alongside the custom avatar utilizing audio from the training video. The voice is exclusively associated with the custom avatar and can't be independently used.

[Professional voice fine-tuning](../custom-neural-voice.md) and [custom text to speech avatar](what-is-custom-text-to-speech-avatar.md) are separate features. You can use them independently or together. If you plan to also use [professional voice fine-tuning](../custom-neural-voice.md) with a text to speech avatar, you need to deploy or [copy](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) your fine-tuned professional voice model to one of the [avatar supported regions](#available-locations).

For more information, see [What is custom text to speech avatar](./what-is-custom-text-to-speech-avatar.md).

## Sample code

Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). These samples cover the most popular scenarios:

* [Batch synthesis (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-avatar)
* [Real-time synthesis (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
* [Live chat with Azure OpenAI in behind (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar#chat-sample)
* [Use avatar in Voice Live API](https://github.com/azure-ai-foundry/voicelive-samples/tree/main/javascript/voice-live-avatar)

## Pricing

- Throughout an avatar real-time session or batch content creation, the text to speech, speech to text, Azure OpenAI, or other Azure services are charged separately.
- Voice sync for avatar (via custom avatar training) is charged the same as a personal voice in terms of voice creation and synthesis. The storage of the voice is free.
- Refer to [text to speech avatar pricing note](../text-to-speech.md#text-to-speech-avatar) to learn how billing works for the text-to-speech avatar feature.
- For the detailed pricing, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Avatar pricing is only visible for service regions where the feature is available. For the current list of supported regions, see the [Speech service regions table](../regions.md?tabs=ttsavatar).

## Available locations

For the current list of regions that support text to speech avatar, see the [Speech service regions table](../regions.md?tabs=ttsavatar).

### Responsible AI

We care about the people who use AI and the people who will be affected by it as much as we care about technology. For more information, see the Responsible AI [transparency notes](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note) and [disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent).

## Next steps

* [Use batch synthesis for text to speech avatar](./batch-synthesis-avatar.md)
* [What is custom text to speech avatar](what-is-custom-text-to-speech-avatar.md)
