---
title: Agent evaluators for generative AI
titleSuffix: Azure AI Foundry
description: Learn how to evaluate Azure AI agents using intent resolution, tool call accuracy, and task adherence evaluators.
author: lgayhardt
ms.author: lagayhar
manager: scottpolly
ms.reviewer: changliu2
ms.date: 06/26/2025
ms.service: azure-ai-foundry
ms.topic: reference
ms.custom:
  - build-aifnd
  - build-2025
---

# Agent evaluators (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Agents are powerful productivity assistants. They can plan, make decisions, and execute actions. Agents typically first [reason through user intents in conversations](#intent-resolution), [select the correct tools](#tool-call-accuracy) to call and satisfy the user requests, and [complete various tasks](#task-adherence) according to their instructions. We current support evaluating:
- [Intent resolution](#intent-resolution)
- [Tool call accuracy](#tool-call-accuracy)
- [Task adherence](#task-adherence)

## Evaluating Azure AI agents

Agents emit messages, and providing the above inputs typically require parsing messages and extracting the relevant information. If you're building agents using Azure AI Agent Service, we provide native integration for evaluation that directly takes their agent messages. To learn more, see an [end-to-end example of evaluating agents in Azure AI Agent Service](https://aka.ms/e2e-agent-eval-sample).

Besides `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence` specific to agentic workflows, you can also assess other quality as well as safety aspects of your agentic workflows, leveraging out comprehensive suite of built-in evaluators. We support this list of evaluators for Azure AI agent messages from our converter: 
- **Quality**: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, `Coherence`, `Fluency`
- **Safety**: `CodeVulnerabilities`, `Violence`, `Self-harm`, `Sexual`, `HateUnfairness`, `IndirectAttack`, `ProtectedMaterials`.

We will show examples of `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence` here. See more examples in [evaluating Azure AI agents](../../how-to/develop/agent-evaluate-sdk.md#evaluate-azure-ai-agents) for other evaluators with Azure AI agent message support.

## Model configuration for AI-assisted evaluators

For reference in the following code snippets, the AI-assisted evaluators use a model configuration for the LLM-judge:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get["AZURE_API_KEY"],
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

### Evaluator model support
We support AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (ex: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (ex: gpt-4.1, gpt-4o, etc.) | To enable |
|------------|-----------------------------------------------------------------------------|-------------------------------------------------------------|-------|
| `Intent Resolution` / `Task Adherence` / `Tool Call Accuracy` / `Response Completeness`) | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other quality evaluators| Not Supported | Supported | -- |

For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `o3-mini` and o-series mini models released afterwards with a balance of reasoning performance and cost efficiency.

## Intent resolution

`IntentResolutionEvaluator` measures how well the system identifies and understands a user's request, including how well it scopes the user’s intent, asks clarifying questions, and reminds end users of its scope of capabilities. Higher score means better identification of user intent.

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

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason and additional fields can help you understand why the score is high or low.

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

If you're building agents outside of Azure AI Agent Serice, this evaluator accepts a schema typical for agent messages. To learn more, see our sample notebook for [Intent Resolution](https://aka.ms/intentresolution-sample).

## Tool call accuracy

`ToolCallAccuracyEvaluator` measures an agent's ability to select appropriate tools, extract, and process correct parameters from previous steps of the agentic workflow. It detects whether each tool call made is accurate (binary) and reports back the average scores, which can be interpreted as a passing rate across tool calls made.

> [!NOTE]
> `ToolCallAccuracyEvaluator` only supports Azure AI Agent's Function Tool evaluation, but does not support Built-in Tool evaluation. The agent messages must have at least one Function Tool actually called to be evaluated.    

### Tool call accuracy example

```python
from azure.ai.evaluation import ToolCallAccuracyEvaluator

tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config, threshold=3)
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

The numerical score (passing rate of correct tool calls) is 0-1 and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason and tool call detail fields can help you understand why the score is high or low.

```python
{
    "tool_call_accuracy": 1.0,
    "tool_call_accuracy_result": "pass",
    "tool_call_accuracy_threshold": 0.8,
    "per_tool_call_details": [
        {
            "tool_call_accurate": True,
            "tool_call_accurate_reason": "The input Data should get a Score of 1 because the TOOL CALL is directly relevant to the user's question about the weather in Seattle, includes appropriate parameters that match the TOOL DEFINITION, and the parameter values are correct and relevant to the user's query.",
            "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ"
        }
    ]
}
```

If you're building agents outside of Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. To learn more, see, our sample notebook for [Tool Call Accuracy](https://aka.ms/toolcallaccuracy-sample).

## Task adherence

In various task-oriented AI systems such as agentic systems, it's important to assess whether the agent has stayed on track to complete a given task instead of making inefficient or out-of-scope steps. `TaskAdherenceEvaluator` measures how well an agent’s response adheres to their assigned tasks, according to their task instruction (extracted from system message and user query), and available tools. Higher score means better adherence of the system instruction to resolve the given task.

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

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score >= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
   "task_adherence": 2.0,
    "task_adherence_result": "fail",
    "task_adherence_threshold": 3,
    "task_adherence_reason": "The response partially addresses the query by mentioning relevant practices but lacks critical details and depth, making it insufficient for a comprehensive understanding of maintaining a rose garden in summer."
}
```

If you're building agents outside of Azure AI Agent Service, this evaluator accepts a schema typical for agent messages. To learn more, see our sample notebook for [Task Adherence](https://aka.ms/taskadherence-sample).

## Related content

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-test-datasets-using-evaluate)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
