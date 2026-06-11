---
title: "Live transcribe audio from a microphone"
titleSuffix: Foundry Local
description: "Use the Foundry Local live audio transcription API to transcribe microphone audio in real time."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: samkemp
ms.reviewer: samkemp
ms.date: 07/23/2025
author: samuel100
reviewer: samuel100
zone_pivot_groups: foundry-local-sdk
ai-usage: ai-assisted
---

# Live transcribe audio from a microphone with Foundry Local

Use Foundry Local's live audio transcription API to stream microphone audio and receive transcription results in real time. In this article, you create a console application that captures audio from your microphone, streams it to a local speech model, and prints transcription output as you speak.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/live-audio-transcription/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/live-audio-transcription/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/live-audio-transcription/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/live-audio-transcription/rust.md)]
::: zone-end

## Related content

- [Transcribe recorded audio files](how-to-transcribe-audio.md)
- [Use native chat completions API with Foundry Local](how-to-use-native-chat-completions.md)
- [Explore the Foundry Local SDK reference](../reference/reference-sdk-current.md)
