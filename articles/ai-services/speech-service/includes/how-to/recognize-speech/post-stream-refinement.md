---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 07/23/2026
ms.author: pafarley
ai-usage: ai-assisted
---

## Post-stream refinement

Post-stream refinement gives you more accurate final results for [real-time transcription](../../../speech-to-text.md#real-time-transcription) with no impact to first-token latency. It runs a second recognition pass in parallel with real-time streaming, so intermediate and partial results stay low-latency. Only the final result is replaced with a more accurate version that uses broader audio context.

Monolingual post-stream refinement is generally available. Multilingual post-stream refinement is in public preview.

| Capability | Monolingual post-stream refinement | Multilingual post-stream refinement |
| --- | --- | --- |
| Availability | Generally available | Public preview |
| Language scope | One configured locale per recognition session | Multiple supported languages in one session, including language switching |
| Language configuration | Set the recognition locale | Use open-range automatic language detection without a candidate language list |
| Phrase lists | [Supported](../../../improve-accuracy-phrase-list.md) | Not supported during public preview |
| Diarization | [Supported](../../../get-started-stt-diarization.md) | [Supported](../../../get-started-stt-diarization.md) |

To enable post-stream refinement, set the `SpeechServiceResponse_PostProcessingOption` property on the `SpeechConfig` instance:

::: zone pivot="programming-language-cpp"

```cpp
speechConfig->SetProperty(PropertyId::SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-csharp"

```csharp
speechConfig.SetProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-java"

```java
speechConfig.setProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");
```

::: zone-end

::: zone pivot="programming-language-python"

```python
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
    "PostRefinement"
)
```

::: zone-end

### Multilingual post-stream refinement (preview)

Post-stream refinement supports multilingual recognition, so a single audio stream can span multiple languages, including switching between languages during a conversation. A single multilingual model recognizes the languages directly, so you don't set a language identification mode or provide a candidate language list. To enable the multilingual path, set `SpeechServiceResponse_PostProcessingOption` to `PostRefinement` and pass an `AutoDetectSourceLanguageConfig` configured for automatic language detection when you create the `SpeechRecognizer`.

Multilingual post-stream refinement requires Speech SDK version 1.50 or later and is available through the Speech SDK only.

During public preview, phrase lists aren't supported with multilingual post-stream refinement.

::: zone pivot="programming-language-cpp"

```cpp
speechConfig->SetProperty(PropertyId::SpeechServiceResponse_PostProcessingOption, "PostRefinement");

auto autoDetectSourceLanguageConfig = AutoDetectSourceLanguageConfig::FromOpenRange();

auto recognizer = SpeechRecognizer::FromConfig(speechConfig, autoDetectSourceLanguageConfig, audioConfig);
```

::: zone-end

::: zone pivot="programming-language-csharp"

```csharp
speechConfig.SetProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");

var autoDetectSourceLanguageConfig = AutoDetectSourceLanguageConfig.FromOpenRange();

var recognizer = new SpeechRecognizer(speechConfig, autoDetectSourceLanguageConfig, audioConfig);
```

::: zone-end

::: zone pivot="programming-language-java"

```java
speechConfig.setProperty(PropertyId.SpeechServiceResponse_PostProcessingOption, "PostRefinement");

AutoDetectSourceLanguageConfig autoDetectSourceLanguageConfig =
    AutoDetectSourceLanguageConfig.fromOpenRange();

SpeechRecognizer recognizer =
    new SpeechRecognizer(speechConfig, autoDetectSourceLanguageConfig, audioConfig);
```

::: zone-end

::: zone pivot="programming-language-python"

```python
speech_config.set_property(
    speechsdk.PropertyId.SpeechServiceResponse_PostProcessingOption,
    "PostRefinement"
)

auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig()

recognizer = speechsdk.SpeechRecognizer(
    speech_config=speech_config,
    auto_detect_source_language_config=auto_detect_source_language_config,
    audio_config=audio_config)
```

::: zone-end

During public preview, multilingual post-stream refinement recognizes 25 languages: Arabic, Chinese, Czech, Danish, Dutch, English, Finnish, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Italian, Japanese, Korean, Norwegian Bokmål, Polish, Portuguese, Russian, Spanish, Swedish, Thai, and Turkish. Because the service detects the spoken language automatically, you don't configure a locale. Audio in a language that isn't supported might produce unexpected results. For the specific locales that support monolingual and multilingual post-stream refinement, see [Speech to text language support](../../../language-support.md?tabs=stt).

Some important considerations for post-stream refinement:

- Post-stream refinement works best for longer utterances such as conversations, meetings, and dictation. For very short phrases, the refined result might be identical to the standard result.
- Post-stream refinement and TrueText are separate values of the same `SpeechServiceResponse_PostProcessingOption` property. Only one value can be set at a time.
- Monolingual and multilingual post-stream refinement have different [Azure region availability](../../../regions.md?tabs=stt).

For more information about post-processing options, see [How to use post-processing](../../../how-to-post-processing.md).

> [!IMPORTANT]
> In multilingual post-stream refinement, some locales might not show significant quality gains, and results can differ from what you observe with standard recognition.
