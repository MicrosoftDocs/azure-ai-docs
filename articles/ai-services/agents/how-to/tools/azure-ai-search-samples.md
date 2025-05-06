---
title: 'How to use Azure AI Search in Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to ground Azure AI Agents using Azure AI Search.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/11/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
zone_pivot_groups: selection-azure-ai-search
---

# How to use an existing Azure AI Search index with the Azure AI Search tool

This article shows how to use an existing Azure AI Search index with the Azure AI Search tool.

## Prerequisites
Complete the [Azure AI Search tool setup](../../how-to/tools/azure-ai-search.md?pivot=overview-azure-ai-search).

:::zone pivot="portal"

1. Go to the Azure AI Foundry portal, and navigate to the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Azure AI Search** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

:::zone-end

:::zone pivot="python"

## Step 1: Create an Azure AI Client
First, create an Azure AI Client using the connection string of your project.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import AzureAISearchTool

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery" 
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;my-subscription-id;my-resource-group;my-hub-name

connection_string = os.environ["PROJECT_CONNECTION_STRING"] 

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=connection_string,
)
```

## Step 2: Get the connection ID for the Azure AI Search resource
Get the connection ID of the Azure AI Search connection in the project. You can use the code snippet to print the connection ID of all the Azure AI Search connections in the project.

```python
# AI Search resource connection ID
# This code looks for the AI Search Connection ID and saves it as variable conn_id

# If you have more than one AI search connection, try to establish the value in your .env file.
# Extract the connection list.
conn_list = project_client.connections._list_connections()["value"]
conn_id = ""

# Search in the metadata field of each connection in the list for the azure_ai_search type and get the id value to establish the variable
for conn in conn_list:
    metadata = conn["properties"].get("metadata", {})
    if metadata.get("type", "").upper() == "AZURE_AI_SEARCH":
        conn_id = conn["id"]
        break
```

## Step 3: Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.

```python
# TO DO: replace this value with the connection ID of the search index
conn_id =  "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-azure-ai-search-connection-name>"

# Initialize agent AI search tool and add the search index connection ID and index name
# TO DO: replace <your-index-name> with the name of the index you want to use
ai_search = AzureAISearchTool(index_connection_id=conn_id, index_name="<your-index-name>",
query_type="<select-search-type>")
```

## Step 4: Create an agent with the Azure AI Search tool enabled
Change the model to the one deployed in your project. You can find the model name in the Azure AI Foundry under the **Models** tab. You can also change the name and instructions of the agent to suit your needs.

```python
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=ai_search.definitions,
    tool_resources = ai_search.resources,
)
print(f"Created agent, ID: {agent.id}")
```

## Step 5: Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index. The example assumes your Azure AI Search index contains information about health care plans.

```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")
 
# Create a message
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="what are my health insurance plan coverage types?",
)
print(f"Created message, message ID: {message.id}")
    
# Run the agent
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")
 
if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# Get messages from the thread 
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
    
assistant_message = ""
for message in messages.data:
    if message["role"] == "assistant":
        assistant_message = message["content"][0]["text"]["value"]

# Get the last message from the sender
print(f"Assistant response: {assistant_message}")
```

:::zone-end

:::zone pivot="csharp"

## Step 1: Create an Azure AI Client
First, create an Azure AI Client using the connection string of your project.

```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.TestFramework;
using NUnit.Framework;
using System.Collections.Generic;

// Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
var clientOptions = new AIProjectClientOptions();

// Adding the custom headers policy
clientOptions.AddPolicy(new CustomHeadersPolicy(), HttpPipelinePosition.PerCall);
var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential(), clientOptions);
```

## Step 2: Get the connection ID for the Azure AI Search resource
Get the connection ID of the Azure AI Search connection in the project.

```csharp
ListConnectionsResponse connections = await projectClient.GetConnectionsClient().GetConnectionsAsync(ConnectionType.AzureAISearch).ConfigureAwait(false);

if (connections?.Value == null || connections.Value.Count == 0)
{
    throw new InvalidOperationException("No connections found for the Azure AI Search.");
}
```

## Step 3: Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.

```csharp
// TO DO: replace this value with the connection ID of the search index
ConnectionResponse connection = connections.Value[0];

// Initialize agent Azure AI search tool and add the search index connection ID and index name
// TO DO: replace <your-index-name> with the name of the index you want to use
ToolResources searchResource = new ToolResources
{
    AzureAISearch = new AzureAISearchResource
    {
        IndexList = { new IndexResource(connection.Id, "<your-index-name>", "<select-search-type>") }
    }
};
```

## Step 4: Create an agent with the Azure AI Search tool enabled
Change the model to the one deployed in your project. You can find the model name in the Azure AI Foundry under the **Models** tab. You can also change the name and instructions of the agent to suit your needs.

```csharp
AgentsClient agentClient = projectClient.GetAgentsClient();

Response<Agent> agentResponse = await agentClient.CreateAgentAsync(
    model: "gpt-4o-mini",
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: new List<ToolDefinition> { new AzureAISearchToolDefinition() },
    toolResources: searchResource);
Agent agent = agentResponse.Value;
```

## Step 5: Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

```csharp
// Create thread for communication
Response<AgentThread> threadResponse = await agentClient.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

// Create message to thread
Response<ThreadMessage> messageResponse = await agentClient.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "what are my health insurance plan coverage types?");
ThreadMessage message = messageResponse.Value;

