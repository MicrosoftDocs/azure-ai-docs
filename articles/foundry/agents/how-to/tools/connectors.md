---
title: "Add managed MCP servers powered by connector namespaces (preview)"
description: "Add managed MCP servers powered by connector namespaces to your Foundry agents. Browse, configure, and connect to over 1,000 SaaS and line-of-business services from the Foundry Tools Catalog."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 05/27/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
  - references_regions
ai-usage: ai-assisted
zone_pivot_groups: foundry-connector-config
---

# Add managed MCP servers powered by connector namespaces (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

> [!NOTE]
> For information on optimizing tool usage, see [best practices](../../concepts/tool-best-practice.md).

The Foundry Tools Catalog provides over 1,000 connectors — pre-built integrations to SaaS, data, and line-of-business systems. When you add a connector to your agent, Foundry creates a **managed MCP server**: an MCP server that Foundry provisions and manages in your Foundry account's Connector Namespace. Your agent calls the managed MCP server's tools to perform actions during a conversation — for example, creating a GitHub issue, querying a database, or sending a message.

> [!NOTE]
> Only validated connectors surface the new managed-MCP-server experience in the Foundry portal **Add tool** catalog. Unvalidated connectors remain available through the previous connector experience. If you configure connectors through the code-first path (REST API, SDK, or `azd`), there's no gating — you can use any connector in the catalog. Reach out to the Foundry team if you run into issues with a specific connector.

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

## Supported regions

Managed MCP servers powered by connector namespaces are available in the following Foundry project regions:

- australiaeast
- brazilsouth
- canadacentral
- eastus2
- francecentral
- germanywestcentral
- japaneast
- norwayeast
- southafricanorth
- southcentralus
- spaincentral
- swedencentral
- switzerlandnorth
- westus3

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
1. Fill in the credentials the connector requires. Foundry generates the form from the connector's definition. For **OAuth2** connectors, Foundry displays an authorization link — sign in with the account you want to use, then authorize the connection.
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

> [!TIP]
> If you use GitHub Copilot for Azure or another coding agent that supports skills, point it at the [Foundry tool catalog skill](https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/foundry-agent/create/references/foundry-tool-catalog.md). The skill packages the same REST flows shown below so the agent can generate connector wiring code for you.

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

After running either scenario, extract the variables you need for the next steps:

```bash
# Replace .value[0] with the correct index if the search returns multiple results
ENTITY_ID=$(echo "$RESPONSE" | jq -r '.value[0].entityId')
CONNECTOR_NAME=$(echo "$RESPONSE" | jq -r '.value[0].annotations.name')

echo "entityId:       $ENTITY_ID"
echo "connectorName:  $CONNECTOR_NAME"
```

> [!NOTE]
> Foundry currently supports `OAuth2` connectors for the managed MCP server flow. Inspect `properties["x-ms-connection-parameters"]` on the catalog row to confirm: the parameter set contains a field with `"type": "oauthSetting"` for an OAuth2 connector.

### Step 3: Create the project connection

Set your remaining variables (`ENTITY_ID` and `CONNECTOR_NAME` were set in Step 2):

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

Issue the create PUT. The required fields are `connectorName`, the `toolEntityId` from Step 2, and `metadata.connectionproperties` with the connector name as a stringified JSON object.

> [!IMPORTANT]
> Set `target` to the literal string `"https://placeholder"` on this PUT. The platform rewrites it to the real managed MCP server URL when you register actions in [Step 6](#step-6-register-the-connector-actions). Do not attempt to compute or guess a target URL here.

```bash
curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "OAuth2",
      "category": "RemoteTool",
      "connectorName": "'"$CONNECTOR_NAME"'",
      "target": "https://placeholder",
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

A successful response returns HTTP 200 with `overallStatus: "Unauthenticated"`. The status remains `Unauthenticated` until both [Step 4](#step-4-get-an-oauth-consent-link) (OAuth consent) and [Step 6](#step-6-register-the-connector-actions) (register actions) complete.

### Step 4: Get an OAuth consent link

Each end-user that calls the agent must complete a one-time OAuth consent. Call `listConsentLinks` to mint a per-user authorization URL.

```bash
CALLER_OID=$(az ad signed-in-user show --query id -o tsv)
CALLER_TID=$(az account show --query tenantId -o tsv)

CONSENT_RESPONSE=$(curl -sS -X POST \
  "$CONNECTION_URL&action=listConsentLinks" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": [{
      "objectId":      "'"$CALLER_OID"'",
      "parameterName": "token",
      "redirectUrl":   "https://ai.azure.com/nextgen/authConsentPopup",
      "tenantId":      "'"$CALLER_TID"'"
    }]
  }')

