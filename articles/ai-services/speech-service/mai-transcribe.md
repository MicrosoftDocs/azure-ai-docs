---
title: MAI-Transcribe-1 in LLM Speech API - Speech Service
titleSuffix: Foundry Tools
description: Learn how to use the MAI-Transcribe-1 model in Azure Speech LLM Speech API.
manager: nitinme
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 04/01/2026
zone_pivot_groups: llm-speech-quickstart

# Customer intent: As a user who implements audio transcription, I want to create transcriptions with MAI's latest MAI-Transcribe-1 model.
---

# MAI-Transcribe-1 in Azure Speech (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI‑Transcribe‑1 is a speech recognition model developed by the Microsoft AI (MAI) Superintelligence team. The model has a dual focus: high accuracy and high efficiency. You can use the MAI‑Transcribe‑1 model with the LLM Speech API.

## Prerequisites

> [!div class="checklist"]
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - [A Microsoft Foundry resource for Speech](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.
> - The Speech resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).
> - An audio file (less than 300 MB in size) in one of these formats: WAV, MP3, or FLAC.

## Use the MAI-Transcribe-1 model

Note the following limitations when you use the MAI-Transcribe-1 model:

- Diarization isn't supported.

- Prompt-tuning isn't supported.

::: zone pivot="ai-foundry"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=ai-foundry). Then, specify `mai-transcribe-1` as the **Model**.

::: zone-end

::: zone pivot="programming-language-rest"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-rest).

To use the MAI-Transcribe-1 model, set the `model` property accordingly in the request.

```azurecli-interactive
curl --location 'https://<YourServiceRegion>.api.cognitive.microsoft.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={
  "locales": ["en"],
  "enhancedMode": {
    "enabled": true,
    "model":"mai-transcribe-1"
  }
}'
```

::: zone-end

::: zone pivot="programming-language-python"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python). Then, specify `mai-transcribe-1` as the `model` in the `enhancedMode` property.

::: zone-end

::: zone pivot="programming-language-csharp"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-csharp). Then, specify `mai-transcribe-1` as the `Model` in the `EnhancedMode` property.

::: zone-end

::: zone pivot="programming-language-javascript"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-javascript). Then, specify `mai-transcribe-1` as the model in the `enhancedMode` property.

::: zone-end

::: zone pivot="programming-language-java"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-java). Then, specify `mai-transcribe-1` as the model in the `EnhancedModeOptions` object.

::: zone-end

## Language support

When you use the MAI-Transcribe-1 model, diarization and prompt features aren't supported.

Optionally, specify a language code in `locales` to force recognition in a single language (for example, `en`). If you don't specify a language, the service automatically detects it. The following languages are currently supported:

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

## Related content

- For more information about using LLM Speech API, see [LLM Speech API](llm-speech.md)
- [MAI-Voice-1 in Azure Speech](mai-voices.md)
