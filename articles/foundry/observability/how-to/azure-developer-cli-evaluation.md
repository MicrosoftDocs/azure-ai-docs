---
title: Run agent evaluations with the azd CLI (preview)
description: Learn how to scaffold an evaluation, generate a dataset and evaluator, run the evaluation, and gate a build for a Microsoft Foundry agent by using the Azure Developer (azd) CLI.
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: how-to
ms.date: 08/18/2026
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
---

# Run agent evaluations with the azd CLI (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use the `azd ai eval` extension to add a measured quality loop to an agent built with Microsoft Foundry. You scaffold an evaluation next to your project, optionally generate a dataset and a rubric evaluator, run the evaluation against your agent, and read the results without leaving the terminal.

The same evaluation can run from a pipeline, and `--fail-on` turns its results into a build gate.

This article covers the first evaluation with `azd ai eval init` and `azd ai eval run start`.

## Prerequisites

- An Azure subscription with access to Microsoft Foundry.
- The Azure Developer CLI (`azd`), version 1.27.1 or later. For installation instructions, see [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).
- The `azd ai eval` extension: `azd extension install azure.ai.evaluations`. Run `azd extension list --installed` to check the installed version.
- An authenticated `azd` session. To check your authentication status, run `azd auth status`. If you're not signed in, run `azd auth login`.
- The `Foundry User` role on the Foundry resource (previously named `Azure AI User`). For more information, see [Role-based access control for Microsoft Foundry](../../concepts/rbac-foundry.md).
- A Foundry project, and an agent to evaluate. To let `init` detect the target, the agent must be declared as a service in the project's `azure.yaml`, as `azd ai agent init` does. Otherwise name it with `--target`. For hosted agents, see [Hosted agents](../../agents/concepts/hosted-agents.md).
- A model deployment that supports chat completions in the same project. The graders judge with it.
- Optional: a JSONL dataset of representative examples, if you don't want `generate` to synthesize one.

## How azd evaluations work

An evaluation is described by a file, `evals/azure.eval.yaml`, that you can read, edit, and commit. The commands either write that file or act on what it declares.

```bash
azd ai eval init          # scaffold the configuration. Makes no service calls
azd ai eval generate      # optional: synthesize a dataset and a rubric evaluator
azd ai eval create        # register the eval in the Foundry project
azd ai eval run start     # run it and summarize the results
```

| Item | Description |
| --- | --- |
| `init` | Scaffolds `evals/azure.eval.yaml` for an agent and adds an evaluation service to `azure.yaml`. Makes no service calls. |
| `generate` | Synthesizes a dataset, a rubric evaluator, or both, downloads them, and adds a catalog entry for each to the configuration. Submits billed generation jobs. |
| `evals/azure.eval.yaml` | The evaluation recipe: what is evaluated, where the rows come from, and which evaluators grade them. |
| `create` | Registers the declared datasets, evaluators, and the eval itself in the project. |
| `run start` | Starts a run and, by default, waits for it and prints a per-evaluator summary. |
| `run output list` | The per-sample results behind that summary. |
| `dataset`, `evaluator` | Manage registered datasets and evaluators directly, including `versions list`. |
| `job` | Inspect, cancel, and delete the generation jobs `generate` submits. |

Every command accepts `-o json` for scripting and `--debug` for diagnostics. Every command except `init` accepts `--project-endpoint`.

## Choose where the rows come from

An evaluation grades rows. They come from one of two places, and this is the first decision:

- `--source traces` evaluates what your agent already did, read from the traces it emitted. Nothing to author.
- `--source dataset` evaluates a fixed set of examples, either yours or generated. Repeatable and comparable across agent versions.

Trace-sourced evaluations need an agent that emits traces. Dataset-sourced evaluations need a `.jsonl` file or a registered dataset.

## Scaffold the evaluation

Run `init` from your project root:

```bash
azd ai eval init
```

With no flags, `init` detects the agent when `azure.yaml` declares one, prompts when it declares several, and asks which model deployment the graders judge with and which evaluators to use. It writes `evals/azure.eval.yaml` and adds an evaluation service to `azure.yaml`. It makes no service calls, so it's safe to run before anything is deployed.

