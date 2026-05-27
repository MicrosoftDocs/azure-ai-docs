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

Your Azure subscription must be on the allowlist for the agent optimizer. Contact your Microsoft representative to request access.

## Install the CLI extension

Install the `azure.ai.agents` extension for the azd CLI:

```bash
azd ext install azure.ai.agents
```

Verify the installation:

```bash
azd ai agent optimize --help
```

## Create the project

Initialize a new project from the agent optimizer sample. Create a folder, then use `azd ai agent init` with the sample manifest:

```bash
mkdir my-agent && cd my-agent
azd ai agent init -m https://github.com/microsoft/faos-pri-preview/blob/main/samples/python/customer-support/agent.manifest.yaml
```

This downloads the sample and generates `agent.yaml`, `.agent_configs/baseline/`, the evaluation dataset, and infrastructure-as-code files for provisioning.

> [!TIP]
> If you already have an existing agent project, skip this step and see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md) to add optimization support.
>
> If you already have a Foundry project and model deployments, add `-p <project-resource-id>` to target existing resources:
> ```bash
> azd ai agent init -m <manifest-url> -p "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
> ```

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

Choose one of the following options based on whether you need to create new Azure resources or already have an existing Foundry project.

### Option A: Create new resources

Set your Azure subscription and location, then provision. Choose any [region where hosted agents are available](../concepts/hosted-agents.md#region-availability):

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
- Model deployments (gpt-5.1 for eval and optimization)

### Option B: Use an existing Foundry project

If you already have a Foundry project with models deployed, use `agent init` to configure your environment:

```bash
azd ai agent init --project-id "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
```

> [!TIP]
> Find your project resource ID in the Azure portal → your Foundry project → **Properties** → **Resource ID**.

Set your model deployment name:

```bash
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "gpt-5.1"
```

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

The CLI reads the `name` field from your `agent.yaml` file to determine which deployed agent to optimize. If you have multiple agents or want to target a different one, use the `--agent` flag:

```bash
azd ai agent optimize --agent <your-agent-name>
```

For more details on agent targeting, see [Which agent gets optimized](../how-to/optimize-agent-targets.md#which-agent-gets-optimized).

The agent optimizer completes the following steps:

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

The *eval model* scores each response. The *optimization model* generates improved candidates. Both must be gpt-5 family models deployed in your Foundry project.

> [!WARNING]
> If the eval model is not deployed, all scores are zero with no error message. Verify that your eval model exists before running optimization.

## Deploy the winner

The ★ indicates the best candidate. The recommended workflow is to apply the optimized config locally, then deploy:

```bash
# Apply the winning candidate locally
azd ai agent optimize apply --candidate <candidate-id>

# Deploy with the optimized config
azd deploy
```

This downloads the optimized configuration into `.agent_configs/<candidate_id>/` in your project. On next deploy, your agent uses the improved instructions and tool descriptions.

Alternatively, for quick testing you can deploy directly:

```bash
azd ai agent optimize deploy --candidate <candidate-id>
```

The `azure-ai-agentserver-optimization` package's `load_config()` function picks up the new configuration automatically at startup.

Invoke your agent again to verify the improvement:

```bash
azd ai agent invoke "Write a Python function to check if a number is prime."
```

You can also run evaluation separately to confirm the score improvement:

```bash
azd ai agent eval run
```

## Next steps: Use a custom dataset

This quickstart uses the built-in dataset (3 tasks, 12 criteria). For meaningful optimization with your own scenarios, generate a dataset with `eval init`:

```bash
azd ai agent eval init
```

The command creates an `eval.yaml` with a dataset and evaluators tuned to your agent's domain. Then run optimization with the generated config:

```bash
azd ai agent optimize --config eval.yaml
```

For details, see [Create an evaluation dataset](../how-to/create-optimizer-dataset.md).

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
| All scores are zero | Eval model not deployed | Deploy a gpt-5 family model in your Foundry project, or use `--eval-model` to specify a deployed model |
| `azd deploy` fails with Docker error | Docker Desktop not running | Start Docker Desktop and retry |
| `azd provision` fails with quota error | Subscription lacks capacity | Try a different subscription or request a quota increase |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Create an evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
- [Optimize agent instructions and skills](../how-to/optimize-agent-targets.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)

