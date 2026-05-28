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

# What is MAI-Voice (preview)?

> **Note**
> 
> This feature is currently in public preview. This preview is provided without a service-level agreement, and is not recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

MAI-Voice is a family of neural text-to-speech models available through Azure Speech in Foundry Tools in public preview. Built on Microsoft's in-house speech foundation models, MAI-Voice models produce expressive, natural speech output with consistent voice persona quality. Similar to Azure Neural HD voices, MAI-Voice models understand input text holistically and automatically adapt tone, emotion, and speaking style. This enables more human-like and conversational speech without requiring extensive manual tuning.

Speech offers the following MAI-Voice models:

| Model | Voice Count | Key Characteristics | Best For |
|---|---|---|---|
| MAI-Voice-1 | Six prebuilt English (US) voices | Emotionally rich, highly expressive, consistent persona quality, SSML style control | Conversational AI, creative applications, long-form narration |
| MAI-Voice-2 | Multilingual prebuilt voices across 10+ languages | High-fidelity expressive synthesis, multilingual, voice prompting (gated), long-form and multi-speaker generation | Multilingual conversational AI, expressive long-form content, multi-speaker scenarios |

---

## MAI-Voice-1

MAI-Voice-1 is optimized for expressive, conversational, and long-form scenarios in English (US).

### Key features

| Key features | Description |
|---|---|
| Human-like speech generation | MAI-Voice-1 generates highly natural and emotionally rich speech. The model interprets input text holistically and automatically adjusts emotion, pace, and rhythm without manual configuration. |
| Conversational expressiveness | MAI-Voice-1 is optimized for conversational scenarios, producing engaging and context-aware speech suitable for assistants and interactive experiences. |
| Emotion and style control | Developers can influence speaking style using SSML with `mstts:express-as`, enabling control over emotions such as joy, excitement, empathy, and more. |
| Consistent voice persona | MAI-Voice-1 maintains a stable and consistent voice persona across long-form content while still allowing expressive variation. |
| High fidelity audio | The model produces high-quality neural speech with natural prosody and clarity suitable for production-grade applications. |
| Real-time synthesis | MAI-Voice-1 supports real-time speech synthesis using the Speech SDK and APIs. |

### Prerequisites

- An Azure account. Create one for free.
- Create a Speech resource in a region that supports MAI-Voice-1 (region support).

### Use MAI-Voice-1

MAI-Voice-1 uses the same Azure Speech SDKs and APIs as other Azure Neural and HD voices. Follow the Text to speech quickstart in the platform of your choice. Use the speech synthesis method that incorporates SSML specification, and enter one of the available MAI-Voice-1 prebuilt voices in the `name` attribute of the `<voice>` element.

For example, the following Python code synthesizes speech using `en-us-Teo:MAI-Voice-1` and saves it to `output.mp3`. Replace `<key>` with your Speech resource key.

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="<key>", region="eastus"
)
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.mp3")
speech_config.set_speech_synthesis_output_format(
    speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
)
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

ssml = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
  <voice name='en-us-Jasper:MAI-Voice-1'>
    <mstts:express-as style="excitement">hello world.</mstts:express-as>
  </voice>
