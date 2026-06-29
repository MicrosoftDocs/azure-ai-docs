---
title: "Monitor hosted agent logs with the Azure Developer CLI"
description: "Stream and inspect Microsoft Foundry hosted agent logs with azd to troubleshoot sessions, container events, and runtime behavior."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 06/15/2026
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Monitor hosted agent logs with the Azure Developer CLI


[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Stream and inspect logs from your deployed Microsoft Foundry hosted agent for troubleshooting and observability. You learn how to view console logs, stream in real time, inspect system events, filter by session, and recognize common log patterns.

## Prerequisites

- A deployed hosted agent. To deploy one, see [Deploy a hosted agent](deploy-hosted-agent.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- For session-specific logs, a session ID from an `azd ai agent invoke` response. To invoke an agent, see [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md).

## View recent console logs

- Fetch recent console logs:

   ```bash
   azd ai agent monitor
   ```

   This command fetches recent console logs, including stdout and stderr, from the agent's last invoke session. If no session exists, it streams container logs. The command exits after fetching the available logs. Use `--follow` to stream continuously.

## Stream logs in real time

- Stream logs continuously:

   ```bash
   azd ai agent monitor --follow
   ```

   Press **Ctrl+C** to stop. This is the most useful mode for debugging. Run it in one terminal while sending requests in another.

## View system event logs

- Show container lifecycle events instead of console output:

   ```bash
   azd ai agent monitor --type system
   ```

   Use system event logs to diagnose container crashes, restart loops, and resource issues.

## View session-specific logs

- Filter logs to a specific agent session:

   ```bash
   azd ai agent monitor --session-id <session-id>
   ```

- Combine with `--follow` for real-time streaming:

   ```bash
   azd ai agent monitor --session-id <session-id> --follow
   ```

   To find session IDs, check the output of `azd ai agent invoke`. It prints the session ID for each request.

## Control log length

- Show the last 100 lines:

   ```bash
   azd ai agent monitor --tail 100
   ```

   The range is 1-300. The default is 50.

## Monitor a specific agent

- In multi-service projects, pass the agent name:

   ```bash
   azd ai agent monitor my-agent
   ```

## Recognize common log patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| `Listening on 0.0.0.0:8088` | Agent started successfully. | None needed. |
| `AuthenticationError` | The agent's Entra Agent Identity can't authenticate. | Check RBAC roles. |
| `ModelNotFound` | Model deployment name mismatch. | Verify deployment name in `agent.yaml` matches Foundry portal. |
| `ResourceNotFound` | Foundry endpoint mismatch. | Check `FOUNDRY_PROJECT_ENDPOINT` value. |
| Container restart events in system logs | Crash loop. | Check code for unhandled exceptions; consider increasing container resource limits in `azure.yaml`. |
| `TimeoutError` | Request took too long. | Check model responsiveness; increase timeout on invoke. |

## Follow a debugging workflow

A typical debugging session looks like this:

1. Stream logs in one terminal:

   ```bash
   azd ai agent monitor --follow
   ```

1. Send a request in another terminal:

   ```bash
   azd ai agent invoke "Test message"
   ```

1. Watch the logs for error patterns or unexpected behavior.

1. Check system events if the agent seems unresponsive:

   ```bash
   azd ai agent monitor --type system
   ```

For a comprehensive debugging workflow, see [Debug a hosted agent](debug-hosted-agent.md).

## Related content

- [Debug a hosted agent](debug-hosted-agent.md) for step-by-step diagnostic workflows.
- [Test a hosted agent](test-hosted-agent.md) for validation strategies before production.
- [Isolate hosted agent sessions per user](isolate-sessions-per-user.md) for logs in isolated sessions.
