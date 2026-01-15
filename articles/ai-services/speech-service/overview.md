---
title: What Is Azure Speech?
titleSuffix: Foundry Tools
description: Get an overview of Azure Speech, which provides speech to text, text to speech, speech translation, and other capabilities with a Microsoft Foundry resource.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 08/07/2025
ms.author: pafarley
#Customer intent: As a developer, I want to learn about Azure Speech and its capabilities to add speech to my applications, tools, and devices.
---

# What is Azure Speech?

Azure Speech in Foundry Tools provides speech to text, text to speech, and other capabilities with a [Microsoft Foundry resource](~/articles/ai-services/multi-service-resource.md?pivots=azportal). You can transcribe speech to text with high accuracy, produce natural-sounding text-to-speech voices, translate spoken audio, and conduct live AI voice conversations.

:::image type="content" border="false" source="media/overview/speech-features-highlight.png" alt-text="Image of tiles that highlight some Azure Speech features.":::

Create custom voices, add specific words to your base vocabulary, or build your own models. Run Azure Speech anywhere, in the cloud or at the edge in containers. Enable your applications, tools, and devices for Azure Speech by using the [Speech CLI](spx-overview.md), [Speech SDK](./speech-sdk.md), and [REST APIs](./rest-speech-to-text.md).

Azure Speech is available for many [languages](language-support.md), [regions](regions.md), and [price points](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/).

## Scenarios

Common scenarios for Azure Speech include:

