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

The Speech SDK is available as a Go package. You install the Speech SDK later in this guide. For any other requirements, see [Install the Speech SDK](../../../quickstarts/setup-platform.md?pivots=programming-language-go).

### Set environment variables

[!INCLUDE [Environment variables](../../common/environment-variables-resourcekey-endpoint.md)]

## Recognize speech from a microphone

Follow these steps to create a Go application and install the Speech SDK.

1. Open a command prompt window in the folder where you want the new project. Run this command to create a new Go file.

   ```bash
   touch main.go
   ```

1. Replace the contents of *main.go* with the following code:

   ```go
   package main

   import (
       "fmt"
       "os"

       "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"
       "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
   )

   func main() {
       // This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
       speechKey := os.Getenv("SPEECH_KEY")
       endpoint := os.Getenv("ENDPOINT")

       speechConfig, err := speech.NewSpeechConfigFromEndpointWithSubscription(endpoint, speechKey)
       if err != nil {
           fmt.Println("Got an error: ", err)
           return
       }
       defer speechConfig.Close()

       audioConfig, err := audio.NewAudioConfigFromDefaultMicrophoneInput()
       if err != nil {
           fmt.Println("Got an error: ", err)
           return
       }
       defer audioConfig.Close()

       speechRecognizer, err := speech.NewSpeechRecognizerFromConfig(speechConfig, audioConfig)
       if err != nil {
           fmt.Println("Got an error: ", err)
           return
       }
       defer speechRecognizer.Close()

       fmt.Println("Speak into your microphone.")
       outcome := <-speechRecognizer.RecognizeOnceAsync()
       defer outcome.Close()
       if outcome.Error != nil {
           fmt.Println("Got an error: ", outcome.Error)
           return
       }

       fmt.Println("RECOGNIZED: Text=", outcome.Result.Text)
   }
   ```

1. To change the speech recognition language, replace `en-US` with another [supported language](~/articles/ai-services/speech-service/language-support.md). For example, use `es-ES` for Spanish (Spain). If you don't specify a language, the default is `en-US`. For details about how to identify one of multiple languages that might be spoken, see [Language identification](~/articles/ai-services/speech-service/language-identification.md).

1. Run your new Go application to start speech recognition from a microphone:

   ```cmd
   go mod init speech-recognition
   go get github.com/Microsoft/cognitive-services-speech-sdk-go
   ```

   > [!IMPORTANT]
   > Make sure that you set the `SPEECH_KEY` and `ENDPOINT` [environment variables](#set-environment-variables). If you don't set these variables, the sample fails with an error message.

1. Speak into your microphone when prompted. What you speak should appear as text:

   ```output
   Speak into your microphone.
   RECOGNIZED: Text=I'm excited to try speech to text.
   ```

## Remarks

Here are some other considerations:

- This example uses the `RecognizeOnceAsync` operation to transcribe utterances of up to 30 seconds, or until silence is detected. For information about continuous recognition for longer audio, including multi-lingual conversations, see [How to recognize speech](~/articles/ai-services/speech-service/how-to-recognize-speech.md).
- To recognize speech from an audio file, use `NewAudioConfigFromWavFileInput` instead of `NewAudioConfigFromDefaultMicrophoneInput`:

   ```go
   audioConfig, err := audio.NewAudioConfigFromWavFileInput("YourAudioFile.wav")
   if err != nil {
       fmt.Println("Got an error: ", err)
       return
   }
   defer audioConfig.Close()
   ```

- For compressed audio files such as MP4, install GStreamer and use `PullAudioInputStream` or `PushAudioInputStream`. For more information, see [How to use compressed input audio](~/articles/ai-services/speech-service/how-to-use-codec-compressed-audio-input-streams.md).

## Clean up resources

[!INCLUDE [Delete resource](../../common/delete-resource.md)]  
