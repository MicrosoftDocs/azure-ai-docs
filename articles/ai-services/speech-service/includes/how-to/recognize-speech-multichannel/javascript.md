---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: devx-track-js, doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/javascript.md)]

In this guide, you use the Speech SDK for JavaScript to transcribe a stereo audio source and read a separate speech-to-text result for each channel.

## Prerequisites

- The [Speech SDK for JavaScript](../../../quickstarts/setup-platform.md?pivots=programming-language-javascript) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create a [`SpeechConfig`](/javascript/api/microsoft-cognitiveservices-speech-sdk/speechconfig)
instance and set the `Speech_EnableMultiChannelProcessing` property to `true`. Replace
`YourSpeechEndpoint` and `YourSpeechKey` with your Speech resource endpoint and key.

```javascript
const sdk = require("microsoft-cognitiveservices-speech-sdk");

const speechConfig = sdk.SpeechConfig.fromEndpoint(
    new URL("YourSpeechEndpoint"), "YourSpeechKey");
speechConfig.speechRecognitionLanguage = "en-US";

// Enable per-channel transcription of up to two channels.
speechConfig.setProperty(sdk.PropertyId.Speech_EnableMultiChannelProcessing, "true");
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an [`AudioConfig`](/javascript/api/microsoft-cognitiveservices-speech-sdk/audioconfig) instance from the file:

```javascript
const fs = require("fs");
const audioConfig = sdk.AudioConfig.fromWavFileInput(fs.readFileSync("stereo.wav"));
```

For a real-time source, create the `AudioConfig` instance from a push stream. When you create the stream format, set the channel count to `2`:

```javascript
// Match the format of your stereo source: sample rate, bits per sample, and 2 channels.
const streamFormat = sdk.AudioStreamFormat.getWaveFormatPCM(16000, 16, 2);
const pushStream = sdk.AudioInputStream.createPushStream(streamFormat);
const audioConfig = sdk.AudioConfig.fromStreamInput(pushStream);

// Write raw PCM audio (without the WAV header) to pushStream as it becomes available,
// and call pushStream.close() when the source ends.
```

## Recognize and read per-channel results

Create a [`SpeechRecognizer`](/javascript/api/microsoft-cognitiveservices-speech-sdk/speechrecognizer) instance and use continuous recognition. Multichannel transcription supports continuous recognition only; single-shot recognition (`recognizeOnceAsync`) isn't supported.

```javascript
const recognizer = new sdk.SpeechRecognizer(speechConfig, audioConfig);

recognizer.recognized = (s, e) => {
    if (e.result.reason === sdk.ResultReason.RecognizedSpeech) {
        // e.result.channel identifies the source channel (0 or 1).
        console.log(`RECOGNIZED (channel ${e.result.channel}): ${e.result.text}`);
    }
};

recognizer.sessionStopped = (s, e) => {
    recognizer.stopContinuousRecognitionAsync();
};

recognizer.startContinuousRecognitionAsync();
```

Use the channel value on each result to keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To identify speakers, use a [`ConversationTranscriber`](/javascript/api/microsoft-cognitiveservices-speech-sdk/conversationtranscriber) instead of a `SpeechRecognizer`. The transcriber reports final results on the `transcribed` event, and each result includes a speaker ID.

> [!IMPORTANT]
> In Speech SDK for JavaScript version 1.51.0, `ConversationTranscriber` results don't reliably report the source channel. A fix is planned for version 1.52.0. If you use version 1.51.0, use `speakerId` to identify speakers, but don't use `channel` to separate diarization results by source channel. Use `SpeechRecognizer` when you need reliable source-channel metadata.

```javascript
const conversationTranscriber = new sdk.ConversationTranscriber(speechConfig, audioConfig);

conversationTranscriber.transcribed = (s, e) => {
    if (e.result.reason === sdk.ResultReason.RecognizedSpeech) {
        console.log(`TRANSCRIBED (speaker ${e.result.speakerId}): ${e.result.text}`);
    }
};

conversationTranscriber.sessionStopped = (s, e) => {
    conversationTranscriber.stopTranscribingAsync();
};

conversationTranscriber.startTranscribingAsync();
```
