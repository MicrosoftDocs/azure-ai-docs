---
title: Host LangGraph agents as Foundry hosted agents
description: Learn how to use langchain_azure_ai.agents.hosting to host LangGraph agents on Foundry hosted agent service with Responses and Invocations protocols.
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
ms.topic: how-to
ms.date: 05/27/2026
ms.author: aochengwang
author: a1exwang
ms.reviewer: sgilley
ms.custom:
  - dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to host a LangGraph agent on Foundry hosted agents service.
---

# Host LangGraph agents as Foundry hosted agents

Use the `langchain_azure_ai.agents.hosting` package to expose a compiled
LangGraph graph through the protocols for Microsoft Foundry
[hosted agents](../../agents/overview.md#hosted-agents). The hosting
package lets you keep your LangChain and LangGraph agent logic in code while
Foundry manages the hosted runtime, sessions, scale, identity, and protocol
endpoints.

In this article, you create a minimal LangGraph agent, expose it through either
the Responses or Invocations protocol, test it through HTTP, and deploy it to
Foundry with the Azure Developer CLI or the Foundry Toolkit Visual Studio Code
extension.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Foundry project](../create-projects.md).
- A deployed chat model, such as `gpt-4.1` or `gpt-5-mini`.
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate.

## Install the package

Install `langchain-azure-ai` 1.2.4 or later with the hosting extra:

```bash
pip install -U "langchain-azure-ai[hosting]>=1.2.4" azure-identity
```

The `hosting` extra installs the Foundry protocol libraries used by the host
servers:

- `azure-ai-agentserver-responses` for the OpenAI-compatible `/responses`
  endpoint.
- `azure-ai-agentserver-invocations` for the generic `/invocations` endpoint.

## Choose a hosting protocol

Hosted agents can expose one or more protocols. Start with Responses for most
conversational agents.

| Protocol | Host class | Endpoint | Use when |
|---|---|---|---|
| Responses | `ResponsesHostServer` | `/responses` | You want OpenAI-compatible chat, streaming, response history, and conversation threading. |
| Invocations | `InvocationsHostServer` | `/invocations` | You want a custom JSON shape, a webhook-style endpoint, or non-conversational processing. |

For background on protocol behavior and sessions, see [Hosted agents](../../agents/concepts/hosted-agents.md) and [Manage Hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md).

## Configure environment variables

Set the project endpoint and model deployment name for local development:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4.1"
```

When the same code runs as a Hosted agent in Foundry, the platform injects
`FOUNDRY_PROJECT_ENDPOINT`. If you use `azd ai agent init` with a sample
manifest, the generated project also uses `AZURE_AI_MODEL_DEPLOYMENT_NAME` for
the selected model deployment.

## Responses protocol

Use the Responses protocol when you want an OpenAI-compatible chat endpoint with
streaming, response history, and conversation threading.

### Create a Responses host

Create a file named `main.py` with a minimal LangGraph agent that uses a
Foundry model. This pattern matches the basic Responses sample in the
`langchain-azure-ai` source repository.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from langchain_azure_ai.agents.hosting import ResponsesHostServer

_AZURE_AI_SCOPE = "https://ai.azure.com/.default"


def build_chat_model() -> ChatOpenAI:
    project_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"].rstrip("/")
    deployment = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4.1")
    credential = DefaultAzureCredential()
    project = AIProjectClient(endpoint=project_endpoint, credential=credential)
    openai_client = project.get_openai_client()
    token_provider = get_bearer_token_provider(credential, _AZURE_AI_SCOPE)

    return ChatOpenAI(
        model=deployment,
        base_url=str(openai_client.base_url),
        api_key=token_provider,
    )


def main() -> None:
    graph = create_agent(build_chat_model(), tools=[])
    port = int(os.environ.get("PORT", "8088"))
    ResponsesHostServer(graph).run(port=port)


if __name__ == "__main__":
    main()
```

**What this snippet does:** Creates a LangGraph agent with LangChain's
`create_agent`, connects it to the Foundry project's OpenAI-compatible model
endpoint, and passes the compiled graph to `ResponsesHostServer`. The host
starts an HTTP server and exposes the graph through `POST /responses`. By
default, the server binds to port `8088`, or to the value of the `PORT`
environment variable when one is set.

Run the app locally:

```bash
python main.py
```

### Test the Responses endpoint

Send a non-streaming Responses request to the local server.

**Bash:**

```bash
curl -sS -H "Content-Type: application/json" \
  -X POST http://localhost:8088/responses \
  -d '{"input":"Give me one practical tip for testing hosted agents.","stream":false}'
```

**PowerShell:**

```powershell
$body = @{
  input = "Give me one practical tip for testing hosted agents."
  stream = $false
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8088/responses `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

For streaming responses, set `stream` to `true`. The host emits Responses API
server-sent events, such as `response.created`, `response.output_text.delta`,
and `response.completed`.

### Conversations

