---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 06/04/2026
ms.custom: include, doc-kit-assisted
ai-usage: ai-assisted
---

Skills are versioned bundles of files that you can reuse across shell environments in the **Responses API**. Use skills to codify processes and conventions—anything from a company style guide to a multi-step workflow—and make them available to the model when it runs the [shell tool](../how-to/shells.md).

A skill is a bundle of files plus a `SKILL.md` manifest. The manifest contains YAML front matter and prompt-style instructions. The model uses the front matter to discover the skill, and reads the instructions when it decides to invoke the skill. Skills are compatible with the open [Agent Skills standard](https://agentskills.io/home).

> [!IMPORTANT]
> Skills can influence planning, tool selection, and command execution. Treat every skill as privileged code and review it carefully before you use it. For more information, see [Risks and safety](#risks-and-safety).

> [!NOTE]
> Skills require an Azure OpenAI API version that supports the shell tool and skills. Confirm support for your target API version before you deploy to production.

## Prerequisites

- An Azure OpenAI model deployed that supports the Responses API and the shell tool.
- An authentication method:
  - API key, or
  - Microsoft Entra ID.
- Install the client library for your language:
  - **Python**: `pip install openai azure-identity`
  - **JavaScript/TypeScript**: `npm install openai @azure/identity`
- For REST examples, set `AZURE_OPENAI_API_KEY` (API key flow) or `AZURE_OPENAI_AUTH_TOKEN` (Microsoft Entra ID flow).

## What's in a skill

A skill bundle has a single top-level folder that contains a `SKILL.md` manifest and any supporting files:

```text
csv-insights/
├── SKILL.md
├── scripts/
│   └── summarize.py
└── templates/
    └── report.md
```

The `SKILL.md` file declares the skill's `name` and `description` in YAML front matter, and provides the instructions the model follows when the skill is invoked. Front matter validation follows the [Agent Skills specification](https://agentskills.io/specification#name-field).

## Create a skill

Upload a skill bundle in either of these formats:

- **Directory upload (multipart)**: Upload multiple files. Each part includes the file path relative to a single top-level folder.
- **Zip upload**: Zip a single top-level folder and upload the `.zip` file.

The upload returns a `skill_id` that you reference when you attach the skill to a shell environment.

## Use skills with hosted shell

To make skills available in a hosted shell environment, attach them through the environment's `skills` array. After a skill is mounted, the model decides whether to invoke it based on your prompt.

In the examples that follow, replace `gpt-5.5` with the name of your own model deployment.

# [Python](#tab/python)

```python
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

# Create the client against the Azure OpenAI v1 endpoint.
openai = OpenAI(base_url=endpoint, api_key=token_provider)

# Mount skills in an auto-provisioned hosted container.
response = openai.responses.create(
    model="gpt-5.5",
    tools=[{
        "type": "shell",
        "environment": {
            "type": "container_auto",
            "skills": [{"type": "skill_reference", "skill_id": "<skill_id>"}],
        },
    }],
    input="Use the csv-insights skill to summarize report.csv.",
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)

```javascript
import { OpenAI } from "openai";
import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

const endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
const tokenProvider = getBearerTokenProvider(
  new DefaultAzureCredential(),
  "https://ai.azure.com/.default"
);

// Create the client against the Azure OpenAI v1 endpoint.
const openai = new OpenAI({ baseURL: endpoint, apiKey: await tokenProvider() });

// Mount skills in an auto-provisioned hosted container.
const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [{
    type: "shell",
    environment: {
      type: "container_auto",
      skills: [{ type: "skill_reference", skill_id: "<skill_id>" }],
    },
  }],
  input: "Use the csv-insights skill to summarize report.csv.",
});

