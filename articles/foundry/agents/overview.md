---
title: "What is Microsoft Foundry Agent Service?"
description: "Learn about Microsoft Foundry Agent Service capabilities, agent types, tools, and runtime features for building AI agents."
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: overview
ms.date: 03/10/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
keywords:
    - Foundry Agent Service
    - AI agents
    - agent orchestration
    - tool calling
    - content filters
    - agent observability
    - hosted agents
    - prompt agents
    - workflow agents
    - Microsoft Foundry
    - agent development lifecycle
---

# What is Microsoft Foundry Agent Service?

Foundry Agent Service is a fully managed platform for building, deploying, and scaling AI agents. Use any framework and any model from the [Foundry model catalog](../foundry-models/how-to/deploy-foundry-models.md). Create no-code **prompt agents** in the Foundry portal, or deploy code-based **[hosted agents](concepts/hosted-agents.md)** built with Agent Framework, LangGraph, or your own code.

Agent Service handles hosting, scaling, identity, observability, and enterprise security so you can focus on your agent logic.

## What is an agent?

An agent is an AI application that uses a large language model (LLM) to reason about user requests and take autonomous actions to fulfill them. Unlike a simple chatbot that only generates text, an agent can call tools, access external data, and make decisions across multiple steps to complete a task. Every agent combines three core components:

* **Model (LLM)**: Provides reasoning and language capabilities.
* **Instructions**: Define goals, constraints, and behavior. In Foundry, instructions can be prompt-based, workflow definitions, or hosted agent code.
* **Tools**: Provide access to data or actions, such as search, file operations, or API calls.

:::image type="content" source="media/what-is-an-agent.png" alt-text="A diagram showing the components of an AI agent.":::

Agent Service provides:

* **Agent Runtime**: Hosts and scales both prompt agents and hosted agents. Manages conversations, tool calls, and [agent lifecycle](concepts/development-lifecycle.md).
* **Observability**: End-to-end tracing, metrics, and Application Insights integration. See every decision your agent makes.
**Identity & Security**: Microsoft Entra identity, RBAC, content filters, and virtual network isolation. Enterprise-grade trust is built in.
**Publishing**: Version agents, create stable endpoints, and share through Microsoft Teams, Microsoft 365 Copilot, and the Entra Agent Registry.

## Agent types

Agent Service supports three types of agents, each designed for different needs.

### Prompt agents

Prompt agents are defined entirely through configuration — instructions, model selection, and tools. Create them in the Foundry portal or through the API or SDKs, and Agent Service handles the orchestration and hosting automatically.

**Best for**: Rapid prototyping, internal tools, and agents that don't need custom orchestration logic. Create a working agent in minutes using the portal.

### Workflow agents

[Workflow agents](concepts/workflow.md) orchestrate a sequence of actions or coordinate multiple agents using declarative definitions. Build workflows visually in the Foundry portal or define them in YAML through Visual Studio Code. Workflows support branching logic, human-in-the-loop steps, and sequential or group-chat patterns.

**Best for**: Multi-step orchestration, agent-to-agent coordination, approval workflows, and scenarios that need repeatable automation without custom code.

### Hosted agents (preview)

[Hosted agents](concepts/hosted-agents.md) are code-based agents built with a framework of your choice and deployed as containers on Agent Service. You write the orchestration logic — tool calls, multi-step reasoning, agent-to-agent coordination — and Foundry manages the runtime, scaling, and infrastructure.

> [!NOTE]
> Hosted agents are currently in public preview.

**Best for**: Complex workflows, custom tool integrations, multi-agent systems, and scenarios where you need full control over agent behavior.

### Compare agent types

| | Prompt agents | Workflow agents | Hosted agents (preview) |
| --- | --- | --- | --- |
| **Code required** | No | No (YAML optional) | Yes |
| **Hosting** | Fully managed | Fully managed | Container-based, managed |
| **Orchestration** | Single agent | Multi-agent, branching | Custom logic |
| **Best for** | Prototyping, simple tasks | Multi-step automation | Full control, custom frameworks |

## Framework and model support

Agent Service is framework-agnostic. Bring the framework that fits your team and use case.

| Framework | Python | C# |
| --- | --- | --- |
| Microsoft Agent Framework (recommended) | Supported | Supported |
| LangGraph | Supported | — |
| Custom code | Supported | Supported |

Agent Service works with any model available in the Foundry model catalog. For the full list, see [Quotas, limits, and regional support](concepts/limits-quotas-regions.md).

## Tools

Agent Service provides built-in tools and supports custom tools so your agents can take actions and access data.

