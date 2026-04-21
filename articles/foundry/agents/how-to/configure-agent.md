---
title: "Configure and share your agent"
description: "Learn how to configure your agent's stable endpoint, select the active version, and share your agent with consumers in Microsoft Foundry."
#customer intent: As a developer, I want to configure my agent's stable endpoint in Microsoft Foundry so that consumers can invoke it.
author: sdgilley
ms.author: sgilley
ms.reviewer: fosteramanda
ms.date: 04/14/2026
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
ms.custom: pilot-ai-workflow-jan-2026, doc-kit-assisted
---

# Configure and share your agent 

Every agent in Microsoft Foundry has a stable endpoint from the moment it's created. When end users interact with your agent through Microsoft 365 Copilot, Teams, your existing application, or other surfaces, they interact with the agent's stable endpoint. Before you share your agent, verify these settings:
- **Active agent version** — Confirm the version that receives traffic is the one you want end users to interact with. By default, the agent auto-updates to the latest version, which means a newly created version is immediately served. If that isn't what you want, pin traffic to a specific version.
- **Protocols and authorization schemes** — Make sure they match where and how your users interact with the agent. For example, an agent published to Microsoft 365 or Teams must have the Activity protocol enabled and use a BotService or BotServiceRbac authorization scheme.

This article shows you how to select the active version, enable protocols, set authorization schemes, and add an agent card. Once your endpoint is configured, you can
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Publish an agent as a digital worker in Agent 365](./agent-365.md)

> [!NOTE]
> If you're migrating from the previous publishing model, see [Migrate from Agent Applications to the new agent model](./migrate-agent-applications.md).


## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with at least one agent version created
- [Azure AI User role](../../concepts/rbac-foundry.md) on the Foundry project scope to create, manage, and invoke agents
- Familiarity with [Azure role-based access control (RBAC)](/azure/role-based-access-control/overview) for permission configuration
- Familiarity with [Agent identity concepts in Foundry](../concepts/agent-identity.md)
- Install the required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md)

[!INCLUDE [code-preview](../../includes/code-preview.md)]

## Understand the agent object model

Before working with your agent's endpoint, understand the relationship between projects, agents, agent versions, and the stable endpoint.

:::image type="content" source="../media/agent-object-model.png" alt-text="Diagram illustrating how Foundry projects organize agent versions and agents.":::

**Foundry project**: A Foundry project is a folder that groups related resources such as agents, files, and tools.

**Agent version**: is an immutable snapshot of the agent's configuration. Any change (even a single prompt edit) produces a new version.

**Agent**: The stable, consumer-facing representation of an agent. An agent's "self" is defined by its evolving context, capabilities, and behavior—not by a fixed implementation snapshot. The agent anchors that evolution to a consistent identity, endpoint, and authorization surface, so consumers always interact with the same entity even as the underlying agent versions change.

**Agent endpoint**: The URL consumers call to invoke the agent. It's live the moment you create the agent—there's no separate publish step—and the URL doesn't change as you roll out new versions. You configure which version it serves, which protocols it speaks, and how callers authenticate.

