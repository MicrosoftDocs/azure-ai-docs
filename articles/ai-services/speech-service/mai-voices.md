---
title: What is MAI-Voice?
titleSuffix: Foundry Tools
description: Learn about neural text to speech MAI voices that you can use with speech synthesis.
author: PatrickFarley
ms.author: pafarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 03/27/2026
ms.custom: references_regions, dev-focus
zone_pivot_groups: llm-speech-quickstart
ai-usage: ai-assisted
#customer intent: As a user who implements text to speech, I want to understand the options and differences between available neural text to speech MAI voices in Azure Speech in Foundry Tools.
---

# What is MAI-Voice (preview)?

> [!NOTE]
> 
> This feature is currently in public preview. This preview is provided without a service-level agreement, and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

MAI-Voice is a family of text-to-speech models available through Azure Speech in Foundry Tools in public preview. Built on Microsoft's in-house speech foundation models, MAI-Voice models produce expressive, natural speech output with consistent voice persona quality. 

Speech offers the following MAI-Voice models:

| Model | Voice Count | Key Characteristics | Best For |
|---|---|---|---|
| MAI-Voice-2-Flash | Prebuilt voices across 15+ languages | Ultra-fast low-latency, emotionally rich, highly expressive, multilingual, supports 15 languages and 18 locales, instant voice cloning (gated), fine-grained emotion control via SSML | Real-time voice agents and assistants, low-latency call center/IVR flows, multilingual interactive experiences |
| MAI-Voice-2 | Prebuilt voices across 15+ languages | Emotionally rich, highly expressive, high-fidelity, multilingual, supports 15 languages and 18 locales, instant voice cloning (gated), long-form generation with speaker consistency, fine-grained emotion control via SSML | Expressive long-form content, educational content, Audiobooks/Podcasts, Voice Overs |


## Model details

#### [MAI-Voice-2-Flash](#tab/mai-voice-2-flash)

MAI‑Voice‑2‑Flash is a text‑to‑speech model built for fast, low‑latency generation. It produces high‑fidelity, natural, and expressive speech across 15 languages and supports gated instant voice cloning, all while being optimized for real‑time responsiveness. Its human‑like intonation, rhythm, and emotional nuance make it ideal for voice agents, assistants, and other interactive scenarios where latency and cost are critical.

