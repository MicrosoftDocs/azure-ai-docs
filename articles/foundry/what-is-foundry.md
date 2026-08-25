---
title: "What is Microsoft Foundry?"
description: "Microsoft Foundry is a trusted platform that empowers developers to build AI agents, models, and apps. Learn what you can build and how to choose your build approach."
author: sdgilley
ms.author: sgilley
ms.reviewer: sgilley
ms.date: 08/13/2026
ms.service: microsoft-foundry
ms.subservice: foundry-platform
ms.topic: overview
ai-usage: ai-assisted
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
  - build-aifnd
  - build-2025
  - doc-kit-assisted
keywords:
  - Foundry Tools
  - cognitive
# customer intent: As a developer, I want to understand what Microsoft Foundry is and how to build on it so that I can pick the right approach for my scenario.
---

# What is Microsoft Foundry?

Microsoft Foundry unifies agents, models, and tools under a single management grouping with built-in enterprise-readiness capabilities including tracing, monitoring, evaluations, and customizable enterprise setup configurations. The platform provides streamlined management through unified role-based access control (RBAC), networking, and policies under one Azure resource provider namespace.

> [!TIP]
> * Coming from Azure OpenAI? [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md) while preserving your endpoint, API keys, and existing state. 
> * Using hub-based projects? Hub-based projects are accessible in the [Foundry (classic) portal](../foundry-classic/what-is-foundry.md). New investments are focused on Foundry projects in the new portal.

## Get started

Build your first agent in minutes, or open the portal to explore models and tools.

> [!div class="nextstepaction"]
> [Build with models and agents](./quickstarts/get-started-code.md)

[Open the Foundry portal](https://ai.azure.com) | [Get an Azure account](https://azure.microsoft.com/pricing/purchase-options/azure-account)

## What you can build

| Capability | Description |
| --- | --- |
| **Agents** | Build declarative [prompt agents](./agents/quickstarts/prompt-agent.md) in the portal or SDK, or deploy [hosted agents](./agents/quickstarts/quickstart-hosted-agent.md) that run your own code. Learn more in [Foundry Agent Service](./agents/overview.md). |
| **Models** | Access more than 10,000 models from Microsoft, OpenAI, Anthropic, Meta, and others. Browse the [Foundry Models catalog](./concepts/foundry-models-overview.md). |
| **Tools and knowledge** | Extend agents with built-in tools, memory (preview), and retrieval from the [tool catalog](./agents/concepts/tool-catalog.md). |

## Enterprise-ready platform

Foundry brings platform capabilities to every project. Some capabilities are in preview. For current status, see the [general availability overview](./concepts/general-availability.md).

- **Observability:** Trace and evaluate agents and models, and monitor them with built-in dashboards (preview). See [Observability](./concepts/observability.md).
- **Governance and security:** Apply Microsoft Entra identity, role-based access control, content filters, network isolation, and Azure Policy. See the [Foundry control plane](./control-plane/overview.md).
- **One management plane:** Manage agents, models, and tools as a single Azure resource with unified access control, networking, and policies.

## Start by building an agent

Most projects on Foundry center on an agent: a model paired with instructions and tools that can reason over a request and take action. The main decision is how much you want to customize and control how that agent runs. Think of it as a spectrum from declarative to full code.

- **Declarative, with the least to manage.** Specify instructions, choose a model, and attach tools in the Foundry portal or with the SDK. Foundry hosts and runs the agent for you, with no application code or containers to maintain. In Foundry, this is a **prompt agent**. [Create a prompt agent](./agents/quickstarts/prompt-agent.md).
- **Full code, with the most control.** Bring your own code or framework (for example, Microsoft Agent Framework, LangGraph, or Semantic Kernel), package it as a container, and Foundry runs it with a managed endpoint, scaling, identity, and observability. In Foundry, this is a **hosted agent**. [Deploy a hosted agent](./agents/quickstarts/quickstart-hosted-agent.md).

You can start declarative and move to code as your needs grow. For a detailed comparison, see [What are hosted agents?](./agents/concepts/hosted-agents.md). For the end-to-end build, test, and ship cycle, see the [agent development lifecycle](./agents/concepts/development-lifecycle.md).

Not building an agent yet? If you only need to send prompts to a model with no tools or orchestration, start with a single [model call](./quickstarts/get-started-code.md).

## Choose your developer surface

Foundry supports several surfaces. Many developers combine them, for example, prototyping in the portal and then moving to code.

| Surface | Best for | Start here |
| --- | --- | --- |
| **Foundry portal** | Exploring models, prototyping prompts, and building prompt agents without writing code. | [Playgrounds and quick evaluation](./concepts/concept-playgrounds.md) |
| **SDKs** | Building applications in Python, C#, JavaScript, or Java. | [Microsoft Foundry SDKs](./how-to/develop/sdk-overview.md) |
| **Azure Developer CLI (azd)** | Scaffolding, running, testing, and deploying Hosted agent projects from the command line. | [Develop agents with the Azure Developer CLI](./agents/concepts/cli-agent-development.md) |
| **Visual Studio Code** | Building and debugging agents in your editor with the Foundry extension. | [Work in VS Code](./how-to/develop/get-started-projects-vs-code.md) |
| **Coding agents and MCP** | Driving Foundry from coding agents (for example, GitHub Copilot or Claude Code) with the Foundry Skill and MCP server. | [Use the Microsoft Foundry Skill in coding agents](./how-to/develop/use-microsoft-foundry-skill.md) |

## Recommended path for new developers

Follow these steps to go from zero to a working integration:

1. **Make your first model call.** Set up your environment and send a prompt with the [build with models and agents quickstart](./quickstarts/get-started-code.md).
1. **Set up your developer environment.** Install the CLI and SDK so you can build in code. See [Set up your developer environment](./how-to/develop/install-cli-sdk.md).
1. **Choose a model.** Browse the catalog and compare options in the [Foundry Models overview](./concepts/foundry-models-overview.md).
1. **Build your first agent.** Start with a [prompt agent](./agents/quickstarts/prompt-agent.md), or go straight to a [Hosted agent](./agents/quickstarts/quickstart-hosted-agent.md) if you want to bring your own code.
1. **Add tools and knowledge.** Extend your agent with tools, retrieval, and memory (preview). Start with the [toolbox overview](./agents/concepts/toolbox-overview.md), the recommended way to add tools to an agent.

[!INCLUDE [previous-current](includes/previous-current.md)]

## Related content

- [What is Foundry Agent Service?](./agents/overview.md)
- [Foundry Models](./concepts/foundry-models-overview.md)
- [Microsoft Foundry architecture](./concepts/architecture.md)
- [Agent development lifecycle](./agents/concepts/development-lifecycle.md)
- [What's new in Microsoft Foundry](./whats-new-foundry.md)
- [Microsoft Foundry portal general availability overview](concepts/general-availability.md)
- [Upgrade your Azure OpenAI resource to a Foundry resource](./how-to/upgrade-azure-openai.md)
- [Find hub-based projects in the Foundry (classic) portal](../foundry-classic/what-is-foundry.md)
