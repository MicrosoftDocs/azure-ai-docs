---
title: Agent Evaluation with the Azure AI Evaluation SDK
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to evaluate an AI agent with the Azure AI Evaluation SDK.
ms.service: azure-ai-foundry
ms.custom: 
- build-2025
- references_regions
ms.topic: how-to
ms.date: 09/15/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---

# Evaluate your AI agents locally with the Azure AI Evaluation SDK (preview)

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

AI agents are powerful productivity assistants that can create workflows for business needs. However, observability can be a challenge, due to their complex interaction patterns. In this article, you learn how to run built-in evaluators locally on simple agent data or agent messages.

To build production-ready agentic applications and enable observability and transparency, developers need tools to assess not just the final output from an agent's workflows, but the quality and efficiency of the workflows themselves.

An event like a user querying "weather tomorrow" triggers an agentic workflow. To produce a final response, the agentic workflow runs multiple steps that include reasoning through user intents, tool calling, and utilizing retrieval-augmented generation. In this process, it's crucial to evaluate each step of the workflow, and the quality and safety of the final output. We formulate these evaluation aspects into the following evaluators for agents:

- [Intent resolution](https://aka.ms/intentresolution-sample): Measures whether the agent correctly identifies the user's intent.
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample): Measures whether the agent made the correct function tool calls to a user's request.
- [Task adherence](https://aka.ms/taskadherence-sample): Measures whether the agent's final response adheres to its assigned tasks, according to its system message and prior steps.

You can also assess other quality and safety aspects of your agentic workflows, using our comprehensive suite of built-in evaluators. In general, agents emit agent messages. Transforming agent messages into the right evaluation data to use our evaluators can be a nontrivial task. If you build your agent using [Foundry Agent Service](../../../ai-services/agents/overview.md), you can [seamlessly evaluate it via our converter support](#evaluate-azure-ai-agents). If you build your agent outside of Foundry Agent Service, you can still use our evaluators as appropriate to your agentic workflow, by parsing your agent messages into the [required data formats](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). See examples in [Evaluating other agents](#evaluating-other-agents).

## Get started

Install the evaluators package from the Azure AI evaluation SDK:

```python
pip install azure-ai-evaluation
```

## Evaluate Azure AI agents

If you use [Foundry Agent Service](../../../ai-services/agents/overview.md), you can seamlessly evaluate your agents using our converter support for Azure AI agents and Semantic Kernel agents. The following evaluators are supported for evaluation data returned by the converter: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, and `Groundedness`.

> [!NOTE]
> If you are building other agents that output a different schema, you can convert them into the general openai-style [agent message schema](#agent-message-schema) and use the above evaluators.
> More generally, if you can parse the agent messages into the [required data formats](./evaluate-sdk.md#data-requirements-for-built-in-evaluators), you can also all of our evaluators.

### Model support for AI-assisted evaluators

We support AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the LLM-judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o, etc.) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other evaluators| Not Supported | Supported | -- |

For complex evaluation that requires refined reasoning, we recommend a strong reasoning model like `4.1-mini` with a balance of reasoning performance and cost efficiency.



#### Tool call evaluation support
`ToolCallAccuracyEvaluator` supports evaluation in Azure AI Agent for the following tools:

- File Search
- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent 
- OpenAPI   
- Function Tool (user-defined tools)

However, if a non-supported tool is used in the agent run, it outputs a "pass" and a reason that evaluating the invoked tool(s) isn't supported, for ease of filtering out these cases. It is recommended that you wrap non-supported tools as user-defined tools to enable evaluation.

Here's an example that shows you how to seamlessly build and evaluate an Azure AI agent. Separately from evaluation, Azure AI Foundry Agent Service requires `pip install azure-ai-projects azure-identity`, an Azure AI project connection string, and the supported models.

### Create agent threads and runs

Agents can use tool. Here's an example of creating custom tools you intend the agent to use (using a mock weather function as an example):

```python
from azure.ai.projects.models import FunctionTool, ToolSet
from typing import Set, Callable, Any
import json

# Define a custom Python function.
def fetch_weather(location: str) -> str:
    """
    Fetches the weather information for the specified location.

    :param location (str): The location to fetch weather for.
    :return: Weather information as a JSON string.
    :rtype: str
    """
    # In a real-world scenario, you'd integrate with a weather API.
    # In the following code snippet, we mock the response.
    mock_weather_data = {"Seattle": "Sunny, 25°C", "London": "Cloudy, 18°C", "Tokyo": "Rainy, 22°C"}
    weather = mock_weather_data.get(location, "Weather data not available for this location.")
    weather_json = json.dumps({"weather": weather})
    return weather_json

user_functions: Set[Callable[..., Any]] = {
    fetch_weather,
}

# Add tools that the agent will use. 
functions = FunctionTool(user_functions)

toolset = ToolSet()
toolset.add(functions)

AGENT_NAME = "Seattle Tourist Assistant"
```

If you're using [Azure AI Foundry (non-Hub) project](../create-projects.md?tabs=ai-foundry), create an agent with the toolset as follows:

> [!NOTE]
> If you're using a [Foundry Hub-based project](../hub-create-projects.md?tabs=ai-foundry) (which only supports lower versions of `azure-ai-projects<1.0.0b10 azure-ai-agents<1.0.0b10`), we strongly recommend migrating to [the latest Foundry Agent Service SDK Python client library](../../agents/quickstart.md?pivots=programming-language-python-azure) with a [Foundry project set up for logging batch evaluation results](../../how-to/develop/evaluate-sdk.md#prerequisite-set-up-steps-for-azure-ai-foundry-projects).

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
# Azure AI Foundry project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
project_endpoint = os.environ["AZURE_AI_PROJECT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)


# Create an agent with the toolset 
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
    name="my-agent",  # Name of the agent
    instructions="You are a helpful agent",  # Instructions for the agent
    toolset=toolset
)
print(f"Created agent, ID: {agent.id}")

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Add a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="What is the weather in Seattle today?",  # Message content
)
print(f"Created message, ID: {message['id']}")

# Create and process an agent run
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message.role}, Content: {message.content}")
    
```

### Evaluate a single agent run

After you create agent runs, you can easily use our converter to transform the Azure AI agent thread data into the required evaluation data that the evaluators can understand.

```python
import json, os
from azure.ai.evaluation import AIAgentConverter, IntentResolutionEvaluator

# Initialize the converter for Azure AI agents.
converter = AIAgentConverter(project_client)

# Specify the thread and run ID.
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)
```

And that's it! `converted_data` contains all inputs required for [these evaluators](#evaluate-azure-ai-agents). You don't need to read the input requirements for each evaluator and do any work to parse the inputs. All you need to do is select your evaluator and call the evaluator on this single run. We support AzureOpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o, etc.) | To enable |
|--|--|--|--|
| All quality evaluators except for `GroundednessProEvaluator` | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| `GroundednessProEvaluator` | User does not need to support model | User does not need to support model | -- |

For complex tasks that require refined reasoning for the evaluation, we recommend a strong reasoning model like `o3-mini` or the o-series mini models released afterwards with a balance of reasoning performance and cost efficiency.

We set up a list of quality and safety evaluators in `quality_evaluators` and `safety_evaluators` and reference them in [evaluating multiples agent runs or a thread](#evaluate-multiple-agent-runs-or-threads).

```python
# This is specific to agentic workflows.
from azure.ai.evaluation import IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator 
# Other quality, risk, and safety metrics:
from azure.ai.evaluation import RelevanceEvaluator, CoherenceEvaluator, CodeVulnerabilityEvaluator, ContentSafetyEvaluator, IndirectAttackEvaluator, FluencyEvaluator
from azure.identity import DefaultAzureCredential

