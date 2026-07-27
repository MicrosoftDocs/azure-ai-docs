---
title: "Automate agents with routines (preview)"
description: "Create, manage, and monitor routines that automatically trigger agents on a schedule or at a specific time in Microsoft Foundry."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 07/08/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
  - references_regions
  
ai-usage: ai-assisted
zone_pivot_groups: foundry-routines-config
---

# Automate agents with routines (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

A *routine* is a named automation rule that triggers an agent on a schedule or at a specific time. You define what fires the routine (the *trigger*) and what agent to invoke (the *action*). Foundry queues the invocation, runs the agent, and stores a run record you can inspect later.

This article shows you how to create, manage, and monitor routines by using the Foundry portal, the REST API, and the Python and JavaScript SDKs.

> [!NOTE]
> Routines are in preview. Send the `Foundry-Features: Routines=V1Preview` header on every REST call. All routine operations are on the data plane under your project endpoint.


## Supported trigger types

Routines support the following trigger types:

| Trigger type | Description |
|---|---|
| `schedule` | Recurring trigger defined by a cron expression. Minimum interval is five minutes. |
| `timer` | One-shot trigger that fires at a specific future date/time or after a duration. |
| `github_issue` | Event-based trigger that fires when an issue is opened or closed in a watched GitHub repository. |

## Supported action types

Each routine specifies exactly one action that runs when the routine fires. Two action types are supported:

| Action type | Description |
|---|---|
| `invoke_agent_responses_api` | Invokes the agent through the Responses API. Provide either the agent name or endpoint ID. |
| `invoke_agent_invocations_api` | Invokes the agent through the Invocations API. Requires the endpoint-scoped agent identifier. |

For required and optional fields of each action type, see [Action fields](#action-fields).

> [!NOTE]
> Routines can't invoke an agent that requires an end-user identity to be passed at run time. A routine runs unattended, so there's no signed-in user to delegate. Use routines only with agents that authenticate through their own configured identity, not on-behalf-of the caller.

## Prerequisites

- An active [Microsoft Foundry project](../../how-to/create-projects.md) with at least one agent deployed.
- **Foundry User** role or higher on the project scope.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

> [!NOTE]
> Routines are available in a subset of regions in preview. Confirm that your Foundry project is provisioned in one of the supported regions before you create a routine:
>
> - East US
> - East US 2
> - West US
> - West US 2
> - West Central US
> - North Central US
> - Sweden Central
> - Japan East

:::zone pivot="programming-language-python"

- Install the `azure-ai-projects` SDK, version 2.2.0 or later (preview):

  ```bash
  pip install "azure-ai-projects>=2.3.0"
  ```

  Version 2.2.0 introduces the duration shorthand (`"30m"`, `"2h"`) for timer triggers.

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

- Install `Azure.Identity` for authentication:

  ```bash
  dotnet add package Azure.Identity
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

:::zone pivot="azd"

- Install the [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd` 1.23.13 or later).
- Install the routines extension (preview):

  ```bash
  azd extension install azure.ai.routines
  ```

- Sign in and set your project endpoint:

  ```bash
  azd auth login
  export FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
  ```

:::zone-end

## Create a routine

A routine definition specifies a trigger (when to fire) and an action (which agent to run and through which API). The preview supports exactly one trigger entry.

### Schedule trigger

A schedule trigger fires repeatedly on a cron expression. The service enforces a minimum interval of five minutes.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. In the left navigation, select **Routines**.
1. Select **+ New routine**.
1. Enter a **Name** for the routine, such as `daily-summary`.
1. Select an **Agent** from the dropdown.
1. Enter a **Prompt** for the agent to run on each invocation.
1. Under **Trigger**, set **Type** to **Recurring schedule**, and then choose a **Frequency** (**Daily** or **Weekly**) and a **Time**.
1. Select **Create & start**.

   :::image type="content" source="../media/routines/routine-recurring-schedule.png" alt-text="Screenshot of the New routine dialog with the Recurring schedule trigger type selected, showing Frequency set to Daily and Time set to 9:00 AM." lightbox="../media/routines/routine-recurring-schedule.png":::

The portal interprets the **Time** in your browser's local time zone. To pin a routine to a specific time zone independently of the browser, create it through the REST API or an SDK and supply the `time_zone` field.

> [!NOTE]
> If **Routines** isn't visible in the navigation, the feature isn't enabled for your region or subscription. Contact your account team to request access.

:::zone-end

:::zone pivot="programming-language-rest"

Replace the placeholder values, and then run the command:

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
      "agent_name": "'"$AGENT_NAME"'",
      "input": "Summarize activity from the last 24 hours."
    }
  }'