- [Captioning](./captioning-concepts.md): Learn how to synchronize captions with your input audio, apply profanity filters, get partial results, apply customizations, and identify spoken languages for multilingual scenarios.
- [Audio content creation](text-to-speech.md#more-about-neural-text-to-speech-features): You can use neural voices to make interactions with chatbots and voice agents more natural and engaging, convert digital texts such as e-books into audiobooks, and enhance in-car navigation systems.
- [Call center](call-center-overview.md): Transcribe calls in real time or process a batch of calls, redact personal information, and extract insights such as sentiment to help with your call-center use case.
- [Language learning](language-learning-overview.md): Provide pronunciation assessment feedback to language learners, support real-time transcription for remote learning conversations, and read aloud teaching materials with neural voices.
- [Voice live](voice-live.md): Create natural, humanlike conversational interfaces for applications and experiences. The voice live feature provides fast, reliable interaction between a human and an agent implementation.

Microsoft uses Azure Speech for many scenarios, such as captioning in Teams, dictation in Office 365, and Read Aloud in the Microsoft Edge browser.

:::image type="content" border="false" source="media/overview/microsoft-uses-speech.png" alt-text="Diagram that shows logos of Microsoft products that use Azure Speech.":::

## Capabilities

The following sections summarize Azure Speech features and provide links for more information.

### Speech to text

Use [speech to text](speech-to-text.md) to convert audio into text. Capabilities include [real-time transcription](get-started-speech-to-text.md) for streaming audio, [fast transcription](fast-transcription-create.md) for pre-recorded audio files, or [batch transcription](batch-transcription.md) for processing large volumes of audio asynchronously.

The base model might not be sufficient if the audio contains ambient noise or includes numerous industry and domain-specific jargon. In these cases, you can create and train [custom speech models](custom-speech-overview.md) with acoustic, language, and pronunciation data. Custom speech models are private and can offer a competitive advantage.

### Text to speech

With [text to speech](text-to-speech.md), you can convert input text into human like synthesized speech. Use neural voices, which are human like voices powered by deep neural networks. Use the [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup.md) to fine-tune the pitch, pronunciation, speaking rate, volume, and more.

- Standard voice: Highly natural out-of-the-box voices. Check the standard voice samples the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery) and determine the right voice for your business needs.
- Custom voice: Besides the standard voices that come out of the box, you can also create a [custom voice](custom-neural-voice.md) that is recognizable and unique to your brand or product. Custom voices are private and can offer a competitive advantage. Check the [custom voice samples](https://aka.ms/customvoice).

### Speech translation

[Speech translation](speech-translation.md) enables real-time, multilingual translation of speech to your applications, tools, and devices. Use this feature for speech-to-speech and speech-to-text translation.

### LLM speech (preview)

[LLM speech](llm-speech.md) currently supports the following tasks:

- `transcribe`: Convert pre-recorded audio into text.
- `translate`: Convert pre-recorded audio into text in a specified target language.

LLM speech uses a large-language-model-enhanced speech model that delivers improved quality, deep contextual understanding, multilingual support, and prompt-tuning capabilities. It shares the same ultra-fast inference performance as fast transcription, making it ideal for use cases such as generating captions and subtitles from audio files, summarizing meeting notes, assisting call center agents, transcribing voicemails, and more.

### Language identification

[Language identification](language-identification.md) is used to identify languages spoken in audio when compared against a list of [supported languages](language-support.md). Use language identification by itself, with speech-to-text recognition, or with speech translation.

### Pronunciation assessment

[Pronunciation assessment](./how-to-pronunciation-assessment.md) evaluates speech pronunciation and gives speakers feedback on the accuracy and fluency of spoken audio. With pronunciation assessment, language learners can practice, get instant feedback, and improve their pronunciation so that they can speak and present with confidence.

## Delivery and presence

You can deploy Azure Speech in Foundry Tools features in the cloud or on-premises.

With [containers](speech-container-howto.md), you can bring the service closer to your data for compliance, security, or other operational reasons.

Azure Speech deployment in sovereign clouds is available for some government entities and their partners. For example, the Azure Government cloud is available to US government entities and their partners. Microsoft Azure operated by 21Vianet cloud is available to organizations with a business presence in China. For more information, see [sovereign clouds](sovereign-clouds.md).

:::image type="content" border="false" source="media/overview/speech-delivery-presence.png" alt-text="Diagram showing where Azure Speech can be deployed and accessed.":::

## Use Azure Speech in your application

[Speech Studio](speech-studio-overview.md) is a set of UI-based tools for building and integrating features from Azure Speech in your applications. You create projects in Speech Studio by using a no-code approach, and then reference those assets in your applications by using the [Speech SDK](speech-sdk.md), the [Speech CLI](spx-overview.md), or the REST APIs.

The Speech CLI is a command-line tool for using Azure Speech without having to write any code. Most features in the Speech SDK are available in the Speech CLI, and some advanced features and customizations are simplified in the Speech CLI.

The Speech SDK exposes many of the Azure Speech capabilities you can use to develop speech-enabled applications. The Speech SDK is available in many programming languages and across all platforms.

In some cases, you can't or shouldn't use the Speech SDK. In those cases, you can use REST APIs to access Azure Speech. For example, use REST APIs for [batch transcription](batch-transcription.md).

## Get started

We offer quickstarts in many popular programming languages. Each quickstart is designed to teach you basic design patterns and have you running code in less than 10 minutes. See the following list for the quickstart for each feature:

- [Speech-to-text quickstart](get-started-speech-to-text.md)
- [Text-to-speech quickstart](get-started-text-to-speech.md)
- [Speech translation quickstart](./get-started-speech-translation.md)

## Code samples

Sample code for Azure Speech is available on GitHub. These samples cover common scenarios like reading audio from a file or stream, continuous and single-shot recognition, and working with custom models. Use these links to view SDK and REST samples:

- [Speech-to-text, text-to-speech, and speech translation samples (SDK)](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
- [Batch transcription samples (REST)](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/batch)
- [Text-to-speech samples (REST)](https://github.com/Azure-Samples/Cognitive-Speech-TTS)

## Responsible AI

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment in which it's deployed. Read the transparency notes to learn about responsible AI use and deployment in your systems.

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

- [Get started with speech to text](get-started-speech-to-text.md)
- [Get started with text to speech](get-started-text-to-speech.md)
