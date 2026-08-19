---
title: "What is Microsoft Foundry Agent Service?"
description: "Learn about Microsoft Foundry Agent Service capabilities, agent types, tools, and runtime features for building AI agents."
manager: mcleans
author: aahill
ms.author: aahi
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: overview
ms.date: 08/13/2026
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
    - Microsoft Foundry
    - agent development lifecycle
---

# Agents in Microsoft Foundry

Foundry Agent Service is a managed platform for building, deploying, and scaling AI agents. Build with any framework, any [supported model](https://ai.azure.com/catalog/models?capabilities=agentsv2&cid=learnDocs) from the Foundry model catalog, and a single entry point for model inference and tools.

Foundry meets you anywhere on the spectrum from declarative to full code: define a **prompt agent** and let Foundry run it, package your own code as a **hosted agent**, or call the **Responses API** from an agent you already run elsewhere. [Choose how to build](#choose-how-to-build) covers each path.

## Agent Service at a glance

| Component | What it does |
| --- | --- |
| **[Agent Runtime](concepts/runtime-components.md)** | Hosts and scales prompt agents and Hosted agents. Manages conversations, tool calls, and agent lifecycle. |
| **[Toolboxes](concepts/toolbox-overview.md)** | Curate a set of tools once, such as: web search, file search, code interpreter, MCP servers, and custom functions. Then share them across agents through a single managed MCP endpoint with centralized authentication, governance, and versioning. |
| **[Models](https://ai.azure.com/catalog/models?capabilities=agentsv2&cid=learnDocs)** | Works with many models from the Foundry model catalog, such as GPT-4o, Llama, and DeepSeek. Swap models without changing your agent code. |
| **[Observability](../observability/concepts/trace-agent-concept.md)** | End-to-end tracing, metrics, evaluations, and Application Insights integration. See every decision your agent makes and measure its quality. |
| **[Optimization](concepts/agent-optimizer-overview.md)** | Agent optimizer (preview) evaluates agent behavior and automatically generates better instructions, skills, tool descriptions, and model selections for prompt agents and Hosted agents. |
| **[Identity & Security](concepts/agent-identity.md)** | Microsoft Entra identity, RBAC, content filters, and virtual network isolation. Enterprise-grade trust built in. |
| **[Publishing](how-to/publish-copilot.md)** | Version agents, create stable endpoints, and share through Microsoft Teams, Microsoft 365 Copilot, and the Entra Agent Registry. |

## Choose how to build

> [!TIP]
> Building your first agent? Start with a prompt agent using either the [Foundry portal](https://ai.azure.com/?cid=learnDocs), or the quickstart for [creating a prompt agent with code](quickstarts/prompt-agent.md).

Foundry gives you several ways to build, from a single model call to a fully containerized agent. Choose your path based on what you're trying to do:

- **Want the least to manage?** [Start with a prompt agent](./quickstarts/prompt-agent.md). Configure instructions, a model, and tools; Foundry runs it with no code or infrastructure.
- **Want full control in Foundry?** [Deploy a hosted agent](quickstarts/quickstart-hosted-agent.md). Bring your own code and framework as a container; Foundry runs it with a managed endpoint, scaling, and identity.
- **Already run agent code elsewhere?** [Call the Responses API](quickstarts/responses-api.md) directly to use Foundry models and tools, with no agent resource to manage.

Prompt agents and hosted agents are the two agent types in Foundry. The next section breaks down the value of each so you can choose with confidence.

## Agent types

Agent Service offers two agent types. Your choice sets how much you build versus how much Foundry manages:

- **[Prompt agents](#prompt-agents)**: the fastest path. Define instructions, a model, and tools, and Foundry runs the agent for you with no code or infrastructure to manage.
- **[Hosted agents](#hosted-agents)**: the most control. Bring your own code and framework, and Foundry runs it as a container with a managed endpoint, scaling, and identity.

### Prompt agents

You define prompt agents entirely through configuration, including instructions, model selection, and tools. Author them in the Foundry portal for a quick start, or define them programmatically with the SDKs or REST API to integrate with your CI/CD workflows. Either way, Foundry runs the agent for you. There's no application code to maintain, and no containers or packages to optimize, scale, or monitor for security.

Two paths to get started:

- **Portal-first**: create an agent interactively in the Foundry portal, test it in the playground, then call it from your application code.
- **Code-first**: define the agent using the SDK or REST API in your deployment pipeline, enabling version control, code review, and automated rollout.

**Best for**: Getting started fast, internal tools, production agents that don't need custom orchestration logic, and teams that want a managed runtime without infrastructure overhead.

### Hosted agents

[Hosted agents](concepts/hosted-agents.md) are code-based agents you build with [Agent Framework](https://github.com/microsoft/agent-framework), [LangGraph](https://github.com/langchain-ai/langgraph), the [OpenAI Agents SDK](https://github.com/openai/openai-agents-python), the [Anthropic Agent SDK](https://github.com/anthropics/anthropic-sdk-python), the [GitHub Copilot SDK](https://github.com/github/copilot-sdk), or your own code. Ship your agent as either a container image or a .zip file of your source code (Foundry builds the image for you when you bring a .zip file), and Foundry runs it with a managed endpoint, automatic scaling, a dedicated Microsoft Entra identity, session-level state persistence, and end-to-end observability.

Under the hood, your agent code calls your Foundry project endpoint for model inference and tool orchestration, which gives you access to Foundry models from the catalog and a unified set of platform tools: standard tools like file search, code interpreter, and web search, plus additional tools like SharePoint, WorkIQ, and Fabric IQ.

**Best for**: Agents that call into your own custom code; secondarily, custom orchestration logic, multi-agent systems, and custom protocols (webhooks, voice, AG-UI) where you want full control over agent logic while letting Foundry handle hosting, scaling, and identity.

### Compare agent types

| | Prompt agents | Hosted agents |
| --- | --- | --- |
| **Authoring surface** | Portal, SDK, or REST | Agent Framework, LangGraph, OpenAI Agents SDK, Anthropic Agent SDK, GitHub Copilot SDK, custom code |
| **Foundry models + platform tools** | Yes | Yes (via the Responses API on the Foundry project endpoint) |
| **Skill support** | Yes | Yes |
| **Runtime code to maintain** | None | Yes, your agent logic |
| **Compute to manage** | None, fully managed | Container compute, Foundry-managed |
| **Managed endpoint** | Yes | Yes |
| **Autoscale** | Automatic, Foundry-managed; scales with request volume | Automatic, Foundry-managed; scales container instances per session and request volume |
| **Agent identity (Entra)** | Yes | Automatic, dedicated per agent |
| **Cost model** | Per-call inference + tool usage | Per-call inference + tool usage + container compute |
| **Best for** | Fast start, production agents without custom orchestration | Agents that call into custom code; secondarily, custom orchestration logic |

### Use the Responses API for ephemeral agents

When you call the Responses API directly from your own code, you build an *ephemeral agent*: the agent's definition (instructions, tools, and model) lives in your application code instead of as a persisted resource in Foundry. Each call assembles the agent in your process and runs it against the Responses API, so there's no agent to create, update, or delete in Foundry.

Use this pattern when you want:

- **Agent logic that ships with your app.** The definition versions alongside the rest of your code through source control and code review, instead of as a separate Foundry resource that someone has to keep in sync with the app.
- **Foundry capabilities without the resource overhead.** You still get catalog models, platform tools, project-scoped data, On-Behalf-Of authentication, and project-level observability and governance. All through your Foundry project endpoint.

See [Quickstart: Use the Responses API](quickstarts/responses-api.md) for information.

## Model support

Agent Service works with many models available in the Foundry model catalog. For the full list, see the [Foundry portal](https://ai.azure.com/catalog/models?capabilities=agentsv2&cid=learnDoc).

## Tools and toolboxes

Agents act on the world through **tools**. Foundry offers built-in tools such as web search, file search, code interpreter, and memory, while also letting you add custom tools through functions, OpenAPI specs, and MCP servers. For the full set, see the [toolbox overview](concepts/toolbox-overview.md#supported-tools).

A **toolbox** groups those tools into a single, reusable unit. You curate the tools once, and Foundry exposes them behind one managed MCP-compatible endpoint that any agent or runtime can consume, regardless of framework. Toolboxes centralize authentication, governance, and versioning, so you update tools in one place instead of rewiring every agent. Create a new version, test it, and promote it to default when you're ready. To learn more, see [What is Toolbox in Foundry?](concepts/toolbox-overview.md).

### Connect and authenticate to MCP remote servers

Foundry supports remote MCP servers that you can add to your agent, such as the [Azure DevOps MCP Server](/azure/devops/mcp-server/mcp-server-overview). Connect your Azure DevOps organization to enable agent access, and configure a subset of available tools to control which actions agents can perform. You can also connect custom MCP servers hosted on Azure Functions using the Functions MCP webhook endpoint (`/runtime/webhooks/mcp`) to expose custom tools to your agents.

Supported authentication options for MCP servers and other tool connections include:

- Key-based access
- Microsoft Entra (using the agent's managed identity or the project's managed identity)
- OAuth identity passthrough (On-Behalf-Of)
- Unauthenticated access, where appropriate

These authentication options also apply when connecting remote MCP servers, with credentials and scopes managed in the tool configuration.

## Development lifecycle

Agent Service supports the full build-test-deploy-monitor workflow:

1. **Create**: Define a prompt agent in the portal or with the SDK, or write a Hosted agent that calls the Responses API.
1. **Test**: Chat with your agent in the [agents playground](../concepts/concept-playgrounds.md) or run locally. MCP server integrations, including custom MCP servers hosted on Azure Functions, can be exercised directly in the playground to validate tool connectivity, permissions, and behavior before publishing.
1. **Trace**: Inspect every model call, tool invocation, and decision with [agent tracing](../observability/concepts/trace-agent-concept.md).
1. **Evaluate**: Run evaluations to measure quality and catch regressions.
1. **Optimize**: Automatically improve your hosted agent's instructions using the [agent optimizer](concepts/agent-optimizer-overview.md).
1. **Publish**: [Promote your agent](how-to/agent-applications.md) to a managed resource with a stable endpoint.
1. **Monitor**: Track performance and reliability with [service metrics](../observability/how-to/how-to-monitor-agents-dashboard.md) and dashboards.

For a detailed walkthrough, see [Agent development lifecycle](concepts/development-lifecycle.md).

## Enterprise capabilities

Agent Service provides enterprise-grade infrastructure for every agent you deploy:

- **[Agent identity](concepts/agent-identity.md)**: Each agent can have a dedicated Microsoft Entra identity, enabling secure, scoped access to resources and APIs without sharing credentials. Agent identities can authenticate to external MCP servers, including those hosted on Azure Functions, and OAuth On-Behalf-Of (OBO) passthrough is supported when configured.
- **[Private networking](how-to/virtual-networks.md)**: Run agents within your Azure virtual network for full network isolation and compliance with data residency requirements. Private networking is available for prompt agents. Hosted agents support bring-your-own Azure Virtual Network (BYO VNet), where each session runs in a VM-isolated sandbox connected to your VNet.
- **Role-based access control**: Fine-grained permissions through Microsoft Entra and Azure RBAC. Control who can create, invoke, and manage agents.
- **Content safety**: Integrated content filters help mitigate prompt injection risks (including cross-prompt injection) and prevent unsafe outputs.

For environment setup instructions, see [Set up your environment](environment-setup.md).

## Publishing and sharing

Agent Service provides built-in versioning and publishing so your agents can move from development to production with confidence.

- **Versioning**: As you iterate on your agent, versions are automatically snapshotted. Roll back to any previous version or compare changes between versions.
- **[Publishing](how-to/agent-applications.md)**: Promote an agent to a managed resource with a stable endpoint. Published agents inherit the [enterprise identity and access controls](#enterprise-capabilities) configured for your project and can be invoked programmatically.
- **Distribution**: Share published agents through [Microsoft 365 Copilot and Teams](how-to/publish-copilot.md) and the Entra Agent Registry, putting your agents where your users already work. Foundry Agent Service supports the OpenResponses and Activity Protocols for Microsoft 365 publishing, an Invocations protocol for flexible endpoint integration with custom apps and services, and the [A2A protocol (preview)](how-to/enable-agent-to-agent-endpoint.md) for agent-to-agent communication.

## Security, privacy, and compliance

Agent Service is designed for enterprise workloads where you need strong controls over identity, networking, data handling, and safety.

- **Safety controls**: Use integrated [guardrails](../guardrails/guardrails-overview.md) to help reduce unsafe outputs and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA).
- **Network isolation and data residency controls**: Use [virtual networks](how-to/virtual-networks.md) and bring-your-own resources to meet your requirements.
- **Bring your own resources**: Use your own Azure resources (for example, storage, Azure AI Search, and Azure Cosmos DB for conversation state) to meet compliance and operational needs. See [Use your own resources](how-to/use-your-own-resources.md).
- **Responsible AI guidance**: For a broader set of recommendations and governance resources, see [Responsible AI for Microsoft Foundry](../responsible-use-of-ai-overview.md).

## Related content

- [Set up your environment](environment-setup.md)
- [Agent development lifecycle](concepts/development-lifecycle.md)
- [Deploy your first hosted agent](quickstarts/quickstart-hosted-agent.md)
- [Tool catalog](concepts/tool-catalog.md)
- [Quotas, limits, and regional support](concepts/limits-quotas-regions.md)
- For help or to connect with the community, join the [Microsoft AI Discord](https://aka.ms/ai-discord).
