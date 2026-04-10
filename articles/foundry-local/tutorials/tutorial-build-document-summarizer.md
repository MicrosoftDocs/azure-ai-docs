---
title: "Tutorial: Build a document summarizer"
titleSuffix: Foundry Local
description: Build a document summarization application that reads text files and generates concise summaries using the Foundry Local SDK. Everything runs locally on your device.
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
# CustomerIntent: As a developer, I want to build a document summarizer so that I can process text files locally without sending data to the cloud.
---

# Tutorial: Build a document summarizer

Build an application that reads text files and generates concise summaries — entirely on your device. This is useful when you need to quickly understand the content of documents without reading them in full, and when the documents contain sensitive information that shouldn't leave your machine.

In this tutorial, you learn how to:

> [!div class="checklist"]
> * Set up a project and install the Foundry Local SDK
> * Read a text document from the file system
> * Load a model and generate a summary
> * Control summary output with system prompts
> * Process multiple documents in a batch
> * Clean up resources

## Prerequisites

- A Windows, macOS, or Linux computer with at least 8 GB of RAM.

::: zone pivot="programming-language-csharp"
[!INCLUDE [C#](../includes/tutorial-document-summarizer/csharp.md)]
::: zone-end
::: zone pivot="programming-language-javascript"
[!INCLUDE [JavaScript](../includes/tutorial-document-summarizer/javascript.md)]
::: zone-end
::: zone pivot="programming-language-python"
[!INCLUDE [Python](../includes/tutorial-document-summarizer/python.md)]
::: zone-end
::: zone pivot="programming-language-rust"
[!INCLUDE [Rust](../includes/tutorial-document-summarizer/rust.md)]
::: zone-end

## Clean up resources

The model weights remain in your local cache after you unload a model. This means the next time you run the application, the download step is skipped and the model loads faster. No extra cleanup is needed unless you want to reclaim disk space.

## Related content

- [Get started with Foundry Local](../get-started.md)
- [Tutorial: Build a multi-turn chat assistant](tutorial-build-chat-assistant.md)
- [Foundry Local SDK reference](../reference/reference-sdk-current.md)