You can integrate with MAI-Voice-2-Flash using the Azure Speech SDK via SSML, and also via [Voice Live](/azure/ai-services/speech-service/voice-live-how-to#audio-output-through-azure-text-to-speech).

#### [MAI-Voice-2](#tab/mai-voice-2)

MAI‑Voice‑2 is our highest‑fidelity, most expressive text‑to‑speech model, delivering rich, natural speech across more than 15 languages. It extends the MAI‑Voice family with broad multilingual coverage, gated instant voice cloning, and strong long‑form generation capabilities. With its detailed prosody, nuanced expressiveness, and studio‑grade audio quality, MAI‑Voice‑2 is ideal for experiences where maximum voice quality and fidelity are required - long‑form narration, brand‑defining audio etc.

---

## Key features

#### [MAI-Voice-2-Flash](#tab/mai-voice-2-flash)

| Key features | Description |
|---|---|
| Ultra-fast low-latency synthesis | Built for real-time text-to-speech with very low latency, suitable for interactive voice scenarios. |
| High-fidelity natural synthesis | Produces natural, expressive, emotionally rich, and high-clarity voice output with human-like rhythm and intonation. |
| Multilingual support | Supports synthesis across 15 languages and 18 locales. |
| Emotion and style control | Developers can influence speaking style by using SSML with `mstts:express-as` and `style`, enabling control over emotions such as `joy`, `excitement`, `empathy`, and more. |
| Voice prompting with instant cloning (gated) | Matches a consented reference voice from a short audio clip (5-60 seconds) without additional training. |
| Voice library | Includes licensed curated voices for 15+ languages that work out of the box for rapid deployment. |
| Real-time agent optimization | Optimized for voice agents, assistants, IVR, and call-center interactions where responsiveness is critical. |

#### [MAI-Voice-2](#tab/mai-voice-2)

| Key features | Description |
|---|---|
| High-fidelity natural synthesis | Produces natural, expressive, emotionally rich, and high-clarity voice output with human-like rhythm and intonation. |
| Multilingual support | Supports synthesis across 15 languages and 18 locales. |
| Emotion and style control | Developers can influence speaking style by using SSML with `mstts:express-as` and `style`, enabling control over emotions such as `joy`, `excitement`, `empathy`, and more. |
| Voice prompting with instant cloning (gated) | Matches a consented reference voice from a short audio clip (5-60 seconds) without additional training. |
| Voice library | Includes licensed curated voices for 15+ languages that work out of the box for rapid deployment. |
| High fidelity audio | The model produces high-quality speech with natural prosody and clarity suitable for production-grade applications. |
| Long-form generation | Optimized for long-form narration with stable persona quality and speaker consistency across extended content. |
| Out-of-scope note | The model prioritizes naturalness and expressivity over latency-critical scenarios. |


---

## Prerequisites

To use MAI related models, complete the following steps:

- An Azure account. [Create one for free](https://azure.microsoft.com/free/).
- A Speech resource in a region that supports MAI models ([region support](/azure/cognitive-services/speech-service/regions)).
- For voice prompting, apply for [limited access](https://aka.ms/customneural) approval and complete consent safeguards.

---

## SSML examples

#### [MAI-Voice-2-Flash](#tab/mai-voice-2-flash)

The examples use the following voices.

| **Voice ID** | **Gender** |
|---|---|
| **en-us-Harper:MAI-Voice-2-Flash** | Female |
| **en-us-Ethan:MAI-Voice-2-Flash** | Male |

**Basic SSML Example (Harper):**

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice xml:lang='en-US' name='en-US-Harper:MAI-Voice-2-Flash'>
    hello world, it's very great
  </voice>
</speak>
```


**Basic SSML Example (Ethan):**

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice xml:lang='en-US' name='en-US-Ethan:MAI-Voice-2-Flash'>
    hello world, it's very great, hello world, it's very great?
  </voice>
</speak>
```

**Expressive Control with SSML `mstts:express-as`**

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice xml:lang='en-US' name='en-US-Ethan:MAI-Voice-2-Flash'>
    <mstts:express-as style="excited">
       hello world, it's very great, hello world, it's very great?
    </mstts:express-as>
  </voice>
</speak>
```

#### [MAI-Voice-2](#tab/mai-voice-2)

**Basic multilingual SSML**

The following SSML synthesizes a greeting in Spanish (Mexico) by using `es-MX-Valeria:MAI-Voice-2`.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="es-MX">
  <voice name="es-MX-Valeria:MAI-Voice-2">
    Hola, esta es una muestra de MAI Voice 2.
  </voice>
</speak>
```

**Expressive Control with SSML `mstts:express-as`**

MAI-Voice-2 supports expressive styles by using `style` and `styledegree` attributes for fine-grained control:

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2">
    <mstts:express-as style="happiness" styledegree="1.2">
      Welcome to Microsoft Build. MAI Voice 2 supports multilingual expressive synthesis.
    </mstts:express-as>
  </voice>
</speak>
```


## **Sample code**

The following Python example demonstrates how to synthesize SSML to an MP3 audio file by using the Azure Speech SDK:

```python
# call Azure speech SDK to synthesize a SSML into mp3 audio file

import os
import time
import azure.cognitiveservices.speech as speechsdk

speech_key = os.environ.get('SUBSCRIPTION_SPEECH_KEY')
service_region = os.environ.get('SUBSCRIPTION_SPEECH_REGION')

# [generate]() audio with Azure TTS HD voices
def GenerateAudio(ssml, outaudio, development=False):
    # start time
    st = time.time()

    if development:
        print("Using development subscription key and endpoint.")
        # use development subscription key and endpoint
        # speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SUBSCRIPTION_KEY_DEV"), region=os.getenv("SERVICE_REGION_DEV"))
        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv("SUBSCRIPTION_KEY_DEV"),
            endpoint="https://dev.tts-frontend.speech-test.microsoft.com/cognitiveservices/v1"
        )
    else:
        print("Using production subscription key and region.")
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # speech_config = speechsdk.SpeechConfig(subscription=os.getenv("SUBSCRIPTION_KEY_DEV"), endpoint="https://dev.tts-frontend.speech-test.microsoft.com/cognitiveservices/v1")

    # Creates an audio configuration that points to an audio file.
    audio_output = speechsdk.audio.AudioOutputConfig(filename=outaudio)

    # set output format
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
    )

    # Creates a speech synthesizer using the Azure Speech Service.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_output
    )

    # Synthesizes the received text to speech.
    result = speech_synthesizer.speak_ssml_async(ssml).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis was successful. Audio was written to '{}'".format(outaudio))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")

    et = time.time()
    print("Time taken for synthesis: {:.2f} seconds".format(et - st))


