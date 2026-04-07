---
title: "Use skills with Microsoft Foundry agents (preview)"
description: "Manage skills in Microsoft Foundry using the Skills REST API. Author SKILL.md files, store them centrally, and use them in hosted agents."
author: alvinashcraft
ms.author: aashcraft
ms.reviewer: zhuoqunli
ms.date: 04/05/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: dev-focus
zone_pivot_groups: selection-foundry-skills
ai-usage: ai-assisted
---

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A skill is a `SKILL.md` file that a hosted agent discovers at startup and injects as additional instructions into every conversation session. Skills let you define reusable behavioral guidelines — such as a greeting style, a code review checklist, or domain-specific constraints — and manage them centrally through the Skills REST API.

In this article, you learn how to:

- Import, list, get, download, and delete skills using the Skills REST API.
- Bundle downloaded skills into a hosted agent.

## Feature support

| Feature | REST API | Python | .NET | Hosted agent | Prompt agent |
|---------|----------|--------|------|--------------|---------------|
| Skills CRUD (create, import, list, get, download, delete) | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Include downloaded skills in agent | N/A | N/A | N/A | ✔️ | N/A |

> [!IMPORTANT]
> Skills are used in **hosted agents** only. The Skills REST API handles
> storage and retrieval; the hosted agent bundles the downloaded `SKILL.md`
> files into its container image and injects them at session startup.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Azure AI User role on the Foundry project.

## Author a skill

A skill is a Markdown file with a YAML front matter block:

```markdown
---
name: greeting
description: Generate a personalized greeting for the user.
---

# Greeting Skill

You are a friendly greeting assistant for Foundry Hosted Agents.

## Instructions

- Include the user's name if they provided one.
- Keep greetings concise — 1 to 2 sentences.
- Thank the user for trying out Foundry Hosted Agents and this sample skill.
```

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Short identifier, no spaces. **Must be unquoted** in YAML. |
| `description` | Yes | One-liner shown in skill listings. **Must be unquoted** in YAML. |
| Body | Yes | Free Markdown. Becomes the skill's injected instructions. |

> [!IMPORTANT]
> - The `name` and `description` values must be unquoted in the YAML front matter.
> - Using quoted values (for example, `name: 'greeting'`) causes an HTTP 500
> error on import.

Place each skill in its own subdirectory under the agent root directory.
For example, `greeting/SKILL.md`, not `SKILL.md` at the root.

## Manage skills with the REST API

The Skills REST API stores skills centrally so any hosted agent in your
Foundry project can download and use them.

**Skills endpoint:** `{FOUNDRY_PROJECT_ENDPOINT}/skills`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope
`https://ai.azure.com/.default`.

### Create a skill

There are two ways to create a skill: submit the content directly as JSON, or
upload a ZIP archive containing a `SKILL.md` file.

#### Option 1: Create from JSON

Use this option when you want to supply the skill's `instructions` text
directly without packaging a file.

:::zone pivot="rest-api"

```http
POST {endpoint}/skills?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json

{
  "name": "greeting",
  "description": "Generate a personalized greeting for the user.",
  "instructions": "You are a friendly greeting assistant. Include the user's name and keep greetings concise."
}
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

Example response:

```json
{
  "id": "skill_abc123",
  "object": "skill",
  "name": "greeting",
  "description": "Generate a personalized greeting for the user.",
  "instructions": "You are a friendly greeting assistant. ...",
  "has_blob": false,
  "created_at": 1741305600
}
```

#### Option 2: Import from a SKILL.md ZIP

Use this option when you have a `SKILL.md` file. Package it as a ZIP and POST
to the `:import` endpoint. The skill name and description are read from the
`SKILL.md` front matter. The request body must be a valid ZIP file with a `SKILL.md` entry at the root.

:::zone pivot="rest-api"

```http
POST {endpoint}/skills:import?api-version=v1
Authorization: Bearer {token}
Content-Type: application/zip
Accept: application/json

