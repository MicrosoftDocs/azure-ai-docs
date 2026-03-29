---
title: "Tutorial: Build a multi-turn chat assistant with Foundry Local"
titleSuffix: Foundry Local
description: Build an interactive chat assistant that maintains conversation context across multiple exchanges using the Foundry Local SDK. This tutorial covers model selection, system prompts, conversation history, and streaming responses.
ms.service: azure-ai-foundry
ms.custom: build-2025, dev-focus
ms.topic: tutorial
ms.author: jburchel
ms.reviewer: samkemp
ms.date: 03/29/2026
author: jonburchel
reviewer: samuel100
zone_pivot_groups: foundry-local-sdk
ai-usage: ai-assisted
# CustomerIntent: As a developer, I want to build a multi-turn chat assistant so that I can create conversational AI apps that run locally on my device.
---

# Tutorial: Build a multi-turn chat assistant with Foundry Local

In this tutorial, you build an interactive chat assistant that runs entirely on your device. The assistant maintains conversation context across multiple exchanges, so it remembers what you discussed earlier in the conversation. You use the Foundry Local SDK to select a model, define a system prompt, and stream responses token by token.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Set up a project and install the Foundry Local SDK
> * Browse the model catalog and select a model
> * Define a system prompt to shape assistant behavior
> * Implement multi-turn conversation with message history
> * Stream responses for a responsive experience
> * Clean up resources when the conversation ends

## Prerequisites

- A Windows, macOS, or Linux computer with at least 8 GB of RAM.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/tutorial-chat-assistant/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/tutorial-chat-assistant/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/tutorial-chat-assistant/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/tutorial-chat-assistant/rust.md)]
::: zone-end

## Clean up resources

The model weights remain in your local cache after you unload a model. This means the next time you run the application, the download step is skipped and the model loads faster. No extra cleanup is needed unless you want to reclaim disk space.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Foundry Local architecture](../concepts/foundry-local-architecture.md)
- [Use tool calling with Foundry Local](../how-to/how-to-use-tool-calling-with-foundry-local.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
