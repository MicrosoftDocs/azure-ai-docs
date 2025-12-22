---
title: "How to use the Custom Bing Search with Foundry Agent Service tool"
titleSuffix: Azure OpenAI
description: Find samples to ground Microsoft Foundry Agents using Custom Bing Search results.
ai-usage: ai-assisted
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 12/22/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - azure-ai-agents
  - build-2025
zone_pivot_groups: selection-bing-custom-grounding
---

# How to use Grounding with Bing Custom Search (preview)

> [!NOTE]
> This article refers to the classic version of the agents API. 
>
> 🔍 [View the new Grounding with Bing Search documentation](../../../default/agents/how-to/tools/bing-tools.md).

This article provides step-by-step instructions and code samples for using the Grounding with Bing Custom Search tool in the Foundry Agent Service.

::: zone pivot="portal"
1. Go to the **Agents** screen for your agent in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). Scroll down the Setup pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot of the agents screen in the Foundry portal.":::

1. Select the **Grounding with Bing Custom Search** tool.  

1. Select to create a new connection or use an existing connection. 

    1. For a new connection, select your Grounding with Bing Custom Search resource. 

1. After you connect to a resource, select the configuration name. 

1. Save the tool and start chatting with your agent. 

:::zone-end

::: zone pivot="python"
## Prerequisites

* Your Foundry Project endpoint.

    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`. 

* The name of your Grounding with Bing Custom Search resource name. Find it in the Foundry portal by selecting **Management center** from the left navigation menu. Then select **Connected resources**.
    
    :::image type="content" source="../../media/tools/bing/custom-resource-name.png" alt-text="A screenshot showing the Grounding with Bing Custom Search resource name. " lightbox="../../media/tools/bing/custom-resource-name.png":::

    Save this resource name to an environment variable named `BING_CUSTOM_CONNECTION_NAME`. 

* The name of your Grounding with Bing Custom Search configuration, which contains the URLs you want to allow or disallow. Find it by navigating to the overview page for your resource in the [Azure portal](https://portal.azure.com/). Select **Configurations**, then select your configuration. 

    :::image type="content" source="../../media/tools/bing/custom-connection-name.png" alt-text="A screenshot showing the Grounding with Bing Custom Search configuration name. " lightbox="../../media/tools/bing/custom-connection-name.png":::

    Save this configuration name to an environment variable named `BING_CUSTOM_INSTANCE_NAME`. 

* The names of your model's deployment name. Find it in **Models + Endpoints** in the left navigation menu. 

    :::image type="content" source="../../media/tools/model-deployment-portal.png" alt-text="A screenshot showing the model deployment screen the Foundry portal." lightbox="../../media/tools/model-deployment-portal.png":::
    
    Save the name of your model deployment name as an environment variable named `MODEL_DEPLOYMENT_NAME`. 

## Create a project client

Create a client object that holds the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingCustomSearchTool


# Create an Azure AI Client from an endpoint, copied from your Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)
```

## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent.

```python
bing_custom_connection = project_client.connections.get(name=os.environ["BING_CUSTOM_CONNECTION_NAME"])
conn_id = bing_custom_connection.id

print(conn_id)

configuration_name = os.environ["BING_CUSTOM_INSTANCE_NAME"]
# Initialize Bing Custom Search tool with connection id and configuration name
bing_custom_tool = BingCustomSearchTool(connection_id=conn_id, instance_name=configuration_name)

# Create agent with the bing custom search tool and process assistant run
with project_client:
    agents_client = project_client.agents

    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent",
        tools=bing_custom_tool.definitions,
    )
    print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create thread for communication
thread = agents_client.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
message = agents_client.messages.create(
    thread_id=thread.id,
    role="user",
    content="How many medals did the USA win in the 2024 summer olympics?",
)
print(f"Created message, ID: {message.id}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

```python
# Create and process Agent run in thread with tools
run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Uncomment these lines to delete the Agent when done
#agents_client.delete_agent(agent.id)
#print("Deleted agent")

# Fetch and log all messages
messages = agents_client.messages.list(thread_id=thread.id)
for msg in messages:
    if msg.text_messages:
        for text_message in msg.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in msg.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
```

### Understand URL citations in the response

When the agent response includes URL citations, you can show them to users as a list of references.

In the Python SDK, you can find the answer text in `msg.text_messages[*].text.value`. You can find the citations in `msg.url_citation_annotations[*].url_citation`.

The following example prints the answer followed by a de-duplicated list of references:

```python
messages = agents_client.messages.list(thread_id=thread.id)
for msg in messages:
  if msg.text_messages:
    answer = "\n".join(t.text.value for t in msg.text_messages)
    print(answer)

  if msg.url_citation_annotations:
    print("\nReferences")
    seen_urls = set()
    for ann in msg.url_citation_annotations:
      url = ann.url_citation.url
      title = ann.url_citation.title or url
      if url not in seen_urls:
        print(f"- {title}: {url}")
        seen_urls.add(url)
```
:::zone-end

<!--
::: zone pivot="csharp"

## Create a project client

Create a client object that holds the connection string for connecting to your AI project and other resources.

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

## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

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
-->
<!--
::: zone pivot="javascript"

## Create a project client

Create a client object that holds the connection string for connecting to your AI project and other resources.

```javascript
const { AIProjectsClient, ToolUtility, isOutputOfType } = require("@azure/ai-projects");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

const connectionString =
  process.env["AZURE_AI_PROJECTS_CONNECTION_STRING"] || "<project connection string>";

// Create an Azure AI Client from a connection string, copied from your Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
const client = AIProjectsClient.fromConnectionString(
    connectionString || "",
    new DefaultAzureCredential(),
);
```


## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

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
-->

::: zone pivot="rest"

>[!IMPORTANT]
> * This REST API enables developers to invoke the Grounding with Bing Custom Search tool through the Agent Service. It doesn't send calls to the Grounding with Bing Custom Search API directly.
> * The following samples apply if you're using **Foundry Project** resource with Microsoft Fabric tool through REST API call.
> * Your connection ID should be in this format: `/subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-bing-connection-name>`.

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT`, and `API_VERSION`.


## Create an agent with the Grounding with Bing Custom Search tool enabled

To make the Grounding with Bing Custom Search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Foundry portal](https://ai.azure.com/?cid=learnDocs).

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
                        "connection_id": /subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-bing-connection-name>,
                        "instance_name": <your_custom_search_configuration_name>, 
                        "count": 7,
                        "market": "en-US", 
                        "set_lang": "en",
                        "freshness": "day",
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
