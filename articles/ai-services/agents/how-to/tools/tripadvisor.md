---
title: 'How to use Agents with your licensed data'
titleSuffix: Azure AI Foundry
description: Learn how to connect your licensed data for grounding with Azure AI Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 03/04/2025
author: aahill
ms.author: aahi
recommendations: false
---

# Use Tripadvisor data to ground your AI agents

Azure AI Agent Service lets you integrate licensed data from specialized data providers to enhance the quality of your agent's responses with high-quality, fresh data. [Tripadvisor](https://tripadvisor-content-api.readme.io/reference/overview) is a useful travel platform that can, for example, provide travel guidance and reviews. The insights from this data source can empower your agents to deliver nuanced, informed solutions tailored to specific use cases.

> [!IMPORTANT]
> - Your use of connected non-Microsoft services is subject to the terms between you and the service provider. By connecting to a non-Microsoft service, you acknowledge that some of your data, such as prompt content, is passed to the non-Microsoft service, and/or your application might receive data from the non-Microsoft service. You're responsible for your use of non-Microsoft data.
> - Grounding with licensed data incurs usage with licensed data providers, review the pricing plan with your selected licensed data providers.

## Prerequisites

* Obtain an API key for your [Tripadvisor developer account](https://www.tripadvisor.com/developers?screen=credentials).
* Make sure when you put 0.0.0.0/0 for the IP address restriction to allow traffic from Azure AI Agent Service.

[!INCLUDE [licensed-data-setup](../../includes/licensed-data-setup.md)]

## Use your tool in code

You can follow the instructions in [OpenAPI spec tool](./openapi-spec.md) to connect your tool through the OpenAPI spec.

1. Remember to store and import your Tripadvisor OpenAPI spec. You can find it in the Azure AI Foundry portal.

1. Make sure you have updated the authentication method to be `connection` and fill in the connection ID of your custom key connection.

   ``` python
   auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
   ```
    
   > [!TIP]
   > Your connection ID will have the following format:`/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.CognitiveService/account/{project name}/connections/{connection name}`  

Here is full code example:

## Step 1: Initialize the Tripadvisor tool

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme, OpenApiTool

# Define the endpoint and model deployment name
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]  # Ensure the MODEL_DEPLOYMENT_NAME environment variable is set

# Define the Tripadvisor connection ID
tripadvisor_conn_id = os.environ["TRIPADVISOR_CONNECTION_ID"]  # Ensure the TRIPADVISOR_CONNECTION_ID environment variable is set

# Define the OpenAPI specification for the Tripadvisor API
tripadvisor_spec = {
    "openapi": "3.0.1",
    "servers": [{"url": "https://api.content.tripadvisor.com/api"}],
    "info": {
        "version": "1.0.0",
        "title": "Content API - TripAdvisor(Knowledge)",
        "description": "SSP includes Locations Details, Locations Photos, Locations Reviews, Location Search"
    },
    "paths": {
        "/v1/location/{locationId}/details": {
            "get": {
                "summary": "Location Details",
                "description": "A Location Details request returns comprehensive information about a location (hotel, restaurant, or an attraction).",
                "operationId": "getLocationDetails",
                "parameters": [
                    {"name": "locationId", "in": "path", "required": True, "schema": {"type": "integer"}},
                    {"name": "language", "in": "query", "schema": {"type": "string", "default": "en"}},
                    {"name": "currency", "in": "query", "schema": {"type": "string", "default": "USD"}}
                ],
                "responses": {"200": {"description": "Details for the location"}}
            }
        }
    },
    "components": {
        "securitySchemes": {
            "cosoLocationApiLambdaAuthorizer": {
                "type": "apiKey",
                "name": "key",
                "in": "query"
            }
        }
    }
}

# Initialize the OpenAPI tool for Tripadvisor
tripadvisor_tool = OpenApiTool(
    name="TripadvisorTool",
    description="Tool to access Tripadvisor data for travel recommendations.",
    spec=tripadvisor_spec,
    auth=OpenApiConnectionAuthDetails(
        security_scheme=OpenApiConnectionSecurityScheme(connection_id=tripadvisor_conn_id)
    )
)
```

## Step 2: Create an agent with the Tripadvisor tool

```python
# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)

with project_client:
    # Create an agent with the Tripadvisor tool
    agent = project_client.agents.create_agent(
        model=model_deployment_name,  # Model deployment name
        name="tripadvisor-agent",  # Name of the agent
        instructions="You are a helpful travel assistant that uses Tripadvisor data to provide travel guidance.",  # Instructions for the agent
        tools=tripadvisor_tool.definitions,  # Tools available to the agent
    )
    print(f"Created agent, ID: {agent.id}")
```

## Step 3: Interact with the agent

```python
    # Create a thread for communication with the agent
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Send a message to the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Can you recommend some top-rated hotels in Paris?",  # Message content
    )
    print(f"Created message, ID: {message['id']}")

    # Create and process a run with the specified thread and agent
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        # Log the error if the run fails
        print(f"Run failed: {run.last_error}")

    # Fetch and log all messages from the thread
    messages = project_client.agents.messages.list(thread_id=thread.id)
    for message in messages.data:
        print(f"Role: {message.role}, Content: {message.content}")

    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")
```