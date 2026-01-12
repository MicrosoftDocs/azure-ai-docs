---
title: Agent Runtime Components
titleSuffix: Microsoft Foundry
description: Learn about how agents work, including the conversation response loop.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 10/29/2025
author: aahill
ms.author: aahi
---

# Agent runtime components

Microsoft Foundry Agent Service enables response generation and persistent conversations, which are key for interacting with users and maintaining conversation states.

## Agent components

When you work with an agent, these steps are involved:

1. **Create an agent**: Define an agent to start sending messages and receiving responses.

1. **Create a conversation (optional)**: Use a conversation to maintain history across turns. If you don't create one, the state is stored automatically with each response.

1. **Generate a response**: The agent processes input items in the conversation and any instructions provided in the request. Items might be appended to the conversation.

1. **Check response status**: Monitor the response until it finishes (especially in streaming or background mode).

1. **Retrieve the response**: Display the generated response to the user.

:::image type="content" source="../media/runtime-components.png" alt-text="Diagram that shows the runtime of an agent.":::

## Agent

An agent is a persisted orchestration definition that combines AI models, instructions, code, tools, parameters, and optional safety or governance controls.

Agents are stored as named, versioned assets in Microsoft Foundry. During response generation, the agent definition works with interaction history (conversation or previous response) to process and respond to user input.

## Conversation

A conversation manages states automatically, so you don't need to pass inputs manually for each turn.

Conversations are durable objects with unique identifiers. After creation, you can reuse them across sessions.

Conversations store items, which can include messages, tool calls, tool outputs, and other data.

## Response

Response generation invokes the agent. The agent uses its configuration and any provided history (conversation or previous response) to perform tasks by calling models and tools. As part of response generation, items are appended to the conversation.

You can also generate a response without defining an agent. In this case, all configurations are provided directly in the request and used only for that response. This approach is useful for simple scenarios with minimal tools.
