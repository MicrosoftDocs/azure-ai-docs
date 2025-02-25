---
title: 'How to use the Microsoft Fabric tool in Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Microsfot Fabric.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/25/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-fabric-ai-skill
ms.custom: azure-ai-agents
---

# Use the Microsoft Fabric AI skill

::: zone pivot="overview"

Integrate your Azure AI Agent with the [**Microsoft Fabric AI skill**](/fabric/data-science/concept-ai-skill) to unlock powerful data analysis capabilities. The Fabric AI skill transforms enterprise data into conversational Q&A systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric AI skill and then connect your Fabric AI skill with the published endpoint. When a user sends a query, Azure AI Agent will first determine if the Fabric AI skill should be leveraged or not. If so, it will use the end user’s identity to generate queries over data they have access to. Lastly, Azure AI Agent will generate responses based on queries returned from Fabric AI skills. With Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | - | - | ✔️ | ✔️ | ✔️ |

## Prerequisite
1. You have created and published an AI skill endpoint

1. Developers and end users have at least `AI Developer` RBAC role. 

## Setup  
> [!NOTE]
> 1. The model you selected in Azure AI Agent setup is only used for agent orchestration and response generation. It doesn't impact which model Fabric AI skill uses for NL2SQL operation.
1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create and publish an [AI skill](/fabric/data-science/how-to-create-ai-skill)

1. You can add the Fabric AI skill tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal, in the Create and debug screen for your agent, scroll down the Setup pane on the right to knowledge. Then select Add.
   :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Microsoft Fabric** and follow the prompts to add the tool. You can add only one per agent.

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.
   1. To create a new connection, you need to find `workspace-id` and `artifact-id` in your published AI skill endpoint. Your AI skill endpoint would look like `https://daily.powerbi.com/groups/<workspace_id>/aiskills/<artifact-id>`

   1. Then, you can add both to your connection. Make sure you have checked `is secret` for both of them
   
        :::image type="content" source="../../media/tools/fabric-foundry.png" alt-text="A screenshot showing the fabric connection in the Azure AI Foundry portal." lightbox="../../media/tools/fabric-foundry.png":::

::: zone-end

::: zone pivot="code-example"
## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FabricTool
```

# [REST API](#tab/rest)

TBD

---

## Step 2: Create an Agent with the Fabric AI skill tool enabled

To make the Fabric AI skill tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

# [Python](#tab/python)

```python
# The Fabric connection id can be found in the Azure AI Foundry project as a property of the Fabric tool
# Your connection id is in the format /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-fabric-connection-name>
conn_id = "your-connection-id"

# Initialize agent fabric tool and add the connection id
fabric = FabricTool(connection_id=conn_id)

# Create agent with the fabric tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=fabric.definitions,
        headers={"x-ms-enable-preview": "true"},
    )
    print(f"Created agent, ID: {agent.id}")
```

# [REST API](#tab/rest)

TBD

---

## Step 3: Create a thread

# [Python](#tab/python)

```python
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
# Remember to update the message with your data
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="what is top sold product in Contoso last month?",
)
print(f"Created message, ID: {message.id}")
```
# [REST API](#tab/rest)

TBD

---

## Step 4: Create a run and check the output

Create a run and observe that the model uses the Fabric AI skill tool to provide a response to the user's question.

# [Python](#tab/python)

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
# [REST API](#tab/rest)

TBD

---

::: zone-end

## Next steps

[See the full sample for Fabric AI skill.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_fabric.py)
