---
title: 'How to use the Sharepoint tool'
titleSuffix: Azure AI Foundry
description: Find examples on how to ground agents with Sharepoint.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/09/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents-code
zone_pivot_groups: selection-sharepoint
---

# How to use the Sharepoint tool

Use this article to find step-by-step instructions and code samples for using the Sharepoint tool in Azure AI Foundry Agent Service.

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import SharepointTool
```

## Create an Agent with the SharePoint tool enabled

To make the SharePoint tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

```python
# Initialize Sharepoint tool with connection id
sharepoint_connection = project_client.connections.get(
    connection_name="CONNECTION_NAME",
)
conn_id = sharepoint_connection.id
print(conn_id)
sharepoint = SharepointTool(connection_id=conn_id)

# Create agent with SharePoint tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_NAME"],
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=sharepoint.definitions,
        headers={"x-ms-enable-preview": "true"},
    )
    print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
# Remember to update the message with your data
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="<ask questions specific to your SharePoint documents>",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

Create a run and observe that the model uses the SharePoint tool to provide a response to the user's question.

```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the assistant when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```