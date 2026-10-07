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
zone_pivot_groups: programming-languages-mai-transcribe-2-streaming-sdk
ai-usage: ai-assisted

# Customer intent: As a developer, I want to transcribe live audio with MAI-Transcribe-2-Streaming by using Azure Speech SDK.
---

# Use MAI-Transcribe-2-Streaming with Azure Speech SDK

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Transcribe-2-Streaming is a low-latency, speech-to-text model for real-time transcription. Send audio as a continuous stream and receive incremental transcripts while the speaker talks. Intermediate results update the current transcription, and final results confirm each segment.

The model supports live audio workloads such as call centers, voice assistants, meeting and lecture captioning, voice-driven interfaces, and real-time note taking.

For the OpenAI Realtime-compatible WebSocket integration, see [Use MAI-Transcribe-2-Streaming with the Realtime API](mai-transcribe-2-streaming-realtime.md).

See the overview for [serving regions](mai-transcribe-2-streaming.md#availability-and-regions) and [supported languages](mai-transcribe-2-streaming.md#language-support).

## Prerequisites

> [!div class="checklist"]
> - Azure Speech SDK v1.52.0.
> - An Azure subscription. You can [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
> - Create a [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) or Speech Resource in one of the supported regions by using the Azure portal.
> - After you deploy your resource, select **Go to resource** to view and manage keys. For the current list of supported regions, see [Speech service regions](regions.md?tabs=llmspeech).

::: zone pivot="programming-language-python"
## Transcribe audio from a file

```python
import threading
import azure.cognitiveservices.speech as speechsdk

def speech_recognize_continuous_from_file():
    speech_config = speechsdk.SpeechConfig(
        subscription="YourSpeechKey",
        region="YourSpeechRegion"
    )
    speech_config.model = "mai-transcribe-2-streaming"

    audio_config = speechsdk.audio.AudioConfig(
        filename="your_file_name.wav"
    )

    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    done = threading.Event()

    def stop_cb(evt):
        print("CLOSING on {}".format(evt))
        done.set()

    speech_recognizer.recognizing.connect(
        lambda evt: print("RECOGNIZING: {}".format(evt))
    )
    speech_recognizer.recognized.connect(
        lambda evt: print("RECOGNIZED: {}".format(evt))
    )
    speech_recognizer.session_started.connect(
        lambda evt: print("SESSION STARTED: {}".format(evt))
    )
    speech_recognizer.session_stopped.connect(
        lambda evt: print("SESSION STOPPED: {}".format(evt))
    )
    speech_recognizer.canceled.connect(
        lambda evt: print("CANCELED: {}".format(evt))
    )

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    done.wait()

    speech_recognizer.stop_continuous_recognition()


speech_recognize_continuous_from_file()
```
::: zone-end

::: zone pivot="programming-language-java"
## Transcribe audio from a file

```java
import java.util.concurrent.Semaphore;
import com.microsoft.cognitiveservices.speech.CancellationReason;
import com.microsoft.cognitiveservices.speech.ResultReason;
import com.microsoft.cognitiveservices.speech.SpeechConfig;
import com.microsoft.cognitiveservices.speech.SpeechRecognizer;
import com.microsoft.cognitiveservices.speech.audio.AudioConfig;

public final class MaiStreamingRecognition {
    public static void main(String[] args) throws Exception {
        // <recognitionContinuousWithFile>
        Semaphore stopRecognitionSemaphore = new Semaphore(0);

        // Creates an instance of a speech config with specified
        // subscription key and endpoint URL. Replace with your own subscription key
        // and endpoint URL.
        SpeechConfig config = SpeechConfig.fromSubscription("YourSubscriptionKey", "YourResourceRegion");
        config.setModel("mai-transcribe-2-streaming");

        // Creates a speech recognizer using file as audio input.
        // Replace with your own audio file name.
        AudioConfig audioInput = AudioConfig.fromWavFileInput("YourAudioFile.wav");

        SpeechRecognizer recognizer = new SpeechRecognizer(config, audioInput);
        {
            // Subscribes to events.
            recognizer.recognizing.addEventListener((s, e) -> {
                System.out.println("RECOGNIZING: Text=" + e.getResult().getText());
            });

            recognizer.recognized.addEventListener((s, e) -> {
                if (e.getResult().getReason() == ResultReason.RecognizedSpeech) {
                    System.out.println("RECOGNIZED: Text=" + e.getResult().getText());
                }
                else if (e.getResult().getReason() == ResultReason.NoMatch) {
                    System.out.println("NOMATCH: Speech could not be recognized.");
                }
            });

            recognizer.canceled.addEventListener((s, e) -> {
                System.out.println("CANCELED: Reason=" + e.getReason());

                if (e.getReason() == CancellationReason.Error) {
                    System.out.println("CANCELED: ErrorCode=" + e.getErrorCode());
                    System.out.println("CANCELED: ErrorDetails=" + e.getErrorDetails());
                    System.out.println("CANCELED: Did you update the subscription info?");
                }

                stopRecognitionSemaphore.release();
            });

            recognizer.sessionStarted.addEventListener((s, e) -> {
                System.out.println("\n    Session started event.");
            });

            recognizer.sessionStopped.addEventListener((s, e) -> {
                System.out.println("\n    Session stopped event.");
            });

            // Starts continuous recognition. Uses stopContinuousRecognitionAsync() to stop recognition.
            recognizer.startContinuousRecognitionAsync().get();

            // Waits for completion.
            stopRecognitionSemaphore.acquire();

            recognizer.stopContinuousRecognitionAsync().get();
        }

        config.close();
        audioInput.close();
        recognizer.close();
    }
}
```
::: zone-end

::: zone pivot="programming-language-csharp"
## Transcribe audio from a file

```csharp
using System;
using System.Threading.Tasks;
using Microsoft.CognitiveServices.Speech;
using Microsoft.CognitiveServices.Speech.Audio;

using var config = SpeechConfig.FromSubscription("YourSubscriptionKey", "YourResourceRegion");
config.Model = "mai-transcribe-2-streaming";

var stopRecognition = new TaskCompletionSource<int>(TaskCreationOptions.RunContinuationsAsynchronously);

// Creates a speech recognizer using file as audio input.
// Replace with your own audio file name.
using (var audioInput = AudioConfig.FromWavFileInput(@"YourAudioFile.wav"))
{
    using (var recognizer = new SpeechRecognizer(config, audioInput))
    {
        // Subscribes to events.
        recognizer.Recognizing += (s, e) =>
        {
            Console.WriteLine($"RECOGNIZING: Text={e.Result.Text}");
        };

        recognizer.Recognized += (s, e) =>
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

        recognizer.Canceled += (s, e) =>
        {
            Console.WriteLine($"CANCELED: Reason={e.Reason}");

            if (e.Reason == CancellationReason.Error)
            {
                Console.WriteLine($"CANCELED: ErrorCode={e.ErrorCode}");
                Console.WriteLine($"CANCELED: ErrorDetails={e.ErrorDetails}");
                Console.WriteLine($"CANCELED: Did you update the subscription info?");
            }

            stopRecognition.TrySetResult(0);
        };

        recognizer.SessionStarted += (s, e) =>
        {
            Console.WriteLine("\n    Session started event.");
        };

        recognizer.SessionStopped += (s, e) =>
        {
            Console.WriteLine("\n    Session stopped event.");
            Console.WriteLine("\nStop recognition.");
            stopRecognition.TrySetResult(0);
        };

        // Starts continuous recognition. Uses StopContinuousRecognitionAsync() to stop recognition.
        await recognizer.StartContinuousRecognitionAsync().ConfigureAwait(false);

        // Waits for completion.
        // Use Task.WaitAny to keep the task rooted.
        await stopRecognition.Task;

        // Stops recognition.
        await recognizer.StopContinuousRecognitionAsync().ConfigureAwait(false);
    }
}
```
::: zone-end

::: zone pivot="programming-language-cpp"
## Transcribe audio from a file

To install Speech SDK v1.52.0, follow the [C++ Speech SDK setup](quickstarts/setup-platform.md?pivots=programming-language-cpp). Replace the subscription key, region, and WAV file path with your own values.

```cpp
#include <speechapi_cxx.h>

#include <exception>
#include <future>
#include <iostream>

using namespace Microsoft::CognitiveServices::Speech;
using namespace Microsoft::CognitiveServices::Speech::Audio;
using namespace std;

void SpeechContinuousRecognitionWithFile()
{
    // Replace with your own subscription key and region.
    auto config = SpeechConfig::FromSubscription(
        "YourSubscriptionKey", "YourServiceRegion");
    config->SetModel("mai-transcribe-2-streaming");

    // Replace with your own audio file name.
    auto audioInput =
        AudioConfig::FromWavFileInput("YourAudioFile.wav");
    auto recognizer =
        SpeechRecognizer::FromConfig(config, audioInput);
    promise<void> recognitionEnd;

    recognizer->Recognizing.Connect([](
        const SpeechRecognitionEventArgs& event)
    {
        cout << "RECOGNIZING: Text="
             << event.Result->Text << endl;
    });

    recognizer->Recognized.Connect([](
        const SpeechRecognitionEventArgs& event)
    {
        if (event.Result->Reason == ResultReason::RecognizedSpeech)
        {
            cout << "RECOGNIZED: Text="
                 << event.Result->Text << endl;
        }
        else if (event.Result->Reason == ResultReason::NoMatch)
        {
            cout << "NOMATCH: Speech could not be recognized."
                 << endl;
        }
    });

    recognizer->Canceled.Connect([&recognitionEnd](
        const SpeechRecognitionCanceledEventArgs& event)
    {
        cout << "CANCELED: Reason="
             << static_cast<int>(event.Reason) << endl;

        if (event.Reason == CancellationReason::Error)
        {
            cout << "CANCELED: ErrorCode="
                 << static_cast<int>(event.ErrorCode) << "\n"
                 << "CANCELED: ErrorDetails="
                 << event.ErrorDetails << endl;
            recognitionEnd.set_value();
        }
    });

    recognizer->SessionStarted.Connect([](const SessionEventArgs&)
    {
        cout << "Session started." << endl;
    });

    recognizer->SessionStopped.Connect([&recognitionEnd](
        const SessionEventArgs&)
    {
        cout << "Session stopped." << endl;
        recognitionEnd.set_value();
    });

    recognizer->StartContinuousRecognitionAsync().get();

    recognitionEnd.get_future().get();

    recognizer->StopContinuousRecognitionAsync().get();
}

int main()
{
    try
    {
        SpeechContinuousRecognitionWithFile();
    }
    catch (const std::exception& error)
    {
        cerr << error.what() << endl;
        return 1;
    }
    return 0;
}
```

Reference: [`SpeechConfig`](/cpp/cognitive-services/speech/speechconfig), [`AudioConfig`](/cpp/cognitive-services/speech/audio-audioconfig), and [`SpeechRecognizer`](/cpp/cognitive-services/speech/speechrecognizer).
::: zone-end

::: zone pivot="programming-language-go"
## Transcribe audio from a file

To install Go, the Speech SDK native library, and its `cgo` dependencies on Linux, follow the [Go Speech SDK setup](quickstarts/setup-platform.md?pivots=programming-language-go). Create a module with `go mod init mai-streaming`, and install the Go bindings with `go get github.com/Microsoft/cognitive-services-speech-sdk-go@v1.52.0`. Replace the subscription key, region, and WAV file path with your own values. Save the example as `main.go`, and run `go run .`.

```go
package main

import (
    "fmt"
    "sync"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

func continuousRecognitionWithFile() error {
    config, err := speech.NewSpeechConfigFromSubscription(
        "YourSubscriptionKey", "YourServiceRegion")
    if err != nil {
        return err
    }
    defer config.Close()
    if err := config.SetModel("mai-transcribe-2-streaming"); err != nil {
        return err
    }

    audioConfig, err :=
        audio.NewAudioConfigFromWavFileInput("YourAudioFile.wav")
    if err != nil {
        return err
    }
    defer audioConfig.Close()
    recognizer, err := speech.NewSpeechRecognizerFromConfig(
        config, audioConfig)
    if err != nil {
        return err
    }
    defer recognizer.Close()

    done := make(chan struct{})
    var once sync.Once
    stopRecognition := func() {
        once.Do(func() { close(done) })
    }

    recognizer.Recognizing(func(event speech.SpeechRecognitionEventArgs) {
        defer event.Close()
        fmt.Println("RECOGNIZING: Text=", event.Result.Text)
    })
    recognizer.Recognized(func(event speech.SpeechRecognitionEventArgs) {
        defer event.Close()
        switch event.Result.Reason {
        case common.RecognizedSpeech:
            fmt.Println("RECOGNIZED: Text=", event.Result.Text)
        case common.NoMatch:
            fmt.Println("NOMATCH: Speech could not be recognized.")
        }
    })
    recognizer.Canceled(func(event speech.SpeechRecognitionCanceledEventArgs) {
        defer event.Close()
        fmt.Println("CANCELED: Reason=", event.Reason)
        if event.Reason == common.Error {
            fmt.Println("CANCELED: ErrorCode=", event.ErrorCode)
            fmt.Println("CANCELED: ErrorDetails=", event.ErrorDetails)
        }
        stopRecognition()
    })
    recognizer.SessionStarted(func(event speech.SessionEventArgs) {
        defer event.Close()
        fmt.Println("Session started.")
    })
    recognizer.SessionStopped(func(event speech.SessionEventArgs) {
        defer event.Close()
        fmt.Println("Session stopped.")
        stopRecognition()
    })

    if err := <-recognizer.StartContinuousRecognitionAsync(); err != nil {
        return err
    }

    <-done

    return <-recognizer.StopContinuousRecognitionAsync()
}

func main() {
    if err := continuousRecognitionWithFile(); err != nil {
        fmt.Println("Got an error:", err)
    }
}
```

Reference: [`SpeechConfig`](https://pkg.go.dev/github.com/Microsoft/cognitive-services-speech-sdk-go@v1.52.0/speech#SpeechConfig), [`AudioConfig`](https://pkg.go.dev/github.com/Microsoft/cognitive-services-speech-sdk-go@v1.52.0/audio#AudioConfig), and [`SpeechRecognizer`](https://pkg.go.dev/github.com/Microsoft/cognitive-services-speech-sdk-go@v1.52.0/speech#SpeechRecognizer).
::: zone-end

::: zone pivot="programming-language-javascript"
## Transcribe audio from a file

Install the Speech SDK for Node.js with `npm install microsoft-cognitiveservices-speech-sdk@1.52.0`. Save a PCM WAV file as `YourAudioFile.wav`. Replace the subscription key and region with your own values, add `"type": "module"` to `package.json`, and run `node speech.js`.

```javascript
import { readFileSync } from "node:fs";
import * as sdk from "microsoft-cognitiveservices-speech-sdk";

async function main() {
  const audioConfig = sdk.AudioConfig.fromWavFileInput(
    readFileSync("YourAudioFile.wav"),
    "YourAudioFile.wav"
  );
  const speechConfig = sdk.SpeechConfig.fromSubscription(
    "YourSubscriptionKey", "YourServiceRegion");
  speechConfig.setModel("mai-transcribe-2-streaming");

  const recognizer =
    new sdk.SpeechRecognizer(speechConfig, audioConfig);
  let stopRecognition;
  const recognitionEnd = new Promise((resolve) => {
    stopRecognition = resolve;
  });

  recognizer.recognizing = (_, event) => {
    console.log(`RECOGNIZING: Text=${event.result.text}`);
  };

  recognizer.recognized = (_, event) => {
    if (event.result.reason === sdk.ResultReason.RecognizedSpeech) {
      console.log(`RECOGNIZED: Text=${event.result.text}`);
    } else if (event.result.reason === sdk.ResultReason.NoMatch) {
      console.log("NOMATCH: Speech could not be recognized.");
    }
  };

  recognizer.canceled = (_, event) => {
    console.log(`CANCELED: Reason=${event.reason}`);
    if (event.reason === sdk.CancellationReason.Error) {
      console.log(`CANCELED: ErrorCode=${event.errorCode}`);
      console.log(`CANCELED: ErrorDetails=${event.errorDetails}`);
    }
    stopRecognition();
  };

  recognizer.sessionStarted = () => {
    console.log("Session started.");
  };

  recognizer.sessionStopped = () => {
    console.log("Session stopped.");
    stopRecognition();
  };

  await new Promise((resolve, reject) => {
    recognizer.startContinuousRecognitionAsync(resolve, reject);
  });

  try {
    await recognitionEnd;
  } finally {
    await new Promise((resolve, reject) => {
      recognizer.stopContinuousRecognitionAsync(resolve, reject);
    });
    recognizer.close();
    speechConfig.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

Reference: [`SpeechConfig`](/javascript/api/microsoft-cognitiveservices-speech-sdk/speechconfig), [`AudioConfig`](/javascript/api/microsoft-cognitiveservices-speech-sdk/audioconfig), and [`SpeechRecognizer`](/javascript/api/microsoft-cognitiveservices-speech-sdk/speechrecognizer).
::: zone-end

::: zone pivot="programming-language-objectivec"
## Transcribe audio from a file

Add Speech SDK version 1.52.0 by following the [Swift Package Manager setup](https://github.com/microsoft/speech-sdk-spm#getting-started). Select the `MicrosoftCognitiveServicesSpeech-iOS` product for your app target. Add a PCM WAV file named `YourAudioFile.wav` to the app bundle. Add the following methods to `ViewController.m`, and replace the subscription key and region with your own values.

```objectivec
#import "ViewController.h"

#import <MicrosoftCognitiveServicesSpeech/SPXSpeechApi.h>
#import <dispatch/dispatch.h>

@implementation ViewController

- (IBAction)continuousRecognitionButtonTapped:(UIButton *)sender {
    dispatch_async(
        dispatch_get_global_queue(QOS_CLASS_USER_INITIATED, 0), ^{
            [self continuousRecognitionWithFile];
        });
}

- (void)continuousRecognitionWithFile {
    NSBundle *mainBundle = [NSBundle mainBundle];
    NSString *audioFilePath = [mainBundle
        pathForResource:@"YourAudioFile" ofType:@"wav"];
    if (!audioFilePath) {
        NSLog(@"Cannot find audio file.");
        return;
    }

    SPXAudioConfiguration *audioConfig = [[SPXAudioConfiguration alloc]
        initWithWavFileInput:audioFilePath];
    SPXSpeechConfiguration *speechConfig =
        [[SPXSpeechConfiguration alloc]
            initWithSubscription:@"YourSubscriptionKey"
            region:@"YourServiceRegion"];
    speechConfig.model = @"mai-transcribe-2-streaming";

    SPXSpeechRecognizer *recognizer = [[SPXSpeechRecognizer alloc]
        initWithSpeechConfiguration:speechConfig
        audioConfiguration:audioConfig];
    dispatch_semaphore_t stopRecognitionSemaphore =
        dispatch_semaphore_create(0);

    [recognizer addRecognizingEventHandler:^(
        SPXSpeechRecognizer *sender,
        SPXSpeechRecognitionEventArgs *event) {
        NSLog(@"RECOGNIZING: Text=%@", event.result.text);
    }];

    [recognizer addRecognizedEventHandler:^(
        SPXSpeechRecognizer *sender,
        SPXSpeechRecognitionEventArgs *event) {
        if (event.result.reason == SPXResultReason_RecognizedSpeech) {
            NSLog(@"RECOGNIZED: Text=%@", event.result.text);
        } else if (event.result.reason == SPXResultReason_NoMatch) {
            NSLog(@"NOMATCH: Speech could not be recognized.");
        }
    }];

    [recognizer addCanceledEventHandler:^(
        SPXSpeechRecognizer *sender,
        SPXSpeechRecognitionCanceledEventArgs *event) {
        NSLog(@"CANCELED: Reason=%lu", (unsigned long)event.reason);
        if (event.reason == SPXCancellationReason_Error) {
            NSLog(@"CANCELED: ErrorCode=%lu",
                (unsigned long)event.errorCode);
            NSLog(@"CANCELED: ErrorDetails=%@",
                event.errorDetails);
        }
        dispatch_semaphore_signal(stopRecognitionSemaphore);
    }];

    [recognizer addSessionStartedEventHandler:^(
        SPXRecognizer *sender, SPXSessionEventArgs *event) {
        NSLog(@"Session started.");
    }];

    [recognizer addSessionStoppedEventHandler:^(
        SPXRecognizer *sender, SPXSessionEventArgs *event) {
        NSLog(@"Session stopped.");
        dispatch_semaphore_signal(stopRecognitionSemaphore);
    }];

    [recognizer startContinuousRecognition];

    dispatch_semaphore_wait(
        stopRecognitionSemaphore, DISPATCH_TIME_FOREVER);

    [recognizer stopContinuousRecognition];
}

@end
```

Reference: [`SPXSpeechConfiguration`](/objectivec/cognitive-services/speech/spxspeechconfiguration), [`SPXAudioConfiguration`](/objectivec/cognitive-services/speech/spxaudioconfiguration), and [`SPXSpeechRecognizer`](/objectivec/cognitive-services/speech/spxspeechrecognizer).
::: zone-end

::: zone pivot="programming-language-swift"
## Transcribe audio from a file

Add Speech SDK version 1.52.0 by following the [Swift Package Manager setup](https://github.com/microsoft/speech-sdk-spm#getting-started). Select the `MicrosoftCognitiveServicesSpeech-iOS` product for your app target. Add a WAV file named `YourAudioFile.wav` to the app bundle. Add the following methods to `ViewController.swift`, and replace the subscription key and region with your own values.

```swift
import UIKit
import Dispatch
import MicrosoftCognitiveServicesSpeech

extension ViewController {
    @IBAction func continuousRecognitionButtonTapped(
        _ sender: UIButton
    ) {
        DispatchQueue.global(qos: .userInitiated).async {
            do {
                try self.continuousRecognition()
            } catch {
                print("Recognition error: \(error)")
            }
        }
    }

    func continuousRecognition() throws {
        let speechConfig = try SPXSpeechConfiguration(
            subscription: "YourSubscriptionKey",
            region: "YourServiceRegion")
        speechConfig.model = "mai-transcribe-2-streaming"

        let bundle = Bundle.main
        guard let path = bundle.path(
            forResource: "YourAudioFile", ofType: "wav") else {
            print("Cannot find audio file.")
            return
        }

        guard let audioConfig = SPXAudioConfiguration(
            wavFileInput: path) else {
            print("Cannot create the audio configuration.")
            return
        }

        let recognizer = try SPXSpeechRecognizer(
            speechConfiguration: speechConfig,
            audioConfiguration: audioConfig)
        let stopRecognition = DispatchSemaphore(value: 0)

        recognizer.addSessionStartedEventHandler { _, event in
            print("Session started: \(event.sessionId)")
        }

        recognizer.addRecognizingEventHandler { _, event in
            print("RECOGNIZING: Text=\(event.result.text ?? "")")
        }

        recognizer.addRecognizedEventHandler { _, event in
            if event.result.reason ==
                SPXResultReason.recognizedSpeech {
                print("RECOGNIZED: Text=\(event.result.text ?? "")")
            } else if event.result.reason ==
                SPXResultReason.noMatch {
                print("NOMATCH: Speech could not be recognized.")
            }
        }

        recognizer.addCanceledEventHandler { _, event in
            print("CANCELED: Reason=\(event.reason)")
            if event.reason == SPXCancellationReason.error {
                print("CANCELED: ErrorCode=\(event.errorCode)")
                print(
                    "CANCELED: ErrorDetails=\(event.errorDetails ?? "")")
            }
            stopRecognition.signal()
        }

        recognizer.addSessionStoppedEventHandler { _, _ in
            print("Session stopped.")
            stopRecognition.signal()
        }

        try recognizer.startContinuousRecognition()

        stopRecognition.wait()

        try recognizer.stopContinuousRecognition()
    }
}
```

Reference: [`SPXSpeechConfiguration`](/objectivec/cognitive-services/speech/spxspeechconfiguration), [`SPXAudioConfiguration`](/objectivec/cognitive-services/speech/spxaudioconfiguration), and [`SPXSpeechRecognizer`](/objectivec/cognitive-services/speech/spxspeechrecognizer).
::: zone-end

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Authentication failure | The key and selected Foundry/Speech region must match. |
| Invalid audio | Verify that the input is a supported WAV file. |
| Model unavailable | Verify that you selected an available region. |
| Service error | Record the error code, Session ID, and UTC time. |

> [!IMPORTANT]
> Don't include keys or authentication headers in application logs or support requests. Receiving intermediate text doesn't mean the request completed successfully.
