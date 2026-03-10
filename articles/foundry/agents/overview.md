---
title: "What is Foundry Agent Service?"
description: "Learn about Foundry Agent Service capabilities, agent types, tools, and runtime features for building AI agents in Microsoft Foundry."
manager: nitinme
author: aahill
ms.author: aahi
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: overview
ms.date: 03/10/2026
ms.custom: azure-ai-agents, pilot-ai-workflow-jan-2026, classic-and-new, doc-kit-assisted
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

Foundry Agent Service is the runtime and orchestration layer for AI agents in Microsoft Foundry. Define an agent's model, instructions, and tools — Agent Service manages conversations, executes tool calls, applies safety controls, and integrates with identity, networking, and observability systems.

## Core AI agent components

Every agent in Agent Service combines three components:

- **Model (LLM)**: Provides reasoning and language capabilities.
- **Instructions**: Define goals, constraints, and behavior. Instructions can be prompt-based, workflow definitions, or hosted agent code.
- **Tools**: Provide access to data or actions, such as search, file operations, or API calls.

![Diagram showing the three core components of an AI agent: input flows into an Agent box containing a Model, Instructions, and Tools, which produces output. Bidirectional arrows connect the agent to external tool services for data retrieval and actions.](./media/what-is-an-agent.png)

## Agent execution stages

Agent Service organizes agent development into six stages:

![Diagram showing the six runtime stages of agent development arranged horizontally: 1) Model selection with icons for GPT-4 and Llama, 2) Customization showing fine-tuning and prompts, 3) Tools displaying data retrieval and actions, 4) Orchestration with workflow connections, 5) Observability with tracing and monitoring icons, and 6) Trust showing identity, content filters, and encryption controls.](./media/agent-factory.png)

1. **Models** — Select a model (GPT-4.1, GPT-4, Llama) that provides reasoning and language capabilities for your agent.
2. **Customizability** — Configure the model with fine-tuning, distillation, or domain-specific prompts.
3. **Knowledge and tools** — Connect tools for data retrieval (Bing, SharePoint, Azure AI Search) and external actions (Azure Functions, OpenAPI).
4. **Orchestration** — Use [workflows](concepts/workflow.md) to coordinate tool calls, conversation state, retries, and multi-agent processes.
5. **Observability** — [Trace agent decisions](../observability/how-to/trace-agent-setup.md) and monitor with [Application Insights](how-to/metrics.md) to inspect every tool call, model response, and execution flow.
6. **Trust** — Apply identity controls through Microsoft Entra, role-based access control (RBAC), content filters, encryption, and network isolation.

For details on each stage, see [Agent development lifecycle](concepts/development-lifecycle.md).

## Agent types

Agent Service supports three approaches to building agents. Each type provides different capabilities depending on the level of control and complexity your scenario requires.

### Prompt-based agents

A prompt-based agent combines model configuration, instructions, tools, and natural language prompts to drive behavior. Create prompt-based agents with the Python, C#, JavaScript/TypeScript, or Java SDKs, the REST API, or the Foundry portal.

Prompt-based agents support:

- Tool calling (file search, code interpreter, web search, MCP, and more)
- Integrated content filters and safety controls
- Conversation management with state persistence
- Versioning, evaluation, and publishing from the Foundry portal
- Tracing and observability

Use prompt-based agents for single-agent scenarios, quick prototyping, and production agents that don't require custom runtime code. For details, see [Agent development lifecycle](concepts/development-lifecycle.md).

### Workflow agents

Workflows orchestrate a sequence of actions or coordinate multiple agents using a visual builder, YAML, or Visual Studio Code. Workflows support branching logic, human-in-the-loop steps, and variable handling without requiring custom code.

Workflow agents support:

- Sequential and group-chat orchestration patterns
- Human-in-the-loop approval and clarification steps
- Conditional branching with if/else and loop nodes
- Variable handling and data transformation with Power Fx
- Agent-to-agent coordination across specialized agents

Use workflows when your scenario requires conditional logic, approvals, or multi-agent coordination. For details, see [Build a workflow in Microsoft Foundry](concepts/workflow.md).

