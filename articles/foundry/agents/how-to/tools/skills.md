---
title: "Use skills with Microsoft Foundry agents (preview)"
description: "Manage versioned skills in Microsoft Foundry using the Skills REST API. Author SKILL.md files, store them centrally with version control, and attach them to toolboxes or hosted agents."
author: jonburchel
reviewer: lindazqli
ms.author: jburchel
ms.reviewer: zhuoqunli
ms.date: 06/24/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
zone_pivot_groups: selection-foundry-skills
ai-usage: ai-assisted
---

# Use skills in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

As agents grow beyond simple prototypes, teams accumulate behavioral guidelines that must stay consistent across every conversation. A support agent follows a fixed escalation policy. A code-review agent applies the same checklist each time. A sales agent respects set messaging constraints. When you embed these guidelines in each agent's system prompt or code, you create duplication. If the policy changes, you update and redeploy every agent that uses it.

Skills solve this problem by decoupling behavioral guidelines from agent code. A skill is a `SKILL.md` file that you author once and store centrally in Foundry through the versioned Skills API. You then deliver it to agents in two modes. **Attach to a toolbox** so any MCP client discovers and loads skills alongside tools. Or **download directly** into a Hosted or local agent project to inject the content into each session's context. Skills are versioned: every update creates a new immutable version, and the parent skill tracks a `default_version`. To update a skill, you create a new version, test it, then promote it to default without changing any agent code.

In this article, you learn how to:

- Create versioned skills and manage them through the Skills API.
- List, get, and delete skills and skill versions.
- Download skill content for use in a Hosted agent.
- Attach skills to a toolbox.

## Feature support

| Feature | REST API | Python | .NET | JavaScript | VS Code | Toolbox | Hosted agent |
| ------- | -------- | ------ | ---- | ---------- | ------- | ------- | ------------ |
| Create skill version (JSON inline content) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Create skill version (ZIP file upload) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| List, get, and delete skills and versions | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Download skill content | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Update skill default version | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A | N/A |
| Attach skills to a toolbox | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A |

## Limitations

Skills don't support private networking. The Skills API isn't accessible over a private endpoint, so you can't create, manage, or download skills from a Foundry resource that has public network access disabled.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Foundry User role on the Foundry project.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]

