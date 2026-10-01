---
title: Use MAI-Transcribe-2-Streaming with Azure Speech SDK - Speech Service
titleSuffix: Foundry Tools
description: Learn how to transcribe streaming audio with MAI-Transcribe-2-Streaming by using Azure Speech SDK.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 09/30/2026
ms.custom: references_regions
ai-usage: ai-assisted

# Customer intent: As a developer, I want to transcribe live audio with MAI-Transcribe-2-Streaming by using Azure Speech SDK.
---

# Use MAI-Transcribe-2-Streaming with Azure Speech SDK

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Transcribe-2-Streaming is a low-latency, speech-to-text model for real-time transcription. Send audio as a continuous stream and receive incremental transcripts while the speaker talks. Intermediate results update the current transcription, and final results confirm each segment.

The model supports live audio workloads such as call centers, voice assistants, meeting and lecture captioning, voice-driven interfaces, and real-time note taking.

For the OpenAI Realtime-compatible WebSocket integration, see [Use MAI-Transcribe-2-Streaming with the Realtime API](mai-transcribe-2-streaming-realtime.md).

## Prerequisites

> [!div class="checklist"]
> - Azure Speech SDK v1.52.0.
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - Create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) or Speech Resource in one of the supported regions by using the Azure portal.
> - After you deploy your resource, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).

## Supported models

- `MAI-Transcribe-2-Streaming`

## Availability and regions

You can access MAI-Transcribe-2-Streaming globally. Azure serves the model from the following regions, and routes requests to them:

| Region | Region identifier | Availability |
| --- | --- | --- |
| Sweden Central | `swedencentral` | Available |
| Central US | `centralus` | Available |
| East US 2 | `eastus2` | Coming soon |
| Southeast Asia | `southeastasia` | Available |

## Pricing

