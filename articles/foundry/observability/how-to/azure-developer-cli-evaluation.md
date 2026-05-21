---
title: Run agent evaluations with the azd CLI (preview)
description: Learn how to initialize evaluation assets, run an evaluation, and inspect results for a Microsoft Foundry agent by using the Azure Developer (azd) CLI.
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.date: 05/20/2026
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted 
---

# Run agent evaluations with the azd CLI (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use the Azure Developer CLI (`azd`) CLI evaluation experience to add a measured quality loop to an agent created with Microsoft Foundry. This article focuses on the hosted-agent lifecycle in `azd`, where you create, provision, deploy, initialize evaluation assets, run a first evaluation, inspect the run, and reuse the evaluation recipe for later runs.

Prompt-based agents can also be evaluated when they are available as agent targets in the Foundry project. The hosted-agent deployment steps apply only to hosted agents.

This article covers how to run the first agent evaluation with `azd ai agent eval init` and `azd ai agent eval run`.

## Prerequisites

- An Azure subscription with access to Microsoft Foundry.
- The Azure Developer CLI (`azd`). For installation instructions, see [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).
- The Foundry agent extension for `azd`. Install it by running:

  ```bash
  azd extension install <foundry-agent-extension-id>
  ```

  [TO VERIFY: confirm the correct extension ID and registry URL with the azd Foundry team.]

- An authenticated `azd` session. To check your authentication status, run `azd auth status`. If you're not signed in, run `azd auth login`.
- The `Foundry User` role on the Foundry resource (previously named `Azure AI User`). For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- **For hosted agents:** No pre-existing Foundry project is required. `azd ai agent init` and `azd provision` create the necessary resources.
- **For prompt-based agents:** An existing Foundry project with the agent already deployed and available as an evaluation target.
- A model deployment that supports chat completions in the same Foundry project. The default model used for evaluation generation is `gpt-4o`.
- Optional: a JSONL evaluation dataset with representative examples, if you do not want `eval init` to generate a smoke dataset.

## How azd agent evaluations work

The primary azd CLI evaluation experience is designed for the hosted-agent lifecycle:

```bash
azd ai agent init
azd provision
azd deploy
azd ai agent eval init
azd ai agent eval run
azd ai agent eval update
# Optional, after the agent and eval recipe meet optimization prerequisites:
azd ai agent optimize --config eval.yaml
```

The evaluation flow includes the following artifacts and commands.

| Item | Description |
|---|---|
| `eval init` | Creates or repairs local evaluation assets for an agent target. |
| `eval.yaml` | Local runnable evaluation recipe. It records the agent target, dataset reference, evaluator references, thresholds, generation options, and pending operation IDs. |
| Generated review artifacts | Local copies of generated datasets and evaluator rubrics for inspection and editing. Generated review artifacts are stored under `.azure/.foundry/`. |
| Registered service artifacts | The Foundry dataset and evaluator versions used by evaluation runs. These are the source of truth for generated assets. |
| `eval run` | Runs the evaluation recipe against the selected agent target. |
| `eval update` | Registers new service versions from local dataset or evaluator edits and updates `eval.yaml` after confirmation. |
| `eval list` and `eval show` | Inspect evaluation runs and results from the CLI. |
| `optimize --config eval.yaml` | Optionally starts optimization from an evaluation recipe after the agent and recipe meet optimization prerequisites. |

`azd provision` does not create evaluation datasets, evaluators, suites, or optimization jobs. Evaluation setup can involve generation work that takes minutes, so it stays explicit and retryable.

For hosted agents, the first evaluation requires a deployed and invokable agent target. For prompt-based agents, the deployment step does not apply; the agent must already exist in the Foundry project and be available as an evaluation target.

## Create and deploy a hosted agent

If you do not already have a hosted-agent project, initialize one with `azd`:

```bash
azd ai agent init
```

Provision the Foundry resources and deploy the agent:

```bash
azd provision
azd deploy
```

After deployment completes, verify the agent is invokable:

```bash
azd ai agent status
```

The hosted agent must be deployed and invokable before you initialize evaluation assets.

After a successful deployment, the CLI suggests evaluation as an explicit next step:

```text
Deployment succeeded and the hosted agent is invokable.

Evaluation next steps:
  Next:  azd ai agent eval init
```

To evaluate a prompt-based agent, skip the hosted-agent creation and deployment commands. Continue to the next section after you confirm that the prompt-based agent exists in the Foundry project and is available as an evaluation target.

## Initialize evaluation assets

Run `eval init` from the azd workspace or agent project folder:

```bash
azd ai agent eval init
```

With no flags, the command starts an interactive wizard. The wizard asks for a generation instruction so the service can create useful seed evaluation data and an evaluator rubric.

Example interactive output:

```text
Detecting agent...
  Found: reservation-agent (hosted)

Generation prompt
  Describe what this agent does and what scenarios to test.
  > This agent handles restaurant reservations. Test booking, modification, cancellation, and policy enforcement.

Generation model
  gpt-4o (default)

Max samples: 100

Generating dataset and evaluators...
  Dataset generation:    done  (registered: reservation-agent-dev-eval-seed/v1)
  Evaluator generation:  done  (registered: reservation-agent-quality/v1)

Eval suite created
  Config:     eval.yaml
  Dataset:    .azure/.foundry/datasets/reservation-agent-dev-eval-seed.v1.jsonl
  Evaluator:  .azure/.foundry/evaluators/reservation-agent-quality.v1.yaml

Review the generated assets, then run:
  azd ai agent eval run
```

For scripted use, pass the generation inputs directly:

```bash
azd ai agent eval init \
  --gen-instruction "This agent handles restaurant reservations. Test booking, modification, cancellation, and policy enforcement." \
  --eval-model gpt-4o \
  --max-samples 100
```

`--output` is optional and defaults to `eval.yaml` in the agent project root. Use `--output <path>` to write the config to a different location.

To use an existing dataset and selected evaluators:

```bash
azd ai agent eval init \
  --dataset ./tests/support-golden.jsonl \
  --gen-instruction "Support quality, policy adherence, and escalation behavior" \
  --max-samples 50 \
  --evaluator builtin.intent_resolution \
  --evaluator custom.support-quality \
  --output eval.yaml
```

Replace `./tests/support-golden.jsonl` with the path to your own evaluation dataset.

The `--dataset` value can point to a local file or a registered dataset name. Repeat `--evaluator` to include multiple built-in or registered custom evaluators. Evaluator references use the format `<source>.<name>`:

- `builtin.<name>` — references a [built-in evaluator](../../concepts/built-in-evaluators.md) provided by Foundry.
- `custom.<name>` — references a [custom evaluator](../../concepts/evaluation-evaluators/custom-evaluators.md) registered in the Foundry project. Use the evaluator's registered name without the version suffix.

### Defer generation with `--no-wait`

If dataset or evaluator generation takes too long, use `--no-wait` to submit generation jobs and exit immediately:

```bash
azd ai agent eval init \
  --gen-instruction "..." \
  --no-wait
```

The pending operation IDs are written to `eval.yaml`. When you later run `azd ai agent eval run`, it automatically resumes those operations before starting the evaluation run.

## Use a prompt-based agent target

If you initialized evaluation assets for a prompt-based agent, you can use the same evaluation recipe flow. The hosted-agent deployment step is not required for prompt-based agents.

Before you run an evaluation, confirm that:

- The prompt-based agent exists in the Foundry project.
- The agent is available as an evaluation target.
- You have access to the project endpoint and the agent target.
- `eval.yaml` selects the intended prompt-based agent.

To list agents available in the current Foundry project, run:

```bash
azd ai agent list
```

[TO VERIFY: confirm `azd ai agent list` returns prompt-based agents. If not, verify agent availability in the Foundry portal under your project > Agents.]

Then use the same commands to run and inspect the evaluation:

```bash
azd ai agent eval run --config eval.yaml
azd ai agent eval show latest
```

## Review eval.yaml

After `eval init` succeeds, open `eval.yaml` in the agent project root. For example:

```text
src/reservation-agent/eval.yaml
```

Run `eval run` from this directory, or pass the path explicitly with `--config src/reservation-agent/eval.yaml`. The file identifies the agent target, dataset reference, evaluator references, and generation options. A simplified shape is:

```yaml
name: smoke-core
agent:
  name: reservation-agent
  kind: hosted     # Use "hosted" for hosted agents or "prompt" for prompt-based agents.
  version: "3"
dataset_reference:
  name: reservation-agent-dev-eval-seed
  version: "1"
evaluators:
  - reservation-agent-quality    # Custom evaluators use their registered name; built-in evaluators omit the "builtin." prefix.
options:
  eval_model: gpt-4o
generation_instruction: Test booking, modification, cancellation, and policy enforcement.
max_samples: 100
```

Treat version fields as strings, even if they look numeric, so the recipe remains stable across YAML parsers.

## Run the evaluation

From the agent project folder, run:

```bash
azd ai agent eval run
```

By default, zero-argument `eval run` resolves `eval.yaml` in the agent project root. You can also pass the config path explicitly:

```bash
azd ai agent eval run --config eval.yaml
```

If `eval init --no-wait` created pending generation operations, `eval run` resumes those operations before it starts the evaluation run. It does not start new dataset or evaluator generation jobs from scratch.

## Inspect evaluation runs

List recent evaluation runs:

```bash
azd ai agent eval list
```

Show the latest run:

```bash
azd ai agent eval show latest
```

`latest` is a reserved alias that resolves to the most recently completed evaluation run.

Show a specific run by its run ID. Copy the ID from the `azd ai agent eval list` output:

```text
ID                                         Status     Agent              Date
run-a1b2c3d4-e5f6-7890-abcd-ef1234567890   completed  reservation-agent  2026-05-20
```

```bash
azd ai agent eval show <evaluation-run-id>
```

Use the run output to answer:

- Which agent version was evaluated.
- Which dataset and evaluator versions were resolved.
- Whether the run completed, failed, or completed partially.
- Which metrics or evaluator scores were produced.
- Whether token usage or evaluator logs need investigation.

## Re-run after changing the agent

