---
title: "Agent optimizer in Foundry Agent Service overview (preview)"
description: "Improve prompt and hosted agents by evaluating behavior and generating better instructions, skills, tools, and model configurations."
author: aahill
ms.author: aahi
ms.date: 08/07/2026
ms.topic: overview
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions, doc-kit-assisted
ai-usage: ai-assisted
---

# What is the agent optimizer? (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer in Foundry Agent Service automatically improves prompt agents and hosted agents by evaluating their behavior and generating better configurations. Depending on the agent type, these configurations can include improved instructions, skills, tool descriptions, and model selection.

Building effective AI agents requires extensive prompt engineering. You deploy an agent with handcrafted instructions, test it against real scenarios, identify weaknesses, revise the prompt, and repeat. This loop is slow, subjective, and doesn't scale. The agent optimizer automates this cycle so you can focus on your agent's core logic.

## Supported agent types

The optimizer uses the same evaluation-driven improvement loop for both agent types, but the setup, optimization targets, and deployment experience differ.

| Agent type | What the optimizer can improve | How you start a run |
| --- | --- | --- |
| **Prompt agent** | Instructions, function-calling tool descriptions, and model selection | Use the optimization wizard in the Foundry portal. No code changes are required. |
| **Hosted agent** | Instructions, skills, function-calling tool descriptions, and model selection | Use Foundry Toolkit, which scaffolds optimization support automatically, or make the agent optimizer-ready and use the Azure Developer CLI. |

### Prompt agents

For a prompt agent, the optimizer evaluates a selected agent version and generates alternative instructions. It can also improve descriptions for function-calling tools and compare the prompt across multiple candidate model deployments.

Prompt-agent function-calling tools run on the client side. The optimizer can improve the tool and parameter descriptions that guide the model's function calls, but it can't evaluate the tool execution during tool-description optimization.

Start the optimization wizard from the agent's **Optimize** tab in the Foundry portal. The wizard guides you through selecting the agent version, dataset, evaluation criteria, and optimization models before you submit the run. You can generate a dataset from agent traces, select an existing Foundry dataset, or upload a dataset in the wizard.

When the run finishes, compare score changes, review the before-and-after prompt, and inspect per-evaluator results. You can then promote a selected candidate to a new prompt-agent version from the optimization run.

For the end-to-end portal experience, see [Quickstart: Optimize a prompt agent](../quickstarts/quickstart-optimize-prompt-agent.md).

### Hosted agents

For a hosted agent, the optimizer improves the configuration that your code loads at runtime. The agent needs the optimization package and a baseline configuration that exposes the instructions and, optionally, skills and function-calling tool definitions. Foundry Toolkit can automatically scaffold this integration. For the Azure Developer CLI workflow, add the integration before you run the optimizer. The optimizer can then generate and evaluate candidate configurations without changing your agent's core logic.

Hosted-agent optimization supports local JSONL datasets and datasets registered in your Foundry project, including evaluation datasets generated from traces. After a run, apply the selected candidate to your local configuration, review the changes, and redeploy the agent.

For the end-to-end hosted-agent experience, see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md).

## The optimization workflow

Both agent types follow the same high-level path:

1. **Select the agent baseline.** Choose the prompt-agent version or hosted-agent configuration that you compare candidates against.
1. **Select an evaluation dataset.** Use representative tasks from an existing or uploaded dataset. You can also use a registered dataset generated from agent traces.
1. **Select evaluation criteria.** Choose built-in or custom evaluators that measure the behaviors you want to improve.
1. **Run the optimizer.** Choose the available optimization targets and models, and then generate and evaluate candidates. For prompt agents, review the [cost estimate](agent-optimizer-costs.md#pre-run-cost-estimate-for-prompt-agents) in the portal before you submit the run.
1. **Review the results.** Compare candidate scores against your baseline, and then pick the best candidate. When available, review the [post-run measured token usage](agent-optimizer-costs.md#post-run-measured-token-usage). See [Understand optimization results](#understand-optimization-results).
1. **Apply the selected candidate.** Promote a prompt-agent candidate to a new agent version, or apply the hosted-agent configuration and redeploy.

Hosted agents require optimizer-ready code integration. Foundry Toolkit automatically scaffolds this integration when you start an optimization. For the Azure Developer CLI workflow, add the optimization package and a baseline configuration before you start. See [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md). Prompt agents don't require this code integration.

## How the agent optimizer works

The agent optimizer runs a closed-loop evaluation and improvement cycle:

1. **Evaluate the baseline.** The optimizer invokes your agent against a dataset of tasks and scores each response against criteria you define or a built-in default set. The *baseline* is your agent's score before any changes.
1. **Generate candidates.** The optimizer produces alternative configurations called *candidates*, such as rewritten instructions, discovered skills, improved tool descriptions, or different model selections. Available candidate types depend on the agent type.
1. **Evaluate candidates.** The optimizer tests each candidate against the same dataset.
1. **Rank and recommend.** The optimizer ranks results by composite *score*, a value between 0.0 and 1.0 that represents aggregate performance, and marks the best candidate with ★. You then apply and deploy the winner.

The entire process runs in the cloud. Run time depends on the dataset size, the number of candidates, and the selected models.

For hosted agents, after you make your agent [optimizer-ready](../how-to/make-agent-optimizer-ready.md), no further code changes are needed between runs. `load_config()` returns your baseline normally and supplies optimized configuration during a run without feature flags or conditional logic.

> [!WARNING]
> During optimization, the optimizer evaluates your agent by invoking it against every task in your dataset. If your agent calls external tools—such as APIs, databases, or third-party services—those calls execute during each evaluation run. To avoid unintended side effects (charges, state mutations, or rate limiting), consider using test endpoints or mocking tool implementations during optimization.

<!-- :::image type="content" source="media/agent-optimizer-architecture.svg" alt-text="Diagram showing how the agent optimizer evaluates an agent baseline, generates candidates, and ranks them."::: -->

## Optimization targets

An optimization *target* is a specific aspect of your agent's configuration that the optimizer can improve. Available targets depend on the agent type. For hosted agents, the optimizer automatically activates applicable targets from the baseline configuration and `eval.yaml` settings.

| Target | What the optimizer improves | Prompt agent | Hosted agent |
| ------ | --------------------------- | ------------ | ------------ |
| **Instruction tuning** | Rewrites and refines the system prompt to score higher. | Uses the selected prompt-agent version as the baseline. | Activates when the baseline has an `instructions.md` file. |
| **Skill improvement** | Refines the body of each reusable skill while keeping its purpose intact. | Not supported. | Activates when the baseline has a `skills/` directory with `SKILL.md` files. |
| **Tool optimization** | Improves function-calling tool and parameter descriptions so the model calls tools more accurately. It doesn't change types, defaults, or required fields. | Available for function-calling tools. Because the client executes these tools, tool execution isn't evaluated during optimization. | Activates when the baseline has a `tools.json` file. Only function-calling tools are supported. |
| **Model selection** | Evaluates the agent across multiple model deployments to find the best quality-to-cost trade-off. | Select candidate models in the optimization wizard. | Add candidate deployments to `model_search_space` in `eval.yaml`. |

For hosted-agent baseline inputs, see [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md). To run and configure hosted-agent targets, see [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md).

## Models

The agent optimizer uses two models during an optimization run. Both must be deployed in your Foundry project.

| Model | Hosted-agent config key | Hosted-agent CLI flag | Role | Supported models |
| ------- | ------------ | -------- | ------ | ------------------ |
| **Eval model** | `eval_model` | `--eval-model` | Scores agent responses against criteria in the dataset | Any chat-completion model (for example, `gpt-4.1-mini`) |
| **Optimization model** | `optimization_model` | `--optimize-model` | Generates candidate configurations (instructions, skills, tools, model selection) | `gpt-5`, `gpt-5.1`, `gpt-5.2`, `gpt-5.4`, `gpt-5.5`, `DeepSeek-V4-Pro`, `DeepSeek-V-3.2` |

The eval model runs once for each evaluator, task, and candidate evaluation. It
reads the agent's response and each criterion, then returns a binary score. The
optimization model analyzes baseline results and generates improved candidates
across the configured targets, including instructions, skills, tools, and
models. Because it reasons over the full dataset, a more capable optimization
model typically produces better candidates.

For prompt agents, select the eval model and candidate models in the optimization wizard. For hosted agents, specify the models in `eval.yaml` or with CLI flags. The `optimization_model` setting is required for hosted-agent runs. For configuration steps, see [Choose the eval and optimization models](../how-to/optimize-agent-targets.md#choose-the-eval-and-optimization-models).

## Understand optimization results

This section explains the results table, how the composite score is computed, and how to interpret improvements.

> [!TIP]
> View optimization results in the [Foundry portal](https://ai.azure.com). Navigate to your project, select **Agents**, choose your agent, and then select the **Optimize** tab to see score comparisons, prompt or configuration changes, and evaluator details.

For prompt agents, a completed run shows the baseline and candidate scores, a before-and-after prompt, model, and tools description comparison, and per-evaluator scores.

For hosted agents, the CLI also displays a results table:

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

For details about the pre-run cost range and post-run measured usage, see
[Agent optimizer cost estimates and token usage](agent-optimizer-costs.md).

## Limitations and availability

- The agent optimizer supports prompt agents and hosted agents during preview.
- Prompt-agent optimization runs start in the Foundry portal. You can promote a selected candidate to a new agent version from the completed run.
- Hosted-agent optimization is available in all regions where [hosted agents are available](hosted-agents.md#region-availability), except Norway East.
- Hosted-agent optimization requires the [Responses protocol](hosted-agents.md#protocols-responses-invocations-and-invocations-websocket).

## Related content

- [Quickstart: Create a prompt agent](../quickstarts/prompt-agent.md)
- [Quickstart: Optimize a prompt agent](../quickstarts/quickstart-optimize-prompt-agent.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Agent optimizer cost estimates and token usage](agent-optimizer-costs.md)
- [Make your agent optimizer-ready](../how-to/make-agent-optimizer-ready.md)
- [Create an evaluation dataset and evaluators](../how-to/create-optimizer-dataset.md)
- [Optimize agent instructions, skills, tools, and models](../how-to/optimize-agent-targets.md)
- [Convert agent traces into evaluation datasets](../../observability/how-to/traces-to-dataset.md)
- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
