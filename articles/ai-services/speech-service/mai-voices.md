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

MAI-Voice is a family of neural text-to-speech models available through Azure Speech in Foundry Tools in public preview. Built on Microsoft's in-house speech foundation models, MAI-Voice models produce expressive, natural speech output with consistent voice persona quality. Similar to Azure Neural HD voices, MAI-Voice models understand input text holistically and automatically adapt tone, emotion, and speaking style. This adaptation enables more human-like and conversational speech without requiring extensive manual tuning.

Speech offers the following MAI-Voice models:

| Model | Voice Count | Key Characteristics | Best For |
|---|---|---|---|
| MAI-Voice-1 | Six prebuilt English (US) voices | Emotionally rich, highly expressive, consistent persona quality, SSML style control | Conversational AI, creative applications, long-form narration |
| MAI-Voice-2 | Multilingual prebuilt voices across 10+ languages | High-fidelity expressive synthesis, multilingual, voice prompting (gated), long-form and multi-speaker generation | Multilingual conversational AI, expressive long-form content, multi-speaker scenarios |

## Model details

#### [MAI-Voice-1](#tab/mai-voice-1)

MAI-Voice-1 is optimized for expressive, conversational, and long-form scenarios in English (US).

#### [MAI-Voice-2](#tab/mai-voice-2)

MAI-Voice-2 is a high-fidelity, expressive, prompted text-to-speech model that supports multilingual synthesis across more than 10 languages. It extends the MAI-Voice family with multilingual coverage, voice prompting (gated), long-form generation, and multi-speaker generation.

---

## Key features

#### [MAI-Voice-1](#tab/mai-voice-1)

| Key features | Description |
|---|---|
| Human-like speech generation | MAI-Voice-1 generates highly natural and emotionally rich speech. The model interprets input text holistically and automatically adjusts emotion, pace, and rhythm without manual configuration. |
| Conversational expressiveness | MAI-Voice-1 is optimized for conversational scenarios, producing engaging and context-aware speech suitable for assistants and interactive experiences. |
| Emotion and style control | Developers can influence speaking style by using SSML with `mstts:express-as`, enabling control over emotions such as joy, excitement, empathy, and more. |
| Consistent voice persona | MAI-Voice-1 maintains a stable and consistent voice persona across long-form content while still allowing expressive variation. |
| High fidelity audio | The model produces high-quality neural speech with natural prosody and clarity suitable for production-grade applications. |
| Real-time synthesis | MAI-Voice-1 supports real-time speech synthesis by using the Speech SDK and APIs. |

#### [MAI-Voice-2](#tab/mai-voice-2)

| Key features | Description |
|---|---|
| High-fidelity natural synthesis | Produces highly natural voice output with expressive control. |
| Multilingual support | Supports synthesis across more than 10 languages with locale-specific prebuilt voices. |
| Expressive SSML control | Supports `mstts:express-as` with `style` and `styledegree` for fine-grained expressive control (for example, `happiness`). |
| Voice prompting (gated) | Supports voice prompting with short reference clips (10–120 seconds), subject to gated access approval and consent safeguards. |
| Long-form generation | Optimized for long-form narration with stable persona quality across extended content. |
| Multi-speaker generation | Supports multi-speaker scenarios within a single synthesis flow. |
| Out-of-scope note | The model prioritizes naturalness and expressivity over latency-critical scenarios. |

---

## Prerequisites

#### [MAI-Voice-1](#tab/mai-voice-1)

- An Azure account. [Create one for free](https://azure.microsoft.com/free/).
- A Speech resource in a region that supports MAI-Voice-1 ([region support](https://learn.microsoft.com/azure/cognitive-services/speech-service/regions)).
- For voice prompting, apply for [limited access](https://aka.ms/customneural) approval and complete consent safeguards.

#### [MAI-Voice-2](#tab/mai-voice-2)

- An Azure account. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account).
- A Speech resource in a [region](regions.md#regions) that supports MAI-Voice-2.
- For voice prompting, apply for [limited access](https://aka.ms/customneural) approval and complete consent safeguards.

---

## SSML examples

#### [MAI-Voice-1](#tab/mai-voice-1)

**Basic SSML**

The following SSML synthesizes a greeting by using the `en-US-Jasper:MAI-Voice-1` voice.

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='en-US-Jasper:MAI-Voice-1'>
    <mstts:express-as style="excitement">hello world.</mstts:express-as>
  </voice>
</speak>
```

Submit this SSML to the Speech REST API or SDK to receive synthesized audio.

Reference: Speech Synthesis Markup Language (SSML) | `<voice>` element

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

**Expressive control with `mstts:express-as`**

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

---

## Voice prompting (gated access)

#### [MAI-Voice-1](#tab/mai-voice-1)

To access personal voice (voice cloning) by using MAI-Voice-1:

1. Apply for gated access through Azure AI Custom Neural Voice and Custom Avatar [Limited Access Review](https://aka.ms/customneural).
1. Once approved, access personal voice APIs at cognitive-services-speech-sdk/samples/custom-voice.
1. Upload audio consent and prompt to create a personal voice.
1. Synthesize given text by using the created voice and MAI-Voice-1 model with the following SSML:

```xml
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
  <voice name='MAI-voice-1'>
    <mstts:ttsembedding speakerProfileId='your speaker profile ID here'>
      I'm happy to hear that you find me amazing and that I have made your trip planning easier and more fun.
    </mstts:ttsembedding>
  </voice>
</speak>
```

#### [MAI-Voice-2](#tab/mai-voice-2)

To access personal voice (voice cloning) by using MAI-Voice-2:

1. Apply for limited access approval through Azure AI Custom Neural Voice and Custom Avatar [Limited Access Review](https://aka.ms/customneural).
1. Upload consent audio and reference prompt (10–120 seconds).
1. Use the Personal Voice APIs to create the voice profile.
1. Synthesize by using the approved voice profile and MAI-Voice-2 model.

---

## Prebuilt voices

#### [MAI-Voice-1](#tab/mai-voice-1)

| Voice ID | Gender | Recommended use case |
|---|---|---|
| en-us-Jasper:MAI-Voice-1 | Male | General Conversation, Sales, Emotional styles |
| en-us-June:MAI-Voice-1 | Female | General Conversation, Customer Service, Professional, Emotional styles |
| en-us-Grant:MAI-Voice-1 | Male | General Conversation, Professional, Emotional styles |
| en-us-Iris:MAI-Voice-1 | Female | General Conversation, Narration, Emotional styles |
| en-us-Reed:MAI-Voice-1 | Male | General Conversation |
| en-us-Joy:MAI-Voice-1 | Female | General Conversation |

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
  <voice name='en-US-Jasper:MAI-Voice-1'>
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
