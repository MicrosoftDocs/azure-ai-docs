---
author: eric-urban
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/1/2024
ms.author: eur
---

[!INCLUDE [Header](../../common/go.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up the environment

Install the Speech SDK for the Go language. For detailed installation instructions, see [Install the Speech SDK](../../../quickstarts/setup-platform.md?pivots=programming-language-go).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Create the application

Follow these steps to create a Go module.

1. Open a command prompt window in the folder where you want the new project. Create a new file named *speech-synthesis.go*.
1. Copy the following code into *speech-synthesis.go*:

    ```go
    package main

    import (
        "bufio"
        "fmt"
        "os"
        "strings"
        "time"

        "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
    )

    func synthesizeStartedHandler(event speech.SpeechSynthesisEventArgs) {
        defer event.Close()
        fmt.Println("Synthesis started.")
    }

    func synthesizingHandler(event speech.SpeechSynthesisEventArgs) {
        defer event.Close()
        fmt.Printf("Synthesizing, audio chunk size %d.\n", len(event.Result.AudioData))
    }

    func synthesizedHandler(event speech.SpeechSynthesisEventArgs) {
        defer event.Close()
        fmt.Printf("Synthesized, audio length %d.\n", len(event.Result.AudioData))
    }

    func cancelledHandler(event speech.SpeechSynthesisEventArgs) {
        defer event.Close()
        fmt.Println("Received a cancellation.")
    }

    func main() {
        // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speechKey :=  os.Getenv("SPEECH_KEY")
        speechRegion := os.Getenv("SPEECH_REGION")

        audioConfig, err := audio.NewAudioConfigFromDefaultSpeakerOutput()
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }
        defer audioConfig.Close()
        speechConfig, err := speech.NewSpeechConfigFromSubscription(speechKey, speechRegion)
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }
        defer speechConfig.Close()

        speechConfig.SetSpeechSynthesisVoiceName("en-US-AvaMultilingualNeural")

        speechSynthesizer, err := speech.NewSpeechSynthesizerFromConfig(speechConfig, audioConfig)
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }
        defer speechSynthesizer.Close()

        speechSynthesizer.SynthesisStarted(synthesizeStartedHandler)
        speechSynthesizer.Synthesizing(synthesizingHandler)
        speechSynthesizer.SynthesisCompleted(synthesizedHandler)
        speechSynthesizer.SynthesisCanceled(cancelledHandler)

        for {
            fmt.Printf("Enter some text that you want to speak, or enter empty text to exit.\n> ")
            text, _ := bufio.NewReader(os.Stdin).ReadString('\n')
            text = strings.TrimSuffix(text, "\n")
            if len(text) == 0 {
                break
            }

            task := speechSynthesizer.SpeakTextAsync(text)
            var outcome speech.SpeechSynthesisOutcome
            select {
            case outcome = <-task:
            case <-time.After(60 * time.Second):
                fmt.Println("Timed out")
                return
            }
            defer outcome.Close()
            if outcome.Error != nil {
                fmt.Println("Got an error: ", outcome.Error)
                return
            }

            if outcome.Result.Reason == common.SynthesizingAudioCompleted {
                fmt.Printf("Speech synthesized to speaker for text [%s].\n", text)
            } else {
                cancellation, _ := speech.NewCancellationDetailsFromSpeechSynthesisResult(outcome.Result)
                fmt.Printf("CANCELED: Reason=%d.\n", cancellation.Reason)

                if cancellation.Reason == common.Error {
                    fmt.Printf("CANCELED: ErrorCode=%d\nCANCELED: ErrorDetails=[%s]\nCANCELED: Did you set the speech resource key and region values?\n",
                        cancellation.ErrorCode,
                        cancellation.ErrorDetails)
                }
            }
        }
    }
    ```

1. To change the speech synthesis language, replace `en-US-AvaMultilingualNeural` with another [supported voice](~/articles/ai-services/speech-service/language-support.md#standard-voices).

   All neural voices are multilingual and fluent in their own language and English. For example, if the input text in English is *I'm excited to try text to speech* and you set `es-ES-ElviraNeural`, the text is spoken in English with a Spanish accent. If the voice doesn't speak the language of the input text, the Speech service doesn't output synthesized audio.

1. Run the following commands to create a *go.mod* file that links to components hosted on GitHub:

   ```console
   go mod init speech-synthesis
   go get github.com/Microsoft/cognitive-services-speech-sdk-go
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `SPEECH_REGION` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Now build and run the code:

   ```console
   go build
   go run speech-synthesis
   ```

## Remarks

### OpenAI text to speech voices in Azure AI Speech

OpenAI text to speech voices are also supported. See [OpenAI text to speech voices in Azure AI Speech](../../../openai-voices.md) and [multilingual voices](../../../language-support.md?tabs=tts#multilingual-voices). You can replace `en-US-AvaMultilingualNeural` with a supported OpenAI voice name such as `en-US-FableMultilingualNeural`.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