| Tool | Description |
| --- | --- |
| [Web search (Bing)](how-to/tools/bing-tools.md) | Search the web for real-time information. |
| [File search](how-to/tools/file-search.md) | Search uploaded files and [vector stores](concepts/vector-stores.md). |
| [Code interpreter](how-to/tools/custom-code-interpreter.md) | Execute code dynamically for calculations and data analysis. |
| [Function calling](how-to/tools/function-calling.md) | Call your own functions to integrate with external systems. |
| [MCP servers](how-to/tools/model-context-protocol.md) | Connect Model Context Protocol servers for extensible tool access. |
| [OpenAPI](how-to/tools/openapi.md) | Invoke any API described by an OpenAPI specification. |
| [Azure AI Search](how-to/tools/ai-search.md) | Query your Azure AI Search indexes for grounded retrieval. |
| [Image generation](how-to/tools/image-generation.md) | Generate images from text descriptions. |

This table highlights commonly used tools. For the full list, including Browser Automation, Computer Use, Microsoft Fabric, SharePoint, and Agent-to-Agent, see the [Foundry tool catalog](concepts/tool-catalog.md). For advanced tool selection patterns, see [Tool best practices](concepts/tool-best-practice.md).

## Development lifecycle

Agent Service supports the full build-test-deploy-monitor workflow:

1. **Create** — Define a prompt agent in the portal or build a hosted agent in code.
1. **Test** — Chat with your agent in the [agents playground](../concepts/concept-playgrounds.md) or run locally.
1. **Trace** — Inspect every model call, tool invocation, and decision with [agent tracing](../observability/concepts/trace-agent-concept.md).
1. **Evaluate** — Run evaluations to measure quality and catch regressions.
1. **Publish** — [Promote your agent](how-to/publish-agent.md) to a managed resource with a stable endpoint.
1. **Monitor** — Track performance and reliability with [service metrics](how-to/metrics.md) and dashboards.

For a detailed walkthrough, see [Agent development lifecycle](concepts/development-lifecycle.md).

## Enterprise capabilities

Agent Service provides enterprise-grade infrastructure for every agent you deploy:

- **[Agent identity](concepts/agent-identity.md)** — Each agent can have a dedicated Microsoft Entra identity, enabling secure, scoped access to resources and APIs without sharing credentials.
- **[Private networking](how-to/virtual-networks.md)** — Run agents within your Azure virtual network for full network isolation and compliance with data residency requirements.
- **Role-based access control** — Fine-grained permissions through Microsoft Entra and Azure RBAC. Control who can create, invoke, and manage agents.
- **Content safety** — Integrated content filters help mitigate prompt injection risks (including cross-prompt injection) and prevent unsafe outputs.

For environment setup instructions, see [Set up your environment](environment-setup.md).

## Publishing and sharing

Agent Service provides built-in versioning and publishing so your agents can move from development to production with confidence.

- **Versioning** — As you iterate on your agent, versions are automatically snapshotted. Roll back to any previous version or compare changes between versions.
- **[Publishing](how-to/publish-agent.md)** — Promote an agent to a managed resource with a stable endpoint. Published agents inherit the [enterprise identity and access controls](#enterprise-capabilities) configured for your project and can be invoked programmatically.
- **Distribution** — Share published agents through [Microsoft 365 Copilot and Teams](how-to/publish-copilot.md) and the Entra Agent Registry, putting your agents where your users already work.

## Get started

Choose your path based on how you want to build:

- **New to agents? Start with a prompt agent.** Open the Foundry portal, create an agent with instructions and tools, and test it in minutes — no code required.
  [Microsoft Foundry quickstart](../quickstarts/get-started-code.md)

- **Ready to code? Deploy a hosted agent.** Build an agent with Agent Framework or LangGraph, deploy it to Foundry, and test it end-to-end.
  [Quickstart: Deploy a hosted agent](quickstarts/quickstart-hosted-agent.md)

For help or to connect with the community, join the [Microsoft AI Discord](https://aka.ms/ai-discord).

## Related content

- [Set up your environment](environment-setup.md)
- [Agent development lifecycle](concepts/development-lifecycle.md)
- [Hosted agents](concepts/hosted-agents.md)
- [Agent runtime components](concepts/runtime-components.md)
- [Agent identity](concepts/agent-identity.md)
- [Tool catalog](concepts/tool-catalog.md)
- [Tool best practices](concepts/tool-best-practice.md)
- [Workflows](concepts/workflow.md)
- [Memory](concepts/what-is-memory.md)
- [Foundry IQ](concepts/what-is-foundry-iq.md)
- [Quotas, limits, and regional support](concepts/limits-quotas-regions.md)
- [Deploy your first hosted agent](quickstarts/quickstart-hosted-agent.md)
- [Publish and share agents](how-to/publish-agent.md)
- [Microsoft Foundry SDK overview](../how-to/develop/sdk-overview.md)