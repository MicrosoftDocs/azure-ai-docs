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

Steering needs stored background responses (`store: true` and `background: true`), so send each turn's body from a file. Create the first turn's request file:

```bash
cat > turn1.json <<'EOF'
{ "input": "Explain quantum computing in detail, including its history, principles, algorithms, hardware, error correction, and applications.", "store": true, "background": true }
EOF
```

Start the response in a new session. The command returns while the response is still running and saves the hosted session and conversation for the next invocation:

```bash
azd ai agent invoke --new-session -f turn1.json
```

Create the second turn's request file:

```bash
cat > turn2.json <<'EOF'
{ "input": "Instead, explain relativity and focus on practical examples.", "store": true, "background": true }
EOF
```

Immediately send the new instruction. `azd` reuses the saved session and conversation, so the new turn steers the response that's already in progress:

```bash
azd ai agent invoke -f turn2.json
```

The first turn observes the queued input and winds down at its next safe point. The queued turn then runs to completion. Stream the session logs to watch the handoff:

```bash
azd ai agent monitor --follow
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
