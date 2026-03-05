---
title: "Use LangGraph with the Agent Service (classic)"
description: "Learn how to build LangGraph and LangChain applications with Foundry Agent Service in the classic experience."
ms.service: azure-ai-foundry
ms.custom:
  - classic-and-new
  - dev-focus
ms.topic: how-to
ms.date: 03/05/2026
ms.reviewer: fasantia
ms.author: sgilley
author: sdgilley
ai-usage: ai-assisted
---

# Develop agents with LangGraph and Microsoft Foundry Agent Service (classic)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

Use the `langchain-azure-ai` package to connect LangGraph and LangChain
applications to Foundry Agent Service. This article walks through practical
scenarios, from basic prompt agents to tool-enabled workflows.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A Foundry project in Foundry classic.
- A deployed chat model (for example, `gpt-4.1`) in your project.
- Python 3.10 or later.
- Azure CLI signed in (`az login`) so `DefaultAzureCredential` can authenticate.

### Configure your environment

Install the packages used in this article:

```bash
pip install langchain-azure-ai[tools,v1] azure-ai-agents azure-identity pandas
```

> [!IMPORTANT]
>  Install `[v1]` to include support for Foundry classic.

Install the extras `[tools]` to use tools like Document Intelligence or Azure
Logic Apps connectors.

Set the environment variables used in the samples:

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project>"
export MODEL_DEPLOYMENT_NAME="gpt-4.1"
```

## Create the agent factory

Create an `AgentServiceFactory` by using the v1 integration. Agents created
through this factory are managed in Foundry classic.

```python
import os

from azure.identity import DefaultAzureCredential
from langchain_azure_ai.agents.v1 import AgentServiceFactory

