---
title: "How to use the data agents in Microsoft Fabric with Foundry Agent Service"
titleSuffix: Microsoft Foundry
description: Learn how to perform data analytics in Microsoft Foundry Agents using Microsoft Fabric data agent.
author: alvinashcraft
ms.author: aashcraft
manager: nitinme
ms.date: 12/16/2025
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.custom:
  - build-2025
zone_pivot_groups: selection-fabric-data-agent
---

# Use the Microsoft Fabric data agent (preview)

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Fabric data agent documentation](../../../default/agents/how-to/tools/fabric.md?view=foundry&preserve-view=true).

Integrate your Microsoft Foundry Agent with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational Q&A systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric data agent and then connect your Fabric data agent with the published endpoint. When a user sends a query, the will first determine if the Fabric data agent should be leveraged or not. If so, it will use the end user’s identity to generate queries over data they have access to. Lastly, the agent will generate responses based on queries returned from Fabric data agents. With Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

> [!NOTE] 
> The Fabric data agent only supports user identity authentication. Service Principal Name (SPN) authentication is not supported.

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ |  |  | ✔️ | ✔️ | ✔️ |

## Prerequisites
* You have created and published a Fabric data agent endpoint

* Developers and end users have at least `Azure AI User` RBAC role. 

* Developers and end users have at least `READ` access to the Fabric data agent and the underlying data sources it connects with.

* Your Fabric Data Agent and Foundry Agent need to be in the same tenant.


* Your Foundry Project endpoint.

    [!INCLUDE [endpoint-string-portal](../../includes/endpoint-string-portal.md)]

    Save this endpoint to an environment variable named `PROJECT_ENDPOINT`. 


* The name of your Microsoft Fabric connection name. You can find it in the Foundry portal by selecting **Management center** from the left navigation menu. Then selecting **Connected resources**.
    
    :::image type="content" source="../../media/tools/fabric-connection.png" alt-text="A screenshot showing the SharePoint connection name. " lightbox="../../media/tools/fabric-connection.png":::

    Save this endpoint to an environment variable named `FABRIC_CONNECTION_ID`


* The names of your model's deployment name. You can find it in **Models + Endpoints** in the left navigation menu. 

    :::image type="content" source="../../media/tools/model-deployment-portal.png" alt-text="A screenshot showing the model deployment screen the Foundry portal." lightbox="../../media/tools/model-deployment-portal.png":::
    
    Save the name of your model deployment name as an environment variable named `MODEL_DEPLOYMENT_NAME`. 

## Setup  

> [!NOTE]
> * The model you selected in Foundry Agent setup is only used for agent orchestration and response generation. It doesn't impact which model Fabric data agent uses for NL2SQL operation.
> * To help your model invoke your Microsoft Fabric tool in the expected way, make sure you update agent instructions with descriptions of your Fabric data agent and what data it can access. An example is "for customer and product sales related data, please use the Fabric tool". We recommend using a smaller AI model such as `gpt-4o-mini`. You can also use `tool_choice` parameter in SDK or API to force Fabric tool to be invoked at each run. 

1. Create a Foundry Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910)

    > [!NOTE]
    > * Make sure you have **published** the data agent in Fabric.

:::zone pivot="portal"

You can add the Microsoft Fabric tool to an agent programmatically using the code examples listed at the top of this article, or the Foundry portal. If you want to use the portal: 

1. Navigate to the **Agents** screen for your agent in [Foundry](https://ai.azure.com/?cid=learnDocs), scroll down the Setup pane on the right to **knowledge**. Then select **Add**.
   
    :::image type="content" source="../../media\tools\knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Foundry portal." lightbox="../../media\tools\knowledge-tools.png":::

1. Select **Microsoft Fabric** and follow the prompts to add the tool. You can add only one per agent.

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.

   1. To create a new connection, you need to find `workspace-id` and `artifact-id` in your published Fabric data agent endpoint. Your Fabric data agent endpoint would look like `https://<environment>.fabric.microsoft.com/groups/<workspace_id>/aiskills/<artifact-id>`

   1. Then, you can add both to your connection. Make sure you have checked `is secret` for both of them
   
        :::image type="content" source="../../media\tools\fabric-foundry.png" alt-text="A screenshot showing the fabric connection in the Foundry portal." lightbox="../../media\tools\fabric-foundry.png":::

:::zone-end

:::zone pivot="python"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FabricTool, ListSortOrder

# Retrieve the endpoint and credentials
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)
``` 

## Create an agent with the Microsoft Fabric tool enabled

To make the Microsoft Fabric tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Foundry portal.

```python
# The Fabric connection id can be found in the Foundry project as a property of the Fabric tool
# Your connection id is in the format /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-fabric-connection-name>

# Retrieve the Fabric connection ID from environment variables
conn_id = os.environ["FABRIC_CONNECTION_ID"]  # Ensure the FABRIC_CONNECTION_ID environment variable is set