```

To use the Invocations API action instead, replace the `action` object with the following. `agent_name` is required; `session_id` is optional.

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
      "agent_name": "'"$AGENT_NAME"'",
      "input": "Summarize activity from the last 24 hours."
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
routine = client.beta.routines.create_or_update(
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
        "agent_name": agent_name,  # required
        "input": "Summarize activity from the last 24 hours.",  # optional
        # "conversation_id": "...",  # optional
    },
)

print(f"Routine created: {routine.name}, enabled={routine.enabled}")

# To use the Invocations API action instead:
# action={
#     "type": "invoke_agent_invocations_api",
#     "agent_name": agent_name,  # required
#     # "session_id": "...",      # optional
# }
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var projectEndpoint = Environment.GetEnvironmentVariable("PROJECT_ENDPOINT");
var agentName = Environment.GetEnvironmentVariable("AGENT_NAME");

var projectClient = new AIProjectClient(new Uri(projectEndpoint), new DefaultAzureCredential());
var routinesClient = projectClient.Routines;

// Using Responses API action
var action = new AgentResponsesApiRoutineAction
{
    AgentName = agentName,
    Input = BinaryData.FromObjectAsJson("Summarize activity from the last 24 hours."),
};

var routineOptions = new ProjectsRoutineOptions(
    action: action,
    description: "Runs a daily summary agent on weekday mornings.",
    enabled: true);

routineOptions.Triggers.Add("weekday-morning", new ScheduleRoutineTrigger(
    cronExpression: "0 7 * * 1-5",  // required
    timeZone: "UTC"                  // required
));

ProjectsRoutine routine = await routinesClient.CreateOrUpdateAsync(
    name: "daily-summary",
    options: routineOptions);

Console.WriteLine($"Routine created: {routine.Name}, enabled={routine.IsEnabled}");

// To use the Invocations API action instead:
// var action = new AgentInvocationsApiRoutineAction
// {
//     AgentName = agentName,
//     // SessionId = "...",
// };
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
const routine = await client.beta.routines.createOrUpdate("daily-summary", {
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
    agent_name: agentName,  // required
    input: "Summarize activity from the last 24 hours.",  // optional
    // conversation_id: "...",  // optional
  },
});

console.log(`Routine created: ${routine.name}, enabled=${routine.enabled}`);

// To use the Invocations API action instead:
// action: {
//   type: "invoke_agent_invocations_api",
//   agent_name: agentName,  // required
//   // session_id: "...",    // optional
// }
```

:::zone-end

:::zone pivot="azd"

Inline `azd ai routine create --trigger schedule` isn't supported in preview. Create the routine from a YAML manifest instead:

```yaml
# routine.yaml
name: daily-summary
description: Runs a daily summary agent on weekday mornings.
enabled: true
triggers:
  weekday-morning:
    type: schedule
    cron: "0 7 * * 1-5"
    time_zone: UTC
action:
  type: invoke_agent_responses_api
  agent_name: <your-agent-name>
  input: Summarize activity from the last 24 hours.
```

```bash
azd ai routine create --file routine.yaml
```

The minimum interval between fires is five minutes. Set `time_zone` to any IANA zone (for example, `America/Los_Angeles`); omit it to interpret `cron` in UTC.

> [!NOTE]
> The agent referenced by `agent_name` must have a configured agent identity. The service rejects prompt-only agents when they're bound to a routine action.

:::zone-end

### Timer trigger

A timer trigger fires once at a specific future date and time, or after a duration from now.

:::zone pivot="foundry-portal"

1. Follow steps 1 through 6 in the previous procedure to open the **New routine** dialog and fill in **Name**, **Agent**, and **Prompt**. Use a name such as `once-on-release-day`.
1. Under **Trigger**, set **Type** to **One-time schedule**.
1. Under **Run at**, pick the date and time when the routine should fire.
1. Select **Create & start**.

   :::image type="content" source="../media/routines/routine-one-time-schedule.png" alt-text="Screenshot of the New routine dialog with the One-time schedule trigger type selected, showing a date picker and a time picker under Run at.":::

The **Run at** value is interpreted in your browser's local time zone. A one-time schedule fires exactly once, at the time you pick.

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
      "agent_name": "'"$AGENT_NAME"'",
      "input": "Run the release-day tasks."
    }
  }'
```

The `at` field accepts:

- An ISO 8601 timestamp with an explicit UTC offset, for example `"2026-06-01T09:00:00Z"`.
- A local timestamp paired with `time_zone`, for example `"at": "2026-09-01T09:00:00", "time_zone": "America/Los_Angeles"`.
- A positive duration from the current time, for example `"30m"` (30 minutes from now) or `"2h"` (two hours from now).

:::zone-end

:::zone pivot="programming-language-python"

```python
routine = client.beta.routines.create_or_update(
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
        "input": "Run the release-day tasks.",  # optional
    },
)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
var action = new AgentResponsesApiRoutineAction
{
    AgentName = agentName,
    Input = BinaryData.FromObjectAsJson("Run the release-day tasks."),
};

