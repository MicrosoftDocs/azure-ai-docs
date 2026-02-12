---
title: Configure Claude Code with Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Set up Claude Code CLI and VS Code extension to use Claude models in Microsoft Foundry with enterprise security, authentication, and CI/CD integration.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/03/2026
ms.custom: dev-focus
author: msakande
ms.author: mopeakande
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to configure Claude Code, Anthropic's agentic coding tool, to use Microsoft Foundry so I can use enterprise-managed Claude models for AI-assisted coding with proper security and compliance.
---

# Configure Claude Code with Microsoft Foundry

Anthropic's [Claude Code](https://docs.anthropic.com/en/docs/claude-code) is an AI coding agent available as a CLI tool and VS Code extension. When you configure Claude Code with Microsoft Foundry, you run the coding agent on Azure infrastructure while keeping your data inside your compliance boundary. This configuration provides enterprise-grade security, private networking, role-based access control, and cost management.

In this article, you learn how to:

- Install and configure Claude Code CLI for Microsoft Foundry
- Set up the Claude Code VS Code extension
- Authenticate with Microsoft Entra ID or API keys
- Create project context files for better AI assistance
- Integrate Spec Kit for structured development workflows
- Run Claude Code in GitHub Actions for CI/CD automation

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- Access to Microsoft Foundry with appropriate permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md) created in one of the [supported regions](../../how-to/deploy-models-serverless-availability.md#region-availability) for Claude models.
- Node.js 18 or later installed for the Claude Code CLI.
- (Optional) [Azure CLI](/cli/azure/install-azure-cli) installed with `az login` completed for Microsoft Entra ID authentication.

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

### System requirements

| Requirement | Details |
| ----------- | ------- |
| Operating system | macOS 12+, Ubuntu 20.04+/Debian 10+, Windows 11 via WSL2 |
| RAM | 4-GB minimum (8-GB recommended) |
| Git (optional) | 2.23+ for pull request helpers |

## Deploy a Claude model

Before configuring Claude Code, deploy an available [Claude model](../concepts/models-from-partners.md#anthropic) in Microsoft Foundry. Claude models in Foundry are available for [global standard deployment](../concepts/deployment-types.md#global-standard). 

To deploy a Claude model, such as Opus 4.5, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md).

After deployment, select the **Details** tab and note your **Target URI** and **Key**. You need these values for configuration.


### Alternative: Use Model Router

[Model Router](../../openai/concepts/model-router.md) is a Foundry model that intelligently routes each prompt to the best underlying model based on query complexity, cost, and performance. Model Router version `2025-11-18` supports Claude Haiku 4.5, Sonnet 4.5, and Opus 4.1 alongside GPT, DeepSeek, Llama, and Grok models.

Benefits for Claude Code users:

- **Automatic model selection**: Simple prompts route to faster, cheaper models. Complex coding tasks route to more capable models.
- **Cost optimization**: Use routing profiles to balance quality versus cost while maintaining baseline performance.
- **Single endpoint**: One deployment handles all routing decisions across your model fleet.

To use Model Router with Claude Code, first deploy the Claude models you want included, then deploy Model Router and enable them through [model subset configuration](../../openai/how-to/model-router.md#select-your-model-subset).

## Install Claude Code CLI

Install the Claude Code CLI and verify the installation. Use npm or Homebrew.

**Installation with npm**

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

**Installation with Homebrew**

```bash
brew install claude-code
claude --version
```

For more installation options, see [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code).

## Configure environment variables

Set environment variables to connect Claude Code to your Microsoft Foundry deployment.

> [!TIP]
> Find your Foundry resource name in the Azure portal under your resource's **Overview** page, or in the Foundry portal URL: `https://ai.azure.com/resource/{your-resource-name}`.

# [Bash / WSL](#tab/bash)

```bash
# Required: Enable Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Optional: Specify model deployment names if different from defaults
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-5"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-5"
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-5"
```

# [PowerShell](#tab/powershell)

```powershell
# Required: Enable Foundry integration
$env:CLAUDE_CODE_USE_FOUNDRY = "1"

# Azure resource name (replace {resource} with your resource name)
$env:ANTHROPIC_FOUNDRY_RESOURCE = "{resource}"
# Or provide the full base URL:
# $env:ANTHROPIC_FOUNDRY_BASE_URL = "https://{resource}.services.ai.azure.com"

# Optional: Specify model deployment names if different from defaults
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "claude-sonnet-4-5"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "claude-haiku-4-5"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "claude-opus-4-5"
```

---

## Authenticate with Foundry

Choose one of the following authentication methods.

### Option A: Microsoft Entra ID (recommended)

Microsoft Entra ID authentication uses your Azure CLI credentials automatically. Run `az login` before starting Claude Code:

```bash
az login
```

Claude Code detects your Azure CLI session and uses it for authentication without extra configuration.

### Option B: API key

If you prefer API key authentication, set the key in your environment variables.

# [Bash / WSL](#tab/bash)

```bash
export ANTHROPIC_FOUNDRY_API_KEY="your-foundry-api-key"
```

# [PowerShell](#tab/powershell)

```powershell
$env:ANTHROPIC_FOUNDRY_API_KEY = "your-foundry-api-key"
```

---

Find your API key in the Foundry portal under your model deployment's **Details** tab.

## Configure the VS Code extension

The Claude Code VS Code extension provides a native graphical interface for Claude Code directly in your IDE.

1. Install the extension from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code).

1. Open VS Code settings (**Ctrl+,** or **Cmd+,**) and search for **Claude Code: Environment Variables**.

1. Select **Edit in settings.json** and add the following configuration:

    ```json
    {
      "Claude Code: Environment Variables": {
        "CLAUDE_CODE_USE_FOUNDRY": "1",
        "ANTHROPIC_FOUNDRY_RESOURCE": "{your-resource-name}",
        "ANTHROPIC_FOUNDRY_API_KEY": "<optional-for-non-entra-auth>"
      }
    }
    ```

1. Select the **Spark icon** in the sidebar to open the Claude Code panel.

1. Claude Code authenticates using your Azure credentials. Run `az login` first if you're using Microsoft Entra ID authentication.

The extension supports auto-accept edits mode, plan mode, extended thinking, and file management with @-mentions—all while routing through your Microsoft Foundry deployment.

## Validate the configuration

Verify that Claude Code is correctly configured to use Microsoft Foundry. Open a terminal, launch Claude Code, and run the `/status` command:

```bash
claude
> /status
```

The output should look similar to:

```text
Claude Code v1.0.0
─────────────────────────────────────
API Provider:      Microsoft Foundry
Foundry Resource:  your-resource-name
Model:             claude-sonnet-4-5
Status:            Connected
─────────────────────────────────────
```

Confirm the following in the status output:

| Field | Expected value |
| ----- | -------------- |
| API provider | Microsoft Foundry |
| Foundry resource | Your Foundry resource name |
| Model | Your deployed model (for example, `claude-sonnet-4-5`) |

## Create project context with CLAUDE.md

Claude Code reads `CLAUDE.md` files for project context. Files load in order, with later files overriding earlier ones:

1. `~/.claude/CLAUDE.md` – Global defaults across all projects
1. `./CLAUDE.md` – Repository root settings
1. `./current-dir/CLAUDE.md` – Current directory specifics

Create a `CLAUDE.md` file in your project root to help Claude Code understand your codebase. Here's an example for a [Microsoft Agent Framework](https://aka.ms/agent-framework) project:

````markdown
# Project: Customer Service Agent

## Overview
Multi-agent system using Microsoft Agent Framework with Foundry Agent Service.

## Tech Stack
- Python 3.11+
- agent-framework (Microsoft Agent Framework Python SDK)
- Microsoft Foundry for hosted agents
- MCP tools for enterprise data access

## Architecture
- `src/agents/` - Agent definitions (triage, specialist, escalation)
- `src/tools/` - MCP tool implementations
- `src/workflows/` - Multi-agent orchestration
- `tests/` - pytest with async fixtures

## Commands
```bash
# Run locally
python -m src.main

# Test
pytest tests/ -v

# Deploy to Foundry Agent Service
az ai agent deploy --config deploy.yaml
```

## Code Patterns
Use `AzureAIAgentClient` with `AzureCliCredential`:
```python
async with AzureAIAgentClient(async_credential=AzureCliCredential()) as client:
    agent = client.create_agent(instructions="...", tools=[...])
```

## Current Sprint
- Implementing RAG grounding with Foundry IQ
- Adding Fabric connector for sales data
````

To get Claude Code to read your `CLAUDE.md` and understand your project context, run these commands in your terminal:

```bash
# Start Claude Code in your project
cd your-project
claude

# Or run a one-off command
claude "explain the agent orchestration in src/workflows/"
```


## (Optional) Integrate Spec Kit for structured development

[Spec Kit](https://github.com/github/spec-kit) provides structured commands for turning requirements into implementation. Install it [globally or for one-time use](https://github.com/github/spec-kit?tab=readme-ov-file#1-install-specify-cli).

| Command | Purpose | Output |
| ------- | ------- | ------ |
| `/speckit.constitution` | Set project principles and coding standards | `.speckit/constitution.md` |
| `/speckit.specify` | Define feature requirements | `.speckit/spec.md` |
| `/speckit.plan` | Create architecture and dependencies | `.speckit/plan.md` |
| `/speckit.tasks` | Generate ordered task list | `.speckit/tasks.md` |
| `/speckit.implement` | Execute tasks and create files | Implementation files |

### Example: Build an Agent Framework tool

The following example shows how to use Spec Kit commands to build a SharePoint MCP tool for RAG grounding:

```bash
# 1. Set project principles
claude /speckit.constitution
# Creates .speckit/constitution.md with coding standards, patterns

# 2. Define the feature
claude /speckit.specify
> "Add a SharePoint MCP tool that retrieves documents for RAG grounding"
# Creates .speckit/spec.md with requirements

# 3. Plan implementation
claude /speckit.plan
# Creates .speckit/plan.md with architecture, dependencies

# 4. Generate tasks
claude /speckit.tasks
# Creates .speckit/tasks.md with ordered task list

# 5. Implement
claude /speckit.implement
# Executes tasks, creates files, runs tests
```

For detailed usage and installation, see [Spec Kit on GitHub](https://github.com/github/spec-kit).

## Run Claude Code in GitHub Actions

Claude Code integrates with GitHub Actions for CI/CD automation. Store your API key in the repository's secret store before using these workflows.

### Generate tests on pull requests

Create a workflow that generates tests when agent or tool files change:

```yaml
name: Generate Agent Tests
on:
  pull_request:
    paths:
      - 'src/agents/**'
      - 'src/tools/**'

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Claude Code
        uses: anthropic-ai/claude-code-action@v1
        with:
          prompt: |
            Review the changed agent files and generate pytest tests.
            Use async fixtures for AIProjectClient mocking.
            Follow patterns in tests/conftest.py.
          allowed_tools: "edit,write,bash"
        env:
          CLAUDE_CODE_USE_FOUNDRY: "1"
          ANTHROPIC_FOUNDRY_RESOURCE: ${{ secrets.AZURE_FOUNDRY_RESOURCE }}
          ANTHROPIC_FOUNDRY_API_KEY: ${{ secrets.AZURE_FOUNDRY_API_KEY }}
```

### Trigger PR review with @claude

Create a workflow that responds to @claude mentions in pull request comments:

```yaml
name: Claude PR Assistant
on:
  issue_comment:
    types: [created]

jobs:
  respond:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
      
      - name: Claude Review
        uses: anthropic-ai/claude-code-action@v1
        with:
          prompt: ${{ github.event.comment.body }}
          context: "PR #${{ github.event.issue.number }}"
        env:
          CLAUDE_CODE_USE_FOUNDRY: "1"
          ANTHROPIC_FOUNDRY_RESOURCE: ${{ secrets.AZURE_FOUNDRY_RESOURCE }}
          ANTHROPIC_FOUNDRY_API_KEY: ${{ secrets.AZURE_FOUNDRY_API_KEY }}
```

::: moniker range="foundry"

## Monitor usage

Monitor Claude Code usage in the Foundry portal:

1. Go to [Microsoft Foundry](https://ai.azure.com/) and open your project.

1. Navigate to **Operate** to view usage metrics:
   - Token consumption by model
   - Request latency
   - Error rates and rate limit hits

To set token limits per request, configure the `ANTHROPIC_MAX_TOKENS` environment variable:

# [Bash / WSL](#tab/bash)

```bash
export ANTHROPIC_MAX_TOKENS=100000
```

# [PowerShell](#tab/powershell)

```powershell
$env:ANTHROPIC_MAX_TOKENS = "100000"
```

---

::: moniker-end

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| Authorization failed (HTTP 401/403) | Verify that `az login` completed successfully or that the API key is set correctly. Check that your account has access to the Foundry resource. |
| Model not found | Verify that the deployment name in your environment variables matches the deployment name in the Foundry portal. |
| Rate limit exceeded (HTTP 429) | Adjust `ANTHROPIC_MAX_TOKENS` or check your quotas in the Foundry portal under **Operate** > **Quotas**. |
| VS Code extension not connecting | Ensure environment variables are set before launching VS Code. Try launching VS Code from the terminal after setting variables. |
| WSL + VS Code extension issues | The extension might check for the API key on the Windows host instead of within WSL. Set the environment variable on both the Windows host and WSL, then launch a new terminal from WSL and run `code .` |
| Region errors | Claude models are only available in East US2 and Sweden Central. |

## Related content

- [Deploy and use Claude models in Microsoft Foundry](use-foundry-models-claude.md)
- [Codex with Azure OpenAI in Microsoft Foundry Models](../../openai/how-to/codex.md)
- [Model Router overview](../../openai/concepts/model-router.md)
- [Data, privacy, and security for Claude models](../../responsible-ai/claude-models/data-privacy.md)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Spec Kit on GitHub](https://github.com/github/spec-kit)
