---
title: "Agent optimizer in Foundry Agent Service overview (preview)"
description: "Automatically improve hosted agents by evaluating behavior and generating better instructions, skills, tools, and model configurations using the agent optimizer in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: overview
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# What is the agent optimizer? (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer in Foundry Agent Service automatically improves your hosted agents by evaluating their behavior and generating better configurations. These configurations primarily include improved system instructions and discovered skills.

Building effective AI agents requires extensive prompt engineering. You deploy an agent with handcrafted instructions, test it against real scenarios, identify weaknesses, revise the prompt, and repeat. This loop is slow, subjective, and doesn't scale. The agent optimizer automates this cycle so you can focus on your agent's core logic.

## How the agent optimizer works

The agent optimizer runs a closed-loop evaluation and improvement cycle:

1. **Evaluate the baseline.** The optimizer invokes your agent against a dataset of tasks and scores each response against criteria you define or a built-in default set. The *baseline* is your agent's score before any changes.
1. **Generate candidates.** The optimizer produces alternative configurations called *candidates*—rewritten instructions or discovered skills—designed to improve scores.
1. **Evaluate candidates.** The optimizer tests each candidate against the same dataset.
1. **Rank and recommend.** The optimizer ranks results by composite *score*, a value between 0.0 and 1.0 that represents aggregate performance, and marks the best candidate with ★.
1. **Deploy the winner.** A single command promotes the winning candidate and saves its configuration to your agent's environment.

