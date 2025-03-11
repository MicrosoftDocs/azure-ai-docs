---
manager: nitinme
author: fosteramanda
ms.author: fosteramanda
ms.service: azure-ai-agent-service
ms.topic: include
ms.date: 12/10/2024
---

## Quickstart – Upload Local Files with file search 

In this example, we use Azure AI Agent Service to create an agent that can help answer questions on information you upload from local files.  

##  Prerequisites 
1. Complete the [agent setup](../../quickstart.md).

2. Ensure that you have the role  **Storage Blob Data Contributor** on your project's storage account.

3. Ensure that you have the role **Azure AI Developer** on your project.

## Step 1: Create a project client

Create a client object that contains the connection string for connecting to your AI project and other resources.
# [Python](#tab/python)

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, MessageAttachment, FilePurpose
from azure.identity import DefaultAzureCredential


# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
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

// Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
// Customer needs to login to Azure subscription via Azure CLI and set the environment variables
var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());
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
Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AZURE_AI_AGENTS_TOKEN` and `AZURE_AI_AGENTS_ENDPOINT`.

---

## Step 2: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are out of the `in_progress` state to ensure that all content is fully processing. The SDK provides helpers for uploading and polling.
# [Python](#tab/python)

```python
# We will upload the local file and will use it for vector store creation.

#upload a file
file = project_client.agents.upload_file_and_poll(file_path='./data/product_catelog.md', purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

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

# [JavaScript](#tab/javascript)

```javascript
const localFileStream = fs.createReadStream("sample_file_for_upload.txt");
const file = await client.agents.uploadFile(localFileStream, "assistants", {
  fileName: "sample_file_for_upload.txt",
});
console.log(`Uploaded file, ID: ${file.id}`);

const vectorStore = await client.agents.createVectorStore({
  fileIds: [file.id],
  name: "my_vector_store",
});
console.log(`Created vector store, ID: ${vectorStore.id}`);
```

# [REST API](#tab/rest)
### Upload a file
```console
curl $AZURE_AI_AGENTS_ENDPOINT/files?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store
```console
curl $AZURE_AI_AGENTS_ENDPOINT/vector_stores?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store"
  }'

```

### Attach the uploaded file to the vector store
```console
curl $AZURE_AI_AGENTS_ENDPOINT/vector_stores/vs_abc123/files?api-version=2024-12-01-preview \
    -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "file_id": "assistant-abc123"
    }'
```

---

## Step 3: Create an agent and enable file search

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

# [JavaScript](#tab/javascript)

```javascript
const fileSearchTool = ToolUtility.createFileSearchTool([vectorStore.id]);

const agent = await client.agents.createAgent("gpt-4o-mini", {
  name: "SDK Test Agent - Retrieval",
  instructions: "You are helpful agent that can help fetch data from files you know about.",
  tools: [fileSearchTool.definition],
  toolResources: fileSearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

# [REST API](#tab/rest)
```console
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "api-key: $AZURE_OPENAI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Financial Analyst Assistant",
    "instructions": "You are an expert financial analyst. Use your knowledge base to answer questions about audited financial statements.",
    "tools": [{"type": "file_search"}],
    "model": "gpt-4o-mini",
    "tool_resources": {"file_search": {"vector_store_ids": ["vs_1234abcd"]}}
  }'
```

---

## Step 4: Create a thread
You can also attach files as Message attachments on your thread. Doing so creates another ```vector_store``` associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store.  When you create a Run on this thread, the file search tool queries both the ```vector_store``` from your agent and the ```vector_store``` on the thread.
# [Python](#tab/python)

```python
# Create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

# Upload the user provided file as a messsage attachment
message_file = project_client.agents.upload_file_and_poll(file_path='product_info_1.md', purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {message_file.id}")

# Create a message with the file search attachment
# Notice that vector store is created temporarily when using attachments with a default expiration policy of seven days.
attachment = MessageAttachment(file_id=message_file.id, tools=FileSearchTool().definitions)
message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?", attachments=[attachment]
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

# [JavaScript](#tab/javascript)

```javascript
// Create thread with file resources.
// If the agent has multiple threads, only this thread can search this file.
const thread = await client.agents.createThread({ toolResources: fileSearchTool.resources });

// add a message to thread
await client.agents.createMessage(
    thread.id, {
    role: "user",
    content: "Can you give me the documented codes for 'banana' and 'orange'?",
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
      "content": "Which months do we have covered in the financial statements?"
    }'
```

---

## Step 5: Create a run and check the output
Create a run and observe that the model uses the file search tool to provide a response to the user's question.
# [Python](#tab/python)
```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
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