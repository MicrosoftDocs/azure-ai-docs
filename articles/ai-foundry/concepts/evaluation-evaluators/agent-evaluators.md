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

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

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

Azure AI Agent Service supports AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and nonreasoning models for the LLM-judge depending on the evaluators:

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

| Evaluator | Best practice | Use when | Purpose | Inputs | Output |
|--|--|--|--|--|--|
| Task Completion (preview) | System evaluation | Assessing end-to-end task success in workflow automation, goal-oriented AI interactions, or any scenario where full task completion is critical | Measures if the agent completed the requested task with a usable deliverable that meets all user requirements | Query, Response, Tool definitions (Optional) | Binary: Pass/Fail |
| Task Adherence (preview) | System evaluation | Ensuring agents follow system instructions validating compliance in regulated environments | Measures if the agent's actions adhere to its assigned tasks according to rules, procedures, and policy constraints, based on its system message and prior steps | Query, Response, Tool definitions (Optional) | Binary: Pass/Fail |
| Task Navigation Efficiency (preview) | System evaluation | Optimizing agent workflows, reducing unnecessary steps, validating against known optimal paths (requires ground truth) | Measures whether the agent made tool calls efficiently to complete a task by comparing them to expected tool sequences | Response, Ground truth | Binary: Pass/Fail |
| Intent Resolution (preview) | System evaluation | Customer support scenarios, conversational AI, FAQ systems where understanding user intent is essential | Measures whether the agent correctly identifies the user's intent | Query, Response, Tool definitions (Optional) | Binary: Pass/Fail based on threshold (1-5 scale)
| Tool Call Accuracy (preview)| Process evaluation | Overall tool call quality assessment in agent systems with tool integration, API interactions to complete its tasks | Measures whether the agent made the right tool calls with correct parameters to complete its task| Query, Tool definitions, Tool calls (Optional), Response | Binary: Pass/Fail based on threshold (1-5 scale) |
| Tool Selection (preview) | Process evaluation | Validating tool choice quality in orchestration platforms, ensuring efficient tool usage without redundancy | Measures whether the agent selected the correct tools without selecting unnecessary ones | Query, Tool definitions, Tool calls (Optional), Response | Binary: Pass/Fail |
| Tool Input Accuracy (preview) | Process evaluation |  Strict validation of tool parameters in production environments, API integration tests, critical workflows requiring 100% parameter correctness | Measures if all tool call parameters are correct across six strict criteria: groundedness, type compliance, format compliance, required parameters, no unexpected parameters, and value appropriateness | Query, Response, Tool definitions | Binary: Pass/Fail  |
| Tool Output Utilization (preview) | Process evaluation | Validating correct use of API responses, database query results, search outputs in agent reasoning and responses | Measures if the agent correctly understood and used tool call results contextually in its reasoning and final response | Query, Response,  Tool definitions (Optional)| Binary: Pass/Fail |
| Tool Call Success (preview) | Process evaluation | Monitoring tool reliability, detecting API failures, timeout issues, or technical errors in tool execution | Measures if tool calls succeeded or resulted in technical errors or exceptions | Response, Tool definitions (Optional)  | Binary: Pass/Fail |

## System evaluation

System evaluation examines the quality of the final outcome of your agentic workflow. These evaluators are applicable to single agents and, in multi-agent systems, to the main orchestrator or the final agent responsible for task completion:

- Task Completion - Did the agent fully complete the requested task?
- Task Adherence - Did the agent follow the rules and constraints in its instructions?
- Task Navigation Efficiency - Did the agent perform the expected steps efficiently?
- Intent Resolution - Did the agent correctly identify and address user intentions?

Specifically, for textual outputs from agents, you can also apply RAG quality evaluators such as `Relevance` and `Groundedness` that takes agentic inputs to assess the final response quality.

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

For AI-assisted evaluators, you can use AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators. For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `gpt-5-mini` with a balance of reasoning performance, cost-effectiveness, and efficiency.

### Tool evaluators support

Evaluators including tool_call_accuracy, tool_selection, tool_input_accuracy, tool_output_utilization support evaluation in Agent Service for the following tools:

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

### Examples of system-level and process evaluation

