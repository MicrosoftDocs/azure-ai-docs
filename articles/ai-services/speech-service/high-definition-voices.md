---
title: What are neural text to speech HD voices?
titleSuffix: Azure AI services
description: Learn about neural text to speech HD voices that you can use with speech synthesis.
author: eric-urban
ms.author: eur
ms.reviewer: eur
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 4/8/2025
ms.custom: references_regions
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech HD voices in Azure AI Speech.
---

# What are high definition voices?

Azure AI Speech continues to advance in the field of text to speech technology with the introduction of neural text to speech high definition (HD) voices. The HD voices can understand the content, automatically detect emotions in the input text, and adjust the speaking tone in real-time to match the sentiment. HD voices maintain a consistent voice persona from their neural (and non HD) counterparts, and deliver even more value through enhanced features.

## Key features of neural text to speech HD voices

The following are the key features of Azure AI Speech HD voices:

| Key features | Description |
|--------------|-------------|
| **Human-like speech generation** | Neural text to speech HD voices can generate highly natural and human-like speech. The model is trained on millions of hours of multilingual data, enabling it to accurately interpret input text and generate speech with the appropriate emotion, pace, and rhythm without manual adjustments. |
| **Conversational** | Neural text to speech HD voices can replicate natural speech patterns, including spontaneous pauses and emphasis. When given conversational text, the model can reproduce common phonemes like pauses and filler words. The generated voice sounds as if someone is conversing directly with you. |
| **Prosody variations** | Neural text to speech HD voices introduce slight variations in each output to enhance realism. These variations make the speech sound more natural, as human voices naturally exhibit variation. |
| **High fidelity** | The primary objective of neural text to speech HD voices is to generate high-fidelity audio. The synthetic speech produced by our system can closely mimic human speech in both quality and naturalness. |

## Comparison of Azure AI Speech HD voices to other Azure text to speech voices

How do Azure AI Speech HD voices compare to other Azure text to speech voices? How do they differ in terms of features and capabilities? 

Here's a comparison of features between Azure AI Speech HD voices, Azure OpenAI HD voices, and Azure AI Speech voices:

