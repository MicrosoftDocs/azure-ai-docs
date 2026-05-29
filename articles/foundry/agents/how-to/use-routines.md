---
title: "Automate agents with routines (preview)"
description: "Create, manage, and monitor routines that automatically trigger agents on a schedule or at a specific time in Microsoft Foundry."
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

A *routine* is a named automation rule that triggers an agent on a schedule or at a specific time. You define what fires the routine (the *trigger*) and what agent to invoke (the *action*). Foundry queues the invocation, runs the agent, and stores a run record you can inspect later.

This article shows you how to create, manage, and monitor routines by using the Foundry portal, the REST API, and the Python, C#, and JavaScript SDKs.

> [!NOTE]
> Routines are in preview. Send the `Foundry-Features: Routines=V1Preview` header on every REST call. All routine operations are on the data plane under your project endpoint.


## Supported trigger types

Routines support two time-based trigger types:

| Trigger type | Description |
|---|---|
| `schedule` | Recurring trigger defined by a cron expression. Minimum interval is five minutes. |
| `timer` | One-shot trigger that fires at a specific future date/time or after a duration. |

## Supported action types

Each routine specifies exactly one action that runs when the routine fires. Two action types are supported:

| Action type | Description |
|---|---|
| `invoke_agent_responses_api` | Invokes the agent through the Responses API. Provide either the agent name or endpoint ID. |
| `invoke_agent_invocations_api` | Invokes the agent through the Invocations API. Requires the endpoint-scoped agent identifier. |

