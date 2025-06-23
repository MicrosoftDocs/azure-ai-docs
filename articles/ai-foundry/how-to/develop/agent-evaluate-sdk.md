---
title: Agent Evaluation with the Azure AI Evaluation SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to evaluate an AI agent with the Azure AI Evaluation SDK.
Manager: scottpolly
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

# Evaluate your AI agents locally with the Azure AI Evaluation SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

AI agents are powerful productivity assistants that can create workflows for business needs. However, observability can be a challenge, due to their complex interaction patterns. In this article, you learn how to run built-in evaluators locally on simple agent data or agent messages.

To build production-ready agentic applications and enable observability and transparency, developers need tools to assess not just the final output from an agent's workflows, but the quality and efficiency of the workflows themselves. For example, consider a typical agentic workflow:

:::image type="content" source="../../media/evaluations/agent-workflow-evaluation.gif" alt-text="Animation of the agent's workflow that shows a user query, intent resolution, tool calls, and the final response." lightbox="../../media/evaluations/agent-workflow-evaluation.gif":::

An event, like a user querying "weather tomorrow" triggers an agentic workflow. To produce a final response, the agentic workflow runs multiple steps that include reasoning through user intents, tool calling, and utilizing retrieval-augmented generation. In this process, it's crucial to evaluate each step of the workflow, as well as the quality and safety of the final output. We formulate these evaluation aspects into the following evaluators for agents:

- [Intent resolution](https://aka.ms/intentresolution-sample): Measures whether the agent correctly identifies the user's intent.
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample): Measures whether the agent made the correct function tool calls to a user's request.
- [Task adherence](https://aka.ms/taskadherence-sample): Measures whether the agent's final response adheres to its assigned tasks, according to its system message and prior steps.

You can also assess other quality and safety aspects of your agentic workflows, by using our comprehensive suite of built-in evaluators. In general, agents emit agent messages. Transforming agent messages into the right evaluation data so that you can use our evaluators can be a nontrivial task. If you use [Azure AI Foundry Agent Service](../../../ai-services/agents/overview.md) to build your agent, you can [seamlessly evaluate it via our converter support](#evaluate-azure-ai-agents). If you build your agent outside of Azure AI Foundry Agent Service, you can still use our evaluators as appropriate to your agentic workflow, by parsing your agent messages into the [required data formats](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). See examples in [Evaluate other agents](#evaluating-other-agents).

## Get started

Install the evaluators package from the Azure AI evaluation SDK:

```python
pip install azure-ai-evaluation
```

## Evaluate Azure AI agents

If you use [Azure AI Foundry Agent Service](../../../ai-services/agents/overview.md), you can seamlessly evaluate your agents via our converter support for Azure AI agent threads and runs. We support this list of evaluators for Azure AI agent messages from our converter:

- Quality: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, `Coherence`, `Fluency`
- Safety: `CodeVulnerabilities`, `Violence`, `Self-harm`, `Sexual`, `HateUnfairness`, `IndirectAttack`, `ProtectedMaterials`

> [!NOTE]
> `ToolCallAccuracyEvaluator` supports only the Function Tool evaluation of the Azure AI Agent, and doesn't support the Built-in Tool evaluation. The agent messages must have at least one Function Tool actually called to be evaluated.

Here's an example that shows you how to seamlessly build and evaluate an Azure AI agent. Separately from evaluation, Azure AI Foundry Agent Service requires `pip install azure-ai-projects azure-identity`, an Azure AI project connection string, and the supported models.

### Create agent threads and runs

See the following code to create agent threads and runs:

```python
import os, json
import pandas as pd
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from typing import Set, Callable, Any
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

### Evaluate a single agent run

After you create agent runs, you can easily use our converter to transform the Azure AI agent thread data into the required evaluation data that the evaluators can understand.

```python
import json, os
from azure.ai.evaluation import AIAgentConverter, IntentResolutionEvaluator

# Initialize the converter for Azure AI agents
converter = AIAgentConverter(project_client)

# Specify the thread and run id
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)
```

And that's it! You don't need to read the input requirements for each evaluator and do any work to parse them. You need only to select your evaluator and call the evaluator on this single run. For model choice, we recommend a strong reasoning model like `o3-mini` and later models. We set up a list of quality and safety evaluators in `quality_evaluators` and `safety_evaluators` and reference them in [Evaluating multiples agent runs or a thread](#evaluate-multiple-agent-runs-or-threads).

```python
# specific to agentic workflows
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator 
# other quality as well as risk and safety metrics
from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator, CodeVulnerabilityEvaluator, ContentSafetyEvaluator, IndirectAttackEvaluator, FluencyEvaluator
from azure.ai.projects.models import ConnectionType
from azure.identity import DefaultAzureCredential

import os
from dotenv import load_dotenv
load_dotenv()

model_config = project_client.connections.get_default(
                                            connection_type=ConnectionType.AZURE_OPEN_AI,
                                            include_credentials=True) \
                                         .to_evaluator_model_config(
                                            deployment_name="o3-mini",
                                            api_version="2023-05-15",
                                            include_credentials=True
                                          )

quality_evaluators = {evaluator.__name__: evaluator(model_config=model_config) for evaluator in [IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator, CoherenceEvaluator, FluencyEvaluator, RelevanceEvaluator]}


## Using Azure AI Foundry Hub
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}
## Using Azure AI Foundry Development Platform, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

