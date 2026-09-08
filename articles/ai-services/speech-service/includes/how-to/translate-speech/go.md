---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
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

## Event-based translation

The previous example uses single-shot translation, which translates a single utterance. You can also use event based translation for long-running sessions. Event based translation requires you to subscribe to events to receive translation results.

> [!NOTE]
> Intermediate translation results aren't available when you use [multi-lingual speech translation](#multi-lingual-translation-with-language-identification).

The following example shows how to use event based translation:

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

    fmt.Println("Event based translation started. Press Enter to stop...")
    bufio.NewReader(os.Stdin).ReadBytes('\n')

    // Stop continuous recognition
    err = <-translationRecognizer.StopContinuousRecognitionAsync()
    if err != nil {
        fmt.Println("Error stopping continuous recognition:", err)
        return
    }
}
```

## Synthesize translations

After a successful speech recognition and translation, the result contains all the translations in a map. The `GetTranslations()` method returns a map with the key as the target translation language and the value as the translated text. Recognized speech can be translated and then synthesized in a different language (speech-to-speech).

### Event-based synthesis

The `TranslationRecognizer` object exposes a `Synthesizing` callback. The event fires several times and provides a mechanism to retrieve the synthesized audio from the translation recognition result. If you're translating to multiple languages, see [Manual synthesis](#manual-synthesis). 

Specify the synthesis voice by calling the `SetVoiceName` method on the configuration, and provide a callback function for the `Synthesizing` event to get the audio. The following example saves the translated audio as a .wav file.

> [!IMPORTANT]
> The event-based synthesis works only with a single translation. *Do not* add multiple target translation languages. Additionally, the `SetVoiceName` value should be the same language as the target translation language. For example, `"de"` could map to `"de-DE-Hedda"`.

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
    toLanguage := "de"

    translationConfig.SetSpeechRecognitionLanguage(fromLanguage)
    translationConfig.AddTargetLanguage(toLanguage)

    // See: https://aka.ms/speech/sdkregion#standard-and-neural-voices
    translationConfig.SetVoiceName("de-DE-Hedda")

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

    translationRecognizer.Synthesizing(func(event speech.TranslationSynthesisEventArgs) {
        audioData := event.Result.GetAudio()
        size := len(audioData)
        fmt.Printf("Audio synthesized: %d byte(s) %s\n", size, map[bool]string{true: "(COMPLETE)", false: ""}[size == 0])

        if size > 0 {
            file, err := os.Create("translation.wav")
            if err != nil {
                fmt.Println("Error creating file:", err)
                return
            }
            defer file.Close()
            file.Write(audioData)
        }
    })

    fmt.Printf("Say something in '%s' and we'll translate to '%s'...\n", fromLanguage, toLanguage)

    outcome := <-translationRecognizer.RecognizeOnceAsync()
    if outcome.Error != nil {
        fmt.Println("Recognition error:", outcome.Error)
        return
    }

    result := outcome.Result
    defer result.Close()

    if result.Reason == speech.ResultReason.TranslatedSpeech {
        fmt.Printf("Recognized: \"%s\"\n", result.Text)
        translations := result.GetTranslations()
        fmt.Printf("Translated into '%s': %s\n", toLanguage, translations[toLanguage])
    }
}
```

### Manual synthesis

You can use the translations map to synthesize audio from the translation text. Iterate through each translation and synthesize it. When you're creating a `SpeechSynthesizer` instance, the `SpeechConfig` object needs to have its `SetSpeechSynthesisVoiceName` method called with the desired voice.

