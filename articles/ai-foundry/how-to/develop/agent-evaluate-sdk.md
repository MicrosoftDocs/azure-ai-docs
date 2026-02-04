---
title: Agent Evaluation with the Microsoft Foundry SDK
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to evaluate an AI agent with the Microsoft Foundry SDK
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.custom: 
- build-2025
- references_regions
ms.topic: how-to
ms.date: 11/25/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
# customer intent: As a developer, I want to evaluate my AI agents using the Microsoft Foundry SDK so I can assess the quality, safety, and efficiency of agentic workflows.
ai-usage: ai-assisted
---

# Evaluate your AI agents (preview)

[!INCLUDE [version-banner](../../includes/version-banner.md)]

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

AI agents are powerful productivity assistants that create workflows for business needs. However, observability is challenging because of their complex interaction patterns. In this article, you learn how to evaluate Microsoft Foundry agents or other agents using built-in evaluators.

To build production-ready agentic applications and ensure observability and transparency, developers need tools to assess not only the final output of an agent's workflows but also the quality and efficiency of the workflows.

An event like a user querying "weather tomorrow" triggers an agentic workflow. To produce a final response, the workflow includes reasoning through user intents, calling tools, and using retrieval-augmented generation.

[!INCLUDE [evaluation-preview](../../includes/evaluation-preview.md)]

::: moniker range="foundry-classic"

In this process, evaluating each step of the workflow and the quality and safety of the final output is crucial.
We formulate these evaluation aspects into the following evaluators for agents:

- [Intent resolution](https://aka.ms/intentresolution-sample): Measures whether the agent correctly identifies the user's intent.
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample): Measures whether the agent made the correct function tool calls to a user's request.
- [Task adherence](https://aka.ms/taskadherence-sample): Measures whether the agent's final response adheres to its assigned tasks, according to its system message and prior steps.

Assess other quality and safety aspects of your agentic workflows using our comprehensive suite of built-in evaluators. In general, agents emit agent messages. Transforming agent messages into the correct evaluation data for our evaluators can be challenging. If you build your agent using [Foundry Agent Service](../../../ai-services/agents/overview.md), you can [seamlessly evaluate it via our converter support](#evaluate-microsoft-foundry-agents). If you build your agent outside of Foundry Agent Service, you can still use our evaluators as appropriate to your agentic workflow, by parsing your agent messages into the [required data formats](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). See examples in [evaluating other agents](#evaluating-other-agents).

::: moniker-end

::: moniker range="foundry"

As a best practice, it's crucial to perform:

- **System Evaluation**: assess the overall quality and efficiency of the agent's workflow; and
- **Process Evaluation**: evaluate tool calling steps of the workflow.

See [agent evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) for detailed information about the use case of the two practices and a sample of each agent evaluator.

You can also assess other quality and safety aspects of your agentic workflows, using our [comprehensive suite of built-in evaluators](../../concepts/observability.md#what-are-evaluators) or write [custom evaluators](../../concepts/evaluation-evaluators/custom-evaluators.md).

If you're building Foundry Agents, you can [seamlessly evaluate them](#evaluate-microsoft-foundry-agents).

If you build your agents outside of Foundry, you can still use our evaluators as appropriate to your agentic workflow, by parsing your agent messages into the required data formats. See details in [Evaluating other agents](#evaluating-other-agents).

::: moniker-end

## Get started

::: moniker range="foundry-classic"

Install the evaluators package from the Azure AI evaluation SDK:

```python
pip install azure-ai-evaluation
```

::: moniker-end

::: moniker range="foundry"

Install the package from the Azure AI evaluation SDK:

```bash
pip install "azure-ai-projects>=2.0.0b1" azure-identity python-dotenv
```

Set these environment variables with your values in a `.env` file:

```python
AZURE_AI_PROJECT_ENDPOINT="<your-endpoint>" # The Azure AI Project project endpoint, as found in the Home page of your Microsoft Foundry portal.
AZURE_AI_MODEL_DEPLOYMENT_NAME="<your-model-deployment-name>" # The deployment name of the AI model, as found under the "Build" page in the "Models" tab in your Foundry project.
```

::: moniker-end

## Evaluate Microsoft Foundry agents

::: moniker range="foundry-classic"

If you use [Foundry Agent Service](../../../ai-services/agents/overview.md), you can seamlessly evaluate your agents by using our converter support for Microsoft Foundry agents and Semantic Kernel agents. The following evaluators support evaluation data returned by the converter: `IntentResolution`, `ToolCallAccuracy`, `TaskAdherence`, `Relevance`, and `Groundedness`.

> [!NOTE]
> If you're building other agents that output a different schema, convert them into the general OpenAI-style [agent message schema](#agent-message-schema) and use the preceding evaluators.
> More generally, if you can parse the agent messages into the [required data formats](./evaluate-sdk.md#data-requirements-for-built-in-evaluators), you can also use all of our evaluators.

### Model support for AI-assisted evaluators

AzureOpenAI and OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models support the LLM-judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o, etc.) | To enable |
|--|--|--|--|
| `IntentResolution`, `TaskAdherence`, `ToolCallAccuracy`, `ResponseCompleteness`, `Coherence`, `Fluency`, `Similarity`, `Groundedness`, `Retrieval`, `Relevance`  | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| Other evaluators| Not Supported | Supported |--|

For complex evaluation that requires refined reasoning, use a strong reasoning model like `4.1-mini` for a balance of reasoning performance and cost efficiency.

#### Tool call evaluation support

`ToolCallAccuracyEvaluator` supports evaluation in Microsoft Foundry Agent for the following tools:

- File Search
- Azure AI Search
- Bing Grounding
- Bing Custom Search
- SharePoint Grounding
- Code Interpreter
- Fabric Data Agent
- OpenAPI
- Function Tool (user-defined tools)

However, if you use a non-supported tool in the agent run, the evaluator outputs a "pass" and a reason that evaluating the invoked tools isn't supported, for ease of filtering out these cases. To enable evaluation, wrap non-supported tools as user-defined tools.

This example shows how to build and evaluate a Microsoft Foundry agent. Separately from evaluation, Foundry Agent Service requires `pip install azure-ai-projects azure-identity`, a Foundry project connection string, and the supported models.

### Create agent threads and runs

Agents can use tools. Here's an example of creating custom tools for the agent to use (using a mock weather function as an example):

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

If you use a [Foundry (non-Hub) project](../create-projects.md?tabs=ai-foundry), create an agent with the toolset as follows:

> [!NOTE]
> If you're using a [Foundry Hub-based project](../hub-create-projects.md?tabs=ai-foundry) (which only supports lower versions of `azure-ai-projects<1.0.0b10 azure-ai-agents<1.0.0b10`), we strongly recommend migrating to [the latest Foundry Agent Service SDK Python client library](../../agents/quickstart.md?pivots=programming-language-python-azure) with a [Foundry project set up for logging batch evaluation results](../../how-to/develop/evaluate-sdk.md#prerequisite-set-up-steps-for-microsoft-foundry-projects).

Create an agent with the toolset as follows:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

load_dotenv()

# Create an Azure AI Client from an endpoint, copied from your Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
# Foundry project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
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

After you create agent runs, you can use our converter to transform the Microsoft Foundry agent thread data into the required evaluation data that evaluators can understand.

```python
import json, os
from azure.ai.evaluation import AIAgentConverter, IntentResolutionEvaluator

# Initialize the converter for Microsoft Foundry agents.
converter = AIAgentConverter(project_client)

# Specify the thread and run ID.
thread_id = thread.id
run_id = run.id

converted_data = converter.convert(thread_id, run_id)
```

That's it! `converted_data` contains all inputs required for these evaluators. You don't need to read the input requirements for each evaluator or do any work to parse the inputs. Select your evaluator and call the evaluator on this single run. We support Azure OpenAI or OpenAI [reasoning models](../../../ai-services/openai/how-to/reasoning.md) and non-reasoning models for the judge depending on the evaluators:

| Evaluators | Reasoning Models as Judge (example: o-series models from Azure OpenAI / OpenAI) | Non-reasoning models as Judge (example: gpt-4.1, gpt-4o, etc.) | To enable |
|--|--|--|--|
| All quality evaluators except for `GroundednessProEvaluator` | Supported | Supported | Set additional parameter `is_reasoning_model=True` in initializing evaluators |
| `GroundednessProEvaluator` | User doesn't need to support model | User doesn't need to support model |--|

For complex tasks that require refined reasoning for the evaluation, we recommend a strong reasoning model like `o3-mini` or the o-series mini models released afterward with a balance of reasoning performance and cost efficiency.

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

## Using Foundry (non-Hub) project endpoint, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
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

AI-assisted quality evaluators return a result for a query and response pair. The result is a dictionary that includes:

- `{metric_name}`: Provides a numerical score, on a Likert scale (integer 1 to 5) or a float between 0 and 1.
- `{metric_name}_label`: Provides a binary label (if the metric naturally outputs a binary score).
- `{metric_name}_reason`: Explains why a certain score or label was given for each data point.
- `details`: Optional output containing debugging information about the quality of a single agent run.

To improve clarity, all evaluators accept a binary threshold (unless their outputs are already binary) and generate two new keys. For the binarization threshold, a default is set, which the user can override. The two new keys are:

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

To evaluate multiple agent runs or threads, use the batch `evaluate()` API for asynchronous evaluation. First, convert your agent thread data into a file by using our converter support:

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
    # optionally, log your results to your Foundry project for rich visualization 
    azure_ai_project=os.environ.get("AZURE_AI_PROJECT"),  # example: https://your-account.services.ai.azure.com/api/projects/your-project
)
# Inspect the average scores at a high level.
print(response["metrics"])
# Use the URL to inspect the results on the UI.
print(f'Foundry URL: {response.get("studio_url")}')
```

After selecting the URL, you're redirected to Foundry. View your evaluation results in your Foundry project and debug your application. Use reason fields and pass/fail results to assess the quality and safety performance of your applications. You can run and compare multiple runs to test for regression or improvements.  

Use the Azure AI Evaluation SDK client library to evaluate your Microsoft Foundry agents with converter support, enabling observability and transparency into agent workflows.

::: moniker-end

::: moniker range="foundry"

You can seamlessly evaluate Foundry agents by using evaluators in [Agent Evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) and [RAG evaluators](../../concepts/evaluation-evaluators/rag-evaluators.md). This section walks you through creating an agent and evaluating it.

> [!NOTE]
> If you're building other agents that output a different schema, convert them into the general OpenAI-style [agent message schema](#agent-message-schema) and use the preceding evaluators.
> More generally, if you can parse the agent messages into the required data formats, you can also use all of our evaluators.

### Prerequisites

```python
import json
from azure.ai.projects.models import Tool, FunctionTool

# Define a function tool for the model to use
func_tool = fetch_weather(
    name="fetch_weather",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to fetch weather for.",
            },
        },
        "required": ["location"],
        "additionalProperties": False,
    },
    description="Get the current weather for a location.",
    strict=True,
)