safety_evaluators = {evaluator.__name__: evaluator(azure_ai_project=azure_ai_project, credential=DefaultAzureCredential()) for evaluator in[ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator]}

# reference the quality and safety evaluator list above
quality_and_safety_evaluators = {**quality_evaluators, **safety_evaluators}

for name, evaluator in quality_and_safety_evaluators.items():
   try:
      result = evaluator(**converted_data)
      print(name)
      print(json.dumps(result, indent=4)) 
   except:
      print("Note: if there is no tool call to evaluate in the run history, ToolCallAccuracyEvaluator will raise an error")
      pass

```

#### Output format

AI-assisted quality evaluators provide a result for a query and response pair. The result is a dictionary that contains:

- `{metric_name}`: Provides a numerical score, on a Likert scale (integer 1 to 5) or a float between 0-1.
- `{metric_name}_label`: Provides a binary label (if the metric naturally outputs a binary score).
- `{metric_name}_reason`: Explains why a certain score or label was given for each data point.

To further improve intelligibility, all evaluators accept a binary threshold (unless their outputs are already binary) and output two new keys. For the binarization threshold, a default is set, which the user can override. The two new keys are:

- `{metric_name}_result`: A "pass" or "fail" string based on a binarization threshold.
- `{metric_name}_threshold`: A numerical binarization threshold set by default or by the user.
- `additional_details`: Contains debugging information about the quality of a single agent run.

See the following example output for some evaluators:

```json
{
    "intent_resolution": 5.0, # likert scale: 1-5 integer 
    "intent_resolution_result": "pass", # pass because 5 > 3 the threshold
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The assistant correctly understood the user's request to fetch the weather in Seattle. It used the appropriate tool to get the weather information and provided a clear and accurate response with the current weather conditions in Seattle. The response fully resolves the user's query with all necessary information.",
    "additional_details": {
        "conversation_has_intent": true,
        "agent_perceived_intent": "fetch the weather in Seattle",
        "actual_user_intent": "fetch the weather in Seattle",
        "correct_intent_detected": true,
        "intent_resolved": true
    }
}
{
    "task_adherence": 5.0, # likert scale: 1-5 integer 
    "task_adherence_result": "pass", # pass because 5 > 3 the threshold
    "task_adherence_threshold": 3,
    "task_adherence_reason": "The response accurately follows the instructions, fetches the correct weather information, and relays it back to the user without any errors or omissions."
}
{
    "tool_call_accuracy": 1.0,  # this is the average of all correct tool calls (or passing rate) 
    "tool_call_accuracy_result": "pass", # pass because 1.0 > 0.8 the threshold
    "tool_call_accuracy_threshold": 0.8,
    "per_tool_call_details": [
        {
            "tool_call_accurate": true,
            "tool_call_accurate_reason": "The tool call is directly relevant to the user's query, uses the correct parameter, and the parameter value is correctly extracted from the conversation.",
            "tool_call_id": "call_2svVc9rNxMT9F50DuEf1XExx"
        }
    ]
}
```

### Evaluate multiple agent runs or threads

To evaluate multiple agent runs or threads, we recommend using the batch `evaluate()` API for asynchronous evaluation. First, convert your agent thread data into a file via our converter support:

```python
import json
from azure.ai.evaluation import AIAgentConverter

