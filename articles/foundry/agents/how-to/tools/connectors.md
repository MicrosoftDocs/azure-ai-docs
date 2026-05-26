---
title: "Add managed MCP servers powered by connector namespaces (preview)"
description: "Add managed MCP servers powered by connector namespaces to your Foundry agents. Browse, configure, and connect to over 1,000 SaaS and line-of-business services from the Foundry Tools Catalog."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 05/10/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: foundry-connector-config
---

# Add managed MCP servers powered by connector namespaces (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

The Foundry Tools Catalog provides over 1,000 connectors — pre-built integrations to SaaS, data, and line-of-business systems. When you add a connector to your agent, Foundry creates a **managed MCP server**: an MCP server that Foundry provisions and manages in your Foundry account's Connector Namespace. Your agent calls the managed MCP server's tools to perform actions during a conversation — for example, creating a GitHub issue, querying a database, or sending a message.

> [!IMPORTANT]
> Non-Microsoft tools including third-party MCP servers available in the Foundry Tools Catalog ("Third-Party Tools") are Non-Microsoft Products under your agreement governing use of Azure. When you connect to a Third-Party Tool, you do so at your own risk. You're responsible for any terms and charges for Third-Party Tools. Microsoft has no responsibility to you or others in relation to your use of Third-Party Tools. Carefully review and track the Third-Party Tools you add to your MCP client.
>
> Some of your information and data (such as authentication keys and prompt content) might be passed to the Third-Party Tool, or your MCP client might receive data from the Third-Party Tool. Review all data shared with Third-Party Tools and stay aware of third-party practices for data retention and location. You're responsible for managing whether your data flows outside your organization's Azure compliance and geographic boundaries.
>
> MCP implementations are vulnerable to attacks, cascading failures, and loss of human oversight. To mitigate these risks, vet MCP servers for security and reliability, follow Microsoft's recommendations and industry best practices, and implement approval mechanisms to monitor cascading behaviors.

## How it works

Each Foundry account has a **Connector Namespace** — a fully managed service that hosts connector runtimes and MCP servers. Each project maps to an environment in that namespace. When you configure a connector, Foundry publishes it as a managed MCP server in your project's environment. The namespace handles server hosting, tool definitions, authentication, credential management, and lifecycle. Your agent calls the managed MCP server's tools without you writing custom server code or managing infrastructure.

The configuration flow has four steps:

1. **Browse** — find the connector in the Tools Catalog.
1. **Connect** — authenticate to the connector's service.
1. **Select actions** — choose which connector actions to expose as MCP tools.
1. **Add tool** — Foundry creates the managed MCP server and adds it to your agent.

## Publisher tiers and data handling

The catalog includes connectors published by Microsoft, verified third-party publishers, and independent publishers. Check the **By:** field on the connector's detail page before connecting, or review the full list at [List of all MCP servers](/connectors/connector-reference/connector-reference-mcpserver-connectors).

| Publisher tier | Examples | Data responsibility |
|---|---|---|
| **Microsoft** (internal services) | SharePoint, Teams, Dynamics 365 | Data stays on Microsoft infrastructure; Microsoft privacy policies apply end-to-end |
| **Microsoft** (external services) | GitHub | Data transits Microsoft infrastructure to the external service; Microsoft policies apply in transit, the external company's policies apply at the destination |
| **Verified third-party** | Docusign, Databricks, Box | Same as Microsoft external; review the publisher's privacy policy and data-protection terms before connecting |
| **Independent publisher** | Community-contributed connectors | Lower certification bar than first-party connectors; review the publisher's terms and data practices carefully |

The Connector Namespace acts as a proxy to external services. While data is in transit through the namespace (Microsoft infrastructure), Microsoft privacy policies apply. Once the namespace sends the request to the external service, that company's policies govern data storage, retention, and geography.

For details on connector validation and data protection, see [Vet with data protection in connectors](/connectors/protection).

