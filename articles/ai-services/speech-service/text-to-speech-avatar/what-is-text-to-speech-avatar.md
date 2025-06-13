---
title: Text to speech avatar overview - Speech service
titleSuffix: Azure AI services
description: Get an overview of the Text to speech avatar feature of speech service, which allows users to create synthetic videos featuring avatars speaking based on text input.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 4/28/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
ms.custom: references_regions
---

# Text to speech avatar overview

Text to speech avatar converts text into a digital video of a photorealistic human (either a standard avatar or a [custom text to speech avatar](#custom-text-to-speech-avatar)) speaking with a natural-sounding voice. The text to speech avatar video can be synthesized asynchronously or in real time. Developers can build applications integrated with text to speech avatar through an API, or use a content creation tool on Speech Studio to create video content without coding.

With text to speech avatar's advanced neural network models, the feature empowers users to deliver life-like and high-quality synthetic talking avatar videos for various applications while adhering to [responsible AI practices](/azure/ai-foundry/responsible-ai/speech-service/disclosure-voice-talent).

> [!TIP]
> To convert text to speech with a no-code approach, try the [Text to speech avatar tool in Speech Studio](https://speech.microsoft.com/portal/talkingavatar).

## Avatar capabilities

Text to speech avatar capabilities include:

- Converts text into a digital video of a photorealistic human speaking with natural-sounding voices powered by Azure AI text to speech.
- Provides a collection of standard avatars.
- Azure AI text to speech generates the voice of the avatar. For more information, see [Avatar voice and language](#avatar-voice-and-language).
- Synthesizes text to speech avatar video asynchronously with the [batch synthesis API](./batch-synthesis-avatar.md) or in [real-time](./real-time-synthesis-avatar.md).
- Provides a [content creation tool](https://speech.microsoft.com/portal/talkingavatar) in Speech Studio for creating video content without coding.
- Enables real-time avatar conversations through the [live chat avatar tool](https://speech.microsoft.com/portal/livechat) in Speech Studio.

With text to speech avatar's advanced neural network models, the feature empowers you to deliver lifelike and high-quality synthetic talking avatar videos for various applications while adhering to responsible AI practices.

## Avatar voice and language

You can choose from a range of standard voices for the avatar. The language support for text to speech avatar is the same as the language support for text to speech. For details, see [Language and voice support for the Speech service](../language-support.md?tabs=tts). Standard text to speech avatars can be accessed through the [Speech Studio portal](https://speech.microsoft.com/portal/talkingavatar) or via API.

The voice in the synthetic video could be an Azure AI Speech standard voice or the [custom voice](../custom-neural-voice.md) of voice talent selected by you.

## Avatar video output

Both batch synthesis and real-time synthesis resolution are 1920 x 1080, and the frames per second (FPS) are 25. Batch synthesis codec can be h264, hevc, or av1 if the format is `mp4` and can set codec as vp9 or av1 if the format is `webm`; only `vp9` can contain an alpha channel. Real-time synthesis codec is h264. Video bitrate can be configured for both batch synthesis and real-time synthesis in the request; the default value is 2000000; more detailed configurations can be found in the sample code.

|                  | Batch synthesis   | Real-time synthesis |
|------------------|-------------------|----------------------|
| **Resolution**   | 1920 x 1080       | 1920 x 1080          |
| **FPS**          | 25                | 25                   |
| **Codec**        | h264/hevc/vp9/av1 | h264                 |

## Custom text to speech avatar

You can create custom text to speech avatars that are unique to your product or brand. All it takes to get started is taking 10 minutes of video recordings. If you're also fine-tuning a professional voice for the actor, the avatar can be highly realistic. 

Voice sync for avatar is trained alongside the custom avatar utilizing audio from the training video. The voice is exclusively associated with the custom avatar and cannot be independently used.

[Professional voice fine-tuning](../custom-neural-voice.md) and [custom text to speech avatar](what-is-custom-text-to-speech-avatar.md) are separate features. You can use them independently or together. If you plan to also use [professional voice fine-tuning](../custom-neural-voice.md) with a text to speech avatar, you need to deploy or [copy](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) your fine-tuned professional voice model to one of the [avatar supported regions](#available-locations).

For more information, see [What is custom text to speech avatar](./what-is-custom-text-to-speech-avatar.md).

## Sample code

Sample code for text to speech avatar is available on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples). These samples cover the most popular scenarios:

* [Batch synthesis (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch-avatar)
* [Real-time synthesis (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar)
* [Live chat with Azure OpenAI in behind (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar#chat-sample)
* To create a live chat APP with Azure OpenAI [On Your Data](/azure/ai-services/openai/concepts/use-your-data), you can refer to [this sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/browser/avatar/README.md) (search "On Your Data")

## Pricing

- Throughout an avatar real-time session or batch content creation, the text-to-speech, speech-to-text, Azure OpenAI, or other Azure services are charged separately.
- Voice sync for avatar (via custom avatar training) is charged the same as a personal voice in terms of voice creation and synthesis. The storage of the voice is free.
- Refer to [text to speech avatar pricing note](../text-to-speech.md#text-to-speech-avatar) to learn how billing works for the text-to-speech avatar feature.
- For the detailed pricing, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Note that avatar pricing will only be visible for service regions where the feature is available, including Southeast Asia, North Europe, West Europe, Sweden Central, South Central US, East US 2, and West US 2.

## Available locations

The text to speech avatar feature is only available in the following service regions: Southeast Asia, North Europe, West Europe, Sweden Central, South Central US, East US 2, and West US 2.

### Responsible AI

We care about the people who use AI and the people who will be affected by it as much as we care about technology. For more information, see the Responsible AI [transparency notes](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note) and [disclosure for voice and avatar talent](/azure/ai-foundry/responsible-ai/speech-service/disclosure-voice-talent).

## Next steps

* [Use batch synthesis for text to speech avatar](./batch-synthesis-avatar.md)
* [What is custom text to speech avatar](what-is-custom-text-to-speech-avatar.md)