// Run the agent
Response<ThreadRun> runResponse = await agentClient.CreateRunAsync(thread, agent);

do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    runResponse = await agentClient.GetRunAsync(thread.Id, runResponse.Value.Id);
}
while (runResponse.Value.Status == RunStatus.Queued
    || runResponse.Value.Status == RunStatus.InProgress);

Response<PageableList<ThreadMessage>> afterRunMessagesResponse
    = await agentClient.GetMessagesAsync(thread.Id);
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

:::zone-end

:::zone pivot="javascript"

## Step 1: Create an Azure AI Client
First, create an Azure AI Client using the connection string of your project.

```javascript
const connectionString =
  process.env["AZURE_AI_PROJECTS_CONNECTION_STRING"] || "<project connection string>";

if (!connectionString) {
  throw new Error("AZURE_AI_PROJECTS_CONNECTION_STRING must be set in the environment variables");
}

const client = AIProjectsClient.fromConnectionString(
    connectionString || "",
    new DefaultAzureCredential(),
);
```

## Step 2: Get the connection ID for the Azure AI Search resource
Get the connection ID of the Azure AI Search connection in the project.

```javascript
const cognitiveServicesConnectionName = "<cognitiveServicesConnectionName>";
const cognitiveServicesConnection = await client.connections.getConnection(
  cognitiveServicesConnectionName,
);
```

## Step 3: Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.

```javascript
const azureAISearchTool = ToolUtility.createAzureAISearchTool(
  cognitiveServicesConnection.id,
  cognitiveServicesConnection.name,
);

// Create agent with the Azure AI search tool
const agent = await client.agents.createAgent("gpt-4o-mini", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [azureAISearchTool.definition],
  toolResources: azureAISearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Step 4: Create an agent with the Azure AI Search tool enabled

Change the model to the one deployed in your project. You can find the model name in the Azure AI Foundry under the **Models** tab. You can also change the name and instructions of the agent to suit your needs.

```javascript
const agent = await client.agents.createAgent("gpt-4o-mini", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [azureAISearchTool.definition],
  toolResources: azureAISearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```


## Step 5: Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

```javascript
// create a thread
const thread = await client.agents.createThread();

// add a message to thread
await client.agents.createMessage(
  thread.id, {
  role: "user",
  content: "what are my health insurance plan coverage types?",
});

// Intermission is now correlated with thread
// Intermission messages will retrieve the message just added

// create a run
const streamEventMessages = await client.agents.createRun(thread.id, agent.id).stream();

for await (const eventMessage of streamEventMessages) {
  switch (eventMessage.event) {
    case RunStreamEvent.ThreadRunCreated:
      break;
    case MessageStreamEvent.ThreadMessageDelta:
      {
        const messageDelta = eventMessage.data;
        messageDelta.delta.content.forEach((contentPart) => {
          if (contentPart.type === "text") {
            const textContent = contentPart;
            const textValue = textContent.text?.value || "No text";
          }
        });
      }
      break;

    case RunStreamEvent.ThreadRunCompleted:
      break;
    case ErrorEvent.Error:
      console.log(`An error occurred. Data ${eventMessage.data}`);
      break;
    case DoneEvent.Done:
      break;
  }
}

// Print the messages from the agent
const messages = await client.agents.listMessages(thread.id);

// Messages iterate from oldest to newest
// messages[0] is the most recent
for (let i = messages.data.length - 1; i >= 0; i--) {
  const m = messages.data[i];
  if (isOutputOfType<MessageTextContentOutput>(m.content[0], "text")) {
    const textContent = m.content[0];
    console.log(`${textContent.text.value}`);
    console.log(`---------------------------------`);
  }
}
```

:::zone-end

:::zone pivot="rest"

## Step 1: Create an Azure AI Client
Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`.

## Step 2: Get the connection ID for the Azure AI Search resource
Follow the next section on how to get the connection ID from the Azure AI Foundry.

The second way to get the connection ID is to navigate to the project in the Azure AI Foundry and click on the **Connected resources** tab and then select your Azure AI Search resource.

:::image type="content" source="../../media/tools/ai-search/success-connection.png" alt-text="A screenshot of an AI Search resource connection page in Azure AI Foundry." lightbox="../../media/tools/ai-search/success-connection.png":::

In the URL, you see the wsid=/subscription/your-subscription-id..., this is the connection ID you need to use. Copy everything that comes after wsid=.

:::image type="content" source="../../media/tools/ai-search/connection-id.png" alt-text="A screenshot of an AI Search resource connection and how to copy the connection ID." lightbox="../../media/tools/ai-search/connection-id.png":::

## Step 3: Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.

```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "instructions": "You are a helpful agent.",
        "name": "my-agent",
        "tools": [
          {"type": "azure_ai_search"}
        ],
        "model": "gpt-4o-mini",
        "tool_resources": {
            "azure_ai_search": {
              "indexes": [
                  {
                      "index_connection_id": "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-azure-ai-search-connection-name>",
                      "index_name": "<your-index-name>",
                      "query_type": "semantic"
                  }
              ]
            }
        }
      }'
```

### Step 4: Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

#### Create a thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

#### Add a user question to the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "what are my health insurance plan coverage types?"
    }'
```

#### Run the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

#### Retrieve the status of the run

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

#### Retrieve the agent response

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end