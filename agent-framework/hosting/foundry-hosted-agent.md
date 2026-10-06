---
title: Foundry Hosted Agents
description: Learn how to host Agent Framework agents in Microsoft Foundry Agent Service as containerized, managed hosted agents.
zone_pivot_groups: programming-languages
author: taochen
ms.topic: article
ms.author: taochen
ms.date: 10/02/2026
ms.service: agent-framework
ai-usage: ai-assisted
---

<!--
  Language parity table – keep in sync when adding/removing sections.

    | Section                         | C# | Python | Go | Notes                         |
    |---------------------------------|:--:|:------:|:--:|-------------------------------|
    | Overview                        | ✅ |   ✅   | ❌ | No Go Foundry hosting package |
    | Prerequisites                   | ✅ |   ✅   | ❌ |                               |
    | Responses protocol              | ✅ |   ✅   | ❌ |                               |
    | Invocations protocol            | ✅ |   ✅   | ❌ |                               |
    | Running locally                 | ✅ |   ✅   | ❌ |                               |
    | Deploying to Foundry            | ✅ |   ✅   | ❌ |                               |
-->

# Foundry Hosted Agents

[Hosted agents](/azure/foundry/agents/concepts/hosted-agents) in Microsoft Foundry Agent Service let you deploy containerized agent applications to Microsoft-managed infrastructure. The platform handles scaling, session state persistence, security, and lifecycle management so you can focus on your agent's logic. Microsoft Foundry Hosted Agents is generally available and supports agents built with your own code or a preferred agent framework. This article covers the Agent Framework hosting integration specifically.

By using the Agent Framework hosting integration, you can expose an `Agent` through the Foundry Responses or Invocations protocol with minimal code. Python also supports hosting a native `Workflow` directly, without converting it to an agent.

> [!NOTE]
> You can also deploy agent code built with other frameworks to Foundry hosted agents by using [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) workflows. For framework-agnostic concepts and deployment guidance, see [What are hosted agents?](/azure/foundry/agents/concepts/hosted-agents) The rest of this article focuses on the Agent Framework integration.

## When to use hosted agents

Choose Foundry hosted agents when you want:

- **Managed infrastructure** — no need to configure containers, web servers, or scaling rules yourself.
- **Built-in session management** — the platform persists `$HOME` and uploaded files across turns and idle periods.
- **Dedicated agent identity** — every deployed agent gets its own Entra identity for secure access to models, tools, and downstream services.
- **OpenAI-compatible endpoints** — clients can interact with your agent using any OpenAI-compatible SDK through the Responses protocol.

### Related scenarios

- For real-time audio agents, use hosted agents with Azure Speech in Foundry Tools (Voice Live) for server-side voice activity detection, echo cancellation, and noise reduction. For details, see [Use Voice Live with hosted agents](/azure/ai-services/speech-service/how-to-voice-live-hosted-agent-integration).

> [!NOTE]
> The Python `agent-framework-foundry-hosting` integration is prerelease. Microsoft Foundry Hosted Agents, the managed hosting service, is generally available.

## Prerequisites

- An Azure subscription
- [Azure Developer CLI (`azd`)](/azure/developer/azure-developer-cli/install-azd) with the AI agent extension: `azd ext install azure.ai.agents`

For local testing, you also need:

- A [Microsoft Foundry](/azure/foundry/) project with a model deployment (for example, `gpt-4o`)
- [Azure CLI](/cli/azure/install-azure-cli) installed and authenticated (`az login`)

:::zone pivot="programming-language-csharp"

