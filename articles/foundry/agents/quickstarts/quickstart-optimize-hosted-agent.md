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
zone_pivot_groups: hosted-agent-optimize-quickstart-method
---

# Quickstart: Optimize a hosted agent (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

In this quickstart, you deploy the optimization sample agent, run the agent optimizer to improve its instructions, and deploy the winning candidate.

## Prerequisites

Before you begin, you need:

* An Azure subscription--[Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

:::zone pivot="azd"

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

:::zone-end

:::zone pivot="python"

* [Azure CLI](/cli/azure/install-azure-cli) for authentication.
* Python 3.10 or later.
* The Python packages used in this path:

  ```bash
  pip install "azure-ai-projects>=2.3.0" azure-identity python-dotenv
  ```

* An existing Foundry project that already contains the hosted agent,
  registered dataset, and evaluator you want to use for optimization.

:::zone-end

* Your Azure subscription must be on the allow list for the agent optimizer. Contact your Microsoft representative to request access.

> [!NOTE]
> The agent optimizer is currently in preview.

:::zone pivot="azd"

## Step 1: Create the project

Initialize a new project from the optimization sample template:

```bash
mkdir my-agent && cd my-agent
azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support/azure.yaml .
```

The interactive flow prompts for your Azure subscription, region, and model deployment settings. It adopts `azure.yaml` for hosted-agent configuration and generates `.agent_configs/baseline/`, the evaluation dataset, and infrastructure files.

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

The CLI detects your agent from `azure.yaml` and uses the generated `eval.yaml` automatically. With two candidates, optimization typically completes in about 8 minutes. Real-time progress is shown:

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

The star (*) in the output indicates the best candidate. Apply the optimized config locally, then deploy:

```bash
azd ai agent optimize apply --candidate <candidate-id>
azd deploy
```

The `apply` command downloads the optimized configuration into `.agent_configs/<candidate_id>/` and updates your `azure.yaml` to use the new instructions. The `deploy` command pushes the optimized agent live using code deploy.

Invoke your agent to verify the improvement:

```bash
azd ai agent invoke "What is your return policy?"
```

You can also run evaluation to confirm the score improvement:

```bash
azd ai agent eval run
```

:::zone-end

:::zone pivot="python"

## Python SDK path

Use the following steps if you want to run the optimizer from Python instead of
the Azure Developer CLI workflow described earlier.

This path assumes you already have the following resources in an existing
Foundry project:

* A hosted agent to optimize.
* A registered training dataset.
* A registered evaluator.

Unlike the Azure Developer CLI flow described earlier, the Python SDK path doesn't scaffold
a project or generate `eval.yaml`, a dataset, or evaluators for you. If you
want the sample to create those assets automatically, use
`azd ai agent eval generate` first.

### 1. Create a `.env` file

Create a working folder, and then add a `.env` file with these values:

```text
FOUNDRY_PROJECT_ENDPOINT=<your-project-endpoint>
FOUNDRY_AGENT_NAME=<your-hosted-agent-name>
DATASET_NAME=<your-registered-dataset-name>
EVALUATOR_NAME=<your-registered-evaluator-name>
DATASET_VERSION=1
POLL_INTERVAL_SECONDS=10
EVAL_MODEL=<your-eval-model-deployment-name>
OPTIMIZATION_MODEL=<your-optimization-model-deployment-name>
```

Run the script from this same working folder so `load_dotenv()` can load the
`.env` file automatically. If you prefer to run it from another directory, set
the same values in your shell environment first.

Use the exact project endpoint from your Foundry project's **Overview** page.
The Python script sends its first request immediately. If
`FOUNDRY_PROJECT_ENDPOINT` is only a placeholder or points to the wrong
project, the run fails with `ResourceNotFound: The project does not exist`.

Set `EVAL_MODEL` and `OPTIMIZATION_MODEL` to deployment names that already
exist in your Foundry project, not just model family names. For example, if
your project deployment is named `gpt-4.1-mini` or `DeepSeek-V3.2`, use that
exact deployment name in `.env`.

### 2. Run the optimization job

Create a file named `optimize_hosted_agent.py` in the same folder as `.env`:

```python
import os
import time

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
  JobStatus,
  OptimizationAgentIdentifier,
  OptimizationEvaluatorRef,
  OptimizationJob,
  OptimizationJobInputs,
  OptimizationOptions,
  OptimizationReferenceDatasetInput,
)
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_AGENT_NAME"]
dataset_name = os.environ["DATASET_NAME"]
evaluator_name = os.environ["EVALUATOR_NAME"]
dataset_version = os.environ.get("DATASET_VERSION", "1")
poll_interval = int(os.environ.get("POLL_INTERVAL_SECONDS", "10"))
eval_model = os.environ.get("EVAL_MODEL", "gpt-4o")
optimization_model = os.environ.get("OPTIMIZATION_MODEL", "gpt-5")

terminal_statuses = {JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED}

with (
  DefaultAzureCredential() as credential,
  AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
):
  job = project_client.beta.agents.create_optimization_job(
    job=OptimizationJob(
      inputs=OptimizationJobInputs(
        agent=OptimizationAgentIdentifier(agent_name=agent_name),
        train_dataset=OptimizationReferenceDatasetInput(
          name=dataset_name,
          version=dataset_version,
        ),
        evaluators=[OptimizationEvaluatorRef(name=evaluator_name)],
        options=OptimizationOptions(
          max_candidates=2,
          eval_model=eval_model,
          optimization_model=optimization_model,
        ),
      )
    )
  )

  print(f"Created optimization job: {job.id}")
  print(f"Initial status: {job.status}")

  while job.status not in terminal_statuses:
    time.sleep(poll_interval)
    job = project_client.beta.agents.get_optimization_job(job_id=job.id)
    print(f"Status: {job.status}")

  if job.status == JobStatus.FAILED:
    message = job.error.message if job.error else "<no error message>"
    raise RuntimeError(f"Optimization job failed: {message}")

  if job.result:
    print(f"Baseline candidate: {job.result.baseline}")
    print(f"Best candidate: {job.result.best}")

    for candidate in job.result.candidates or []:
      print(
        f"{candidate.name}: candidate_id={candidate.candidate_id}, "
        f"avg_score={candidate.avg_score:.4f}, "
        f"avg_tokens={candidate.avg_tokens:.0f}"
      )
```

Run the script:

```bash
python optimize_hosted_agent.py
```

When the job succeeds, the script prints the winning candidate and its
`candidate_id`.

Unlike `azd ai agent optimize`, the Python SDK flow doesn't create a local
`.agent_configs/baseline/metadata.yaml` file. The optimization job metadata
stays in the returned `job` object and in the Foundry service response,
including the baseline candidate, best candidate, and scored candidate list.

### 3. Apply the winning candidate

If you're also working from the local `azd` project used in the CLI flow above,
apply the winning candidate by using the `candidate_id` returned by the Python
script:

```bash
azd ai agent optimize apply --candidate <candidate-id>
azd deploy
```

If you only need to inspect the result, use the candidate scores and evaluation
identifiers printed by the script to review the winning configuration in
Foundry before promoting it.

:::zone-end

## Clean up resources

If you used the preceding Azure Developer CLI workflow, delete the provisioned resources when you finish experimenting:

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
| Python script fails with `KeyError: 'DATASET_NAME'` or another missing variable | The script didn't load your `.env` file, or the variable is missing | Run the script from the same folder as `.env`, or export the required values in your shell before running `python optimize_hosted_agent.py`. |
| Python script fails with `ResourceNotFound: The project does not exist` | `FOUNDRY_PROJECT_ENDPOINT` doesn't point to an existing Foundry project | Copy the project endpoint from the Foundry project's **Overview** page and update `FOUNDRY_PROJECT_ENDPOINT` in `.env`. |
| Python script fails with `Optimization model deployment '<name>' not found` | `OPTIMIZATION_MODEL` is not the name of a deployed model in your Foundry project | Use the exact deployment name from **Build** > **Deployments**, such as an existing `gpt-5` family or DeepSeek deployment in your project. |
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
