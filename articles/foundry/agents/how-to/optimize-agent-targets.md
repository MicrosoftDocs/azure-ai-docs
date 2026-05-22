---
title: "Optimize agent instructions and skills in Foundry Agent Service (preview)"
description: "Run instruction tuning or skill discovery using the agent optimizer to automatically improve your hosted agent's performance in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Optimize agent instructions and skills (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The agent optimizer supports two optimization targets: **instruction tuning** (the default) rewrites your agent's system prompt, and **skill discovery** generates reusable capabilities. This guide covers both targets.

| Scenario | Recommended target |
| ---------- | ----------------------- |
| Improve overall response quality | Instruction tuning |
| Reduce hallucination | Instruction tuning |
| Add repeatable behaviors (escalation, debugging patterns) | Skill discovery |
| Agent needs structured procedures | Skill discovery |
| First optimization, not sure which to choose | Instruction tuning (default) |

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- The `azure.ai.agents` CLI extension installed (see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md))
- An eval model deployed in your Foundry project (defaults to `gpt-4.1-mini`)
- Your agent is [optimizer-ready](make-agent-optimizer-ready.md) (calls `load_config()`)

## Optimize instructions

The *instruction target* is the default optimization approach. It rewrites and refines your agent's system prompt to improve performance on your evaluation dataset.

### How it works

1. **Baseline evaluation.** Your agent is invoked with its current instructions against every task in the dataset. Each response is scored against the task's criteria.
1. **Instruction generation.** The optimizer analyzes the baseline scores and generates alternative system prompts. These alternatives are designed to improve weak areas while maintaining strong areas.
1. **Candidate evaluation.** Each candidate instruction set is injected into your agent through the `AGENT_OPTIMIZATION_CANDIDATE_ID` environment variable and evaluated against the same dataset. The agent optimizer sets this variable automatically during evaluation.
1. **Ranking.** Candidates are ranked by composite score. The best candidate is marked with ★.

### Run instruction optimization

```bash
# Default target is 'instruction' — these are equivalent:
azd ai agent optimize
azd ai agent optimize --target instruction
```

With a custom dataset:

```yaml
# spec.yaml
agent:
  name: my-agent

dataset_file: ./eval.jsonl

evaluators:
  - task_adherence

options:
  eval_model: gpt-4.1-mini
  strategies:
    - instruction
  budget: 5
```

```bash
azd ai agent optimize --config spec.yaml
```

### What gets changed

The optimizer rewrites the system prompt. Your code stays the same because `load_config()` returns the new instructions automatically. Common improvements include:

- Adding explicit constraints that the original prompt implied but did not state
- Restructuring instructions for clarity
- Adding output format specifications
- Strengthening safety and scope boundaries

### Example: Before and after

**Before** (your default instructions):

```
You are a helpful assistant.
```

**After** (optimized):

```
You are a helpful coding assistant. Follow these guidelines:
1. Always include working code examples
2. Explain your reasoning step by step
3. If a question is outside your expertise, say so clearly
4. Use markdown formatting for code blocks
5. Handle edge cases in code examples
```

### Budget

The *budget* option controls how many candidate instruction sets are generated. Each iteration produces one candidate.

| Budget | Candidates | Time | Best for |
| -------- | ----------- | ------ | ---------- |
| 3 (default) | 3 | 5 to 10 min | Quick experiments |
| 5 | 5 | 10 to 15 min | Good balance |
| 10 | 10 | 20 to 30 min | Thorough exploration |

Higher budgets explore more variations but take longer. The optimizer learns from earlier iterations, so later candidates tend to score higher.

> [!NOTE]
> Times are approximate for a dataset of 3 to 10 tasks. Larger datasets or slower eval models increase run duration.

### Eval model

The eval model scores agent responses against criteria. It must be deployed in your Foundry project.

```bash
azd ai agent optimize --eval-model gpt-4.1-mini
```

> [!IMPORTANT]
> If the eval model is not deployed, all scores are zero with no error message. Always verify your eval model exists in the project.

## Optimize with skill discovery

The *skill target* discovers reusable capabilities your agent should have. It generates skill definitions and appends them to the agent's instruction set.

### How it works

1. **Baseline evaluation.** Same as the instruction target. Your agent is evaluated against the dataset.
1. **Skill discovery.** The optimizer analyzes weak areas and generates skill definitions. A skill is a named capability with:
   - **Name**: For example, `"step_by_step_reasoning"`
   - **Description**: What the skill does and when to use it
   - **Body**: Implementation details or procedure
1. **Injection.** Discovered skills are appended to the agent's instructions through `compose_instructions()`, which creates a skill catalog the model can reference.

    ```python
    # compose_instructions() appends discovered skills to your prompt
    full_prompt = config.compose_instructions()
    # Returns: "You are a helpful assistant.\n\n## Available Skills\n- **step_by_step_reasoning**: ..."
    ```

1. **Evaluation.** The agent with skills is evaluated against the dataset.

### Run skill optimization

```bash
azd ai agent optimize --target skill
```

With a config file:

```yaml
# spec.yaml
agent:
  name: my-agent

dataset_file: ./eval.jsonl

evaluators:
  - task_adherence

options:
  strategies:
    - skill
  budget: 5
```

```bash
azd ai agent optimize --config spec.yaml
```

### Skill file downloads

For candidates that include skill files (implementation code), `load_config()` can download them through the resolver API. The skills are stored in a local directory. The default directory is `.agent_optimization_skills/`.

```python
config = load_config(
    default_instructions="You are a helpful assistant.",
    default_skills_dir="./my_skills",
)

if config.has_skills:
    print(f"Skills loaded from: {config.skills_dir}")
    for skill in config.skills:
        print(f"  - {skill.name}: {skill.description}")
```

## Interpret results

After optimization completes, review the results table. For detailed scoring guidance, see [Understand optimization results](../concepts/agent-optimizer-overview.md#understand-optimization-results).

Key thresholds:

| Improvement | Interpretation |
| ------------- | --------------- |
| Less than 0.03 | Noise. Not meaningful. |
| 0.03 to 0.10 | Moderate. Worth deploying. |
| 0.10 to 0.20 | Significant improvement. |
| Greater than 0.20 | Major improvement. |

## Deploy the winner

```bash
azd ai agent optimize deploy --candidate <candidate-id>
```

This command sets `OPTIMIZATION_CONFIG` in the agent's environment. On next startup, `load_config()` returns the optimized instructions.

If all candidates score lower than the baseline, do not deploy any candidate. The baseline configuration remains active.

## Troubleshooting

| Problem | Cause | Fix |
| --------- | ------- | ----- |
| All scores are 0.00 | Eval model not deployed | Deploy the eval model in your Foundry project, or use `--eval-model` to specify one that exists |
| `optimize` returns 403 | Subscription not on allowlist | Contact your Microsoft representative to request access |
| `"agent.yaml does not declare any protocols"` | Invalid `agent.yaml` format | Use flat format: `kind: hosted` at top level with `protocols:` list |
| Job stuck at "running" | Service issue | Cancel with `azd ai agent optimize cancel <id>` and retry |
| No candidate IDs in output | Job still running | Wait for completion or use `--watch` |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Create a custom evaluation dataset](create-optimizer-dataset.md)
- [Make your agent optimizer-ready](make-agent-optimizer-ready.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
