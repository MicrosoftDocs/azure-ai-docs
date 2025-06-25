---
title: "Deep research tool"
titleSuffix: Azure AI Foundry
description: Learn how to use the deep research tool with agents.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 06/25/2025
ms.service: azure-ai-agent-service
ms.topic: how-to
---

# Deep Research

The [Deep Research](https://openai.com/index/introducing-deep-research/) model in the Azure AI Foundry Agent Service enables you to use OpenAI's advanced agentic research capability, and integrate it with your data and systems.

> [!IMPORTANT]
> * Deep Research uses [Grounding with Bing Search](./tools/bing-grounding.md).
>     * Your usage of Grounding with Bing Search can incur costs. See the [pricing page](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
>     * By creating and using a Grounding with Bing Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the terms available at https://www.microsoft.com/bing/apis/grounding-legal, which may be updated from time to time.
>     * When you use Grounding with Bing Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is not subject to the same data processing terms (including location of processing) and does not have     the same compliance standards and certifications as the Azure AI Foundry Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/bing/apis/grounding-legal). It is your responsibility to assess whether use of Grounding with Bing Search in your agent meets your needs and requirements.
>    * Your applications must follow the Grounding with Bing Search [use and display requirements](./tools/bing-grounding.md#how-to-display-grounding-with-bing-search-results)

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
|  | ✔️ | ✔️ | ✔️ | ✔️ |  | ✔️ |

## How Deep Research works

At its core, the Deep Research model orchestrates a multi-step research pipeline that’s tightly integrated with Grounding with Bing Search and OpenAI models

### Clarifying intent and scoping the task

When a user or downstream app submits a research query, the agent uses GPT-4o to clarify the question, gather additional context if needed, and precisely scope the research task. This ensures the agent’s output is both relevant and actionable, and that every search is optimized for your business scenario.

### Grounding with Bing Search

Once the task is scoped, the agent invokes the [Grounding with Bing Search](./tools/bing-grounding.md) tool to gather a curated set of high-quality, recent web data. This ensures the research model is working from a foundation of authoritative, up-to-date sources. 

### Task execution

The Deep Research model then starts the research task execution. This involves thinking reasoning, analyzing, and synthesizing information across all discovered sources. Unlike simple summarization, it reasons step-by-step, pivots as it encounters new insights, and composes a comprehensive answer that's sensitive to nuance, ambiguity, and emerging patterns in the data. 

### Transparency, safety, and compliance

Every stage of the process is safeguarded by input/output classifiers and chain-of-thought (CoT) summarizers. The final output is a structured report that documents not only the answer, but also the model's reasoning path, source citations, and any clarifications requested during the session. This makes every answer fully auditable.

## Prerequisites
- A basic or standard agent [environment setup](../environment-setup.md)
- The [Grounding with Bing Search tool](./tools/bing-grounding.md)
- The following [deployed models](../../model-inference/how-to/create-model-deployments.md)
    - **GPT-4o**
    - **o3-deep-research** 
- A [deployed agent](../quickstart.md)

## Setup 

To use the Deep Research model, you need to add your Grounding with Bing Search as a new connection. In the [AI Foundry portal](https://ai.azure.com/?cid=learnDocs):

1. In Azure AI Foundry, navigate to the project you created in the agent setup. Click on **Open in management center**.
    :::image type="content" source="../media\tools\ai-search\project-studio.png" alt-text="A screenshot of a project in Azure AI Foundry." lightbox="../media\tools\ai-search\project-studio.png":::

1. Select **Create conneciton**.

    :::image type="content" source="../media/create-connection.png" alt-text="A screenshot showing the connection creation screen in the Azure AI Foundry portal" lightbox="../media/create-connection.png":::

1. In the screen that appears, select **Grounding with Bing Search**. 

    :::image type="content" source="../media\tools\bing\add-connection.png" alt-text="A screenshot of the screen to add a Grounding with Bing Search connection." lightbox="../media\tools\bing\add-connection.png":::

## Example code

After completing the setup, you can create an agent to use Deep Research.

## Create a project client
Create a client object, which will contain the endpoint for connecting to your AI project and other resources. 

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import DeepResearchTool, MessageRole

project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

```
## Create an agent with the Grounding with Bing search tool enabled
To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the connected resources section of your project in the Azure AI Foundry portal. You also will need to specify the name of your Deep Research model.

```python

# [START create_agent_with_deep_research_tool]
conn_id = os.environ["AZURE_BING_CONNECTION_ID"]

# Initialize a Deep Research tool with Bing Connection ID and Deep Research model deployment name
deep_research_tool = DeepResearchTool(
    bing_grounding_connection_id=conn_id,
    deep_research_model=os.environ["DEEP_RESEARCH_MODEL_DEPLOYMENT_NAME"],
)

with project_client.agents as agents_client:

        agent = agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],
            name="my-agent",
            instructions="You are a helpful Agent that assists in researching scientific topics.",
            tools=deep_research_tool.definitions,
        )

        # [END create_agent_with_deep_research_tool]
        print(f"Created agent, ID: {agent.id}")
```

## Create a thread

Create a thread and attach a message to it

```python
# Create thread for communication
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content=(
        "What is the latest research on quantum computing? "
        "Please summarize your findings in a 5-point bullet list, "
        "each one a few sentences long, and provide citations for the sources you used. "
        "Conclude with a short summary of the findings."
    ),
)
print(f"Created message, ID: {message.id}")

```

## Create a run and check the output

Create a run and observe the response to the question.

```python
# Create and process Agent run in thread with tools
print(f"Start processing the message... this may take a few minutes to finish. Be patient!")
run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the Agent when done
agents_client.delete_agent(agent.id)
print("Deleted agent")

# Fetch the last message from the agent in the thread
response_message = agents_client.messages.get_last_message_by_role(thread_id=thread.id, role=MessageRole.AGENT)
if response_message:
    for text_message in response_message.text_messages:
        print(f"Agent response: {text_message.text.value}")
    for annotation in response_message.url_citation_annotations:
        print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
```
