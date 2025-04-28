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

# How to use Grounding with Bing Custom Search 


::: zone pivot="portal"


1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and use the Grounding with Bing Custom Search tool in your agent. 

    1. Select the agent you created. 

    1. Select to add a knowledge tool. 

    1. Select the **Grounding with Bing Custom Search** tool  

    1. Select to create a new connection or use an existing connection 

    1. For new connection, select your Grounding with Bing Custom Search resource. 

    1. Once you have connected to a resource, select the configuration name. 

    1. Save the tool and start chatting with your agent. 
:::zone-end

::: zone pivot="javascript"

## Step 1: Create a project client

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


## Step 2: Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

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

## Step 3: Create a thread

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

## Step 4: Create a run and check the output

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

:::zone-end

::: zone pivot="python"

## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python

import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole, BingCustomSearchTool
from azure.identity import DefaultAzureCredential


# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=os.environ["PROJECT_CONNECTION_STRING"],
)

```


## Step 2: Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

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

## Step 3: Create a thread

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

## Step 4: Create a run and check the output

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
