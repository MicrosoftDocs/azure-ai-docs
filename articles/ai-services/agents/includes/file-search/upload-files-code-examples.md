## Quickstart – Upload Local Files with file search 

In this example, we’ll use Azure AI Agent Service to create an agent that can help answer questions on information you upload from local files.  

##  Prerequisites 
Complete the [agent setup](../../quickstart.md).

## Step 1: Create a project client

Create a client object, which will contain the connection string for connecting to your AI project and other resources. 

# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool
from azure.identity import DefaultAzureCredential


# Create an Azure AI Client from a connection string, copied from your AI Studio project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables

credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    credential=credential, conn_str=os.environ["PROJECT_CONNECTION_STRING"] 
)
```

# [C#](#tab/csharp)

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Azure.Core.TestFramework;
using NUnit.Framework;

// Create an Azure AI Client from a connection string, copied from your AI Studio project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredentia());
```

---

## Step 2: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the `in_progress` state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling.

Vector stores are created using message attachments that have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run). This default exists to help you manage your vector storage costs. You can override these expiration policies at any time.

# [Python](#tab/python)

```python
# We will upload the local file and will use it for vector store creation.

#upload a file
file = project_client.agents.upload_file_and_poll(file_path='./data/product_info_1.md', purpose="assistants")
print(f"Uploaded file, file ID: {file.id}")

_, asset_uri = project_client.upload_file("./data/product_info_1.md")
print(f"Uploaded file, asset URI: {asset_uri}")

# create a vector store with the file you uploaded
vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
print(f"Created vector store, vector store ID: {vector_store.id}")
```

# [C#](#tab/csharp)

```csharp
// Upload a file and wait for it to be processed
File.WriteAllText(
    path: "sample_file_for_upload.txt",
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
Response<AgentFile> uploadAgentFileResponse = await client.UploadFileAsync(
    filePath: "sample_file_for_upload.txt",
    purpose: AgentFilePurpose.Agents);

AgentFile uploadedAgentFile = uploadAgentFileResponse.Value;

// Create a vector store with the file and wait for it to be processed.
// If you do not specify a vector store, create_message will create a vector store with a default expiration policy of seven days after they were last active
VectorStore vectorStore = await client.CreateVectorStoreAsync(
    fileIds:  new List<string> { uploadedAgentFile.Id },
    name: "my_vector_store");
```
---

## Step 3: Enable file search

To make the files accessible to your agent, create a `FileSearchTool` object with the `vector_store` ID, and attach `tools` and `tool_resources` to the agent.

# [Python](#tab/python)

```python

# create a file search tool
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

# notices that FileSearchTool as tool and tool_resources must be added or the agent will be unable to search the file
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful agent",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

# [C#](#tab/csharp)

```csharp
FileSearchToolResource fileSearchToolResource = new FileSearchToolResource();
fileSearchToolResource.VectorStoreIds.Add(vectorStore.Id);

// Create an agent with toolResources and process assistant run
Response<Agent> agentResponse = await client.CreateAgentAsync(
        model: "gpt-4o-mini",
        name: "SDK Test Agent - Retrieval",
        instructions: "You are a helpful agent that can help fetch data from files you know about.",
        tools: new List<ToolDefinition> { new FileSearchToolDefinition() },
        toolResources: new ToolResources() { FileSearch = fileSearchToolResource });
Agent agent = agentResponse.Value;
```

---

## Step 4: Create a thread

# [Python](#tab/python)

```python
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?"
)
print(f"Created message, message ID: {message.id}")
```

# [C#](#tab/csharp)

```csharp
// Create thread for communication
Response<AgentThread> threadResponse = await client.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

// Create message to thread
Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "Can you give me the documented codes for 'banana' and 'orange'?");
ThreadMessage message = messageResponse.Value;
```
---

## Step 5: Create a run and check the output
Create a run and observe that the model uses the file search tool to provide a response to the user's question.
# [Python](#tab/python)
```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, assistant_id=agent.id)
print(f"Created run, run ID: {run.id}")

project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")
```

# [C#](#tab/csharp)

```csharp
// Run the agent
Response<ThreadRun> runResponse = await client.CreateRunAsync(thread, agent);

do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
}
while (runResponse.Value.Status == RunStatus.Queued
    || runResponse.Value.Status == RunStatus.InProgress);

Response<PageableList<ThreadMessage>> afterRunMessagesResponse
    = await client.GetMessagesAsync(thread.Id);
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