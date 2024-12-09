---
title: Use pronunciation assessment
titleSuffix: Azure AI services
description: Learn about pronunciation assessment features that are currently publicly available. Choose the programming solution for your needs.
author: eric-urban
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
ms.date: 9/20/2024
ms.author: eur
zone_pivot_groups: programming-languages-ai-services
#Customer intent: As a developer, I want to implement pronunciation assessment on spoken language using a technology that works in my environment to gives feedback on accuracy and fluency.
---

# Use pronunciation assessment

In this article, you learn how to evaluate pronunciation with speech to text through the Speech SDK. Pronunciation assessment evaluates speech pronunciation and gives speakers feedback on the accuracy and fluency of spoken audio.

> [!NOTE]
> Pronunciation assessment uses a specific version of the speech-to-text model, different from the standard speech to text model, to ensure consistent and accurate pronunciation assessment.

## Use pronunciation assessment in streaming mode

Pronunciation assessment supports uninterrupted streaming mode. The recording time can be unlimited through the Speech SDK. As long as you don't stop recording, the evaluation process doesn't finish and you can pause and resume evaluation conveniently.

For information about availability of pronunciation assessment, see [supported languages](language-support.md?tabs=pronunciation-assessment) and [available regions](regions.md#speech-service).

As a baseline, usage of pronunciation assessment costs the same as speech to text for pay-as-you-go or commitment tier [pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services). If you [purchase a commitment tier](../commitment-tier.md) for speech to text, the spend for pronunciation assessment goes towards meeting the commitment. For more information, see [Pricing](./pronunciation-assessment-tool.md#pricing).

::: zone pivot="programming-language-csharp"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/speech_recognition_samples.cs#:~:text=PronunciationAssessmentWithStream).

::: zone-end

::: zone pivot="programming-language-cpp"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/cpp/windows/console/samples/speech_recognition_samples.cpp#:~:text=PronunciationAssessmentWithStream).

::: zone-end

::: zone pivot="programming-language-java"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/java/android/sdkdemo/app/src/main/java/com/microsoft/cognitiveservices/speech/samples/sdkdemo/MainActivity.java#L548).

::: zone-end

::: zone pivot="programming-language-python"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/python/console/speech_sample.py#L915).

::: zone-end

::: zone pivot="programming-language-javascript"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/node/pronunciationAssessment.js).

::: zone-end

::: zone pivot="programming-language-objectivec"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m#L831).

::: zone-end

::: zone pivot="programming-language-swift"

For how to use Pronunciation Assessment in streaming mode in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/swift/ios/speech-samples/speech-samples/ViewController.swift#L191).

::: zone-end

::: zone pivot="programming-language-go"

::: zone-end

### Continuous recognition

::: zone pivot="programming-language-csharp"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/csharp/sharedcontent/console/speech_recognition_samples.cs) under the function `PronunciationAssessmentContinuousWithFile`.

::: zone-end

::: zone pivot="programming-language-cpp"

If your audio file exceeds 30 seconds, use continuous mode for processing.

::: zone-end

::: zone pivot="programming-language-java"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/java/jre/console/src/com/microsoft/cognitiveservices/speech/samples/console/SpeechRecognitionSamples.java) under the function `pronunciationAssessmentContinuousWithFile`.

::: zone-end

::: zone pivot="programming-language-python"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/261160e26dfcae4c3aee93308d58d74e36739b6f/samples/python/console/speech_sample.py) under the function `pronunciation_assessment_continuous_from_file`.

::: zone-end

::: zone pivot="programming-language-javascript"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/261160e26dfcae4c3aee93308d58d74e36739b6f/samples/js/node/pronunciationAssessmentContinue.js).

::: zone-end

::: zone pivot="programming-language-objectivec"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/objective-c/ios/speech-samples/speech-samples/ViewController.m) under the function `pronunciationAssessFromFile`.

::: zone-end

::: zone pivot="programming-language-swift"

If your audio file exceeds 30 seconds, use continuous mode for processing. The sample code for continuous mode can be found on [GitHub](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/swift/ios/speech-samples/speech-samples/ViewController.swift) under the function `continuousPronunciationAssessment`.

::: zone-end

::: zone pivot="programming-language-go"

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

