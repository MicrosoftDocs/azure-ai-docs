---
title: "Migrate hosted agents to the refreshed public preview"
description: "Migrate your hosted agents from the initial public preview to the refreshed public preview, including API, SDK, CLI, protocol library, and identity model changes."
author: aahill
ms.author: aahi
ms.date: 04/15/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
---

# Migrate hosted agents to the refreshed public preview

This article walks you through migrating hosted agents from the initial public preview to the refreshed public preview of Foundry Agent Service. The refreshed preview introduces a new hosting backend, protocol libraries, identity model, and management APIs.

> [!IMPORTANT]
> The initial public preview hosting backend is being retired. You must redeploy your agents using the new model described in this article. Existing agent deployments on the old backend won't be migrated automatically.

This guide applies to you if you deployed a hosted agent before April 2026 using the `azure-ai-agentserver-agentframework` or `azure-ai-agentserver-langgraph` packages, or any custom code that used the initial preview hosting APIs.

## What changed

The refreshed preview updates the existing platform with a session-based sandbox model. Key changes:

- **Automatic compute lifecycle** — No manual start, stop, or replica management. The platform provisions compute when a request arrives and deprovisions it after 15 minutes of inactivity. See [CLI command mapping](#cli-command-mapping).
- **Session-based isolation** — Each session gets its own sandbox with persistent `$HOME` and `/files` storage across turns and idle periods.
- **Protocol libraries replace framework adapters** — The framework-specific adapter packages (`azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`) are replaced by protocol-specific libraries (`azure-ai-agentserver-responses`, `azure-ai-agentserver-invocations`). See [Protocol library and framework migration](#protocol-library-and-framework-migration).
- **Dedicated agent identity from deploy time** — Every agent gets its own Entra identity at creation, replacing the shared project managed identity model. See [Identity and RBAC changes](#identity-and-rbac-changes).
- **Dedicated agent endpoint** — Each agent gets its own endpoint URL (`{project_endpoint}/agents/{name}/endpoint/protocols/responses`). You no longer route through a shared project endpoint with `agent_reference` in the request body. See [Agent invocation changes](#agent-invocation-changes).
- **New protocols** — Invocations, Activity, and A2A protocols join the existing Responses protocol. A single agent can expose multiple protocols simultaneously.
- **REST API for full lifecycle** — Complete REST coverage for agent, version, session, and file operations. See [SDK method changes](#sdk-method-changes).
- **Capability host creation removed** — The platform handles infrastructure provisioning automatically. You no longer need to create an account-level capability host. See [Removed APIs](#removed-apis).

## Prerequisites

- [Azure AI Projects SDK](https://pypi.org/project/azure-ai-projects/) version 2.1.0 or later (was 2.0.0).
- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later with the updated Foundry agents extension:

    ```bash
    azd ext install azure.ai.agents
    ```

## Migration steps at a glance

The following steps summarize the end-to-end migration. Each links to the detailed section.

1. **Update protocol libraries and agent code** — Replace framework adapters with the new protocol libraries and update your agent entry point. Choose your path: [Agent Framework](#migrate-agent-framework-agents), [LangGraph](#migrate-langgraph-agents), or [custom/BYO](#migrate-custom-or-byo-agents).
1. **Update API, CLI, and SDK calls** — Remove retired CLI commands, update SDK methods, and switch to the dedicated agent endpoint. See [Removed APIs](#removed-apis), [CLI command mapping](#cli-command-mapping), [SDK method changes](#sdk-method-changes), and [Agent invocation changes](#agent-invocation-changes).
1. **Update identity and RBAC** — Grant downstream resource access to the agent's dedicated Entra identity. See [Identity and RBAC changes](#identity-and-rbac-changes).
1. **Update Azure Developer CLI tooling** — Install the latest `azd` Foundry agents extension and update `agent.yaml`. See [Azure Developer CLI changes](#azure-developer-cli-changes).
1. **Redeploy and verify** — Build your container image, deploy using `azd up` or the SDK, and confirm the version reaches `active` status.

For a task-by-task summary, see the [Migration checklist](#migration-checklist) at the end of this article.

## Protocol library and framework migration

The initial preview used framework-specific adapter packages (`azure-ai-agentserver-agentframework`, `azure-ai-agentserver-langgraph`) that wrapped your agent code. The refreshed preview replaces these with protocol-specific libraries and updated framework integration packages.

Your migration path depends on which framework you use:

- **Microsoft Agent Framework** — Use the updated Agent Framework packages with the `ResponsesHostServer` bridge.
- **LangGraph** — Use the `azure-ai-agentserver-responses` protocol library directly with `ResponsesAgentServerHost`.
- **CrewAI, Semantic Kernel, or custom code** — Use the protocol libraries directly (`azure-ai-agentserver-responses` or `azure-ai-agentserver-invocations`).

### Package changes

#### Protocol libraries (all users)

| Initial preview package | Refreshed preview replacement |
|-------------------------|-------------------------------|
| `azure-ai-agentserver-core` | `azure-ai-agentserver-core` 2.0.0b1 — still required, now installed automatically as a dependency of the protocol packages |
| `azure-ai-agentserver-agentframework` | Removed — see Agent Framework or protocol library paths below |
| `azure-ai-agentserver-langgraph` | Removed — use `azure-ai-agentserver-responses` or `azure-ai-agentserver-invocations` directly |
| `Azure.AI.AgentServer.Core` (.NET) | `Azure.AI.AgentServer.Core` 1.0.0-beta.21 — still required as a dependency |
| `Azure.AI.AgentServer.AgentFramework` (.NET) | `Azure.AI.AgentServer.Responses` 1.0.0-beta.1 or `Azure.AI.AgentServer.Invocations` 1.0.0-beta.1 |

#### Agent Framework packages (Agent Framework users only)

The Agent Framework packages were also updated for the refreshed preview:

| Initial preview | Refreshed preview |
|-----------------|-------------------|
| `agent-framework` (single package) | `agent-framework-core`, `agent-framework-openai`, `agent-framework-foundry`, `agent-framework-orchestrations` |
| `AzureAIAgentClient` | `FoundryChatClient` (from `agent_framework.foundry`) |
| `ChatAgent` | `Agent` (from `agent_framework`) |
| `@ai_function` decorator | `@tool` decorator with `approval_mode` parameter |
| Not available | `agent-framework-foundry-hosting` — bridge between Agent Framework and the protocol library |

## Migrate Agent Framework agents

If your agent uses the Microsoft Agent Framework, use the `ResponsesHostServer` bridge from `agent-framework-foundry-hosting`. This approach keeps your Agent Framework code (agent definition, tools, instructions) intact while using the new protocol library under the hood.

**Initial preview**:

```python
from azure.ai.agentserver.agentframework import from_agent_framework
from agent_framework import ai_function, ChatAgent
from agent_framework.azure import AzureAIAgentClient

client = AzureAIAgentClient(
    project_endpoint=PROJECT_ENDPOINT,
    model_deployment_name="gpt-4.1",
    credential=DefaultAzureCredential(),
)

@ai_function
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."

agent = ChatAgent(
    chat_client=client,
    instructions="You are a helpful assistant.",
    tools=[get_weather],
)

if __name__ == "__main__":
    from_agent_framework(agent).run()
```

**Refreshed preview**:

```python
import os

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.ai.agentserver.responses import InMemoryResponseProvider
from azure.identity import DefaultAzureCredential
from pydantic import Field
from typing_extensions import Annotated

client = FoundryChatClient(
    project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    credential=DefaultAzureCredential(),
)


@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."


agent = Agent(
    client=client,
    instructions="You are a helpful assistant.",
    tools=[get_weather],
    default_options={"store": False},
)

server = ResponsesHostServer(agent, store=InMemoryResponseProvider())
server.run()
```

Key differences:

- `AzureAIAgentClient` → `FoundryChatClient` (from `agent_framework.foundry`).
- `ChatAgent` → `Agent` (from `agent_framework`).
- `@ai_function` → `@tool(approval_mode="never_require")` with `Annotated` type hints for parameter descriptions.
- `from_agent_framework(agent).run()` → `ResponsesHostServer(agent, store=InMemoryResponseProvider()).run()`.
- Add `default_options={"store": False}` because conversation history is managed by the hosting platform.

For MCP tools, use `client.get_mcp_tool()` instead of defining tools in the `create_version` API:

```python
mcp_tool = client.get_mcp_tool(
    name="GitHub",
    url="https://api.githubcopilot.com/mcp/",
    headers={"Authorization": f"Bearer {github_pat}"},
    approval_mode="never_require",
)

agent = Agent(client=client, tools=[mcp_tool], ...)
```

For samples, see the [Agent Framework hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework).

> [!NOTE]
> For .NET (C#) Agent Framework migration, the pattern uses `AddFoundryResponses` and `MapFoundryResponses` ASP.NET extensions instead of `ResponsesHostServer`. See the [.NET Agent Framework hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/AgentFramework) for complete examples.

## Migrate LangGraph agents

If your agent uses LangGraph, replace the `azure-ai-agentserver-langgraph` adapter with the `azure-ai-agentserver-responses` protocol library. Your LangGraph agent logic (graph definition, tools, LLM configuration) stays the same — only the hosting entry point changes.

**Initial preview**:

```python
from azure.ai.agentserver.langgraph import from_langgraph
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(azure_endpoint=ENDPOINT, azure_deployment="gpt-4o", ...)
tools = [my_tool_a, my_tool_b]
graph = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)

if __name__ == "__main__":
    from_langgraph(graph).run()
```

**Refreshed preview**:

```python
import asyncio
import os
from collections.abc import AsyncIterable
from typing import Any

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponseEventStream,
    ResponsesAgentServerHost,
)
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_openai import AzureChatOpenAI
from langgraph.prebuilt import create_react_agent

llm = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "gpt-4.1"),
    api_version="2024-10-21",
    azure_ad_token_provider=get_bearer_token_provider(
        DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    ),
)
tools = [my_tool_a, my_tool_b]
app = ResponsesAgentServerHost()


@app.response_handler
async def handle(
    request: CreateResponse,
    context: ResponseContext,
    cancellation_signal: asyncio.Event,
) -> AsyncIterable[dict[str, Any]]:
    user_input = await context.get_input_text()
    graph = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)

    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_input}]},
    )

    # Extract the final AI message from the graph result
    messages = result.get("messages", [])
    answer = ""
    for msg in reversed(messages):
        if hasattr(msg, "content") and getattr(msg, "type", None) == "ai":
            answer = msg.content
            break

    stream = ResponseEventStream(
        response_id=context.response_id,
        model=request.model or "gpt-4.1",
    )
    yield stream.emit_created()
    yield stream.emit_in_progress()
    message_item = stream.add_output_item_message()
    yield message_item.emit_added()
    text_content = message_item.add_text_content()
    yield text_content.emit_added()
    yield text_content.emit_delta(answer)
    yield text_content.emit_text_done(answer)
    yield text_content.emit_done()
    yield message_item.emit_done()
    yield stream.emit_completed()


if __name__ == "__main__":
    app.run()
```

Key differences:

- `azure-ai-agentserver-langgraph` → `azure-ai-agentserver-responses`. The LangGraph-specific adapter is removed.
- `from_langgraph(graph).run()` → Explicit `ResponsesAgentServerHost` with a `@app.response_handler` that invokes the graph and yields `ResponseEventStream` events.
- You now control how input is extracted (`context.get_input_text()`) and how output is streamed. This gives full flexibility for multi-turn, tool-calling, and streaming patterns.
- LangGraph agent logic (model, tools, graph creation) is unchanged.

### MCP Toolbox integration

To connect your LangGraph agent to tools in the Foundry Toolbox via MCP, use `langchain-mcp-adapters` inside your handler. Load tools dynamically from the MCP endpoint:

```python
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


@app.response_handler
async def handle(request, context, cancellation_signal):
    user_input = await context.get_input_text()
    endpoint = os.environ["TOOLBOX_ENDPOINT"]
    token = DefaultAzureCredential().get_token("https://ai.azure.com/.default").token
    headers = {
        "Authorization": f"Bearer {token}",
        "Foundry-Features": "Toolsets=V1Preview",
    }

    async with streamablehttp_client(endpoint, headers=headers) as (r, w, _):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            graph = create_react_agent(llm, tools=tools, prompt=SYSTEM_PROMPT)
            result = await graph.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
            )
            # ... extract answer and yield ResponseEventStream events
```

Add these packages to your `requirements.txt`:

```
langchain-mcp-adapters>=0.1.0
mcp>=1.0.0
```

For complete samples, see the [LangGraph hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/langchain).

## Migrate custom or BYO agents

If you use CrewAI, Semantic Kernel, or other custom code, use the protocol library directly. The protocol libraries are framework-agnostic — you handle orchestration, tools, and memory in your own code.

**Responses protocol** — Use `ResponsesAgentServerHost` for conversational agents. Register your handler with the `@app.response_handler` decorator:

```python
import asyncio

from azure.ai.agentserver.responses import (
    CreateResponse,
    ResponseContext,
    ResponsesAgentServerHost,
    TextResponse,
)

app = ResponsesAgentServerHost()


@app.response_handler
async def handler(
    request: CreateResponse,
    context: ResponseContext,
    cancellation_signal: asyncio.Event,
):
    text = await context.get_input_text()
    return TextResponse(context, request, text=f"Echo: {text}")


app.run()
```

For streaming responses, pass an async iterable to `TextResponse`. For fine-grained control over function calls, reasoning items, or multiple output types, use `ResponseEventStream` instead of `TextResponse`.

**Invocations protocol** — Use `InvocationAgentServerHost` for agents that need arbitrary JSON payloads (webhooks, non-conversational processing). The handler uses Starlette `Request`/`Response` types directly:

```python
from azure.ai.agentserver.invocations import InvocationAgentServerHost
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = InvocationAgentServerHost()


@app.invoke_handler
async def handle(request: Request) -> Response:
    data = await request.json()
    return JSONResponse({"greeting": f"Hello, {data['name']}!"})


app.run()
```

The Invocations protocol also supports long-running operations with `@app.get_invocation_handler` and `@app.cancel_invocation_handler` for polling and cancellation.

Choose your protocol based on your agent's interaction pattern. See [What are hosted agents — Protocols](../concepts/hosted-agents.md#protocols-responses-and-invocations) for guidance on which protocol to use.

## Protocol version format change

The protocol version format changed from `"v1"` to semver `"1.0.0"`:

```python
# Initial preview
ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")

# Refreshed preview
ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="1.0.0")
```

## Removed APIs

The following APIs from the initial preview aren't available in the refreshed preview:

| Removed API | Reason |
|-------------|--------|
| `az cognitiveservices agent start` | Compute lifecycle is automatic — no manual start needed |
| `az cognitiveservices agent stop` | Compute deprovisions automatically after 15 minutes of inactivity |
| `az cognitiveservices agent update` | Replaced by `PATCH /agents/{name}` for endpoint routing; create a new version for runtime changes |
| `az cognitiveservices agent delete-deployment` | Delete the version directly instead |
| `az cognitiveservices agent list-versions` | Use `az rest --method GET` against the REST API |
| `az cognitiveservices agent show` | Use `az rest --method GET` or `azd ai agent show` |
| Capability host creation (`PUT .../capabilityHosts/accountcaphost`) | Platform handles infrastructure automatically |
| `tools` parameter in `create_version` | Tools are accessed via Foundry Toolbox MCP endpoint at runtime |

## CLI command mapping

| Initial preview CLI | Refreshed preview equivalent |
|---------------------|------------------------------|
| `az cognitiveservices agent start --name X --agent-version 1` | Removed — compute starts automatically on first request |
| `az cognitiveservices agent stop --name X --agent-version 1` | Removed — compute stops automatically after idle timeout |
| `az cognitiveservices agent update --min-replicas N --max-replicas M` | Removed — no replica management |
| `az cognitiveservices agent show --name X` | `az rest --method GET --url "$BASE_URL/agents/X" --resource "https://ai.azure.com"` |
| `az cognitiveservices agent list-versions --name X` | `az rest --method GET --url "$BASE_URL/agents/X/versions" --resource "https://ai.azure.com"` |
| `az cognitiveservices agent delete --name X` | `az rest --method DELETE --url "$BASE_URL/agents/X" --resource "https://ai.azure.com"` |
| `az cognitiveservices agent delete --name X --agent-version 1` | `az rest --method DELETE --url "$BASE_URL/agents/X/versions/1" --resource "https://ai.azure.com"` |
| `az cognitiveservices agent delete-deployment --name X --agent-version 1` | Removed — delete the version instead |

Where `BASE_URL` is `https://{account}.services.ai.azure.com/api/projects/{project}`.

## SDK method changes

| Initial preview | Refreshed preview |
|-----------------|-------------------|
| `pip install "azure-ai-projects>=2.0.0"` | `pip install "azure-ai-projects>=2.1.0"` |
| `project.get_openai_client()` with `extra_body={"agent_reference": {"name": ..., "type": "agent_reference"}}` | `project.get_openai_client(agent_name="my-agent")` — client is pre-bound, no `extra_body` needed |
| `ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="v1")` | `ProtocolVersionRecord(protocol=AgentProtocol.RESPONSES, version="1.0.0")` |
| `tools=[...]` in `HostedAgentDefinition` | Removed — use Foundry Toolbox MCP endpoint instead |
| Not available | `project.beta.agents.create_session(agent_name, isolation_key=..., version_indicator=...)`, `.get_session()`, `.list_sessions()`, `.delete_session(isolation_key=...)` |
| Not available | `project.beta.agents.download_session_file(path=...)`, `.list_session_files(path=...)`, `.delete_session_file(path=...)` |
| Not available | `project.beta.agents.patch_agent_object()` for endpoint routing and traffic splitting |
| Not available | `metadata={"enableVnextExperience": "true"}` parameter on `client.agents.create_version()` |

## Agent invocation changes

In the initial preview, you routed to agents through a shared project endpoint by passing an `agent_reference` in the request body. In the refreshed preview, each agent gets a dedicated endpoint and the SDK binds to it automatically.

**Initial preview**:

```python
openai_client = project.get_openai_client()
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Hello!"}],
    extra_body={"agent_reference": {"name": "my-agent", "type": "agent_reference"}}
)
```

**Refreshed preview**:

```python
openai_client = project.get_openai_client(agent_name="my-agent")
response = openai_client.responses.create(
    input="Hello!",
)
print(response.output_text)
```

> [!NOTE]
> Using `agent_name` requires `allow_preview=True` when constructing the `AIProjectClient`:
>
> ```python
> project = AIProjectClient(
>     credential=DefaultAzureCredential(),
>     endpoint=PROJECT_ENDPOINT,
>     allow_preview=True,
> )
> ```

The `agent_name` parameter tells the SDK to target the agent's dedicated endpoint. For REST calls, use the agent endpoint directly:

```bash
curl -X POST "$BASE_URL/agents/my-agent/endpoint/protocols/openai/responses?api-version=$API_VERSION" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Foundry-Features: HostedAgents=V1Preview" \
  -d '{"input": "Hello!", "model": "gpt-4.1", "stream": false}'
```

> [!IMPORTANT]
> REST calls to hosted agent endpoints require the `Foundry-Features: HostedAgents=V1Preview` header during preview. Without it, the request returns a `preview_feature_required` error. The SDK sets this header automatically.

The endpoint URL format is `{project_endpoint}/agents/{name}/endpoint/protocols/{protocol}`. Active endpoints depend on which protocols you declare in your agent version definition.

## Version status changes

The agent lifecycle states changed from a manual state machine to automatic provisioning statuses:

| Initial preview state | Refreshed preview status |
|-----------------------|--------------------------|
| `Stopped` (initial) | Not applicable — no stopped state |
| `Starting` → `Started` | `creating` → `active` |
| `Failed` | `failed` |
| `Running` → `Stopping` → `Stopped` | Not applicable — compute deprovisions automatically |
| Not available | `deleting` → `deleted` |

## Identity and RBAC changes

The identity model changed significantly:

| Aspect | Initial preview | Refreshed preview |
|--------|-----------------|-------------------|
| **Unpublished agent runtime identity** | Project managed identity (shared) | Dedicated Entra agent identity (per agent) |
| **When dedicated identity is created** | At publish time only | At deploy time (every agent) |
| **Project managed identity role** | Runtime identity for all unpublished agents | Infrastructure only — used for container image pulls |
| **Required deployment role** | Azure AI Owner (new project), AI Owner + Contributor (new resources), or Reader + Azure AI User (existing project) | **Azure AI User** at project scope |
| **Post-publish RBAC reconfiguration** | Required — project MI permissions don't transfer to agent identity | Not required — agent has its own identity from the start |

### Action required

1. **Update RBAC assignments**: The project managed identity is no longer the runtime identity. Grant RBAC roles for any downstream Azure resources directly to the agent's Entra identity instead.
2. **Simplify deployment roles**: You need only **Azure AI User** at project scope to create and deploy hosted agents.

## Azure Developer CLI changes

### Updated commands

| Initial preview | Refreshed preview |
|-----------------|-------------------|
| `azd init -t https://github.com/Azure-Samples/azd-ai-starter-basic` | `azd ai agent init` (interactive template selection) |
| `azd ai agent init --project-id /subscriptions/.../projects/...` | Same syntax, still supported |
| `azd up` | Same — provisions, builds, pushes, creates version |
| `azd down` | Same — cleans up resources |
| Not available | `azd ai agent show` — view agent status |
| Not available | `azd ai agent monitor` — real-time logs and status |
| Not available | `azd ai agent invoke --input "..."` — invoke the agent |
| Not available | `azd ai agent files upload/list/download/remove` — session file management |

### Action required

1. Update the Foundry agents extension:

    ```bash
    azd ext install azure.ai.agents
    ```

2. If your `agent.yaml` specifies `version: "v1"` for protocol versions, change it to `version: "1.0.0"`.

## Log streaming changes

| Aspect | Initial preview | Refreshed preview |
|--------|-----------------|-------------------|
| **Endpoint** | `.../versions/{v}/containers/default:logstream` | `.../versions/{v}/sessions/{sessionId}:logstream` |
| **Response format** | Plain text (chunked) | Server-Sent Events (SSE) with JSON payloads |
| **Query parameters** | `kind=console\|system`, `tail=20`, `replica_name` | Simplified — no query parameters needed |
| **Max connection** | 10 minutes | 30 minutes |
| **Idle timeout** | 1 minute | 2 minutes |
| **azd access** | Not available | `azd ai agent monitor` |

## Known gaps

The following capabilities from the initial preview aren't yet available in the refreshed preview:

| Feature | Status | Workaround |
|---------|--------|------------|
| `az cognitiveservices agent` CLI extension | Removed — no first-party CLI commands | Use `az rest` for REST API calls or `azd ai agent` for developer workflows |
| Non-versioned metadata updates (description, tags) | Not yet available via SDK | Use `az rest --method PATCH` against the REST API |
| Explicit replica scaling (min/max replicas) | Replaced by session-based auto-scaling | Sessions scale automatically; no configuration needed |
| Delete deployment without deleting version | Not available | Delete the version directly; create a new version when needed |

## Migration checklist

Use this checklist to track your migration:

- Update `azure-ai-projects` SDK to version 2.1.0 or later.
- **Agent Framework users**: Update Agent Framework packages (`agent-framework-core`, `agent-framework-foundry`, `agent-framework-foundry-hosting`, etc.). Replace `from_agent_framework(agent).run()` with `ResponsesHostServer(agent, store=InMemoryResponseProvider()).run()`. Update `AzureAIAgentClient` → `FoundryChatClient`, `ChatAgent` → `Agent`, and `@ai_function` → `@tool`.
- **LangGraph users**: Replace `azure-ai-agentserver-langgraph` with `azure-ai-agentserver-responses`. Replace `from_langgraph(graph).run()` with a `ResponsesAgentServerHost` handler that invokes the graph and yields `ResponseEventStream` events. Add `langchain-mcp-adapters` and `mcp` if using Foundry Toolbox.
- **Custom/BYO users**: Replace framework adapter packages with protocol libraries (`azure-ai-agentserver-responses` or `azure-ai-agentserver-invocations`). Rewrite agent entry points using `ResponsesAgentServerHost` or `InvocationAgentServerHost`.
- Update protocol version strings from `"v1"` to `"1.0.0"` in code and `agent.yaml`.
- Update `agent.yaml` if using `azd` (protocol version format, remove any `tools` definitions from agent definition).
- Remove `az cognitiveservices agent` CLI calls from scripts and CI/CD pipelines; replace with `az rest` or `azd ai agent` commands.
- Remove capability host creation steps from provisioning scripts.
- Update agent invocation code — use `project.get_openai_client(agent_name=...)` instead of `extra_body` with `agent_reference`.
- Review RBAC — grant downstream resource access to the agent's dedicated Entra identity, not the project managed identity.
- Update `azd` Foundry agents extension to the latest version.
- Build container image with `--platform linux/amd64` (if not already).
- Redeploy your agent using `azd up` or the SDK `create_version` method.
- Verify the new version reaches `active` status before sending traffic.

## Next steps

> [!div class="nextstepaction"]
> [Deploy a hosted agent](deploy-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Manage hosted agents](manage-hosted-agent.md)
- [Manage hosted agent sessions](manage-hosted-sessions.md)
