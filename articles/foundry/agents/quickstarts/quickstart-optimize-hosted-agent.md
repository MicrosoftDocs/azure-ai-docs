---
title: "Quickstart: Optimize a hosted agent (preview)"
description: "Deploy the optimization sample agent, run the agent optimizer to automatically improve its instructions, and deploy the winning candidate."
author: aahill
ms.author: aahi
ms.date: 06/22/2026
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Quickstart: Optimize a hosted agent (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

In this quickstart, you deploy the optimization sample agent, run the agent optimizer to improve its instructions, and deploy the winning candidate.

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* [azd CLI](https://aka.ms/azd) (Azure Developer CLI).
* [Azure CLI](/cli/azure/install-azure-cli) for authentication.
* The `microsoft.foundry` extension for azd (0.1.40-preview or later of the `azure.ai.agents` dependency):

    ```bash
    azd ext install microsoft.foundry
    ```

    If already installed, upgrade:

    ```bash
    azd ext upgrade microsoft.foundry
    ```

* Your Azure subscription must be on the allow list for the agent optimizer. Contact your Microsoft representative to request access.

> [!NOTE]
> Hosted agents and the agent optimizer are currently in preview.

## Step 1: Create the project

Initialize a new project from the optimization sample template:

```bash
mkdir my-agent && cd my-agent
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support/agent.manifest.yaml .
```

The interactive flow prompts for your Azure subscription, region, and model deployment settings. It generates `agent.yaml`, `.agent_configs/baseline/`, the evaluation dataset, and infrastructure files.

> [!TIP]
> If you already have an existing agent project, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md) to add optimization support.
>
> If you already have a Foundry project, add `-p <project-resource-id>` to target existing resources.

## Step 2: Provision and deploy

Authenticate and provision the Azure resources:

```bash
az login
azd auth login
azd provision
```

Provisioning takes approximately two minutes and creates a Foundry account, project, Azure Container Registry, and model deployments.

Deploy the agent:

```bash
azd deploy
```

Test the deployment:

```bash
azd ai agent invoke "What is 2+2?"
```

## Step 3: Generate evaluation suite and optimize

Generate an evaluation dataset and evaluators for your agent:

```bash
azd ai agent eval generate
```

This step creates `eval.yaml`, a test dataset, and scoring evaluators based on your agent's instructions. The optimizer uses these files to measure improvement.

Run the optimizer:

```bash
azd ai agent optimize --max-candidates 2
```

The CLI prompts you to select an optimization model. To skip the prompt, pass it directly:

```bash
azd ai agent optimize --max-candidates 2 --optimize-model gpt-5
```

The CLI detects your agent from `agent.yaml` and uses the generated `eval.yaml` automatically. With two candidates, optimization typically completes in about 8 minutes. Real-time progress is shown:

```output
Optimizing agent "customer-support-py"...
  Config: eval.yaml
  Baseline saved to .agent_configs/baseline/metadata.yaml
  Job ID: opt_162bd0f09....
  Status: pending
  Portal: <OPTIMIZATION-JOB-URL>
```

Use the portal URL to monitor your job in the Foundry portal.

The *eval model* scores each response (any chat-completion model works). The *optimization model* (`--optimize-model`) generates improved candidates and must be from the [supported list](../concepts/agent-optimizer-overview.md#models) (gpt-5 family or DeepSeek). You can also set `optimization_model` under `options:` in `eval.yaml` to avoid passing the flag each time.

## Step 4: Deploy the winner

The ★ in the output indicates the best candidate. Apply the optimized config locally, then deploy:

```bash
azd ai agent optimize apply --candidate <candidate-id>
azd deploy
```

The `apply` command downloads the optimized configuration into `.agent_configs/<candidate_id>/` and updates your `agent.yaml` to use the new instructions. The `deploy` command pushes the optimized agent live using code deploy.

Invoke your agent to verify the improvement:

```bash
azd ai agent invoke "What is your return policy?"
```

You can also run evaluation to confirm the score improvement:

```bash
azd ai agent eval run
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
| `azd ai agent optimize` command not found | Extension too old | Run `azd ext upgrade microsoft.foundry` to get 0.1.40-preview or later. |
| `optimization_model is required` | Running in non-interactive mode without a model configured | Add `--optimize-model gpt-5` to the command, or set `optimization_model: gpt-5` under `options:` in `eval.yaml`. In interactive mode, the CLI prompts for model selection. |
| Optimization score is 0 or very low | Evaluation has many errored rows | Open the **Eval** link in the results. Fix response generation or evaluator errors, then rerun. |
| `azd provision` fails with quota error | Subscription lacks capacity | Try a different region or request a quota increase. |

## What you learned

In this quickstart, you:

* Deployed the optimization sample agent by using the customer-support template.
* Ran the agent optimizer to automatically improve agent instructions.
* Deployed the winning candidate and verified the improvement.

## Next steps

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Create a custom evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
