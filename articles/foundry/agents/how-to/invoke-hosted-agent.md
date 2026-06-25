---
title: "Invoke a hosted agent with the Azure Developer CLI"
description: "Send prompts, files, and protocol-specific requests to Microsoft Foundry hosted agents with azd locally or after deployment."
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

# Invoke a hosted agent with the Azure Developer CLI

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use `azd ai agent invoke` to send messages to your agent, either the deployed version in Microsoft Foundry or a locally running instance. You learn how to choose an agent, use direct endpoints, manage sessions, send files, pin versions, and inspect raw responses.

## Prerequisites

- An initialized hosted agent project. To create one, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- For remote invocation, a deployed hosted agent. To deploy one, see [Deploy a hosted agent](deploy-hosted-agent.md).
- For local invocation, a running local agent. To start one, see [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md).

## Invoke the deployed agent

- Send a prompt to the deployed agent:

   ```bash
   azd ai agent invoke "What is Microsoft Foundry?"
   ```

## Invoke a specific agent

- If your project contains multiple agents, specify which one to invoke:

   ```bash
   azd ai agent invoke my-agent "What is Microsoft Foundry?"
   ```

## Invoke a specific deployed endpoint

When you want to invoke a specific deployed agent without depending on the active azd environment or `azure.yaml`, use `--agent-endpoint` to point directly at the deployed agent's URL. This pattern is useful from a script outside the project, from a coding agent, or when you test a specific agent version.

- Pass the deployed agent endpoint:

   ```bash
   azd ai agent invoke \
     --agent-endpoint https://my-project.services.ai.azure.com/api/projects/my-project/agents/release-summarizer/versions/3 \
     "Summarize today's release notes."
   ```

   `--agent-endpoint` overrides azd environment and `azure.yaml` resolution, so you don't need to be inside an azd project directory to use it.

## Invoke locally

- Invoke a local agent:

   ```bash
   azd ai agent invoke --local "Hello!"
   ```

   The agent must already be running with `azd ai agent run` in another terminal.

## Invoke on a custom local port

- If your agent is running on a non-default port, pass `--port`:

   ```bash
   azd ai agent invoke --local --port 9090 "Hello!"
   ```

## Choose a protocol

The protocol used for invoke is determined by the `protocols` field in your `agent.yaml`.

- **`responses`** -- sends a standard OpenAI Responses API request with `{"input": "your message"}`. Conversation history is managed automatically.
- **`invocations`** -- sends whatever payload your agent code expects. Use `--input-file` (`-f`) with a JSON file matching the schema your handler defines.

For `invocations` agents, check the sample's README or inspect the handler entry point to understand the expected payload.

- If your agent implements multiple protocols, pass `--protocol` (`-p`) to choose:

   ```bash
   azd ai agent invoke --protocol invocations -f request.json
   ```

## Manage sessions

Sessions are persisted per-agent. When you invoke an agent, `azd` saves the session ID locally so the next `invoke` automatically continues the same session and maintains conversation history across calls.

### Start a new session

- Discard the saved session and begin fresh:

   ```bash
   azd ai agent invoke --new-session "Start fresh"
   ```

### Use a specific session ID

- Pass an existing session ID:

   ```bash
   azd ai agent invoke --session-id my-session-123 "Continue conversation"
   ```

## Send a file as input

For structured or large payloads, especially with the `invocations` protocol, pass a JSON file.

1. Send a file:

   ```bash
   azd ai agent invoke -f request.json
   ```

1. Or send a file to a specific agent:

   ```bash
   azd ai agent invoke my-agent -f request.json
   ```

## Invoke a deployed version

When an agent has multiple deployed versions, pin a specific one with `--version`. `azd` creates or reuses a session backed by that version, so each version keeps its own conversation state.

- Pin a version:

   ```bash
   azd ai agent invoke --version 3 "Use the v3 prompt"
   ```

   `--version` can't be combined with `--local` or `--session-id` because sessions are bound to a version when they're created.

## Set a custom timeout

- Pass a timeout in seconds:

   ```bash
   azd ai agent invoke --timeout 300 "Process this large dataset"
   ```

   The default timeout is 1800 seconds (30 minutes). Use `--timeout 0` for no timeout.

## Pass isolation keys

Agents configured with Foundry header-based isolation require per-user or per-chat keys on every request. Pass them with `--user-isolation-key` and `--chat-isolation-key`.

- Pass isolation keys with the request:

   ```bash
   azd ai agent invoke \
     --user-isolation-key "$USER_KEY" \
     --chat-isolation-key "$CHAT_KEY" \
     "Hello!"
   ```

For the full pattern, including how sessions, files, and monitor commands use the same flags, see [Pass isolation keys to a hosted agent](pass-isolation-keys.md).

## Inspect the raw HTTP response

When you need to see exactly what the server returned, including response headers like the agent version, status line, and the unmodified body, pass `--output raw` (`-o raw`).

- Request raw output:

   ```bash
   azd ai agent invoke --output raw "Hello!"
   ```

   In raw mode, friendly summary lines like `Session:` and `Invocation:` are suppressed and the HTTP response is dumped verbatim. This mode is useful for debugging server behavior and confirming which agent version handled the call.

## Related content

- [Pass isolation keys to a hosted agent](pass-isolation-keys.md) for header-based isolation in multi-tenant agents.
- [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) to start your agent for local development.
- [Monitor hosted agent logs with the Azure Developer CLI](monitor-hosted-agent-logs.md) to inspect deployed agent behavior.
