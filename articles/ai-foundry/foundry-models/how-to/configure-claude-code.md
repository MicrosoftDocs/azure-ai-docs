---
title: Claude Code with Microsoft Foundry
titleSuffix: Microsoft Foundry
description: Set up Claude Code CLI and VS Code extension to use Claude models in Microsoft Foundry with enterprise security, authentication, and CI/CD integration.
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: how-to
ms.date: 02/24/2026
ms.custom: dev-focus
author: msakande
ms.author: mopeakande
ms.reviewer: ambadal
reviewer: AmarBadal
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
#CustomerIntent: As a developer, I want to configure Claude Code, Anthropic's agentic coding tool, to use Microsoft Foundry so I can use enterprise-managed Claude models for AI-assisted coding with proper security and compliance.
---

# Claude Code with Microsoft Foundry

Anthropic's [Claude Code](https://docs.anthropic.com/en/docs/claude-code) is an AI coding agent available as a CLI tool and VS Code extension. When you configure Claude Code with Microsoft Foundry, you run the coding agent on Azure infrastructure while keeping your data inside your compliance boundary. This configuration provides enterprise-grade security, private networking, role-based access control, and cost management. Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. It works in your terminal, IDE, browser, and as a desktop app.

In this article, you learn how to:

- Install and configure Claude Code CLI for Microsoft Foundry
- Set up the Claude Code VS Code extension
- Authenticate with Microsoft Entra ID or API keys
- Create project context files for better AI assistance
- Run Claude Code in GitHub Actions for CI/CD automation

[!INCLUDE [claude-usage-restriction](../includes/claude-usage-restriction.md)]

## Prerequisites

