---
title: Custom text to speech avatar overview - Speech service
titleSuffix: Azure AI services
description: Get an overview of the custom text to speech avatar feature of speech service, which allows you to create a customized, one-of-a-kind synthetic talking avatar for your application.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 4/28/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
ms.custom: references_regions
---

# What is custom text to speech avatar?

Custom text to speech avatar allows you to create a customized, one-of-a-kind synthetic talking avatar for your application. With custom text to speech avatar, you can build a unique and natural-looking avatar for your product or brand by providing video recording data of your selected actors. The avatar is even more realistic if you also use a [professional voice or voice sync for avatar](#custom-voice-and-custom-text-to-speech-avatar) for the same actor.

> [!IMPORTANT]
> Custom text to speech avatar access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access-custom-neural-voice) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

## How does it work?

Creating a custom text to speech avatar requires at least 10 minutes of video recording of the avatar talent as training data, and you must first get consent from the actor talent.

The custom avatar model can support:
- Video generation via the [batch synthesis API](./batch-synthesis-avatar.md).
- Live chat via the [streaming synthesis API](./real-time-synthesis-avatar.md).

Before you get started, here are some considerations:

**Your use case:** Will you use the avatar to create video content such as training material, product introduction, or use the avatar as a virtual salesperson in a real-time conversation with your customers? There are some recording requirements for different use cases.

**The look of the avatar:** The custom text to speech avatar looks the same as the avatar talent in the training data, and we don't support customizing the appearance of the avatar model, such as clothes, hairstyle, etc. So if your application requires multiple styles of the same avatar, you should prepare training data for each style, as each style of an avatar is considered as a single avatar model.

**The voice of the avatar:** The custom text to speech avatar can work with standard voice, professional voice, and voice sync for avatar. 
- Voice sync for avatar: A synthetic voice resembling the avatar talent’s voice is trained alongside the custom avatar utilizing audio from the training video.
- Professional voice: Fine-tune a professional voice with more training data, providing a premium voice experience for your avatar, including natural conversations, multi-style, and multilingual support.

Here's an overview of the steps to create a custom text to speech avatar:

1. **Get consent video.** Obtain a video recording of the talent reading a consent statement. They must consent to the usage of their image and voice data to train a custom text to speech avatar model and a synthetic version of their voice.

1. **Prepare training data.** Ensure that the video recording is in the right format. It's a good idea to shoot the video recording in a professional-quality video shooting studio to get a clean background image. The quality of the resulting avatar heavily depends on the recorded video used for training. Factors like speaking rate, body posture, facial expression, hand gestures, consistency in the actor's position, and lighting of the video recording are essential to create an engaging custom text to speech avatar. See [how to prepare training data](./custom-avatar-record-video-samples.md) for more details.

1. **Train the avatar model.** Once you have the data ready, upload your data to the [custom avatar portal](https://aka.ms/customavatar-portal) and start to train your model. Consent verification is conducted during the training. Make sure that you have access to the custom text to speech avatar feature before you can create a project. 

1. **Deploy and use your avatar model in your applications.**

## Components sequence

The custom text to speech avatar model contains three components: text analyzer, the text to speech audio synthesizer, and text to speech avatar video renderer. 
- To generate an avatar video file or stream with the avatar model, text is first input into the text analyzer, which provides the output in the form of a phoneme sequence. 
- The audio synthesizer synthesizes the speech audio for input text, and these two parts are provided by standard or custonm voice models. 
- Finally, the text to speech avatar model predicts the image of lip sync with the speech audio, so that the synthetic video is generated. 

:::image type="content" source="./media/custom-avatar-workflow.png" alt-text="Screenshot of displaying an overview of the custom text to speech avatar workflow." lightbox="./media/custom-avatar-workflow.png":::

The text to speech avatar models are trained using deep neural networks based on the recording samples of human videos in different languages. All languages of standard voices and custom voices can be supported.

## Available locations

Custom avatar *training* is only available in the following service regions: Southeast Asia, West Europe, and West US 2. You can use a custom avatar model in the following service regions: Southeast Asia, North Europe, West Europe, Sweden Central, South Central US, East US 2, and West US 2.

## Custom voice and custom text to speech avatar

[Custom voice](../custom-neural-voice.md) and custom text to speech avatar are separate features. You can use them independently or together. If you're also creating a professional voice for the actor, the avatar can be highly realistic. 

The custom text to speech avatar can work with a standard voice or custom voice as the avatar's voice. For more information, see [Avatar voice and language](./what-is-text-to-speech-avatar.md#avatar-voice-and-language).

There are two kinds of custom voice for a custom avatar:
- **Voice sync for avatar**: When you enable the voice sync for avatar option during custom avatar training, a synthetic voice model using the likeness of the avatar talent is simultaneously trained with the avatar. This voice is exclusively associated with the custom avatar and can't be independently used. Voice sync for avatar is currently supported in the Southeast Asia, West Europe, and West US 2 regions.
- **Professional voice**: You can fine-tune a professional voice. [Professional voice fine-tuning](../custom-neural-voice.md) and custom text to speech avatar are separate features. You can use them independently or together. If you choose to use them together, you need to apply for [professional voice fine-tuning](https://aka.ms/customneural) and [custom text to speech avatar](https://aka.ms/customneural) separately, and you are charged separately for professional voice fine-tuning and custom text to speech avatar. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Additionally, if you plan to use [professional voice fine-tuning](../custom-neural-voice.md) with a text to speech avatar, you need to deploy or [copy your custom voice model](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) to one of the [avatar supported regions](./what-is-custom-text-to-speech-avatar.md#available-locations).

If you fine-tune a professional voice and want to use it together with the custom avatar, pay attention to the following points:

- Ensure that the custom voice endpoint is created in the same Azure AI Foundry resource as the custom avatar endpoint. As needed, refer to [train your professional voice model](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) to copy the custom voice model to the same Azure AI Foundry resource as the custom avatar endpoint.
- You can see the custom voice option in the voices list of the [avatar content generation page](https://speech.microsoft.com/portal/talkingavatar) and [live chat voice settings](https://speech.microsoft.com/portal/livechat).
- If you're using batch synthesis for avatar API, add the `"customVoices"` property to associate the deployment ID of the custom voice model with the voice name in the request. For more information, see the [text to speech properties](batch-synthesis-avatar-properties.md#text-to-speech-properties).
- If you're using real-time synthesis for avatar API, refer to our sample code on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar) to set the custom voice.

## Related content

- [How to create a custom text to speech avatar](./custom-avatar-create.md)
- [How to prepare custom text to speech avatar training data](./custom-avatar-record-video-samples.md)
- [Real-time synthesis for live chat avatar](./real-time-synthesis-avatar.md)
- [Batch synthesis for video creation](./batch-synthesis-avatar.md)
- [Transparency note for text to speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
