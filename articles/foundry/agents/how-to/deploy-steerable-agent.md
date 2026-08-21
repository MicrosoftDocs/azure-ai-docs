---
title: "Deploy a steerable agent (preview)"
description: "Deploy a hosted agent that accepts a new instruction mid-run, cooperatively winding down the in-flight turn and continuing with the redirected input."
author: aahill
ms.author: aahi
ms.manager: mcleans
ms.date: 08/05/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# Deploy a steerable agent (preview)

In this article, you deploy a [long-running hosted agent](../concepts/long-running-agent-resilience.md) that supports *steering*: when a second turn arrives on the same conversation while the first turn is still running, the platform queues the new turn and cooperatively cancels the current one instead of rejecting it with `409 conversation_locked`.

The sample is a Microsoft Agent Framework agent that turns steering on with a single option.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Prerequisites

- An Azure subscription with Microsoft Foundry access and a model deployment.
- The [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) with the Foundry agents extension.
- The [Azure CLI](/cli/azure/install-azure-cli).
- [uv](https://docs.astral.sh/uv/) to run the steering client.

## Get the sample

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/python/steering-maf
```

The agent enables steering when it constructs the host:

```python
app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(steerable_conversations=True),
)
```

By using `steerable_conversations=True`, a second turn on a busy conversation is queued and the running handler is cooperatively cancelled, rather than returning `409 conversation_locked`.

## Provision and deploy

Authenticate, create an environment, and provision the project. When prompted for a location, choose a [region that supports hosted agents](../concepts/hosted-agents.md#region-availability).

```bash
azd extension install azure.ai.agents
azd auth login
az login

azd env new
azd provision
azd deploy
```

Get the hosted Responses endpoint and create a session:

```bash
azd ai agent show --output json
azd ai agent sessions create --output json
```

## Run the steering client

Pass the endpoint and the returned `agent_session_id` to the client. The client starts a long streaming turn, submits a second turn on the same conversation two seconds later, and shows the first turn ending early before the queued turn completes.

```bash
uv run ./client.py \
  --endpoint "https://<account>.services.ai.azure.com/api/projects/<project>/agents/steering-agent/endpoint/protocols/openai/responses?api-version=v1" \
  --session-id "<agent-session-id>"
```

Both turns use the same hosted session and Responses conversation ID. The first turn observes the queued input and winds down at its next safe point; the queued turn then runs to completion.

## Clean up

```bash
azd down
```

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Add a human-in-the-loop approval step](add-human-in-the-loop.md)
- [Deploy a crash-resilient long-running agent](deploy-resilient-agent.md)
