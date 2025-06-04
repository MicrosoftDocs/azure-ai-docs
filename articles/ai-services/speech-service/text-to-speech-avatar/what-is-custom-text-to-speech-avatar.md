---
title: Custom text to speech avatar overview - Speech service
titleSuffix: Azure AI services
description: Get an overview of the custom text to speech avatar feature of speech service, which allows you to create a customized, one-of-a-kind synthetic talking avatar for your application.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 1/13/2025
ms.reviewer: eur
ms.author: eur
author: eric-urban
ms.custom: references_regions
---

# What is custom text to speech avatar?

Custom text to speech avatar allows you to create a customized, one-of-a-kind synthetic talking avatar for your application. With custom text to speech avatar, you can build a unique and natural-looking avatar for your product or brand by providing video recording data of your selected actors. If you also create a [custom neural voice](#custom-voice-and-custom-text-to-speech-avatar) for the same actor and use it as the avatar's voice, the avatar is even more realistic.

> [!IMPORTANT]
> Custom text to speech avatar access is [limited](/azure/ai-foundry/responsible-ai/speech-service/custom-neural-voice/limited-access-custom-neural-voice?context=%2fazure%2fcognitive-services%2fspeech-service%2fcontext%2fcontext) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

## How does it work?

Creating a custom text to speech avatar requires at least 10 minutes of video recording of the avatar talent as training data, and you must first get consent from the actor talent.

The custom avatar model can support:
- Video generation via the [batch synthesis API](./batch-synthesis-avatar.md).
- Live chat via the [streaming synthesis API](./real-time-synthesis-avatar.md).

Before you get started, here are some considerations:

**Your use case:** Will you use the avatar to create video content such as training material, product introduction, or use the avatar as a virtual salesperson in a real-time conversation with your customers? There are some recording requirements for different use cases.

**The look of the avatar:** The custom text to speech avatar looks the same as the avatar talent in the training data, and we don't support customizing the appearance of the avatar model, such as clothes, hairstyle, etc. So if your application requires multiple styles of the same avatar, you should prepare training data for each style, as each style of an avatar is considered as a single avatar model.

**The voice of the avatar:** The custom text to speech avatar can work with both prebuilt neural voices and custom neural voices. Creating a custom neural voice for the avatar talent and using it with the avatar significantly increases the naturalness of the avatar experience.

Here's an overview of the steps to create a custom text to speech avatar:

1. **Get consent video.** Obtain a video recording of the consent statement. The consent statement is a video recording of the avatar talent reading a statement, giving consent to the usage of their image and voice data to train a custom text to speech avatar model.

1. **Prepare training data.** Ensure that the video recording is in the right format. It's a good idea to shoot the video recording in a professional-quality video shooting studio to get a clean background image. The quality of the resulting avatar heavily depends on the recorded video used for training. Factors like speaking rate, body posture, facial expression, hand gestures, consistency in the actor's position, and lighting of the video recording are essential to create an engaging custom text to speech avatar. See [how to prepare training data](./custom-avatar-record-video-samples.md) for more details.

1. **Train the avatar model.** Once you have the data ready, upload your data to the [custom avatar portal](https://aka.ms/customavatar-portal) and start to train your model. Consent verification is conducted during the training. Make sure that you have access to the custom text to speech avatar feature before you can create a project. 

1. **Deploy and use your avatar model in your applications.**

## Components sequence

The custom text to speech avatar model contains three components: text analyzer, the text to speech audio synthesizer, and text to speech avatar video renderer. 
- To generate an avatar video file or stream with the avatar model, text is first input into the text analyzer, which provides the output in the form of a phoneme sequence. 
- The audio synthesizer synthesizes the speech audio for input text, and these two parts are provided by text to speech or custom neural voice models. 
- Finally, the neural text to speech avatar model predicts the image of lip sync with the speech audio, so that the synthetic video is generated. 

:::image type="content" source="./media/custom-avatar-workflow.png" alt-text="Screenshot of displaying an overview of the custom text to speech avatar workflow." lightbox="./media/custom-avatar-workflow.png":::

The neural text to speech avatar models are trained using deep neural networks based on the recording samples of human videos in different languages. All languages of prebuilt voices and custom neural voices can be supported.

## Available locations

Custom avatar *training* is only available in the following service regions: Southeast Asia, West Europe, and West US 2. You can use a custom avatar model in the following service regions: Southeast Asia, North Europe, West Europe, Sweden Central, South Central US, East US 2, and West US 2.

## Custom voice and custom text to speech avatar

The custom text to speech avatar can work with a prebuilt neural voice or custom neural voice as the avatar's voice. For more information, see [Avatar voice and language](./what-is-text-to-speech-avatar.md#avatar-voice-and-language).

[Custom neural voice](../custom-neural-voice.md) and custom text to speech avatar are separate features. You can use them independently or together. If you choose to use them together, you need to apply for [custom neural voice](https://aka.ms/customneural) and [custom text to speech avatar](https://aka.ms/customneural) separately, and you'll be charged separately for custom neural voice and custom text to speech avatar. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Additionally, if you plan to use [custom neural voice](../custom-neural-voice.md) with a text to speech avatar, you need to deploy or [copy](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) your custom neural voice model to one of the [avatar supported regions](./what-is-custom-text-to-speech-avatar.md#available-locations). 

## Related content

- [How to create a custom text to speech avatar](./custom-avatar-create.md)
- [How to prepare custom text to speech avatar training data](./custom-avatar-record-video-samples.md)
- [Real-time synthesis for live chat avatar](./real-time-synthesis-avatar.md)
- [Batch synthesis for video creation](./batch-synthesis-avatar.md)
- [Transparency note for text to speech](/legal/cognitive-services/speech-service/text-to-speech/transparency-note?context=/azure/ai-services/speech-service/context/context)
/azure/ai-foundry/responsible-ai/