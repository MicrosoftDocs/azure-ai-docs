---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/17/2024
ms.custom: devx-track-java
ms.author: eur
---

[!INCLUDE [Header](../../common/java.md)]

[!INCLUDE [Introduction](intro.md)]

## Create a speech configuration instance

To call the Speech service by using the Speech SDK, you need to create a [SpeechConfig](/java/api/com.microsoft.cognitiveservices.speech.speechconfig) instance. This class includes information about your subscription, like your key and associated region, endpoint, host, or authorization token.

1. Create a Speech resource in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices). Get the Speech resource key and region.
1. Create a `SpeechConfig` instance by using your Speech key and region.

```java
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class Program {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        SpeechConfig speechConfig = SpeechConfig.fromSubscription("<paste-your-speech-key>", "<paste-your-region>");
    }
}
```

You can initialize `SpeechConfig` in a few other ways:

* Use an endpoint, and pass in a Speech service endpoint. A key or authorization token is optional.
* Use a host, and pass in a host address. A key or authorization token is optional.
* Use an authorization token with the associated region/location.

> [!NOTE]
> Regardless of whether you're performing speech recognition, speech synthesis, translation, or intent recognition, you'll always create a configuration.

## Recognize speech from a microphone

To recognize speech by using your device microphone, create an `AudioConfig` instance by using the `fromDefaultMicrophoneInput()` method. Then initialize the [`SpeechRecognizer`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer) object by passing `audioConfig` and `config`.

```java
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class Program {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        SpeechConfig speechConfig = SpeechConfig.fromSubscription("<paste-your-speech-key>", "<paste-your-region>");
        fromMic(speechConfig);
    }

    public static void fromMic(SpeechConfig speechConfig) throws InterruptedException, ExecutionException {
        AudioConfig audioConfig = AudioConfig.fromDefaultMicrophoneInput();
        SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

        System.out.println("Speak into your microphone.");
        Future<SpeechRecognitionResult> task = speechRecognizer.recognizeOnceAsync();
        SpeechRecognitionResult speechRecognitionResult = task.get();
        System.out.println("RECOGNIZED: Text=" + speechRecognitionResult.getText());
    }
}
```

If you want to use a *specific* audio input device, you need to specify the device ID in `AudioConfig`. To learn how to get the device ID, see [Select an audio input device with the Speech SDK](../../../how-to-select-audio-input-devices.md).

## Recognize speech from a file

If you want to recognize speech from an audio file instead of using a microphone, you still need to create an `AudioConfig` instance. However, you don't call `FromDefaultMicrophoneInput()`. You call `fromWavFileInput()` and pass the file path:

```java
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class Program {
    public static void main(String[] args) throws InterruptedException, ExecutionException {
        SpeechConfig speechConfig = SpeechConfig.fromSubscription("<paste-your-speech-key>", "<paste-your-region>");
        fromFile(speechConfig);
    }

    public static void fromFile(SpeechConfig speechConfig) throws InterruptedException, ExecutionException {
        AudioConfig audioConfig = AudioConfig.fromWavFileInput("YourAudioFile.wav");
        SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
        
        Future<SpeechRecognitionResult> task = speechRecognizer.recognizeOnceAsync();
        SpeechRecognitionResult speechRecognitionResult = task.get();
        System.out.println("RECOGNIZED: Text=" + speechRecognitionResult.getText());
    }
}
```

## Handle errors

The previous examples only get the recognized text by using `speechRecognitionResult.getText()`. To handle errors and other responses, you need to write some code to handle the result. The following example evaluates [`speechRecognitionResult.getReason()`](/java/api/com.microsoft.cognitiveservices.speech.recognitionresult.getreason) and:

* Prints the recognition result: `ResultReason.RecognizedSpeech`.
* If there's no recognition match, it informs the user: `ResultReason.NoMatch`.
* If an error is encountered, it prints the error message: `ResultReason.Canceled`.

```java
switch (speechRecognitionResult.getReason()) {
    case ResultReason.RecognizedSpeech:
        System.out.println("We recognized: " + speechRecognitionResult.getText());
        exitCode = 0;
        break;
    case ResultReason.NoMatch:
        System.out.println("NOMATCH: Speech could not be recognized.");
        break;
    case ResultReason.Canceled: {
            CancellationDetails cancellation = CancellationDetails.fromResult(speechRecognitionResult);
            System.out.println("CANCELED: Reason=" + cancellation.getReason());

            if (cancellation.getReason() == CancellationReason.Error) {
                System.out.println("CANCELED: ErrorCode=" + cancellation.getErrorCode());
                System.out.println("CANCELED: ErrorDetails=" + cancellation.getErrorDetails());
                System.out.println("CANCELED: Did you set the speech resource key and region values?");
            }
        }
        break;
}
```

## Use continuous recognition

The previous examples use single-shot recognition, which recognizes a single utterance. The end of a single utterance is determined by listening for silence at the end or until a maximum of 15 seconds of audio is processed.

In contrast, you use continuous recognition when you want to control when to stop recognizing. It requires you to subscribe to the `recognizing`, `recognized`, and `canceled` events to get the recognition results. To stop recognition, you must call [`stopContinuousRecognitionAsync`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer.stopcontinuousrecognitionasync). Here's an example of how you can perform continuous recognition on an audio input file.

Start by defining the input and initializing [`SpeechRecognizer`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer):

```java
AudioConfig audioConfig = AudioConfig.fromWavFileInput("YourAudioFile.wav");
SpeechRecognizer speechRecognizer = new SpeechRecognizer(config, audioConfig);
```

