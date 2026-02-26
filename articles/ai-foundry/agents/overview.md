---
title: What is Foundry Agent Service?
titleSuffix: Microsoft Foundry
description: Learn what Foundry Agent Service is, how it works, and how to build production-ready agents in Microsoft Foundry.
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: overview
ms.date: 01/21/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
keywords:
    - Foundry Agent Service
    - AI agents
    - agent orchestration
    - tool calling
    - content filters
    - agent observability
---

# What is Foundry Agent Service?

[!INCLUDE [version-banner](../includes/version-banner.md)]

Most businesses don't want just chatbots. They want automation that's faster and has fewer errors. That desire might mean summarizing documents, processing invoices, managing support tickets, or publishing blog posts. In all cases, the goal is the same: freeing people and resources to focus on higher-value work by offloading repetitive and predictable tasks.

Large language models (LLMs) introduce a new type of automation with systems that can understand unstructured data, make decisions, and generate content. In practice, businesses can have difficulty moving beyond demos and into production. LLMs can drift, be incorrect, and lack accountability. Without visibility, policy enforcement, and orchestration, these models are hard to trust in real business workflows.

:::row:::
    :::column span="1":::
*Microsoft Foundry* is designed to change that. It's a platform that combines models, tools, frameworks, and governance into a unified system for building intelligent agents. At the center of this system is *Foundry Agent Service*, which enables the operation of agents across development, deployment, and production.
    :::column-end:::
    :::column span="3":::
![Diagram that shows Foundry Agent Service as the central hub connecting four components: AI models on the left, tools and frameworks on the top, governance and compliance on the right, and orchestration at the bottom. Arrows indicate Agent Service enables agents to move from development through deployment to production.](media/agent-service-the-glue.png)
    :::column-end:::
:::row-end:::

Agent Service connects the core pieces of Foundry, such as models, tools, and frameworks, into a single runtime. It manages conversations, orchestrates tool calls, enforces content safety, and integrates with identity, networking, and observability systems. These capabilities help you build agents that are secure, scalable, and production ready.

By abstracting away infrastructure complexity and enforcing trust and safety by design, Agent Service can help you move from prototype to production with confidence.

## Prerequisites

- An Azure subscription with permission to create and manage Foundry resources.
- A Foundry project. If you haven't created one yet, start with [environment setup](environment-setup.md).
- A deployed model that your agent can use. Model and region availability can vary; see [models that inform agents](concepts\model-region-support.md).

## Availability, regions, and limits

Agent Service capabilities can vary based on the Foundry experience you're using and the model and region you choose.

- For service limits, quotas, and throttling considerations, see [Quotas and limits for Agent Service](quotas-limits.md).
- For model and region support, see [models that inform agents](concepts\model-region-support.md).

If you're building your first agent, start with the quickstart links in [Get started with Foundry Agent Service](#get-started-with-foundry-agent-service) to make sure you're on the right API path for your Foundry experience.

## What is an AI agent?

Agents make decisions, invoke tools, and participate in workflows. They perform these tasks sometimes independently and sometimes in collaboration with other agents or humans. They're foundational to real process automation.

Agents you create through Foundry aren't monoliths. They're composable units. Each agent has a specific role, is powered by the right model, and is equipped with the right tools. You deploy each agent within a secure, observable, and governable runtime.

An agent has three core components:

- **Model (LLM)**: Powers reasoning and language understanding.
- **Instructions**: Define the agent's goals, behavior, and constraints. They can have the following types:
  - Declarative:
    - Prompt based: A declaratively defined single agent that combines model configuration, instruction, tools, and natural language prompts to drive behavior.
    - Workflow: An agentic workflow that can be expressed as a YAML or other code to orchestrate multiple agents together, or to trigger an action on certain criteria.
  - Hosted: Containerized agents that are created and deployed in code and are hosted by Foundry.
- **Tools**: Let the agent retrieve knowledge or take action.

![Diagram that shows an agent receiving user inputs on the left, processing them through the model and instructions in the center, and producing outputs on the right. A bidirectional arrow below the agent connects to tools, indicating the agent can call tools during processing to retrieve knowledge or take actions.](media/what-is-an-agent.png)

