---
title: Include file
description: Include file
author: alvinashcraft #dereklegenzoff
ms.reviewer: sgilley
ms.author: aashcraft #delegenz
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/24/2026
ms.custom:
  - include
  - doc-kit-assisted
ai-usage: ai-assisted
---

In this article, you send chat completion requests, build a multi-turn conversation, and manage the conversation's token budget.

Chat models are language models optimized for conversational interfaces. Unlike older text-in and text-out completion models, chat models accept a transcript of messages and return a model-generated message. This format supports multi-turn conversations and nonchat scenarios.

Use the message format described in this article instead of prompting chat models like older completion models. Otherwise, the models might produce verbose or less useful responses.

> [!TIP]
> For new apps, consider building on the [Responses API](../how-to/responses.md) instead of Chat Completions. To upgrade an existing app, see [Azure OpenAI To Responses](https://aka.ms/azure-openai-to-responses) and [Upgrade your Azure OpenAI app from Chat Completions to the Responses API](/azure/developer/ai/how-to/azure-openai-to-responses).
