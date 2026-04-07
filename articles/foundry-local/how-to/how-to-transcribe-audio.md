---
title: "Transcribe audio files with Foundry Local"
titleSuffix: Foundry Local
description: "This article provides instructions on how to transcribe audio using Foundry Local with C# and JavaScript."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 01/06/2026
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
zone_pivot_groups: foundry-local-sdk-vnext
---
    
# Transcribe recorded audio files with Foundry Local
[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Use Foundry Local's native audio transcription API to convert a local audio file into text. In this article, you create a console application that downloads a Whisper model, loads it, and streams transcription output.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/audio-transcription/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/audio-transcription/javascript.md)]
::: zone-end

## Related content

- [Use native chat completions API with Foundry Local](how-to-use-native-chat-completions.md)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)