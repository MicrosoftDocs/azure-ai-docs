---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 1/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/go.md)]

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

[!INCLUDE [Prerequisites](../../common/azure-prerequisites-resourcekey-endpoint.md)]

## Set up the environment

The Speech SDK is available as a Go package. Install the Speech SDK later in this guide by using the terminal. For detailed installation instructions, see [Install the Speech SDK](../../../quickstarts/setup-platform.md?pivots=programming-language-go).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Create the application

Follow these steps to create a Go application and install the Speech SDK.

1. Open a terminal window in the folder where you want the new project. Create a new file named *main.go*.

1. Install the Speech SDK in your new project with the Go CLI.

   ```console
   go get github.com/Microsoft/cognitive-services-speech-sdk-go
   ```

1. Replace the contents of *main.go* with the following code.

    ```go
    package main

    import (
        "bufio"
        "fmt"
        "os"
        "strings"

        "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
    )

    func main() {
        // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
       speechKey := os.Getenv("SPEECH_KEY")
       endpoint := os.Getenv("ENDPOINT")
       if speechKey == "" || endpoint == "" {
           fmt.Println("Missing required environment variables. Set SPEECH_KEY and ENDPOINT.")
           return
       }

       speechConfig, err := speech.NewSpeechConfigFromEndpointWithSubscription(endpoint, speechKey)
       if err != nil {
           fmt.Println("Got an error: ", err)
           return
       }
       defer speechConfig.Close()
    
        // The neural multilingual voice can speak different languages based on the input text.
        speechConfig.SetSpeechSynthesisVoiceName("en-US-Ava:DragonHDLatestNeural") 

        audioConfig, err := audio.NewAudioConfigFromDefaultSpeakerOutput()
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }
        defer audioConfig.Close()

        speechSynthesizer, err := speech.NewSpeechSynthesizerFromConfig(speechConfig, audioConfig)
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }
        defer speechSynthesizer.Close()

        fmt.Println("Enter some text that you want to speak >")
        reader := bufio.NewReader(os.Stdin)
        text, _ := reader.ReadString('\n')
        text = strings.TrimSuffix(text, "\n")

        result, err := speechSynthesizer.SpeakText(context.Background(), text)
        if err != nil {
            fmt.Println("Got an error: ", err)
            return
        }

        if result.Reason == common.SynthesizingAudioCompleted {
            fmt.Printf("Speech synthesized for text: [%s]\n", text)
        } else if result.Reason == common.Canceled {
            cancellation, err := speech.NewCancellationDetailsFromSpeechSynthesisResult(result)
            if err != nil {
                fmt.Printf("Error getting cancellation details: %v\n", err)
                return
            }
            fmt.Printf("CANCELED: Reason=%v\n", cancellation.Reason)
            if cancellation.Reason == common.Error {
                fmt.Printf("CANCELED: ErrorCode=%v\nCANCELED: ErrorDetails=[%s]\nCANCELED: Did you set the speech resource key and region values?\n",
                    cancellation.ErrorCode,
                    cancellation.ErrorDetails)
            }
        }

        fmt.Println("Press any key to exit...")
        reader.ReadString('\n')
    }
    ```

1. To change the speech synthesis language, replace `en-US-Ava:DragonHDLatestNeural` with another [supported voice](~/articles/ai-services/speech-service/language-support.md#standard-voices).

   All neural voices are multilingual and fluent in their own language and English. For example, if the input text in English is *I'm excited to try text to speech* and you set `es-ES-Ximena:DragonHDLatestNeural` as the language, the text is spoken in English with a Spanish accent. If the voice doesn't speak the language of the input text, the Speech service doesn't output synthesized audio.

1. Run your new console application to start speech synthesis to the default speaker.

   ```console
   go run main.go
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `SPEECH_REGION` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Enter some text that you want to speak. For example, type *I'm excited to try text to speech*. Press the **Enter** key to hear the synthesized speech.

   ```console
   Enter some text that you want to speak >
   I'm excited to try text to speech
   ```

## Remarks

### More speech synthesis options

This quickstart uses the `SpeakText` function to synthesize a short block of text that you enter. You can also use long-form text from a file and get finer control over voice styles, prosody, and other settings.

- See [how to synthesize speech](~/articles/ai-services/speech-service/how-to-speech-synthesis.md) and [Speech Synthesis Markup Language (SSML) overview](~/articles/ai-services/speech-service/speech-synthesis-markup.md) for information about speech synthesis from a file and finer control over voice styles, prosody, and other settings.
- See [batch synthesis API for text to speech](~/articles/ai-services/speech-service/batch-synthesis.md) for information about synthesizing long-form text to speech.

### OpenAI text to speech voices in Azure Speech in Foundry Tools

OpenAI text to speech voices are also supported. See [OpenAI text to speech voices in Azure Speech](../../../openai-voices.md) and [multilingual voices](../../../language-support.md?tabs=tts#multilingual-voices). You can replace `en-US-Ava:DragonHDLatestNeural` with a supported OpenAI voice name such as `en-US-FableMultilingualNeural`.

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