# Initialize the converter
converter = AIAgentConverter(project_client)

# Specify a file path to save agent output (which is evaluation input data)
filename = os.path.join(os.getcwd(), "evaluation_input_data.jsonl")

evaluation_data = converter.prepare_evaluation_data(thread_ids=thread_id, filename=filename) 

print(f"Evaluation data saved to {filename}")
```

With the evaluation data prepared in one line of code, you can select the evaluators to assess the agent quality and submit a batch evaluation run. In the following example, we reference the same list of quality and safety evaluators in section [Evaluate a single agent run](#evaluate-a-single-agent-run) `quality_and_safety_evaluators`:  

```python
import os
from dotenv import load_dotenv
load_dotenv()


# Batch evaluation API (local)
from azure.ai.evaluation import evaluate

response = evaluate(
    data=filename,
    evaluation_name="agent demo - batch run",
    evaluators=quality_and_safety_evaluators,
    # optionally, log your results to your Azure AI Foundry project for rich visualization 
    azure_ai_project={
        "subscription_id": os.environ["AZURE_SUBSCRIPTION_ID"],
        "project_name": os.environ["PROJECT_NAME"],
        "resource_group_name": os.environ["RESOURCE_GROUP_NAME"],
    }
)
# Inspect the average scores at a high-level
print(response["metrics"])
# Use the URL to inspect the results on the UI
print(f'AI Foundary URL: {response.get("studio_url")}')
```

After the URI, you'll be redirected to Foundry. You can view your evaluation results in your Azure AI project and debug your application. Using reason fields and pass/fail, you can easily assess the quality and safety performance of your applications. You can run and compare multiple runs to test for regression or improvements.  

With the Azure AI Evaluation SDK client library, you can seamlessly evaluate your Azure AI agents via our converter support, which enables observability and transparency into agentic workflows.

## <a name = "evaluating-other-agents"></a> Evaluate other agents

If you're using agents outside of Azure AI Foundry Agent Service, you can still evaluate them by preparing the right data for the evaluators of your choice.

Agents typically emit messages to interact with a user or other agents. Our built-in evaluators can accept simple data types such as strings in `query`, `response`, and `ground_truth` according to the [Single-turn data input requirements](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). However, it can be a challenge to extract these simple data types from agent messages, due to the complex interaction patterns of agents and framework differences. For example, a single user query can trigger a long list of agent messages, typically with multiple tool calls invoked.

As illustrated in the example, we enabled agent message support specifically for the built-in evaluators `IntentResolution`, `ToolCallAccuracy`, and `TaskAdherence` to evaluate these aspects of agentic workflow. These evaluators take `tool_calls` or `tool_definitions` as parameters unique to agents.

| Evaluator       | `query`      | `response`      | `tool_calls`       | `tool_definitions`  |
|----------------|---------------|---------------|---------------|---------------|
| `IntentResolutionEvaluator`   | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |
| `ToolCallAccuracyEvaluator`   | Required: `Union[str, list[Message]]` | Optional: `Union[str, list[Message]]`  | Optional: `Union[dict, list[ToolCall]]` | Required: `list[ToolDefinition]`  |
| `TaskAdherenceEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |

- `Message`: `dict` OpenAI-style message that describes agent interactions with a user, where the `query` must include a system message as the first message.
- `ToolCall`: `dict` that specifies tool calls invoked during agent interactions with a user.
- `ToolDefinition`: `dict` that describes the tools available to an agent.

For `ToolCallAccuracyEvaluator`, either `response` or  `tool_calls` must be provided.

