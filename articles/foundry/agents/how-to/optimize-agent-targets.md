---
title: "Optimize agent instructions, skills, tools, and models in Foundry Agent Service (preview)"
description: "Run instruction tuning, skill discovery, tool optimization, or model selection using the agent optimizer to automatically improve your hosted agent's performance in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Optimize agent instructions, skills, tools, and models (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer improves four aspects of your hosted agent: **instructions**, **skills**, **tools**, and **model selection**. It automatically detects which of these targets to optimize from your agent's baseline configuration.

This article shows how to run an optimization, configure and monitor the run, and deploy the results. For what each target does and when it activates, see [Optimization targets](../concepts/agent-optimizer-overview.md#optimization-targets). To set up the baseline inputs, see [Make your agent optimizer-ready](make-agent-optimizer-ready.md). For a quick reference on what the optimizer changes, see [What each target changes](#what-each-target-changes).

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- The `azure.ai.agents` CLI extension installed (see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md))
- A model deployed for evaluation (for example, `gpt-4.1-mini`) and an optimization model from the [supported list](../concepts/agent-optimizer-overview.md#models) (for example, `gpt-5.1`)
- Your agent is [optimizer-ready](make-agent-optimizer-ready.md) (calls `load_config()`)

## Run an optimization

Start an optimization run with a single command:

```bash
azd ai agent optimize
```

The optimizer evaluates your baseline, generates candidates, evaluates them, and ranks the results. For the full evaluate-and-improve cycle, see [How the agent optimizer works](../concepts/agent-optimizer-overview.md#how-the-agent-optimizer-works). Which targets run depends on your baseline configuration—instruction tuning, skill improvement, and tool optimization activate automatically when the matching baseline files are present. See [Optimization targets](../concepts/agent-optimizer-overview.md#optimization-targets).

To control the run with a config file, pass an `eval.yaml` that references your dataset, evaluators, and options:

```bash
azd ai agent optimize --config eval.yaml
```

For the full `eval.yaml` schema, see [Configure the optimization run](#configure-the-optimization-run).

### Target a specific agent

By default, the CLI optimizes the agent detected from your current `azd` environment and your project's local `agent.yaml`. The optimizer resolves the agent name in this priority order:

| Priority | Source | Example |
| -------- | ------ | ------- |
| 1 (highest) | `--agent` CLI flag | `azd ai agent optimize --agent my-support-agent` |
| 2 (default) | Current `azd` environment and the `name` field in local `agent.yaml` | `name: my-support-agent` |
| 3 | `agent.name` field in `eval.yaml` | `agent:\n  name: my-support-agent` |

Use the `--agent` flag when you have multiple agents in your project or want to override the default. The agent name must match a deployed hosted agent in your Foundry project.

> [!NOTE]
> Run `azd ai agent invoke "test"` to verify your agent responds before starting optimization.

## Configure the optimization run

Configure optimization runs through an `eval.yaml` file that ties together your dataset, evaluators, and run options. The command `azd ai agent eval generate` writes this file for you, or you can create it by hand. The optimizer auto-detects `eval.yaml` in your project root, or you can pass it explicitly with `--config eval.yaml`.

```yaml
# eval.yaml
name: my-optimization              # Optional label for the run
agent:
  name: my-agent                   # Deployed hosted agent name
  kind: hosted
  version: "1"                     # Agent version (optional)
  model: gpt-4.1-mini              # Baseline model deployment
  config: .agent_configs/baseline/metadata.yaml
dataset:
  local_uri: ./eval.jsonl          # A local JSONL file...
  # name: my-foundry-dataset       # ...OR a registered Foundry dataset
  # version: "1"
# validation_dataset:              # Optional held-out dataset
#   name: my-validation-dataset
#   version: "1"
evaluators:
  - builtin.task_adherence         # A built-in evaluator...
  # - name: my-custom-evaluator    # ...or a custom evaluator
  #   version: "1"
  #   local_uri: ./my_evaluator.json
options:
  eval_model: gpt-4.1-mini         # Scores responses
  optimization_model: gpt-5.1      # Generates candidates
  max_candidates: 4
  optimization_config:
    model_search_space:            # Optional: compare model deployments
      - gpt-4.1
```

| Field | Required | Description |
| ----- | -------- | ----------- |
| `name` | No | Label for the optimization run. |
| `agent.name` | Yes | Name of the deployed hosted agent to optimize. |
| `agent.kind` | Yes | Agent kind. Use `hosted`. |
| `agent.version` | No | Agent version to target. |
| `agent.model` | Yes | Baseline model deployment name. |
| `agent.config` | Yes | Path to the baseline `metadata.yaml`. |
| `dataset` | Yes | The dataset to evaluate against, as a local JSONL file (`local_uri`) or a registered Foundry dataset (`name` and `version`). See [Create a custom dataset](create-optimizer-dataset.md#create-a-custom-dataset-advanced). |
| `validation_dataset` | No | A held-out dataset used to validate results. |
| `evaluators` | Yes | Evaluators applied to every task. See [Customize evaluators](create-optimizer-dataset.md#customize-evaluators-advanced). |
| `options.eval_model` | Yes | Deployed chat model that scores responses. See [Choose the eval and optimization models](#choose-the-eval-and-optimization-models). |
| `options.optimization_model` | Yes | Deployed model that generates candidates. Must be on the [supported list](../concepts/agent-optimizer-overview.md#models). |
| `options.max_candidates` | No | Number of candidates to generate (default 5). See [Set the number of candidates](#set-the-number-of-candidates). |
| `options.optimization_config.model_search_space` | No | Model deployments to compare during model selection. See [Evaluate multiple models](#evaluate-multiple-models). |

Author the dataset and evaluators separately; see [Create an evaluation dataset and evaluators](create-optimizer-dataset.md). The following sections describe the run options.

### Choose the eval and optimization models

The optimizer uses two models: an *eval model* that scores agent responses against criteria, and an *optimization model* that generates candidate configurations. Set them in `eval.yaml` or use CLI flags.

```yaml
options:
  eval_model: gpt-4.1-mini
  optimization_model: gpt-5.1
```

```bash
azd ai agent optimize --eval-model gpt-4.1-mini --optimize-model gpt-5.1
```

Any chat-completion model deployed in your project works as the eval model. The optimization model must be from the supported list. For roles and supported models, see [Models](../concepts/agent-optimizer-overview.md#models).

> [!IMPORTANT]
> The `optimization_model` field is required. If you don't specify it and don't pass `--optimize-model`, the optimization API returns an error. Always verify that both models are deployed in your project before you run optimization.

### Set the number of candidates

The `max_candidates` option sets the expected number of candidate configurations for the run. The optimizer typically returns after it reaches that count, unless the run stops early because of an error or another stopping condition.

| Max candidates | Candidates | Time | Best for |
| ---------------- | ----------- | ------ | ---------- |
| 2 | 2 | 5 to 10 min | Quick experiments |
| 5 (default) | 5 | 20 to 30 min | Good balance |
| 10 | 10 | 30 to 60 min | Thorough exploration |

Higher values explore more variations but take longer. The optimizer learns from earlier candidates, so later candidates tend to score higher.

> [!NOTE]
> Times are approximate for a dataset of 3 to 10 tasks. Larger datasets or slower eval models increase run duration.

### Evaluate multiple models

To compare model deployments in a single run, list them under `optimization_config.model_search_space`. The optimizer evaluates your agent with each model against the same dataset and ranks the results by score and token cost.

```yaml
# eval.yaml
options:
  optimization_config:
    model_search_space:
      - gpt-4.1
      - gpt-4.1-mini
      - gpt-4o
```

Each model listed under `model_search_space` must be deployed in your Foundry project.

> [!NOTE]
> If the list includes your agent's current model deployment, the optimizer automatically removes it from the candidates because the baseline already represents that model. If no models remain after this removal, you receive a validation error.

Model selection runs alongside the targets that activate automatically from your baseline. A single run can produce candidates that combine improved instructions, skills, and tool descriptions with different model options - you don't configure the combination yourself.

## Monitor a running job

An optimization run is asynchronous. Use these commands when a job is long-running or you want to check its progress:

```bash
# Check status and stream progress
azd ai agent optimize status <operation-id> --watch

# List recent optimization jobs
azd ai agent optimize list

# Cancel a running job
azd ai agent optimize cancel <operation-id>
```

Capture the operation ID, portal URL, scores, and candidate IDs from the run output. You can also monitor the job in the [Foundry portal](https://ai.azure.com) using the URL shown when the run starts.

## Interpret results

After optimization completes, review the results table. An asterisk (`*`) marks the best candidate. For the results table columns, scoring details, score-improvement thresholds, and the portal view, see [Understand optimization results](../concepts/agent-optimizer-overview.md#understand-optimization-results).

## Deploy the winner

The recommended workflow is to apply the optimized config locally, then deploy:

```bash
# Apply the winning candidate locally
azd ai agent optimize apply --candidate <candidate-id>

# Deploy with the optimized config
azd deploy
```

This downloads the optimized configuration into `.agent_configs/<candidate_id>/` in your project. On next deploy, your agent uses the improved instructions and tool descriptions.

Alternatively, you can deploy directly via the API (useful for quick A/B testing):

```bash
azd ai agent optimize deploy --candidate <candidate-id>
```

> [!WARNING]
> Direct deploy updates the agent service without changing your local files. Use the `apply` -> `deploy` workflow for production.

If all candidates score lower than the baseline, don't deploy any candidate. The baseline configuration remains active.

## What each target changes

The optimizer automatically activates the targets that apply to your baseline. This section is a reference for what a run changes. Use the following table to anticipate what optimization does for your agent:

| Scenario | Target |
| ---------- | ------ |
| Improve overall response quality | Instruction tuning |
| Reduce incorrect information | Instruction tuning |
| Improve repeatable behaviors (escalation, debugging patterns) | Skill improvement |
| Refine structured procedures | Skill improvement |
| Find the best quality/cost model trade-off | Model selection |
| First optimization, not sure what to expect | All applicable targets run automatically |

Your code stays the same across all targets because `load_config()` returns the optimized values automatically. Only the configuration the model sees changes.

### Instructions

The optimizer rewrites the system prompt. Common improvements include:

- Adding explicit constraints that the original prompt implied but didn't state
- Restructuring instructions for clarity
- Adding output format specifications
- Strengthening safety and scope boundaries

For example, a minimal baseline prompt like `You are a helpful assistant.` might become:

```
You are a helpful coding assistant. Follow these guidelines:
1. Always include working code examples
2. Explain your reasoning step by step
3. If a question is outside your expertise, say so clearly
4. Use markdown formatting for code blocks
5. Handle edge cases in code examples
```

### Skills

The optimizer refines each skill's description, body, and activation criteria while keeping the skill's purpose intact. The agent loads improved skills through `load_config()`, which appends them to the instruction set. Skills use the open [Agent Skills](https://agentskills.io) format. For how your agent loads skills, see [Make your agent optimizer-ready](make-agent-optimizer-ready.md#load-and-use-the-config).

### Tools

The optimizer refines your `tools.json` definitions. Common improvements include:

- Clearer function descriptions that help the model know when to call a tool
- More specific parameter descriptions that reduce inaccurate arguments
- Added constraints (enums, required fields) that prevent invalid inputs

Your tool implementation code stays the same. Only the definitions the model sees change.

### Models

The optimizer ranks each candidate model by composite score and token cost, so you can choose the best quality-to-cost trade-off. To configure the candidates, see [Evaluate multiple models](#evaluate-multiple-models).

## Troubleshooting

| Problem | Cause | Fix |
| --------- | ------- | ----- |
| `optimize` returns 400 | Subscription not on allow list | Contact your Microsoft representative to request access |
| Protocol validation error | Invalid `azure.yaml` agent service | Ensure the `azure.ai.agent` service includes `kind: hosted` and a `protocols:` list |
| Job stuck at "running" | Service issue | Cancel with `azd ai agent optimize cancel <id>` and retry |
| No candidate IDs in output | Job still running | Wait for completion or use `--watch` |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Make your agent optimizer-ready](make-agent-optimizer-ready.md)
- [Create an evaluation dataset and evaluators](create-optimizer-dataset.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
