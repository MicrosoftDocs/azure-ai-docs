---
title: "Use skills with Microsoft Foundry agents (preview)"
description: "Manage versioned skills in Microsoft Foundry using the Skills REST API. Author SKILL.md files, store them centrally with version control, and attach them to toolboxes or hosted agents."
author: jonburchel
reviewer: lindazqli
ms.author: jburchel
ms.reviewer: zhuoqunli
ms.date: 05/23/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
zone_pivot_groups: selection-foundry-skills
ai-usage: ai-assisted
---

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

As agents grow beyond simple prototypes, teams accumulate behavioral guidelines that need to be consistent across every conversation. A support agent should always follow a specific escalation policy, a code-review agent should always apply the same checklist, and a sales agent should always respect certain messaging constraints. Embedding these guidelines directly in each agent's system prompt or code creates duplication: when the policy changes, you need to update and redeploy every agent that uses it.

Skills solve this problem by decoupling behavioral guidelines from agent code. A skill is a `SKILL.md` file you author once, store centrally in Foundry through the versioned Skills API, and reference from toolboxes or download into Hosted agent projects. Skills are versioned: every update creates a new immutable version while the parent skill tracks a `default_version`. When you update a skill, you create a new version, test it, then promote it to default without changing any agent code.

In this article, you learn how to:

- Create versioned skills and manage them through the Skills API.
- List, get, and delete skills and skill versions.
- Download skill content for use in a Hosted agent.
- Attach skills to a toolbox.

> [!IMPORTANT]
> If you use Skills with any third-party servers, agents, code, or with models outside the Foundry Models category sold by Azure ("Third-Party Systems"), you do so at your own risk. Third-Party Systems are Non-Microsoft Products under the Microsoft Product Terms and follow their own third-party license terms. You're responsible for any usage and associated costs.
>
> Review all data shared with and received from Third-Party Systems. Be aware of third-party practices for handling, sharing, retention, and location of data. Similarly, if you connect to or integrate with non-Foundry Microsoft services and features, it's important to review their data practices. You must manage whether your data flows outside your organization's Azure compliance and geographic boundaries, understand any related implications, and confirm that appropriate permissions, boundaries, and approvals are in place.
>
> You're responsible for carefully reviewing and testing applications you build for your specific use cases. Implement your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems. Ensure your applications meet appropriate quality, reliability, security, and trustworthiness standards. See the [Foundry Agent Service transparency note](../../../responsible-ai/agents/transparency-note.md).

## Feature support

| Feature | REST API | Python | .NET | JavaScript | Toolbox | Hosted agent |
| ------- | -------- | ------ | ---- | ---------- | ------- | ------------ |
| Create skill version (JSON inline content) | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Create skill version (ZIP file upload) | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| List, get, and delete skills and versions | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Download skill content | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Update skill default version | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Attach skills to a toolbox | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A |

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Foundry User role on the Foundry project.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]

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
- Keep greetings concise, 1 to 2 sentences.
- Thank the user for trying out Foundry Hosted Agents and this sample skill.
```

| Field | Required | Rules |
| ----- | -------- | ----- |
| `name` | Yes | **Skill name** used as the URL path key. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen or contain consecutive hyphens. Maximum 64 characters. Pattern: `^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$`. **Must be unquoted** in YAML. |
| `description` | Yes | One-liner shown in skill listings. Maximum 1,024 characters. **Must be unquoted** in YAML. |
| Body | Yes | Free Markdown. Becomes the skill's injected instructions. |

> [!IMPORTANT]
> - The `name` and `description` values must be unquoted in the YAML front matter.
> - Skill names follow the pattern `^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$` (lowercase, numbers, and hyphens, no leading/trailing hyphens, max 64 characters). Invalid names cause an `invalid_payload` error on version creation.

Place each skill in its own subdirectory under the agent root directory. For example, `greeting/SKILL.md`, not `SKILL.md` at the root.

## Attach skills to a toolbox

After you create skill versions, attach skills to a toolbox version so agents can discover and load them through the toolbox's MCP endpoint.

> [!IMPORTANT]
> Skills can only reference skills in the same Foundry project as the toolbox.

When agents connect to the toolbox MCP endpoint, skills are exposed as [MCP Resources](https://modelcontextprotocol.io/docs/concepts/resources). The MCP client or agent framework must support the MCP Resources protocol (`resources/list`, `resources/read`) to discover and load the skills automatically.

For REST, Python, .NET, JavaScript, and `azd` examples of adding skill references to a toolbox version, see the [Attach skills to a toolbox](toolbox.md#attach-skills-to-a-toolbox) section in the toolbox article.

## Manage skills with the REST API

The Skills API is versioned: creating a skill version auto-creates the skill if it doesn't exist yet. Each update creates a new immutable `SkillVersion`. The parent `Skill` object tracks `default_version` (the active version) and `latest_version`.

**Skills endpoint:** `{FOUNDRY_PROJECT_ENDPOINT}/skills`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope `https://ai.azure.com/.default`.