console.log(response.output_text);
```

---

> [!TIP]
> After a skill is mounted, the model decides when to use it. For more deterministic behavior, instruct the model to use a named skill—for example, *Use the `csv-insights` skill to summarize the report.*

Reference: [Use the shell tool with the Responses API](../how-to/shells.md) | [OpenAI Python SDK](https://github.com/openai/openai-python) | [OpenAI Node SDK](https://github.com/openai/openai-node)

## Use skills with local shell mode

Skills also work with local shell mode. Instead of using a `skill_reference`, supply skill files from local paths in the runtime you control.

# [Python](#tab/python)

```python
# Mount a skill from a local path in local shell mode.
response = openai.responses.create(
    model="gpt-5.5",
    tools=[{
        "type": "shell",
        "environment": {
            "type": "local",
            "skills": [{
                "name": "csv-insights",
                "description": "Summarize CSV files and produce a markdown report.",
                "path": "<path-to-skill-folder>",
            }],
        },
    }],
    input="Use the csv-insights skill to summarize today's CSV reports.",
)

print(response.output_text)
```

# [JavaScript](#tab/javascript)

```javascript
// Mount a skill from a local path in local shell mode.
const response = await openai.responses.create({
  model: "gpt-5.5",
  tools: [{
    type: "shell",
    environment: {
      type: "local",
      skills: [{
        name: "csv-insights",
        description: "Summarize CSV files and produce a markdown report.",
        path: "<path-to-skill-folder>",
      }],
    },
  }],
  input: "Use the csv-insights skill to summarize today's CSV reports.",
});

console.log(response.output_text);
```

---

> [!NOTE]
> Local shell mode doesn't support uploaded `skill_reference` attachments. Supply skill files from local paths instead.

## Inline skills

If you don't want to create an uploaded skill, you can inline a base64-encoded zip bundle in the environment's `skills` array. Inline skills are useful when you want a skill to live only for the duration of a single container's lifecycle.

```python
import base64

# Read and encode a local skill bundle.
with open("csv_insights.zip", "rb") as f:
    inline_zip = base64.b64encode(f.read()).decode("utf-8")

# Create a container with the inline skill mounted.
container = openai.containers.create(
    name="inline-skill-container",
    skills=[{
        "type": "inline",
        "name": "csv-insights",
        "description": "Summarize CSV files and produce a markdown report.",
        "source": {
            "type": "base64",
            "media_type": "application/zip",
            "data": inline_zip,
        },
    }],
)

print(container.id)
```

## Versioning and management

Skills are versioned. Each upload creates a new version, and you reference a version through the `version` field on a `skill_reference`. The `version` field accepts an integer or `"latest"`.

Two pointers track versions:

- `default_version` is used when you don't provide a version in a `skill_reference`.
- `latest_version` tracks the newest upload.

Deletion follows these rules:

- You can't delete the default version. Set another version as the default first.
- Deleting the last remaining version deletes the skill itself.
- Deleting a skill removes all its versions.

## Limits and validation

| Limit | Value |
| --- | --- |
| `SKILL.md` files per bundle | Exactly one (filename matching is case-insensitive) |
| Maximum zip upload size | 50 MB |
| Maximum file count per skill version | 500 |
| Maximum uncompressed file size | 25 MB |

Skill front matter validation follows the [Agent Skills specification](https://agentskills.io/specification#name-field).

## Risks and safety

Always inspect a skill before you use it with the Responses API. Skills introduce security risks such as prompt-injection-driven data exfiltration and unauthorized command execution. Follow these practices:

- **Treat skills as privileged code and instructions.** Skill content can influence planning, tool usage, and command execution. Treat any skill as potentially untrusted input until you validate it.
- **Don't expose an open skills catalog to end users.** Open selection of arbitrary skills increases the risk of prompt injection, policy bypass, and destructive actions from unvetted automation.
- **Integrate skills at the developer level.** Map each skill to a specific product workflow, prevent end users from selecting arbitrary skills, and gate high-impact actions behind explicit approval and policy checks.
- **Require approval for sensitive actions.** For workflows that can perform write or high-impact actions, require explicit approval before execution.

## Related content

- [Use the shell tool with the Responses API](../how-to/shells.md)
- [Use the Azure OpenAI Responses API](../how-to/responses.md)
