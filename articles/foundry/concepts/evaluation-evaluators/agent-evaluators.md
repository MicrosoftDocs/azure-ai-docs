---
title: "Agent Evaluators for Generative AI"
description: "Learn how to evaluate Azure AI agents using intent resolution, tool call accuracy, and task adherence evaluators."
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 09/30/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
---

# Agent evaluators

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

AI agents are powerful productivity assistants that can create workflows for business needs. However, observability can be a challenge due to their complex interaction patterns. Agent evaluators provide systematic observability into agentic workflows by measuring quality, safety, and performance.

An agent workflow typically involves reasoning through user intents, calling relevant tools, and using tool results to complete tasks like updating a database or drafting a report. To build production-ready agentic applications, you need to evaluate not just the final output, but also the quality and efficiency of each step in the workflow.

Foundry provides built-in agent evaluators that function like unit tests for agentic systems—they take agent messages as input and output binary Pass/Fail scores (or scaled scores converted to binary scores based on thresholds). These evaluators support two best practices for agent evaluation:

- System evaluation - to examine the end-to-end outcomes of the agentic system.
- Process evaluation - to verify the step-by-step execution to achieve the outcomes.

| Evaluator | Best practice | Use when | Purpose | Output |
|--|--|--|--|--|
| Task Completion (preview) | System evaluation | Assessing end-to-end task success in workflow automation, goal-oriented AI interactions, or any scenario where full task completion is critical | Measures if the agent completed the requested task with a usable deliverable that meets all user requirements | Binary: Pass/Fail |
| Customer Satisfaction (preview) | System evaluation | Measuring overall user satisfaction across a conversation, detecting user frustration | Measures holistic user satisfaction across six dimensions: helpfulness, completeness, clarity, tone, resolution, and adaptability | 1-5 Likert scale |
| Task Adherence (preview) | System evaluation | Ensuring agents follow system instructions, validating compliance in regulated environments | Measures if the agent's actions adhere to its assigned tasks according to rules, procedures, and policy constraints, based on its system message and prior steps | Binary: Pass/Fail |
| Task Navigation Efficiency | System evaluation | Optimizing agent workflows, reducing unnecessary steps, validating against known optimal paths (requires ground truth) | Measures whether the agent made tool calls efficiently to complete a task by comparing them to expected tool sequences | Binary: Pass/Fail |
| Intent Resolution (preview) | System evaluation | Customer support scenarios, conversational AI, FAQ systems where understanding user intent is essential | Measures whether the agent correctly identifies the user's intent | Binary: Pass/Fail based on threshold (1-5 scale) |
| Tool Call Accuracy | Process evaluation | Overall tool call quality assessment in agent systems with tool integration, API interactions to complete its tasks | Measures whether the agent made the right tool calls with correct parameters to complete its task | Binary: Pass/Fail based on threshold (1-5 scale) |
| Tool Selection | Process evaluation | Validating tool choice quality in orchestration platforms, ensuring efficient tool usage without redundancy | Measures whether the agent selected the correct tools without selecting unnecessary ones | Binary: Pass/Fail |
| Tool Input Accuracy | Process evaluation | Strict validation of tool parameters in production environments, API integration tests, critical workflows requiring 100% parameter correctness | Measures if all tool call parameters are correct across six strict criteria: groundedness, type compliance, format compliance, required parameters, no unexpected parameters, and value appropriateness | Binary: Pass/Fail |
| Tool Output Utilization | Process evaluation | Validating correct use of API responses, database query results, search outputs in agent reasoning and responses | Measures if the agent correctly understood and used tool call results contextually in its reasoning and final response | Binary: Pass/Fail |
| Tool Call Success | Process evaluation | Monitoring tool reliability, detecting API failures, timeout issues, or technical errors in tool execution | Measures if tool calls succeeded or resulted in technical errors or exceptions | Binary: Pass/Fail |
| Quality Grader (deprecated) | Quality evaluation | Reviewing existing Quality Grader configurations | Previously enabled quality evaluation across multiple dimensions in a single evaluator instead of running individual evaluators separately. It can no longer be run in an evaluation. | Not available |
| Output Quality (preview) | System and quality evaluation | Assessing response quality and task outcomes across several dimensions while reducing evaluation cost and latency | Batches Fluency, Coherence, Intent Resolution, Task Adherence, Groundedness, and Task Completion into one LLM judge call | Composite: component scores with Pass/Fail |
| Tool Use Quality (preview) | Process evaluation | Assessing the complete tool-use process while reducing evaluation cost and latency | Batches Tool Call Accuracy, Tool Call Success, Tool Input Accuracy, Tool Output Utilization, and Tool Selection into one LLM judge call | Composite: component scores with Pass/Fail |