CONSENT_URL=$(echo "$CONSENT_RESPONSE" | jq -r '.value[0].link')
echo "Open this URL in a browser to authorize the connector:"
echo "$CONSENT_URL"
```

Open the URL in a browser, sign in to the connector's service, and approve the consent prompt. The browser redirects to a blank Foundry page when consent succeeds — the gateway has stored the token.

> [!NOTE]
> The consent link is short-lived (about one hour). If a click returns a 500 error, re-run `listConsentLinks` to mint a fresh link. For service-principal callers, supply the principal's `objectId` and home `tenantId` instead of the signed-in user's.

### Step 5: List the available operations

Get the operation catalog for the connector from Logic Apps. The `eastus` region is shared with the asset gallery.

```bash
OPERATIONS_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID\
/providers/Microsoft.Web/locations/eastus/managedApis/$CONNECTOR_NAME\
/apiOperations?api-version=2016-06-01"

curl -sS "$OPERATIONS_URL" -H "Authorization: Bearer $ARM_TOKEN" \
  | jq -r '.value[] | select(.properties.isWebhook != true and .properties.isNotification != true)
                    | "\(.name)\t\(.properties.summary)"'
```

Each row prints an operation name (the value you pass to `mcpserverConfigProperties.operations[].name` in the next step) and its human-readable summary. Skip webhook and notification operations — they're triggers, not agent-callable actions.

To inspect the input schema for a specific operation, expand `inputsDefinition`:

```bash
OPERATION_NAME=<operation-name>   # for example, GetFileMetadata

curl -sS "https://management.azure.com/subscriptions/$SUBSCRIPTION_ID\
/providers/Microsoft.Web/locations/eastus/managedApis/$CONNECTOR_NAME\
/apiOperations/$OPERATION_NAME?api-version=2016-06-01&\$expand=properties/inputsDefinition" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  | jq '.properties.inputsDefinition'
```

Use `properties` and `required` from `inputsDefinition` to build each operation's `agentParameters[].schema` in the next step. Map `inputsDefinition.properties[name].title` ? `x-ms-summary`, and copy `type` and `description` as-is.

### Step 6: Register the connector actions

Issue a second PUT against the same connection name. The body is identical to [Step 3](#step-3-create-the-project-connection) plus an additional `metadata.mcpserverConfigProperties` field — a stringified JSON object that lists the operations the agent can invoke and each operation's parameter schema.

> [!TIP]
> Register only the operations your agent actually needs. Limiting the action set reduces the risk of unintended operations and helps the model reason more effectively about available tools.

```bash
# Build mcpserverConfigProperties as a JSON string.
# Replace the operations[] array with the ops you chose in Step 5.
MCP_CONFIG=$(jq -c -n \
  --arg conn "$CONNECTION_NAME" \
  --arg name "$CONNECTOR_NAME" '
  {
    description: "",
    state:       "Enabled",
    connectors: [{
      name:           $name,
      connectionName: $conn,
      displayName:    $name,
      description:    "",
      operations: [
        {
          name:        "GetFileMetadata",
          displayName: "Get file metadata using id",
          description: "",
          userParameters:  [],
          agentParameters: [{
            name: "id",
            schema: {
              type:           "string",
              description:    "The unique identifier of the file.",
              "x-ms-summary": "File Id"
            }
          }]
        }
      ]
    }]
  }')

curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "OAuth2",
      "category": "RemoteTool",
      "connectorName": "'"$CONNECTOR_NAME"'",
      "target": "https://placeholder",
      "credentials": {},
      "peRequirement": "NotRequired",
      "metadata": {
        "type": "gateway_connector",
        "toolEntityId": "'"$ENTITY_ID"'",
        "connectionproperties": "{\"connectorName\":\"'"$CONNECTOR_NAME"'\"}",
        "mcpserverConfigProperties": '"$(jq -Rs . <<< "$MCP_CONFIG")"'
      }
    }
  }'
```

The response rewrites `target` to the real managed MCP server URL — for example, `https://app-XX.<region>.logic.azure.com/api/connectorGateways/<envId>/mcpServerConfigs/<connectionName>/mcp`. Once both this PUT and the Step 4 consent have completed, `overallStatus` flips to `Connected`.

> [!NOTE]
> The portal replaces `mcpserverConfigProperties` wholesale when the user re-edits the action list. To change the operations later, re-run this PUT with the full new operations array — not a partial diff.

### Step 7: Use the connection from your agent

