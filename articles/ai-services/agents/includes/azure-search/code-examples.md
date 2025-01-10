---
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 12/10/2024
---
## Quickstart – Use an existing Azure AI Search index with the Azure AI Search tool

This quickstart shows how to use an existing Azure AI Search index with the Azure AI Search tool.

### Prerequisites
Complete the [Azure AI Search tool setup](../../how-to/tools/azure-ai-search.md?pivot=overview-azure-ai-search).

### Step 1: Create an Azure AI Client
First, create an Azure AI Client using the connection string of your project.
# [Python](#tab/python)
```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import AzureAISearchTool

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# HostName can be found by navigating to your discovery_url and removing the leading "https://" and trailing "/discovery" 
# To find your discovery_url, run the CLI command: az ml workspace show -n {project_name} --resource-group {resource_group_name} --query discovery_url
# Project Connection example: eastus.api.azureml.ms;my-subscription-id;my-resource-group;my-hub-name

connection_string = os.environ["PROJECT_CONNECTION_STRING"] 

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str=connection_string,
)
```

# [C#](#tab/csharp)
```csharp
using System;
using System.Threading.Tasks;
using Azure.Core;
using Azure.Core.TestFramework;
using NUnit.Framework;
using System.Collections.Generic;

// Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
var clientOptions = new AIProjectClientOptions();

// Adding the custom headers policy
clientOptions.AddPolicy(new CustomHeadersPolicy(), HttpPipelinePosition.PerCall);
var projectClient = new AIProjectClient(connectionString, new DefaultAzureCredential(), clientOptions);
```
---
### Step 2: Get the connection ID for the Azure AI Search resource

Get the connection ID of the Azure AI Search connection in the project. You can use the code snippet to print the connection ID of all the Azure AI Search connections in the project. 

# [Python](#tab/python)

```python
# AI Search resource connection ID
# This code prints out the connection ID of all the Azure AI Search connections in the project
# If you have more than one AI search connection, make sure to select the correct one that contains the index you want to use.
conn_list = project_client.connections.list()
conn_id = ""
for conn in conn_list:
    if conn.connection_type == "CognitiveSearch":
        print(f"Connection ID: {conn.id}")
```
# [C#](#tab/csharp)
```csharp
ListConnectionsResponse connections = await projectClient.GetConnectionsClient().GetConnectionsAsync(ConnectionType.AzureAISearch).ConfigureAwait(false);

        if (connections?.Value == null || connections.Value.Count == 0)
        {
            throw new InvalidOperationException("No connections found for the Azure AI Search.");
        }

```
---
The second way to get the connection ID is to navigate to the project in the Azure AI Foundry and click on the **Connected resources** tab and then select your Azure AI Search resource.
:::image type="content" source="../../media/tools/ai-search/success-connection.png" alt-text="A screenshot of an AI Search resource connection page in Azure AI Foundry." lightbox="../../media/tools/ai-search/success-connection.png":::
In the URL, you see the wsid=/subscription/your-subscription-id..., this is the connection ID you need to use. Copy everything that comes after wsid=.
:::image type="content" source="../../media/tools/ai-search/connection-id.png" alt-text="A screenshot of an AI Search resource connection and how to copy the connection ID." lightbox="../../media/tools/ai-search/connection-id.png":::

### Step 3: Configure the Azure AI Search tool
Using the connection ID you got in the previous step, you can now configure the Azure AI Search tool to use your Azure AI Search index.
# [Python](#tab/python)
```python
# TO DO: replace this value with the connection ID of the search index
conn_id =  "/subscriptions/<your-subscription-id>/resourceGroups/<your-resource-group>/providers/Microsoft.MachineLearningServices/workspaces/<your-project-name>/connections/<your-azure-ai-search-connection-name>"

# Initialize agent AI search tool and add the search index connection ID and index name
# TO DO: replace <your-index-name> with the name of the index you want to use
ai_search = AzureAISearchTool()
ai_search.add_index(conn_id, "<your-index-name>")
```
# [C#](#tab/csharp)
```csharp
// TO DO: replace this value with the connection ID of the search index
ConnectionResponse connection = connections.Value[0];

// Initialize agent Azure AI search tool and add the search index connection ID and index name
// TO DO: replace <your-index-name> with the name of the index you want to use
ToolResources searchResource = new ToolResources
{
    AzureAISearch = new AzureAISearchResource
    {
        IndexList = { new IndexResource(connection.Id, "<your-index-name>") }
    }
};
```
---

### Step 4: Create an agent with the Azure AI Search tool enabled
Change the model to the one deployed in your project. You can find the model name in the Azure AI Foundry under the **Models** tab. You can also change the name and instructions of the agent to suit your needs.
# [Python](#tab/python)
```python
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-assistant",
    instructions="You are a helpful assistant",
    tools=ai_search.definitions,
    tool_resources = ai_search.resources,
)
print(f"Created agent, ID: {agent.id}")
```
# [C#](#tab/csharp)
```csharp
AgentsClient agentClient = projectClient.GetAgentsClient();

Response<Agent> agentResponse = await agentClient.CreateAgentAsync(
    model: "gpt-4o-mini",
    name: "my-assistant",
    instructions: "You are a helpful assistant.",
    tools: new List<ToolDefinition> { new AzureAISearchToolDefinition() },
    toolResources: searchResource);
Agent agent = agentResponse.Value;
```
---

### Step 5: Ask the agent questions about data in the index
Now that the agent is created, ask it questions about the data in your Azure AI Search index. The example assumes your Azure AI Search index contains information about health care plans.
# [Python](#tab/python)
```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")
 
# Create a message
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="what are my health insurance plan coverage types?",
)
print(f"Created message, message ID: {message.id}")
    
# Run the agent
run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
print(f"Run finished with status: {run.status}")
 
if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# Get messages from the thread 
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
    
assistant_message = ""
for message in messages.data:
    if message["role"] == "assistant":
        assistant_message = message["content"][0]["text"]["value"]

# Get the last message from the sender
print(f"Assistant response: {assistant_message}")
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
    "Hello, send an email with the datetime and weather information in New York?");
ThreadMessage message = messageResponse.Value;

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