---
title: 'How to use Microsoft SharePoint content with Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Microsoft SharePoint content.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 05/01/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
---
# Use the Microsoft SharePoint tool (preview)

Integrate your Azure AI Agent with the **Microsoft Sharepoint** to chat with your private documents securely. You can connect to your SharePoint site, such as `contoso.sharepoint.com/sites/policies` to ground your Agents with that data. When a user sends a query, the agent will determine if SharePoint should be leveraged or not. If so, it will send a query using the SharePoint tool, which checks if the user has a Microsoft 365 copilot license and use managed identity to retrieve relevant documents they have access to. The scope of retrieval includes all supported documents in this SharePoint site. Lastly, the agent will generate responses based on retrieved information. With identity passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in SharePoint while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites
1. Developers and end users have Microsoft 365 copilot license

1. Developers and end users have at least `AI Developer` RBAC role. 

1. Developers and end users have at least `READ` access to the SharePoint site.

## Setup  

> [!NOTE]
> 1. Supported document types: text data in the following format: `.pdf`, `.docx`, `.ppt`, `.txt`, `.aspx` 
> 2. We recommend you start with SharePoint sites that have: a simple folder structure and a small number of short documents. 

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. You can add the SharePoint tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal, in either the **Agents** or **Agent playground** screen for your agent, scroll down the setup pane on the right to knowledge. Then select **Add**.

   :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **SharePoint** and follow the prompts to add the tool. You can only add one per agent.

1. Click to add a new connection. Once you have added a connection, you can directly select from existing list.
   1. To create a new connection, you need to find `site_url` in your SharePoint site. You can add either a SharePoint site or a SharePoint folder. For a SharePoint site, it will look like `https://microsoft.sharepoint.com/teams/<site_name>`. For a SharePoint folder, it will look like `https://microsoft.sharepoint.com/teams/<site_name>/Shared%20documents/<folder_name>`

   1. Then, you can add it to your connection. Make sure you have selected the **is secret** option.

## Code example

See the following code samples for using the sharepoint tool in code. 

## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import MessageRole, SharepointTool

# Retrieve endpoint and model deployment name from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Ensure the MODEL_DEPLOYMENT_NAME environment variable is set

# Initialize the AIProjectClient with the endpoint and credentials
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)
```

## Step 2: Create an agent with the SharePoint tool enabled

To make the SharePoint tool available to your agent, use a connection to initialize the tool and attach it to the agent.

```python
with project_client:
    # Retrieve the SharePoint connection ID
    sharepoint_connection = project_client.connections.get(
        name="CONNECTION_NAME",  # Replace with your connection name
    )
    conn_id = sharepoint_connection.id  # Retrieve the connection ID
    print(conn_id)

    # Initialize the SharePoint tool with the connection ID
    sharepoint = SharepointTool(connection_id=conn_id)

    # Create an agent with the SharePoint tool
    agent = project_client.agents.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=sharepoint.definitions,  # Tools available to the agent
    )
    print(f"Created agent, ID: {agent.id}")
```

## Step 3: Create a thread

```python
    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,  # Role of the message sender
        content="Hello, summarize the key points of the <sharepoint_resource_document>",  # Message content
    )
    print(f"Created message, ID: {message['id']}")
```

## Step 4: Create a run and check the output

```python
    # Create and process an agent run in the thread using the tools
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Delete the agent when done to clean up resources
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message['role']}, Content: {message['content']}")
```

## Next steps

[See the full sample for SharePoint.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_sharepoint.py)
