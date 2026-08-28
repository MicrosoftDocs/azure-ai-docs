---
title: "Deploy a steerable agent (preview)"
description: "Deploy a hosted agent that accepts a new instruction mid-run, cooperatively winding down the in-flight turn and continuing with the redirected input."
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

# Deploy a steerable agent (preview)

In this article, you deploy a [long-running hosted agent](../concepts/long-running-agent-resilience.md) that supports *steering*: when a second turn arrives on the same conversation while the first turn is still running, the platform queues the new turn and cooperatively cancels the current one instead of rejecting it with `409 conversation_locked`.

The sample is a Responses protocol agent that turns on resilience and steering with two options. It uses a simulated model stream, so you can run it without model credentials.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Prerequisites

- An Azure subscription with Microsoft Foundry access.
- [Python 3.13](https://www.python.org/downloads/).
- The [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) with the Foundry agents extension.
- The [Azure CLI (`az`)](/cli/azure/install-azure-cli) and [`curl`](https://curl.se/) to call the deployed agent.

## Get the sample

In an empty directory, initialize the resilient steering agent from its `azure.yaml` manifest:

```bash
azd auth login
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/resilient-steering/azure.yaml
```

The command downloads the sample source, adopts its `azure.yaml`, creates an azd environment, and connects it to the Foundry project you select.

The agent enables resilience and steering when it constructs the host:

```python
options = ResponsesServerOptions(
    resilient_background=True,
    steerable_conversations=True,
)
app = ResponsesAgentServerHost(options=options)
```

By using `steerable_conversations=True`, a second turn on a busy conversation is queued and the running handler is cooperatively cancelled, rather than returning `409 conversation_locked`.

## Provision and deploy

Provision the project and deploy the agent. When prompted for a location, choose a [region that supports hosted agents](../concepts/hosted-agents.md#region-availability).

```bash
azd up
```

`azd up` prints the Responses endpoint and a playground link.

## Steer the deployed agent

`azd up` prints the Responses endpoint. Save it, remove its query string, and get an access token:

```bash
ENDPOINT="<responses-endpoint-from-azd-up>"
RESPONSES_ENDPOINT="${ENDPOINT%%\?*}"
TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)
```

Steering needs stored background responses (`store: true` and `background: true`). Start the first turn and note the `conversation` ID in the response:

```bash
curl -sS -X POST "$RESPONSES_ENDPOINT?api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": "Explain quantum computing in detail, including its history, principles, algorithms, hardware, error correction, and applications.", "store": true, "background": true}'
```

While the first turn is still running, immediately send a new instruction on the *same conversation* so it steers the in-flight turn:

```bash
curl -sS -X POST "$RESPONSES_ENDPOINT?api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"input": "Instead, explain relativity and focus on practical examples.", "conversation": "<conversation-id-from-turn-1>", "store": true, "background": true}'
```

The first turn observes the queued input and winds down at its next safe point. The queued turn then runs to completion. Stream either response with its `id` to watch the handoff:

```bash
curl -sS "$RESPONSES_ENDPOINT/<response-id>?api-version=2025-11-15-preview" \
  -H "Authorization: Bearer $TOKEN"
```

## Clean up

```bash
azd down
```

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Add a human-in-the-loop approval step](add-human-in-the-loop.md)
- [Deploy a crash-resilient long-running agent](deploy-resilient-agent.md)
