---
title: "OpenAPI spec code samples"
titleSuffix: Azure AI Foundry
description: Find code samples to use OpenAPI tools with agents.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 06/18/2025
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.custom:
  - azure-ai-agents-code
  - build-2025
zone_pivot_groups: selection-openapi-function
---

# How to use the OpenAPI spec tool

Use this article to find step-by-step instructions and code samples for using OpenAPI based tools.

:::zone pivot="portal"

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs). in the **Agents** screen or **Agent playground**, select your agent.
1. Scroll down the **Setup** pane to **action**. Then select **Add**.

    :::image type="content" source="../../media\tools\action-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media\tools\action-tools.png":::
   
1. Select **OpenAPI 3.0 specified tool**.

    :::image type="content" source="../../media\tools\action-tools-list.png" alt-text="A screenshot showing the available action tools in the Azure AI Foundry portal." lightbox="../../media\tools\action-tools-list.png":::
   
1. Give your tool a name (required) and a description (optional). The description will be used by the model to decide when and how to use the tool.

   :::image type="content" source="../../media\tools\open-api-details.png" alt-text="A screenshot showing the openAPI tool details in the Azure AI Foundry portal." lightbox="../../media\tools\open-api-details.png":::

1. Select **Next** and select your authentication method. Choose your connection.
   1. If you choose `connection`, you need to select the custom keys connection you have created before.
   1. If you choose `managed identity`, you need to input the audience to get your token. An example of an audience would be `https://cognitiveservices.azure.com/` to connect to Azure AI Services. Make sure you have already set up authentication and role assignment (as described in the [section](./openapi-spec.md#authenticating-with-managed-identity-microsoft-entra-id) above).
      
1. Copy and paste your OpenAPI specification in the text box.

1. Review and add the tool to your agent.

:::zone-end

:::zone pivot="python"

## Initialization
The code begins by setting up the necessary imports and initializing the AI Project client:

```python
# Import necessary libraries
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
# import the folloing 
from azure.ai.agents.models import OpenApiTool, OpenApiAnonymousAuthDetails
# use the following for connection auth
# from azure.ai.agents.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme
# use the following for managed identity auth
# from azure.ai.agents.models import OpenApiTool, OpenApiManagedAuthDetails, OpenApiManagedSecurityScheme

endpoint = os.environ["PROJECT_ENDPOINT"]
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]
# Initialize the project client using the endpoint and default credentials
with AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
) as project_client:
```

## Tool setup
Similarly, the OpenAPI specification is loaded from `weather.json`. An anonymous authentication object (`OpenApiAnonymousAuthDetails`) is created, as this specific API doesn't require authentication in this example. You can find an example OpenAPI spec on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/python/getting-started-agents/openapi/weather_openapi.json).

```python
    # Load the OpenAPI specification for the weather service from a local JSON file
    with open(os.path.join(os.path.dirname(__file__), "weather.json"), "r") as f:
         openapi_weather = jsonref.loads(f.read())

    # Create Auth object for the OpenApiTool (note: using anonymous auth here; connection or managed identity requires additional setup)
    auth = OpenApiAnonymousAuthDetails()
    # for connection setup
    # auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=os.environ["CONNECTION_ID"]))
    # for managed identity set up
    # auth = OpenApiManagedAuthDetails(security_scheme=OpenApiManagedSecurityScheme(audience="https://your_identity_scope.com"))

    # Initialize the main OpenAPI tool definition for weather
    openapi_tool = OpenApiTool(
        name="get_weather", spec=openapi_weather, description="Retrieve weather information for a location", auth=auth
    )
```

## Agent Creation
An agent is created using the `project_client.agents.create_agent` method.

```python
    # Create an agent configured with the combined OpenAPI tool definitions
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent",
        tools=openapi_tool.definitions,
    )
    print(f"Created agent, ID: {agent.id}")
```

## Thread Management
Create the thread and add the initial user message.

```python
    # Create a new conversation thread for the interaction
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create the initial user message in the thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather in Seattle?",
    )
    print(f"Created message, ID: {message.id}")
```


## Create a run and check the output
Create the run, check the output, and examine what tools were called during the run.

```python
    # Create and automatically process the run, handling tool calls internally
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Retrieve the steps taken during the run for analysis
    run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

    # Loop through each step to display information
    for step in run_steps:
        print(f"Step {step['id']} status: {step['status']}")

        tool_calls = step.get("step_details", {}).get("tool_calls", [])
        for call in tool_calls:
            print(f"  Tool Call ID: {call.get('id')}")
            print(f"  Type: {call.get('type')}")
            function_details = call.get("function", {})
            if function_details:
                print(f"  Function name: {function_details.get('name')}")
                print(f" function output: {function_details.get('output')}")

        print()
```


## Cleanup
After the interaction is complete, the script performs cleanup by deleting the created agent resource using `agents_client.delete_agent()` to avoid leaving unused resources. It also fetches and prints the entire message history from the thread using `agents_client.list_messages()` for review or logging.

```python
        # Delete the agent resource to clean up
        project_client.agents.delete_agent(agent.id)
        print("Deleted agent")

        # Fetch and log all messages exchanged during the conversation thread
        messages = project_client.agents.messages.list(thread_id=thread.id)
        for msg in messages:
            print(f"Message ID: {msg.id}, Role: {msg.role}, Content: {msg.content}")
```

:::zone-end


:::zone pivot="javascript"


## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```javascript
const { AgentsClient, isOutputOfType, ToolUtility } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");
const fs = require("fs");
require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"];

// Create an Azure AI Client
const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```

## Read in the OpenAPI spec

You can find an example OpenAPI spec on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/python/getting-started-agents/openapi/weather_openapi.json).

```javascript
// Read in OpenApi spec
const filePath = "./data/weatherOpenApi.json";
const openApiSpec = JSON.parse(fs.readFileSync(filePath, "utf-8"));

// Define OpenApi function
const openApiFunction = {
name: "getWeather",
spec: openApiSpec,
description: "Retrieve weather information for a location",
auth: {
    type: "anonymous",
},
default_params: ["format"], // optional
};
```

## Create an agent and enable the OpenAPI tool

```javascript
// Create OpenApi tool
const openApiTool = ToolUtility.createOpenApiTool(openApiFunction);

// Create agent with OpenApi tool
const agent = await client.createAgent(modelDeploymentName, {
name: "myAgent",
instructions: "You are a helpful agent",
tools: [openApiTool.definition],
});
console.log(`Created agent, agent ID: ${agent.id}`);
```

## Create a thread

```javascript
// Create a thread
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create a message
const message = await client.messages.create(thread.id, "user", "What's the weather in Seattle?");
console.log(`Created message, message ID: ${message.id}`);
```

## Create a run and check the output

```javascript
// Create and execute a run
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
await delay(1000);
run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
// Check if you got "Rate limit is exceeded.", then you want to get more quota
console.log(`Run failed: ${run.lastError}`);
}
console.log(`Run finished with status: ${run.status}`);

// Get most recent message from the assistant
const messagesIterator = client.messages.list(thread.id);
const messages = [];
for await (const m of messagesIterator) {
messages.push(m);
}
const assistantMessage = messages.find((msg) => msg.role === "assistant");
if (assistantMessage) {
const textContent = assistantMessage.content.find((content) => isOutputOfType(content, "text"));
if (textContent) {
    console.log(`Last message: ${textContent.text.value}`);
}
}
// Delete the agent once done
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);
```

:::zone-end

:::zone pivot="csharp"

## Configure client and OpenAPI tool
First, retrieve configuration details and create a `PersistentAgentsClient`, then define the `OpenApiToolDefinition` using the OpenAPI specification. You can find an example OpenAPI spec on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/python/getting-started-agents/openapi/weather_openapi.json).

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;

IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
var openApiSpec = configuration["OpenApiSpec"];
PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

BinaryData spec = BinaryData.FromBytes(File.ReadAllBytes(openApiSpec));

// Using anonymous auth for this example
OpenApiAnonymousAuthDetails openApiAnonAuth = new();

// Define the OpenAPI tool
OpenApiToolDefinition openApiToolDef = new(
    name: "get_weather",
    description: "Retrieve weather information for a location",
    spec: spec,
    openApiAuthentication: openApiAnonAuth,
    defaultParams: ["format"]
);
```

