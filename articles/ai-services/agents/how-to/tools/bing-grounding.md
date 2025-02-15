---
title: 'How to use Grounding with Bing Search in Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 01/07/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-bing-grounding
ms.custom: azure-ai-agents
---

# Grounding with Bing Search 

::: zone pivot="overview"

**Grounding with Bing Search** allows your Azure AI Agents to incorporate real-time public web data when generating responses. You need to create a Grounding with Bing Search resource, and then connect this resource to your Azure AI Agents. When a user sends a query, Azure AI Agents decide if Grounding with Bing Search should be leveraged or not. If so, it will leverage Bing to search over public web data and return relevant chunks. Lastly, Azure AI Agents will use returned chunks to generate a response.  

You can ask questions such as "*what is the top news today*" or "*what is the recent update in the retail industry in the US?*", which require real-time public data.

Developers and end users don't have access to raw content returned from Grounding with Bing Search. The response, however, includes citations with links to the websites used to generate the response, and a link to the Bing query used for the search. These two *References* must be retained and displayed in the exact form provided by Microsoft, as per Grounding with Bing Search's [Use and Display Requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal#use-and-display-requirements). See the [how to display Grounding with Bing Search results](#how-to-display-grounding-with-bing-search-results) section for details.

>[!IMPORTANT]
> 1. Your usage of Grounding with Bing Search can incur costs. See the [pricing page](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> 1. By creating and using a Grounding with Bing Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the terms available at https://www.microsoft.com/en-us/bing/apis/grounding-legal, which may be updated from time to time.
> 1. When you use Grounding with Bing Search, your customer data is transferred outside of the Azure compliance boundary to the Grounding with Bing Search service. Grounding with Bing Search is not subject to the same data processing terms (including location of processing) and does not have the same compliance standards and certifications as the Azure AI Agent Service, as described in the [Grounding with Bing Search Terms of Use](https://www.microsoft.com/en-us/bing/apis/grounding-legal). It is your responsibility to assess whether use of Grounding with Bing Search in your agent meets your needs and requirements.

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Setup  

> [!NOTE]
> 1. Grounding with Bing Search only works with the following Azure OpenAI models: `gpt-3.5-turbo-0125`, `gpt-4-0125-preview`, `gpt-4-turbo-2024-04-09`, `gpt-4o-0513`

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create a Grounding with Bing Search resource. You need to have `owner` or `contributor` role in your subscription or resource group to create it.

   1. You can create one in the [Azure portal](https://portal.azure.com/#create/Microsoft.BingGroundingSearch), and select the different fields in the creation form. Make sure you create this Grounding with Bing Search resource in the same resource group as your Azure AI Agent, AI Project, and other resources.

    :::image type="content" source="../../media/tools/bing/resource-selection.png" alt-text="A screenshot of the Bing resource selection in the Azure portal." lightbox="../../media/tools/bing/resource-selection.png":::
  
   1. You can also create one through code-first experience. If so, you need to manually [register](/azure/azure-resource-manager/management/resource-providers-and-types#register-resource-provider) Bing Search as an Azure resource provider. You must have permission to perform the `/register/action` operation for the resource provider. The permission is included in the **Contributor** and **Owner** roles.

   ```console
       az provider register --namespace 'Microsoft.Bing'
   ```

1. After you have created a Grounding with Bing Search resource, you can find it in [Azure portal](https://portal.azure.com/#home). Navigate to the resource group you've created the resource in, search for the Grounding with Bing Search resource you have created.

    :::image type="content" source="../../media/tools/bing/resource-azure-portal.png" alt-text="A screenshot of the Bing resource in the Azure portal." lightbox="../../media/tools/bing/resource-azure-portal.png":::

1. You can add the Grounding with Bing Search tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal, in the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Grounding with Bing Search** and follow the prompts to add the tool. Note you can add only one per agent.

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.
   
   :::image type="content" source="../../media/tools/bing/choose-bing-connection.png" alt-text="A screenshot showing the button for creating a new connection." lightbox="../../media/tools/bing/choose-bing-connection.png":::

1. Select the Grounding with Bing Search resource you want to use and click to add connection. 

   :::image type="content" source="../../media/tools/bing/create-bing-connection.png" alt-text="A screenshot showing available Grounding with Bing Search connections." lightbox="../../media/tools/bing/create-bing-connection.png":::



## How to display Grounding with Bing Search results

According to Grounding with Bing's [terms of use and use and display requirements](https://www.microsoft.com/en-us/bing/apis/grounding-legal#use-and-display-requirements), you need to display both website URLs and Bing search query URLs in your custom interface. You can find website URLs through `annotations` parameter in API response and Bing search query URLs through `runstep` details. To render the webpage, we recommend you replace the endpoint of Bing search query URLs with `www.bing.com` and your Bing search query URL would look like "https://www.bing.com/search?q={search query}"

```python
run_steps = project_client.agents.list_run_steps(run_id=run.id, thread_id=thread.id)
run_steps_data = run_steps['data']
print(f"Last run step detail: {run_steps_data}")
```

:::image type="content" source="../../media/tools/bing/website-citations.png" alt-text="A screenshot showing citations for Bing search results." lightbox="../../media/tools/bing/website-citations.png":::

### Other legal considerations

Microsoft will use data you send to Grounding with Bing to improve Microsoft products and services. Where you send personal data to this service, you are responsible for obtaining sufficient consent from the data subjects. The Data Protection Terms in the Online Services Terms do not apply to Grounding with Bing. 

Your use of Grounding with Bing Search will be governed by the Terms of Use. By using Grounding with Bing Search, you agree to be bound by and comply with these Terms of Use.

::: zone-end

::: zone pivot="code-example"

## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

# [Python](#tab/python)

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

# [C#](#tab/csharp)

```csharp
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.TestFramework;
using NUnit.Framework;

var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;

var clientOptions = new AIProjectClientOptions();

// Adding the custom headers policy
clientOptions.AddPolicy(new CustomHeadersPolicy(), HttpPipelinePosition.PerCall);
var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential(), clientOptions);

```

# [JavaScript](#tab/javascript)

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

# [REST API](#tab/rest)
Follow the [REST API Quickstart](../quickstart-rest.md) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`.

---

## Step 2: Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

# [Python](#tab/python)

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

# [C#](#tab/csharp)

```csharp
GetConnectionResponse bingConnection = await projectClient.GetConnectionsClient().GetConnectionAsync(TestEnvironment.BINGCONNECTIONNAME);
var connectionId = bingConnection.Id;

AgentsClient agentClient = projectClient.GetAgentsClient();

ToolConnectionList connectionList = new ToolConnectionList
{
    ConnectionList = { new ToolConnection(connectionId) }
};
BingGroundingToolDefinition bingGroundingTool = new BingGroundingToolDefinition(connectionList);

Response<Agent> agentResponse = await agentClient.CreateAgentAsync(
    model: "gpt-4o",
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: new List<ToolDefinition> { bingGroundingTool });
Agent agent = agentResponse.Value;
```

# [JavaScript](#tab/javascript)

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

# [REST API](#tab/rest)
```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "instructions": "You are a helpful agent.",
        "name": "my-agent",
        "model": "gpt-4o",
        "tools": [
          {
            "type": "bing_grounding",
            "bing_grounding": {
                "connections": [
                    {
                        "connection_id": "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-bing-connection-name>"
                    }
                ]
            }
          }
        ]
      }'
```

---


## Step 3: Create a thread

# [Python](#tab/python)

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

# [C#](#tab/csharp)

```csharp
// Create thread for communication
Response<AgentThread> threadResponse = await agentClient.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

// Create message to thread
Response<ThreadMessage> messageResponse = await agentClient.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");
ThreadMessage message = messageResponse.Value;
```

# [JavaScript](#tab/javascript)

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

---

## Step 4: Create a run and check the output

Create a run and observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

# [Python](#tab/python)

```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
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

# [C#](#tab/csharp)

```csharp
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

# [JavaScript](#tab/javascript)

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

# [REST API](#tab/rest)
### Run the thread

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123 \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

### Retrieve the agent response

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

---

::: zone-end

## Next steps

[See the full sample for Grounding with Bing Search.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_bing_grounding.py)