import os
from dotenv import load_dotenv
load_dotenv()

model_config = {
    "azure_deployment": os.getenv("AZURE_DEPLOYMENT_NAME"),
    "api_key": os.getenv("AZURE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "api_version": os.getenv("AZURE_API_VERSION"),
}

# example config for a reasoning model
reasoning_model_config = {
    "azure_deployment": "o3-mini",
    "api_key": os.getenv("AZURE_API_KEY"),
    "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
    "api_version": os.getenv("AZURE_API_VERSION"),
}

# Evaluators you might want to use with reasoning models 
quality_evaluators = {evaluator.__name__: evaluator(model_config=reasoning_model_config, is_reasoning_model=True) for evaluator in [IntentResolutionEvaluator, TaskAdherenceEvaluator, ToolCallAccuracyEvaluator]}

# Other evaluators you might NOT want to use with reasoning models 
quality_evaluators.update({ evaluator.__name__: evaluator(model_config=model_config) for evaluator in [CoherenceEvaluator, FluencyEvaluator, RelevanceEvaluator]})

## Using Azure AI Foundry (non-Hub) project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

safety_evaluators = {evaluator.__name__: evaluator(azure_ai_project=azure_ai_project, credential=DefaultAzureCredential()) for evaluator in [ContentSafetyEvaluator, IndirectAttackEvaluator, CodeVulnerabilityEvaluator]}

# Reference the quality and safety evaluator list above.
quality_and_safety_evaluators = {**quality_evaluators, **safety_evaluators}

for name, evaluator in quality_and_safety_evaluators.items():
    result = evaluator(**converted_data)
    print(name)
    print(json.dumps(result, indent=4)) 

```

#### Output format

AI-assisted quality evaluators provide a result for a query and response pair. The result is a dictionary that contains:

- `{metric_name}`: Provides a numerical score, on a Likert scale (integer 1 to 5) or a float between 0 and 1.
- `{metric_name}_label`: Provides a binary label (if the metric naturally outputs a binary score).
- `{metric_name}_reason`: Explains why a certain score or label was given for each data point.
- `details`: Optional output containing debugging information about the quality of a single agent run.

To further improve intelligibility, all evaluators accept a binary threshold (unless their outputs are already binary) and output two new keys. For the binarization threshold, a default is set, which the user can override. The two new keys are:

- `{metric_name}_result`: A "pass" or "fail" string based on a binarization threshold.
- `{metric_name}_threshold`: A numerical binarization threshold set by default or by the user.

See the following example output for some evaluators:

```
{
    "intent_resolution": 5.0, # likert scale: 1-5 integer 
    "intent_resolution_threshold": 3,
    "intent_resolution_result": "pass", # pass because 5 > 3 the threshold
    "intent_resolution_reason": "The assistant correctly understood the user's request to fetch the weather in Seattle. It used the appropriate tool to get the weather information and provided a clear and accurate response with the current weather conditions in Seattle. The response fully resolves the user's query with all necessary information."
}
{
    "task_adherence": 5.0, # likert scale: 1-5 integer 
    "task_adherence_threshold": 3,
    "task_adherence_result": "pass", # pass because 5 > 3 the threshold
    "task_adherence_reason": "The response accurately follows the instructions, fetches the correct weather information, and relays it back to the user without any errors or omissions."
}
{
    "tool_call_accuracy": 5,  # a score between 1-5, higher is better
    "tool_call_accuracy_threshold": 3,
    "tool_call_accuracy_result": "pass", # pass because 5 > 3 the threshold
    "details": { ... } # helpful details for debugging the tool calls made by the agent
}
```

### Evaluate multiple agent runs or threads

To evaluate multiple agent runs or threads, we recommend using the batch `evaluate()` API for asynchronous evaluation. First, convert your agent thread data into a file via our converter support:

```python
import json
from azure.ai.evaluation import AIAgentConverter

# Initialize the converter.
converter = AIAgentConverter(project_client)

# Specify a file path to save the agent output (evaluation input data) to.
filename = os.path.join(os.getcwd(), "evaluation_input_data.jsonl")

evaluation_data = converter.prepare_evaluation_data(thread_ids=thread_id, filename=filename) 

print(f"Evaluation data saved to {filename}")
```

With the evaluation data prepared in one line of code, you can select the evaluators to assess the agent quality and submit a batch evaluation run. In the following example, we reference the same list of quality and safety evaluators in section [Evaluate a single agent run](#evaluate-a-single-agent-run) `quality_and_safety_evaluators`:  

```python
import os
from dotenv import load_dotenv
load_dotenv()


# Batch evaluation API (local):
from azure.ai.evaluation import evaluate

response = evaluate(
    data=filename,
    evaluation_name="agent demo - batch run",
    evaluators=quality_and_safety_evaluators,
    # optionally, log your results to your Azure AI Foundry project for rich visualization 
    azure_ai_project=os.environ.get("AZURE_AI_PROJECT"),  # example: https://your-account.services.ai.azure.com/api/projects/your-project
)
# Inspect the average scores at a high level.
print(response["metrics"])
# Use the URL to inspect the results on the UI.
print(f'AI Foundry URL: {response.get("studio_url")}')
```

After the URL, you'll be redirected to Foundry. You can view your evaluation results in your Azure AI project and debug your application. Using reason fields and pass/fail, you can easily assess the quality and safety performance of your applications. You can run and compare multiple runs to test for regression or improvements.  

With the Azure AI Evaluation SDK client library, you can seamlessly evaluate your Azure AI agents via our converter support, which enables observability and transparency into agentic workflows.

## <a name = "evaluating-other-agents"></a> Evaluate other agents

If you're using agents outside Azure AI Foundry Agent Service, you can still evaluate them by preparing the right data for the evaluators of your choice.

Agents typically emit messages to interact with a user or other agents. Our built-in evaluators can accept simple data types such as strings in `query`, `response`, and `ground_truth` according to the [single-turn data input requirements](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). However, it can be a challenge to extract these simple data types from agent messages, due to the complex interaction patterns of agents and framework differences. For example, a single user query can trigger a long list of agent messages, typically with multiple tool calls invoked.

As illustrated in the following example, we enable agent message support for the following built-in evaluators to evaluate these aspects of agentic workflow. These evaluators may take `tool_calls` or `tool_definitions` as parameters unique to agents when evaluating agents.

| Evaluator       | `query`      | `response`      | `tool_calls`       | `tool_definitions`  |
|----------------|---------------|---------------|---------------|---------------|
| `IntentResolutionEvaluator`   | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |
| `ToolCallAccuracyEvaluator`   | Required: `Union[str, list[Message]]` | Optional: `Union[str, list[Message]]`  | Optional: `Union[dict, list[ToolCall]]` | Required: `list[ToolDefinition]`  |
| `TaskAdherenceEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |
| `GroundednessEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Required: `list[ToolCall]`  |

- `Message`: `dict` OpenAI-style message that describes agent interactions with a user, where the `query` must include a system message as the first message.
- `ToolCall`: `dict` that specifies tool calls invoked during agent interactions with a user.
- `ToolDefinition`: `dict` that describes the tools available to an agent.

For `ToolCallAccuracyEvaluator`, either `response` or  `tool_calls` must be provided.

`GroundednessEvaluator` requires `tool_definitions` to be provided to evaluate the groundedness of the agent's responses with respect to the tool outputs the agent receives.

Following are examples of the two data formats: simple agent data, and agent messages. However, due to the unique requirements of these evaluators, we recommend referring to the [Sample notebooks](#sample-notebooks), which illustrate the possible input paths for each evaluator.  

As with other [built-in AI-assisted quality evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md), `IntentResolutionEvaluator` and `TaskAdherenceEvaluator` output a Likert score (integer 1-5; higher score is better). `ToolCallAccuracyEvaluator` outputs the passing rate of all tool calls made (a float between 0 and 1) based on user query. To further improve intelligibility, all evaluators accept a binary threshold and output two new keys. For the binarization threshold, a default is set and the user can override it. The two new keys are:

- `{metric_name}_result`: A "pass" or "fail" string based on a binarization threshold.
- `{metric_name}_threshold`: A numerical binarization threshold set by default or by the user.

### Simple agent data

In simple agent data format, `query` and `response` are simple Python strings. For example:  

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

# Evaluate the query and response as strings.
# The following is a positive example. Intent is identified and understood and the response correctly resolves user intent.
result = intent_resolution_evaluator(
    query="What are the opening hours of the Eiffel Tower?",
    response="Opening hours of the Eiffel Tower are 9:00 AM to 11:00 PM.",
)
print(json.dumps(result, indent=4))
 
```

See the following output (reference [Output format](#output-format) for details):

```
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response provides the opening hours of the Eiffel Tower, which directly addresses the user's query. The information is clear, accurate, and complete, fully resolving the user's intent.",
}
```

### Agent tool calls and definitions

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

from azure.ai.evaluation import ToolCallAccuracyEvaluator

tool_call_accuracy = ToolCallAccuracyEvaluator(model_config) # reuse the config defined above
response = tool_call_accuracy(query=query, tool_calls=tool_calls, tool_definitions=tool_definitions)
print(json.dumps(response, indent=4))
```

See the following output (reference [Output format](#output-format) for details):

```
{
    "tool_call_accuracy": 3,  # a score between 1-5, higher is better
    "tool_call_accuracy_result": "fail",
    "tool_call_accuracy_threshold": 4,
    "details": { ... } # helpful details for debugging the tool calls made by the agent
}
```

### Agent message schema

In agent message format, `query` and `response` are a list of OpenAI-style messages. Specifically, `query` carries the past agent-user interactions leading up to the last user query and requires the system message (of the agent) on top of the list; and `response` carries the last message of the agent in response to the last user query. 

The expected input format for the evaluators is a Python list of messages as follows:

```
[
  {
    "role": "system" | "user" | "assistant" | "tool",
    "createdAt": "ISO 8601 timestamp",     // Optional for 'system'
    "run_id": "string",                    // Optional, only for assistant/tool in tool call context
    "tool_call_id": "string",              // Optional, only for tool/tool_result
    "name": "string",                      // Present if it's a tool call
    "arguments": { ... },                  // Parameters passed to the tool (if tool call)
    "content": [
      {
        "type": "text" | "tool_call" | "tool_result",
        "text": "string",                  // if type == text
        "tool_call_id": "string",         // if type == tool_call
        "name": "string",                 // tool name if type == tool_call
        "arguments": { ... },             // tool args if type == tool_call
        "tool_result": { ... }            // result if type == tool_result
      }
    ]
  }
]
```

Sample query and response objects:

```python
query = [
    {
        "role": "system",
        "content": "You are an AI assistant interacting with Azure Maps services to serve user requests."
    },
    {
        "createdAt": "2025-04-25T23:55:43Z",
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Find the address for coordinates 41.8781,-87.6298."
            }
        ]
    },
    {
        "createdAt": "2025-04-25T23:55:45Z",
        "run_id": "run_DGE8RWPS8A9SmfCg61waRx9u",
        "role": "assistant",
        "content": [
            {
                "type": "tool_call",
                "tool_call_id": "call_nqNyhOFRw4FmF50jaCCq2rDa",
                "name": "azure_maps_reverse_address_search",
                "arguments": {
                    "lat": "41.8781",
                    "lon": "-87.6298"
                }
            }
        ]
    },
    {
        "createdAt": "2025-04-25T23:55:47Z",
        "run_id": "run_DGE8RWPS8A9SmfCg61waRx9u",
        "tool_call_id": "call_nqNyhOFRw4FmF50jaCCq2rDa",
        "role": "tool",
        "content": [
            {
                "type": "tool_result",
                "tool_result": {
                    "address": "300 South Federal Street, Chicago, IL 60604",
                    "position": {
                        "lat": "41.8781",
                        "lon": "-87.6298"
                    }
                }
            }
        ]
    },
    {
        "createdAt": "2025-04-25T23:55:48Z",
        "run_id": "run_DGE8RWPS8A9SmfCg61waRx9u",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The address for the coordinates 41.8781, -87.6298 is 300 South Federal Street, Chicago, IL 60604."
            }
        ]
    },
    {
        "createdAt": "2025-04-25T23:55:50Z",
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What timezone corresponds to 41.8781,-87.6298?"
            }
        ]
    },
]

