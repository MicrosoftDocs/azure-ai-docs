---
title: Audio processing - Speech service
titleSuffix: Foundry Tools
description: An overview of audio processing pipelines and capabilities of the Microsoft Audio Stack.
manager: nitinme
ms.service: azure-ai-speech
ms.topic: overview
ms.date: 03/05/2026
author: PatrickFarley
ms.author: pafarley
ms.reviewer: jagoerge
---

# Audio processing with the Microsoft Audio Stack

The Microsoft Audio Stack (MAS) is a set of audio processing enhancements optimized for speech processing scenarios such as keyword recognition and speech recognition. The Speech SDK integrates MAS, allowing any application or product to use its audio processing capabilities on input audio.

## Audio processing pipelines

The Microsoft Audio Stack provides two audio processing pipelines, each optimized for different scenarios:

### DSP-based pipeline (default)

The default pipeline (`AUDIO_INPUT_PROCESSING_ENABLE_DEFAULT`) uses traditional digital signal processing (DSP) algorithms and provides a full set of enhancements: beamforming, dereverberation, acoustic echo cancellation, automatic gain control, and noise suppression. You can disable individual enhancements to match your scenario. This pipeline supports all microphone array geometries and is available on Windows and Linux.

For details on DSP enhancements and code samples, see [DSP-based audio processing with the Microsoft Audio Stack](audio-processing-speech-sdk.md).

### Model-based echo cancellation pipeline

The model-based pipeline (`AUDIO_INPUT_PROCESSING_ENABLE_V2`) replaces the DSP-based echo canceller with a machine learning model for improved echo suppression. This pipeline focuses specifically on acoustic echo cancellation and is designed for scenarios where echo suppression quality is critical.

For details and code samples, see [Model-based echo cancellation with the Microsoft Audio Stack](audio-processing-model-based-aec.md).

### Pipeline comparison

#### Audio enhancements

| Feature | DSP-based (default) | Model-based (V2) |
|---------|:--------------------:|:-----------------:|
| Acoustic echo cancellation | &#x2714; | &#x2714;&#x2714; |
| Noise suppression | &#x2714; | &#x2718; |
| Dereverberation | &#x2714; | &#x2718; |
| Automatic gain control | &#x2714; | &#x2718; |
| Beamforming | &#x2714; | &#x2718; |
| Disable individual enhancements | &#x2714; | &#x2718; |

&#x2714;&#x2714; = ML-enhanced &nbsp;&nbsp; &#x2714; = Supported &nbsp;&nbsp; &#x2718; = Not supported

#### Platform and language support

| Feature | DSP-based (default) | Model-based (V2) |
|---------|:--------------------:|:-----------------:|
| Windows x64 | &#x2714; | &#x2714; |
| Windows ARM64 | &#x2714; | &#x2714; |
| Linux | &#x2714; | &#x2718; |
| C++ | &#x2714; | &#x2714; |
| C# | &#x2714; | &#x2714; |
| Java | &#x2714; | &#x2718; |

## Speech SDK integration

Both pipelines are available through the Speech SDK's `AudioProcessingOptions` class. Key capabilities include:
* **Real-time microphone input and file input** - Audio processing can be applied to real-time microphone input, streams, and file-based input.
* **Speaker reference channel** - A speaker reference channel can be specified for echo cancellation, using the `SpeakerReferenceChannel.LastChannel` option.

## Privacy and data handling

Processing is performed fully locally where the Speech SDK is being used. No audio data is streamed to Microsoft's cloud services for processing by the Microsoft Audio Stack. The only exception is the Conversation Transcription Service, where raw audio is sent to Microsoft's cloud services for processing.

## Related content

- [DSP-based audio processing with the Microsoft Audio Stack](audio-processing-speech-sdk.md)
- [Model-based echo cancellation with the Microsoft Audio Stack](audio-processing-model-based-aec.md)
