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
zone_pivot_groups: selection-foundry-skills
ai-usage: ai-assisted
---

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A skill is a `SKILL.md` file or a folder with markdown files and python files that a hosted agent discovers at startup and
injects as additional instructions into every conversation session. Skills let
you define reusable behavioral guidelines — such as a greeting style, a code
review checklist, or domain-specific constraints — and manage them centrally
through the Foundry Skills REST API.

In this article, you learn how to:

- Import, list, get, download, and delete skills using the Skills REST API.
- Bundle downloaded skills into a hosted agent.

## Feature support

| Feature | REST API | Hosted agent | Prompt agent |
|---------|----------|--------------| --------------|
| Skills CRUD (import, list, get, download, delete) | ✔️ | N/A | N/A| 
| Include downloaded skills as part of agent | N/A | ✔️ | N/A|

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
> The `name` and `description` values must be unquoted in the YAML front matter.
> Using quoted values (for example, `name: 'greeting'`) causes an HTTP 500
> error on import.

Place each skill in its own subdirectory under the agent root directory.
For example, `greeting/SKILL.md`, not `SKILL.md` at the root.

## Manage skills with the REST API

The Skills REST API stores skills centrally so any hosted agent in your
Foundry project can download and use them.

**Skills endpoint:** `{FOUNDRY_PROJECT_ENDPOINT}/skills?api-version=v1`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope
`https://ai.azure.com/.default`.

**Required header:** `Foundry-Features: Skills=V1Preview` on every request.

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
Foundry-Features: Skills=V1Preview

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
Foundry-Features: Skills=V1Preview

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
> The `name` and `description` in the `SKILL.md` front matter must be
> unquoted — for example, `name: greeting`, not `name: 'greeting'`.

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
Foundry-Features: Skills=V1Preview
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
Foundry-Features: Skills=V1Preview
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
Foundry-Features: Skills=V1Preview
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
Foundry-Features: Skills=V1Preview
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

### Step 1: Download skills into the agent directory

Download each skill into its own subdirectory under the agent root.
Use the download operation from [Download a skill](#download-a-skill).

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
the root path to the agent. Then pass `skill_directories` to `create_session()`
in `agent.py`. The agent auto-discovers all `*/SKILL.md` files under each
listed directory and injects them as instructions for every session.

## Troubleshoot

| Error | Cause | Fix |
|-------|-------|-----|
| HTTP 500 on import | Quoted `name` or `description` in YAML front matter | Use `name: foo`, not `name: 'foo'` |
| HTTP 404 on get or download | Skill name not found | Verify the name with `GET /skills?api-version=v1` first |
| HTTP 404 on download | Skill was created from JSON (`has_blob: false`) | Only ZIP-imported skills (`has_blob: true`) can be downloaded |
| `Missing GitHub Token` | `GITHUB_TOKEN` env var not set in the hosted agent container | Set in `agent.yaml` `environment_variables` |
| ZIP not extractable after download | Caller treated response as gzip | Response is `application/zip`; use `zipfile.ZipFile` to extract |
| Skill not injected | `SKILL.md` placed at agent root, not in a subdirectory | Put it in `greeting/SKILL.md`, not `./SKILL.md` |

## Related content

- [Curate a toolbox in Foundry (preview)](toolbox.md)
- [Tool best practices](../../../agents/concepts/tool-best-practice.md)
