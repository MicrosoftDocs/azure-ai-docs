---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: devx-track-python, doc-kit-assisted
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/python.md)]

In this guide, you use the Speech SDK for Python to transcribe a stereo audio source and read a separate speech-to-text result for each channel.

## Prerequisites

- The [Speech SDK for Python](../../../quickstarts/setup-platform.md?pivots=programming-language-python) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create a [`SpeechConfig`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig)
instance and set the `Speech_EnableMultiChannelProcessing` property to `true`. Replace
`YourSpeechEndpoint` and `YourSpeechKey` with your Speech resource endpoint and key.

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="YourSpeechKey", endpoint="YourSpeechEndpoint")
speech_config.speech_recognition_language = "en-US"

# Enable per-channel transcription of up to two channels.
speech_config.set_property(speechsdk.PropertyId.Speech_EnableMultiChannelProcessing, "true")
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an [`AudioConfig`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.audio.audioconfig) instance from the file name:

```python
audio_config = speechsdk.audio.AudioConfig(filename="stereo.wav")
```

For a real-time source, create the `AudioConfig` instance from a push or pull stream. When you create the stream format, set the channel count to `2`:

```python
# Match the format of your stereo source: sample rate, bits per sample, and 2 channels.
stream_format = speechsdk.audio.AudioStreamFormat(samples_per_second=16000, bits_per_sample=16, channels=2)
push_stream = speechsdk.audio.PushAudioInputStream(stream_format=stream_format)
audio_config = speechsdk.audio.AudioConfig(stream=push_stream)

# Write raw PCM audio (without the WAV header) to push_stream as it becomes available,
# and call push_stream.close() when the source ends.
```

## Recognize and read per-channel results

Create a [`SpeechRecognizer`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechrecognizer) instance and use continuous recognition. Each final result includes the source channel in the `channel` property. Multichannel transcription supports continuous recognition only; single-shot recognition (`recognize_once`) isn't supported.

```python
import time

speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

done = False

def recognized_cb(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("RECOGNIZED (channel {}): {}".format(evt.result.channel, evt.result.text))

def stop_cb(evt):
    global done
    done = True

speech_recognizer.recognized.connect(recognized_cb)
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(0.5)
speech_recognizer.stop_continuous_recognition()
```

The `channel` property identifies the zero-based channel that produced the result, so you can keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use a [`ConversationTranscriber`](/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.transcription.conversationtranscriber) instead of a `SpeechRecognizer`. The transcriber reports final results on the `transcribed` event, and each result includes both the `channel` and the `speaker_id`.

```python
import time

conversation_transcriber = speechsdk.transcription.ConversationTranscriber(
    speech_config=speech_config, audio_config=audio_config)

done = False

def transcribed_cb(evt):
    if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("TRANSCRIBED (channel {}, speaker {}): {}".format(
            evt.result.channel, evt.result.speaker_id, evt.result.text))

def stop_cb(evt):
    global done
    done = True

conversation_transcriber.transcribed.connect(transcribed_cb)
conversation_transcriber.session_stopped.connect(stop_cb)
conversation_transcriber.canceled.connect(stop_cb)

conversation_transcriber.start_transcribing_async().get()
while not done:
    time.sleep(0.5)
conversation_transcriber.stop_transcribing_async().get()
```