response = [
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
]
```

> [!NOTE]
> The evaluator throws a warning that query (the conversation history till the current run) or agent response (the response to the query) can't be parsed when their format isn't the expected one.

See an example of evaluating the agent messages with `ToolCallAccuracyEvaluator`:

```python
import json

# The user asked a question.
query = [
    {
        "role": "system",
        "content": "You are a friendly and helpful customer service agent."
    },
    # Past interactions are omitted. 
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
# The agent emits multiple messages to fulfill the request.
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
    # Many more messages are omitted. 
    # ...
    # Here is the agent's final response:
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

# An example of tool definitions available to the agent:
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
    # Other tool definitions are omitted. 
    # ...
]

result = tool_call_accuracy(
    query=query,
    response=response,
    tool_definitions=tool_definitions 
)
print(json.dumps(result, indent=4))

```

See the following output (reference [Output format](#output-format) for details):

```
{
    "tool_call_accuracy": 2,  # a score between 1-5, higher is better
    "tool_call_accuracy_result": "fail",
    "tool_call_accuracy_threshold": 3,
    "details": { ... } # helpful details for debugging the tool calls made by the agent
}
```

This evaluation schema helps you parse your agent data outside Azure AI Foundry Agent Service, so that you can use our evaluators to support observability into your agentic workflows.

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
