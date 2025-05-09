---
title: 'How to use Logic Apps with Azure AI Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to integrate Logic Apps with Azure AI Agents to execute tasks like sending emails.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 05/07/2025
author: aahill
ms.author: aahi
ms.reviewer: umangsehgal
zone_pivot_groups: selection-logic-apps
ms.custom: azure-ai-agents
---

# How to use Logic Apps with Azure AI Agent Service

This article demonstrates how to integrate Logic Apps with Azure AI Agents to execute tasks like sending emails.

## Prerequisites

1. Create a Logic App within the same resource group as your Azure AI Project in the Azure Portal.
2. Configure your Logic App to send emails by including an HTTP request trigger that accepts JSON with `to`, `subject`, and `body`. Refer to the [Logic App Workflow guide](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/agents-logic-apps#create-logic-apps-workflows-for-function-calling).
3. Install the required Python packages:
   ```bash
   pip install azure-ai-agents azure-identity
   ```
4. Set the following environment variables:
   - `PROJECT_ENDPOINT`: The Azure AI Agents endpoint.
   - `MODEL_DEPLOYMENT_NAME`: The deployment name of the AI model.
   - `SUBSCRIPTION_ID`: Your Azure subscription ID.
   - `resource_group_name`: The name of your resource group.

:::zone pivot="python"

## Step 1: Create a project client

Create a client object to connect to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
    api_version="latest",
)
```

## Step 2: Register the Logic App

Register the Logic App by providing its name and trigger details.

```python
from user_logic_apps import AzureLogicAppTool

# Extract subscription and resource group from environment variables
subscription_id = os.environ["SUBSCRIPTION_ID"]
resource_group = os.environ["resource_group_name"]

# Logic App details
logic_app_name = "<LOGIC_APP_NAME>"  # Replace with your Logic App name
trigger_name = "<TRIGGER_NAME>"  # Replace with your Logic App trigger name

# Create and initialize AzureLogicAppTool utility
logic_app_tool = AzureLogicAppTool(subscription_id, resource_group)
logic_app_tool.register_logic_app(logic_app_name, trigger_name)
print(f"Registered logic app '{logic_app_name}' with trigger '{trigger_name}'.")
```

## Step 3: Create an agent with the Logic App tool

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

## Step 4: Create a thread

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

## Step 5: Create a run and check the output

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

## Step 6: Clean up resources

Delete the agent after use to clean up resources.

```python
# Delete the agent
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end

## Next steps

[See the full sample for Logic Apps integration.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_logic_apps.py)