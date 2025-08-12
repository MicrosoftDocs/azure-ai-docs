---
title: Integrate with inference SDKs
titleSuffix: Foundry Local
description: This article provides instructions on how to integrate Foundry Local with common Inferencing SDKs.
ms.service: azure-ai-foundry
ms.subservice: foundry-local
ms.custom: build-2025
ms.topic: how-to
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 07/03/2025
zone_pivot_groups: foundry-local-sdk
author: jonburchel
reviewer: samuel100
---

# Integrate inferencing SDKs with Foundry Local

[!INCLUDE [foundry-local-preview](./../includes/foundry-local-preview.md)]

Foundry Local integrates with various inferencing SDKs - such as OpenAI, Azure OpenAI, Langchain, etc. This guide shows you how to connect your applications to locally running AI models using popular SDKs.

## Prerequisites

- Foundry Local installed. See the [Get started with Foundry Local](../get-started.md) article for installation instructions.

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/integrate-examples/python.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/integrate-examples/javascript.md)]
::: zone-end
::: zone pivot="programming-language-csharp"
[!INCLUDE [JavaScript](../includes/integrate-examples/csharp.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [JavaScript](../includes/integrate-examples/rust.md)]
::: zone-end

## Next steps

- [Compile Hugging Face models to run on Foundry Local](how-to-compile-hugging-face-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)
