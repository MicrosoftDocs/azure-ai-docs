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

[!INCLUDE [Prerequisites](../../common/azure-prerequisites.md)]

## Set up the environment

The Speech SDK for Go is available as a module. For more information, see the [Speech SDK for Go on pkg.go.dev](https://pkg.go.dev/github.com/Microsoft/cognitive-services-speech-sdk-go).

Before you can use the Speech SDK for Go, install the Speech SDK native library. See the [installation guide](../../../quickstarts/setup-platform.md?pivots=programming-language-go) for more information.

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables.md)]

## Translate speech from a microphone

Follow these steps to create a new console application.

1. Create a new directory for your project and create a file named `speech_translation.go`.

1. Install the Speech SDK module:

    ```console
    go get github.com/Microsoft/cognitive-services-speech-sdk-go
    ```

1. Copy the following code into `speech_translation.go`:

    ```go
    package main

    import (
        "fmt"
        "os"

        "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
        "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
    )

    func main() {
        // This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
        speechKey := os.Getenv("SPEECH_KEY")
        speechRegion := os.Getenv("SPEECH_REGION")

        translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
        if err != nil {
            fmt.Println("Error creating translation config:", err)
            return
        }
        defer translationConfig.Close()

        err = translationConfig.SetSpeechRecognitionLanguage("en-US")
        if err != nil {
            fmt.Println("Error setting speech recognition language:", err)
            return
        }

        toLanguage := "it"
        err = translationConfig.AddTargetLanguage(toLanguage)
        if err != nil {
            fmt.Println("Error adding target language:", err)
            return
        }

        audioConfig, err := audio.NewAudioConfigFromDefaultMicrophoneInput()
        if err != nil {
            fmt.Println("Error creating audio config:", err)
            return
        }
        defer audioConfig.Close()

        translationRecognizer, err := speech.NewTranslationRecognizerFromConfig(translationConfig, audioConfig)
        if err != nil {
            fmt.Println("Error creating translation recognizer:", err)
            return
        }
        defer translationRecognizer.Close()

        fmt.Println("Speak into your microphone.")
        outcome := <-translationRecognizer.RecognizeOnceAsync()
        if outcome.Error != nil {
            fmt.Println("Recognition error:", outcome.Error)
            return
        }

        result := outcome.Result
        defer result.Close()

        if result.Reason == speech.ResultReason.TranslatedSpeech {
            fmt.Printf("Recognized: %s\n", result.Text)
            translations := result.GetTranslations()
            fmt.Printf("Translated into '%s': %s\n", toLanguage, translations[toLanguage])
        } else if result.Reason == speech.ResultReason.NoMatch {
            fmt.Println("No speech could be recognized.")
        } else if result.Reason == speech.ResultReason.Canceled {
            fmt.Println("Speech recognition canceled.")
        }
    }
    ```

1. To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=stt#supported-languages). Specify the full locale with a dash (`-`) separator. For example, `es-ES` for Spanish (Spain). The default language is `en-US` if you don't specify a language. For details about how to identify one of multiple languages that might be spoken, see [language identification](~/articles/ai-services/speech-service/language-identification.md).
1. To change the translation target language, replace `it` with another [supported language](~/articles/ai-services/speech-service/language-support.md?tabs=speech-translation#supported-languages). With few exceptions, you only specify the language code that precedes the locale dash (`-`) separator. For example, use `es` for Spanish (Spain) instead of `es-ES`. The default language is `en` if you don't specify a language.

Run your new console application to start speech recognition from a microphone:

```console
go run speech_translation.go
```

Speak into your microphone when prompted. What you speak should be output as translated text in the target language:

```output
Speak into your microphone.
Recognized: I'm excited to try speech translation.
Translated into 'it': Sono entusiasta di provare la traduzione vocale.
```

## Remarks

After completing the quickstart, here are some more considerations:

- This example uses the `RecognizeOnceAsync` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to translate speech](~/articles/ai-services/speech-service/how-to-translate-speech.md).
- To recognize speech from an audio file, use `NewAudioConfigFromWavFileInput` instead of `NewAudioConfigFromDefaultMicrophoneInput`:
    ```go
    audioConfig, err := audio.NewAudioConfigFromWavFileInput("YourAudioFile.wav")
    ```
- For compressed audio files such as MP4, install GStreamer and use `CreatePullStream` or `CreatePushStream`. For more information, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
