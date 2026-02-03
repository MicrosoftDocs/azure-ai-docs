---
title: What are OpenAI text to speech voices?
titleSuffix: Foundry Tools
description: Learn about OpenAI voices that you can use for text to speech in Foundry Tools.
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
manager: nitinme
ms.date: 10/21/2025
ms.service: azure-ai-speech
ms.topic: overview
ms.custom:
  - references_regions
  - build-2025
# customer intent: As a user who implements text to speech, I want to understand the options and differences between available OpenAI text to speech voices in Foundry Tools.
---

# What are OpenAI text to speech voices? 

Like Azure Speech in Foundry Tools voices, OpenAI text to speech voices deliver high-quality speech synthesis to convert written text into natural sounding spoken audio. This unlocks a wide range of possibilities for immersive and interactive user experiences. 

OpenAI text to speech voices are available via two model variants: `Neural` and `NeuralHD`.

- `Neural`: Optimized for real-time use cases with the lowest latency, but lower quality than `NeuralHD`.
- `NeuralHD`: Optimized for quality.

## Available text to speech voices in Foundry Tools

You might ask: If I want to use an OpenAI text to speech voice, should I use it via the Azure OpenAI in Microsoft Foundry Models or via Azure Speech? What are the scenarios that guide me to use one or the other?

Each voice model offers distinct features and capabilities, allowing you to choose the one that best suits your specific needs. You want to understand the options and differences between available text to speech voices in Foundry Tools.

You can choose from the following text to speech voices in Foundry Tools:

- OpenAI text to speech voices in [Azure OpenAI](../openai/reference.md#text-to-speech-preview). For the current list of supported regions, see the [Speech service regions table](regions.md?tabs=tts).
- OpenAI text to speech voices in [Azure Speech](./language-support.md?tabs=tts#multilingual-voices). For the current list of supported regions, see the [Speech service regions table](regions.md?tabs=tts).
- Azure Speech service [text to speech voices](./language-support.md?tabs=tts#standard-voices). Available in dozens of regions. See the [region list](regions.md#regions).

## OpenAI text to speech voices via Azure OpenAI or via Azure Speech?

If you want to use OpenAI text to speech voices, you can choose whether to use them via [Azure OpenAI](../../ai-foundry/openai/text-to-speech-quickstart.md) or via [Azure Speech](./get-started-text-to-speech.md). You can visit the [Voice Gallery](https://speech.microsoft.com/portal/voicegallery) to listen to samples of Azure OpenAI voices or synthesize speech with your own text using the [Audio Content Creation](https://speech.microsoft.com/portal/audiocontentcreation). The audio output is identical in both cases, with only a few feature differences between the two services. See the table below for details.

Here's a comparison of features between OpenAI text to speech voices in Azure OpenAI and OpenAI text to speech voices in Azure Speech. 

| Feature | Azure OpenAI (OpenAI voices) | Azure Speech (OpenAI voices) | Azure Speech voices |
|---------|---------------|------------------------|------------------------|
| **Region** | North Central US, Sweden Central | North Central US, Sweden Central | Available in dozens of regions. See the [region list](regions.md#regions).|
| **Voice variety** | 6 | 12 | More than 500 |
| **Multilingual voice number** | 6 | 12 | 49 |
| **Max multilingual language coverage** | 57 | 57 | 77 |
| **Speech Synthesis Markup Language (SSML) support** | Not supported | Support for [a subset of SSML elements](#ssml-elements-supported-by-openai-text-to-speech-voices-in-azure-speech). | Support for the [full set of SSML](speech-synthesis-markup-structure.md) in Azure Speech. |
| **Development options** | REST API | Speech SDK, Speech CLI, REST API | Speech SDK, Speech CLI, REST API |
| **Deployment option** | Cloud only | Cloud only | Cloud, embedded, hybrid, and containers. |
| **Real-time or batch synthesis** |  Real-time | Real-time | Real-time and batch synthesis |
| **Latency** | greater than 500 ms | greater than 500 ms | less than 300 ms |
| **Sample rate of synthesized audio** | 24 kHz | 8, 16, 24, and 48 kHz | 8, 16, 24, and 48 kHz |
| **Speech output audio format** | opus, mp3, aac, flac | opus, mp3, pcm, truesilk | opus, mp3, pcm, truesilk |

There are additional features and capabilities available in Azure Speech that aren't available with OpenAI voices. For example:
- OpenAI text to speech voices in Azure Speech [only support a subset of SSML elements](#ssml-elements-supported-by-openai-text-to-speech-voices-in-azure-speech). Azure Speech voices support the full set of SSML elements.
- Azure Speech supports [word boundary events](./how-to-speech-synthesis.md#subscribe-to-synthesizer-events). OpenAI voices don't support word boundary events. 

### Available OpenAI text to speech voices

The available OpenAI voices in Azure OpenAI are: 

- `alloy`
- `echo`
- `fable`
- `onyx`
- `nova`
- `shimmer` 

The available OpenAI voices in Azure Speech are:

- `en-US-AlloyMultilingualNeural`
- `en-US-EchoMultilingualNeural`
- `en-US-FableMultilingualNeural`
- `en-US-OnyxMultilingualNeural`
- `en-US-NovaMultilingualNeural`
- `en-US-ShimmerMultilingualNeural`
- `en-US-AlloyMultilingualNeuralHD`
- `en-US-EchoMultilingualNeuralHD`
- `en-US-FableMultilingualNeuralHD`
- `en-US-OnyxMultilingualNeuralHD`
- `en-US-NovaMultilingualNeuralHD`
- `en-US-ShimmerMultilingualNeuralHD`

## SSML elements supported by OpenAI text to speech voices in Azure Speech

The [Speech Synthesis Markup Language (SSML)](./speech-synthesis-markup.md) with input text determines the structure, content, and other characteristics of the text to speech output. For example, you can use SSML to define a paragraph, a sentence, a break or a pause, or silence. You can wrap text with event tags such as bookmark or viseme that can be processed later by your application.

The following table outlines the Speech Synthesis Markup Language (SSML) elements supported by OpenAI text to speech voices in Azure Speech. Only the following subset of SSML tags are supported for OpenAI voices. See [SSML document structure and events](speech-synthesis-markup-structure.md) for more information.

| SSML element name | Description |
| --- | --- |
| `<speak>` | Encloses the entire content to be spoken. It’s the root element of an SSML document. |
| `<voice>` | Specifies a voice used for text to speech output. |
| `<sub>` | Indicates that the alias attribute's text value should be pronounced instead of the element's enclosed text. |
| `<say-as>` | Indicates the content type, such as number or date, of the element's text.<br/><br/>All of the `interpret-as` property values are supported for this element except `interpret-as="name"`. For example, `<say-as interpret-as="date" format="dmy">10-12-2016</say-as>` is supported, but `<say-as interpret-as="name">ED</say-as>` isn't supported. For more information, see [pronunciation with SSML](./speech-synthesis-markup-pronunciation.md#say-as-element). |
| `<s>` | Denotes sentences. |
| `<lang>` | Indicates the default locale for the language that you want the neural voice to speak.  |
| `<break>` | Use to override the default behavior of breaks or pauses between words. |

## Related content

- [Try the text to speech quickstart in Azure Speech](get-started-text-to-speech.md)
- [Try the text to speech via Azure OpenAI](../../ai-foundry/openai/text-to-speech-quickstart.md)
