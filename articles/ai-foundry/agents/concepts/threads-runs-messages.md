---
title: Threads, Runs, and Messages in Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about the components used in the Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 04/15/2025
ms.custom: azure-ai-agents
---

# Threads, Runs, and Messages in Azure AI Foundry Agent Service

Azure AI Foundry Agent Service supports persistent threads, runs, and messages, which are essential components for managing conversation states and interactions with users.

## Agent components

When you use an Agent, there are a series of steps that are involved.

- **Creating an agent:** You create an agent to start sending messages and recieving responses.
- **Creating a thread:** You create a thread once and append messages to it as users reply. This ensures that the conversation history is maintained and managed automatically.
- **Sending messages:** Messages can be sent by both the agent and the user. These messages can include text, images, and other files, providing a rich interaction experience.
- **Running the agent:** When a run is initiated, the agent processes the messages in the thread and performs tasks based on its configuration. It may append new messages to the thread as part of its response.
- **Check the run status:** Monitor the run until it has completed. 
- **Getting the response:** After the agent has created a response, display it to the user.

:::image type="content" source="../media\run-thread-model.png" alt-text="A diagram showing an example of an agent run." lightbox="../media\run-thread-model.png":::

## Agent

A custom AI that uses AI models in conjunction with tools.

## Threads

Threads are conversation sessions between an agent and a user. They store messages and automatically handle truncation to fit content into a model’s context. When you create a thread, you can append new messages to it as users respond.

## Messages

Messages are the individual pieces of communication within a thread. They can be created by either the agent or the user and can include text, or other files. Messages are stored as a list within the thread, allowing for a structured and organized conversation flow.

## Runs

A run involves invoking the agent on the thread, where it processes the messages in the thread and may append new messages (responses from the agent). The agent uses its configuration and the thread’s messages to perform tasks by calling models and tools. As part of a run, the agent appends messages to the thread.

## Next steps

* [Quickstart: create an agent](../quickstart.md)
