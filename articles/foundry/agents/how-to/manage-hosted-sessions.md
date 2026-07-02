---
title: "Manage hosted agent sessions"
description: "Create, invoke, and manage sessions for hosted agents in Foundry Agent Service by using the REST API, Python SDK, or Azure Developer CLI."
author: aahill
ms.author: aahi
ms.date: 04/14/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
zone_pivot_groups: hosted-agent-manage-method
---

# Manage hosted agent sessions

This article shows you how to manage sessions for Hosted agents in Foundry Agent Service. A session is a stateful, isolated sandbox tied to a single logical workload (for example, one user's chat). The platform persists the session's filesystem (`$HOME` and uploaded files) across turns and across idle periods, so the agent can resume where it left off. Sessions persist for up to 30 days, with a 15-minute idle timeout that deprovisions compute and saves state until the session is referenced again. For background, see [Hosted agents in Foundry Agent Service](../concepts/hosted-agents.md#sessions-and-conversations).

## Sessions versus conversations

Sessions and conversations are distinct concepts in Foundry Agent Service:

| Aspect | Session | Conversation |
|---|---|---|
| What it represents | Sandbox compute and persisted filesystem (`$HOME`, `/files`) | History of messages, tool calls, and responses |
| Identifier | `agent_session_id` | `previous_response_id` or `conversation` (Responses protocol only) |
| Used for | File uploads, working state across turns | Threading turns of a chat together |
| Managed by | The platform, through the `/sessions` API | The platform (Responses); your container code (Invocations) |

The `/sessions` API in this article works the same way for both Responses-protocol and Invocations-protocol agents. What differs is how a per-call invocation binds to a session and whether the platform stores conversation history:

- **Responses protocol.** Conversation continuity comes from `previous_response_id` or a `conversation` ID—not from the session ID. Reusing the same `agent_session_id` doesn't, on its own, replay prior messages to the model. You have two ways to thread Responses turns:

    - **`previous_response_id`.** Chain each new response to the previous response's ID. Stateless on the client. Each call without an explicit `agent_session_id` lands in a new sandbox, so include `agent_session_id` as well when you need to reuse uploaded files or `$HOME` state.
    - **`conversation`.** Create a conversation object once via `POST .../endpoint/protocols/openai/conversations`, then pass its `id` on every `responses.create` call. The platform stores the message history under that conversation ID, and a stable `agent_session_id` is automatically associated with the conversation. Subsequent calls reuse the same sandbox without you having to track the session ID.

- **Invocations protocol.** The platform doesn't store conversation history; your container manages any state your agent needs across turns. Sessions are still useful for `$HOME`/uploaded-file persistence and as a stable handle your code can use to look up its own per-session state.

> [!TIP]
> Sending `agent_session_id` back on follow-up calls binds them to the same sandbox. The invoke endpoints don't infer the session from `previous_response_id` alone. You only need that binding when later turns must see files uploaded through the session's `/files` endpoint or state the agent wrote to `$HOME`. For pure stateless invocations, you can let each call get a fresh session.

### How each protocol binds an invocation to a session

The two invoke endpoints accept the session ID in different places. Use the mechanism shown for the protocol you're calling.

| Protocol | Endpoint | Where to put `agent_session_id` |
|---|---|---|
| Responses | `POST .../endpoint/protocols/openai/responses` | Request body field `agent_session_id` (or use the `conversation` field, which autobinds a session) |
| Invocations | `POST .../endpoint/protocols/invocations` | Query string parameter `?agent_session_id=<id>` |

For Invocations, the platform reads the query parameter only. Fields named `agent_session_id` or `session_id` in the request body and headers like `x-agent-session-id` are passed through to your container untouched but don't influence which sandbox the platform routes to.

## Prerequisites

- A [deployed Hosted agent](deploy-hosted-agent.md) with an `active` version. See [Manage Hosted agents](manage-hosted-agent.md) for how to check version status.

:::zone pivot="rest"

- [Azure CLI](/cli/azure/install-azure-cli) version 2.80 or later, authenticated with `az login`.

:::zone-end

:::zone pivot="python"

- Python SDK: `azure-ai-projects>=2.1.0` and `azure-identity`.

:::zone-end

:::zone pivot="azd"

- [Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) version 1.23.0 or later.
- The Foundry agents extension:

    ```bash
    azd ext install azure.ai.agents
    ```

:::zone-end

:::zone pivot="rest"

## Set up variables

The REST API examples in this article use `az rest` to call the Foundry Agent Service endpoints directly. Set the following variables before running the commands:

```bash
ACCOUNT_NAME="<your-foundry-account-name>"
PROJECT_NAME="<your-project-name>"
BASE_URL="https://${ACCOUNT_NAME}.services.ai.azure.com/api/projects/${PROJECT_NAME}"
API_VERSION="v1"
RESOURCE="https://ai.azure.com"
```

> [!IMPORTANT]
> The `--resource` parameter is required for all `az rest` calls to Foundry Agent Service data-plane endpoints. Without it, `az rest` can't derive the correct Microsoft Entra audience from the URL and authentication fails.

> [!NOTE]
> Session operations are a preview feature. Include the `Foundry-Features: HostedAgents=V1Preview` header in every REST request.

:::zone-end

:::zone pivot="python"

## Set up the client

All Python examples in this article use the following client configuration:

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project = AIProjectClient(
    endpoint="<your-project-endpoint>",
    credential=DefaultAzureCredential(),
    allow_preview=True,
)
```

> [!NOTE]
> Session operations are exposed under the `project.beta.agents` subclient. Calls to `project.beta.agents` work without `allow_preview=True`, but `project.get_openai_client(agent_name=...)`—used in this article to invoke Responses-protocol agents—requires `allow_preview=True` and raises `ValueError` without it.

:::zone-end

## Invoke an agent and let the platform create the session

For most agents, you don't need to create a session in advance. When you invoke the agent without an `agent_session_id`, the service creates one and returns it on the response. Capture that ID and pass it on later calls when you want subsequent invocations to share the same sandbox state—for example, files you upload through the `/files` endpoint.

> [!NOTE]
> Session continuity *isn't* the same as conversation continuity. For Responses, preserve message history across turns by passing `previous_response_id` or a `conversation` ID. For Invocations, the platform doesn't store history—your container code is responsible for tracking any per-session state. In both cases, `agent_session_id` only ties calls to the same sandbox.

### Responses protocol

The Responses endpoint returns either a single JSON payload or a Server-Sent Events (SSE) stream, depending on the `stream` field in the request body. The default is `false`. Set `"stream": true` to receive incremental events.

:::zone pivot="rest"

```bash
AGENT_NAME="my-agent"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/openai/responses?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body '{
        "input": "Find me hotels in Seattle under $200 per night",
        "stream": false
    }'
```

The response payload includes the `agent_session_id` the platform created. To continue using that session on a later call when threading with `previous_response_id`, include `agent_session_id` in the request body:

```bash
az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/openai/responses?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body '{
        "input": "Recommend one of those hotels",
        "stream": false,
        "agent_session_id": "<session-id-from-first-response>",
        "previous_response_id": "<id-from-first-response>"
    }'
