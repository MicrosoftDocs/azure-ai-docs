---
title: "Automate agents with routines (preview)"
description: "Create, manage, and monitor routines that automatically trigger agents on a schedule, timer, GitHub issue event, or custom event in Microsoft Foundry."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/01/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: foundry-routines-config
---

# Automate agents with routines (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A *routine* is a named automation rule that triggers an agent on a schedule, at a specific time, or in response to an event. You define what fires the routine (the *trigger*) and what agent to invoke (the *action*). Foundry queues the invocation, runs the agent, and stores a run record you can inspect later.

This article shows you how to create, manage, and monitor routines by using the Foundry portal, the REST API, and the Python, C#, and JavaScript SDKs.

> [!NOTE]
> Routines are in preview. Send the `Foundry-Features: Routines=V1Preview` header on every REST call. All routine operations are on the data plane under your project endpoint.


## Supported trigger types

Routines support two categories of trigger.

**Time-based triggers** fire on a recurring schedule or a one-shot timer:

| Trigger type | Description |
|---|---|
| `schedule` | Recurring trigger defined by a cron expression. Minimum interval is five minutes. |
| `timer` | One-shot trigger that fires at a specific future date/time or after a duration. |

**Event-based triggers** fire in response to an external event:

| Trigger type | Description |
|---|---|
| `github_issue` | Fires when a GitHub issue is opened or closed in a connected repository. |
| `custom` | Fires on a provider-specific event you define. |

Event-based routines are powered by the **Connector Namespace** — the same managed service that backs [managed MCP servers](tools/connectors.md) in your Foundry account. Each Foundry account has a Connector Namespace; each project maps to an environment in that namespace. Only connectors that declare trigger support (those with `"triggers"` in their `x-ms-capabilities` field) can be used as event sources for routines. Connectors that expose only actions — such as most managed MCP servers — can't fire event-based routines.

> [!NOTE]
> Your connector credentials are stored and managed by the Connector Namespace, not in your routine definition. At runtime, the namespace retrieves and injects the right token or key when polling for events or receiving webhook calls. Your routine configuration never contains raw credentials.

> [!IMPORTANT]
> Non-Microsoft connectors available in the Foundry Tools Catalog ("Third-Party Tools") are Non-Microsoft Products under your agreement governing use of Azure. When you connect to a Third-Party Tool as an event source, you do so at your own risk. You're responsible for any terms and charges for Third-Party Tools. Microsoft has no responsibility to you or others in relation to your use of Third-Party Tools. Carefully review and track the connectors you use as event sources.
>
> Some of your information and data might be passed to the Third-Party Tool (for example, during webhook subscription or event polling). Review all data shared with Third-Party Tools and stay aware of third-party practices for data retention and location. You're responsible for managing whether your data flows outside your organization's Azure compliance and geographic boundaries.

## Publisher tiers and data handling for event sources

