---
title: What are neural text to speech HD voices?
titleSuffix: Foundry Tools
description: Learn about neural text to speech HD voices that you can use with speech synthesis.
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 10/21/2025
ms.custom: references_regions
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech HD voices in Azure Speech in Foundry Tools.
---

# High-Definition voices in Azure Speech

Azure Speech in Foundry Tools continues to advance text to speech technology with neural high-definition (HD) voices. Our HD voices understand content, automatically detect emotions in input text, and adjust speaking tone in real-time to match sentiment. They maintain consistent voice personas while delivering enhanced expressiveness, naturalness, and control.

## HD voice overview

Azure Speech offers two advanced HD voice models, each optimized for different use cases:

| Model | Voice Count | Key Characteristics | Best For |
|-------|-------------|-------------------|----------|
| **DragonHD** | 30+ fine-tuned voices | Professional quality, accurate pronunciation, multi talker support | Enterprise applications requiring high quality output |
| **DragonHDOmni** | 700+ voices (all released voices + new AI-generated) | Styles support, multilingual, flexible to add new voices and styles.  | Diverse applications, content creation, broad persona variety |

### Key features of HD voices

The following are the key features of Azure Speech HD voices:

| Key features | Description |
|--------------|-------------|
| **Human-like speech generation** | Neural text to speech HD voices can generate highly natural and human-like speech. The model is trained on millions of hours of multilingual data, enabling it to accurately interpret input text and generate speech with the appropriate emotion, pace, and rhythm without manual adjustments. |
| **Conversational** | Neural text to speech HD voices can replicate natural speech patterns, including spontaneous pauses and emphasis. When given conversational text, the model can reproduce common phonemes like pauses and filler words. The generated voice sounds as if someone is conversing directly with you. |
| **Prosody variations** | Neural text to speech HD voices introduce slight variations in each output to enhance realism. These variations make the speech sound more natural, as human voices naturally exhibit variation. |
| **High fidelity** | The primary objective of neural text to speech HD voices is to generate high-fidelity audio. The synthetic speech produced by our system can closely mimic human speech in both quality and naturalness. |

## Comparison of Azure Speech HD voices to other Azure text to speech voices

How do Azure Speech HD voices compare to other Azure text to speech voices? Here's a detailed comparison:

| Feature | Azure Speech HD voices  | Azure OpenAI HD voices | Azure Speech voices (not HD) |
|---------|---------------|------------------------|------------------------|
| **Region** | See [Speech service regions](regions.md?tabs=tts) | See [Speech service regions](regions.md?tabs=tts) | Available in dozens of regions. See the [Speech service regions](regions.md?tabs=tts).|
| **Number of voices** | 30 | 6 | More than 500 |
| **Multilingual**  | Yes | Yes  | Yes (applicable only to multilingual voices)  |
| **SSML support** | Support for [a subset of SSML elements](#supported-and-unsupported-ssml-elements-for-azure-speech-hd-voices).|  Support for [a subset of SSML elements](openai-voices.md#ssml-elements-supported-by-openai-text-to-speech-voices-in-azure-speech).  | Support for the [full set of SSML](speech-synthesis-markup-structure.md) in Azure Speech.  |
| **Development options** | Speech SDK, Speech CLI, REST API  | Speech SDK, Speech CLI, REST API  | Speech SDK, Speech CLI, REST API  |
| **Deployment options**  | Cloud only | Cloud only | Cloud, embedded, hybrid, and containers. |
| **Real-time or batch synthesis**  | Real-time only  | Real-time and batch synthesis  | Real-time and batch synthesis |
| **Latency**  | Less than 300 ms | Greater than 500 ms | Less than 300 ms  |
| **Sample rate of synthesized audio** | 8, 16, 24, and 48 kHz  | 8, 16, 24, and 48 kHz | 8, 16, 24, and 48 kHz |
| **Speech output audio format** | opus, mp3, pcm, truesilk |  opus, mp3, pcm, truesilk  |  opus, mp3, pcm, truesilk  |

## Supported Azure Speech HD voices

Azure Speech provides two sets of HD voices with different model architectures:

### Dragon HD voices

The Azure Speech HD voice values are in the format `voicename:DragonHD:version`. The name before the colon, such as `en-US-Ava`, is the voice persona name and its original locale.

To ensure that you're using the latest version of the base model that we provide, use the `LatestNeural` version.

For example, for the persona `en-US-Ava` you can specify:
- `en-US-Ava:DragonHDLatestNeural`: Always uses the latest version of the DragonHD base model.

The following table lists the available DragonHD voices:

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

### Dragon HD Omni voices

Dragon HD Omni is Azure Speech's unified next-generation model that combines prebuilt and AI-generated voices into a single, flexible platform. It features over 700 voices with enhanced expressiveness, multilingual support, advanced style control, and automatic style prediction.

#### Key capabilities of Dragon HD Omni

- **700+ Voices**: Includes most of the previous voices with improved quality and 300+ AI-generated voices with diverse characteristics
- **Advanced Style Control**: Automatic style prediction using natural language descriptions (initially available for `en-US-Ava` and `en-US-Andrew`)
- **Multilingual Support**: All Dragon HD Omni voices support multiple languages with automatic language detection and SSML `<lang>` tag support
- **Enhanced Prosody**: Improved naturalness with automatic contextual adaptation
- **Word Boundary Event Support**: Enables precise word-level timing for synchronized applications

#### Supported styles for Dragon HD Omni

Dragon HD Omni supports a comprehensive set of 100+ speaking styles. Use the `style` attribute within `<mstts:express-as>` to apply any of these styles:

`angry`, `chill surfer`, `confused`, `curious`, `determined`, `disgusted`, `embarrassed`, `emo teenager`, `empathetic`, `encouraging`, `excited`, `fearful`, `friendly`, `grateful`, `joyful`, `mad scientist`, `meditative`, `narration`, `neutral`, `new yorker`, `news`, `reflective`, `regretful`, `relieved`, `sad`, `santa`, `shy`, `soft voice`, `surprised`

> [!NOTE]
> Styles are available on `en-US-Ava` and `en-US-Andrew` for this version. Style results are strongly relevant to the input content: the model adapts style application based on the semantic meaning of the text.

#### Dragon HD Omni voice naming convention

Dragon HD Omni voices follow the naming pattern: `languagelocale-voicename:DragonHDOmniLatestNeural`. You can use this voice name format by adding the suffix `:DragonHDOmniLatestNeural` to find the Omni version quickly:

Example:

| Previous neural voice | Omni version voice name                |
|------------------------|----------------------------------------|
| de-DE-ConradNeural     | de-DE-Conrad:DragonHDOmniLatestNeural  |

Check out the full [Dragon HD Omni voice list](https://github.com/Azure-Samples/Cognitive-Speech-TTS/blob/master/Blog-Samples/Introducing-Dragon-HD-Omni/dragonhdomni_voice_list.json).


### Dragon HD Flash voices

HD Flash voices are optimized variants of selected DragonHD voices, currently supporting Chinese (`zh-CN`) and English (`en-US`) text. These voices deliver enhanced naturalness and are available in standard Azure regions (`eastus`, `westeurope`, `southeastasia`) as well as China regions (`chinaeast2`, `chinanorth2`, `chinanorth3`).

Below is the complete list of available HD Flash voices:

| Voice Name                                 | Gender |
|-------------------------------------------|--------|
| zh-CN-Xiaochen:DragonHDFlashLatestNeural  | Female |
| zh-CN-Xiaoxiao:DragonHDFlashLatestNeural  | Female |
| zh-CN-Xiaoxiao2:DragonHDFlashLatestNeural | Female |
| zh-CN-Yunxia:DragonHDFlashLatestNeural    | Male   |
| zh-CN-Yunxiao:DragonHDFlashLatestNeural   | Male   |
| zh-CN-Yunye:DragonHDFlashLatestNeural     | Male   |
| zh-CN-Yunyi:DragonHDFlashLatestNeural     | Male   |

> [!NOTE]
> HD Flash only supports text in `zh-CN` and `en-US`.

## How to use Azure Speech HD voices

You can use HD voices with the same Speech SDK and REST APIs as the non HD voices. 

Here are some key points to consider when using Azure Speech HD voices:

- **Voice locale**: The locale in the voice name indicates its original language and region.
- **Base models**:
  - HD voices come with a base model that understands the input text and predicts the speaking pattern accordingly. You can specify the desired model (such as DragonHDLatestNeural) according to the availability of each voice.
- **SSML usage**: To reference a voice in SSML, use the format `voicename:basemodel:version`. The name before the colon, such as `de-DE-Seraphina`, is the voice persona name and its original locale. The base model is tracked by versions in subsequent updates.
- **Temperature parameter**:
  - The temperature value is a float ranging from 0 to 1, influencing the randomness of the output. You can also adjust the temperature parameter to control the variation of outputs. Less randomness yields more stable results, while more randomness offers variety but less consistency.
  - Lower temperature results in less randomness, leading to more predictable outputs. Higher temperature increases randomness, allowing for more diverse outputs. The default temperature is set at 1.0.

Here's an example of how to use Azure Speech HD voices in SSML:

```ssml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
<voice name='en-US-Ava:DragonHDLatestNeural' parameters='temperature=0.8'>Here is a test</voice>
</speak>
```

## Dragon HD Omni advanced features

### Style control with Express-As

Dragon HD Omni supports advanced style control using the `mstts:express-as` element with natural language descriptions. Here's an example:

```ssml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-us-ava:DragonHDOmniLatestNeural">
    <mstts:express-as style="sick">
      Ugh… I'm not feeling so great today. My head's pounding, and even my voice sounds like it's been through a blender. I think I need to lie down for a bit… maybe some soup would help.
    </mstts:express-as>
  </voice>
</speak>
```

### Multilingual support

All Dragon HD Omni voices support multiple languages with automatic language detection. You can also use the `<lang xml:lang>` tag to explicitly specify the speaking language and accent:

```ssml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
        xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-us-ava:DragonHDOmniLatestNeural">
    <lang xml:lang="fr-FR">
      Bonjour ! Ce matin, j'ai pris un café au jardin du Luxembourg. Il faisait frais, mais très agréable. Ensuite, j'ai acheté une baguette et quelques macarons. Paris est vraiment charmant.
    </lang>
  </voice>
</speak>
```

### Word boundary events

Dragon HD Omni supports word boundary events, allowing precise word-level timing for synchronized applications like karaoke, real-time captioning, and interactive voice experiences.

When a word boundary event fires, it provides:
- **Text**: The word spoken
- **AudioOffset**: Time offset in the audio stream (milliseconds)
- **TextOffset**: Position of the word in the input text

#### Python example with word boundary events

```python
import azure.cognitiveservices.speech as speechsdk

def word_boundary_cb(evt):
    print(f"Word: '{evt.text}', AudioOffset: {evt.audio_offset / 10000}ms, TextOffset: {evt.text_offset}")

speech_config = speechsdk.SpeechConfig(subscription="YourSubscriptionKey", region="YourServiceRegion")
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

synthesizer.synthesis_word_boundary.connect(word_boundary_cb)

ssml = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
       xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='en-us-ava:DragonHDOmniLatestNeural'>
    Hello Azure, welcome to Dragon HD Omni!
  </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml).get()
```

Sample output:
```
Word: 'Hello', AudioOffset: 110.0ms, TextOffset: 182
Word: 'Azure', AudioOffset: 590.0ms, TextOffset: 188
Word: ',', AudioOffset: 1110.0ms, TextOffset: 193
Word: 'welcome', AudioOffset: 1270.0ms, TextOffset: 195
Word: 'to', AudioOffset: 1750.0ms, TextOffset: 203
Word: 'Dragon HD Omni', AudioOffset: 1910.0ms, TextOffset: 206
Word: '!', AudioOffset: 2750.0ms, TextOffset: 216
```

### Advanced parameter tuning for Dragon HD Omni

Dragon HD Omni supports advanced parameter tuning to customize voice output for different scenarios.

#### Parameter reference

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `temperature` | 0.7 | 0.3–1.0 | Controls creativity vs. stability |
| `top_p` | 0.7 | 0.3–1.0 | Filters output for diversity |
| `top_k` | 22 | 1–50 | Limits number of options considered |
| `cfg_scale` | 1.4 | 1.0–2.0 | Adjusts relevance and speech speed |

#### Tuning strategies

**For expressiveness vs. stability:**
- Higher values for `temperature`, `top_p`, and `top_k` result in more expressive, emotionally varied speech
- Lower values produce more stable and predictable output
- Recommendation: Keep `top_p` equal to `temperature` for best results

**For speed and contextual relevance:**
- `cfg_scale` affects how quickly the voice speaks and how well it aligns with context
  - Higher values (1.8–2.0): Faster speech with stronger contextual relevance
  - Lower values (1.0–1.2): Slower speech with less contextual alignment

#### Suggested tuning table

| Goal | Suggested adjustment |
|------|----------------------|
| More expressive | Increase `temperature`, `top_p`, and `top_k` together |
| More stable | Lower `temperature` first, then adjust `top_p` if needed |
| Faster & relevant | Increase `cfg_scale` |
| Slower & neutral | Decrease `cfg_scale` |

#### Parameter usage examples

Single parameter adjustment:
```ssml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
        xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-us-ava:DragonHDOmniLatestNeural" parameters="top_p=0.8">
    Hello Azure!
  </voice>
</speak>
```

Multiple parameters adjustment:
```ssml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
        xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-us-ava:DragonHDOmniLatestNeural" parameters="top_p=0.8;top_k=22;temperature=0.7;cfg_scale=1.2">
    Hello Azure! Welcome to Dragon HD Omni!
  </voice>
</speak>
```

## Supported and unsupported SSML elements for Azure Speech HD voices

The Speech Synthesis Markup Language (SSML) with input text determines the structure, content, and other characteristics of the text to speech output. For example, you can use SSML to define a paragraph, a sentence, a break or a pause, or silence. You can wrap text with event tags such as bookmark or viseme that your application processes later.

The Azure Speech HD voices support different SSML elements depending on the model:
- **DragonHD voices**: Support a subset of SSML elements (see table below)
- **Dragon HD Omni voices**: Support additional elements including `mstts:express-as` for style control and word boundary events

For detailed information on the supported and unsupported SSML elements for Azure Speech HD voices, refer to the following table. For instructions on how to use SSML elements, refer to the [Speech Synthesis Markup Language (SSML) documentation](speech-synthesis-markup-structure.md). 

| SSML element | Description  | DragonHD | Dragon HD Omni |
|------------------------------|--------------------------------|----------|---------|
| `<voice>`  | Specifies the voice and optional effects (`eq_car` and `eq_telecomhp8k`). | Yes | Yes |
| `<mstts:express-as>`  | Specifies speaking styles and roles. | No  | Yes  |
| `<mstts:ttsembedding>` |  Specifies the `speakerProfileId` property for a personal voice. | No | No |
| `<lang xml:lang>` | Specifies the speaking language.  | Yes | Yes |
| `<prosody>`  |  Adjusts pitch, contour, range, rate, and volume. | No | No |
| `<emphasis>`| Adds or removes word-level stress for the text. | No| No |
| `<audio>`| Embeds prerecorded audio into an SSML document. | No| No |
| `<mstts:audioduration>` | Specifies the duration of the output audio. | No  | No |
| `<mstts:backgroundaudio>`  | Adds background audio to your SSML documents or mixes an audio file with text to speech.  | No  | No |
| `<phoneme>`  |Specifies phonetic pronunciation in SSML documents. | No | No |
| `<lexicon>`  | Defines how multiple entities are read in SSML.  | Yes (only supports alias)  | Yes (only supports alias) |
| `<say-as>` | Indicates the content type, such as number or date, of the element's text.  | Yes  | Yes |
| `<sub>`  |  Indicates that the alias attribute's text value should be pronounced instead of the element's enclosed text.  | Yes | Yes |
| `<math>` | Uses the MathML as input text to properly pronounce mathematical notations in the output audio.  | No | No |
| `<bookmark>` | Gets the offset of each marker in the audio stream.  | No | No |
| `<break>`  | Overrides the default behavior of breaks or pauses between words. | No | No |
| `<mstts:silence>`  | Inserts pause before or after text, or between two adjacent sentences.  | No | No |
| `<mstts:viseme>` | Defines the position of the face and mouth while a person is speaking.  | No | No |
| `<p>`  | Denotes paragraphs in SSML documents.  | Yes | Yes |
| `<s>`  | Denotes sentences in SSML documents.  | Yes | Yes |

> [!NOTE]
> Although a [previous section in this guide](#comparison-of-azure-speech-hd-voices-to-other-azure-text-to-speech-voices) also compared Azure Speech HD voices to Azure OpenAI HD voices, the SSML elements supported by Azure Speech aren't applicable to Azure OpenAI voices.

## Choosing between DragonHD and Dragon HD Omni

Both HD voice models deliver high-quality synthesis, but they serve different use cases:

| Consideration | DragonHD | Dragon HD Omni |
|---|---|---|
| **Number of Voices** | 30+ fine tuned voices | 700+ voices (including previous voices & new AI-generated voices) |
| **Voice Diversity** | Limited to predefined personas | Extensive variety with diverse characteristics from all library voices |
| **Style Control** | Temperature and advanced parameters only | Automatic style prediction and 100+ styles control on Ava and Andrew |
| **Use Cases** | Customer service, accessibility, consistency-focused applications | Content creation, audiobooks, podcasts, diverse persona requirements |

### When to use each model

**Choose Dragon HD if you:**
- Need a specific voice persona for specific languages to be high quality
- Building enterprise customer service applications
- Want fine-tuned control via temperature and advanced parameters

**Choose Dragon HD Omni if you:**
- Need flexibility with many voice options
- Are creating diverse content (audiobooks, podcasts, storytelling)
- Want to improve from current neural voices but the locales have no HD model supported yet
- Need broad persona variety for different use cases

## Related content
- [Try the text to speech quickstart in Azure Speech](get-started-text-to-speech.md)
- [Learn more about how to use SSML and events](speech-synthesis-markup-structure.md)
