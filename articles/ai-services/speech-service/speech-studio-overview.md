---
title: "Speech Studio overview - Speech service"
titleSuffix: Azure AI services
description: Speech Studio is a set of UI-based tools for building and integrating features from Speech service in your applications.
author: eric-urban
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 9/24/2024
ms.author: eur
#Customer intent: As a developer, I want to learn about Speech Studio.
---

# What is Speech Studio?

[Speech Studio](https://aka.ms/speechstudio/) is a set of UI-based tools for building and integrating features from Azure AI Speech service in your applications. You create projects in Speech Studio by using a no-code approach, and then reference those assets in your applications by using the [Speech SDK](speech-sdk.md), the [Speech CLI](spx-overview.md), or the REST APIs.

> [!TIP]
> You can also try speech to text and text to speech in the [Azure AI Foundry portal](https://ai.azure.com) without signing up or writing any code.

## Speech Studio scenarios

Explore, try out, and view sample code for some of common use cases.

* [Captioning](https://aka.ms/speechstudio/captioning): Choose a sample video clip to see real-time or offline processed captioning results. Learn how to synchronize captions with your input audio, apply profanity filters, get partial results, apply customizations, and identify spoken languages for multilingual scenarios. For more information, see the [captioning quickstart](captioning-quickstart.md).

* [Call Center](https://aka.ms/speechstudio/callcenter): View a demonstration on how to use the Language and Speech services to analyze call center conversations. Transcribe calls in real-time or process a batch of calls, redact personally identifying information, and extract insights such as sentiment to help with your call center use case. For more information, see the [call center quickstart](call-center-quickstart.md).

For a demonstration of these scenarios in Speech Studio, view this [introductory video](https://youtu.be/mILVerU6DAw).
> [!VIDEO https://www.youtube.com/embed/mILVerU6DAw]

## Speech Studio features

In Speech Studio, the following Speech service features are available as project types:

* [Real-time speech to text](https://aka.ms/speechstudio/speechtotexttool): Quickly test speech to text by dragging audio files here without having to use any code. Speech Studio has a demo tool for seeing how speech to text works on your audio samples. To explore the full functionality, see [What is speech to text](speech-to-text.md).

* [Batch speech to text](https://aka.ms/speechstudio/batchspeechtotext): Quickly test batch transcription capabilities to transcribe a large amount of audio in storage and receive results asynchronously, To learn more about Batch Speech-to-text, see [Batch speech to text overview](batch-transcription.md).

* [Custom speech](https://aka.ms/speechstudio/customspeech): Create speech recognition models that are tailored to specific vocabulary sets and styles of speaking. In contrast to the base speech recognition model, Custom speech models become part of your unique competitive advantage because they're not publicly accessible. To get started with uploading sample audio to create a custom speech model, see [Upload training and testing datasets](how-to-custom-speech-upload-data.md).

* [Pronunciation assessment](https://aka.ms/speechstudio/pronunciationassessment): Evaluate speech pronunciation and give speakers feedback on the accuracy and fluency of spoken audio. Speech Studio provides a sandbox for testing this feature quickly, without code. To use the feature with the Speech SDK in your applications, see the [Pronunciation assessment](how-to-pronunciation-assessment.md) article.

* [Speech Translation](https://aka.ms/speechstudio/speechtranslation): Quickly test and translate speech into other languages of your choice with low latency. To explore the full functionality, see [What is speech translation](speech-translation.md).

* [Voice Gallery](https://aka.ms/speechstudio/voicegallery): Build apps and services that speak naturally. Choose from a broad portfolio of [languages, voices, and variants](language-support.md?tabs=tts). Bring your scenarios to life with highly expressive and human-like neural voices.

* [Custom voice](https://aka.ms/speechstudio/customvoice): Create custom, one-of-a-kind voices for text to speech. You supply audio files and create matching transcriptions in Speech Studio, and then use the custom voices in your applications. To create and use custom voices via endpoints, see [Create and use your voice model](professional-voice-train-voice.md). 

* [Audio Content Creation](https://aka.ms/speechstudio/audiocontentcreation): A no-code approach for text to speech synthesis. You can use the output audio as-is, or as a starting point for further customization. You can build highly natural audio content for various scenarios, such as audiobooks, news broadcasts, video narrations, and chat bots. For more information, see the [Audio Content Creation](how-to-audio-content-creation.md) documentation.

* [Custom Keyword](https://aka.ms/speechstudio/customkeyword): A custom keyword is a word or short phrase that you can use to voice-activate a product. You create a custom keyword in Speech Studio, and then generate a binary file to [use with the Speech SDK](custom-keyword-basics.md) in your applications.

## Next steps

* [Explore Speech Studio](https://speech.microsoft.com)
