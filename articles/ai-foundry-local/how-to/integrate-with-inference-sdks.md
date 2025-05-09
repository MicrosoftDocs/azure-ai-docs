---
title: Integrate with Inference SDKs
titleSuffix: Foundry Local
description: This article provides instructions on how to integrate Foundry Local with common Inferencing SDKs.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2025
ms.topic: how-to
ms.date: 02/12/2025
ms.author: samkemp
zone_pivot_groups: azure-ai-model-catalog-samples-chat
author: samuel100
---

# Integrate Foundry Local with Inferencing SDKs

Foundry Local provides a REST API endpoint that makes it easy to integrate with various inferencing SDKs and programming languages. This guide shows you how to connect your applications to locally running AI models using popular SDKs.

## Prerequisites

- Foundry Local installed. See the [Get started with Foundry Local](../get-started.md) article for installation instructions.
- Basic knowledge of the programming language you want to use for integration

## Understanding the REST API

When Foundry Local is running, it exposes an OpenAI-compatible REST API endpoint at `http://localhost:5272/v1`. This endpoint supports standard API operations like:

- `/completions` - For text completion
- `/chat/completions` - For chat-based interactions
- `/models` - To list available models

::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/integrate-examples/python.md)]
::: zone-end

::: zone pivot="programming-language-rest"
[!INCLUDE [Rest](../includes/integrate-examples/rest.md)]
::: zone-end

::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/integrate-examples/javascript.md)]
::: zone-end

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/integrate-examples/csharp.md)]
::: zone-end


## Next steps

- [How to compile Hugging Face models to run on Foundry Local](how-to-compile-hf-models.md)
- [Explore the Foundry Local CLI reference](../reference/reference-cli.md)
