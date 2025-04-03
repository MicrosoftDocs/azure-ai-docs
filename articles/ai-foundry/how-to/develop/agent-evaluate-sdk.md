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
# Evaluate your AI agents locally with Azure AI Evaluation SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

AI Agents are powerful productivity assistants to create workflows for business needs. However, they come with challenges for observability due to their complex interaction patterns. In this article, you learn how to run built-in evaluators locally on simple agent data or agent messages with built-in evaluators to thoroughly assess the performance of your AI agents.

To build production-ready agentic applications and enable observability and transparency, developers need tools to assess not just the final output from an agent's workflows, but the quality and efficiency of the workflows themselves. For example, consider a typical agentic workflow:

:::image type="content" source="../../media/evaluations/agent-workflow-evaluation.gif" alt-text="Animation of the agent's workflow from user query to intent resolution to tool calls to final response." lightbox="../../media/evaluations/agent-workflow-evaluation.gif":::

The agentic workflow is triggered by a user query "weather tomorrow". It starts to execute multiple steps, such as reasoning through user intents, tool calling, and utilizing retrieval-augmented generation to produce a final response. In this process, evaluating each step of the workflow—along with the quality and safety of the final output—is crucial. Specifically, we formulate these evaluation aspects into the following evaluators for agents:

-   [Intent resolution](https://aka.ms/intentresolution-sample): Measures how well the agent identifies the user’s request, including how well it scopes the user’s intent, asks clarifying questions, and reminds end users of its scope of capabilities.
-	[Tool call accuracy](https://aka.ms/toolcallaccuracy-sample): Evaluates the agent’s ability to select the appropriate tools, and process correct parameters from previous steps.
-	[Task adherence](https://aka.ms/taskadherence-sample): Measures how well the agent’s final response adheres to its assigned tasks, according to its system message and prior steps.

To see more quality and risk and safety evaluators, refer to [built-in evaluators](./evaluate-sdk.md#data-requirements-for-built-in-evaluators) to assess the content in the process where appropriate.

## Getting started

First install the evaluators package from Azure AI evaluation SDK:

```python
pip install azure-ai-evaluation
```

## Evaluators with agent message support

Agents typically emit messages to interact with a user or other agents. Our built-in evaluators can accept simple data types such as strings in `query`, `response`, `ground_truth` according to the [single-turn data input requirements](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). However, to extract these simple data types from agent messages can be a challenge, due to the complex interaction patterns of agents and framework differences. For example, as mentioned, a single user query can trigger a long list of agent messages, typically with multiple tool calls invoked.

As illustrated in the example, we enabled agent message support specifically for these built-in evaluators to evaluate these aspects of agentic workflow. These evaluators take `tool_calls` or `tool_definitions` as parameters unique to agents.

| Evaluator       | `query`      | `response`      | `tool_calls`       | `tool_definitions`  | 
|----------------|---------------|---------------|---------------|---------------|
| `IntentResolutionEvaluator`   | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | N/A | Optional: `list[ToolCall]`  |
| `ToolCallAccuracyEvaluator`   | Required: `Union[str, list[Message]]` | Optional: `Union[str, list[Message]]`  | Optional: `Union[dict, list[ToolCall]]` | Required: `list[ToolDefinition]`  |
| `TaskAdherenceEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | N/A | Optional: `list[ToolCall]`  |

- `Message`: `dict` openai-style message describing agent interactions with a user, where `query` must include a system message as the first message.
- `ToolCall`: `dict` specifying tool calls invoked during agent interactions with a user.
- `ToolDefinition`: `dict` describing the tools available to an agent.

For `ToolCallAccuracyEvaluator`, either `response` or  `tool_calls` must be provided. 

We'll demonstrate some examples of the two data formats: simple agent data, and agent messages. However, due to the unique requirements of these evaluators, we recommend referring to the [sample notebooks](#sample-notebooks) which illustrate the possible input paths for each evaluator.  

As with other [built-in AI-assisted quality evaluators](./evaluate-sdk.md#performance-and-quality-evaluators), `IntentResolutionEvaluator` and `TaskAdherenceEvaluator` output a likert score (integer 1-5; higher score is better). `ToolCallAccuracyEvaluator` outputs the passing rate of all tool calls made (a float between 0-1) based on user query. To further improve intelligibility, all evaluators accept a binary threshold and output two new keys. For the binarization threshold, a default is set and user can override it. The two new keys are:

- `{metric_name}_result` a "pass" or "fail" string based on a binarization threshold.
- `{metric_name}_threshold` a numerical binarization threshold set by default or by the user

### Simple agent data

In simple agent data format, `query` and `response` are simple python strings. For example:  

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from azure.identity import DefaultAzureCredential
from azure.ai.evaluation import IntentResolutionEvaluator, ResponseCompletenessEvaluator
  
model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["MODEL_DEPLOYMENT_NAME"],
)
 
intent_resolution_evaluator = IntentResolutionEvaluator(model_config)
response_completeness_evaluator = ResponseCompletenessEvaluator(model_config=model_config)
 
# Evaluating query and response as strings
# A positive example. Intent is identified and understood and the response correctly resolves user intent
result = intent_resolution_evaluator(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM.",
)
print(result)
 
# A negative example. Only half of the statements in the response were complete according to the ground truth  
result = response_completeness_evaluator(
    response="Itinery: Day 1 take a train to visit Disneyland outside of the city; Day 2 rests in hotel.",
    ground_truth="Itinery: Day 1 take a train to visit the downtown area for city sightseeing; Day 2 rests in hotel."
)
print(result)
```

Examples of `tool_calls` and `tool_definitions` for `ToolCallAccuracyEvaluator`: 

```python
query = "How is the weather in Seattle?"
tool_calls = [{
                    "type": "tool_call",
                    "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                    "name": "fetch_weather",
                    "arguments": {
                        "location": "Seattle"
                    }
            },
            {
                    "type": "tool_call",
                    "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ",
                    "name": "fetch_weather",
                    "arguments": {
                        "location": "London"
                    }
            }]

tool_definition = {
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
response = tool_call_accuracy(query=query, tool_calls=tool_calls, tool_definitions=tool_definition)
print(response)
```

### Agent messages

In agent message format, `query` and `response` are list of openai-style messages. Specifically, `query` carry the past agent-user interactions leading up to the last user query and requires the system message (of the agent) on top of the list; and `response` will carry the last message of the agent in response to the last user query. Example:

```python
# user asked a question
query = [
    {
        "role": "system",
        "content": "You are a friendly and helpful customer service agent."
    },
    # past interactions omitted 
    # ...
    {
        "createdAt": "2025-03-14T06:14:20Z",
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Hi, I need help with the last 2 orders on my account #888. Could you please update me on their status?"
            }
        ]
    }
]
# the agent emits multiple messages to fulfill the request
response = [
    {
        "createdAt": "2025-03-14T06:14:30Z",
        "run_id": "0",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Hello! Let me quickly look up your account details."
            }
        ]
    },
    {
        "createdAt": "2025-03-14T06:14:35Z",
        "run_id": "0",
        "role": "assistant",
        "content": [
            {
                "type": "tool_call",
                "tool_call_id": "tool_call_20250310_001",
                "name": "get_orders",
                "arguments": {
                    "account_number": "888"
                }
            }
        ]
    },
    # many more messages omitted 
    # ...
    # here is the agent's final response 
    {
        "createdAt": "2025-03-14T06:15:05Z",
        "run_id": "0",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The order with ID 123 has been shipped and is expected to be delivered on March 15, 2025. However, the order with ID 124 is delayed and should now arrive by March 20, 2025. Is there anything else I can help you with?"
            }
        ]
    }
]

# An example of tool definitions available to the agent 
tool_definitions = [
    {
        "name": "get_orders",
        "description": "Get the list of orders for a given account number.",
        "parameters": {
            "type": "object",
            "properties": {
                "account_number": {
                    "type": "string",
                    "description": "The account number to get the orders for."
                }
            }
        }
    },
    # other tool definitions omitted 
    # ...
]

result = intent_resolution_evaluator(
    query=query,
    response=response,
    # optionally provide the tool definitions
    tool_definitions=tool_definitions 
)
print(result)

```

## Converter support

Transforming agent messages into the right evaluation data to use our evaluators can be a nontrivial task. If you use [Azure AI Agent Service](../../../ai-services/agents/overview.md), however, you can seamlessly evaluate your agents via our converter support for Azure AI agent threads and runs. Here's an example to create an Azure AI agent and some data for evaluation. Separately from evaluation, Azure AI Agent Service requires `pip install azure-ai-projects azure-identity` and an Azure AI project connection string and the supported models.

### Create agent threads and runs

```python
import os, json
import pandas as pd
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FunctionTool, ToolSet

from dotenv import load_dotenv

load_dotenv()

# Define some custom python function
def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a JSON string.
    :rtype: str
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # Here, we'll mock the response.
    mock_weather_data = {"Seattle": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    weather_json = json.dumps({"weather": weather})
    return weather_json


user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}

# Adding Tools to be used by Agent 
functions = FunctionTool(user_functions)

toolset = ToolSet()
toolset.add(functions)


# Create the agent
AGENT_NAME = "Seattle Tourist Assistant"

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name=AGENT_NAME,
    instructions="You are a helpful assistant",
    toolset=toolset,
)
print(f"Created agent, ID: {agent.id}")

thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
MESSAGE = "Can you fetch me the weather in Seattle?"

message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content=MESSAGE,
)
print(f"Created message, ID: {message.id}")

run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)

print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

print(f"Run ID: {run.id}")

# display messages
for message in project_client.agents.list_messages(thread.id, order="asc").data:
    print(f"Role: {message.role}")
    print(f"Content: {message.content[0].text.value}")
    print("-" * 40)
```

#### Convert agent runs (single-run)

Now you use our converter to transform the Azure AI agent thread or run data into required evaluation data that the evaluators can understand. 
```python
import json
from azure.ai.evaluation import AIAgentConverter

# Initialize the converter for Azure AI agents
converter = AIAgentConverter(project_client)

# Specify the thread and run id
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)
print(json.dumps(converted_data, indent=4))
```

#### Convert agent threads (multi-run)

```python
import json
from azure.ai.evaluation import AIAgentConverter

# Initialize the converter
converter = AIAgentConverter(project_client)

# specify a file path to save agent output (which is evaluation input data)
filename = os.path.join(os.getcwd(), "evaluation_input_data.jsonl")

evaluation_data = converter.prepare_evaluation_data(thread_ids=thread_id, filename=filename) 

print(f"Evaluation data saved to {filename}")
```

#### Batch evaluation on agent thread data

With the evaluation data prepared in one line of code, you can select the evaluators to assess the agent quality (for example, intent resolution, tool call accuracy, and task adherence), and submit a batch evaluation run:
```python
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator
from azure.ai.projects.models import ConnectionType
import os

from dotenv import load_dotenv
load_dotenv()


project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
model_config = project_client.connections.get_default(
                                            connection_type=ConnectionType.AZURE_OPEN_AI,
                                            include_credentials=True) \
                                         .to_evaluator_model_config(
                                            deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
                                            api_version=os.environ["MODEL_DEPLOYMENT_API_VERSION"],
                                            include_credentials=True
                                          )

# select evaluators
intent_resolution = IntentResolutionEvaluator(model_config=model_config)
task_adherence = TaskAdherenceEvaluator(model_config=model_config)
tool_call_accuracy = ToolCallAccuracyEvaluator(model_config=model_config)

# batch run API
from azure.ai.evaluation import evaluate

response = evaluate(
    data=file_path,
    evaluation_name="agent demo - batch run",
    evaluators={
        "intent_resolution": intent_resolution,
        "task_adherence": task_adherence,
        "tool_call_accuracy": tool_call_accuracy,
    },
    # optionally, log your results to your Azure AI Foundry project for rich visualization 
    azure_ai_project={
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "project_name": os.environ["PROJECT_NAME"],
        "resource_group_name": os.environ["RESOURCE_GROUP_NAME"],
    }
)
# look at the average scores 
print(response["metrics"])
# use the URL to inspect the results on the UI
print(f'AI Foundary URL: {response.get("studio_url")}')
```

With Azure AI Evaluation SDK, you can seamlessly evaluate your Azure AI agents via our converter support, which enables observability and transparency into agentic workflows. You can evaluate other agents by preparing the right data for the evaluators of your choice.

## Sample notebooks

Now you're ready to try a sample for each of these evaluators:
- [Intent resolution](https://aka.ms/intentresolution-sample)
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample)
- [Task adherence](https://aka.ms/taskadherence-sample)
- [Response Completeness](https://aka.ms/rescompleteness-sample)
- [End-to-end Azure AI agent evaluation](https://aka.ms/e2e-agent-eval-sample)

## Related content

- [Azure AI Evaluation Python SDK client reference documentation](https://aka.ms/azureaieval-python-ref)
- [Azure AI Evaluation SDK client Troubleshooting guide](https://aka.ms/azureaieval-tsg)
- [Learn more about the evaluation metrics](../../concepts/evaluation-metrics-built-in.md)
- [Evaluate your Generative AI applications remotely on the cloud](./cloud-evaluation.md)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View your evaluation results in Azure AI project](../../how-to/evaluate-results.md)
- [Get started building a chat app using the Azure AI Foundry SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
