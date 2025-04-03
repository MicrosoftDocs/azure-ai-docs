---
title: 'How to use the data agents in Microsoft Fabric with Azure AI Agent Service'
titleSuffix: Azure OpenAI
description: Learn how to perform data analytics in Azure AI Agents using Microsoft Fabric data agent.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 02/25/2025
author: aahill
ms.author: aahi
zone_pivot_groups: selection-fabric-data-agent
ms.custom: azure-ai-agents, references_regions
---

# Use the Microsoft Fabric data agent

::: zone pivot="overview"

Integrate your Azure AI Agent with the [**Microsoft Fabric data agent**](https://go.microsoft.com/fwlink/?linkid=2312815) to unlock powerful data analysis capabilities. The Fabric data agent transforms enterprise data into conversational Q&A systems, allowing users to interact with the data through chat and uncover data-driven and actionable insights. 

You need to first build and publish a Fabric data agent and then connect your Fabric data agent with the published endpoint. When a user sends a query, Azure AI Agent will first determine if the Fabric data agent should be leveraged or not. If so, it will use the end user’s identity to generate queries over data they have access to. Lastly, Azure AI Agent will generate responses based on queries returned from Fabric data agents. With Identity Passthrough (On-Behalf-Of) authorization, this integration simplifies access to enterprise data in Fabric while maintaining robust security, ensuring proper access control and enterprise-grade protection. 

## Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API |Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites
* You have created and published a Fabric data agent endpoint

* Developers and end users have at least `AI Developer` RBAC role. 

* Developers and end users have at least `READ` access to the Fabric data agent and the underlying data sources it connects with.

## Setup  
> [!NOTE]
> * The model you selected in Azure AI Agent setup is only used for agent orchestration and response generation. It doesn't impact which model Fabric data agent uses for NL2SQL operation.
> *  Supported regions: `westus`, `japaneast`.
1. Create an Azure AI Agent by following the steps in the [quickstart](../../quickstart.md).

1. Create and publish a [Fabric data agent](https://go.microsoft.com/fwlink/?linkid=2312910)

1. You can add the Microsoft Fabric tool to an agent programatically using the code examples listed at the top of this article, or the Azure AI Foundry portal. If you want to use the portal, in the Create and debug screen for your agent, scroll down the Setup pane on the right to knowledge. Then select Add.
   :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Microsoft Fabric** and follow the prompts to add the tool. You can add only one per agent.

1. Click to add new connections. Once you have added a connection, you can directly select from existing list.
   1. To create a new connection, you need to find `workspace-id` and `artifact-id` in your published Fabric data agent endpoint. Your Fabric data agent endpoint would look like `https://<environment>.fabric.microsoft.com/groups/<workspace_id>/aiskills/<artifact-id>`

   1. Then, you can add both to your connection. Make sure you have checked `is secret` for both of them
   
        :::image type="content" source="../../media/tools/fabric-foundry.png" alt-text="A screenshot showing the fabric connection in the Azure AI Foundry portal." lightbox="../../media/tools/fabric-foundry.png":::

::: zone-end

::: zone pivot="code-example"
## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources.

# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import FabricTool
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

>[!IMPORTANT]
> This REST API allows developers to invoke the Grounding with Bing Search tool through the Azure AI Agent service. It does not send calls to the Grounding with Bing Search API directly. 

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`. The client creation is demonstrated in the next section.

---

## Step 2: Create an agent with the Microsoft Fabric tool enabled

To make the Microsoft Fabric tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the Azure AI Foundry portal.

# [Python](#tab/python)

```python
# The Fabric connection id can be found in the Azure AI Foundry project as a property of the Fabric tool
# Your connection id is in the format /subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-fabric-connection-name>
conn_id = "your-connection-id"

# Initialize agent fabric tool and add the connection id
fabric = FabricTool(connection_id=conn_id)

# Create agent with the fabric tool and process agent run
with project_client:
    agent = project_client.agents.create_agent(
        model="gpt-4o",
        name="my-assistant",
        instructions="You are a helpful assistant",
        tools=fabric.definitions,
        headers={"x-ms-enable-preview": "true"},
    )
    print(f"Created agent, ID: {agent.id}")
```
# [JavaScript](#tab/javascript)

```javascript
const fabricConnection = await client.connections.getConnection("FABRICCONNECTIONNAME"
);

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
---

## Step 3: Create a thread

# [Python](#tab/python)

```python
# Create thread for communication
thread = project_client.agents.create_thread()
print(f"Created thread, ID: {thread.id}")

# Create message to thread
# Remember to update the message with your data
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="what is top sold product in Contoso last month?",
)
print(f"Created message, ID: {message.id}")
```
# [JavaScript](#tab/javascript)

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
      "content": "<question related to your data>"
    }'
```

---

## Step 4: Create a run and check the output

Create a run and observe that the model uses the Fabric data agent tool to provide a response to the user's question.

# [Python](#tab/python)

```python
# Create and process agent run in thread with tools
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Delete the assistant when done
project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
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
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

### Retrieve the agent response

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

---

::: zone-end

## Next steps

[See the full sample for Fabric data agent.](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/sample_agents_fabric.py)
