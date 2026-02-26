---
title: Use pronunciation assessment
titleSuffix: Foundry Tools
description: Learn about pronunciation assessment features that are currently publicly available. Choose the programming solution for your needs.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.custom:
  - devx-track-extended-java
  - devx-track-go
  - devx-track-js
  - devx-track-python
  - ignite-2023
  - build-2024
ms.topic: how-to
ms.date: 11/21/2025
ms.author: pafarley
zone_pivot_groups: programming-languages-ai-services
#Customer intent: As a developer, I want to implement pronunciation assessment on spoken language using a technology that works in my environment to gives feedback on accuracy and fluency.
---

# Use pronunciation assessment

In this article, you learn how to evaluate a user's speech pronunciation with speech to text in the Speech SDK. Pronunciation assessment gives speakers feedback on the accuracy and fluency of spoken audio.

> [!NOTE]
> Pronunciation assessment uses a specific version of the speech to text model, different from the standard speech to text model, to ensure consistent and accurate pronunciation assessment.

## Availability and pricing

For information about the availability of pronunciation assessment, see [supported languages](language-support.md?tabs=pronunciation-assessment) and [available regions](regions.md?tabs=scenarios#regions).

As a baseline, usage of pronunciation assessment costs the same as speech to text for Standard or commitment tier [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services). If you [purchase a commitment tier](../commitment-tier.md) for speech to text, the spend for pronunciation assessment goes towards meeting the commitment. For more information, see [Pricing](./pronunciation-assessment-tool.md#pricing).


## Streaming vs. continuous mode

Pronunciation assessment supports uninterrupted streaming mode. The recording time can be unlimited through the Speech SDK. As long as you don't stop recording, the evaluation process doesn't finish and you can pause and resume evaluation conveniently.


::: zone pivot="programming-language-csharp"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/csharp/sharedcontent/console/speech_recognition_samples.cs#:~:text=PronunciationAssessmentWithStream).

::: zone-end

::: zone pivot="programming-language-cpp"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/cpp/windows/language-learning/samples/speech_recognition_samples.cpp#:~:text=PronunciationAssessmentWithStream).

::: zone-end

::: zone pivot="programming-language-java"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/java/android/language-learning/app/src/main/java/com/microsoft/cognitiveservices/speech/samples/sdkdemo/MainActivity.java#:~:text=pronunciationAssessmentFromStreamButton.setOnClickListener).

::: zone-end

::: zone pivot="programming-language-python"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/python/console/language-learning/pronunciation_assessment.py#:~:text=def%20pronunciation_assessment_from_stream()), or try the [Azure Speech in Foundry Tools Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit).

::: zone-end

::: zone pivot="programming-language-javascript"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/javascript/node/language-learning/pronunciationAssessment.js).

::: zone-end

::: zone pivot="programming-language-objectivec"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/objective-c/ios/language-learning/speech-samples/ViewController.m#:~:text=(void)pronunciationAssessFromStream).

::: zone-end

::: zone pivot="programming-language-swift"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/swift/ios/language-learning/speech-samples/ViewController.swift#:~:text=func%20pronunciationAssessmentWithStream()).

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end


::: zone pivot="programming-language-csharp"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/csharp/sharedcontent/console/speech_recognition_samples.cs) under the function `PronunciationAssessmentContinuousWithFile`.

::: zone-end

::: zone pivot="programming-language-cpp"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text.

::: zone-end

::: zone pivot="programming-language-java"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/java/jre/console/language-learning/src/com/microsoft/cognitiveservices/speech/samples/console/SpeechRecognitionSamples.java) under the function `pronunciationAssessmentContinuousWithFile`.

::: zone-end

::: zone pivot="programming-language-python"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/python/console/language-learning/pronunciation_assessment.py) under the function `pronunciation_assessment_continuous_from_file`, or try the [Azure Speech Toolkit](https://marketplace.visualstudio.com/items?itemName=ms-azureaispeech.azure-ai-speech-toolkit).

::: zone-end

::: zone pivot="programming-language-javascript"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/javascript/node/language-learning/pronunciationAssessmentContinue.js).

::: zone-end

::: zone pivot="programming-language-objectivec"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m) under the function `pronunciationAssessFromFile`.

::: zone-end

::: zone pivot="programming-language-swift"

If your audio file exceeds 30 seconds, use continuous mode for processing. In continuous mode, the `EnableMiscue` option is not supported. To obtain `Omission` and `Insertion` tags, you need to compare the recognized results with the reference text. You can find a sample implementation for continuous mode on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/scenarios/swift/ios/language-learning/speech-samples/ViewController.swift) under the function `continuousPronunciationAssessment`.

::: zone-end

::: zone pivot="programming-language-go"

If your audio file exceeds 30 seconds, use continuous mode for processing. Please note that pronunciation assessment is not supported in the Speech SDK for Go. To enable this feature, select a different programming language for your solution.

::: zone-end


## Set configuration parameters

::: zone pivot="programming-language-go"

> [!NOTE]
> Pronunciation assessment is not available with the Speech SDK for Go. You can read about the concepts in this guide. Select another programming language for your solution.

::: zone-end

In the `SpeechRecognizer`, you can specify the language to learn or practice improving pronunciation. The default locale is `en-US`. To learn how to specify the learning language for pronunciation assessment in your own application, you can use the following sample code.