In a project that declares no agent service, `init` stops rather than guess:

```output
ERROR: this project declares no agent service to evaluate. Add one, or name an existing agent with --target
```

Name the agent yourself in that case, with `--target`.

For scripted use, pass the decisions directly:

```bash
azd ai eval init \
  --source traces \
  --target support-agent \
  --judge-model gpt-4.1-nano \
  --name support-trace-eval \
  --no-prompt
```

To evaluate a dataset you already have:

```bash
azd ai eval init \
  --source dataset \
  --target support-agent \
  --dataset ./tests/support-golden.jsonl \
  --evaluator builtin.intent_resolution,builtin.task_adherence \
  --judge-model gpt-4.1-nano
```

`--dataset` takes a local `.jsonl` path or the name of a registered dataset. `--evaluator` is repeatable and comma-separated; `builtin.<name>` references a [built-in evaluator](../../concepts/built-in-evaluators.md), and a bare name references a [custom evaluator](../../concepts/evaluation-evaluators/custom-evaluators.md) registered in the project. Passing `--evaluator` replaces the defaults, so it also opts out of rubric generation.

To discover the built-in names:

```bash
azd ai eval evaluator list --builtin
```

## Generate a dataset and an evaluator

If you don't have a dataset, or you want a rubric written for this agent rather than a generic one, generate them:

```bash
azd ai eval generate \
  --target support-agent \
  --generation-model gpt-4.1-nano \
  --agent-instruction "Handles support requests. Test triage, policy adherence, and escalation."
```

By default this generates both a dataset and a rubric evaluator, downloads them under `evals/`, and adds a catalog entry for each to `evals/azure.eval.yaml`. Narrow it with `--dataset` or `--evaluator` to generate only one, and cap the rows with `--max-samples` (15 to 1000, default 15).

`generate` submits jobs that cost model calls. The instruction matters: it's what the service uses to decide what the rows and rubric are about, so describe what the agent does and what should be tested.

A catalog entry declares the artifact; it doesn't decide which evaluation uses it. After `generate`, open `evals/azure.eval.yaml` and check that the eval you intend to run references what was produced — a trace-sourced eval reads traces, so a generated dataset is only used once an eval names it:

```yaml
datasets:
    - name: support-agent-dataset
      source: ./datasets/support-agent-dataset.jsonl
evals:
    - name: support-agent-eval
      dataset: support-agent-dataset   # point the eval at the generated dataset
```

To submit the jobs and come back later:

```bash
azd ai eval generate --target support-agent --generation-model gpt-4.1-nano --no-wait
azd ai eval job list --dataset
azd ai eval job show <job-id> --dataset
```

`--dataset` and `--evaluator` on `job` choose which collection to act on, and one of them is required.

## Review azure.eval.yaml

`init` writes a file you're meant to read. A trace-sourced evaluation looks like this:

```yaml
evals:
    - name: support-trace-eval
      description: Basic quality evaluation for support-agent
      source:
        type: traces
        max_traces: 20
        agent_name: support-agent
      evaluation_level: turn
      evaluators:
        - evaluator: builtin.task_adherence
          initialization_parameters:
            model: gpt-4.1-nano
```

A dataset-sourced evaluation names the dataset instead of a trace source, and records the agent it targets:

```yaml
datasets:
    - name: support-golden
      source: ../tests/support-golden.jsonl
evals:
    - name: support-agent-eval
      description: Basic quality evaluation for support-agent
      dataset: support-golden
      evaluation_level: turn
      evaluators:
        - evaluator: builtin.intent_resolution
          initialization_parameters:
            model: gpt-4.1-nano
        - evaluator: builtin.task_adherence
          initialization_parameters:
            model: gpt-4.1-nano
      target:
        type: agent
        name: support-agent
```

Paths under `source:` are relative to the configuration file. The generated `.jsonl` and evaluator JSON are ordinary files: edit them, then run `create` again to register a new version.

Commit this file. It's the reproducible part of the evaluation.

## Create the eval and run it

