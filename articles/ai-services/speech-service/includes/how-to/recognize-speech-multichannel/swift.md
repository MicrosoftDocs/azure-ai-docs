---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/swift.md)]

In this guide, you use the Speech SDK for Swift to transcribe a stereo audio source and read a separate speech to text result for each channel.

## Prerequisites

- The [Speech SDK for Swift](../../../quickstarts/setup-platform.md?pivots=programming-language-swift) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create an `SPXSpeechConfiguration` instance and enable multichannel processing. Replace
`YourSpeechEndpoint` and `YourSpeechKey` with your Speech resource endpoint and key.

```swift
let speechConfig = try! SPXSpeechConfiguration(
    endpoint: "YourSpeechEndpoint", subscription: "YourSpeechKey")
speechConfig.speechRecognitionLanguage = "en-US"

// Enable per-channel transcription of up to two channels.
speechConfig.setPropertyTo("true", by: SPXPropertyId.speechEnableMultiChannelProcessing)
```

The multichannel property is available in the Speech SDK version 1.51.0 or later. If you use an earlier SDK, set the same property by name for backward compatibility:

```swift
speechConfig.setPropertyTo("true", byName: "SPEECH-EnableMultiChannelProcessing")
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an `SPXAudioConfiguration` instance from the file name:

```swift
let audioConfig = SPXAudioConfiguration(wavFileInput: "stereo.wav")
```

For a real-time source, create the `SPXAudioConfiguration` instance from a stream whose format specifies two channels, and write raw PCM audio (without the WAV header) to the stream as it becomes available.

## Recognize and read per-channel results

Create an `SPXSpeechRecognizer` instance and use continuous recognition. Multichannel transcription supports continuous recognition only; single-shot recognition (`recognizeOnce`) isn't supported.

```swift
let recognizer = try! SPXSpeechRecognizer(speechConfiguration: speechConfig, audioConfiguration: audioConfig!)

recognizer.addRecognizedEventHandler { recognizer, evt in
    guard let result = evt.result else {
        return
    }

    if result.reason == SPXResultReason.recognizedSpeech {
        // result.channel identifies the source channel (0 or 1).
        print("RECOGNIZED (channel \(result.channel)): \(result.text ?? "")")
    }
}

try! recognizer.startContinuousRecognition()
```

Use the channel value on each result to keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use an `SPXConversationTranscriber` instead of an `SPXSpeechRecognizer`. The transcriber reports final results on the transcribed event, and each result includes both the channel and the speaker ID.

```swift
let conversationTranscriber = try! SPXConversationTranscriber(speechConfiguration: speechConfig, audioConfiguration: audioConfig!)

conversationTranscriber.addTranscribedEventHandler { transcriber, evt in
    guard let result = evt.result else {
        return
    }

    if result.reason == SPXResultReason.recognizedSpeech {
        print("TRANSCRIBED (channel \(result.channel), speaker \(result.speakerId ?? "")): \(result.text ?? "")")
    }
}

do {
    try conversationTranscriber.startTranscribingAsync { started, error in
        if let error = error {
            print("Could not start transcription: \(error)")
        } else if started {
            print("Transcription started")
        }
    }
} catch {
    print("Could not start transcription: \(error)")
}
```

When transcription is complete, stop the transcriber:

```swift
do {
    try conversationTranscriber.stopTranscribingAsync { stopped, error in
        if let error = error {
            print("Could not stop transcription: \(error)")
        } else if stopped {
            print("Transcription stopped")
        }
    }
} catch {
    print("Could not stop transcription: \(error)")
}
```