For a full list of agent object properties, see the [reference section](#reference-agent-object-properties) at the bottom of this article.


### Traffic routing

The agent's `version_selector` determines how traffic is routed to agent versions. Two routing policies are available:

- **Always use latest** (default) — 100% of traffic routes to the most recently created agent version. When the agent is published to Teams or Microsoft 365, creating a new version automatically updates what's served in those channels.
- **Pinned to a specific version** — 100% of traffic routes to the agent version you select, referred to as the "active agent version." New versions don't change what's served until you update the selector.

Pin to a specific version when you need stability across new version creation — for example, when an agent is in production or published to end users in Teams or Microsoft 365.

### Protocols

An agent can expose multiple protocols simultaneously:

| Protocol | Endpoint pattern |
|----------|-----------------|
| **Responses** | `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/protocols/openai/v1/responses` |
| **Activity Protocol** | `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/protocols/activityprotocol` |
| **Invocations** | `https://{account}.services.ai.azure.com/api/projects/{project}/agents/{agent}/protocols/invocations` |

### Authorization schemes

You can configure inbound authentication on the agent endpoint:

| Scheme type | Description | Isolation key source |
|-------------|-------------|----------------------|
| **`Entra`** | Microsoft Entra ID authorization. The caller must have the **Azure AI User** on the Foundry project. | `Entra` — derives user identity from the Entra token. `Header` — reads isolation keys from custom headers (`user_isolation_key`, `chat_isolation_key`). |
| **`BotService`** | Azure Bot Service channel authorization. Used when publishing to M365/Teams. Configured automatically during the channel publish flow. | N/A |
| **`BotServiceRbac`** | Azure Bot Service authorization combined with Azure RBAC. Use when you need Bot Service channel auth with additional RBAC enforcement. | N/A |

API key authentication isn't supported. Use Microsoft Entra ID (Azure RBAC) to authorize callers.

## Configure the agent properties

If not explicitly set, by default the version sector routes 100% of traffic to the latest agent version, responses protocol is enable, and authorization is set as Entra. You can reconfigure the version routing, enable protocols, set authorization schemes, and add an agent card.

> [!TIP]
> Each section below shows how to update one setting at a time so the examples are easy to follow. When you use the REST API or SDK, you can update several settings at once in a single request — only the fields you include change, and everything else stays the same.

### Select the active agent version

By default, the routing policy is **Always use latest**. To pin traffic to a specific version, update the `version_selector`.

#### [Foundry portal](#tab/portal)

1. In the Foundry portal, create an agent or open an existing agent.
1. Expand the **Publish** dropdown to see endpoint configuration options.

   **Expected result**: You see the available endpoints for your agent and the current version routing configuration. The endpoints are live from agent creation — no publish step is required to activate them.

1. Click the version selector arrow and choose a specific version.

   **Expected result**: The stable endpoint now routes 100% of traffic to the selected version. When pinned, creating new versions doesn't change what's served.

#### [REST API](#tab/rest)

```
PATCH {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/merge-patch+json
Foundry-Features: AgentEndpoints=V1Preview

{
  "agent_endpoint": {
    "version_selector": {
      "version_selection_rules": [
        {
          "type": "FixedRatio",
          "agent_version": "2",
          "traffic_percentage": 100
        }
      ]
    }
  }
}
```

#### [Python SDK](#tab/python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpoint, VersionSelector, VersionSelectionRule
)
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = "https://{account}.services.ai.azure.com/api/projects/{project}"

agent_name = "name-of-your-existing-agent"

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

with project_client:
    endpoint_config = AgentEndpoint(
        version_selector=VersionSelector(
            version_selection_rules=[
                FixedRatioVersionSelectionRule(agent_version="2", traffic_percentage=100),
            ]
        ),
    )

    patched_agent = project_client.beta.agents.patch_agent_details(
        agent_name=agent_name,
        agent_endpoint=endpoint_config,
    )
    print(f"Agent endpoint configured for agent: {patched_agent.name}")