**Preview header:** All Skills API calls require `Foundry-Features: Skills=V1Preview`.

| Object | Key fields | Description |
|--------|-----------|-------------|
| `Skill` | `id`, `name`, `description`, `created_at`, `default_version`, `latest_version` | The skill container. `default_version` points to the active version. |
| `SkillVersion` | `id`, `skill_id`, `name`, `version`, `description`, `created_at` | An immutable snapshot of the skill content. |

### Create a skill version

Creating a version auto-creates the parent skill if it doesn't exist. After creating a version, call [Update default version](#update-default-version) to make it the active version.

You can create a version in two ways: submit the content directly as JSON via `inline_content`, or upload a ZIP archive containing a `SKILL.md` file.

#### Option 1: Create from inline content (JSON)

Use this option when you want to supply the skill's `instructions` text directly without packaging a file.

:::zone pivot="rest-api"

```http
POST {endpoint}/skills/greeting/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
Foundry-Features: Skills=V1Preview

{
  "inline_content": {
    "description": "Generate a personalized greeting for the user.",
    "instructions": "You are a friendly greeting assistant. Include the user's name and keep greetings concise."
  },
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
    # Create skill version from inline content
    created = project.beta.skills.create_version(
        name="greeting",
        inline_content={
            "description": "Generate a personalized greeting for the user.",
            "instructions": "You are a friendly greeting assistant. Include the user's name and keep greetings concise.",
        },
    )
    print(
        f"Created skill: {created.name} version: {created.version}"
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

AgentsSkillVersion created = skillsClient.CreateSkillVersion(
    name: "greeting",
    inlineContent: new SkillInlineContent(
        description: "Generate a personalized greeting for the user.",
        instructions: "You are a friendly greeting assistant. Include the user's name and keep greetings concise."
    ),
);
Console.WriteLine($"Created skill: {created.Name} version: {created.Version}");

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

const skillVersion = await project.beta.skills.createVersion("greeting", {
  inlineContent: {
    description: "Generate a personalized greeting for the user.",
    instructions: "You are a friendly greeting assistant. Include the user's name and keep greetings concise.",
  },
});
console.log(`Created skill: ${skillVersion.name} version: ${skillVersion.version}`);
```

:::zone-end
Example response (`SkillVersion` object):

```json
{
  "id": "skillver_abc123",
  "skill_id": "skill_abc123",
  "name": "greeting",
  "version": "v1",
  "description": "Generate a personalized greeting for the user.",
  "created_at": 1741305600
}
```

#### Option 2: Create from a SKILL.md ZIP

Use multipart form upload when you have a `SKILL.md` file. The skill name comes from the `{name}` path parameter. Upload a single ZIP file or multiple individual files. The `SKILL.md` is parsed to populate the version description and instructions.

