---
title: "Agent optimizer in Foundry Agent Service overview (preview)"
description: "Automatically improve hosted agents by evaluating behavior and generating better instructions, skills, tools, and model configurations using the agent optimizer in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: overview
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# What is the agent optimizer? (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer in Foundry Agent Service automatically improves your hosted agents by evaluating their behavior and generating better configurations. These configurations can include improved instructions, skills, tool descriptions, and model selection.

Building effective AI agents requires extensive prompt engineering. You deploy an agent with handcrafted instructions, test it against real scenarios, identify weaknesses, revise the prompt, and repeat. This loop is slow, subjective, and doesn't scale. The agent optimizer automates this cycle so you can focus on your agent's core logic.

## The optimization workflow

Optimizing an agent follows a repeatable path. Each step links to the article that covers it in detail:

1. **Prepare your agent.** Add the optimization package and a baseline configuration so the optimizer can read and improve your agent. See [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md).
1. **Create an evaluation dataset.** Define the tasks and criteria the optimizer scores against. See [Create an evaluation dataset and evaluators](../how-to/create-optimizer-dataset.md).
1. **Run the optimizer.** Start an optimization run and choose which targets and models to explore. See [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md).
1. **Review the results.** Compare candidate scores against your baseline and pick the best one. See [Understand optimization results](#understand-optimization-results).
1. **Apply and deploy.** Promote the winning candidate to your agent's configuration and redeploy. See [Deploy the winner](../how-to/optimize-agent-targets.md#deploy-the-winner).

To try the full workflow with a sample agent, start with the [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md).

## How the agent optimizer works

The agent optimizer runs a closed-loop evaluation and improvement cycle:

1. **Evaluate the baseline.** The optimizer invokes your agent against a dataset of tasks and scores each response against criteria you define or a built-in default set. The *baseline* is your agent's score before any changes.
1. **Generate candidates.** The optimizer produces alternative configurations called *candidates*—rewritten instructions or discovered skills—designed to improve scores.
1. **Evaluate candidates.** The optimizer tests each candidate against the same dataset.
1. **Rank and recommend.** The optimizer ranks results by composite *score*, a value between 0.0 and 1.0 that represents aggregate performance, and marks the best candidate with ★. You then apply and deploy the winner.

The entire process runs in the cloud and takes 5 to 20 minutes, depending on dataset size. After you make your agent [optimizer-ready](../how-to/make-agent-optimizer-ready.md), no further code changes are needed between runs: `load_config()` returns your baseline normally and supplies optimized configuration automatically during and after a run - no feature flags or conditional logic.

> [!WARNING]
> During optimization, the optimizer evaluates your agent by invoking it against every task in your dataset. If your agent calls external tools—such as APIs, databases, or third-party services—those calls execute during each evaluation run. To avoid unintended side effects (charges, state mutations, or rate limiting), consider using test endpoints or mocking tool implementations during optimization.

<!-- :::image type="content" source="media/agent-optimizer-architecture.svg" alt-text="Diagram showing how the agent optimizer interacts with your hosted agent. The agent loads configuration at startup, and the agent optimizer evaluates, generates candidates, and ranks them."::: -->

## Optimization targets

An optimization *target* is a specific aspect of your agent's configuration that the optimizer can improve. The optimizer runs all applicable targets in a single run and automatically activates each one based on your baseline configuration and `eval.yaml` settings.

| Target | What the optimizer improves | Activates when your baseline has |
| ------ | --------------------------- | -------------------------------- |
| **Instruction tuning** | Rewrites and refines the system prompt to score higher. The most common target. | An `instructions.md` file |
| **Skill improvement** | Refines the body of each reusable skill (in `SKILL.md`) while keeping skill descriptions unchanged. | A `skills/` directory |
| **Tool optimization** | Improves tool and parameter descriptions so the model calls tools more accurately. Doesn't change types, defaults, or required fields. | A `tools.json` file |
| **Model selection** | Evaluates your agent across multiple model deployments to find the best quality-to-cost trade-off. | `model_search_space` in `eval.yaml` |

To set up these baseline inputs, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md). To run and configure each target, see [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md).