```python

from dotenv import load_dotenv
import os
import json
import time
from pprint import pprint
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)


load_dotenv()


endpoint = os.environ[
    "AZURE_AI_PROJECT_ENDPOINT"
]  # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>
model_deployment_name = os.environ.get("AZURE_AI_MODEL_DEPLOYMENT_NAME", "")  # Sample : gpt-4o-mini

with DefaultAzureCredential() as credential:
    with AIProjectClient(
        endpoint=endpoint, credential=credential
    ) as project_client:
        print("Creating an OpenAI client from the AI Project client")

        client = project_client.get_openai_client()

        data_source_config = {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {
                    "query": {"anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "object"}}]},
                    "tool_definitions": {
                        "anyOf": [{"type": "object"}, {"type": "array", "items": {"type": "object"}}]
                    },
                    "tool_calls": {"anyOf": [{"type": "object"}, {"type": "array", "items": {"type": "object"}}]},
                    "response": {"anyOf": [{"type": "string"}, {"type": "array", "items": {"type": "object"}}]},
                },
                "required": ["query", "response", "tool_definitions"],
            },
            "include_sample_schema": True,
        }

        testing_criteria = [
            # System Evaluation
            # 1. Task Completion
            {
                "type": "azure_ai_evaluator",
                "name": "task_completion",
                "evaluator_name": "builtin.task_completion",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # 2. Task Adherence
            {
                "type": "azure_ai_evaluator",
                "name": "task_adherence",
                "evaluator_name": "builtin.task_adherence",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # 3. Intent Resolution
            {
                "type": "azure_ai_evaluator",
                "name": "intent_resolution",
                "evaluator_name": "builtin.intent_resolution",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # RAG Evaluation
            # 4. Groundedness
            {
                "type": "azure_ai_evaluator",
                "name": "groundedness",
                "evaluator_name": "builtin.groundedness",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                    "response": "{{item.response}}",
                },
            },
            # 5. Relevance
            {
                "type": "azure_ai_evaluator",
                "name": "relevance",
                "evaluator_name": "builtin.relevance",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                },
            },
            # Process Evaluation
            # 1. Tool Call Accuracy
            {
                "type": "azure_ai_evaluator",
                "name": "tool_call_accuracy",
                "evaluator_name": "builtin.tool_call_accuracy",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                    "tool_calls": "{{item.tool_calls}}",
                    "response": "{{item.response}}",
                },
            },
            # 2. Tool Selection
            {
                "type": "azure_ai_evaluator",
                "name": "tool_selection",
                "evaluator_name": "builtin.tool_selection",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_calls": "{{item.tool_calls}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # 3. Tool Input Accuracy
            {
                "type": "azure_ai_evaluator",
                "name": "tool_input_accuracy",
                "evaluator_name": "builtin.tool_input_accuracy",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # 4. Tool Output Utilization
            {
                "type": "azure_ai_evaluator",
                "name": "tool_output_utilization",
                "evaluator_name": "builtin.tool_output_utilization",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "query": "{{item.query}}",
                    "response": "{{item.response}}",
                    "tool_definitions": "{{item.tool_definitions}}",
                },
            },
            # 5. Tool Call Success
            {
                "type": "azure_ai_evaluator",
                "name": "tool_success",
                "evaluator_name": "builtin.tool_success",
                "initialization_parameters": {
                    "deployment_name": f"{model_deployment_name}",
                    # "is_reasoning_model": True # if you use an AOAI reasoning model
                },
                "data_mapping": {
                    "tool_definitions": "{{item.tool_definitions}}",
                    "response": "{{item.response}}"
                },
            },

        ]

        print("Creating Eval Group")
        eval_object = client.evals.create(
            name="Test Tool Call Accuracy Evaluator with inline data",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
        )
        print(f"Eval Group created")

        print("Get Eval Group by Id")
        eval_object_response = client.evals.retrieve(eval_object.id)
        print("Eval Run Response:")
        print(eval_object_response)
        
        query = [
            # system message is required for task adherence evaluator to examine agent instructions
            {"role": "system", "content": "You are a weather report agent."},
            # (optional) prior conversation messages may be included as context for better evaluation accuracy
            # user message with tool use request
            {
                "createdAt": "2025-03-14T08:00:00Z",
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Can you send me an email at your_email@example.com with weather information for Seattle?"
                    }
                ],
            },
        ]

        # agent's response with tool calls and tool results to resolve the user request
        response = [
            {
                "createdAt": "2025-03-26T17:27:35Z",
                "run_id": "run_zblZyGCNyx6aOYTadmaqM4QN",
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_call",
                        "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                        "name": "fetch_weather",
                        "arguments": {"location": "Seattle"},
                    }
                ],
            },
            {
                "createdAt": "2025-03-26T17:27:37Z",
                "run_id": "run_zblZyGCNyx6aOYTadmaqM4QN",
                "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                "role": "tool",
                "content": [{"type": "tool_result", "tool_result": {"weather": "Rainy, 14\u00b0C"}}],
            },
            {
                "createdAt": "2025-03-26T17:27:38Z",
                "run_id": "run_zblZyGCNyx6aOYTadmaqM4QN",
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_call",
                        "tool_call_id": "call_iq9RuPxqzykebvACgX8pqRW2",
                        "name": "send_email",
                        "arguments": {
                            "recipient": "your_email@example.com",
                            "subject": "Weather Information for Seattle",
                            "body": "The current weather in Seattle is rainy with a temperature of 14\u00b0C.",
                        },
                    }
                ],
            },
            {
                "createdAt": "2025-03-26T17:27:41Z",
                "run_id": "run_zblZyGCNyx6aOYTadmaqM4QN",
                "tool_call_id": "call_iq9RuPxqzykebvACgX8pqRW2",
                "role": "tool",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_result": {"message": "Email successfully sent to your_email@example.com."},
                    }
                ],
            },
            {
                "createdAt": "2025-03-26T17:27:42Z",
                "run_id": "run_zblZyGCNyx6aOYTadmaqM4QN",
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "I have successfully sent you an email with the weather information for Seattle. The current weather is rainy with a temperature of 14\u00b0C.",
                    }
                ],
            },
        ]

        # tool definitions: schema of tools available to the agent
        tool_definitions = [
            {
                "name": "fetch_weather",
                "description": "Fetches the weather information for the specified location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The location to fetch weather for."}
                    },
                },
            },
            {
                "name": "send_email",
                "description": "Sends an email with the specified subject and body to the recipient.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "recipient": {"type": "string", "description": "Email address of the recipient."},
                        "subject": {"type": "string", "description": "Subject of the email."},
                        "body": {"type": "string", "description": "Body content of the email."},
                    },
                },
            }
        ]

        print("Creating Eval Run with Inline Data")
        eval_run_object = client.evals.runs.create(
            eval_id=eval_object.id,
            name="inline_data_run",
            metadata={"team": "Evaluation", "scenario": "inline-data-agent-quality"},
            data_source=CreateEvalJSONLRunDataSourceParam(
                type="jsonl",
                source=SourceFileContent(
                    type="file_content",
                    content=[
                        # Conversation format with object types
                        SourceFileContentContent(
                            item={
                                "query": query,
                                "tool_definitions": tool_definitions,
                                "response": response,
                                "tool_calls": None, # only needed for tool-focused evaluators if separate from response
                            }
                        ),
                    ],
                ),
            ),
        )

        print(f"Eval Run created")
        pprint(eval_run_object)

        print("Get Eval Run by Id")
        eval_run_response = client.evals.runs.retrieve(run_id=eval_run_object.id, eval_id=eval_object.id)
        print("Eval Run Response:")
        pprint(eval_run_response)

        print("\n\n----Eval Run Output Items----\n\n")

        while True:
            run = client.evals.runs.retrieve(run_id=eval_run_response.id, eval_id=eval_object.id)
            if run.status == "completed" or run.status == "failed":
                output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id))
                pprint(output_items)
                print(f"Eval Run Status: {run.status}")
                print(f"Eval Run Report URL: {run.report_url}")
                break
            time.sleep(5)
            print("Waiting for eval run to complete...")

```

