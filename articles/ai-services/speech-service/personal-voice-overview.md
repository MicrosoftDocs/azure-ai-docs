---
title: What is personal voice?
titleSuffix: Azure AI services
description: With personal voice, you can get AI generated replication of your voice (or users of your application) in a few seconds.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 9/20/2024
ms.author: eur
ms.custom: references_regions, build-2024
#Customer intent: As a developer, I want to learn about personal voice for text to speech.
---

# What is personal voice for text to speech? 

With personal voice, you can enable your users to get AI generated replication of their own voices in a few seconds. With a verbal statement and a short speech sample as the audio prompt, you can create a personal voice for your users and allow them to generate speech in any of the more than 90 languages supported across more than 100 locales.

> [!NOTE]
> Personal voice is available in these regions: West Europe, East US, and South East Asia. 
> For supported locales, see [personal voice language support](./language-support.md?tabs=tts#personal-voice).

The following table summarizes the difference between personal voice and professional custom neural voice.  
 
| Comparison | Personal voice | Professional voice |
|-------|-------------------------|-----|
| Target scenarios | Business customers to build an app to allow their users to create and use their own personal voice in the app. | Professional scenarios like brand and character voices for chat bots, or audio content reading. |
| Use cases | Restricted to limited use cases. See the [transparency note](/legal/cognitive-services/speech-service/custom-neural-voice/transparency-note?context=/azure/ai-services/speech-service/context/context&tabs=prebuilt-voice#intended-uses-for-personal-voice-preview). Approved customers should have a plan to support more than 1,000 personal voices.  | Restricted to limited use cases. See the [transparency note](/legal/cognitive-services/speech-service/custom-neural-voice/transparency-note?context=/azure/ai-services/speech-service/context/context&tabs=prebuilt-voice#intended-uses-for-custom-neural-voice-pro-and-custom-neural-voice-lite). |
| Training data | Make sure you follow the code of conduct. | Bring your own data. Recording in a professional studio is recommended. |
| Required data size | One minute of human speech. | 300-2000 utterances (about 30 minutes to 3 hours of human speech). |
| Training time | Less than 5 seconds | Approximately 20-40 compute hours. |
| Voice quality | Natural | Highly natural |
| Multilingual support | Yes. The voice is able to speak about 100 languages, with automatic language detection enabled. | Yes. You need to select the "Neural – cross lingual" feature to train a model that speaks a different language from the training data. |
| Availability | The demo on [Speech Studio](https://aka.ms/speechstudio/) is available upon registration. Access to the API is restricted to eligible customers and approved use cases. Request access through the intake form. | You can only train and deploy a CNV Pro model after access is approved. CNV Pro access is limited based on eligibility and usage criteria. Request access through the intake form. |
| Pricing | Check the pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)<sup>1</sup>. | Check the pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). |
| Responsible AI requirements | Speaker's verbal statement required. No unapproved use case allowed. | Speaker's verbal statement required. No unapproved use case allowed. |

<sup>1</sup> Note that personal voice pricing will only be visible for service regions where the feature is available, including West Europe, East US, and South East Asia. 

## Try the demo

If you have an S0 resource, you can access the personal voice demo in Speech Studio. To use the personal voice API, you can apply for access [here](https://aka.ms/customneural).

1. Go to [Speech Studio](https://aka.ms/speechstudio/)
   
1. Select the **Personal Voice** card.
   
1. You can record your own voice and try the voice output samples in different languages. The demo includes a subset of the languages supported by personal voice.

    :::image type="content" source="./media/personal-voice/personal-voice-samples.png" alt-text="Screenshot of the personal voice demo experience in Speech Studio." lightbox="./media/personal-voice/personal-voice-samples.png":::


## How to create a personal voice

To get started, here's a summary of the steps to create a personal voice:
1. [Create a project](./personal-voice-create-project.md). 
1. [Upload consent file](./personal-voice-create-consent.md). With the personal voice feature, it's required that every voice be created with explicit consent from the user. A recorded statement from the user is required acknowledging that the customer (Azure AI Speech resource owner) will create and use their voice.
1. [Get a speaker profile ID](./personal-voice-create-voice.md) for the personal voice. You get a speaker profile ID based on the speaker's verbal consent statement and an audio prompt. The user's voice characteristics are encoded in the `speakerProfileId` property that's used for text to speech. 

Once you have a personal voice, you can [use it](./personal-voice-how-to-use.md) to synthesize speech in any of the 91 languages supported across 100+ locales. A locale tag isn't required. Personal voice uses automatic language detection at the sentence level. For more information, see [use personal voice in your application](./personal-voice-how-to-use.md).

> [!TIP]
> Check out the code samples in the [Speech SDK repository on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/custom-voice/README.md) to see how to use personal voice in your application.

## Reference documentation

> [!div class="nextstepaction"]
> [Custom voice REST API reference documentation](/rest/api/speech/)

## Responsible AI 

We care about the people who use AI and the people who will be affected by it as much as we care about technology. For more information, see the Responsible AI [transparency notes](/legal/cognitive-services/speech-service/text-to-speech/transparency-note?context=/azure/ai-services/speech-service/context/context).


## Next steps

- [Create a project](./personal-voice-create-project.md). 
- Learn more about custom neural voice in the [overview](custom-neural-voice.md).
- Learn more about Speech Studio in the [overview](speech-studio-overview.md).
