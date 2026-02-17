---
title: "Agent Evaluators for Generative AI (temp)"
description: "Learn how to evaluate Azure AI agents using intent resolution, tool call accuracy, and task adherence evaluators. (temp)"
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - classic-and-new
  - build-aifnd
  - build-2025
---

# Agent evaluators (preview) (temp)

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

AI agents are powerful productivity assistants that can create workflows for business needs. However, observability can be a challenge due to their complex interaction patterns. Agent evaluators provide systematic observability into agentic workflows by measuring quality, safety, and performance.

An agent workflow typically involves reasoning through user intents, calling relevant tools, and using tool results to complete tasks like updating a database or drafting a report. To build production-ready agentic applications, you need to evaluate not just the final output, but also the quality and efficiency of each step in the workflow.

Foundry provides built-in agent evaluators that function like unit tests for agentic systems—they take agent messages as input and output binary Pass/Fail scores (or scaled scores converted to binary scores based on thresholds). These evaluators support two best practices for agent evaluation:

- System evaluation - to examine the end-to-end outcomes of the agentic system.
- Process evaluation - to verify the step-by-step execution to achieve the outcomes.

| Evaluator | Best practice | Use when | Purpose | Output |
|--|--|--|--|--|
| Task Completion (preview) | System evaluation | Assessing end-to-end task success in workflow automation, goal-oriented AI interactions, or any scenario where full task completion is critical | Measures if the agent completed the requested task with a usable deliverable that meets all user requirements | Binary: Pass/Fail |
| Task Adherence (preview) | System evaluation | Ensuring agents follow system instructions, validating compliance in regulated environments | Measures if the agent's actions adhere to its assigned tasks according to rules, procedures, and policy constraints, based on its system message and prior steps | Binary: Pass/Fail |
| Task Navigation Efficiency (preview) | System evaluation | Optimizing agent workflows, reducing unnecessary steps, validating against known optimal paths (requires ground truth) | Measures whether the agent made tool calls efficiently to complete a task by comparing them to expected tool sequences | Binary: Pass/Fail |
| Intent Resolution (preview) | System evaluation | Customer support scenarios, conversational AI, FAQ systems where understanding user intent is essential | Measures whether the agent correctly identifies the user's intent | Binary: Pass/Fail based on threshold (1-5 scale) |
| Tool Call Accuracy (preview) | Process evaluation | Overall tool call quality assessment in agent systems with tool integration, API interactions to complete its tasks | Measures whether the agent made the right tool calls with correct parameters to complete its task | Binary: Pass/Fail based on threshold (1-5 scale) |
| Tool Selection (preview) | Process evaluation | Validating tool choice quality in orchestration platforms, ensuring efficient tool usage without redundancy | Measures whether the agent selected the correct tools without selecting unnecessary ones | Binary: Pass/Fail |
| Tool Input Accuracy (preview) | Process evaluation | Strict validation of tool parameters in production environments, API integration tests, critical workflows requiring 100% parameter correctness | Measures if all tool call parameters are correct across six strict criteria: groundedness, type compliance, format compliance, required parameters, no unexpected parameters, and value appropriateness | Binary: Pass/Fail |
| Tool Output Utilization (preview) | Process evaluation | Validating correct use of API responses, database query results, search outputs in agent reasoning and responses | Measures if the agent correctly understood and used tool call results contextually in its reasoning and final response | Binary: Pass/Fail |
| Tool Call Success (preview) | Process evaluation | Monitoring tool reliability, detecting API failures, timeout issues, or technical errors in tool execution | Measures if tool calls succeeded or resulted in technical errors or exceptions | Binary: Pass/Fail |

## System evaluation

System evaluation examines the quality of the final outcome of your agentic workflow. These evaluators are applicable to single agents and, in multi-agent systems, to the main orchestrator or the final agent responsible for task completion:

- Task Completion - Did the agent fully complete the requested task?
- Task Adherence - Did the agent follow the rules and constraints in its instructions?
- Task Navigation Efficiency - Did the agent perform the expected steps efficiently?
- Intent Resolution - Did the agent correctly identify and address user intentions?

Specifically, for textual outputs from agents, you can also apply RAG quality evaluators such as `Relevance` and `Groundedness` that take agentic inputs to assess the final response quality.

Examples:

- [Task completion (preview) sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_completion.py)
- [Task adherence sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_adherence.py)
- [Task navigation efficiency (preview) sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_task_navigation_efficiency.py)
- [Intent resolution sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_intent_resolution.py)

## Process evaluation

Process evaluation examines the quality and efficiency of each step in your agentic workflow. These evaluators focus on the tool calls executed in a system to complete tasks:

- Tool Call Accuracy - Did the agent make the right tool calls with correct parameters without redundancy?
- Tool Selection - Did the agent select the correct and necessary tools?
- Tool Input Accuracy - Did the agent provide correct parameters for tool calls?
- Tool Output Utilization - Did the agent correctly use tool call results in its reasoning and final response?
- Tool Call Success - Did the tool calls succeed without technical errors?

Examples:

- [Tool call accuracy sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_call_accuracy.py)
- [Tool selection (preview) sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_selection.py)
- [Tool input accuracy (preview) sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_input_accuracy.py)
- [Tool output utilization (preview) sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_output_utilization.py)
- [Tool call success (preview) sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators/sample_tool_call_success.py)

## Evaluator model and tool support for agent evaluators

For AI-assisted evaluators, you can use Azure OpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and non-reasoning models for the LLM judge. For complex evaluation that requires refined reasoning, we recommend `gpt-5-mini` for its balance of performance, cost, and efficiency.

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
- Fabric Data Agent
- Web Search

## Using agent evaluators

Agent evaluators assess how well AI agents perform tasks, follow instructions, and use tools effectively. Each evaluator requires specific data mappings and parameters:

| Evaluator | Required inputs | Required parameters |
|-----------|-----------------|---------------------|
| Task Completion | `query`, `response` | `deployment_name` |
| Task Adherence | `query`, `response` | `deployment_name` |
| Intent Resolution | `query`, `response` | `deployment_name` |
| Tool Call Accuracy | (`query`, `response`, `tool_definitions`) OR (`query`, `tool_calls`, `tool_definitions`) | `deployment_name` |
| Tool Selection | (`query`, `response`, `tool_definitions`) OR (`query`, `tool_calls`, `tool_definitions`) | `deployment_name` |
| Tool Input Accuracy | `query`, `response`, `tool_definitions` | `deployment_name` |
| Tool Output Utilization | `query`, `response`, `tool_definitions` | `deployment_name` |
| Tool Call Success | `response` | `deployment_name` |
| Task Navigation Efficiency | `actions`, `expected_actions` | *(none)* |

### Example input

Your test dataset should contain the fields referenced in your data mappings. Both fields accept simple strings or conversation arrays:

```jsonl
{"query": "What's the weather in Seattle?", "response": "The weather in Seattle is rainy, 14°C."}
{"query": "Book a flight to Paris for next Monday", "response": "I've booked your flight to Paris departing next Monday at 9:00 AM."}
```

For more complex agent interactions with tool calls, use the conversation array format. This format follows the OpenAI message schema (see [Agent message schema](#agent-message-schema)). The system message is optional but useful for evaluators that assess agent behavior against instructions, including `task_adherence`, `task_completion`, `tool_call_accuracy`, `tool_selection`, `tool_input_accuracy`, `tool_output_utilization`, and `groundedness`:

```json
{
    "query": [
        {"role": "system", "content": "You are a travel booking agent."},
        {"role": "user", "content": "Book a flight to Paris for next Monday"}
    ],
    "response": [
        {"role": "assistant", "content": [{"type": "tool_call", "name": "search_flights", "arguments": {"destination": "Paris", "date": "next Monday"}}]},
        {"role": "tool", "content": [{"type": "tool_result", "tool_result": {"flight": "AF123", "time": "9:00 AM"}}]},
        {"role": "assistant", "content": "I've booked flight AF123 to Paris departing next Monday at 9:00 AM."}
    ]
}
```

### Configuration example

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_items}}` references agent responses generated or retrieved during evaluation. Use this when evaluating with an agent target or agent response data source.
- `{{sample.tool_definitions}}` references tool definitions. Use this when evaluating with an agent target or agent response data source. These are auto-populated for supported built-in tools or inferred for custom functions.

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

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

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

When using conversation array format, `query` and `response` follow the OpenAI message structure:

- **query**: Contains the conversation history leading up to the user's request. Include the system message to provide context for evaluators that assess agent behavior against instructions.
- **response**: Contains the agent's reply, including any tool calls and their results.

**Message schema:**

```
[
  {
    "role": "system" | "user" | "assistant" | "tool",
    "content": "string" | [                // string or array of content items
      {
        "type": "text" | "tool_call" | "tool_result",
        "text": "string",                  // if type == text
        "tool_call_id": "string",          // if type == tool_call
        "name": "string",                  // tool name if type == tool_call
        "arguments": { ... },              // tool args if type == tool_call
        "tool_result": { ... }             // result if type == tool_result
      }
    ]
  }
]
```

**Role types:**

| Role | Description |
|------|-------------|
| `system` | Agent instructions (optional, placed at start of query) |
| `user` | User messages and requests |
| `assistant` | Agent responses, including tool calls |
| `tool` | Tool execution results |

**Example:**

```json
{
  "query": [
    {"role": "system", "content": "You are a weather assistant."},
    {"role": "user", "content": [{"type": "text", "text": "What's the weather in Seattle?"}]}
  ],
  "response": [
    {"role": "assistant", "content": [{"type": "tool_call", "tool_call_id": "call_123", "name": "get_weather", "arguments": {"city": "Seattle"}}]},
    {"role": "tool", "content": [{"type": "tool_result", "tool_result": {"temp": "62°F", "condition": "Cloudy"}}]},
    {"role": "assistant", "content": [{"type": "text", "text": "It's currently 62°F and cloudy in Seattle."}]}
  ]
}
```

## Related content

- [More examples for agent quality evaluator](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators)
<!-- CLASSIC-ONLY: - [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md) -->
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)
