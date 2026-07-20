---
title: "Create an evaluation dataset and evaluators for the agent optimizer (preview)"
description: "Generate or manually define evaluation datasets and evaluators used by the agent optimizer to evaluate and improve your hosted agent in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Create an evaluation dataset and evaluators (preview)

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer evaluates your agent against a *dataset* - a collection of tasks - scored by *evaluators*. You can generate both automatically from the CLI or create a dataset manually for full control.

Both parts are essential to good optimization: the dataset defines *what* to test, and the evaluators define *how* to judge each response. Weak evaluators produce noisy scores that lead to poor optimization, so invest in strong evaluators as much as representative tasks.

Creating these assets is the second step in the [optimization workflow](../concepts/agent-optimizer-overview.md#the-optimization-workflow), after you [make your agent optimizer-ready](make-agent-optimizer-ready.md). The optimizer uses them to score your baseline and rank candidates.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- The `azure.ai.agents` CLI extension installed (see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md))

## Generate a dataset and evaluators (recommended)

The fastest way to create evaluation assets is with `azd ai agent eval generate`. The command auto-detects your agent and generates everything the optimizer needs:

```bash
azd ai agent eval generate
```

By default, it generates:

- A **seed dataset** of tasks tuned to your agent's domain.
- **Evaluators** that score responses - a built-in evaluator (such as `builtin.task_adherence`) plus a custom **rubric evaluator** tailored to your agent.
- A runnable **`eval.yaml`** that wires them together.

For the interactive wizard, non-interactive flags, and details about the generated artifacts, see [Initialize evaluation assets](../../observability/how-to/azure-developer-cli-evaluation.md#initialize-evaluation-assets).

After generation, `azd ai agent optimize` auto-detects `eval.yaml`:

```bash
azd ai agent optimize
```

To customize the generated assets, see [Customize evaluators](#customize-evaluators-advanced) and [Create a custom dataset](#create-a-custom-dataset-advanced). To change run options, edit `eval.yaml`; see [Configure the optimization run](optimize-agent-targets.md#configure-the-optimization-run).

## Customize evaluators (advanced)

Evaluators score each agent response. The optimizer supports two kinds:

- **Built-in evaluators**, such as `builtin.task_adherence`, which scores each task-level criterion as pass or fail.
- **Custom rubric evaluators**, which score responses across several quality dimensions tuned to your agent. `azd ai agent eval generate` creates one automatically as an editable `rubric_dimensions.json` file.

For most agents, the generated rubric evaluator gives the most meaningful scores because it's tailored to your domain. Edit the generated `rubric_dimensions.json` to refine dimensions, then run `azd ai agent eval update` to register the changes as a new version. For details on generating, editing, and versioning evaluators, see [Initialize evaluation assets](../../observability/how-to/azure-developer-cli-evaluation.md#initialize-evaluation-assets).

To wire evaluators into your run configuration, see [Configure the optimization run](optimize-agent-targets.md#configure-the-optimization-run).

## Create a custom dataset (advanced)

Create a custom dataset when you need precise control over test scenarios or have production data to use directly. The recommended approach is to iterate on top of the seed dataset that `azd ai agent eval generate` produces—refine it into a local dataset, or point to another dataset already registered in your Foundry project.

### Choose a dataset source

A dataset can come from either of two sources:

- **Foundry dataset** — a dataset already registered in your Foundry project. Reference it in `eval.yaml` by `name` and `version`.
- **Local dataset** — a JSONL file you author and keep in your project. Reference it in `eval.yaml` by `local_uri`.

Both sources use the same task schema described in the next section. For the `eval.yaml` wiring, see [Configure the optimization run](optimize-agent-targets.md#configure-the-optimization-run).

### Dataset schema

A dataset uses **JSONL** (JSON Lines) format. Each line is one JSON object that represents a single evaluation *task*—an individual scenario. A task has a prompt (`query`) and, optionally, task-level `criteria`.

```jsonl
{"name": "task_1", "query": "Your prompt here"}
{"name": "task_2", "query": "Another prompt", "ground_truth": "Expected answer"}
```

| Field | Required | Description |
| ------- | ---------- | ------------- |
| `name` | Yes | Unique task identifier (for example, `"greeting"`, `"math_test"`). |
| `query` | Yes | The message sent to the agent. |
| `ground_truth` | No | Expected answer, used by evaluators that support a reference. |
| `criteria` | No | Optional task-level checks. See [Add task-level criteria](#add-task-level-criteria). |

When you use a local dataset, validate the JSONL syntax before you run optimization:

```bash
python -c "import json; [json.loads(l) for l in open('eval.jsonl')]"
```

### Add task-level criteria

Criteria are optional. The [evaluators](#customize-evaluators-advanced) you configure in `eval.yaml` apply to every task in the dataset. Add per-task `criteria` only when a specific task needs checks beyond those shared evaluators. When present, a task's `criteria` are scored and aggregated together with the shared evaluators to produce the task's overall score.

| Field | Required | Description |
| ------- | ---------- | ------------- |
| `criteria[].name` | Yes | Short name for the criterion (for example, `"is_polite"`). |
| `criteria[].instruction` | Yes | What the evaluator checks. Be specific and testable. |

The following customer-support dataset shows tasks with task-level criteria:

```jsonl
{"name": "refund_policy", "query": "What is your refund policy?", "criteria": [{"name": "mentions_30_days", "instruction": "Response must mention the 30-day refund window"}, {"name": "polite_tone", "instruction": "Response must be professional and empathetic"}]}
{"name": "order_status", "query": "Where is my order #12345?", "criteria": [{"name": "asks_for_details", "instruction": "Agent should ask for email or order details to look up the order"}, {"name": "no_hallucination", "instruction": "Agent must NOT make up a fake order status"}]}
{"name": "out_of_scope", "query": "Can you help me fix my car?", "criteria": [{"name": "polite_decline", "instruction": "Agent should politely explain this is outside its scope"}, {"name": "redirect", "instruction": "Agent should suggest contacting an appropriate service"}]}
```

## Tips for writing good datasets

### Include edge cases

Test beyond the happy path. Include:

- **Out-of-scope requests** — Inputs your agent should decline or redirect
- **Ambiguous queries** — Tasks where the agent should ask for clarification
- **Adversarial inputs** — Attempts to trick the agent into bad behavior
- **Multi-step tasks** — Complex requests that require structured reasoning

### Size guidelines

| Dataset size | Trade-off |
| ------------- | ----------- |
| 3–5 tasks | Quick iteration, limited signal |
| 5–10 tasks | Good balance of speed and coverage |
| 10–20 tasks | Comprehensive evaluation, longer runs |
| 20+ tasks | Thorough but slow — consider for final validation |

Larger datasets give broader coverage but take longer to evaluate.

### Provide ground truth when useful

The `ground_truth` field gives evaluators a reference answer to compare against. It's not required - evaluators can also judge responses from their instructions and any task-level criteria alone.

```jsonl
{"name": "geography_fact", "query": "What is the largest city in France by population?", "ground_truth": "Paris", "criteria": [{"name": "correct_answer", "instruction": "Response must state that Paris is the largest city in France by population"}]}
```

### Write prompts like real users

Use actual messages from your users if possible. Real prompts capture the vocabulary and context that your agent faces in production, which also helps you write realistic task-level criteria.

### Be specific in criteria

Vague criteria lead to inconsistent scoring. Make each criterion specific and testable.

Bad:

```json
{"name": "good_answer", "instruction": "The response should be good"}
```

Good:

```json
{"name": "mentions_30_days", "instruction": "Response must explicitly mention the 30-day refund window"}
```

## Troubleshooting

| Problem | Cause | Fix |
| --------- | ------- | ----- |
| `dataset not found` | Wrong path in `eval.yaml` | For `dataset.local_uri`, use a path relative to the config file location. For a Foundry dataset, verify `dataset.name` and `dataset.version`. |
| `invalid JSON on line N` | Malformed JSONL | Validate that each line is valid JSON. Check for trailing commas. |
| Scores are inconsistent between runs | Vague criteria | Make criteria specific and testable. |

## Related content

- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Make your agent optimizer-ready](make-agent-optimizer-ready.md)
- [Optimize agent instructions, skills, tools, and models](optimize-agent-targets.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
- [Run agent evaluations with the azd CLI](../../observability/how-to/azure-developer-cli-evaluation.md)
