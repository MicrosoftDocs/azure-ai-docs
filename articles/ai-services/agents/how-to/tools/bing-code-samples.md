---
title: 'Grounding with Bing Search code samples'
titleSuffix: Azure AI Foundry
description: Find code samples to ground Azure AI Agents using Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/09/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-bing-grounding-code
ms.custom: azure-ai-agents-code
---

# How to use Grounding with Bing Search

Use this article to find step-by-step instructions and code samples for Grounding with Bing search.

## Prerequisites

* A [connected Grounding with Bing Search resource](./bing-grounding.md#setup).
* Your connection ID needs to be in this format: `/subscriptions/<subscription_id>/resourceGroups/<resource_group_name>/providers/Microsoft.CognitiveServices/accounts/<ai_service_name>/projects/<project_name>/connections/<connection_name>`

> [!IMPORTANT]
> There are requirements for displaying Grounding with Bing Search results. See the [overview article](./bing-grounding.md#how-to-display-grounding-with-bing-search-results) for details. 

::: zone pivot="portal"

1. In the [Azure AI Foundry portal](https://ai.azure.com/) navigate to the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Grounding with Bing Search** and follow the prompts to add the tool. Note you can add only one per agent.

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.
   
   :::image type="content" source="../../media/tools/bing/choose-bing-connection.png" alt-text="A screenshot showing the button for creating a new connection." lightbox="../../media/tools/bing/choose-bing-connection.png":::

1. Select the Grounding with Bing Search resource you want to use and click to add connection. 

   :::image type="content" source="../../media/tools/bing/create-bing-connection.png" alt-text="A screenshot showing available Grounding with Bing Search connections." lightbox="../../media/tools/bing/create-bing-connection.png":::

::: zone-end

::: zone pivot="python"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import BingGroundingTool


# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)
```


## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```python
bing_connection = project_client.connections.get(
    connection_name=os.environ["BING_CONNECTION_NAME"]
)
conn_id = bing_connection.id

print(conn_id)

# Initialize agent bing tool and add the connection id
bing = BingGroundingTool(connection_id=conn_id)

# Create agent with the bing tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=bing.definitions,
        headers={"x-ms-enable-preview": "true"}
    )
    print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="What is the top news today",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Retrieve run step details to get Bing Search query link
# To render the webpage, we recommend you replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like "https://www.bing.com/search?q={search query}"
run_steps = project_client.agents.list_run_steps(run_id=run.id, thread_id=thread.id)
run_steps_data = run_steps['data']
print(f"Last run step detail: {run_steps_data}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the assistant when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```


::: zone-end
 
::: zone pivot="csharp"
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
var bingConnectionId = configuration["BingConnectionId"];

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```csharp
// Create the BingGroundingToolDefinition object used when creating the agent
BingGroundingToolDefinition bingGroundingTool = new BingGroundingToolDefinition(
    new BingGroundingSearchConfigurationList(
        [
            new BingGroundingSearchConfiguration(bingConnectionId)
        ]
    )
);

// Create the Agent
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "You are a helpful agent.",
    tools: [bingGroundingTool]
);
```

## Create a thread and run

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
ThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");

ThreadRun run = agentClient.Runs.CreateRun(thread, agent);

```

## Wait for the agent to complete and print the output

First, wait for the agent to complete the run by polling its status. Observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

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
```

Then, retrieve and process the messages from the completed run.

```csharp
// Retrieve all messages from the agent client
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
            string response = textItem.Text;

            // If we have Text URL citation annotations, reformat the response to show title & URL for citations
            if (textItem.Annotations != null)
            {
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUrlCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, 
                            $" [{urlAnnotation.UrlCitation.Title}]({urlAnnotation.UrlCitation.Url})");
                    }
                }
            }
            Console.Write($"Agent response: {response}");
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
agentClient.Threads.DeleteThread(threadId: thread.Id);
agentClient.Administration.DeleteAgent(agentId: agent.Id);

```

::: zone-end

::: zone pivot="javascript"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```javascript
const connectionString =
  process.env["AZURE_AI_PROJECTS_CONNECTION_STRING"] || "<project connection string>";

if (!connectionString) {
  throw new Error("AZURE_AI_PROJECTS_CONNECTION_STRING must be set.");
}
const client = AIProjectsClient.fromConnectionString(
    connectionString || "",
    new DefaultAzureCredential(),
);
```


## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```javascript
const bingGroundingConnectionId = "<bingGroundingConnectionId>";
const bingTool = ToolUtility.createConnectionTool(connectionToolType.BingGrounding, [
  bingGroundingConnectionId,
]);

const agent = await client.agents.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [bingTool.definition],
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Create a thread

```javascript
// create a thread
const thread = await client.agents.createThread();

// add a message to thread
await client.agents.createMessage(
    thread.id, {
    role: "user",
    content: "What is the weather in Seattle?",
});
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```javascript

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

::: zone-end


::: zone pivot="rest"

>[!IMPORTANT]
> 1. This REST API allows developers to invoke the Grounding with Bing Search tool through the Azure AI Foundry Agent Service. It does not send calls to the Grounding with Bing Search API directly. 

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.


## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "instructions": "You are a helpful agent.",
        "name": "my-agent",
        "model": "gpt-4o",
        "tools": [
          {
            "type": "bing_grounding",
            "bing_grounding": {
                "search_configurations": [
                    {
                        "connection_id": "<your_connection_id>",
                        "count": 7, 
                        "market": "en-US", 
                        "set_lang": "en", 
                        "freshness": "7d",
                    }
                ]
            }
          }
        ]
      }'
```

## Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "What is the weather in Seattle?"
    }'
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

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

::: zone-end

## Next steps

[See the full sample for Grounding with Bing Search.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_bing_grounding.py)
