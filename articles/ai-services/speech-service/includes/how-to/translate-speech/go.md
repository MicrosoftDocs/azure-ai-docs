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

## Sensitive data and environment variables

The example source code in this article depends on environment variables for storing sensitive data, such as the Speech resource's key and region. The Go code file contains two values that are assigned from the host machine's environment variables: `SPEECH_KEY` and `SPEECH_REGION`. Both of these variables are at the package scope, so they're accessible within the functions of the package:

```go
speechKey := os.Getenv("SPEECH_KEY")
speechRegion := os.Getenv("SPEECH_REGION")
```

For more information on environment variables, see [Environment variables and application configuration](../../../../cognitive-services-environment-variables.md).

[!INCLUDE [Azure key vault](~/reusable-content/ce-skilling/azure/includes/ai-services/security/azure-key-vault.md)]

## Create a speech translation configuration

To call the Speech service by using the Speech SDK, you need to create a `SpeechTranslationConfig` instance. This class includes information about your Speech resource, like your key and associated region, endpoint, host, or authorization token.

> [!TIP]
> Regardless of whether you're performing speech recognition, speech synthesis, translation, or intent recognition, you'll always create a configuration.

You can initialize a `SpeechTranslationConfig` instance in a few ways:

* With a subscription: pass in a key and the associated region.
* With an endpoint: pass in a Speech service endpoint. A key or authorization token is optional.
* With a host: pass in a host address. A key or authorization token is optional.
* With an authorization token: pass in an authorization token and the associated region.

Let's look at how you can create a `SpeechTranslationConfig` instance by using a key and region. Get the Speech resource key and region in the [Azure portal](https://portal.azure.com).

```go
import (
    "fmt"
    "os"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

func translateSpeech() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()
}
```

## Change the source language

One common task of speech translation is specifying the input (or source) language. The following example shows how you would change the input language to Italian. In your code, interact with the `SpeechTranslationConfig` instance by calling the `SetSpeechRecognitionLanguage` method:

```go
func translateSpeech() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()

    // Source (input) language
    translationConfig.SetSpeechRecognitionLanguage("it-IT")
}
```

The `SetSpeechRecognitionLanguage` method expects a language-locale format string. Refer to the [list of supported speech translation locales](../../../language-support.md?tabs=speech-translation).

## Add a translation language

Another common task of speech translation is to specify target translation languages. At least one is required, but multiples are supported. The following code snippet sets both French and German as translation language targets:

```go
func translateSpeech() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()

    translationConfig.SetSpeechRecognitionLanguage("it-IT")

    // Translate to languages. See https://aka.ms/speech/sttt-languages
    translationConfig.AddTargetLanguage("fr")
    translationConfig.AddTargetLanguage("de")
}
```

With every call to `AddTargetLanguage`, a new target translation language is specified. In other words, when speech is recognized from the source language, each target translation is available as part of the resulting translation operation.

## Initialize a translation recognizer

After you create a `SpeechTranslationConfig` instance, the next step is to initialize `TranslationRecognizer`. When you initialize `TranslationRecognizer`, you need to pass it your `translationConfig` instance. The configuration object provides the credentials that the Speech service requires to validate your request.

If you're recognizing speech by using your device's default microphone, here's what `TranslationRecognizer` should look like:

```go
func translateSpeech() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()

    fromLanguage := "en-US"
    toLanguages := []string{"it", "fr", "de"}

    translationConfig.SetSpeechRecognitionLanguage(fromLanguage)
    for _, language := range toLanguages {
        translationConfig.AddTargetLanguage(language)
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
}
```

If you want to provide an audio file instead of using a microphone, you still need to provide an `audioConfig` parameter. However, when you create an `AudioConfig` instance, instead of calling `NewAudioConfigFromDefaultMicrophoneInput`, you call `NewAudioConfigFromWavFileInput` and pass the filename:

```go
audioConfig, err := audio.NewAudioConfigFromWavFileInput("YourAudioFile.wav")
if err != nil {
    fmt.Println("Error creating audio config:", err)
    return
}
defer audioConfig.Close()
```

## Translate speech

To translate speech, the Speech SDK relies on a microphone or an audio file input. Speech recognition occurs before speech translation. After all objects are initialized, call the recognize-once function and get the result:

```go
package main

import (
    "fmt"
    "os"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

func main() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()

    fromLanguage := "en-US"
    toLanguages := []string{"it", "fr", "de"}

    translationConfig.SetSpeechRecognitionLanguage(fromLanguage)
    for _, language := range toLanguages {
        translationConfig.AddTargetLanguage(language)
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

    fmt.Printf("Say something in '%s' and we'll translate...\n", fromLanguage)

    outcome := <-translationRecognizer.RecognizeOnceAsync()
    if outcome.Error != nil {
        fmt.Println("Recognition error:", outcome.Error)
        return
    }

    result := outcome.Result
    defer result.Close()

    translations := result.GetTranslations()
    fmt.Printf("Recognized: \"%s\"\n", result.Text)
    for lang, translation := range translations {
        fmt.Printf("Translated into '%s': %s\n", lang, translation)
    }
}
```

For more information about speech to text, see [the basics of speech recognition](../../../get-started-speech-to-text.md).

## Continuous translation

The previous example uses single-shot translation, which translates a single utterance. You can also use continuous translation for long-running sessions. Continuous translation requires you to subscribe to events to receive translation results:

```go
package main

import (
    "bufio"
    "fmt"
    "os"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

func main() {
    speechKey := os.Getenv("SPEECH_KEY")
    speechRegion := os.Getenv("SPEECH_REGION")

    translationConfig, err := speech.NewSpeechTranslationConfigFromSubscription(speechKey, speechRegion)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer translationConfig.Close()

    fromLanguage := "en-US"
    toLanguages := []string{"de", "fr"}

    translationConfig.SetSpeechRecognitionLanguage(fromLanguage)
    for _, language := range toLanguages {
        translationConfig.AddTargetLanguage(language)
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

    // Subscribe to events
    translationRecognizer.Recognizing(func(event speech.TranslationRecognitionEventArgs) {
        fmt.Printf("RECOGNIZING: %s\n", event.Result.Text)
    })

    translationRecognizer.Recognized(func(event speech.TranslationRecognitionEventArgs) {
        if event.Result.Reason == speech.ResultReason.TranslatedSpeech {
            fmt.Printf("RECOGNIZED: %s\n", event.Result.Text)
            for lang, translation := range event.Result.GetTranslations() {
                fmt.Printf("TRANSLATED into '%s': %s\n", lang, translation)
            }
        }
    })

    translationRecognizer.Canceled(func(event speech.TranslationRecognitionCanceledEventArgs) {
        fmt.Printf("CANCELED: Reason=%d\n", event.Reason)
        if event.Reason == speech.CancellationReason.Error {
            fmt.Printf("CANCELED: ErrorDetails=%s\n", event.ErrorDetails)
        }
    })

    translationRecognizer.SessionStopped(func(event speech.SessionEventArgs) {
        fmt.Println("Session stopped.")
    })

    // Start continuous recognition
    err = <-translationRecognizer.StartContinuousRecognitionAsync()
    if err != nil {
        fmt.Println("Error starting continuous recognition:", err)
        return
    }

    fmt.Println("Continuous translation started. Press Enter to stop...")
    bufio.NewReader(os.Stdin).ReadBytes('\n')

    // Stop continuous recognition
    err = <-translationRecognizer.StopContinuousRecognitionAsync()
    if err != nil {
        fmt.Println("Error stopping continuous recognition:", err)
        return
    }
}
```

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