Next, create a variable to manage the state of speech recognition. Declare a `Semaphore` instance at the class scope:

```java
private static Semaphore stopTranslationWithFileSemaphore;
```

Next, subscribe to the events that [`SpeechRecognizer`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer) sends:

* [`recognizing`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer.recognizing): Signal for events that contain intermediate recognition results.
* [`recognized`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer.recognized): Signal for events that contain final recognition results, which indicate a successful recognition attempt.
* [`sessionStopped`](/java/api/com.microsoft.cognitiveservices.speech.recognizer.sessionstopped): Signal for events that indicate the end of a recognition session (operation).
* [`canceled`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer.canceled): Signal for events that contain canceled recognition results. These results indicate a recognition attempt that was canceled as a result of a direct cancelation request. Alternatively, they indicate a transport or protocol failure.

```java
// First initialize the semaphore.
stopTranslationWithFileSemaphore = new Semaphore(0);

speechRecognizer.recognizing.addEventListener((s, e) -> {
    System.out.println("RECOGNIZING: Text=" + e.getResult().getText());
});

speechRecognizer.recognized.addEventListener((s, e) -> {
    if (e.getResult().getReason() == ResultReason.RecognizedSpeech) {
        System.out.println("RECOGNIZED: Text=" + e.getResult().getText());
    }
    else if (e.getResult().getReason() == ResultReason.NoMatch) {
        System.out.println("NOMATCH: Speech could not be recognized.");
    }
});

speechRecognizer.canceled.addEventListener((s, e) -> {
    System.out.println("CANCELED: Reason=" + e.getReason());

    if (e.getReason() == CancellationReason.Error) {
        System.out.println("CANCELED: ErrorCode=" + e.getErrorCode());
        System.out.println("CANCELED: ErrorDetails=" + e.getErrorDetails());
        System.out.println("CANCELED: Did you set the speech resource key and region values?");
    }

    stopTranslationWithFileSemaphore.release();
});

speechRecognizer.sessionStopped.addEventListener((s, e) -> {
    System.out.println("\n    Session stopped event.");
    stopTranslationWithFileSemaphore.release();
});
```

With everything set up, call [`startContinuousRecognitionAsync`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer.startcontinuousrecognitionasync) to start recognizing:

```java
// Starts continuous recognition. Uses StopContinuousRecognitionAsync() to stop recognition.
speechRecognizer.startContinuousRecognitionAsync().get();

// Waits for completion.
stopTranslationWithFileSemaphore.acquire();

// Stops recognition.
speechRecognizer.stopContinuousRecognitionAsync().get();
```

## Change the source language

A common task for speech recognition is specifying the input (or source) language. The following example shows how to change the input language to French. In your code, find your [`SpeechConfig`](/java/api/com.microsoft.cognitiveservices.speech.speechconfig) instance, and add this line directly below it:

```java
config.setSpeechRecognitionLanguage("fr-FR");
```

[`setSpeechRecognitionLanguage`](/java/api/com.microsoft.cognitiveservices.speech.speechconfig.setspeechrecognitionlanguage) is a parameter that takes a string as an argument. Refer to the [list of supported speech to text locales](../../../language-support.md?tabs=stt).

## Language identification

You can use language identification with speech to text recognition when you need to identify the language in an audio source and then transcribe it to text.

For a complete code sample, see [Language identification](../../../language-identification.md?pivots=programming-language-java).

## Use a custom endpoint

With [custom speech](../../../custom-speech-overview.md), you can upload your own data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint. The following example shows how to set a custom endpoint:

```java
SpeechConfig speechConfig = SpeechConfig.FromSubscription("YourSpeechKey", "YourServiceRegion");
speechConfig.setEndpointId("YourEndpointId");
SpeechRecognizer speechRecognizer = new SpeechRecognizer(speechConfig);
```

## Run and use a container

Speech containers provide websocket-based query endpoint APIs that are accessed through the Speech SDK and Speech CLI. By default, the Speech SDK and Speech CLI use the public Speech service. To use the container, you need to change the initialization method. Use a container host URL instead of key and region.

For more information about containers, see Host URLs in [Install and run Speech containers with Docker](../../../speech-container-howto.md#host-urls).

## Semantic segmentation

Semantic segmentation is a speech recognition segmentation strategy that's designed to mitigate issues associated with silence-based segmentation: 
- Under-segmentation: When users speak for a long time without pauses, they can see a long sequence of text without breaks ("wall of text"), which severely degrades their readability experience. 
- Over-segmentation: When a user pauses for a short time, the silence detection mechanism can segment incorrectly. 

Instead of relying on silence timeouts, semantic segmentation segments and returns final results when it detects sentence-ending punctuation (such as '.' or '?'). This improves the user experience with higher-quality, semantically complete segments and prevents long intermediate results. 

To use semantic segmentation, you need to set the following property on the `SpeechConfig` instance used to create a `SpeechRecognizer`:

```java
speechConfig.SetProperty(PropertyId.Speech_SegmentationStrategy, "Semantic");
```

Some of the limitations of semantic segmentation are as follows:
- You need the Speech SDK version 1.41 or later to use semantic segmentation.
- Semantic segmentation is only intended for use in [continuous recognition](#use-continuous-recognition). This includes scenarios such as transcription and captioning. It shouldn't be used in the single recognition and dictation mode. 
- Semantic segmentation isn't available for all languages and locales. Currently, semantic segmentation is only available for English (en) locales such as en-US, en-GB, en-IN, and en-AU.
- Semantic segmentation doesn't yet support confidence scores and NBest lists. As such, we don't recommend semantic segmentation if you're using confidence scores or NBest lists.
