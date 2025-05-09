---
title: 'How to use Azure Blob Storage with the file search tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for using your existing Azure Blob Storage with Azure AI Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/11/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-bing-grounding-code
ms.custom: azure-ai-agents-code
---


# How to use existing files in Azure Blob Storage with file search

In this example, we use Azure AI Foundry Agent Service to create an agent that can help answer questions on information from files in Azure Blob Storage.

###  Prerequisites 
1. Complete the [standard agent setup](../../quickstart.md).

2. Ensure that you have the role  **Storage Blob Data Contributor** on your project's storage account.

3. Ensure that you have the role **Azure AI Developer** on your project.

> [!IMPORTANT]
> File search using Blob storage is only supported by the standard agent setup.

### Step 1: Create a project client
```python
### Step 1: Create a project client

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Retrieve the endpoint from environment variables
endpoint = os.environ["PROJECT_ENDPOINT"]

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
)
```

### Step 2: Use an existing file in Azure Blob Storage

Use the `asset_uri` of a file already in Azure Blob Storage to create a vector store. This is useful if you have multiple agents that need access to the same files, as it eliminates the need to upload the same file multiple times.

```python
from azure.ai.agents.models import VectorStoreDataSource, VectorStoreDataSourceAssetType

# Define the asset URI for the file in Azure Blob Storage
asset_uri = os.environ["AZURE_BLOB_URI"]

# Create a vector store using the asset URI
data_source = VectorStoreDataSource(asset_identifier=asset_uri, asset_type=VectorStoreDataSourceAssetType.URI_ASSET)
vector_store = project_client.agents.create_vector_store_and_poll(data_sources=[data_source], name="sample_vector_store")
print(f"Created vector store, vector store ID: {vector_store.id}")
```

### Step 3: Create an agent with access to the file search tool

```python
from azure.ai.agents.models import FileSearchTool

# Create a file search tool using the vector store
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

# Create an agent with the file search tool
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are a helpful assistant",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

### Step 4: Create a thread and send a message

```python
# Create a thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

# Send a message to the thread
message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What does the file say?"
)
print(f"Created message, message ID: {message.id}")
```

### Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```python
# Create and process a run with the specified thread and agent
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Cleanup resources
project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# List and print all messages in the thread
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```