::: zone pivot="programming-language-csharp"

```csharp
var recognizer = new SpeechRecognizer(speechConfig, "en-US", audioConfig);
```

::: zone-end

::: zone pivot="programming-language-cpp"

```cpp
auto recognizer = SpeechRecognizer::FromConfig(speechConfig, "en-US", audioConfig);
```

::: zone-end

::: zone pivot="programming-language-java"

```Java
SpeechRecognizer recognizer = new SpeechRecognizer(speechConfig, "en-US", audioConfig);
```

::: zone-end

::: zone pivot="programming-language-python"

```Python
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, language="en-US", audio_config=audio_config)
```

::: zone-end

::: zone pivot="programming-language-javascript"

```JavaScript
speechConfig.speechRecognitionLanguage = "en-US";
```

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
SPXSpeechRecognizer* recognizer = [[SPXSpeechRecognizer alloc] initWithSpeechConfiguration:speechConfig language:@"en-US" audioConfiguration:audioConfig];
```

::: zone-end

::: zone pivot="programming-language-swift"

```swift
let recognizer = try! SPXSpeechRecognizer(speechConfiguration: speechConfig, language: "en-US", audioConfiguration: audioConfig)
```

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

> [!TIP]
> If you aren't sure which locale to set for a language that has multiple locales, try each locale separately. For instance, for Spanish, try `es-ES` and `es-MX`. Determine which locale scores higher for your scenario.

You must create a `PronunciationAssessmentConfig` object. You can set `EnableProsodyAssessment` to enable prosody assessment. For more information, see [configuration methods](#configuration-methods).

::: zone pivot="programming-language-csharp"

```csharp
var pronunciationAssessmentConfig = new PronunciationAssessmentConfig(
    referenceText: "",
    gradingSystem: GradingSystem.HundredMark,
    granularity: Granularity.Phoneme,
    enableMiscue: false);
pronunciationAssessmentConfig.EnableProsodyAssessment();
```

::: zone-end

::: zone pivot="programming-language-cpp"

```cpp
auto pronunciationConfig = PronunciationAssessmentConfig::Create("", PronunciationAssessmentGradingSystem::HundredMark, PronunciationAssessmentGranularity::Phoneme, false);
pronunciationConfig->EnableProsodyAssessment();
```

::: zone-end

::: zone pivot="programming-language-java"

```Java
PronunciationAssessmentConfig pronunciationConfig = new PronunciationAssessmentConfig("",
    PronunciationAssessmentGradingSystem.HundredMark, PronunciationAssessmentGranularity.Phoneme, false);
pronunciationConfig.enableProsodyAssessment();
```

::: zone-end

::: zone pivot="programming-language-python"

```Python
pronunciation_config = speechsdk.PronunciationAssessmentConfig(
    reference_text="",
    grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
    granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme,
    enable_miscue=False)
pronunciation_config.enable_prosody_assessment()
```

::: zone-end

::: zone pivot="programming-language-javascript"

```JavaScript
var pronunciationAssessmentConfig = new sdk.PronunciationAssessmentConfig(
    referenceText: "",
    gradingSystem: sdk.PronunciationAssessmentGradingSystem.HundredMark,
    granularity: sdk.PronunciationAssessmentGranularity.Phoneme,
    enableMiscue: false);
pronunciationAssessmentConfig.enableProsodyAssessment();
```

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
SPXPronunciationAssessmentConfiguration *pronunicationConfig =
[[SPXPronunciationAssessmentConfiguration alloc] init:@"" gradingSystem:SPXPronunciationAssessmentGradingSystem_HundredMark granularity:SPXPronunciationAssessmentGranularity_Phoneme enableMiscue:false];
[pronunicationConfig enableProsodyAssessment];
```

::: zone-end

::: zone pivot="programming-language-swift"

```swift
let pronAssessmentConfig = try! SPXPronunciationAssessmentConfiguration("",
    gradingSystem: .hundredMark,
    granularity: .phoneme,
    enableMiscue: false)
pronAssessmentConfig.enableProsodyAssessment()
```

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

This table lists some of the key configuration parameters for pronunciation assessment.