</speak>
"""

synthesizer.speak_ssml_async(ssml).get()
```

On success, an `output.mp3` file containing the synthesized speech is saved to the current directory.

Reference: SpeechConfig | AudioOutputConfig | SpeechSynthesizer | speak_ssml_async

### SSML examples

**Basic SSML**

The following SSML synthesizes a greeting using the `en-us-Noa:MAI-Voice-1` voice.

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='en-US-Jasper:MAI-Voice-1'>
    <mstts:express-as style="excitement">hello world.</mstts:express-as>
  </voice>
</speak>
```

Submit this SSML to the Speech REST API or SDK to receive synthesized audio.

Reference: Speech Synthesis Markup Language (SSML) | `<voice>` element

### Personal Voice (MAI-voice-1 prompt mode)

Steps to Access:

To access personal voice (voice cloning) using MAI-Voice-1:

1. Apply for gated access via Azure AI Custom Neural Voice and Custom Avatar Limited Access Review.
2. Once approved, access personal voice APIs at cognitive-services-speech-sdk/samples/custom-voice.
3. Upload audio consent and prompt to create a personal voice.
4. Synthesize text using the created voice and MAI-Voice-1 model using the following SSML:

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='MAI-voice-1'>
    <mstts:ttsembedding speakerProfileId='your speaker profile ID here'>
      I'm happy to hear that you find me amazing and that I have made your trip planning easier and more fun.
    </mstts:ttsembedding>
  </voice>
</speak>
```

### Prebuilt voices

| Voice ID | Gender | Recommended use case |
|---|---|---|
| en-us-Jasper:MAI-Voice-1 | Male | General Conversation, Sales, Emotional styles |
| en-us-June:MAI-Voice-1 | Female | General Conversation, Customer Service, Professional, Emotional styles |
| en-us-Grant:MAI-Voice-1 | Male | General Conversation, Professional, Emotional styles |
| en-us-Iris:MAI-Voice-1 | Female | General Conversation, Narration, Emotional styles |
| en-us-Reed:MAI-Voice-1 | Male | General Conversation |
| en-us-Joy:MAI-Voice-1 | Female | General Conversation |

Usage: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

---

## MAI-Voice-2

MAI-Voice-2 is a high-fidelity, expressive, prompted text-to-speech model that supports multilingual synthesis across 10+ languages. It extends the MAI-Voice family with multilingual coverage, voice prompting (gated), long-form generation, and multi-speaker generation.

### Key features

| Key features | Description |
|---|---|
| High-fidelity natural synthesis | Produces highly natural voice output with expressive control. |
| Multilingual support | Supports synthesis across 10+ languages with locale-specific prebuilt voices. |
| Expressive SSML control | Supports `mstts:express-as` with `style` and `styledegree` for fine-grained expressive control (for example, `happiness`). |
| Voice prompting (gated) | Voice prompting is supported with short reference clips (10–120 seconds), subject to gated access approval and consent safeguards. |
| Long-form generation | Optimized for long-form narration with stable persona quality across extended content. |
| Multi-speaker generation | Supports multi-speaker scenarios within a single synthesis flow. |
| Out-of-scope note | The model prioritizes naturalness and expressivity over latency-critical scenarios. |

### Prerequisites

- An Azure account. Create one for free.
- Create a Speech resource in a region that supports MAI-Voice-2.
- For voice prompting, apply for limited access approval and complete consent safeguards.

### Use MAI-Voice-2

MAI-Voice-2 is available through the Azure Speech REST API. Send an SSML POST request to the `cognitiveservices/v1` endpoint of your Speech resource, and place the desired MAI-Voice-2 voice in the `name` attribute of the `<voice>` element.

The following Python example sends an SSML request to the REST endpoint and writes the resulting 24kHz MP3 to disk. Authentication can be done with an API key (`Ocp-Apim-Subscription-Key`) or Entra ID (`Authorization: Bearer ...`).

```python
import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

load_dotenv('deployment.env', override=True)

VOICE2_ENDPOINT = os.getenv('MAI_VOICE_2_ENDPOINT', 'https://eastus.tts.speech.microsoft.com/')
VOICE2_KEY = os.getenv('MAI_VOICE_2_KEY')
USE_ENTRA_AUTH = os.getenv('USE_ENTRA_AUTH', 'true').lower() == 'true' or not VOICE2_KEY

OUT_DIR = Path('./audio')
OUT_DIR.mkdir(parents=True, exist_ok=True)

token_provider = None
if USE_ENTRA_AUTH:
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        'https://cognitiveservices.azure.com/.default',
    )

def headers() -> dict:
    h = {
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3',
        'User-Agent': 'mai-voice-2-sample',
    }
    if USE_ENTRA_AUTH:
        h['Authorization'] = f"Bearer {token_provider()}"
    else:
        h['Ocp-Apim-Subscription-Key'] = VOICE2_KEY
    return h

def synthesize_to_file(ssml: str, out_file: str) -> Path:
    url = f"{VOICE2_ENDPOINT.rstrip('/')}/cognitiveservices/v1"
    resp = requests.post(url, headers=headers(), data=ssml.encode('utf-8'), timeout=180)
    resp.raise_for_status()
    p = OUT_DIR / out_file
    p.write_bytes(resp.content)
    return p

ssml = """<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2">
    Hello, this is a sample from MAI Voice 2.
  </voice>
</speak>"""

synthesize_to_file(ssml, 'mai_voice2_en.mp3')
```

On success, an `mai_voice2_en.mp3` file containing the synthesized speech is saved to the output directory.

### SSML examples

**Basic multilingual SSML**

The following SSML synthesizes a greeting in Spanish (Mexico) using `es-MX-Valeria:MAI-Voice-2`.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="es-MX">
  <voice name="es-MX-Valeria:MAI-Voice-2">
    Hola, esta es una muestra de MAI Voice 2.
  </voice>
</speak>
```

**Expressive control with `mstts:express-as`**

MAI-Voice-2 supports expressive styles with `style` and `styledegree` attributes for fine-grained control:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2">
    <mstts:express-as style="happiness" styledegree="1.2">
      Welcome to Microsoft Build. MAI Voice 2 supports multilingual expressive synthesis.
    </mstts:express-as>
  </voice>
</speak>
```

### Voice prompting (gated access)

Voice prompting (personal voice cloning) with MAI-Voice-2 is gated and requires Microsoft approval plus consent safeguards.

Steps to access:

1. Apply for limited access approval via Azure AI Custom Neural Voice and Custom Avatar Limited Access Review.
2. Upload consent audio and reference prompt (10–120 seconds).
3. Use the Personal Voice APIs to create the voice profile.
4. Synthesize with the approved voice profile and MAI-Voice-2 model.

### Prebuilt voices

MAI-Voice-2 provides locale-specific prebuilt voices across multiple languages.

| Voice ID | Locale | Language | Gender | Recommended use case |
|---|---|---|---|---|
| en-US-Harper:MAI-Voice-2 | en-US | English (United States) | Female | General Conversation, Expressive Long-form |
| es-MX-Valeria:MAI-Voice-2 | es-MX | Spanish (Mexico) | Female | General Conversation, Multilingual Narration |
| fr-FR-Soleil:MAI-Voice-2 | fr-FR | French (France) | Female | General Conversation, Multilingual Narration |
| de-DE-Klaus:MAI-Voice-2 | de-DE | German (Germany) | Male | General Conversation, Multilingual Narration |

> **Note**
> The voices listed above are the currently published MAI-Voice-2 prebuilt voices. The model card indicates support across 10+ languages, and additional locales and voices will be added as they become generally available.

Usage: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

## Next steps

- [Speech Synthesis Markup Language (SSML) overview](speech-synthesis-markup.md)
- [Get started with text to speech](get-started-text-to-speech.md)
- [High definition (HD) voices](high-definition-voices.md)
