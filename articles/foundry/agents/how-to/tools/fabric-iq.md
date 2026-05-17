---
title: "Connect agents to Microsoft Fabric with Fabric IQ (preview)"
description: "Learn how to connect your Microsoft Foundry agent to Fabric IQ, a Microsoft Fabric workload that unifies business data through an enterprise ontology and AI agents so your agents can reason over your data in shared semantic context."
services: cognitive-services
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 05/10/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
 - dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-fabric-iq
---

# Connect agents to Microsoft Fabric with Fabric IQ (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!WARNING]
> When you connect to non-Foundry tools, you might incur costs and data might be sent outside Foundry's compliance boundary and processed according to the applicable terms and data handling policies. See [Admin management](#admin-management) to learn how to manage access to the tool.

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

[Fabric IQ (preview)](/fabric/iq/overview) is a Microsoft Fabric workload that unifies data across OneLake and organizes it according to the language of your business. It exposes that data to analytics, AI agents, and applications with consistent semantic meaning through its core items: the [ontology (preview)](/fabric/iq/ontology/overview), which defines your enterprise vocabulary as entity types (such as Customer, Order, and Product), their properties, relationships, and data bindings to OneLake sources (lakehouses, eventhouses, and Power BI semantic models); the [Fabric data agent](/fabric/data-science/concept-data-agent), which enables conversational Q&A over ontology-grounded data; [Power BI semantic models](/fabric/data-warehouse/semantic-models), which provide curated analytics with measures and hierarchies. The ontology includes a Natural Language to Ontology (NL2Ontology) layer that converts natural-language questions into structured queries, so agents can ask questions using business terms instead of table names or query syntax.

When you connect your Foundry agent to Fabric IQ by registering it as a server-side tool, your agent can delegate natural-language tasks to the Fabric IQ workload—for example, "Which customers placed orders above $10,000 last quarter?" Fabric IQ handles data retrieval, ontology-grounded reasoning, and response synthesis, then returns the result to your agent. All requests run in the context of the signed-in user, honor Fabric permissions and governance policies, and remain within the Microsoft Fabric trust boundary.

## Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fabric IQ | ✔️ | — | — | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

Before you begin, make sure you have:

- A [Microsoft Fabric license](https://www.microsoft.com/microsoft-fabric) that grants access to the Fabric items your agent queries. Users who invoke Fabric IQ through your agent must also have this license.
- An active [Microsoft Foundry project](../../../how-to/create-projects.md) with a deployed model.
- **Azure RBAC roles**:
  - **Foundry User** role on the Foundry project for the developer identity, the agent's runtime identity, and any user identity involved in OAuth flows.
  - **Foundry Project Manager** role on the Foundry project for creating a Foundry connection to the Fabric IQ endpoint.

## Connect to Fabric IQ

Fabric IQ acts as a server-side tool. Your agent delegates natural-language tasks to it — Fabric IQ handles data retrieval from Microsoft Fabric, reasoning, and response synthesis — then returns the result to your agent.

### Find your Fabric IQ server details

Fabric IQ exposes different MCP endpoint URLs depending on the type of Fabric item you're connecting to. The value you supply as `server_url` follows one of these patterns:

| Fabric item type | `server_url` pattern | Supported authentication |
|---|---|---|
| **Power BI semantic model** | `https://{host}/v1/mcp/powerbi` | BYO Entra app, managed OAuth |
| **Ontology** | `https://{host}/v1/mcp/dataPlane/workspaces/{workspaceId}/items/{itemId}/ontologyEndpoint` | BYO Entra app |
| **Data agent** | `https://{host}/v1/mcp/workspaces/{workspaceId}/dataagents/{dataAgentId}/agent` | BYO Entra app, managed OAuth |

Replace the placeholders as follows:

- `{host}` — The Fabric API host, typically `api.fabric.microsoft.com`
- `{workspaceId}` — The GUID of your Microsoft Fabric workspace
- `{itemId}` / `{dataAgentId}` — The GUID of the specific Fabric item

You can find the workspace and item GUIDs in the Microsoft Fabric portal: open your workspace, select the item, and copy the IDs from the browser URL.

For **`server_label`**, use any short lowercase identifier with hyphens, for example `fabriciq-ontology`. This label appears in approval prompts when the model calls the tool.

### Add the Fabric IQ tool to your agent

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    FabricIQPreviewTool,
)