<ZIP bytes containing SKILL.md at the root>
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

> [!NOTE]
> The ZIP must contain `SKILL.md` at the root, not in a subdirectory.

Example response:

```json
{
  "id": "skill_def456",
  "object": "skill",
  "name": "greeting",
  "description": "Generate a personalized greeting for the user.",
  "has_blob": true,
  "created_at": 1741305600
}
```

`has_blob: true` means the skill was created from a ZIP and can be downloaded.
Skills created from JSON have `has_blob: false` and can't be downloaded.

### List skills

:::zone pivot="rest-api"

```http
GET {endpoint}/skills?api-version=v1&limit=20&order=desc
Authorization: Bearer {token}
Accept: application/json
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

Example response:

```json
{
  "object": "list",
  "data": [
    {
      "id": "skill_abc123",
      "object": "skill",
      "name": "greeting",
      "description": "Generate a personalized greeting for the user.",
      "has_blob": true,
      "created_at": 1741305600
    }
  ],
  "has_more": false,
  "first_id": "skill_abc123",
  "last_id": "skill_abc123"
}
```

Use `first_id` and `last_id` with the `after` or `before` query parameters
for cursor-based pagination.

### Get a skill

:::zone pivot="rest-api"

```http
GET {endpoint}/skills/{name}?api-version=v1
Authorization: Bearer {token}
Accept: application/json
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

Returns the skill metadata. Returns HTTP 404 if the skill doesn't exist.

### Download a skill

Downloads the original ZIP archive for skills created via `:import`
(`has_blob: true`). Returns HTTP 404 for skills created via JSON.

:::zone pivot="rest-api"

```http
GET {endpoint}/skills/{name}:download?api-version=v1
Authorization: Bearer {token}
Accept: application/zip
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

> [!NOTE]
> The response body is a binary ZIP archive (`Content-Type: application/zip`).

### Delete a skill

:::zone pivot="rest-api"

```http
DELETE {endpoint}/skills/{name}?api-version=v1
Authorization: Bearer {token}
Accept: application/json
```

:::zone-end

:::zone pivot="python"

> [!NOTE]
> Python sample coming soon.

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample coming soon.

:::zone-end

Returns HTTP 200 on success:

```json
{
  "id": "skill_abc123",
  "object": "skill.deleted",
  "name": "greeting",
  "deleted": true
}
```

## Use skills in a hosted agent

After importing skills to Foundry, download them and bundle them into your
hosted agent's container image. The agent discovers them at startup and injects
them as additional instructions in every session.

> [!IMPORTANT]
> Your agent framework must support skills integration. The framework needs to scan for `SKILL.md` files in subdirectories and inject their content as system instructions at session startup. The [GitHub Copilot SDK](https://pypi.org/project/github-copilot-sdk/) supports this natively through the `skill_directories` parameter. If your framework doesn't support skills, you must implement the discovery and injection logic yourself.

The following example uses the GitHub Copilot SDK with the Foundry invocations protocol.

### Step 1: Download skills into the agent directory

Download each skill into its own subdirectory under the agent root.
Use the download operation from [Download a skill](#download-a-skill).

After downloading, the agent directory looks like this:

```
my-agent/
├── main.py
├── agent.yaml
├── agent.manifest.yaml
├── Dockerfile
├── requirements.txt
├── skills/
│   ├── greeting/
│   │   └── SKILL.md        ← downloaded from Foundry
│   └── another-skill/
│       └── SKILL.md
```

### Step 2: Wire up skills in the agent

Create `main.py` using the Copilot SDK. The key integration point is the `skill_directories` parameter in `create_session` and `resume_session` — the SDK scans those directories for `*/SKILL.md` files and injects their content as instructions.

```python
import asyncio
import json
import logging
import os
import pathlib
import sys
import uuid

from starlette.requests import Request
from starlette.responses import Response, StreamingResponse