| Parameter | Description |
|-----------|-------------|
| `ReferenceText` | The text that the pronunciation is evaluated against.<br/><br/>The `ReferenceText` parameter is optional. Set the reference text if you want to run a [scripted assessment](#scripted-assessment-results) for the reading language learning scenario. Don't set the reference text if you want to run an [unscripted assessment](#unscripted-assessment-results).<br/><br/>For pricing differences between scripted and unscripted assessment, see [Pricing](./pronunciation-assessment-tool.md#pricing). |
| `GradingSystem` | The point system for score calibration. `FivePoint` gives a 0-5 floating point score. `HundredMark` gives a 0-100 floating point score. Default: `FivePoint`. |
| `Granularity` | Determines the lowest level of evaluation granularity. Returns scores for levels greater than or equal to the minimal value. Accepted values are `Phoneme`, which shows the score on the full text, word, syllable, and phoneme level, `Word`, which shows the score on the full text and word level, or `FullText`, which shows the score on the full text level only. The provided full reference text can be a word, sentence, or paragraph. It depends on your input reference text. Default: `Phoneme`.|
| `EnableMiscue` | Enables miscue calculation when the pronounced words are compared to the reference text. Enabling miscue is optional. If this value is `True`, the `ErrorType` result value can be set to `Omission` or `Insertion` based on the comparison. Values are `False` and `True`. Default: `False`. To enable miscue calculation, set the `EnableMiscue` to `True`. You can refer to the code snippet above the table. |
| `ScenarioId` | A GUID for a customized point system. |

### Configuration methods

This table lists some of the optional methods you can set for the `PronunciationAssessmentConfig` object.

> [!NOTE]
> Prosody assessment is only available in the [en-US](./language-support.md?tabs=pronunciation-assessment) locale.
>
> To explore the prosody assessment, upgrade to the SDK version 1.35.0 or later.

| Method | Description |
|-----------|-------------|
| `EnableProsodyAssessment` | Enables prosody assessment for your pronunciation evaluation. This feature assesses aspects like stress, intonation, speaking speed, and rhythm. This feature provides insights into the naturalness and expressiveness of your speech.<br/><br/>Enabling prosody assessment is optional. If this method is called, the `ProsodyScore` result value is returned. |

## Get pronunciation assessment results

When speech is recognized, you can request the pronunciation assessment results as SDK objects or a JSON string.

::: zone pivot="programming-language-csharp"

```csharp
using (var speechRecognizer = new SpeechRecognizer(
    speechConfig,
    audioConfig))
{
    // (Optional) get the session ID
    speechRecognizer.SessionStarted += (s, e) => {
        Console.WriteLine($"SESSION ID: {e.SessionId}");
    };
    pronunciationAssessmentConfig.ApplyTo(speechRecognizer);
    var speechRecognitionResult = await speechRecognizer.RecognizeOnceAsync();

    // The pronunciation assessment result as a Speech SDK object
    var pronunciationAssessmentResult =
        PronunciationAssessmentResult.FromResult(speechRecognitionResult);

    // The pronunciation assessment result as a JSON string
    var pronunciationAssessmentResultJson = speechRecognitionResult.Properties.GetProperty(PropertyId.SpeechServiceResponse_JsonResult);
}
```

::: zone-end

::: zone pivot="programming-language-cpp"

Word, syllable, and phoneme results aren't available by using SDK objects with the Speech SDK for C++. Word, syllable, and phoneme results are only available in the JSON string.

```cpp
auto speechRecognizer = SpeechRecognizer::FromConfig(
    speechConfig,
    audioConfig);
// (Optional) get the session ID
speechRecognizer->SessionStarted.Connect([](const SessionEventArgs& e) {
    std::cout << "SESSION ID: " << e.SessionId << std::endl;
});
pronunciationAssessmentConfig->ApplyTo(speechRecognizer);
speechRecognitionResult = speechRecognizer->RecognizeOnceAsync().get();

// The pronunciation assessment result as a Speech SDK object
auto pronunciationAssessmentResult =
    PronunciationAssessmentResult::FromResult(speechRecognitionResult);

// The pronunciation assessment result as a JSON string
auto pronunciationAssessmentResultJson = speechRecognitionResult->Properties.GetProperty(PropertyId::SpeechServiceResponse_JsonResult);
```

To learn how to specify the learning language for pronunciation assessment in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/cpp/windows/console/samples/speech_recognition_samples.cpp#L624).

::: zone-end

::: zone pivot="programming-language-java"

For Android application development, the word, syllable, and phoneme results are available by using SDK objects with the Speech SDK for Java. The results are also available in the JSON string. For Java Runtime (JRE) application development, the word, syllable, and phoneme results are only available in the JSON string.

```Java
SpeechRecognizer speechRecognizer = new SpeechRecognizer(
    speechConfig,
    audioConfig);
// (Optional) get the session ID
speechRecognizer.sessionStarted.addEventListener((s, e) -> {
    System.out.println("SESSION ID: " + e.getSessionId());
});
pronunciationAssessmentConfig.applyTo(speechRecognizer);
Future<SpeechRecognitionResult> future = speechRecognizer.recognizeOnceAsync();
SpeechRecognitionResult speechRecognitionResult = future.get(30, TimeUnit.SECONDS);

// The pronunciation assessment result as a Speech SDK object
PronunciationAssessmentResult pronunciationAssessmentResult =
    PronunciationAssessmentResult.fromResult(speechRecognitionResult);

// The pronunciation assessment result as a JSON string
String pronunciationAssessmentResultJson = speechRecognitionResult.getProperties().getProperty(PropertyId.SpeechServiceResponse_JsonResult);

recognizer.close();
speechConfig.close();
audioConfig.close();
pronunciationAssessmentConfig.close();
speechRecognitionResult.close();
```

::: zone-end

::: zone pivot="programming-language-javascript"

```JavaScript
var speechRecognizer = SpeechSDK.SpeechRecognizer.FromConfig(speechConfig, audioConfig);
// (Optional) get the session ID
speechRecognizer.sessionStarted = (s, e) => {
    console.log(`SESSION ID: ${e.sessionId}`);
};
pronunciationAssessmentConfig.applyTo(speechRecognizer);

speechRecognizer.recognizeOnceAsync((speechRecognitionResult: SpeechSDK.SpeechRecognitionResult) => {
    // The pronunciation assessment result as a Speech SDK object
    var pronunciationAssessmentResult = SpeechSDK.PronunciationAssessmentResult.fromResult(speechRecognitionResult);

    // The pronunciation assessment result as a JSON string
    var pronunciationAssessmentResultJson = speechRecognitionResult.properties.getProperty(SpeechSDK.PropertyId.SpeechServiceResponse_JsonResult);
},
{});
```

To learn how to specify the learning language for pronunciation assessment in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/tree/master/samples/js/node).

