---
title: Agent Evaluators for Generative AI
titleSuffix: Microsoft Foundry
description: Learn how to evaluate Azure AI agents using intent resolution, tool call accuracy, and task adherence evaluators.
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 11/18/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Agent evaluators (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

Agents are powerful productivity assistants. They plan, make decisions, and execute actions. Agents typically [reason through user intents in conversations](#intent-resolution), [select the correct tools](#tool-call-accuracy) to satisfy user requests, and [complete tasks](#task-adherence) according to instructions. Microsoft Foundry supports these agent-specific evaluators for agentic workflows:

- [Intent resolution (preview)](#intent-resolution)
- [Tool call accuracy (preview)](#tool-call-accuracy)
- [Task adherence (preview)](#task-adherence)

## Evaluating Azure AI agents

Agents emit messages, and providing inputs typically requires parsing these messages to extract relevant information. If you're building agents using Azure AI Agent Service, the service provides native integration for evaluation that directly takes their agent messages. For an example, see [Evaluate AI agents](https://aka.ms/e2e-agent-eval-sample).

In addition to `IntentResolution`, `ToolCallAccuracy`, and `TaskAdherence`, which are specific to agentic workflows, you can assess other quality and safety aspects of these workflows using a comprehensive suite of built-in evaluators. Foundry supports this list of evaluators for Azure AI agent messages from our converter:

- **Quality**: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, `Coherence`, and `Fluency`
- **Safety**: `CodeVulnerabilities`, `Violence`, `Self-harm`, `Sexual`, `HateUnfairness`, `IndirectAttack`, and `ProtectedMaterials`

This article includes examples of `IntentResolution`, `ToolCallAccuracy`, and `TaskAdherence`. For examples of other evaluators with Azure AI agent messages, see [evaluating Azure AI agents](../../how-to/develop/agent-evaluate-sdk.md#evaluate-microsoft-foundry-agents).

## Model configuration for AI-assisted evaluators

For reference in the following code snippets, the AI-assisted evaluators use a model configuration for the large language model-judge (LLM-judge):

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get("AZURE_API_KEY"),
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

### Evaluator models support

Azure AI Agent Service supports AzureOpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and nonreasoning models for the LLM-judge depending on the evaluators:

| Evaluators | Reasoning models as judge (example: o-series models from Azure OpenAI / OpenAI) | Nonreasoning models as judge (example: gpt-4.1 or gpt-4o) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set the additional parameter `is_reasoning_model=True` when initializing evaluators |
| Other evaluators| Not Supported | Supported |--|

For complex evaluation that requires refined reasoning, use a strong reasoning model like `4.1-mini` with a balance of reasoning performance and cost efficiency.

## Intent resolution

`IntentResolutionEvaluator` measures how well the system identifies and understands a user's request. This understanding includes how well it scopes the user's intent, asks questions to clarify, and reminds end users of its scope of capabilities. A higher score indicates better identification of user intent.

### Intent resolution example

```python
from azure.ai.evaluation import IntentResolutionEvaluator

intent_resolution = IntentResolutionEvaluator(model_config=model_config, threshold=3)
intent_resolution(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM."
)

```

### Intent resolution output

The numerical score uses a Likert scale (integer 1 to 5), where a higher score is better. Given a numerical threshold (default is 3), the evaluator outputs *pass* if the score is greater than or equal to the threshold, or *fail* otherwise. Using the reason and other fields can help you understand why the score is high or low.

```python
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response provides the opening hours of the Eiffel Tower clearly and accurately, directly addressing the user's query. It includes specific times, which fully resolves the user's request for information about the opening hours.",
}

```

If you build agents outside Foundry Agent Service, this evaluator accepts a schema typical for agent messages. To explore a sample notebook, see [Intent Resolution](https://aka.ms/intentresolution-sample).

## Tool call accuracy

`ToolCallAccuracyEvaluator` measures the accuracy and efficiency of tool calls made by an agent in a run. It provides a score from 1 to 5 based on:
 
- The relevance and helpfulness of the tool used
- The correctness of parameters used in tool calls
- The counts of missing or excessive calls

### Tool call evaluation support

`ToolCallAccuracyEvaluator` supports evaluation in Agent Service for the following tools:

- File Search
- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent
- OpenAPI
- Function Tool (user-defined tools)

If an unsupported tool is used in the agent run, the evaluator outputs a *pass* and explains that evaluating the tools isn't supported. This approach makes it easy to filter out these cases. We recommend that you wrap non-supported tools as user-defined tools to enable evaluation.

### Tool call accuracy example

```python
from azure.ai.evaluation import ToolCallAccuracyEvaluator

tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config, threshold=3)

# provide the agent response with tool calls 
tool_call_accuracy(
    query="What timezone corresponds to 41.8781,-87.6298?",
    response=[
    {
        "createdAt": "2025-04-25T23:55:52Z",
        "run_id": "run_DmnhUGqYd1vCBolcjjODVitB",
        "role": "assistant",
        "content": [
            {
                "type": "tool_call",
                "tool_call_id": "call_qi2ug31JqzDuLy7zF5uiMbGU",
                "name": "azure_maps_timezone",
                "arguments": {
                    "lat": 41.878100000000003,
                    "lon": -87.629800000000003
                }
            }
        ]
    },    
    {
        "createdAt": "2025-04-25T23:55:54Z",
        "run_id": "run_DmnhUGqYd1vCBolcjjODVitB",
        "tool_call_id": "call_qi2ug31JqzDuLy7zF5uiMbGU",
        "role": "tool",
        "content": [
            {
                "type": "tool_result",
                "tool_result": {
                    "ianaId": "America/Chicago",
                    "utcOffset": None,
                    "abbreviation": None,
                    "isDaylightSavingTime": None
                }
            }
        ]
    },
    {
        "createdAt": "2025-04-25T23:55:55Z",
        "run_id": "run_DmnhUGqYd1vCBolcjjODVitB",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The timezone for the coordinates 41.8781, -87.6298 is America/Chicago."
            }
        ]
    }
    ],   
    tool_definitions=[
                {
                    "name": "azure_maps_timezone",
                    "description": "local time zone information for a given latitude and longitude.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "lat": {
                                "type": "float",
                                "description": "The latitude of the location."
                            },
                            "lon": {
                                "type": "float",
                                "description": "The longitude of the location."
                            }
                        }
                    }
                }
    ]
)

# alternatively, provide the tool calls directly without the full agent response
tool_call_accuracy(
    query="How is the weather in Seattle?",
    tool_calls=[{
                    "type": "tool_call",
                    "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                    "name": "fetch_weather",
                    "arguments": {
                        "location": "Seattle"
                    }
                }],
    tool_definitions=[{
                    "id": "fetch_weather",
                    "name": "fetch_weather",
                    "description": "Fetches the weather information for the specified location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The location to fetch weather for."
                            }
                        }
                    }
                }
    ]
)

```

### Tool call accuracy output

The numerical score is on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), the evaluator also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason and tool call detail fields to understand why the score is high or low.

```python
{
    "tool_call_accuracy": 5,
    "tool_call_accuracy_result": "pass",
    "tool_call_accuracy_threshold": 3,
    "details": {
        "tool_calls_made_by_agent": 1,
        "correct_tool_calls_made_by_agent": 1,
        "per_tool_call_details": [
            {
                "tool_name": "fetch_weather",
                "total_calls_required": 1,
                "correct_calls_made_by_agent": 1,
                "correct_tool_percentage": 1.0,
                "tool_call_errors": 0,
                "tool_success_result": "pass"
            }
        ],
        "excess_tool_calls": {
            "total": 0,
            "details": []
        },
        "missing_tool_calls": {
            "total": 0,
            "details": []
        }
    }
}
```

If you build agents outside Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. For a sample notebook, see [Tool Call Accuracy](https://aka.ms/toolcallaccuracy-sample).

## Task adherence

In various task-oriented AI systems, such as agentic systems, it's important to assess whether the agent stays on track to complete a task instead of making inefficient or out-of-scope steps. `TaskAdherenceEvaluator` measures how well an agent's response adheres to their assigned tasks, according to their task instruction and available tools. The task instruction is extracted from the system message and the user query. A higher score indicates better adherence to the system instruction for resolving the task.

### Task adherence example

```python
from azure.ai.evaluation import TaskAdherenceEvaluator

task_adherence = TaskAdherenceEvaluator(model_config=model_config, threshold=3)
task_adherence(
        query="What are the best practices for maintaining a healthy rose garden during the summer?",
        response="Make sure to water your roses regularly and trim them occasionally."                         
)
```

### Task adherence output

The evaluator outputs *pass* or *fail* otherwise. Use the reason field to understand the reasoning behind the score

```python
{
    "task_adherence_result": "fail",
    "task_adherence_reason": "The response partially addresses the query by mentioning relevant practices but lacks critical details and depth, making it insufficient for a comprehensive understanding of maintaining a rose garden in summer."
}
```

If you're building agents outside of Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. For a sample notebook, see [Task Adherence](https://aka.ms/taskadherence-sample).

::: moniker-end

::: moniker range="foundry"

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

## Evaluator model support for AI-assisted evaluators

For AI-assisted evaluators, you can use AzureOpenAI or OpenAI [reasoning models](../../openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators. For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `gpt-5-mini` with a balance of reasoning performance, cost-effectiveness, and efficiency.

### Tool evaluators support

Evaluators including `tool_call_accuracy`, `tool_selection`, `tool_input_accuracy`, `tool_output_utilization` support evaluation in Agent Service for the following tools:

- File Search
- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent
- OpenAPI
- Function Tool (user-defined tools)

If a non-supported tool is used in the agent run, the evaluator outputs a *pass* and a reason that evaluating the invoked tools isn't supported. This approach makes it easy to filter out these cases. We recommend that you wrap non-supported tools as user-defined tools to enable tool evaluation.

## Using agent evaluators

To use agent evaluators, configure them in your `testing_criteria`. Each evaluator requires specific data mappings:

| Evaluator | Required inputs | Required parameters |
|-----------|-----------------|---------------------|
| Task Completion | `query`, `response` | `deployment_name` |
| Task Adherence | `query`, `response` | `deployment_name` |
| Intent Resolution | `query`, `response` | `deployment_name` |
| Tool Call Accuracy | `query`, `tool_definitions` | `deployment_name` |
| Tool Selection | `query`, `tool_definitions` | `deployment_name` |
| Tool Input Accuracy | `query`, `response`, `tool_definitions` | `deployment_name` |
| Tool Output Utilization | `query`, `response` | `deployment_name` |
| Tool Call Success | `response` | `deployment_name` |
| Task Navigation Efficiency | `actions`, `expected_actions` | *(none)* |

**Data mapping syntax:**

- `{{item.field_name}}` references fields from your test dataset (for example, `{{item.query}}`).
- `{{sample.output_items}}` references agent responses generated or retrieved during evaluation. Use this when evaluating with an agent target or agent response data source.
- `{{sample.tool_definitions}}` references tool definitions. These are auto-populated for supported built-in tools or inferred for custom functions.

See [Run evaluations in the cloud](../../how-to/develop/cloud-evaluation.md) for details on running evaluations and configuring data sources.

### Example input

Your test dataset should contain the fields referenced in your data mappings. For agent evaluators, include `query` and `response` fields. Both fields accept simple strings or conversation arrays:

```jsonl
{"query": "What's the weather in Seattle?", "response": "The weather in Seattle is rainy, 14°C."}
{"query": "Book a flight to Paris for next Monday", "response": "I've booked your flight to Paris departing next Monday at 9:00 AM."}
```

For more complex agent interactions with tool calls, use the conversation array format. This format follows the OpenAI message schema (see [Agent message schema](#agent-message-schema)). The system message is optional but useful for evaluators like Task Adherence that assess whether the agent follows its instructions:

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

### Example output

Agent evaluators return Pass/Fail results with reasoning. The following snippet shows representative fields from the full output object:

```json
{
    "type": "azure_ai_evaluator",
    "name": "Task Adherence",
    "metric": "task_adherence",
    "label": "pass",
    "reason": "Agent followed system instructions correctly",
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
        "response": "{{item.response}}",
        "ground_truth": "{{item.ground_truth}}"
    },
}
```

**Matching modes:**

| Mode | Description |
|------|-------------|
| `exact_match` | Agent's trajectory must match the ground truth exactly (order and content) |
| `in_order_match` | All ground truth steps must appear in the agent's trajectory in correct order (extra steps allowed) |
| `any_order_match` | All ground truth steps must appear in the agent's trajectory, order doesn't matter (extra steps allowed) |

**Ground truth format:**

The `ground_truth` can be a simple list of expected steps:

```python
ground_truth = ["identify_tools_to_call", "call_tool_A", "call_tool_B", "response_synthesis"]
```

Or a tuple with tool names and parameters for more detailed validation:

```python
ground_truth = (
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

- **query**: Contains the conversation history leading up to the user's request. Include the system message to let evaluators examine agent instructions.
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

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)

::: moniker-end

::: moniker range="foundry"

- [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)

::: moniker-end
