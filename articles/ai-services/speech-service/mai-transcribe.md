---
title: MAI-Transcribe-2 - Speech Service
titleSuffix: Foundry Tools
description: Learn how to use the MAI-Transcribe model via Azure Speech API.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 09/05/2026
ms.custom: references_regions
zone_pivot_groups: llm-speech-quickstart
ai-usage: ai-assisted

# Customer intent: As a user who implements audio transcription, I want to create transcriptions with MAI's latest MAI-Transcribe-1 model.
---

# MAI-Transcribe in Azure Speech (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Transcribe is a next‑generation speech-to-text model built in‑house by the Microsoft AI team. It delivers fast and accurate transcription across 60 languages and real-world audio conditions. MAI-Transcribe-2 supports a wide range of workloads including video captioning, meetings, clinical notes, call center documentation, accessibility tools, content creation, and voice agents. The model provides speaker diarization, strong performance in noisy environments, word-level timestamps, automatic language identification, keyword biasing, code switching, and configurable transcription styles (clean transcripts without fillers, or verbatim). 

The following models are supported:

- `MAI-Transcribe-2`
- `MAI-Transcribe-1.5`
- `MAI-Transcribe-1`: **Deprecated on Aug 20, 2026.**

## Prerequisites

> [!div class="checklist"]
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - [A Microsoft Foundry resource for Speech](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) in the Azure portal.
> - The Speech resource key and region. After your Speech resource is deployed, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).
> - An audio file (less than 300 MB in size) in one of these formats: WAV, MP3, or FLAC. For the maximum audio duration, see the `audio` parameter in the [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe) REST reference. If you enable speaker diarization, see the note on recording length in the next section.


## Use a MAI-Transcribe model

Use MAI‑Transcribe‑2 to generate transcripts from audio input. Configure the following features through the corresponding API parameters:

| Feature | Parameter | Values | Default | Description |
| --- | :-- | :------------- | --- | --- |
| **Model selection** _(Required)_ | `enhancedMode.`<br>`model` | `"MAI-Transcribe-2"`&nbsp; | — | **Set to call the MAI‑Transcribe model.** |
| **Enhanced mode** _(Required)_ | `enhancedMode.`<br>`enabled` | `true`&nbsp;\|&nbsp;`false` | `false` | **Set to `true` to call MAI-Transcribe.** |
| **Speaker diarization** | `diarization.`<br>`enabled` | `true`&nbsp;\|&nbsp;`false` | `false` | Segments the recording by speaker and attributes each segment to the correct person. Returns speaker-labelled segments with `speaker`, `offsetMilliseconds`, and `durationMilliseconds` metadata. Supports shorter recordings than transcription without diarization; see the note that follows this table. |
| **Word-level timestamps** | `modelOptions.`<br>`timestamps` | `"word"`&nbsp;\|&nbsp;`"segment"`&nbsp;\|&nbsp;`"none"` | `none` | Controls timing granularity. `"word"` returns `offsetMilliseconds` and `durationMilliseconds` for every word, enabling precise alignment, search, navigation, and editing. `"segment"` returns timing information for each segment: the output transcript is partitioned into segments by language and speaker. So when diarization is enabled, a segment is created for each speaker and language, and when it's disabled it's created for each language. `"none"` omits timing data. |
| **Keyword biasing** | `phraseList.phrases` | Array of strings | `[]` | Biases recognition toward supplied keywords. Use for domain-specific terminology, abbreviations, product names, and proper nouns that are hard to disambiguate from context alone. Terms are hints, not forced output. |
| **Transcription styles** | `modelOptions.`<br>`transcribeStyle` | `"verbatim"`&nbsp;\|&nbsp;`"clean"` | `"verbatim"` | Controls output style. `"verbatim"` captures speech exactly as spoken, including filler words and false starts, for compliance, QA, and analysis workloads. `clean` removes fillers to produce readable captions, notes, and published transcripts. |
| **Language selection** | `locales` | [`"language_code"`] | *Unspecified (Automatic Detection)* | Allows forcing transcription in a specific language. This is a very strong hint to the model, and don't specify it unless you're absolutely certain that the recording is in the given language, and the default auto-detection doesn't work. Only one language can be provided here. MAI-Transcribe-2 supports 60 languages.|
| **Code switching** | *Automatic* | — | — |  For commonly blended language pairs such as Hinglish and Spanglish, handles conversations that move between languages mid-utterance. |
| **Noise robustness** | *Inherent* | — | — | Maintains transcription quality on audio recorded outside controlled environments, including background noise, overlapping speech, and variable microphone quality. |

> [!NOTE]
> Speaker diarization in enhanced mode currently supports shorter recordings than transcription does. In preview, requests with `diarization.enabled` set to `true` have failed for recordings of about 15 minutes and longer, returning HTTP 408 with a `Timeout` error, HTTP 500, or HTTP 503 with a `diarization_unavailable` error — while the same recordings transcribed successfully with diarization disabled, including a 73-minute file in a single request. These errors don't indicate a network or upload problem. For long recordings, transcribe with diarization disabled and use the returned word-level timestamps with a separate speaker diarization step.

::: zone pivot="ai-foundry"

