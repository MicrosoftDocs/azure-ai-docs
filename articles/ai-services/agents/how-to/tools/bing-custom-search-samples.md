---
title: 'How to use the Custom Bing Search with Azure AI Agent Service tool'
titleSuffix: Azure OpenAI
description: Find samples to ground Azure AI Agents using Custom Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/15/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
zone_pivot_groups: selection-bing-custom-grounding
---

# How to use Grounding with Bing Custom Search (preview)


::: zone pivot="portal"


1. Navigate to the **Agents** screen for your agent in the [Azure AI Foundry portal](https://ai.azure.com/), scroll down the Setup pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot of the agents screen in the AI Foundry portal.":::

1. Select the **Grounding with Bing Custom Search** tool.  

1. Select to create a new connection, or use an existing connection 

    1. For a new connection, select your Grounding with Bing Custom Search resource. 

1. Once you have connected to a resource, select the configuration name. 

1. Save the tool and start chatting with your agent. 

:::zone-end

::: zone pivot="python"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole, BingCustomSearchTool
from azure.identity import DefaultAzureCredential


# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
    api_version="latest",
)
```


## Create an Agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```python
bing_custom_connection = project_client.connections.get(connection_name=os.environ["BING_CUSTOM_CONNECTION_NAME"])
conn_id = bing_custom_connection.id

print(conn_id)

# Initialize agent bing custom search tool and add the connection id
bing_custom_tool = BingCustomSearchTool(connection_id=conn_id, instance_name="<config_instance_name>")

# Create agent with the bing custom search tool and process assistant run
with project_client:
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent",
        tools=bing_custom_tool.definitions
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
    role=MessageRole.USER,
    content="How many medals did the USA win in the 2024 summer olympics?",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the assistant when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Print the Agent's response message with optional citation
response_message = project_client.agents.list_messages(thread_id=thread.id).get_last_message_by_role(
    MessageRole.AGENT
)
if response_message:
    for text_message in response_message.text_messages:
        print(f"Agent response: {text_message.text.value}")
    for annotation in response_message.url_citation_annotations:
        print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
```


:::zone-end

::: zone pivot="csharp"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.TestFramework;
using NUnit.Framework;

var connectionString = System.Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
var bingConnectionName = System.Environment.GetEnvironmentVariable("BING_CONNECTION_NAME");

var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential());

AgentsClient agentClient = projectClient.GetAgentsClient();
```

## Create an Agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```csharp
AgentsClient agentClient = projectClient.GetAgentsClient();
ConnectionResponse bingConnection = await projectClient.GetConnectionsClient().GetConnectionAsync(bingConnectionName);
var connectionId = bingConnection.Id;
var instanceName = "<your_config_instance_name>";

SearchConfigurationList searchConfigurationList = new SearchConfigurationList(
    new List<SearchConfiguration>
    {
        new SearchConfiguration(connectionId, instanceName)
    });

BingCustomSearchToolDefinition bingGroundingTool = new(searchConfigurationList);
Agent agent = await agentClient.CreateAgentAsync(
    model: modelDeploymentName,
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: [ bingGroundingTool ]);
```

## Create a thread

```csharp
AgentThread thread = agentClient.CreateThread();

// Create message to thread
ThreadMessage message = agentClient.CreateMessage(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```csharp

// Run the agent
ThreadRun run = agentClient.CreateRun(thread, agent);
do
{
    Thread.Sleep(TimeSpan.FromMilliseconds(500));
    run = agentClient.GetRun(thread.Id, run.Id);
}
while (run.Status == RunStatus.Queued
    || run.Status == RunStatus.InProgress);

Assert.AreEqual(
    RunStatus.Completed,
    run.Status,
    run.LastError?.Message);

PageableList<ThreadMessage> messages = agentClient.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

foreach (ThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            string response = textItem.Text;
            if (textItem.Annotations != null)
            {
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextUrlCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UrlCitation.Title}]({urlAnnotation.UrlCitation.Url})");
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

agentClient.DeleteThread(threadId: thread.Id);
agentClient.DeleteAgent(agentId: agent.Id);
```

:::zone-end

::: zone pivot="javascript"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```javascript
const { AIProjectsClient, ToolUtility, isOutputOfType } = require("@azure/ai-projects");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

const connectionString =
  process.env["AZURE_AI_PROJECTS_CONNECTION_STRING"] || "<project connection string>";

// Create an Azure AI Client from a connection string, copied from your AI Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
const client = AIProjectsClient.fromConnectionString(
    connectionString || "",
    new DefaultAzureCredential(),
);
```


## Create an Agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```javascript
const bingCustomSearchConnection = await client.connections.getConnection(
    process.env["BING_CUSTOM_SEARCH"] || "<connection-name>",
);
console.log(`Bing custom search connection ID:`, bingCustomSearchConnection.id);

// Initialize agent bing custom search tool with the connection id
const bingCustomSearchTool = ToolUtility.createBingCustomSearchTool([
    {
        connectionId: bingCustomSearchConnection.id,
        instanceName: bingCustomSearchConnection.name,
    },
]);

// Create agent with the bing tool and process assistant run
const agent = await client.agents.createAgent("gpt-4o", {
    name: "my-agent",
    instructions:
        "You are a customer support chatbot. Use the tools provided and your knowledge base to best respond to customer queries",
    tools: [bingCustomSearchTool.definition]
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

Create a run and observe that the model uses the Grounding with Bing Custom Search tool to provide a response to the user's question.


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

:::zone-end


::: zone pivot="rest"

>[!IMPORTANT]
> 1. This REST API allows developers to invoke the Grounding with Bing Custom Search tool through the Azure AI Foundry Agent Service. It does not send calls to the Grounding with Bing Custom Search API directly. 

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.


## Create an Agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

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
            "type": "bing_custom_search",
            "bing_custom_search": {
                "search_configurations": [
                    {
                        "connection_id": <your_custom_search_connecion_id>,
                        "instance_name": <your_custom_search_configuration_name>, 
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
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "<ask a question tailored towards your web domains>"
    }'
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Custom Search tool to provide a response to the user's question.

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