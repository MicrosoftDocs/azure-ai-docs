---
title: "Use native chat completions"
titleSuffix: Foundry Local
description: "This article provides instructions on how to use native chat completions API in Foundry Local."
ms.service: azure
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 01/06/2026
author: jonburchel
reviewer: samuel100
zone_pivot_groups: foundry-local-sdk-vnext
ai-usage: ai-assisted
---
    
# Use Foundry Local native chat completions API
[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

The native chat completions API enables you to run chat completions directly in-process, without starting a REST web server.

In this article, you create a console app that downloads a local model, generates a streaming chat response, and then unloads the model.

This article explains how to use the native chat completions API in the Foundry Local SDK. 

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/native-chat-completions/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/native-chat-completions/javascript.md)]
::: zone-end


## Related content

- [Transcribe audio files with Foundry Local](how-to-transcribe-audio.md)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Use Foundry Local with LangChain](how-to-use-langchain-with-foundry-local.md)
- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)