- An Azure subscription with a valid payment method. If you don't have an Azure subscription, create a [paid Azure account](https://azure.microsoft.com/pricing/purchase-options/pay-as-you-go).
- Access to [Microsoft Foundry](https://ai.azure.com/) with Contributor permissions to create and manage resources.
- A [Microsoft Foundry project](../../how-to/create-projects.md) created in one of the [supported regions](../../how-to/deploy-models-serverless-availability.md#region-availability) for Claude models. Claude models are currently available in **East US 2** and **Sweden Central** only.
- **Contributor** or **Owner** role on your Foundry resource group. For more information, see [Azure RBAC roles](/azure/role-based-access-control/built-in-roles).
- Access to [Azure Marketplace](../../foundry-models/how-to/configure-marketplace.md) to deploy Foundry Models from partners.
- For Windows, use Git Bash (included with [Git for Windows](https://gitforwindows.org/)) or install WSL2 (recommended for full Linux compatibility). See [Install WSL](/windows/wsl/install).
- (Optional) [Azure CLI](/cli/azure/install-azure-cli) installed with `az login` completed for Microsoft Entra ID authentication.

### System requirements

| Requirement | Details |
| ----------- | ------- |
| Operating system | macOS 13+, Ubuntu 20.04+/Debian 10+, Windows 10+ (native via Git Bash, or WSL) |
| RAM | 4-GB minimum (8-GB recommended) |
| Git (optional, recommended) | 2.23+ for pull request helpers |

## Deploy a Claude model in Foundry

Before configuring Claude Code, deploy the available [Claude models](../concepts/models-from-partners.md#anthropic) that Claude Code needs. Claude models in Foundry are available for [global standard deployment](../concepts/deployment-types.md#global-standard). Claude Code uses different models for different tasks:

> [!IMPORTANT]
> Claude models in Microsoft Foundry are currently in preview. Model availability might change. Check the [Foundry Models from partners](../concepts/models-from-partners.md#anthropic) page for the latest list of available models.

| Claude Code role | Recommended deployment | Purpose |
|---|---|---|
| Primary model | `claude-sonnet-4-6` | General coding — balanced speed and quality |
| Fast model | `claude-haiku-4-5` | Quick operations — file reads, small edits |
| Extended thinking | `claude-opus-4-6` | Complex reasoning tasks (optional) |

Other Claude models available in Foundry include `claude-sonnet-4-5`, `claude-opus-4-5` and `claude-opus-4-1`.

To deploy a model:

1. To deploy a Claude model, such as Opus 4.6, follow the instructions in [Deploy Microsoft Foundry Models in the Foundry portal](deploy-foundry-models.md).

1. After deployment, select the deployment's **Details** tab and note your **Target URI** and **Key**. You need these values for configuration.

### Alternative: Use Model Router

[Model Router](../../openai/concepts/model-router.md) is a Foundry model that intelligently routes each prompt to the best underlying model based on query complexity, cost, and performance. Model Router version `2025-11-18` supports select Claude models (`claude-haiku-4-5`, `claude-opus-4-1`, and `claude-sonnet-4-5`), alongside other Foundry models.

> [!NOTE]
> Model Router doesn't currently support `claude-sonnet-4-6` or `claude-opus-4-6`. If you need these models, deploy and reference them directly instead of using Model Router.

Benefits for Claude Code users:

- **Automatic model selection**: Simple prompts route to faster, cheaper models. Complex coding tasks route to more capable models.
- **Cost optimization**: Use routing profiles to balance quality versus cost while maintaining baseline performance.
- **Single endpoint**: One deployment handles all routing decisions across your model fleet.

To use Model Router with Claude Code, first deploy the supported Claude models, then deploy Model Router and enable them through [model subset configuration](../../openai/how-to/model-router.md#select-your-model-subset).

## Install Claude Code CLI

Install the Claude Code CLI to work with Claude Code directly in your terminal. Then, verify that `claude` is in your PATH by running `claude --version`.

> [!NOTE]
> Anthropic has deprecated the npm installation method. Use the native installer or Homebrew instead. If you already installed via npm, run `claude install` to migrate to the native method.


### Native install (recommended)

Native installations automatically update in the background to keep you on the latest version.

# [Bash / WSL](#tab/bash)

On macOS or Windows (Git Bash or WSL), run the installer script, which downloads and configures the `claude` binary:

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version # verify installation
```

# [PowerShell](#tab/powershell)

```powershell
irm https://claude.ai/install.ps1 | iex
claude --version # verify installation
```

---

### Installation with Homebrew

If using macOS:

```bash
brew install --cask claude-code
claude --version # verify installation
```
Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.


### Troubleshoot install location

If the `claude --version` command isn't found, add the install location to your PATH as follows:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

For more installation options, see [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code).

## Configure Claude Code for Foundry

You use either your Foundry resource name or the base URL to configure Claude Code for Foundry. 

To find your Foundry resource name from the Foundry portal,

1. Go to the top left navigation and select the project name > **Project details**.
1. Copy the value of "Parent resource" from the Project details page.

To find your base URL from the Foundry portal,

1. From the home page of the Foundry portal, find the **Project endpoint** and copy the part of the URL that comes before `/api/projects/<your-project-name>`. Your base URL is of the form: `https://<your-resource-name>.services.ai.azure.com`, and Claude Code appends `/anthropic` to this URL automatically when you use `ANTHROPIC_FOUNDRY_RESOURCE`.


Set environment variables to connect Claude Code to your Microsoft Foundry deployment: 

# [Bash / WSL](#tab/bash)

```bash
# Required: Enable Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace <your-resource-name> with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE=<your-resource-name>
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://<your-resource-name>.services.ai.azure.com

# Optional: Specify model deployment names if different from defaults
export ANTHROPIC_DEFAULT_SONNET_MODEL="claude-sonnet-4-6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="claude-haiku-4-5"
export ANTHROPIC_DEFAULT_OPUS_MODEL="claude-opus-4-6"
```

# [PowerShell](#tab/powershell)

```powershell
# Required: Enable Foundry integration
$env:CLAUDE_CODE_USE_FOUNDRY = "1"

# Azure resource name (replace <your-resource-name> with your resource name)
$env:ANTHROPIC_FOUNDRY_RESOURCE = "<your-resource-name>"
# Or provide the full base URL:
# $env:ANTHROPIC_FOUNDRY_BASE_URL = "https://<your-resource-name>.services.ai.azure.com"

# Optional: Specify model deployment names if different from defaults
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "claude-sonnet-4-6"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "claude-haiku-4-5"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "claude-opus-4-6"
```

---

The following table describes each variable:

| Variable | Description |
|---|---|
| `CLAUDE_CODE_USE_FOUNDRY` | Set to `1` to enable the Microsoft Foundry integration. |
| `ANTHROPIC_FOUNDRY_RESOURCE` | Your Foundry resource name. Claude Code constructs the endpoint URL as `https://<resource-name>.services.ai.azure.com/anthropic`. |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | The deployment name for the Claude Sonnet model (primary coding model). |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | The deployment name for the Claude Haiku model (fast operations). |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | The deployment name for the Claude Opus model (complex reasoning). |

> [!TIP]
> If you use a custom endpoint URL, set `ANTHROPIC_FOUNDRY_BASE_URL` instead of `ANTHROPIC_FOUNDRY_RESOURCE`. Include the full URL with the `/anthropic` suffix:
>
> ```bash
> export ANTHROPIC_FOUNDRY_BASE_URL=https://<your-resource-name>.services.ai.azure.com/anthropic
> ```

To persist these variables across terminal sessions, add them to your shell profile (such as `~/.bashrc` or `~/.zshrc`).


## Authenticate with Foundry

Claude Code supports two authentication methods for Microsoft Foundry. Choose the method that best fits your security requirements.

### Option A: Microsoft Entra ID (recommended)

Microsoft Entra ID authentication uses your Azure CLI credentials automatically. Run `az login` before starting Claude Code:

1. Sign in with the Azure CLI:

    ```bash
    az login
    ```

    > [!TIP]
    > If your Foundry resource is in a different tenant than your default Azure CLI tenant, specify the tenant ID:
    > ```bash
    > az login --tenant <tenant-id>
    > ```
    
1. Verify your sign-in targets the correct subscription:

    ```bash
    az account show
    ```

When you use Microsoft Foundry, the `/login` and `/logout` commands inside Claude Code are disabled. Authentication is handled through your Azure credentials.

Claude Code detects your Azure CLI session and uses it for authentication without extra configuration.

### Option B: API key

If you prefer API key authentication, set the key in your environment variables.

1. In the [Microsoft Foundry portal](https://ai.azure.com/nextgen), open your resource.
1. On the **Home** page, find the **Project API key** field.
1. Select **Copy Project API key** to copy the value. This is the key you use for the `ANTHROPIC_FOUNDRY_API_KEY` environment variable.
1. Set the environment variable in your terminal:

  # [Bash / WSL](#tab/bash)
  
  ```bash
  export ANTHROPIC_FOUNDRY_API_KEY="<your-foundry-api-key>"
  ```
  
  # [PowerShell](#tab/powershell)
  
  ```powershell
  $env:ANTHROPIC_FOUNDRY_API_KEY = "<your-foundry-api-key>"
  ```
  
  ---

> [!TIP]
> You can also find your API key in the Foundry portal under your model deployment's **Details** tab.
 

## Configure the VS Code extension

The Claude Code VS Code extension provides a native graphical interface for Claude Code directly in your IDE.

1. Install the extension from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code).

1. Open VS Code settings (**Ctrl+,** or **Cmd+,**) and search for **Claude Code: Environment Variables**.

1. Select **Edit in settings.json** and add the following configuration:

    ```json
    {
      "Claude Code: Environment Variables": {
        "CLAUDE_CODE_USE_FOUNDRY": "1",
        "ANTHROPIC_FOUNDRY_RESOURCE": "<your-resource-name>",
        "ANTHROPIC_FOUNDRY_API_KEY": "<optional-for-non-entra-auth>"
      }
    }
    ```

1. Select the **Spark icon** in the sidebar to open the Claude Code panel.

1. Claude Code authenticates using your Azure credentials. Run `az login` first if you're using Microsoft Entra ID authentication.

The extension supports auto-accept edits mode, plan mode, extended thinking, and file management with @-mentions—all while routing through your Microsoft Foundry deployment.

## Validate the configuration

Verify that Claude Code is correctly configured to use Microsoft Foundry. 

1. Open a terminal and navigate to a project directory:

    ```bash
    cd your-project
    ```

1. Launch Claude Code:

    ```bash
    claude
    ```

    Claude Code defaults to the Sonnet model for general coding. If you haven't deployed all three models yet, you can specify a deployed model directly:

    ```bash
    claude --model claude-opus-4-6
    ```

1. Run the `/status` command:

    ```bash
    > /status
    ```

    The output should look similar to the following example. The exact format might vary depending on your Claude Code version.
  
    ```text
    Claude Code v1.0.0
    ─────────────────────────────────────
    Version: 2.1.47
    Session name: /rename to add a name
    Session ID: your-session-ID
    cwd: C:\WINDOWS\system32
    API provider: Microsoft Foundry
    Microsoft Foundry Resource: <your-resource-name>
    Model: Default (claude-sonnet-4-6)
    Memory:
    Setting sources:
    ─────────────────────────────────────
    ```
    
    Confirm the following in the status output:
    
    | Field | Expected value |
    | ----- | -------------- |
    | API provider | Microsoft Foundry |
    | Foundry resource | Your Foundry resource name |
    | Model | Your deployed model (for example, `claude-sonnet-4-6`) |

1. Send a test prompt such as "Summarize this project's structure."

1. Confirm that Claude Code responds with an analysis of your project. A successful connection shows Claude Code's interactive prompt without authentication errors.

  If Claude Code displays an error like "Failed to get token" or "model is not available", see the [Troubleshooting](#troubleshooting) section. If Claude Code starts and responds to prompts, your Foundry connection is working correctly.

## Create project context with CLAUDE.md

You can give Claude Code extra instructions and guidance using `CLAUDE.md` files. Claude Code looks for `CLAUDE.md` files in the following places and merges them top-down (that is, the files load in order, with later files overriding earlier ones), giving it context about your personal preferences, project-specific details, and the current task:

1. `~/.claude/CLAUDE.md` – Global defaults across all projects
1. `./CLAUDE.md` – Repository root settings
1. `./current-dir/CLAUDE.md` – Current directory specifics

Claude Code also supports project rules (`.claude/rules/*.md`) and local memory (`CLAUDE.local.md`) for more granular control. For the full memory hierarchy, see [Claude Code memory documentation](https://docs.anthropic.com/en/docs/claude-code/memory).

For example, create a `CLAUDE.md` file in your project root to help Claude Code understand your codebase. Here's an example for a [Microsoft Agent Framework](https://aka.ms/agent-framework) project:

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

## Experiment with Claude Code

To get Claude Code to read your `CLAUDE.md` and understand your project context, run these commands in your terminal:

```bash
# Start Claude Code in your project
cd your-project
claude

# Or run a one-off command
claude "explain the agent orchestration in src/workflows/"
```

## Configure Azure RBAC

To grant team members access to your Foundry-hosted Claude models, assign one of the following built-in roles:

| Role | Permissions |
|---|---|
| **Azure AI User** | Invoke models, view deployments |
| **Cognitive Services User** | Invoke models, view deployments (legacy Azure AI Services role) |

The **Azure AI User** role is the recommended Foundry-native role. The **Cognitive Services User** role is a legacy role that also grants model invocation permissions at the Azure resource level.

These roles include all required permissions for running Claude Code with Foundry.

For more restrictive access, create a custom role scoped to the specific data actions your team needs. For guidance on defining custom roles, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

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
        uses: anthropics/claude-code-action@v1
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
        uses: anthropics/claude-code-action@v1
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

> [!NOTE]
> The `ANTHROPIC_MAX_TOKENS` variable might not be supported in all Claude Code versions. Check the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) for the latest supported environment variables.

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

## Clean up resources

If you no longer need the Claude model deployments, delete them to free up deployment slots and quota in your resource. Claude models use Global Standard deployments with pay-per-token billing, so idle deployments don't incur charges. However, each deployment counts against your [deployment limit](../../foundry-models/quotas-limits.md) of 32 per resource.

### Delete deployments in the Foundry portal

Use either of these navigation paths:

- Select **Operate** from the top navigation, then select **Assets** > **Models** from the left navigation. Select the deployment you want to delete, then select **Delete**.
- Select **Build** from the top navigation, then select **Models** from the left navigation. Select the deployment name to open its detail page, select the **Details** tab, then select **Delete** from the top panel.

### Delete deployments with the Azure CLI

Run the [az cognitiveservices account deployment delete](/cli/azure/cognitiveservices/account/deployment#az-cognitiveservices-account-deployment-delete) command for each deployment:

```azurecli
az cognitiveservices account deployment delete \
  --deployment-name <deployment-name> \
  --name <resource-name> \
  --resource-group <resource-group-name>
```

Replace `<deployment-name>` with the model deployment name (such as `claude-sonnet-4-6`), `<resource-name>` with your Foundry resource name, and `<resource-group-name>` with the resource group that contains your Foundry resource.

## Troubleshooting

| Problem | Solution |
| ----- | -------- |
| Authorization failed (HTTP 401/403) | Verify that `az login` completed successfully or that the API key is set correctly. Check that your account has access to the Foundry resource. |
| Claude Code starts but can't find models | Verify `ANTHROPIC_FOUNDRY_RESOURCE` matches your resource name and that the `ANTHROPIC_DEFAULT_*_MODEL` values match your deployment names. |
| Rate limit exceeded (HTTP 429) | Adjust `ANTHROPIC_MAX_TOKENS` or check your quotas in the Foundry portal under **Operate** > **Quotas**. |
| VS Code extension not connecting | Ensure environment variables are set before launching VS Code. Try launching VS Code from the terminal after setting variables. |
| WSL + VS Code extension issues | The extension might check for the API key on the Windows host instead of within WSL. Set the environment variable on both the Windows host and WSL, then launch a new terminal from WSL and run `code .` |
| Region errors | Claude models are only available in East US2 and Sweden Central. |
| "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed" | Sign in with `az login`, or set `ANTHROPIC_FOUNDRY_API_KEY` for API key authentication. |
| "The model `<model-name>` is not available on your foundry deployment" | Deploy the missing model in the Foundry portal. Claude Code requires each model role (Sonnet, Haiku, Opus) to have a corresponding deployment. |
| "Token tenant does not match resource tenant" | Your Azure CLI is signed in to a different tenant than your Foundry resource. Run `az login --tenant <tenant-id>` to sign in to the correct tenant. |
| Deployment creation fails in the Foundry portal | Verify you have **Contributor** or **Owner** role on the resource group, and your subscription has [Azure Marketplace access](../../foundry-models/how-to/configure-marketplace.md) enabled. |
| Claude Code prompts for Anthropic login | Verify `CLAUDE_CODE_USE_FOUNDRY=1` is set. Without this variable, Claude Code uses the default Anthropic API. |


## Related content

- [Deploy and use Claude models in Microsoft Foundry](use-foundry-models-claude.md)
- [Data, privacy, and security for Claude models](../../responsible-ai/claude-models/data-privacy.md)
- [Microsoft Foundry Models quotas and limits](../../foundry-models/quotas-limits.md)
- [Monitor model usage and costs](../../how-to/costs-plan-manage.md)
- [Microsoft Dev Blogs | Claude Code + Microsoft Foundry: Enterprise AI Coding Agent Setup](https://devblogs.microsoft.com/all-things-azure/claude-code-microsoft-foundry-enterprise-ai-coding-agent-setup/)
- [Claude in Microsoft Foundry (Anthropic docs)](https://docs.claude.com/en/docs/build-with-claude/claude-in-microsoft-foundry)
- [Claude Code Documentation (Anthropic docs)](https://docs.anthropic.com/en/docs/claude-code)
