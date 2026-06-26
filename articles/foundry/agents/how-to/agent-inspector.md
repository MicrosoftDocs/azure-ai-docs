---
title: "Inspect a local agent with the Agent Inspector"
description: "Open the Agent Inspector for a local Microsoft Foundry hosted agent to inspect requests, responses, sessions, and streams."
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

# Inspect a local agent with the Agent Inspector

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The Agent Inspector is a browser-based UI for poking at a Microsoft Foundry agent running on your local machine. It connects to the local agent's HTTP / SSE endpoint, shows requests and responses, and lets you replay messages while you iterate on prompts, tools, and code.

## Prerequisites

- An initialized hosted agent project. To create one, see [Initialize an agent project](init-agent-project.md).
- The azd Foundry extensions installed. For installation steps, see [Install the azd Foundry extensions](install-cli-foundry-extensions.md).
- An authenticated Azure Developer CLI session. Run `azd auth login` if needed.
- A local agent to inspect. To start one, see [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md).

The inspector ships in its own extension (`azure.ai.inspector`) and is installed automatically by the `microsoft.foundry` meta-package. It's also pulled in as a dependency of `azure.ai.agents`, so installing just the agent extension is enough.

> [!NOTE]
> The inspector only targets a local agent on `http://localhost:8088` by default. It doesn't authenticate to or proxy a deployed Foundry agent. For the deployed agent, use [`azd ai agent invoke`](invoke-hosted-agent.md) and [`azd ai agent monitor`](monitor-hosted-agent-logs.md).

## Start the agent locally

1. Start the agent in one terminal:

   ```bash
   azd ai agent run
   ```

   By default, `azd ai agent run` opens the inspector for you when the local server starts listening.

1. To skip the auto-launch, pass `--no-inspector`:

   ```bash
   azd ai agent run --no-inspector
   ```

## Launch the inspector manually

If you started the agent yourself, for example with `python app.py` or `dotnet run`, or if you closed the inspector tab and want to reopen it, launch the inspector manually.

1. Run the launch command:

   ```bash
   azd ai inspector launch
   ```

   The UI is served on `http://localhost:8087` by default and connects to an agent on `http://localhost:8088`.

1. Configure both ports if needed:

   ```bash
   # Agent on port 9000, UI on port 9001.
   azd ai inspector launch --port 9000 --inspector-port 9001
   ```

1. To seed the inspector with an existing conversation or session ID for replaying a specific run, pass the IDs explicitly:

   ```bash
   azd ai inspector launch \
     --conversation-id conv_abc123 \
     --session-id sess_xyz789
   ```

## Inspect local traffic

When the inspector is open, the single-page app streams the agent's responses over SSE and mirrors them in your terminal as well. You can:

- Inspect the full request and response payloads for each turn.
- Continue an existing conversation by reusing the conversation ID across turns.
- Reset to a fresh session at any time.

The inspector doesn't modify your agent code or `agent.yaml`. It's purely a runtime view.

## Related content

- [Run a hosted agent locally with the Azure Developer CLI](run-hosted-agent-locally.md) to start the local agent.
- [Invoke a hosted agent with the Azure Developer CLI](invoke-hosted-agent.md) for terminal-based local and deployed invocation.
- [Pass isolation keys to a hosted agent](pass-isolation-keys.md) to test isolation against a deployed agent.