## Models

The agent optimizer uses two models during an optimization run. Both must be deployed in your Foundry project.

| Model | Config key | CLI flag | Role | Supported models |
| ------- | ------------ | -------- | ------ | ------------------ |
| **Eval model** | `eval_model` | `--eval-model` | Scores agent responses against criteria in the dataset | Any chat-completion model (for example, `gpt-4.1-mini`) |
| **Optimization model** | `optimization_model` | `--optimize-model` | Generates candidate configurations (instructions, skills, tools, model selection) | `gpt-5`, `gpt-5.1`, `gpt-5.2`, `gpt-5.4`, `gpt-5.5`, `DeepSeek-V4-Pro`, `DeepSeek-V-3.2` |

The eval model runs once per task per candidate. It reads the agent's response and each criterion, then returns a binary score. The optimization model analyzes baseline results and generates improved candidates across the configured targets (instructions, skills, tools, and models). Because it reasons over the full dataset, a more capable optimization model typically produces better candidates.

You specify these models in `eval.yaml` or with CLI flags, and `optimization_model` is required. For configuration steps, see [Choose the eval and optimization models](../how-to/optimize-agent-targets.md#choose-the-eval-and-optimization-models).

## Understand optimization results

This section explains the results table, how the composite score is computed, and how to interpret improvements.

> [!TIP]
> You can also view optimization results in the [Foundry portal](https://ai.azure.com). Navigate to your project, select **Agents**, choose your agent, and then select the **Optimize** tab to see score comparisons, charts, and deployment options.

After an optimization run completes, you see a results table:

```
Results:
  Candidate              Score  Eval  Strategy
  ──────────────────── ───────  ────  ────────
  baseline                0.93  View
  candidate_1             0.90  View  skill_policy-reviewer
  candidate_2 ★           0.94  View  skill_policy-reviewer, tools
  candidate_3             0.94  View  skill_policy-reviewer, system_prompt, tools
  candidate_4             0.93  View  skill_policy-reviewer, tools

  Candidate IDs:
      baseline             cand_a8a951...
      candidate_1          cand_8d5c85...
    ★ candidate_2          cand_a0ea2e...
      candidate_3          cand_2ae7bb...
      candidate_4          cand_0f6485...

  Apply the best candidate locally, then deploy:
    azd ai agent optimize apply --candidate cand_a0ea2e...
    azd deploy
```

### Results table columns

| Column | Description |
| -------- | ------------- |
| **Candidate** | Name of the configuration. `baseline` is your current agent before optimization. |
| **Score** | Composite score across all tasks and criteria, ranging from 0.0 to 1.0. |
| **Eval** | Link to the evaluation job in the Foundry portal. |
| **Strategy** | Mutation targets included in the candidate, such as `skill_policy-reviewer, tools`. |

The ★ marks the candidate with the highest composite score. This is the recommended candidate to deploy.

### How scores are computed

Each evaluator in your dataset produces a raw score for the agent's response. The optimizer processes these scores to produce the composite score shown in results:

- **Rescale**: Each evaluator's raw score is rescaled to 0–1.
- **Flip if needed**: If an evaluator is configured so that *lower is better*, the score is flipped so that all evaluators use "higher is better" semantics.
- **Average**: The rescaled scores across all evaluators and tasks are averaged to produce the composite score.

**Composite score**: The average of all rescaled evaluator scores across all tasks.

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

## Limitations and availability

- The agent optimizer is available in all regions where [hosted agents are available](hosted-agents.md#region-availability), except Norway East.
- The agent optimizer is supported for hosted agents that use the [Responses protocol](hosted-agents.md#protocols-responses-invocations-and-invocations-websocket).


## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Create an evaluation dataset and evaluators](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
