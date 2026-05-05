---
title: "Use skills with Microsoft Foundry agents (preview)"
description: "Manage skills in Microsoft Foundry using the Skills REST API. Author SKILL.md files, store them centrally, and use them in hosted agents."
author: jonburchel
reviewer: lindazqli
ms.author: jburchel
ms.reviewer: zhuoqunli
ms.date: 04/23/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
zone_pivot_groups: selection-foundry-skills
ai-usage: ai-assisted
---

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

As agents grow beyond simple prototypes, teams accumulate behavioral guidelines that need to be consistent across every conversation. A support agent should always follow a specific escalation policy, a code-review agent should always apply the same checklist, and a sales agent should always respect certain messaging constraints. Embedding these guidelines directly in each agent's system prompt or code creates duplication: when the policy changes, you need to update and redeploy every agent that uses it.

Skills solve this problem by decoupling behavioral guidelines from agent code. A skill is a `SKILL.md` file you author once, store centrally in Foundry through the Skills REST API, and download into any hosted agent project. Your agent code loads these skill files and injects their contents as additional instructions into conversation sessions, guiding the model's behavior. When you update a skill, download it again and redeploy the agent to pick up the change — no code changes required.

In this article, you learn how to:

- Import, list, get, download, and delete skills by using the Skills REST API.
- Bundle downloaded skills into a hosted agent.

> [!IMPORTANT]
> If you use Skills with any third-party servers, agents, code, or non-Azure Direct models ("Third-Party Systems"), you do so at your own risk. Third-Party Systems are Non-Microsoft Products under the Microsoft Product Terms and are governed by their own third-party license terms. You're responsible for any usage and associated costs.
>
> We recommend reviewing all data being shared with and received from Third-Party Systems and being cognizant of third-party practices for handling, sharing, retention, and location of data. It is your responsibility to manage whether your data will flow outside of your organization’s Azure compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. See the [Azure OpenAI transparency note](../../../responsible-ai/agents/transparency-note.md).

## Feature support

| Feature | REST API | Python | .NET | JavaScript | Hosted agent | Prompt agent |
| ------- | -------- | ------ | ---- | ---------- | ------------ | ------------- |
| Skills CRUD (create, import, list, get, download, delete) | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Include downloaded skills in agent | N/A | N/A | N/A | N/A | ✔️ | N/A |

> [!IMPORTANT]
> Use skills in **hosted agents** only. The Skills REST API handles storage and retrieval. Your agent code bundles the downloaded `SKILL.md` files into the container image and loads them when creating sessions.

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

You're a friendly greeting assistant for Foundry Hosted Agents.

## Instructions

- Include the user's name if they provided one.
- Keep greetings concise — 1 to 2 sentences.
- Thank the user for trying out Foundry Hosted Agents and this sample skill.
```

| Field | Required | Rules |
| ----- | -------- | ----- |
| `name` | Yes | Short identifier, no spaces. **Must be unquoted** in YAML. |
| `description` | Yes | One-liner shown in skill listings. **Must be unquoted** in YAML. |
| Body | Yes | Free Markdown. Becomes the skill's injected instructions. |

> [!IMPORTANT]
> - The `name` and `description` values must be unquoted in the YAML front matter.
> - The use of quoted values (for example, `name: 'greeting'`) causes an HTTP 500
> error on import.

Place each skill in its own subdirectory under the agent root directory. For example, `greeting/SKILL.md`, not `SKILL.md` at the root.

## Manage skills with the REST API

The Skills REST API stores skills centrally so any hosted agent in your Foundry project can download and use them.

**Skills endpoint:** `{FOUNDRY_PROJECT_ENDPOINT}/skills`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope `https://ai.azure.com/.default`.

### Create a skill

You can create a skill in two ways: submit the content directly as JSON, or upload a ZIP archive containing a `SKILL.md` file.

#### Option 1: Create from JSON

