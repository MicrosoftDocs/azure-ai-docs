---
title: "Hosted agents in Foundry Agent Service (preview)"
description: "Deploy and manage containerized agents on Foundry Agent Service (preview) with managed hosting, scaling, and observability."
author: aahill
ms.author: aahi
ms.date: 03/05/2026
ms.manager: nitinme
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
---

# What are hosted agents?
When you build agentic applications by using open-source frameworks, you typically manage containerization, web server setup, security integration, memory persistence, infrastructure scaling, data transmission, instrumentation, and version rollbacks. These tasks become even more challenging in heterogeneous cloud environments.

Hosted agents in Foundry Agent Service solve these challenges for Microsoft Foundry users. By using this managed platform, you can deploy and operate AI agents securely and at scale. You can use your custom agent code or a preferred agent framework with streamlined deployment and management.

### When to use hosted agents

Choose hosted agents over prompt-based agents when you need to:

- **Bring your own code** — use any framework (Agent Framework, LangGraph, Semantic Kernel, or custom code) rather than prompt-only definitions.
- **Use custom protocols** — accept webhooks or non-OpenAI payloads via the Invocations protocol.
- **Control compute resources** — specify CPU and memory for your agent’s sandbox.
- **Run stateful workloads** — persist files and state across turns via $HOME and the /files endpoint.

### How it works

You package your agent as a container image and push it to Azure Container Registry. When you deploy, Agent Service pulls the image, provisions compute, assigns a dedicated Entra agent identity, and exposes a dedicated endpoint. At runtime, your agent code handles requests from clients and can call Foundry models, Foundry Toolbox tools, and downstream Azure services using its agent identity. The platform handles scaling, session state persistence, observability, and lifecycle management.

> [!IMPORTANT]
> When you use Hosted Agents with other Microsoft products and services, you must read all relevant documentation for such products and services and understand related risks and compliance considerations. If you use Hosted Agents with any third-party servers, agents, code, or models that are not Azure Direct models (“Third-Party Systems”), you do so at your own risk. Third-Party Systems are Non-Microsoft Products under the Microsoft Product Terms and are governed by their own third-party license terms.  You are responsible for any usage and associated costs. We recommend reviewing all data being shared with and received from Third-Party Systems and being cognizant of third-party practices for handling, sharing, retention, and location of data. It is your responsibility to manage whether your data will flow outside of your organization’s Azure compliance and geographic boundaries and any related implications. Microsoft has no responsibility to you or others in relation use of Third-Party Systems, and you are responsible for implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems.

## Key concepts

### Hosted agents

Hosted agents are containerized agentic AI applications that run on Agent Service. Unlike prompt-based agents — which are defined entirely through prompts and tool configuration in the Foundry portal — hosted agents are your own code packaged as a container image. You choose the framework, control the runtime behavior, and deploy the image to Microsoft-managed infrastructure.

The platform automatically manages the container lifecycle based on activity, provisioning resources when you create a version and deprovisioning when the idle timeout is reached.

### Protocols: Responses and Invocations

Hosted agent containers expose one or both of two protocols. Each protocol is provided by a lightweight library that handles the HTTP server, health checks, and OpenTelemetry integration.

#### Which protocol should I use?

| Scenario | Protocol | Why |
|----------|----------|-----|
| Conversational chatbot or assistant | **Responses** | The platform manages conversation history, streaming events, and session lifecycle — use any OpenAI-compatible SDK as the client. |
| Multi-turn Q&A with RAG or tools | **Responses** | Built-in conversation ID threading and tool result handling. |
| Background / async processing | **Responses** | background: true with platform-managed polling and cancellation — no custom code needed. |
| Agent published to Teams or M365 | **Responses** + **Activity** | The Responses protocol powers the agent logic; the Activity protocol handles the Teams channel integration. |
| Webhook receiver (GitHub, Stripe, Jira, etc.) | **Invocations** | The external system sends its own payload format — you can't change it to match /responses. |
| Non-conversational processing (classification, extraction, batch) | **Invocations** | The input is structured data, not a chat message. Arbitrary JSON in, arbitrary JSON out. |
| Custom streaming protocol (AG-UI, etc.) | **Invocations** | AG-UI and other agent-UI protocols aren't OpenAI-compatible — you need raw SSE control. |
| Protocol bridge (GitHub Copilot, proprietary systems) | **Invocations** | The caller has its own protocol that doesn't map to /responses. |