Get the managed MCP server URL from the connection. After [Step 6](#step-6-register-the-connector-actions), `target` is the real gateway URL (no longer `https://placeholder`).

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

:::zone-end

:::zone pivot="azd"

The [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`) provides commands to create and manage connector connections through the `microsoft.foundry` extension. The `azd` path supports **OAuth2** connectors, which are the connectors supported in Foundry today.

> [!TIP]
> If you use GitHub Copilot for Azure or another coding agent that supports skills, point it at the [Foundry tool catalog skill](https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/foundry-agent/create/references/foundry-tool-catalog.md). The skill packages the same `azd` flows shown below so the agent can generate connector wiring commands for you.

### Step 1: Install prerequisites

```pwsh
azd auth login

# Install the Foundry extensions for azd
azd extension install microsoft.foundry

azd ai project set "https://<account>.services.ai.azure.com/api/projects/<project>"
```

> [!NOTE]
> The `microsoft.foundry` extension is in preview. It bundles the top-level `azd ai` experience across `agent`, `connection`, `inspector`, `project`, `routine`, `skill`, and `toolbox`. Use `azd` version 1.25.2 or later.

### Step 2: Create the OAuth2 connection

`azd ai connection create` registers the connector as a project connection with `authType=OAuth2` and the required gateway metadata. Pass the connector's catalog name with `--connector-name` (for example, `box`, `linkedinv2`, `outlook`, `github`).

The connector name is the `annotations.name` value returned by the Foundry Tools Catalog API. Switch to the **REST API** pivot and follow [Step 2: Discover the connector](#step-2-discover-the-connector) to list every connector or look up a specific one.

```pwsh
azd ai connection create <connection-name> `
  --connector-name <connector-name>
```

For example, to create a connection to the Box connector:

```pwsh
azd ai connection create my-box-conn `
  --connector-name box
```

### Step 3: Complete OAuth consent

The connection is created in an `Unauthenticated` state, and the consent URL is returned in the connection details at creation time. Inspect the connection to retrieve it:

```pwsh
azd ai connection show my-box-conn
```

Open the returned consent URL in a browser and sign in once. After consent is recorded, subsequent MCP calls succeed and `overallStatus` transitions to `Connected`.

### Step 4: Register the connector actions

Use `--metadata mcpserverConfigProperties=<json>` to declare which connector operations the agent can call and which parameters the model controls.

Values for `connectorName`, `operationName`, and each operation's parameter names come from the Foundry Tools Catalog API. Switch to the **REST API** pivot and use [Step 2: Discover the connector](#step-2-discover-the-connector) to retrieve a connector's full metadata — operations are listed under `properties.actions[]`, and each operation's parameters are listed under `parameters[]`.

The example below registers a single `GetEmailsV2` operation on an Outlook connection:

```pwsh
$mcp = @{
  connectors = @(@{
    connectorName = "outlook"
    operations = @(@{
      operationName = "GetEmailsV2"
      agentParameters = @(
        @{ name = "folderPath";      required = $true  },
        @{ name = "top";             required = $false },
        @{ name = "fetchOnlyUnread"; required = $false }
      )
    })
  })
} | ConvertTo-Json -Depth 10 -Compress

azd ai connection update my-outlook-conn `
  --metadata "mcpserverConfigProperties=$mcp"
```

> [!TIP]
> Register only the operations your agent actually needs. Limiting the action set reduces the risk of unintended operations and helps the model reason more effectively about available tools.

### Step 5: Use the connection from an agent

After the connection is created and consent is recorded, reference it from your agent the same way as any other managed MCP server. The simplest path is to add the connection to a [Foundry Toolbox](toolbox.md) and attach the toolbox to your agent:

```yaml
# my-toolbox.yaml
description: Toolbox with connector MCP servers
connections:
  - name: my-box-conn
  - name: my-outlook-conn
```

```pwsh
azd ai toolbox create my-toolbox `
  --from-file .\my-toolbox.yaml
```

For end-to-end agent scaffolding and deployment with `azd`, see [Create and use a Foundry Toolbox](toolbox.md).

### Manage the connection

```pwsh
# List connections in the project
azd ai connection list

# Show details for one connection
azd ai connection show <connection-name>

# Delete a connection
azd ai connection delete <connection-name> --force
```

:::zone-end

## Related content

- [Connect agents to Model Context Protocol servers](model-context-protocol.md)
- [MCP server authentication](../mcp-authentication.md)
- [Agent tools overview](../../concepts/tool-catalog.md)
- [Create and use a Foundry Toolbox](toolbox.md)

