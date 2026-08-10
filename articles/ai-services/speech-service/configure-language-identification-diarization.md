---
title: Configure language identification and diarization for speech transcription
titleSuffix: Foundry Tools
description: Configure language identification and speaker diarization for real-time, fast, and batch transcription workloads with SDK and REST examples.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 08/10/2026
ms.author: pafarley
ai-usage: ai-assisted
#Customer intent: As a developer, I want to configure language identification and diarization correctly so that short, noisy, and multi-speaker audio is transcribed reliably.
---

# Configure language identification and diarization for speech transcription

This guide shows a single configuration approach for language identification (LID) and speaker diarization across real-time speech to text, speech translation, fast transcription, and batch transcription. It focuses on two common failure patterns:

- Relying on default language detection without constraining candidate locales.
- Expecting speaker labels without explicitly enabling diarization.

The request and response properties differ by workload. Use this guide with the workload-specific articles linked in [Related content](#related-content).

| Workload | Language identification configuration | Speaker label in the response |
|---|---|---|
| Real-time speech to text or speech translation | `AutoDetectSourceLanguageConfig` with candidate locales, or a fixed source locale | `SpeakerId` when using `ConversationTranscriber` |
| Fast transcription | `locales`, or the multilingual model when supported | `speaker` on each phrase when diarization is enabled |
| Batch transcription | `properties.languageIdentification.candidateLocales` and top-level `locale` as the fallback | `speaker` on each recognized phrase when diarization is enabled |

## Prerequisites

- A [Microsoft Foundry resource](../multi-service-resource.md) for Speech.
- A [supported Speech region](regions.md?tabs=stt).
- For SDK examples, one of the supported SDK setups:
  - [Speech SDK](speech-sdk.md) for real-time speech to text and speech translation.
  - [Speech Transcription SDK](transcription-sdk.md) for fast transcription.
- Test audio that represents production conditions, including:
  - Short utterances.
  - Background noise.
  - Expected number of speakers.

## Check supported locales before you configure requests

Use these locale lists before setting `candidateLocales`, `locales`, or a fixed source locale:

- [Language identification locales](language-support.md?tabs=language-identification)
- [Speech to text locales](language-support.md?tabs=stt)
- [Speech translation locales](language-support.md?tabs=speech-translation)

Fast Transcription's multilingual model supports a separate set of locales. Check the [Speech to text supported languages](language-support.md?tabs=stt) table before you omit `locales`. If the audio locale isn't supported by that model, provide a fixed supported locale instead.

## Configure language identification for real-time speech to text or speech translation (SDK)

For full SDK coverage of `AutoDetectSourceLanguageConfig` with real-time speech to text and speech translation - including all supported languages, at-start vs. continuous modes, and custom-model mapping - see [Implement language identification](language-identification.md).

The key points when combining LID with diarization or offline transcription are:

- Supply a candidate locale list when you know the likely languages. A smaller, accurate candidate set can improve detection, especially for short or noisy audio.
- Don't include more than one locale per base language (for example, use `en-US` or `en-GB`, not both).
- If `AutoDetectSourceLanguageResult.Language` returns an empty or unexpected value, bypass auto-detect and set a fixed `SpeechRecognitionLanguage` instead.

For speech translation, read the detected language from `PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult` on the recognition result, not from `SpeechRecognitionLanguage`. The latter is a required placeholder but is currently ignored by the service when auto-detect is active.

The following pattern enables candidate-locale language identification for real-time speech to text. Use the same `AutoDetectSourceLanguageConfig` pattern with speech translation, and read the detected language from the result-specific property described above.

```csharp
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

var speechConfig = SpeechConfig.FromEndpoint(
  new Uri("YourSpeechEndpoint"), "YourSpeechKey");
var autoDetectConfig = AutoDetectSourceLanguageConfig.FromLanguages(
  new[] { "en-US", "es-ES", "fr-FR" });

using var audioConfig = AudioConfig.FromWavFileInput("sample.wav");
using var recognizer = new SpeechRecognizer(
  speechConfig, autoDetectConfig, audioConfig);
var result = await recognizer.RecognizeOnceAsync();
var detectedLanguage = AutoDetectSourceLanguageResult
  .FromResult(result).Language;
Console.WriteLine($"Detected language: {detectedLanguage}");
```

Reference: [AutoDetectSourceLanguageConfig](/dotnet/api/microsoft.cognitiveservices.speech.autodetectsourcelanguageconfig),
[AutoDetectSourceLanguageResult](/dotnet/api/microsoft.cognitiveservices.speech.autodetectsourcelanguageresult)

## Configure real-time diarization (SDK)

Real-time speaker diarization isn't enabled by default. Use `ConversationTranscriber`, enable the diarization result property when intermediate labels are needed, and verify `SpeakerId` in transcribing or transcribed events. Real-time diarization and offline diarization have different request and response properties.

```csharp
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.CognitiveServices.Speech.Transcription;

string endpoint = Environment.GetEnvironmentVariable("ENDPOINT");
string key = Environment.GetEnvironmentVariable("SPEECH_KEY");

var speechConfig = SpeechConfig.FromEndpoint(new Uri(endpoint), key);
speechConfig.SpeechRecognitionLanguage = "en-US";
speechConfig.SetProperty(
    PropertyId.SpeechServiceResponse_DiarizeIntermediateResults,
    "true");

using var audioConfig = AudioConfig.FromWavFileInput("meeting.wav");
using var transcriber = new ConversationTranscriber(speechConfig, audioConfig);

transcriber.Transcribing += (s, e) =>
{
    Console.WriteLine($"TRANSCRIBING: SpeakerId={e.Result.SpeakerId} Text={e.Result.Text}");
};

transcriber.Transcribed += (s, e) =>
{
    Console.WriteLine($"TRANSCRIBED: SpeakerId={e.Result.SpeakerId} Text={e.Result.Text}");
};

await transcriber.StartTranscribingAsync();
Console.ReadKey();
await transcriber.StopTranscribingAsync();
```

Reference: [ConversationTranscriber](/dotnet/api/microsoft.cognitiveservices.speech.transcription.conversationtranscriber), [SpeechServiceResponse_DiarizeIntermediateResults](/dotnet/api/microsoft.cognitiveservices.speech.propertyid)

## Configure fast transcription (REST and SDK)

For fast transcription, explicitly set both language and diarization behavior.

### REST example

```azurecli-interactive
curl --location "https://YourResourceName.cognitiveservices.azure.com/speechtotext/transcriptions:transcribe?api-version=2025-10-15" \
  --header "Ocp-Apim-Subscription-Key: YourSpeechResourceKey" \
  --form 'audio=@"call.wav"' \
  --form 'definition={
    "locales": ["en-US", "es-ES"],
    "diarization": {
      "enabled": true,
      "maxSpeakers": 4
    }
  }'
```

Reference: [Transcriptions - Transcribe](/rest/api/speechtotext/transcriptions/transcribe)

### Python SDK example

```python
from azure.core.credentials import AzureKeyCredential
from azure.ai.transcription import TranscriptionClient
from azure.ai.transcription.models import (
    TranscriptionContent,
    TranscriptionOptions,
    TranscriptionDiarizationOptions,
)

endpoint = "https://<your-resource>.cognitiveservices.azure.com/"
api_key = "<your-key>"

client = TranscriptionClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

with open("call.wav", "rb") as audio_file:
    options = TranscriptionOptions(
        locales=["en-US", "es-ES"],
        diarization_options=TranscriptionDiarizationOptions(max_speakers=4),
    )
    result = client.transcribe(TranscriptionContent(definition=options, audio=audio_file))

    for phrase in result.phrases:
        print(f"locale={phrase.locale}, speaker={phrase.speaker}, text={phrase.text}")
```

Reference: [TranscriptionClient](/python/api/azure-ai-transcription/azure.ai.transcription.transcriptionclient), [TranscriptionOptions](/python/api/azure-ai-transcription/azure.ai.transcription.models.transcriptionoptions), [TranscriptionDiarizationOptions](/python/api/azure-ai-transcription/azure.ai.transcription.models.transcriptiondiarizationoptions)

## Configure batch transcription (REST)

For batch jobs, set all three items explicitly:

- `locale` for fallback when no language is detected.
- `properties.languageIdentification.candidateLocales` for LID scope.
- `properties.diarization.enabled` and `properties.diarization.maxSpeakers` for speaker labels.

```json
{
  "displayName": "Batch LID + diarization",
  "locale": "en-US",
  "contentUrls": [
    "https://contoso.example/audio1.wav",
    "https://contoso.example/audio2.wav"
  ],
  "properties": {
    "languageIdentification": {
      "candidateLocales": ["en-US", "es-ES", "fr-FR"],
      "mode": "Single"
    },
    "diarization": {
      "enabled": true,
      "maxSpeakers": 4
    },
    "timeToLiveHours": 48
  }
}
```

Submit that payload with:

```http
POST /speechtotext/transcriptions:submit?api-version=2025-10-15
```

Reference: [Transcriptions - Submit](/rest/api/speechtotext/transcriptions/submit)

> [!CAUTION]
> Batch language identification supports base models. If you specify language identification together with a custom model, the service uses base models for the candidate locales, which can produce unexpected recognition results.

For diarization, use mono audio. Diarization isn't supported for stereo recordings. Set `maxSpeakers` to a realistic upper bound for the conversation; if the recording contains more speakers than the configured maximum, the service can combine speakers.

## Run a preflight verification checklist

Use this checklist before you enable production traffic:

1. Validate locale support.
   - Confirm every locale in `candidateLocales` (or `locales`) appears in the supported locale lists.
1. Verify request configuration.
  - Confirm the request uses `AutoDetectSourceLanguageConfig`, `locales`, or `properties.languageIdentification.candidateLocales` as appropriate for the workload.
  - Confirm the fixed `SpeechRecognitionLanguage` or top-level `locale` fallback is supported.
1. Verify language detection fields.
   - Real-time SDK: confirm `AutoDetectSourceLanguageResult` (or property `SpeechServiceConnection_AutoDetectSourceLanguageResult`) is populated.
   - Fast or batch transcription: confirm each phrase includes the expected `locale` value.
1. Verify speaker labeling fields.
  - Real-time diarization: confirm `SpeakerId` appears in transcribing or transcribed events.
  - Fast or batch transcription: confirm phrase-level `speaker` values are present.
  - Confirm the audio is mono when diarization is enabled.
1. Validate short or noisy audio behavior.
   - Run a noisy sample set and compare detected language against expected language.
   - If detection is unstable, rerun with a fixed source locale instead of auto-detect.
1. Validate speaker-count tuning.
   - Set `maxSpeakers` to the realistic participant ceiling.
  - Compare the returned speaker labels with the expected participant count.

## Related content

- [Implement language identification](language-identification.md)
- [Real-time diarization quickstart](get-started-stt-diarization.md)
- [Use the fast transcription API](fast-transcription-create.md)
- [Create a batch transcription](batch-transcription-create.md)