:::zone pivot="rest-api"

```http
POST {endpoint}/skills/greeting/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: multipart/form-data
Accept: application/json
Foundry-Features: Skills=V1Preview

--boundary
Content-Disposition: form-data; name="files"; filename="SKILL.md"
Content-Type: text/markdown

<SKILL.md content>
--boundary--
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
    # Create skill version from ZIP / SKILL.md file
    imported = project.beta.skills.create_version(
        name="greeting",
        file=Path("greeting.zip").read_bytes(),
    )
    print(
        f"Created skill: {imported.name} version: {imported.version}"
    )
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

// CreateSkillVersionFromPackage accepts a local zip or directory path containing a SKILL.md file.
AgentsSkillVersion imported = skillsClient.CreateSkillVersionFromPackage(
    name: "greeting",
    packagePath: "path/to/skill-directory",
);
Console.WriteLine($"Created skill: {imported.Name} version: {imported.Version}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
import { readFileSync } from "fs";

const zipBytes = readFileSync("greeting.zip");
const skillVersion = await project.beta.skills.createVersion("greeting", {
  file: zipBytes,
});
console.log(`Created skill: ${skillVersion.name} version: ${skillVersion.version}`);
```

:::zone-end

> [!NOTE]
> For ZIP uploads, the server extracts and validates the `SKILL.md` content. For individual file uploads, files are validated as-is.

Example response (`SkillVersion` object):