tools: list[Tool] = [func_tool]

# Define a custom Python function.
async def fetch_weather(location: str) -> str:
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

```

Set up an agent with the toolset and create a response run to evaluate.

Create an agent with the toolset as follows:

```python
import os
import json
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential
from openai.types.responses.response_input_param import FunctionCallOutput, ResponseInputParam

credential = DefaultAzureCredential()


project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with project_client:

    openai_client = project_client.get_openai_client()

    agent = await project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful assistant that can use function tools.",
            tools=tools,
        ),
    )

    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    conversation = openai_client.conversations.create(
        items=[{"type": "message", "role": "user", "content": "What is the weather in Seattle?"}],
    )
    print(f"Created conversation with initial user message (id: {conversation.id})")

    response = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response output: {response.output_text} (id: {response.id})")


    # Now create evaluation for the response
    data_source_config = {"type": "azure_ai_source", "scenario": "responses"}

    # add your desired evaluators here
    testing_criteria = [
        {"type": "azure_ai_evaluator", "name": "task_adherence", "evaluator_name": "builtin.task_adherence"},
        {"type": "azure_ai_evaluator", "name": "groundedness", "evaluator_name": "builtin.groundedness"},
    ]
    eval_object = openai_client.evals.create(
        name="Agent Response Evaluation",
        data_source_config=data_source_config,
        testing_criteria=testing_criteria,
    )
    print(f"Evaluation created (id: {eval_object.id}, name: {eval_object.name})")

    data_source = {
        "type": "azure_ai_responses",
        "item_generation_params": {
            "type": "response_retrieval",
            "data_mapping": {"response_id": "{{item.resp_id}}"},
            "source": {"type": "file_content", "content": [{"item": {"resp_id": response.id}}]},
        },
    }

    response_eval_run = openai_client.evals.runs.create(
        eval_id=eval_object.id, name=f"Evaluation Run for Agent {agent.name}", data_source=data_source
    )
    print(f"Evaluation run created (id: {response_eval_run.id})")

    while response_eval_run.status not in ["completed", "failed"]:
        response_eval_run = openai_client.evals.runs.retrieve(run_id=response_eval_run.id, eval_id=eval_object.id)
        print(f"Waiting for eval run to complete... current status: {response_eval_run.status}")
        time.sleep(5)

    if response_eval_run.status == "completed":
        print("\n✓ Evaluation run completed successfully!")
        print(f"Result Counts: {response_eval_run.result_counts}")
        print(f"Eval Run Report URL: {response_eval_run.report_url}")
        output_items = list(
            openai_client.evals.runs.output_items.list(run_id=response_eval_run.id, eval_id=eval_object.id)
        )
        print(f"\nOUTPUT ITEMS (Total: {len(output_items)})")
        print(f"{'-'*60}")
        pprint(output_items)
        print(f"{'-'*60}")
    else:
        print("\n✗ Evaluation run failed.")

