---
title: "Create an evaluation dataset for the agent optimizer (preview)"
description: "Generate or manually define evaluation datasets used by the agent optimizer to evaluate and improve your hosted agent in Foundry Agent Service."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
---

# Create an evaluation dataset (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

[!INCLUDE [agent-optimizer-limited-preview](../../includes/agent-optimizer-limited-preview.md)]

The agent optimizer evaluates your agent against a *dataset* — a collection of tasks with evaluation criteria. You can generate a dataset automatically from the CLI or create one manually for full control.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with a deployed hosted agent
- The `azure.ai.agents` CLI extension installed (see [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md))

## Generate a dataset (recommended)

The fastest way to create an evaluation dataset is with `azd ai agent eval init`. This command generates a dataset and adaptive evaluators tuned to your agent's domain:

```bash
azd ai agent eval init
```

The interactive wizard auto-detects your agent from `azure.yaml` and prompts for a generation instruction describing what your agent does and what scenarios to test.

Example output:

```text
Detecting agent...
  Found: my-support-agent (hosted)

Generation prompt
  Describe what this agent does and what scenarios to test.
  > This agent handles customer support for electronics. Test returns, troubleshooting, and out-of-scope requests.

Generating dataset and evaluators...
  Dataset generation:    done  (registered: my-support-agent-eval-seed/v1)
  Evaluator generation:  done  (registered: my-support-agent-quality/v1)

Eval suite created
  Config:     eval.yaml
  Dataset:    .azure/.foundry/datasets/my-support-agent-eval-seed.v1.jsonl
  Evaluator:  .azure/.foundry/evaluators/my-support-agent-quality.v1.yaml

Review the generated assets, then run:
  azd ai agent eval run
```

### Non-interactive mode

For scripted workflows, pass the inputs directly:

```bash
azd ai agent eval init \
  --gen-instruction "Customer support agent. Test refund handling, troubleshooting, and out-of-scope deflection." \
  --eval-model gpt-4.1-mini \
  --max-samples 50
```

### Use your own data with generated evaluators

If you already have a golden dataset but want auto-generated evaluators:

```bash
azd ai agent eval init --dataset ./my-golden-dataset.jsonl
```

### Run optimization with the generated config

After `eval init` completes, `azd ai agent optimize` auto-detects the generated `eval.yaml`:

```bash
azd ai agent optimize
```

Or pass it explicitly:

```bash
azd ai agent optimize --config eval.yaml
```

For the full evaluation CLI workflow, see [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation).

## Create a custom dataset manually (advanced)

For full control over evaluation tasks and criteria, create a JSONL dataset by hand. This is useful when you need precise control over test scenarios or have production data to use directly.

By default, `azd ai agent optimize` uses a built-in dataset with 3 general coding tasks and 25 criteria. For meaningful optimization of your specific agent, create a custom *dataset* that reflects your agent's real-world use cases.

### Dataset format

Datasets use **JSONL** (JSON Lines) format. Each line is one JSON object that represents a single evaluation *task*. A task is an individual scenario in the dataset. It contains a prompt and evaluation criteria.

```jsonl
{"name": "task_1", "prompt": "Your prompt here", "criteria": [{"name": "criterion_name", "instruction": "What the evaluator checks for"}]}
{"name": "task_2", "prompt": "Another prompt", "criteria": [{"name": "check_1", "instruction": "..."}, {"name": "check_2", "instruction": "..."}]}
```

### Field reference

| Field | Required | Description |
| ------- | ---------- | ------------- |
| `name` | Yes | Unique task identifier (for example, `"greeting"`, `"math_test"`) |
| `prompt` | Yes | The message sent to the agent |
| `criteria` | Yes | Array of evaluation *criteria* — rules that define what "good" looks like for the task |
| `criteria[].name` | Yes | Short name for the criterion (for example, `"is_polite"`) |
| `criteria[].instruction` | Yes | What the *evaluator* checks. Be specific and testable. The built-in evaluator (`builtin.task_adherence`) scores each criterion independently as a binary value (0 or 1). |
| `groundTruth` | No | Expected answer (used by some evaluators for reference) |