> [!NOTE]
> Managed MCP servers are scoped to the Foundry project where they're created. Connector triggers aren't supported; only actions that your agent can invoke are available.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **Foundry Project Manager** role on the Foundry project.
- Credentials for the service you want to connect to (for example, an API key, OAuth account, or personal access token).

## Authentication types

| Auth type | When to use | Catalog signal |
| --- | --- | --- |
| **OAuth2** | The connector uses OAuth2 authorization code flow. Foundry manages the token exchange; you complete a one-time consent flow. | `x-ms-connection-parameters` contains a field with `"type": "oauthSetting"` |

## Add a managed MCP server

> [!NOTE]
> The configuration experience in this article applies to managed MCP servers that support **OAuth2** authentication. For managed MCP servers with other authentication types, see [Add connector actions as agent tools in Azure Logic Apps](/azure/logic-apps/add-agent-tools-connector-actions).

:::zone pivot="foundry-portal"

### Step 1: Browse connectors

1. In [Microsoft Foundry](https://ai.azure.com/nextgen), open your project and select **Tools** in the left navigation.
1. Select **+ Add tool** to open the Tools Catalog.
1. Browse or search for the connector you want to use. The catalog lists all supported connectors with details such as the publisher, supported authentication types, and available actions.
1. Select the connector to open its detail page.

### Step 2: Configure the connection

1. On the connector detail page, select **Configure**.
1. Fill in the credentials the connector requires. Foundry generates the form from the connector's definition; fields vary by connector:
   - **OAuth2** — Foundry displays an authorization link. Sign in with the account you want to use, then authorize the connection. About half of catalog connectors use this flow.
   - **CustomKeys** — Foundry displays one or more input fields for secrets such as an API key, personal access token, or username and password. Enter the credentials issued by the service.
   - **None** — Some connectors require no credentials. The form has no credential fields.
1. Select **Connect** to save the credentials and establish the connection.

### Step 3: Select connector actions

1. After the connection is established, review the list of available actions (for example, **Create issue** for GitHub, or **Send message** for Slack).
1. Select the actions you want your agent to be able to call.
1. You can change the action selection later by editing the MCP server in the **Tools** view.

> [!TIP]
> Select only the actions your agent actually needs. Limiting the action set reduces the risk of unintended operations and helps the model reason more effectively about available tools.

### Step 4: Add the tool

1. Review your configuration — the connector name, connection, and selected actions.
1. Select **Add tool**.

Foundry creates a managed MCP server and adds it to your agent. You can view and edit it at any time from **Tools** in your project.

:::zone-end

:::zone pivot="programming-language-rest"

### Step 1: Acquire tokens

You need two separate tokens: one for the Foundry Tools Catalog (an Azure Machine Learning endpoint) and one for the Azure Resource Manager API that manages project connections.

```bash
# Token for the Foundry Tools Catalog (AzureML endpoint)
CATALOG_TOKEN=$(az account get-access-token \
  --resource https://ai.azure.com \
  --query accessToken -o tsv)

# Token for Azure Resource Manager (connection and agent management)
ARM_TOKEN=$(az account get-access-token \
  --resource https://management.azure.com \
  --query accessToken -o tsv)
```

### Step 2: Discover the connector

The catalog is always served from the `eastus` region regardless of your project's region. Choose one of the following scenarios.

**Scenario 1: List all supported connectors**

Use this to browse the full catalog. The catalog has over 1,000 connectors; use `skip` to paginate. The response includes `totalCount` so you can determine how many pages to fetch.

```bash
RESPONSE=$(curl -sS -X POST \
  "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools" \
  -H "Authorization: Bearer $CATALOG_TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-ms-user-agent: AzureMachineLearningWorkspacePortal/12.0" \
  -d '{
    "freeTextSearch": "*",
    "filters": [
      { "field": "entityContainerId", "operator": "eq", "values": ["connectors-registry-prod-bl"] },
      { "field": "type",              "operator": "eq", "values": ["tools"] },
      { "field": "kind",              "operator": "eq", "values": ["Versioned"] },
      { "field": "labels",            "operator": "eq", "values": ["latest"] }
    ],
    "includeTotalResultCount": true,
    "pageSize": 100,
    "skip": 0
  }')

# Print name, title, and detected auth type for each connector
echo "$RESPONSE" | jq -r '
  .totalCount as $total |
  "Total connectors: \($total)",
  (.value[] | "\(.annotations.name)\t\(.properties.title)\t\(
    .properties["x-ms-connection-parameters"] |
    if . == null then "None"
    elif ([.[].type] | any(. == "oauthSetting")) then "OAuth2"
    elif ([.[].type] | any(. == "securestring")) then "CustomKeys"
    else "None" end
  )")
'
```

**Scenario 2: Retrieve details of a specific connector**

Use an exact `eq` filter on `annotations/name` to fetch a single connector and its full metadata, including `x-ms-connection-parameters`.

```bash
CONNECTOR_NAME="github"   # replace with the connector's annotations.name value

RESPONSE=$(curl -sS -X POST \
  "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools" \
  -H "Authorization: Bearer $CATALOG_TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-ms-user-agent: AzureMachineLearningWorkspacePortal/12.0" \
  -d "{
    \"freeTextSearch\": \"*\",
    \"filters\": [
      { \"field\": \"entityContainerId\", \"operator\": \"eq\",  \"values\": [\"connectors-registry-prod-bl\"] },
      { \"field\": \"type\",              \"operator\": \"eq\",  \"values\": [\"tools\"] },
      { \"field\": \"kind\",              \"operator\": \"eq\",  \"values\": [\"Versioned\"] },
      { \"field\": \"labels\",            \"operator\": \"eq\",  \"values\": [\"latest\"] },
      { \"field\": \"annotations/name\",  \"operator\": \"eq\",  \"values\": [\"$CONNECTOR_NAME\"] }
    ],
    \"includeTotalResultCount\": true,
    \"pageSize\": 1
  }")
```

After running either scenario, extract the variables you need for the next step:

From the response, extract the following and set them as shell variables:

```bash
# Replace .value[0] with the correct index if the search returns multiple results
ENTITY_ID=$(echo "$RESPONSE" | jq -r '.value[0].entityId')
TARGET_URL=$(echo "$RESPONSE" | jq -r '.value[0].properties["x-ms-runtime-urls"][0]')

# Detect auth type: oauthSetting → OAuth2 | securestring → CustomKeys | absent → None
AUTH_TYPE=$(echo "$RESPONSE" | jq -r '
  .value[0].properties["x-ms-connection-parameters"]
  | if . == null then "None"
    elif [.[] | .type] | any(. == "oauthSetting") then "OAuth2"
    elif [.[] | .type] | any(. == "securestring") then "CustomKeys"
    else "None" end
')

echo "entityId:  $ENTITY_ID"
echo "targetURL: $TARGET_URL"
echo "authType:  $AUTH_TYPE"   # use this value in Step 3
```

The `AUTH_TYPE` value tells you which connection body to use in Step 3.

### Step 3: Create the project connection

Set your remaining variables (`ENTITY_ID`, `TARGET_URL`, `CONNECTOR_NAME`, and `AUTH_TYPE` were set in Step 2):

```bash
SUBSCRIPTION_ID=<your-subscription-id>
RESOURCE_GROUP=<your-resource-group>
ACCOUNT_NAME=<your-foundry-account-name>
PROJECT_NAME=<your-project-name>
CONNECTION_NAME=<name-for-this-connection>

CONNECTION_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID\
/resourceGroups/$RESOURCE_GROUP\
/providers/Microsoft.CognitiveServices/accounts/$ACCOUNT_NAME\
/projects/$PROJECT_NAME\
/connections/$CONNECTION_NAME?api-version=2025-04-01-preview"
```

**OAuth2:**

Foundry manages the OAuth token exchange for the connector. The required fields are `connectorName`, the `toolEntityId` from Step 2, and `metadata.connectionproperties` with the connector name as a JSON string. `TARGET_URL` is the connector's runtime URL from Step 2.

```bash
curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "OAuth2",
      "category": "RemoteTool",
      "connectorName": "'"$CONNECTOR_NAME"'",
      "target": "'"$TARGET_URL"'",
      "credentials": {},
      "peRequirement": "NotRequired",
      "metadata": {
        "type": "gateway_connector",
        "toolEntityId": "'"$ENTITY_ID"'",
        "connectionproperties": "{\"connectorName\":\"'"$CONNECTOR_NAME"'\"}"
      }
    }
  }'
```

A successful response returns HTTP 200 with `overallStatus: "Unauthenticated"`. Foundry updates the `target` to its internal endpoint URL during the OAuth consent flow. Use `CONNECTION_NAME` to reference the connection in your agent — you don't need the target URL directly.

**CustomKeys (API key or personal access token):**

Use this when the connector's `x-ms-connection-parameters` contains `securestring`-typed fields. The key name in `credentials.keys` must match the header or parameter name the connector's MCP server expects (for example, `Authorization` for a `Bearer <token>` header).

```bash
curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "CustomKeys",
      "category": "RemoteTool",
      "target": "'"$TARGET_URL"'",
      "credentials": {
        "keys": {
          "Authorization": "Bearer '"$YOUR_TOKEN"'"
        }
      },
      "peRequirement": "NotRequired"
    }
  }'
```

After a successful PUT, confirm the connection with:

```bash
curl -sS "$CONNECTION_URL" -H "Authorization: Bearer $ARM_TOKEN"
```

For CustomKeys, the response returns `"credentials": null` — the server scrubs secrets after write. For OAuth2, `overallStatus` starts as `Unauthenticated` until you complete the OAuth consent flow.

### Step 4: Add the connection to your agent

Get the MCP server URL from the connection (the `target` field, which is updated to the active endpoint after OAuth consent):

```bash
SERVER_URL=$(curl -sS "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" | jq -r '.properties.target')

echo "serverURL: $SERVER_URL"
```

**Prompt agent (Python SDK):**

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"

client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential()
)