Use this option when you want to supply the skill's `instructions` text directly without packaging a file.

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
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Create skill from JSON
    created = project.beta.skills.create(
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

// Create Foundry project client
var projectEndpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>";
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

// Create Foundry project client
const projectEndpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>";
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

Use this option when you have a `SKILL.md` file. Package it as a ZIP and POST to the `:import` endpoint. The skill name and description come from the `SKILL.md` front matter. The request body must be a valid ZIP file with a `SKILL.md` entry at the root.

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
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Import skill from ZIP package
    imported = project.beta.skills.create_from_package(
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

`has_blob: true` means the skill was created from a ZIP and can be downloaded. Skills created from JSON have `has_blob: false` and can't be downloaded.

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
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # List all skills in the project
    skills = list(project.beta.skills.list())
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
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Get skill by name
    skill = project.beta.skills.get("greeting")
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

Downloads the original ZIP archive for skills created through `:import` (`has_blob: true`). Returns HTTP 404 for skills created through JSON.

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
import tempfile
from datetime import datetime
from pathlib import Path
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"
download_folder = Path(tempfile.gettempdir()).resolve()

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Download skill package
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_path = download_folder / f"greeting_{timestamp}.zip"
    download_path.write_bytes(
        b"".join(project.beta.skills.download("greeting"))
    )
    print(f"Downloaded skill package to: {download_path}")
```

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> .NET sample isn't available yet.

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
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Delete skill
    deleted = project.beta.skills.delete("greeting")
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

After importing skills to Foundry through the REST API, download them into your agent project. The following walkthrough uses a [GitHub Copilot SDK sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot) that loads `SKILL.md` files from a local `skills/` directory and injects their contents as additional instructions into each session.

> [!NOTE]
> This sample requires a GitHub fine-grained personal access token (PAT) with **Copilot Requests → Read-only** permission. Create one at [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new). Classic tokens (`ghp_`) aren't supported — use a fine-grained PAT (`github_pat_`).

### Step 1: Initialize the agent project

Scaffold the project from the sample manifest:

```bash
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot/agent.manifest.yaml
```

Set the required GitHub token:

```bash
azd env set GITHUB_TOKEN="github_pat_..."
```

The scaffolded project includes `main.py`, configuration files, and a sample `joke` skill:

```
├── main.py                  ← agent code that loads skills via CopilotClient
├── agent.yaml
├── agent.manifest.yaml
├── requirements.txt
└── skills/
    └── joke/
        └── SKILL.md         ← bundled sample skill
```

In `main.py`, the `skill_directories` parameter tells the Copilot SDK where to find skill files. Any `SKILL.md` in a subdirectory of `skills/` is loaded as additional instructions when a session starts.

### Step 2: Add the greeting skill

Add the greeting skill you created in the [Author a skill](#author-a-skill) section. Create a subdirectory under `skills/` and add the `SKILL.md` file:

```bash
mkdir skills/greeting
```

Copy the greeting `SKILL.md` content from the [Author a skill](#author-a-skill) section into `skills/greeting/SKILL.md`. You can also use the download operation from [Download a skill](#download-a-skill) if you imported the skill to Foundry earlier.

The project now includes both skills:

```
├── main.py
├── agent.yaml
├── agent.manifest.yaml
├── requirements.txt
└── skills/
    ├── greeting/
    │   └── SKILL.md         ← your greeting skill
    └── joke/
        └── SKILL.md
```

### Step 3: Run and test locally

Start the agent:

```bash
azd ai agent run
```

In a separate terminal, test the greeting skill:

```bash
azd ai agent invoke --local '{"input": "Hi, my name is Alex!"}'
```

> [!TIP]
> On PowerShell, escape the inner quotes: `azd ai agent invoke --local '{\"input\": \"Hi, my name is Alex!\"}'`

### Step 4: Deploy and test remotely

Provision Azure resources and deploy the agent:

```bash
azd provision
azd deploy
```

Test the deployed agent on Foundry:

```bash
azd ai agent invoke '{"input": "Hi, my name is Alex!"}'
```

## Related content

- [Curate intent-based toolbox in Foundry](toolbox.md)
- [Deploy a hosted agent](../deploy-hosted-agent.md)
