---
title: Custom voice overview - Speech service
titleSuffix: Foundry Tools
description: Custom voice is a text to speech feature that allows you to create a one-of-a-kind, customized, synthetic voice for your applications. You provide your own audio data as a sample.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: concept-article
ms.date: 08/07/2025
ms.author: pafarley
---

# What is custom voice?

Custom voice is a text to speech feature that lets you create a one-of-a-kind, customized, synthetic voice for your applications. With custom voice, you can build a highly natural-sounding voice for your brand or characters by providing human speech samples as fine-tuning data.

> [!IMPORTANT]
> Custom voice access is [limited](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) based on eligibility and usage criteria. Request access on the [intake form](https://aka.ms/customneural).

Out of the box, [text to speech](text-to-speech.md) can be used with standard voices for each [supported language](language-support.md?tabs=tts). The standard voices work well in most text to speech scenarios if a unique voice isn't required.

Custom voice is based on the neural text to speech technology and the multilingual, multi-speaker, universal model. You can create synthetic voices that are rich in speaking styles, or adaptable cross languages. The realistic and natural sounding voice of custom voice can represent brands, personify machines, and allow users to interact with applications conversationally. See the [supported languages](language-support.md?tabs=tts) for custom voice.

## How does it work?

To create a custom voice, use [Speech Studio](https://aka.ms/speechstudio/customvoice) to upload the recorded audio and corresponding scripts, train the model, and deploy the voice to a custom endpoint. 

Creating a great custom voice requires careful quality control in each step, from voice design and data preparation, to the deployment of the voice model to your system. 

Before you get started in Speech Studio, here are some considerations:

- [Design a persona](record-custom-voice-samples.md#choose-your-voice-talent) of the voice that represents your brand by using a persona brief document. This document defines elements such as the features of the voice, and the character behind the voice. This helps to guide the process of creating a custom voice model, including defining the scripts, selecting your voice talent, training, and voice tuning.
- [Select the recording script](record-custom-voice-samples.md#script-selection-criteria) to represent the user scenarios for your voice. For example, you can use the phrases from bot conversations as your recording script if you're creating a customer service bot. Include different sentence types in your scripts, including statements, questions, and exclamations.

Here's an overview of the steps to create a custom voice in Speech Studio:

1. [Create a project](professional-voice-create-project.md) to contain your data, voice models, tests, and endpoints. Each project is specific to a country/region and language. If you're going to create multiple voices, it's recommended that you create a project for each voice.
1. [Set up voice talent](professional-voice-create-project.md). Before you can fine-tune a professional voice, you must submit a recording of the voice talent's consent statement. The voice talent statement is a recording of the voice talent reading a statement that they consent to the usage of their speech data for professional voice fine-tuning.
1. [Prepare fine-tuning data](professional-voice-create-training-set.md) in the right [format](how-to-custom-voice-training-data.md). It's a good idea to capture the audio recordings in a professional quality recording studio to achieve a high signal-to-noise ratio. The quality of the voice model depends heavily on your fine-tuning data. Consistent volume, speaking rate, pitch, and consistency in expressive mannerisms of speech are required.
1. [Train your voice model](professional-voice-train-voice.md). Select at least 300 utterances to create a custom voice. A series of data quality checks are automatically performed when you upload them. To build high-quality voice models, you should fix any errors and submit again.
1. [Test your voice](professional-voice-train-voice.md#test-your-voice-model). Prepare test scripts for your voice model that cover the different use cases for your apps. It’s a good idea to use scripts within and outside the training dataset, so you can test the quality more broadly for different content.
1. [Deploy and use your voice model](professional-voice-deploy-endpoint.md) in your apps.

You can tune, adjust, and use your custom voice, similarly as you would use a standard voice. Convert text into speech in real-time, or generate audio content offline with text input. You use the [REST API](./rest-text-to-speech.md), the [Speech SDK](./get-started-text-to-speech.md), or the [Speech Studio](https://speech.microsoft.com/audiocontentcreation).

> [!TIP]
> Check out the code samples in the [Speech SDK repository on GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/custom-voice/README.md) to see how to use custom voice in your application.

The style and the characteristics of the trained voice model depend on the style and the quality of the recordings from the voice talent used for training. However, you can make several adjustments by using [SSML (Speech Synthesis Markup Language)](./speech-synthesis-markup.md?tabs=csharp) when you make the API calls to your voice model to generate synthetic speech. SSML is the markup language used to communicate with the text to speech service to convert text into audio. The adjustments you can make include change of pitch, rate, intonation, and pronunciation correction. If the voice model is built with multiple styles, you can also use SSML to switch the styles.

## Components sequence

Custom voice consists of three major components: the text analyzer, the neural acoustic
model, and the neural vocoder. To generate natural synthetic speech from text, text is first input into the text analyzer, which provides output in the form of phoneme sequence. A *phoneme* is a basic unit of sound that distinguishes one word from another in a particular language. A sequence of phonemes defines the pronunciations of the words provided in the text.

Next, the phoneme sequence goes into the neural acoustic model to predict acoustic features that define speech signals. Acoustic features include the timbre, the speaking style, speed, intonations, and stress patterns. Finally, the neural vocoder converts the acoustic features into audible waves, so that synthetic speech is generated.

![Flowchart that shows the components of custom voice.](./media/custom-voice/cnv-intro.png)

Neural text to speech voice models are trained by using deep neural networks based on
the recording samples of human voices. For more information, see [this Microsoft blog post](https://techcommunity.microsoft.com/t5/azure-ai/neural-text-to-speech-extends-support-to-15-more-languages-with/ba-p/1505911). To learn more about how a neural vocoder is trained, see [this Microsoft blog post](https://techcommunity.microsoft.com/t5/azure-ai/azure-neural-tts-upgraded-with-hifinet-achieving-higher-audio/ba-p/1847860).

## Responsible AI 

An AI system includes not only the technology, but also the people who use it, the people who are affected by it, and the environment in which it's deployed. Read the transparency notes to learn about responsible AI use and deployment in your systems. 

* [Transparency note and use cases for custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)  
* [Characteristics and limitations for using custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)   
* [Limited access to custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/limited-access) 
* [Guidelines for responsible deployment of synthetic voice technology](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/transparency-note)   
* [Disclosure for voice talent](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/disclosure-voice-talent)   
* [Disclosure design guidelines](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines)   
* [Disclosure design patterns](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-patterns)   
* [Code of Conduct for Text to speech integrations](/azure/ai-foundry/responsible-use-of-ai-overview)   
* [Data, privacy, and security for custom voice](/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/data-privacy-security)

## Next steps

* [Create a project](professional-voice-create-project.md) 
* [Prepare fine-tuning data](professional-voice-create-training-set.md)
* [Train model](professional-voice-train-voice.md)