## System evaluation

System evaluation examines the quality of the final outcome of your agentic workflow. These evaluators are applicable to single agents and, in multi-agent systems, to the main orchestrator or the final agent responsible for task completion:

- Task Completion - Did the agent fully complete the requested task?
- Customer Satisfaction - How satisfied would a user be with the agent's performance?
- Task Adherence - Did the agent follow the rules and constraints in its instructions?
- Task Navigation Efficiency - Did the agent perform the expected steps efficiently?
- Intent Resolution - Did the agent correctly identify and address user intentions?

Specifically, for textual outputs from agents, you can also apply RAG quality evaluators such as `Relevance` and `Groundedness` that take agentic inputs to assess the final response quality.

Examples:

- [Task completion (preview) sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_completion.py)
- [Task adherence sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_adherence.py)
- [Task navigation efficiency sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_navigation_efficiency.py)
- [Intent resolution sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_intent_resolution.py)

## Process evaluation

Process evaluation examines the quality and efficiency of each step in your agentic workflow. These evaluators focus on the tool calls executed in a system to complete tasks:

- Tool Call Accuracy - Did the agent make the right tool calls with correct parameters without redundancy?
- Tool Selection - Did the agent select the correct and necessary tools?
- Tool Input Accuracy - Did the agent provide correct parameters for tool calls?
- Tool Output Utilization - Did the agent correctly use tool call results in its reasoning and final response?
- Tool Call Success - Did the tool calls succeed without technical errors?

Examples:

- [Tool call accuracy sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_call_accuracy.py)
- [Tool selection sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_selection.py)
- [Tool input accuracy sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_input_accuracy.py)
- [Tool output utilization sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_output_utilization.py)
- [Tool call success sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_call_success.py)

## Quality evaluation (deprecated)

> [!IMPORTANT]
> Quality Grader is deprecated and can no longer be run in an evaluation.

Quality Grader assessed the overall quality of an AI assistant's response at the turn level. It examined multiple dimensions of response quality:

- **Relevance** - Is the response relevant to the user's query?
- **Abstention** - Does the agent appropriately abstain when it cannot or should not answer?
- **Answer completeness** - Does the response fully address the user's question?

When context was provided, Quality Grader also evaluated:

- **Groundedness** - Is the response grounded in the provided context?
- **Context coverage** - Does the response make use of the relevant information in the context?

## Composite evaluators (preview)

Composite evaluators measure several quality dimensions in one LLM judge call.
Use them to reduce the cost and latency of running the corresponding built-in
evaluators separately while retaining a score and reason for each quality
dimension.

> [!NOTE]
> Use a model from the GPT-5.6 family as the LLM judge for composite evaluators.
> For the lowest-cost option that maintains high evaluation quality, use
> `gpt-5.6-luna`.

### Output Quality

The Output Quality evaluator (`builtin.output_quality`) assesses the quality of
an agent's response and its success in addressing the user's task. It batches
the following evaluators into one LLM judge call:

| Component evaluator | What it measures | Score | Default pass threshold |
|---------------------|------------------|-------|------------------------|
| Fluency | Grammatical quality and readability. | 1-5 | 3 |
| Coherence | Logical flow and organization. | 1-5 | 3 |
| Intent Resolution | Whether the response identifies and addresses the user's intent. | 1-5 | 3 |
| Task Adherence | Whether the agent follows its instructions and constraints. | 0 or 1 | 1 |
| Groundedness | Whether the response is supported by the available context. | 1-5 | 3 |
| Task Completion | Whether the agent completes the requested task with a usable result. | 0 or 1 | 1 |

### Tool Use Quality

The Tool Use Quality evaluator (`builtin.tool_use_quality`) assesses an agent's
tool-use process from tool selection through use of the returned result. It
batches the following evaluators into one LLM judge call:

| Component evaluator | What it measures | Score | Default pass threshold |
|---------------------|------------------|-------|------------------------|
| Tool Call Accuracy | Overall correctness of the tool calls, parameters, and efficiency. | 1-5 | 3 |
| Tool Call Success | Whether tool calls complete without technical errors. | 0 or 1 | 1 |
| Tool Input Accuracy | Whether tool call parameters are correct. | 0 or 1 | 1 |
| Tool Output Utilization | Whether the agent correctly uses tool results in its response. | 0 or 1 | 1 |
| Tool Selection | Whether the agent selects the necessary tools without unnecessary calls. | 0 or 1 | 1 |

