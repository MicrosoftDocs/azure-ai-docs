---
title: "Deploy a crash-resilient long-running agent (preview)"
description: "Deploy a long-running hosted agent that keeps working with no client traffic, survives a container crash, and resumes from its last checkpoint."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 08/20/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy a crash-resilient long-running agent (preview)

In this article, you deploy a [long-running hosted agent](../concepts/long-running-agent-resilience.md) that uses the Responses protocol and the resilient background response feature. You run a stored background response, crash the agent process on purpose, and watch it resume from the last checkpoint after restart.

The agent runs three simulated streamed stages: analyze, generate, and refine. Each completed stage is one checkpointed output item, so a recovered run repeats at most one stage.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Prerequisites

- An Azure subscription with Microsoft Foundry access.
- [Python 3.13](https://www.python.org/downloads/).
- The [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) with the Foundry agents extension: `azd extension install azure.ai.agents`.
- The [Azure CLI (`az`)](/cli/azure/install-azure-cli) and [`curl`](https://curl.se/) to call the deployed agent.

## Get the sample

In an empty directory, initialize the resilient streaming agent from its `azure.yaml` manifest:

```bash
azd auth login
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/resilient-streaming/azure.yaml
```

The command downloads the sample source, adopts its `azure.yaml`, creates an azd environment, and connects it to the Foundry project you select.

The sample opts in to resilience when it creates the host:

```python
# src/resilient-streaming/main.py
options = ResponsesServerOptions(resilient_background=True)
app = ResponsesAgentServerHost(options=options)
```

> [!IMPORTANT]
> `resilient_background` defaults to `False`. Without it, a background response that crashes is marked `failed` instead of being recovered. See [Recover long-running work after a crash](recover-long-running-work.md).

## Run it locally

The resilient state store uses files when you run it locally, so your machine uses the same recovery code path. This walkthrough drives the agent with `curl`, so every run uses `azd ai agent run --no-client`, which installs the Python dependencies, injects the active azd environment, and starts the agent on `http://localhost:8088` without launching Agent Inspector.

## Test crash recovery locally

Use Linux, WSL2, or a container for this exercise so the operating system releases the file lock when the process exits.

Set `SIMULATE_CRASH_AFTER_STAGE` so the sample crashes after it checkpoints the first stage, and then start the agent:

```bash
SIMULATE_CRASH_AFTER_STAGE=0 azd ai agent run --no-client
```

Recovery needs a stored background response (`store: true` and `background: true`). In a second terminal, send the request inline with `curl`:

```bash
curl -sS -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "renewable energy supply chains", "store": true, "background": true}'
```

The agent checkpoints the analyze stage and then exits. Restart it from the first terminal:

```bash
azd ai agent run --no-client
```

The framework reinvokes the handler with `context.is_recovery == True`. The handler restores `context.persisted_response`, skips the checkpointed analyze stage, and completes the generate and refine stages.

## Deploy to Foundry

Provision the project and deploy the agent. When prompted for a location, choose a [region that supports hosted agents](../concepts/hosted-agents.md#region-availability).

```bash
azd up
```

`azd up` prints the Responses endpoint and a playground link.

## Invoke the deployed agent

`azd up` prints the Responses endpoint. Save it, remove its query string, and get an access token:

```bash
ENDPOINT="<responses-endpoint-from-azd-up>"
RESPONSES_ENDPOINT="${ENDPOINT%%\?*}"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
```

Create a stored background response, and note the returned `id`:

```bash
curl -sS -X POST "$RESPONSES_ENDPOINT?api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": "renewable energy supply chains", "store": true, "background": true}'
```

The platform keeps the background response running with no client traffic. Poll or stream it with the `id` from the previous response:

```bash
curl -sS "$RESPONSES_ENDPOINT/<response-id>?api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $TOKEN"
```

For the reconnect protocol and the `starting_after` cursor, see [Stream with reconnect](stream-with-reconnect.md).

## Clean up

```bash
azd down
```

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
- [Recover long-running work after a crash](recover-long-running-work.md)
- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Stream with reconnect](stream-with-reconnect.md)
