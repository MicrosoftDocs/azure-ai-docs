---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 10/17/2024
ms.author: eur
ms.custom: devx-track-csharp
---

[!INCLUDE [Header](../../common/csharp.md)]

[!INCLUDE [Introduction](intro.md)]

## Create a speech configuration instance

To call the Speech service by using the Speech SDK, you need to create a [`SpeechConfig`](/dotnet/api/microsoft.cognitiveservices.speech.speechconfig) instance. This class includes information about your subscription, like your key and associated region, endpoint, host, or authorization token.

1. Create a Speech resource in the [Azure portal](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices). Get the Speech resource key and region.
1. Create a `SpeechConfig` instance by using the following code. Replace `YourSpeechKey` and `YourSpeechRegion` with your Speech resource key and region.

```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

class Program 
{
    async static Task Main(string[] args)
    {
        var speechConfig = SpeechConfig.FromSubscription("YourSpeechKey", "YourSpeechRegion");
    }
}
```

You can initialize `SpeechConfig` in a few other ways:

* Use an endpoint, and pass in a Speech service endpoint. A key or authorization token is optional.
* Use a host, and pass in a host address. A key or authorization token is optional.
* Use an authorization token with the associated region/location.

> [!NOTE]
> Regardless of whether you're performing speech recognition, speech synthesis, translation, or intent recognition, you always create a configuration.

## Recognize speech from a microphone

To recognize speech by using your device microphone, create an [`AudioConfig`](/dotnet/api/microsoft.cognitiveservices.speech.audio.audioconfig) instance by using the `FromDefaultMicrophoneInput()` method. Then initialize the [`SpeechRecognizer`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer) object by passing `speechConfig` and `audioConfig`.

```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

class Program 
{
    async static Task FromMic(SpeechConfig speechConfig)
    {
        using var audioConfig = AudioConfig.FromDefaultMicrophoneInput();
        using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

        Console.WriteLine("Speak into your microphone.");
        var speechRecognitionResult = await speechRecognizer.RecognizeOnceAsync();
        Console.WriteLine($"RECOGNIZED: Text={speechRecognitionResult.Text}");
    }

    async static Task Main(string[] args)
    {
        var speechConfig = SpeechConfig.FromSubscription("YourSpeechKey", "YourSpeechRegion");
        await FromMic(speechConfig);
    }
}
```

If you want to use a *specific* audio input device, you need to specify the device ID in `AudioConfig`. To learn how to get the device ID, see [Select an audio input device with the Speech SDK](../../../how-to-select-audio-input-devices.md).

## Recognize speech from a file

If you want to recognize speech from an audio file instead of a microphone, you still need to create an `AudioConfig` instance. However, you don't call `FromDefaultMicrophoneInput()`. You call `FromWavFileInput()` and pass the file path:

```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

class Program 
{
    async static Task FromFile(SpeechConfig speechConfig)
    {
        using var audioConfig = AudioConfig.FromWavFileInput("PathToFile.wav");
        using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

        var speechRecognitionResult = await speechRecognizer.RecognizeOnceAsync();
        Console.WriteLine($"RECOGNIZED: Text={speechRecognitionResult.Text}");
    }

    async static Task Main(string[] args)
    {
        var speechConfig = SpeechConfig.FromSubscription("YourSpeechKey", "YourSpeechRegion");
        await FromFile(speechConfig);
    }
}
```

## Recognize speech from an in-memory stream

For many use cases, it's likely that your audio data comes from Azure Blob Storage, or it's otherwise already in memory as a `byte[]` instance or a similar raw data structure. The following example uses [`PushAudioInputStream`](/dotnet/api/microsoft.cognitiveservices.speech.audio.pushaudioinputstream) to recognize speech, which is essentially an abstracted memory stream. The sample code does the following actions:

* Writes raw audio data to `PushAudioInputStream` by using the `Write()` function, which accepts a `byte[]` instance.
* Reads a *.wav* file by using `FileReader` for demonstration purposes. If you already have audio data in a `byte[]` instance, you can skip directly to writing the content to the input stream.
* The default format is 16-bit, 16-kHz mono pulse-code modulation (PCM) data. To customize the format, you can pass an [`AudioStreamFormat`](/dotnet/api/microsoft.cognitiveservices.speech.audio.audiostreamformat) object to `CreatePushStream()` by using the static function `AudioStreamFormat.GetWaveFormatPCM(sampleRate, (byte)bitRate, (byte)channels)`.

```csharp
using System;
using System.IO;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

class Program 
{
    async static Task FromStream(SpeechConfig speechConfig)
    {
        var reader = new BinaryReader(File.OpenRead("PathToFile.wav"));
        using var audioConfigStream = AudioInputStream.CreatePushStream();
        using var audioConfig = AudioConfig.FromStreamInput(audioConfigStream);
        using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);

        byte[] readBytes;
        do
        {
            readBytes = reader.ReadBytes(1024);
            audioConfigStream.Write(readBytes, readBytes.Length);
        } while (readBytes.Length > 0);

        var speechRecognitionResult = await speechRecognizer.RecognizeOnceAsync();
        Console.WriteLine($"RECOGNIZED: Text={speechRecognitionResult.Text}");
    }

    async static Task Main(string[] args)
    {
        var speechConfig = SpeechConfig.FromSubscription("YourSpeechKey", "YourSpeechRegion");
        await FromStream(speechConfig);
    }
}
```

Using a push stream as input assumes that the audio data is raw PCM and skips any headers. The API still works in certain cases if the header isn't skipped. For the best results, consider implementing logic to read off the headers so that `byte[]` begins at the *start of the audio data*.

## Handle errors

The previous examples only get the recognized text from the `speechRecognitionResult.Text` property. To handle errors and other responses, you need to write some code to handle the result. The following code evaluates the [`speechRecognitionResult.Reason`](/dotnet/api/microsoft.cognitiveservices.speech.recognitionresult.reason) property and:

* Prints the recognition result: `ResultReason.RecognizedSpeech`.
* If there's no recognition match, it informs the user: `ResultReason.NoMatch`.
* If an error is encountered, it prints the error message: `ResultReason.Canceled`.

```csharp
switch (speechRecognitionResult.Reason)
{
    case ResultReason.RecognizedSpeech:
        Console.WriteLine($"RECOGNIZED: Text={speechRecognitionResult.Text}");
        break;
    case ResultReason.NoMatch:
        Console.WriteLine($"NOMATCH: Speech could not be recognized.");
        break;
    case ResultReason.Canceled:
        var cancellation = CancellationDetails.FromResult(speechRecognitionResult);
        Console.WriteLine($"CANCELED: Reason={cancellation.Reason}");

        if (cancellation.Reason == CancellationReason.Error)
        {
            Console.WriteLine($"CANCELED: ErrorCode={cancellation.ErrorCode}");
            Console.WriteLine($"CANCELED: ErrorDetails={cancellation.ErrorDetails}");
            Console.WriteLine($"CANCELED: Did you set the speech resource key and region values?");
        }
        break;
}
```

## Use continuous recognition

The previous examples use single-shot recognition, which recognizes a single utterance. The end of a single utterance is determined by listening for silence at the end or until a maximum of 15 seconds of audio is processed.

In contrast, you use continuous recognition when you want to control when to stop recognizing. It requires you to subscribe to the `Recognizing`, `Recognized`, and `Canceled` events to get the recognition results. To stop recognition, you must call [`StopContinuousRecognitionAsync`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer.stopcontinuousrecognitionasync). Here's an example of how continuous recognition is performed on an audio input file.

Start by defining the input and initializing [`SpeechRecognizer`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer):

```csharp
using var audioConfig = AudioConfig.FromWavFileInput("YourAudioFile.wav");
using var speechRecognizer = new SpeechRecognizer(speechConfig, audioConfig);
```

Then create a `TaskCompletionSource<int>` instance to manage the state of speech recognition:

```csharp
var stopRecognition = new TaskCompletionSource<int>();
```

Next, subscribe to the events that `SpeechRecognizer` sends:

* [`Recognizing`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer.recognizing): Signal for events that contain intermediate recognition results.
* [`Recognized`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer.recognized): Signal for events that contain final recognition results, which indicate a successful recognition attempt.
* [`SessionStopped`](/dotnet/api/microsoft.cognitiveservices.speech.recognizer.sessionstopped): Signal for events that indicate the end of a recognition session (operation).
* [`Canceled`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer.canceled): Signal for events that contain canceled recognition results. These results indicate a recognition attempt that was canceled as a result of a direct cancelation request. Alternatively, they indicate a transport or protocol failure.

```csharp
speechRecognizer.Recognizing += (s, e) =>
{
    Console.WriteLine($"RECOGNIZING: Text={e.Result.Text}");
};

speechRecognizer.Recognized += (s, e) =>
{
    if (e.Result.Reason == ResultReason.RecognizedSpeech)
    {
        Console.WriteLine($"RECOGNIZED: Text={e.Result.Text}");
    }
    else if (e.Result.Reason == ResultReason.NoMatch)
    {
        Console.WriteLine($"NOMATCH: Speech could not be recognized.");
    }
};

speechRecognizer.Canceled += (s, e) =>
{
    Console.WriteLine($"CANCELED: Reason={e.Reason}");

    if (e.Reason == CancellationReason.Error)
    {
        Console.WriteLine($"CANCELED: ErrorCode={e.ErrorCode}");
        Console.WriteLine($"CANCELED: ErrorDetails={e.ErrorDetails}");
        Console.WriteLine($"CANCELED: Did you set the speech resource key and region values?");
    }

    stopRecognition.TrySetResult(0);
};

speechRecognizer.SessionStopped += (s, e) =>
{
    Console.WriteLine("\n    Session stopped event.");
    stopRecognition.TrySetResult(0);
};
```

With everything set up, call `StartContinuousRecognitionAsync` to start recognizing:

```csharp
await speechRecognizer.StartContinuousRecognitionAsync();

// Waits for completion. Use Task.WaitAny to keep the task rooted.
Task.WaitAny(new[] { stopRecognition.Task });

// Make the following call at some point to stop recognition:
// await speechRecognizer.StopContinuousRecognitionAsync();
```

## Change the source language

A common task for speech recognition is specifying the input (or source) language. The following example shows how to change the input language to Italian. In your code, find your [`SpeechConfig`](/dotnet/api/microsoft.cognitiveservices.speech.speechconfig) instance and add this line directly below it:

```csharp
speechConfig.SpeechRecognitionLanguage = "it-IT";
```

The [`SpeechRecognitionLanguage`](/dotnet/api/microsoft.cognitiveservices.speech.speechconfig.speechrecognitionlanguage) property expects a language-locale format string. For a list of supported locales, see [Language and voice support for the Speech service](../../../language-support.md?tabs=stt).

## Language identification

You can use language identification with speech to text recognition when you need to identify the language in an audio source and then transcribe it to text.

For a complete code sample, see [Language identification](../../../language-identification.md?pivots=programming-language-csharp).

## Use a custom endpoint

With [custom speech](../../../custom-speech-overview.md), you can upload your own data, test and train a custom model, compare accuracy between models, and deploy a model to a custom endpoint. The following example shows how to set a custom endpoint.

```csharp
var speechConfig = SpeechConfig.FromSubscription("YourSubscriptionKey", "YourServiceRegion");
speechConfig.EndpointId = "YourEndpointId";
var speechRecognizer = new SpeechRecognizer(speechConfig);
```

## Run and use a container

Speech containers provide websocket-based query endpoint APIs that are accessed through the Speech SDK and Speech CLI. By default, the Speech SDK and Speech CLI use the public Speech service. To use the container, you need to change the initialization method. Use a container host URL instead of key and region.