`create` registers everything the configuration declares — datasets, evaluators, and the eval itself:

```bash
azd ai eval create
```

Then run it:

```bash
azd ai eval run start
```

`run start` waits for the run by default and prints a per-evaluator table with a pass rate and a mean score, plus a link to the run in the portal. Use `--no-wait` to submit and return, and `--max-samples` to cap the rows sent.

If the configuration declares more than one eval, name the one you mean:

```bash
azd ai eval run start --eval support-trace-eval
```

## Inspect the results

The summary tells you whether quality moved. The per-sample rows tell you why:

```bash
azd ai eval run output list --eval support-trace-eval
azd ai eval run output list --eval support-trace-eval --failed-only
```

To see runs over time, and what the service holds for one eval:

```bash
azd ai eval list
azd ai eval run list --eval support-trace-eval
azd ai eval show support-trace-eval
```

`show` returns the eval's identity in the project — id, name, and when it was created. What the eval *does* is in your `evals/azure.eval.yaml`.

`run list` carries one pass rate per run. The per-evaluator breakdown is in `-o json`, under `per_testing_criteria_results`, because a column per evaluator stops being readable once runs score different evaluators.

To take the results elsewhere:

```bash
azd ai eval run output list --eval support-trace-eval --output-file rows.json
azd ai eval run output export --eval support-trace-eval --format csv --output-file summary.csv
```

The two differ, and the difference matters: `run output list --output-file` writes the per-sample rows, while `run output export` writes one line per run — the totals behind the summary.

## Gate a build

Pass `--fail-on` to turn the run into a check. It exits non-zero when the run misses the threshold, which is how a pipeline fails a change that regressed quality:

```bash
azd ai eval run start --fail-on pass-rate=0.8
azd ai eval run start --fail-on any-failure
```

Without `--fail-on`, a completed run with failing samples still exits 0. Failing samples are the expected output of a working evaluation, not a tool error, so gating is opt-in.

`pass-rate` takes a number between 0 and 1. A threshold that isn't one is refused before the run is submitted, so a mistyped gate costs nothing.

`--fail-on` needs a run that has finished. On `run show`, pair it with `--wait`.

## Deploy evaluations with the rest of the project

`init` adds an evaluation service to `azure.yaml`, so the eval is part of the project rather than a side artifact:

```bash
azd up
```

That provisions the project and registers the declared datasets, evaluators, and evals, the same work `azd ai eval create` does on its own.

## Change the agent and re-evaluate

After you change and redeploy the agent, run the same evaluation again:

```bash
azd deploy
azd ai eval run start --eval support-trace-eval
```

Reusing the same eval keeps the dataset, evaluators, and thresholds fixed, so the comparison is about the agent.

To change what the evaluation measures, edit `evals/azure.eval.yaml` or the generated artifacts under `evals/`, then run `create` again. `create` registers a new version of anything that changed and leaves earlier runs pinned to the versions they used.

## Best practices

- Start with `--source traces` if the agent already runs and emits traces. It measures what happened, and there's nothing to author.
- Move to `--source dataset` once you want a fixed set of cases you can compare across versions.
- Read the generated dataset and rubric before trusting the scores. `generate` seeds them from the instruction you give it, so a vague instruction produces vague rows.
- Use more than one evaluator. A single criterion moves the number without telling you why.
- Commit `evals/azure.eval.yaml` and the generated artifacts, so the evaluation is reviewable.
- Gate with `--fail-on` in CI, and keep the threshold where a real regression trips it.

## Limitations

- The extension is in preview, and the command surface can change.
- `generate` submits billed jobs. Datasets and evaluators are not created by `azd provision`.
- A trace-sourced evaluation can only read traces the agent has already emitted.
- `azd` collapses an extension's exit code, so a gate breach and an operational failure both surface as a non-zero exit. Read the gate message to tell them apart.

## Related content

- [Evaluate your agents](evaluate-agent.md)
- [Built-in evaluators](../../concepts/built-in-evaluators.md)
- [Custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md)
- [Trace evaluation](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview)
- [Set up tracing for your agent](trace-agent-setup.md)