### Hosted agents (preview)

Hosted agents are containerized agents that you build in code using supported frameworks (LangGraph, Semantic Kernel, AutoGen) or custom code. Agent Service deploys and manages these agents on pay-as-you-go infrastructure. Create hosted agents with the Python, C#, JavaScript/TypeScript, or Java SDKs.

Hosted agents support:

- Bring-your-own agent framework or custom code
- Container image deployment with managed scaling
- Publishing to channels (Teams, web, custom endpoints)
- Full SDK access to tools, identity, and observability

Use hosted agents when you need to bring existing framework code or require full control over the agent runtime environment. For details, see [What are hosted agents?](concepts/hosted-agents.md).

### Comparison

| Agent type | Supported languages | Tool calling | Orchestration | Custom code | Portal support |
| ---------- | ------------------- | ------------ | ------------- | ----------- | -------------- |
| **Prompt-based** | Python, C#, JS/TS, Java, REST | Yes | Single agent | No | Full |
| **Workflow** | Portal, YAML, VS Code | Yes | Multi-agent | Optional | Full |
| **Hosted (preview)** | Python, C#, JS/TS, Java | Yes | Framework-dependent | Yes | Limited |

## Create your first prompt-based agent

The following code samples create a prompt-based agent, start a conversation, and get a response. If this is your first time using Microsoft Foundry, see the [quickstart](../tutorials/quickstart-create-foundry-resources.md) to set up your project.

### Prerequisites

- A [Microsoft Foundry project](../tutorials/quickstart-create-foundry-resources.md) with a deployed model
    - Agent Service is available in [supported regions](./concepts/limits-quotas-regions.md). Verify your project is in a supported region before proceeding.
- The **Azure AI User** or **Azure AI Developer** [RBAC role](../concepts/rbac-foundry.md) on the project

# [Python](#tab/python)