| Feature | Azure AI Speech HD voices  | Azure OpenAI HD voices | Azure AI Speech voices (not HD) |
|---------|---------------|------------------------|------------------------|
| **Region** | East US, Southeast Asia, West Europe | North Central US, Sweden Central | Available in dozens of regions. See the [region list](regions.md#regions).|
| **Number of voices** | 12 | 6 | More than 500 |
| **Multilingual**  | No (perform on primary language only) | Yes  | Yes (applicable only to multilingual voices)  |
| **SSML support** | Support for [a subset of SSML elements](#supported-and-unsupported-ssml-elements-for-azure-ai-speech-hd-voices).|  Support for [a subset of SSML elements](openai-voices.md#ssml-elements-supported-by-openai-text-to-speech-voices-in-azure-ai-speech).  | Support for the [full set of SSML](speech-synthesis-markup-structure.md) in Azure AI Speech.  |
| **Development options** | Speech SDK, Speech CLI, REST API  | Speech SDK, Speech CLI, REST API  | Speech SDK, Speech CLI, REST API  |
| **Deployment options**  | Cloud only | Cloud only | Cloud, embedded, hybrid, and containers. |
| **Real-time or batch synthesis**  | Real-time only  | Real-time and batch synthesis  | Real-time and batch synthesis |
| **Latency**  | Less than 300 ms | Greater than 500 ms | Less than 300 ms  |
| **Sample rate of synthesized audio** | 8, 16, 24, and 48 kHz  | 8, 16, 24, and 48 kHz | 8, 16, 24, and 48 kHz |
| **Speech output audio format** | opus, mp3, pcm, truesilk |  opus, mp3, pcm, truesilk  |  opus, mp3, pcm, truesilk  |

## Supported Azure AI Speech HD voices

The Azure AI Speech HD voice values are in the format `voicename:basemodel:version`. The name before the colon, such as `en-US-Ava`, is the voice persona name and its original locale. The base model is tracked by versions in subsequent updates.

Currently, `DragonHD` is the only base model available for Azure AI Speech HD voices. To ensure that you're using the latest version of the base model that we provide without having to make a code change, use the `LatestNeural` version.

For example, for the persona `en-US-Ava` you can specify the following HD voice values:
- `en-US-Ava:DragonHDLatestNeural`: Always uses the latest version of the base model that we provide later.

The following table lists the Azure AI Speech HD voices that are currently available.

| Voice Name                                 | Gender | Status  | Note                                  |
|-------------------------------------------|--------|---------|---------------------------------------|
| de-DE-Florian:DragonHDLatestNeural        | Male   | GA      |                                       |
| de-DE-Seraphina:DragonHDLatestNeural      | Female | GA      |                                       |
| en-US-Adam:DragonHDLatestNeural           | Male   | GA      |                                       |
| en-US-Alloy:DragonHDLatestNeural          | Male   | Preview |                                       |
| en-US-Andrew:DragonHDLatestNeural         | Male   | GA      |                                       |
| en-US-Andrew2:DragonHDLatestNeural        | Male   | GA      | Optimized for conversational content  |
| en-US-Andrew3:DragonHDLatestNeural        | Male   | Preview | Optimized for podcast content         |
| en-US-Aria:DragonHDLatestNeural           | Female | Preview |                                       |
| en-US-Ava:DragonHDLatestNeural            | Female | GA      |                                       |
| en-US-Ava3:DragonHDLatestNeural           | Female | Preview | Optimized for podcast content         |
| en-US-Brian:DragonHDLatestNeural          | Male   | GA      |                                       |
| en-US-Davis:DragonHDLatestNeural          | Male   | GA      |                                       |
| en-US-Emma:DragonHDLatestNeural           | Female | GA      |                                       |
| en-US-Emma2:DragonHDLatestNeural          | Female | GA      | Optimized for conversational content  |
| en-US-Jenny:DragonHDLatestNeural          | Female | Preview |                                       |
| en-US-MultiTalker-Ava-Andrew:DragonHDLatestNeural | Male | Preview |                                       |
| en-US-Nova:DragonHDLatestNeural           | Female | Preview |                                       |
| en-US-Phoebe:DragonHDLatestNeural         | Female | Preview |                                       |
| en-US-Serena:DragonHDLatestNeural         | Female | Preview |                                       |
| en-US-Steffan:DragonHDLatestNeural        | Male   | GA      |                                       |
| es-ES-Tristan:DragonHDLatestNeural        | Male   | GA      |                                       |
| es-ES-Ximena:DragonHDLatestNeural         | Female | GA      |                                       |
| fr-FR-Remy:DragonHDLatestNeural           | Male   | GA      |                                       |
| fr-FR-Vivienne:DragonHDLatestNeural       | Female | GA      |                                       |
| ja-JP-Masaru:DragonHDLatestNeural         | Male   | GA      |                                       |
| ja-JP-Nanami:DragonHDLatestNeural         | Female | GA      |                                       |
| zh-CN-Xiaochen:DragonHDLatestNeural       | Female | GA      |                                       |
| zh-CN-Yunfan:DragonHDLatestNeural         | Male   | GA      |                                       |


## How to use Azure AI Speech HD voices

You can use HD voices with the same Speech SDK and REST APIs as the non HD voices. 

Here are some key points to consider when using Azure AI Speech HD voices:

- **Voice locale**: The locale in the voice name indicates its original language and region.
- **Base models**:
  - HD voices come with a base model that understands the input text and predicts the speaking pattern accordingly. You can specify the desired model (such as DragonHDLatestNeural) according to the availability of each voice.
- **SSML usage**: To reference a voice in SSML, use the format `voicename:basemodel:version`. The name before the colon, such as `de-DE-Seraphina`, is the voice persona name and its original locale. The base model is tracked by versions in subsequent updates.
- **Temperature parameter**:
  - The temperature value is a float ranging from 0 to 1, influencing the randomness of the output. You can also adjust the temperature parameter to control the variation of outputs. Less randomness yields more stable results, while more randomness offers variety but less consistency.
  - Lower temperature results in less randomness, leading to more predictable outputs. Higher temperature increases randomness, allowing for more diverse outputs. The default temperature is set at 1.0.

Here's an example of how to use Azure AI Speech HD voices in SSML:

```ssml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
<voice name='en-US-Ava:DragonHDLatestNeural' parameters='temperature=0.8'>Here is a test</voice>
</speak>
```

## Supported and unsupported SSML elements for Azure AI Speech HD voices

The Speech Synthesis Markup Language (SSML) with input text determines the structure, content, and other characteristics of the text to speech output. For example, you can use SSML to define a paragraph, a sentence, a break or a pause, or silence. You can wrap text with event tags such as bookmark or viseme that your application processes later.

The Azure AI Speech HD voices don't support all SSML elements or events that other Azure AI Speech voices support. Of particular note, Azure AI Speech HD voices don't support [word boundary events](./how-to-speech-synthesis.md#subscribe-to-synthesizer-events). 

For detailed information on the supported and unsupported SSML elements for Azure AI Speech HD voices, refer to the following table. For instructions on how to use SSML elements, refer to the [Speech Synthesis Markup Language (SSML) documentation](speech-synthesis-markup-structure.md). 

| SSML element | Description  | Supported in Azure AI Speech HD voices |
|------------------------------|--------------------------------|-----------------------------------|
| `<voice>`  | Specifies the voice and optional effects (`eq_car` and `eq_telecomhp8k`). | Yes |
| `<mstts:express-as>`  | Specifies speaking styles and roles. | No  |
| `<mstts:ttsembedding>` |  Specifies the `speakerProfileId` property for a personal voice. | No |
| `<lang xml:lang>` | Specifies the speaking language.  | Yes |
| `<prosody>`  |  Adjusts pitch, contour, range, rate, and volume. | No |
| `<emphasis>`| Adds or removes word-level stress for the text. | No|
| `<audio>`| Embeds prerecorded audio into an SSML document. | No|
| `<mstts:audioduration>` | Specifies the duration of the output audio. | No  |
| `<mstts:backgroundaudio>`  | Adds background audio to your SSML documents or mixes an audio file with text to speech.  | No  |
| `<phoneme>`  |Specifies phonetic pronunciation in SSML documents. | No |
| `<lexicon>`  | Defines how multiple entities are read in SSML.  | Yes (only supports alias)  |
| `<say-as>` | Indicates the content type, such as number or date, of the element's text.  | Yes  |
| `<sub>`  |  Indicates that the alias attribute's text value should be pronounced instead of the element's enclosed text.  | Yes |
| `<math>` | Uses the MathML as input text to properly pronounce mathematical notations in the output audio.  | No |
| `<bookmark>` | Gets the offset of each marker in the audio stream.  | No |
| `<break>`  | Overrides the default behavior of breaks or pauses between words. | No  |
| `<mstts:silence>`  | Inserts pause before or after text, or between two adjacent sentences.  | No |
| `<mstts:viseme>` | Defines the position of the face and mouth while a person is speaking.  | No  |
| `<p>`  | Denotes paragraphs in SSML documents.  | Yes |
| `<s>`  | Denotes sentences in SSML documents.  | Yes  |

> [!NOTE]
> Although a [previous section in this guide](#comparison-of-azure-ai-speech-hd-voices-to-other-azure-text-to-speech-voices) also compared Azure AI Speech HD voices to Azure OpenAI HD voices, the SSML elements supported by Azure AI Speech aren't applicable to Azure OpenAI voices. 

## Related content

- [Try the text to speech quickstart in Azure AI Speech](get-started-text-to-speech.md)
- [Learn more about how to use SSML and events](speech-synthesis-markup-structure.md)
