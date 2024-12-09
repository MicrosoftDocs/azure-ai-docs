---
title: Text to speech overview - Speech service
titleSuffix: Azure AI services
description: Get an overview of the benefits and capabilities of the text to speech feature of the Speech service.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 9/24/2024
ms.author: eur
#Customer intent: As a developer, I want to learn about the benefits and capabilities of the text to speech feature of the Speech service.
---

# What is text to speech?

In this overview, you learn about the benefits and capabilities of the text to speech feature of the Speech service, which is part of Azure AI services.

Text to speech enables your applications, tools, or devices to convert text into human like synthesized speech. The text to speech capability is also known as speech synthesis. Use human like prebuilt neural voices out of the box, or create a custom neural voice that's unique to your product or brand. For a full list of supported voices, languages, and locales, see [Language and voice support for the Speech service](language-support.md?tabs=tts).

## Core features

Text to speech includes the following features:

| Feature | Summary | Demo |
| --- | --- | --- |
| Prebuilt neural voice (called *Neural* on the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)) | Highly natural out-of-the-box voices. Create an Azure subscription and Speech resource, and then use the [Speech SDK](./get-started-text-to-speech.md) or visit the [Speech Studio portal](https://speech.microsoft.com/portal) and select prebuilt neural voices to get started. Check the [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). | Check the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery) and determine the right voice for your business needs. |
| Custom neural voice (called *Custom Neural* on the [pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/)) | Easy-to-use self-service for creating a natural brand voice, with limited access for responsible use. Create an Azure subscription and Speech resource (with the S0 tier), and [apply](https://aka.ms/customneural) to use the custom voice feature. After you're granted access, visit the [Speech Studio portal](https://speech.microsoft.com/portal) and select **Custom voice** to get started. Check the [pricing details](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/). | Check the [voice samples](https://aka.ms/customvoice). |

### More about neural text to speech features

Text to speech uses deep neural networks to make the voices of computers nearly indistinguishable from the recordings of people. With the clear articulation of words, neural text to speech significantly reduces listening fatigue when users interact with AI systems.

The patterns of stress and intonation in spoken language are called _prosody_. Traditional text to speech systems break down prosody into separate linguistic analysis and acoustic prediction steps governed by independent models. That can result in muffled, buzzy voice synthesis.

Here's more information about neural text to speech features in the Speech service, and how they overcome the limits of traditional text to speech systems:

* **Real-time speech synthesis**: Use the [Speech SDK](./get-started-text-to-speech.md) or [REST API](rest-text-to-speech.md) to convert text to speech by using [prebuilt neural voices](language-support.md?tabs=tts) or [custom neural voices](custom-neural-voice.md).

* **Asynchronous synthesis of long audio**: Use the [batch synthesis API](batch-synthesis.md) to asynchronously synthesize text to speech files longer than 10 minutes (for example, audio books or lectures). Unlike synthesis performed via the Speech SDK or Speech to text REST API, responses aren't returned in real-time. The expectation is that requests are sent asynchronously, responses are polled for, and synthesized audio is downloaded when the service makes it available.

* **Prebuilt neural voices**: Azure AI Speech uses deep neural networks to overcome the limits of traditional speech synthesis regarding stress and intonation in spoken language. Prosody prediction and voice synthesis happen simultaneously, which results in more fluid and natural-sounding outputs. Each prebuilt neural voice model is available at 24 kHz and high-fidelity 48 kHz. You can use neural voices to:

  - Make interactions with chatbots and voice assistants more natural and engaging.
  - Convert digital texts such as e-books into audiobooks.
  - Enhance in-car navigation systems.

  For a full list of prebuilt Azure AI Speech neural voices, see [Language and voice support for the Speech service](language-support.md?tabs=tts).

* **Improve text to speech output with SSML**: Speech Synthesis Markup Language (SSML) is an XML-based markup language used to customize text to speech outputs. With SSML, you can adjust pitch, add pauses, improve pronunciation, change speaking rate, adjust volume, and attribute multiple voices to a single document.

  You can use SSML to define your own lexicons or switch to different speaking styles. With the [multilingual voices](https://techcommunity.microsoft.com/t5/azure-ai/azure-text-to-speech-updates-at-build-2021/ba-p/2382981), you can also adjust the speaking languages via SSML. To improve the voice output for your scenario, see [Improve synthesis with Speech Synthesis Markup Language](speech-synthesis-markup.md) and [Speech synthesis with the Audio Content Creation tool](how-to-audio-content-creation.md).

* **Visemes**: [Visemes](how-to-speech-synthesis-viseme.md) are the key poses in observed speech, including the position of the lips, jaw, and tongue in producing a particular phoneme. Visemes have a strong correlation with voices and phonemes.

  By using viseme events in Speech SDK, you can generate facial animation data. This data can be used to animate faces in lip-reading communication, education, entertainment, and customer service. Viseme is currently supported only for the `en-US` (US English) [neural voices](language-support.md?tabs=tts).

> [!NOTE]
> In addition to Azure AI Speech neural (non HD) voices, you can also use [Azure AI Speech high definition (HD) voices](high-definition-voices.md) and [Azure OpenAI neural (HD and non HD) voices](openai-voices.md). The HD voices provide a higher quality for more versatile scenarios.
> 
> Some voices don't support all [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup-structure.md) tags. This includes neural text to speech HD voices, personal voices, and embedded voices. 
- For Azure AI Speech high definition (HD) voices, check the SSML support [here](high-definition-voices.md#supported-and-unsupported-ssml-elements-for-azure-ai-speech-hd-voices). 
- For personal voice, you can find the SSML support [here](personal-voice-how-to-use.md#supported-and-unsupported-ssml-elements-for-personal-voice). 
- For embedded voices, check the SSML support [here](embedded-speech.md#embedded-voices-capabilities).

## Get started

To get started with text to speech, see the [quickstart](get-started-text-to-speech.md). Text to speech is available via the [Speech SDK](speech-sdk.md), the [REST API](rest-text-to-speech.md), and the [Speech CLI](spx-overview.md).

> [!TIP]
> To convert text to speech with a no-code approach, try the [Audio Content Creation](how-to-audio-content-creation.md) tool in [Speech Studio](https://aka.ms/speechstudio/audiocontentcreation).

## Sample code

Sample code for text to speech is available on GitHub. These samples cover text to speech conversion in most popular programming languages:

* [Text to speech samples (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
* [Text to speech samples (REST)](https://github.com/Azure-Samples/Cognitive-Speech-TTS)

## Custom neural voice

In addition to prebuilt neural voices, you can create custom neural voices that are unique to your product or brand. All it takes to get started is a handful of audio files and the associated transcriptions. For more information, see [Get started with custom neural voice](professional-voice-create-project.md).

## Pricing note

### Billable characters
When you use the text to speech feature, you're billed for each character that's converted to speech, including punctuation. Although the SSML document itself isn't billable, optional elements that are used to adjust how the text is converted to speech, like phonemes and pitch, are counted as billable characters. Here's a list of what's billable:

* Text passed to the text to speech feature in the SSML body of the request
* All markup within the text field of the request body in the SSML format, except for `<speak>` and `<voice>` tags
* Letters, punctuation, spaces, tabs, markup, and all white-space characters
* Every code point defined in Unicode

For detailed information, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

> [!IMPORTANT]
> Each Chinese character is counted as two characters for billing, including kanji used in Japanese, hanja used in Korean, or hanzi used in other languages.  

### Model training and hosting time for custom neural voice

Custom neural voice training and hosting are both calculated by hour and billed per second. For the billing unit price, see [Speech service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

Custom neural voice (CNV) training time is measured by ‘compute hour’ (a unit to measure machine running time). Typically, when training a voice model, two computing tasks are running in parallel. So, the calculated compute hours are longer than the actual training time. On average, it takes less than one compute hour to train a CNV Lite voice; while for CNV Pro, it usually takes 20 to 40 compute hours to train a single-style voice, and around 90 compute hours to train a multi-style voice. The CNV training time is billed with a cap of 96 compute hours. So in the case that a voice model is trained in 98 compute hours, you'll only be charged with 96 compute hours. 

Custom neural voice (CNV) endpoint hosting is measured by the actual time (hour). The hosting time (hours) for each endpoint is calculated at 00:00 UTC every day for the previous 24 hours. For example, if the endpoint has been active for 24 hours on day one, it's billed for 24 hours at 00:00 UTC the second day. If the endpoint is newly created or suspended during the day, it's billed for its accumulated running time until 00:00 UTC the second day. If the endpoint isn't currently hosted, it isn't billed. In addition to the daily calculation at 00:00 UTC each day, the billing is also triggered immediately when an endpoint is deleted or suspended. For example, for an endpoint created at 08:00 UTC on December 1, the hosting hour will be calculated to 16 hours at 00:00 UTC on December 2 and 24 hours at 00:00 UTC on December 3. If the user suspends hosting the endpoint at 16:30 UTC on December 3, the duration (16.5 hours) from 00:00 to 16:30 UTC on December 3 will be calculated for billing.

### Personal voice

When you use the personal voice feature, you're billed for both profile storage and synthesis.

*  **Profile storage**: After a personal voice profile is created, it will be billed until it is removed from the system. The billing unit is per voice per day. If voice storage lasts for a period of less than 24 hours, it will be billed as one full day.
*  **Synthesis**: Billed per character. For details on billable characters, see the above [billable characters](#billable-characters).

### Text to speech avatar

When using the text-to-speech avatar feature, charges will be incurred based on the length of video output and will be billed per second. However, for the real-time avatar, charges are based on the time when the avatar is active, regardless of whether it is speaking or remaining silent, and will also be billed per second. To optimize costs for real-time avatar usage, refer to the tips provided in the [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/browser/avatar#chat-sample) (search "Use Local Video for Idle"). Avatar hosting is billed per second per endpoint. You can suspend your endpoint to save costs. If you want to suspend your endpoint, you can delete it directly. To use it again, simply redeploy the endpoint.

## Monitor Azure text to speech metrics

Monitoring key metrics associated with text to speech services is crucial for managing resource usage and controlling costs. This section will guide you on how to find usage information in the Azure portal and provide detailed definitions of the key metrics. For more details on Azure monitor metrics, refer to [Azure Monitor Metrics overview](/azure/azure-monitor/essentials/data-platform-metrics).

### How to find usage information in the Azure portal

To effectively manage your Azure resources, it's essential to access and review usage information regularly. Here's how to find the usage information:

1. Go to the [Azure portal](https://ms.portal.azure.com/) and sign in with your Azure account.

1. Navigate to **Resources** and select your resource you wish to monitor.

1. Select **Metrics** under **Monitoring** from the left-hand menu.

   :::image type="content" source="media/text-to-speech/monitoring-metrics.png" alt-text="Screenshot of selecting metrics option under monitoring.":::

1. Customize metric views.

   You can filter data by resource type, metric type, time range, and other parameters to create custom views that align with your monitoring needs. Additionally, you can save the metric view to dashboards by selecting **Save to dashboard** for easy access to frequently used metrics.

1. Set up alerts.

   To manage usage more effectively, set up alerts by navigating to the **Alerts** tab under **Monitoring** from the left-hand menu. Alerts can notify you when your usage reaches specific thresholds, helping to prevent unexpected costs.

### Definition of metrics

Below is a table summarizing the key metrics for Azure text to speech services. 

| **Metric name**                  | **Description** |
|----------------------------------|-----------------|
| **Synthesized Characters**       | Tracks the number of characters converted into speech, including prebuilt neural voice and custom neural voice. For details on billable characters, see [Billable characters](#billable-characters). |
| **Video Seconds Synthesized**    | Measures the total duration of video synthesized, including batch avatar synthesis, real-time avatar synthesis, and custom avatar synthesis.  |
| **Avatar Model Hosting Seconds** | Tracks the total time in seconds that your custom avatar model is hosted. |
| **Voice Model Hosting Hours**    | Tracks the total time in hours that your custom neural voice model is hosted.  |
| **Voice Model Training Minutes** | Measures the total time in minutes for training your custom neural voice model.   |

## Reference docs

* [Speech SDK](speech-sdk.md)
* [REST API: Text to speech](rest-text-to-speech.md)

## Responsible AI 

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment in which it's deployed. Read the transparency notes to learn about responsible AI use and deployment in your systems. 

* [Transparency note and use cases for custom neural voice](/legal/cognitive-services/speech-service/custom-neural-voice/transparency-note-custom-neural-voice?context=/azure/ai-services/speech-service/context/context)  
* [Characteristics and limitations for using custom neural voice](/legal/cognitive-services/speech-service/custom-neural-voice/characteristics-and-limitations-custom-neural-voice?context=/azure/ai-services/speech-service/context/context)   
* [Limited access to custom neural voice](/legal/cognitive-services/speech-service/custom-neural-voice/limited-access-custom-neural-voice?context=/azure/ai-services/speech-service/context/context) 
* [Guidelines for responsible deployment of synthetic voice technology](/legal/cognitive-services/speech-service/custom-neural-voice/concepts-guidelines-responsible-deployment-synthetic?context=/azure/ai-services/speech-service/context/context)   
* [Disclosure for voice talent](/legal/cognitive-services/speech-service/disclosure-voice-talent?context=/azure/ai-services/speech-service/context/context)   
* [Disclosure design guidelines](/legal/cognitive-services/speech-service/custom-neural-voice/concepts-disclosure-guidelines?context=/azure/ai-services/speech-service/context/context)   
* [Disclosure design patterns](/legal/cognitive-services/speech-service/custom-neural-voice/concepts-disclosure-patterns?context=/azure/ai-services/speech-service/context/context)   
* [Code of Conduct for Text to speech integrations](/legal/cognitive-services/speech-service/tts-code-of-conduct?context=/azure/ai-services/speech-service/context/context)   
* [Data, privacy, and security for custom neural voice](/legal/cognitive-services/speech-service/custom-neural-voice/data-privacy-security-custom-neural-voice?context=/azure/ai-services/speech-service/context/context)

## Next steps

* [Text to speech quickstart](get-started-text-to-speech.md)
* [Get the Speech SDK](speech-sdk.md)
