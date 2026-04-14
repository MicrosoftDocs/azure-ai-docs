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

A skill is a `SKILL.md` file that a hosted agent discovers at startup and injects as additional instructions into every conversation session. Skills let you define reusable behavioral guidelines—such as a greeting style, a code review checklist, or domain-specific constraints—and manage them centrally through the Skills REST API.

In this article, you learn how to:

- Import, list, get, download, and delete skills using the Skills REST API.
- Bundle downloaded skills into a hosted agent.

> [!IMPORTANT]
> If you use Skills with any third-party servers, agents, code, or non-Azure Direct models("Third-Party Systems"), you do so at your own risk. Third-Party Systems are Non-Microsoft Products under the Microsoft Product Terms and are governed by their own third-party license terms. You are responsible for any usage and associated costs.
>
> We recommend reviewing all data being shared with and received from Third-Party Systems and being cognizant of third-party practices for handling, sharing, retention, and location of data. It is your responsibility to manage whether your data will flow outside of your organization’s Azure compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You are responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. See the [Azure OpenAI transparency note](../../../responsible-ai/agents/transparency-note.md).

## Feature support

| Feature | REST API | Python | .NET | JavaScript | Hosted agent | Prompt agent |
|---------|----------|--------|------|------------|--------------|---------------|
| Skills CRUD (create, import, list, get, download, delete) | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Include downloaded skills in agent | N/A | N/A | N/A | N/A | ✔️ | N/A |

> [!IMPORTANT]
> Skills are used in **hosted agents** only. The Skills REST API handles storage and retrieval; the hosted agent bundles the downloaded `SKILL.md` files into its container image and injects them at session startup.

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

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    created = project_client.beta.skills.create(
        name="greeting",
        description="Generate a personalized greeting for the user.",
        instructions="You are a friendly greeting assistant. Include the user's name and keep greetings concise.",
    )
    print(
        f"Created skill: {created.name} ({created.skill_id}) "
        f"has_blob={created.has_blob}"
    )
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
using Azure.AI.Projects.Agents;
using Azure.Core.Pipeline;
using Azure.Identity;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
AgentAdministrationClientOptions options = new();
options.AddPolicy(new FeaturePolicy("Skills=V1Preview"), PipelinePosition.PerCall);
AgentAdministrationClient adminClient = new(new Uri(projectEndpoint), new DefaultAzureCredential(), options);
AgentSkills skillsClient = adminClient.GetAgentSkills();

AgentsSkill created = skillsClient.CreateSkill(
    name: "greeting",
    description: "Generate a personalized greeting for the user.",
    instructions: "You are a friendly greeting assistant. Include the user's name and keep greetings concise."
);
Console.WriteLine($"Created skill: {created.Name} ({created.SkillId}) HasBlob={created.HasBlob}");

// FeaturePolicy: inject the preview feature header on every request.
internal class FeaturePolicy(string feature) : PipelinePolicy
{
    public override void Process(PipelineMessage msg, IReadOnlyList<PipelinePolicy> pipeline, int idx)
    {
        msg.Request.Headers.Add("Foundry-Features", feature);
        ProcessNext(msg, pipeline, idx);
    }
    public override async ValueTask ProcessAsync(PipelineMessage msg, IReadOnlyList<PipelinePolicy> pipeline, int idx)
    {
        msg.Request.Headers.Add("Foundry-Features", feature);
        await ProcessNextAsync(msg, pipeline, idx);
    }
}
```

:::zone-end
:::zone pivot="javascript"

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());

const skill = await project.beta.skills.create("greeting", {
  description: "Generate a personalized greeting for the user.",
  instructions: "You are a friendly greeting assistant. Include the user's name and keep greetings concise.",
});
console.log(`Created skill: ${skill.name} (id: ${skill.skillId})`);
```

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

