---
title: 'How to use Logic Apps with Foundry Agent Service'
titleSuffix: Microsoft Foundry
description: Learn how to integrate Logic Apps with Azure AI Agents to execute tasks like sending emails.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/19/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-logic-apps
ms.custom: azure-ai-agents
---

# How to use Logic Apps with Foundry Agent Service

[!INCLUDE [classic-banner](../../../includes/classic-banner.md)]

This article demonstrates how to integrate Logic Apps with Azure AI Agents to execute tasks like sending emails.

## Prerequisites

1. Create a Logic App within the same resource group as your Azure AI Project in the Azure portal.
1. Configure your Logic App to send emails by including an HTTP request trigger that accepts JSON with `to`, `subject`, and `body`. See the [Logic App Workflow guide](../../../openai/how-to/assistants-logic-apps.md) for more information.
1. Set the following environment variables:
   - `PROJECT_ENDPOINT`: The Azure AI Agents endpoint.
   - `MODEL_DEPLOYMENT_NAME`: The deployment name of the AI model.
   - `SUBSCRIPTION_ID`: Your Azure subscription ID.
   - `resource_group_name`: The name of your resource group.

:::zone pivot="portal"


## Add a Logic Apps workflow to an agent using the Microsoft Foundry portal

1. Go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs). In the **Agents** screen for your agent, scroll down the **Setup** pane on the right to **Actions**. Then select **Add**.

    :::image type="content" source="../../media/tools/action-tools.png" alt-text="A screenshot showing the available tool categories in the Foundry portal." lightbox="../../media/tools/action-tools.png":::

1. Select **Azure Logic Apps** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/action-tools-list.png" alt-text="A screenshot showing the available action tools in the Foundry portal." lightbox="../../media/tools/action-tools-list.png":::

    You can choose to add Microsoft authored workflows, or add your own.
    
    > [!NOTE]
    > For your logic apps to appear in the Foundry portal, they must:
    > * Be in the same subscription and resource group.
    > * Follow a request trigger with a description, and end with a response action.
    > * Currently we only support consumption workflows.  

    :::image type="content" source="../../media/tools/add-logic-apps.png" alt-text="A screenshot showing the screen to add Logic Apps." lightbox="../../media/tools/add-logic-apps.png":::


:::zone-end

:::zone pivot="python"

## Create a project client

Create a client object to connect to your AI project and other resources.


```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)
```

## Register the Logic App

Register the Logic App by providing its name and trigger details. You can find code for `AzureLogicAppTool` on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples-classic/python/getting-started-agents/logic_apps/user_logic_apps.py).

```python
from user_logic_apps import AzureLogicAppTool

# Extract subscription and resource group from environment variables
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_group = os.environ["resource_group_name"]

# Logic App details
logic_app_name = "<LOGIC_APP_NAME>"
trigger_name = "<TRIGGER_NAME>"

# Create and initialize AzureLogicAppTool utility
logic_app_tool = AzureLogicAppTool(subscription_id, resource_group)
logic_app_tool.register_logic_app(logic_app_name, trigger_name)
print(f"Registered logic app '{logic_app_name}' with trigger '{trigger_name}'.")
```

## Create an agent with the Logic App tool

Create an agent and attach the Logic App tool to it.

```python
from azure.ai.agents.models import ToolSet, FunctionTool
from user_functions import fetch_current_datetime
from user_logic_apps import create_send_email_function

# Create the specialized "send_email_via_logic_app" function
send_email_func = create_send_email_function(logic_app_tool, logic_app_name)

# Prepare the function tools for the agent
functions_to_use = {fetch_current_datetime, send_email_func}

# Create an agent
functions = FunctionTool(functions=functions_to_use)
toolset = ToolSet()
toolset.add(functions)

agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="SendEmailAgent",
    instructions="You are a specialized agent for sending emails.",
    toolset=toolset,
)
print(f"Created agent, ID: {agent.id}")
```

## Create a thread

Create a thread for communication with the agent.

```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create a message in the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello, please send an email to <RECIPIENT_EMAIL> with the date and time in '%Y-%m-%d %H:%M:%S' format.",
)
print(f"Created message, ID: {message['id']}")
```

## Create a run and check the output

Create a run and observe that the model uses the Logic App tool to execute the task.

```python
# Create and process an agent run in the thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message['role']}, Content: {message['content']}")
```

## Clean up resources

Delete the agent after use to clean up resources.

```python
# Delete the agent
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end

## Next steps

[See the full sample for Logic Apps integration.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_logic_apps.py)