agent = client.agents.create_agent(
    model="gpt-4o",
    name="my-connector-agent",
    instructions="You are a helpful assistant.",
    tools=MCPTool(
        server_label=CONNECTION_NAME,
        server_url=SERVER_URL,
        project_connection_id=CONNECTION_NAME
    ).definitions
)
print(f"Created agent: {agent.id}")
```

For other languages and runtime options, see [Connect agents to MCP servers](model-context-protocol.md).

**Toolbox (Python SDK):**

```python
toolbox_version = client.beta.toolboxes.create_toolbox_version(
    toolbox_name="my-toolbox",
    description="Toolbox with connector MCP server",
    tools=[
        MCPTool(
            server_label=CONNECTION_NAME,
            server_url=SERVER_URL,
            project_connection_id=CONNECTION_NAME,
            require_approval="never",
        )
    ],
)
print(f"Created toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

For full toolbox configuration and deployment, see [Create and use a Foundry Toolbox](toolbox.md).

> [!NOTE]
> For OAuth2 connections, the first MCP call from your agent returns error code `-32006` with a `consent_url`. Open that URL in a browser and complete the OAuth flow. After consent, `overallStatus` transitions to `Connected` and subsequent calls succeed.

:::zone-end

## Related content

- [Connect agents to Model Context Protocol servers](model-context-protocol.md)
- [MCP server authentication](../mcp-authentication.md)
- [Agent tools overview](../../concepts/tool-catalog.md)
- [Create and use a Foundry Toolbox](toolbox.md)

