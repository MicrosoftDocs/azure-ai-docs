---
title: "Generate text embeddings"
titleSuffix: Foundry Local
description: "Learn how to generate text embeddings with the Foundry Local SDK using an on-device embedding model."
ms.service: microsoft-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: nakersha
ms.reviewer: samkemp
ms.date: 04/24/2026
author: natke
reviewer: samuel100
zone_pivot_groups: foundry-local-sdk
ai-usage: ai-assisted
---
    
# Generate text embeddings with Foundry Local

The Foundry Local SDK provides an embedding API that converts text into numerical vectors on-device. Use these vectors for similarity search, classification, clustering, and retrieval-augmented generation (RAG).

The SDK supports both single-input and batch embedding generation through a dedicated embedding client.

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/embeddings/python.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/embeddings/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/embeddings/javascript.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/embeddings/rust.md)]
::: zone-end


## Related content

- [Use native chat completions API with Foundry Local](how-to-use-native-chat-completions.md)
- [Transcribe audio files with Foundry Local](how-to-transcribe-audio.md)
- [Use chat completions via REST server with Foundry Local](how-to-integrate-with-inference-sdks.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)
