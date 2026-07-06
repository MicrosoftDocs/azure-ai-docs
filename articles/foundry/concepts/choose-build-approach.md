---
title: "Choose how to build with Microsoft Foundry"
description: "Decide what to build on Microsoft Foundry and which developer surface to use, with links to the right quickstart for your scenario."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: concept-article
ms.date: 06/16/2026
ai-usage: ai-assisted
# customer intent: As a developer, I want to understand the build options in Foundry so that I can pick the right agent type and developer surface for my scenario.
---

# Choose how to build with Microsoft Foundry

Microsoft Foundry gives you several ways to build, from a single model call to a fully containerized agent. This article helps you decide how to build your agent and which developer surface to use. Each section links to the canonical quickstart or overview so you can go deeper.

If you're brand new, start with the [recommended path for new developers](#recommended-path-for-new-developers).

## Start by building an agent

Most projects on Foundry center on an agent: a model paired with instructions and tools that can reason over a request and take action. The main decision is how much you want to customize and control how that agent runs. Think of it as a spectrum from declarative to full code.

- **Declarative, with the least to manage.** Specify instructions, choose a model, and attach tools in the Foundry portal or with the SDK. Foundry hosts and runs the agent for you, with no application code or containers to maintain. In Foundry, this is a **prompt agent**. [Create a prompt agent](../agents/quickstarts/prompt-agent.md).
- **Full code, with the most control.** Bring your own code or framework (for example, Microsoft Agent Framework, LangGraph, or Semantic Kernel), package it as a container, and Foundry runs it with a managed endpoint, scaling, identity, and observability. In Foundry, this is a **hosted agent**. [Deploy a hosted agent](../agents/quickstarts/quickstart-hosted-agent.md).

You can start declarative and move to code as your needs grow. For a detailed comparison, see [What are hosted agents?](../agents/concepts/hosted-agents.md). For the end-to-end build, test, and ship cycle, see the [agent development lifecycle](../agents/concepts/development-lifecycle.md).

Not building an agent yet? If you only need to send prompts to a model with no tools or orchestration, start with a single [model call](../quickstarts/get-started-code.md).

## Choose your developer surface

Foundry supports several surfaces. Many developers combine them, for example, prototyping in the portal and then moving to code.

| Surface | Best for | Start here |
|---|---|---|
| **Foundry portal** | Exploring models, prototyping prompts, and building prompt agents without writing code. | [Playgrounds and quick evaluation](concept-playgrounds.md) |
| **SDKs** | Building applications in Python, C#, JavaScript, or Java. | [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md) |
| **Azure Developer CLI (azd)** | Scaffolding, running, testing, and deploying Hosted agent projects from the command line. | [Develop agents with the Azure Developer CLI](../agents/concepts/cli-agent-development.md) |
| **Visual Studio Code** | Building and debugging agents in your editor with the Foundry extension. | [Work in VS Code](../how-to/develop/get-started-projects-vs-code.md) |
| **Coding agents and MCP** | Driving Foundry from coding agents (for example, GitHub Copilot or Claude Code) with the Foundry Skill and MCP server. | [Use the Microsoft Foundry Skill in coding agents](../how-to/develop/use-microsoft-foundry-skill.md) |

## Recommended path for new developers

Follow these steps to go from zero to a working integration:

1. **Make your first model call.** Set up your environment and send a prompt with the [build with models and agents quickstart](../quickstarts/get-started-code.md).
1. **Set up your developer environment.** Install the CLI and SDK so you can build in code. See [Set up your developer environment](../how-to/develop/install-cli-sdk.md).
1. **Choose a model.** Browse the catalog and compare options in the [Foundry Models overview](foundry-models-overview.md).
1. **Build your first agent.** Start with a [prompt agent](../agents/quickstarts/prompt-agent.md), or go straight to a [Hosted agent](../agents/quickstarts/quickstart-hosted-agent.md) if you want to bring your own code.
1. **Add tools and knowledge.** Extend your agent with tools, retrieval, and memory from the [tools overview](../agents/concepts/tool-catalog.md).

## Related content

- [What is Microsoft Foundry?](../what-is-foundry.md)
- [Microsoft Foundry architecture](architecture.md)
- [Agent development lifecycle](../agents/concepts/development-lifecycle.md)