- [Visual Studio Code (VS Code)](https://code.visualstudio.com/).
- Install the [Microsoft Foundry Toolkit for Visual Studio Code extension](https://aka.ms/foundrytk) from the Visual Studio Code Marketplace.

## Author a skill

Skills follow the [Agent Skills](https://agentskills.io) specification format. A skill is a Markdown file with a YAML front matter block:

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

## Attach skills to a toolbox (preview)

After you create skill versions, attach them to a toolbox version so any MCP client can discover and load them alongside tools from the same endpoint. Toolbox-based skill discovery is in preview and follows the [Skills extension for the Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2640) specification (SEP-2640).

> [!IMPORTANT]
> Skills attached to a toolbox must exist in the same Foundry project. Cross-project references aren't supported.

When an agent or MCP client connects to the toolbox endpoint, skills appear as [MCP Resources](https://modelcontextprotocol.io/docs/concepts/resources). Clients that support the MCP Resources protocol call `resources/list` once at startup to discover all attached skills, then `resources/read` to download the content. Any MCP client — GitHub Copilot, Claude Code, or your own agent harness — can consume skills this way without any Foundry SDK.

Create a toolbox version that references the `greeting` skill you created earlier. Omit `version` to follow the skill's `default_version`, or pin a `version` string to lock the reference to an immutable snapshot.

:::zone pivot="rest-api"

```http
POST {endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
<<<<<<< HEAD
Foundry-Features: Skills=V1Preview
=======
Foundry-Features: Toolboxes=V1Preview
>>>>>>> origin/main

{
  "description": "Toolbox with a skill reference",
  "tools": [],
  "skills": [
    {
      "type": "skill_reference",
      "name": "greeting"
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import ToolboxSkillReference

# Reuse the AIProjectClient (project) from the previous step.
toolbox_version = project.beta.toolboxes.create_version(
    name="my-toolbox",
    description="Toolbox with a skill reference",
    tools=[],
    skills=[ToolboxSkillReference(name="greeting")],  # add version="v1" to pin
)
print(f"Created toolbox version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// Reuse the AgentToolboxes client (toolboxClient) from the previous step.
ToolboxSkillReference skillRef = new("greeting");  // add { Version = "v1" } to pin

ToolboxVersion toolboxVersion = toolboxClient.CreateToolboxVersion(
    name: "my-toolbox",
    tools: [],
    skills: [skillRef],
    description: "Toolbox with a skill reference"
);
Console.WriteLine($"Created toolbox version: {toolboxVersion.Version}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
// Reuse the AIProjectClient (project) from the previous step.
const toolboxVersion = await project.beta.toolboxes.createVersion(
  "my-toolbox",
  [],
  {
    description: "Toolbox with a skill reference",
    skills: [{ type: "skill_reference", name: "greeting" }],  // add version: "v1" to pin
  },
);
console.log(`Created toolbox version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="azd"

Declare skills in the `azd ai toolbox create --from-file` YAML, or attach them to an existing toolbox with `azd ai toolbox skill add`.

```yaml
# my-toolbox.yaml
description: Toolbox with a skill reference
skills:
  - name: greeting              # follows the skill's default version
  # - name: greeting
  #   version: "1"              # pin to a specific skill version (string)
```

```bash
azd ai toolbox create my-toolbox --from-file ./my-toolbox.yaml --no-prompt
```

:::zone-end

:::zone pivot="vscode"

In the Microsoft Foundry Toolkit for Visual Studio Code extension, attach skills to a toolbox in two ways:

- **During toolbox creation**: On the **Build a Custom Toolbox** tab, select **+ Add** > **Add skills**. In the **Select skills** dialog, select one or more configured skills, and then select **Add**.

  :::image type="content" source="../../media/tools/skills/skills-vs-code-toolbox-add-skills.png" alt-text="Screenshot of the Build a Custom Toolbox view in the Foundry Toolkit with the Add menu open and Add skills highlighted." lightbox="../../media/tools/skills/skills-vs-code-toolbox-add-skills.png":::

  :::image type="content" source="../../media/tools/skills/skills-vs-code-toolbox-select-skills.png" alt-text="Screenshot of the Select skills dialog in the Foundry Toolkit showing a configured skill that's ready to add to a toolbox." lightbox="../../media/tools/skills/skills-vs-code-toolbox-select-skills.png":::

- **From an existing skill**: In the **Tools** view, open the **Skills** tab and select **Use in a toolbox** in the skill's row.

Only skills already configured in your Foundry project appear in the **Select skills** dialog. To create a skill first, see [Create a skill version](#create-a-skill-version).

:::zone-end

For the full toolbox workflow — including connections, versioning, and the `azd ai toolbox skill add`, `azd ai toolbox skill list`, and `azd ai toolbox skill remove` commands — see the [Attach skills to a toolbox](toolbox.md#attach-skills-to-a-toolbox) section in the toolbox article. Changes from the imperative `azd` skill commands don't take effect for MCP clients until you promote the new version with `azd ai toolbox publish`.

### Consume toolbox skills in Microsoft Agent Framework

After you attach skills to a toolbox, an agent can discover and load them from the toolbox MCP endpoint at runtime instead of bundling `SKILL.md` files locally. For a complete C# example, see the [Skills in Toolbox sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework/foundry-toolbox-mcp-skills). The sample hosts an agent with the Microsoft Agent Framework Responses hosting layer and uses an `AgentSkillsProvider`, built with `AgentSkillsProviderBuilder.UseMcpSkills`, to apply the [Agent Skills](https://agentskills.io/) progressive-disclosure pattern:

1. **Advertise**: The provider injects skill names and descriptions into the system prompt so the agent knows which skills are available.
1. **Load**: When the agent decides a skill is relevant, it retrieves the full skill body from the toolbox.
1. **Read resources**: If a skill includes supplementary content, such as reference documents or assets, the agent reads them on demand.

The agent fetches the full skill body and resources from the toolbox only when it needs them, which reduces token usage. The sample consumes skills from an existing toolbox; it doesn't create or provision them.

## Manage skills with the REST API

The Skills API is versioned: creating a skill version auto-creates the skill if it doesn't exist yet. Each update creates a new immutable `SkillVersion`. The parent `Skill` object tracks `default_version` (the active version) and `latest_version`.

**Skills endpoint:** `{FOUNDRY_PROJECT_ENDPOINT}/skills`

**Authentication:** Bearer token from `DefaultAzureCredential` with scope `https://ai.azure.com/.default`.

**Preview header:** All Skills API calls require `Foundry-Features: Skills=V1Preview`.

| Object | Key fields | Description |
|--------|-----------|-------------|
| `Skill` | `id`, `name`, `description`, `created_at`, `default_version`, `latest_version` | The skill container. `default_version` points to the active version. |
| `SkillVersion` | `id`, `skill_id`, `name`, `version`, `description`, `created_at` | An immutable snapshot of the skill content. |

> [!TIP]
> For an end-to-end Python CRUD walkthrough — create two versions, switch `default_version`, fetch, list, delete — see the [`sample_skills_crud.py`](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/hosted_agents/sample_skills_crud.py) sample in the `azure-ai-projects` SDK.

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
    "instructions": "You are a friendly greeting assistant. Keep greetings brief and warm."
  },
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import SkillInlineContent

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project,
):
    # Create skill version from inline content
    created = project.beta.skills.create(
        name="greeting",
        inline_content=SkillInlineContent(
            description="Generate a personalized greeting for the user.",
            instructions="You are a friendly greeting assistant. Keep greetings brief and warm.",
        ),
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

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
AgentAdministrationClientOptions options = new();
options.AddPolicy(new FeaturePolicy("Skills=V1Preview"), PipelinePosition.PerCall);
AgentAdministrationClient agentsClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential(), options: options);
ProjectAgentSkills skillsClient = agentsClient.GetAgentSkills();

AgentsSkill created = skillsClient.CreateSkill(
    name: "greeting",
    description: "Generate a personalized greeting for the user.",
    instructions: "You are a friendly greeting assistant. Keep greetings brief and warm.");
Console.WriteLine($"Created skill: {created.Name}, Id: {created.SkillId}");

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

const skillVersion = await project.beta.skills.create("greeting", {
  inlineContent: {
    description: "Generate a personalized greeting for the user.",
    instructions: "You are a friendly greeting assistant. Keep greetings brief and warm.",
  },
});
console.log(`Created skill: ${skillVersion.name} version: ${skillVersion.version}`);
```

:::zone-end

:::zone pivot="azd"

Use the `azd ai skill` commands from the [Azure Developer CLI Foundry extensions](../install-cli-foundry-extensions.md).

**Prerequisites:**

```pwsh
azd extension install microsoft.foundry
azd auth login

azd ai project set "https://<account>.services.ai.azure.com/api/projects/<project>"
```

**Create the first version** with inline metadata:

```pwsh
azd ai skill create greeting `
  --description "Generate a personalized greeting for the user." `
  --instructions "You are a friendly greeting assistant. Keep greetings brief and warm." `
  --no-prompt
```

Or from a `SKILL.md` file. The `name:` field in the file must equal the positional argument:

```markdown
---
name: greeting
description: Generate a personalized greeting for the user.
---
# Greeting assistant

You are a friendly greeting assistant. Keep greetings brief and warm.
```

```pwsh
azd ai skill create greeting --file ./SKILL.md --no-prompt
```

**Add a new version** to an existing skill (auto-promoted to `default_version`):

```pwsh
azd ai skill update greeting --file ./SKILL.md --no-prompt

# Or with inline flags:
azd ai skill update greeting `
  --description "Updated description." `
  --instructions "Updated instructions." `
  --no-prompt
```

:::zone-end

:::zone pivot="vscode"

The Microsoft Foundry Toolkit for Visual Studio Code extension gives you two no-code ways to add a skill: browse the prebuilt catalog, or author a new skill in the editor.

**Add a prebuilt skill from the catalog**

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **Developer Tools** > **Agent Dev Tools**, select **Tool Catalog**.
1. In the **Skills** section, select **Add** on a skill card to register it in your Foundry project.

The catalog displays ready-to-use skills grouped by category:

| Category | Skills |
| --- | --- |
| **Office documents** | `docx`, `pptx`, `xlsx`, `pdf` |
| **Design & creative** | `canvas-design`, `algorithmic-art`, `brand-guidelines`, `theme-factory` |
| **Writing & comms** | `doc-coauthoring`, `internal-comms`, `slack-gif-creator` |

:::image type="content" source="../../media/tools/skills/skills-vs-code-catalog.png" alt-text="Screenshot of the Tool Catalog in the Foundry Toolkit showing the Skills section with prebuilt skill cards and Add buttons." lightbox="../../media/tools/skills/skills-vs-code-catalog.png":::

**Author a new skill**

1. In the **Tools** view, open the **Skills** tab.
1. Select **Add skill** > **Create skill**.
1. In the authoring panel, edit the `SKILL.md` template. Set the `name` and `description` in the YAML front matter, and define the instructions in the body.
1. Select **Create**.

:::image type="content" source="../../media/tools/skills/skills-vs-code-create.png" alt-text="Screenshot of the Create skill authoring panel in the Foundry Toolkit showing an editable SKILL.md template with name, description, and body." lightbox="../../media/tools/skills/skills-vs-code-create.png":::

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
    imported = project.beta.skills.create(
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

// CreateSkillFromPackage accepts a local directory containing a SKILL.md file.
AgentsSkill imported = skillsClient.CreateSkillFromPackage("path/to/greeting-directory");
Console.WriteLine($"Created skill from directory: {imported.Name}, Id: {imported.SkillId}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
import { readFileSync } from "fs";

const zipBytes = readFileSync("greeting.zip");
const skillVersion = await project.beta.skills.createFromFiles("greeting", {
  files: [{ contents: zipBytes, filename: "greeting.zip", contentType: "application/zip" }],
});
console.log(`Created skill: ${skillVersion.name} version: ${skillVersion.version}`);
```

:::zone-end

:::zone pivot="azd"

The CLI accepts a single `.zip` archive containing a `SKILL.md` plus any sibling assets. Bare folders are rejected — zip them first.

```pwsh
# Lay out the package, then zip it
mkdir skill-src\assets
# ... author skill-src/SKILL.md and any sibling assets ...
Compress-Archive -Path skill-src\* -DestinationPath greeting.zip -Force

# Upload as a new skill
azd ai skill create greeting --file ./greeting.zip --no-prompt
```

`azd ai skill update` rejects `.zip`. To replace an existing skill with a new package, use `create --force` — this deletes the existing skill and **all of its versions** first, then uploads v1 from the new zip:

```pwsh
azd ai skill create greeting --file ./greeting-v2.zip --force --no-prompt
```

:::zone-end

:::zone pivot="vscode"

1. In the **Tools** view, open the **Skills** tab.
1. Select **Add skill** > **Upload a skill**.
1. Select **Browse**, and then choose a skill file (`.md`) or a `.zip` folder that contains a `SKILL.md` file.
1. Select **Create**.

:::image type="content" source="../../media/tools/skills/skills-vs-code-upload.png" alt-text="Screenshot of the Upload a skill dialog in the Foundry Toolkit with a file picker for a SKILL.md file or a zip folder." lightbox="../../media/tools/skills/skills-vs-code-upload.png":::

To replace an existing skill with a new version, select the **...** (more actions) menu in the skill's row, and then select **Replace**. Upload the updated file. For more information, see [Delete a skill](#delete-a-skill).

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
  console.log(`${skill.name} (default: ${skill.default_version})`);
}
```

:::zone-end

:::zone pivot="azd"

```pwsh
azd ai skill list -o table
```

:::zone-end

:::zone pivot="vscode"

In the **Tools** view, open the **Skills** tab to list every skill in your project. Each row shows the skill name, description, and default version, along with actions to use the skill in a toolbox, view it, or manage it.

:::image type="content" source="../../media/tools/skills/skills-vs-code-list.png" alt-text="Screenshot of the Skills tab in the Foundry Toolkit Tools view listing a skill with its name, description, default version, and actions." lightbox="../../media/tools/skills/skills-vs-code-list.png":::

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

Use `last_id` with the `after` query parameter for forward cursor-based pagination.

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
    skill = project.beta.skills.get(name="greeting")
    print(f"{skill.name}: default version {skill.default_version}")
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

:::zone pivot="azd"

```pwsh
azd ai skill show greeting
```

:::zone-end

:::zone pivot="vscode"

The **Skills** tab shows each skill's metadata, including its name, description, and default version. To open the skill content, select **View skill** in the skill's row.

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

```csharp
#pragma warning disable AAIP001
// See the FeaturePolicy class definition and client setup in the Create a skill section above.

string savePath = Path.GetFullPath("saved_skill");
skillsClient.DownloadSkill("greeting", savePath);
Console.WriteLine($"Skill saved to: {savePath}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const response = await project.beta.skills.download("greeting");
const blob = await response.blobBody;
// blob is the ZIP archive (default version). For a specific version, use downloadVersion(name, version).
```

:::zone-end

:::zone pivot="azd"

Default mode extracts the skill into a directory (defaults to `./.agents/skills/<name>/`):

```pwsh
# Default version
azd ai skill download greeting --output-dir ./downloaded --no-prompt

# A specific version
azd ai skill download greeting --version 2 --output-dir ./downloaded-v2 --no-prompt
```

Raw mode keeps the original `.zip` archive untouched:

```pwsh
azd ai skill download greeting --raw --output-dir ./downloaded-raw --no-prompt
```

Pass `--force` to overwrite existing files in the output directory.

:::zone-end

:::zone pivot="vscode"

In the **Skills** tab, select **View skill** in the skill's row. A multi-file skill downloads as a `.zip` archive; a single-file skill opens directly in the editor.

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
    deleted = project.beta.skills.delete(name="greeting")
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

:::zone pivot="azd"

```pwsh
azd ai skill delete greeting --force
```

:::zone-end

:::zone pivot="vscode"

In the **Skills** tab, select the **...** (more actions) menu in the skill's row, and then select **Delete**. The same menu includes **Replace**, which uploads a new version of the skill.

:::image type="content" source="../../media/tools/skills/skills-vs-code-replace-delete.png" alt-text="Screenshot of the more actions menu in the Skills tab showing the Replace and Delete options for a skill." lightbox="../../media/tools/skills/skills-vs-code-replace-delete.png":::

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

:::zone pivot="vscode"

The **Default Version** dropdown in the **Skills** tab lists a skill's available versions. For full version metadata, use the REST API, Python, .NET, or JavaScript tab.

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
v = project.beta.skills.get_version(name="greeting", version="v1")
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

:::zone pivot="vscode"

To inspect a specific skill version, use the REST API, Python, .NET, or JavaScript tab.

:::zone-end

### Delete a skill version

To inspect a specific skill version, use the REST API, Python, .NET, or JavaScript tab.

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

:::zone pivot="vscode"

To delete a specific skill version, use the REST API, Python, .NET, or JavaScript tab.

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
const result = await project.beta.skills.update("greeting", "v2");
console.log(`New default version: ${result.default_version}`);
```

:::zone-end

:::zone pivot="azd"

```pwsh
azd ai skill update greeting --set-default-version v2 --no-prompt
```

`--set-default-version` is a metadata-only repoint — no upload, no new version. Use it to roll back (or forward) without touching skill content.

:::zone-end

:::zone pivot="vscode"

In the **Skills** tab, use the **Default Version** dropdown in the skill's row to repoint the skill to a different version. This change is metadata-only - toolboxes and agents that reference the skill without pinning a version automatically pick up the new default.

:::zone-end

## Use skills in a hosted agent

In **direct injection** mode, you download skills from the Foundry Skills API into your agent project directory. The agent reads the `SKILL.md` files at startup and injects their content as extra system instructions for each session. This mode works without a toolbox. Use it when you want to bundle specific skill versions with your agent code.

For the alternative mode — where skills and tools share a single discoverable endpoint that any MCP client can reach — see [Attach skills to a toolbox (preview)](#attach-skills-to-a-toolbox-preview).

The following walkthrough uses a [GitHub Copilot SDK sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot) that reads `SKILL.md` files from a local `skills/` directory. Use the [Download skill content](#download-skill-content) operation to pull skills from Foundry into this directory.

> [!NOTE]
> This sample requires a GitHub fine-grained personal access token (PAT) with **Copilot requests: Read-only** permission. Create one at [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new). Classic tokens (`ghp_`) aren't supported. Use a fine-grained PAT (`github_pat_`).

### Step 1: Initialize the agent project

Scaffold the project from the sample's `azure.yaml`:

```bash
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/invocations/github-copilot/azure.yaml
```

Set the required GitHub token:

```bash
azd env set GITHUB_TOKEN="github_pat_..."
```

The scaffolded project includes a root `azure.yaml`, agent code, configuration files, and a sample `joke` skill:

```
|-- azure.yaml
`-- src/
    `-- <agent-name>/
        |-- main.py          # agent code that loads skills via CopilotClient
        |-- requirements.txt
        `-- skills/
            `-- joke/
                `-- SKILL.md # bundled sample skill
```

In `main.py`, the `skill_directories` parameter tells the Copilot SDK where to find skill files. Any `SKILL.md` in a subdirectory of `skills/` is loaded as extra instructions when a session starts.

### Step 2: Populate skills from Foundry

Use the [Download skill content](#download-skill-content) operation to pull the greeting skill from Foundry. Extract the `SKILL.md` from the downloaded ZIP and save it to `skills/greeting/SKILL.md`:

```bash
mkdir skills/greeting
```

If you haven't stored the greeting skill in Foundry yet, copy the skill content from [Author a skill](#author-a-skill) directly into `skills/greeting/SKILL.md`.

The project now includes both skills:

```
|-- azure.yaml
`-- src/
    `-- <agent-name>/
        |-- main.py
        |-- requirements.txt
        `-- skills/
            |-- greeting/
            |   `-- SKILL.md # your greeting skill
            `-- joke/
                `-- SKILL.md
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
- [Agent Skills overview](https://agentskills.io/home)