See [Speech service pricing](https://azure.microsoft.com/pricing/details/speech/).

## Python example

```python
import os
import threading

import azure.cognitiveservices.speech as speechsdk


region = os.environ["SPEECH_REGION"]
endpoint = f"wss://{region}.stt.speech.microsoft.com/speech/universal/v2"
speech_config = speechsdk.SpeechConfig(subscription=os.environ["SPEECH_KEY"], endpoint=endpoint)
speech_config.model = "MAI-Transcribe-2-Streaming"
speech_config.speech_recognition_language = "en-US"

audio_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=1)
audio_stream = speechsdk.audio.PushAudioInputStream(stream_format=audio_format)
audio_config = speechsdk.audio.AudioConfig(stream=audio_stream)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
recognition_done = threading.Event()
recognition_errors = []


def on_recognized(event):
    result = event.result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Final:", result.text)
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized for this segment.")


def on_canceled(event):
    details = event.cancellation_details
    if details.reason == speechsdk.CancellationReason.Error:
        recognition_errors.append(f"{details.code}: {details.error_details}")
    recognition_done.set()


recognizer.recognizing.connect(lambda event: print("Intermediate:", event.result.text))
recognizer.recognized.connect(on_recognized)
recognizer.canceled.connect(on_canceled)
recognizer.session_started.connect(lambda event: print("Session ID:", event.session_id))
recognizer.session_stopped.connect(lambda event: recognition_done.set())

recognition_started = False
input_closed = False
try:
    recognizer.start_continuous_recognition_async().get()
    recognition_started = True

    # Adapt this block to your application's audio source.
    # Write raw audio matching audio_format, and close the push stream when input ends.
    # Each full chunk below contains 100 ms of audio.
    with open("audio.pcm", "rb") as pcm_input:
        bytes_per_second = 16000 * 2
        while not recognition_done.is_set():
            audio_data = pcm_input.read(3200)
            if not audio_data:
                break
            audio_stream.write(audio_data)
            if recognition_done.wait(timeout=len(audio_data) / bytes_per_second):
                break

    audio_stream.close()
    input_closed = True
    # The 30-second wait is an application-level drain timeout, not a service latency guarantee.
    # Choose a suitable timeout for your use.
    if not recognition_done.wait(timeout=30):
        raise TimeoutError("Timed out waiting for recognition to finish.")
    if recognition_errors:
        raise RuntimeError(recognition_errors[0])
finally:
    if not input_closed:
        audio_stream.close()
    if recognition_started:
        recognizer.stop_continuous_recognition_async().get()
```

## Java example

```java
import com.microsoft.cognitiveservices.speech.CancellationReason;
import com.microsoft.cognitiveservices.speech.ResultReason;
import com.microsoft.cognitiveservices.speech.SpeechConfig;
import com.microsoft.cognitiveservices.speech.SpeechRecognitionResult;
import com.microsoft.cognitiveservices.speech.SpeechRecognizer;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;
import com.microsoft.cognitiveservices.speech.audio.AudioInputStream;
import com.microsoft.cognitiveservices.speech.audio.AudioStreamFormat;
import com.microsoft.cognitiveservices.speech.audio.PushAudioInputStream;
import java.io.FileInputStream;
import java.net.URI;
import java.util.Arrays;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;

public final class MaiStreamingRecognition {
    public static void main(String[] args) throws Exception {
        String key = requiredEnvironment("SPEECH_KEY");
        String region = requiredEnvironment("SPEECH_REGION");
        URI endpoint = new URI("wss://" + region + ".stt.speech.microsoft.com/speech/universal/v2");
        AudioStreamFormat audioFormat = AudioStreamFormat.getWaveFormatPCM(16000, (short) 16, (short) 1);

        try (SpeechConfig speechConfig = SpeechConfig.fromEndpoint(endpoint, key);
             PushAudioInputStream audioStream = AudioInputStream.createPushStream(audioFormat);
             AudioConfig audioConfig = AudioConfig.fromStreamInput(audioStream)) {
            speechConfig.setModel("MAI-Transcribe-2-Streaming");
            speechConfig.setSpeechRecognitionLanguage("en-US");

            try (SpeechRecognizer recognizer = new SpeechRecognizer(speechConfig, audioConfig)) {
                CompletableFuture<Void> recognitionDone = new CompletableFuture<>();

                recognizer.recognizing.addEventListener((sender, event) ->
                    System.out.println("Intermediate: " + event.getResult().getText()));
                recognizer.recognized.addEventListener((sender, event) -> {
                    SpeechRecognitionResult result = event.getResult();
                    if (result.getReason() == ResultReason.RecognizedSpeech) {
                        System.out.println("Final: " + result.getText());
                    } else if (result.getReason() == ResultReason.NoMatch) {
                        System.out.println("No speech recognized.");
                    }
                });
                recognizer.canceled.addEventListener((sender, event) -> {
                    if (event.getReason() == CancellationReason.Error) {
                        IllegalStateException error = new IllegalStateException(
                            event.getErrorCode() + ": " + event.getErrorDetails());
                        recognitionDone.completeExceptionally(error);
                    } else {
                        recognitionDone.complete(null);
                    }
                });
                recognizer.sessionStarted.addEventListener((sender, event) ->
                    System.out.println("Session ID: " + event.getSessionId()));
                recognizer.sessionStopped.addEventListener((sender, event) -> recognitionDone.complete(null));

                recognizer.startContinuousRecognitionAsync().get();
                // Adapt this block to your application's audio source.
                // Write raw audio matching audioFormat, and close the push stream when input ends.
                // Each full chunk below contains 100 ms of audio.
                try (FileInputStream pcmInput = new FileInputStream("audio.pcm")) {
                    final int bytesPerSecond = 16000 * 2;
                    byte[] audioBuffer = new byte[3200];
                    while (!recognitionDone.isDone()) {
                        int bytesRead = pcmInput.read(audioBuffer);
                        if (bytesRead == -1) {
                            break;
                        }
                        if (bytesRead > 0) {
                            audioStream.write(Arrays.copyOf(audioBuffer, bytesRead));
                            long delayNanos = TimeUnit.SECONDS.toNanos(1) * bytesRead / bytesPerSecond;
                            TimeUnit.NANOSECONDS.sleep(delayNanos);
                        }
                    }
                    audioStream.close();
                    // The 30-second wait is an application-level drain timeout, not a service latency guarantee.
                    // Choose a suitable timeout for your use.
                    recognitionDone.get(30, TimeUnit.SECONDS);
                } finally {
                    recognizer.stopContinuousRecognitionAsync().get();
                }
            }
        } finally {
            audioFormat.close();
        }
    }

    private static String requiredEnvironment(String name) {
        String value = System.getenv(name);
        if (value == null || value.trim().isEmpty()) {
            throw new IllegalArgumentException("Set " + name + ".");
        }
        return value;
    }
}
```

## C# example

```csharp
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

var key = RequiredEnvironment("SPEECH_KEY");
var region = RequiredEnvironment("SPEECH_REGION");
var endpoint = new Uri($"wss://{region}.stt.speech.microsoft.com" + "/speech/universal/v2");
var speechConfig = SpeechConfig.FromEndpoint(endpoint, key);
speechConfig.Model = "MAI-Transcribe-2-Streaming";
speechConfig.SpeechRecognitionLanguage = "en-US";

using var audioFormat = AudioStreamFormat.GetWaveFormatPCM(16000, 16, 1);
using var audioStream = AudioInputStream.CreatePushStream(audioFormat);
using var audioConfig = AudioConfig.FromStreamInput(audioStream);
using var inputCancellation = new CancellationTokenSource();
using var recognizer = new SpeechRecognizer(speechConfig, audioConfig);
var recognitionDone = new TaskCompletionSource<bool>(TaskCreationOptions.RunContinuationsAsynchronously);

recognizer.Recognizing += (sender, eventArgs) => Console.WriteLine($"Intermediate: {eventArgs.Result.Text}");
recognizer.Recognized += (sender, eventArgs) =>
{
    var result = eventArgs.Result;
    if (result.Reason == ResultReason.RecognizedSpeech)
    {
        Console.WriteLine($"Final: {result.Text}");
    }
    else if (result.Reason == ResultReason.NoMatch)
    {
        Console.WriteLine("No speech recognized.");
    }
};
recognizer.Canceled += (sender, eventArgs) =>
{
    if (eventArgs.Reason == CancellationReason.Error)
    {
        var error = new InvalidOperationException($"{eventArgs.ErrorCode}: {eventArgs.ErrorDetails}");
        recognitionDone.TrySetException(error);
    }
    else
    {
        recognitionDone.TrySetResult(true);
    }
    inputCancellation.Cancel();
};
recognizer.SessionStarted += (sender, eventArgs) => Console.WriteLine($"Session ID: {eventArgs.SessionId}");
recognizer.SessionStopped += (sender, eventArgs) =>
{
    recognitionDone.TrySetResult(true);
    inputCancellation.Cancel();
};

await recognizer.StartContinuousRecognitionAsync();
bool inputClosed = false;
try
{
    // Adapt this block to your application's audio source.
    // Write raw audio matching audioFormat, and close the push stream when input ends.
    // Each full chunk below contains 100 ms of audio.
    using var pcmInput = File.OpenRead("audio.pcm");
    const int bytesPerSecond = 16000 * 2;
    var audioBuffer = new byte[3200];
    try
    {
        while (!recognitionDone.Task.IsCompleted)
        {
            int bytesRead = await pcmInput.ReadAsync(audioBuffer.AsMemory(), inputCancellation.Token);
            if (bytesRead == 0)
            {
                break;
            }
            audioStream.Write(audioBuffer.AsSpan(0, bytesRead).ToArray());
            await Task.Delay(TimeSpan.FromSeconds((double)bytesRead / bytesPerSecond), inputCancellation.Token);
        }
    }
    catch (OperationCanceledException) when (recognitionDone.Task.IsCompleted)
    {
    }

    audioStream.Close();
    inputClosed = true;
    // The 30-second wait is an application-level drain timeout, not a service latency guarantee.
    // Choose a suitable timeout for your use.
    await recognitionDone.Task.WaitAsync(TimeSpan.FromSeconds(30));
}
finally
{
    if (!inputClosed)
    {
        audioStream.Close();
    }
    await recognizer.StopContinuousRecognitionAsync();
}

static string RequiredEnvironment(string name)
{
    var value = Environment.GetEnvironmentVariable(name);
    return !string.IsNullOrWhiteSpace(value) ? value : throw new ArgumentException($"Set {name}.");
}
```

## Technical details

- Results don't include detected language information, confidence scores,
  or word-level timestamps. Only final results include segment-level `Offset`
  and `Duration`; intermediate results don't include timestamps. These values
  cover the submitted audio segment, which can include silence.

- The service ignores Speech SDK output format (`OutputFormat`) and profanity (`ProfanityOption`)
  settings; they don't affect transcription text or result structure.

- Intermediate text is provisional. Replace the current partial text in
  your UI instead of appending every intermediate event to the transcript.

- A final result confirms a segment. Append confirmed text separately from
  the current partial text; don't treat a partial as a final on failure.

- `NoMatch` is a recognition outcome, not necessarily a connection error.

- Normal end of input means closing the push stream, then waiting for
  recognition to finish. Calling stop immediately after the last write can
  prevent remaining results from being delivered.

- The SDK manages audio acknowledgments and connection recovery. Your
  application doesn't need to send ACK messages or reset result offsets.
  Unconfirmed audio can be replayed after a connection failure, so intermediate
  text might reappear. Avoid adding another retry loop that resends all audio
  while the SDK is still recovering.

## Language support

By default, the model operates in multilingual mode with language auto-detection. The following languages are currently supported:

[!INCLUDE [MAI Transcribe language support](includes/language-support/mai-transcribe.md)]

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Authentication failure | The key and selected Foundry/Speech region must match. |
| Invalid audio | Verify PCM format, byte order, and whole-sample chunks. |
| Model unavailable | Verify that you selected an available region. |
| Input ended but no completion | Close the stream, then wait for recognition to finish. |
| Service error | Record the error code, Session ID, and UTC time. |

> [!IMPORTANT]
> Don't include keys or authentication headers in application logs or support requests. Receiving intermediate text doesn't mean the request completed successfully.
