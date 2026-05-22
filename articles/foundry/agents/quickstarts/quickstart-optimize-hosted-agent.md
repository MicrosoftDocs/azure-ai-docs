---
title: "Quickstart: Optimize a hosted agent in Foundry Agent Service (preview)"
description: "Set up the optimization CLI extension, deploy a hosted agent, and run your first optimization using the agent optimizer to improve agent instructions automatically."
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

In this quickstart, you install the optimization CLI extension, deploy a hosted agent, run the agent optimizer, and deploy the winning candidate.

## Prerequisites

| Tool | Required | Purpose |
| ------ | ---------- | --------- |
| [azd CLI](https://aka.ms/azd) | Yes | Azure Developer CLI. Provisions, deploys, and manages your agent. |
| [Azure CLI](/cli/azure/install-azure-cli) | Yes | Azure authentication (`az login`) |
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) (must be running) | Yes | Builds and pushes container images for agent deployment |
| [Python 3.12+](https://www.python.org/downloads/) | Yes | Agent runtime |
| Git | Yes | Source control |

Your Azure subscription must be on the allowlist for the agent optimizer. Contact your Microsoft representative to request access.

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

Set your Azure subscription and location, then provision the required resources. Choose any [region where hosted agents are available](../concepts/hosted-agents.md#region-availability):

# [Bash](#tab/bash)

```bash
azd env set AZURE_SUBSCRIPTION_ID $(az account show --query id -o tsv)
azd env set AZURE_LOCATION <your-region>
```

# [PowerShell](#tab/powershell)

```powershell
azd env set AZURE_SUBSCRIPTION_ID (az account show --query id -o tsv)
azd env set AZURE_LOCATION <your-region>
```

---

Provision the Azure resources. This step takes approximately two minutes:

```bash
azd provision
```

This step creates:

- A Foundry account and project
- An Azure Container Registry
- A model deployment for gpt-4.1-mini

## Deploy the agent

```bash
azd deploy
```

This command builds the container image, pushes it to Azure Container Registry, and registers the hosted agent. The process takes approximately 1.5 minutes. The output includes a portal playground link you can use to chat with the agent.

Test the deployment:

```bash
azd ai agent invoke "What is 2+2?"
```

## Run optimization

```bash
azd ai agent optimize
```

The CLI auto-detects the agent name from `agent.yaml`. The agent optimizer completes the following steps:

1. Evaluates your baseline agent against a built-in dataset that contains 3 tasks and 12 criteria.
1. Generates improved instruction candidates.
1. Evaluates each candidate.
1. Ranks the candidates by score.

This process takes 5 to 20 minutes. You see real-time progress:

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

  Deploy the best candidate:
    azd ai agent optimize deploy --candidate cand_91a5861f5c0245c4b2acb9ccaa48d4aa
```

The *eval model*, which defaults to `gpt-4.1-mini`, scores each response. This model must be deployed in your Foundry project.

> [!WARNING]
> If the eval model is not deployed, all scores are zero with no error message. Verify that your eval model exists before running optimization.

To evaluate the baseline only, without running optimization:

```bash
azd ai agent optimize --eval
```

## Deploy the winner

The ★ indicates the best candidate. Deploy it with the command shown in the optimization output:

```bash
azd ai agent optimize deploy --candidate <candidate-id>
```

This command creates a new agent version with the optimized instructions. The `agent_optimization` SDK's `load_config()` function picks up the new configuration automatically at startup.

Invoke your agent again to verify the improvement:

```bash
azd ai agent invoke "Write a Python function to check if a number is prime."
```

You can also re-run eval-only to confirm the score improvement:

```bash
azd ai agent optimize --eval
```

## Monitor and manage

Use the *job ID*, which is formatted as `opt_<hex>` and is printed in optimization output, to track and manage runs:

```bash
# Watch a running job
azd ai agent optimize status <job-id> --watch

# List all optimization runs
azd ai agent optimize list

# Cancel a running job
azd ai agent optimize cancel <job-id>
```

## Clean up resources

When you finish experimenting, delete the provisioned resources:

```bash
azd down --force --purge
```

> [!TIP]
> **Why `--purge`?** Foundry accounts use soft-delete by default. Without `--purge`, the resource name stays reserved for 48 hours, and reprovisioning with the same name fails.

## Troubleshooting

| Problem | Cause | Fix |
| --------- | ------- | ----- |
| `optimize` returns 403 | Subscription not on allowlist | Contact your Microsoft representative to request access |
| All scores are zero | Eval model not deployed | Deploy `gpt-4.1-mini` in your Foundry project, or use `--eval-model` to specify a deployed model |
| `azd deploy` fails with Docker error | Docker Desktop not running | Start Docker Desktop and retry |
| `azd provision` fails with quota error | Subscription lacks capacity | Try a different subscription or request a quota increase |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Create a custom evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions and skills](../how-to/optimize-agent-strategies.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)