> [!TIP]
> **Not sure?** Start with **Responses**. You can always add an Invocations endpoint later — a hosted agent can support both protocols simultaneously.

#### Protocol comparison

| | **Responses** | **Invocations** |
|---|---|---|
| **Best for** | Most agents — the platform manages conversation history, streaming lifecycle, and background execution | Agents that need full HTTP control, custom payloads, or long-running async workflows |
| **Payload** | OpenAI-compatible /responses contract | Arbitrary JSON via /invocations — you define the schema |
| **Client SDK** | Any OpenAI-compatible SDK (Python, JS, C#) works out of the box | Custom client — you define the contract |
| **Session history** | Platform-managed via conversation ID | You manage sessions (in-memory, Cosmos DB, etc.) |
| **Streaming** | Platform-managed ResponseEventStream with lifecycle events | Raw SSE — you format and write events directly |
| **Background / long-running** | Built-in (background: true + platform-managed polling) | Manual task tracking and custom polling endpoints |

#### Additional protocols

Hosted agents also support the **Activity** protocol for Teams and M365 channel integration (typically used alongside Responses) and the **A2A** protocol for agent-to-agent delegation. All four protocols — Responses, Invocations, Activity, and A2A — can be combined in a single agent.

### Agent identity and endpoint

Every hosted agent deployed to a Foundry project gets its own **dedicated Entra agent identity** and **dedicated endpoint** — both created automatically at deploy time. You don't need to configure managed identities or routing manually.

The endpoint is available immediately after deployment — publishing is not required for programmatic access:

- **Responses**: {project_endpoint}/agents/{name}/endpoint/protocols/responses
- **Invocations**: {project_endpoint}/agents/{name}/endpoint/protocols/invocations

Which endpoints are active depends on the protocols declared in the agent version definition (set in agent.yaml when using azd, or via container_protocol_versions when using the SDK).

Two identities are involved:

| Identity | Scope | Purpose |
|----------|-------|---------|
| **Agent Entra identity** (per-agent) | Created automatically at deploy time | The identity the agent container authenticates with at runtime. Used for model invocation, tool access, and downstream Azure services. |
| **Project managed identity** (project-wide) | System-assigned on the Foundry project | Used by the platform for infrastructure operations (for example, Container Registry Repository Reader on the container registry). Not the agent's runtime identity. |

When you deploy with azd, the required RBAC role (Azure AI User at account scope) is assigned to the agent's Entra identity automatically. For external resources (for example, your own Azure Storage), you assign RBAC manually to the agent's Entra identity.

### Sessions and conversations

Hosted agents use **sessions** and **conversations** to manage state. How they work depends on the protocol.

#### Sessions

A session ID identifies a logical session with persisted state — including $HOME and files uploaded via the /files endpoint. The platform provisions compute on demand and restores persisted state onto it.

- **State persistence**: $HOME and /files content are persisted across turns and across idle periods. When compute goes idle and is brought back (on new or existing infrastructure), the session's state is automatically restored.
- **Isolation**: Each session is isolated from other sessions.
- **Automatic lifecycle**: Sessions are created on first use. The platform provisions and deprovisions compute automatically.
- **Session lifetime**: Sessions persist for up to 30 days. The idle timeout is 15 minutes — if no request arrives within that window, the platform deprovisions the compute and persists the session state.
- **Session management APIs**: List sessions, terminate sessions, and upload or download files per session.

#### Conversations

A conversation ID is a durable record of conversation history (messages, tool calls, and responses) stored in Foundry.

- **Persistence**: Conversation history is stored in Foundry and persists independently of compute state.
- **Cross-channel access**: Users can access the same conversation from the playground, API, Teams, or other published channels.

#### How sessions and conversations work with each protocol

**Responses protocol**: conversation ID is the primary concept. The platform manages conversation history automatically and associates a session ID with each conversation. The platform returns the session ID to the client, which can use it to upload files via the /files endpoint — making those files available to the conversation's compute.

**Invocations protocol**: session ID is the primary concept. The client manages the session ID directly to maintain state across interactions. The client can upload content via the /files endpoint using the session ID to make it available for the session. There is no platform-managed conversation history — you manage state in your own code.

#### Session compute lifecycle

| State | What happens |
|-------|----------------------------------------------|
| **Active** | Compute is running. Requests are routed to it. $HOME and /files content are available. |
| **Idle** | No requests for 15 minutes. Compute is deprovisioned. Session state ($HOME, /files) is persisted. |
| **Resumed** | Same session ID is referenced again. Platform provisions new compute and restores persisted state. |

## Security and data handling

Treat a hosted agent like production application code.

> [!IMPORTANT]
> If you use Foundry Agent Service to host agents that interact with third-party models, servers, or agents, you do so at your own risk. We recommend reviewing all data being shared with third-party models, servers, or agents and understanding third-party practices for retention and location of data. It is your responsibility to manage whether your data will flow outside of your organization's Azure compliance and geographic boundaries and any related implications.

- **Don't put secrets in container images or environment variables**. Use managed identities and connections, and store secrets in a managed secret store. For guidance, see [Set up a Key Vault connection](../../how-to/set-up-key-vault-connection.md).
- **Be careful with non-Microsoft tools and servers**. If your agent calls tools backed by non-Microsoft services, some data might flow to those services. Review data sharing, retention, and location policies for any non-Microsoft service you connect.

## Platform details

### Versioning

Each call to create a version produces an **immutable agent version** — a snapshot of the container image, resource allocation, environment variables, and protocol configuration. Deployments reference a specific version. To update your agent, you create a new version and the platform deploys it. You can also split traffic between versions for canary or blue-green deployments.

Environment variables are the primary mechanism for passing configuration to your container at runtime (for example, the project endpoint, model deployment name, and custom settings). They are set per version and are immutable once the version is created.

### Foundry Toolbox

Hosted agents access Foundry-managed tools (Code Interpreter, Web Search, Azure AI Search, OpenAPI, custom MCP connections, A2A) through a **Toolbox MCP endpoint** provisioned in your Foundry project. Your agent code connects to this endpoint using standard MCP client libraries — the platform doesn't inject tools automatically. For details, see [Curate intent-based toolbox in Foundry](../how-to/tools/toolbox.md).

### Language support

Hosted agents support **Python** and **C#**. You can use any agent framework — the protocol libraries are framework-agnostic. For samples using Microsoft Agent Framework, LangGraph, and custom code, see the [foundry-samples repo](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents).

### Sandbox sizes

Hosted agent sandboxes support CPU and memory allocations ranging from 0.25 vCPU / 0.5 GiB to 4 vCPU / 8 GiB.

### Private networking

Hosted agents support deployment within network-isolated Foundry resources. For more information, see [Configure virtual networks](../../agents/how-to/virtual-networks.md).

## Limits, pricing, and availability (preview)

Hosted agents are currently in preview.

### Limitations during preview

| Limit | Scope | Default Value | Adjustable |
| --------- | ------ | ----- | ------- |
| Maximum active concurrent sessions | per subscription per region | 50 | Yes, with quota requests to Microsoft Support |

### Pricing

Managed hosting runtime billing is based on consumption of CPU and memory resources during active sessions. For current rates, see the Foundry [pricing page](https://azure.microsoft.com/en-us/pricing/details/foundry-agent-service/).

### Region availability

Hosted agents are currently available in the following regions: 

- East US2
- Sweden Central
- West US
- Australia East
- Germany West Central
- France Central
- Japan East
- South India
- North Central US
- Switzerland North
- West US3
- Norway East
- South East Asia
- Korea Central
- Poland Central
- Brazil South
- Canada Central
- South Africa North
- Spain Central

## Next steps

| Task | Link |
|------|------|
| Build and deploy your first hosted agent | [Quickstart: Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md) |
| Deploy using the Foundry SDK | [Deploy a hosted agent by using the Foundry SDK](../../agents/how-to/deploy-hosted-agent.md) |
| Update, delete, invoke, or stream logs | [Manage hosted agents](../../agents/how-to/manage-hosted-agent.md) |
| Set up tracing and monitoring | [Enable tracing in your project](../../observability/concepts/trace-agent-concept.md) |
| Evaluate agent performance | [Agent evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) |
| Publish to Teams, M365, or custom apps | [Publish and share agents](../how-to/publish-agent.md) |
| Browse code samples | [Python samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents) · [C# samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents) |

## Related content

- [Agent runtime components](./runtime-components.md)
- [Agent development lifecycle](./development-lifecycle.md)
- [Agent identity concepts in Microsoft Foundry](./agent-identity.md)
- [Discover tools in Foundry Tools](./tool-catalog.md)
- [Azure Container Registry documentation](/azure/container-registry/)
