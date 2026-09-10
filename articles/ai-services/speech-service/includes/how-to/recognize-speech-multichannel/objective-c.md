---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/objectivec.md)]

In this guide, you use the Speech SDK for Objective-C to transcribe a stereo audio source and read a separate speech to text result for each channel.

## Prerequisites

- The [Speech SDK for Objective-C](../../../quickstarts/setup-platform.md?pivots=programming-language-objectivec) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create an `SPXSpeechConfiguration` instance and set the
`SPXSpeechEnableMultiChannelProcessing` property to `true`. Replace `YourSpeechEndpoint` and
`YourSpeechKey` with your Speech resource endpoint and key.

```objectivec
SPXSpeechConfiguration *speechConfig = [[SPXSpeechConfiguration alloc]
    initWithEndpoint:@"YourSpeechEndpoint" subscription:@"YourSpeechKey"];
speechConfig.speechRecognitionLanguage = @"en-US";

// Enable per-channel transcription of up to two channels.
[speechConfig setPropertyTo:@"true" byId:SPXSpeechEnableMultiChannelProcessing];
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an `SPXAudioConfiguration` instance from the file name:

```objectivec
SPXAudioConfiguration *audioConfig = [[SPXAudioConfiguration alloc] initWithWavFileInput:@"stereo.wav"];
```

For a real-time source, create the `SPXAudioConfiguration` instance from a stream whose format specifies two channels, and write raw PCM audio (without the WAV header) to the stream as it becomes available.

## Recognize and read per-channel results

Create an `SPXSpeechRecognizer` instance and use continuous recognition. Multichannel transcription supports continuous recognition only; single-shot recognition (`recognizeOnce`) isn't supported.

```objectivec
SPXSpeechRecognizer *recognizer = [[SPXSpeechRecognizer alloc] initWithSpeechConfiguration:speechConfig audioConfiguration:audioConfig];

[recognizer addRecognizedEventHandler:^(SPXSpeechRecognizer *recognizer, SPXSpeechRecognitionEventArgs *evt) {
    SPXSpeechRecognitionResult *result = evt.result;
    if (result != nil && result.reason == SPXResultReason_RecognizedSpeech) {
        // result.channel identifies the source channel (0 or 1).
        NSLog(@"RECOGNIZED (channel %ld): %@", (long)result.channel, result.text);
    }
}];

[recognizer startContinuousRecognition];
```

Use the channel value on each result to keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use an `SPXConversationTranscriber` instead of an `SPXSpeechRecognizer`. The transcriber reports final results on the transcribed event, and each result includes both the channel and the speaker ID.

```objectivec
SPXConversationTranscriber *conversationTranscriber = [[SPXConversationTranscriber alloc] initWithSpeechConfiguration:speechConfig audioConfiguration:audioConfig];

[conversationTranscriber addTranscribedEventHandler:^(SPXConversationTranscriber *transcriber, SPXConversationTranscriptionEventArgs *evt) {
    SPXConversationTranscriptionResult *result = evt.result;
    if (result != nil && result.reason == SPXResultReason_RecognizedSpeech) {
        NSLog(@"TRANSCRIBED (channel %ld, speaker %@): %@", (long)result.channel, result.speakerId, result.text);
    }
}];

[conversationTranscriber startTranscribingAsync:^(BOOL started, NSError *error) {
    if (!started || error != nil) {
        NSLog(@"Could not start transcription: %@", error);
    }
}];
```

When transcription is complete, stop the transcriber:

```objectivec
[conversationTranscriber stopTranscribingAsync:^(BOOL stopped, NSError *error) {
    if (!stopped || error != nil) {
        NSLog(@"Could not stop transcription: %@", error);
    }
}];
```