---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: devx-track-extended-java, doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/java.md)]

In this guide, you use the Speech SDK for Java to transcribe a stereo audio source and read a separate speech-to-text result for each channel.


## Prerequisites

- The [Speech SDK for Java](../../../quickstarts/setup-platform.md?pivots=programming-language-java) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create a [`SpeechConfig`](/java/api/com.microsoft.cognitiveservices.speech.speechconfig) instance and
set the `Speech_EnableMultiChannelProcessing` property to `true`. Replace `YourSpeechEndpoint` and
`YourSpeechKey` with your Speech resource endpoint and key.

```java
import com.microsoft.cognitiveservices.speech.*;
import com.microsoft.cognitiveservices.speech.audio.*;
import com.microsoft.cognitiveservices.speech.transcription.*;
import java.net.URI;

SpeechConfig speechConfig = SpeechConfig.fromEndpoint(
    new URI("YourSpeechEndpoint"), "YourSpeechKey");
speechConfig.setSpeechRecognitionLanguage("en-US");

// Enable per-channel transcription of up to two channels.
speechConfig.setProperty(PropertyId.Speech_EnableMultiChannelProcessing, "true");
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an [`AudioConfig`](/java/api/com.microsoft.cognitiveservices.speech.audio.audioconfig) instance from the file name:

```java
AudioConfig audioConfig = AudioConfig.fromWavFileInput("stereo.wav");
```

For a real-time source, create the `AudioConfig` instance from a push or pull stream. When you create the stream format, set the channel count to `2`:

```java
// Match the format of your stereo source: sample rate, bits per sample, and 2 channels.
AudioStreamFormat streamFormat = AudioStreamFormat.getWaveFormatPCM(16000, (short)16, (short)2);
PushAudioInputStream pushStream = AudioInputStream.createPushStream(streamFormat);
AudioConfig audioConfig = AudioConfig.fromStreamInput(pushStream);

// Write raw PCM audio (without the WAV header) to pushStream as it becomes available,
// and call pushStream.close() when the source ends.
```

## Recognize and read per-channel results

Create a [`SpeechRecognizer`](/java/api/com.microsoft.cognitiveservices.speech.speechrecognizer) instance and use continuous recognition. Each final result includes the source channel from the `getChannel()` method. Multichannel transcription supports continuous recognition only; single-shot recognition (`recognizeOnceAsync`) isn't supported.

```java
import java.util.concurrent.Semaphore;

SpeechRecognizer recognizer = new SpeechRecognizer(speechConfig, audioConfig);
Semaphore recognitionEnd = new Semaphore(0);

recognizer.recognized.addEventListener((s, e) -> {
    if (e.getResult().getReason() == ResultReason.RecognizedSpeech) {
        System.out.println("RECOGNIZED (channel " + e.getResult().getChannel() + "): " + e.getResult().getText());
    }
});

recognizer.canceled.addEventListener((s, e) -> {
    if (e.getReason() == CancellationReason.Error) {
        recognitionEnd.release();
    }
});

recognizer.sessionStopped.addEventListener((s, e) -> recognitionEnd.release());

recognizer.startContinuousRecognitionAsync().get();
recognitionEnd.acquire();
recognizer.stopContinuousRecognitionAsync().get();

recognizer.close();
```

The `getChannel()` method returns the zero-based channel that produced the result, so you can keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use a [`ConversationTranscriber`](/java/api/com.microsoft.cognitiveservices.speech.transcription.conversationtranscriber) instead of a `SpeechRecognizer`. The transcriber reports final results on the `transcribed` event, and each result includes both the channel and the speaker ID.

```java
ConversationTranscriber conversationTranscriber = new ConversationTranscriber(speechConfig, audioConfig);
Semaphore transcriptionEnd = new Semaphore(0);

conversationTranscriber.transcribed.addEventListener((s, e) -> {
    if (e.getResult().getReason() == ResultReason.RecognizedSpeech) {
        System.out.println("TRANSCRIBED (channel " + e.getResult().getChannel()
            + ", speaker " + e.getResult().getSpeakerId() + "): " + e.getResult().getText());
    }
});

conversationTranscriber.canceled.addEventListener((s, e) -> {
    if (e.getReason() == CancellationReason.Error) {
        transcriptionEnd.release();
    }
});

conversationTranscriber.sessionStopped.addEventListener((s, e) -> transcriptionEnd.release());

conversationTranscriber.startTranscribingAsync().get();
transcriptionEnd.acquire();
conversationTranscriber.stopTranscribingAsync().get();

conversationTranscriber.close();
```
