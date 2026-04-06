---
title: "Use Copilot skills with Microsoft Foundry agents (preview)"
description: "Manage and use Copilot skills in Microsoft Foundry. Author SKILL.md files, store them centrally with the Skills REST API, and inject them into prompt agent sessions."
author: zhuoqunli
ms.author: zhuoqunli
ms.date: 04/05/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: dev-focus
ai-usage: ai-assisted
---

# Use Copilot skills with Microsoft Foundry agents (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A Copilot skill is a `SKILL.md` file that the GitHub Copilot SDK injects as
additional instructions into every conversation session. Skills let you define
reusable behavioral guidelines — such as a greeting style, a code review
checklist, or domain-specific constraints — and manage them centrally through
the Foundry Skills REST API.

In this article, you learn how to:

- Author a `SKILL.md` file.
- Import, list, get, download, and delete skills using the Skills REST API.
- Wire skills into a prompt agent with the GitHub Copilot SDK.

## Feature support

| Feature | REST API | Prompt agent | Hosted agent |
|---------|----------|--------------|--------------|
| Skills CRUD (import, list, get, download, delete) | ✔️ | ✔️ | ❌ |

> [!IMPORTANT]
> Skills are only supported in **prompt agents** that use the GitHub Copilot
> SDK. They are not available in standard hosted agents or other agent types.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Azure AI User role on the Foundry project.
- A GitHub fine-grained personal access token (PAT) with
  **Copilot Requests → Read-only** permission.
  Create one at [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new).
  Classic tokens starting with `ghp_` are not supported.
- **Python packages**: `pip install azure-identity requests python-dotenv`

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
> The `name` and `description` values must be unquoted in the YAML front matter.
> Using quoted values (for example, `name: 'greeting'`) causes an HTTP 500
> error on import.

Place each skill in its own subdirectory under the agent root directory.
For example, `greeting/SKILL.md`, not `SKILL.md` at the root.

## Manage skills with the REST API

The Skills REST API stores skills centrally so any prompt agent in your
Foundry project can use them.

**Base URL:** `{AZURE_AI_PROJECT_ENDPOINT}/skills`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope
`https://ai.azure.com/.default`.

### Import a skill

Package the `SKILL.md` into a ZIP archive and POST to the `:import` endpoint.
Importing creates the skill if it doesn't exist or updates it if it does.

```python
import io
import os
import zipfile
import requests
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
token = DefaultAzureCredential().get_token(
    "https://ai.azure.com/.default"
).token

skill_name = "greeting"
skill_md = open(f"{skill_name}/SKILL.md").read()

buf = io.BytesIO()
with zipfile.ZipFile(buf, "w") as z:
    z.writestr("SKILL.md", skill_md)

response = requests.post(
    f"{endpoint}/skills/{skill_name}:import",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/zip",
    },
    data=buf.getvalue(),
)
response.raise_for_status()  # HTTP 200 on success
print(response.json())
```

The equivalent REST request:

```http
POST {endpoint}/skills/{name}:import
Authorization: Bearer {token}
Content-Type: application/zip

<ZIP bytes containing SKILL.md at the root>
```

> [!NOTE]
> The ZIP must contain `SKILL.md` at its root. A `SKILL.md` nested in a
> subdirectory inside the ZIP is not recognized.

### List skills

```http
GET {endpoint}/skills
Authorization: Bearer {token}
```

Example response:

```json
{
  "object": "list",
  "data": [
    {
      "id": "greeting",
      "object": "skill",
      "name": "greeting",
      "description": "Generate a personalized greeting for the user."
    }
  ]
}
```

### Get a skill

```http
GET {endpoint}/skills/{name}
Authorization: Bearer {token}
```

Returns the skill metadata: `id`, `name`, `description`, and `created_at`.

### Download a skill

```http
GET {endpoint}/skills/{name}:download
Authorization: Bearer {token}
```

Returns a ZIP archive containing the `SKILL.md` file.

> [!NOTE]
> The response `Content-Type` header reports `application/gzip`, but the
> bytes are a valid ZIP archive (magic bytes `PK`). Always use
> `zipfile.ZipFile` to extract the contents; do not use `gzip`.

