---
title: What is MAI-Voice?
titleSuffix: Foundry Tools
description: Learn about neural text to speech MAI voices that you can use with speech synthesis.
author: PatrickFarley
ms.author: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 03/27/2026
ms.custom: references_regions, dev-focus
ai-usage: ai-assisted
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech MAI voices in Azure Speech in Foundry Tools.
---


# MAI-Voice-1 in Azure Speech

MAI-Voice-1 is a neural text-to-speech model available through Azure Speech in Foundry Tools in **public preview**. It's built on Microsoft's in-house speech foundation models and produces expressive, natural speech output with consistent voice persona quality.

Similar to Azure Neural HD voices, MAI-Voice-1 understands input text holistically and automatically adapts tone, emotion, and speaking style. This enables more human-like and conversational speech without requiring extensive manual tuning.

Speech offers MAI-Voice-1 as an advanced neural voice model optimized for expressive, conversational, and long-form scenarios.

| Model | Voice Count | Key Characteristics | Best For |
|------|-------------|---------------------|----------|
| **MAI-Voice-1** | two prebuilt English (US) voices | Emotionally rich, highly expressive, consistent persona quality, SSML style control | Conversational AI, creative applications, long-form narration |


## Key features

| Key features | Description |
|-------------|-------------|
| **Human-like speech generation** | MAI-Voice-1 generates highly natural and emotionally rich speech. The model interprets input text holistically and automatically adjusts emotion, pace, and rhythm without manual configuration. |
| **Conversational expressiveness** | MAI-Voice-1 is optimized for conversational scenarios, producing engaging and context-aware speech suitable for assistants and interactive experiences. |
| **Emotion and style control** | Developers can influence speaking style using SSML with `mstts:express-as`, enabling control over emotions such as joy, excitement, empathy, and more. |
| **Consistent voice persona** | MAI-Voice-1 maintains a stable and consistent voice persona across long-form content while still allowing expressive variation. |
| **High fidelity audio** | The model produces high-quality neural speech with natural prosody and clarity suitable for production-grade applications. |
| **Real-time synthesis** | MAI-Voice-1 supports real-time speech synthesis using the Speech SDK and APIs. |

### Supported speaking styles

- Empathetic
- Excitement
- Joy
- Friendly
- Neutral
- Encouragement
- Confusion
- Sadness
- Surprise
- Curiosity


## Use MAI-Voice-1

MAI-Voice-1 uses the same Azure Speech SDKs and APIs as other Azure Neural and HD voices.

## Prerequisites

- An Azure account. [Create one for free](https://azure.microsoft.com/free/cognitive-services/).
- A Speech resource in the **East US** region. See [Get started with text to speech](get-started-text-to-speech.md) to create one.
- Your Speech resource key and region from the **Keys and Endpoint** page in the Azure portal.
- The Azure Speech SDK installed: `pip install azure-cognitiveservices-speech`

## SSML examples

### Basic SSML

The following SSML synthesizes a greeting using the `en-us-Noa:MAI-Voice-1` voice.

```xml
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xml:lang="en-US">
  <voice name="en-us-Noa:MAI-Voice-1">
    Hello world, it's great to meet you.
  </voice>
</speak>
```

Submit this SSML to the Speech REST API or SDK to receive synthesized audio.

**Reference**: [Speech Synthesis Markup Language (SSML)](speech-synthesis-markup.md) | [`<voice>` element](speech-synthesis-markup-voice.md)

### Styled SSML (excitement)

The following SSML applies an `excitement` speaking style using the `mstts:express-as` element.

```xml
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="http://www.w3.org/2001/mstts"
       xml:lang="en-US">
  <voice name="en-us-Noa:MAI-Voice-1">
    <mstts:express-as style="excitement">
      Hello world, this is MAI-Voice-1!
    </mstts:express-as>
  </voice>
</speak>
```

Submit this SSML to receive audio with an excited speaking style applied.

**Reference**: [`mstts:express-as`](speech-synthesis-markup-voice.md#use-speaking-styles-and-roles) | [Supported styles](speech-synthesis-markup-voice.md)

### Python example

The following Python code synthesizes speech using `en-us-Teo:MAI-Voice-1` and saves it to `output.mp3`. Replace `<key>` with your Speech resource key.

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="<key>",
    region="eastus"
)

audio_config = speechsdk.audio.AudioOutputConfig(
    filename="output.mp3"
)

speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
)

synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)

ssml = """
<speak version='1.0'
       xmlns='http://www.w3.org/2001/10/synthesis'
       xml:lang='en-US'>
  <voice name='en-us-Teo:MAI-Voice-1'>
    Hello from MAI Voice.
  </voice>
</speak>
"""

synthesizer.speak_ssml_async(ssml).get()
```

On success, an `output.mp3` file containing the synthesized speech is saved to the current directory.

**Reference**: [`SpeechConfig`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig) | [`AudioOutputConfig`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.audio.audiooutputconfig) | [`SpeechSynthesizer`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesizer) | [`speak_ssml_async`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesizer#azure-cognitiveservices-speech-speechsynthesizer-speak-ssml-async)

## Prebuilt voices

| Voice ID | Gender |
|--------|--------|
| `en-us-Noa:MAI-Voice-1` | Female |
| `en-us-Teo:MAI-Voice-1` | Male |

**Usage**: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

## Next steps

- [Speech Synthesis Markup Language (SSML) overview](speech-synthesis-markup.md)
- [Get started with text to speech](get-started-text-to-speech.md)
- [High definition (HD) voices](high-definition-voices.md)
