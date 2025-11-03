---
title: Transcribe audio files with Foundry Local
titleSuffix: Foundry Local
description: This article provides instructions on how to transcribe audio using Foundry Local.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 10/01/2025
zone_pivot_groups: foundry-local-sdk-v2
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---
    
# Transcribe recorded audio files with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local has a native audio transcription API that allows you to transcribe audio files in the following formats:

- WAV
- MP3
- FLAC


This article shows you how to use the native audio transcription API in Foundry Local.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/audio-transcription/csharp.md)]
::: zone-end

## Related content

- [Integrate Foundry Local with 3rd party SDKs](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)