factory = AgentServiceFactory(
    project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
```

**What this snippet does:** Connects the v1 `AgentServiceFactory` to your
project so subsequent LangGraph agents can be created and managed in Foundry
classic.

> [!NOTE]
> Agents created with `langchain_azure_ai.agents.v1.AgentServiceFactory` are
> visible in the Foundry portal (classic).

## Create a basic prompt agent

Start with a minimal prompt agent to validate your setup quickly.

```python
agent = factory.create_prompt_agent(
    name="my-echo-agent",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions=(
        "You are a helpful AI assistant that always replies back saying the "
        "opposite of what the user says."
    ),
    trace=True,
)

print(f"Agent with ID {factory.get_agents_id_from_graph(agent)} created.")
```

```output
Agent with ID {'my-echo-agent:1'} created.
```

Invoke the agent:

```python
from langchain_core.messages import HumanMessage
from langchain_azure_ai.utils.agents import pretty_print

messages = [HumanMessage(content="I'm a genius and I love programming!")]
state = agent.invoke({"messages": messages})

pretty_print(state)
```

```output
================================ Human Message =================================

I'm a genius and I love programming!
================================== Ai Message ==================================
Name: my-echo-agent

You are not a genius and you hate programming!
```

**What this snippet does:** Creates a prompt-based v1 agent in Foundry Agent
Service (classic), invokes it, and prints the full message sequence from the
LangGraph state.

You can visualize how the agent got created and used within the LangGraph
graph by printing its diagram representation. The node `foundryAgent` runs
in the Foundry Agent Service. Notice how the agent name and version is
visible in the graph.

```python
from IPython import display

display.Image(agent.get_graph().draw_mermaid_png())

factory.delete_agent(agent)
```

**What this snippet does:** Renders the graph to show the single Agent Service
node and then deletes the temporary sample agent.

:::image type="content" source="../../../foundry/how-to/media/langchain-azure-ai-agents/agent-no-tools.png" alt-text="Diagram of the agent graph for an agent without tools.":::

## Configure advanced settings

You can configure model behavior and metadata by passing optional arguments to
`create_prompt_agent`.

```python
custom_agent = factory.create_prompt_agent(
    name="custom-configured-agent",
    description="A creative writing assistant with poetic flair",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions="You are a creative writing assistant. Write in a poetic style.",
    temperature=0.8,
)

response = custom_agent.invoke(
    {"messages": [HumanMessage("Describe a sunset over the ocean.")]}
)

pretty_print(response)
```

```output
================================ Human Message =================================

Describe a sunset over the ocean.
================================== Ai Message ==================================
Name: custom-configured-agent

...poetic response...
```

Common options include `temperature`, `top_p`, `response_format`, `tools`,
`tool_resources`, and `metadata`.

**What this snippet does:** Creates a second agent with non-default generation
settings and validates behavior with a sample prompt.

## Add tools to your agent

You can add tools to your agent to perform actions. The method `create_prompt_agent` implements
the agent loop for you.

You should distinguish two types of tools:

* [Local tools](#add-local-tools): Those are tools that run colocated where your agent code is running. They can be callable functions or any function available for LangChain/LangGraph ecosystem.
* [Built-in tools](#add-built-in-tools): Those are tools that can run exclusively in the Foundry Agent Service; server-side. Server-side tools can only be applied to Foundry agents.

Adding **local tools** to your agent adds a **tool node** to your graph for those tools to run. **Built-in tools** do not add a **tool node** and are executed in the service when you make a request.

:::image type="content" source="../../../foundry/how-to/media/langchain-azure-ai-agents/agent-tools.png" alt-text="Diagram of the agent graph for an agent with tools.":::

The following section explains how to use both:

## Add local tools

Define local Python functions and pass them in `tools`.

```python
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b


def divide(a: int, b: int) -> float:
    """Divide one integer by another."""
    return a / b


tools = [add, multiply, divide]

math_agent = factory.create_prompt_agent(
    name="math-agent",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions=(
        "You are a helpful assistant tasked with performing arithmetic on "
        "a set of inputs."
    ),
    tools=tools,
)
```

Invoke the tool-enabled agent:

```python
messages = [
    HumanMessage(content="Add 3 and 4. Multiply the output by 2. Divide the output by 5")
]
state = math_agent.invoke({"messages": messages})
pretty_print(state)
```

```output
================================ Human Message =================================

Add 3 and 4. Multiply the output by 2. Divide the output by 5
================================== Ai Message ==================================
Tool Calls:
    add (...)
    multiply (...)
    divide (...)
...
================================== Ai Message ==================================
Name: math-agent

The final result is 2.8.
```

**What this snippet does:** Attaches three local Python tools to a v1 prompt
agent and shows multi-step tool calling orchestrated through the agent loop.

Use other tools from the LangGraph/LangChain ecosystem like Azure Document Intelligence in Foundry Tools from the same agent flow. While those tools are connected to a Foundry resource, **they are not exclusive to the Agent Service and hence act like a local tool**.

```python
from langchain_azure_ai.tools import AzureAIDocumentIntelligenceTool

document_parser_agent = factory.create_prompt_agent(
    name="document-agent",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions="You are a helpful assistant tasked with analyzing documents.",
    tools=[AzureAIDocumentIntelligenceTool(credential=DefaultAzureCredential())],
)
```

> [!TIP]
> `AzureAIDocumentIntelligenceTool` can use the Foundry project to connect to
> the service and it also supports Microsoft Entra for authentication. By default,
> the tool uses `AZURE_AI_PROJECT_ENDPOINT` with `DefaultAzureCredential`, which
> is why no further configuration is required. You can change that to use a
> specific endpoint and key if needed.

Ask the agent to analyze an invoice from a URL:

```python
messages = [
    HumanMessage(
        content=(
            "What's the total amount in the invoice at "
            "https://raw.githubusercontent.com/Azure/azure-sdk-for-python/main/"
            "sdk/formrecognizer/azure-ai-formrecognizer/tests/sample_forms/"
            "forms/Form_1.jpg"
        )
    )
]
response = document_parser_agent.invoke({"messages": messages})
pretty_print(response)
```

```output
================================ Human Message =================================

What's the total amount in the invoice at ...
================================== Ai Message ==================================
Tool Calls:
    azure_ai_document_intelligence (...)
...
================================== Ai Message ==================================
Name: document-agent

The total amount in the invoice is **$144.00**.
```

**What this snippet does:** Asks the agent to extract data from a sample
invoice image. The agent calls `AzureAIDocumentIntelligenceTool` to parse the
document and returns the result. Expected output: *"The total amount in the
invoice is **$144.00**."*


## Add built-in tools

Built-in tools in Foundry Agent Service run server-side instead of in a **tool node**
like local tools. In this v1 pattern, create built-in tools from
`azure.ai.agents.models` and wrap them with `AgentServiceBaseTool` for
`create_prompt_agent`.

### Example: use code interpreter tool

Create a code interpreter agent for data analysis and invoke it with a fictitious
`data.csv` data file.

Before running this sample, create a local `data.csv` file in your current
working directory.

```python
from pathlib import Path

import pandas as pd

data = {
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "sales": [12000, 15000, 18000, 14000, 22000, 25000],
    "region": ["North", "South", "East", "West", "North", "South"],
}

df = pd.DataFrame(data)
csv_path = Path.cwd() / "data.csv"
df.to_csv(csv_path, index=False, encoding="utf-8-sig")

print(f"Created sample data file: {csv_path}")
```

```output
Created sample data file: .../data.csv
```

Files need to be uploaded to the project for agents to use them. You can either
upload it and configure the file for the tool or let the `AgentServiceFactory`
handle that for you.

#### Upload and configure files for tools

We need to upload this file so it's available to the code interpreter tool. Use
the Foundry SDK to upload them.

```python
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import CodeInterpreterTool, FilePurpose

client = AgentsClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

uploaded_file = client.files.upload_and_poll(
    file_path=str(csv_path),
    purpose=FilePurpose.AGENTS,
)
print(f"Uploaded file ID: {uploaded_file.id}")
```

```output
Uploaded file ID: file_...
```

**What this snippet does:** Uploads the CSV as an agent file so built-in tools
can access it in the service runtime.

Then configure the tool:

```python
code_interpreter = CodeInterpreterTool(file_ids=[uploaded_file.id])
print("Code interpreter tool configured.")
```

```output
Code interpreter tool configured.
```

**What this snippet does:** Binds the uploaded file to a code interpreter tool
instance so the agent can run analysis over that file.

The `create_prompt_agent` method needs Agent Service tools to be wrapped in 
`AgentServiceBaseTool`.

```python
from langchain_azure_ai.agents.v1.prebuilt.tools import AgentServiceBaseTool


code_interpreter_agent = factory.create_prompt_agent(
    name="code-interpreter-agent",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions=(
        "You are a data analyst agent. Analyze the provided CSV data and "
        "create visualizations when helpful."
    ),
    tools=[AgentServiceBaseTool(tool=code_interpreter)],
)
```

Let's see it in practice:

```python
messages = [
    HumanMessage(
        content=(
            "Create a pie chart with the previously uploaded file "
            f"(ID: {uploaded_file.id}) showing sales by region and show it "
            "to me as a PNG image."
        )
    )
]
state = code_interpreter_agent.invoke({"messages": messages})
pretty_print(state)
```

```output
================================ Human Message =================================

Create a pie chart with the previously uploaded file ...
================================== Ai Message ==================================
Name: code-interpreter-agent

[
    {'type': 'text', 'text': 'Here is the pie chart ...'},
    {'type': 'image', 'mime_type': 'image/png', 'base64': 'iVBORw0...'}
]
```

:::image type="content" source="../../../foundry/how-to/media/langchain-azure-ai-agents/agent-codegen-tool.png" alt-text="The image generated by the `CodeInterpreterTool`.":::

**What this snippet does:** Wraps `CodeInterpreterTool` with
`AgentServiceBaseTool`, executes analysis in Agent Service, and renders the
returned PNG image from base64 content.

#### Send file content inline

When you pass file content as inputs and the code interpreter tool is
attached to the agent, files are uploaded automatically.

```python
import base64

code_interpreter_agent = factory.create_prompt_agent(
    name="code-interpreter-agent-inline-file",
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    instructions=(
        "You are a data analyst agent. Analyze the provided CSV data and "
        "create visualizations when helpful."
    ),
    tools=[AgentServiceBaseTool(tool=CodeInterpreterTool())],
)

with open("data.csv", "rb") as file_handle:
    csv_data = base64.b64encode(file_handle.read()).decode()

state = code_interpreter_agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=[
                    {"type": "file", "mime_type": "text/csv", "base64": csv_data},
                    {
                        "type": "text",
                        "text": (
                            "Create a pie chart with the uploaded data showing "
                            "sales by region and show it as a PNG image."
                        ),
                    },
                ]
            )
        ]
    }
)
```

**What this snippet does:** Sends a CSV file inline in the message payload so
the code interpreter can process it without a separate explicit upload step.

## Run asynchronous operations

You can invoke v1 agents asynchronously with `ainvoke`.

```python
async def async_example() -> None:
    async_agent = factory.create_prompt_agent(
        name="async-demo-agent",
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        instructions="You are an async AI assistant.",
    )

    try:
        response = await async_agent.ainvoke(
            {
                "messages": [
                    HumanMessage("What are the benefits of asynchronous programming?")
                ]
            }
        )
        print(response)
    finally:
        factory.delete_agent(async_agent)


