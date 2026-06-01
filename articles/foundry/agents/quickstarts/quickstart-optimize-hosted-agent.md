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

Your Azure subscription must be on the allow list for the agent optimizer. Contact your Microsoft representative to request access.

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
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support/agent.manifest.yaml .
```

The interactive flow prompts for your Azure subscription, region, and model deployment settings. It downloads the sample and generates `agent.yaml`, `.agent_configs/baseline/`, the evaluation dataset, and infrastructure-as-code files for provisioning.

> [!TIP]
> If you already have an existing agent project, skip this step and see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md) to add optimization support.
>
> If you already have a Foundry project and model deployments, add `-p <project-resource-id>` to target existing resources:
> ```bash
> azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support/agent.manifest.yaml -p "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
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

Provision the Azure resources. This step takes approximately two minutes:

```bash
azd provision
```

This step creates:

- A Foundry account and project
- An Azure Container Registry
- Model deployments (gpt-4.1-mini for eval, gpt-5.4 for optimization)

### Option B: Use an existing Foundry project

If you already have a Foundry project with models deployed, use `agent init` to configure your environment:

```bash
azd ai agent init --project-id "/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
```

> [!TIP]
> Find your project resource ID in the Azure portal → your Foundry project → **Properties** → **Resource ID**.

Set your model deployment name:

```bash
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "gpt-4.1-mini"
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

## Generate custom dataset and evalutations

For meaningful optimization with your own scenarios, generate a dataset with `eval init`:

```bash
azd ai agent eval init --gen-instruction "You are a helpful customer support agent."
```

The command creates an `eval.yaml` with a dataset and evaluators tuned to your agent's domain.

For details, see [Create an evaluation dataset](../how-to/create-optimizer-dataset.md).

## Run optimization

Then run optimization with the generated configuration:

```bash
azd ai agent optimize
```

The CLI reads the `name` field from your `agent.yaml` file to determine which deployed agent to optimize. It'll also automatically detect and use the generated `eval.yaml` file to run optimization. If you have multiple agents or configurations or want to target a different one, use the `--agent` and `--config` flags:

```bash
azd ai agent optimize --agent <your-agent-name> --config <your-config-file>.yaml
```

For more details on agent targeting, see [Which agent gets optimized](../how-to/optimize-agent-targets.md#which-agent-gets-optimized).

The agent optimizer completes the following steps:

1. Evaluates your baseline agent against a built-in dataset that contains 3 tasks and 12 criteria.
1. Generates improved candidates (instructions, skills, tools, or model configurations depending on your target).
1. Evaluates each candidate.
1. Ranks the candidates by score.

This process takes a few minutes. You see real-time progress:

```output
Optimizing agent "customer-support-py"...
  Config: C:\Dev\my-agent\eval.yaml
  Baseline saved to .agent_configs\baseline\metadata.yaml
  Job ID: opt_162bd0f09070432c9ca4a699a908abb0
  Status: pending
  Portal: <OPTIMIZATION-JOB-URL>
```

Use the URL provided in the CLI to view and monitor your job in the Foundry portal. 

The *eval model* scores each response (any chat-completion model works). The *optimization model* generates improved candidates and must be from the [supported list](../concepts/agent-optimizer-overview.md#models) (gpt-5 family or DeepSeek).

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
azd ai agent invoke "What is your return policy?"
```

You can also run evaluation separately to confirm the score improvement:

```bash
azd ai agent eval run
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
| All scores are zero | Agent or eval model not deployed | Deploy the agent or eval model in your Foundry project, or use `--eval-model` to specify a deployed model |
| `azd provision` fails with quota error | Subscription lacks capacity | Try a different subscription or request a quota increase |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Create an evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)

