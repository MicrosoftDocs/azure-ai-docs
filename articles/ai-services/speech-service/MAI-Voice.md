---
title: What are MAI-Voice?
titleSuffix: Foundry Tools
description: Learn about neural text to speech MAI voices that you can use with speech synthesis.
author: PatrickFarley
reviewer: patrickfarley
ms.author: pafarley
ms.reviewer: pafarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 03/20/2026
ms.custom: references_regions
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech MAI voices in Azure Speech in Foundry Tools.
---


# MAI-Voice-1 in Azure Speech

Azure Speech continues to advance text to speech technology with **MAI-Voice-1**, a next-generation neural text to speech (TTS) model available through Azure AI Speech in **public preview**. Built on Microsoft’s latest in-house speech foundation models, MAI-Voice-1 delivers highly expressive, natural, and emotionally rich speech output while maintaining consistent voice persona quality.

Similar to Azure Neural HD voices, MAI-Voice-1 understands input text holistically and automatically adapts tone, emotion, and speaking style. This enables more human-like and conversational speech without requiring extensive manual tuning.

## MAI-Voice-1 overview

Azure Speech offers MAI-Voice-1 as an advanced neural voice model optimized for expressive, conversational, and long-form scenarios.

| Model | Voice Count | Key Characteristics | Best For |
|------|-------------|---------------------|----------|
| **MAI-Voice-1** | 2 prebuilt English (US) voices | Emotionally rich, highly expressive, consistent persona quality, SSML style control | Conversational AI, creative applications, long-form narration |

### Prebuilt voices

| Voice ID | Gender |
|--------|--------|
| `en-us-Noa:MAI-Voice-1` | Female |
| `en-us-Teo:MAI-Voice-1` | Male |

**Usage**: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

### Key features of MAI-Voice-1

| Key features | Description |
|-------------|-------------|
| **Human-like speech generation** | MAI-Voice-1 generates highly natural and emotionally rich speech. The model interprets input text holistically and automatically adjusts emotion, pace, and rhythm without manual configuration. |
| **Conversational expressiveness** | MAI-Voice-1 is optimized for conversational scenarios, producing engaging and context-aware speech suitable for assistants and interactive experiences. |
| **Emotion and style control** | Developers can influence speaking style using SSML with `mstts:express-as`, enabling control over emotions such as joy, excitement, empathy, and more. |
| **Consistent voice persona** | MAI-Voice-1 maintains a stable and consistent voice persona across long-form content while still allowing expressive variation. |
| **High fidelity audio** | The model produces high-quality neural speech with natural prosody and clarity suitable for production-grade applications. |
| **Real-time synthesis** | MAI-Voice-1 supports real-time speech synthesis using the Azure Speech SDK and APIs. |

## Supported speaking styles

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

### Prerequisites

1. Create an Azure account
2. Create an Azure Speech resource in **East US**
3. Retrieve the subscription key and region from the Azure portal
4. Install the Azure Speech SDK

## SSML examples

### Basic SSML

```
xml
<speak version="1.0"
       xmlns="http://www.w3.org/2001/10/synthesis"
       xml:lang="en-US">
  <voice name="en-us-Noa:MAI-Voice-1">
    Hello world, it’s great to meet you.
  </voice>
</speak>
```

### Styled SSML (Excitement)
```
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

### Sample code (Python)
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

## Summary
MAI-Voice-1 extends the Azure Speech HD voice portfolio by introducing higher emotional expressiveness and stronger persona consistency. It complements existing HD voice models by targeting next-generation conversational and creative use cases while leveraging the same SDKs and SSML patterns used across Azure Neural and HD voices.
