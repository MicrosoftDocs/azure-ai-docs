---
title: 'How to use Grounding with Bing Search in Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to ground Azure AI Agents using Bing Search results.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 12/11/2024
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
> 1. Your usage of Grounding with Bing Search may incur costs. See the [pricing page](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> 1. By creating and using a Grounding with Bing Search resource through code-first experience, such as Azure CLI, or deploying through deployment template, you agree to be bound by and comply with the terms available at https://www.microsoft.com/en-us/bing/apis/grounding-legal, which may be updated from time to time.


## Setup  

> [!NOTE]
> 1. Grounding with Bing Search only works with the following Azure OpenAI models: `gpt-3.5-turbo-0125`, `gpt-4-0125-preview`, `gpt-4-turbo-2024-04-09`, `gpt-4o-0513`

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Register the Bing Search provider.

   ```console
       az provider register --namespace 'Microsoft.Bing'
   ```

1. Create a new Grounding with Bing Search resource in the [Azure portal](https://portal.azure.com/#create/Microsoft.BingGroundingSearch), and select the different fields in the creation form. Make sure you create this Grounding with Bing Search resource in the same resource group as your Azure AI Agent, AI Project, and other resources.

1. After you have created a Grounding with Bing Search resource, you can find it in [Azure portal](https://portal.azure.com/#home). Navigate to the resource group you've created the resource in, search for the Grounding with Bing Search resource you have created.

    :::image type="content" source="../../media/tools/bing/resource-azure-portal.png" alt-text="A screenshot of the Bing resource in the Azure portal." lightbox="../../media/tools/bing/resource-azure-portal.png":::

1. Select the Grounding with Bing Search resource you have created and copy any of the API keys.

    :::image type="content" source="../../media/tools/bing/key-resource-azure-portal.png" alt-text="A screenshot of the key and endpoint screen for the Bing resource in the Azure portal." lightbox="../../media/tools/bing/key-resource-azure-portal.png":::

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/) and select the AI Project (make sure it's in the same resource group of your Grounding with Bing Search resource). Click **management center**.

    :::image type="content" source="../../media/tools/bing/project-settings-button.png" alt-text="A screenshot of the settings button for an AI project." lightbox="../../media/tools/bing/project-settings-button.png":::

1. Select **+ new connection** in the settings page. 

    >[!NOTE]
    > If you re-generate the API key at a later date, you need to update the connection with the new key.

    :::image type="content" source="../../media/tools/bing/project-connections.png" alt-text="A screenshot of the connections screen for the AI project." lightbox="../../media/tools/bing/project-connections.png":::


1. Select **API key** in **other resource types**.

    :::image type="content" source="../../media/tools/bing/api-key-connection.png" alt-text="A screenshot of the resource types available for connections." lightbox="../../media/tools/bing/api-key-connection.png":::

1. Enter the following information and then create a new connection to your Grounding with Bing Search resource.

    - Endpoint: `https://api.bing.microsoft.com/`
    - Key: `YOUR_API_KEY`
    - Connection name: `YOUR_CONNECTION_NAME` (You will use this connection name in the sample code below.)
    - Access: you can choose either *this project only* or *shared to all projects*. Just make sure in the sample code below, the project you entered connection string for has access to this connection.

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

## Step 1: Create an agent with Grounding with Bing Search

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

---

## Step 2: Enable the Grounding with Bing search tool

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
---

::: zone-end

## Next steps

[See the full sample for Grounding with Bing Search.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_bing_grounding.py)