```python
import os
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    imported = project_client.beta.skills.create_from_package(
        Path("greeting.zip").read_bytes()
    )
    print(
        f"Imported skill: {imported.name} ({imported.skill_id}) "
        f"has_blob={imported.has_blob}"
    )
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

// CreateSkillFromPackage accepts a local directory path containing a SKILL.md file.
AgentsSkill imported = skillsClient.CreateSkillFromPackage("path/to/skill-directory");
Console.WriteLine($"Imported skill: {imported.Name} ({imported.SkillId}) HasBlob={imported.HasBlob}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
import { readFileSync } from "fs";

const zipBytes = readFileSync("greeting.zip");
const skill = await project.beta.skills.createFromPackage(zipBytes);
console.log(`Imported skill: ${skill.name} (has_blob: ${skill.hasBlob})`);
```

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
Foundry-Features: Skills=V1Preview
```

:::zone-end

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    skills = list(project_client.beta.skills.list())
    print(f"Found {len(skills)} skill(s)")
    for skill in skills:
        print(f"  {skill.name} (has_blob: {skill.has_blob})")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

List<AgentsSkill> skills = [.. skillsClient.GetSkills()];
Console.WriteLine($"Found {skills.Count} skill(s).");
foreach (AgentsSkill item in skills)
{
    Console.WriteLine($"  - {item.Name} ({item.SkillId})");
}
```

:::zone-end
:::zone pivot="javascript"

```javascript
const skills = project.beta.skills.list({ limit: 20, order: "desc" });
for await (const skill of skills) {
  console.log(`${skill.name} (has_blob: ${skill.hasBlob})`);
}
```

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

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    skill = project_client.beta.skills.get("greeting")
    print(f"{skill.name}: {skill.description}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

AgentsSkill skill = skillsClient.GetSkill(skillName: "greeting");
Console.WriteLine($"Retrieved skill: {skill.Name}, description: {skill.Description}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const skill = await project.beta.skills.get("greeting");
console.log(`${skill.name}: ${skill.description}`);
```

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

```python
import os
import tempfile
from datetime import datetime
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
download_folder = Path(tempfile.gettempdir()).resolve()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_path = download_folder / f"greeting_{timestamp}.zip"
    download_path.write_bytes(
        b"".join(project_client.beta.skills.download("greeting"))
    )
    print(f"Downloaded skill package to: {download_path}")
```

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample not yet available.

:::zone-end

:::zone pivot="javascript"

```javascript
const response = await project.beta.skills.download("greeting");
// response.body contains the ZIP archive bytes
```

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

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    deleted = project_client.beta.skills.delete("greeting")
    print(f"Deleted skill: {deleted}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

skillsClient.DeleteSkill("greeting");
Console.WriteLine("Skill deleted.");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const result = await project.beta.skills.delete("greeting");
console.log(`Deleted: ${result.name} (${result.deleted})`);
```

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

### Step 2: Initialize the agent locally

After downloading the skills, initialize the agent. Skills are autodiscovered at startup—the agent scans the project root for any `*/SKILL.md` pattern.

```bash
azd ai agent init --skills --name my-agent
```

Start the local agent:

```bash
azd ai agent start
```

Test the local agent:

```bash
azd ai agent invoke "What Azure products do you offer?"
```

### Step 3: Deploy and test the hosted agent

Deploy the agent:

```bash
azd ai agent deploy
```

Test the remote hosted agent:

```bash
azd ai agent invoke --remote "What Azure products do you offer?"
```

## Known fast follows and gaps

The following capabilities are planned or have known limitations:

| Feature | Status | Description |
|---------|--------|-------------|
| Python SDK samples for skill operations | Available | Native Python SDK samples for create, import, list, get, download, and delete skill operations are now available. |
| .NET SDK samples for skill operations | Partially available | .NET SDK samples are now available for create, import, list, get, and delete. Download is not yet available. |
| `"latest"` as `default_version` | Not supported | There is no way to set `default_version` to a special value like `"latest"` that automatically points to the most recently created version. Publishers must explicitly promote each new version via PATCH. See [Curate intent-based toolbox in Foundry](toolbox.md). |
| Default project toolbox (`/mcp`) | Not yet implemented | A built-in, implicit toolbox at `{project_endpoint}/mcp` that serves all project-configured tools without toolbox CRUD. Currently, developers must create a named toolbox explicitly. |
| File and vector store updates without new version | Not supported | For toolbox tools like File Search and Code Interpreter, uploading new files or updating vector stores requires creating a new toolbox version. There is no way to update the underlying file or vector store content without re-creating the version. See [Curate intent-based toolbox in Foundry](toolbox.md). |
| Tool configuration via `_meta` | Out of scope for public preview | Pass developer-controlled configuration (connection IDs, index names, query types) separately from model-provided arguments using MCP's standard `_meta` field on `tools/call`. |

## Related content

- [Curate intent-based toolbox in Foundry](toolbox.md)
- [Deploy a hosted agent](../deploy-hosted-agent.md)
- [Add a connection to your project](../../../how-to/connections-add.md)
