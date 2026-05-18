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

This article shows you how to create, manage, and monitor routines by using the Foundry portal, the REST API, and the Python SDK.

> [!NOTE]
> Routines are in preview. Send the `Foundry-Features: Routines=V1Preview` header on every REST call. All routine operations are on the data plane under your project endpoint.

## Supported trigger types

| Trigger type | Description |
|---|---|
| `schedule` | Recurring trigger defined by a cron expression. Minimum interval is 5 minutes. |
| `timer` | One-shot trigger that fires at a specific future date/time or after a duration. |
| `github_issue` | Fires when a GitHub issue is opened or closed in a repository you connect. |
| `custom` | Fires on a provider-specific event you define. |

## Supported action types

| Action type | Description |
|---|---|
| `invoke_agent_responses_api` | Invokes the agent through the Responses API. Use the agent name or endpoint ID. |
| `invoke_agent_invocations_api` | Invokes the agent through the raw Invocations API. Use the agent endpoint ID. |

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

:::zone pivot="programming-language-rest"

- Install [curl](https://curl.se/) or any HTTP client.
- Install the [Azure CLI](/cli/azure/install-azure-cli) to acquire access tokens.

:::zone-end

## Create a routine

A routine definition specifies a trigger (when to fire) and an action (which agent to run). Exactly one trigger entry is supported in preview.

### Schedule trigger

A schedule trigger fires repeatedly on a cron expression. Foundry enforces a minimum interval of 5 minutes.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. In the left navigation, select **Routines**.
1. Select **+ New routine**.
1. Enter a **Name** for the routine, for example `daily-summary`.
1. Under **Trigger**, select **Schedule**.
1. Enter a [cron expression](https://en.wikipedia.org/wiki/Cron#CRON_expression), for example `0 7 * * 1-5` (07:00 UTC on weekdays).
1. Select a **Time zone** from the dropdown, for example **UTC**.
1. Under **Action**, select **Responses API** and enter the agent name.
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

A successful response returns HTTP 200 or 201 with the routine object, including `created_at` and `updated_at` timestamps.

**Reference:**

- [PUT /routines/{routine_name}](https://aka.ms/foundry-routines-api) — Create or update a routine.

:::zone-end

:::zone pivot="programming-language-python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["PROJECT_ENDPOINT"]
agent_name = os.environ["AGENT_NAME"]

client = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

routine = client.routines.create_or_update(
    routine_name="daily-summary",
    description="Runs a daily summary agent on weekday mornings.",
    enabled=True,
    triggers={
        "weekday-morning": {
            "type": "schedule",
            "cron_expression": "0 7 * * 1-5",
            "time_zone": "UTC",
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)

print(f"Routine created: {routine.name}, enabled={routine.enabled}")
```

**Reference:**

- [`AIProjectClient.routines.create_or_update`](https://aka.ms/foundry-routines-sdk-python)

:::zone-end

### Timer trigger

A timer trigger fires once at a specific future date and time, or after a duration from now.

:::zone pivot="foundry-portal"

1. Follow steps 1–4 for creating a routine, and enter a name such as `once-on-release-day`.
1. Under **Trigger**, select **Timer**.
1. Enter the date and time in ISO 8601 format, for example `2026-09-01T09:00:00Z`, or a duration such as `PT2H` (two hours from now).
1. Optionally select a **Time zone** if you supply a local timestamp without a UTC offset.
1. Under **Action**, select **Responses API** and enter the agent name.
1. Select **Create**.

:::zone-end

:::zone pivot="programming-language-rest"

```bash
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

The `at` field supports:

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
            "at": "2026-09-01T09:00:00Z",
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
```

:::zone-end

### GitHub issue trigger

A GitHub issue trigger fires when an issue is opened or closed in a connected repository.

**Before you begin:** Create a connection to GitHub in your Foundry project. You'll need the connection name as the `connection_id`.

:::zone pivot="foundry-portal"

1. Follow steps 1–4 for creating a routine, and enter a name such as `gh-issue-triage`.
1. Under **Trigger**, select **GitHub issue**.
1. Select the GitHub **Connection** you set up for your project.
1. Enter the **Owner** (GitHub organization or user), for example `contoso`.
1. Enter the **Repository**, for example `contoso-app`.
1. Select the **Issue event**: **Opened** or **Closed**.
1. Under **Action**, select **Responses API** and enter the agent name.
1. Select **Create**.

:::zone-end

:::zone pivot="programming-language-rest"

```bash
CONNECTION_ID=<your-github-connection-name>

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

:::zone-end

:::zone pivot="programming-language-python"

```python
connection_id = os.environ["GITHUB_CONNECTION_NAME"]

routine = client.routines.create_or_update(
    routine_name="gh-issue-triage",
    description="Triages new GitHub issues with an agent.",
    enabled=True,
    triggers={
        "new-issue": {
            "type": "github_issue",
            "connection_id": connection_id,
            "owner": "contoso",
            "repository": "contoso-app",
            "issue_event": "opened",
        }
    },
    action={
        "type": "invoke_agent_responses_api",
        "agent_name": agent_name,
    },
)
```

:::zone-end

## Enable and disable a routine

Routines start enabled if you set `"enabled": true` at creation. You can pause a routine without deleting it.

:::zone pivot="foundry-portal"

1. In [Microsoft Foundry](https://ai.azure.com), open your project.
1. Select **Routines** in the left navigation.
1. Find the routine in the list and select it.
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

## Test a routine manually

Use the `dispatch_async` operation to queue a one-off run without waiting for the trigger to fire. This lets you verify that the routine reaches your agent correctly.

:::zone pivot="foundry-portal"

1. Open the routine in [Microsoft Foundry](https://ai.azure.com).
1. Select **Run now**.
1. For Responses API routines, optionally enter a test **Input message**.
1. Select **Dispatch**.

Foundry queues the run and opens the run history view. The new run appears with status **Queued** and progresses to **Dispatching** and then **Completed** or **Failed**.

:::zone-end

:::zone pivot="programming-language-rest"

**With a custom input message (Responses API routine):**

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
# Dispatch with an optional input override
result = client.routines.dispatch_async(
    routine_name="daily-summary",
    payload={
        "type": "invoke_agent_responses_api",
        "input": "Run the daily summary for testing.",
    },
)

print(f"dispatch_id: {result.dispatch_id}")
print(f"task_id:     {result.task_id}")
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

**Filter runs by phase (using MLflow filter syntax):**

```bash
curl -sS "$PROJECT_ENDPOINT/routines/daily-summary/runs?filter=tags.phase%3D'failed'" \
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

The `phase` field uses Foundry lifecycle values (`queued`, `dispatching`, `completed`, `failed`). The `status` field is the underlying MLflow run status (`RUNNING`, `FINISHED`, `FAILED`).

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
        print(f"  error: {run.error_type} — {run.error_message}")
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

## Reference: trigger and action fields

### Schedule trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"schedule"`. |
| `cron_expression` | string | Yes | A 5-field cron expression. Minimum interval: 5 minutes. |
| `time_zone` | string | Yes | An IANA or Windows time zone identifier, for example `"UTC"` or `"America/Los_Angeles"`. |

### Timer trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"timer"`. |
| `at` | string | Yes | An ISO 8601 timestamp with a UTC offset, a local timestamp paired with `time_zone`, or a positive ISO 8601 duration from now. |
| `time_zone` | string | No | Required when `at` is a local timestamp without a UTC offset. |

### GitHub issue trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"github_issue"`. |
| `connection_id` | string | Yes | The Foundry project connection name that resolves the GitHub credentials. Maximum 256 characters. |
| `owner` | string | Yes | The GitHub organization or user that owns the repository. Maximum 128 characters. |
| `repository` | string | Yes | The GitHub repository name. Maximum 128 characters. |
| `issue_event` | string | Yes | The event that fires the trigger: `"opened"` or `"closed"`. |

### Custom trigger fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"custom"`. |
| `provider` | string | Yes | The provider or source identifier. Maximum 128 characters. |
| `event_name` | string | No | An optional provider-specific event name. Maximum 128 characters. |
| `parameters` | object | Yes | Provider-specific parameters passed to the trigger. |

### Responses API action fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_responses_api"`. |
| `agent_name` | string | Conditional | The project-scoped agent name. Provide either `agent_name` or `agent_endpoint_id`. Maximum 256 characters. |
| `agent_endpoint_id` | string | Conditional | The endpoint-scoped agent identifier. Provide either `agent_name` or `agent_endpoint_id`. Maximum 256 characters. |
| `conversation_id` | string | No | An existing conversation to continue during the dispatch. Maximum 256 characters. |

### Invocations API action fields

| Field | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `"invoke_agent_invocations_api"`. |
| `agent_endpoint_id` | string | Yes | The endpoint-scoped agent identifier. Maximum 256 characters. |
| `session_id` | string | No | An existing hosted-agent session to continue during the dispatch. Maximum 256 characters. |

## Preview limitations

- In v1 preview, each routine supports exactly one trigger entry in the `triggers` map.
- The `custom` trigger type requires a provider configured in your subscription.
- GitHub issue triggers require a GitHub connection created in the project.
- Routine run history is backed by MLflow. Advanced filtering uses [MLflow search syntax](https://mlflow.org/docs/latest/search-runs.html).

## Related content

- [What are routines?](../concepts/routines.md)
- [Create a Foundry project](../../how-to/create-projects.md)
- [Create and configure agents](configure-agent.md)
- [Use toolboxes with agents](tools/toolbox.md)