`ResponsesHostServer` supports two conversation-state patterns. The pattern it
uses depends on whether your compiled graph has a LangGraph checkpointer.

| Graph configuration | Conversation source | What the host sends to the graph on later turns |
|---|---|---|
| Graph without a checkpointer | Responses history from the protocol runtime | Prior response history plus the current request input |
| Graph compiled with a checkpointer | LangGraph checkpoint state keyed by the conversation or response thread | Current request input only |

Use a checkpointer when your graph needs LangGraph runtime state, interrupts,
or node-local state across turns. For local testing, you can use an in-memory
checkpointer:

```python
from langgraph.checkpoint.memory import MemorySaver

graph = create_agent(
    build_chat_model(),
    tools=[],
    checkpointer=MemorySaver(),
)
```

For production Hosted agents, use a durable checkpointer instead of an
in-memory checkpointer so graph state survives container restarts.

Clients continue a Responses conversation by passing `previous_response_id` or
a `conversation` ID. For local testing, chain the previous response ID in the
next request:

```http
POST http://localhost:8088/responses
Content-Type: application/json

{
  "input": "Can you make that more concise?",
  "previous_response_id": "<previous-response-id>",
  "stream": false
}
```

When the agent runs in Foundry, the same pattern works through the Hosted agent
Responses endpoint. If later turns also need the same hosted sandbox filesystem,
include `agent_session_id` or use a `conversation` ID. For details, see
[Manage Hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md).

### Human-in-the-loop

If your graph uses LangGraph `interrupt()` calls, `ResponsesHostServer` surfaces
pending interrupts through standard Responses API output items:

- A `function_call` item named `__hosted_agent_adapter_interrupt__`.
- An `mcp_approval_request` item with `server_label` set to `langgraph`.

Clients can resume the graph by sending either a `function_call_output` item
whose `call_id` matches the interrupt ID or an `mcp_approval_response` item
whose `approval_request_id` matches the interrupt ID. Use
`function_call_output` when you need to send a rich LangGraph `Command` payload
with `resume`, `update`, or `goto` fields. Use `mcp_approval_response` for a
simple approve or reject flow.

## Invocations protocol

Use `InvocationsHostServer` when your callers can't use the Responses API
request shape or when your scenario isn't a chat conversation. The default
Invocations host accepts a `message` string and an optional `stream` flag.

### Create an Invocations host

Use the same model-building function from the Responses example, but start
`InvocationsHostServer` instead of `ResponsesHostServer`.

```python
import os

from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

from langchain_azure_ai.agents.hosting import InvocationsHostServer


def main() -> None:
    graph = create_agent(
        build_chat_model(),
        tools=[],
        checkpointer=MemorySaver(),
    )
    port = int(os.environ.get("PORT", "8088"))
    InvocationsHostServer(graph).run(port=port)


if __name__ == "__main__":
    main()
```

**What this snippet does:** Hosts the LangGraph agent through `POST
/invocations`. The `MemorySaver` checkpointer gives local multi-turn continuity
for a given session ID. For production, use a durable checkpointer so state
survives container restarts.

### Test the Invocations endpoint

Send a non-streaming request:

```bash
curl -i -X POST http://localhost:8088/invocations \
  -H "Content-Type: application/json" \
  -d '{"message":"My name is Alice.","stream":false}'
```

Non-streaming requests return JSON in this shape:

```json
{
  "response": "Assistant text"
}
```

For multi-turn conversations, reuse the `x-agent-session-id` response header as
the `agent_session_id` query parameter on the next request:

```bash
curl -X POST "http://localhost:8088/invocations?agent_session_id=<session-id>" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is my name?"}'
```

Streaming requests return `text/event-stream` events with token payloads:

```bash
curl -N -X POST http://localhost:8088/invocations \
  -H "Content-Type: application/json" \
  -d '{"message":"Count to 5.","stream":true}'
```

The stream contains token events followed by a terminal `done` event:

```text
data: {"token": "..."}

event: done
data: {}
```

### Customize the request schema

To customize the request body, subclass `InvocationsHostServer` and override
`parse_request`. You can also override `build_input` to map the parsed data to a
custom graph state.

```python
from starlette.requests import Request

from langchain_azure_ai.agents.hosting import InvocationsHostServer


class TicketHostServer(InvocationsHostServer):
    async def parse_request(self, request: Request) -> tuple[str, bool]:
        data = await request.json()
        ticket_id = data["ticket_id"]
        description = data["description"]
        stream = bool(data.get("stream", False))
        return f"Summarize ticket {ticket_id}: {description}", stream


if __name__ == "__main__":
    TicketHostServer(graph).run()
```

**What this snippet does:** Accepts a custom ticket payload and converts it to a
single user message before the host invokes the graph. For more complex graph
state, override `build_input` instead of flattening the request to text.

## Deploy

