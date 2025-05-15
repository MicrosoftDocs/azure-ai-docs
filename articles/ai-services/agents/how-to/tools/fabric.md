---
title: 'How to use the data agents in Microsoft Fabric with Azure AI Foundry Agent Service'
titleSuffix: Azure AI Foundry
description: Learn how to perform data analytics in Azure AI Agents using Microsoft Fabric data agent.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/07/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-fabric-data-agent
---

# Use the Microsoft Fabric data agent (preview)

Integrate your Azure AI Agent with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational Q&A systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric data agent and then connect your Fabric data agent with the published endpoint. When a user sends a query, Azure AI Agent will first determine if the Fabric data agent should be leveraged or not. If so, it will use the end user’s identity to generate queries over data they have access to. Lastly, Azure AI Agent will generate responses based on queries returned from Fabric data agents. With Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites
* You have created and published a Fabric data agent endpoint

* Developers and end users have at least `Azure AI User` RBAC role. 

* Developers and end users have at least `READ` access to the Fabric data agent and the underlying data sources it connects with.

* Your Fabric Data Agent and Azure AI Agent need to be in the same tenant.

## Setup  
> [!NOTE]
> * The model you selected in Azure AI Agent setup is only used for agent orchestration and response generation. It doesn't impact which model Fabric data agent uses for NL2SQL operation.

1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910)

:::zone pivot="portal"

You can add the Microsoft Fabric tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal: 

1. Navigate to the **Agents** screen for your agent in [Azure AI Foundry](https://ai.azure.com/), scroll down the Setup pane on the right to **knowledge**. Then select **Add**.
   
    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Microsoft Fabric** and follow the prompts to add the tool. You can add only one per agent.

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.

   1. To create a new connection, you need to find `workspace-id` and `artifact-id` in your published Fabric data agent endpoint. Your Fabric data agent endpoint would look like `https://<environment>.fabric.microsoft.com/groups/<workspace_id>/aiskills/<artifact-id>`

   1. Then, you can add both to your connection. Make sure you have checked `is secret` for both of them
   
        :::image type="content" source="../../media/tools/fabric-foundry.png" alt-text="A screenshot showing the fabric connection in the Azure AI Foundry portal." lightbox="../../media/tools/fabric-foundry.png":::

:::zone-end

:::zone pivot="python"

## Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import FabricTool

# Retrieve the endpoint and credentials
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)
``` 

## Create an agent with the Microsoft Fabric tool enabled

To make the Microsoft Fabric tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

```python
# The Fabric connection id can be found in the Azure AI Foundry project as a property of the Fabric tool
# Your connection id is in the format /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-fabric-connection-name>

# Retrieve the Fabric connection ID from environment variables
conn_id = os.environ["FABRIC_CONNECTION_ID"]  # Ensure the FABRIC_CONNECTION_ID environment variable is set

# Initialize the FabricTool with the connection ID
fabric = FabricTool(connection_id=conn_id)

# Create an agent with the Fabric tool
with project_client:
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="my-agent",  # Name of the agent
        instructions="You are a helpful agent",  # Instructions for the agent
        tools=fabric.definitions,  # Attach the Fabric tool
        headers={"x-ms-enable-preview": "true"},  # Enable preview features
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
# Create and process an agent run in the thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

# Check if the run failed
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Fetch and log all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages.data:
    print(f"Role: {message.role}, Content: {message.content}")

# Delete the agent after use
project_client.agents.delete_agent(agent.id)
print("Deleted agent")
```

:::zone-end

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

To make the Microsoft Fabric tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

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

## Create an agent with the Microsoft Fabric tool enabled

```javascript
const fabricConnection = await client.connections.getConnection("FABRICCONNECTIONNAME");

const connectionId = fabricConnection.id;

// Initialize agent Microsoft Fabric tool with the connection id
const fabricTool = ToolUtility.createFabricTool(connectionId);

// Create agent with the Microsoft Fabric tool and process assistant run
const agent = await client.agents.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [fabricTool.definition],
  toolResources: {}, // Add empty tool_resources which is required by the API
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
    content: "<Ask a question related to your Fabric data>",
});
```

## Create a run and check the output

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

:::zone pivot="rest"

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

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
                        "connection_id": "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-fabric-connection-name>"
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

[See the full sample for Fabric data agent.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_fabric.py)
