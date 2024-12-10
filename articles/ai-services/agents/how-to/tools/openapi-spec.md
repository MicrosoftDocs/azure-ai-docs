---
title: 'How to use Azure AI Agent service with OpenAPI Specified Tools'
titleSuffix: Azure OpenAI
description: Learn how to use Azure AI Agents with OpenAPI Specified Tools.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 12/06/2024
author: aahill
ms.author: aahi
zone_pivot_groups: selection-function-calling
recommendations: false
---
# How to use Azure AI Agent service with OpenAPI Specified Tools

::: zone pivot="overview"

You can now connect your Azure AI Agent to an external API using an OpenAPI 3.0 specified tool, 
allowing for scalable interoperability with various applications. Enable your custom tools 
to authenticate access and connections with managed identities (Microsoft Entra ID) for 
added security, making it ideal for integrating with existing infrastructure or web services.

OpenAPI Specified tool improves your function calling experience by providing standardized, 
automated, and scalable API integrations that enhance the capabilities and efficiency of your agent. 
[OpenAPI specifications](https://spec.openapis.org/oas/latest.html) provide a formal standard for 
describing HTTP APIs. This allows people to understand how an API works, how a sequence of APIs 
work together, generate client code, create tests, apply design standards, and much, much more. 

## Set up
1. Ensure you've completed the prerequisites and setup steps in the [quickstart](../../quickstart.md).

1. [optional]If your OpenAPI spec requires API key, you can store your API key in a `custom keys` connection and use `connection` authentication

    1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and select the AI Project. Click **connected resources**.
    :::image type="content" source="../../media/tools/bing/project-settings-button.png" alt-text="A screenshot of the settings button for an AI project." lightbox="../../media/tools/bing/project-settings-button.png":::

    1. Select **+ new connection** in the settings page. 
        >[!NOTE]
        > If you re-generate the API key at a later date, you need to update the connection with the new key.
        
       :::image type="content" source="../../media/tools/bing/project-connections.png" alt-text="A screenshot of the connections screen for the AI project." lightbox="../../media/tools/bing/project-connections.png":::

   1. Select **custom keys** in **other resource types**.
    ![image](https://github.com/user-attachments/assets/2e6e8efe-1a31-4097-a859-58ac5ee17a96)

   1. Enter the following information
      - `key`: "key"
      - value: YOUR_API_KEY
      - Connection name: `YOUR_CONNECTION_NAME` (You will use this connection name in the sample code below.)
      - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.
        
::: zone-end

::: zone pivot="code-example"
## Step 1: Create an agent with OpenAPI Spec tool
Create a client object, which will contain the connection string for connecting to your AI project and other resources.
```python
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool, OpenApiAnonymousAuthDetails


# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
```

## Step 2: Enable the OpenAPI Spec tool
You may want to store the OpenAPI specification in another file and import the content to initialize the tool. Please note the sample code is using `anonymous` as authentication type.
```python
with open('./weather_openapi.json', 'r') as f:
    openapi_spec = jsonref.loads(f.read())

# Create Auth object for the OpenApiTool (note that connection or managed identity auth setup requires additional setup in Azure)
auth = OpenApiAnonymousAuthDetails()

# Initialize agent OpenApi tool using the read in OpenAPI spec
openapi = OpenApiTool(name="get_weather", spec=openapi_spec, description="Retrieve weather information for a location", auth=auth)
```
If you want to use connection, which stores API key, for authentication, replace the line with
```python
auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id="your_connection_id"))
```
Your connection ID looks like `/subscriptions/{subscription ID}/resourceGroups/{resource group name}/providers/Microsoft.MachineLearningServices/workspaces/{project name}/connections/{connection name}`.

If you want to use managed identity for authentication, replace the line with
```python
auth = OpenApiManagedAuthDetails(security_scheme=OpenApiManagedSecurityScheme(audience="https://your_identity_scope.com"))
```
An example of the audience would be ```https://cognitiveservices.azure.com/```.

## Step 3: Create a thread
```python
# Create agent with OpenApi tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o-mini",
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=openapi.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    # Create thread for communication
    thread = project_client.agents.create_thread()
    print(f"Created thread, ID: {thread.id}")
```

## Step 4: Create a run and check the output
Create a run and observe that the model uses the OpenAPI Spec tool to provide a response to the user's question.
```python
# Create message to thread
    message = project_client.agents.create_message(
        thread_id=thread.id,
        role="user",
        content="What's the weather in Seattle?",
    )
    print(f"Created message, ID: {message.id}")

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
