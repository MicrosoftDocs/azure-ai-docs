---
title: "Agent optimization overview for Foundry Agent Service (preview)"
description: "Automatically improve hosted agents by evaluating behavior and generating better system instructions and skills using the Foundry Agent Optimization Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: overview
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# What is agent optimization? (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Foundry Agent Optimization Service automatically improves your hosted agents by evaluating their behavior and generating better configurations. These configurations primarily include improved system instructions and discovered skills.

Building effective AI agents requires extensive prompt engineering. You deploy an agent with hand-crafted instructions, test it against real scenarios, identify weaknesses, revise the prompt, and repeat. This loop is slow, subjective, and does not scale. Agent optimization automates this cycle so you can focus on your agent's core logic.

## How optimization works

The optimization service runs a closed-loop evaluation and improvement cycle:

1. **Evaluate the baseline.** Your agent is invoked against a dataset of tasks. Each response is scored against criteria you define or a built-in default set. The *baseline* is your agent's score before any changes.
1. **Generate candidates.** The service produces alternative configurations called *candidates*, such as rewritten instructions or discovered skills, that are designed to improve scores.
1. **Evaluate candidates.** Each candidate is tested against the same dataset.
1. **Rank and recommend.** Results are ranked by composite *score*, a value between 0.0 and 1.0 that represents aggregate performance. The best candidate is marked with ★.
1. **Deploy the winner.** A single command promotes the winning candidate and saves its configuration to your agent's environment.

The entire process runs in the cloud. Start it with `azd ai agent optimize` (requires the [azd CLI extension](../quickstarts/quickstart-optimize-hosted-agent.md#install-the-cli-extension)). The run takes 5 to 20 minutes depending on dataset size.

```
┌─────────────────────────────────────────────┐
│  Your Agent (Hosted in Microsoft Foundry)   │
│                                             │
│  main.py                                    │
│    └─ load_config()  ←─ reads optimized     │
│         │               config at startup   │
│         ▼                                   │
│  agent_optimization/                        │
│    └─ Resolves: env var → API → defaults    │
└─────────────────────────────────────────────┘
         ▲                          │
         │                          │ Invoked during eval
         │                          ▼
┌────────┴──────────────────────────────────┐
│  Optimization Service                     │
│                                           │
│  1. Evaluate baseline                     │
│  2. Generate candidate configs            │
│  3. Evaluate candidates                   │
│  4. Rank by score                         │
└───────────────────────────────────────────┘
```

## Optimization strategies

### Instruction tuning (default)

The *instruction strategy* rewrites and refines your agent's system prompt. It analyzes baseline performance and generates prompt variations that score higher.

**When to use:** Most agents. This is the default and works well for improving response quality, adherence to task requirements, and reducing hallucination.

```bash
azd ai agent optimize --strategy instruction
```

### Skill discovery

The *skill strategy* discovers reusable capabilities your agent should have. It generates *skill* definitions that include a name, description, and implementation body. The service appends these definitions to the agent's instruction set.

**When to use:** Agents that need structured, repeatable behaviors. For example, a support agent that should always follow a specific escalation procedure, or a coding agent that should use particular debugging patterns.

```bash
azd ai agent optimize --strategy skill
```

## Config resolution

When your agent starts, the `load_config()` function checks three sources in order:

| Priority | Source | When it's used |
| ---------- | -------- | ---------------- |
| 1 | `AGENT_OPTIMIZATION_CANDIDATE_ID` environment variable, resolved through the API | During optimization evaluation |
| 2 | `AGENT_OPTIMIZATION_CONFIG` or `OPTIMIZATION_CONFIG` environment variable (inline JSON) | After deploying a candidate |
| 3 | Your defaults in code | Normal operation (no optimization) |

Your agent always works with or without optimization. No feature flags or conditional logic are required. Call `load_config()` and use the values it returns. For implementation details, see [Make your agent optimization-ready](../how-to/make-agent-optimization-ready.md).

## What gets optimized

| Field | Description | Strategy |
| ------- | ------------- | ---------- |
| `instructions` | System prompt and instructions | instruction, skill |
| `skills` | Discovered skill catalog | skill |
| `model` | Model deployment name | (future) |
| `temperature` | Sampling temperature | (future) |

## Understand optimization results

This section describes the results table structure, how scores are computed, what score improvements mean, and how to diagnose common issues.

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

- Agent optimization is in **private preview**. Your Azure subscription must be on the allowlist. Contact your Microsoft representative to request access.
- The service is available in **North Central US** only. Other regions deploy the agent but return a 404 error for optimization commands.
- Optimization is supported for hosted agents in Foundry Agent Service.
- Optimization runs consume eval model tokens in your Foundry project.

## Related content

- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Make your agent optimization-ready](../how-to/make-agent-optimization-ready.md)
- [Create a custom evaluation dataset](../how-to/create-optimization-dataset.md)
- [Optimize agent instructions and skills](../how-to/optimize-agent-strategies.md)
