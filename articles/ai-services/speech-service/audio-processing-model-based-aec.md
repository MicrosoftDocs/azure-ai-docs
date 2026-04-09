---
title: Model-based echo cancellation audio processing - Speech service
titleSuffix: Foundry Tools
description: An overview of model-based echo cancellation (V2) audio processing with the Microsoft Audio Stack for improved acoustic echo suppression.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 02/13/2026
author: PatrickFarley
ms.author: pafarley
ms.reviewer: jagoerge
ai-usage: ai-assisted
---

# Model-based echo cancellation with the Microsoft Audio Stack

The Microsoft Audio Stack (MAS) provides a model-based echo cancellation pipeline (`AUDIO_INPUT_PROCESSING_ENABLE_V2`) that uses machine learning models for enhanced acoustic echo suppression in voice call scenarios. This pipeline replaces the traditional DSP-based echo cancellation in the [default audio processing pipeline](audio-processing-overview.md) with a deep learning model, delivering improved echo suppression in challenging acoustic environments.

> [!IMPORTANT]
> This feature is only available on Windows x64 and ARM64 platforms.

## What is acoustic echo cancellation?

Acoustic echo cancellation (AEC) removes the echo that occurs when audio played from a device's loudspeaker is picked up by its microphone. Without AEC, the far-end participant hears their own voice played back, and speech recognition accuracy degrades because the recognizer processes the echoed audio along with the near-end speaker's voice.

AEC works by using a **reference channel** (also called loopback audio) that captures the audio being played out of the device. The echo canceller compares this reference signal with the microphone input, identifies the echo component, and subtracts it — leaving only the near-end speaker's voice for speech recognition or transmission.

AEC is essential in scenarios such as:

* **Hands-free voice assistants** - The device plays prompts or music while the user speaks.
* **Video conferencing** - Both parties speak while audio is rendered from the loudspeaker.
* **Smart speakers and displays** - The device outputs audio continuously and must still respond to voice commands.

## How model-based echo cancellation works

The model-based echo cancellation pipeline (`AUDIO_INPUT_PROCESSING_ENABLE_V2`) uses a machine learning model for improved echo cancellation performance:

* **Improved echo suppression** - The ML model adapts more effectively to complex acoustic environments, reducing residual echo that traditional DSP approaches might leave behind.
* **Better handling of nonlinear distortions** - The model can learn and compensate for nonlinear distortions introduced by loudspeaker playback, which are difficult for linear DSP methods to address.

> [!NOTE]
> `AUDIO_INPUT_PROCESSING_ENABLE_V2` is mutually exclusive with `AUDIO_INPUT_PROCESSING_ENABLE_DEFAULT`. You can't combine these flags. The `AUDIO_INPUT_PROCESSING_DISABLE_*` flags don't affect the V2 pipeline.

## Speech SDK integration

The model-based echo cancellation pipeline is available through the Speech SDK's `AudioProcessingOptions` class. Some key features include:

* **Real-time microphone input and file input** - Model-based echo cancellation processing can be applied to real-time microphone input, audio streams, and file-based input.
* **Speaker reference channel** - A speaker reference channel can be specified for echo cancellation, using the `SpeakerReferenceChannel.LastChannel` option.

### Usage examples

The following examples demonstrate how to use the model-based echo cancellation pipeline with different input sources.

> [!NOTE]
> Echo cancellation requires both microphone audio and a speaker reference (loopback) channel. When reading from files, use a multi-channel WAV file where the last channel contains the speaker reference audio, and provide it through a `PullAudioInputStream`.

#### Multi-channel file input with pull stream

This example reads a 2-channel WAV file (1 microphone channel + 1 speaker reference channel) through a pull audio stream. The `SpeakerReferenceChannel.LastChannel` option tells MAS that the last channel in the audio contains the speaker reference for echo cancellation.

### [C#](#tab/csharp)

```csharp
var speechConfig = SpeechConfig.FromEndpoint(
    new Uri("YourSpeechEndpoint"), "YourSpeechKey");

var audioProcessingOptions = AudioProcessingOptions.Create(
    AudioProcessingConstants.AUDIO_INPUT_PROCESSING_ENABLE_V2,
    PresetMicrophoneArrayGeometry.Mono,
    SpeakerReferenceChannel.LastChannel);

// Create a pull stream with 2-channel PCM format
// (1 mic channel + 1 speaker reference channel)
var audioFormat = AudioStreamFormat.GetWaveFormatPCM(
    16000, 16, 2);
var pullStream = AudioInputStream.CreatePullStream(
    audioFormat, pullStreamCallback);
var audioInput = AudioConfig.FromStreamInput(
    pullStream, audioProcessingOptions);

var recognizer = new SpeechRecognizer(speechConfig, audioInput);
```