To start using transcription with enhanced mode, first follow the [LLM Speech quickstart](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=ai-foundry). Then, specify the `Model`.

::: zone-end

::: zone pivot="programming-language-rest"

To use the MAI-Transcribe model:
- Set the `enhancedMode.enabled` property to `true` in the request.
- Set the `enhancedMode.model` property to `"MAI-Transcribe-2"` in the request.
- Use one of the regions where MAI-Transcribe is available [Speech service regions](regions.md?tabs=llmspeech).

```azurecli-interactive
curl --location 'https://YourResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15' \
--header 'Content-Type: multipart/form-data' \
--header 'Ocp-Apim-Subscription-Key: <YourSpeechResourceKey>' \
--form 'audio=@"YourAudioFile.wav"' \
--form 'definition={ 
  "enhancedMode": {
    "enabled": true,
    "model": "MAI-Transcribe-2"
  }
}'
```

Optionally, for `MAI-Transcribe-2`, enable speaker `diarization` to distinguish between speakers and attribute words to the right person within a recording.

```
 --form 'definition={ 
  "enhancedMode": {
    "enabled": true,
    "model": "MAI-Transcribe-2"
  },
  "diarization": {"enabled": true}
}
```

Optionally, for `MAI-Transcribe-2`, control the transcript style using `transcribeStyle`. The default output is `verbatim` if you need the raw spoken content preserved, including fillers (“um”, “uh”), false starts, and self‑corrections. Set `transcribeStyle` to `clean` if you need a readability‑optimized transcript that removes filler words and auto‑formats common speech patterns.

```
 --form 'definition={ 
  "enhancedMode": {
    "enabled": true,
    "model": "MAI-Transcribe-2",
    "modelOptions": {
      "transcribeStyle": "clean"
    }
  }
}
```

Optionally, for `MAI-Transcribe-2`, enable word‑level `timestamps` to provide precise timing for every word, supporting accurate alignment, search, navigation, and editing.


```
 --form 'definition={ 
  "enhancedMode": {
    "enabled": true,
    "model": "MAI-Transcribe-2",
    "modelOptions": {
      "timestamps": "word"
    }
  }
}
```

Optionally, add a list of phrases to increase accuracy in specialized domains by using `phraseList.phrases`. This feature implements keyword biasing.

```
 --form 'definition={ 
  "enhancedMode": {
    "enabled": true,
    "model": "MAI-Transcribe-2"
  }, 
  "phraseList": {
     "phrases": ["phrase 1", "phrase 2"]
   },
 }'
```

Optionally, specify a language code in `locales` to force recognition in a single language. If you don't specify, the model automatically detects the language. For example:

```
--form 'definition={
  "locales": ["en"],
  "enhancedMode": {
    "enabled": true,
    "model":"MAI-Transcribe-2"
  }
}'
```
::: zone-end

::: zone pivot="programming-language-python"

To start using the MAI-Transcribe model, first follow the [Azure Speech API's quickstart guide](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python) to use Fast Transcription API's `enhancedMode`. Then, specify `MAI-Transcribe-2` in the `enhancedMode.model` property. See the complete guide for all the parameters supported by MAI-Transcribe, currently only available under the **REST API** tab.

::: zone-end

::: zone pivot="programming-language-csharp"

To start using the MAI-Transcribe model, first follow the [Azure Speech API's quickstart guide](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python) to use Fast Transcription API's `enhancedMode`. Then, specify `MAI-Transcribe-2` in the `enhancedMode.model` property. See the complete guide for all the parameters supported by MAI-Transcribe, currently only available under the **REST API** tab.


::: zone-end

::: zone pivot="programming-language-javascript"

To start using the MAI-Transcribe model, first follow the [Azure Speech API's quickstart guide](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python) to use Fast Transcription API's `enhancedMode`. Then, specify `MAI-Transcribe-2` in the `enhancedMode.model` property. See the complete guide for all the parameters supported by MAI-Transcribe, currently only available under the **REST API** tab.

::: zone-end

::: zone pivot="programming-language-java"

To start using the MAI-Transcribe model, first follow the [Azure Speech API's quickstart guide](/azure/ai-services/speech-service/llm-speech?tabs=new-foundry%2Cwindows&pivots=programming-language-python) to use Fast Transcription API's `enhancedMode`. Then, specify `MAI-Transcribe-2` in the `enhancedMode.model` property. For a complete guide to all the parameters supported by MAI-Transcribe, see the **REST API** tab.

::: zone-end

## Language support

By default, the model operates in multilingual mode. The following languages are currently supported:

[!INCLUDE [MAI Transcribe language support](includes/language-support/mai-transcribe.md)]


### Use MAI-Transcribe with Voice Live

You can also use the MAI-Transcribe model for input audio transcription in the [Voice Live API](./voice-live.md). Set the `model` field in the `input_audio_transcription` session configuration. For details, see [How to customize Voice Live input and output](./voice-live-how-to-customize.md).


## Related content

- For more information about using LLM Speech API, see [LLM Speech API](llm-speech.md)
- [MAI-Voice in Azure Speech](mai-voices.md)
- [How to customize Voice Live input and output](./voice-live-how-to-customize.md)
