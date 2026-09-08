---
title: "Work with chat completion models"
description: "Learn how to use Azure OpenAI chat completions in Python, C#, and TypeScript, manage conversations, and handle context windows and common errors."
author: alvinashcraft #dereklegenzoff
ms.author: aashcraft #delegenz
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python, devx-track-dotnet
  - classic-and-new
  - doc-kit-assisted
ms.topic: how-to
ms.date: 08/24/2026
manager: mcleans
keywords: ChatGPT
ai-usage: ai-assisted
zone_pivot_groups: openai-chat-completions
---

<!-- markdownlint-disable MD044 -->

# Work with chat completion models

[!INCLUDE [chatgpt 1](../includes/how-to-chatgpt-1.md)]

> [!NOTE]
> Reasoning models, such as the GPT-5 series, behave differently on this API. They use `max_completion_tokens` instead of `max_tokens`, and they don't support `temperature`, `top_p`, or the penalty parameters. On the `gpt-5.6` and later models, a Chat Completions request that includes function tools fails unless you set `reasoning_effort` to `none`. Use the [Responses API](responses.md) for tool calling with reasoning models. For details, see [Azure OpenAI reasoning models](reasoning.md).

## Prerequisites

- An Azure OpenAI resource with a chat completion model deployment. To create a resource and deploy a model, see [Create a resource and deploy a model with Azure OpenAI](/azure/ai-foundry/openai/how-to/create-resource).
::: zone pivot="programming-language-python"

- Install the OpenAI Python library: `pip install openai`.
- For Microsoft Entra ID authentication, install Azure Identity (`pip install azure-identity`) and the [Azure CLI](/cli/azure/install-azure-cli). Assign the `Cognitive Services User` role to your user account, and then run `az login`.
- For the token-counting example, install tiktoken: `pip install tiktoken`.
- If you use API keys, set the `AZURE_OPENAI_API_KEY` environment variable.

::: zone-end

::: zone pivot="programming-language-dotnet"

- [The .NET 8.0 SDK](https://dotnet.microsoft.com/download) or later.
- For Microsoft Entra ID authentication, install the [Azure CLI](/cli/azure/install-azure-cli) and assign the `Cognitive Services User` role to your user account.
- If you use API keys, set the `AZURE_OPENAI_API_KEY` environment variable.

::: zone-end

::: zone pivot="programming-language-javascript"

- Node.js 22 or later.
- For Microsoft Entra ID authentication, install the [Azure CLI](/cli/azure/install-azure-cli), assign the `Cognitive Services User` role to your user account, and then run `az login`.
- If you use API keys, set the `AZURE_OPENAI_API_KEY` environment variable.

::: zone-end

In the code samples, replace `YOUR-RESOURCE-NAME` with your Azure OpenAI resource name and `YOUR-DEPLOYMENT-NAME` with your model deployment name.

::: zone pivot="programming-language-python"

[!INCLUDE [Python](../includes/chat-completion-python.md)]

::: zone-end

::: zone pivot="programming-language-dotnet"

[!INCLUDE [.NET](../includes/chat-completion-dotnet.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript and TypeScript](../includes/chat-completion-javascript.md)]

::: zone-end

## Related content

- [Use the Responses API](responses.md)
- [Azure OpenAI reasoning models](reasoning.md)
- [Explore Foundry Models sold by Azure](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Generate embeddings](../tutorials/embeddings.md)
