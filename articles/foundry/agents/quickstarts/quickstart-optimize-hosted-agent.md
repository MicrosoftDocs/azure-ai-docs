---
title: "Quickstart: Optimize a hosted agent in Foundry Agent Service (preview)"
description: "Set up the optimization CLI extension, deploy a hosted agent, and run your first optimization to improve agent instructions automatically."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Quickstart: Optimize a hosted agent (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

In this quickstart, you install the optimization CLI extension, deploy a hosted agent, run optimization, and deploy the winning candidate — all in about 10 minutes.

## Prerequisites

| Tool | Required | Purpose |
| ------ | ---------- | --------- |
| [azd CLI](https://aka.ms/azd) | Yes | Azure Developer CLI — provisions, deploys, and manages your agent |
| [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) | Yes | Azure authentication (`az login`) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | Yes | Builds and pushes container images for agent deployment |
| [Python 3.12+](https://www.python.org/downloads/) | Yes | Agent runtime |
| Git | Yes | Source control |

Your Azure subscription must be on the allowlist for agent optimization. Contact your Microsoft representative to request access.

## Install the CLI extension

### Option A: Use the template (recommended)

The template includes prebuilt extension binaries for all platforms:

```bash
mkdir my-agent && cd my-agent
azd init -t microsoft/faos-pri-preview
```

Run the install scripts to set up the extension:

# [Bash](#tab/bash)

```bash
./scripts/install-extension.sh
```

# [PowerShell](#tab/powershell)

```powershell
.\scripts\install-extension.ps1
```

---

This copies the correct binary for your platform to `~/.azd/extensions/azure.ai.agents/`.

> [!TIP]
> **For Dev Containers**: Select the **Open in Dev Containers** badge in the repo README. The dev container auto-installs everything.

### Option B: Build from source

<details>
<summary>Expand for build-from-source instructions (requires Go 1.21+)</summary>

```bash
# Clone the extension source
git clone https://github.com/coreai-microsoft/azure-dev-optimize.git
cd azure-dev-optimize/cli/azd/extensions/azure.ai.agents

# Build the binary
azd x build
```

Then install the extension and overlay the binary you built:

# [Bash](#tab/bash)

```bash
azd ext install azure.ai.agents
cp bin/azure-ai-agents-$(uname -s | tr A-Z a-z)-* ~/.azd/extensions/azure.ai.agents/
```

# [PowerShell](#tab/powershell)

```powershell
azd ext install azure.ai.agents
Copy-Item bin\azure-ai-agents-windows-amd64.exe $env:USERPROFILE\.azd\extensions\azure.ai.agents\ -Force
```

---

</details>

Verify the installation:

```bash
azd ai agent optimize --help
```

## Authenticate

```bash
az login
azd auth login
```

If you have multiple subscriptions, select the one you want:

```bash
az account set --subscription "<subscription-name-or-id>"
```

## Configure and provision

> [!IMPORTANT]
> **Region matters.** The optimization service is currently only available in **North Central US**. Other regions deploy the agent fine, but `azd ai agent optimize` returns a 404.

# [Bash](#tab/bash)

```bash
azd env set AZURE_SUBSCRIPTION_ID $(az account show --query id -o tsv)
azd env set AZURE_LOCATION northcentralus
```

# [PowerShell](#tab/powershell)

```powershell
azd env set AZURE_SUBSCRIPTION_ID (az account show --query id -o tsv)
azd env set AZURE_LOCATION northcentralus
```

---

Provision the Azure resources (~2 min):

```bash
azd provision
```

This creates:

- A Foundry account and project
- An Azure Container Registry
- A model deployment (gpt-4.1-mini)

## Deploy the agent

```bash
azd deploy
```

This builds the container image, pushes it to Azure Container Registry, and registers the hosted agent (~1.5 min). The output includes a portal playground link you can use to chat with the agent.

Test the deployment:

```bash
azd ai agent invoke "What is 2+2?"
```

## Run optimization

```bash
azd ai agent optimize
```

The agent name is auto-detected from `agent.yaml`. The service:

1. Evaluates your baseline agent against a built-in dataset (3 tasks, 12 criteria)
1. Generates improved instruction candidates
1. Evaluates each candidate
1. Ranks them by score

This process takes ~5–20 minutes. You see real-time progress:

```output
Optimizing agent "faos-sample-agent"...
  Dataset: built-in (3 tasks, 12 criteria)
  Job ID: opt_5978943447f7413fa268e9398642529a
  ⠏ completed · strategy: instruction · iteration 1 · score: 0.95 · 5m45s

Results:
  Candidate              Score    Pass   Tokens
  ──────────────────── ─────── ─────── ────────
  baseline                0.83    100%      640
  baseline_instr_v4       0.87    100%      471
  baseline_instr_v1       0.86    100%      456
  baseline_instr_v3 ★     0.91    100%      438
```

The *eval model* (defaults to `gpt-4.1-mini`) scores each response. This model must be deployed in your Foundry project.

> [!WARNING]
> If the eval model isn't deployed, all scores are zero with no error message. Verify your eval model exists before running optimization.

To evaluate the baseline only (no optimization):

```bash
azd ai agent optimize --eval
```

## Deploy the winner

The ★ marks the best candidate. Copy the deploy command from the output:

```bash
azd ai agent optimize deploy --candidate <candidate-id>
```

This creates a new agent version with the optimized instructions baked in. The `agent_optimization` SDK's `load_config()` function picks up the new config automatically at startup.

Invoke your agent again to verify the improvement:

```bash
azd ai agent invoke "Write a Python function to check if a number is prime."
```

You can also re-run eval-only to confirm the score improvement:

```bash
azd ai agent optimize --eval
```

## Monitor and manage

Use the *job ID* (format: `opt_<hex>`, printed in optimization output) to track and manage runs:

```bash
# Watch a running job
azd ai agent optimize status <job-id> --watch

# List all optimization runs
azd ai agent optimize list

# Cancel a running job
azd ai agent optimize cancel <job-id>
```

## Clean up resources

When you're done experimenting:

```bash
azd down --force --purge
```

> [!TIP]
> **Why `--purge`?** Foundry accounts use soft-delete by default. Without `--purge`, the resource name stays reserved for 48 hours and re-provisioning with the same name fails.

## Related content

- [Agent optimization overview](../concepts/agent-optimization-overview.md)
- [Create a custom evaluation dataset](../how-to/create-optimization-dataset.md)
- [Optimize agent instructions and skills](../how-to/optimize-agent-strategies.md)
- [Make your agent optimization-ready](../how-to/make-agent-optimization-ready.md)
