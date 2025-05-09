---
title: 'How to upload files using the file search tool'
titleSuffix: Azure AI Foundry
description: Find code samples and instructions for uploading files to Azure AI Foundry Agent Service.
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

# How to upload files using the file search tool

Use this article to find step-by-step instructions and code samples for uploading files using the file search tool.

## Prerequisites 
1. Complete the [agent setup](../../quickstart.md).

2. Ensure that you have the role **Storage Blob Data Contributor** on your project's storage account.

3. Ensure that you have the role **Azure AI Developer** on your project.


::: zone pivot="portal"

## Add file search to an agent using the Azure AI Foundry portal

1. Go to the [Azure AI Foundry portal](https://ai.azure.com/). In the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Files** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

    :::image type="content" source="../../media/tools/file-upload.png" alt-text="A screenshot showing the file upload page." lightbox="../../media/tools/file-upload.png":::

::: zone-end

:::zone pivot="python"

## Step 1: Create a project client

Create a client object that contains the connection string for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Define the project endpoint
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False),  # Use Azure Default Credential for authentication
    api_version="latest",
)
```

## Step 2: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store.

```python
from azure.ai.agents.models import FilePurpose

# Define the path to the file to be uploaded
file_path = "./data/product_info_1.md"

# Upload the file
file = project_client.agents.upload_file_and_poll(file_path=file_path, purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

# Create a vector store with the uploaded file
vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
print(f"Created vector store, vector store ID: {vector_store.id}")
```

## Step 3: Create an agent and enable file search

To make the files accessible to your agent, create a `FileSearchTool` object with the `vector_store` ID, and attach tools and `tool_resources` to the agent.

```python
from azure.ai.agents.models import FileSearchTool

# Create a file search tool
file_search = FileSearchTool(vector_store_ids=[vector_store.id])

# Create an agent with the file search tool
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
    name="my-agent",  # Name of the agent
    instructions="You are a helpful agent and can search information from uploaded files",  # Instructions for the agent
    tools=file_search.definitions,  # Tools available to the agent
    tool_resources=file_search.resources,  # Resources for the tools
)
print(f"Created agent, ID: {agent.id}")
```

## Step 4: Create a thread

You can also attach files as message attachments on your thread. Doing so creates another `vector_store` associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store.

```python
# Create a thread
thread = project_client.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

# Send a message to the thread
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role="user",
    content="Hello, what Contoso products do you know?",  # Message content
)
print(f"Created message, ID: {message['id']}")
```

## Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```python
# Create and process an agent run in the thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Cleanup resources
project_client.agents.delete_vector_store(vector_store.id)
print("Deleted vector store")

project_client.agents.delete_file(file_id=file.id)
print("Deleted file")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
for message in messages.data:
    print(f"Role: {message.role}, Content: {message.content}")
```
:::zone-end

:::zone pivot="csharp"

## Step 1: Create a project client

Create a client object that contains the connection string for connecting to your AI project and other resources.

```csharp
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Azure.Core.TestFramework;

// Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
// At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<ProjectName>"
// You need to login to your Azure subscription via the Azure CLI and set the environment variables
var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());
```

## Step 2: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are uploaded to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

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
    fileIds: new List<string> { uploadedAgentFile.Id },
    name: "my_vector_store");
```

## Step 3: Create an agent and enable file search

Create a file search tool object with the vector store ID, and attach tool and tool resources to the agent.

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

## Step 4: Create a thread

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```csharp
Response<AgentThread> threadResponse = await client.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "Can you give me the documented codes for 'banana' and 'orange'?");
ThreadMessage message = messageResponse.Value;
```

## Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```csharp
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

foreach (ThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");
    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            Console.Write(textItem.Text);
        }
        Console.WriteLine();
    }
}
```

:::zone-end

:::zone pivot="javascript"

## Step 1: Create a project client

Create a client object that contains the connection string for connecting to your AI project and other resources.

```javascript
const connectionString =
  process.env["AZURE_AI_PROJECTS_CONNECTION_STRING"] || "<project connection string>";

const client = AIProjectsClient.fromConnectionString(
    connectionString || "",
    new DefaultAzureCredential(),
);
```

## Step 2: Upload files and add them to a Vector Store

Upload your files and create a vector store.

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

## Step 3: Create an agent and enable file search

Create a `FileSearchTool` object with the vector store ID, and attach `tools` and `toolResources` to the agent.

```javascript
const fileSearchTool = ToolUtility.createFileSearchTool([vectorStore.id]);

const agent = await client.agents.createAgent("gpt-4o-mini", {
  name: "SDK Test Agent - Retrieval",
  instructions: "You are a helpful agent that can help fetch data from files you know about.",
  tools: [fileSearchTool.definition],
  toolResources: fileSearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Step 4: Create a thread

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```javascript
const thread = await client.agents.createThread({ toolResources: fileSearchTool.resources });

await client.agents.createMessage(
    thread.id, {
    role: "user",
    content: "Can you give me the documented codes for 'banana' and 'orange'?",
});
```

## Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```javascript
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
  }
}

const messages = await client.agents.listMessages(thread.id);

for (let i = messages.data.length - 1; i >= 0; i--) {
  const m = messages.data[i];
  if (isOutputOfType<MessageTextContentOutput>(m.content[0], "text")) {
    const textContent = m.content[0];
    console.log(`${textContent.text.value}`);
  }
}
```

:::zone-end

:::zone pivot="rest"

## Step 1: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are out of the in_progress state to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

### Upload a file

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/files?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/vector_stores?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store"
  }'
```

### Attach the uploaded file to the vector store

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/vector_stores/vs_abc123/files?api-version=2024-12-01-preview \
    -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "file_id": "assistant-abc123"
    }'
```

## Step 2: Create an agent and enable file search

```bash
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


## Step 3: Create a thread

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread
 
```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "Which months do we have covered in the financial statements?"
    }'
```

## Step 4: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

### Run the thread

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

### Retrieve the agent response

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end