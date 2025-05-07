---
title: Multi-agent workflows in Azure AI Foundry Agent Service
titleSuffix: Azure AI Foundry
description: Learn about building agentic systems with multiple agents in the Azure AI Foundry Agent Service.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-agent-service
ms.topic: conceptual
ms.date: 05/05/2025
ms.custom: azure-ai-agents
---

# Multi-agent workflows in Azure AI Agent Service

Use this article to learn about how to streamline complex processes by utilizing multi-agent workflows. 

Multi-agent workflows involve the coordinated efforts of multiple AI agents, each specializing in different tasks or possessing distinct capabilities. These agents communicate and collaborate to complete intricate processes that would be challenging for a single agent to handle. 

Multi-agent workflows consist of:

* A main agent: These agents act as the primary interaction point with end-users. The agent manages the workflow, determining which (if any) connected agents are called and that tasks are delegated appropriately.
* Task-specific connected agents: These agents focus on specific tasks such as data extraction, analysis, or decision-making. They are called by the main agent to perform their task and return outputs.

:::image type="content" source="../media/multi-agent/agent-tree.png" alt-text="A diagram showing a main agent and several sub agents.":::

Agent coordination is responsible for defining and executing the sequence of tasks within a workflow. An event-driven architecture is used to trigger actions based on specific events. In a basic implementation, for example, all user interaction goes through the main agent, which then hands-off to connected agents. When the connected agent completes a task, the output is passed back to the main agent. 

:::image type="content" source="../media/multi-agent/example-thread.png" alt-text="A diagram showing a main agent and several sub agents.":::

## Multi-agent solutions in AI Foundry Agent Service

AI Foundry Agent Service enables you to develop multi-agent solutions in two ways: The connected agent feature, and using the Semantic kernel.

### Connected agents

The [connected agents](../how-to/connected-agents.md) feature lets you define and manage one or more specialized agents, and handles agent-to-agent communication. The benefit of using the connected agents feature is that orchestration is handled for you, and you can use the AI Foundry portal or a code-based approach to configure your agent setup.

### Semantic Kernel

[Semantic Kernel](/semantic-kernel/overview/) is an open-source SDK that lets you build AI agents with the flexibility to define custom agent orchestration, making it useful for more complex multi-agent interactions. The `AzureAIAgent` in the [Semantic Kernel framework](/semantic-kernel/frameworks/agent/azure-ai-agent) lets you integrate the AI Foundry Agent Service into your applications, and provides tools for creating a [multi-agent solution](/semantic-kernel/frameworks/agent/agent-chat).