if __name__ == "__main__":
    ssml = """
<speak
version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'><voice
xml:lang='en-US' name='en-US-Ethan:MAI-Voice-2-Flash'>hello world, it's very
great, hello world, it's very great?</voice></speak>
    """

    outaudio = "Ethan-mai.mp3"
    GenerateAudio(ssml, outaudio, development=False)

    ssml = """
<speak
version='1.0' xmlns='http://www.w3.org/2001/10/synthesis'
xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'><voice
xml:lang='en-US' name='en-US-Harper:MAI-Voice-2-Flash'>hello world, it's
very great, hello world, it's very great?</voice></speak>
"""

    outaudio = "Harper-mai.mp3"
    GenerateAudio(ssml, outaudio, development=False)
```

## Custom voice - Personal Voice/Instant Voice Cloning (gated access)

Developers can create a custom voice in Microsoft Foundry across all supported languages by using just a short reference clip - no retraining or fine-tuning required. With only a few seconds of audio (recommended: 5-60 seconds), MAI-Voice-2 generates high-quality speech that matches the speaker's identity, making it easy for companies to bring their own brand voice into products without maintaining a separate voice model.

All MAI-Voice models support Instant Voice Cloning. Only authorized, licensed voices can be synthesized in production. No unlicensed voice cloning is possible. To gain access to this feature

1. Apply for gated access through Azure AI Custom Neural Voice and Custom Avatar [Limited Access Review](https://aka.ms/customneural).
1. Once approved, access personal voice APIs at cognitive-services-speech-sdk/samples/custom-voice.
1. Upload audio consent and prompt to create a personal voice.
1. Synthesize given text by using the created voice and MAI related models with the following SSML (example below with 'MAI-voice-2') :

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='MAI-voice-2'>
    <mstts:ttsembedding speakerProfileId='your speaker profile ID here'>
      I'm happy to hear that you find me amazing and that I have made your trip planning easier and more fun.
    </mstts:ttsembedding>
  </voice>
</speak>
```

---

## Prebuilt voices

#### [MAI-Voice-2](#tab/mai-voice-2)

MAI-Voice-2 provides locale-specific prebuilt voices across multiple languages.

