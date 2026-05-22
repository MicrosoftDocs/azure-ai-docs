---
title: "Agent optimizer in Foundry Agent Service overview (preview)"
description: "Automatically improve hosted agents by evaluating behavior and generating better system instructions and skills using the agent optimizer in Foundry Agent Service."
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

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The agent optimizer in Foundry Agent Service automatically improves your hosted agents by evaluating their behavior and generating better configurations. These configurations primarily include improved system instructions and discovered skills.

Building effective AI agents requires extensive prompt engineering. You deploy an agent with hand-crafted instructions, test it against real scenarios, identify weaknesses, revise the prompt, and repeat. This loop is slow, subjective, and does not scale. The agent optimizer automates this cycle so you can focus on your agent's core logic.

## How the agent optimizer works

The agent optimizer runs a closed-loop evaluation and improvement cycle:

1. **Evaluate the baseline.** Your agent is invoked against a dataset of tasks. Each response is scored against criteria you define or a built-in default set. The *baseline* is your agent's score before any changes.
1. **Generate candidates.** The agent optimizer produces alternative configurations called *candidates*, such as rewritten instructions or discovered skills, that are designed to improve scores.
1. **Evaluate candidates.** Each candidate is tested against the same dataset.
1. **Rank and recommend.** Results are ranked by composite *score*, a value between 0.0 and 1.0 that represents aggregate performance. The best candidate is marked with ★.
1. **Deploy the winner.** A single command promotes the winning candidate and saves its configuration to your agent's environment.

The entire process runs in the cloud. Start it with `azd ai agent optimize` (requires the [azd CLI extension](../quickstarts/quickstart-optimize-hosted-agent.md#install-the-cli-extension)). The run takes 5 to 20 minutes depending on dataset size.

:::image type="content" source="media/agent-optimizer-architecture.svg" alt-text="Diagram showing how the agent optimizer interacts with your hosted agent. The agent loads configuration at startup, and the agent optimizer evaluates, generates candidates, and ranks them.":::

## Optimization targets

### Instruction tuning (default)

The *instruction target* rewrites and refines your agent's system prompt. It analyzes baseline performance and generates prompt variations that score higher.

**When to use:** Most agents. This is the default and works well for improving response quality, adherence to task requirements, and reducing hallucination.

```bash
azd ai agent optimize --target instruction
```

### Skill discovery

The *skill target* discovers reusable capabilities your agent should have. It generates *skill* definitions that include a name, description, and implementation body. The agent optimizer appends these definitions to the agent's instruction set.

**When to use:** Agents that need structured, repeatable behaviors. For example, a support agent that should always follow a specific escalation procedure, or a coding agent that should use particular debugging patterns.

```bash
azd ai agent optimize --target skill
```

## Config resolution

When your agent starts, the `load_config()` function checks four sources in order:

| Priority | Source | When it's used |
| ---------- | -------- | ---------------- |
| 1 | `OPTIMIZATION_CONFIG` environment variable (inline JSON) | After deploying a candidate |
| 2 | `OPTIMIZATION_CANDIDATE_ID` environment variable, resolved through the API | During optimization evaluation |
| 3 | Local directory (`.agent_configs/`) | After resolver persists config locally |
| 4 | Your defaults in code | Normal operation (no optimization) |

Your agent always works with or without optimization. No feature flags or conditional logic are required. Call `load_config()` and use the values it returns. For implementation details, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md).

## What gets optimized

| Field | Description | Target |
| ------- | ------------- | ---------- |
| `instructions` | System prompt and instructions | instruction, skill |
| `skills` | Discovered skill catalog | skill |
| `model` | Model deployment name | (future) |
| `temperature` | Sampling temperature | (future) |

## Models

The agent optimizer uses two models during an optimization run. Both must be deployed in your Foundry project.

| Model | Config key | Role | Supported models |
| ------- | ------------ | ------ | ------------------ |
| **Eval model** | `eval_model` | Scores agent responses against criteria in the dataset | `gpt-4.1-mini` (default) |
| **Reflection model** | `reflection_model` | Generates candidate instructions and skills (the optimization reasoning) | `gpt-5`, `gpt-5.1`, `gpt-5.3` |

The eval model runs once per task per candidate — it reads the agent's response and each criterion, then returns a binary score. The reflection model analyzes baseline results and generates improved instructions or skills. Because it reasons over the full dataset, a more capable reflection model typically produces better candidates.

```yaml
# spec.yaml
options:
  eval_model: gpt-4.1-mini
  reflection_model: gpt-5
```

> [!IMPORTANT]
> Both models are required. If `reflection_model` is not specified in your config, the optimization API returns an error.

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

Each criterion in the evaluation *dataset* is scored independently as a binary value (0 or 1). The evaluator model reads the agent's response and the criterion's instruction, then determines whether the response satisfies that criterion.

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

A pass rate below 100% means some tasks produced invalid responses. For example, the agent might have crashed, timed out, or returned empty. If a candidate has a lower pass rate than the baseline, it might have introduced instability.

### All scores are zero

If all candidates (including baseline) score 0.00, the likely cause is a missing *eval model*. The eval model is the model that scores agent responses against criteria. It must be deployed in your Foundry project.

```bash
azd ai agent optimize --eval-model gpt-4.1-mini
```

> [!IMPORTANT]
> If the eval model is not deployed, all scores are zero with no error message. Always verify that your eval model exists in the project.

## Limitations and availability

- The agent optimizer is available in all regions where [hosted agents are available](hosted-agents.md#region-availability).
- The agent optimizer is supported for hosted agents that use the [Responses protocol](hosted-agents.md#protocols-responses-and-invocations).

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Create a custom evaluation dataset](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions and skills](../how-to/optimize-agent-targets.md)