::: zone-end

::: zone pivot="programming-language-python"

```Python
speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, \
        audio_config=audio_config)
# (Optional) get the session ID
speech_recognizer.session_started.connect(lambda evt: print(f"SESSION ID: {evt.session_id}"))
pronunciation_assessment_config.apply_to(speech_recognizer)
speech_recognition_result = speech_recognizer.recognize_once()
# The pronunciation assessment result as a Speech SDK object
pronunciation_assessment_result = speechsdk.PronunciationAssessmentResult(speech_recognition_result)

# The pronunciation assessment result as a JSON string
pronunciation_assessment_result_json = speech_recognition_result.properties.get(speechsdk.PropertyId.SpeechServiceResponse_JsonResult)
```

To learn how to specify the learning language for pronunciation assessment in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py#LL937C1-L937C1).

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
SPXSpeechRecognizer* speechRecognizer = \
        [[SPXSpeechRecognizer alloc] initWithSpeechConfiguration:speechConfig
                                              audioConfiguration:audioConfig];
// (Optional) get the session ID
[speechRecognizer addSessionStartedEventHandler: ^ (SPXRecognizer *sender, SPXSessionEventArgs *eventArgs) {
    NSLog(@"SESSION ID: %@", eventArgs.sessionId);
}];
[pronunciationAssessmentConfig applyToRecognizer:speechRecognizer];

SPXSpeechRecognitionResult *speechRecognitionResult = [speechRecognizer recognizeOnce];

// The pronunciation assessment result as a Speech SDK object
SPXPronunciationAssessmentResult* pronunciationAssessmentResult = [[SPXPronunciationAssessmentResult alloc] init:speechRecognitionResult];