Following are examples of the two data formats: simple agent data, and agent messages. However, due to the unique requirements of these evaluators, we recommend referring to the [Sample notebooks](#sample-notebooks), which illustrate the possible input paths for each evaluator.  

As with other [built-in AI-assisted quality evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md), `IntentResolutionEvaluator` and `TaskAdherenceEvaluator` output a Likert score (integer 1-5; higher score is better). `ToolCallAccuracyEvaluator` outputs the passing rate of all tool calls made (a float between 0-1) based on user query. To further improve intelligibility, all evaluators accept a binary threshold and output two new keys. For the binarization threshold, a default is set and the user can override it. The two new keys are:

- `{metric_name}_result`: A "pass" or "fail" string based on a binarization threshold.
- `{metric_name}_threshold`: A numerical binarization threshold set by default or by the user.

### Simple agent data

In simple agent data format, `query` and `response` are simple python strings. For example:  

```python
import os
import json
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

# Evaluating query and response as strings
# A positive example. Intent is identified and understood and the response correctly resolves user intent
result = intent_resolution_evaluator(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM.",
)
print(json.dumps(result, indent=4))
 
```

See the following output (reference [Output format](#output-format) for details):

```json
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response provides the opening hours of the Eiffel Tower, which directly addresses the user's query. The information is clear, accurate, and complete, fully resolving the user's intent.",
    "additional_details": {
        "conversation_has_intent": true,
        "agent_perceived_intent": "inquire about the opening hours of the Eiffel Tower",
        "actual_user_intent": "inquire about the opening hours of the Eiffel Tower",
        "correct_intent_detected": true,
        "intent_resolved": true
    }
}
```

See the following examples of `tool_calls` and `tool_definitions` for `ToolCallAccuracyEvaluator`:

```python
import json 

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

tool_definitions = [{
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
                }]
response = tool_call_accuracy(query=query, tool_calls=tool_calls, tool_definitions=tool_definitions)
print(json.dumps(response, indent=4))
```

See the following output (reference [Output format](#output-format) for details):

```json
{
    "tool_call_accuracy": 0.5,
    "tool_call_accuracy_result": "fail",
    "tool_call_accuracy_threshold": 0.8,
    "per_tool_call_details": [
        {
            "tool_call_accurate": true,
            "tool_call_accurate_reason": "The TOOL CALL is directly relevant to the user's query, uses appropriate parameters, and the parameter values are correctly extracted from the conversation. It is likely to provide useful information to advance the conversation.",
            "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ"
        },
        {
            "tool_call_accurate": false,
            "tool_call_accurate_reason": "The TOOL CALL is not relevant to the user's query about the weather in Seattle and uses a parameter value that is not present or inferred from the conversation.",
            "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ"
        }
    ]
}
```

### Agent messages

In agent message format, `query` and `response` are a list of OpenAI-style messages. Specifically, the `query` carries the past agent-user interactions leading up to the last user query and requires the system message (of the agent) on top of the list; and `response` carries the last message of the agent in response to the last user query. See the following example:

```python
import json

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
print(json.dumps(result, indent=4))

```

See the following output (reference [Output format](#output-format) for details):

```json
{
    "tool_call_accuracy": 0.5,
    "tool_call_accuracy_result": "fail",
    "tool_call_accuracy_threshold": 0.8,
    "per_tool_call_details": [
        {
            "tool_call_accurate": true,
            "tool_call_accurate_reason": "The TOOL CALL is directly relevant to the user's query, uses appropriate parameters, and the parameter values are correctly extracted from the conversation. It is likely to provide useful information to advance the conversation.",
            "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ"
        },
        {
            "tool_call_accurate": false,
            "tool_call_accurate_reason": "The TOOL CALL is not relevant to the user's query about the weather in Seattle and uses a parameter value that is not present or inferred from the conversation.",
            "tool_call_id": "call_CUdbkBfvVBla2YP3p24uhElJ"
        }
    ]
}
```

This evaluation schema helps you parse your agent data outside of Azure AI Foundry Agent Service, so that you can use our evaluators to support observability into your agentic workflows.

## Sample notebooks

Now you're ready to try a sample for each of these evaluators:

- [Intent resolution](https://aka.ms/intentresolution-sample)
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample)
- [Task adherence](https://aka.ms/taskadherence-sample)
- [Response completeness](https://aka.ms/rescompleteness-sample)
- [End-to-end Azure AI agent evaluation](https://aka.ms/e2e-agent-eval-sample)

## Related content

- [Azure AI Evaluation Python SDK client reference documentation](https://aka.ms/azureaieval-python-ref)
- [Azure AI Evaluation SDK client troubleshooting guide](https://aka.ms/azureaieval-tsg)
- [Learn more about the evaluation metrics](../../concepts/evaluation-metrics-built-in.md)
- [Evaluate your Generative AI applications remotely on the cloud](./cloud-evaluation.md)
- [Learn more about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View your evaluation results in an Azure AI project](../../how-to/evaluate-results.md)
- [Get started building a chat app by using the Azure AI Foundry SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)
