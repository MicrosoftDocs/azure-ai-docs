---
title: Threads, Runs, and Messages in the Foundry Agent Service
titleSuffix: Microsoft Foundry
description: Learn about the components used in the Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/06/2026
ms.custom: azure-ai-agents, dev-focus
ai-usage: ai-assisted
---

# Threads, runs, and messages in Foundry Agent Service

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Foundry Agent Service supports persistent threads, runs, and messages. These components are essential for managing conversation states and interactions with users.

## Agent components

When you use an agent, the following steps are involved:

- **Create an agent:** Create an agent to start sending messages and receiving responses.
- **Create a thread:** Create a thread once and append messages to it as users reply. The conversation history is maintained and managed automatically.
- **Send messages:** Both the agent and the user can send messages. These messages can include text, images, and other files.
- **Run the agent:** When you initiate a run, the agent processes the messages in the thread and performs tasks based on its configuration. It might append new messages to the thread as part of its response.
- **Monitor the run status:** Monitor the run until it completes.
- **Get the response:** After the agent creates a response, display it to the user.

:::image type="content" source="../media/run-thread-model.png" alt-text="A diagram showing an example of an agent run." lightbox="../media/run-thread-model.png":::

## Agent

An agent is a configurable orchestration component that uses AI models with instructions, tools, parameters, and optional safety and governance controls. At run time, an agent uses these components and a given thread's message history to respond to user inputs. 

## Threads

Threads are conversation sessions between an agent and a user. They store messages and automatically handle truncation to fit content into a model's context. When you create a thread, you can append new messages (up to 100,000 per thread) as users respond.

### When to create a new thread

- **New conversation context**: Create a new thread when starting a fresh topic or when the user explicitly wants to "start over."
- **Different users**: Each user should typically have their own thread(s) to maintain conversation isolation.
- **Performance considerations**: Threads with thousands of messages may have increased latency. Consider creating new threads for long-running interactions.

### Thread lifecycle

Threads persist until explicitly deleted. In the Standard agent setup, threads are stored in your Azure Cosmos DB account. Plan your thread retention strategy based on:
- **Storage costs**: Large numbers of threads with many messages consume storage
- **Compliance requirements**: Consider your data retention policies when managing thread deletion

## Messages

Messages are the individual pieces of communication within a thread. They can be created by either the agent or the user and can include text, or other files. Messages are stored as a list within the thread, allowing for a structured and organized conversation flow.

## Runs

A run involves invoking the agent on the thread. The agent processes the messages in the thread and might append new messages, which are responses from the agent. The agent uses its configuration and the thread's messages to perform tasks by calling models and tools. As part of a run, the agent appends messages to the thread.

### Run status values

Monitor the run status to determine when processing is complete:

| Status | Description |
|--------|-------------|
| `queued` | Run is waiting to be processed |
| `in_progress` | Agent is actively processing |
| `requires_action` | Agent needs function call results (for function calling tools) |
| `completed` | Run finished successfully |
| `failed` | Run encountered an error |
| `cancelled` | Run was cancelled |
| `expired` | Run exceeded time limits |

## Best practices

- **Clean up resources**: Delete threads and agents when no longer needed to manage costs and storage
- **Handle errors gracefully**: Always check for `failed` run status and implement retry logic with exponential backoff
- **Use appropriate polling intervals**: When checking run status, start with 500ms intervals and increase for longer-running operations
- **Limit message size**: While threads support up to 100,000 messages, aim to keep conversations concise for optimal performance

## Next steps

* [Quickstart: create an agent](../quickstart.md)