The same connector catalog and publisher tiers that apply to [managed MCP servers](tools/connectors.md#publisher-tiers-and-data-handling) also apply when using a connector as a routine event source. Check the **By:** field on the connector's detail page before connecting, or review the full list at [List of all MCP servers](https://learn.microsoft.com/connectors/connector-reference/connector-reference-mcpserver-connectors).

| Publisher tier | Examples | Data responsibility |
|---|---|---|
| **Microsoft** (internal services) | SharePoint, Teams, Dynamics 365 | Data stays on Microsoft infrastructure; Microsoft privacy and GDPR policies apply end-to-end |
| **Microsoft** (external services) | GitHub | Data transits Microsoft infrastructure to the external service; Microsoft policies apply in transit, the external company's policies apply at the destination |
| **Verified third-party** | Salesforce, Docusign | Same as Microsoft external; review the publisher's privacy policy and GDPR terms before connecting |
| **Independent publisher** | Community-contributed connectors | Lower certification bar than first-party connectors; review the publisher's terms and data practices carefully |

The Connector Namespace acts as a proxy between Foundry and the external event source. While data transits the namespace (Microsoft infrastructure), Microsoft's privacy and GDPR policies apply. Once the namespace sends a request to the external service — for example, to register a webhook or poll for new events — that company's policies govern data storage, retention, and geography.

For details on connector validation and data protection, see [Vet with data protection in connectors](https://learn.microsoft.com/connectors/protection).

## Supported action types

Each routine specifies exactly one action that runs when the routine fires. Two action types are supported:

| Action type | Description |
|---|---|
| `invoke_agent_responses_api` | Invokes the agent through the Responses API. Provide either the agent name or endpoint ID. |
| `invoke_agent_invocations_api` | Invokes the agent through the Invocations API. Requires the endpoint-scoped agent identifier. |

For required and optional fields of each action type, see [Action fields](#action-fields).

## Discover connectors with trigger support

:::zone pivot="foundry-portal"

The portal handles connector browsing and connection setup for you. Skip to [Create a routine](#create-a-routine).

:::zone-end

:::zone pivot="programming-language-rest,programming-language-python,programming-language-csharp,programming-language-javascript"

Event-based routines need two things: a **trigger event source** (a connector operation that fires when an external event occurs) and a **project connection** (credentials Foundry uses to subscribe to or poll that event). The catalog API exposes each connector's full spec, including which operations are triggers and what auth the connector requires.

The end-to-end discovery flow has five steps:

1. Acquire tokens for the catalog API and Azure Resource Manager.
1. Query the catalog to list connectors that declare trigger support.
1. Inspect the connector spec to extract trigger `operationId` values.
1. Read `x-ms-connection-parameters` to determine required auth.
1. Create the project connection.

After completing these steps, use the trigger's `operationId` as the `event_name` when you [create a custom trigger routine](#event-based-triggers), or verify it matches a built-in trigger type such as `github_issue`.

:::zone-end

:::zone pivot="programming-language-rest"

> [!NOTE]
> The connector catalog is always served from the `eastus` region regardless of your project's location.

### Step 1: Acquire tokens

```bash
# Token for the Foundry Tools Catalog
CATALOG_TOKEN=$(az account get-access-token \
  --resource https://ai.azure.com \
  --query accessToken -o tsv)

# Token for Azure Resource Manager (connection management)
ARM_TOKEN=$(az account get-access-token \
  --resource https://management.azure.com \
  --query accessToken -o tsv)
```

### Step 2: List connectors with trigger support

**List all trigger-enabled connectors:**

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

# Print connectors that declare trigger support
echo "$RESPONSE" | jq -r '
  .value[]
  | select(.properties["x-ms-capabilities"] | arrays | contains(["triggers"]))
  | "\(.annotations.name)\t\(.properties.title)"
'
```

**Fetch details of a specific connector:**

```bash
CONNECTOR_NAME="github"   # value from annotations.name in the list above

RESPONSE=$(curl -sS -X POST \
  "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools" \
  -H "Authorization: Bearer $CATALOG_TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-ms-user-agent: AzureMachineLearningWorkspacePortal/12.0" \
  -d "{
    \"freeTextSearch\": \"*\",
    \"filters\": [
      { \"field\": \"entityContainerId\", \"operator\": \"eq\", \"values\": [\"connectors-registry-prod-bl\"] },
      { \"field\": \"type\",              \"operator\": \"eq\", \"values\": [\"tools\"] },
      { \"field\": \"kind\",              \"operator\": \"eq\", \"values\": [\"Versioned\"] },
      { \"field\": \"labels\",            \"operator\": \"eq\", \"values\": [\"latest\"] },
      { \"field\": \"annotations/name\",  \"operator\": \"eq\", \"values\": [\"$CONNECTOR_NAME\"] }
    ],
    \"includeTotalResultCount\": true,
    \"pageSize\": 1
  }")

# Extract entity ID and runtime URL for later steps
ENTITY_ID=$(echo "$RESPONSE" | jq -r '.value[0].entityId')
TARGET_URL=$(echo "$RESPONSE" | jq -r '.value[0].properties["x-ms-runtime-urls"][0]')

echo "entityId:  $ENTITY_ID"
echo "targetURL: $TARGET_URL"
```

### Step 3: Identify trigger operations

Each connector's `x-ms-operations` array lists all available operations. Operations with a non-null `x-ms-trigger` field are event triggers. The `x-ms-trigger` value indicates the trigger mechanism:

| `x-ms-trigger` value | Mechanism | Routine `type` to use |
|---|---|---|
| `"batch"` | Foundry polls the connector endpoint at a fixed interval | `github_issue` (built-in) or `custom` |
| `"single"` | Connector registers a webhook; Foundry receives push notifications | `custom` |

```bash
# Print all trigger operations for the fetched connector
echo "$RESPONSE" | jq -r '
  .value[0].properties["x-ms-operations"][]
  | select(."x-ms-trigger" != null)
  | "\(.operationId)\t trigger=\(."x-ms-trigger")\t \(.operationName)"
'
```

Sample output for the GitHub connector:

```
IssueOpened               trigger=batch    When a new issue is opened and assigned to me
IssueClosed               trigger=batch    When an issue assigned to me is closed
IssueAssigned             trigger=batch    When an issue is assigned to me
WebhookPullRequestTrigger trigger=single   When a pull request is created or modified
```

The `operationId` is the value you pass as `event_name` in a `custom` trigger. The GitHub issue operations are also covered by the built-in `github_issue` trigger type, which handles polling automatically.

### Step 4: Determine connection auth requirements

```bash
AUTH_TYPE=$(echo "$RESPONSE" | jq -r '
  .value[0].properties["x-ms-connection-parameters"]
  | if . == null then "None"
    elif ([.[].type] | any(. == "oauthSetting")) then "OAuth2"
    elif ([.[].type] | any(. == "securestring")) then "CustomKeys"
    else "None" end
')

echo "authType: $AUTH_TYPE"
```

| Auth type | Connection creation |
|---|---|
| `OAuth2` | Create the connection stub via API; complete the OAuth consent flow in the Foundry portal. |
| `CustomKeys` | Create the connection with credentials in a single API call. |
| `None` | Create an unauthenticated connection stub; no credentials required. |

### Step 5: Create the project connection

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
RESOURCE_GROUP="<your-resource-group>"
ACCOUNT_NAME="<your-foundry-account>"
PROJECT_NAME="<your-project>"
CONNECTION_NAME="<name-for-this-connection>"

CONNECTION_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID\
/resourceGroups/$RESOURCE_GROUP\
/providers/Microsoft.CognitiveServices/accounts/$ACCOUNT_NAME\
/projects/$PROJECT_NAME\
/connections/$CONNECTION_NAME?api-version=2025-04-01-preview"
```

**OAuth2:**

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

A successful response returns HTTP 200 with `overallStatus: "Unauthenticated"`. Open the Foundry portal and complete the OAuth consent flow to bring the connection to `"Connected"` status.

**CustomKeys (API key or PAT):**

```bash
curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "CustomKeys",
      "category": "RemoteTool",
      "connectorName": "'"$CONNECTOR_NAME"'",
      "target": "'"$TARGET_URL"'",
      "credentials": {
        "keys": {
          "Authorization": "Bearer '"$YOUR_TOKEN"'"
        }
      },
      "peRequirement": "NotRequired",
      "metadata": {
        "type": "gateway_connector",
        "toolEntityId": "'"$ENTITY_ID"'",
        "connectionproperties": "{\"connectorName\":\"'"$CONNECTOR_NAME"'\"}"
      }
    }
  }'
```

Verify the connection was created:

```bash
curl -sS "$CONNECTION_URL" -H "Authorization: Bearer $ARM_TOKEN" \
  | jq '{name: .name, status: .properties.overallStatus, authType: .properties.authType}'
```

Use `CONNECTION_NAME` as the `connection_id` and the `operationId` from Step 3 as the `event_name` when you create the routine. See [Event-based triggers](#event-based-triggers).

:::zone-end

:::zone pivot="programming-language-python"

```python
import os
import requests
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

# ── Step 1: acquire tokens ─────────────────────────────────────────────────

catalog_token = credential.get_token("https://ai.azure.com/.default").token
arm_token     = credential.get_token("https://management.azure.com/.default").token

CATALOG_URL = "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools"
catalog_headers = {
    "Authorization": f"Bearer {catalog_token}",
    "Content-Type": "application/json",
    "x-ms-user-agent": "AzureMachineLearningWorkspacePortal/12.0",
}
arm_headers = {
    "Authorization": f"Bearer {arm_token}",
    "Content-Type": "application/json",
}

# ── Step 2: find trigger-enabled connectors ────────────────────────────────

def list_trigger_connectors() -> list[dict]:
    resp = requests.post(
        CATALOG_URL,
        headers=catalog_headers,
        json={
            "freeTextSearch": "*",
            "filters": [
                {"field": "entityContainerId", "operator": "eq", "values": ["connectors-registry-prod-bl"]},
                {"field": "type",              "operator": "eq", "values": ["tools"]},
                {"field": "kind",              "operator": "eq", "values": ["Versioned"]},
                {"field": "labels",            "operator": "eq", "values": ["latest"]},
            ],
            "includeTotalResultCount": True,
            "pageSize": 100,
            "skip": 0,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return [
        item for item in resp.json()["value"]
        if "triggers" in (item["properties"].get("x-ms-capabilities") or [])
    ]

for item in list_trigger_connectors():
    print(f"{item['annotations']['name']:30s}  {item['properties'].get('title', '')}")

# ── Steps 3–4: fetch connector spec, read trigger ops and auth type ────────

def get_connector(name: str) -> dict:
    resp = requests.post(
        CATALOG_URL,
        headers=catalog_headers,
        json={
            "freeTextSearch": "*",
            "filters": [
                {"field": "entityContainerId", "operator": "eq", "values": ["connectors-registry-prod-bl"]},
                {"field": "type",              "operator": "eq", "values": ["tools"]},
                {"field": "kind",              "operator": "eq", "values": ["Versioned"]},
                {"field": "labels",            "operator": "eq", "values": ["latest"]},
                {"field": "annotations/name",  "operator": "eq", "values": [name]},
            ],
            "includeTotalResultCount": True,
            "pageSize": 1,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["value"][0]

connector = get_connector("github")
entity_id  = connector["entityId"]
target_url = connector["properties"]["x-ms-runtime-urls"][0]

# Trigger operations
trigger_ops = [
    op for op in connector["properties"].get("x-ms-operations", [])
    if op.get("x-ms-trigger") is not None
]
for op in trigger_ops:
    print(f"  {op['operationId']:35s} trigger={op['x-ms-trigger']:8s} '{op['operationName']}'")

# Auth type
conn_params = connector["properties"].get("x-ms-connection-parameters") or {}
if any(p.get("type") == "oauthSetting" for p in conn_params.values()):
    auth_type = "OAuth2"
elif any(p.get("type") == "securestring" for p in conn_params.values()):
    auth_type = "CustomKeys"
else:
    auth_type = "None"
print(f"auth_type: {auth_type}")

# ── Step 5: create the project connection ──────────────────────────────────

subscription = os.environ["AZURE_SUBSCRIPTION_ID"]
rg           = os.environ["AZURE_RESOURCE_GROUP"]
account      = os.environ["FOUNDRY_ACCOUNT_NAME"]
project      = os.environ["FOUNDRY_PROJECT_NAME"]
conn_name    = "my-connector-conn"

conn_url = (
    f"https://management.azure.com/subscriptions/{subscription}"
    f"/resourceGroups/{rg}/providers/Microsoft.CognitiveServices"
    f"/accounts/{account}/projects/{project}"
    f"/connections/{conn_name}?api-version=2025-04-01-preview"
)

base_metadata = {
    "type": "gateway_connector",
    "toolEntityId": entity_id,
    "connectionproperties": '{"connectorName":"github"}',
}

if auth_type == "OAuth2":
    body = {
        "properties": {
            "authType": "OAuth2", "category": "RemoteTool",
            "connectorName": "github", "target": target_url,
            "credentials": {}, "peRequirement": "NotRequired",
            "metadata": base_metadata,
        }
    }
else:  # CustomKeys
    pat = os.environ["CONNECTOR_PAT"]
    body = {
        "properties": {
            "authType": "CustomKeys", "category": "RemoteTool",
            "connectorName": "github", "target": target_url,
            "credentials": {"keys": {"Authorization": f"Bearer {pat}"}},
            "peRequirement": "NotRequired",
            "metadata": base_metadata,
        }
    }

resp = requests.put(conn_url, headers=arm_headers, json=body, timeout=30)
resp.raise_for_status()
print(f"Connection '{conn_name}' created. Status: {resp.json()['properties'].get('overallStatus')}")
# For OAuth2: open the Foundry portal and complete the OAuth consent flow.
```

After the connection is ready, use `conn_name` as `connection_id` and the trigger operation's `operationId` as `event_name` when you [create the routine](#event-based-triggers).

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using Azure.Identity;

var credential = new DefaultAzureCredential();
var catalogToken = await credential.GetTokenAsync(
    new Azure.Core.TokenRequestContext(["https://ai.azure.com/.default"]));
var armToken = await credential.GetTokenAsync(
    new Azure.Core.TokenRequestContext(["https://management.azure.com/.default"]));

using var http = new HttpClient();
const string CatalogUrl = "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools";

// ── Steps 2–4: fetch connector spec ───────────────────────────────────────

var filterBody = JsonSerializer.Serialize(new
{
    freeTextSearch = "*",
    filters = new object[]
    {
        new { field = "entityContainerId", @operator = "eq", values = new[] { "connectors-registry-prod-bl" } },
        new { field = "type",              @operator = "eq", values = new[] { "tools" } },
        new { field = "kind",              @operator = "eq", values = new[] { "Versioned" } },
        new { field = "labels",            @operator = "eq", values = new[] { "latest" } },
        new { field = "annotations/name",  @operator = "eq", values = new[] { "github" } },
    },
    includeTotalResultCount = true,
    pageSize = 1,
    skip = 0,
});

using var req = new HttpRequestMessage(HttpMethod.Post, CatalogUrl)
{
    Content = new StringContent(filterBody, Encoding.UTF8, "application/json"),
};
req.Headers.Authorization = new AuthenticationHeaderValue("Bearer", catalogToken.Token);
req.Headers.Add("x-ms-user-agent", "AzureMachineLearningWorkspacePortal/12.0");

var resp = await http.SendAsync(req);
resp.EnsureSuccessStatusCode();
using var doc = JsonDocument.Parse(await resp.Content.ReadAsStringAsync());
var item  = doc.RootElement.GetProperty("value")[0];
var props = item.GetProperty("properties");

string entityId  = item.GetProperty("entityId").GetString()!;
string targetUrl = props.GetProperty("x-ms-runtime-urls")[0].GetString()!;

// Trigger operations
foreach (var op in props.GetProperty("x-ms-operations").EnumerateArray())
{
    if (op.TryGetProperty("x-ms-trigger", out var trig) && trig.ValueKind != JsonValueKind.Null)
        Console.WriteLine($"  {op.GetProperty("operationId").GetString(),-35} " +
                          $"trigger={trig.GetString(),-8} '{op.GetProperty("operationName").GetString()}'");
}

// Auth type
string authType = "None";
if (props.TryGetProperty("x-ms-connection-parameters", out var cp))
{
    foreach (var p in cp.EnumerateObject())
    {
        if (!p.Value.TryGetProperty("type", out var t)) continue;
        if (t.GetString() == "oauthSetting") { authType = "OAuth2";      break; }
        if (t.GetString() == "securestring") { authType = "CustomKeys";  break; }
    }
}
Console.WriteLine($"authType: {authType}");

// ── Step 5: create the project connection ──────────────────────────────────

var sub     = Environment.GetEnvironmentVariable("AZURE_SUBSCRIPTION_ID");
var rg      = Environment.GetEnvironmentVariable("AZURE_RESOURCE_GROUP");
var account = Environment.GetEnvironmentVariable("FOUNDRY_ACCOUNT_NAME");
var project = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_NAME");
var pat     = Environment.GetEnvironmentVariable("CONNECTOR_PAT") ?? "";
const string ConnName = "my-connector-conn";

var connUrl = $"https://management.azure.com/subscriptions/{sub}"
            + $"/resourceGroups/{rg}/providers/Microsoft.CognitiveServices"
            + $"/accounts/{account}/projects/{project}"
            + $"/connections/{ConnName}?api-version=2025-04-01-preview";

var metadata = new { type = "gateway_connector", toolEntityId = entityId,
                     connectionproperties = "{\"connectorName\":\"github\"}" };

object connBody = authType == "OAuth2"
    ? new { properties = new { authType = "OAuth2", category = "RemoteTool",
              connectorName = "github", target = targetUrl, credentials = new { },
              peRequirement = "NotRequired", metadata } }
    : new { properties = new { authType = "CustomKeys", category = "RemoteTool",
              connectorName = "github", target = targetUrl,
              credentials = new { keys = new { Authorization = $"Bearer {pat}" } },
              peRequirement = "NotRequired", metadata } };

using var putReq = new HttpRequestMessage(HttpMethod.Put, connUrl)
{
    Content = new StringContent(JsonSerializer.Serialize(connBody), Encoding.UTF8, "application/json"),
};
putReq.Headers.Authorization = new AuthenticationHeaderValue("Bearer", armToken.Token);
var putResp = await http.SendAsync(putReq);
putResp.EnsureSuccessStatusCode();
using var putDoc = JsonDocument.Parse(await putResp.Content.ReadAsStringAsync());
Console.WriteLine($"Connection '{ConnName}' created. " +
    $"Status: {putDoc.RootElement.GetProperty("properties").GetProperty("overallStatus").GetString()}");
// For OAuth2: open the Foundry portal and complete the OAuth consent flow.
```

After the connection is ready, use `ConnName` as `connection_id` and the trigger operation's `operationId` as `event_name` when you [create the routine](#event-based-triggers).

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();
const [catalogToken, armToken] = await Promise.all([
  credential.getToken("https://ai.azure.com/.default"),
  credential.getToken("https://management.azure.com/.default"),
]);

const CATALOG_URL = "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools";
const catalogHeaders = {
  Authorization: `Bearer ${catalogToken.token}`,
  "Content-Type": "application/json",
  "x-ms-user-agent": "AzureMachineLearningWorkspacePortal/12.0",
};

// ── Steps 2–4: fetch connector spec ────────────────────────────────────────

const connResp = await fetch(CATALOG_URL, {
  method: "POST",
  headers: catalogHeaders,
  body: JSON.stringify({
    freeTextSearch: "*",
    filters: [
      { field: "entityContainerId", operator: "eq", values: ["connectors-registry-prod-bl"] },
      { field: "type",              operator: "eq", values: ["tools"] },
      { field: "kind",              operator: "eq", values: ["Versioned"] },
      { field: "labels",            operator: "eq", values: ["latest"] },
      { field: "annotations/name",  operator: "eq", values: ["github"] },
    ],
    includeTotalResultCount: true,
    pageSize: 1,
    skip: 0,
  }),
});
const catalog = await connResp.json();
const item = catalog.value[0];

const entityId  = item.entityId;
const targetUrl = item.properties["x-ms-runtime-urls"][0];

// Trigger operations: x-ms-trigger is non-null
const triggerOps = (item.properties["x-ms-operations"] ?? [])
  .filter((op) => op["x-ms-trigger"] != null);
for (const op of triggerOps) {
  console.log(
    `  ${op.operationId.padEnd(35)} trigger=${op["x-ms-trigger"].padEnd(8)} '${op.operationName}'`
  );
}

// Auth type
const connParams = item.properties["x-ms-connection-parameters"] ?? {};
let authType = "None";
for (const param of Object.values(connParams)) {
  if (param.type === "oauthSetting") { authType = "OAuth2";     break; }
  if (param.type === "securestring") { authType = "CustomKeys"; break; }
}
console.log(`authType: ${authType}`);

// ── Step 5: create the project connection ──────────────────────────────────

const { AZURE_SUBSCRIPTION_ID: sub, AZURE_RESOURCE_GROUP: rg,
        FOUNDRY_ACCOUNT_NAME: account, FOUNDRY_PROJECT_NAME: project,
        CONNECTOR_PAT: pat } = process.env;
const connName = "my-connector-conn";

const connUrl =
  `https://management.azure.com/subscriptions/${sub}` +
  `/resourceGroups/${rg}/providers/Microsoft.CognitiveServices` +
  `/accounts/${account}/projects/${project}` +
  `/connections/${connName}?api-version=2025-04-01-preview`;

const metadata = {
  type: "gateway_connector",
  toolEntityId: entityId,
  connectionproperties: JSON.stringify({ connectorName: "github" }),
};

const connBody =
  authType === "OAuth2"
    ? { properties: { authType: "OAuth2", category: "RemoteTool",
          connectorName: "github", target: targetUrl,
          credentials: {}, peRequirement: "NotRequired", metadata } }
    : { properties: { authType: "CustomKeys", category: "RemoteTool",
          connectorName: "github", target: targetUrl,
          credentials: { keys: { Authorization: `Bearer ${pat}` } },
          peRequirement: "NotRequired", metadata } };

const putResp = await fetch(connUrl, {
  method: "PUT",
  headers: { Authorization: `Bearer ${armToken.token}`, "Content-Type": "application/json" },
  body: JSON.stringify(connBody),
});
if (!putResp.ok) throw new Error(await putResp.text());
const conn = await putResp.json();
console.log(`Connection '${connName}' created. Status: ${conn.properties.overallStatus}`);
// For OAuth2: open the Foundry portal and complete the OAuth consent flow.
```

After the connection is ready, use `connName` as `connection_id` and the trigger operation's `operationId` as `event_name` when you [create the routine](#event-based-triggers).

:::zone-end

## Prerequisites

- An active [Microsoft Foundry project](../../how-to/create-projects.md) with at least one agent deployed.
- **Foundry User** role or higher on the project scope.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

:::zone pivot="programming-language-python"

- Install the `azure-ai-projects` SDK (preview):

  ```bash
  pip install azure-ai-projects
  ```

- Install `azure-identity` for authentication:

  ```bash
  pip install azure-identity
  ```

:::zone-end

:::zone pivot="programming-language-csharp"

- Install the `Azure.AI.Projects` NuGet package (preview):

  ```bash
  dotnet add package Azure.AI.Projects --prerelease
  ```

:::zone-end

:::zone pivot="programming-language-javascript"

- Install the `@azure/ai-projects` npm package (preview):

  ```bash
  npm install @azure/ai-projects @azure/identity
  ```

:::zone-end

:::zone pivot="programming-language-rest"

- Install [curl](https://curl.se/) or any HTTP client.
- Install the [Azure CLI](/cli/azure/install-azure-cli) to acquire access tokens.

:::zone-end

## Create a routine

A routine definition specifies a trigger (when to fire) and an action (which agent to run and through which API). Exactly one trigger entry is supported in preview.

### Time-based triggers

#### Schedule trigger

A schedule trigger fires repeatedly on a cron expression. The service enforces a minimum interval of five minutes.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. In the left navigation, select **Routines**.
1. Select **+ New routine**.
1. Enter a **Name** for the routine, for example `daily-summary`.
1. Under **Trigger**, select **Schedule**.
1. Enter a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression), for example `0 7 * * 1-5` (07:00 UTC on weekdays).
1. Select a **Time zone** from the dropdown, for example **UTC**.
1. Under **Action**, select the action type (**Responses API** or **Invocations API**) and enter the required agent identifier.
1. Select **Create**.

> [!NOTE]
> If **Routines** isn't visible in the navigation, the feature isn't enabled for your region or subscription. Contact your account team to request access.

:::zone-end

:::zone pivot="programming-language-rest"

Replace the placeholder values, then run:

```bash
PROJECT_ENDPOINT=<your-project-endpoint>   # e.g. https://<account>.services.ai.azure.com/api/projects/<project>
AGENT_NAME=<your-agent-name>

TOKEN=$(az account get-access-token \
  --resource https://ai.azure.com \
  --query accessToken -o tsv)

# Using Responses API action
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/daily-summary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Runs a daily summary agent on weekday mornings.",
    "enabled": true,
    "triggers": {
      "weekday-morning": {
        "type": "schedule",
        "cron_expression": "0 7 * * 1-5",
        "time_zone": "UTC"
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'"
    }
  }'
```

To use the Invocations API action instead, replace the `action` object with the following. `agent_endpoint_id` is required; `session_id` is optional.

```bash
# Using Invocations API action
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/daily-summary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Runs a daily summary agent on weekday mornings.",
    "enabled": true,
    "triggers": {
      "weekday-morning": {
        "type": "schedule",
        "cron_expression": "0 7 * * 1-5",
        "time_zone": "UTC"
      }
    },
    "action": {
      "type": "invoke_agent_invocations_api",
      "agent_endpoint_id": "<your-agent-endpoint-id>"
    }
  }'
```

A successful response returns HTTP 200 or 201 with the routine object, including `created_at` and `updated_at` timestamps.

:::zone-end

:::zone pivot="programming-language-python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["PROJECT_ENDPOINT"]
agent_name = os.environ["AGENT_NAME"]

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

# Using Responses API action
routine = client.routines.create_or_update(
    routine_name="daily-summary",
    description="Runs a daily summary agent on weekday mornings.",
    enabled=True,
    triggers={
        "weekday-morning": {
            "type": "schedule",
            "cron_expression": "0 7 * * 1-5",  # required
            "time_zone": "UTC",                 # required
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,  # required: agent_name or agent_endpoint_id
        # "conversation_id": "...",  # optional
    },
)

print(f"Routine created: {routine.name}, enabled={routine.enabled}")

# To use the Invocations API action instead:
# action={
#     "type": "invoke_agent_invocations_api",
#     "agent_endpoint_id": os.environ["AGENT_ENDPOINT_ID"],  # required
#     # "session_id": "...",                                  # optional
# }
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
using Azure.AI.Projects;
using Azure.Identity;

var endpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var agentName = Environment.GetEnvironmentVariable("AGENT_NAME");

var client = new AIProjectClient(new Uri(endpoint), new DefaultAzureCredential());

// Using Responses API action
var routine = await client.GetRoutinesClient().CreateOrUpdateRoutineAsync(
    "daily-summary",
    new RoutineCreateOrUpdateRequest(
        triggers: new Dictionary<string, RoutineTrigger>
        {
            ["weekday-morning"] = new ScheduleRoutineTrigger(
                cronExpression: "0 7 * * 1-5",  // required
                timeZone: "UTC")                 // required
        },
        action: new InvokeAgentResponsesApiRoutineAction
        {
            AgentName = agentName,  // required: AgentName or AgentEndpointId
            // ConversationId = "...",  // optional
        })
    {
        Description = "Runs a daily summary agent on weekday mornings.",
        Enabled = true,
    });

Console.WriteLine($"Routine created: {routine.Value.Name}, enabled={routine.Value.Enabled}");

// To use the Invocations API action instead:
// action: new InvokeAgentInvocationsApiRoutineAction(agentEndpointId: "...")  // required
// {
//     SessionId = "..."  // optional
// }
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const { AIProjectClient } = require("@azure/ai-projects");
const { DefaultAzureCredential } = require("@azure/identity");

const endpoint = process.env.PROJECT_ENDPOINT;
const agentName = process.env.AGENT_NAME;

const client = new AIProjectClient(endpoint, new DefaultAzureCredential());

// Using Responses API action
const routine = await client.routines.createOrUpdate("daily-summary", {
  description: "Runs a daily summary agent on weekday mornings.",
  enabled: true,
  triggers: {
    "weekday-morning": {
      type: "schedule",
      cron_expression: "0 7 * * 1-5",  // required
      time_zone: "UTC",                 // required
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,  // required: agent_name or agent_endpoint_id
    // conversation_id: "...",  // optional
  },
});

console.log(`Routine created: ${routine.name}, enabled=${routine.enabled}`);

// To use the Invocations API action instead:
// action: {
//   type: "invoke_agent_invocations_api",
//   agent_endpoint_id: process.env.AGENT_ENDPOINT_ID,  // required
//   // session_id: "...",                               // optional
// }
```

:::zone-end

#### Timer trigger

A timer trigger fires once at a specific future date and time, or after a duration from now.

:::zone pivot="foundry-portal"

1. Follow steps 1â€“4 for creating a routine, and enter a name such as `once-on-release-day`.
1. Under **Trigger**, select **Timer**.
1. Enter the date and time in ISO 8601 format, for example `2026-09-01T09:00:00Z`, or a duration such as `PT2H` (two hours from now).
1. Optionally select a **Time zone** if you supply a local timestamp without a UTC offset.
1. Under **Action**, select the action type and enter the required agent identifier.
1. Select **Create**.

:::zone-end

:::zone pivot="programming-language-rest"

```bash
# Using Responses API action
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/once-on-release-day" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Runs the agent once on release day.",
    "enabled": true,
    "triggers": {
      "release-day": {
        "type": "timer",
        "at": "2026-09-01T09:00:00Z"
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'"
    }
  }'
```

The `at` field accepts:

- An ISO 8601 timestamp with an explicit UTC offset, for example `2026-09-01T09:00:00Z`.
- A local timestamp paired with `time_zone`, for example `"at": "2026-09-01T09:00:00", "time_zone": "America/Los_Angeles"`.
- A positive ISO 8601 duration from the current time, for example `PT2H` (fires two hours from now).

:::zone-end

:::zone pivot="programming-language-python"

```python
routine = client.routines.create_or_update(
    routine_name="once-on-release-day",
    description="Runs the agent once on release day.",
    enabled=True,
    triggers={
        "release-day": {
            "type": "timer",
            "at": "2026-09-01T09:00:00Z",  # required
            # "time_zone": "UTC",           # optional; required when 'at' has no UTC offset
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
var routine = await client.GetRoutinesClient().CreateOrUpdateRoutineAsync(
    "once-on-release-day",
    new RoutineCreateOrUpdateRequest(
        triggers: new Dictionary<string, RoutineTrigger>
        {
            ["release-day"] = new TimerRoutineTrigger(at: "2026-09-01T09:00:00Z")  // required
            {
                // TimeZone = "UTC",  // optional; required when 'at' has no UTC offset
            }
        },
        action: new InvokeAgentResponsesApiRoutineAction
        {
            AgentName = agentName,
        })
    {
        Description = "Runs the agent once on release day.",
        Enabled = true,
    });
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const routine = await client.routines.createOrUpdate("once-on-release-day", {
  description: "Runs the agent once on release day.",
  enabled: true,
  triggers: {
    "release-day": {
      type: "timer",
      at: "2026-09-01T09:00:00Z",  // required
      // time_zone: "UTC",          // optional; required when 'at' has no UTC offset
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,
  },
});
```

:::zone-end

### Event-based triggers

#### GitHub issue trigger

A GitHub issue trigger fires when an issue is opened or closed in a connected repository. The `connection_id` value is the name of a project connection that stores GitHub credentials.

**Before you begin:** Create a GitHub connection in your Foundry project. For full instructions on using the Foundry Tools Catalog to discover connectors and create project connections, see [Model Context Protocol (MCP)](tools/model-context-protocol.md).

:::zone pivot="foundry-portal"

1. Follow steps 1â€“4 for creating a routine, and enter a name such as `gh-issue-triage`.
1. Under **Trigger**, select **GitHub issue**.
1. Select the GitHub **Connection** you created in your project.
1. Enter the **Owner** (GitHub organization or user), for example `contoso`.
1. Enter the **Repository** name, for example `contoso-app`.
1. Select the **Issue event**: **Opened** or **Closed**.
1. Under **Action**, select the action type and enter the required agent identifier.
1. Select **Create**.

:::zone-end

:::zone pivot="programming-language-rest"

**Step 1: Create the GitHub project connection**

Use the Foundry Tools Catalog to find the GitHub connector and create a project connection. The connection name you choose becomes your `CONNECTION_ID`. For full instructions, see [Model Context Protocol (MCP)](tools/model-context-protocol.md).

**Step 2: Create the routine**

```bash
CONNECTION_ID=<your-github-connection-name>

# Using Responses API action
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/gh-issue-triage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Triages new GitHub issues with an agent.",
    "enabled": true,
    "triggers": {
      "new-issue": {
        "type": "github_issue",
        "connection_id": "'"$CONNECTION_ID"'",
        "owner": "contoso",
        "repository": "contoso-app",
        "issue_event": "opened"
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'"
    }
  }'
```

Set `"issue_event"` to `"closed"` to fire when issues are closed instead.

To use the Invocations API action instead, replace the `action` object:

```json
"action": {
  "type": "invoke_agent_invocations_api",
  "agent_endpoint_id": "<your-agent-endpoint-id>"
}
```

:::zone-end

:::zone pivot="programming-language-python"

```python
connection_id = os.environ["GITHUB_CONNECTION_NAME"]

# Using Responses API action
routine = client.routines.create_or_update(
    routine_name="gh-issue-triage",
    description="Triages new GitHub issues with an agent.",
    enabled=True,
    triggers={
        "new-issue": {
            "type": "github_issue",
            "connection_id": connection_id,  # required; max 256 characters
            "owner": "contoso",              # required; max 128 characters
            "repository": "contoso-app",     # required; max 128 characters
            "issue_event": "opened",         # required: "opened" or "closed"
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
var connectionId = Environment.GetEnvironmentVariable("GITHUB_CONNECTION_NAME");

var routine = await client.GetRoutinesClient().CreateOrUpdateRoutineAsync(
    "gh-issue-triage",
    new RoutineCreateOrUpdateRequest(
        triggers: new Dictionary<string, RoutineTrigger>
        {
            ["new-issue"] = new GitHubIssueRoutineTrigger(
                connectionId: connectionId,           // required; max 256 characters
                owner: "contoso",                     // required; max 128 characters
                repository: "contoso-app",            // required; max 128 characters
                issueEvent: GitHubIssueEvent.Opened)  // required: Opened or Closed
        },
        action: new InvokeAgentResponsesApiRoutineAction
        {
            AgentName = agentName,
        })
    {
        Description = "Triages new GitHub issues with an agent.",
        Enabled = true,
    });
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const connectionId = process.env.GITHUB_CONNECTION_NAME;

const routine = await client.routines.createOrUpdate("gh-issue-triage", {
  description: "Triages new GitHub issues with an agent.",
  enabled: true,
  triggers: {
    "new-issue": {
      type: "github_issue",
      connection_id: connectionId,  // required; max 256 characters
      owner: "contoso",             // required; max 128 characters
      repository: "contoso-app",    // required; max 128 characters
      issue_event: "opened",        // required: "opened" or "closed"
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,
  },
});
```

:::zone-end

#### Custom trigger

A custom trigger fires on a provider-specific event. The `provider` field identifies the event source, and the `parameters` field passes provider-specific configuration.

:::zone pivot="foundry-portal"

Custom triggers aren't configurable from the portal in v1 preview. Use the REST API or an SDK.

:::zone-end

:::zone pivot="programming-language-rest"

```bash
# Using Responses API action
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/custom-event-routine" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Fires on a custom provider event.",
    "enabled": true,
    "triggers": {
      "my-event": {
        "type": "custom",
        "provider": "my-provider",
        "event_name": "my-event-name",
        "parameters": {
          "key1": "value1"
        }
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'"
    }
  }'
```

:::zone-end

:::zone pivot="programming-language-python"

```python
routine = client.routines.create_or_update(
    routine_name="custom-event-routine",
    description="Fires on a custom provider event.",
    enabled=True,
    triggers={
        "my-event": {
            "type": "custom",
            "provider": "my-provider",        # required; max 128 characters
            "event_name": "my-event-name",    # optional; max 128 characters
            "parameters": {"key1": "value1"}, # required
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
var routine = await client.GetRoutinesClient().CreateOrUpdateRoutineAsync(
    "custom-event-routine",
    new RoutineCreateOrUpdateRequest(
        triggers: new Dictionary<string, RoutineTrigger>
        {
            ["my-event"] = new CustomRoutineTrigger(
                provider: "my-provider",                                       // required; max 128 characters
                parameters: new Dictionary<string, object> { ["key1"] = "value1" })  // required
            {
                EventName = "my-event-name",  // optional; max 128 characters
            }
        },
        action: new InvokeAgentResponsesApiRoutineAction
        {
            AgentName = agentName,
        })
    {
        Description = "Fires on a custom provider event.",
        Enabled = true,
    });
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const routine = await client.routines.createOrUpdate("custom-event-routine", {
  description: "Fires on a custom provider event.",
  enabled: true,
  triggers: {
    "my-event": {
      type: "custom",
      provider: "my-provider",        // required; max 128 characters
      event_name: "my-event-name",    // optional; max 128 characters
      parameters: { key1: "value1" }, // required
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,
  },
});
```

:::zone-end

## Action fields

Each routine specifies exactly one action. The two supported action types have different required and optional fields.

### Responses API action (`invoke_agent_responses_api`)

Invokes the agent through the Responses API. Exactly one of `agent_name` or `agent_endpoint_id` must be provided.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_responses_api"`. |
| `agent_name` | string | Conditional | The project-scoped agent name. Provide either `agent_name` or `agent_endpoint_id`. Maximum 256 characters. |
| `agent_endpoint_id` | string | Conditional | The endpoint-scoped agent identifier. Provide either `agent_name` or `agent_endpoint_id`. Maximum 256 characters. |
| `conversation_id` | string | No | An existing conversation to continue during the dispatch. Maximum 256 characters. |

### Invocations API action (`invoke_agent_invocations_api`)

Invokes the agent through the Invocations API. Requires the endpoint-scoped agent identifier.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_invocations_api"`. |
| `agent_endpoint_id` | string | Yes | The endpoint-scoped agent identifier. Maximum 256 characters. |
| `session_id` | string | No | An existing hosted-agent session to continue during the dispatch. Maximum 256 characters. |


## Enable and disable a routine

Routines start enabled if you set `"enabled": true` at creation. You can pause a routine without deleting it.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. Select **Routines** in the left navigation.
1. Find the routine and select it.
1. Toggle the **Enabled** switch to pause or resume the routine.

:::zone-end

:::zone pivot="programming-language-rest"

**Disable a routine:**

```bash
curl -sS -X POST "$PROJECT_ENDPOINT/routines/daily-summary:disable" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

**Enable a routine:**

```bash
curl -sS -X POST "$PROJECT_ENDPOINT/routines/daily-summary:enable" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

Both operations return the updated routine object.

:::zone-end

:::zone pivot="programming-language-python"

```python
# Disable
disabled_routine = client.routines.disable("daily-summary")
print(f"Enabled: {disabled_routine.enabled}")   # False

# Enable
enabled_routine = client.routines.enable("daily-summary")
print(f"Enabled: {enabled_routine.enabled}")    # True
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
// Disable
var disabled = await client.GetRoutinesClient().DisableRoutineAsync("daily-summary");
Console.WriteLine($"Enabled: {disabled.Value.Enabled}");   // False

// Enable
var enabled = await client.GetRoutinesClient().EnableRoutineAsync("daily-summary");
Console.WriteLine($"Enabled: {enabled.Value.Enabled}");    // True
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// Disable
const disabled = await client.routines.disable("daily-summary");
console.log(`Enabled: ${disabled.enabled}`);   // false

// Enable
const enabled = await client.routines.enable("daily-summary");
console.log(`Enabled: ${enabled.enabled}`);    // true
```

:::zone-end

## Test a routine manually

Use the `dispatch_async` operation to queue a one-off run without waiting for the trigger to fire. This lets you verify that the routine reaches your agent correctly.

The dispatch payload type must match the routine's action type. Use `invoke_agent_responses_api` for Responses API routines and `invoke_agent_invocations_api` for Invocations API routines.

| Payload field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must match the routine's action type: `"invoke_agent_responses_api"` or `"invoke_agent_invocations_api"`. |
| `input` | string | No | Override input sent to the downstream target for testing. Maximum 32,768 characters. |

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Run now**.
1. Optionally enter a test **Input message**.
1. Select **Dispatch**.

Foundry queues the run and opens the run history view. The new run appears with status **Queued** and progresses to **Dispatching** and then **Completed** or **Failed**.

:::zone-end

:::zone pivot="programming-language-rest"

**Responses API routine â€” with optional input override:**

```bash
curl -sS -X POST "$PROJECT_ENDPOINT/routines/daily-summary:dispatch_async" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "payload": {
      "type": "invoke_agent_responses_api",
      "input": "Run the daily summary for testing."
    }
  }'
```

**Invocations API routine â€” with optional input override:**

```bash
curl -sS -X POST "$PROJECT_ENDPOINT/routines/my-invocations-routine:dispatch_async" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "payload": {
      "type": "invoke_agent_invocations_api",
      "input": "Run the agent for testing."
    }
  }'
```

**Response:**

```json
{
  "dispatch_id": "disp-abc123",
  "action_correlation_id": "resp-xyz456",
  "task_id": "task-def789"
}
```

Use the `dispatch_id` to find the run in the run history.

**Without an input override:**

```bash
curl -sS -X POST "$PROJECT_ENDPOINT/routines/daily-summary:dispatch_async" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{}'
```

:::zone-end

:::zone pivot="programming-language-python"

```python
# Responses API routine
result = client.routines.dispatch_async(
    routine_name="daily-summary",
    payload={
        "type": "invoke_agent_responses_api",
        "input": "Run the daily summary for testing.",  # optional
    },
)
print(f"dispatch_id: {result.dispatch_id}")
print(f"task_id:     {result.task_id}")

# Invocations API routine
result2 = client.routines.dispatch_async(
    routine_name="my-invocations-routine",
    payload={
        "type": "invoke_agent_invocations_api",
        "input": "Run the agent for testing.",  # optional
    },
)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
// Responses API routine
var result = await client.GetRoutinesClient().DispatchRoutineAsync(
    "daily-summary",
    new DispatchRoutineRequest
    {
        Payload = new InvokeAgentResponsesApiDispatchPayload
        {
            Input = "Run the daily summary for testing.",  // optional
        },
    });
Console.WriteLine($"dispatch_id: {result.Value.DispatchId}");

// Invocations API routine
var result2 = await client.GetRoutinesClient().DispatchRoutineAsync(
    "my-invocations-routine",
    new DispatchRoutineRequest
    {
        Payload = new InvokeAgentInvocationsApiDispatchPayload
        {
            Input = "Run the agent for testing.",  // optional
        },
    });
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// Responses API routine
const result = await client.routines.dispatchAsync("daily-summary", {
  payload: {
    type: "invoke_agent_responses_api",
    input: "Run the daily summary for testing.",  // optional
  },
});
console.log(`dispatch_id: ${result.dispatch_id}`);

// Invocations API routine
const result2 = await client.routines.dispatchAsync("my-invocations-routine", {
  payload: {
    type: "invoke_agent_invocations_api",
    input: "Run the agent for testing.",  // optional
  },
});
```

:::zone-end

## View run history

Run history records every time a routine fired and the outcome of each attempt.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select the **Run history** tab.
1. Each row shows the trigger type, source (for example **schedule_delivery** or **manual_dispatch**), start time, end time, and phase (**completed** or **failed**).
1. Select a run to see detailed diagnostics including any error messages.

:::zone-end

:::zone pivot="programming-language-rest"

**List all runs for a routine:**

```bash
curl -sS "$PROJECT_ENDPOINT/routines/daily-summary/runs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

**Example response:**

```json
{
  "value": [
    {
      "id": "run-abc123",
      "status": "FINISHED",
      "phase": "completed",
      "trigger_type": "schedule",
      "attempt_source": "schedule_delivery",
      "started_at": "2026-06-02T07:00:05Z",
      "ended_at": "2026-06-02T07:00:42Z",
      "dispatch_id": "disp-abc123",
      "response_id": "resp-xyz456"
    }
  ]
}
```

:::zone-end

:::zone pivot="programming-language-python"

```python
runs = client.routines.list_runs("daily-summary")

for run in runs:
    print(
        f"{run.id}  phase={run.phase}  "
        f"source={run.attempt_source}  "
        f"started={run.started_at}  ended={run.ended_at}"
    )
    if run.phase == "failed":
        print(f"  error: {run.error_type} â€” {run.error_message}")
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
await foreach (var run in client.GetRoutinesClient().GetRunsAsync("daily-summary"))
{
    Console.WriteLine($"{run.Id}  phase={run.Phase}  source={run.AttemptSource}");
    if (run.Phase == RoutineRunPhase.Failed)
        Console.WriteLine($"  error: {run.ErrorType} â€” {run.ErrorMessage}");
}
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
for await (const run of client.routines.listRuns("daily-summary")) {
  console.log(`${run.id}  phase=${run.phase}  source=${run.attempt_source}`);
  if (run.phase === "failed") {
    console.log(`  error: ${run.error_type} â€” ${run.error_message}`);
  }
}
```

:::zone-end

## List and retrieve routines

:::zone pivot="foundry-portal"

All routines in your project are shown on the **Routines** page. Select any routine to see its configuration and run history.

:::zone-end

:::zone pivot="programming-language-rest"

**List all routines in the project:**

```bash
curl -sS "$PROJECT_ENDPOINT/routines" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

**Retrieve a specific routine:**

```bash
curl -sS "$PROJECT_ENDPOINT/routines/daily-summary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

:::zone-end

:::zone pivot="programming-language-python"

```python
# List all routines
for r in client.routines.list():
    print(f"{r.name}  enabled={r.enabled}  triggers={list(r.triggers.keys())}")

# Get a single routine
routine = client.routines.get("daily-summary")
print(routine)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
// List all routines
await foreach (var r in client.GetRoutinesClient().GetRoutinesAsync())
{
    Console.WriteLine($"{r.Name}  enabled={r.Enabled}");
}

// Get a single routine
var routine = await client.GetRoutinesClient().GetRoutineAsync("daily-summary");
Console.WriteLine(routine.Value);
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// List all routines
for await (const r of client.routines.list()) {
  console.log(`${r.name}  enabled=${r.enabled}`);
}

// Get a single routine
const routine = await client.routines.get("daily-summary");
console.log(routine);
```

:::zone-end

## Update a routine

To change a routine's trigger or action, issue a new create-or-update request with the same name. The operation replaces the stored definition.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Edit**.
1. Change the trigger or action settings.
1. Select **Save**.

:::zone-end

:::zone pivot="programming-language-rest"

Reissue the `PUT` request with the updated body. Include all fields; omitted fields reset to defaults.

```bash
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/daily-summary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Updated: runs at 08:00 UTC on weekdays.",
    "enabled": true,
    "triggers": {
      "weekday-morning": {
        "type": "schedule",
        "cron_expression": "0 8 * * 1-5",
        "time_zone": "UTC"
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'"
    }
  }'
```

:::zone-end

:::zone pivot="programming-language-python"

```python
updated = client.routines.create_or_update(
    routine_name="daily-summary",
    description="Updated: runs at 08:00 UTC on weekdays.",
    enabled=True,
    triggers={
        "weekday-morning": {
            "type": "schedule",
            "cron_expression": "0 8 * * 1-5",
            "time_zone": "UTC",
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
print(f"Updated at: {updated.updated_at}")
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
var updated = await client.GetRoutinesClient().CreateOrUpdateRoutineAsync(
    "daily-summary",
    new RoutineCreateOrUpdateRequest(
        triggers: new Dictionary<string, RoutineTrigger>
        {
            ["weekday-morning"] = new ScheduleRoutineTrigger("0 8 * * 1-5", "UTC"),
        },
        action: new InvokeAgentResponsesApiRoutineAction
        {
            AgentName = agentName,
        })
    {
        Description = "Updated: runs at 08:00 UTC on weekdays.",
        Enabled = true,
    });
Console.WriteLine($"Updated at: {updated.Value.UpdatedAt}");
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const updated = await client.routines.createOrUpdate("daily-summary", {
  description: "Updated: runs at 08:00 UTC on weekdays.",
  enabled: true,
  triggers: {
    "weekday-morning": {
      type: "schedule",
      cron_expression: "0 8 * * 1-5",
      time_zone: "UTC",
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,
  },
});
console.log(`Updated at: ${updated.updated_at}`);
```

:::zone-end

## Delete a routine

Deleting a routine removes it and stops all future trigger deliveries. Existing run records are preserved.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Delete**, then confirm.

:::zone-end

:::zone pivot="programming-language-rest"

```bash
curl -sS -X DELETE "$PROJECT_ENDPOINT/routines/daily-summary" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Foundry-Features: Routines=V1Preview"
```

A successful response returns HTTP 204 No Content.

:::zone-end

:::zone pivot="programming-language-python"

```python
client.routines.delete("daily-summary")
print("Routine deleted.")
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
await client.GetRoutinesClient().DeleteRoutineAsync("daily-summary");
Console.WriteLine("Routine deleted.");
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
await client.routines.delete("daily-summary");
console.log("Routine deleted.");
```

:::zone-end

## Trigger fields

### Schedule trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"schedule"`. |
| `cron_expression` | string | Yes | A 5-field cron expression. The service enforces a minimum interval of five minutes. |
| `time_zone` | string | Yes | An IANA or Windows time zone identifier, for example `"UTC"` or `"America/Los_Angeles"`. |

### Timer trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"timer"`. |
| `at` | string | Yes | A future timer expression. Accepts an ISO 8601 timestamp with an explicit UTC offset, a local timestamp paired with `time_zone`, or a positive ISO 8601 duration from now. |
| `time_zone` | string | No | An IANA or Windows time zone identifier. Required when `at` is a local timestamp without a UTC offset. |

### GitHub issue trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"github_issue"`. |
| `connection_id` | string | Yes | The project connection name that resolves the GitHub credentials. Maximum 256 characters. |
| `owner` | string | Yes | The GitHub owner or organization that scopes which issues can fire the trigger. Maximum 128 characters. |
| `repository` | string | Yes | The GitHub repository name. Maximum 128 characters. |
| `issue_event` | string | Yes | The event that fires the trigger: `"opened"` or `"closed"`. |

### Custom trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"custom"`. |
| `provider` | string | Yes | The provider or source identifier for the custom trigger. Maximum 128 characters. |
| `event_name` | string | No | An optional provider-specific event name. Maximum 128 characters. |
| `parameters` | object | Yes | Provider-specific parameters passed to the trigger. |

## Preview limitations

- In v1 preview, each routine supports exactly one trigger entry in the `triggers` map.
- The `custom` trigger type requires a provider configured in your subscription.
- GitHub issue triggers require a GitHub connection created in the project.

## Related content

- [Create a Foundry project](../../how-to/create-projects.md)
- [Create and configure agents](configure-agent.md)
- [Model Context Protocol (MCP)](tools/model-context-protocol.md)
- [Use toolboxes with agents](tools/toolbox.md)