The following example translates to five languages. Each translation is then synthesized to an audio file in the corresponding neural language.

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
    toLanguages := []string{"de", "fr", "it", "pt", "zh-Hans"}

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

    fmt.Println("Say something...")

    outcome := <-translationRecognizer.RecognizeOnceAsync()
    if outcome.Error != nil {
        fmt.Println("Recognition error:", outcome.Error)
        return
    }

    result := outcome.Result
    defer result.Close()

    if result.Reason == speech.ResultReason.TranslatedSpeech {
        languageToVoiceMap := map[string]string{
            "de":      "de-DE-KatjaNeural",
            "fr":      "fr-FR-DeniseNeural",
            "it":      "it-IT-ElsaNeural",
            "pt":      "pt-BR-FranciscaNeural",
            "zh-Hans": "zh-CN-XiaoxiaoNeural",
        }

        fmt.Printf("Recognized: \"%s\"\n", result.Text)
        translations := result.GetTranslations()

        for language, translation := range translations {
            fmt.Printf("Translated into '%s': %s\n", language, translation)

            speechConfig, err := speech.NewSpeechConfigFromSubscription(speechKey, speechRegion)
            if err != nil {
                fmt.Println("Error creating speech config:", err)
                continue
            }

            speechConfig.SetSpeechSynthesisVoiceName(languageToVoiceMap[language])

            outputFile := fmt.Sprintf("%s-translation.wav", language)
            audioOutput, err := audio.NewAudioConfigFromWavFileOutput(outputFile)
            if err != nil {
                fmt.Println("Error creating audio output config:", err)
                speechConfig.Close()
                continue
            }

            synthesizer, err := speech.NewSpeechSynthesizerFromConfig(speechConfig, audioOutput)
            if err != nil {
                fmt.Println("Error creating synthesizer:", err)
                audioOutput.Close()
                speechConfig.Close()
                continue
            }

            <-synthesizer.SpeakTextAsync(translation)

            synthesizer.Close()
            audioOutput.Close()
            speechConfig.Close()
        }
    }
}
```

For more information about speech synthesis, see [the basics of speech synthesis](../../../get-started-text-to-speech.md).

## Multi-lingual translation with language identification

In many scenarios, you might not know which input languages to specify. Using [language identification](../../../language-identification.md?pivots=programming-language-go#run-speech-translation) you can detect up to 10 possible input languages and automatically translate to your target languages. 

The following example anticipates that `en-US` or `zh-CN` should be detected because they're defined in `AutoDetectSourceLanguageConfig`. Then, the speech is translated to `de` and `fr` as specified in the calls to `AddTargetLanguage()`.

```go
translationConfig.AddTargetLanguage("de")
translationConfig.AddTargetLanguage("fr")
autoDetectSourceLanguageConfig, err := speech.NewAutoDetectSourceLanguageConfigFromLanguages([]string{"en-US", "zh-CN"})
if err != nil {
    fmt.Println("Error creating auto detect config:", err)
    return
}
defer autoDetectSourceLanguageConfig.Close()

translationRecognizer, err := speech.NewTranslationRecognizerFromAutoDetectSourceLangConfig(translationConfig, autoDetectSourceLanguageConfig, audioConfig)
```

For a complete code sample, see [language identification](../../../language-identification.md?pivots=programming-language-go#run-speech-translation).

## Using live interpreter for real-time speech-to-speech translation with personal voice

Live Interpreter continuously identifies the language being spoken without requiring you to set an input language. It delivers low-latency speech-to-speech translation in a natural voice that preserves the speaker's style and tone. 

To use the Live Interpreter API, first [apply for personal voice access](https://aka.ms/customneural) and select "Personal Voice" for Question 20. For resource ID, make sure that it's in one of the regions that support Live Interpreter. See the [Speech service regions table](../../../regions.md?tabs=speech-translation) for current regional availability.

After personal voice access permission is granted, you can enable Live Interpreter with the following code:

```go
// Replace YourResourceName with your Speech resource name
endpoint := "wss://YourResourceName.cognitiveservices.azure.com/stt/speech/universal/v2"

// Store your Speech resource key securely, for example, in an environment variable
speechKey := os.Getenv("SPEECH_KEY")
speechTranslationConfig, err := speech.NewSpeechTranslationConfigFromEndpointWithSubscription(endpoint, speechKey)
if err != nil {
    fmt.Println("Error creating translation config:", err)
    return
}
defer speechTranslationConfig.Close()

// Translation target language and enable personal voice
speechTranslationConfig.AddTargetLanguage("zh-Hans")
speechTranslationConfig.SetVoiceName("personal-voice")

// You don't need to define any candidate languages to detect.
autoDetectSourceLanguageConfig, err := speech.NewAutoDetectSourceLanguageConfigFromOpenRange()
if err != nil {
    fmt.Println("Error creating auto detect config:", err)
    return
}
defer autoDetectSourceLanguageConfig.Close()
```

Below is a more detailed example:

```go
// Live Interpreter: real-time speech-to-speech translation with personal voice.
package main