Agents receive unstructured inputs such as user prompts, alerts, or messages from other agents. They produce outputs in the form of tool results or messages. Along the way, they might call tools to perform retrieval or trigger actions.

## How do agents in Foundry work?

Think of Foundry as an assembly line for intelligent agents. Like any modern factory, Foundry brings together specialized stations that are each responsible for shaping part of the final product. Instead of machines and conveyor belts, the agent factory uses models, tools, policies, and orchestration to build agents that are secure, testable, and production ready. Here's how the factory works step by step:

![Diagram that shows the agent factory as a six-step assembly line. Step 1 Models shows selecting an LLM. Step 2 Customizability shows fine-tuning and prompts. Step 3 Knowledge and Tools shows connecting to enterprise data and actions. Step 4 Orchestration shows coordinating agent workflows. Step 5 Observability shows logging and tracing. Step 6 Trust shows security controls. The steps flow left to right, producing a production-ready agent.](media/agent-factory.png)

:::row:::
    :::column span="1":::
### 1. Models

The assembly line starts when you select a model that gives your agent its intelligence. Choose from a growing catalog of large language models (LLMs), including GPT-4o, GPT-4, GPT-3.5 (Azure OpenAI), and others like Llama. The model is the reasoning core of the agent that informs its decisions.
    :::column-end:::
    :::column span="1":::
### 2. Customizability

Shape the model to fit your use case. Customize your agent with fine-tuning, distillation, or domain-specific prompts. Encode agent behavior, role-specific knowledge, and patterns from prior performance by using data captured from real conversation content and tool results.
    :::column-end:::
    :::column span="1":::
### 3. Knowledge and tools

Equip your agent with tools. These tools let the agent access enterprise knowledge (such as Bing, SharePoint, and Azure AI Search) and take real-world actions (via Azure Logic Apps, Azure Functions, OpenAPI, and more). This step enhances the agent's ability to expand its capabilities.
    :::column-end:::
:::row-end:::

:::row:::
    :::column span="1":::
### 4. Orchestration

:::moniker range="foundry-classic"
The agent needs coordination. [Connected agents](how-to\connected-agents.md) orchestrate the full lifecycle, such as handling tool calls, updating conversation state, managing retries, and logging outputs.

:::moniker-end
:::moniker range="foundry"
The agent needs coordination. [Workflows](../default/agents/concepts/workflow.md) orchestrate the full lifecycle, such as handling tool calls, updating conversation state, managing retries, and logging outputs.

:::moniker-end

    :::column-end:::
    :::column span="1":::
### 5. Observability

Test and monitor agents. Foundry can capture logs, traces, and evaluations at every step. With full conversation-level visibility and Application Insights integration, teams can inspect every decision and continuously improve agents over time.
    :::column-end:::
    :::column span="1":::
### 6. Trust

Ensure that agents are suitable and reliable for the workload they're assigned to. Foundry applies enterprise-grade trust features, including identity via Microsoft Entra, role-based access control (RBAC), content filters, encryption, and network isolation. You choose how and where your agents run, by using platform-managed or bring-your-own infrastructure.
    :::column-end:::
:::row-end:::

The result is an agent that's ready for production: reliable, extensible, and safe to deploy across your workflows.

## Why use Foundry Agent Service?

Agent Service provides a production-ready foundation for deploying intelligent agents in enterprise environments. Here's how it compares across key capabilities:

| Capability | Agent Service |
| --- | --- |
| **Visibility into conversations** | Full access to structured [conversations](../default/agents/concepts/runtime-components.md#what-is-a-conversation), including both user-to-agent and agent-to-agent messages. Ideal for UIs, debugging, and training. |
| **Multiple-agent coordination** | Built-in support for agent-to-agent messaging. |
| **Tool orchestration** | Server-side execution and retry of tool calls with structured logging. No manual orchestration is required. |
| **Trust and safety** | Integrated [content filters](../openai/how-to/content-filters.md) to help prevent misuse and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA). All outputs are policy governed. |
| **Enterprise integration** | Ability to bring your own [storage](./how-to/use-your-own-resources.md#use-an-existing-azure-cosmos-db-for-nosql-account-for-conversation-storage), [Azure AI Search index](./how-to/use-your-own-resources.md#use-an-existing-azure-ai-search-resource), and [virtual network](how-to\virtual-networks.md) to meet compliance needs. |
| **Observability and debugging** | [Full traceability](../how-to/develop/trace-agents-sdk.md) of conversations, tool invocations, and message traces; [Application Insights integration](./how-to/metrics.md) for usage data. |
| **Identity and policy control** | Built on Microsoft Entra with full support for RBAC, audit logs, and enterprise conditional access. |

## Security, privacy, and compliance

Agent Service is designed for enterprise workloads where you need strong controls over identity, networking, data handling, and safety.

- **Safety controls**: Use integrated [content filters](../openai/how-to/content-filters.md) to help reduce unsafe outputs and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA).
- **Network isolation and data residency controls**: Use [virtual networks](how-to\virtual-networks.md) and bring-your-own resources to meet your requirements.
- **Bring your own resources**: Use your own Azure resources (for example, storage, Azure AI Search, and Azure Cosmos DB for conversation state) to meet compliance and operational needs. See [Use your own resources](how-to/use-your-own-resources.md).
- **Responsible AI guidance**: For a broader set of recommendations and governance resources, see [Responsible AI for Microsoft Foundry](../responsible-use-of-ai-overview.md).

## Get started with Foundry Agent Service

To get started with Agent Service, create a Foundry project in your Azure subscription.

If you're building in code, see [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md) for SDK options and guidance.

:::moniker range="foundry-classic"

If it's your first time using the service, start with the [environment setup](environment-setup.md) and [quickstart](./quickstart.md) guides.

:::moniker-end

:::moniker range="foundry"

If it's your first time using the service, start with the [environment setup](environment-setup.md) and [quickstart](../default/tutorials/quickstart-create-foundry-resources.md) guides.

:::moniker-end

Create a project with the required resources. After you create a project, deploy a compatible model such as GPT-4o. When you have a deployed model, you can start making API calls to Agent Service by using the SDKs.

:::moniker range="foundry"

You can find a list of official samples with the new Python agent SDK on [GitHub](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects).

:::moniker-end

## BCDR for agents

To support service resilience, Agent Service relies on customer-provisioned Azure Cosmos DB accounts for business continuity and disaster recovery (BCDR). This approach helps ensure that your agent state can be preserved and recovered in the event of a regional outage.

As an Azure Standard customer, you provision and manage your own single-tenant Azure Cosmos DB account. You store all agent state in this account. You control backup and recovery through native capabilities in Azure Cosmos DB.

If the primary region becomes unavailable, the agent automatically connects to the same Azure Cosmos DB account in the secondary region. Because Cosmos DB preserves all history, the agent can continue operation with minimal disruption.

Provision and maintain your Azure Cosmos DB account, and configure appropriate backup and recovery policies. This effort helps ensure seamless continuity if the primary region becomes unavailable.

For configuration guidance, see [Use your own resources](how-to/use-your-own-resources.md) and [virtual networks](how-to\virtual-networks.md).

## Costs

Using Agent Service can incur costs from the model you deploy and the Azure resources you use for your project (for example, logging and any customer-managed resources you connect).

To understand and manage cost drivers, see [Plan and manage costs](../concepts/manage-costs.md).

## Troubleshooting

If you're blocked getting started, check these common issues:

- **Model isn't available in your region**: See [models that inform agents](concepts\model-region-support.md).
- **Requests are throttled or fail due to quota**: See [Quotas and limits for Agent Service](quotas-limits.md).
- **You can't access resources or deployments**: Confirm your role assignments and follow [environment setup](environment-setup.md).
- **You need to debug tool calls or agent behavior**: Start with [trace agents with the SDK](../how-to/develop/trace-agents-sdk.md) and [metrics](how-to/metrics.md).

## Related content

- [Quickstart: Create your first agent](./quickstart.md)
- [Models that inform agents](concepts/model-region-support.md)
- [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md)
- [Content filters for safety](../openai/how-to/content-filters.md)
- [Trace agents with the SDK](../how-to/develop/trace-agents-sdk.md)
- [Use your own resources](how-to/use-your-own-resources.md)
- [Quotas and limits for Agent Service](quotas-limits.md)
