---
title: Agent Evaluation with Azure AI Evaluation SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to evaluate an AI agent with the Azure AI Evaluation SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2025
  - references_regions
ms.topic: how-to
ms.date: 04/04/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---
# Evaluate AI agents with Azure AI Evaluation SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

Use the Azure AI Evaluation SDK to assess AI agent quality and safety locally. The SDK provides built-in evaluators that measure intent resolution, tool call accuracy, task adherence, and safety metrics across your agent workflows.

Agent workflows involve multiple steps: user queries trigger intent reasoning, tool calls, and response generation. Each step requires evaluation to ensure production readiness.

## Prerequisites

- Azure AI Foundry project with connection string
- Supported AI model deployment (we recommend `o3-mini` or later)
- Python 3.8 or later

## Available evaluators

The SDK includes three agent-specific evaluators:

- **Intent resolution**: Measures whether the agent correctly identifies user intent
- **Tool call accuracy**: Measures correct function tool calls for user requests  
- **Task adherence**: Measures whether responses follow assigned tasks and system messages

Additional quality and safety evaluators include: `Relevance`, `Coherence`, `Fluency`, `Violence`, `Self-harm`, `Sexual`, `HateUnfairness`, `IndirectAttack`, `ProtectedMaterials`, and `CodeVulnerabilities`.

## Install the SDK

Install the Azure AI Evaluation SDK:

```python
pip install azure-ai-evaluation
```

For Azure AI Agent Service evaluation, also install:

```python
pip install azure-ai-projects azure-identity
```

## Evaluate Azure AI agents

Azure AI Agent Service users can evaluate agents using the built-in converter. The converter transforms agent threads and runs into evaluation data automatically.

### Create an agent and run

Create an agent with function tools:

```python
import os, json
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, ToolSet
from dotenv import load_dotenv

load_dotenv()

# Define custom function
def fetch_weather(location: str) -> str:
    """Fetches weather information for the specified location."""
    mock_weather_data = {"Seattle": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    return json.dumps({"weather": weather})

# Set up tools
functions = FunctionTool({fetch_weather})
toolset = ToolSet()
toolset.add(functions)

# Create agent
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="Weather Assistant",
    instructions="You are a helpful weather assistant",
    toolset=toolset,
)

# Create thread and message
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Can you fetch me the weather in Seattle?",
)

# Run agent
run = project_client.agents.create_and_process_run(
    thread_id=thread.id, 
    agent_id=agent.id
)
```

### Evaluate a single run

Convert agent data and run evaluators:

```python
from azure.ai.evaluation import AIAgentConverter, IntentResolutionEvaluator

# Convert agent data
converter = AIAgentConverter(project_client)
converted_data = converter.convert(thread.id, run.id)

# Configure model for evaluators
from azure.ai.projects.models import ConnectionType

model_config = project_client.connections.get_default(
    connection_type=ConnectionType.AZURE_OPEN_AI,
    include_credentials=True
).to_evaluator_model_config(
    deployment_name="o3-mini",
    api_version="2023-05-15",
    include_credentials=True
)

# Set up evaluators
from azure.ai.evaluation import (
    IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator,
    RelevanceEvaluator, CoherenceEvaluator, FluencyEvaluator,
    ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator
)

# Quality evaluators
quality_evaluators = {
    evaluator.__name__: evaluator(model_config=model_config) 
    for evaluator in [
        IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator,
        CoherenceEvaluator, FluencyEvaluator, RelevanceEvaluator
    ]
}

# Safety evaluators
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}

safety_evaluators = {
    evaluator.__name__: evaluator(azure_ai_project=azure_ai_project, credential=DefaultAzureCredential()) 
    for evaluator in [ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator]
}

# Run evaluation
all_evaluators = {**quality_evaluators, **safety_evaluators}

for name, evaluator in all_evaluators.items():
    try:
        result = evaluator(**converted_data)
        print(f"{name}: {result}")
    except Exception as e:
        print(f"Error evaluating {name}: {e}")
```

> [!NOTE]
> `ToolCallAccuracyEvaluator` requires at least one Function Tool call in the run history.

### Understanding evaluation results

