---
title: 'How to use the deep research tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for using deep research in the Azure AI Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 06/26/2025
author: aahill
ms.author: aahi
---

# How to use Deep Research
Use this article to find step-by-step instructions and code samples for Grounding with Bing search.

## Prerequisites

* The requirements in the [Deep Research overview](./deep-research.md)

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