PROJECT_ENDPOINT = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT = os.environ.get("FOUNDRY_MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
FABRICIQ_CONNECTION_NAME = "fabriciq-conn"
FABRICIQ_SERVER_LABEL = os.environ["FABRICIQ_SERVER_LABEL"]
FABRICIQ_SERVER_URL = os.environ["FABRICIQ_SERVER_URL"]
AGENT_NAME = "fabriciq-agent"

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()

# Retrieve the Fabric IQ connection
fabriciq_conn = project.connections.get(FABRICIQ_CONNECTION_NAME)

# Create an agent with the Fabric IQ tool
tool = FabricIQPreviewTool(
    project_connection_id=fabriciq_conn.id,
    server_label=FABRICIQ_SERVER_LABEL,
    server_url=FABRICIQ_SERVER_URL,
)

agent = project.agents.create_version(
    agent_name=AGENT_NAME,
    definition=PromptAgentDefinition(
        model=MODEL_DEPLOYMENT,
        instructions=(
            "You are a helpful assistant with access to your organization's "
            "Microsoft Fabric data through Fabric IQ. "
            "Use Fabric IQ to answer questions about business entities, "
            "relationships, and data in the ontology—such as customers, orders, products, and pipelines."
        ),
        tools=[tool],
    ),
)
print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

# Invoke the agent
user_input = "Which customers placed orders above $10,000 last quarter?"
stream_response = openai.responses.create(
    stream=True,
    input=user_input,
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)

for event in stream_response:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
    elif event.type == "response.completed":
        print(f"\n\nCompleted. Full response: {event.response.output_text}")

# Clean up
project.agents.delete_version(agent_name=agent.name, agent_version=agent.version)
```

**Expected output**: The agent calls Fabric IQ with the user's query. Fabric IQ queries the ontology-grounded data using your business terms, synthesizes results from bound OneLake sources, and returns the answer as streamed text.

:::zone-end



:::zone pivot="rest-api"

**Step 1:** Create the agent with the Fabric IQ tool:

```http
POST {project_endpoint}/agents/{agent_name}/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "definition": {
    "kind": "prompt",
    "model": "gpt-4o-mini",
    "instructions": "You are a helpful assistant with access to your organization's Microsoft Fabric data through Fabric IQ. Use Fabric IQ to answer questions about business entities, relationships, and data in the ontology—such as customers, orders, products, and pipelines.",
    "tools": [
      {
        "type": "fabric_iq_preview",
        "project_connection_id": "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.CognitiveServices/accounts/{account}/projects/{project}/connections/{connection-name}",
        "server_label": "{fabric-iq-server-label}",
        "server_url": "{fabric-iq-server-url}"
      }
    ]
  }
}
```

**Step 2:** Create a conversation session:

```http
POST {project_endpoint}/openai/v1/conversations
Authorization: Bearer {token}
Content-Type: application/json

{}
```

The response includes an `id` field. Use it in the next step.

**Step 3:** Send a request to the agent:

```http
POST {project_endpoint}/openai/v1/responses
Authorization: Bearer {token}
Content-Type: application/json

{
  "conversation": "{conversation_id}",
  "input": "Which customers placed orders above $10,000 last quarter?",
  "agent_reference": {
    "type": "agent_reference",
    "name": "{agent_name}"
  }
}
```

The response includes metadata about the agent execution and a `text` field in `content` with the synthesized answer.

> [!NOTE]
> Use token scope `https://ai.azure.com/.default` when getting the bearer token.

:::zone-end

## Optional parameters

`FabricIQPreviewTool` accepts the following optional parameter in addition to the required fields:

| Parameter | Type | Default | Description |
|---|---|---|---|
| `require_approval` | `string` | `"always"` | Controls whether the agent must ask for user approval before executing actions. Accepted values: `"always"`, `"never"`. |

:::zone pivot="python"

```python
tool = FabricIQPreviewTool(
    project_connection_id=fabriciq_conn.id,
    server_label=FABRICIQ_SERVER_LABEL,
    server_url=FABRICIQ_SERVER_URL,
    require_approval="never",  # optional; "always" (default) or "never"
)
```

:::zone-end

:::zone pivot="rest-api"

```json
{
  "type": "fabric_iq_preview",
  "project_connection_id": "...",
  "server_label": "{fabric-iq-server-label}",
  "server_url": "https://{fabric-iq-server-url}",
  "require_approval": "never"
}
```

:::zone-end

## Authentication and security

Fabric IQ uses Microsoft Entra ID delegated authentication (On-Behalf-Of, OBO). All requests run in the context of the signed-in user. Application-only (app-only) authentication isn't supported. Microsoft Fabric permissions and data governance policies are enforced automatically — Fabric IQ can never surface data that the signed-in user isn't already permitted to see.

The authentication method available depends on the Fabric item type:

- **Ontology** — BYO Entra app only. You must register a dedicated Entra application with Power BI delegated permissions.
- **Data agent** — BYO Entra app (with data agent scopes) or managed OAuth.
- **Power BI semantic model** — BYO Entra app or managed OAuth.

### Set up your Entra app for ontology (one-time, per organization)

An Entra admin must complete the following steps before you can create a Fabric IQ connection for an ontology item in Foundry.

#### Create the app registration

1. Go to the [Microsoft Entra admin center](https://entra.microsoft.com/). In the left navigation, select **Entra ID** > **App registrations**.
1. Select **New registration**. Give the app a descriptive name and set **Supported account types** to **Accounts in this organizational directory only**. Select **Register**.
1. Copy the **Application (client) ID**. You need this value when creating the Foundry connection.
1. Select **API permissions** > **Add a permission** > **APIs my organization uses**. Search for **Power BI service**, select **Delegated permissions**, and add the following permissions:
   - `Item.Execute.All`
   - `Item.Read.All`

   :::image type="content" source="../../media/tools/fabric-iq/entra-api-permissions-search.png" alt-text="Screenshot of the Request API permissions panel in the Microsoft Entra admin center, showing the APIs my organization uses tab with Power BI Service found by searching for Power BI service." lightbox="../../media/tools/fabric-iq/entra-api-permissions-search.png":::

   Select **Add permissions**.
1. Select **Grant admin consent for [your tenant]**. Review the confirmation dialog and select **Yes**.
1. Select **Certificates & secrets** > **New client secret**. Add a description and expiration. Select **Add**, then immediately copy the secret **Value** — it's only shown once.
1. Copy your **Directory (tenant) ID** from the **Microsoft Entra ID** overview page.

### Fill in the Foundry connection values

In [Microsoft Foundry](https://ai.azure.com/nextgen), open your project and go to **Settings** > **Connections** > **New connection** > **Fabric IQ**. Fill in the following fields:

| Field | Value |
| --- | --- |
| **Client ID** | Application (client) ID from step 3 |
| **Client secret** | Client secret value from step 6 |
| **Authorization URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/authorize` |
| **Token URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
| **Refresh URL** | `https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token` |
| **Scopes** | `https://analysis.windows.net/powerbi/api/Item.Execute.All,https://analysis.windows.net/powerbi/api/Item.Read.All` |

Replace `{tenant-id}` with your Directory (tenant) ID from step 7. Select **Save** to create the connection.

> [!NOTE]
> For data agent connections using BYO Entra, use the `DataAgent.Execute.All` delegated permission instead of the Power BI scopes listed above. Add `https://analysis.windows.net/powerbi/api/DataAgent.Execute.All` as the scope in the Foundry connection, and grant admin consent for that permission in your app registration.

### Add the redirect URI to your app registration

After Foundry creates the connection, it displays an OAuth redirect URL. Add this URL to your app registration:

1. In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Entra ID** > **App registrations** and select your app.
1. Select **Authentication** > **Add a platform** > **Web**.
1. Under **Redirect URIs**, paste the OAuth redirect URL from Foundry.
1. Select **Configure**.

## Admin management

### Govern access with your Entra app registration

For connections that use BYO Entra app authentication, your Entra admin controls which users in your organization can access Fabric IQ data on behalf of signed-in users through the app registration.

- **Grant consent**: In the [Microsoft Entra admin center](https://entra.microsoft.com/), go to **Entra ID** > **App registrations** > select your app > **API permissions**. Select **Grant admin consent for [your tenant]**.
- **Revoke consent**: On the same **API permissions** page, select the relevant permission and select **Revoke admin consent**. Existing tokens remain valid until they expire; no new tokens are issued after revocation.

### Restrict network access

To restrict agent traffic to your private network, configure Foundry Agent Service with a virtual network. See [Private networking for agents](../virtual-networks.md) for setup instructions.

### Publish Fabric items before use

A Fabric admin must publish each Fabric item — ontology, data agent, or Power BI semantic model — before it can be consumed through Fabric IQ. Unpublished items aren't reachable at the MCP endpoint, and requests against them fail. Confirm that the item is published in the Microsoft Fabric portal before configuring the Foundry connection.

## Related content

- [What is Fabric IQ (preview)?](/fabric/iq/overview)
- [What is ontology (preview)?](/fabric/iq/ontology/overview)
- [Fabric data agent concepts](/fabric/data-science/concept-data-agent)
- [Overview of the Power BI MCP servers (preview)](/power-bi/developer/mcp/mcp-servers-overview)
- [Tool best practices](../../concepts/tool-best-practice.md)