```

### Interpretation of results

For a single data example, all evaluators always output the following schema:  

- **Label**: a binary "pass" or "fail" label, similar to a unit test's output. Use this result to facilitate comparisons across evaluators.
- **Score**: a score from the natural scale of each evaluator. Some evaluators use a fine-grained rubric, scoring on a 5-point scale (quality evaluators) or a 7-point scale (content safety evaluators). Others, like textual similarity evaluators, use F1 scores, which are floats between 0 and 1. The "label" field binarizes any non-binary "score" to "pass" or "fail" based on the "threshold".
- **Threshold**: any non-binary scores are binarized to "pass" or "fail" based on a default threshold, which you can override in the SDK experience.
- **Reason**: To improve intelligibility, all LLM-judge evaluators also output a reasoning field to explain why a certain score is given.
- **Details**: (optional) For some evaluators, such as tool_call_accuracy, there might be a "details" field or flags that contain additional information to help users debug their applications.
For aggregate results over multiple data examples (a dataset), the average rate of the examples with a "pass" forms the passing rate for that dataset.

After the URL, you're redirected to Foundry. You can view your evaluation results in your Foundry project and debug your application. Use "reason" fields and pass/fail to assess the quality and safety performance of your applications. You can run and compare multiple runs to test for regression or improvements.  

Use the Microsoft Foundry SDK Python client library to evaluate your Microsoft Foundry agents, enabling observability and transparency in agent workflows.

::: moniker-end

## <a name = "evaluating-other-agents"></a> Evaluate other agents

::: moniker range="foundry-classic"

If you use agents outside Agent Service, you can still evaluate them by preparing the right data for the evaluators of your choice.

Agents typically emit messages to interact with a user or other agents. Built-in evaluators accept simple data types such as strings in `query`, `response`, and `ground_truth` according to the [single-turn data input requirements](./evaluate-sdk.md#data-requirements-for-built-in-evaluators). However, extracting these simple data types from agent messages can be challenging due to the complex interaction patterns of agents and framework differences. For example, a single user query can trigger a long list of agent messages, typically with multiple tool calls invoked.

::: moniker-end

::: moniker range="foundry"

Agents typically emit messages to interact with a user or other agents. Our built-in evaluators can accept simple data types such as strings in `query`, `response`, and `ground_truth` according to the single-turn data input requirements. However, it can be a challenge to extract these simple data types from agent messages, due to the complex interaction patterns of agents and framework differences. For example, a single user query can trigger a long list of agent messages, typically with multiple tool calls invoked. We show examples of agent message schema in [Agent message schema](#agent-message-schema) with `tool_definitions` and `tool_calls` embedded in `query` and `response`. 

::: moniker-end

::: moniker range="foundry-classic"

As illustrated in the following example, we enable agent message support for the following built-in evaluators to evaluate these aspects of agentic workflow. These evaluators might take `tool_calls` or `tool_definitions` as parameters unique to agents when evaluating agents.

| Evaluator       | `query`      | `response`      | `tool_calls`       | `tool_definitions`  |
|----------------|---------------|---------------|---------------|---------------|
| `IntentResolutionEvaluator`   | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |
| `ToolCallAccuracyEvaluator`   | Required: `Union[str, list[Message]]` | Optional: `Union[str, list[Message]]`  | Optional: `Union[dict, list[ToolCall]]` | Required: `list[ToolDefinition]`  |
| `TaskAdherenceEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Optional: `list[ToolCall]`  |
| `GroundednessEvaluator`         | Required: `Union[str, list[Message]]` | Required: `Union[str, list[Message]]`  | Doesn't apply | Required: `list[ToolCall]`  |

