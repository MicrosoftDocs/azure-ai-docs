---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 9/12/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Create a keyword in Speech Studio

[!INCLUDE [Create a keyword](use-speech-studio.md)]

## Use a keyword model with the Speech SDK

First, load your keyword model file using the `FromFile()` static function, which returns a `KeywordRecognitionModel`. Use the path to the `.table` file you downloaded from Speech Studio. Additionally, you create an `AudioConfig` using the default microphone, then instantiate a new `KeywordRecognizer` using the audio configuration.

```csharp
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

var keywordModel = KeywordRecognitionModel.FromFile("your/path/to/Activate_device.table");
using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
using var keywordRecognizer = new KeywordRecognizer(audioConfig);
```
> [!IMPORTANT]
> If you prefer testing a keyword model directly with audio samples via the `AudioConfig.fromStreamInput()` method, make sure you use samples that have at least 1.5 seconds of silence before the first keyword. This is to provide an adequate time for the Keyword recognition engine to initialize and to get to the listening state prior to detecting the first keyword.

Next, running keyword recognition is done with one call to `RecognizeOnceAsync()` by passing your model object. This method starts a keyword recognition session that lasts until the keyword is recognized. Thus, you generally use this design pattern in multi-threaded applications, or in use cases where you might be waiting for a wake-word indefinitely.

```csharp
KeywordRecognitionResult result = await keywordRecognizer.RecognizeOnceAsync(keywordModel);
```

> [!NOTE]
> The example shown here uses local keyword recognition, since it does not require a `SpeechConfig` 
object for authentication context, and does not contact the back-end. However, you can run both keyword recognition and verification [utilizing a direct back-end connection](../../../tutorial-voice-enable-your-bot-speech-sdk.md#view-the-source-code-that-enables-keyword-detection).

### Continuous recognition

Other classes in the Speech SDK support continuous recognition (for both speech and intent recognition) with keyword recognition. The SDK allows you to use the same code you would normally use for continuous recognition, with the ability to reference a `.table` file for your keyword model.

For speech to text, follow the same design pattern shown in the [recognize speech guide](../../../how-to-recognize-speech.md?pivots=programming-language-csharp#continuous-recognition) to set up continuous recognition. Then, replace the call to `recognizer.StartContinuousRecognitionAsync()` with `recognizer.StartKeywordRecognitionAsync(KeywordRecognitionModel)`, and pass your `KeywordRecognitionModel` object. To stop continuous recognition with keyword recognition, use `recognizer.StopKeywordRecognitionAsync()` instead of `recognizer.StopContinuousRecognitionAsync()`.

Intent recognition uses an identical pattern with the [`StartKeywordRecognitionAsync`](/dotnet/api/microsoft.cognitiveservices.speech.intent.intentrecognizer.startkeywordrecognitionasync#Microsoft_CognitiveServices_Speech_Intent_IntentRecognizer_StartKeywordRecognitionAsync_Microsoft_CognitiveServices_Speech_KeywordRecognitionModel_) and [`StopKeywordRecognitionAsync`](/dotnet/api/microsoft.cognitiveservices.speech.intent.intentrecognizer.stopkeywordrecognitionasync#Microsoft_CognitiveServices_Speech_Intent_IntentRecognizer_StopKeywordRecognitionAsync) functions.
