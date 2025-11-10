---
title: Agent Evaluators for Generative AI
titleSuffix: Azure AI Foundry
description: Learn how to evaluate Azure AI agents using intent resolution, tool call accuracy, and task adherence evaluators.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: changliu2
ms.date: 10/17/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Agent evaluators (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Agents are powerful productivity assistants. They can plan, make decisions, and execute actions. Agents typically first [reason through user intents in conversations](#intent-resolution), [select the correct tools](#tool-call-accuracy) to call and satisfy the user requests, and [complete various tasks](#task-adherence) according to their instructions. Azure AI Foundry currently supports these agent-specific evaluators for agentic workflows:

- [Intent resolution](#intent-resolution)
- [Tool call accuracy](#tool-call-accuracy)
- [Task adherence](#task-adherence)

## Evaluating Azure AI agents

Agents emit messages. Providing inputs typically requires parsing messages and extracting the relevant information. If you're building agents using Azure AI Agent Service, the service provides native integration for evaluation that directly takes their agent messages. For an example, see [Evaluate AI agents](https://aka.ms/e2e-agent-eval-sample).

Besides `IntentResolution`, `ToolCallAccuracy`, and `TaskAdherence` specific to agentic workflows, you can also assess other quality and safety aspects of your agentic workflows, using a comprehensive suite of built-in evaluators. Azure AI Foundry supports this list of evaluators for Azure AI agent messages from our converter:

- **Quality**: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, `Coherence`, `Fluency`
- **Safety**: `CodeVulnerabilities`, `Violence`, `Self-harm`, `Sexual`, `HateUnfairness`, `IndirectAttack`, `ProtectedMaterials`

This article shows examples of `IntentResolution`, `ToolCallAccuracy`, and `TaskAdherence`. For examples of using other evaluators with Azure AI agent messages, see [evaluating Azure AI agents](../../how-to/develop/agent-evaluate-sdk.md#evaluate-azure-ai-agents).

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

Azure AI Agent Service supports AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1 or gpt-4o) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other evaluators| Not Supported | Supported | -- |

For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `4.1-mini` with a balance of reasoning performance and cost efficiency.

## Intent resolution

`IntentResolutionEvaluator` measures how well the system identifies and understands a user's request. This understanding includes how well it scopes the user's intent, asks questions to clarify, and reminds end users of its scope of capabilities. Higher score means better identification of user intent.

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

The numerical score is on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), the evaluator also outputs *pass* if the score >= threshold, or *fail* otherwise. Using the reason and other fields can help you understand why the score is high or low.

```python
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response provides the opening hours of the Eiffel Tower clearly and accurately, directly addressing the user's query. It includes specific times, which fully resolves the user's request for information about the opening hours.",
    "additional_details": {
        "conversation_has_intent": True,
        "agent_perceived_intent": "inquire about opening hours",
        "actual_user_intent": "find out the opening hours of the Eiffel Tower",
        "correct_intent_detected": True,
        "intent_resolved": True
    }
}

```

If you're building agents outside of Azure AI Foundry Agent Service, this evaluator accepts a schema typical for agent messages. For a sample notebook, see [Intent Resolution](https://aka.ms/intentresolution-sample).

## Tool call accuracy

`ToolCallAccuracyEvaluator` measures the accuracy and efficiency of tool calls made by an agent in a run. It provides a 1-5 score based on:
 
- The relevance and helpfulness of the tool invoked
- The correctness of parameters used in tool calls
- The counts of missing or excessive calls

#### Tool call evaluation support

`ToolCallAccuracyEvaluator` supports evaluation in Azure AI Foundry Agent Service for the following tools:

- File Search
- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent
- OpenAPI
- Function Tool (user-defined tools)

If a non-supported tool is used in the agent run, the evaluator outputs a *pass* and a reason that evaluating the invoked tools isn't supported. This approach makes it easy to filter out these cases. We recommend that you wrap non-supported tools as user-defined tools to enable evaluation.

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

If you're building agents outside of Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. For a sample notebook, see [Tool Call Accuracy](https://aka.ms/toolcallaccuracy-sample).

## Task adherence

In various task-oriented AI systems, such as agentic systems, it's important to assess whether the agent stays on track to complete a task instead of making inefficient or out-of-scope steps. `TaskAdherenceEvaluator` measures how well an agent's response adheres to their assigned tasks, according to their task instruction and available tools. The task instruction is extracted from system message and user query. Higher score means better adherence of the system instruction to resolve the task.

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

The numerical score is on a Likert scale (integer 1 to 5). A higher score is better. Given a numerical threshold (default to 3), the evaluator also outputs *pass* if the score >= threshold, or *fail* otherwise. Use the reason field to understand why the score is high or low.

```python
{
   "task_adherence": 2.0,
    "task_adherence_result": "fail",
    "task_adherence_threshold": 3,
    "task_adherence_reason": "The response partially addresses the query by mentioning relevant practices but lacks critical details and depth, making it insufficient for a comprehensive understanding of maintaining a rose garden in summer."
}
```

If you're building agents outside of Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. For a sample notebook, see [Task Adherence](https://aka.ms/taskadherence-sample).

## Related content

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
