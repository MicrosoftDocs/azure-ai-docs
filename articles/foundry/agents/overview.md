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

Foundry Agent Service is a fully managed platform for building, deploying, and scaling AI agents. Use any framework and [many models](./concepts/limits-quotas-regions.md) from the Foundry model catalog. Create no-code [prompt agents](#agent-types) in the Foundry portal, or use the available SDKs and REST API to deploy them and code-based **[hosted agents](concepts/hosted-agents.md)** built with Agent Framework, LangGraph, or your own code.

Agent Service handles hosting, scaling, identity, observability, and enterprise security so you can focus on your agent logic.

## Get started with agents

Ready to get started with agents? Choose your path based on how you want to build:

- **New to agents?** [Start with a prompt agent](../quickstarts/get-started-code.md) to create an agent with instructions and tools. Use the Foundry portal to create one with no code required, or use the SDKs or REST API.
- **Want to deploy an agent as a container with a framework of your choice?** [Build a hosted agent](quickstarts/quickstart-hosted-agent.md) with Agent Framework or LangGraph, deploy it to Foundry, and test it end-to-end.
- **Want to orchestrate multiple agents?** [Build a workflow](./concepts/workflow.md) to orchestrate agents and business logic in a visual builder.

## What is an agent?

An agent is an AI application that uses a large language model (LLM) to reason about user requests and take autonomous actions to fulfill them. Unlike a simple chatbot that only generates text, an agent can call tools, access external data, and make decisions across multiple steps to complete a task. Every agent combines three core components:

* **Model (LLM)**: Provides reasoning and language capabilities.
* **Instructions**: Define goals, constraints, and behavior. In Foundry, instructions can be prompt-based, workflow definitions, or hosted agent code.
* **Tools**: Provide access to data or actions, such as search, file operations, or API calls.

:::image type="content" source="media/what-is-an-agent.png" alt-text="A diagram showing the components of an AI agent.":::

## Agent Service at a glance

| Component | What it does |
| --- | --- |
| **Agent Runtime** | Hosts and scales both prompt agents and hosted agents. Manages conversations, tool calls, and agent lifecycle. |
| **Tools** | Built-in tools including web search, file search, memory, code interpreter, MCP servers, and custom functions. Extend your agent's capabilities without building infrastructure. Tools have managed authentication - service managed credentials and On-Behalf-Of (OBO) authentication. |
| **Models** | Works with many models from the Foundry model catalog, such as GPT-4o, Llama, and DeepSeek. Swap models without changing your agent code. |
| **Observability** | End-to-end tracing, metrics, and Application Insights integration. See every decision your agent makes. |
| **Identity & Security** | Microsoft Entra identity, RBAC, content filters, and virtual network isolation. Enterprise-grade trust built in. |
| **Publishing** | Version agents, create stable endpoints, and share through Microsoft Teams, Microsoft 365 Copilot, and the Entra Agent Registry. |

## Agent types

Agent Service supports three types of agents, each designed for different needs:

* Prompt agents
* Workflow agents (preview)
* Hosted agents (preview)

### Prompt agents

Prompt agents are defined entirely through configuration — instructions, model selection, and tools. Create them in the Foundry portal or through the API or SDKs, and Agent Service handles the orchestration and hosting automatically.

**Best for**: Rapid prototyping, internal tools, and agents that don't need custom orchestration logic. Create a working agent in minutes using the portal.

### Workflow agents (preview)

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

## Model support

Agent Service works with many models available in the Foundry model catalog. For the full list, see [Quotas, limits, and regional support](concepts/limits-quotas-regions.md).

## Tools

Agent Service provides built-in tools and supports custom tools so your agents can take actions and access data. For a full list, see the [Foundry tool catalog](concepts/tool-catalog.md). For advanced tool selection patterns, see [Tool best practices](concepts/tool-best-practice.md).

> [!NOTE]
> Some tools, including memory and web search, are in preview. For availability by region and preview status, see [tool support by region and model](./concepts/tool-best-practice.md#tool-support-by-region-and-model).

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
- **[Private networking](how-to/virtual-networks.md)** — Run agents within your Azure virtual network for full network isolation and compliance with data residency requirements. Private networking is available for prompt agents and workflow agents. Hosted agents don't currently support private networking during preview.
- **Role-based access control** — Fine-grained permissions through Microsoft Entra and Azure RBAC. Control who can create, invoke, and manage agents.
- **Content safety** — Integrated content filters help mitigate prompt injection risks (including cross-prompt injection) and prevent unsafe outputs.

For environment setup instructions, see [Set up your environment](environment-setup.md).

## Publishing and sharing

Agent Service provides built-in versioning and publishing so your agents can move from development to production with confidence.

- **Versioning** — As you iterate on your agent, versions are automatically snapshotted. Roll back to any previous version or compare changes between versions.
- **[Publishing](how-to/publish-agent.md)** — Promote an agent to a managed resource with a stable endpoint. Published agents inherit the [enterprise identity and access controls](#enterprise-capabilities) configured for your project and can be invoked programmatically.
- **Distribution** — Share published agents through [Microsoft 365 Copilot and Teams](how-to/publish-copilot.md) and the Entra Agent Registry, putting your agents where your users already work.

## Security, privacy, and compliance

Agent Service is designed for enterprise workloads where you need strong controls over identity, networking, data handling, and safety.

- **Safety controls**: Use integrated [guardrails](../guardrails/guardrails-overview.md) to help reduce unsafe outputs and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA).
- **Network isolation and data residency controls**: Use [virtual networks](how-to\virtual-networks.md) and bring-your-own resources to meet your requirements.
- **Bring your own resources**: Use your own Azure resources (for example, storage, Azure AI Search, and Azure Cosmos DB for conversation state) to meet compliance and operational needs. See [Use your own resources](how-to/use-your-own-resources.md).
- **Responsible AI guidance**: For a broader set of recommendations and governance resources, see [Responsible AI for Microsoft Foundry](../responsible-use-of-ai-overview.md).

## Related content

- [Set up your environment](environment-setup.md)
- [Agent development lifecycle](concepts/development-lifecycle.md)
- [Deploy your first hosted agent](quickstarts/quickstart-hosted-agent.md)
- [Tool catalog](concepts/tool-catalog.md)
- [Quotas, limits, and regional support](concepts/limits-quotas-regions.md)
- For help or to connect with the community, join the [Microsoft AI Discord](https://aka.ms/ai-discord).