For required and optional fields of each action type, see [Action fields](#action-fields).

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
  pip install "azure-ai-projects>=2.2.0"
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
  export AZURE_AI_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
  ```

:::zone-end

## Create a routine

A routine definition specifies a trigger (when to fire) and an action (which agent to run and through which API). Exactly one trigger entry is supported in preview.

### Schedule trigger

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
      "agent_name": "'"$AGENT_NAME"'"
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
        "agent_name": agent_name,  # required
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
            AgentName = agentName,  // required
            // ConversationId = "...",  // optional
        })
    {
        Description = "Runs a daily summary agent on weekday mornings.",
        Enabled = true,
    });

Console.WriteLine($"Routine created: {routine.Value.Name}, enabled={routine.Value.Enabled}");

// To use the Invocations API action instead:
// action: new InvokeAgentInvocationsApiRoutineAction(agentName: agentName)  // required
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
    agent_name: agentName,  // required
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

Recurring `schedule` triggers aren't supported through the `azd ai routine` extension in preview. Use the REST API, Python, C#, or JavaScript SDK to create a schedule routine, or use the [timer trigger](#timer-trigger) from `azd` for a one-shot run.

:::zone-end

### Timer trigger

A timer trigger fires once at a specific future date and time, or after a duration from now.

:::zone pivot="foundry-portal"

1. Follow steps 1Ã¢â‚¬â€œ4 for creating a routine, and enter a name such as `once-on-release-day`.
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

- An ISO 8601 timestamp with an explicit UTC offset, for example `"2026-06-01T09:00:00Z"`.
- A local timestamp paired with `time_zone`, for example `"at": "2026-09-01T09:00:00", "time_zone": "America/Los_Angeles"`.
- A positive duration from the current time, for example `"30m"` (30 minutes from now) or `"2h"` (two hours from now).

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
```

```bash
azd ai routine create --file routine.yaml
```

> [!NOTE]
> The agent referenced by `agent_name` must have a configured agent identity. Prompt-only agents are rejected by the service when bound to a routine action.

:::zone-end

## Action fields

Each routine specifies exactly one action. The two supported action types have different required and optional fields.

### Responses API action (`invoke_agent_responses_api`)

Invokes the agent through the Responses API.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_responses_api"`. |
| `agent_name` | string | Yes | The project-scoped agent name. Maximum 256 characters. |
| `conversation_id` | string | No | An existing conversation to continue during the dispatch. Maximum 256 characters. |

### Invocations API action (`invoke_agent_invocations_api`)

Invokes the agent through the Invocations API.

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_invocations_api"`. |
| `agent_name` | string | Yes | The project-scoped agent name. Maximum 256 characters. |
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

:::zone pivot="azd"

```bash
# Disable
azd ai routine disable once-on-release-day

# Enable
azd ai routine enable once-on-release-day
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

**Responses API routine Ã¢â‚¬â€ with optional input override:**

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

**Invocations API routine Ã¢â‚¬â€ with optional input override:**

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

:::zone pivot="azd"

Queue a manual run for a Responses API routine:

```bash
azd ai routine dispatch once-on-release-day \
  --input "Run the routine for testing."
```

The command prints the `dispatch_id` and `task_id`. Use the `dispatch_id` to find the run in the run history.

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
        print(f"  error: {run.error_type} Ã¢â‚¬â€ {run.error_message}")
```

:::zone-end

:::zone pivot="programming-language-csharp"

```csharp
await foreach (var run in client.GetRoutinesClient().GetRunsAsync("daily-summary"))
{
    Console.WriteLine($"{run.Id}  phase={run.Phase}  source={run.AttemptSource}");
    if (run.Phase == RoutineRunPhase.Failed)
        Console.WriteLine($"  error: {run.ErrorType} Ã¢â‚¬â€ {run.ErrorMessage}");
}
```

:::zone-end

:::zone pivot="programming-language-javascript"

```javascript
for await (const run of client.routines.listRuns("daily-summary")) {
  console.log(`${run.id}  phase=${run.phase}  source=${run.attempt_source}`);
  if (run.phase === "failed") {
    console.log(`  error: ${run.error_type} Ã¢â‚¬â€ ${run.error_message}`);
  }
}
```

:::zone-end

:::zone pivot="azd"

Listing run history through `azd ai routine` isn't supported in preview. Use the Foundry portal, REST API, or an SDK to retrieve runs.

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

:::zone pivot="azd"

Retrieve a single routine:

```bash
azd ai routine show once-on-release-day
```

Listing all routines through `azd ai routine` isn't supported in preview. Use the Foundry portal, REST API, or an SDK.

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

:::zone pivot="azd"

Apply changes from a YAML manifest:

```bash
azd ai routine update once-on-release-day --file routine.yaml
```

The `--description` flag isn't supported for timer routines in preview; edit the manifest and reapply with `--file` instead.

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


## Dispatch behavior and retry policy

When a trigger fires or you call `:dispatch_async` manually, Foundry acknowledges that the run was enqueued. The acknowledgement doesn't mean the downstream agent call has finished. Use the run state, telemetry, or the returned `dispatch_id` to confirm completion.

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

- The default delivery policy is 3 total attempts with exponential backoff starting at 1 second and capped at 5 seconds.
- The downstream HTTP request has a per-attempt timeout of 30 seconds. Queueing time, retry backoff, and worker concurrency limits aren't included in that per-request timeout.

## Known issues and limitations

The preview has the following known issues and limitations:

- **One trigger and one action per routine.** Each routine supports exactly one entry in the `triggers` map and one action. To run multiple agents or multiple schedules, create separate routines.
- **Trigger types.** Only `timer` (one-shot) and `schedule` (cron-based recurring) triggers are supported. Event-based triggers aren't available in preview.
- **Action types.** The only action is invoking one Foundry agent through the Responses API or Invocations API.
- **Schedule minimum interval.** A `schedule` trigger fires at most once every five minutes. Cron expressions that resolve to a shorter interval are rejected.
- **Regional availability.** Routines are available only in the regions listed under [Prerequisites](#prerequisites). If **Routines** isn't visible in the Foundry portal navigation, the feature isn't enabled for your region or subscription.
- **Use `:dispatch_async` for manual dispatch.** Only the `POST .../routines/{routineName}:dispatch_async` route is part of the public contract. The legacy `:dispatch` route isn't supported for customer use.
- **Acknowledgement isn't completion.** A `:dispatch_async` response acknowledges that the run was enqueued, not that the downstream agent call finished. Use the run state, telemetry, or the returned `dispatch_id` to observe final delivery.
- **Per-attempt timeout.** The downstream HTTP request to the agent has a per-attempt timeout of 30 seconds. Queueing time, retry backoff, message-bus delivery time, and worker concurrency limits aren't included in that timeout. Requests that exceed the per-attempt timeout are retried per the [retry and timeout defaults](#retry-and-timeout-defaults), and the routine run is marked failed if all attempts time out.
- **Successful delivery doesn't guarantee end-to-end completion.** A completed routine run means the downstream API returned success for the dispatch request. It doesn't guarantee that asynchronous work started by the agent has finished.

## Related content

- [Create a Foundry project](../../how-to/create-projects.md)
- [Create and configure agents](configure-agent.md)
- [Model Context Protocol (MCP)](tools/model-context-protocol.md)
- [Use toolboxes with agents](tools/toolbox.md)
