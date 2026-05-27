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

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

The agent optimizer supports four optimization targets: **instruction tuning** (the default) rewrites your agent's system prompt, **skill discovery** generates reusable capabilities, **tool optimization** improves tool descriptions and parameters, and **model selection** evaluates across multiple model deployments. This guide covers all targets.

| Scenario | Recommended target |
| ---------- | ----------------------- |
| Improve overall response quality | Instruction tuning |
| Reduce hallucination | Instruction tuning |
| Add repeatable behaviors (escalation, debugging patterns) | Skill discovery |
| Agent needs structured procedures | Skill discovery |
| Find the best quality/cost model trade-off | Model selection |
| First optimization, not sure which to choose | Instruction tuning (default) |

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- The `azure.ai.agents` CLI extension installed (see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md))
- A model deployed for evaluation (for example, `gpt-4.1-mini`) and an optimization model from the [supported list](../concepts/agent-optimizer-overview.md#models) (for example, `gpt-5.1`)
- Your agent is [optimizer-ready](make-agent-optimizer-ready.md) (calls `load_config()`)

## Which agent gets optimized

The optimizer needs to know which deployed hosted agent to target. It resolves the agent name using the following priority order:

| Priority | Source | Example |
| -------- | ------ | ------- |
| 1 (highest) | `--agent` CLI flag | `azd ai agent optimize --agent my-support-agent` |
| 2 | `agent.name` field in `spec.yaml` | `agent:\n  name: my-support-agent` |
| 3 (default) | `name` field in `agent.yaml` | `name: my-support-agent` |

In most cases, you don't need to specify the agent name explicitly. The CLI reads it from your project's `agent.yaml` file. Use the `--agent` flag when you have multiple agents in your project or want to override the default:

```bash
azd ai agent optimize --agent my-support-agent --target instruction
```

> [!NOTE]
> The agent name must match a deployed hosted agent in your Foundry project. Run `azd ai agent invoke "test"` to verify your agent responds before starting optimization.

## Optimize instructions

The *instruction target* is the default optimization approach. It rewrites and refines your agent's system prompt to improve performance on your evaluation dataset.

### How it works

1. **Baseline evaluation.** Your agent is invoked with its current instructions against every task in the dataset. Each response is scored against the task's criteria.
1. **Instruction generation.** The optimizer analyzes the baseline scores and generates alternative system prompts. These alternatives are designed to improve weak areas while maintaining strong areas.
1. **Candidate evaluation.** Each candidate instruction set is injected into your agent through the `OPTIMIZATION_CANDIDATE_ID` environment variable and evaluated against the same dataset. The agent optimizer sets this variable automatically during evaluation.
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
  optimization_model: gpt-5.1
  target_attributes:
    - instruction
  max_iterations: 5
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

### Max iterations

The `max_iterations` option controls how many candidate instruction sets are generated. Each iteration produces one candidate.

| Max iterations | Candidates | Time | Best for |
| ---------------- | ----------- | ------ | ---------- |
| 4 (default) | 4 | 5 to 10 min | Quick experiments |
| 5 | 5 | 10 to 15 min | Good balance |
| 10 | 10 | 20 to 30 min | Thorough exploration |

Higher values explore more variations but take longer. The optimizer learns from earlier iterations, so later candidates tend to score higher.

> [!NOTE]
> Times are approximate for a dataset of 3 to 10 tasks. Larger datasets or slower eval models increase run duration.

### Eval model

The eval model scores agent responses against criteria. Any chat-completion model deployed in your Foundry project works.

```bash
azd ai agent optimize --eval-model gpt-4.1-mini
```

> [!IMPORTANT]
> If the eval model is not deployed, all scores are zero with no error message. Always verify your eval model exists in the project.

### Optimization model (reflection)

The optimization model (also called "reflection model") generates candidate configurations — improved instructions, skills, and tool descriptions. It analyzes baseline results and produces improved variants. It must be deployed in your Foundry project.

Supported models: `gpt-5`, `gpt-5.1`, `gpt-5.3`.

Specify the optimization model in your config file or via CLI:

```yaml
options:
  optimization_model: gpt-5.1
```

Or via CLI flag:

```bash
azd ai agent optimize --optimize-model gpt-5.1
```

> [!IMPORTANT]
> The `optimization_model` field is required. If it's not specified and `--optimize-model` is not passed, the optimization API returns an error.

For more details on how these models are used, see [Models](../concepts/agent-optimizer-overview.md#models).

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
  eval_model: gpt-4.1-mini
  optimization_model: gpt-5.1
  target_attributes:
    - skill
  max_iterations: 5
```

```bash
azd ai agent optimize --config spec.yaml
```

### Skill file downloads

For candidates that include skill files, the config loader can download them through the resolver API. Skills use the open [Agent Skills](https://agentskills.io) format and are stored in a local directory.

```python
from azure.ai.agentserver.optimization import load_config, load_skills_from_dir
from pathlib import Path

config = load_config()

if config.skills:
    print(f"Skills loaded from optimization config:")
    for skill in config.skills:
        print(f"  - {skill.name}: {skill.description}")
elif config.skills_dir:
    # Load skills from local directory
    skills = load_skills_from_dir(Path(config.skills_dir))
    config.skills.extend(skills)
    for skill in skills:
        print(f"  - {skill.name}: {skill.description}")
```

Learn more about the Agent Skills format at [agentskills.io](https://agentskills.io).

## Optimize model selection

The *model target* evaluates your agent across multiple model deployments to find the best quality/cost trade-off. Each model is scored against the same dataset, so you can compare results directly.

### Configure target models

Specify the models to evaluate in your spec.yaml:

```yaml
# spec.yaml
agent:
  name: my-agent

dataset_file: ./eval.jsonl

evaluators:
  - task_adherence

options:
  eval_model: gpt-4.1-mini
  optimization_model: gpt-5.1
  target_attributes:
    - model
  target_config:
    model:
      - gpt-4.1
      - gpt-4.1-mini
      - gpt-4o
  max_iterations: 5
```

Each model listed under `target_config.model` must be deployed in your Foundry project.

### Run model optimization

```bash
azd ai agent optimize --config spec.yaml
```

The optimizer evaluates your agent using each specified model deployment and ranks the results by score and token cost.

### Combine with other targets

You can optimize instructions, skills, and model selection in a single run:

```yaml
options:
  target_attributes:
    - instruction
    - skill
    - model
  target_config:
    model:
      - gpt-4.1
      - gpt-5
```

This produces candidates that combine improved instructions with different model options, giving you the full picture of what works best.

---

## Interpret results

After optimization completes, review the results table. For detailed scoring guidance, see [Understand optimization results](../concepts/agent-optimizer-overview.md#understand-optimization-results).

Key thresholds:

| Improvement | Interpretation |
| ------------- | --------------- |
| Less than 0.03 | Noise. Not meaningful. |
| 0.03 to 0.10 | Moderate. Worth deploying. |
| 0.10 to 0.20 | Significant improvement. |
| Greater than 0.20 | Major improvement. |

> [!TIP]
> To view optimization results in more detail, open the [Azure AI Foundry portal](https://ai.azure.com). Navigate to your project, select **Agents**, choose your agent, and then select the **Optimize** tab. The portal shows score comparisons, score-versus-token charts, and a **Deploy best candidate** button.

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
> Direct deploy updates the agent service without changing your local files. Use the `apply` → `deploy` workflow for production.

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