Evaluators return structured results with scores, labels, and explanations:

- **`{metric_name}`**: Numerical score (1-5 for Likert scale or 0-1 for accuracy)
- **`{metric_name}_result`**: "pass" or "fail" based on threshold
- **`{metric_name}_threshold`**: Binarization threshold value
- **`{metric_name}_reason`**: Explanation for the score
- **`additional_details`**: Debugging information

Example output:

```json
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The assistant correctly understood the user's request...",
    "additional_details": {
        "conversation_has_intent": true,
        "agent_perceived_intent": "fetch the weather in Seattle",
        "correct_intent_detected": true,
        "intent_resolved": true
    }
}
```


### Evaluate multiple runs

For batch evaluation of multiple agent runs or threads:

```python
from azure.ai.evaluation import evaluate

# Convert multiple threads to evaluation data
converter = AIAgentConverter(project_client)
filename = "evaluation_input_data.jsonl"

evaluation_data = converter.prepare_evaluation_data(
    thread_ids=[thread.id], 
    filename=filename
)

# Run batch evaluation
response = evaluate(
    data=filename,
    evaluation_name="agent-batch-evaluation",
    evaluators=all_evaluators,
    azure_ai_project={
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "project_name": os.environ["PROJECT_NAME"],
        "resource_group_name": os.environ["RESOURCE_GROUP_NAME"],
    }
)

# View results
print(f"Metrics: {response['metrics']}")
print(f"Studio URL: {response.get('studio_url')}")
```

The evaluation results appear in Azure AI Foundry for detailed analysis and comparison across runs.


## Evaluate custom agents

For agents built outside Azure AI Agent Service, prepare data manually for the evaluators.

Agent-specific evaluators accept these parameters:

| Evaluator | `query` | `response` | `tool_calls` | `tool_definitions` |
|-----------|---------|------------|--------------|-------------------|
| `IntentResolutionEvaluator` | Required | Required | N/A | Optional |
| `ToolCallAccuracyEvaluator` | Required | Optional | Optional | Required |
| `TaskAdherenceEvaluator` | Required | Required | N/A | Optional |

Parameters can be simple strings or OpenAI-style message lists. For `ToolCallAccuracyEvaluator`, provide either `response` or `tool_calls`.

### Simple string evaluation

```python
from azure.ai.evaluation import IntentResolutionEvaluator, AzureOpenAIModelConfiguration

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["MODEL_DEPLOYMENT_NAME"],
)

evaluator = IntentResolutionEvaluator(model_config)

result = evaluator(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM.",
)
print(result)
```

### Tool call evaluation

```python
from azure.ai.evaluation import ToolCallAccuracyEvaluator

query = "How is the weather in Seattle?"
tool_calls = [{
    "type": "tool_call",
    "tool_call_id": "call_123",
    "name": "fetch_weather",
    "arguments": {"location": "Seattle"}
}]

tool_definitions = [{
    "name": "fetch_weather",
    "description": "Fetches weather information for the specified location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to fetch weather for."
            }
        }
    }
}]

evaluator = ToolCallAccuracyEvaluator(model_config)
result = evaluator(
    query=query, 
    tool_calls=tool_calls, 
    tool_definitions=tool_definitions
)
```

### Message-based evaluation

For complex agent interactions, use OpenAI-style message lists:

```python
query = [
    {
        "role": "system",
        "content": "You are a helpful customer service agent."
    },
    {
        "role": "user", 
        "content": "Can you help me with my order?"
    }
]

response = [
    {
        "role": "assistant",
        "content": "I'd be happy to help with your order. Could you provide your order number?"
    }
]

result = evaluator(query=query, response=response)
```

## Next steps

- [Learn more about built-in evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md)
- [View evaluation results in Azure AI Foundry](../evaluate-results.md)
- [Explore agent evaluation samples](https://aka.ms/intentresolution-sample)

## Related content

- [Azure AI Evaluation SDK overview](./evaluate-sdk.md)
- [Azure AI Agent Service documentation](../../../ai-services/agents/overview.md)
- [Data requirements for evaluators](./evaluate-sdk.md#data-requirements-for-built-in-evaluators)