```python
import io
import zipfile
import requests
from azure.identity import DefaultAzureCredential

endpoint = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
token = DefaultAzureCredential().get_token(
    "https://ai.azure.com/.default"
).token

response = requests.get(
    f"{endpoint}/skills/greeting:download",
    headers={"Authorization": f"Bearer {token}"},
)
response.raise_for_status()

with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
    skill_md = zf.read("SKILL.md").decode()
    print(skill_md)
```

### Delete a skill

```http
DELETE {endpoint}/skills/{name}
Authorization: Bearer {token}
```

Returns HTTP 204 on success.

```python
response = requests.delete(
    f"{endpoint}/skills/greeting",
    headers={"Authorization": f"Bearer {token}"},
)
response.raise_for_status()  # HTTP 204
```

## Use skills in a prompt agent

### Step 1: Download skills into the agent directory

After importing skills to Foundry, download them into your agent's directory
so the Copilot SDK can discover them at startup.

```
my-agent/
├── main.py
├── agent.py
├── greeting/
│   └── SKILL.md        ← downloaded from Foundry
└── another-skill/
    └── SKILL.md
```

### Step 2: Discover skill directories in main.py

Use a discovery function to locate all `*/SKILL.md` files under the agent
root and return the root path:

```python
import pathlib

def _discover_skill_directories() -> list[str]:
    """Return the agent root if any child folder contains SKILL.md."""
    root = pathlib.Path(__file__).parent.resolve()
    skills = list(root.glob("*/SKILL.md"))
    if skills:
        print(f"Found {len(skills)} skill(s): "
              f"{[s.parent.name for s in skills]}")
        return [str(root)]
    return []
```

### Step 3: Pass skill directories to the agent session

In `agent.py`, pass `skill_directories` to `create_session()` when
creating a Copilot SDK session. The SDK auto-discovers all `*/SKILL.md`
files under each listed directory.

```python
import os
from copilot import CopilotClient
from copilot.types import SubprocessConfig

client = CopilotClient(
    SubprocessConfig(github_token=os.environ["GITHUB_TOKEN"])
)

session = await client.create_session(
    on_permission_request=lambda req, ctx: {"kind": "approved"},
    skill_directories=skill_dirs,  # SDK discovers all */SKILL.md
    streaming=True,
)
```

> [!IMPORTANT]
> Pass `SubprocessConfig` to `CopilotClient` — do not pass a raw dictionary.
> Unpack session kwargs with `**` — do not pass a dictionary positionally.
> Both patterns cause `AttributeError` at runtime.

### Step 4: Observe skill invocation

The Copilot SDK emits `SessionEventType.SKILL_INVOKED` when a skill fires.
Handle this event to surface which skill was activated:

```python
from copilot.generated.session_events import SessionEventType

def handler(event) -> None:
    if event.type == SessionEventType.SKILL_INVOKED:
        name = getattr(event.data, "tool_name", None) or "skill"
        print(f"\n> Skill: `{name}`")
    elif event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        if event.data.delta_content:
            print(event.data.delta_content, end="", flush=True)
    elif event.type == SessionEventType.SESSION_IDLE:
        pass  # turn complete
```

When a skill fires, the output includes an annotation line:

```
> Skill: `greeting`
Hello, Alex! Thank you for trying out Foundry Hosted Agents...
```

## Troubleshoot

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 500 on import | Quoted `name` or `description` in YAML front matter | Use `name: foo`, not `name: 'foo'` |
| HTTP 404 on get or download | Skill name not found | Verify the name with `GET /skills` (list) first |
| `Missing GitHub Token` | `GITHUB_TOKEN` env var not set | Set in `.env` or agent environment variables |
| `AttributeError: dict has no attribute 'cli_path'` | Passed raw dict to `CopilotClient()` | Use `CopilotClient(SubprocessConfig(...))` |
| `create_session() takes 1 positional argument` | Passed config dict positionally | Unpack with `create_session(**config_dict)` |
| ZIP not extractable after download | Treated response as gzip | Use `zipfile.ZipFile`; bytes start with `PK`, not `\x1f\x8b` |
| Skill not firing | `SKILL.md` placed at agent root, not in a subdirectory | Put it in `greeting/SKILL.md`, not `./SKILL.md` |

## Related content

- [Build a prompt agent with the GitHub Copilot SDK](../../how-to/build-a-prompt-agent.md)
- [Curate a toolbox in Foundry (preview)](toolbox.md)
- [Tool best practices](../../../agents/concepts/tool-best-practice.md)