| Voice Name (ShortName) | Locale | Language | Gender | Supported Styles |
|---|---|---|---|---|
| de-DE-Klaus:MAI-Voice-2 | de-DE | German (Germany) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| de-DE-Mia:MAI-Voice-2 | de-DE | German (Germany) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-AU-Lisa:MAI-Voice-2 | en-AU | English (Australia) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-US-Ethan:MAI-Voice-2 | en-US | English (United States) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-US-Grant:MAI-Voice-2 | en-US | English (United States) | Male | — |
| en-US-Harper:MAI-Voice-2 | en-US | English (United States) | Female | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, shouting, softvoice, whispering |
| en-US-Iris:MAI-Voice-2 | en-US | English (United States) | Female | — |
| en-US-Jasper:MAI-Voice-2 | en-US | English (United States) | Male | — |
| en-US-Olivia:MAI-Voice-2 | en-US | English (United States) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| es-ES-Marta:MAI-Voice-2 | es-ES | Spanish (Spain) | Female | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| es-MX-Alejo:MAI-Voice-2 | es-MX | Spanish (Mexico) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| es-MX-Valeria:MAI-Voice-2 | es-MX | Spanish (Mexico) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| fr-FR-Marc:MAI-Voice-2 | fr-FR | French (France) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| fr-FR-Soleil:MAI-Voice-2 | fr-FR | French (France) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Arjun:MAI-Voice-2 | hi-IN | Hindi (India) | Male | angry, confused, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, sad, surprised |
| hi-IN-Dhruv:MAI-Voice-2 | hi-IN | Hindi (India) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Kavya:MAI-Voice-2 | hi-IN | Hindi (India) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Priya:MAI-Voice-2 | hi-IN | Hindi (India) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hu-HU-Bence:MAI-Voice-2 | hu-HU | Hungarian (Hungary) | Male | — |
| hu-HU-Levente:MAI-Voice-2 | hu-HU | Hungarian (Hungary) | Male | — |
| hu-HU-Lilla:MAI-Voice-2 | hu-HU | Hungarian (Hungary) | Female | — |
| hu-HU-Réka:MAI-Voice-2 | hu-HU | Hungarian (Hungary) | Female | — |
| it-IT-Luca:MAI-Voice-2 | it-IT | Italian (Italy) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| it-IT-Rosa:MAI-Voice-2 | it-IT | Italian (Italy) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| ko-KR-Hana:MAI-Voice-2 | ko-KR | Korean (Korea) | Female | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| ko-KR-Junho:MAI-Voice-2 | ko-KR | Korean (Korea) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, relieved, sad, softvoice |
| nl-NL-Fleur:MAI-Voice-2 | nl-NL | Dutch (Netherlands) | Female | — |
| nl-NL-Sander:MAI-Voice-2 | nl-NL | Dutch (Netherlands) | Male | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| pt-BR-Caio:MAI-Voice-2 | pt-BR | Portuguese (Brazil) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| pt-BR-Luana:MAI-Voice-2 | pt-BR | Portuguese (Brazil) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| pt-BR-Pedro:MAI-Voice-2 | pt-BR | Portuguese (Brazil) | Male | confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| pt-BR-Rafael:MAI-Voice-2 | pt-BR | Portuguese (Brazil) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| pt-PT-Rui:MAI-Voice-2 | pt-PT | Portuguese (Portugal) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| ro-RO-Andrei:MAI-Voice-2 | ro-RO | Romanian (Romania) | Male | — |
| ro-RO-Elena:MAI-Voice-2 | ro-RO | Romanian (Romania) | Female | — |
| ro-RO-Ioana:MAI-Voice-2 | ro-RO | Romanian (Romania) | Female | — |
| ro-RO-Radu:MAI-Voice-2 | ro-RO | Romanian (Romania) | Male | — |
| ru-RU-Lev:MAI-Voice-2 | ru-RU | Russian (Russia) | Male | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| ru-RU-Masha:MAI-Voice-2 | ru-RU | Russian (Russia) | Female | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| th-TH-Krit:MAI-Voice-2 | th-TH | Thai (Thailand) | Male | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| th-TH-Nattapong:MAI-Voice-2 | th-TH | Thai (Thailand) | Male | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| tr-TR-Aydin:MAI-Voice-2 | tr-TR | Turkish (Turkey) | Male | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| tr-TR-Elif:MAI-Voice-2 | tr-TR | Turkish (Turkey) | Female | adventurous, caring, empathy, curious, encouraging, excited, friendly, cheerful, nostalgic, reflective, sad, disappointed, serious |
| zh-CN-Bo:MAI-Voice-2 | zh-CN | Chinese (Mandarin, Simplified) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| zh-CN-Lan:MAI-Voice-2 | zh-CN | Chinese (Mandarin, Simplified) | Female | angry, confused, disgusted, embarrassed, excited, fearful, happy, joyful, sad, surprised |
| zh-CN-Mei:MAI-Voice-2 | zh-CN | Chinese (Mandarin, Simplified) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |

> [!NOTE]
> The voices listed in the preceding table are the currently published MAI-Voice-2 prebuilt voices. The model card indicates support across 10+ languages. Microsoft adds more locales and voices as they become generally available.

#### [MAI-Voice-2-Flash](#tab/mai-voice-2-flash)

