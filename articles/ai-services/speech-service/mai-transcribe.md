---
title: MAI-Transcribe in LLM Speech API - Speech Service
titleSuffix: Foundry Tools
description: Learn how to use the MAI-Transcribe model in Azure Speech LLM Speech API.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 05/28/2026
zone_pivot_groups: llm-speech-quickstart

# Customer intent: As a user who implements audio transcription, I want to create transcriptions with MAI's latest MAI-Transcribe-1 model.
ai-usage: ai-assisted
---

# MAI-Transcribe in Azure Speech (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI‑Transcribe models are speech recognition models developed by the Microsoft AI (MAI) Superintelligence team. These models are optimized for both high accuracy and high efficiency, and are available through the LLM Speech API.

The following models are supported:
- `mai-transcribe-1.5`
- `mai-transcribe-1`

## Prerequisites

> [!div class="checklist"]
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - [A Microsoft Foundry resource for Speech](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.
> - The Speech resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).
> - An audio file (less than 300 MB in size) in one of these formats: WAV, MP3, or FLAC.

## Language support

By default, the model operates in multi-lingual mode. The following languages are currently supported:

| Language code | Language |
| ----- | ----- |
| `ar` | Arabic |
| `zh` | Chinese |
| `cs` | Czech |
| `da` | Danish |
| `nl` | Dutch |
| `en` | English |
| `fi` | Finnish |
| `fr` | French |
| `de` | German |
| `hi` | Hindi |
| `hu` | Hungarian |
| `id` | Indonesian |
| `it` | Italian |
| `ja` | Japanese |
| `ko` | Korean |
| `nb` | Norwegian Bokmål |
| `pl` | Polish |
| `pt` | Portuguese |
| `ro` | Romanian |
| `ru` | Russian |
| `es` | Spanish |
| `sv` | Swedish |
| `th` | Thai |
| `tr` | Turkish |
| `vi` | Vietnamese |

## Use a MAI-Transcribe model

You can use MAI‑Transcribe models with the LLM Speech API to generate transcriptions from audio input.

Note the following limitations when you use a MAI-Transcribe model:
- Diarization isn't supported.
- Prompt-tuning isn't supported.
- Phrase list and transcribe style are supported only in `mai-transcribe-1.5`.


::: zone pivot="ai-foundry"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=ai-foundry). Then, specify the `Model`.

::: zone-end

::: zone pivot="programming-language-rest"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-rest).

To use the MAI-Transcribe model, set the `model` property accordingly in the request.

```azurecli-interactive
curl --location 'https://YourResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "enhancedMode": {
    "enabled": true,
    "model":"mai-transcribe-1.5"
  }
}'
```

Optionally, specify a language code in `locales` to force recognition in a single language. For example:

```
--form 'definition={
  "locales": ["en"],
  "enhancedMode": {
    "enabled": true,
    "model":"mai-transcribe-1.5"
  }
}'
```

Optionally, for `mai-transcribe-1.5`, you can specify the style of the transcript output by using `transcribeStyle`. By default, the model returns a readability‑optimized transcript. You can set the value to `verbatim` to preserve the original spoken content, including filler words and disfluencies.

```
  "enhancedMode": {
    "enabled": true,
    "model":"mai-transcribe-1.5",
    "transcribeStyle":"verbatim"
  }
```

Optionally, for `mai-transcribe-1.5`, you can add a list of phrases to increase accuracy in specialized domains by using `phraseList`. This implements entity biasing.

```
 --form 'definition={
   "phraseList": {
     "phrases": ["Contoso", "Jessie", "Rehaan"]
   },
   "enhancedMode": {
     "enabled": true,
     "model": "mai-transcribe-1.5"
   }
 }'
```

::: zone-end

::: zone pivot="programming-language-python"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python). Then, specify the model in the `enhancedMode` property.

::: zone-end

::: zone pivot="programming-language-csharp"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-csharp). Then, specify the model in the `EnhancedMode` property.


::: zone-end

::: zone pivot="programming-language-javascript"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-javascript). Then, specify the model in the `enhancedMode` property.

::: zone-end

::: zone pivot="programming-language-java"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-java). Then, specify the model in the `EnhancedModeOptions` object.

::: zone-end




### Use MAI-Transcribe with Voice Live

You can also use the MAI-Transcribe model for input audio transcription in the [Voice Live API](./voice-live.md). Set the `model` field in the `input_audio_transcription` session configuration. For details, see [How to customize Voice Live input and output](./voice-live-how-to-customize.md#mai-transcribe-1-model-preview).


## Related content

- For more information about using LLM Speech API, see [LLM Speech API](llm-speech.md)
- [MAI-Voice in Azure Speech](mai-voices.md)
- [How to customize Voice Live input and output](./voice-live-how-to-customize.md)