```json
{
  "id": "skillver_def456",
  "skill_id": "skill_def456",
  "name": "greeting",
  "version": "v1",
  "description": "Generate a personalized greeting for the user.",
  "created_at": 1741305600
}
```

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
        print(f"  {skill.name} (default: {skill.default_version})")
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
    Console.WriteLine($"  - {item.Name} (default: {item.DefaultVersion})");
}
```

:::zone-end
:::zone pivot="javascript"

```javascript
const skills = project.beta.skills.list({ limit: 20, order: "desc" });
for await (const skill of skills) {
  console.log(`${skill.name} (default: ${skill.defaultVersion})`);
}
```

:::zone-end
Example response:

```json
{
  "data": [
    {
      "id": "skill_abc123",
      "name": "greeting",
      "description": "Generate a personalized greeting for the user.",
      "created_at": 1741305600,
      "default_version": "v1",
      "latest_version": "v1"
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

### Download skill content

Downloads the skill content as a ZIP archive. Use the default version endpoint to get the active version, or the version-specific endpoint to get a specific version.

:::zone pivot="rest-api"

```http
# Download default version content
GET {endpoint}/skills/{name}/content?api-version=v1
Authorization: Bearer {token}
Accept: application/zip
Foundry-Features: Skills=V1Preview

# Download a specific version's content
GET {endpoint}/skills/{name}/versions/{version}/content?api-version=v1
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
        b"".join(project.beta.skills.download_content("greeting"))
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
const response = await project.beta.skills.downloadContent("greeting");
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
  "name": "greeting",
  "deleted": true
}
```

### List skill versions

:::zone pivot="rest-api"

```http
GET {endpoint}/skills/{name}/versions?api-version=v1
Authorization: Bearer {token}
Accept: application/json
Foundry-Features: Skills=V1Preview
```

:::zone-end

:::zone pivot="python"

```python
versions = list(project.beta.skills.list_versions("greeting"))
for v in versions:
    print(f"  {v.name} version: {v.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
List<AgentsSkillVersion> versions = [.. skillsClient.GetSkillVersions("greeting")];
foreach (var v in versions)
    Console.WriteLine($"  {v.Name} version: {v.Version}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const versions = project.beta.skills.listVersions("greeting");
for await (const v of versions) {
  console.log(`  ${v.name} version: ${v.version}`);
}
```

:::zone-end

Example response:

```json
{
  "data": [
    {
      "id": "skillver_abc123",
      "skill_id": "skill_abc123",
      "name": "greeting",
      "version": "v1",
      "description": "Generate a personalized greeting for the user.",
      "created_at": 1741305600
    }
  ],
  "has_more": false
}
```

### Get a skill version

:::zone pivot="rest-api"

```http
GET {endpoint}/skills/{name}/versions/{version}?api-version=v1
Authorization: Bearer {token}
Accept: application/json
Foundry-Features: Skills=V1Preview
```

:::zone-end

:::zone pivot="python"

```python
v = project.beta.skills.get_version("greeting", "v1")
print(f"{v.name} version: {v.version}, description: {v.description}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
AgentsSkillVersion v = skillsClient.GetSkillVersion("greeting", "v1");
Console.WriteLine($"{v.Name} version: {v.Version}, description: {v.Description}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const v = await project.beta.skills.getVersion("greeting", "v1");
console.log(`${v.name} version: ${v.version}`);
```

:::zone-end

### Delete a skill version

:::zone pivot="rest-api"

```http
DELETE {endpoint}/skills/{name}/versions/{version}?api-version=v1
Authorization: Bearer {token}
Accept: application/json
Foundry-Features: Skills=V1Preview
```

:::zone-end

:::zone pivot="python"

```python
result = project.beta.skills.delete_version("greeting", "v1")
print(f"Deleted version: {result.version} ({result.deleted})")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
skillsClient.DeleteSkillVersion("greeting", "v1");
Console.WriteLine("Skill version deleted.");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const result = await project.beta.skills.deleteVersion("greeting", "v1");
console.log(`Deleted version: ${result.version} (${result.deleted})`);
```

:::zone-end

Returns HTTP 200 on success:

```json
{
  "id": "skillver_abc123",
  "name": "greeting",
  "deleted": true,
  "version": "v1"
}
```

### Update default version

Change which version the skill resolves to by default. Toolboxes and agents that reference the skill without pinning a version use the `default_version`.

:::zone pivot="rest-api"

```http
POST {endpoint}/skills/{name}?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
Foundry-Features: Skills=V1Preview

{
  "default_version": "v2"
}
```

:::zone-end

:::zone pivot="python"

```python
result = project.beta.skills.update("greeting", default_version="v2")
print(f"New default version: {result.default_version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
AgentsSkill updated = skillsClient.UpdateSkillDefaultVersion("greeting", "v2");
Console.WriteLine($"New default version: {updated.DefaultVersion}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const result = await project.beta.skills.update("greeting", { defaultVersion: "v2" });
console.log(`New default version: ${result.defaultVersion}`);
```

:::zone-end
## Use skills in a hosted agent

After importing skills to Foundry through the REST API, download them into your agent project. The following walkthrough uses a [GitHub Copilot SDK sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot) that loads `SKILL.md` files from a local `skills/` directory and injects their contents as extra instructions into each session.

> [!NOTE]
> This sample requires a GitHub fine-grained personal access token (PAT) with **Copilot Requests â Read-only** permission. Create one at [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new). Classic tokens (`ghp_`) aren't supported. Use a fine-grained PAT (`github_pat_`).

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

In `main.py`, the `skill_directories` parameter tells the Copilot SDK where to find skill files. Any `SKILL.md` in a subdirectory of `skills/` is loaded as extra instructions when a session starts.

### Step 2: Add the greeting skill

Add the greeting skill you created in the [Author a skill](#author-a-skill) section. Create a subdirectory under `skills/` and add the `SKILL.md` file:

```bash
mkdir skills/greeting
```

Copy the greeting `SKILL.md` content from the [Author a skill](#author-a-skill) section into `skills/greeting/SKILL.md`. You can also use the download operation from [Download skill content](#download-skill-content) if you imported the skill to Foundry earlier.

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

Create Azure resources and deploy the agent:

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
- [Deploy a Hosted agent](../deploy-hosted-agent.md)