The entire process runs in the cloud. Start it with `azd ai agent optimize` (requires the [azd CLI extension](../quickstarts/quickstart-optimize-hosted-agent.md#install-the-cli-extension)). The run takes 5 to 20 minutes depending on dataset size.

> [!TIP]
> For the best results, generate a dataset tailored to your agent with `azd ai agent eval init` before running optimization. The optimizer auto-detects the generated `eval.yaml`. For details, see [Create an evaluation dataset](../how-to/create-optimizer-dataset.md).

<!-- :::image type="content" source="media/agent-optimizer-architecture.svg" alt-text="Diagram showing how the agent optimizer interacts with your hosted agent. The agent loads configuration at startup, and the agent optimizer evaluates, generates candidates, and ranks them."::: -->

## Optimization targets

The agent optimizer automatically determines which targets to improve based on your agent's baseline configuration and the `eval.yaml` settings.

### Instruction tuning

The optimizer rewrites and refines your agent's system prompt. It analyzes baseline performance and generates prompt variations that score higher.

**When it activates:** Instruction tuning runs when your agent has an `instructions.md` file in the baseline config directory. This is the most common optimization target and works well for improving response quality, adherence to task requirements, and reducing hallucination.

### Skill improvement

The optimizer improves reusable skills your agent uses. It refines existing *skill* definitions, including their descriptions and implementation bodies. The agent loads these skills through `load_config()` and appends them to the instruction set.

**When it activates:** Skill improvement runs when your agent has a `skills/` directory in the baseline config. Use skills for agents that need structured, repeatable behaviors. For example, a support agent that follows a specific escalation procedure or a travel agent that checks budget policies.

### Tool optimization

The optimizer improves tool descriptions and parameters to help the model call tools more accurately. It refines the function-calling definitions in your `tools.json` file.

**When it activates:** Tool optimization runs when your agent has a `tools.json` file in the baseline config. The optimizer analyzes which tool calls succeed or fail and generates clearer descriptions and parameter definitions.

### Model selection

The optimizer evaluates your agent across multiple model deployments in a single run to find the best quality-to-cost trade-off. For example, it can determine whether `gpt-4.1-mini` handles your workload at lower cost or whether `gpt-4.1` provides a quality improvement that justifies the extra token cost.

**When it activates:** Model selection runs when you include `optimization_config.model` in your `eval.yaml` with a list of model deployments to evaluate. The optimizer scores each model option against the same dataset and shows the trade-offs.

Configure model candidates in your `eval.yaml`:

```yaml
# eval.yaml
options:
  optimization_config:
    model:
      - gpt-4.1
      - gpt-4.1-mini
      - gpt-4o
```

You can combine model selection with instruction and skill optimization in the same run. The optimizer automatically determines which targets to improve based on your baseline configuration and the `optimization_config` settings.

## Config resolution

When your agent starts, the `load_config()` function checks four sources in order:

| Priority | Source | Environment variables | When it's used |
| ---------- | -------- | ---------------------- | ---------------- |
| 1 | Inline JSON | `OPTIMIZATION_CONFIG` | After deploying directly through the API |
| 2 | Resolver API | `OPTIMIZATION_CANDIDATE_ID` + `OPTIMIZATION_RESOLVE_ENDPOINT` | During optimization evaluation |
| 3 | Local directory | `OPTIMIZATION_LOCAL_DIR` (defaults to `.agent_configs/`) | After `azd ai agent optimize apply` writes config locally |
| 4 | No config | — | Raises `ValueError` (or returns `None` if `required=False`) |

Your agent always works with or without optimization. You don't need feature flags or conditional logic. Call `load_config()` and use the values it returns. For implementation details, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md).

## What gets optimized

| Field | Description | Target |
| ------- | ------------- | ---------- |
| `instructions` | System prompt and instructions | instruction, skill |
| `skills` | Discovered skill catalog | skill |
| `model` | Model deployment name | model |
| `temperature` | Sampling temperature | (future) |

## Models

The agent optimizer uses two models during an optimization run. Both must be deployed in your Foundry project.

| Model | Config key | CLI flag | Role | Supported models |
| ------- | ------------ | -------- | ------ | ------------------ |
| **Eval model** | `eval_model` | `--eval-model` | Scores agent responses against criteria in the dataset | Any chat-completion model (for example, `gpt-4.1-mini`) |
| **Optimization model** | `optimization_model` | `--optimize-model` | Generates candidate configurations (instructions, skills, tools, model selection) | `gpt-5`, `gpt-5.1`, `gpt-5.2`, `gpt-5.4`, `gpt-5.5`, `DeepSeek-V4-Pro`, `DeepSeek-V-3.2` |

The eval model runs once per task per candidate. It reads the agent's response and each criterion, then returns a binary score. The optimization model analyzes baseline results and generates improved candidates across the configured targets (instructions, skills, tools, and models). Because it reasons over the full dataset, a more capable optimization model typically produces better candidates.

```yaml
# eval.yaml
options:
  eval_model: gpt-4.1-mini
  optimization_model: gpt-5.1
```

> [!IMPORTANT]
> The optimization model must be from the supported list above. If you don't specify `optimization_model`, the optimizer falls back to the eval model. In that case, the eval model must also be a supported optimization model.

## Understand optimization results

This section describes the results table structure, how scores are computed, what score improvements mean, and how to diagnose common issues.

> [!TIP]
> You can also view optimization results in the [Azure AI Foundry portal](https://ai.azure.com). Navigate to your project, select **Agents**, choose your agent, and then select the **Optimize** tab to see score comparisons, charts, and deployment options.

After an optimization run completes, you see a results table:

```
Results:
  Candidate              Score    Pass   Tokens
  ──────────────────── ─────── ─────── ────────
  baseline                0.73    100%      430
  baseline_instr_v2       0.77    100%     1180
  baseline_instr_v3       0.85    100%     1204
  baseline_instr_v1 ★     0.92    100%     1063
```

### Results table columns

| Column | Description |
| -------- | ------------- |
| **Candidate** | Name of the configuration. `baseline` is your current agent before optimization. |
| **Score** | Composite score across all tasks and criteria, ranging from 0.0 to 1.0. |
| **Pass** | Percentage of tasks where the agent produced a valid response. |
| **Tokens** | Average token count per response. |

The ★ marks the candidate with the highest composite score. This is the recommended candidate to deploy.

### How scores are computed

The evaluator scores each criterion in the dataset independently as a binary value (0 or 1). The evaluator model reads the agent's response and the criterion's instruction, then determines whether the response satisfies that criterion.

**Per-task score**: The average of a task's criteria scores:

```
Task "refund_policy":
  ✓ mentions_30_days      → 1
  ✓ polite_tone           → 1
  ✗ includes_email        → 0
  Task score: 2/3 = 0.67
```

**Composite score**: The average across all task scores.

### Interpret score improvements

| Improvement | Interpretation |
| ------------- | --------------- |
| Less than 0.03 | Noise. Not a meaningful improvement. |
| 0.03 to 0.10 | Moderate improvement. Worth deploying. |
| 0.10 to 0.20 | Significant improvement. |
| Greater than 0.20 | Major improvement. Likely from a poor baseline. |

### Token trade-offs

Optimized instructions are often longer and more detailed, which can increase response token usage. Consider these factors:

- Whether the token increase is proportional to the score improvement
- Whether the cost increase fits your budget
- Whether responses are unnecessarily verbose or adding value with the extra length

### Pass rate

A pass rate below 100% means some tasks produced invalid responses. For example, the agent might have crashed, timed out, or returned an empty response. If a candidate has a lower pass rate than the baseline, it might have introduced instability.

### All scores are zero

If all candidates (including baseline) score 0.00, the likely cause is a missing eval model. The eval model scores agent responses against criteria and must be deployed in your Foundry project.

```bash
azd ai agent optimize --eval-model gpt-4.1-mini
```

> [!IMPORTANT]
> If the eval model isn't deployed, all scores are zero with no error message. Always verify that your eval model exists in the project.

## Limitations and availability

- The agent optimizer is available in all regions where [hosted agents are available](hosted-agents.md#region-availability).
- The agent optimizer is supported for hosted agents that use the [Responses protocol](hosted-agents.md#protocols-responses-invocations-and-invocations-websocket).

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Create an evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