import (
    "fmt"
    "os"
    "sync"

    "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

func main() {
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    // Set your test WAV file here.
    // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    audioFile := "<TEST_FILE>"

    // Translation target language.
    targetLanguage := "zh-Hans"

    // Live Interpreter requires the universal v2 endpoint, created with FromEndpoint. Replace
    // YourResourceName with your Speech resource name. You can also use the regional form:
    //   wss://<region>.stt.speech.microsoft.com/speech/universal/v2
    endpoint := "wss://YourResourceName.cognitiveservices.azure.com/stt/speech/universal/v2"

    // Store your key securely (for example in an environment variable); never hardcode it in source.
    speechKey := os.Getenv("SPEECH_KEY")

    speechTranslationConfig, err := speech.NewSpeechTranslationConfigFromEndpointWithSubscription(endpoint, speechKey)
    if err != nil {
        fmt.Println("Error creating translation config:", err)
        return
    }
    defer speechTranslationConfig.Close()

    // Set the translation target language and enable personal voice.
    if err := speechTranslationConfig.AddTargetLanguage(targetLanguage); err != nil {
        fmt.Println("Error adding target language:", err)
        return
    }
    if err := speechTranslationConfig.SetVoiceName("personal-voice"); err != nil {
        fmt.Println("Error setting voice name:", err)
        return
    }

    // You don't need to define any candidate languages to detect.
    autoDetectSourceLanguageConfig, err := speech.NewAutoDetectSourceLanguageConfigFromOpenRange()
    if err != nil {
        fmt.Println("Error creating auto detect config:", err)
        return
    }
    defer autoDetectSourceLanguageConfig.Close()

    audioConfig, err := audio.NewAudioConfigFromWavFileInput(audioFile)
    if err != nil {
        fmt.Println("Error creating audio config:", err)
        return
    }
    defer audioConfig.Close()

    recognizer, err := speech.NewTranslationRecognizerFromAutoDetectSourceLangConfig(
        speechTranslationConfig, autoDetectSourceLanguageConfig, audioConfig)
    if err != nil {
        fmt.Println("Error creating translation recognizer:", err)
        return
    }
    defer recognizer.Close()

    stopTranslation := make(chan struct{})
    var stopOnce sync.Once
    signalStop := func() { stopOnce.Do(func() { close(stopTranslation) }) }

    // Index of the output audio files.
    audioIndex := 0

    recognizer.Recognizing(func(event speech.TranslationRecognitionEventArgs) {
        defer event.Close()
        lid := event.Result.Properties.GetProperty(common.SpeechServiceConnectionAutoDetectSourceLanguageResult, "")
        fmt.Printf("RECOGNIZING in '%s': Text=%s\n", lid, event.Result.Text)
        for lang, translation := range event.Result.GetTranslations() {
            fmt.Printf("    TRANSLATING into '%s': %s\n", lang, translation)
        }
    })

    recognizer.Recognized(func(event speech.TranslationRecognitionEventArgs) {
        defer event.Close()
        switch event.Result.Reason {
        case common.TranslatedSpeech:
            lid := event.Result.Properties.GetProperty(common.SpeechServiceConnectionAutoDetectSourceLanguageResult, "")
            fmt.Printf("RECOGNIZED in '%s': Text=%s\n", lid, event.Result.Text)
            for lang, translation := range event.Result.GetTranslations() {
                fmt.Printf("    TRANSLATED into '%s': %s\n", lang, translation)
            }
        case common.RecognizedSpeech:
            fmt.Printf("RECOGNIZED: Text=%s\n", event.Result.Text)
            fmt.Println("    Speech not translated.")
        case common.NoMatch:
            fmt.Println("NOMATCH: Speech could not be recognized.")
        }
    })

    recognizer.Synthesizing(func(event speech.TranslationSynthesisEventArgs) {
        defer event.Close()
        audioData := event.Result.GetAudioData()
        fmt.Printf("Audio synthesized: %d byte(s)\n", len(audioData))
        if len(audioData) > 0 {
            audioIndex++
            outputFile := fmt.Sprintf("YourAudioFile-%d.wav", audioIndex)
            if err := os.WriteFile(outputFile, audioData, 0644); err != nil {
                fmt.Println("Error writing audio:", err)
            }
        }
    })

    recognizer.Canceled(func(event speech.TranslationRecognitionCanceledEventArgs) {
        defer event.Close()
        // For file input, translation ends with Reason=EndOfStream — that is normal completion.
        fmt.Printf("CANCELED: Reason=%v\n", event.Reason)
        if event.Reason == common.Error {
            fmt.Printf("CANCELED: ErrorCode=%v\n", event.ErrorCode)
            fmt.Printf("CANCELED: ErrorDetails=%s\n", event.ErrorDetails)
            fmt.Println("CANCELED: Did you set the resource key and enable personal voice access?")
        }
        signalStop()
    })

    recognizer.SessionStopped(func(event speech.SessionEventArgs) {
        defer event.Close()
        fmt.Println("Session stopped.")
        signalStop()
    })

    fmt.Println("Start translation...")
    if err := <-recognizer.StartContinuousRecognitionAsync(); err != nil {
        fmt.Println("Error starting continuous recognition:", err)
        return
    }

    // Wait for completion (end-of-stream cancellation or session stop).
    <-stopTranslation

    if err := <-recognizer.StopContinuousRecognitionAsync(); err != nil {
        fmt.Println("Error stopping continuous recognition:", err)
    }
}
```

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]