```

If you thread turns with a `conversation` ID instead, the platform automatically routes every call for that conversation to the same `agent_session_id`. You don't need to pass `agent_session_id` yourself.

:::zone-end

:::zone pivot="python"

When you call `get_openai_client` with an `agent_name`, the returned OpenAI client is routed at the agent's endpoint. The first call creates the session; the response carries the new `agent_session_id` in `model_extra`.

```python
openai_client = project.get_openai_client(agent_name="my-agent")

response = openai_client.responses.create(
    input="Find me hotels in Seattle under $200 per night",
)
session_id = response.model_extra.get("agent_session_id")
print(f"Session: {session_id}")
print(f"Response: {response.output_text}")

# Reuse the session and thread the conversation on a later turn.
follow_up = openai_client.responses.create(
    input="Recommend one of those hotels",
    previous_response_id=response.id,
    extra_body={"agent_session_id": session_id},
)
print(follow_up.output_text)
```

If you thread turns with a `conversation` ID instead of `previous_response_id`, the platform automatically routes every call for that conversation to the same `agent_session_id`—you can omit `extra_body={"agent_session_id": ...}`:

```python
conversation = openai_client.conversations.create()

first = openai_client.responses.create(
    input="Find me hotels in Seattle under $200 per night",
    extra_body={"conversation": conversation.id},
)
follow_up = openai_client.responses.create(
    input="Recommend one of those hotels",
    extra_body={"conversation": conversation.id},
)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent invoke --input "Find me hotels in Seattle under $200 per night"
```

:::zone-end

### Invocations protocol

Invocations agents accept arbitrary JSON request bodies that match the schema your container defines. The platform routes the call to a session and forwards the body to your container; the response shape is whatever your container emits. Sample agents and containers built with the `azure-ai-agentserver-invocations` SDK return an SSE stream by default, with a terminal `done` event that carries the `session_id` (the same value as `agent_session_id`) and an `invocation_id`. Your own container can return JSON, NDJSON, SSE, or any other content type.

The first call without an `agent_session_id` query parameter creates a new session. To reuse the sandbox on a later call, pass the session ID as the `agent_session_id` query parameter.

:::zone pivot="rest"

```bash
AGENT_NAME="my-agent"

