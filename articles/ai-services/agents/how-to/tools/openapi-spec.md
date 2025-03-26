---
title: 'How to use Azure AI Agent Service with OpenAPI Specified Tools'
titleSuffix: Azure OpenAI
description: Learn how to use Azure AI Agents with OpenAPI Specified Tools.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 03/12/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-function-calling
ms.custom: azure-ai-agents
---
# How to use Azure AI Agent Service with OpenAPI Specified Tools

::: zone pivot="overview"

You can now connect your Azure AI Agent to an external API using an OpenAPI 3.0 specified tool, 
allowing for scalable interoperability with various applications. Enable your custom tools 
to authenticate access and connections with managed identities (Microsoft Entra ID) for 
added security, making it ideal for integrating with existing infrastructure or web services.

OpenAPI Specified tool improves your function calling experience by providing standardized, 
automated, and scalable API integrations that enhance the capabilities and efficiency of your agent. 
[OpenAPI specifications](https://spec.openapis.org/oas/latest.html) provide a formal standard for 
describing HTTP APIs. This allows people to understand how an API works, how a sequence of APIs works together, generate client code, create tests, apply design standards, and more. Currently, we support three authentication types with the OpenAPI 3.0 specified tools: `anonymous`, `API key`, `managed identity`.

### Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|
|   ✔️   | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites
1. Ensure you've completed the prerequisites and setup steps in the [quickstart](../../quickstart.md).

1. Check the OpenAPI spec for the following requirements:
    1. Although not required by the OpenAPI spec, `operationId` is required for each function to be used with the OpenAPI tool.
    1. `operationId` should only contain letters, `-` and `_`. You can modify it to meet the requirement. We recommend using descriptive name to help models efficiently decide which function to use.

## Authenticating with API Key

With API key authentication, you can authenticate your OpenAPI spec using various methods such as an API key or Bearer token. Only one API key security schema is supported per OpenAPI spec. If you need multiple security schemas, create multiple OpenAPI spec tools.

1. Update your OpenAPI spec security schemas. it has a `securitySchemes` section and one scheme of type `apiKey`. For example:

   ```json
    "securitySchemes": {
        "apiKeyHeader": {
                "type": "apiKey",
                "name": "x-api-key",
                "in": "header"
            }
    }
   ```

   You usually only need to update the `name` field, which corresponds to the name of `key` in the connection. If the security schemes include multiple schemes, we recommend keeping only one of them.

1. Update your OpenAPI spec to include a `security` section:
   ```json
   "security": [
        {  
        "apiKeyHeader": []  
        }  
    ]
   ```

1. Remove any parameter in the OpenAPI spec that needs API key, because API key will be stored and passed through a connection, as described later in this article.

1. Create a `custom keys` connection to store your API key.

    1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and select the AI Project. Click **connected resources**.
    :::image type="content" source="../../media/tools/bing/project-settings-button.png" alt-text="A screenshot of the settings button for an AI project." lightbox="../../media/tools/bing/project-settings-button.png":::

    1. Select **+ new connection** in the settings page. 
        >[!NOTE]
        > If you regenerate the API key at a later date, you need to update the connection with the new key.
        
       :::image type="content" source="../../media/tools/bing/project-connections.png" alt-text="A screenshot of the connections screen for the AI project." lightbox="../../media/tools/bing/project-connections.png":::

   1. Select **custom keys** in **other resource types**.
    
        :::image type="content" source="../../media/tools/bing/api-key-connection.png" alt-text="A screenshot of the custom keys selection for the AI project." lightbox="../../media/tools/bing/api-key-connection.png":::
    
   1. Enter the following information
      - key: `name` field of your security scheme. In this example, it should be `x-api-key`
        ```json
               "securitySchemes": {
                  "apiKeyHeader": {
                            "type": "apiKey",
                            "name": "x-api-key",
                            "in": "header"
                        }
                }
        ```
      - value: YOUR_API_KEY
      - Connection name: YOUR_CONNECTION_NAME (You will use this connection name in the sample code below.)
      - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.

1. Once you have created a connection, you can use it through the SDK or REST API. Use the tabs at the top of this article to see code examples.

## Authenticating with managed identity (Microsoft Entra ID)

[Microsoft Entra ID](/entra/fundamentals/whatis) is a cloud-based identity and access management service that your employees can use to access external resources. Microsoft Entra ID allows you to authenticate your APIs with additional security without the need to pass in API keys. Once you have set up managed identity authentication, it will authenticate through the Azure AI Service your agent is using. 

To set up authenticating with Managed Identity:

1. Enable the Azure AI Service of your agent has `system assigned managed identity` enabled.

    :::image type="content" source="../../media/tools/managed-identity-portal.png" alt-text="A screenshot showing the managed identity selector in the Azure portal." lightbox="../../media/tools/managed-identity-portal.png":::

1. Create a resource of the service you want to connect to through OpenAPI spec.

1. Assign proper access to the resource.
    1. Click **Access Control** for your resource
       
    1. Click **Add** and then **add role assignment** at the top of the screen.

        :::image type="content" source="../../media/tools/role-assignment-portal.png" alt-text="A screenshot showing the role assignment selector in the Azure portal." lightbox="../../media/tools/role-assignment-portal.png":::
        
    1. Select the proper role assignment needed, usually it will require at least *READER* role. Then click **Next**.

    1. Select **Managed identity** and then click **select members**.

    1. In the managed identity dropdown menu, search for **Azure AI services** and then select the AI Service of your agent.

    1. Click **Finish**.

1. Once the setup is done, you can continue by using the tool through the Foundry Portal, SDK, or REST API. Use the tabs at the top of this article to see code samples.

## Add OpenAPI spec tool in the Azure AI Foundry portal

You can add the Grounding with Bing Search tool to an agent programatically using the code examples listed at the top of this article, or the [Azure AI Foundry portal](https://ai.azure.com/). If you want to use the portal:

1. in the **Create and debug** screen or **Agent playground**, select your agent.
1. Scroll down the **Setup** pane on the right to **action**. Then select **Add**.

    :::image type="content" source="../../media/tools/action-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools.png":::
   
1. Select **OpenAPI 3.0 specified tool**.

    :::image type="content" source="../../media/tools/action-tools-list.png" alt-text="A screenshot showing the available action tools in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools-list.png":::
   
1. Give your tool a name (required) and a description (optional). The description will be used by the model to decide when and how to use the tool.

   :::image type="content" source="../../media/tools/open-api-details.png" alt-text="A screenshot showing the openAPI tool details in the Azure AI Foundry portal." lightbox="../../media/tools/open-api-details.png":::

1. Click Next and select your authentication method. Choose `connection` for `API key`.
   1. If you choose `connection`, you need to select the custom keys connection you have created before.
   1. If you choose `managed identity`, you need to input the audience to get your token. An example of an audience would be `https://cognitiveservices.azure.com/` to connect to Azure AI Services. Make sure you have already set up authentication and role assignment (as described in the [section](#authenticating-with-managed-identity-microsoft-entra-id) above).
      
1. Copy and paste your OpenAPI specification in the text box.

1. Review and add the tool to your agent.

::: zone-end

::: zone pivot="code-example"
## Step 1: Create a project client
Create a client object, which will contain the connection string for connecting to your AI project and other resources.
# [Python](#tab/python)

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
# [C#](#tab/csharp)
```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Text.Json.Serialization;
using System.Text.Json;
using System.Threading.Tasks;
using Azure.Core.TestFramework;
using NUnit.Framework;
using Newtonsoft.Json.Linq;

namespace Azure.AI.Projects.Tests;

public partial class Sample_Agent_OpenAPI : SamplesBase<AIProjectsTestEnvironment>
{
    private static string GetFile([CallerFilePath] string pth = "")
    {
        var dirName = Path.GetDirectoryName(pth) ?? "";
        return Path.Combine(dirName, "weather_openapi.json");
    }

    [Test]
    public async Task OpenAPICallingExample()
    {
        var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
        var storageQueueUri = TestEnvironment.STORAGE_QUEUE_URI;
        AgentsClient client = new(connectionString, new DefaultAzureCredential());
        var file_path = GetFile();
```
# [REST API](#tab/rest)
Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`.

---

## Step 2: Create the OpenAPI Spec tool definition
You might want to store the OpenAPI specification in another file and import the content to initialize the tool. Note the sample code is using `anonymous` as authentication type.

# [Python](#tab/python)

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
An example of the audience would be ```https://cognitiveservices.azure.com/```.

# [C#](#tab/csharp)

```csharp
    #region Snippet:OpenAPIDefineFunctionTools
    OpenApiAnonymousAuthDetails oaiAuth = new();
    OpenApiToolDefinition openapiTool = new(
        name: "get_weather",
        description: "Retrieve weather information for a location",
        spec: BinaryData.FromBytes(File.ReadAllBytes(file_path)),
        auth: oaiAuth
    );
```
# [REST API](#tab/rest)
We will create an agent with the tool configuration in the next section.

---

## Step 3: Create an agent and a thread

# [Python](#tab/python)

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
# [C#](#tab/csharp)
```csharp
Response<Agent> agentResponse = await client.CreateAgentAsync(
            model: "gpt-4o",
            name: "azure-function-agent-foo",
            instructions: "You are a helpful assistant.",
            tools: new List<ToolDefinition> { openapiTool }
            );
Agent agent = agentResponse.Value;
#endregion
Response<AgentThread> threadResponse = await client.CreateThreadAsync();
AgentThread thread = threadResponse.Value;
```

# [REST API](#tab/rest)
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

---

## Step 4: Create a run and check the output
Create a run and observe that the model uses the OpenAPI Spec tool to provide a response to the user's question.

# [Python](#tab/python)

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

# [C#](#tab/csharp)

```csharp
        #region Snippet:OpenAPIHandlePollingWithRequiredAction
        Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
            thread.Id,
            MessageRole.User,
            "What's the weather in Seattle?");
        ThreadMessage message = messageResponse.Value;

        Response<ThreadRun> runResponse = await client.CreateRunAsync(thread, agent);

        do
        {
            await Task.Delay(TimeSpan.FromMilliseconds(500));
            runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
        }
        while (runResponse.Value.Status == RunStatus.Queued
            || runResponse.Value.Status == RunStatus.InProgress
            || runResponse.Value.Status == RunStatus.RequiresAction);
        #endregion

        Response<PageableList<ThreadMessage>> afterRunMessagesResponse
            = await client.GetMessagesAsync(thread.Id);
        IReadOnlyList<ThreadMessage> messages = afterRunMessagesResponse.Value.Data;

        // Note: messages iterate from newest to oldest, with the messages[0] being the most recent
        foreach (ThreadMessage threadMessage in messages)
        {
            Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
            foreach (MessageContent contentItem in threadMessage.ContentItems)
            {
                if (contentItem is MessageTextContent textItem)
                {
                    Console.Write(textItem.Text);
                }
                else if (contentItem is MessageImageFileContent imageFileItem)
                {
                    Console.Write($"<image from ID: {imageFileItem.FileId}");
                }
                Console.WriteLine();
            }
        }
```
# [REST API](#tab/rest)
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

---

::: zone-end
