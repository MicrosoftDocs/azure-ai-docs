---
title: "Quickstart: Optimize a hosted agent (preview)"
description: "Deploy and optimize a hosted agent by using the Azure Developer CLI, Python SDK, VS Code, or the Microsoft Foundry Skill."
author: aahill
ms.author: aahi
ms.date: 08/25/2026
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

For the concepts behind each step and the full end-to-end path, see the [optimization workflow](../concepts/agent-optimizer-overview.md#the-optimization-workflow).

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
  pip install "azure-ai-projects>=2.4.0" azure-ai-agentserver-optimization azure-identity python-dotenv
  ```

* An existing Foundry project that already contains the hosted agent,
  registered dataset, and evaluator you want to use for optimization.

:::zone-end

:::zone pivot="vscode"

* [Visual Studio Code](https://code.visualstudio.com/).
* [Microsoft Foundry Toolkit for Visual Studio Code](https://aka.ms/foundrytk)
  version 1.6.4 or later, signed in to Azure. Foundry Toolkit installs and
  updates the [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md)
  used by this workflow.
* [GitHub Copilot in Visual Studio Code](https://code.visualstudio.com/docs/copilot/setup)
  with access to agent mode. Foundry Toolkit sends the Agent Optimizer request
  to GitHub Copilot after you select the agent workspace.
* [Azure CLI](/cli/azure/install-azure-cli) and
  [Azure Developer CLI (AZD)](/azure/developer/azure-developer-cli/install-azd)
  installed and authenticated:

  ```bash
  az login
  azd auth login
  ```

> [!TIP]
> If you don't have Foundry Toolkit, [install it from the Visual Studio Code
> Marketplace](https://aka.ms/foundrytk). Foundry Toolkit brings your Foundry
> resources, model catalog, hosted-agent deployment and playgrounds, and Agent
> Optimization into Visual Studio Code. Reload Visual Studio Code if prompted,
> and then sign in to Azure. For a tour of the extension, see [Work with the
> Microsoft Foundry Toolkit for Visual Studio Code
> extension](../../how-to/develop/get-started-projects-vs-code.md).

:::zone-end

:::zone pivot="foundry-skills"

* A coding agent host with the
  [Microsoft Foundry Skill](../../how-to/develop/use-microsoft-foundry-skill.md)
  installed.
* [Azure CLI](/cli/azure/install-azure-cli) and
  [Azure Developer CLI (AZD)](/azure/developer/azure-developer-cli/install-azd)
  installed and authenticated:

  ```bash
  az login
  azd auth login
  ```

* The `microsoft.foundry` extension for AZD. Install it before you start the
  workflow:

  ```bash
  azd ext install microsoft.foundry
  ```

  If it's already installed, upgrade it:

  ```bash
  azd ext upgrade microsoft.foundry
  ```

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

This template imports the [Optimization Customer Support sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support), an optimization-ready Python hosted agent that uses the bring-your-own approach and the Responses protocol. It represents a consumer electronics support agent that handles order inquiries, returns, warranty claims, troubleshooting, complaints, recommendations, and escalation. The deliberately minimal baseline instruction makes the improvements from instruction optimization and skill discovery easy to compare.

The sample calls `load_config()` to load baseline or candidate configuration and includes `.agent_configs/baseline/`, `eval.yaml`, full and quick evaluation datasets, container configuration, and the Foundry deployment manifest. The interactive flow imports these files and prompts for your Azure subscription, region, and model deployment settings.

> [!TIP]
> If you already have an existing agent project, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md) to add optimization support.
>
> If you already have a Foundry project, add `-p <project-resource-id>` to target existing resources.
>
> To optimize an already deployed agent without running `azd ai agent init` or creating `azure.yaml` and `.azure` files, skip this project-creation step and follow [Optimize an existing agent without AZD project files](../how-to/optimize-agent-targets.md#optimize-an-existing-agent-without-azd-project-files).

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

from azure.ai.agentserver.optimization import load_config
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
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
eval_model = os.environ.get("EVAL_MODEL", "gpt-4o")
optimization_model = os.environ.get("OPTIMIZATION_MODEL", "gpt-5")
poll_interval_seconds = int(os.environ.get("POLL_INTERVAL_SECONDS", "10"))

optimization_config = load_config() # Reads agent optimization config from .agent_configs/baseline/metadata.yaml

with (
  DefaultAzureCredential() as credential,
  AIProjectClient(endpoint=endpoint, credential=credential) as project_client,
):
  job = OptimizationJob(
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
        optimization_config={
          "system_prompt": optimization_config.instructions,
          **({"tools": optimization_config.tool_definitions} if optimization_config.tool_definitions else {}),
          **({"skills": optimization_config.skills} if optimization_config.has_skills else {}),
        }
      ),
    )
  )
  poller = project_client.beta.agents.begin_create_optimization_job(job=job)

  print(f"Optimization job started, waiting for completion...")
  while not poller.done():
    print(f"\tstatus=`{poller.status()}`")
    time.sleep(poll_interval_seconds)

  result = poller.result()

  if result:
    print(f"Baseline candidate: {result.baseline}")
    print(f"Best candidate: {result.best}")

    for candidate in result.candidates or []:
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

:::zone pivot="vscode"

## Run the optimization in VS Code

Foundry Toolkit includes a native Agent Optimization experience for deployed
hosted agents. From the agent playground, you can start an optimization run,
compare candidates with the baseline, inspect configuration changes, and deploy
the best candidate.

### Step 1: Select a deployed hosted agent

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, select **Agents**.
1. If you have a deployed hosted agent, select it to open the hosted agent
  playground.
1. If you don't have a deployed hosted agent, complete the VS Code path in
  [Quickstart: Deploy your first hosted agent](quickstart-hosted-agent.md?pivots=vscode).
  After deployment finishes, return to **Agents** and select the new hosted
  agent.

### Step 2: Start an optimization run

1. Select the **Optimize** tab, which is marked **Preview**.

:::image type="content" source="../media/quickstart/optimize-hosted-agent-vscode-optimize-tab.png" alt-text="Screenshot of a hosted agent in Foundry Toolkit with the Optimize preview tab selected and the New Optimization button available." lightbox="../media/quickstart/optimize-hosted-agent-vscode-optimize-tab.png":::

1. Select **New Optimization**.
1. In **Select Workspace**, choose the workspace that contains the selected
   hosted agent's code:

   * Select **Current workspace** if the current workspace contains the agent
     code and its `azure.yaml` file.
   * Select **Browse...** to open the workspace that contains the agent code.

   Foundry Toolkit uses the workspace files to prepare the optimization and to
   apply a candidate to the matching `azure.ai.agent` service.

:::image type="content" source="../media/quickstart/optimize-hosted-agent-vscode-select-workspace.png" alt-text="Screenshot of the Select Workspace prompt in Foundry Toolkit showing Current workspace and Browse options for locating the hosted agent code." lightbox="../media/quickstart/optimize-hosted-agent-vscode-select-workspace.png":::

1. Foundry Toolkit opens GitHub Copilot Chat and sends an Agent Optimizer
   request populated with the selected agent's kind, name, and Foundry project
   endpoint.
1. Answer the four optimization questions in Copilot Chat:

   | Input | What to provide |
   | ----- | --------------- |
   | Evaluation metrics | Enter the metrics or evaluators to use. If you don't have them, choose whether to run `azd ai agent eval generate` or use the optimizer's built-in defaults. |
   | Dataset | Select the optimization dataset. If you don't have one, choose whether to run `azd ai agent eval generate` or use the optimizer's built-in defaults. |
   | Maximum candidates | Enter the maximum number of candidates to generate, such as `2`. |
   | Optimization model | Select an existing deployment from the [supported optimization models](../concepts/agent-optimizer-overview.md#models). |

GitHub Copilot waits for these inputs before it starts optimization. The
generated request directs Copilot to use the Microsoft Foundry Skill's Agent
Optimizer workflow and Azure Developer CLI commands exclusively. It doesn't use
Foundry MCP tools. Copilot:

* Inspects the agent code in the selected workspace.
* Initializes an AZD environment from existing `azure.yaml` and `.env` values
  if the project doesn't already have one.
* Wires the agent for optimization and deploys the updated hosted agent.
* Creates `eval.yaml` in the agent service folder.
* Starts the optimization after you review and approve the proposed file
  changes and commands.

After Copilot submits the job, return to the **Optimize** tab. The run appears
under **Optimization runs**. The table shows its run ID, status, candidate count,
baseline score, best score, and creation time.

### Step 3: Compare and deploy the best candidate

1. When the run succeeds, select it under **Optimization runs**.
1. Compare the **Baseline** and **Best** scores. Review **Score details** for
  each candidate, and select **View changes** to inspect its configuration
  changes.
1. If the best candidate improves on the baseline, select **Deploy best
  candidate** to update the current agent. To deploy it as a new agent or
  change deployment settings, select **Custom deploy** instead.

> [!NOTE]
> If every candidate scores lower than the baseline, don't deploy a candidate.
> Keep the current agent and revise the dataset or optimization settings before
> you run the optimizer again.

:::image type="content" source="../media/quickstart/optimize-hosted-agent-vscode-results.png" alt-text="Screenshot of a completed optimization run in Foundry Toolkit comparing the baseline and generated candidates, with scores, configuration changes, and deployment options." lightbox="../media/quickstart/optimize-hosted-agent-vscode-results.png":::


:::zone-end

:::zone pivot="foundry-skills"

## Run the optimization with the Microsoft Foundry Skill

Use this path in any coding agent host that supports the Microsoft Foundry
Skill, such as GitHub Copilot in Visual Studio Code, Copilot CLI, or Claude
Code. The skill resolves the agent context from `azure.yaml`, loads its Agent
Optimizer workflow, and keeps candidate application and deployment behind
review gates.

### Step 1: Open the agent workspace

Open an empty folder in your coding agent host. Confirm that the
`microsoft-foundry` skill is available. If the skill isn't available, follow
[Use the Microsoft Foundry Skill in coding agents](../../how-to/develop/use-microsoft-foundry-skill.md).

### Step 2: Ask the skill to run Agent Optimizer

Submit this prompt to your coding agent:

```text
Use the Microsoft Foundry Skill to run the Agent Optimizer workflow for a
Python hosted agent. If this workspace doesn't contain an agent, initialize the
customer support optimization sample from this template:
https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/responses/optimization-customer-support/azure.yaml
Resolve the AZD environment and hosted-agent service, verify that the agent is
optimizer-ready, and deploy and invoke the baseline. Generate and show me the
evaluation dataset, evaluators, and eval.yaml before running optimization.
Verify that the project has a supported optimization model deployment, then run
Agent Optimizer with two candidates. Stop after reporting the operation ID,
portal URL, candidate IDs, and scores. Don't apply or deploy a candidate yet.
```

The coding agent might ask you to select a subscription, region, Foundry
project, agent service, evaluation model, or optimization model when it can't
resolve those values from the workspace. Review generated files and
cost-bearing resources before you approve any changes or commands.

### Step 3: Apply and deploy an approved candidate

After you review the optimization results, submit this follow-up prompt:

```text
Recommend the best optimization candidate and explain the score improvement.
Summarize the candidate changes before applying anything. After I approve the
candidate, apply it locally, show the source diff, and stop again before
deployment. After I approve deployment, run azd deploy, invoke the agent with
"What is your return policy?", and rerun the evaluation to confirm the
improvement.
```

The skill uses `azd ai agent optimize apply --candidate <candidate-id>` so you
can review the optimized configuration locally. It deploys only after your
approval, then invokes and evaluates the updated hosted agent.

:::zone-end

## Clean up resources

If your workflow created resources through the AZD project, delete the
provisioned resources when you finish experimenting:

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
| The **Optimize** section doesn't appear for a hosted agent | Foundry Toolkit is older than version 1.6.4, or the selected agent isn't a deployed hosted agent | Update [Foundry Toolkit](https://aka.ms/foundrytk), reload Visual Studio Code, and reopen the deployed agent from the **Agents** tab. |
| GitHub Copilot Chat doesn't open after you select the workspace | GitHub Copilot isn't installed, isn't available for your account, or agent mode is disabled | Set up [GitHub Copilot in Visual Studio Code](https://code.visualstudio.com/docs/copilot/setup), enable agent mode, and then select **New Optimization** again. |
| Foundry Toolkit can't apply the best candidate to the current workspace | The workspace doesn't contain an `azure.yaml` service whose name matches the deployed hosted agent | Open the workspace that contains the selected agent's code and matching `azure.ai.agent` service, then try again. |
| Coding agent can't find the hosted agent | The wrong folder is open, or `azure.yaml` doesn't define an `azure.ai.agent` service | Open the AZD project folder that contains `azure.yaml`, then ask the coding agent to resolve the hosted-agent service again. |
| Coding agent stops before applying or deploying a candidate | The Agent Optimizer skill requires review before source changes and deployment | Review the candidate scores and local diff, then explicitly approve the apply or deployment step. |
| Optimization score is 0 or very low | Evaluation has many errored rows | Open the **Eval** link in the results. Fix response generation or evaluator errors, then rerun. |
| `azd provision` fails with quota error | Subscription lacks capacity | Try a different region or request a quota increase. |

## What you learned

In this quickstart, you:

* Deployed the optimization sample agent by using the customer-support template.
* Ran the agent optimizer by using the Azure Developer CLI, Python SDK, Visual
  Studio Code, or the Microsoft Foundry Skill.
* Deployed the winning candidate and verified the improvement.

## Next steps

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Create an evaluation dataset and evaluators](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