# First call — platform creates a new session.
az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/invocations?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body '{"input": "Hello"}'
```

For an SSE-emitting container like the Agent Service samples, the final `done` event carries `session_id` and an `invocation_id`. To reuse that sandbox on a later call, pass the session ID as the `agent_session_id` query parameter:

```bash
SESSION_ID="<session_id-from-first-response>"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/protocols/invocations?api-version=${API_VERSION}&agent_session_id=${SESSION_ID}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --body '{"input": "Continue our previous discussion"}'
```

> [!IMPORTANT]
> The Invocations endpoint reads the session ID from the **query string**. Fields named `agent_session_id` or `session_id` in the request body and headers like `x-agent-session-id` are forwarded to your container untouched but don't change which sandbox the platform routes to.

:::zone-end

:::zone pivot="python"

The Python SDK doesn't ship a typed Invocations client. Call the endpoint with `requests` (or any HTTP library) and authenticate with a bearer token from `azure-identity`:

```python
import json
import requests
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://ai.azure.com/.default").token
headers = {
    "Authorization": f"Bearer {token}",
    "Foundry-Features": "HostedAgents=V1Preview",
    "Content-Type": "application/json",
}

base = "<your-project-endpoint>/agents/my-agent/endpoint/protocols/invocations?api-version=v1"

# First call — platform creates a new session.
response = requests.post(base, headers=headers, data=json.dumps({"input": "Hello"}))
for line in response.iter_lines(decode_unicode=True):
    if line.startswith("data:"):
        event = json.loads(line[len("data:"):].strip())
        if event.get("type") == "done":
            session_id = event["session_id"]