# Initialize the FabricTool with the connection ID
fabric = FabricTool(connection_id=conn_id)

# Create an agent with the Fabric tool
# Create an Agent with the Fabric tool and process an Agent run
with project_client:
    agents_client = project_client.agents
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent",
        tools=fabric.definitions,
    )
    print(f"Created Agent, ID: {agent.id}")
```

## Create a thread

```python
# Create a thread for communication
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Create a message in the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",  # Role of the message sender
    content="What insights can you provide from the Fabric resource?",  # Message content
)
print(f"Created message, ID: {message['id']}")
```

## Create a run and check the output

```python
# Create and process an Agent run in thread with tools
run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Uncomment the following lines to delete the agent when done
#agents_client.delete_agent(agent.id)
#print("Deleted agent")

# Fetch and log all messages
messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for msg in messages:
    if msg.text_messages:
        last_text = msg.text_messages[-1]
        print(f"{msg.role}: {last_text.text.value}")
```

:::zone-end


<!--
:::zone pivot="csharp"

## Create a project client

Create a client object, which will contain the project endpoint connecting to your AI project and other resources.

```csharp
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using System;
using Microsoft.Extensions.Configuration;
using System.Threading;
using Azure;

// Get Connection information from App Configuration
IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];
var fabricConnectionId = configuration["FabricConnectionId"];

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Create an agent with the Microsoft Fabric tool enabled

To make the Microsoft Fabric tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Foundry portal.

```csharp
// Create the MicrosoftFabricToolDefinition object needed when creating the agent
ToolConnectionList connectionList = new()
{
    ConnectionList = { new ToolConnection(fabricConnectionId) }
};
MicrosoftFabricToolDefinition fabricTool = new(connectionList);

// Create the Agent
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: [fabricTool]);
```

## Create a thread and run

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
ThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "What are the top 3 weather events with highest property damage?");
ThreadRun run = agentClient.Runs.CreateRun(thread, agent);
```

## Wait for the agent to complete and print the output

Wait for the agent to complete the run and print output to console. Observe that the model uses the Fabric data agent tool to provide a response to the user's question.

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
```

## Clean up resources

Clean up the resources from this sample.

```csharp

// Delete thread and agent
agentClient.Threads.DeleteThread(threadId: thread.Id);
agentClient.Administration.DeleteAgent(agentId: agent.Id);

```
:::zone-end

:::zone pivot="javascript"

## Create a project client

```javascript
const { AgentsClient, ToolUtility, isOutputOfType } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");
require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"] || "<project connection string>";

// Create an Azure AI Client
  const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```

## Create an agent with the Microsoft Fabric tool enabled

```javascript
const connectionId = process.env["FABRIC_CONNECTION_ID"] || "<connection-name>";
// Initialize agent Microsoft Fabric tool with the connection id
const fabricTool = ToolUtility.createFabricTool(connectionId);

// Create agent with the Microsoft Fabric tool and process assistant run
const agent = await client.createAgent(modelDeploymentName, {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [fabricTool.definition],
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
  "What are the top 3 weather events with the highest property damage?",
);
console.log(`Created message, message ID: ${message.id}`);
```

## Create a run and check the output

```javascript
// Create and process agent run in thread with tools
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
  console.log(`Run failed: ${run.lastError}`);
}
console.log(`Run finished with status: ${run.status}`);
console.log(`Failure: ${run.lastError?.message}`);

// Delete the agent when done
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);

// Fetch and log all messages
const messagesIterator = client.messages.list(thread.id);
console.log(`Messages:`);

// Get the first message
for await (const m of messagesIterator) {
  const agentMessage = message.content[0];
  if (isOutputOfType(agentMessage, "text")) {
    const textContent = agentMessage;
    console.log(`Text Message Content - ${textContent.text.value}`);
  }
  break; // Only process the first message
}
```
:::zone-end
-->
:::zone pivot="rest"

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`. For `API_VERSION`, make sure you are using `2025-05-15-preview`.
> [!IMPORTANT]
> The following samples are applicable if you are using **Foundry Project** resource with Microsoft Fabric tool through REST API call
> Your connection ID should be in this format: `/subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-fabric-connection-name>`

### Create an agent with the Microsoft Fabric tool enabled

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
            "type": "fabric_dataagent",
            "fabric_dataagent": {
                "connections": [
                    {
                        "connection_id": "/subscriptions/<sub-id>/resourceGroups/<your-rg-name>/providers/Microsoft.CognitiveServices/accounts/<your-ai-services-name>/projects/<your-project-name>/connections/<your-fabric-connection-name>"
                    }
                ]
            }
          }
        ]
      }'
```

### Create a thread

#### Create a thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

#### Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "<question related to your data>"
    }'
```

### Create a run and check the output

#### Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

#### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

#### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```
:::zone-end

## Next steps

[See the full sample for Fabric data agent.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-agents/samples/agents_tools/sample_agents_fabric.py)
