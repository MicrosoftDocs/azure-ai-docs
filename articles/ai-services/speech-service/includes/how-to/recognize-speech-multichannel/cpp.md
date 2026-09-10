---
author: PatrickFarley
ms.service: azure-speech-foundry-tools
ms.topic: include
ms.date: 08/05/2026
ms.author: pafarley
ms.custom: doc-kit-assisted
ms.devlang: cpp
ai-usage: ai-assisted
---

[!INCLUDE [Header](../../common/cpp.md)]

In this guide, you use the Speech SDK for C++ to transcribe a stereo audio source and read a separate speech-to-text result for each channel.

## Prerequisites

- The [Speech SDK for C++](../../../quickstarts/setup-platform.md?pivots=programming-language-cpp) version 1.51.0 or later.
- A two-channel (stereo) WAV file or a stereo audio stream. The Speech service transcribes up to two channels.

## Create a speech configuration and enable multichannel processing

Create a [`SpeechConfig`](/cpp/cognitive-services/speech/speechconfig) instance and set the
`Speech_EnableMultiChannelProcessing` property to `true`. Replace `YourSpeechEndpoint` and
`YourSpeechKey` with your Speech resource endpoint and key.

```cpp
#include <speechapi_cxx.h>

using namespace Microsoft::CognitiveServices::Speech;
using namespace Microsoft::CognitiveServices::Speech::Audio;
using namespace Microsoft::CognitiveServices::Speech::Transcription;

auto speechConfig = SpeechConfig::FromEndpoint(
    "YourSpeechEndpoint", "YourSpeechKey");
speechConfig->SetSpeechRecognitionLanguage("en-US");

// Enable per-channel transcription of up to two channels.
speechConfig->SetProperty(PropertyId::Speech_EnableMultiChannelProcessing, "true");
```

## Provide stereo audio

Multichannel transcription accepts a stereo audio file or a stereo stream. To transcribe a file, create an [`AudioConfig`](/cpp/cognitive-services/speech/audio-audioconfig) instance from the file name:

```cpp
auto audioConfig = AudioConfig::FromWavFileInput("stereo.wav");
```

For a real-time source, create the `AudioConfig` instance from a push or pull stream. When you create the stream format, set the channel count to `2`:

```cpp
// Match the format of your stereo source: sample rate, bits per sample, and 2 channels.
auto streamFormat = AudioStreamFormat::GetWaveFormatPCM(16000, 16, 2);
auto pushStream = AudioInputStream::CreatePushStream(streamFormat);
auto audioConfig = AudioConfig::FromStreamInput(pushStream);

// Write raw PCM audio (without the WAV header) to pushStream as it becomes available,
// and call pushStream->Close() when the source ends.
```

## Recognize and read per-channel results

Create a [`SpeechRecognizer`](/cpp/cognitive-services/speech/speechrecognizer) instance and use continuous recognition. Each final result includes the source channel from the `Channel()` method. Multichannel transcription supports continuous recognition only; single-shot recognition (`RecognizeOnceAsync`) isn't supported.

```cpp
#include <atomic>
#include <future>

auto recognizer = SpeechRecognizer::FromConfig(speechConfig, audioConfig);
std::promise<void> recognitionEnd;
std::atomic<bool> recognitionEnded{false};

auto signalRecognitionEnd = [&recognitionEnd, &recognitionEnded]()
{
    if (!recognitionEnded.exchange(true))
    {
        recognitionEnd.set_value();
    }
};

recognizer->Recognized.Connect([](const SpeechRecognitionEventArgs& e)
{
    if (e.Result->Reason == ResultReason::RecognizedSpeech)
    {
        printf("RECOGNIZED (channel %d): %s\n", e.Result->Channel(), e.Result->Text.c_str());
    }
});

recognizer->Canceled.Connect([&signalRecognitionEnd](const SpeechRecognitionCanceledEventArgs& e)
{
    if (e.Reason == CancellationReason::Error)
    {
        signalRecognitionEnd();
    }
});

recognizer->SessionStopped.Connect([&signalRecognitionEnd](const SessionEventArgs& e)
{
    signalRecognitionEnd();
});

recognizer->StartContinuousRecognitionAsync().get();
recognitionEnd.get_future().get();
recognizer->StopContinuousRecognitionAsync().get();
```

The `Channel()` method returns the zero-based channel that produced the result, so you can keep each channel's transcript separate.

## Combine multichannel transcription with diarization

To also identify speakers within each channel, use a [`ConversationTranscriber`](/cpp/cognitive-services/speech/transcription-conversationtranscriber) instead of a `SpeechRecognizer`. The transcriber reports final results on the `Transcribed` event, and each result includes both the channel and the speaker ID.

```cpp
auto conversationTranscriber = ConversationTranscriber::FromConfig(speechConfig, audioConfig);
std::promise<void> transcriptionEnd;
std::atomic<bool> transcriptionEnded{false};

auto signalTranscriptionEnd = [&transcriptionEnd, &transcriptionEnded]()
{
    if (!transcriptionEnded.exchange(true))
    {
        transcriptionEnd.set_value();
    }
};

conversationTranscriber->Transcribed.Connect([](const ConversationTranscriptionEventArgs& e)
{
    if (e.Result->Reason == ResultReason::RecognizedSpeech)
    {
        printf("TRANSCRIBED (channel %d, speaker %s): %s\n",
            e.Result->Channel(), e.Result->SpeakerId.c_str(), e.Result->Text.c_str());
    }
});

conversationTranscriber->Canceled.Connect([&signalTranscriptionEnd](const ConversationTranscriptionCanceledEventArgs& e)
{
    if (e.Reason == CancellationReason::Error)
    {
        signalTranscriptionEnd();
    }
});

conversationTranscriber->SessionStopped.Connect([&signalTranscriptionEnd](const SessionEventArgs& e)
{
    signalTranscriptionEnd();
});

conversationTranscriber->StartTranscribingAsync().get();
transcriptionEnd.get_future().get();
conversationTranscriber->StopTranscribingAsync().get();
```
