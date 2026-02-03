---
title: What Is Azure Speech?
titleSuffix: Foundry Tools
description: Learn how Azure Speech provides speech to text, text to speech, and speech translation so that you can add speech to your applications and devices.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 01/30/2026
ms.author: pafarley
#Customer intent: As a developer, I want to learn about Azure Speech and its capabilities to add speech to my applications, tools, and devices.
---

# What is Azure Speech?

[Azure Speech in Foundry Tools](./speech-features-foundry.md) provides speech to text, text to speech, and other capabilities through a [Microsoft Foundry resource](~/articles/ai-services/multi-service-resource.md?pivots=azportal). You can transcribe speech to text with high accuracy, produce natural-sounding text-to-speech voices, translate spoken audio, and conduct live AI voice conversations.

:::image type="content" border="false" source="media/overview/speech-features-highlight.png" alt-text="Screenshot of tiles that highlight some Azure Speech features.":::

You can create custom voices, add specific words to your base vocabulary, or build your own models. Run Azure Speech anywhere, in the cloud or at the edge in containers. Enable your applications, tools, and devices for speech by using the [Speech CLI](spx-overview.md), [Speech SDK](./speech-sdk.md), and [REST APIs](./rest-speech-to-text.md).

Azure Speech is available for many [languages](language-support.md), [regions](regions.md), and [price points](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

## <a name = "speech-scenarios"></a>Scenarios

Common scenarios for speech include:

- [Captioning](./captioning-concepts.md): Learn how to synchronize captions with your input audio, apply profanity filters, get partial results, apply customizations, and identify spoken languages for multilingual scenarios.
- [Audio content creation](text-to-speech.md#neural-text-to-speech-features): Use neural voices to make interactions with chatbots and voice agents more natural and engaging, convert digital texts such as e-books into audiobooks, and enhance in-car navigation systems.
- [Call center](call-center-overview.md): Transcribe calls in real time or process a batch of calls, redact personal information, and extract insights such as sentiment to help with your call-center use case.
- [Language learning](language-learning-overview.md): Provide pronunciation assessment feedback to language learners, support real-time transcription for remote learning conversations, and read aloud teaching materials with neural voices.
- [Voice Live](voice-live.md): Create natural, humanlike conversational interfaces for applications and experiences. The Voice Live feature provides fast, reliable interaction between a human and an agent implementation.
- [Speech translation](speech-translation.md): Generate high-quality speech-to-speech translation in real time, or automatically generate translated videos in a broad range of languages.
- [Video avatar creation](/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar): Create lifelike and high-quality synthetic talking avatar videos for various real-time and batch applications while adhering to responsible AI practices.

Microsoft uses Azure Speech for many scenarios, such as captioning in Microsoft Teams, dictation in Microsoft Office 365, and Read Aloud in the Microsoft Edge browser.

:::image type="content" border="false" source="media/overview/microsoft-uses-speech.png" alt-text="Screenshot that shows logos of Microsoft products that use Azure Speech.":::

## Capabilities

The following sections summarize Azure Speech features and provide links for more information.

### Speech to text

Use [speech to text](speech-to-text.md) to convert audio into text. Choose from:

- [Real-time transcription](get-started-speech-to-text.md) for streaming audio.
- [Fast transcription](fast-transcription-create.md) for pre-recorded audio files.
- [Batch transcription](batch-transcription.md) for processing large volumes of audio asynchronously.

The base model might not be sufficient if the audio contains ambient noise or includes industry and domain-specific jargon. In these cases, you can create and train [custom speech models](custom-speech-overview.md) with acoustic, language, and pronunciation data. Custom speech models are private and can offer a competitive advantage.

### Text to speech

With [text to speech](text-to-speech.md), you can convert input text into humanlike synthesized speech. Use neural voices, which are humanlike voices powered by deep neural networks. Use [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup.md) to fine-tune the pitch, pronunciation, speaking rate, volume, and more.

Voice options include:

- **Standard voice**: You can choose among highly natural out-of-the-box voices. Check the standard voice samples in the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery) and determine the right voice for your business needs.
- **Custom voice**: You can create a [custom voice](custom-neural-voice.md) that's recognizable and unique to your brand or product. Custom voices are private and can offer a competitive advantage. Check the [custom voice samples](https://aka.ms/customvoice).

### Text-to-speech avatar

[Text-to-speech avatar](/azure/ai-services/speech-service/text-to-speech-avatar/what-is-text-to-speech-avatar) converts text into a digital video of a photorealistic human speaking with a natural-sounding voice. The video can be synthesized asynchronously or in real time. You can build applications integrated with text-to-speech avatar through an API, or use text-to-speech avatar in Foundry to create video content without coding. The feature empowers you to deliver lifelike and high-quality synthetic talking avatar videos for various applications while adhering to responsible AI practices.

You can choose from a range of standard voices for the avatar. The language support for text-to-speech avatar is the same as the language support for text to speech.

### Speech translation

[Speech translation](speech-translation.md) enables real-time, multilingual translation of speech to your applications, tools, and devices. Use this feature for speech-to-speech and speech-to-text translation.

### LLM speech (preview)

Take advantage of a large language model (LLM)-enhanced speech model in [LLM speech](llm-speech.md). This feature currently supports the following tasks:

- `transcribe`: Convert pre-recorded audio into text.
- `translate`: Convert pre-recorded audio into text in a specified target language.

The LLM-enhanced speech model delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. LLM speech shares the same ultra-fast inference performance as fast transcription. Use cases include generating captions and subtitles from audio files, summarizing meeting notes, assisting call center agents, transcribing voicemails, and more.

### Language identification

[Language identification](language-identification.md) helps you identify languages spoken in audio by comparing them against a list of [supported languages](language-support.md). Use language identification by itself, with speech-to-text recognition, or with speech translation.

### Pronunciation assessment

[Pronunciation assessment](./how-to-pronunciation-assessment.md) evaluates speech pronunciation and gives speakers feedback on the accuracy and fluency of spoken audio. By using pronunciation assessment, language learners can practice, get instant feedback, and improve their pronunciation so that they can speak and present with confidence.

## Delivery and presence

You can deploy Azure Speech features in the cloud or on-premises.

By using [containers](speech-container-howto.md), you can bring the service closer to your data for compliance, security, or other operational reasons.

Azure Speech deployment in sovereign clouds is available for some government entities and their partners. For example, the Azure Government cloud is available to US government entities and their partners. The Azure operated by 21Vianet cloud is available to organizations that have a business presence in China. For more information, see [Speech service in sovereign clouds](sovereign-clouds.md).

:::image type="content" border="false" source="media/overview/speech-delivery-presence.png" alt-text="Diagram that shows where Azure Speech can be deployed and accessed.":::

## Integration of Azure Speech in your application

[Speech Studio](speech-studio-overview.md) is a set of UI-based tools for building and integrating features from Azure Speech in your applications. You create projects in Speech Studio by using a no-code approach. You can then reference those assets in your applications by using:

- [Speech SDK](speech-sdk.md). This SDK exposes many of the Azure Speech capabilities that you can use to develop speech-enabled applications. The Speech SDK is available in many programming languages and across all platforms.

- [Speech CLI](spx-overview.md). With this command-line tool, you can use Azure Speech without having to write any code. Most features in the Speech SDK are available in the Speech CLI, and some advanced features and customizations are simplified in the Speech CLI.

- [REST APIs](./rest-speech-to-text.md). In some cases, you can't or shouldn't use the Speech SDK. In those cases, you can use REST APIs to access Azure Speech. For example, use REST APIs for [batch transcription](batch-transcription.md).

## Code samples

Sample code for Azure Speech is available on GitHub. These samples cover common scenarios like reading audio from a file or stream, continuous and single-shot recognition, and working with custom models. Use these links to view SDK and REST samples:

- [Speech-to-text, text-to-speech, and speech translation samples (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
- [Batch transcription samples (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch)
- [Text-to-speech samples (REST)](https://github.com/Azure-Samples/Cognitive-Speech-TTS)

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment where it's deployed. Use the following resources to learn about responsible AI use and deployment in your systems.

### Speech to text

- [Transparency note and use cases](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note)
- [Characteristics and limitations](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note)
- [Integration and responsible use](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/transparency-note)
- [Data, privacy, and security](/azure/ai-foundry/responsible-ai/speech-service/speech-to-text/data-privacy-security)

### Pronunciation assessment

- [Transparency note and use cases](/azure/ai-foundry/responsible-ai/speech-service/pronunciation-assessment/transparency-note-pronunciation-assessment)
- [Characteristics and limitations](/azure/ai-foundry/responsible-ai/speech-service/pronunciation-assessment/characteristics-and-limitations-pronunciation-assessment)

### Custom voice

- [Transparency note and use cases](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
- [Characteristics and limitations](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
- [Limited access](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access)
- [Responsible deployment of synthetic speech](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)
- [Disclosure of voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent)
- [Disclosure of design guidelines](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines)
- [Disclosure of design patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns)
- [Code of conduct](/azure/ai-foundry/responsible-use-of-ai-overview)
- [Data, privacy, and security](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security)

## Related content

The following quickstarts are available for Azure Speech features. Each quickstart teaches you basic design patterns in many popular programming languages and has you running code in less than 10 minutes.

- [Speech-to-text quickstart](get-started-speech-to-text.md)
- [Text-to-speech quickstart](get-started-text-to-speech.md)
- [Speech translation quickstart](./get-started-speech-translation.md)
