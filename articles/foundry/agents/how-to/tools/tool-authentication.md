---
title: "Toolbox authentication in Microsoft Foundry"
description: "Learn how toolbox authentication in Microsoft Foundry supports per-user access through OAuth or Microsoft Entra and keeps authentication out of agent code."
author: mattwojo
ms.author: mattwoj
ms.reviewer: lindazqli
reviewer: zhuoqunli
ms.date: 07/29/2026
manager: mcleans
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus
ai-usage: ai-assisted
---

# How toolbox authentication works in Microsoft Foundry

Toolbox authentication in Microsoft Foundry determines how tools authenticate to downstream services. Authentication settings are configured on project connections, allowing agents to use anonymous access, shared credentials, service identities, or a signed-in user's identity without implementing authentication logic in agent code.

This article explains how toolbox authentication works and shows how to configure OAuth identity passthrough for a private MCP server and Work IQ while preserving each user's permissions and access boundaries.

A [toolbox](../../concepts/toolbox-overview.md) centralizes authentication on the connection. Authentication is a property of the connection, not code in your agent. When you connect a tool, you select an authentication type and Foundry handles token acquisition, exchange, refresh, and injection on the service side. Your agent code remains focused on business logic rather than authentication flows.

## Why per-user authentication is hard to build yourself

If you wire up per-user access to Entra-protected tools yourself, you take on security-critical plumbing that's easy to get subtly wrong:

1. **Implement per-user token isolation yourself.** You must partition token caches correctly by user and tenant. A wrong cache key can silently leak one user's downstream API access to another user, a bug that passes every functional test.
1. **Manage consent and lifecycle per user, per resource.** You need to detect consent failures such as `AADSTS65001`, send users through consent, refresh expired tokens, and handle 401/403 retries correctly for each API in every agent you write.
1. **Absorb complexity that scales linearly with tools and agents.** Every new tool adds another scope, token exchange, cache entry, consent path, retry path, and header path. As you scale to hundreds of tools and thousands of agents, you rebuild the same fragile plumbing again and again.

## The two identities in every tool call

The mental model to hold onto: there are always two identities in play, and everything hard about per-user authentication lives in keeping them correct, separate, and never crossed across concurrent users.

- **Agent-to-toolbox boundary (the stable one).** The agent authenticates to the platform with its own agent identity. This identity gates access to the *toolbox itself*, not the individual tools inside it.
- **Tool-to-data boundary (the per-user one).** For the actual data call, Foundry supplies the downstream service with credentials that represent the signed-in user. Depending on the authentication type, those credentials come from an OAuth authorization flow or an audience-specific Microsoft Entra access token. The downstream service returns only what the user can access and honors their permissions and sensitivity labels.

## How a toolbox handles authentication

A toolbox moves the entire authentication burden off your agent and onto the connection:

- **Auth lives on the connection, not in the agent.** You pick an auth type once, when you connect a tool. The agent code stays auth-free.
- **Foundry handles the whole flow.** Depending on what a tool needs, Foundry stores and injects API keys, obtains credentials for service identities, completes OAuth authorization, or supplies an audience-specific Microsoft Entra access token. Foundry isolates per-user credentials from other users.
- **You just build business logic.** The auth flow was never yours to build.

| The DIY burden | What a toolbox does instead |
| -------------- | --------------------------- |
| Per-user token isolation | Foundry isolates tokens per caller automatically. There's no cache key to get wrong. |
| Consent and lifecycle handling, per user and per resource | Foundry manages the consent flow and token lifecycle for each user, including acquiring and refreshing tokens after required consent is granted. |
| Auth reimplemented per tool and per team | You build a toolbox with its tools and auth once, then reuse it across every agent and runtime. |

## Set the authentication type on the connection

You choose the authentication type when you *create the connection*, in the portal, with the Azure Developer CLI, or through the REST API. Never in agent code. Each auth type determines whose identity reaches the tool:

| `authType` | Whose identity reaches the tool | Use it for |
| ---------- | ------------------------------- | ---------- |
| `none` | Anonymous | Public servers (for example, the Microsoft Learn MCP server). |
| `custom-keys` | A stored API key or header | Key-based SaaS. The agent never sees the secret. |
| `project-managed-identity` | The project's managed identity | Service-to-service calls with no user context. |
| `agentic-identity` | The agent's own identity | Per-agent audit and least privilege. |
| `oauth2` | The user who completes OAuth authorization | OAuth-compliant services, including Work IQ and partner MCP servers (for example, Vercel). |
| `user-entra-token` | The signed-in Microsoft Entra user | Managed Microsoft services that require an audience-specific Entra token, such as workspace-private Fabric data agent endpoints. |

Both `oauth2` and `user-entra-token` support per-user access, but they obtain credentials differently. With `oauth2`, the user completes an OAuth authorization flow, and Foundry stores and refreshes the resulting credentials. With `user-entra-token`, Foundry supplies the downstream service with an audience-specific Microsoft Entra access token that represents the signed-in user. Use the authentication type required by the service.

## Configure a connection for each authentication type

Register each connection with `azd ai connection create`. The command shape is always the same; the flags differ per auth type. Use `--kind remote-tool` for MCP and A2A servers.

# [No auth](#tab/none)

```azurecli
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://public-mcp.example.com/mcp \
  --auth-type none
```

# [Custom keys](#tab/custom-keys)

```azurecli
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://saas.example.com/mcp \
  --auth-type custom-keys \
  --custom-key "Authorization=Bearer <token>"
```

The `--custom-key "Header=Value"` flag is repeatable when a service needs more than one header.

# [OAuth identity passthrough](#tab/oauth2)

