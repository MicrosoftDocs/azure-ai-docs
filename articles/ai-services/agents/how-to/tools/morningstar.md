---
title: 'How to use Agents with Morningstar licensed data'
titleSuffix: Azure AI Foundry
description: Learn how to use your developer account with Morningstar grounding with Azure AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 05/09/2025
author: umangsehgal
ms.author: umangsehgal
recommendations: false
---

# Use Morningstar data to ground your AI agents

Azure AI Agent Service lets you integrate licensed data from specialized data providers to enhance the quality of your agent's responses with high-quality, fresh data. [Morningstar](https://developer.morningstar.com/). Morningstar is a prominent investment research company that provides comprehensive analysis, ratings, and data on mutual funds, ETFs, stocks, and bonds. The insights from this data source can empower your agents to deliver nuanced, informed solutions tailored to specific use cases.

> [!IMPORTANT]
> - Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data.
> - Grounding with licensed data incurs usage with licensed data providers, review the pricing plan with your selected licensed data providers.


## Prerequisites

Create a developer account with Morningstar: To start, access the Morningstar tool with your Morningstar credentials. If you don't have a Morningstar account, contact `iep-dev@morningstar.com`. Provide an email address for your account username during onboarding. Morningstar will email instructions for creating a password and activating your account. Store and transmit your unique username and password securely. 

To get your token for your Morningstar developer account, you can use the following script: 

```python 
import requests 
from requests.auth import HTTPBasicAuth 
url = "https://www.us-api.morningstar.com/token/oauth" 
auth = HTTPBasicAuth("YOUR_EMAIL_ADDRESS", "YOUR_PASSWORD") 
response = requests.post(url, auth=auth) 
print(response.text) 
#Note: This token expires, remember to refresh your credentials. 
``` 

[!INCLUDE [licensed-data-setup](../../includes/licensed-data-setup.md)]

## Use your tool in code

You can follow the instructions in [OpenAPI spec tool](./openapi-spec.md) to connect your tool through the OpenAPI spec.

1. Remember to store and import your [Morningstar](https://developer.morningstar.com/content/documentation/intelligence-engine/apps/morningstar-agent-api/3.1.0/morningstar-agent-api.json) OpenAPI spec. You can find it in the Azure AI Foundry portal.

1. Make sure you have updated the authentication method to be `connection` and fill in the connection ID of your custom key connection.

   ``` python
   auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
   ```
    
   > [!TIP]
   > Your connection ID will have the following format:`/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.CognitiveService/account/{project name}/connections/{connection name}`

:::zone pivot="python"

## Step 1: Create a project client

Create a client object to connect to your AI project and other resources.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme

# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,  # Azure AI Project endpoint
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
    api_version="latest",  # Use the latest API version
)
```

## Step 2: Configure the Morningstar tool

Set up the Morningstar tool using the connection ID for your custom key connection.

```python
# Retrieve the connection ID for the Morningstar custom key connection
connection_id = os.environ["CONNECTION_ID"]  # Ensure the CONNECTION_ID environment variable is set

# Set up authentication details for the Morningstar tool
auth = OpenApiConnectionAuthDetails(
    security_scheme=OpenApiConnectionSecurityScheme(connection_id=connection_id)  # Use the connection ID for authentication
)
```

## Step 3: Create an agent with the Morningstar tool

Create an agent and attach the Morningstar tool to it.

```python
with project_client:
    # Create an agent with the Morningstar tool
    agent = project_client.agents.create_agent(
        model="gpt-4o",  # Specify the model to use
        name="MorningstarAgent",  # Name of the agent
        instructions="You are a financial assistant that uses Morningstar data to provide investment insights.",  # Instructions for the agent
        tools=[auth],  # Attach the Morningstar tool to the agent
    )
    print(f"Created agent, ID: {agent.id}")
```

## Step 4: Interact with the agent

Send a query to the agent and process the response.

```python
    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",  # Role of the message sender
        content="What are the top-rated mutual funds according to Morningstar?",  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run for the agent to handle the message
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    # Check if the run failed
    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages:
        print(f"Role: {message['role']}, Content: {message['content']}")
```

## Step 5: Clean up resources

Delete the agent after use to clean up resources.

```python
    # Delete the agent after the interaction is complete
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```
