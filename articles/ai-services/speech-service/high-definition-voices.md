---
title: What are neural text to speech HD voices?
titleSuffix: Foundry Tools
description: Learn about neural text to speech HD voices that you can use with speech synthesis.
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: overview
ms.date: 05/21/2026
ms.custom: references_regions
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech HD voices in Azure Speech in Foundry Tools.
---

# High-definition voices in Azure Speech

Azure Speech in Foundry Tools continues to advance text-to-speech technology with neural high-definition (HD) voices. These HD voices understand content, automatically detect emotions in input text, and adjust speaking tone in real-time to match sentiment. They maintain consistent voice personas while delivering enhanced expressiveness, naturalness, and control.

## HD voice overview

Azure Speech offers two advanced HD voice models, each optimized for different use cases:

| Model | Voice Count | Key Characteristics | Best For |
|-------|-------------|-------------------|----------|
| **DragonHD** | 30+ fine-tuned voices | Professional quality, accurate pronunciation, multi-talker support | Enterprise applications requiring high-quality output |
| **DragonHDOmni** | 700+ voices (all released voices + new AI-generated) | Styles support, multilingual, flexible to add new voices and styles.  | Diverse applications, content creation, broad persona variety |

### Key features of HD voices

The following table describes the key features of Azure Speech HD voices:

| Key features | Description |
|--------------|-------------|
| **Human-like speech generation** | Neural text-to-speech HD voices generate highly natural and human-like speech. The model is trained on millions of hours of multilingual data, enabling it to accurately interpret input text and generate speech with the appropriate emotion, pace, and rhythm without manual adjustments. |
| **Conversational** | Neural text-to-speech HD voices replicate natural speech patterns, including spontaneous pauses and emphasis. When given conversational text, the model can reproduce common phonemes like pauses and filler words. The generated voice sounds as if someone is conversing directly with you. |
| **Prosody variations** | Neural text-to-speech HD voices introduce slight variations in each output to enhance realism. These variations make the speech sound more natural, as human voices naturally exhibit variation. |
| **High fidelity** | The primary objective of neural text-to-speech HD voices is to generate high-fidelity audio. The synthetic speech produced by the system can closely mimic human speech in both quality and naturalness. |

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

The Azure Speech HD voice values use the format `voicename:DragonHD:version`. The name before the colon, such as `en-US-Ava`, is the voice persona name and its original locale.

To make sure you use the latest version of the base model that Microsoft provides, use the `LatestNeural` version.

For example, for the persona `en-US-Ava`, you can specify:
- `en-US-Ava:DragonHDLatestNeural`: Always uses the latest version of the DragonHD base model.

The following table lists the available DragonHD voices:

| Voice Name | Gender | Status | Note |
|-----------|--------|--------|------|
| `de-de-Florian:DragonHDLatestNeural` | Male | GA | |
| `de-de-Seraphina:DragonHDLatestNeural` | Female | GA | |
| `en-us-Adam:DragonHDLatestNeural` | Male | GA | |
| `en-us-Alloy:DragonHDLatestNeural` | Male | GA | |
| `en-us-Andrew:DragonHDLatestNeural` | Male | GA | |
| `en-us-Andrew2:DragonHDLatestNeural` | Male | GA | Optimized for conversational content |
| `en-us-Andrew3:DragonHDLatestNeural` | Male | Preview | Optimized for podcast content |
| `en-us-Aria:DragonHDLatestNeural` | Female | GA | |
| `en-us-Ava:DragonHDLatestNeural` | Female | GA | |
| `en-us-Ava3:DragonHDLatestNeural` | Female | Preview | Optimized for podcast content |
| `en-us-Brian:DragonHDLatestNeural` | Male | GA | |
| `en-us-Davis:DragonHDLatestNeural` | Male | GA | |
| `en-us-Emma:DragonHDLatestNeural` | Female | GA | |
| `en-us-Emma2:DragonHDLatestNeural` | Female | GA | Optimized for conversational content |
| `en-us-Jenny:DragonHDLatestNeural` | Female | GA | |
| `en-us-MultiTalker-Ava-Andrew:DragonHDLatestNeural` | Male | Preview | |
| `en-us-Nova:DragonHDLatestNeural` | Female | GA | |
| `en-us-Phoebe:DragonHDLatestNeural` | Female | GA | |
| `en-us-Serena:DragonHDLatestNeural` | Female | GA | |
| `en-us-Steffan:DragonHDLatestNeural` | Male | GA | |
| `es-es-Tristan:DragonHDLatestNeural` | Male | GA | |
| `es-es-Ximena:DragonHDLatestNeural` | Female | GA | |
| `fr-fr-Remy:DragonHDLatestNeural` | Male | GA | |
| `fr-fr-Vivienne:DragonHDLatestNeural` | Female | GA | |
| `ja-jp-Masaru:DragonHDLatestNeural` | Male | GA | |
| `ja-jp-Nanami:DragonHDLatestNeural` | Female | GA | |
| `zh-cn-Xiaochen:DragonHDLatestNeural` | Female | GA | |
| `zh-cn-Yunfan:DragonHDLatestNeural` | Male | GA | |