# Reuse the session on a later call.
requests.post(
    f"{base}&agent_session_id={session_id}",
    headers=headers,
    data=json.dumps({"input": "Continue our previous discussion"}),
)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent invoke --input '{"input": "Hello"}'
```

:::zone-end

## Isolation keys

The isolation key is a scoping value attached to each session. Every session belongs to exactly one isolation key, and the platform routes session requests so that a caller only sees and operates on sessions tagged with the key the request supplies. The same key applies consistently across all session-related endpoints regardless of which protocol the agent uses:

- `POST/GET/DELETE .../endpoint/sessions[/{id}]`
- `POST .../endpoint/protocols/openai/responses` (Responses agents)
- `POST .../endpoint/protocols/invocations` (Invocations agents)
- `PUT/GET/DELETE .../endpoint/sessions/{id}/files[/content]`

The isolation key is a partitioning value, not an authentication or authorization mechanism. The Microsoft Entra token on the request authenticates the caller and authorizes the call against the project's role assignments. The isolation key only narrows which sessions that authenticated caller acts on. Apply your application's own access controls at a layer above the agent endpoint when you need to decide which users may act on which keys.

How the key is set depends on the agent endpoint's authorization scheme, which you configure when you set up the agent (see [Configure an agent](configure-agent.md#enable-protocols-and-authorization-schemes)):

- **`Entra` (default).** The platform derives the isolation key from the caller's Microsoft Entra token. The `x-ms-user-isolation-key` header is accepted but ignored. Each authenticated caller automatically gets their own scope.
- **`Header`.** The platform reads the isolation key from the `x-ms-user-isolation-key` request header. Send a stable string per session owner (for example, an end-user or tenant identifier) on every session request, including invocations and file operations. Requests without the header fail. The platform doesn't validate the value, so your client is responsible for choosing the right key for each call.

For information about how the platform automatically isolates each caller's sessions and how to extend that isolation to your own application's users, see [Isolate hosted agent sessions per user](isolate-sessions-per-user.md).

## View and manage sessions across users

By default, each caller sees and manages only the sessions that belong to their own identity. List, get, and delete operations return or affect only that caller's sessions.

An administrator or automation that needs to work with every session on an agent - for debugging, cost analysis, or incident response - needs the **Foundry User** role on the Foundry project. This role carries the `sessions/read` and `sessions/write` data actions for cross-user access. By using that role, the same list, get, and delete operations return and act on all sessions on the agent, regardless of which identity created them.

[!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

Grant the Foundry User role only to identities that need cross-user session access. Regular callers keep the default, own-sessions-only scope.

## Create a session explicitly (advanced)

Create a session in advance only when you need to:

- Upload files to the sandbox (`/files`) before the agent's first turn.
- Preallocate a session you can reference from your client code before the first invocation.
- Pin the session to a specific agent version with `version_indicator`. Each session is bound to a single version at creation time. By default, the platform resolves the version using the agent endpoint's traffic-routing rules (`version_selector`)—for example, `@latest`. Pass `version_indicator` to override that and bind the session to a concrete version (such as `"2"`) so later turns keep using that version even if you publish a newer one. The value must be a concrete version identifier returned by the agent versions API; aliases like `@latest` aren't accepted here.

:::zone pivot="rest"

```bash
AGENT_NAME="my-agent"

az rest --method POST \
    --url "${BASE_URL}/agents/${AGENT_NAME}/endpoint/sessions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "x-ms-user-isolation-key=user-123" "Foundry-Features=HostedAgents=V1Preview" \
    --body '{
        "version_indicator": {
            "type": "version_ref",
            "agent_version": "2"
        }
    }'
```

Omit the body (or send `{}`) to let the platform pick the version using the agent endpoint's traffic-routing rules.

:::zone-end

:::zone pivot="python"

```python
session = project.beta.agents.create_session(
    agent_name="my-agent",
    body={},
    isolation_key="user-123",
)
print(f"Session created (ID: {session.agent_session_id}, status: {session.status})")
```

The SDK requires the `isolation_key` keyword on `create_session` and `delete_session`. The server only enforces it when the agent endpoint is configured to read keys from headers—see [Isolation keys](#isolation-keys).

To pin the session to a specific agent version, include `version_indicator` in the body:

```python
session = project.beta.agents.create_session(
    agent_name="my-agent",
    body={
        "version_indicator": {"type": "version_ref", "agent_version": "2"},
    },
    isolation_key="user-123",
)
```

:::zone-end

:::zone pivot="azd"

Sessions are created automatically when you invoke an agent through `azd`. Manual session creation isn't currently available as a standalone command.

:::zone-end


## List sessions

:::zone pivot="rest"

```bash
az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
sessions = project.beta.agents.list_sessions(agent_name="my-agent")
for item in sessions:
    print(f"Session: {item.agent_session_id} (status: {item.status})")