// The pronunciation assessment result as a JSON string
NSString* pronunciationAssessmentResultJson = [speechRecognitionResult.properties getPropertyByName:SPXSpeechServiceResponseJsonResult];
```

To learn how to specify the learning language for pronunciation assessment in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L862).

::: zone-end

::: zone pivot="programming-language-swift"

```swift
let speechRecognizer = try! SPXSpeechRecognizer(speechConfiguration: speechConfig, audioConfiguration: audioConfig)
// (Optional) get the session ID
speechRecognizer.addSessionStartedEventHandler { (sender, evt) in
	print("SESSION ID: \(evt.sessionId)")
try! pronConfig.apply(to: speechRecognizer)

let speechRecognitionResult = try? speechRecognizer.recognizeOnce()

// The pronunciation assessment result as a Speech SDK object
let pronunciationAssessmentResult = SPXPronunciationAssessmentResult(speechRecognitionResult!)

// The pronunciation assessment result as a JSON string
let pronunciationAssessmentResultJson = speechRecognitionResult!.properties?.getPropertyBy(SPXPropertyId.speechServiceResponseJsonResult)
```

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

### Result parameters

Depending on whether you're using [scripted](#scripted-assessment-results) or [unscripted](#unscripted-assessment-results) assessment, you can get different pronunciation assessment results. Scripted assessment is for the reading language learning scenario. Unscripted assessment is for the speaking language learning scenario.

> [!NOTE]
> For pricing differences between scripted and unscripted assessment, see [Pricing](./pronunciation-assessment-tool.md#pricing).

#### Scripted assessment results

This table lists some of the key pronunciation assessment results for the scripted assessment, or reading scenario.

| Parameter | Description | Granularity |
|:----------|:------------|:------------|
| `AccuracyScore` | Pronunciation accuracy of the speech. Accuracy indicates how closely the phonemes match a native speaker's pronunciation. Syllable, word, and full text accuracy scores are aggregated from the phoneme-level accuracy score, and refined with assessment objectives. | Phoneme level，<br>Syllable level (en-US only)，<br>Word level，<br>Full Text level |
| `FluencyScore` | Fluency of the given speech. Fluency indicates how closely the speech matches a native speaker's use of silent breaks between words. | Full Text level |
| `CompletenessScore` | Completeness of the speech, calculated by the ratio of pronounced words to the input reference text. |Full Text level|
| `ProsodyScore` | Prosody of the given speech. Prosody indicates how natural the given speech is, including stress, intonation, speaking speed, and rhythm. | Full Text level|
| `PronScore` | Overall score of the pronunciation quality of the given speech. `PronScore` is calculated from `AccuracyScore`, `FluencyScore`, `CompletenessScore`, and `ProsodyScore` with weight, provided that `ProsodyScore` and `CompletenessScore` are available. If either of them isn't available, `PronScore` won't consider that score.|Full Text level|
| `ErrorType` | This value indicates the error type compared to the reference text. Options include whether a word is omitted, inserted, or improperly inserted with a break. It also indicates a missing break at punctuation. It also indicates whether a word is badly pronounced, or monotonically rising, falling, or flat on the utterance. Possible values are `None` for no error on this word, `Omission`, `Insertion`, `Mispronunciation`, `UnexpectedBreak`, `MissingBreak`, and `Monotone`. The error type can be `Mispronunciation` when the pronunciation `AccuracyScore` for a word is below 60.| Word level|

#### Unscripted assessment results

This table lists some of the key pronunciation assessment results for the unscripted assessment, or speaking scenario.

> [!NOTE]
> Prosody assessment is only available in the [en-US](./language-support.md?tabs=pronunciation-assessment) locale. For unscripted assessment, the speech-to-text (STT) model used is different from Azure STT. If you need assessment based on highly accurate recognized text, we recommend first calling Azure STT to obtain the reference text, and then performing scripted assessment.

| Response parameter | Description | Granularity |
|:-------------------|:------------|:------------|
| `AccuracyScore`    | Pronunciation accuracy of the speech. Accuracy indicates how closely the phonemes match a native speaker's pronunciation. Syllable, word, and full text accuracy scores are aggregated from phoneme-level accuracy score, and refined with assessment objectives. | Phoneme level，<br>Syllable level (en-US only)，<br>Word level，<br>Full Text level |
| `FluencyScore`     | Fluency of the given speech. Fluency indicates how closely the speech matches a native speaker's use of silent breaks between words. | Full Text level |
| `ProsodyScore`     | Prosody of the given speech. Prosody indicates how natural the given speech is, including stress, intonation, speaking speed, and rhythm. | Full Text level |
| `PronScore`        | Overall score of the pronunciation quality of the given speech. `PronScore` is calculated from `AccuracyScore`, `FluencyScore`, and `ProsodyScore` with weight, provided that `ProsodyScore` is available. If `ProsodyScore` isn't available, `PronScore` won't consider that score.| Full Text level |
| `ErrorType`        | A word is badly pronounced, improperly inserted with a break, or missing a break at punctuation. It also indicates whether a pronunciation is monotonically rising, falling, or flat on the utterance. Possible values are `None` for no error on this word, `Mispronunciation`, `UnexpectedBreak`, `MissingBreak`, and `Monotone`. | Word level |

The following table describes the prosody assessment results in more detail:

| Field | Description |
|:------|:------------|
| `ProsodyScore`    | Prosody score of the entire utterance. |
| `Feedback`        | Feedback on the word level, including `Break` and `Intonation`. |
| `Break`           |                                                             |
| `ErrorTypes`      | Error types related to breaks, including `UnexpectedBreak` and `MissingBreak`. The current version doesn't provide the break error type. You need to set thresholds on the fields `UnexpectedBreak – Confidence` and `MissingBreak – confidence` to decide whether there's an unexpected break or missing break before the word. |
| `UnexpectedBreak` | Indicates an unexpected break before the word. |
| `MissingBreak`    | Indicates a missing break before the word. |
| `Thresholds`      | Suggested thresholds on both confidence scores are 0.75. That means, if the value of `UnexpectedBreak – Confidence` is larger than 0.75, it has an unexpected break. If the value of `MissingBreak – confidence` is larger than 0.75, it has a missing break. While 0.75 is a value we recommend, it's better to adjust the thresholds based on your own scenario. If you want to have variable detection sensitivity on these two breaks, you can assign different thresholds to the `UnexpectedBreak - Confidence` and `MissingBreak - Confidence` fields.  |
| `Intonation`      | Indicates intonation in speech. |
| `ErrorTypes`      | Error types related to intonation, currently supporting only Monotone. If the `Monotone` exists in the field `ErrorTypes`, the utterance is detected to be monotonic. Monotone is detected on the whole utterance, but the tag is assigned to all the words. All the words in the same utterance share the same monotone detection information. |
| `Monotone`   | Indicates monotonic speech. |
| `Thresholds (Monotone Confidence)` | The fields `Monotone - SyllablePitchDeltaConfidence` are reserved for user-customized monotone detection. If you're unsatisfied with the provided monotone decision, adjust the thresholds on these fields to customize the detection according to your preferences. |

### JSON result example

The [scripted](#scripted-assessment-results) pronunciation assessment results for the spoken word "hello" are shown as a JSON string in the following example.

- The phoneme [alphabet](#phoneme-alphabet-format) is IPA.
- The [syllables](#syllable-groups) are returned alongside phonemes for the same word.
- You can use the `Offset` and `Duration` values to align syllables with their corresponding phonemes. For example, the starting offset (11700000) of the second syllable `loʊ` aligns with the third phoneme, `l`. The offset represents the time at which the recognized speech begins in the audio stream. The value is measured in 100-nanosecond units. To learn more about `Offset` and `Duration`, see [response properties](rest-speech-to-text-short.md#response-properties).
- There are five `NBestPhonemes` that correspond to the number of [spoken phonemes](#assess-spoken-phonemes) requested.
- Within `Phonemes`, the most likely [spoken phonemes](#assess-spoken-phonemes) was `ə` instead of the expected phoneme `ɛ`. The expected phoneme `ɛ` only received a confidence score of 47. Other potential matches received confidence scores of 52, 17, and 2.

```json
{
    "Id": "bbb42ea51bdb46d19a1d685e635fe173",
    "RecognitionStatus": 0,
    "Offset": 7500000,
    "Duration": 13800000,
    "DisplayText": "Hello.",
    "NBest": [
        {
            "Confidence": 0.975003,
            "Lexical": "hello",
            "ITN": "hello",
            "MaskedITN": "hello",
            "Display": "Hello.",
            "PronunciationAssessment": {
                "AccuracyScore": 100,
                "FluencyScore": 100,
                "CompletenessScore": 100,
                "PronScore": 100
            },
            "Words": [
                {
                    "Word": "hello",
                    "Offset": 7500000,
                    "Duration": 13800000,
                    "PronunciationAssessment": {
                        "AccuracyScore": 99.0,
                        "ErrorType": "None"
                    },
                    "Syllables": [
                        {
                            "Syllable": "hɛ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 91.0
                            },
                            "Offset": 7500000,
                            "Duration": 4100000
                        },
                        {
                            "Syllable": "loʊ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0
                            },
                            "Offset": 11700000,
                            "Duration": 9600000
                        }
                    ],
                    "Phonemes": [
                        {
                            "Phoneme": "h",
                            "PronunciationAssessment": {
                                "AccuracyScore": 98.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "h",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 52.0
                                    },
                                    {
                                        "Phoneme": "ə",
                                        "Score": 35.0
                                    },
                                    {
                                        "Phoneme": "k",
                                        "Score": 23.0
                                    },
                                    {
                                        "Phoneme": "æ",
                                        "Score": 20.0
                                    }
                                ]
                            },
                            "Offset": 7500000,
                            "Duration": 3500000
                        },
                        {
                            "Phoneme": "ɛ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 47.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "ə",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "l",
                                        "Score": 52.0
                                    },
                                    {
                                        "Phoneme": "ɛ",
                                        "Score": 47.0
                                    },
                                    {
                                        "Phoneme": "h",
                                        "Score": 17.0
                                    },
                                    {
                                        "Phoneme": "æ",
                                        "Score": 2.0
                                    }
                                ]
                            },
                            "Offset": 11100000,
                            "Duration": 500000
                        },
                        {
                            "Phoneme": "l",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "l",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 46.0
                                    },
                                    {
                                        "Phoneme": "ə",
                                        "Score": 5.0
                                    },
                                    {
                                        "Phoneme": "ɛ",
                                        "Score": 3.0
                                    },
                                    {
                                        "Phoneme": "u",
                                        "Score": 1.0
                                    }
                                ]
                            },
                            "Offset": 11700000,
                            "Duration": 1100000
                        },
                        {
                            "Phoneme": "oʊ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "d",
                                        "Score": 29.0
                                    },
                                    {
                                        "Phoneme": "t",
                                        "Score": 24.0
                                    },
                                    {
                                        "Phoneme": "n",
                                        "Score": 22.0
                                    },
                                    {
                                        "Phoneme": "l",
                                        "Score": 18.0
                                    }
                                ]
                            },
                            "Offset": 12900000,
                            "Duration": 8400000
                        }
                    ]
                }
            ]
        }
    ]
}
```

You can get pronunciation assessment scores for:

- Full text
- Words
- Syllable groups
- Phonemes in [SAPI](/previous-versions/windows/desktop/ee431828(v=vs.85)#american-english-phoneme-table) or [IPA](https://en.wikipedia.org/wiki/IPA) format

## Supported features per locale

The following table summarizes which features that locales support. For more specifies, see the following sections. If the locales you require aren't listed in the following table for the supported feature, fill out this [intake form](https://aka.ms/speechpa/intake) for further assistance.

| Phoneme alphabet | IPA     | SAPI |
|:-----------------|:--------|:-----|
| Phoneme name     | `en-US` | `en-US`, `zh-CN` |
| Syllable group   | `en-US` | `en-US`|
| Spoken phoneme   | `en-US` | `en-US` |

### Syllable groups

Pronunciation assessment can provide syllable-level assessment results. A word is typically pronounced syllable by syllable rather than phoneme by phoneme. Grouping in syllables is more legible and aligned with speaking habits.

Pronunciation assessment supports syllable groups only in `en-US` with IPA and with SAPI.

The following table compares example phonemes with the corresponding syllables.

| Sample word | Phonemes | Syllables |
|:------------|:---------|:----------|
| technological | teknələdʒɪkl | tek·nə·lɑ·dʒɪkl |
| hello | hɛloʊ | hɛ·loʊ |
| luck | lʌk |lʌk |
| photosynthesis | foʊtəsɪnθəsɪs | foʊ·tə·sɪn·θə·sɪs |

To request syllable-level results along with phonemes, set the granularity [configuration parameter](#set-configuration-parameters) to `Phoneme`.

### Phoneme alphabet format

Pronunciation assessment supports phoneme name in `en-US` with IPA and in `en-US` and `zh-CN` with SAPI.

For locales that support phoneme name, the phoneme name is provided together with the score. Phoneme names help identify which phonemes were pronounced accurately or inaccurately. For other locales, you can only get the phoneme score.

The following table compares example SAPI phonemes with the corresponding IPA phonemes.

| Sample word | SAPI Phonemes | IPA phonemes |
|:------------|:--------------|:-------------|
| hello | h eh l ow | h ɛ l oʊ |
| luck | l ah k | l ʌ k |
| photosynthesis | f ow t ax s ih n th ax s ih s | f oʊ t ə s ɪ n θ ə s ɪ s |

To request IPA phonemes, set the phoneme alphabet to `IPA`. If you don't specify the alphabet, the phonemes are in SAPI format by default.

::: zone pivot="programming-language-csharp"

```csharp
pronunciationAssessmentConfig.PhonemeAlphabet = "IPA";
```

::: zone-end

::: zone pivot="programming-language-cpp"

```cpp
auto pronunciationAssessmentConfig = PronunciationAssessmentConfig::CreateFromJson("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\"}");
```

::: zone-end

::: zone pivot="programming-language-java"

```Java
PronunciationAssessmentConfig pronunciationAssessmentConfig = PronunciationAssessmentConfig.fromJson("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\"}");
```

::: zone-end

::: zone pivot="programming-language-python"

```Python
pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(json_string="{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\"}")
```

::: zone-end

::: zone pivot="programming-language-javascript"

```JavaScript
var pronunciationAssessmentConfig = SpeechSDK.PronunciationAssessmentConfig.fromJSON("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\"}");
```

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
pronunciationAssessmentConfig.phonemeAlphabet = @"IPA";
```

