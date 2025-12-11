---
title: Custom text to speech avatar overview - Speech service
titleSuffix: Foundry Tools
description: Get an overview of the custom text to speech avatar feature of speech service, which allows you to create a customized, one-of-a-kind synthetic talking avatar for your application.
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

# What is custom text to speech avatar?

Custom text to speech avatar allows you to create a customized, one-of-a-kind synthetic talking avatar for your application. With custom text to speech avatar, you can build a unique and natural-looking avatar for your product or brand. The avatar is even more realistic if you also use a [professional voice or voice sync for avatar](#custom-voice-and-custom-text-to-speech-avatar) for the same actor.

There are two types of custom text to speech avatar:
- Custom video avatar: is created by your provided video recording data of your selected actors. 
- Custom photo avatar: is created by your provided image. 

> [!IMPORTANT]
> Custom text to speech avatar access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

>[!Important]
> Photo avatar (preview) and custom photo avatar (preview) are licensed to you as part of your Azure subscription and are subject to terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms) and the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA)("DPA"), as well as the Microsoft Generative AI Services Previews terms in the [supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
> 
> Access to custom photo avatar (preview), which is part of custom text to speech avatar, is limited based on eligibility and usage criteria. Learn more [here](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access?tabs=cnv) and request access on the [intake form](https://aka.ms/customneural).

 
## How does it work?

Creating a custom video avatar requires at least 10 minutes of video recording of the avatar talent as training data, and you must first get consent from the actor talent.

Creating a custom photo avatar only requires a photo of the character. If the photo is of a real person, you must obtain their consent first.

The custom avatar model can support:
- Video generation via the [batch synthesis API](./batch-synthesis-avatar.md).
- Live chat via the [streaming synthesis API](./real-time-synthesis-avatar.md).

Before you get started, here are some considerations:

**Your use case:** Do you want to use the avatar to create video content such as training material or a product introduction? Do you want to use the avatar as a virtual salesperson in a real-time conversation with your customers? There are some recording requirements for different use cases.

**The look of the avatar:** The custom text to speech avatar looks the same as the avatar talent in the training data, and we don't support customizing the appearance of the avatar model, such as clothes, hairstyle, etc. So if your application requires multiple styles of the same avatar, you should prepare training data for each style, as each style of an avatar is considered as a single avatar model.

**The voice of the avatar:** The custom text to speech avatar can work with standard voice, professional voice, or voice sync for avatar. 
- Voice sync for avatar: A synthetic voice resembling the avatar talent’s voice is trained alongside the custom avatar utilizing audio from the training video. The voice sync for avatar is currently only supported for custom video avatar. 
- Professional voice: Fine-tune a professional voice with more training data, providing a premium voice experience for your avatar, including natural conversations, multi-style, and multilingual support.

**Overview of the steps to create a custom video avatar:**

1. **Get consent video.** Obtain a video recording of the talent reading a consent statement. They must consent to the usage of their image and voice data to train a custom text to speech avatar model. If voice sync for avatar is expected to train with a custom video avatar model, they must also consent to the usage of their voice data to train a synthetic version of their voice.

1. **Prepare training data.** Ensure that the video recording is in the right format. It's a good idea to shoot the video recording in a professional-quality video shooting studio to get a clean background image. The quality of the resulting avatar heavily depends on the recorded video used for training. Factors like speaking rate, body posture, facial expression, hand gestures, consistency in the actor's position, and lighting of the video recording are essential to create an engaging custom text to speech avatar. See [how to prepare training data](./custom-avatar-record-video-samples.md) for more details.

1. **Train the avatar model.** Once you have the data ready, upload your data to the [custom avatar portal](https://aka.ms/customavatar-portal) and start to train your model. Consent verification is conducted during the training. Make sure that you have access to the custom text to speech avatar feature before you can create a project. 

1. **Deploy and use your avatar model in your applications.**


**Overview of the steps to create a custom photo avatar:**

Currently the custom photo avatar training requires a manual offline process. Users can understand the brief steps of how to train it below:
1. **Prepare training data.** A custom photo avatar can be trained using either a real person’s photo or a virtual human image. See [Create custom photo avatar](./custom-photo-avatar-create.md) for details.
   
1. **Get consent video.** Obtain a video of the talent reading a consent statement. This is required when training a photo avatar from a real person’s photo. They must provide consent for the use of their image to train a custom photo avatar model.

1. **Set up the avatar model.** The custom photo avatar training and deployment are handled through a manual process.



## Components sequence

The custom text to speech avatar model contains three components: text analyzer, the text to speech audio synthesizer, and text to speech avatar video renderer. 
- To generate an avatar video file or stream with the avatar model, text is first input into the text analyzer, which provides the output in the form of a phoneme sequence. 
- The audio synthesizer synthesizes the speech audio for input text, and these two parts are provided by standard or custom voice models. 
- Finally, the text to speech avatar model predicts the image of lip sync with the speech audio, so that the synthetic video is generated. 

:::image type="content" source="./media/custom-avatar-workflow.png" alt-text="Screenshot of displaying an overview of the custom text to speech avatar workflow." lightbox="./media/custom-avatar-workflow.png":::

The text to speech avatar models are trained using deep neural networks based on the recording samples of human videos in different languages. All languages of standard voices and custom voices can be supported.

## Available locations

For the current list of regions that support custom avatar training and usage, see the [Speech service regions table](../regions.md?tabs=ttsavatar).

## Custom voice and custom text to speech avatar

[Custom voice](../custom-neural-voice.md) and custom text to speech avatar are separate features. You can use them independently or together. If you're also creating a professional voice for the actor, the avatar can be highly realistic. 

The custom text to speech avatar can work with a standard voice or custom voice as the avatar's voice. For more information, see [Avatar voice and language](./what-is-text-to-speech-avatar.md#avatar-voice-and-language).

There are two kinds of custom voice for a custom avatar:
- **Voice sync for avatar**: When you enable the voice sync for avatar option during custom video avatar training, a synthetic voice model using the likeness of the avatar talent is simultaneously trained with the avatar. This voice is exclusively associated with the custom video avatar and can't be independently used. For supported regions, see the [Speech service regions table](../regions.md?tabs=ttsavatar).
- **Professional voice**: You can fine-tune a professional voice. [Professional voice fine-tuning](../custom-neural-voice.md) and custom text to speech avatar are separate features. You can use them independently or together. If you choose to use them together, you need to apply for [professional voice fine-tuning](https://aka.ms/customneural) and [custom text to speech avatar](https://aka.ms/customneural) separately, and you're charged separately for professional voice fine-tuning and custom text to speech avatar. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). Additionally, if you plan to use [professional voice fine-tuning](../custom-neural-voice.md) with a text to speech avatar, you need to deploy or [copy your custom voice model](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) to one of the [avatar supported regions](./what-is-custom-text-to-speech-avatar.md#available-locations).

If you fine-tune a professional voice and want to use it together with the custom avatar, pay attention to the following points:

- Ensure that the custom voice endpoint is created in the same Microsoft Foundry resource as the custom avatar endpoint. As needed, refer to [train your professional voice model](../professional-voice-train-voice.md#copy-your-voice-model-to-another-project) to copy the custom voice model to the same Microsoft Foundry resource as the custom avatar endpoint.
- You can see the custom voice option in the voices list of the [avatar content generation page](https://speech.microsoft.com/portal/talkingavatar) and [live chat voice settings](https://speech.microsoft.com/portal/livechat).
- If you're using batch synthesis for avatar API, add the `"customVoices"` property to associate the deployment ID of the custom voice model with the voice name in the request. For more information, see the [text to speech properties](batch-synthesis-avatar-properties.md#text-to-speech-properties).
- If you're using real-time synthesis for avatar API, refer to our sample code on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar) to set the custom voice.

## Related content

- [How to create a custom text to speech avatar](./custom-avatar-create.md)
- [How to prepare custom text to speech avatar training data](./custom-avatar-record-video-samples.md)
- [Real-time synthesis for live chat avatar](./real-time-synthesis-avatar.md)
- [Batch synthesis for video creation](./batch-synthesis-avatar.md)
- [Transparency note for text to speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
