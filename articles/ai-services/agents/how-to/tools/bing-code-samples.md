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

1. In the [Azure AI Foundry portal](https://ai.azure.com/) navigate to the **Agents** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

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
from azure.ai.agents.models import BingGroundingTool

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set
subscription_id = os.environ["SUBSCRIPTION_ID"]  
resource_group = os.environ["RESOURCE_GROUP"] 
project_name = os.environ["PROJECT_NAME"]

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
    subscription_id=subscription_id,
    resource_group_name=resource_group_name,
    project_name=project_name
)
```


## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```python
conn_id = os.environ["BING_CONNECTION_ID"]  # Ensure the BING_CONNECTION_ID environment variable is set

with project_client:
    # Initialize the Bing Grounding tool with the connection ID
    # freshness, count, set_lang and market are optional parameters
    bing = BingGroundingTool(connection_id=conn_id, freshness="day", count=5, set_lang="en", market="us")

    # Create an agent with the Bing Grounding tool
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=bing.definitions,  # Attach the Bing Grounding tool
    )
    print(f"Created agent, ID: {agent.id}")
```

## Create a thread

```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Add a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="What is the weather in Seattle today?",  # Message content
)
print(f"Created message, ID: {message['id']}")
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```python
# Create and process an agent run
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages:
    print(f"Role: {message.role}, Content: {message.content}")

# Delete the agent when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
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
BingGroundingSearchConfiguration searchConfig = new BingGroundingSearchConfiguration(bingConnectionId)
{ 
    Count = 5,
    Freshness = "Week"
};

// Create the BingGroundingToolDefinition object used when creating the agent
BingGroundingToolDefinition bingGroundingTool = new BingGroundingToolDefinition(
    new BingGroundingSearchToolParameters(
        [
            searchConfig
        ]
    )
);

// Create the Agent
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "Use the bing grounding tool to answer questions.",
    tools: [bingGroundingTool]
);
```

## Create a thread and run

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
PersistentThreadMessage message = agentClient.Messages.CreateMessage(
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
Pageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Process messages in order
foreach (PersistentThreadMessage threadMessage in messages)
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
                    if (annotation is MessageTextUriCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UriCitation.Title}]({urlAnnotation.UriCitation.Uri})");
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

## Optionally output the run steps used by the agent

```csharp
// Retrieve the run steps used by the agent and print those to the console
Console.WriteLine("Run Steps used by Agent:");
Pageable<RunStep> runSteps = agentClient.Runs.GetRunSteps(run);

foreach (var step in runSteps)
{
    Console.WriteLine($"Step ID: {step.Id}, Total Tokens: {step.Usage.TotalTokens}, Status: {step.Status}, Type: {step.Type}");

    if (step.StepDetails is RunStepMessageCreationDetails messageCreationDetails)
    {
        Console.WriteLine($"   Message Creation Id: {messageCreationDetails.MessageCreation.MessageId}");
    }
    else if (step.StepDetails is RunStepToolCallDetails toolCallDetails)
    {
        // We know this agent only has the Bing Grounding tool, so we can cast it directly
        foreach (RunStepBingGroundingToolCall toolCall in toolCallDetails.ToolCalls)
        {
            Console.WriteLine($"   Tool Call Details: {toolCall.GetType()}");

            foreach (var result in toolCall.BingGrounding)
            {
                Console.WriteLine($"      {result.Key}: {result.Value}");
            }
        }
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
const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project connection string>";

// Create an Azure AI Client
const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```


## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/).

```javascript

const connectionId = process.env["AZURE_BING_CONNECTION_ID"] || "<connection-name>";
// Initialize agent bing tool with the connection id
const bingTool = ToolUtility.createBingGroundingTool([{ connectionId: connectionId }]);

// Create agent with the bing tool and process assistant run
const agent = await client.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [bingTool.definition],
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Create a thread

```javascript
// Create thread for communication
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create message to thread
const message = await client.messages.create(
  thread.id,
  "user",
  "How does wikipedia explain Euler's Identity?",
);
console.log(`Created message, message ID : ${message.id}`);
```

## Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.


```javascript

// Create and process agent run in thread with tools
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
  console.log(`Run failed: ${run.lastError?.message}`);
}
console.log(`Run finished with status: ${run.status}`);

// Delete the assistant when done
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);

// Fetch and log all messages
const messagesIterator = client.messages.list(thread.id);
console.log(`Messages:`);

// Get the first message
const firstMessage = await messagesIterator.next();
if (!firstMessage.done && firstMessage.value) {
  const agentMessage = firstMessage.value.content[0];
  if (isOutputOfType(agentMessage, "text")) {
    const textContent = agentMessage;
    console.log(`Text Message Content - ${textContent.text.value}`);
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

[See the full sample for Grounding with Bing Search.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_bing_grounding.py)