You must create a `PronunciationAssessmentConfig` object. You can set `EnableProsodyAssessment` and `EnableContentAssessmentWithTopic` to enable prosody and content assessment. For more information, see [configuration methods](#configuration-methods).

::: zone pivot="programming-language-csharp"

```csharp
var pronunciationAssessmentConfig = new PronunciationAssessmentConfig( 
    referenceText: "", 
    gradingSystem: GradingSystem.HundredMark,  
    granularity: Granularity.Phoneme,  
    enableMiscue: false); 
pronunciationAssessmentConfig.EnableProsodyAssessment(); 
pronunciationAssessmentConfig.EnableContentAssessmentWithTopic("greeting"); 
```

::: zone-end  

::: zone pivot="programming-language-cpp"

```cpp
auto pronunciationConfig = PronunciationAssessmentConfig::Create("", PronunciationAssessmentGradingSystem::HundredMark, PronunciationAssessmentGranularity::Phoneme, false); 
pronunciationConfig->EnableProsodyAssessment(); 
pronunciationConfig->EnableContentAssessmentWithTopic("greeting"); 
```

::: zone-end

::: zone pivot="programming-language-java"

```Java
PronunciationAssessmentConfig pronunciationConfig = new PronunciationAssessmentConfig("", 
    PronunciationAssessmentGradingSystem.HundredMark, PronunciationAssessmentGranularity.Phoneme, false); 
pronunciationConfig.enableProsodyAssessment(); 
pronunciationConfig.enableContentAssessmentWithTopic("greeting");
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
pronunciation_config.enable_content_assessment_with_topic("greeting")
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
pronunciationAssessmentConfig.enableContentAssessmentWithTopic("greeting");  
```

::: zone-end

::: zone pivot="programming-language-objectivec"

```ObjectiveC
SPXPronunciationAssessmentConfiguration *pronunicationConfig = 
[[SPXPronunciationAssessmentConfiguration alloc] init:@"" gradingSystem:SPXPronunciationAssessmentGradingSystem_HundredMark granularity:SPXPronunciationAssessmentGranularity_Phoneme enableMiscue:false]; 
[pronunicationConfig enableProsodyAssessment]; 
[pronunicationConfig enableContentAssessmentWithTopic:@"greeting"]; 
```

::: zone-end

::: zone pivot="programming-language-swift"

```swift
let pronAssessmentConfig = try! SPXPronunciationAssessmentConfiguration("", 
    gradingSystem: .hundredMark, 
    granularity: .phoneme, 
    enableMiscue: false) 
pronAssessmentConfig.enableProsodyAssessment() 
pronAssessmentConfig.enableContentAssessment(withTopic: "greeting")
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
> Content and prosody assessments are only available in the [en-US](./language-support.md?tabs=pronunciation-assessment) locale.
> 
> To explore the content and prosody assessments, upgrade to the SDK version 1.35.0 or later.
>
> There is no length limit for the topic parameter.

| Method | Description |
|-----------|-------------|
| `EnableProsodyAssessment` | Enables prosody assessment for your pronunciation evaluation. This feature assesses aspects like stress, intonation, speaking speed, and rhythm. This feature provides insights into the naturalness and expressiveness of your speech.<br/><br/>Enabling prosody assessment is optional. If this method is called, the `ProsodyScore` result value is returned. |
| `EnableContentAssessmentWithTopic` | Enables content assessment. A content assessment is part of the [unscripted assessment](#unscripted-assessment-results) for the speaking language learning scenario. By providing a description, you can enhance the assessment's understanding of the specific topic being spoken about. For example, in C# call `pronunciationAssessmentConfig.EnableContentAssessmentWithTopic("greeting");`. You can replace 'greeting' with your desired text to describe a topic. The description has no length limit and currently only supports the `en-US` locale. |

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

To learn how to specify the learning language for pronunciation assessment in your own application, see [sample code](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/samples/js/node/pronunciationAssessmentContinue.js#LL37C4-L37C52).

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

`VocabularyScore`, `GrammarScore`, and `TopicScore` parameters roll up to the combined content assessment.

> [!NOTE]
> Content and prosody assessments are only available in the [en-US](./language-support.md?tabs=pronunciation-assessment) locale.

| Response parameter | Description | Granularity |
|:-------------------|:------------|:------------|
| `AccuracyScore`    | Pronunciation accuracy of the speech. Accuracy indicates how closely the phonemes match a native speaker's pronunciation. Syllable, word, and full text accuracy scores are aggregated from phoneme-level accuracy score, and refined with assessment objectives. | Phoneme level，<br>Syllable level (en-US only)，<br>Word level，<br>Full Text level |
| `FluencyScore`     | Fluency of the given speech. Fluency indicates how closely the speech matches a native speaker's use of silent breaks between words. | Full Text level |
| `ProsodyScore`     | Prosody of the given speech. Prosody indicates how natural the given speech is, including stress, intonation, speaking speed, and rhythm. | Full Text level |
| `VocabularyScore`  | Proficiency in lexical usage. It evaluates the speaker's effective usage of words and their appropriateness within the given context to express ideas accurately, and the level of lexical complexity. | Full Text level |
| `GrammarScore`     | Correctness in using grammar and variety of sentence patterns. Lexical accuracy, grammatical accuracy, and diversity of sentence structures jointly elevate grammatical errors. | Full Text level|
| `TopicScore`       | Level of understanding and engagement with the topic, which provides insights into the speaker’s ability to express their thoughts and ideas effectively and the ability to engage with the topic. | Full Text level|
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

## Related content

- Learn about quality [benchmark](https://aka.ms/pronunciationassessment/techblog).
- Try [pronunciation assessment in the studio](pronunciation-assessment-tool.md).
- Check out an easy-to-deploy Pronunciation Assessment [demo](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/PronunciationAssessment/BrowserJS).
- Watch the [video demo](https://www.youtube.com/watch?v=NQi4mBiNNTE) of pronunciation assessment.