### Example: Customer support agent

```jsonl
{"name": "refund_policy", "prompt": "What is your refund policy?", "criteria": [{"name": "mentions_30_days", "instruction": "Response must mention the 30-day refund window"}, {"name": "polite_tone", "instruction": "Response must be professional and empathetic"}]}
{"name": "order_status", "prompt": "Where is my order #12345?", "criteria": [{"name": "asks_for_details", "instruction": "Agent should ask for email or order details to look up the order"}, {"name": "no_hallucination", "instruction": "Agent must NOT make up a fake order status"}]}
{"name": "out_of_scope", "prompt": "Can you help me fix my car?", "criteria": [{"name": "polite_decline", "instruction": "Agent should politely explain this is outside its scope"}, {"name": "redirect", "instruction": "Agent should suggest contacting an appropriate service"}]}
```

### Example: Coding assistant

```jsonl
{"name": "python_function", "prompt": "Write a Python function to reverse a linked list", "criteria": [{"name": "correct_algorithm", "instruction": "The function must correctly reverse a singly linked list"}, {"name": "handles_empty", "instruction": "The function must handle an empty list without errors"}, {"name": "includes_docstring", "instruction": "The function should include a descriptive docstring"}]}
{"name": "explain_concept", "prompt": "Explain what a closure is in JavaScript", "criteria": [{"name": "accurate_definition", "instruction": "Must correctly define a closure as a function that captures variables from its enclosing scope"}, {"name": "includes_example", "instruction": "Must include at least one working code example"}]}
```

### Use a custom dataset

Reference your dataset in a YAML config file:

```yaml
# eval.yaml
agent:
  name: my-agent

dataset_file: ./my_eval_dataset.jsonl

evaluators:
  - builtin.task_adherence

options:
  eval_model: gpt-4.1-mini
  optimization_model: gpt-5.1
  max_iterations: 10
```

Then run:

```bash
azd ai agent optimize --config eval.yaml
```

Before you run the command, validate the JSONL syntax:

```bash
python -c "import json; [json.loads(l) for l in open('my_eval_dataset.jsonl')]"
```

## Tips for writing good datasets

### Be specific in criteria

Bad:

```json
{"name": "good_answer", "instruction": "The response should be good"}
```

Good:

```json
{"name": "mentions_30_days", "instruction": "Response must explicitly mention the 30-day refund window"}
```

Specific criteria give the evaluator a clear, binary signal. Vague criteria lead to inconsistent scoring.

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

Each task can have multiple criteria. A dataset with 5 tasks × 4 criteria each = 20 evaluation signals.

### Write prompts like real users

Use actual messages from your users if possible. Real prompts capture the vocabulary and context that your agent faces in production.

### Criteria are scored independently

Each criterion gets a binary score (0 or 1). The task score is the average of its criteria scores. The overall score is the average across all tasks. This means:

- A task with 4 criteria where 3 pass scores 0.75
- An agent that passes all criteria on 2 of 3 tasks scores 0.67

### Ground truth is optional

The `groundTruth` field provides a reference answer for evaluators that support it. This field isn't required. The `builtin.task_adherence` evaluator works entirely from criteria instructions.

```jsonl
{"name": "geography_fact", "prompt": "What is the largest city in France by population?", "groundTruth": "Paris", "criteria": [{"name": "correct_answer", "instruction": "Response must state that Paris is the largest city in France by population"}]}
```

## Troubleshooting

| Problem | Cause | Fix |
| --------- | ------- | ----- |
| `dataset_file not found` | Wrong path in `eval.yaml` | Use a path relative to the config file location |
| `invalid JSON on line N` | Malformed JSONL | Validate that each line is valid JSON. Check for trailing commas. |
| Scores are inconsistent between runs | Vague criteria | Make criteria specific and binary-testable |

## Related content

- [Run agent evaluations with the azd CLI](/azure/foundry/observability/how-to/azure-developer-cli-evaluation)
- [Agent optimizer overview](../concepts/agent-optimizer-overview.md)
- [Optimize agent instructions, skills, tools, and models](optimize-agent-targets.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