from azure.ai.agentserver.invocations import InvocationAgentServerHost
from copilot import CopilotClient, SubprocessConfig
from copilot.session import PermissionHandler
from copilot.generated.session_events import SessionEventType

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = InvocationAgentServerHost()

_client: CopilotClient | None = None
_session = None
_session_id: str | None = None
_skills_dir = str(pathlib.Path(__file__).parent / "skills")


async def _ensure_session():
    """Resume a persisted session or create a new one."""
    global _client, _session, _session_id
    if _session is not None:
        return

    _session_id = os.environ.get("FOUNDRY_AGENT_SESSION_ID")
    if not _session_id:
        _session_id = str(uuid.uuid4())

    _client = CopilotClient(
        SubprocessConfig(github_token=os.environ["GITHUB_TOKEN"]),
        auto_start=False,
    )
    await _client.start()

    try:
        _session = await _client.resume_session(
            _session_id,
            on_permission_request=PermissionHandler.approve_all,
            streaming=True,
            skill_directories=[_skills_dir],
        )
    except Exception:
        _session = await _client.create_session(
            session_id=_session_id,
            on_permission_request=PermissionHandler.approve_all,
            streaming=True,
            skill_directories=[_skills_dir],
        )


async def _stream_response(invocation_id: str, input_text: str):
    """Forward Copilot SDK session events as SSE."""
    await _ensure_session()
    queue: asyncio.Queue = asyncio.Queue()

    def on_event(event):
        if event.type == SessionEventType.SESSION_IDLE:
            queue.put_nowait(None)
        elif event.type == SessionEventType.SESSION_ERROR:
            queue.put_nowait(RuntimeError(
                getattr(event.data, "message", "error")))
        else:
            queue.put_nowait(event)

    unsubscribe = _session.on(on_event)
    try:
        await _session.send(input_text)
        while True:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, Exception):
                yield (
                    f"data: {json.dumps({'type': 'error', 'message': str(item)})}"
                    "\n\n"
                ).encode()
                break
            yield f"data: {json.dumps(item.to_dict())}\n\n".encode()

        yield (
            f"event: done\ndata: {json.dumps({'invocation_id': invocation_id, 'session_id': _session_id})}"
            "\n\n"
        ).encode()
    finally:
        unsubscribe()


@app.invoke_handler
async def handle_invoke(request: Request) -> Response:
    data = await request.json()
    input_text = data.get("input", "")
    if not input_text:
        return Response(
            content=json.dumps({"error": "Missing 'input' field"}),
            status_code=400,
            media_type="application/json",
        )
    return StreamingResponse(
        _stream_response(request.state.invocation_id, input_text),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


if __name__ == "__main__":
    if not os.environ.get("GITHUB_TOKEN"):
        sys.exit("Error: GITHUB_TOKEN env var is required")
    app.run()
```

### Step 3: Initialize and test the agent locally

Initialize the agent:

```bash
azd ai agent init --name my-copilot-agent
```

Start the local agent:

```bash
azd ai agent start
```

Test the local agent:

```bash
azd ai agent invoke "Tell me a joke"
```

### Step 4: Deploy the hosted agent

Deploy the agent to Foundry:

```bash
azd ai agent deploy
```

Test the remote hosted agent:

```bash
azd ai agent invoke --remote "Tell me a joke"
```


## Troubleshoot

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 500 on import | Quoted `name` or `description` in YAML front matter | Use `name: foo`, not `name: 'foo'` |
| HTTP 404 on get or download | Skill name not found | Verify the name with `GET /skills?api-version=v1` first |
| HTTP 404 on download | Skill was created from JSON (`has_blob: false`) | Only ZIP-imported skills (`has_blob: true`) can be downloaded |
| ZIP not extractable after download | Caller treated response as gzip | Response is `application/zip`; use `zipfile.ZipFile` to extract |
| Skill not injected | `SKILL.md` placed at agent root, not in a subdirectory | Put it in `greeting/SKILL.md`, not `./SKILL.md` |