```

---

### Enable protocols and authorization schemes

An agent can expose multiple protocols simultaneously. Configure protocols and inbound authorization on the agent endpoint.

#### [Foundry portal](#tab/portal)

Updating protocols and authorization schemes isn't yet configurable in the Foundry portal. Use the REST API or Python SDK.

#### [REST API](#tab/rest)

```
PATCH {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/merge-patch+json
Foundry-Features: AgentEndpoints=V1Preview

{
  "agent_endpoint": {
    "protocols": ["activity", "responses", "invocations"],
    "authorization_schemes": [
      {
        "type": "Entra",
        "isolation_key_source": {
          "kind": "Entra"
        }
      },
      {
        "type": "BotServiceRbac"
      }
    ]
  }
}
```

#### [Python SDK](#tab/python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentEndpoint,
    AgentEndpointProtocol,
    EntraAuthorizationScheme,
    BotServiceRbacAuthorizationScheme,
    EntraIsolationKeySource,
)
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = "https://{account}.services.ai.azure.com/api/projects/{project}"

agent_name = "name-of-your-existing-agent"

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

with project_client:
    endpoint_config = AgentEndpoint(
        protocols=[
            AgentEndpointProtocol.RESPONSES,
            AgentEndpointProtocol.ACTIVITY,
            AgentEndpointProtocol.INVOCATIONS,
        ],
        authorization_schemes=[
            EntraAuthorizationScheme(
                isolation_key_source=EntraIsolationKeySource(),
            ),
            BotServiceRbacAuthorizationScheme(),
        ],
    )

    patched_agent = project_client.beta.agents.patch_agent_details(
        agent_name=agent_name,
        agent_endpoint=endpoint_config,
    )
    print(f"Protocols and authorization updated for agent: {patched_agent.name}")
```

---

### Add an agent card

An agent card surfaces details and capabilities to consumers, including for agent-to-agent (A2A) discovery.

#### [Foundry portal](#tab/portal)

Adding an agent card isn't yet configurable in the Foundry portal. Use the REST API or SDK.

#### [REST API](#tab/rest)

```
PATCH {{endpoint}}/agents/{{agent_name}}?api-version=v1
Authorization: Bearer {{token}}
Content-Type: application/merge-patch+json
Foundry-Features: AgentEndpoints=V1Preview

{
  "agent_card": {
    "version": "1.0.0",
    "description": "A competitive intelligence analyst that monitors market trends and competitor activity.",
    "skills": [
      {
        "id": "competitor-analysis",
        "name": "Competitor Analysis",
        "description": "Analyzes competitor products, pricing strategies, and market positioning across specified industry verticals.",
        "tags": ["research", "analysis", "market-intel"],
        "examples": [
          "Compare our Q3 pricing against Contoso's latest catalog",
          "Summarize recent product launches from our top 5 competitors",
          "Identify gaps in competitor coverage for the EMEA region"
        ]
      },
      {
        "id": "trend-monitoring",
        "name": "Trend Monitoring",
        "description": "Tracks emerging market trends and surfaces early signals from earnings calls, filings, and news.",
        "tags": ["trends", "monitoring"],
        "examples": [
          "What themes are emerging from this quarter's earnings calls?",
          "Flag any regulatory changes affecting our sector in the last 30 days"
        ]
      }
    ]
  }
}
```

#### [Python SDK](#tab/python)

```python
# Agent card update via SDK is not yet supported. Use the REST API.
```

---

## Get your agent properties

To view the current properties of your agent including identity, protocols, authorization, and endpoint configuration:

```
GET {endpoint}/agents/{agent_name}?api-version=2025-11-15-preview
Authorization: Bearer {{token}}
Content-Type: application/json
Foundry-Features: AgentEndpoints=V1Preview
```


## Security and privacy considerations

- Use least privilege. Grant users the minimum role they need (for example, create custom roles that separate agent creation permissions from agent invoke permissions).
- Don’t embed access tokens in source code, scripts, or client applications. Use Microsoft Entra authentication flows appropriate for your app.

## Limitations

| Limitation | Description |
| --- | --- |
| No traffic routing supported | Currently, only one agent version can be active and receiving traffic |

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| `403 Forbidden` when invoking the endpoint | Caller lacks the required role on the agent | Assign the **Azure AI User** role on the Foundry project resource. |
| `401 Unauthorized` when invoking the endpoint | The access token is missing, expired, or for the wrong resource | Reauthenticate and request a token for `https://ai.azure.com`. |
| Tool calls fail | The agent identity doesn't have access to downstream resources | Assign the required RBAC roles to the agent's identity for any Azure resources it accesses. |
| Publishing to M365/Teams fails | The agent doesn't have a unique identity (`agent.identity` is null) | See the [migration guide](./migrate-agent-applications.md) for steps to resolve this. |

## Reference: Agent object properties

<details>
<summary>Agent properties</summary>

| Property | Type | Description | Mutable? | Configurable in portal |
| --- | --- | --- | --- | --- |
| `object` | string | Always `"agent"` | No | No |
| `id` | string | Unique identifier | No | No |
| `name` | string (max 63 chars) | Name of the agent | No | No |
| `versions` | object | Contains `latest` with the latest `AgentVersion` | Yes (via create_version) | Yes |
| `agent_endpoint` | AgentEndpoint | Endpoint configuration (version selector, protocols, authorization). See the AgentEndpoint table below. | Yes (`PATCH /agents/{name}`) | Partial (version selector only) |
| `instance_identity` | object | The agent's unique Microsoft Entra identity (`principal_id`, `client_id`) | No (read-only) | No |
| `blueprint` / `blueprint_reference` | object | Reference to the agent's Microsoft Entra agent blueprint (`principal_id`, `client_id`, or `type`, `blueprint_id`) | No (read-only) | No |
| `agent_card` | AgentCard | Agent details for consumers and A2A | Yes (`PATCH /agents/{name}`) | No (REST API / SDK only) |
| `status` | enum (`Enabled`, `Disabled`) | Whether the agent is serving traffic | Not yet supported | No |

> [!NOTE]
> The `version_selector`, `protocols`, and `authorization_schemes` are nested under `agent_endpoint`. To update any of them, use `PATCH /agents/{agent_name}` with the changes inside the `agent_endpoint` property bag.

</details>

<details>
<summary>AgentEndpoint properties</summary>

| Property | Type | Description |
| --- | --- | --- |
| `version_selector` | VersionSelector | How traffic is routed to agent versions |
| `protocols` | array of string | Protocols enabled (for example, `responses`, `activity`, `a2a`) |
| `authorization_schemes` | array of objects | Authorization schemes (for example, `Entra`, `BotServiceRbac`) |

</details>

## Related content

- Learn about [Agent identity concepts in Foundry](../concepts/agent-identity.md)
- Learn about [Hosted agents](../concepts/hosted-agents.md)
- [Publish agents to Microsoft 365 Copilot and Microsoft Teams](./publish-copilot.md)
- [Migrate from Agent Applications to the new agent model](./migrate-agent-applications.md)