- [.NET 10 SDK](https://dotnet.microsoft.com/download/dotnet/10.0) or later

Install the hosting NuGet package:

```dotnetcli
dotnet add package Microsoft.Agents.AI.Foundry.Hosting --prerelease
```

:::zone-end

:::zone pivot="programming-language-python"

- Python 3.10 or later

Install the prerelease hosting package, Foundry client, and Azure authentication package:

```bash
pip install --pre agent-framework-foundry agent-framework-foundry-hosting azure-identity
```

:::zone-end

In Foundry, the platform supplies the caller's user context and call context; the hosting infrastructure uses them to isolate state per user and forward request context to Foundry services. Local runs don't receive that platform context, so applications must supply their own identity and state controls when needed.

## Responses protocol

The **Responses** protocol is the recommended starting point for most agents. It exposes an OpenAI-compatible `/responses` endpoint, and the platform manages conversation history, streaming, and session lifecycle automatically.

For Python hosted agents, a response that ends early has an `incomplete` status. Streaming clients receive a terminal `response.incomplete` event, while non-streaming clients receive `status` set to `incomplete`. A `content_filter` finish reason maps to `incomplete_details.reason` set to `content_filter`, and `length` maps to `max_output_tokens`. Any generated output or refusal content remains available in the response.

:::zone pivot="programming-language-csharp"

```csharp
using Azure.AI.AgentServer.Core;
using Azure.AI.Projects;
using Azure.Identity;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;

var projectEndpoint = new Uri(Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT is not set."));
var deployment = Environment.GetEnvironmentVariable("FOUNDRY_MODEL")
    ?? Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? "gpt-4o";

AIAgent agent = new AIProjectClient(projectEndpoint, new DefaultAzureCredential())
    .AsAIAgent(
        model: deployment,
        instructions: "You are a helpful AI assistant.",
        name: "my-agent");

var builder = AgentHost.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.RegisterProtocol("responses", endpoints => endpoints.MapFoundryResponses());

var app = builder.Build();
app.Run();
```

The `AgentHost.CreateBuilder` creates an application host preconfigured for the Foundry hosting environment. `AddFoundryResponses` registers your agent with the Responses protocol handler, and `MapFoundryResponses` maps the `/responses` HTTP endpoint.

:::zone-end

:::zone pivot="programming-language-python"

```python
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL") or os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)

agent = Agent(
    client=client,
    instructions="You are a helpful AI assistant.",
)

server = ResponsesHostServer(agent)
server.run()
```

The `ResponsesHostServer` wraps your agent and exposes it through the Foundry Responses protocol. The caller's `store` field controls whether the outer response and host-managed session and approval state are saved. The `history_source` setting independently selects who supplies model history:

| `history_source` | Model history behavior |
| --- | --- |
| `"agent_server"` (default) | The host reconstructs the stored outer Responses transcript and disables downstream service storage to prevent duplicate history. |
| `"service"` | The host sends only the current input and privately saves the storing model service's continuation ID. A stored provider conversation can't branch from an earlier response. |
| `"agent"` | The host sends only the current input. The agent's `HistoryProvider` or downstream service storage defaults manage history. |

Don't combine `"agent_server"` or `"service"` with a load-enabled `HistoryProvider`. The default mode also rejects fixed downstream continuation options such as `conversation_id`, `previous_response_id`, and `conversation`. Use `history_source="agent"` for a custom `SupportsAgentRun` implementation.

The `response_store` constructor parameter selects the backend for outer Responses persistence. The older constructor parameter `store` is a deprecated alias for `response_store`; neither parameter sets the caller's per-request `store` field. A request with `store=false` is one-shot: it doesn't save host-managed state, disables supported downstream storage, and can't use `background=true`.

The host owns the supplied agent and might add hosting-specific context providers. Don't reuse the agent with another host or invoke it directly after host construction.

The Responses host preserves native computer calls, screenshots, and safety
checks. Your application must execute the requested actions and explicitly
acknowledge any safety checks. For the complete flow, see
[Native computer use](../agents/tools/computer-use.md).

### Choose an agent instance or factory

Both `ResponsesHostServer` and `InvocationsHostServer` accept either an agent instance or a zero-argument synchronous or asynchronous callable through the `agent` parameter. The host reuses an instance for its lifetime. A callable runs once per request, and the returned agent belongs to that request.

Use a callable when the agent retains mutable state outside `AgentSession`. In particular, create a `WorkflowAgent` from a factory that builds a fresh workflow, executors, and wrapped agents:

```python
def create_workflow_agent():
    return build_workflow().as_agent(name="support-workflow")


server = ResponsesHostServer(agent=create_workflow_agent)
```

Keep the workflow name and executor IDs stable so later Responses requests can locate saved checkpoints. `ResponsesHostServer` continues supported state through its session, checkpoint, and function-approval stores; it doesn't persist arbitrary fields on a request-scoped agent. See the [workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/workflows) and [resilient long-running workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/resilient_long_running_workflow) samples.

Also use a factory when an integration carries request identity or owns
request-specific resources. For example, create MCP connections, Toolboxes,
skill providers, Search clients, Memory providers, and their credentials inside
the factory when they use the current platform call or user context. Reusing a
process-wide MCP connection can retain the identity of the request that opened
it.

The host enters and exits factory-created agents for each request. `Agent`
manages context-managed clients and MCP tools, but your factory must close any
other provider, transport, or credential it creates. Don't close shared objects
that the application supplied from outside the factory.

### Host a native workflow with Responses

Python can host a built workflow directly through `workflow=`. A native
workflow requires a `parse_response` callback that maps the current Responses
request to either a typed start input or the complete batch of pending replies:

```python
from pydantic import BaseModel

from agent_framework_foundry_hosting import (
    CheckpointStoreProvider,
    HostedResponseRequest,
    ResponsesHostServer,
    WorkflowTurn,
)


class Ticket(BaseModel):
    text: str


def build_workflow(request: HostedResponseRequest):
    return build_fresh_workflow()


async def parse_response(request: HostedResponseRequest) -> WorkflowTurn[Ticket]:
    items = await request.get_input_items()
    if any(item.get("type") in ("function_call_output", "mcp_approval_response") for item in items):
        return WorkflowTurn(responses=await request.get_workflow_responses())

    text = await request.get_input_text()
    return WorkflowTurn(input=Ticket.model_validate_json(text or ""))


server = ResponsesHostServer(
    workflow=build_workflow,
    parse_response=parse_response,
    checkpoint_store_provider=CheckpointStoreProvider(
        allowed_checkpoint_types=[f"{Ticket.__module__}:{Ticket.__qualname__}"],
    ),
)
```

Use a request-aware synchronous or asynchronous factory for workflows that can
pause, continue, or recover background work. The factory must return a freshly
built graph with fresh mutable executors, agents, clients, providers, and
tools. Keep the workflow name and executor IDs stable so the host can restore
the exact checkpoint associated with the outer response.

The trusted platform user and Foundry
sandbox isolate native workflow state. The host validates a complete pending reply batch before it consumes
any reply authority. Stale, partial, duplicate, replayed, cross-user, and
cross-sandbox replies fail before workflow execution. A request with
`store=false` doesn't save workflow state and can't return a resumable pause.

For a legacy workflow that accepts `list[Message]`, use
`response_input_messages(request)` to convert only the current Responses turn.
It doesn't load prior outer history or decode pending workflow replies. Hosting
`agent=workflow.as_agent()` remains available during the current beta, but
emits a deprecation warning. For complete examples, see the
[native Responses workflow samples](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/workflows).

### Persist state and handle long-running conversations

`ResponsesHostServer` and `InvocationsHostServer` configure persistent session
stores by default. `AgentSessionStoreProvider` supplies a
`FoundryAgentSessionStore`; Responses sessions use the `agent_sessions` logical
store, while Invocations sessions use the separate `invocation_sessions`
store. These stores use Foundry State Store when hosted and the SDK's
file-backed storage when you run locally.

For Responses workflow agents, `CheckpointStoreProvider` supplies a
`FoundryCheckpointStore`. Native Responses and Invocations workflows use the
same provider for their exact continuation checkpoints.
`FunctionApprovalStoreProvider` supplies a `FoundryFunctionApprovalStore` for
pending agent tool approvals. Native workflow request and approval replies are
bound to workflow checkpoints instead.

When running in Foundry, the default Python stores namespace state by the
platform user ID and the Foundry sandbox session ID. They also require a
platform call ID for each state operation. The call ID authorizes and correlates
the operation; it isn't a conversation ID and isn't part of the storage key.

For Responses, the platform-configured `FOUNDRY_AGENT_SESSION_ID` identifies the
sandbox, and a different caller-supplied `agent_session_id` is rejected. For
Invocations, the host verifies the routed `agent_session_id` query parameter
against the request context. If `FOUNDRY_AGENT_SESSION_ID` isn't configured, the
query parameter must be present, nonempty, and match the request context.
Missing, duplicate, or conflicting values are rejected instead of using an SDK
fallback ID.

These guarantees apply to the default hosted stores. Custom store providers
must implement equivalent user and sandbox isolation, preserve the inner
`AgentSession.session_id` separately from host lookup keys, and use conditional
writes so stale requests can't overwrite newer snapshots. New keys should use
create-only writes rather than unconditional upserts. See the
[custom storage sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/custom_storage)
for a Cosmos DB implementation with ETag-protected writes and deletes.

With `history_source="agent"`, the configured session store persists provider state carried by `AgentSession`, including messages from `InMemoryHistoryProvider`.

Both hosts accept a `StoreProvider[SessionStore]` through
`agent_session_store_provider`. Session state must support `AgentSession`
serialization. Register codecs for custom state types with
`register_state_type()`; restored state doesn't preserve Python object
identity. New default stores expire sessions 30 days after their last write.
Custom providers control their own retention.

The scoped default stores don't read legacy unscoped `agent_sessions`,
`invocation_sessions`, checkpoint, or function-approval data. Start a fresh
Responses conversation instead of reusing an old `previous_response_id` or
conversation ID. Invocations starts with an empty Agent Framework session in
the scoped store.

Loaded `AgentSession` records use ETag conditions. If another request advances
the same session first, the stale write fails instead of overwriting newer
state. This check doesn't provide transactions or exactly-once execution for
agent or tool side effects, so applications must still coordinate overlapping
requests.

For Responses-specific storage, pass a `StoreProvider` to
`function_approval_store_provider` or a `ContextScopedStoreProvider` to
`checkpoint_store_provider`.

Outer background work uses the caller-visible `response.id` for polling. The default `background_source="agent_server"` keeps background execution in the host. Set `background_source="provider"` only with `history_source="service"` and a storing, resumable Responses client. If `ResponsesServerOptions(resilient_background=True)` is also set, the host can recover provider polling only after it saves the private continuation token. Make local tool side effects idempotent because a crash before the next token is saved can replay them.

Import `ResponsesServerOptions` from `azure.ai.agentserver.responses`, and pass it to `ResponsesHostServer` through the `options` parameter. The available long-running conversation options depend on the agent type:

| Capability | Agent type | Requirements and behavior |
| --- | --- | --- |
| Workflow checkpoint background recovery | Workflow only | Set `ResponsesServerOptions(resilient_background=True)`. Send the Responses request with `store=true` and `background=true`. After a restart, the host resumes the latest durable workflow checkpoint or replays the original input if no checkpoint exists. Don't configure checkpoint storage on the workflow because the host manages it. Make external side effects idempotent because work after the last durable checkpoint might repeat. |
| Provider-native background responses | Non-workflow `Agent` with a storing Responses client | Set `history_source="service"` and `background_source="provider"`. Set `resilient_background=True` when saved provider continuation tokens must survive a host restart. |
| Steerable conversations | Temporarily unavailable | Don't set `steerable_conversations=True`. The host raises `RuntimeError` during construction until the Agent Server SDK safely handles rejected steering turns. |

For complete implementations, see the [custom storage](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/custom_storage), [basic Responses history and background](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/basic), and [resilient long-running workflow](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/resilient_long_running_workflow) samples.

### Read files from the hosted sandbox

Treat a hosted sandbox's persistent `$HOME` as a request-routed resource, not as
a general file-system boundary. Accept only files that your application
explicitly uploads to a dedicated directory, validate the current sandbox
identity, and reject absolute paths, traversal, links, nonregular files, and
oversized or invalid content.

For the Responses protocol, route a request to a hosted session with the
`agent_session_id` body field. The query-string selector is for Invocations.
Session uploads and Toolbox code-interpreter files are separate resources; an
uploaded sandbox file isn't automatically mounted into a Toolbox container.
See the
[session files sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/responses/files)
for bounded UTF-8 reads and local and hosted upload guidance.

### Control request options

The host maps native Responses generation fields to Agent Framework run options. For example, `max_output_tokens` becomes `max_tokens`, and `parallel_tool_calls` becomes `allow_multiple_tool_calls`. Flattened values from `extra_body` override translated native values.

Use the synchronous or asynchronous `prepare_options(request, options)` hook to remove or replace caller model options before a regular agent runs. The hook can't set host-controlled identity, storage, continuation, or transport fields. For a custom `SupportsAgentRun` implementation that can't accept runtime model options, set `unsupported_options` to `"warn"` (the default), `"ignore"`, or `"error"`.

### Handle OAuth consent requests

When a Foundry-hosted MCP tool requires user consent, `ResponsesHostServer` returns an incomplete response with an `oauth_consent_request` output item. Present its `consent_link` to the user, then continue with the incomplete response's ID as `previous_response_id` after the user completes consent. The host preserves the agent session for this retry and exposes only absolute HTTPS consent links.

If your host knows the expected authorization origins, restrict consent links with `allowed_oauth_consent_origins`:

```python
server = ResponsesHostServer(
    agent,
    allowed_oauth_consent_origins=[
        "https://logic-region.consent.azure-apihub.net",
        "https://auth.partner.example",
    ],
)
```

Omitting the allow list keeps the absolute-HTTPS validation without restricting the destination origin. Providing an empty list rejects every consent link. Configure exact HTTPS origins only; entries with a path, query, or fragment are rejected.

:::zone-end

## Invocations protocol

The **Invocations** protocol gives you full control over the HTTP request and response. Use it when you need custom payloads, non-conversational processing, or streaming protocols that aren't OpenAI-compatible.

:::zone pivot="programming-language-csharp"

With the Invocations protocol in C#, you implement a custom `InvocationHandler` to process incoming requests:

```csharp
using Azure.AI.AgentServer.Core;
using Azure.AI.AgentServer.Invocations;
using Microsoft.Agents.AI;

var builder = AgentHost.CreateBuilder(args);

builder.Services.AddSingleton<AIAgent, MyAgent>();
builder.Services.AddInvocationsServer();
builder.Services.AddScoped<InvocationHandler, MyInvocationHandler>();

builder.RegisterProtocol("invocations", endpoints => endpoints.MapInvocationsServer());

var app = builder.Build();
app.Run();
```

The `AddInvocationsServer` method registers the Invocations protocol services. You implement `InvocationHandler` to define how your agent processes each request.

:::zone-end

:::zone pivot="programming-language-python"

For a lightweight setup, use `InvocationsHostServer` from the `agent_framework_foundry_hosting` package. It wraps your agent similarly to `ResponsesHostServer` and handles session management automatically:

```python
import os

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import InvocationsHostServer
from azure.identity import DefaultAzureCredential

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL") or os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)

agent = Agent(
    client=client,
    instructions="You are a friendly assistant. Keep your answers brief.",
    default_options={"store": False},
)

server = InvocationsHostServer(agent)
server.run()
```

`InvocationsHostServer` accepts the same instance or request-scoped factory
forms described for the Responses host. It restores serialized sessions from
the configured store, so completed conversations can continue after the host
restarts. For storage behavior, retention, and customization, see
[Persist state and handle long-running conversations](#persist-state-and-handle-long-running-conversations).

When hosted, Invocations uses the verified request scope described in
[Persist state and handle long-running conversations](#persist-state-and-handle-long-running-conversations).
Treat `AgentSession.session_id` as one opaque value; don't parse or depend on
its internal representation. Local runs keep their existing single-user
storage behavior.

### Host a native workflow with Invocations

Pass `workflow=` and an explicit `parse_request` callback to host a native
workflow. The callback owns the application JSON schema and returns a
`WorkflowTurn` with either typed input or the complete pending reply batch:

```python
from pydantic import BaseModel
from starlette.requests import Request

from agent_framework_foundry_hosting import (
    CheckpointStoreProvider,
    InvocationsHostServer,
    WorkflowTurn,
)


class Ticket(BaseModel):
    ticket_id: str
    question: str


class TicketDecision(BaseModel):
    approved: bool


def build_workflow(_request: Request):
    return build_fresh_workflow()


async def parse_request(request: Request) -> WorkflowTurn[Ticket]:
    payload = await request.json()
    stream = payload.get("stream", False)

    if "responses" in payload:
        decisions = {
            request_id: TicketDecision.model_validate(value)
            for request_id, value in payload["responses"].items()
        }
        return WorkflowTurn(responses=decisions, stream=stream)

    ticket = Ticket.model_validate(payload)
    return WorkflowTurn(input=ticket, stream=stream)


server = InvocationsHostServer(
    workflow=build_workflow,
    parse_request=parse_request,
    checkpoint_store_provider=CheckpointStoreProvider(
        allowed_checkpoint_types=[
            f"{Ticket.__module__}:{Ticket.__qualname__}",
            f"{TicketDecision.__module__}:{TicketDecision.__qualname__}",
        ],
    ),
)
```

Include every custom application type that the workflow saves in the
checkpoint provider's `allowed_checkpoint_types` list.

Hosted workflows require a request-aware factory that returns a fresh built
graph with stable workflow and executor IDs. A direct built workflow is
available only for a local, one-shot run that doesn't pause.

Non-streaming workflow responses use application JSON with an `output` event
list. Streaming emits framed `output` and `request_info` events, followed by
`done` only after the exact workflow cursor is saved. Treat streamed output as
provisional until `done`. Native workflows don't support
`legacy_wire_format=True`.

The host validates replies against the exact pending checkpoint in the trusted
user and sandbox scope. If a workflow has multiple pending requests, reply to
the complete batch in one turn. For a runnable parser, typed ticket workflow,
checkpoint type allow list, and JSON/SSE examples, see the
[native Invocations workflow sample](https://github.com/microsoft/agent-framework/blob/main/python/samples/04-hosting/foundry-hosted-agents/invocations/basic/README.md#native-workflow-with-typed-tickets).

### Customize Invocations requests and responses

By default, `POST /invocations` accepts a JSON object with a string `message`,
an optional `options` object, and an optional Boolean `stream` value. To accept
an application-specific payload, pass a synchronous or asynchronous
`parse_request` callback that returns
`InvocationRun(messages, options, stream)`. Use `prepare_options` to filter or
replace a copy of caller generation options before the agent runs.

The host validates the hook output and rejects platform identity, storage,
continuation, and agent-execution controls. For agents that don't accept
runtime options, set `unsupported_options` to `"warn"` (the default),
`"ignore"`, or `"error"`. See the
[Invocations parser sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/invocations/basic)
for a complete implementation.

Non-streaming success returns JSON in the form `{"response": "..."}`.
Streaming uses server-sent events: one or more `event: delta` frames, followed
by `event: done` on success or `event: error` on failure. A stream can emit
deltas before an error, so clients must treat `done`, not a delta, as successful
completion. The host emits `done` only after it finalizes the response stream
and persists the `AgentSession`. Its `session_id` is the platform sandbox route
ID, not the serialized `AgentSession.session_id`.

Set `legacy_wire_format=True` only while migrating existing clients that require
the previous plain-text response and raw text-chunk stream. This compatibility
mode is deprecated and doesn't convert failures into successful text. The host
serializes same-session requests only within one process; a cross-process
compare-and-swap conflict can still occur after external tool effects.

The Invocations protocol doesn't resume workflow runs that are pending or
interrupted. Use the custom handler pattern in the following section when you
need different workflow continuation behavior.

For full control over request handling, use `InvocationAgentServerHost` from the `azure.ai.agentserver.invocations` package directly and implement your own invoke handler:

```python
import os
from collections.abc import AsyncGenerator

from agent_framework import Agent, AgentSession
from agent_framework.foundry import FoundryChatClient
from azure.ai.agentserver.invocations import InvocationAgentServerHost
from azure.identity import DefaultAzureCredential
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse

_sessions: dict[str, AgentSession] = {}

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ.get("FOUNDRY_MODEL") or os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)

agent = Agent(
    client=client,
    instructions="You are a friendly assistant. Keep your answers brief.",
    default_options={"store": False},
)

app = InvocationAgentServerHost()


@app.invoke_handler
async def handle_invoke(request: Request):
    """Handle streaming multi-turn chat."""
    data = await request.json()
    session_id = request.state.session_id
    stream = data.get("stream", False)
    user_message = data.get("message", None)

    if user_message is None:
        return Response(content="Missing 'message' in request", status_code=400)

    session = _sessions.setdefault(session_id, AgentSession(session_id=session_id))

    if stream:

        async def stream_response() -> AsyncGenerator[str]:
            async for update in agent.run(user_message, session=session, stream=True):
                yield update.text

        return StreamingResponse(
            stream_response(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    response = await agent.run([user_message], session=session, stream=stream)
    return JSONResponse({"response": response.text})


if __name__ == "__main__":
    app.run()
```

> [!WARNING]
> The in-memory session store in the custom handler example is lost on restart. Use durable storage (for example, Cosmos DB) in production.

For a complete Invocations deployment, see the [Foundry-hosted Telegram sample](https://github.com/microsoft/agent-framework/tree/main/python/samples/04-hosting/foundry-hosted-agents/invocations/telegram). It places API Management in front of the hosted agent webhook and uses managed identities, Key Vault, and Cosmos DB for durable conversation history.

:::zone-end

:::zone pivot="programming-language-go"

> [!NOTE]
> Go support for Foundry hosted agents is coming soon. See the [Agent Framework Go repository](https://github.com/microsoft/agent-framework-go) for the latest status.

:::zone-end

> [!TIP]
> Refer to the [Python samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework) or the [C# samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework) for examples of a hosted agent project. Or use the `azd ai agent init` command to scaffold a new hosted agent project from scratch. Refer to this [quickstart guide](/azure/foundry/agents/quickstarts/quickstart-hosted-agent?pivots=azd) for step-by-step instructions.

## Running locally

The Azure Developer CLI (`azd`) provides the easiest way to run and test your hosted agent locally.

### Initialize a project

Create a new folder and initialize from a sample manifest:

```bash
mkdir my-hosted-agent && cd my-hosted-agent
azd ai agent init -m <path-to-agent.manifest.yaml>
```

> [!TIP]
> The manifest can be a path to a local YAML file or a URL to a remote manifest.

### Set environment variables

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_MODEL="<your-model-deployment>"
```

### Run the agent host

```bash
azd ai agent run
```

The agent host starts on `http://localhost:8088`.

### Invoke the agent

```bash
azd ai agent invoke --local "Hello!"
```

Or use `curl`:

```bash
curl -X POST http://localhost:8088/responses \
  -H "Content-Type: application/json" \
  -d '{"input": "Hello!"}'
```

Or in PowerShell:

```powershell
(Invoke-WebRequest -Uri http://localhost:8088/responses -Method POST -ContentType "application/json" -Body '{"input": "Hello!"}').Content
```

## Deploying to Foundry

Once you've verified your agent locally, deploy it to Microsoft Foundry:

1. **Provision resources** (if you don't already have a Foundry project):

   ```bash
   azd provision
   ```

   This creates a resource group with a Foundry instance, project, model deployment, Application Insights, and a container registry.

2. **Deploy the agent:**

   ```bash
   azd deploy
   ```

   This packages your agent as a container image, pushes it to Azure Container Registry, and deploys it to Foundry Agent Service.

The Foundry hosting infrastructure automatically injects the following environment variables into your agent container at runtime:

| Variable | Description |
|----------|-------------|
| `FOUNDRY_PROJECT_ENDPOINT` | The endpoint URL for the Foundry project. |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME` | The azd-managed model deployment name configured during `azd ai agent init`. Python code can prefer `FOUNDRY_MODEL` locally and fall back to this hosted value. |
| `APPLICATIONINSIGHTS_CONNECTION_STRING` | The Application Insights connection string for telemetry. |

Once deployed, your agent is accessible through its dedicated Foundry endpoint and can also be tested from the Foundry portal.

## Next steps

> [!div class="nextstepaction"]
> [Hosted agents concepts](/azure/foundry/agents/concepts/hosted-agents)

- [Deploy a hosted agent with the Foundry SDK](/azure/foundry/agents/how-to/deploy-hosted-agent)
- [Manage hosted agents](/azure/foundry/agents/how-to/manage-hosted-agent)
- [Azure Functions and durable hosting](azure-functions.md)
- [Self-host A2A agents](self-hosting/a2a/index.md)
- [Python samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework)
- [C# samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework)
