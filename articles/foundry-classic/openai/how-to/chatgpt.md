---
title: "Work with chat completion models (classic)"
description: "Learn about the options for how to use models with the chat completions API (classic)"
author: mrbullwinkle #dereklegenzoff
ms.author: mbullwin #delegenz
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.custom:
  - build-2023, build-2023-dataai, devx-track-python
  - classic-and-new
ms.topic: how-to
ms.date: 11/26/2025
manager: nitinme
keywords: ChatGPT
ai-usage: ai-assisted
ROBOTS: NOINDEX, NOFOLLOW
---

# Work with chat completions models (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/chatgpt.md)

[!INCLUDE [chatgpt 1](../../../foundry/openai/includes/how-to-chatgpt-1.md)]

## Prerequisites

- An Azure OpenAI chat competions model deployed
- Install the OpenAI Python library: `pip install openai`.
- For Microsoft Entra ID authentication, install Azure Identity: `pip install azure-identity`.
- For the token-counting example, install tiktoken: `pip install tiktoken`.
- If you use API keys, set `AZURE_OPENAI_API_KEY` (or `OPENAI_API_KEY`).

[!INCLUDE [chat-completion-python](../../../foundry/openai/includes/chat-completion-python.md)]
