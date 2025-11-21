---
title: Agent Development Lifecycle
titleSuffix: Microsoft Foundry
description: This article helps you understand the agent development lifecycle.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 11/13/2025
author: aahill
ms.author: aahi
---

# Agent development lifecycle

The agent building experience in Microsoft Foundry brings many development and observability features, from agent creation to embedding your agent into your applications. You can use the Foundry portal or code to build, customize, and test your agent's behavior. You can then iterate with capabilities like tracing, evaluation, and monitoring to improve your agent's performance. When you're ready, you can publish your agent to preview, share, and see your agent in action within your applications.

## Types of agents

There are three types of agents:

- **Prompt-based**: A prompt-based agent is a declaratively defined single agent that combines model configuration, instruction, tools, and natural language prompts to drive behavior. You can make your agent even more powerful by attaching knowledge and memory capabilities. Prompt-based agents can be edited, versioned, tested, evaluated, monitored, and published from the [agent playground](../../../concepts/concept-playgrounds.md) in the Foundry portal.

- **Workflow**: If you want to develop a more advanced agentic workflow that consists of a sequence of actions, or orchestrate multiple agents together, you can do so with workflows. Workflows have their own development interface in the portal, but the same lifecycle applies. For details, see the [workflow article](../../agents/concepts/workflow.md).

- **Hosted**: Hosted agents are containerized agents that are developed in code via supported agent frameworks or custom code. Foundry Agent Service deploys and manages these agents. They're created primarily through the code-first experience and can't be edited in the agent building interface on Foundry. But they can be viewed, invoked, evaluated, monitored, and published just like prompt-based agents and workflows. For details, see the [hosted agents](./hosted-agents.md) article.

You can create prompt-based agents and workflows in the Foundry portal or your own development environment by using the CLI, SDK, or REST API. For more information, see the [quickstart](../../../quickstarts/get-started-code.md).

## Creating a prompt-based agent

If you already know what kind of agent you want to create, you can name it and then quickly start configuring your model instructions and tools. If you don't already have a model deployed, an available model is deployed for you.

> [!NOTE]
> After you name your agent, you can't change the name. In code, you refer to your agent by `<agent_name>:<version>`.

## Developing in code

If you prefer to work in code, there are a couple supported ways to bring your agent code into a development environment from which you can test locally and then deploy to Azure.

From the **Code** tab in the agent playground's chat pane, you can take a code snippet that references your agent to a dedicated Visual Studio Code for the Web cloud environment. The snippet comes preconfigured with the packages and extensions that you need, along with instructions to efficiently develop and deploy your Foundry agent to Azure. You can also copy the code snippet directly to your preferred development environment. For details, see the [playground documentation](../../../concepts/concept-playgrounds.md#open-in-vs-code-capability).

## Core capabilities for the agent development lifecycle

The agent building experience offers integrated experiences for each core step of the agent development lifecycle. We recommend that you use these core capabilities as you develop your production-ready agent application. Each capability has in-depth documentation where you can learn more.

### Save changes as versions

After you create the first version of a prompt-based agent or a workflow, you can save subsequent changes as new versions. You can test unsaved changes in the agent playground. But if you want to view conversation history, monitor your agent's performance, or run full evaluations, you're prompted to save your changes.

Agent versioning provides the following capabilities for managing agent configurations and iterations. This system ensures that all changes are tracked, testable, and comparable across versions.

- **Version immutability**: Each version of an agent is immutable after you save it. Any modifications to an existing version require saving and creating a new version. This requirement helps ensure version integrity and prevents accidental overwrites.
- **Draft state management**: You can test agents in an unsaved state for experimentation. You lose unsaved changes if you leave the Foundry portal, so save frequently to preserve important modifications.
- **Version control operations**: You can direct requests to specific agent versions to enable controlled deployment and rollback capabilities.
- **Version history navigation**: You can access the version history for any agent, go to any specific version, and perform the following comparisons:

  - Agent setup comparison: Compare configuration settings between versions. You can choose which versions you want to compare by using the version dropdown list.
  - Chat output comparison: Analyze response differences between agent versions by using identical inputs.
  - YAML definition comparison: Review differences in agent definitions.

### Add tools

You can make your agent more powerful by giving it knowledge (specific files or indexes) or allowing it to take actions (calling external APIs). There are tools available for most use cases, from simple file uploads to custom Model Context Protocol (MCP) server connections. For more complicated tools, you might need to configure authentication or add connections as part of attaching them to an agent.

You must successfully configure a tool to be able to save an agent with it attached. You can reuse configured tools across agents. For information about available tools, see the [tools catalog](./tool-catalog.md).

### Publish your agent or workflow

After you have an agent or workflow version that you're happy with, [publish it as an agent application](../how-to/publish-agent.md). You then have a stable endpoint that you can open and test in the browser, share with others, or embed in your existing applications. You and your collaborators can validate performance and identify what needs refinement. You can make any necessary updates and republish a new version at any time.
