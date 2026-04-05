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

[!INCLUDE [chatgpt 1](../includes/how-to-chatgpt-1.md)]

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