The following styles and paralinguistic tags are supported in HD voices:

| Type                                | Tag | 
|-------------------------------------------|--------|
| Styles    | `amazed`, `amused`, `angry`, `annoyed`, `anxious`, `appreciative`, `calm`, `cautious`, `concerned`, `confident`, `confused`, `curious`, `defeated`, `defensive`, `defiant`, `determined`, `disappointed`, `disgusted`, `doubtful`, `ecstatic`, `encouraging`, `excited`, `fast`, `fearful`, `frustrated`, `happy`, `hesitant`, `hurt`, `impatient`, `impressed`, `intrigued`, `joking`, `laughing`, `optimistic`, `painful`, `panicked`, `panting`, `pleading`, `proud`, `quiet`, `reassuring`, `reflective`, `relieved`, `remorseful`, `resigned`, `sad`, `sarcastic`, `secretive`, `serious`, `shocked`, `shouting`, `shy`, `skeptical`, `slow`, `struggling`, `surprised`, `suspicious`, `sympathetic`, `terrified`, `upset`, `urgent`, `whispering`   |
| Paralinguistics    | `laughter`, `coughing`, `throat_clearing`, `breathing`, `sighing`, `yawning`   |

> [!NOTE]
> Styles and paralinguistics are available on all English content for all voices. Style results are strongly relevant to the input content: the model adapts style application based on the semantic meaning of the text. See the styles and paralinguistics [SSML template](speech-synthesis-markup-voice.md#styles-and-paralinguistic-in-hd-voices).

### Dragon HD Omni voices

Dragon HD Omni is Azure Speech's unified next-generation model that combines prebuilt and AI-generated voices into a single, flexible platform. It features more than 700 voices with enhanced expressiveness, multilingual support, advanced style control, and automatic style prediction.

#### Key capabilities of Dragon HD Omni

- **700+ Voices**: Includes most of the previous voices with improved quality and more than 300 AI-generated voices with diverse characteristics.
- **Advanced Style Control**: Automatic style prediction using natural language descriptions (initially available for `en-US-Ava` and `en-US-Andrew`).
- **Multilingual Support**: All Dragon HD Omni voices support multiple languages with automatic language detection and SSML `<lang>` tag support.
- **Enhanced Prosody**: Improved naturalness with automatic contextual adaptation.
- **Word Boundary Event Support**: Enables precise word-level timing for synchronized applications.

#### Supported styles for Dragon HD Omni
The following styles and paralinguistic tags are supported in HDOmni voices:

| Type                                | Tag | 
|-------------------------------------------|--------|
| Styles    | `amazed`, `amused`, `angry`, `annoyed`, `anxious`, `appreciative`, `calm`, `cautious`, `concerned`, `confident`, `confused`, `curious`, `defeated`, `defensive`, `defiant`, `determined`, `disappointed`, `disgusted`, `doubtful`, `ecstatic`, `encouraging`, `excited`, `fast`, `fearful`, `frustrated`, `happy`, `hesitant`, `hurt`, `impatient`, `impressed`, `intrigued`, `joking`, `laughing`, `optimistic`, `painful`, `panicked`, `panting`, `pleading`, `proud`, `quiet`, `reassuring`, `reflective`, `relieved`, `remorseful`, `resigned`, `sad`, `sarcastic`, `secretive`, `serious`, `shocked`, `shouting`, `shy`, `skeptical`, `slow`, `struggling`, `surprised`, `suspicious`, `sympathetic`, `terrified`, `upset`, `urgent`   |
| Paralinguistics    | `laughter`, `coughing`, `throat_clearing`, `breathing`, `sighing`, `yawning`  |

> [!NOTE]
> Styles are available on all English content for all voices. Style results are strongly relevant to the input content: the model adapts style application based on the semantic meaning of the text.
> Paralinguistics are available on all voices with all languages.
> See the styles and paralinguistics [SSML template](speech-synthesis-markup-voice.md#styles-and-paralinguistic-in-hd-voices).

#### Dragon HD Omni voice naming convention

Dragon HD Omni voices follow the naming pattern: `languagelocale-voicename:DragonHDOmniLatestNeural`. To quickly find the Omni version, add the suffix `:DragonHDOmniLatestNeural` to the voice name format:

Example:

| Previous neural voice | Omni version voice name                |
|------------------------|----------------------------------------|
| de-DE-ConradNeural     | de-DE-Conrad:DragonHDOmniLatestNeural  |

### Dragon HD Flash voices

HD Flash voices are optimized variants of selected DragonHD voices, currently supporting Chinese (`zh-CN`) and English (`en-US`) text. These voices deliver enhanced naturalness and are available in standard Azure regions (`eastus`, `westeurope`, `southeastasia`) as well as China regions (`chinaeast2`, `chinanorth2`, `chinanorth3`).

The following table lists all available HD Flash voices and supported styles.

| **Voice name** | **Supported styles** |
|---------------|----------------------|
| `zh-CN-Xiaoxiao:DragonHDFlashLatestNeural` | `angry`, `chat`, `cheerful`, `customer-service`, `excited`, `fearful`, `sad`, `voice-assistant` |
| `zh-CN-Xiaoxiao2:DragonHDFlashLatestNeural` | `affectionate`, `angry`, `anxious`, `cheerful`, `curious`, `disappointed`, `empathetic`, `encouraging`, `excited`, `fearful`, `guilty`, `lonely`, `poetry-reading`, `sad`, `sentimental`, `sorry`, `story`, `surprised`, `tired`, `whispering` |
| `zh-CN-Xiaochen:DragonHDFlashLatestNeural` | `cheerful`, `debating`, `empathetic`, `live-commercial`, `poetry-reading`, `sad`, `sorry` |
| `zh-CN-Xiaoyi:DragonHDFlashLatestNeural` | `angry`, `complaining`, `cute`, `gentle`, `nervous`, `sad`, `shy`, `strict` |
| `zh-CN-Xiaoyu:DragonHDFlashLatestNeural` | `angry`, `debating`, `cheerful`, `comforting`, `sad`, `sorry` |
| `zh-CN-Xiaohan:DragonHDFlashLatestNeural` | `affectionate`, `angry`, `cheerful`, `complaining`, `fearful`, `gentle`, `sad`, `shy`, `strict` |
| `zh-CN-Xiaoshuang:DragonHDFlashLatestNeural` | `chat` |
| `zh-CN-Xiaoyou:DragonHDFlashLatestNeural` | `chat`, `angry`, `cheerful`, `poetry-reading`, `sad`, `story`, `cute` |
| `zh-CN-Yunxi:DragonHDFlashLatestNeural` | `angry`, `chat`, `cheerful`, `complaining`, `depressed`, `fearful`, `news`, `sad`, `shy`, `strict`, `voice-assistant` |
| `zh-CN-Yunyi:DragonHDFlashLatestNeural` | `assassin`, `captain`, `cavalier`, `prince`, `game-narrator`, `geomancer`, `poet` |
| `zh-CN-Yunxiao:DragonHDFlashLatestNeural` | — |
| `zh-CN-Yunhan:DragonHDFlashLatestNeural` | `angry`, `cheerful`, `curious`, `empathetic`, `encouraging`, `excited`, `guilty`, `lonely`, `sad`, `serious`, `sorry`, `whispering`, `surprised`, `tired` |
| `zh-CN-Yunxia:DragonHDFlashLatestNeural` | `affectionate`, `angry`, `cheerful`, `comforting`, `encouraging`, `excited`, `fearful`, `sad`, `surprised` |
| `zh-CN-Yunye:DragonHDFlashLatestNeural` | — |
| `en-US-Tiana:DragonHDFlashLatestNeural` | — |
| `en-US-Tyler:DragonHDFlashLatestNeural` | — |
| `en-US-Jimmie:DragonHDFlashLatestNeural` | — |

> [!NOTE]
> HD Flash only supports text in `zh-CN` and `en-US`.

## How to use Azure Speech HD voices

Use the same Speech SDK and REST APIs for HD voices as you do for non-HD voices. 

Consider these key points when using Azure Speech HD voices:

- **Voice locale**: The locale in the voice name indicates its original language and region.
- **Base models**:
  - HD voices include a base model that understands the input text and predicts the speaking pattern accordingly. You can specify the desired model, such as `DragonHDLatestNeural`, based on the availability of each voice.
- **SSML usage**: To reference a voice in SSML, use the format `voicename:basemodel:version`. The name before the colon, such as `de-DE-Seraphina`, is the voice persona name and its original locale. The base model is tracked by versions in subsequent updates.
- **Temperature parameter**:
  - The temperature value is a float ranging from 0 to 1, influencing the randomness of the output. You can adjust the temperature parameter to control the variation of outputs. Less randomness yields more stable results, while more randomness offers variety but less consistency.
  - Lower temperature results in less randomness, leading to more predictable outputs. Higher temperature increases randomness, allowing for more diverse outputs. The default temperature is set at 1.0.

Here's an example of how to use Azure Speech HD voices in SSML:

```ssml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts' xml:lang='en-US'>
<voice name='en-US-Ava:DragonHDLatestNeural' parameters='temperature=0.8'>Here is a test</voice>
</speak>
```

## Dragon HD Omni advanced features

### Style control with Express-As

Dragon HD Omni supports advanced style control by using the `mstts:express-as` element with natural language descriptions. For more information, see [SSML template](speech-synthesis-markup-voice.md#styles-and-paralinguistic-in-hd-voices).

### Multilingual support

All Dragon HD Omni voices support multiple languages with automatic language detection. You can also use the `<lang xml:lang>` tag to explicitly specify the speaking language and accent. For more information, see [SSML template](speech-synthesis-markup-voice.md#styles-and-paralinguistic-in-hd-voices).

### Word boundary events

Dragon HD Omni supports word boundary events, so you can get precise word-level timing for synchronized applications like karaoke, real-time captioning, and interactive voice experiences.

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
- Higher values for `temperature`, `top_p`, and `top_k` result in more expressive, emotionally varied speech.
- Lower values produce more stable and predictable output.
- Recommendation: Keep `top_p` equal to `temperature` for best results.

**For speed and contextual relevance:**
- `cfg_scale` affects how quickly the voice speaks and how well it aligns with context.
  - Higher values (1.8–2.0): Faster speech with stronger contextual relevance.
  - Lower values (1.0–1.2): Slower speech with less contextual alignment.

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
| `<phoneme>`  |Specifies phonetic pronunciation in SSML documents. | Yes | No |
| `<lexicon>`  | Defines how multiple entities are read in SSML.  | Yes (only supports alias)  | Yes (only supports alias) |
| `<say-as>` | Indicates the content type, such as number or date, of the element's text.  | Yes  | Yes |
| `<sub>`  |  Indicates that the alias attribute's text value should be pronounced instead of the element's enclosed text.  | Yes | Yes |
| `<math>` | Uses the MathML as input text to properly pronounce mathematical notations in the output audio.  | No | No |
| `<bookmark>` | Gets the offset of each marker in the audio stream.  | No | No |
| `<break>`  | Overrides the default behavior of breaks or pauses between words. | Yes | No |
| `<mstts:silence>`  | Inserts pause before or after text, or between two adjacent sentences.  | No | No |
| `<mstts:viseme>` | Defines the position of the face and mouth while a person is speaking.  | No | No |
| `<p>`  | Denotes paragraphs in SSML documents.  | Yes | Yes |
| `<s>`  | Denotes sentences in SSML documents.  | Yes | Yes |

> [!NOTE]
> Although a [previous section in this guide](#comparison-of-azure-speech-hd-voices-to-other-azure-text-to-speech-voices) also compared Azure Speech HD voices to Azure OpenAI HD voices, the SSML elements supported by Azure Speech aren't applicable to Azure OpenAI voices.

## Parameter enhancePronunciation
The `enhancePronunciation` parameter enables enhanced pronunciation handling during speech synthesis. When set to true, the NeuralHD voices apply extra pronunciation optimizations to improve the clarity and correctness of spoken output, particularly for complex, ambiguous, or nonstandard text.

When you enable `enhancePronunciation`, the service prioritizes pronunciation accuracy by applying enhanced linguistic processing during synthesis. This improvement can help how the system reads:
- Proper nouns, names, and uncommon words
- Acronyms, abbreviations, and mixed-case text
- Words with multiple possible pronunciations depending on context
This parameter complements existing pronunciation controls such as SSML-based pronunciation tags and lexicons, and doesn't replace them. The default value is false to preserve predictable, backward-compatible speech output. Enable it when you want the service to apply extra pronunciation optimizations for improved clarity and naturalness.

```SSML
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Ava:DragonHDLatestNeural" parameters="enhancePronunciation=true">
    This is a pronunciation enhanced example for technical terms like
    Kubernetes, Azure OpenAI, and multilingual content such as 今、何か軽く摘めそうなものある？
  </voice>
</speak>
```

### Recommended use cases
Enable `enhancePronunciation` in scenarios with structured or technical domain-specific content.

> [!NOTE]
> The parameter affects pronunciation handling only; it doesn't change voice selection, speaking style, or prosody controls.
> Results might vary depending on language, voice, and input text.
> For deterministic pronunciation control, SSML pronunciation elements remain the recommended approach.

## Choosing between DragonHD and Dragon HD Omni

Both HD voice models deliver high-quality synthesis, but they serve different use cases:

| Consideration | DragonHD | Dragon HD Omni |
|---|---|---|
| **Number of Voices** | More than 30 fine tuned voices | More than 700 voices, including previous voices and new AI-generated voices |
| **Voice Diversity** | Limited to predefined personas | Extensive variety with diverse characteristics from all library voices |
| **Style Control** | Temperature and advanced parameters only | Automatic style prediction and more than 100 styles control on Ava and Andrew |
| **Use Cases** | Customer service, accessibility, consistency-focused applications | Content creation, audiobooks, podcasts, diverse persona requirements |

### When to use each model

**Choose Dragon HD if you:**
- Need a specific voice persona for specific languages to be high quality
- Are building enterprise customer service applications
- Want fine-tuned control through temperature and advanced parameters

**Choose Dragon HD Omni if you:**
- Need flexibility with many voice options
- Are creating diverse content (audiobooks, podcasts, storytelling)
- Want to improve on current neural voices but the locales don't have HD model support yet
- Need broad persona variety for different use cases

## Related content
- [Try the text to speech quickstart in Azure Speech](get-started-text-to-speech.md)
- [Learn more about how to use SSML and events](speech-synthesis-markup-structure.md)
