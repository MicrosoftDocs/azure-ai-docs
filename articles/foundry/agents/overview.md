---
title: "What is Microsoft Foundry Agent Service?"
description: "Learn about Microsoft Foundry Agent Service capabilities, agent types, tools, and runtime features for building AI agents."
manager: nitinme
author: aahill
ms.author: aahi
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: overview
ms.date: 05/27/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
keywords:
    - Foundry Agent Service
    - AI agents
    - agent orchestration
    - tool calling
    - content filters
    - agent observability
    - Hosted agents
    - prompt agents
    - workflow agents
    - Microsoft Foundry
    - agent development lifecycle
---

# What is Microsoft Foundry Agent Service?

Foundry Agent Service is a managed platform for building, deploying, and scaling AI agents. Use any framework, any [supported model](./concepts/limits-quotas-regions.md) from the Foundry model catalog, and the Foundry Responses API as a single entry point.

You choose how much of the platform you want:

- **Fully managed runtime** — author a [prompt agent](#prompt-agents) in the Foundry portal or define it with SDKs and REST, and Foundry runs it for you. No application code to maintain, no compute to pay for, and no containers or packages to optimize, scale, or patch. [Workflow agents](#workflow-agents-preview) extend this model with multi-step orchestration.
- **Code-based** — write your agent with Agent Framework, LangGraph, Semantic Kernel, or your own code, call the [Foundry Responses API](quickstarts/responses-api.md) for models and platform tools, then choose where it runs: your own infrastructure ([self-hosted](#self-hosted-run-in-your-own-process)) or Foundry-managed containers ([Hosted agents, preview](#hosted-agents-preview-deploy-as-a-container)).

## What is an agent?

An agent is an AI application that uses a model from the Foundry model catalog to reason about user requests and take autonomous actions to fulfill them. Unlike a simple chatbot that only generates text, an agent can call tools, access external data, and make decisions across multiple steps to complete a task. Every agent combines three core components:

* **Model**: A model from the Foundry model catalog that provides reasoning and language capabilities.
* **Instructions**: Define goals, constraints, and behavior. In Foundry, instructions can be prompt-based, workflow definitions, or code in a self-hosted or Hosted agent.
* **Tools**: Provide access to data or actions, such as search, file operations, or API calls.

:::image type="content" source="media/what-is-an-agent.png" alt-text="A diagram showing the components of an AI agent.":::

## Agent Service at a glance

| Component | What it does |
| --- | --- |
| **Foundry Responses API** | Single entry point for every agent type. Gives any framework, process, or runtime access to Foundry models plus platform tools (file search, code interpreter, memory, web search, MCP servers). |
| **Agent Runtime** | Hosts and scales prompt agents, workflow agents, and Hosted agents. Manages conversations, tool calls, and agent lifecycle. |
| **Tools** | Built-in tools including web search, file search, memory, code interpreter, MCP servers, and custom functions. Managed authentication includes service-managed credentials and On-Behalf-Of (OBO). |
| **Models** | Works with many models from the Foundry model catalog, such as GPT-4o, Llama, and DeepSeek. Swap models without changing your agent code. |
| **Observability** | End-to-end tracing, metrics, and Application Insights integration. See every decision your agent makes. |
| **Identity & Security** | Microsoft Entra identity, RBAC, content filters, and virtual network isolation. Enterprise-grade trust built in. |
| **Publishing** | Version agents, create stable endpoints, and share through Microsoft Teams, Microsoft 365 Copilot, and the Entra Agent Registry. |

## Get started with agents

Choose your path based on what you're trying to do:

- **New to agents?** [Start with a prompt agent](../quickstarts/get-started-code.md) — create an agent in the Foundry portal, pick a model, attach tools, then call it from code. No runtime code to write or maintain — Foundry runs the agent for you.
- **Have existing agent code (LangGraph, CrewAI, Agent Framework, custom)?** [Call the Foundry Responses API from your existing process](quickstarts/responses-api.md) to get Foundry models and platform tools without changing where your code runs. When you're ready, [package the same code as a Hosted agent](quickstarts/quickstart-hosted-agent.md) and let Foundry run the container.
- **Want to build code-based agents from scratch?** [Use Agent Framework with the Foundry Responses API](quickstarts/responses-api.md) to iterate locally, then graduate to Foundry-hosted deployment when you need a managed endpoint, scaling, and identity.
- **Want to orchestrate multiple agents without code?** [Build a workflow](./concepts/workflow.md) to chain agents and business logic in a visual builder.

## Agent types

There are two top-level decisions:

1. **Fully managed runtime vs. code-based** — do you want Foundry to run the agent (no runtime code, no compute to manage), or do you write and host your own agent code?
1. **For code-based agents, where does the code run?** — your infrastructure (self-hosted) or Foundry-managed containers (Hosted).

That gives you three categories:

* [Prompt agents](#prompt-agents) — author in portal or code, fully managed runtime.
* [Workflow agents (preview)](#workflow-agents-preview) — low-code orchestration, fully managed runtime.
* [Code-based agents](#code-based-agents) — your code, with a choice of hosting (self-hosted or Hosted).

### Prompt agents

Prompt agents are defined entirely through configuration — instructions, model selection, and tools. You author them in the Foundry portal for a quick start, or define them programmatically with the SDKs or REST API to integrate with your CI/CD workflows. Either way, Foundry runs the agent for you — there's no application code to maintain, no compute to pay for, and no containers or packages to optimize, scale, or monitor for security.

Two paths to get started:

- **Portal-first** — create an agent interactively in the Foundry portal, test it in the playground, then call it from your application code.
- **Code-first** — define the agent using the SDK or REST API in your deployment pipeline, enabling version control, code review, and automated rollout.

**Best for**: Getting started fast, internal tools, production agents that don't need custom orchestration logic, and teams that want a managed runtime without infrastructure overhead.

### Workflow agents (preview)

[Workflow agents](concepts/workflow.md) orchestrate multiple agents and business logic using declarative definitions. They serve two audiences from the same underlying representation:

- **Low-code builders** use the visual designer in the Foundry portal to drag together agents, branches, approvals, and tool calls.
- **Developers** edit the same workflow as YAML in Visual Studio Code, which makes it diffable, reviewable, and source-controllable.

Workflows support branching logic, human-in-the-loop steps, and sequential or group-chat patterns.

> [!NOTE]
> Specifics of the portal-to-YAML relationship (round-tripping, fidelity) and the role of Power Fx in workflow expressions are evolving in preview. [TO VERIFY before publication.]

**Best for**: Multi-step orchestration, agent-to-agent coordination, approval workflows, and scenarios that need repeatable automation without custom code.

### Code-based agents

Code-based agents are built with [Agent Framework](https://github.com/microsoft/agent-framework), LangGraph, Semantic Kernel, or your own code. They call the **Foundry Responses API** for model inference and tool orchestration, which gives you access to Foundry models from the catalog and platform tools — file search, code interpreter, memory, web search, MCP servers, and more — that aren't available through the OpenAI API alone.

The same agent code can run in two places. These aren't competing products — they're a graduation path. Build and iterate self-hosted, then deploy the same code as a Hosted agent when you need a managed endpoint and Foundry-managed scaling.

#### Self-hosted: run in your own process

[Self-hosted agents](quickstarts/responses-api.md) run in your own process or on your own infrastructure. They use `FoundryChatClient` to call the Foundry Responses API, but the agent definition isn't persisted to Foundry. You manage hosting, scaling, and the endpoint. Foundry provides the models, the platform tools, and the API.

**Best for**: Local development and iteration, custom function tools that need direct access to your libraries and data, and scenarios where you already have infrastructure for hosting agent code.

#### Hosted agents (preview): deploy as a container

[Hosted agents](concepts/hosted-agents.md) take the same code, packaged as a container, and deploy it to Agent Service. Foundry adds a managed endpoint, automatic scaling on isolated Micro VMs, a dedicated Microsoft Entra identity, session-level state persistence, and end-to-end observability.

> [!NOTE]
> Hosted agents are currently in public preview.

**Best for**: Production deployment of code-based agents, multi-agent systems, custom protocols (webhooks, voice, AG-UI), and scenarios where you want Foundry to handle hosting, scaling, and identity for you.

### Compare agent types

Use these tables to choose between authoring models first, then — if you're going code-based — between hosting models.

#### Authoring: no-code, low-code, or code

| | Prompt agents | Workflow agents (preview) | Code-based agents |
| --- | --- | --- | --- |
| **Authoring surface** | Portal, SDK, or REST | Visual designer or YAML | Agent Framework, LangGraph, Semantic Kernel, custom code |
| **Skill profile** | Anyone | Low-code builder or developer | Developer |
| **Foundry models + platform tools** | Yes | Yes | Yes (via Foundry Responses API) |
| **Runtime code to maintain** | None | None | Yes — your agent logic |
| **Compute to manage** | None — fully managed | None — fully managed | Your own compute (self-hosted) or container compute (Hosted) |
| **Cost model** | Per-call inference + tool usage | Per-call inference + workflow execution | Per-call inference + tool usage; plus your own compute (self-hosted) or container compute (Hosted) |
| **Deployment complexity** | None (portal) or SDK/REST in CI/CD | Low — visual or YAML | Medium to High — your build/CD pipeline, or container build + push |
| **Best for** | Fast start, production agents without infrastructure overhead | Multi-step automation, agent-to-agent coordination | Custom orchestration, integration with existing code, advanced control |

#### Hosting (code-based agents only): self-hosted or Foundry-hosted

| | Self-hosted | Hosted (preview) |
| --- | --- | --- |
| **Where it runs** | Your process or infrastructure | Foundry-managed containers on isolated Micro VMs |
| **Same code?** | Yes | Yes — same code, same Foundry Responses API |
| **Managed endpoint** | No — you provide it | Yes |
| **Scaling & lifecycle** | You manage | Foundry-managed |
| **Cold start / latency** | None beyond your own process | Session warmup on first call to a cold Micro VM |
| **Agent identity (Entra)** | You configure | Automatic, dedicated per agent |
| **Session state** | You implement | Session-level state persisted by Foundry |
| **Observability** | SDK-level tracing | Full platform tracing and dashboards |
| **Best for** | Local iteration, integrating with existing code and infrastructure | Production deployment, custom protocols, multi-agent systems |

## Model support

Agent Service works with many models available in the Foundry model catalog. For the full list, see [Quotas, limits, and regional support](concepts/limits-quotas-regions.md).

## Tools

Agent Service provides built-in tools and supports custom tools so your agents can take actions and access data. For a full list, see the [Foundry tool catalog](concepts/tool-catalog.md). For advanced tool selection patterns, see [Tool best practices](concepts/tool-best-practice.md).

Foundry supports remote MCP servers that you can add from the **Add Tools** catalog in the Foundry portal. For example, the Azure DevOps MCP Server (public preview) can be added directly from the catalog. Connect your Azure DevOps organization to enable agent access, and configure a subset of available tools to control which actions agents can perform. You can also connect custom MCP servers hosted on Azure Functions using the Functions MCP webhook endpoint (`/runtime/webhooks/mcp`) to expose custom tools to your agents.

Supported authentication options for MCP servers and other tool connections include:

- Key-based access
- Microsoft Entra (using the agent's managed identity or the project's managed identity)
- OAuth identity passthrough (On-Behalf-Of)
- Unauthenticated access, where appropriate

### Toolbox (preview)

[Toolbox](how-to/tools/toolbox.md) lets you define a curated set of tools once, manage them centrally in Foundry, and expose them through a single MCP-compatible endpoint. Any MCP-compatible agent runtime or client can consume a toolbox, regardless of the framework you use. Toolbox versioning gives you explicit control over when changes take effect — create a new version, test it, and promote it to default when you're ready.

> [!NOTE]
> Some tools, including memory and web search, are in preview. For availability by region and preview status, see [tool support by region and model](./concepts/tool-best-practice.md#tool-support-by-region-and-model).

## Development lifecycle

Agent Service supports the full build-test-deploy-monitor workflow:

1. **Create** — Define a prompt agent in the portal or with the SDK, build a workflow visually or in YAML, or write a code-based agent that calls the Foundry Responses API.
1. **Test** — Chat with your agent in the [agents playground](../concepts/concept-playgrounds.md) or run locally. MCP server integrations, including custom MCP servers hosted on Azure Functions, can be exercised directly in the playground to validate tool connectivity, permissions, and behavior before publishing.
1. **Trace** — Inspect every model call, tool invocation, and decision with [agent tracing](../observability/concepts/trace-agent-concept.md).
1. **Evaluate** — Run evaluations to measure quality and catch regressions.
1. **Publish** — [Promote your agent](how-to/agent-applications.md) to a managed resource with a stable endpoint. For code-based agents, this is the point where you graduate from self-hosted to deploying as a Hosted agent.
1. **Monitor** — Track performance and reliability with [service metrics](../observability/how-to/how-to-monitor-agents-dashboard.md) and dashboards.

For a detailed walkthrough, see [Agent development lifecycle](concepts/development-lifecycle.md).

## Enterprise capabilities

Agent Service provides enterprise-grade infrastructure for every agent you deploy:

- **[Agent identity](concepts/agent-identity.md)** — Each agent can have a dedicated Microsoft Entra identity, enabling secure, scoped access to resources and APIs without sharing credentials. Agent identities can authenticate to external MCP servers, including those hosted on Azure Functions, and OAuth On-Behalf-Of (OBO) passthrough is supported when configured.
- **[Private networking](how-to/virtual-networks.md)** — Run agents within your Azure virtual network for full network isolation and compliance with data residency requirements. Private networking is available for prompt agents and workflow agents. Hosted agents support bring-your-own Azure Virtual Network (BYO VNet), where each session runs in a VM-isolated sandbox connected to your VNet.
- **Role-based access control** — Fine-grained permissions through Microsoft Entra and Azure RBAC. Control who can create, invoke, and manage agents.
- **Content safety** — Integrated content filters help mitigate prompt injection risks (including cross-prompt injection) and prevent unsafe outputs.

For environment setup instructions, see [Set up your environment](environment-setup.md).

## Publishing and sharing

Agent Service provides built-in versioning and publishing so your agents can move from development to production with confidence.

- **Versioning** — As you iterate on your agent, versions are automatically snapshotted. Roll back to any previous version or compare changes between versions.
- **[Publishing](how-to/agent-applications.md)** — Promote an agent to a managed resource with a stable endpoint. Published agents inherit the [enterprise identity and access controls](#enterprise-capabilities) configured for your project and can be invoked programmatically.
- **Distribution** — Share published agents through [Microsoft 365 Copilot and Teams](how-to/publish-copilot.md) and the Entra Agent Registry, putting your agents where your users already work. Foundry Agent Service supports the OpenResponses and Activity Protocols for Microsoft 365 publishing, an Invocations protocol for flexible endpoint integration with custom apps and services, and the [A2A protocol (preview)](how-to/enable-agent-to-agent-endpoint.md) for agent-to-agent communication.

## Security, privacy, and compliance

Agent Service is designed for enterprise workloads where you need strong controls over identity, networking, data handling, and safety.

- **Safety controls**: Use integrated [guardrails](../guardrails/guardrails-overview.md) to help reduce unsafe outputs and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA).
- **Network isolation and data residency controls**: Use [virtual networks](how-to/virtual-networks.md) and bring-your-own resources to meet your requirements.
- **Bring your own resources**: Use your own Azure resources (for example, storage, Azure AI Search, and Azure Cosmos DB for conversation state) to meet compliance and operational needs. See [Use your own resources](how-to/use-your-own-resources.md).
- **Responsible AI guidance**: For a broader set of recommendations and governance resources, see [Responsible AI for Microsoft Foundry](../responsible-use-of-ai-overview.md).

## Related content

- [Set up your environment](environment-setup.md)
- [Agent development lifecycle](concepts/development-lifecycle.md)
- [Deploy your first Hosted agent](quickstarts/quickstart-hosted-agent.md)
- [Tool catalog](concepts/tool-catalog.md)
- [Quotas, limits, and regional support](concepts/limits-quotas-regions.md)
- For help or to connect with the community, join the [Microsoft AI Discord](https://aka.ms/ai-discord).