::: zone-end

::: zone pivot="programming-language-swift"

```swift
pronunciationAssessmentConfig?.phonemeAlphabet = "IPA"
```

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

### Assess spoken phonemes

With spoken phonemes, you can get confidence scores that indicate how likely the spoken phonemes matched the expected phonemes.

Pronunciation assessment supports spoken phonemes in `en-US` with IPA and with SAPI.

For example, to obtain the complete spoken sound for the word `Hello`, you can concatenate the first spoken phoneme for each expected phoneme with the highest confidence score. In the following assessment result, when you speak the word `hello`, the expected IPA phonemes are `h ɛ l oʊ`. However, the actual spoken phonemes are `h ə l oʊ`. You have five possible candidates for each expected phoneme in this example. The assessment result shows that the most likely spoken phoneme was `ə` instead of the expected phoneme `ɛ`. The expected phoneme `ɛ` only received a confidence score of 47. Other potential matches received confidence scores of 52, 17, and 2.

```json
{
    "Id": "bbb42ea51bdb46d19a1d685e635fe173",
    "RecognitionStatus": 0,
    "Offset": 7500000,
    "Duration": 13800000,
    "DisplayText": "Hello.",
    "NBest": [
        {
            "Confidence": 0.975003,
            "Lexical": "hello",
            "ITN": "hello",
            "MaskedITN": "hello",
            "Display": "Hello.",
            "PronunciationAssessment": {
                "AccuracyScore": 100,
                "FluencyScore": 100,
                "CompletenessScore": 100,
                "PronScore": 100
            },
            "Words": [
                {
                    "Word": "hello",
                    "Offset": 7500000,
                    "Duration": 13800000,
                    "PronunciationAssessment": {
                        "AccuracyScore": 99.0,
                        "ErrorType": "None"
                    },
                    "Syllables": [
                        {
                            "Syllable": "hɛ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 91.0
                            },
                            "Offset": 7500000,
                            "Duration": 4100000
                        },
                        {
                            "Syllable": "loʊ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0
                            },
                            "Offset": 11700000,
                            "Duration": 9600000
                        }
                    ],
                    "Phonemes": [
                        {
                            "Phoneme": "h",
                            "PronunciationAssessment": {
                                "AccuracyScore": 98.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "h",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 52.0
                                    },
                                    {
                                        "Phoneme": "ə",
                                        "Score": 35.0
                                    },
                                    {
                                        "Phoneme": "k",
                                        "Score": 23.0
                                    },
                                    {
                                        "Phoneme": "æ",
                                        "Score": 20.0
                                    }
                                ]
                            },
                            "Offset": 7500000,
                            "Duration": 3500000
                        },
                        {
                            "Phoneme": "ɛ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 47.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "ə",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "l",
                                        "Score": 52.0
                                    },
                                    {
                                        "Phoneme": "ɛ",
                                        "Score": 47.0
                                    },
                                    {
                                        "Phoneme": "h",
                                        "Score": 17.0
                                    },
                                    {
                                        "Phoneme": "æ",
                                        "Score": 2.0
                                    }
                                ]
                            },
                            "Offset": 11100000,
                            "Duration": 500000
                        },
                        {
                            "Phoneme": "l",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "l",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 46.0
                                    },
                                    {
                                        "Phoneme": "ə",
                                        "Score": 5.0
                                    },
                                    {
                                        "Phoneme": "ɛ",
                                        "Score": 3.0
                                    },
                                    {
                                        "Phoneme": "u",
                                        "Score": 1.0
                                    }
                                ]
                            },
                            "Offset": 11700000,
                            "Duration": 1100000
                        },
                        {
                            "Phoneme": "oʊ",
                            "PronunciationAssessment": {
                                "AccuracyScore": 100.0,
                                "NBestPhonemes": [
                                    {
                                        "Phoneme": "oʊ",
                                        "Score": 100.0
                                    },
                                    {
                                        "Phoneme": "d",
                                        "Score": 29.0
                                    },
                                    {
                                        "Phoneme": "t",
                                        "Score": 24.0
                                    },
                                    {
                                        "Phoneme": "n",
                                        "Score": 22.0
                                    },
                                    {
                                        "Phoneme": "l",
                                        "Score": 18.0
                                    }
                                ]
                            },
                            "Offset": 12900000,
                            "Duration": 8400000
                        }
                    ]
                }
            ]
        }
    ]
}
```

