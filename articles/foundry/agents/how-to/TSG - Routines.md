---
title: "Troubleshoot routines (preview)"
description: "Diagnose and resolve common issues when creating, configuring, and monitoring routines in Microsoft Foundry, including trigger failures, run errors, and scheduling problems."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: troubleshooting
ms.date: 05/20/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Troubleshoot routines (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article helps you diagnose and resolve common issues when creating, configuring, and monitoring [routines](use-routines.md) in Microsoft Foundry.

> [!NOTE]
> Routines are in preview. Send the `Foundry-Features: Routines=V1Preview` header on every REST call or the request returns `404`.

## Creation and configuration issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| `404` on routine API calls | Missing preview feature header | Add `Foundry-Features: Routines=V1Preview` to all routine API requests. |
| `400` when creating a routine with multiple triggers | Preview limitation | In v1 preview, each routine supports exactly one trigger entry in the `triggers` map. |
| `github_issue` trigger not firing | GitHub connection not created in the project | Create a project connection to GitHub and reference its connection name in the `connection_id` trigger field. |
| Custom trigger not firing | `provider` not configured in the subscription, or connector lacks trigger support | Verify the connector declares `"triggers"` in `x-ms-capabilities`. Confirm the `provider` value matches the connector's identifier. |
| Cron expression not triggering at the expected time | Incorrect cron syntax or timezone not set | Routines use standard 5-field cron expressions (minute, hour, day, month, weekday). The minimum interval is 5 minutes. Set `time_zone` explicitly to avoid UTC assumptions. |
| Timer routine doesn't fire | `fire_at` time is in the past, or duration has elapsed | For `timer` triggers, `fire_at` must be a future UTC ISO 8601 timestamp or a positive duration string. |
| Agent name in the action not found | Agent name or endpoint ID doesn't exist in the project | Verify the agent exists with the same name used in `agent_name`. For `invoke_agent_invocations_api`, use the endpoint-scoped agent identifier. |

## Run monitoring issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| Run history shows `phase: failed` with no message | Agent invocation failed silently | Check the `error_type` and `error_message` fields in the run record. For `invoke_agent_responses_api`, also inspect `response_id` from the run to retrieve the agent's full response. |
| Runs not appearing in history | Routine disabled | Verify `enabled: true` on the routine. Disabled routines don't fire and don't produce run records. |
| Manual dispatch run doesn't show up immediately | Run records are created asynchronously | List runs a few seconds after calling `POST /routines/{name}/dispatch` to see the new record. |
| Scheduled routine fires but agent response is empty | Agent instructions don't handle automated invocations | For scheduled invocations, no user context is passed. Include a default `input` in the action payload, or write instructions that guide the agent when no user input is present. |
| Event-based routine stops receiving events | Connector credentials in Connector Namespace expired | Credentials are managed by the Connector Namespace. Re-authorize the connection in the Foundry portal to refresh them. |

## Related content

- [Automate agents with routines](use-routines.md)
- [Add managed MCP servers powered by connector namespaces](tools/connectors.md)
- [Create and configure agents](configure-agent.md)
- [Troubleshoot connectors and managed MCP servers](TSG%20-%20Connectors.md)