After you update and redeploy a hosted agent, run the same evaluation recipe again:

```bash
azd deploy
azd ai agent eval run --config eval.yaml
```

For prompt-based agents, update the agent in Foundry, then rerun the same evaluation recipe.

Re-running the same `eval.yaml` helps keep dataset, evaluator, and threshold references stable across agent changes.

## Update, reset, or repair evaluation assets

The agent evaluation flow uses `eval.yaml` as the local evaluation recipe. Use `azd ai agent eval update` when you edit local dataset files or evaluator rubrics and want to register those edits as new service versions.

To update what an evaluation run uses, choose the path that matches the type of change:

| Change | How to update |
|---|---|
| Change thresholds, evaluator references, output settings, or other recipe fields | Edit `eval.yaml`, then run `azd ai agent eval run --config eval.yaml`. |
| Use a different local or registered dataset | Edit the dataset reference in `eval.yaml`, or rerun `azd ai agent eval init --dataset <path-or-name> --output eval.yaml`. |
| Add or change evaluator references | Edit `eval.yaml`, or rerun `azd ai agent eval init` with repeatable `--evaluator` values. |
| Register local edits to a generated dataset or evaluator rubric | Run `azd ai agent eval update`, review the detected changes, and confirm the version-reference update in `eval.yaml`. |
| Start over from the default generated setup | Run `azd ai agent eval init --reset-defaults`. |

For example, after editing a generated evaluator rubric under `.azure/.foundry/evaluators/`, run:

```bash
azd ai agent eval update
azd ai agent eval run --config eval.yaml
```

The update command creates new registered dataset or evaluator versions. Existing evaluation runs remain tied to the versions they originally used.

When `eval.yaml` already exists, `eval init` detects it and suggests `eval run` instead of overwriting it:

```text
Eval config already exists: eval.yaml

To run the evaluation:
  azd ai agent eval run

To overwrite and regenerate:
  azd ai agent eval init --reset-defaults
```

To overwrite the local config and regenerate the default evaluation assets, run:

```bash
azd ai agent eval init --reset-defaults
```

`--reset-defaults` overwrites the local `eval.yaml` and regenerates the default evaluation assets. Existing service-registered dataset and evaluator versions are not deleted; only the local recipe is replaced.

Do not rely on remote latest versions changing the local recipe silently. The local `eval.yaml` records the dataset, evaluator, or suite versions used by the recipe for reproducibility.

## Optional: start optimization from evaluation signal

After at least one evaluation run succeeds, you can use `eval.yaml` as input to agent optimization if the agent and recipe meet the optimization prerequisites.

Before starting optimization, confirm that:

- The agent target is ready for optimization. For hosted agents, the agent is deployed and invokable.
- `eval.yaml` references the intended agent, dataset, evaluator versions, and thresholds.
- At least one evaluation run completed successfully.
- The agent preparation required by the optimizer is complete. For optimizer prerequisites and agent preparation requirements, see [Optimize agent prompts with Prompt Optimizer](prompt-optimizer.md).

Then run:

```bash
azd ai agent optimize --config eval.yaml
```

The optimize command reads the agent target, dataset, evaluators, and thresholds from `eval.yaml`. It submits an optimization job, but it does not silently apply source changes or redeploy the candidate agent. Review any optimizer output before applying changes.

## Best practices

- Run `azd ai agent eval init` only after the agent is available as an evaluation target. For hosted agents, the agent must be deployed and invokable.
- Start with a small generated dataset or a small subset of your golden dataset.
- Check generated dataset and evaluator review artifacts before trusting scores.
- After editing generated dataset or evaluator files, run `azd ai agent eval update` to register the edited assets before running the evaluation again.
- Source-control `eval.yaml` if your team wants a reviewable, reproducible evaluation recipe.
- Keep generated review copies out of source control unless your team intentionally reviews them. The recommended generated-artifact path is `.azure/.foundry/`.
- Re-run the same `eval.yaml` after agent changes so comparisons use the same test recipe.
- Use `azd ai agent optimize --config eval.yaml` only after you have a useful baseline evaluation result and the agent is prepared for optimization.

## Limitations

- The primary command flow is optimized for hosted agents and the post-deploy evaluation loop.
- `azd provision` does not create evaluation assets.
- `eval run` does not generate new datasets or evaluators, except for resuming pending operations from `eval init --no-wait`.
- Full suite lifecycle, scheduled evaluation, continuous evaluation, alerts, and comparison workflows are not required for the first evaluation path.

## Related content

- [Evaluate your AI agents](evaluate-agent.md)
- [Human evaluation for Microsoft Foundry agents](human-evaluation.md)
- [Evaluation cluster analysis](cluster-analysis.md)
- [Optimize agent prompts with Prompt Optimizer](prompt-optimizer.md)
- [Set up tracing for AI agents in Microsoft Foundry](trace-agent-setup.md)
- [Monitor agents with the Agent Monitoring Dashboard](how-to-monitor-agents-dashboard.md)
- [Hosted agents in Foundry Agent Service](../../agents/concepts/hosted-agents.md)
- [Agent development lifecycle](../../agents/concepts/development-lifecycle.md)
