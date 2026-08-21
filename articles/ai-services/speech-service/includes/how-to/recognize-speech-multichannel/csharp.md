---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/csharp.md)]

In this guide, you use the Speech SDK for C# to transcribe a stereo audio source and read a separate speech-to-text result for each channel.

## Prerequisites

- The [Speech SDK for C#](../../../quickstarts/setup-platform.md?pivots=programming-language-csharp) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create a [`SpeechConfig`](/dotnet/api/microsoft.cognitiveservices.speech.speechconfig) instance and
set the `Speech_EnableMultiChannelProcessing` property to `true`. Replace `YourSpeechEndpoint` and
`YourSpeechKey` with your Speech resource endpoint and key.

```csharp
using System;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;
using Microsoft.CognitiveServices.Speech.Transcription;

var speechConfig = SpeechConfig.FromEndpoint(
    new Uri("YourSpeechEndpoint"), "YourSpeechKey");
speechConfig.SpeechRecognitionLanguage = "en-US";

// Enable per-channel transcription of up to two channels.
speechConfig.SetProperty(PropertyId.Speech_EnableMultiChannelProcessing, "true");
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an [`AudioConfig`](/dotnet/api/microsoft.cognitiveservices.speech.audio.audioconfig) instance from the file name:

```csharp
using var audioConfig = AudioConfig.FromWavFileInput("stereo.wav");
```

For a real-time source, create the `AudioConfig` instance from a push or pull stream. When you create the stream format, set the channel count to `2`:

```csharp
// Match the format of your stereo source: sample rate, bits per sample, and 2 channels.
var streamFormat = AudioStreamFormat.GetWaveFormatPCM(16000, 16, 2);
var pushStream = AudioInputStream.CreatePushStream(streamFormat);
using var audioConfig = AudioConfig.FromStreamInput(pushStream);

// Write raw PCM audio (without the WAV header) to pushStream as it becomes available,
// and call pushStream.Close() when the source ends.
```

## Recognize and read per-channel results

Create a [`SpeechRecognizer`](/dotnet/api/microsoft.cognitiveservices.speech.speechrecognizer) instance and use continuous recognition. Each final result includes the source channel in the `Channel` property. Multichannel transcription supports continuous recognition only; single-shot recognition (`RecognizeOnceAsync`) isn't supported.

```csharp
using var recognizer = new SpeechRecognizer(speechConfig, audioConfig);
var stopRecognition = new TaskCompletionSource<int>();

recognizer.Recognized += (s, e) =>
{
    if (e.Result.Reason == ResultReason.RecognizedSpeech)
    {
        Console.WriteLine($"RECOGNIZED (channel {e.Result.Channel}): {e.Result.Text}");
    }
};

recognizer.Canceled += (s, e) => stopRecognition.TrySetResult(0);
recognizer.SessionStopped += (s, e) => stopRecognition.TrySetResult(0);

await recognizer.StartContinuousRecognitionAsync();
Task.WaitAny(new[] { stopRecognition.Task });
await recognizer.StopContinuousRecognitionAsync();
```

The `Channel` property identifies the zero-based channel that produced the result, so you can keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use a [`ConversationTranscriber`](/dotnet/api/microsoft.cognitiveservices.speech.transcription.conversationtranscriber) instead of a `SpeechRecognizer`. The transcriber reports final results on the `Transcribed` event, and each result includes both the channel and the speaker ID.

```csharp
using var conversationTranscriber = new ConversationTranscriber(speechConfig, audioConfig);
var stopTranscription = new TaskCompletionSource<int>();

conversationTranscriber.Transcribed += (s, e) =>
{
    if (e.Result.Reason == ResultReason.RecognizedSpeech)
    {
        Console.WriteLine($"TRANSCRIBED (channel {e.Result.Channel}, speaker {e.Result.SpeakerId}): {e.Result.Text}");
    }
};

conversationTranscriber.Canceled += (s, e) => stopTranscription.TrySetResult(0);
conversationTranscriber.SessionStopped += (s, e) => stopTranscription.TrySetResult(0);

await conversationTranscriber.StartTranscribingAsync();
Task.WaitAny(new[] { stopTranscription.Task });
await conversationTranscriber.StopTranscribingAsync();
```
