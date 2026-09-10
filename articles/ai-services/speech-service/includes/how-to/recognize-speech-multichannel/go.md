---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 07/30/2026
ms.author: pafarley
ms.custom: devx-track-go, doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/go.md)]

In this guide, you use the Speech SDK for Go to transcribe a stereo audio source and read a separate speech-to-text result for each channel.


## Prerequisites

- The [Speech SDK for Go](../../../quickstarts/setup-platform.md?pivots=programming-language-go) version 1.52.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

> [!NOTE]
> Until the release of SDK 1.52.0, download the current [Speech SDK Go source](https://github.com/microsoft/cognitive-services-speech-sdk-go/) directly.

## Create a speech configuration and enable multichannel processing

Create a `SpeechConfig` instance and enable multichannel processing. Replace
`YourSpeechEndpoint` and `YourSpeechKey` with your Speech resource endpoint and key.

```go
import (
    "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

speechConfig, err := speech.NewSpeechConfigFromEndpointWithSubscription(
    "YourSpeechEndpoint", "YourSpeechKey")
if err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer speechConfig.Close()
speechConfig.SetSpeechRecognitionLanguage("en-US")

// Enable per-channel transcription of up to two channels.
speechConfig.SetProperty(common.EnableMultiChannelProcessing, "true")
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an `AudioConfig` instance from the file name:

```go
import "github.com/Microsoft/cognitive-services-speech-sdk-go/audio"

audioConfig, err := audio.NewAudioConfigFromWavFileInput("stereo.wav")
if err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer audioConfig.Close()
```

For a real-time source, create the `AudioConfig` instance from a stream whose format specifies two channels, and write raw PCM audio (without the WAV header) to the stream as it becomes available.

## Recognize and read per-channel results

Create a `SpeechRecognizer` instance and use continuous recognition. Multichannel transcription supports continuous recognition only; single-shot recognition isn't supported.

Each recognition result carries a `Channel` field that identifies the source audio channel. Channel numbering starts at zero.

```go
import (
    "github.com/Microsoft/cognitive-services-speech-sdk-go/common"
    "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"
)

speechRecognizer, err := speech.NewSpeechRecognizerFromConfig(speechConfig, audioConfig)
if err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer speechRecognizer.Close()

speechRecognizer.Recognized(func(event speech.SpeechRecognitionEventArgs) {
    defer event.Close()
    // event.Result.Channel identifies the source channel (0 or 1).
    fmt.Printf("RECOGNIZED (channel %d): %s\n", event.Result.Channel, event.Result.Text)
})

// The Start and Stop methods return a channel that reports the outcome
// of the operation. Read from it to wait for the operation to complete.
if err := <-speechRecognizer.StartContinuousRecognitionAsync(); err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer func() { <-speechRecognizer.StopContinuousRecognitionAsync() }()
```

Use the channel value on each result to keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use a `ConversationTranscriber` instead of a `SpeechRecognizer`. The transcriber reports final results on the `Transcribed` event, and each result includes both the channel and the speaker ID.

```go
import "github.com/Microsoft/cognitive-services-speech-sdk-go/speech"

conversationTranscriber, err := speech.NewConversationTranscriberFromConfig(speechConfig, audioConfig)
if err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer conversationTranscriber.Close()

conversationTranscriber.Transcribed(func(event speech.ConversationTranscriptionEventArgs) {
    defer event.Close()
    fmt.Printf("TRANSCRIBED (channel %d, speaker %s): %s\n",
        event.Result.Channel, event.Result.SpeakerID, event.Result.Text)
})

if err := <-conversationTranscriber.StartTranscribingAsync(); err != nil {
    fmt.Println("Got an error: ", err)
    return
}
defer func() { <-conversationTranscriber.StopTranscribingAsync() }()
```