## Create an agent
Next, create a `PersistentAgent` with the necessary model deployment, name, instructions, and the previously defined OpenAPI tool.

```csharp
PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "Open API Tool Calling Agent",
    instructions: "You are a helpful agent.",
    tools: [openApiToolDef]
);
```

## Create thread, message, and run
Create a `PersistentAgentThread` for the conversation, add a user message to it, and then create a `ThreadRun` to process the message, waiting for its completion.

```csharp
PersistentAgentThread thread = client.Threads.CreateThread();

client.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What's the weather in Seattle?");

ThreadRun run = client.Runs.CreateRun(
    thread.Id,
    agent.Id);

// Poll for the run's completion status
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = client.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress
    || run.Status == RunStatus.RequiresAction);
```

## Display conversation messages
Retrieve and print all messages from the thread to the console in chronological order to display the conversation flow.

```csharp
Pageable<PersistentThreadMessage> messages = client.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending);

foreach (PersistentThreadMessage threadMessage in messages)
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

```

## Clean up resources
Finally, delete the created `PersistentAgentThread` and `PersistentAgent` to clean up the resources used in this example.

```csharp
client.Threads.DeleteThread(thread.Id);
client.Administration.DeleteAgent(agent.Id);
```

:::zone-end

:::zone pivot="rest-api"

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

## Create the OpenAPI Spec tool definition, agent, and thread
 
You might want to store the OpenAPI specification in another file and import the content to initialize the tool. This example is using `anonymous` as the authentication type. You can find an example OpenAPI spec on [GitHub](https://github.com/azure-ai-foundry/foundry-samples/blob/main/samples/microsoft/python/getting-started-agents/openapi/weather_openapi.json).

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
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

## Create a run and check the output
Create a run and observe that the model uses the OpenAPI Spec tool to provide a response to the user's question.

### Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread

```bash
curl curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

### Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

:::zone-end
