---
title: "How to transcribe multichannel audio in real time - Speech service"
titleSuffix: Foundry Tools
description: Learn how to transcribe up to two audio channels independently in real time and read per-channel speech to text results with the Speech SDK.
author: PatrickFarley
manager: mcleans
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 08/05/2026
ms.author: pafarley
ms.devlang: cpp
ms.custom: devx-track-extended-java, devx-track-go, devx-track-js, devx-track-python, doc-kit-assisted
zone_pivot_groups: programming-languages-speech-multichannel
ai-usage: ai-assisted
#Customer intent: As a developer, I want to transcribe stereo audio in real time so that I can get separate speech to text results for each channel.
---

# How to transcribe multichannel audio in real time

[!INCLUDE [preview](includes/previews/preview-generic.md)]

Real-time multichannel transcription processes a stereo (two-channel) audio file or stream and returns recognition results that are tagged by channel. Use it when each channel carries a distinct audio source that you want to transcribe independently, such as the two sides of a customer support call. The Speech service transcribes up to two channels at the same time and reports the source channel with each recognition result.

Heavy overlapping speech across both channels can increase result-processing latency.

::: zone pivot="programming-language-python"
[!INCLUDE [Python include](includes/how-to/recognize-speech-multichannel/python.md)]
::: zone-end

::: zone pivot="programming-language-csharp"
[!INCLUDE [C# include](includes/how-to/recognize-speech-multichannel/csharp.md)]
::: zone-end

::: zone pivot="programming-language-cpp"
[!INCLUDE [C++ include](includes/how-to/recognize-speech-multichannel/cpp.md)]
::: zone-end

::: zone pivot="programming-language-java"
[!INCLUDE [Java include](includes/how-to/recognize-speech-multichannel/java.md)]
::: zone-end

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript include](includes/how-to/recognize-speech-multichannel/javascript.md)]
::: zone-end

::: zone pivot="programming-language-go"
[!INCLUDE [Go include](includes/how-to/recognize-speech-multichannel/go.md)]
::: zone-end

::: zone pivot="programming-language-objectivec"
[!INCLUDE [Objective-C include](includes/how-to/recognize-speech-multichannel/objective-c.md)]
::: zone-end

::: zone pivot="programming-language-swift"
[!INCLUDE [Swift include](includes/how-to/recognize-speech-multichannel/swift.md)]
::: zone-end

## Supported and unsupported features

Multichannel transcription works with several real-time speech to text features and doesn't support others. The following table summarizes the current support.

| Feature | Supported |
| --- | --- |
| [Diarization](get-started-stt-diarization.md) | ✅ |
| [Custom speech](custom-speech-overview.md) | ✅ |
| Semantic segmentation | ✅ |
| TrueText | ✅ |
| [Language identification](language-identification.md) | ❌ |
| Multilingual models | ❌ |
| Post-stream refinement | ❌ |
| [Phrase lists](improve-accuracy-phrase-list.md) | ❌ |
| Pronunciation assessment | ❌ |

When you combine multichannel transcription with diarization, results also include speaker IDs. Source-channel metadata for diarization results varies by Speech SDK. Review the guidance for your programming language before you use channel and speaker metadata together.

Results from different channels aren't guaranteed to arrive in perfect time order, especially when speech overlaps across channels.

## Related content

- [How to recognize speech](how-to-recognize-speech.md)
- [Audio concepts](concepts/audio-concepts.md)
- For per-channel transcription of prerecorded files, see the `channels` property in [batch transcription](batch-transcription.md).