```azurecli
azd ai connection create orders-mcp \
  --kind remote-tool \
  --target https://orders-mcp.example.com/mcp \
  --auth-type oauth2 \
  --authorization-url https://auth.example.com/authorize \
  --token-url https://auth.example.com/token \
  --client-id <oauth-client-id> \
  --client-secret <oauth-client-secret> \
  --scopes "<scope1> <scope2>"
```

Include `offline_access` in `--scopes` to enable automatic token refresh.

# [User Entra token](#tab/user-entra-token)

```azurecli
azd ai connection create my-fabric-conn \
  --kind remote-tool \
  --target https://fabric-mcp.example.com/mcp \
  --auth-type user-entra-token \
  --audience https://analysis.windows.net/powerbi/api
```

# [Project managed identity](#tab/project-managed-identity)

```azurecli
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://service-mcp.example.com/mcp \
  --auth-type project-managed-identity \
  --audience https://cognitiveservices.azure.com
```

Assign the project's system-assigned managed identity the required RBAC role on the target resource.

# [Agentic identity](#tab/agentic-identity)

```azurecli
azd ai connection create my-mcp-conn \
  --kind remote-tool \
  --target https://service-mcp.example.com/mcp \
  --auth-type agentic-identity \
  --audience https://cognitiveservices.azure.com
```

The system intentionally rejects a user token. Assign the agent identity access on the target resource.

---

## Walkthrough: OAuth identity passthrough

This example connects two Microsoft Entra-protected tools for per-user access: a private orders MCP server and Work IQ. Both use OAuth identity passthrough, so each downstream call runs as the user who authorizes the connection.

### 1. Create a connection for each tool

```azurecli
# Private orders MCP: OAuth identity passthrough
azd ai connection create orders-mcp \
  --kind remote-tool \
  --target https://orders-mcp.example.com/mcp \
  --auth-type oauth2 \
  --authorization-url https://auth.example.com/authorize \
  --token-url https://auth.example.com/token \
  --client-id <oauth-client-id> \
  --client-secret <oauth-client-secret> \
  --scopes "openid offline_access orders.read"

# Work IQ: OAuth identity passthrough
azd ai connection create workiq-conn \
  --kind remote-a2a \
  --target https://workiq.svc.cloud.microsoft/a2a/ \
  --auth-type oauth2 \
  --authorization-url https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/authorize \
  --token-url https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token \
  --client-id <oauth-client-id> \
  --client-secret <oauth-client-secret> \
  --scopes "api://workiq.svc.cloud.microsoft/WorkIQAgent.Ask offline_access"
```

### 2. Add both tools to a toolbox

Each tool references its connection by ID. That single reference is the entire difference between running as a shared service account and acting on behalf of the signed-in user. Your agent doesn't need a token broker or per-user token cache.

This example requires `azure-ai-projects` version 2.3.0 or later.

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPToolboxTool, WorkIQPreviewToolboxTool

endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"
project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())
orders_connection = project.connections.get("orders-mcp")
workiq_connection = project.connections.get("workiq-conn")

toolbox_version = project.toolboxes.create_version(
    name="employee-toolbox",
    description="Private orders MCP + Work IQ, both via OAuth identity passthrough.",
    tools=[
        MCPToolboxTool(
            server_label="orders",
            server_url="https://orders-mcp.example.com/mcp",
            require_approval="never",
            project_connection_id=orders_connection.id,
        ),
        WorkIQPreviewToolboxTool(project_connection_id=workiq_connection.id),
    ],
)
print(f"Created toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

### 3. Connect the agent to the toolbox

The agent connects to the toolbox's single consumer endpoint, which always serves the default version. The agent authenticates to the platform with its own identity. For each tool, Foundry supplies credentials that represent the user who completed OAuth authorization. The agent carries no per-tool authentication code.

```python
import httpx
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from agent_framework import MCPStreamableHTTPTool

# Agent-to-toolbox identity: the agent's own credential, scoped to the platform
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
http_client = httpx.AsyncClient(auth=_ToolboxAuth(token_provider), timeout=120.0)

# Consumer endpoint always resolves to the toolbox's default version
CONSUMER_URL = f"{endpoint}/toolboxes/employee-toolbox/mcp?api-version=v1"

toolbox = MCPStreamableHTTPTool(
    name="employee_toolbox",
    url=CONSUMER_URL,
    http_client=http_client,
    load_prompts=False,
)

agent = chat_client.as_agent(
    name="employee-agent",
    instructions="Help employees with their orders and Microsoft 365 context.",
    tools=[toolbox],
)
```

Foundry generates a consent link the first time a particular user needs to authorize a tool. After they consent, subsequent calls use that user's credentials. The user might need to authorize the tool again if the refresh token expires or is revoked.

> [!NOTE]
> Consumers of an agent that uses OAuth identity passthrough need at least the **Foundry Agent Consumer** role on the project. The user's Microsoft Entra tenant must match the tenant of your Foundry project; cross-tenant token exchange isn't supported.

## Beyond passthrough: what else a toolbox gives you

Because authentication and tool traffic flow through the toolbox, you get more than clean identity handling:

- **Responsible AI guardrails.** Guardrails screen every tool's inputs and outputs, so an untrusted MCP response can't smuggle prompt-injection or unsafe content back into the agent.
- **Bring-your-own AI gateway.** Front your MCP servers with Azure API Management (APIM) for rate limiting, logging, and network policy.
- **Versioning.** Create and test a new toolbox version, then promote it to default. Every agent that points to the consumer endpoint picks up the promoted version automatically, with no code changes.

## Related content

- [What is Toolbox in Foundry?](../../concepts/toolbox-overview.md)
- [Create and manage a toolbox in Foundry](toolbox.md)
- [Model Context Protocol (MCP) tools](model-context-protocol.md)
- [Work IQ](work-iq.md)
- [Set up MCP server authentication](../mcp-authentication.md)