To indicate whether, and how many potential spoken phonemes to get confidence scores for, set the `NBestPhonemeCount` parameter to an integer value such as `5`.

::: zone pivot="programming-language-csharp"

```csharp
pronunciationAssessmentConfig.NBestPhonemeCount = 5;
```

::: zone-end

::: zone pivot="programming-language-cpp"

```cpp
auto pronunciationAssessmentConfig = PronunciationAssessmentConfig::CreateFromJson("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\",\"nBestPhonemeCount\":5}");
```

::: zone-end

::: zone pivot="programming-language-java"

```Java
PronunciationAssessmentConfig pronunciationAssessmentConfig = PronunciationAssessmentConfig.fromJson("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\",\"nBestPhonemeCount\":5}");
```

::: zone-end

::: zone pivot="programming-language-python"

```Python
pronunciation_assessment_config = speechsdk.PronunciationAssessmentConfig(json_string="{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\",\"nBestPhonemeCount\":5}")
```

::: zone-end

::: zone pivot="programming-language-javascript"

```JavaScript
var pronunciationAssessmentConfig = SpeechSDK.PronunciationAssessmentConfig.fromJSON("{\"referenceText\":\"good morning\",\"gradingSystem\":\"HundredMark\",\"granularity\":\"Phoneme\",\"phonemeAlphabet\":\"IPA\",\"nBestPhonemeCount\":5}");
```

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
pronunciationAssessmentConfig.nbestPhonemeCount = 5;
```

::: zone-end

::: zone pivot="programming-language-swift"

```swift
pronunciationAssessmentConfig?.nbestPhonemeCount = 5
```

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

## Pronunciation score calculation

Pronunciation scores are calculated by weighting accuracy, prosody, fluency, and completeness scores based on specific formulas for reading and speaking scenarios.

When sorting the scores of accuracy, prosody, fluency, and completeness from low to high (if each score is available) and representing the lowest score to the highest score as s0 to s3, the pronunciation score is calculated as follows:

For reading scenario:
  - With prosody score: PronScore = 0.4 * s0 + 0.2 * s1 + 0.2 * s2 + 0.2 * s3
  - Without prosody score: PronScore = 0.6 * s0 + 0.2 * s1 + 0.2 * s2

For the speaking scenario (the completeness score isn't applicable):
  - With prosody score: PronScore = 0.6 * s0 + 0.2 * s1 + 0.2 * s2
  - Without prosody score: PronScore = 0.6 * s0 + 0.4 * s1

This formula provides a weighted calculation based on the importance of each score, ensuring a comprehensive evaluation of pronunciation.

## Content assessment

> [!IMPORTANT]
> Content assessment (preview) is retired from Speech SDK versions 1.46.0 and later. As an alternative, you can use Azure OpenAI in Microsoft Foundry Models to get content assessment results as described in this section.

For some recognized speech, you might also want to get content assessment results for vocabulary, grammar, and topic relevance. You can use a chat model such as Azure OpenAI `gpt-4o` to get the content assessment results. For more information about using chat models, see [Azure OpenAI models](../../ai-foundry/foundry-models/concepts/models-sold-directly-by-azure.md) and the Azure AI Model Inference API [chat completions reference documentation](/rest/api/aifoundry/model-inference/get-chat-completions/get-chat-completions).

The user and system messages are used to set the context for the chat model. In the following example, the user message contains the essay to be assessed, and the system message provides instructions on how to evaluate the essay.


```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an English teacher and please help to grade a student's essay from vocabulary and grammar and topic relevance on how well the essay aligns with the title, and output format as: {\"vocabulary\": *.*(0-100), \"grammar\": *.*(0-100), \"topic\": *.*(0-100)}."
    },
    {
      "role": "user",
      "content": "Example1: this essay: \"sampleSentence1\" has vocabulary and grammar scores of ** and **, respectively. Example2: this essay: \"sampleSentence2\" has vocabulary and grammar scores of ** and **, respectively. Example3: this essay: \"sampleSentence3\" has vocabulary and grammar scores of ** and **, respectively. The essay for you to score is \"sendText\", and the title is \"topic\". The transcript is from speech recognition so that please first add punctuations when needed, remove duplicates and unnecessary un uh from oral speech, then find all the misuse of words and grammar errors in this essay, find advanced words and grammar usages, and finally give scores based on this information. Please only respond as this format {\"vocabulary\": *.*(0-100), \"grammar\": *.*(0-100)}, \"topic\": *.*(0-100)}. [THE TRANSCRIPT FROM SPEECH RECOGNITION IS REDACTED FOR BREVITY]"
    }
  ]
}
```


## Related content

- Learn about quality [benchmark](https://aka.ms/pronunciationassessment/techblog).
- Try [pronunciation assessment in the studio](pronunciation-assessment-tool.md).
- Check out an easy-to-deploy Pronunciation Assessment [demo](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/PronunciationAssessment/BrowserJS).
- Watch the [video demo](https://www.youtube.com/watch?v=NQi4mBiNNTE) of pronunciation assessment.