For more information about containers, see Host URLs in [Install and run Speech containers with Docker](../../../speech-container-howto.md#host-urls).

## Change how silence is handled

If a user speaks faster or slower than usual, the default behaviors for nonspeech silence in input audio might not result in what you expect. Common problems with silence handling include:

- Fast-speech that chains many sentences together into a single recognition result, instead of breaking sentences into individual results.
- Slow speech that separates parts of a single sentence into multiple results.
- A single-shot recognition that ends too quickly while waiting for speech to begin.

These problems can be addressed by setting one of two *timeout properties* on the `SpeechConfig` instance used to create a `SpeechRecognizer`:

- **Segmentation silence timeout** adjusts how much nonspeech audio is allowed within a phrase that's currently being spoken before that phrase is considered "done."
  - *Higher* values generally make results longer and allow longer pauses from the speaker within a phrase but make results take longer to arrive. They can also combine separate phrases into a single result when set too high.
  - *Lower* values generally make results shorter and ensure more prompt and frequent breaks between phrases, but can also cause single phrases to separate into multiple results when set too low.
  - This timeout can be set to integer values between 100 and 5000, in milliseconds, with 500 a typical default.
- **Initial silence timeout** adjusts how much nonspeech audio is allowed *before* a phrase before the recognition attempt ends in a "no match" result.
  - *Higher* values give speakers more time to react and start speaking, but can also result in slow responsiveness when nothing is spoken. 
  - *Lower* values ensure a prompt "no match" for faster user experience and more controlled audio handling, but might cut a speaker off too quickly when set too low.
  - Because continuous recognition generates many results, this value determines how often "no match" results arrive but doesn't otherwise affect the content of recognition results.
  - This timeout can be set to any non-negative integer value, in milliseconds, or set to 0 to disable it entirely. 5000 is a typical default for single-shot recognition while 15000 is a typical default for continuous recognition. 

Since there are tradeoffs when modifying these timeouts, you should only change the settings when you have a problem related to silence handling. Default values optimally handle most spoken audio and only uncommon scenarios should encounter problems.

**Example:** Users speaking a serial number like "ABC-123-4567" might pause between character groups long enough for the serial number to be broken into multiple results. In this case, try a higher value like 2000 milliseconds for the segmentation silence timeout:

```csharp
speechConfig.SetProperty(PropertyId.Speech_SegmentationSilenceTimeoutMs, "2000");
```

**Example:** A recorded presenter's speech might be fast enough that several sentences in a row get combined, with large recognition results only arriving once or twice per minute. In this case, set the segmentation silence timeout to a lower value like 300 ms:

```csharp
speechConfig.SetProperty(PropertyId.Speech_SegmentationSilenceTimeoutMs, "300");
```

**Example:** A single-shot recognition asking a speaker to find and read a serial number ends too quickly while the number is being found. In this case, try a longer initial silence timeout like 10,000 ms:

```csharp
speechConfig.SetProperty(PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, "10000");
```

## Semantic segmentation

Semantic segmentation is a speech recognition segmentation strategy that's designed to mitigate issues associated with [silence-based segmentation](#change-how-silence-is-handled): 
- Under-segmentation: When users speak for a long time without pauses, they can see a long sequence of text without breaks ("wall of text"), which severely degrades their readability experience. 
- Over-segmentation: When a user pauses for a short time, the silence detection mechanism can segment incorrectly. 

Instead of relying on silence timeouts, semantic segmentation segments and returns final results when it detects sentence-ending punctuation (such as '.' or '?'). This improves the user experience with higher-quality, semantically complete segments and prevents long intermediate results. 

To use semantic segmentation, you need to set the following property on the `SpeechConfig` instance used to create a `SpeechRecognizer`:

```csharp
speechConfig.SetProperty(PropertyId.Speech_SegmentationStrategy, "Semantic");
```

Some of the limitations of semantic segmentation are as follows:
- You need the Speech SDK version 1.41 or later to use semantic segmentation.
- Semantic segmentation is only intended for use in [continuous recognition](#use-continuous-recognition). This includes scenarios such as transcription and captioning. It shouldn't be used in the single recognition and dictation mode. 
- Semantic segmentation isn't available for all languages and locales. Currently, semantic segmentation is only available for English (en) locales such as en-US, en-GB, en-IN, and en-AU.
- Semantic segmentation doesn't yet support confidence scores and NBest lists. As such, we don't recommend semantic segmentation if you're using confidence scores or NBest lists.
