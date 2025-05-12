---
title: 'OpenAPI spec code samples'
titleSuffix: Azure AI Foundry
description: Find code samples to use OpenAPI tools with agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/09/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents-code
zone_pivot_groups: selection-openapi-function
---

# How to use the OpenAPI spec tool

Use this article to find step-by-step instructions and code samples for using OpenAPI based tools.

:::zone pivot="portal"

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/). in the **Create and debug** screen or **Agent playground**, select your agent.
1. Scroll down the **Setup** pane on the right to **action**. Then select **Add**.

    :::image type="content" source="../../media/tools/action-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools.png":::
   
1. Select **OpenAPI 3.0 specified tool**.

    :::image type="content" source="../../media/tools/action-tools-list.png" alt-text="A screenshot showing the available action tools in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools-list.png":::
   
1. Give your tool a name (required) and a description (optional). The description will be used by the model to decide when and how to use the tool.

   :::image type="content" source="../../media/tools/open-api-details.png" alt-text="A screenshot showing the openAPI tool details in the Azure AI Foundry portal." lightbox="../../media/tools/open-api-details.png":::

1. Click Next and select your authentication method. Choose `connection` for `API key`.
   1. If you choose `connection`, you need to select the custom keys connection you have created before.
   1. If you choose `managed identity`, you need to input the audience to get your token. An example of an audience would be `https://cognitiveservices.azure.com/` to connect to Azure AI Services. Make sure you have already set up authentication and role assignment (as described in the [section](./openapi-spec.md#authenticating-with-managed-identity-microsoft-entra-id) above).
      
1. Copy and paste your OpenAPI specification in the text box.

1. Review and add the tool to your agent.

:::zone-end

:::zone pivot="csharp"

## Using the .NET SDK

In this example we will demonstrate the possibility to use services with [OpenAPI Specification](https://en.wikipedia.org/wiki/OpenAPI_Specification) with the agent. We will use [wttr.in](https://wttr.in) service to get weather and its specification file [weather_openapi.json](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Projects/tests/Samples/Agent/weather_openapi.json).

1. First get `ProjectEndpoint` and `ModelDeploymentName` from config and create a `PersistentAgentsClient`. Also, create an `OpenApiAnonymousAuthDetails` and `OpenApiToolDefinition` from config. 

```csharp
    var projectEndpoint = configuration["ProjectEndpoint"];
    var modelDeploymentName = configuration["ModelDeploymentName"];
    var openApiSpec = configuration["OpenApiSpec"];
    PersistentAgentsClient client = new(new Uri(projectEndpoint), new DefaultAzureCredential());
    
    var spec = BinaryData.FromBytes(File.ReadAllBytes(openApiSpec));
    OpenApiAnonymousAuthDetails openApiAnonAuth = new();
    OpenApiToolDefinition openApiTool = new(
        name: "get_weather",
        description: "Retrieve weather information for a location",
        spec: spec,
        auth: openApiAnonAuth,
        defaultParams: ["format"]
    );
```

2. Next we will need to create an agent.

```csharp
    PersistentAgent agent = client.CreateAgent(
        model: modelDeploymentName,
        name: "Open API Tool Calling Agent",
        instructions: "You are a helpful agent.",
        tools: [openApiTool]
    );
```

3. Now we will create a `ThreadRun` and wait until it is complete. If the run will not be successful, we will print the last error.


```csharp
    PersistentAgentThread thread = client.CreateThread();
    ThreadMessage message = client.CreateMessage(
        thread.Id,
        MessageRole.User,
        "What's the weather in Seattle?");
    
    ThreadRun run = client.CreateRun(thread, agent);
    
    do
    {
        Thread.Sleep(TimeSpan.FromMilliseconds(500));
        run = client.GetRun(thread.Id, run.Id);
    }
    while (run.Status == RunStatus.Queued
        || run.Status == RunStatus.InProgress
        || run.Status == RunStatus.RequiresAction);
```

4. Print the messages to the console in chronological order.

```csharp
    Pageable<ThreadMessage> messages = client.Messages.GetMessages(
        threadId: thread.Id,
        order: ListSortOrder.Ascending);

    foreach (ThreadMessage threadMessage in messages)
    {
        foreach (MessageContent content in threadMessage.ContentItems)
        {
            switch (content)
            {
                case MessageTextContent textItem:
                    Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                    break;
            }
        }
    }
```

5. Finally, we delete all the resources, we have created in this sample.

```csharp
    client.DeleteThread(thread.Id);
    client.DeleteAgent(agent.Id);
```

:::zone-end

:::zone pivot="python"

## Step 1: Create a project client
Create a client object, which will contain the connection string for connecting to your AI project and other resources.


```python
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import OpenApiTool, OpenApiAnonymousAuthDetails


# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
```


## Step 2: Create the OpenAPI Spec tool definition
You might want to store the OpenAPI specification in another file and import the content to initialize the tool. The sample code is using `anonymous` as the authentication type.


```python
with open('./weather_openapi.json', 'r') as f:
    openapi_spec = jsonref.loads(f.read())

# Create Auth object for the OpenApiTool (note that connection or managed identity auth setup requires additional setup in Azure)
auth = OpenApiAnonymousAuthDetails()

# Initialize agent OpenAPI tool using the read in OpenAPI spec
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
An example of the audience would be `https://cognitiveservices.azure.com/`.

## Step 3: Create an agent and a thread

```python
# Create agent with OpenAPI tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o",
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
    run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
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

:::zone-end

:::zone pivot="rest-api"

## Step 1: Create the OpenAPI Spec tool definition, agent and thread
 
You might want to store the OpenAPI specification in another file and import the content to initialize the tool. This example is using `anonymous` as the authentication type.

```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are a weather bot. Use the provided functions to answer questions about the weather.",
    "model": "gpt-4o",
    "tools": [{
        "type": "openapi",
        "openapi": {
          "name": "weatherapp",
          "description": "Tool to get weather data",
          "auth": {
            "type": "anonymous"
          },
          "spec": {
            "openapi": "3.1.0",
            "info": {
                "title": "get weather data",
                "description": "Retrieves current weather data for a location.",
                "version": "v1.0.0"
            },
            "servers": [{
                "url": "https://wttr.in"
            }],
            "auth": [],
            "paths": {
                "/{location}": {
                    "get": {
                        "description": "Get weather information for a specific location",
                        "operationId": "GetCurrentWeather",
                        "parameters": [
                        {
                            "name": "location",
                            "in": "path",
                            "description": "City or location to retrieve the weather for",
                            "required": true,
                            "schema": {
                            "type": "string"
                            }
                        },
                        {
                            "name": "format",
                            "in": "query",
                            "description": "Format in which to return data. Always use 3.",
                            "required": true,
                            "schema": {
                            "type": "integer",
                            "default": 3
                            }
                        }
                        ],
                        "responses": {
                        "200": {
                            "description": "Successful response",
                            "content": {
                            "text/plain": {
                                "schema": {
                                "type": "string"
                                }
                            }
                            }
                        },
                        "404": {
                            "description": "Location not found"
                        }
                        },
                        "deprecated": false
                    }
                }
            },
            "components": {
                "schemes": { }
            }
            }
        }
    }]
    }'
```

## Step 2: Create a run and check the output
Create a run and observe that the model uses the OpenAPI Spec tool to provide a response to the user's question.

### Create a thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

### Run the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

### Retrieve the agent response

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end

