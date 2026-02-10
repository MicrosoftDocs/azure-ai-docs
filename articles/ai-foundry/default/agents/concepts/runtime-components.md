---
title: Understand agent runtime components in Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn how agents, conversations, and responses work together in Microsoft Foundry Agent Service. Understand state persistence, streaming, and multi-turn interactions.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/02/2026
author: aahill
ms.author: aahi
ms.custom: pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
---

# Agent runtime components

Agent runtime components are the core objects—agents, conversations, and responses—that power stateful, multi-turn interactions in Microsoft Foundry Agent Service. Together, these components let you generate outputs, persist state across turns, and build conversational applications.

This article explains the roles of an **agent**, **conversation**, and **response**, and how they work together during response generation.

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- Familiarity with the [agent development lifecycle](./development-lifecycle.md) (optional).

## How runtime components work together

When you work with an agent, you follow a consistent pattern:

- **Create an agent**: Define an agent to start sending messages and receiving responses.
- **Create a conversation (optional)**: Use a conversation to maintain history across turns. If you don't use a conversation, carry forward context by using the output from a previous response.
- **Generate a response**: The agent processes input items in the conversation and any instructions provided in the request. The agent might append items to the conversation.
- **Check response status**: Monitor the response until it finishes (especially in streaming or background mode).
- **Retrieve the response**: Display the generated response to the user.

The following diagram illustrates how these components interact in a typical agent loop.

:::image type="content" source="../media/runtime-components.png" alt-text="Diagram that shows the agent runtime loop: an agent definition and optional conversation history feed response generation, which can call tools, append items back into the conversation, and produce output items you display to the user.":::

You provide user input (and optionally conversation history), the service generates a response (including tool calls when configured), and the resulting items can be reused as context for the next turn.

## What is an agent?

An agent is a persisted orchestration definition that combines AI models, instructions, code, tools, parameters, and optional safety or governance controls.

Store agents as named, versioned assets in Microsoft Foundry. During response generation, the agent definition works with interaction history (conversation or previous response) to process and respond to user input.

## What is a conversation?

A conversation manages state automatically, so you don't need to pass inputs manually for each turn.

Conversations are durable objects with unique identifiers. After creation, you can reuse them across sessions.

Conversations store items, which can include messages, tool calls, tool outputs, and other data.

### When to use a conversation

Use a conversation when you want:

- **Multi-turn continuity**: Keep a stable history across turns without rebuilding context yourself.
- **Cross-session continuity**: Reuse the same conversation for a user who returns later.
- **Easier debugging**: Inspect what happened over time (for example, tool calls and outputs).

If you don't create a conversation, you can still build multi-turn flows by using the output from a previous response as the starting point for the next request. This approach gives you more flexibility than the older thread-based pattern, where state was tightly coupled to thread objects. For migration guidance, see [Migrate to the Agents SDK](../how-to/migrate.md).

## Conversation items

Conversations store **items** rather than only chat messages. Items capture what happened during response generation so the next turn can reuse that context.

Common item types include:

- **Message items**: User or assistant messages.
- **Tool call items**: Records of tool invocations the agent attempted.
- **Tool output items**: Outputs returned by tools (for example, retrieval results).
- **Output items**: The response content you display back to the user.

For examples that show how conversations and responses work together in code, see [Create and use memory in Foundry Agent Service](../how-to/memory-usage.md).

## How responses work

Response generation invokes the agent. The agent uses its configuration and any provided history (conversation or previous response) to perform tasks by calling models and tools. As part of response generation, the agent appends items to the conversation.

You can also generate a response without defining an agent. In this case, you provide all configurations directly in the request and use them only for that response. This approach is useful for simple scenarios with minimal tools.

## Streaming and background responses

Some response generation modes return results incrementally (streaming) or complete asynchronously (background). In these cases, you typically monitor the response until it finishes and then consume the final output items.

For details about response modes and how to consume outputs, see [Responses API](../../../openai/how-to/responses.md).

## Security and data handling

Because conversations and responses can persist user-provided content and tool outputs, treat runtime data like application data:

- **Avoid storing secrets in prompts or conversation history**. Use connections and managed secret stores instead (for example, [Set up a Key Vault connection](../../../how-to/set-up-key-vault-connection.md)).
- **Use least privilege for tool access**. When a tool accesses external systems, the agent can potentially read or send data through that tool.
- **Be careful with non-Microsoft services**. If your agent calls tools backed by non-Microsoft services, some data might flow to those services. For related considerations, see [Discover tools in the Foundry Tools](./tool-catalog.md).

## Limits and constraints

Limits can depend on the model, region, and the tools you attach (for example, streaming availability and tool support). For current availability and constraints for responses, see [Responses API](../../../openai/how-to/responses.md).

## Related content

- [Agent development lifecycle](./development-lifecycle.md)
- [Discover tools in the Foundry Tools](./tool-catalog.md)
- [Best practices for using tools in Microsoft Foundry Agent Service](./tool-best-practice.md)
- [Publish and share agents in Microsoft Foundry](../how-to/publish-agent.md)
- [Agent tracing overview](../../observability/concepts/trace-agent-concept.md)