### Task navigation efficiency

This code-based evaluator measures whether the agent took an optimal or expected sequence of actions including tool calls to complete a task by comparing against a user-provided expected sequence (ground truth). It helps identify inefficiencies in agent workflows, such as unnecessary steps or deviations from the optimal path.

Use Task Navigation Efficiency for optimizing agent workflows, reducing unnecessary steps, and validating against known optimal paths. This evaluator is best suited for:

- Performance optimization
- Workflow benchmarking
- Regression testing against established patterns
- Scenarios with well-defined optimal paths

### Example using task navigation efficiency

```python

from dotenv import load_dotenv
import os
import json
import time
from pprint import pprint

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from openai.types.evals.create_eval_jsonl_run_data_source_param import (
    CreateEvalJSONLRunDataSourceParam,
    SourceFileContent,
    SourceFileContentContent,
)


load_dotenv()


endpoint = os.environ.get(
    "AZURE_AI_PROJECT_ENDPOINT", ""
)  # Sample : https://<account_name>.services.ai.azure.com/api/projects/<project_name>

with DefaultAzureCredential() as credential:

    with AIProjectClient(
        endpoint=endpoint, credential=credential
    ) as project_client:

        print("Creating an OpenAI client from the AI Project client")

        client = project_client.get_openai_client()

        data_source_config = {
            "type": "custom",
            "item_schema": {
                "type": "object",
                "properties": {"response": {"type": "array"}, "ground_truth": {"type": "array"}},
                "required": ["response", "ground_truth"],
            },
            "include_sample_schema": True,
        }

        testing_criteria = [
            {
                "type": "azure_ai_evaluator",
                "name": "task_navigation_efficiency",
                "evaluator_name": "builtin.task_navigation_efficiency",
                "initialization_parameters": {
                    "matching_mode": "exact_match"  #  Can be "exact_match", "in_order_match", or "any_order_match"
                },
                "data_mapping": {"response": "{{item.response}}", "ground_truth": "{{item.ground_truth}}"},
            }
        ]

        print("Creating Eval Group")
        eval_object = client.evals.create(
            name="Test Task Navigation Efficiency Evaluator with inline data",
            data_source_config=data_source_config,
            testing_criteria=testing_criteria,
        )
        print(f"Eval Group created")

        print("Get Eval Group by Id")
        eval_object_response = client.evals.retrieve(eval_object.id)
        print("Eval Run Response:")
        pprint(eval_object_response)


        response = [
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_call",
                        "tool_call_id": "call_1",
                        "name": "search",
                        "arguments": {"query": "weather", "location": "NYC"},
                    }
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_call",
                        "tool_call_id": "call_2",
                        "name": "format_result",
                        "arguments": {"format": "json"},
                    }
                ],
            },
        ]

        ground_truth = (
            ["search", "format_result"],
            {"search": {"query": "weather", "location": "NYC"}, "format_result": {"format": "json"}},
        )

        print("Creating Eval Run with Inline Data")
        eval_run_object = client.evals.runs.create(
            eval_id=eval_object.id,
            name="inline_data_run",
            metadata={"team": "eval-exp", "scenario": "inline-data-v1"},
            data_source=CreateEvalJSONLRunDataSourceParam(
                type="jsonl",
                source=SourceFileContent(
                    type="file_content",
                    content=[
                        SourceFileContentContent(item={"response": response, "ground_truth": ground_truth}),
                    ],
                ),
            ),
        )

        print(f"Eval Run created")
        pprint(eval_run_object)

        print("Get Eval Run by Id")
        eval_run_response = client.evals.runs.retrieve(run_id=eval_run_object.id, eval_id=eval_object.id)
        print("Eval Run Response:")
        pprint(eval_run_response)

        print("\n\n----Eval Run Output Items----\n\n")

        while True:
            run = client.evals.runs.retrieve(run_id=eval_run_response.id, eval_id=eval_object.id)
            if run.status == "completed" or run.status == "failed":
                output_items = list(client.evals.runs.output_items.list(run_id=run.id, eval_id=eval_object.id))
                pprint(output_items)
                print(f"Eval Run Status: {run.status}")
                print(f"Eval Run Report URL: {run.report_url}")
                break
            time.sleep(5)
            print("Waiting for eval run to complete...")
```

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
- [How to run agent evaluation](../../how-to/develop/agent-evaluate-sdk.md)

::: moniker-end

::: moniker range="foundry"

- [More examples for agent quality evaluator](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators)
- [How to run agent evaluation](../../default/observability/how-to/evaluate-agent.md)
- [How to run cloud evaluation](../../how-to/develop/cloud-evaluation.md)
- [How to optimize agentic RAG](https://aka.ms/optimize-agentic-rag-blog)

::: moniker-end