```

:::zone-end

:::zone pivot="azd"

Session listing isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Get session details

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
session = project.beta.agents.get_session(
    agent_name="my-agent",
    session_id="<session-id>",
)
print(f"Session ID: {session.agent_session_id}, Status: {session.status}")
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Delete a session

Deleting a session terminates the sandbox and releases its resources. When the agent endpoint uses `Header` isolation, the isolation key must match the value used when the session was created. When the endpoint uses `Entra` isolation, the platform scopes the delete to the calling identity.

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"
ISOLATION_KEY="user-123"

az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}?api-version=${API_VERSION}" \
    --resource "${RESOURCE}" \
    --headers "x-ms-user-isolation-key=${ISOLATION_KEY}" "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.delete_session(
    agent_name="my-agent",
    session_id="<session-id>",
    isolation_key="user-123",
)
```

:::zone-end

:::zone pivot="azd"

Session management isn't currently available as a standalone command. Use the REST API or SDK.

:::zone-end

## Session file operations

Upload and download files to agent session sandboxes. Each file is scoped to a specific session. The maximum file size for upload is 50 MB.

A container can also write files directly into the session sandbox (under `$HOME`) and have them appear through these APIs. For an example, see the [note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent), which persists one notes file per session.

> [!NOTE]
> The Python SDK uses `session_id` as the keyword for `upload_session_file`, and `agent_session_id` for `get_session_files`, `download_session_file`, and `delete_session_file`. Use the keyword name shown in each example.

### Upload a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method PUT \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files/content?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --body @data.csv \
    --headers "Content-Type=application/octet-stream" "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.upload_session_file(
    agent_name="my-agent",
    session_id="<session-id>",
    content_or_file_path="./data.csv",
    path="data.csv",
)
```

The `content_or_file_path` parameter accepts a file path string. The SDK reads and uploads the file contents automatically.

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files upload --file ./data.csv --target-path data.csv
```

:::zone-end

### List files in a session

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files?api-version=${API_VERSION}&path=." \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
files = project.beta.agents.get_session_files(
    agent_name="my-agent",
    agent_session_id="<session-id>",
    path=".",
)
for entry in files.entries:
    print(f"  {entry['name']} (size: {entry['size']}, directory: {entry['is_directory']})")
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files list .
```

:::zone-end

### Download a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method GET \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files/content?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview" \
    --output-file output.csv
```

:::zone-end

:::zone pivot="python"

```python
content_bytes = b"".join(
    project.beta.agents.download_session_file(
        agent_name="my-agent",
        agent_session_id="<session-id>",
        path="data.csv",
    )
)
with open("./output.csv", "wb") as f:
    f.write(content_bytes)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files download --file data.csv --target-path ./output.csv
```

:::zone-end

### Delete a file

:::zone pivot="rest"

```bash
SESSION_ID="<session-id>"

az rest --method DELETE \
    --url "${BASE_URL}/agents/my-agent/endpoint/sessions/${SESSION_ID}/files?api-version=${API_VERSION}&path=data.csv" \
    --resource "${RESOURCE}" \
    --headers "Foundry-Features=HostedAgents=V1Preview"
```

:::zone-end

:::zone pivot="python"

```python
project.beta.agents.delete_session_file(
    agent_name="my-agent",
    agent_session_id="<session-id>",
    path="data.csv",
)
```

:::zone-end

:::zone pivot="azd"

```bash
azd ai agent files remove --file data.csv
```

:::zone-end

## Next steps

> [!div class="nextstepaction"]
> [Manage Hosted agents](manage-hosted-agent.md)

## Related content

- [What are Hosted agents?](../concepts/hosted-agents.md)
- [Deploy a Hosted agent](deploy-hosted-agent.md)
- [Manage Hosted agents](manage-hosted-agent.md)
- [Agent identity concepts](../concepts/agent-identity.md)
- [Note-taking agent sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/notetaking-agent) for a container that writes per-session files visible through the Session Files API.