await async_example()
```

```output
{'messages': [...], ...}
```

**What this snippet does:** Demonstrates async invocation with `ainvoke` and
ensures cleanup using `factory.delete_agent` in a `finally` block.

## Clean up agents

Delete agents that you created during your session.

```python
factory.delete_agent(math_agent)
factory.delete_agent(document_parser_agent)
factory.delete_agent(custom_agent)
factory.delete_agent(code_interpreter_agent)
```

## Troubleshooting

Use this checklist to diagnose common setup and runtime issues.

### Enable logging

```python
import logging

logging.getLogger("langchain_azure_ai").setLevel(logging.DEBUG)
```

For broader diagnostics:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Validate your configuration

- Confirm `AZURE_AI_PROJECT_ENDPOINT` points to the correct Foundry classic
  project endpoint.
- Confirm `MODEL_DEPLOYMENT_NAME` matches an existing model deployment.
- Verify authentication context with `az account show`.
- Start with the minimal prompt agent example first.

### Verify resources and permissions

- Ensure your account can access the project and model deployment.
- Ensure dependent resources, such as uploaded files and tool resources, exist.
- Verify resources are in the expected subscription and region.

## Next steps

- [Develop applications with LlamaIndex](llama-index.md)
- [Visualize and manage traces in Foundry](./trace-application.md)
- [Use Foundry Models](../../foundry-models/concepts/models-sold-directly-by-azure.md)
- [Reference: Model Inference API](../../../ai-foundry/model-inference/reference/reference-model-inference-api.md)
