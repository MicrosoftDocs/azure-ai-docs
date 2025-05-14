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

## Create an Azure AI Client
First, create an Azure AI Client using the endpoint of your project.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Retrieve the endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),
    api_version="latest",
)
```

## Configure the Azure AI Search tool
Using the connection ID of your Azure AI Search resource, configure the Azure AI Search tool to use your Azure AI Search index.

```python
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType

# Define the Azure AI Search connection ID and index name
azure_ai_conn_id = os.environ["AZURE_AI_CONNECTION_ID"]
index_name = "sample_index"

# Initialize the Azure AI Search tool
ai_search = AzureAISearchTool(
    index_connection_id=azure_ai_conn_id,
    index_name=index_name,
    query_type=AzureAISearchQueryType.SIMPLE,  # Use SIMPLE query type
    top_k=3,  # Retrieve the top 3 results
    filter="",  # Optional filter for search results
)
```

## Create an agent with the Azure AI Search tool enabled
Create an agent with the Azure AI Search tool attached. Change the model to the one deployed in your project.

```python
# Define the model deployment name
model_deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

# Create an agent with the Azure AI Search tool
agent = project_client.agents.create_agent(
    model=model_deployment_name,
    name="my-agent",
    instructions="You are a helpful agent",
    tools=ai_search.definitions,
    tool_resources=ai_search.resources,
)
print(f"Created agent, ID: {agent.id}")
```

## Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

```python
from azure.ai.agents.models import MessageRole, ListSortOrder

# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Send a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="What is the temperature rating of the cozynights sleeping bag?",
)
print(f"Created message, ID: {message['id']}")

# Create and process a run with the specified thread and agent
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages in the thread
messages = project_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages.data:
    print(f"Role: {message.role}, Content: {message.content}")
```

## Clean up resources
After completing the operations, delete the agent to clean up resources.

```python
# Delete the agent
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end

:::zone pivot="csharp"

## Create a project client
Create a client object, which will contain the project endpoint for connecting to your AI project and other resources.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System;
using System.Threading;

// Get Connection information from app configuration
IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
var azureAiSearchConnectionId = configuration["AzureAiSearchConnectionId"];

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Configure the Azure AI Search tool
Using the AI Search Connection ID, configure the Azure AI Search tool to use your Azure AI Search index.

```csharp
AzureAISearchResource searchResource = new(
    indexConnectionId: azureAiSearchConnectionId,
    indexName: "sample_index",
    topK: 5,
    filter: "category eq 'sleeping bag'",
    queryType: AzureAISearchQueryType.Simple
);

ToolResources toolResource = new() { AzureAISearch = searchResource };

```

## Create an agent with the Azure AI Search tool enabled
Change the model to the one deployed in your project. You can find the model name in the Azure AI Foundry under the **Models** tab. You can also change the name and instructions of the agent to suit your needs.

```csharp
// Create an agent with Tools and Tool Resources
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "You are a helpful agent.",
    tools: [new AzureAISearchToolDefinition()],
    toolResources: toolResource);

```

## Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

```csharp
// Create thread for communication
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
ThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What is the temperature rating of the cozynights sleeping bag?");
ThreadRun run = agentClient.Runs.CreateRun(thread, agent);

```

## Wait for the agent to complete and print the output

Wait for the agent to complete the run and print output to console.

```csharp
// Wait for the agent to finish running
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = agentClient.Runs.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

// Confirm that the run completed successfully
if (run.Status != RunStatus.Completed)
{
    throw new Exception("Run did not complete successfully, error: " + run.LastError?.Message);
}

// Retrieve the messages from the agent client
Pageable<ThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Process messages in order
foreach (ThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            // We need to annotate only Agent messages.
            if (threadMessage.Role == MessageRole.Agent && textItem.Annotations.Count > 0)
            {
                string annotatedText = textItem.Text;

                // If we have Text URL citation annotations, reformat the response to show title & URL for citations
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUrlCitationAnnotation urlAnnotation)
                    {
                        annotatedText = annotatedText.Replace(
                            urlAnnotation.Text,
                            $" [see {urlAnnotation.UrlCitation.Title}] ({urlAnnotation.UrlCitation.Url})");
                    }
                }
                Console.Write(annotatedText);
            }
            else
            {
                Console.Write(textItem.Text);
            }
        }
        else if (contentItem is MessageImageFileContent imageFileItem)
        {
            Console.Write($"<image from ID: {imageFileItem.FileId}");
        }
        Console.WriteLine();
    }
}
```
## Clean up resources

Clean up the resources from this sample.

```csharp

// Delete thread and agent
agentClient.Threads.DeleteThread(thread.Id);
agentClient.Administration.DeleteAgent(agent.Id);

```

:::zone-end

:::zone pivot="javascript"

## Create an Azure AI Client
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

## Get the connection ID for the Azure AI Search resource
Get the connection ID of the Azure AI Search connection in the project.

```javascript
const cognitiveServicesConnectionName = "<cognitiveServicesConnectionName>";
const cognitiveServicesConnection = await client.connections.getConnection(
  cognitiveServicesConnectionName,
);
```

## Configure the Azure AI Search tool
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

## Create an agent with the Azure AI Search tool enabled

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


## Ask the agent questions about data in the index
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

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

## Get the connection ID for the Azure AI Search resource

To get the connection ID, navigate to the project in the Azure AI Foundry and click on the **Connected resources** tab and then select your Azure AI Search resource.

:::image type="content" source="../../media/tools/ai-search/success-connection.png" alt-text="A screenshot of an AI Search resource connection page in Azure AI Foundry." lightbox="../../media/tools/ai-search/success-connection.png":::

In the URL, you see the `wsid=/subscription/your-subscription-id...`, this is the connection ID you need to use. Copy everything that comes after `wsid=`.

:::image type="content" source="../../media/tools/ai-search/connection-id.png" alt-text="A screenshot of an AI Search resource connection and how to copy the connection ID." lightbox="../../media/tools/ai-search/connection-id.png":::

## Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
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

### Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index.

#### Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

#### Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "what are my health insurance plan coverage types?"
    }'
```
#### Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

#### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

#### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end