var routineOptions = new ProjectsRoutineOptions(
    action: action,
    description: "Runs the agent once on release day.",
    enabled: true);

routineOptions.Triggers.Add("release-day", new TimerRoutineTrigger(
    at: DateTimeOffset.Parse("2026-09-01T09:00:00Z")
));

ProjectsRoutine routine = await routinesClient.CreateOrUpdateAsync(
    name: "once-on-release-day",
    options: routineOptions);
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const routine = await client.beta.routines.createOrUpdate("once-on-release-day", {
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
    input: "Run the release-day tasks.",  // optional
  },
});
```

:::zone-end

:::zone pivot="azd"

Create a one-shot timer routine inline:

```bash
azd ai routine create once-on-release-day \
  --trigger timer \
  --at 2026-09-01T09:00:00Z \
  --action agent-response \
  --agent-name <your-agent-name>
```

Or create from a YAML manifest:

```yaml
# routine.yaml
name: once-on-release-day
description: Runs the agent once on release day.
enabled: true
triggers:
  release-day:
    type: timer
    time_zone: UTC
    at: 2026-09-01T09:00:00Z
action:
  type: invoke_agent_responses_api
  agent_name: <your-agent-name>
  input: Run the release-day tasks.
```

```bash
azd ai routine create --file routine.yaml
```

> [!NOTE]
> The agent referenced by `agent_name` must have a configured agent identity. The service rejects prompt-only agents when they're bound to a routine action.

:::zone-end

### Event-based triggers

An event-based trigger runs an agent when an external event occurs, such as a GitHub issue being opened. Event-based triggers rely on a connector connection that Foundry provisions in your account's connector namespace and uses to authenticate to the external system. The trigger references this connection by ID. For more about connector connections, see [Add managed MCP servers powered by connector namespaces](tools/connectors.md).

An event-based routine runs under the identity of the routine creator. The connection uses the routine creator's identity to authenticate with the external system, such as GitHub, so the routine watches and acts on that system with that person's access. If the routine creator loses access to the connected resource, the routine stops firing.

The preview supports the `github_issue` event-based trigger.

> [!IMPORTANT]
> Non-Microsoft tools including third-party MCP servers available in the Foundry Tools Catalog ("Third-Party Tools") are Non-Microsoft Products under your agreement governing use of Azure. When you connect to a Third-Party Tool, you do so at your own risk. You're responsible for any terms and charges for Third-Party Tools. Microsoft has no responsibility to you or others in relation to your use of Third-Party Tools. Carefully review and track the Third-Party Tools you add to your MCP client.
>
> Some of your information and data (such as authentication keys and prompt content) might be passed to the Third-Party Tool, or your MCP client might receive data from the Third-Party Tool. Review all data shared with Third-Party Tools and stay aware of third-party practices for data retention and location. You're responsible for managing whether your data flows outside your organization's Azure compliance and geographic boundaries.
>
> MCP implementations are vulnerable to attacks, cascading failures, and loss of human oversight. To mitigate these risks, vet MCP servers for security and reliability, follow Microsoft's recommendations and industry best practices, and implement approval mechanisms to monitor cascading behaviors.

#### GitHub issue trigger

A `github_issue` trigger fires when an issue is opened or closed in a watched GitHub repository. When the trigger fires, Foundry forwards the GitHub issue payload to the agent as its input, so the agent can triage or act on the issue.

:::image type="content" source="../media/routines/routine-github-trigger.png" alt-text="Screenshot showing the New routine dialog in the Foundry portal with a GitHub issue trigger selected, displaying fields for repository owner and repository name.":::

The trigger relies on a GitHub connector connection. Foundry provisions the connection to GitHub in your account's connector namespace and authenticates to GitHub through it. The `connection_id` you set on the trigger references this connection. Each tab shows how to create the connection and the routine that uses it. For more about connector connections, see [Add managed MCP servers powered by connector namespaces](tools/connectors.md).

The `issue_event` field accepts `opened` or `closed` only.

:::zone pivot="foundry-portal"

To connect GitHub in the portal, follow the portal steps in [Add managed MCP servers powered by connector namespaces](tools/connectors.md?pivots=foundry-portal). After the connection exists, create the routine that references it through the REST API, an SDK, or the Azure Developer CLI, as shown in the other tabs.

:::zone-end

:::zone pivot="programming-language-rest"

First create the GitHub connector connection, then reference it by name in the trigger's `connection_id` field.

**Step 1: Acquire tokens.** You need a catalog token to discover the connector and an Azure Resource Manager token to create the connection.

```bash
CATALOG_TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
ARM_TOKEN=$(az account get-access-token --resource https://management.azure.com --query accessToken -o tsv)
```

**Step 2: Discover the GitHub connector** to get its `entityId`. The catalog is served from `eastus` regardless of your project's region.

```bash
RESPONSE=$(curl -sS -X POST "https://eastus.api.azureml.ms/asset-gallery/v1.0/tools" \
  -H "Authorization: Bearer $CATALOG_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": [
      { "field": "type",             "operator": "eq", "values": ["tools"] },
      { "field": "annotations/name", "operator": "eq", "values": ["github"] }
    ],
    "pageSize": 1
  }')
ENTITY_ID=$(echo "$RESPONSE" | jq -r '.value[0].entityId')
```

**Step 3: Create the project connection.** Set `target` to the literal `https://placeholder`; the platform rewrites it after consent.

```bash
SUBSCRIPTION_ID=<your-subscription-id>
RESOURCE_GROUP=<your-resource-group>
ACCOUNT_NAME=<your-foundry-account-name>
PROJECT_NAME=<your-project-name>
CONNECTION_NAME=github-conn

CONNECTION_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.CognitiveServices/accounts/$ACCOUNT_NAME/projects/$PROJECT_NAME/connections/$CONNECTION_NAME?api-version=2025-04-01-preview"

curl -sS -X PUT "$CONNECTION_URL" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "authType": "OAuth2",
      "category": "RemoteTool",
      "connectorName": "github",
      "target": "https://placeholder",
      "metadata": {
        "type": "gateway_connector",
        "toolEntityId": "'"$ENTITY_ID"'"
      }
    }
  }'
```

**Step 4: Authorize GitHub.** Get a one-time OAuth consent link, then open it in a browser and sign in to GitHub.

```bash
CALLER_OID=$(az ad signed-in-user show --query id -o tsv)
CALLER_TID=$(az account show --query tenantId -o tsv)

curl -sS -X POST "$CONNECTION_URL&action=listConsentLinks" \
  -H "Authorization: Bearer $ARM_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": [{
      "objectId":      "'"$CALLER_OID"'",
      "parameterName": "token",
      "redirectUrl":   "https://ai.azure.com/nextgen/authConsentPopup",
      "tenantId":      "'"$CALLER_TID"'"
    }]
  }' | jq -r '.value[0].link'
```

For the complete connector reference, see [Add managed MCP servers powered by connector namespaces](tools/connectors.md).

**Step 5: Create the routine** that references the connection by name.

```bash
curl -sS -X PUT "$PROJECT_ENDPOINT/routines/on-issue-opened" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: Routines=V1Preview" \
  -d '{
    "description": "Triages a GitHub issue when it is opened in the watched repository.",
    "enabled": true,
    "triggers": {
      "on-issue": {
        "type": "github_issue",
        "connection_id": "github-conn",
        "owner": "your-org",
        "repository": "your-repo",
        "issue_event": "opened"
      }
    },
    "action": {
      "type": "invoke_agent_responses_api",
      "agent_name": "'"$AGENT_NAME"'",
      "input": "Triage this GitHub issue."
    }
  }'
```

> [!NOTE]
> For a `github_issue` trigger, the GitHub issue payload overwrites `action.input`. When an issue event fires the routine, Foundry replaces the `input` value with the issue payload. The `input` you set applies only to manual test dispatches.

:::zone-end

:::zone pivot="programming-language-python"

The Python SDK creates the routine but not the GitHub connector connection. Create the connection first in the [Foundry portal](tools/connectors.md?pivots=foundry-portal), with the [REST API](tools/connectors.md?pivots=programming-language-rest), or with the [Azure Developer CLI](tools/connectors.md?pivots=azd), then reference it by name in the trigger's `connection_id` field.

```python
routine = client.beta.routines.create_or_update(
    routine_name="on-issue-opened",
    description="Triages a GitHub issue when it is opened in the watched repository.",
    enabled=True,
    triggers={
        "on-issue": {
            "type": "github_issue",
            "connection_id": "github-conn",  # required: project connection to GitHub
            "owner": "your-org",              # required
            "repository": "your-repo",        # required
            "issue_event": "opened",          # required: "opened" or "closed"
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
        "input": "Triage this GitHub issue.",  # optional; omitted when the issue payload is present
    },
)
```

> [!NOTE]
> For a `github_issue` trigger, the GitHub issue payload overwrites `action.input`. When an issue event fires the routine, Foundry replaces the `input` value with the issue payload. The `input` you set applies only to manual test dispatches.

:::zone-end

:::zone pivot="programming-language-csharp"

The C# SDK creates the routine but not the GitHub connector connection. Create the connection first in the [Foundry portal](tools/connectors.md?pivots=foundry-portal), with the [REST API](tools/connectors.md?pivots=programming-language-rest), or with the [Azure Developer CLI](tools/connectors.md?pivots=azd). Then reference it by name in the trigger's `ConnectionId` property.

```csharp
var action = new AgentResponsesApiRoutineAction
{
    AgentName = agentName,
    Input = BinaryData.FromObjectAsJson("Triage this GitHub issue."),  // optional; omitted when the issue payload is present
};

var routineOptions = new ProjectsRoutineOptions(
    action: action,
    description: "Triages a GitHub issue when it is opened in the watched repository.",
    enabled: true);

routineOptions.Triggers.Add("on-issue", new GitHubIssueRoutineTrigger(
    connectionId: "github-conn",      // required: project connection to GitHub
    owner: "your-org",                 // required
    repository: "your-repo",           // required
    issueEvent: GitHubIssueEvent.Opened  // required: Opened or Closed
));

ProjectsRoutine routine = await routinesClient.CreateOrUpdateAsync(
    name: "on-issue-opened",
    options: routineOptions);
```

> [!NOTE]
> For a `github_issue` trigger, the GitHub issue payload overwrites `action.Input`. When an issue event fires the routine, Foundry replaces the `Input` value with the issue payload. The `Input` you set applies only to manual test dispatches.

:::zone-end

:::zone pivot="programming-language-javascript"

The JavaScript SDK creates the routine but not the GitHub connector connection. Create the connection first in the [Foundry portal](tools/connectors.md?pivots=foundry-portal), with the [REST API](tools/connectors.md?pivots=programming-language-rest), or with the [Azure Developer CLI](tools/connectors.md?pivots=azd), then reference it by name in the trigger's `connection_id` field.

```javascript
const routine = await client.beta.routines.createOrUpdate("on-issue-opened", {
  description: "Triages a GitHub issue when it is opened in the watched repository.",
  enabled: true,
  triggers: {
    "on-issue": {
      type: "github_issue",
      connection_id: "github-conn",  // required: project connection to GitHub
      owner: "your-org",             // required
      repository: "your-repo",       // required
      issue_event: "opened",         // required: "opened" or "closed"
    },
  },
  action: {
    type: "invoke_agent_responses_api",
    agent_name: agentName,
    input: "Triage this GitHub issue.",  // optional; omitted when the issue payload is present
  },
});
```

> [!NOTE]
> For a `github_issue` trigger, the GitHub issue payload overwrites `action.input`. When an issue event fires the routine, Foundry replaces the `input` value with the issue payload. The `input` you set applies only to manual test dispatches.

:::zone-end

:::zone pivot="azd"

### Step 1: Create the GitHub OAuth2 connection

Before you can create a GitHub issue routine, register the GitHub connector as a project connection. Use `azd ai connection create` with `--connector-name github`:

```bash
azd ai connection create github-conn \
  --connector-name github
```

### Step 2: Complete OAuth consent

The connection is created in an `Unauthenticated` state. Retrieve the consent URL and open it in a browser:

```bash
azd ai connection show github-conn
```

Sign in to GitHub once and authorize the application. After consent is recorded, `overallStatus` transitions to `Connected`.

### Step 3: Create the routine

Reference the connection by name in the routine's `connection_id`. Create the routine inline:

```bash
azd ai routine create on-issue-opened \
  --trigger github-issue \
  --owner your-org \
  --repository your-repo \
  --issue-event opened \
  --connection-id github-conn \
  --agent-name <your-agent-name>
```

Or create it from a YAML manifest:

```yaml
# routine.yaml
name: on-issue-opened
description: Triages a GitHub issue when it is opened in the watched repository.
enabled: true
triggers:
  on-issue:
    type: github_issue
    connection_id: github-conn
    owner: your-org
    repository: your-repo
    issue_event: opened
action:
  type: invoke_agent_responses_api
  agent_name: <your-agent-name>
```

```bash
azd ai routine create on-issue-opened --file routine.yaml
```

> [!NOTE]
> The agent referenced by `agent_name` must have a configured agent identity. The service rejects prompt-only agents when they're bound to a routine action.

:::zone-end

## Action fields

Each routine specifies exactly one action. The two supported action types have different required and optional fields.

### Responses API action (`invoke_agent_responses_api`)

Invokes the agent through the Responses API.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_responses_api"`. |
| `agent_name` | string | Yes | The project-scoped agent name. Maximum 256 characters. |
| `input` | string | No | The input passed to the agent. For a `github_issue` trigger, the GitHub issue payload overwrites this value when an event fires, so it applies only to manual test dispatches. |
| `conversation_id` | string | No | An existing conversation to continue during the dispatch. Maximum 256 characters. |

### Invocations API action (`invoke_agent_invocations_api`)

Invokes the agent through the Invocations API.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_invocations_api"`. |
| `agent_name` | string | Yes | The project-scoped agent name. Maximum 256 characters. |
| `input` | string | No | The input passed to the agent. For a `github_issue` trigger, the GitHub issue payload overwrites this value when an event fires, so it applies only to manual test dispatches. |
| `session_id` | string | No | An existing hosted-agent session to continue during the dispatch. Maximum 256 characters. |


## Enable and disable a routine

Routines start enabled if you set `"enabled": true` at creation. You can pause a routine without deleting it.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. Select **Routines** in the left navigation.
1. Find the routine and select it.
1. Select **Pause** in the top right to pause the routine, or select **Resume** to re-enable a paused routine.

   :::image type="content" source="../media/routines/routine-detail-actions.png" alt-text="Screenshot of a routine detail page showing the Pause button in the top right, the overflow menu with Test run, Edit, and Delete options, and the table of past runs below." lightbox="../media/routines/routine-detail-actions.png":::

From the same page, you can also:

- Select **Test run** (either the button on the right or the entry in the overflow menu) to fire the routine immediately with its current prompt and agent, without waiting for the next scheduled trigger.
- Review past runs in the table below the routine details. Each row shows the response ID, when the run was triggered, its duration, and its state. Use the **Last day**, **7D**, **1M**, or **Custom** filters to scope the time range. Select a response ID to open the full run.

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
disabled_routine = client.beta.routines.disable("daily-summary")
print(f"Enabled: {disabled_routine.enabled}")   # False

# Enable
enabled_routine = client.beta.routines.enable("daily-summary")
print(f"Enabled: {enabled_routine.enabled}")    # True
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
// Disable
ProjectsRoutine disabled = await routinesClient.DisableAsync("daily-summary");
Console.WriteLine($"Enabled: {disabled.IsEnabled}");   // false

// Enable
ProjectsRoutine enabled = await routinesClient.EnableAsync("daily-summary");
Console.WriteLine($"Enabled: {enabled.IsEnabled}");    // true
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// Disable
const disabled = await client.beta.routines.disable("daily-summary");
console.log(`Enabled: ${disabled.enabled}`);   // false

// Enable
const enabled = await client.beta.routines.enable("daily-summary");
console.log(`Enabled: ${enabled.enabled}`);    // true
```

:::zone-end

:::zone pivot="azd"

```bash
# Disable
azd ai routine disable once-on-release-day

# Enable
azd ai routine enable once-on-release-day
```

:::zone-end

## Test a routine manually

Queue a one-off run without waiting for the trigger to fire. This step lets you verify that the routine reaches your agent correctly.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Test run** (either the button on the right or the entry in the overflow menu next to **Pause**).

Foundry queues the run immediately with the routine's current agent and prompt. The new run appears in the past-runs table below the routine details and progresses from **Queued** to **Completed** or **Failed**.

:::zone-end

:::zone pivot="programming-language-rest"

Use the `dispatch_async` operation to queue the run. The dispatch payload type must match the routine's action type: use `invoke_agent_responses_api` for Responses API routines and `invoke_agent_invocations_api` for Invocations API routines.

| Payload field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must match the routine's action type: `"invoke_agent_responses_api"` or `"invoke_agent_invocations_api"`. |
| `input` | string | No | Override input sent to the downstream target for testing. Maximum 32,768 characters. |

**Responses API routine – with optional input override:**

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

**Invocations API routine – with optional input override:**

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
result = client.beta.routines.dispatch(
    routine_name="daily-summary",
    payload={
        "type": "invoke_agent_responses_api",
        "input": "Run the daily summary for testing.",  # optional
    },
)
print(f"dispatch_id: {result.dispatch_id}")
print(f"task_id:     {result.task_id}")

# Invocations API routine
result2 = client.beta.routines.dispatch(
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
var payload = new AgentResponsesApiRoutineDispatch
{
    Input = BinaryData.FromObjectAsJson("Run the daily summary for testing."),  // optional
};

RoutineDispatchResult result = await routinesClient.DispatchAsync(
    name: "daily-summary",
    payload: payload);

Console.WriteLine($"dispatch_id: {result.DispatchId}");
Console.WriteLine($"task_id:     {result.TaskId}");

// Invocations API routine
var payload2 = new AgentInvocationsApiRoutineDispatch
{
    Input = BinaryData.FromObjectAsJson("Run the agent for testing."),  // optional
};

RoutineDispatchResult result2 = await routinesClient.DispatchAsync(
    name: "my-invocations-routine",
    payload: payload2);
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// Responses API routine
const result = await client.beta.routines.dispatch("daily-summary", {
  payload: {
    type: "invoke_agent_responses_api",
    input: "Run the daily summary for testing.",  // optional
  },
});
console.log(`dispatch_id: ${result.dispatch_id}`);

// Invocations API routine
const result2 = await client.beta.routines.dispatch("my-invocations-routine", {
  payload: {
    type: "invoke_agent_invocations_api",
    input: "Run the agent for testing.",  // optional
  },
});
```

:::zone-end

:::zone pivot="azd"

Queue a manual run for a Responses API routine:

```bash
azd ai routine dispatch once-on-release-day \
  --input "Run the routine for testing."
```

The command prints the `dispatch_id` and `task_id`. Use the `dispatch_id` to find the run in the run history.

:::zone-end

## View run history

Run history records every time a routine fires and the outcome of each attempt.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. The table on the routine detail page lists past runs. Each row shows the response ID, when the run triggered, its duration, and its state (for example **Completed** or **Failed**).
1. Use the **Last day**, **7D**, **1M**, or **Custom** range controls above the table to filter the time window.
1. Select a response ID to open the full run, including the response and any error details.

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
runs = client.beta.routines.list_runs("daily-summary")

for run in runs:
    print(
        f"{run.id}  phase={run.phase}  "
        f"source={run.attempt_source}  "
        f"started={run.started_at}  ended={run.ended_at}"
    )
    if run.phase == "failed":
        print(f"  error: {run.error_type} - {run.error_message}")
```


:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
await foreach (RoutineRun run in routinesClient.GetRoutineRunsAsync("daily-summary"))
{
    Console.WriteLine($"{run.Id}  phase={run.Phase}  source={run.AttemptSource}  started={run.StartedAt}");
    if (run.Phase == RoutineRunPhase.Failed)
    {
        Console.WriteLine($"  error: {run.ErrorType} — {run.ErrorMessage}");
    }
}
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
for await (const run of client.beta.routines.listRuns("daily-summary")) {
  console.log(`${run.id}  phase=${run.phase}  source=${run.attempt_source}`);
  if (run.phase === "failed") {
    console.log(`  error: ${run.error_type} - ${run.error_message}`);
  }
}
```

:::zone-end

:::zone pivot="azd"

Listing run history through `azd ai routine` isn't supported in preview. Use the Foundry portal, REST API, or an SDK to retrieve runs.

:::zone-end

## List and retrieve routines

:::zone pivot="foundry-portal"

The **Routines** page shows all routines in your project. Select any routine to see its configuration and run history.

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
for r in client.beta.routines.list():
    print(f"{r.name}  enabled={r.enabled}  triggers={list(r.triggers.keys())}")

# Get a single routine
routine = client.beta.routines.get("daily-summary")
print(routine)
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
// List all routines
await foreach (ProjectsRoutine r in routinesClient.GetRoutinesAsync())
{
    Console.WriteLine($"{r.Name}  enabled={r.IsEnabled}  triggers={string.Join(", ", r.Triggers.Keys)}");
}

// Get a single routine
ProjectsRoutine routine = await routinesClient.GetAsync("daily-summary");
Console.WriteLine(routine);
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
// List all routines
for await (const r of client.beta.routines.list()) {
  console.log(`${r.name}  enabled=${r.enabled}`);
}

// Get a single routine
const routine = await client.beta.routines.get("daily-summary");
console.log(routine);
```

:::zone-end

:::zone pivot="azd"

Retrieve a single routine:

```bash
azd ai routine show once-on-release-day
```

Listing all routines through `azd ai routine` isn't supported in preview. Use the Foundry portal, REST API, or an SDK.

:::zone-end

## Update a routine

To change a routine's trigger or action, send a new create-or-update request with the same name. This operation replaces the stored definition.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Edit**.
1. Change the trigger or action settings.
1. Select **Save**.

:::zone-end

:::zone pivot="programming-language-rest"

Reissue the `PUT` request with the updated body. Include all fields. Omitted fields reset to defaults.

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
updated = client.beta.routines.create_or_update(
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
var action = new AgentResponsesApiRoutineAction { AgentName = agentName };

var routineOptions = new ProjectsRoutineOptions(
    action: action,
    description: "Updated: runs at 08:00 UTC on weekdays.",
    enabled: true);

routineOptions.Triggers.Add("weekday-morning", new ScheduleRoutineTrigger(
    cronExpression: "0 8 * * 1-5",
    timeZone: "UTC"
));

ProjectsRoutine updated = await routinesClient.CreateOrUpdateAsync(
    name: "daily-summary",
    options: routineOptions);

Console.WriteLine($"Updated at: {updated.UpdatedAt}");
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
const updated = await client.beta.routines.createOrUpdate("daily-summary", {
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

:::zone pivot="azd"

Apply changes from a YAML manifest:

```bash
azd ai routine update once-on-release-day --file routine.yaml
```

The `--description` flag isn't supported for timer routines in preview. Edit the manifest and reapply it by using `--file` instead.

:::zone-end

## Delete a routine

When you delete a routine, you remove it and stop all future trigger deliveries. The process preserves existing run records.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Delete**, and then confirm.

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
client.beta.routines.delete("daily-summary")
print("Routine deleted.")
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
await routinesClient.DeleteAsync("daily-summary");
Console.WriteLine("Routine deleted.");
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
await client.beta.routines.delete("daily-summary");
console.log("Routine deleted.");
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai routine delete once-on-release-day
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
| `at` | string | Yes | A future timer expression. Accepts an ISO 8601 timestamp with an explicit UTC offset (for example, `"2026-06-01T09:00:00Z"`), a local timestamp paired with `time_zone`, or a positive duration from now (for example, `"30m"` or `"2h"`). |
| `time_zone` | string | No | An IANA or Windows time zone identifier. Required when `at` is a local timestamp without a UTC offset. |

### GitHub issue trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"github_issue"`. |
| `connection_id` | string | Yes | The project connection that authenticates to GitHub. Maximum 256 characters. |
| `owner` | string | Yes | The GitHub owner or organization that scopes which issues can fire the trigger. Maximum 128 characters. |
| `repository` | string | Yes | The GitHub repository that scopes which issues can fire the trigger. Maximum 128 characters. |
| `issue_event` | string | Yes | The GitHub issue event that fires the routine. Supported values: `opened`, `closed`. |

## Dispatch behavior and retry policy

When a trigger fires or you call `:dispatch_async` manually, Foundry acknowledges that the run was enqueued. The acknowledgment doesn't mean the downstream agent call finished. Use the run state, telemetry, or the returned `dispatch_id` to confirm completion.

### Downstream call outcomes

The delivery worker waits for the downstream `invoke_agent_responses_api` or `invoke_agent_invocations_api` HTTP call to finish before marking the run.

| Downstream HTTP result | Routine run behavior |
|---|---|
| 2xx | Run is marked completed and downstream dispatch identifiers are recorded. |
| 408, 429, or 5xx | Treated as retryable while attempts remain. |
| Other 4xx (for example, 400) | Treated as terminal and the run is marked failed. |
| Request timeout or transient service-invocation failure | Treated as retryable while attempts remain. |

If retries are exhausted, the run is marked failed with the last dispatch error.

A successful run means the downstream API accepted the dispatch request. It doesn't guarantee that asynchronous work started by the agent has completed.

### Retry and timeout defaults

- The default delivery policy is three total attempts with exponential backoff starting at 1 second and capped at 5 seconds.
- The downstream HTTP request has a per-attempt timeout of 30 seconds. Queueing time, retry backoff, and worker concurrency limits aren't included in that per-request timeout.

## Let an agent schedule its own reminders

Routines let an external trigger start an agent. A hosted agent can also schedule *itself* to run again at a future time by calling the built-in `reminder_preview` toolbox tool. Use this pattern when the agent decides during a run that it needs to follow up later, such as to check back on a long-running task.

> [!NOTE]
> The reminder tool is available only for hosted agents. You can't use the reminder tool with prompt agents.

When the agent calls the reminder tool, it specifies a delay in minutes. After that delay, Foundry re-invokes the same agent on the same conversation. The agent can then continue its work or check on external systems.

For full setup instructions, usage examples, and how reminders differ from routines, see [Reminder tool for self-scheduling agents](tools/reminder-tool.md).

## Known issues and limitations

This preview has the following known issues and limitations:

- **One trigger and one action per routine.** Each routine supports exactly one entry in the `triggers` map and one action. To run multiple agents or multiple schedules, create separate routines.
- **Trigger types.** The supported triggers are `timer` (one-shot), `schedule` (cron-based recurring), and `github_issue` (event-based). The agent-scheduled [reminder tool](tools/reminder-tool.md) is available only for hosted agents.
- **Action types.** The only action is invoking one Foundry agent through the Responses API or Invocations API.
- **Schedule minimum interval.** A `schedule` trigger fires at most once every five minutes. Cron expressions that resolve to a shorter interval are rejected.
- **Regional availability.** Routines are available only in the regions listed under [Prerequisites](#prerequisites). If you don't see **Routines** in the Foundry portal navigation, the feature isn't enabled for your region or subscription.
- **Use `:dispatch_async` for manual dispatch.** Only the `POST .../routines/{routineName}:dispatch_async` route is part of the public contract. The legacy `:dispatch` route isn't supported for customer use.
- **Acknowledgment isn't completion.** A `:dispatch_async` response acknowledges that the run was enqueued, not that the downstream agent call finished. Use the run state, telemetry, or the returned `dispatch_id` to observe final delivery.
- **Per-attempt timeout.** The downstream HTTP request to the agent has a per-attempt timeout of 30 seconds. Queueing time, retry backoff, message-bus delivery time, and worker concurrency limits aren't included in that timeout. Requests that exceed the per-attempt timeout are retried per the [retry and timeout defaults](#retry-and-timeout-defaults). The routine run is marked failed if all attempts time out.
- **Successful delivery doesn't guarantee end-to-end completion.** A completed routine run means the downstream API returned success for the dispatch request. It doesn't guarantee that asynchronous work started by the agent has finished.

## Related content

- [Create a Foundry project](../../how-to/create-projects.md)
- [Create and configure agents](configure-agent.md)
- [Model Context Protocol (MCP)](tools/model-context-protocol.md)
- [Use toolboxes with agents](tools/toolbox.md)
