---
title: "Work with chat completion models"
description: "Learn about the options for how to use models with the chat completions API"
author: mrbullwinkle #dereklegenzoff
ms.author: mbullwin #delegenz
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, devx-track-dotnet
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 03/04/2026
manager: nitinme
keywords: ChatGPT
ai-usage: ai-assisted
zone_pivot_groups: openai-chat-completions
---

# Work with chat completions models
Chat models are language models that are optimized for conversational interfaces. The models behave differently than the older completion API models. Previous models were text-in and text-out, which means they accepted a prompt string and returned a completion to append to the prompt. However, the latest models are conversation-in and message-out. The models expect input formatted in a specific chat-like transcript format. They return a completion that represents a model-written message in the chat. This format was designed specifically for multi-turn conversations, but it can also work well for nonchat scenarios.

This article walks you through getting started with chat completions models. To get the best results, use the techniques described here. Don't try to interact with the models the same way you did with the older model series because the models are often verbose and provide less useful responses.

## Prerequisites

- An Azure OpenAI chat completions model deployed.

::: zone pivot="programming-language-python"

- Install the OpenAI Python library: `pip install openai`.
- For Microsoft Entra ID authentication, install Azure Identity: `pip install azure-identity`.
- For the token-counting example, install tiktoken: `pip install tiktoken`.
- If you use API keys, set the `AZURE_OPENAI_API_KEY` environment variable.

::: zone-end

::: zone pivot="programming-language-dotnet"

- [The .NET 8.0 SDK](https://dotnet.microsoft.com/download) or later.
- For Microsoft Entra ID authentication, install the [Azure CLI](/cli/azure/install-azure-cli) and assign the `Cognitive Services User` role to your user account.
- If you use API keys, set the `AZURE_OPENAI_API_KEY` environment variable.

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python](../includes/chat-completion-python.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET](../includes/chat-completion-dotnet.md)]

::: zone-end