### Composite results

The primary `output_quality` or `tool_use_quality` result passes only when every
applicable component passes. A component that isn't applicable is skipped and
doesn't cause the primary result to fail. If all components are skipped, the
primary result is `not_applicable`.

Each composite evaluator returns a primary binary result and the results of its
component evaluators. Use the primary result for a strict quality gate, and use
the component results to identify the quality dimension that caused a failure.

| Output | Description |
|--------|-------------|
| `output_quality` or `tool_use_quality` | Primary score. A value of `1` means every applicable component passed. A value of `0` means at least one applicable component failed. |
| `<component>_score` | Numeric score from the component evaluator. |
| `<component>_result` | Pass/Fail result based on the component's threshold. |
| `<component>_reason` | Explanation for the component score. |
| `<component>_status` | Indicates whether the component completed or was skipped. |
| `<composite>_reason` | Lists failed components or indicates that components were skipped. |
| `<composite>_properties` | Includes lists of failed and skipped components, along with model and token metadata. |

For example, an Output Quality result fails when Fluency, Coherence, Intent
Resolution, Task Adherence, and Task Completion pass but Groundedness fails.
The `output_quality_reason` identifies Groundedness as the failed component, and
the `groundedness_reason` explains its score.

### Configure composite evaluators

Both composite evaluators support turn-level and conversation-level evaluation.
The input shape determines the evaluation level by default:

- Map `query` and `response` for turn-level evaluation.
- Map `messages` for conversation-level evaluation.

Set the `evaluation_level` initialization parameter to `turn` or `conversation`
to override this behavior.