> [!NOTE]
> Install the package: `pip install azure-ai-projects>=2.0.0b1`
>
> Package: [`azure-ai-projects`](https://pypi.org/project/azure-ai-projects/) | Python 3.8+

### Create agent

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/create-agent/quickstart-create-agent.py":::

### Chat with agent

:::code language="python" source="~/foundry-samples-main/samples/python/quickstart/chat-with-agent/quickstart-chat-with-agent.py":::

Set these environment variables before running the samples:

| Variable | Description | Where to find it |
| -------- | ----------- | ---------------- |
| `PROJECT_ENDPOINT` | Your Foundry project endpoint | Overview page in the Foundry portal |
| `MODEL_DEPLOYMENT_NAME` | Your model deployment name | **Models + endpoints** tab in your project |
| `AGENT_NAME` | The name for your new agent | You can use a name of your choice, for example `MyAgent`. |

For more samples, see [Azure SDK for Python agent samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/agents).

# [C#](#tab/csharp)

> [!NOTE]
> Install the package: `dotnet add package Azure.AI.Projects --version 2.0.0-beta.1` or use your IDE's package manager.
>
> Package: [`Azure.AI.Projects`](https://www.nuget.org/packages/Azure.AI.Projects) | .NET 8.0+

### Create agent

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/create-agent/quickstart-create-agent.cs":::

### Chat with agent

:::code language="csharp" source="~/foundry-samples-main/samples/csharp/quickstart/chat-with-agent/quickstart-chat-with-agent.cs":::

Set these environment variables before running the samples:

| Variable | Description | Where to find it |
| -------- | ----------- | ---------------- |
| `PROJECT_ENDPOINT` | Your Foundry project endpoint | Overview page in the Foundry portal |
| `MODEL_DEPLOYMENT_NAME` | Your model deployment name | **Models + endpoints** tab in your project |
| `AGENT_NAME` | The name for your new agent | You can use a name of your choice, for example `MyAgent`. |

For more samples, see [Azure SDK for .NET agent samples](https://github.com/Azure/azure-sdk-for-net/tree/main/sdk/ai/Azure.AI.Projects/samples).

# [JavaScript/TypeScript](#tab/javascript)

> [!NOTE]
> Install the package: `npm install @azure/ai-projects@2.0.0-beta.1`
>
> Package: [`@azure/ai-projects`](https://www.npmjs.com/package/@azure/ai-projects) | Node.js 20+

### Create agent

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/create-agent/src/quickstart-create-agent.ts":::

### Chat with agent

:::code language="typescript" source="~/foundry-samples-main/samples/typescript/quickstart/chat-with-agent/src/quickstart-chat-with-agent.ts":::

Set these environment variables before running the samples:

| Variable | Description | Where to find it |
| -------- | ----------- | ---------------- |
| `PROJECT_ENDPOINT` | Your Foundry project endpoint | Overview page in the Foundry portal |
| `MODEL_DEPLOYMENT_NAME` | Your model deployment name | **Models + endpoints** tab in your project |

For more samples, see [Azure SDK for JavaScript agent samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/ai/ai-projects/samples).

# [Java](#tab/java)

> [!NOTE]
> Add the prerelease dependency to your `pom.xml`:
> ```xml
> <dependency>
>     <groupId>com.azure</groupId>
>     <artifactId>azure-ai-agents</artifactId>
>     <version>2.0.0-beta.2</version>
> </dependency>
> ```
>
> Package: [`com.azure:azure-ai-agents`](https://central.sonatype.com/artifact/com.azure/azure-ai-agents) | Java 17+

### Create agent

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/create-agent/src/main/java/com/azure/ai/agents/CreateAgent.java":::

### Chat with agent

:::code language="java" source="~/foundry-samples-main/samples/java/quickstart/chat-with-agent/src/main/java/com/azure/ai/agents/ChatWithAgent.java" :::

Set these environment variables before running the samples:

| Variable | Description | Where to find it |
| -------- | ----------- | ---------------- |
| `PROJECT_ENDPOINT` | Your Foundry project endpoint | Overview page in the Foundry portal |
| `MODEL_DEPLOYMENT_NAME` | Your model deployment name | **Models + endpoints** tab in your project |
| `AGENT_NAME` | The name for your new agent | You can use a name of your choice, for example `MyAgent`. |

For more samples, see [Azure SDK for Java agent samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples).


# [REST API](#tab/rest)

### Create agent

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-create-agent.sh":::

### Chat with agent

Replace `YOUR-FOUNDRY-RESOURCE-NAME` with your values:

:::code language="console" source="~/foundry-samples-main/samples/REST/quickstart/quickstart-chat-with-agent.sh":::

Set these environment variables before running the samples:

| Variable | Description | Where to find it |
| -------- | ----------- | ---------------- |
| `PROJECT_ENDPOINT` | Your Foundry project endpoint | Overview page in the Foundry portal |
| `MODEL_DEPLOYMENT_NAME` | Your model deployment name | **Models + endpoints** tab in your project |
| `AGENT_NAME` | The name for your new agent | You can use a name of your choice, for example `MyAgent`. |

---

## Available tools

Agent Service provides tools organized into several categories:

**Search and retrieval**
- [Azure AI Search](how-to/tools/ai-search.md) — Query your vector indexes
- [File search](how-to/tools/file-search.md) — Upload and search documents
- [Foundry IQ](concepts/what-is-foundry-iq.md) — Enterprise knowledge bases
- [Web search](how-to/tools/web-search.md) and [Bing grounding](how-to/tools/bing-tools.md)

**Code execution and automation**
- [Code Interpreter](how-to/tools/code-interpreter.md) — Run Python code
- [Browser automation](how-to/tools/browser-automation.md) — Automate web interactions
- [Computer Use](how-to/tools/computer-use.md) — Control desktop applications

**Enterprise integration**
- [SharePoint](how-to/tools/sharepoint.md) — Access SharePoint content
- [Fabric data agent](how-to/tools/fabric.md) — Query Microsoft Fabric
- [OpenAPI tool](how-to/tools/openapi.md) — Call any REST API

**Advanced protocols**
- [Model Context Protocol (MCP)](how-to/tools/model-context-protocol.md) — Connect to MCP servers
- [Agent-to-Agent (A2A)](how-to/tools/agent-to-agent.md) — Multi-agent communication
- [Function calling](how-to/tools/function-calling.md) — Custom functions

For the full catalog, see the [tool catalog](concepts/tool-catalog.md). For guidance on using tools, see [Tool best practices](concepts/tool-best-practice.md).

## Runtime capabilities

Agent Service provides the following runtime features across all agent types:

| Capability | Description |
| ---------- | ----------- |
| **Conversation visibility** | Full access to structured [conversations](concepts/runtime-components.md#what-is-a-conversation), including user-to-agent and agent-to-agent messages. Useful for UI integration, debugging, and training. |
| **Multi-agent coordination** | Built-in support for agent-to-agent messaging and workflow orchestration. |
| **Tool orchestration** | Server-side execution and retry of tool calls with structured logging. No manual orchestration required. |
| **Observability and debugging** | [Traceability](../observability/how-to/trace-agent-setup.md) of conversations, tool invocations, and message traces; [Application Insights integration](how-to/metrics.md) for usage data. |
| **Identity and policy control** | Built on Microsoft Entra with support for RBAC, audit logs, and enterprise conditional access. |

For details on conversations and responses, see [Agent runtime components](concepts/runtime-components.md).

## Choose your development path

Build agents using the portal, an SDK, or the REST API:

| Approach | Languages | Best for | Advantages |
| -------- | --------- | -------- | ---------- |
| **Portal** | N/A (visual) | Prototyping, no-code users, testing | Immediate feedback, no setup required |
| **SDK** | [Python](https://pypi.org/project/azure-ai-projects/), [C#](https://www.nuget.org/packages/Azure.AI.Projects), [JavaScript/TypeScript](https://www.npmjs.com/package/@azure/ai-projects), [Java](https://central.sonatype.com/artifact/com.azure/azure-ai-agents) | Production apps, CI/CD | Programmatic control, version control, automation |
| **REST API** | Any HTTP client | Custom integrations | Language-agnostic, direct HTTP access |

For SDK details, see [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md).

> [!TIP]
> Agent Service usage is billed based on model tokens consumed and tool executions. For production planning, see [Azure AI Foundry pricing](https://azure.microsoft.com/pricing/details/microsoft-foundry/).

## Security, privacy, and compliance

Agent Service provides controls for identity, networking, data handling, and safety:

- **Safety controls**: Integrated [content filters](../../foundry-classic/openai/how-to/content-filters.md) help reduce unsafe outputs and mitigate prompt injection risks, including cross-prompt injection attacks (XPIA).
- **Tool governance**: Control which tools agents can use and enforce enterprise policies. See [Tool governance](how-to/tools/governance.md).
- **Network isolation and data residency**: Use [virtual networks](how-to/virtual-networks.md) and bring-your-own resources to meet your requirements.
- **Bring your own resources**: Use your own Azure resources (for example, storage, Azure AI Search, and Azure Cosmos DB for conversation state) to meet compliance and operational needs. See [Use your own resources](how-to/use-your-own-resources.md).
- **Responsible AI guidance**: For recommendations and governance resources, see [Responsible AI for Microsoft Foundry](../responsible-use-of-ai-overview.md).

## Related content

- [Models that support agents](./concepts/limits-quotas-regions.md)
- [Agent development lifecycle](concepts/development-lifecycle.md)
- [Agent runtime components](concepts/runtime-components.md)
- [Tool catalog](concepts/tool-catalog.md)
- [Agent memory concepts](concepts/what-is-memory.md)
- [Agent identity and authentication](concepts/agent-identity.md)
- [Microsoft Foundry SDKs](../how-to/develop/sdk-overview.md)
- [Build agent workflows in VS Code](how-to/vs-code-agents-workflow-low-code.md)
- [Migrate from Azure OpenAI Assistants](how-to/migrate.md)
- [Business continuity and disaster recovery](../how-to/high-availability-resiliency.md)
- [Azure AI services support options](/azure/ai-services/cognitive-services-support-options)