---
title: "Tutorial: Build an AI assistant with tool calling"
titleSuffix: Foundry Local
description: Build an AI assistant that uses tool calling to perform actions like looking up information and doing calculations, all running locally with the Foundry Local SDK.
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
# CustomerIntent: As a developer, I want to build an AI assistant with tool calling so that my local AI app can perform actions and retrieve information dynamically.
---

# Tutorial: Build an AI assistant with tool calling

Build an AI assistant that goes beyond conversation — it can call functions to perform actions. The assistant decides when a function is needed, you execute it, and feed the result back. Everything runs locally with the Foundry Local SDK.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Set up a project and install the Foundry Local SDK
> * Define tools the assistant can call
> * Send a message that triggers tool use
> * Execute the tool and return results to the model
> * Handle the complete tool calling loop
> * Clean up resources

## Prerequisites

- A Windows, macOS, or Linux computer with at least 8 GB of RAM.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/tutorial-tool-calling-assistant/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/tutorial-tool-calling-assistant/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/tutorial-tool-calling-assistant/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/tutorial-tool-calling-assistant/rust.md)]
::: zone-end

## Clean up resources

The model weights remain in your local cache after you unload a model. This means the next time you run the application, the download step is skipped and the model loads faster. No extra cleanup is needed unless you want to reclaim disk space.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Tutorial: Build a multi-turn chat assistant](tutorial-build-chat-assistant.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
