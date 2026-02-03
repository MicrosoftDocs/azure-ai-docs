---
title: Integrate with inference SDKs
titleSuffix: Foundry Local
description: This article provides instructions on how to integrate Foundry Local with common Inferencing SDKs.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025, dev-focus
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 01/06/2026
zone_pivot_groups: foundry-local-sdk
author: jonburchel
reviewer: samuel100
ai-usage: ai-assisted
---

# Integrate inference SDKs with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local integrates with OpenAI-compatible SDKs and HTTP clients through a local REST server. This article shows you how to connect your app to local AI models by using popular SDKs.

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/integrate-examples/python.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/integrate-examples/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/integrate-examples/javascript.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/integrate-examples/rust.md)]
::: zone-end

## Related content

- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)
