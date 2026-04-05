---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/29/2026
ms.custom: devx-track-go
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/go.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK for Go is available as a module. For more information, see the [Speech SDK for Go on pkg.go.dev](https://pkg.go.dev/github.com/Microsoft/cognitive-services-speech-sdk-go).

Before you can use the Speech SDK for Go, install the Speech SDK native library. See the [installation guide](../../../quickstarts/setup-platform.md?pivots=programming-language-go) for more information.

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Implement diarization from file with conversation transcription

Follow these steps to create a new console application.

1. Create a new directory for your project and create a file named `conversation_transcription.go`.

1. Install the Speech SDK module:

    ```console
    go get github.com/Microsoft/cognitive-services-speech-sdk-go
    ```

1. Copy the following code into `conversation_transcription.go`:

    ```go
    package main

    import (
        "bufio"
        "fmt"
        "os"
        "time"

        "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/transcription"
    )

    func main() {
        // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
        // Replace with your own subscription key and endpoint
        // The endpoint is like: "https://YourServiceRegion.api.cognitive.microsoft.com"
        speechKey := os.Getenv("SPEECH_KEY")
        endpoint := os.Getenv("ENDPOINT")

        speechConfig, err := speech.NewSpeechConfigFromEndpoint(endpoint)
        if err != nil {
            fmt.Println("Error creating speech config:", err)
            return
        }
        defer speechConfig.Close()

        err = speechConfig.SetProperty(common.SpeechServiceAuthorization, speechKey)
        if err != nil {
            fmt.Println("Error setting authorization:", err)
            return
        }

        err = speechConfig.SetSpeechRecognitionLanguage("en-US")
        if err != nil {
            fmt.Println("Error setting language:", err)
            return
        }

        // Enable intermediate diarization results
        err = speechConfig.SetProperty(common.SpeechServiceResponseDiarizeIntermediateResults, "true")
        if err != nil {
            fmt.Println("Error setting diarization property:", err)
            return
        }

        audioConfig, err := audio.NewAudioConfigFromWavFileInput("katiesteve.wav")
        if err != nil {
            fmt.Println("Error creating audio config:", err)
            return
        }
        defer audioConfig.Close()

        conversationTranscriber, err := transcription.NewConversationTranscriberFromConfig(speechConfig, audioConfig)
        if err != nil {
            fmt.Println("Error creating conversation transcriber:", err)
            return
        }
        defer conversationTranscriber.Close()

        transcribingStop := false

        // Connect callbacks to the events
        conversationTranscriber.Transcribing(func(event transcription.ConversationTranscriptionEventArgs) {
            fmt.Println("TRANSCRIBING:")
            fmt.Printf("\tText=%s\n", event.Result.Text)
            fmt.Printf("\tSpeaker ID=%s\n", event.Result.SpeakerID)
        })

        conversationTranscriber.Transcribed(func(event transcription.ConversationTranscriptionEventArgs) {
            fmt.Println("\nTRANSCRIBED:")
            if event.Result.Reason == common.RecognizedSpeech {
                fmt.Printf("\tText=%s\n", event.Result.Text)
                fmt.Printf("\tSpeaker ID=%s\n\n", event.Result.SpeakerID)
            } else if event.Result.Reason == common.NoMatch {
                fmt.Println("\tNOMATCH: Speech could not be transcribed.")
            }
        })

        conversationTranscriber.Canceled(func(event transcription.ConversationTranscriptionCanceledEventArgs) {
            fmt.Println("CANCELED:", event.Reason)
            if event.Reason == common.Error {
                fmt.Println("Error details:", event.ErrorDetails)
            }
            transcribingStop = true
        })

        conversationTranscriber.SessionStarted(func(event speech.SessionEventArgs) {
            fmt.Println("SessionStarted event")
        })

        conversationTranscriber.SessionStopped(func(event speech.SessionEventArgs) {
            fmt.Println("SessionStopped event")
            fmt.Println("CLOSING on session stopped event")
            transcribingStop = true
        })

        // Start transcription
        err = <-conversationTranscriber.StartTranscribingAsync()
        if err != nil {
            fmt.Println("Error starting transcription:", err)
            return
        }

        // Wait for completion
        for !transcribingStop {
            time.Sleep(500 * time.Millisecond)
        }

        // Stop transcription
        err = <-conversationTranscriber.StopTranscribingAsync()
        if err != nil {
            fmt.Println("Error stopping transcription:", err)
            return
        }
    }
    ```

1. Get the [sample audio file](https://github.com/Azure-Samples/cognitive-services-speech-sdk/blob/master/sampledata/audiofiles/katiesteve.wav) or use your own `.wav` file. Replace `katiesteve.wav` with the path and name of your `.wav` file.

   The application recognizes speech from multiple participants in the conversation. Your audio file should contain multiple speakers.

1. To change the speech recognition language, replace `en-US` with another [supported language](/azure/cognitive-services/speech-service/supported-languages). For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](/azure/cognitive-services/speech-service/language-identification).

1. Run your console application to start conversation transcription:

   ```console
   go run conversation_transcription.go
   ```

> [!IMPORTANT]
> Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

The transcribed conversation should be output as text:

```output
SessionStarted event
TRANSCRIBING:
        Text=good morning
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning steve
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning steve how are
        Speaker ID=Guest-1
TRANSCRIBING:
        Text=good morning steve how are you doing today
        Speaker ID=Guest-1

TRANSCRIBED:
        Text=Good morning, Steve. How are you doing today?
        Speaker ID=Guest-1

TRANSCRIBING:
        Text=good morning katie
        Speaker ID=Unknown
TRANSCRIBING:
        Text=good morning katie i hope you're having a
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=good morning katie i hope you're having a great start to
        Speaker ID=Guest-2
TRANSCRIBING:
        Text=good morning katie i hope you're having a great start to your day
        Speaker ID=Guest-2

TRANSCRIBED:
        Text=Good morning, Katie. I hope you're having a great start to your day.
        Speaker ID=Guest-2

SessionStopped event
CLOSING on session stopped event
```

Speakers are identified as Guest-1, Guest-2, and so on, depending on the number of speakers in the conversation.

> [!NOTE]
> You might see `Speaker ID=Unknown` in some of the early intermediate results when the speaker isn't yet identified. Without intermediate diarization results (if you don't set the `SpeechServiceResponse_DiarizeIntermediateResults` property to "true"), the speaker ID is always "Unknown."

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