The following configuration runs both composite evaluators at the turn level.
The response contains agent messages with tool calls and tool results, and the
tool definitions describe the tools available to the agent.

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "output_quality",
        "evaluator_name": "builtin.output_quality",
        "initialization_parameters": {
            "deployment_name": model_deployment,
            "evaluation_level": "turn",
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
    },
    {
        "type": "azure_ai_evaluator",
        "name": "tool_use_quality",
        "evaluator_name": "builtin.tool_use_quality",
        "initialization_parameters": {
            "deployment_name": model_deployment,
            "evaluation_level": "turn",
        },
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
            "tool_definitions": "{{item.tool_definitions}}",
        },
    },
]
```

Reference: [Run evaluations from the SDK](../../observability/how-to/cloud-evaluation.md)

To evaluate a full conversation, map the complete conversation to `messages`
and either omit `evaluation_level` or set it to `conversation`:

```python
"initialization_parameters": {
    "deployment_name": model_deployment,
    "evaluation_level": "conversation",
},
"data_mapping": {
    "messages": "{{item.messages}}",
    "tool_definitions": "{{item.tool_definitions}}",
},
```

Reference: [Messages with tool calls](../../observability/how-to/evaluation-dataset-schema.md#messages-with-tool-calls)

## Model and tool support

For AI-assisted evaluators, you can use Azure OpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and non-reasoning models for the LLM judge.

### Supported tools

Agent evaluators support the following tools:

- File Search
- Function Tool (user-defined tools)
- MCP
- Knowledge-based MCP

The following tools currently have limited support. Avoid using `tool_call_accuracy`, `tool input accuracy`, `tool_output_utilization`, `tool_call_success`, or `groundedness` evaluators if your agent conversation includes calls to these tools:

- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent
- Web Search

## Using agent evaluators

Agent evaluators assess how well AI agents perform tasks, follow instructions, and use tools effectively. Each evaluator requires specific data mappings and parameters:

| Evaluator | Required inputs | Required parameters | Supported evaluation levels |
|-----------|-----------------|---------------------|-----------------------------|
| Task Completion (preview) | (`query`, `response`) or `messages`; optional: `tool_definitions` | `deployment_name`; optional: `evaluation_level` | Turn, conversation |
| Customer Satisfaction (preview) | (`query`, `response`) or `messages` | `deployment_name`; optional: `threshold`, `evaluation_level` | Turn, conversation |
| Task Adherence (preview) | (`query`, `response`) or `messages`; optional: `tool_definitions` | `deployment_name` | Turn |
| Intent Resolution (preview) | (`query`, `response`) or `messages` | `deployment_name`; optional: `evaluation_level` | Turn |
| Tool Call Accuracy | (`query`, `tool_definitions`) or (`messages`, `tool_definitions`); `response` and `tool_calls` are optional with `query` | `deployment_name`; optional: `evaluation_level` | Turn |
| Tool Selection | (`query`, `tool_definitions`) or (`messages`, `tool_definitions`); `response` and `tool_calls` are optional with `query` | `deployment_name`; optional: `evaluation_level` | Turn |
| Tool Input Accuracy | (`query`, `response`, `tool_definitions`) or (`messages`, `tool_definitions`) | `deployment_name`; optional: `evaluation_level` | Turn |
| Tool Output Utilization | (`query`, `response`, `tool_definitions`) or (`messages`, `tool_definitions`) | `deployment_name`; optional: `evaluation_level` | Turn |
| Tool Call Success | `response` or `messages` | `deployment_name`; optional: `evaluation_level` | Turn |
| Task Navigation Efficiency | (`actions` or `messages`), `expected_actions` | *(none; optional: `matching_mode`)* | Turn |
| Output Quality | `query` and `response`; or `messages`. `tool_definitions` is optional. | `deployment_name`; optional: `evaluation_level` | Turn, conversation |
| Tool Use Quality | `query`, `response`, and `tool_definitions`; or `messages` and `tool_definitions`. | `deployment_name`; optional: `evaluation_level` | Turn, conversation |

Turn-level evaluation scores an individual agent response; conversation-level evaluation scores the full interaction. Use `evaluation_level` to select the level when the evaluator supports both. For the message structure, see [Messages with tool calls](../../observability/how-to/evaluation-dataset-schema.md#messages-with-tool-calls).

### Example input

Your test dataset should contain the fields referenced in your data mappings. Examples for the format below:

```jsonl
{"query": "What's the weather in Seattle?", "response": "The weather in Seattle is rainy, 14°C."}
{"query": "Book a flight to Paris for next Monday", "response": "I've booked your flight to Paris departing next Monday at 9:00 AM."}
{"messages": [{"role": "user", "content": "Book a flight to Paris."}, {"role": "assistant", "content": "I booked your flight to Paris."}]}
```

For more complex agent interactions with tool calls, use message arrays for `query` and `response`. These arrays use the same OpenAI message structure as the preferred `messages` schema. See [Separate query and response format](../../observability/how-to/evaluation-dataset-schema.md#separate-query-and-response-format). The system message is optional but useful for evaluators that assess agent behavior against instructions, including `task_adherence`, `task_completion`, `tool_call_accuracy`, `tool_selection`, `tool_input_accuracy`, `tool_output_utilization`, and `groundedness`:

```json
{
    "query": [
        {"role": "system", "content": "You are a travel booking agent."},
        {"role": "user", "content": "Book a flight to Paris for next Monday"}
    ],
    "response": [
        {"role": "assistant", "content": [{"type": "tool_call", "tool_call_id": "call_123", "name": "search_flights", "arguments": {"destination": "Paris", "date": "next Monday"}}]},
        {"role": "tool", "tool_call_id": "call_123", "content": [{"type": "tool_result", "tool_result": {"flight": "AF123", "time": "9:00 AM"}}]},
        {"role": "assistant", "content": "I've booked flight AF123 to Paris departing next Monday at 9:00 AM."}
    ]
}
```

### Tool definitions format

The `tool_definitions` field describes the tools available to the agent. It contains a list of tool objects with a `name`, `description`, and JSON Schema `parameters` object:

```json
[
  {
    "name": "search_flights",
    "description": "Search for available flights to a destination on a given date.",
    "parameters": {
      "type": "object",
      "properties": {
        "destination": { "type": "string", "description": "The destination city." },
        "date": { "type": "string", "description": "The travel date in YYYY-MM-DD format." }
      },
      "required": ["destination", "date"]
    }
  }
]
```

Include this list as the `tool_definitions` field in your test dataset alongside `query` and `response`.

### Configuration example

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_items}}` references the agent's structured output, including tool calls and results. Use this for evaluators that need full interaction context (`task_adherence`, `tool_call_accuracy`, `tool_selection`, `tool_input_accuracy`, `tool_output_utilization`).
- `{{sample.output_text}}` references the agent's plain text response. Use this for evaluators that expect a string response (for example, `coherence`, `violence`).

Here's an example configuration for Task Adherence:

```python
testing_criteria = [
    {
        "type": "azure_ai_evaluator",
        "name": "task_adherence",
        "evaluator_name": "builtin.task_adherence",
        "initialization_parameters": {"deployment_name": model_deployment},
        "data_mapping": {
            "query": "{{item.query}}",
            "response": "{{item.response}}",
        },
    },
]
```

See [Run evaluations from the SDK](../../observability/how-to/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example output

Agent evaluators return Pass/Fail results with reasoning. Key output fields:

```json
{
    "type": "azure_ai_evaluator",
    "name": "Task Adherence",
    "metric": "task_adherence",
    "label": "pass",
    "reason": "Agent followed system instructions correctly",
    "threshold": 3,
    "passed": true
}
```

For evaluators that use a 1–5 scale before thresholding (such as `intent_resolution` and `tool_call_accuracy`), the output includes a numeric `score` field alongside the pass/fail result:

```json
{
    "type": "azure_ai_evaluator",
    "name": "Intent Resolution",
    "metric": "intent_resolution",
    "label": "pass",
    "score": 4,
    "reason": "Agent correctly identified the user's intent to book a flight to Paris",
    "threshold": 3,
    "passed": true
}
```

## Task navigation efficiency

Task Navigation Efficiency measures whether the agent took an optimal sequence of actions by comparing against an expected sequence (ground truth). Use this evaluator for workflow optimization and regression testing.

```python
{
    "type": "azure_ai_evaluator",
    "name": "task_navigation_efficiency",
    "evaluator_name": "builtin.task_navigation_efficiency",
    "initialization_parameters": {
        "matching_mode": "exact_match"  # Options: "exact_match", "in_order_match", "any_order_match"
    },
    "data_mapping": {
        "actions": "{{item.actions}}",
        "expected_actions": "{{item.expected_actions}}"
    },
}
```

**Matching modes:**

| Mode | Description |
|------|-------------|
| `exact_match` | Agent's trajectory must match the ground truth exactly (order and content) |
| `in_order_match` | All ground truth steps must appear in the agent's trajectory in correct order (extra steps allowed) |
| `any_order_match` | All ground truth steps must appear in the agent's trajectory, order doesn't matter (extra steps allowed) |

**Actions format:**

Map either `actions` or `messages` with `expected_actions`. The `actions` field accepts a string or a list of message objects. The `messages` field accepts the full interaction as an array of message objects. Each action message represents a step the agent took during the conversation:

```python
actions = [
    {
        "role": "assistant",
        "content": [
            {"type": "function_call", "name": "call_tool_A", "arguments": "{\"param\": \"value\"}"}
        ]
    },
    {
        "role": "assistant",
        "content": [
            {"type": "function_call", "name": "call_tool_B", "arguments": "{}"}
        ]
    },
]
```

> [!NOTE]
> The `actions` and `expected_actions` fields use different formats. `actions` contains the agent's actual behavior as text or message objects, while `expected_actions` contains the expected tool names and, optionally, their parameters.

To provide the agent interaction as messages instead of `actions`, map `messages` and `expected_actions`:

```python
"data_mapping": {
    "messages": "{{item.messages}}",
    "expected_actions": "{{item.expected_actions}}",
}
```

**Expected actions format:**

The `expected_actions` can be a simple list of expected steps:

```python
expected_actions = ["identify_tools_to_call", "call_tool_A", "call_tool_B", "response_synthesis"]
```

Or a tuple with tool names and parameters for more detailed validation:

```python
expected_actions = (
    ["func_name1", "func_name2"],
    {
        "func_name1": {"param_key": "param_value"},
        "func_name2": {"param_key": "param_value"},
    }
)
```

**Output:**

Returns a binary pass/fail result plus precision, recall, and F1 scores:

```json
{
    "type": "azure_ai_evaluator",
    "name": "task_navigation_efficiency",
    "passed": true,
    "details": {
        "precision_score": 0.85,
        "recall_score": 1.0,
        "f1_score": 0.92
    }
}
```

## Agent message schema

Agent evaluators use message arrays when they need instructions, tool
calls, and tool results. For the canonical message structure, role definitions,
and example data, see
[Messages with tool calls](../../observability/how-to/evaluation-dataset-schema.md#messages-with-tool-calls)
and [Separate query and response format](../../observability/how-to/evaluation-dataset-schema.md#separate-query-and-response-format).

## Related content

- [More examples for agent quality evaluator](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators)
- [Evaluate your AI agents](../../observability/how-to/evaluate-agent.md)
- [How to run batch evaluation](../../observability/how-to/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)