- `Message`: `dict` OpenAI-style message that describes agent interactions with a user, where the `query` must include a system message as the first message.
- `ToolCall`: `dict` that specifies tool calls invoked during agent interactions with a user.
- `ToolDefinition`: `dict` that describes the tools available to an agent.

For `ToolCallAccuracyEvaluator`, you must provide either `response` or `tool_calls`.

`GroundednessEvaluator` requires `tool_definitions` to evaluate the groundedness of the agent's responses with respect to the tool outputs the agent receives.

The following examples show the two data formats: simple agent data and agent messages. However, due to the unique requirements of these evaluators, we recommend referring to the [Sample notebooks](#sample-notebooks), which illustrate the possible input paths for each evaluator.  

All [built-in AI-assisted quality evaluators](../../concepts/evaluation-evaluators/agent-evaluators.md) output a pass or fail for each input. 


::: moniker-end


::: moniker range="foundry-classic"

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

See the following output (refer to [Output format](#output-format) for details):

```
{
    "intent_resolution": 5.0,
    "intent_resolution_result": "pass",
    "intent_resolution_threshold": 3,
    "intent_resolution_reason": "The response provides the opening hours of the Eiffel Tower, which directly addresses the user's query. The information is clear, accurate, and complete, fully resolving the user's intent.",
}
```

::: moniker-end


### Agent tool calls and definitions

::: moniker range="foundry-classic"

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

::: moniker-end

::: moniker range="foundry"

See the following examples of `tool_calls` and `tool_definitions` for `tool_call_accuracy`:

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
```

::: moniker-end

### Agent message schema

In agent message format, `query` and `response` are a list of OpenAI-style messages. Specifically, `query` carries the past agent-user interactions leading up to the last user query and requires the system message (of the agent) at the top of the list. `response` carries the last message of the agent in response to the last user query. 

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

::: moniker range="foundry-classic"

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
> The evaluator shows a warning if the query (the conversation history up to the current run) or agent response (the response to the query) isn't in the expected format.

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

::: moniker-end

::: moniker range="foundry"

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
> The evaluator throws a warning that it can't parse the query (the conversation history up to the current run) or agent response (the response to the query) when their format isn't the expected one.

More examples of agent messages:

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

```

::: moniker-end

This evaluation schema helps parse agent data outside Agent Service, enabling the use of built-in evaluators to support observability in agent workflows.

## Sample notebooks

::: moniker range="foundry-classic"

Try a sample for each of these evaluators:

- [Intent resolution](https://aka.ms/intentresolution-sample)
- [Tool call accuracy](https://aka.ms/toolcallaccuracy-sample)
- [Task adherence](https://aka.ms/taskadherence-sample)
- [Response completeness](https://aka.ms/rescompleteness-sample)
- [End-to-end Microsoft Foundry agent evaluation](https://aka.ms/e2e-agent-eval-sample)

::: moniker-end

::: moniker range="foundry"

Try a sample for each of these evaluators in the [sample repository](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-projects/samples/evaluations/agentic_evaluators).

::: moniker-end

## Related content

::: moniker range="foundry-classic"

- [Azure AI Evaluation Python SDK client reference documentation](https://aka.ms/azureaieval-python-ref)
- [Azure AI Evaluation SDK client troubleshooting guide](https://aka.ms/azureaieval-tsg)
- [Learn about the evaluation metrics](../../concepts/observability.md)
- [Evaluate Generative AI applications remotely on the cloud](./cloud-evaluation.md)
- [Learn about simulating test datasets for evaluation](./simulator-interaction-data.md)
- [View evaluation results in a Foundry project](../../how-to/evaluate-results.md)
- [Get started building a chat app using the Microsoft Foundry SDK](../../quickstarts/get-started-code.md)
- [Get started with evaluation samples](https://aka.ms/aistudio/eval-samples)

::: moniker-end

::: moniker range="foundry"

- [Azure AI Evaluation SDK client troubleshooting guide](https://aka.ms/azureaieval-tsg)
- [Evaluate Generative AI applications remotely on the cloud](./cloud-evaluation.md)
- [View evaluation results in a Foundry project](../../how-to/evaluate-results.md)

::: moniker-end
