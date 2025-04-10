---
title: 'How to upload files using the file search tool'
titleSuffix: Azure OpenAI
description: Find code samples and instructions for uploading files to Azure AI Agent Service.
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
from azure.ai.projects.models import FileSearchTool, MessageAttachment, FilePurpose
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
project_client = AIProjectClient.from_connection_string(
    credential=credential, conn_str=os.environ["PROJECT_CONNECTION_STRING"] 
)
```

## Step 2: Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store.

```python
file = project_client.agents.upload_file_and_poll(file_path='./data/product_catelog.md', purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

vector_store = project_client.agents.create_vector_store_and_poll(file_ids=[file.id], name="my_vectorstore")
print(f"Created vector store, vector store ID: {vector_store.id}")
```

## Step 3: Create an agent and enable file search

Create a `FileSearchTool` object with the `vector_store` ID, and attach `tools` and `tool_resources` to the agent.

```python
file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])

agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are a helpful agent",
    tools=file_search_tool.definitions,
    tool_resources=file_search_tool.resources,
)
print(f"Created agent, agent ID: {agent.id}")
```

## Step 4: Create a thread

Attach files as message attachments on your thread.

```python
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

message_file = project_client.agents.upload_file_and_poll(file_path='product_info_1.md', purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {message_file.id}")

attachment = MessageAttachment(file_id=message_file.id, tools=FileSearchTool().definitions)
message = project_client.agents.create_message(
    thread_id=thread.id, role="user", content="What feature does Smart Eyewear offer?", attachments=[attachment]
)
print(f"Created message, message ID: {message.id}")
```

## Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

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

var connectionString = TestEnvironment.AzureAICONNECTIONSTRING;
AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential());
```

## Step 2: Upload files and add them to a Vector Store

Upload your files and create a vector store.

```csharp
File.WriteAllText(
    path: "sample_file_for_upload.txt",
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
Response<AgentFile> uploadAgentFileResponse = await client.UploadFileAsync(
    filePath: "sample_file_for_upload.txt",
    purpose: AgentFilePurpose.Agents);

AgentFile uploadedAgentFile = uploadAgentFileResponse.Value;

VectorStore vectorStore = await client.CreateVectorStoreAsync(
    fileIds: new List<string> { uploadedAgentFile.Id },
    name: "my_vector_store");
```

## Step 3: Create an agent and enable file search

Create a `FileSearchTool` object with the `vector_store` ID, and attach `tools` and `tool_resources` to the agent.

```csharp
FileSearchToolResource fileSearchToolResource = new FileSearchToolResource();
fileSearchToolResource.VectorStoreIds.Add(vectorStore.Id);

Response<Agent> agentResponse = await client.CreateAgentAsync(
    model: "gpt-4o-mini",
    name: "SDK Test Agent - Retrieval",
    instructions: "You are a helpful agent that can help fetch data from files you know about.",
    tools: new List<ToolDefinition> { new FileSearchToolDefinition() },
    toolResources: new ToolResources() { FileSearch = fileSearchToolResource });
Agent agent = agentResponse.Value;
```

## Step 4: Create a thread

Attach files as message attachments on your thread.

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

Create a `FileSearchTool` object with the `vector_store` ID, and attach `tools` and `tool_resources` to the agent.

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

Attach files as message attachments on your thread.

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

## Step 2: Upload files and add them to a Vector Store

Upload your files and create a vector store.

```console
curl $AZURE_AI_AGENTS_ENDPOINT/files?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/vector_stores?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store"
  }'
```

## Step 4: Create a thread

Attach files as message attachments on your thread.

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "Which months do we have covered in the financial statements?"
    }'
```

## Step 5: Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

```console
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end