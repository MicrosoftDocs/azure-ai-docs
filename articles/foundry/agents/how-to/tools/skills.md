---
title: "Use skills with Microsoft Foundry agents (preview)"
description: "Manage skills in Microsoft Foundry using the Skills REST API. Author SKILL.md files, store them centrally, and use them in hosted agents."
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

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A skill is a `SKILL.md` file that a hosted agent discovers at startup and
injects as additional instructions into every conversation session. Skills let
you define reusable behavioral guidelines — such as a greeting style, a code
review checklist, or domain-specific constraints — and manage them centrally
through the Foundry Skills REST API.

In this article, you learn how to:

- Author a `SKILL.md` file.
- Import, list, get, download, and delete skills using the Skills REST API.
- Bundle downloaded skills into a hosted agent.

## Feature support

| Feature | REST API | Hosted agent |
|---------|----------|--------------|
| Skills CRUD (import, list, get, download, delete) | ✔️ | N/A |
| Use downloaded skills at runtime | N/A | ✔️ |

> [!IMPORTANT]
> Skills are used in **hosted agents** only. The Skills REST API handles
> storage and retrieval; the hosted agent bundles the downloaded `SKILL.md`
> files into its container image and injects them at session startup.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Azure AI User role on the Foundry project.
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

The Skills REST API stores skills centrally so any hosted agent in your
Foundry project can download and use them.

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

## Use skills in a hosted agent

After importing skills to Foundry, download them and bundle them into your
hosted agent's container image. The agent discovers them at startup and injects
them as additional instructions in every session.

### Step 1: Download skills into the agent directory

Download each skill into its own subdirectory under the agent root:

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
response = requests.get(
    f"{endpoint}/skills/{skill_name}:download",
    headers={"Authorization": f"Bearer {token}"},
)
response.raise_for_status()

# Response Content-Type says application/gzip but bytes are ZIP (magic PK)
with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
    os.makedirs(skill_name, exist_ok=True)
    zf.extractall(skill_name)
```

After downloading, the agent directory looks like this:

```
my-agent/
├── main.py
├── greeting/
│   └── SKILL.md        ← downloaded from Foundry
└── another-skill/
    └── SKILL.md
```

### Step 2: Bundle skills into the container image

In your hosted agent's `Dockerfile`, copy the entire agent directory so that
all `*/SKILL.md` files are included in the image:

```dockerfile
COPY . /app/agent/
```

Skills are bundled automatically with every `azd deploy` — no extra
configuration is required.

### Step 3: Configure the agent to discover skills

In `main.py`, discover all `*/SKILL.md` files under the agent root and pass
the root path to the agent:

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

Pass `skill_directories` to `create_session()` in `agent.py`. The agent
auto-discovers all `*/SKILL.md` files under each listed directory and injects
them as instructions for every session.

```python
import os
from copilot import CopilotClient
from copilot.types import SubprocessConfig

client = CopilotClient(
    SubprocessConfig(github_token=os.environ["GITHUB_TOKEN"])
)

skill_dirs = _discover_skill_directories()
session = await client.create_session(
    on_permission_request=lambda req, ctx: {"kind": "approved"},
    skill_directories=skill_dirs,
    streaming=True,
)
```

## Troubleshoot

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 500 on import | Quoted `name` or `description` in YAML front matter | Use `name: foo`, not `name: 'foo'` |
| HTTP 404 on get or download | Skill name not found | Verify the name with `GET /skills` (list) first |
| `Missing GitHub Token` | `GITHUB_TOKEN` env var not set in the hosted agent container | Set in `agent.yaml` `environment_variables` |
| `AttributeError: dict has no attribute 'cli_path'` | Passed raw dict to `CopilotClient()` | Use `CopilotClient(SubprocessConfig(...))` |
| `create_session() takes 1 positional argument` | Passed config dict positionally | Unpack with `create_session(**config_dict)` |
| ZIP not extractable after download | Treated response as gzip | Use `zipfile.ZipFile`; bytes start with `PK`, not `\x1f\x8b` |
| Skill not injected | `SKILL.md` placed at agent root, not in a subdirectory | Put it in `greeting/SKILL.md`, not `./SKILL.md` |

## Related content

- [Curate a toolbox in Foundry (preview)](toolbox.md)
- [Tool best practices](../../../agents/concepts/tool-best-practice.md)