### [C++](#tab/cpp)

```cpp
auto speechConfig = SpeechConfig::FromEndpoint(
    "YourServiceEndpoint", "YourSpeechKey");

auto audioProcessingOptions = AudioProcessingOptions::Create(
    AUDIO_INPUT_PROCESSING_ENABLE_V2,
    PresetMicrophoneArrayGeometry::Mono,
    SpeakerReferenceChannel::LastChannel);

// Create a pull stream with 2-channel PCM format
// (1 mic channel + 1 speaker reference channel)
auto pullStream = AudioInputStream::CreatePullStream(
    AudioStreamFormat::GetWaveFormatPCM(16000, 16, 2),
    [reader](uint8_t* buffer, uint32_t size) -> int {
        return reader->Read(buffer, size);
    },
    [=]() { /* close callback */ });
auto audioInput = AudioConfig::FromStreamInput(
    pullStream, audioProcessingOptions);

auto recognizer = SpeechRecognizer::FromConfig(
    speechConfig, audioInput);
```

---

#### Default microphone input

On Windows, the Speech SDK automatically gathers the speaker reference channel from the system audio loopback when `SpeakerReferenceChannel.LastChannel` is specified. 

### [C#](#tab/csharp)

```csharp
var speechConfig = SpeechConfig.FromEndpoint(
    new Uri("YourSpeechEndpoint"), "YourSpeechKey");

var audioProcessingOptions = AudioProcessingOptions.Create(
    AudioProcessingConstants.AUDIO_INPUT_PROCESSING_ENABLE_V2,
    PresetMicrophoneArrayGeometry.Mono,
    SpeakerReferenceChannel.LastChannel);
var audioInput = AudioConfig.FromDefaultMicrophoneInput(
    audioProcessingOptions);

var recognizer = new SpeechRecognizer(speechConfig, audioInput);
```

### [C++](#tab/cpp)

```cpp
auto speechConfig = SpeechConfig::FromEndpoint(
    "YourServiceEndpoint", "YourSpeechKey");

auto audioProcessingOptions = AudioProcessingOptions::Create(
    AUDIO_INPUT_PROCESSING_ENABLE_V2,
    PresetMicrophoneArrayGeometry::Mono,
    SpeakerReferenceChannel::LastChannel);
auto audioInput = AudioConfig::FromDefaultMicrophoneInput(
    audioProcessingOptions);

auto recognizer = SpeechRecognizer::FromConfig(
    speechConfig, audioInput);
```

---

## Requirements

To use the model-based echo cancellation pipeline, your environment must meet these requirements:

* **Platform** - Windows x64 or ARM64. Set your project's platform target to `x64` or `ARM64` (not `Any CPU`).
* **Speech SDK version** - v1.33.0 or newer. The `Microsoft.CognitiveServices.Speech.Extension.MAS` package must be installed on Windows.
* **Raw audio** - Microsoft Audio Stack requires raw (unprocessed) audio as input for best results.
* **Loopback or reference audio** - An audio channel that represents the audio being played out of the device is required to perform acoustic echo cancellation. 
* **Input format** - Microsoft Audio Stack supports down sampling for sample rates that are integral multiples of 16 kHz. A minimum sampling rate of 16 kHz is required. Supported formats: 32-bit IEEE little endian float, 32-bit little endian signed int, 24-bit little endian signed int, 16-bit little endian signed int, and 8-bit signed int.

## When to use model-based echo cancellation

Consider using the V2 model-based echo cancellation pipeline when:

* **Echo suppression is critical** - Your application requires high-quality echo suppression, such as in hands-free voice interaction scenarios.
* **The default pipeline leaves residual echo** - If the DSP-based echo cancellation in the default pipeline doesn't sufficiently suppress echo in your environment.

Use the default pipeline (`AUDIO_INPUT_PROCESSING_ENABLE_DEFAULT`) when:

* **You need individual enhancement control** - The default pipeline allows you to disable specific enhancements like dereverberation or noise suppression.
* **Cross-platform support is required** - The default pipeline is available on both Windows and Linux.

## Language and platform support

| Language | Platform | Reference docs |
|----------|----------|----------------|
| C++ | Windows x64, Windows ARM64 | [C++ docs](/cpp/cognitive-services/speech/) |
| C# | Windows x64, Windows ARM64 | [C# docs](/dotnet/api/microsoft.cognitiveservices.speech) |

## Related content

- [Audio processing with the Microsoft Audio Stack](audio-processing-overview.md)
- [Use the Microsoft Audio Stack (MAS)](audio-processing-speech-sdk.md)