| Voice Name (ShortName) | Locale | Language | Gender | Supported Styles |
|---|---|---|---|---|
| de-DE-Klaus:MAI-Voice-2-Flash | de-DE | German (Germany) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| de-DE-Mia:MAI-Voice-2-Flash | de-DE | German (Germany) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-AU-Isla:MAI-Voice-2-Flash | en-AU | English (Australia) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-US-Ethan:MAI-Voice-2-Flash | en-US | English (United States) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| en-US-Harper:MAI-Voice-2-Flash | en-US | English (United States) | Female | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, shouting, softvoice, whispering |
| en-US-Olivia:MAI-Voice-2-Flash | en-US | English (United States) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| es-ES-Marta:MAI-Voice-2-Flash | es-ES | Spanish (Spain) | Female | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| es-MX-Alejo:MAI-Voice-2-Flash | es-MX | Spanish (Mexico) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| es-MX-Valeria:MAI-Voice-2-Flash | es-MX | Spanish (Mexico) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| fr-FR-Marc:MAI-Voice-2-Flash | fr-FR | French (France) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| fr-FR-Soleil:MAI-Voice-2-Flash | fr-FR | French (France) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Arjun:MAI-Voice-2-Flash | hi-IN | Hindi (India) | Male | angry, confused, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, sad, surprised |
| hi-IN-Dhruv:MAI-Voice-2-Flash | hi-IN | Hindi (India) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Kavya:MAI-Voice-2-Flash | hi-IN | Hindi (India) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hi-IN-Priya:MAI-Voice-2-Flash | hi-IN | Hindi (India) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| hu-HU-Bence:MAI-Voice-2-Flash | hu-HU | Hungarian (Hungary) | Male | — |
| hu-HU-Levente:MAI-Voice-2-Flash | hu-HU | Hungarian (Hungary) | Male | — |
| hu-HU-Lilla:MAI-Voice-2-Flash | hu-HU | Hungarian (Hungary) | Female | — |
| hu-HU-Réka:MAI-Voice-2-Flash | hu-HU | Hungarian (Hungary) | Female | — |
| it-IT-Luca:MAI-Voice-2-Flash | it-IT | Italian (Italy) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| it-IT-Rosa:MAI-Voice-2-Flash | it-IT | Italian (Italy) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| ko-KR-Haena:MAI-Voice-2-Flash | ko-KR | Korean (Korea) | Female | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| ko-KR-Junho:MAI-Voice-2-Flash | ko-KR | Korean (Korea) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, relieved, sad, softvoice |
| nl-NL-Sander:MAI-Voice-2-Flash | nl-NL | Dutch (Netherlands) | Male | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| pt-BR-Caio:MAI-Voice-2-Flash | pt-BR | Portuguese (Brazil) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| pt-BR-Luana:MAI-Voice-2-Flash | pt-BR | Portuguese (Brazil) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| pt-BR-Pedro:MAI-Voice-2-Flash | pt-BR | Portuguese (Brazil) | Male | confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| pt-BR-Rafael:MAI-Voice-2-Flash | pt-BR | Portuguese (Brazil) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| pt-PT-Rui:MAI-Voice-2-Flash | pt-PT | Portuguese (Portugal) | Male | angry, confused, determined, embarrassed, excited, happy, hopeful, joyful, regretful, relieved, sad, softvoice, surprised |
| ro-RO-Andrei:MAI-Voice-2-Flash | ro-RO | Romanian (Romania) | Male | — |
| ro-RO-Elena:MAI-Voice-2-Flash | ro-RO | Romanian (Romania) | Female | — |
| ro-RO-Ioana:MAI-Voice-2-Flash | ro-RO | Romanian (Romania) | Female | — |
| ro-RO-Radu:MAI-Voice-2-Flash | ro-RO | Romanian (Romania) | Male | — |
| ru-RU-Lev:MAI-Voice-2-Flash | ru-RU | Russian (Russia) | Male | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| ru-RU-Masha:MAI-Voice-2-Flash | ru-RU | Russian (Russia) | Female | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| th-TH-Krit:MAI-Voice-2-Flash | th-TH | Thai (Thailand) | Male | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| th-TH-Nattapong:MAI-Voice-2-Flash | th-TH | Thai (Thailand) | Male | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| tr-TR-Aydın:MAI-Voice-2-Flash | tr-TR | Turkish (Türkiye) | Male | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| tr-TR-Elif:MAI-Voice-2-Flash | tr-TR | Turkish (Türkiye) | Female | adventurous, caringempathy, curious, encouraging, excited, friendlycheerful, nostalgic, reflective, saddisappointed, serious |
| zh-CN-Bo:MAI-Voice-2-Flash | zh-CN | Chinese (Mandarin, Simplified) | Male | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| zh-CN-Lan:MAI-Voice-2-Flash | zh-CN | Chinese (Mandarin, Simplified) | Female | angry, confused, disgusted, embarrassed, excited, fearful, happy, joyful, sad, surprised |
| zh-CN-Mei:MAI-Voice-2-Flash | zh-CN | Chinese (Mandarin, Simplified) | Female | angry, confused, determined, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, relieved, sad, shouting, softvoice, surprised, whispering |
| zh-CN-Wei:MAI-Voice-2-Flash | zh-CN | Chinese (Mandarin, Simplified) | Male | angry, confused, disgusted, embarrassed, excited, fearful, happy, hopeful, jealous, joyful, regretful, sad, surprised |