You can deploy with the Azure Developer CLI or the Foundry Toolkit Visual
Studio Code extension. The Azure Developer CLI flow uses sample manifests and
Docker; the extension flow provides a guided deployment experience in Visual
Studio Code.

Hosted agent deployment requires the **Foundry Project Manager** role on the
project. For details, see [Deploy a Hosted agent](../../agents/how-to/deploy-hosted-agent.md#required-permissions).

### Deploy with Azure Developer CLI

The `langchain-azure-ai` source repository includes Hosted agent samples that
can be run and deployed with the Azure Developer CLI. The flow uses each
sample's `agent.manifest.yaml`, `agent.yaml`, `Dockerfile`, and `main.py`.

Install the AI agent extension and sign in before you initialize a sample:

```bash
azd ext install azure.ai.agents
azd auth login
```

Docker must be running locally because `azd ai agent run` builds the container
image declared in the sample's Dockerfile. For command details, see the
[Azure Developer CLI reference](/azure/developer/azure-developer-cli/reference).

#### Initialize from a sample manifest

Create a new folder and initialize it from a sample manifest. Replace the
manifest URL with the sample you want to use.

```bash
mkdir my-langchain-agent
cd my-langchain-agent

azd ai agent init -m https://github.com/langchain-ai/langchain-azure/blob/main/samples/hosting/langgraph-hosted-agents/responses/01_basic/agent.manifest.yaml
```

Follow the prompts from `azd ai agent init`. If you don't already have a
Foundry project and model deployment, the initialization flow can guide you
through creating them.

#### Run the container locally

Run the agent host locally through `azd`:

```bash
azd ai agent run
```

The host serves on `http://127.0.0.1:8088`. In another terminal, invoke the
local protocol endpoint directly:

```bash
curl -X POST http://127.0.0.1:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello!"}'
```

PowerShell equivalent:

```powershell
(Invoke-WebRequest -Uri http://127.0.0.1:8088/responses `
  -Method POST -ContentType 'application/json' `
  -Body '{"input": "Hello!"}').Content
```

You can also invoke the local agent through `azd`:

```bash
azd ai agent invoke --local "Hello!"
```

#### Deploy to Foundry

If the initialized project uses a new Foundry project and model deployment,
provision the Azure resources first:

```bash
azd provision
```

Deploy the agent:

```bash
azd deploy
```

The deployment packages the agent into a container image, pushes it to the
provisioned container registry, and rolls it out to the Foundry Hosted agent
runtime.

The Foundry hosting infrastructure injects runtime environment variables into
the agent, including:

- `FOUNDRY_PROJECT_ENDPOINT`: The endpoint URL for the Foundry project where
  the agent is deployed.
- `AZURE_AI_MODEL_DEPLOYMENT_NAME`: The model deployment name selected during
  `azd ai agent init`.
- `APPLICATIONINSIGHTS_CONNECTION_STRING`: The connection string for the
  project's Application Insights instance.

For complete deployment concepts, permissions, and management details, see
[Deploy a Hosted agent](../../agents/how-to/deploy-hosted-agent.md) and
[Manage Hosted agent lifecycle](../../agents/how-to/manage-hosted-agent.md).

### Deploy with Foundry Toolkit Visual Studio Code extension

For extension-based deployment, see [Quickstart: Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md?pivots=vscode).

## Troubleshooting

Use this checklist to diagnose common issues while developing Hosted agents
with `langchain_azure_ai.agents.hosting`.

### Graph schema validation fails

The default hosts expect a compiled LangGraph graph whose state has a
`messages` field, such as `MessagesState`. If your graph uses a custom state
schema, subclass the host and override `build_input`. For Responses, override
`handle_create` when you need full control over request parsing, graph
execution, and emitted Responses events.

### Conversation state doesn't continue

For the Responses protocol, pass `previous_response_id` or a `conversation` ID
on later turns. If your graph uses a checkpointer, make sure the checkpointer is
configured and durable for the environment where the agent runs.

For the Invocations protocol, the platform doesn't store conversation history.
Use an `agent_session_id` query parameter to route later calls to the same
hosted sandbox and use your own state store or LangGraph checkpointer for
conversation state.

### The model can't be reached in the hosted container

Confirm that the Hosted agent version includes `AZURE_AI_MODEL_DEPLOYMENT_NAME`,
and that the agent identity has permission to call the Foundry project. The
platform sets `FOUNDRY_PROJECT_ENDPOINT`; your code should read that variable
when running in Foundry.

## Next step

> [!div class="nextstepaction"]
> [Deploy a Hosted agent](../../agents/how-to/deploy-hosted-agent.md)

## Related content

- [Get started with LangChain and LangGraph with Foundry](langchain.md)
- [Use Foundry Agent Service with LangGraph](langchain-agents.md)
- [Trace LangChain and LangGraph apps with Microsoft Foundry and Azure Monitor](langchain-traces.md)
- [Manage Hosted agent sessions](../../agents/how-to/manage-hosted-sessions.md)