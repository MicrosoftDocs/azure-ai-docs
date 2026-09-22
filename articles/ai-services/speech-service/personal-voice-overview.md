---
title: What is personal voice?
titleSuffix: Foundry Tools
description: With personal voice, you can get AI generated replication of your voice (or users of your application) in a few seconds.
author: PatrickFarley
reviewer: patrickfarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: overview
ms.date: 09/09/2026
ms.author: pafarley
ms.reviewer: pafarley
ms.custom: references_regions, build-2024
ai-usage: ai-assisted
#Customer intent: As a developer, I want to learn about personal voice for text to speech.
---

# What is personal voice for text to speech? 

With personal voice, you can enable your users to get AI generated replication of their own voices in a few seconds. With a verbal statement and a short speech sample as the audio prompt, you can create a personal voice for your users and allow them to generate speech in any of the more than 90 languages supported across more than 100 locales.

> [!NOTE]
> For the current list of regions that support personal voice, see the [Speech service regions table](regions.md?tabs=tts). 
> For supported locales, see [personal voice language support](./language-support.md?tabs=custom-tts#personal-voice).

The following table summarizes the difference between personal voice and professional voice.  
 
| Comparison | Personal voice | Professional voice |
|-------|-------------------------|-----|
| Target scenarios | Business customers to build an app to allow their users to create and use their own personal voice in the app. | Professional scenarios like brand and character voices for chat bots, or audio content reading. |
| Use cases | Restricted to limited use cases. See the [transparency note](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note). |
| Training data | Make sure you follow the code of conduct. | Bring your own data. Recording in a professional studio is recommended. |
| Required data size | A 5–90-second human speech sample. | Requirements depend on the selected training method and version. |
| Training time | Less than 5 seconds | Training time depends on the selected training method, version, and data size. |
| Voice quality | Natural | Highly natural |
| Multilingual support | Yes. The voice can speak about 100 languages, with automatic language detection enabled. | Yes. Select a training method and version that supports multilingual synthesis. |
| Availability | The personal voice demo is available in [Foundry (classic)](https://ai.azure.com/?cid=learnDocs) and [Speech Studio](https://aka.ms/speechstudio/) upon registration. Personal voice customization is available in Foundry (new). Access to the API is restricted to eligible customers and approved use cases. Request access through the intake form. | You can only use professional voice fine-tuning after access is approved. Professional voice fine-tuning access is limited based on eligibility and usage criteria. Request access through the intake form. |
| Pricing | Check the pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)<sup>1</sup>. | Check the pricing details [here](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). |
| Responsible AI requirements | Speaker's verbal statement required. No unapproved use case allowed. | Speaker's verbal statement required. No unapproved use case allowed. |

<sup>1</sup> Note that personal voice pricing will only be visible for service regions where the feature is available. For the current list of supported regions, see the [Speech service regions table](regions.md?tabs=tts). 

## Try the demo

The personal voice demo isn't currently available in Foundry (new). You can access the demo in [Foundry (classic)](https://ai.azure.com/?cid=learnDocs) or [Speech Studio](https://aka.ms/speechstudio/). To create a personal voice customization in Foundry (new), see [Set up a personal voice](./personal-voice-create-project.md?pivots=ai-foundry-portal&tabs=foundry-new). To use the personal voice API, [apply for access](https://aka.ms/customneural).

1. Go to [Foundry (classic)](https://ai.azure.com/?cid=learnDocs) or [Speech Studio](https://aka.ms/speechstudio/).
1. Select the **Personal Voice** card.
1. Record your voice and try the voice output samples in different languages. The demo includes a subset of the languages supported by personal voice.

    :::image type="content" source="./media/personal-voice/personal-voice-samples.png" alt-text="Screenshot of the personal voice demo experience in Foundry classic or Speech Studio." lightbox="./media/personal-voice/personal-voice-samples.png":::


## How to create a personal voice

To get started, here's a summary of the steps to create a personal voice:
1. [Set up a personal voice](./personal-voice-create-project.md).
1. [Upload consent file](./personal-voice-create-consent.md). With the personal voice feature, it's required that every voice be created with explicit consent from the user. A recorded statement from the user is required acknowledging that the customer (Azure Speech in Foundry Tools resource owner) will create and use their voice.
1. [Create a personal voice](./personal-voice-create-voice.md) from the speaker's verbal consent statement and a 5–90-second audio prompt. The custom voice REST API returns the `speakerProfileId` that's used for text to speech.

Once you have a personal voice, you can [use it](./personal-voice-how-to-use.md) to synthesize speech in any of the 91 languages supported across 100+ locales. A locale tag isn't required. Personal voice uses automatic language detection at the sentence level. For more information, see [use personal voice in your application](./personal-voice-how-to-use.md).

> [!TIP]
> Check out the code samples in the [Speech SDK repository on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/custom-voice/README.md) to see how to use personal voice in your application.

## Reference documentation

> [!div class="nextstepaction"]
> [Custom voice REST API reference documentation](/rest/api/speech/)

## Responsible AI 

We care about the people who use AI and the people who will be affected by it as much as we care about technology. For more information, see the Responsible AI [transparency notes](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note).


## Next steps

- [Set up a personal voice](./personal-voice-create-project.md).
- Learn more about custom voice in the [overview](custom-neural-voice.md).
- Explore [Foundry (new)](https://ai.azure.com/nextgen?cid=learnDocs) to create and manage your personal voice customization, or use [Speech Studio](https://aka.ms/speechstudio/) for the Personal Voice demo.