---

Usage: Available for third-party developers. Microsoft holds full licensing rights for commercial use.

## Use MAI-Voice models

MAI-Voice models use the same Azure Speech APIs and SDKs as other Azure neural and HD voices. Use the voice name in the `name` attribute of the SSML `<voice>` element. See the prebuilt voice tables in the preceding sections for available names.

::: zone pivot="ai-foundry"

Try a MAI-Voice voice in the Foundry portal:

1. Go to the [Text to speech feature page](https://aka.ms/foundry-text-to-speech) and select **Open in playground**.
1. Select a MAI-Voice voice from the voice dropdown.
1. Enter sample text in the text box.
1. Select **Play** to hear the synthesized speech.

::: zone-end

::: zone pivot="programming-language-rest"

Send an SSML POST request to the `cognitiveservices/v1` endpoint of your Speech resource. Replace `YourRegion` with your Speech resource region and `<YourSpeechResourceKey>` with your resource key.

```azurecli-interactive
curl -X POST \
  "https://YourRegion.tts.speech.microsoft.com/cognitiveservices/v1" \
  --header "Content-Type: application/ssml+xml" \
  --header "X-Microsoft-OutputFormat: audio-24khz-160kbitrate-mono-mp3" \
  --header "Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>" \
  --data '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
  <voice name="en-US-Harper:MAI-Voice-2">
    Hello, this is a sample from MAI Voice.
  </voice>
</speak>' \
  --output output.mp3
```

Replace the voice name with any MAI-Voice voice from the prebuilt voice tables above.

::: zone-end

::: zone pivot="programming-language-python"

The following code synthesizes speech by using the Azure Speech SDK and saves the audio to `output.mp3`. Replace `<key>` with your Speech resource key.

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
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='en-US-Harper:MAI-Voice-2-Flash'>
    <mstts:express-as style="excitement">Hello world.</mstts:express-as>
  </voice>
</speak>
"""

synthesizer.speak_ssml_async(ssml).get()
```

On success, an `output.mp3` file is saved to the current directory. Replace the voice name with any MAI-Voice voice from the prebuilt voice tables above.

::: zone-end

::: zone pivot="programming-language-csharp"

Follow the [text to speech quickstart](get-started-text-to-speech.md?pivots=programming-language-csharp). In the SSML, use a MAI-Voice voice name in the `name` attribute of the `<voice>` element. See the prebuilt voice tables above for available names.

::: zone-end

::: zone pivot="programming-language-javascript"

Follow the [text to speech quickstart](get-started-text-to-speech.md?pivots=programming-language-javascript). In the SSML, use a MAI-Voice voice name in the `name` attribute of the `<voice>` element. See the prebuilt voice tables above for available names.

::: zone-end

::: zone pivot="programming-language-java"

Follow the [text to speech quickstart](get-started-text-to-speech.md?pivots=programming-language-java). In the SSML, use a MAI-Voice voice name in the `name` attribute of the `<voice>` element. See the prebuilt voice tables above for available names.

::: zone-end


## Next steps
- [Speech Synthesis Markup Language (SSML) overview](speech-synthesis-markup.md)
- [Get started with text to speech](get-started-text-to-speech.md)
- [High definition (HD) voices](high-definition-voices.md)
