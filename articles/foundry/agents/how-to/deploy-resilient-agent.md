---
title: "Deploy a crash-resilient long-running agent (preview)"
description: "Deploy a long-running hosted agent that keeps working with no client traffic, survives a container crash, and resumes from its last checkpoint."
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

# Deploy a crash-resilient long-running agent (preview)

In this article, you deploy a [long-running hosted agent](../concepts/long-running-agent-resilience.md) that uses the Responses protocol and the resilient background response feature. You run a single response that works for roughly 25 minutes with no client connected, crash the container on purpose, and watch the platform bring it back and resume from the last checkpoint.

The agent runs a fixed research plan of streamed phases. Each completed phase is one checkpointed output item, so a recovered run repeats at most one phase.

> [!NOTE]
> Long-running agents are in preview. APIs and package versions are subject to change.

## Prerequisites

- An Azure subscription with Microsoft Foundry access.
- A model deployment in your Foundry project (for example, `gpt-5.4-nano`).
- [Python 3.12](https://www.python.org/downloads/).
- The [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) with the Foundry agents extension: `azd extension install azure.ai.agents`.
- The [Azure CLI](/cli/azure/install-azure-cli) for local model calls.

## Get the sample

Clone the samples and change into the resilient research agent (Responses, Python):

```bash
git clone https://github.com/microsoft-foundry/foundry-samples.git
cd foundry-samples/samples/python/resilient-research-responses-python
```

The sample opts in to resilience and steering when it creates the host:

```python
# app.py
app = ResponsesAgentServerHost(
    options=ResponsesServerOptions(
        resilient_background=True,       # re-invoke the handler after a crash
        steerable_conversations=True,    # accept a follow-up turn mid-run
    ),
)
```

> [!IMPORTANT]
> `resilient_background` defaults to `False`. Without it, a background response that crashes is marked `failed` instead of being recovered. See [Recover long-running work after a crash](recover-long-running-work.md).

## Run it locally

The resilient state store uses files when you run it locally, so your machine uses the same recovery code path.



```bash
az login
export FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
export AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-5.4-nano

cd local
./setup.sh     # create the venv and install dependencies
./serve.sh     # run the agent on http://localhost:8088
```

## Deploy to Foundry

From the sample root, provision a project and deploy the container. When prompted for a location, choose a [region that supports hosted agents](../concepts/hosted-agents.md#region-availability).

```bash
azd auth login
azd up         # prompts for environment name, subscription, and location
```

`azd up` prints the Responses endpoint and a playground link.

## Run the demo

Use the sample's client to drive the create → crash → recover flow. It pins one `agent_session_id` so `crash` and `stream` target the same sandbox as the running response.

```bash
./demo-client.sh start "renewable energy supply chains"   # stream phases as output items
./demo-client.sh crash                                     # crash → platform restart → recover in place
./demo-client.sh stream                                    # reconnect: in_progress reset, then continue
```

What each step demonstrates:

| Step | What happens | Concept |
| --- | --- | --- |
| `start` | Creates a background response (`stream:true, store:true, background:true`) and attaches to the SSE stream. | [Long-running, no-ingress survival](../concepts/long-running-agent-resilience.md#background-execution-and-resilience) |
| `crash` | Kills the process. The platform restarts the container and reinvokes the handler with `context.is_recovery == True`. | [Crash recovery](../concepts/long-running-agent-resilience.md#resilient-work-model) |
| `stream` | Reattaches with `GET /responses/{id}?stream=true&starting_after=N`. The first post-reconnect `response.in_progress` event is a snapshot reset. | [Streaming with reconnect](stream-with-reconnect.md) |

To prove the no-ingress guarantee, run `start` and then send no further requests for 20+ minutes. The platform keeps the agent alive and the response keeps progressing. You can reconnect or poll at any time.


## Clean up

```bash
azd down       # removes everything azd created
```

## Related content

- [Resilience for long-running hosted agents](../concepts/long-running-agent-resilience.md)
- [Recover long-running work after a crash](recover-long-running-work.md)
- [Steer an in-flight agent turn](steer-hosted-agent.md)
- [Stream with reconnect](stream-with-reconnect.md)
