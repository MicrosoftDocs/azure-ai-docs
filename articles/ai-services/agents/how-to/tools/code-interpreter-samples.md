---
title: 'Code interpreter code samples'
titleSuffix: Azure AI Foundry
description: Find code samples to enable code interpreter for Azure AI Agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/09/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents-code
zone_pivot_groups: selection-code-interpreter
---

# How to use the code interpreter tool

Use this article to find step-by-step instructions and code samples for using code interpreter.

:::zone pivot="portal"

## Using the code interpreter tool with an agent

You can add the code interpreter tool to an agent programatically using the code examples listed at the top of this article, or the [Azure AI Foundry portal](https://ai.azure.com/). If you want to use the portal:

1. In the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **action**. Then select **Add**.

    :::image type="content" source="../../media/tools/action-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools.png":::

1. Select **Code interpreter** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/action-tools-list.png" alt-text="A screenshot showing the available action tools in the Azure AI Foundry portal." lightbox="../../media/tools/action-tools-list.png":::

1. You can optionally upload files for your agent to read and interpret information from datasets, generate code, and create graphs and charts using your data. 

    :::image type="content" source="../../media/tools/code-interpreter.png" alt-text="A screenshot showing the code interpreter upload page." lightbox="../../media/tools/code-interpreter.png":::

:::zone-end 

:::zone pivot="python"

## Create a project client

To use code interpreter, first add the `import` statements shown in the example, and create a project client, which will contain a connection string to your AI project, and will be used to authenticate API calls.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose
from azure.identity import DefaultAzureCredential
from pathlib import Path

# Create an Azure AI Client from a connection string, copied from your Azure AI Foundry project.
# At the moment, it should be in the format "<HostName>;<AzureSubscriptionId>;<ResourceGroup>;<HubName>"
# Customer needs to login to Azure subscription via Azure CLI and set the environment variables
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)
```

## Upload a File

Upload the file using the `upload_and_poll()` function, specifying the file path and the `FilePurpose.AGENTS` purpose.

```python
# Upload a file and add it to the client 
file = project_client.agents.upload_file_and_poll(
    file_path="nifty_500_quarterly_results.csv", purpose=FilePurpose.AGENTS
)
print(f"Uploaded file, file ID: {file.id}")
```

## Create an Agent with the Code Interpreter Tool

Define the `code_interpreter` tool with `CodeInterpreterTool()` and include the file ID of the file you uploaded. Afterwards, create the agent with tools set to `code_interpreter.definitions` and `tool_resources` set to `code_interpreter.resources`.

```python
code_interpreter = CodeInterpreterTool(file_ids=[file.id])

# create agent with code interpreter tool and tools_resources
agent = project_client.agents.create_agent(
    model="gpt-4o-mini",
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

## Create a Thread, Message, and Get the Agent Response

Next create a thread with `create_thread()` and attach a message to it using `create_message()` that will trigger the code interpreter tool. Afterwards, create and execute a run with `create_and_process_run()`. Once the run finishes, you can delete the file from the agent with `delete_file()` to free up space in the agent. Finally, print the messages from the agent.

```python
# create a thread
thread = project_client.agents.create_thread()
print(f"Created thread, thread ID: {thread.id}")

# create a message
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Could you please create bar chart in the TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
)
print(f"Created message, message ID: {message.id}")

# create and execute a run
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# delete the original file from the agent to free up space (note: this does not delete your version of the file)
project_client.agents.delete_file(file.id)
print("Deleted file")

# print the messages from the agent
messages = project_client.agents.list_messages(thread_id=thread.id)
print(f"Messages: {messages}")

# get the most recent message from the assistant
last_msg = messages.get_last_text_message_by_sender("assistant")
if last_msg:
    print(f"Last Message: {last_msg.text.value}")
```

## Download Files Generated by Code Interpreter

Files generated by Code Interpreter can be found in the Agent message responses. You can download image files generated by code interpreter by iterating through the response's image_contents and calling `save_file()` with a name and the file ID.

```python
# save the newly created file
for image_content in messages.image_contents:
  print(f"Image File ID: {image_content.image_file.file_id}")
  file_name = f"{image_content.image_file.file_id}_image_file.png"
  project_client.agents.save_file(file_id=image_content.image_file.file_id, file_name=file_name)
  print(f"Saved image file to: {Path.cwd() / file_name}") 
```

:::zone-end

:::zone pivot="csharp" 

## Create a project client 

To use code interpreter, first you need to create a project client, which will contain a connection string to your AI project, and will be used to authenticate API calls.

```csharp
var connectionString = Environment.GetEnvironmentVariable("PROJECT_CONNECTION_STRING");
AgentsClient client = new AgentsClient(connectionString, new DefaultAzureCredential()); 
```

## Upload a File

Files can be uploaded and then referenced by agents or messages. First, use the generalized upload API with a `purpose` of `Agents` to make a file ID available. Once uploaded, the file ID can then be provided to create a vector store for it. The vector store ID can then be provided to an agent upon creation.

```csharp
// Upload a file and wait for it to be processed
Response<AgentFile> uploadAgentFileResponse = await client.UploadFileAsync(
    filePath: "sample_file_for_upload.txt",
    purpose: AgentFilePurpose.Agents);

AgentFile uploadedAgentFile = uploadAgentFileResponse.Value;

// Create a vector store with the file and wait for it to be processed.
// If you do not specify a vector store, create_message will create a vector store with a default expiration policy of seven days after they were last active
VectorStore vectorStore = await client.CreateVectorStoreAsync(
    fileIds:  new List<string> { uploadedAgentFile.Id },
    name: "my_vector_store");

CodeInterpreterToolResource codeInterpreterToolResource = new CodeInterpreterToolResource();
CodeInterpreterToolResource.VectorStoreIds.Add(vectorStore.Id);
```

## Create an Agent with the Code Interpreter Tool

```csharp
Response<Agent> agentResponse = await client.CreateAgentAsync(
    model: "gpt-4o-mini",
    name: "My agent",
    instructions: "You are a helpful agent.",
    tools: new List<ToolDefinition> { new CodeInterpreterToolDefinition() },
    toolResources: new ToolResources() { CodeInterpreter = codeInterpreterToolResource });
Agent agent = agentResponse.Value;
```

## Create a Thread, Message, and Get the Agent Response

Next create a thread with `CreateThreadAsync()` and a thread with `CreateMessageAsync()`. After the thread is created, you can add messages to it with `CreateMessageAsync()` that will cause the code interpreter tool to trigger. Create a run, and then continue polling it until it reaches a terminal status. Assuming the run was successful, parse the agent's response by listing the messages.

```csharp
//Create a thread
Response<AgentThread> threadResponse = await client.CreateThreadAsync();
AgentThread thread = threadResponse.Value;

//With a thread created, messages can be created on it:
Response<ThreadMessage> messageResponse = await client.CreateMessageAsync(
    thread.Id,
    MessageRole.User,
    "I need to solve the equation `3x + 11 = 14`. Can you help me?");
ThreadMessage message = messageResponse.Value;

//A run can then be started that evaluates the thread against an agent:
Response<ThreadRun> runResponse = await client.CreateRunAsync(
    thread.Id,
    agent.Id,
    additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");
ThreadRun run = runResponse.Value;

//Once the run has started, it should then be polled until it reaches a terminal status:
do
{
    await Task.Delay(TimeSpan.FromMilliseconds(500));
    runResponse = await client.GetRunAsync(thread.Id, runResponse.Value.Id);
}
while (runResponse.Value.Status == RunStatus.Queued
    || runResponse.Value.Status == RunStatus.InProgress);

//Assuming the run successfully completed, listing messages from the thread that was run will now reflect new information added by the agent:

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

## Download Files Generated by Code Interpreter

Files generated by code interpreter can be found in the Agent message responses. You can download image files generated by code interpreter by iterating through the response's messages and checking for an `ImageFileId`. If that field exists, use the following code:

```csharp
foreach (MessageContent contentItem in message.Content)
{
    if (!string.IsNullOrEmpty(contentItem.ImageFileId))
    {
        OpenAIFileInfo imageInfo = await fileClient.GetFileAsync(contentItem.ImageFileId);
        BinaryData imageBytes = await fileClient.DownloadFileAsync(contentItem.ImageFileId);
        using FileStream stream = File.OpenWrite($"{imageInfo.Filename}.png");
        imageBytes.ToStream().CopyTo(stream);

        Console.WriteLine($"<image: {imageInfo.Filename}.png>");
    }
}
```

:::zone-end

:::zone pivot="javascript" 

## Create a project client 

To use code interpreter, first you need to create a project client, which will contain a connection string to your AI project, and will be used to authenticate API calls.

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

## Upload a File

Files can be uploaded and then referenced by agents or messages. Once it's uploaded it can be added to the tool utility for referencing.

```javascript
const fileStream = fs.createReadStream("nifty_500_quarterly_results.csv");
const fFile = await client.agents.uploadFile(fileStream, "assistants", {
  fileName: "nifty_500_quarterly_results.csv",
});
console.log(`Uploaded local file, file ID : ${file.id}`);

const codeInterpreterTool = ToolUtility.createCodeInterpreterTool([file.id]);
```

## Create an Agent with the Code Interpreter Tool

```javascript
// Notice that CodeInterpreter must be enabled in the agent creation, otherwise the agent will not be able to see the file attachment
const agent = await client.agents.createAgent("gpt-4o-mini", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [codeInterpreterTool.definition],
  toolResources: codeInterpreterTool.resources,
});
console.log(`Created agent, agent ID: ${agent.id}`);
```

## Create a Thread, Message, and Get the Agent Response

```javascript
// create a thread
const thread = await client.agents.createThread();
  
// add a message to thread
await client.agents.createMessage(
    thread.id, {
    role: "user",
    content: "I need to solve the equation `3x + 11 = 14`. Can you help me?",
});
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

## Download files generated by code interpreter

Files uploaded by Agents cannot be retrieved back. If your use case needs to access the file content uploaded by the Agents, you are advised to keep an additional copy accessible by your application. However, files generated by Agents are retrievable by getFileContent.

```javascript
const messages = await client.agents.listMessages(thread.id);
const imageFile = (messages.data[0].content[0] as MessageImageFileContentOutput).imageFile;
const imageFileName = (await client.agents.getFile(imageFile.fileId)).filename;

const fileContent = await (await client.agents.getFileContent(imageFile.fileId).asNodeStream()).body;
if (fileContent) {
  const chunks: Buffer[] = [];
  for await (const chunk of fileContent) {
    chunks.push(Buffer.from(chunk));
  }
  const buffer = Buffer.concat(chunks);
  fs.writeFileSync(imageFileName, buffer);
} else {
  console.error("Failed to retrieve file content: fileContent is undefined");
}
console.log(`Saved image file to: ${imageFileName}`);
```

:::zone-end


:::zone pivot="rest-api" 

## Upload a file 

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/files?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\file.csv"
```

## Create an agent with the code interpreter tool

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/assistants?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "You are an AI assistant that can write code to help answer math questions.",
    "tools": [
      { "type": "code_interpreter" }
    ],
    "model": "gpt-4o-mini",
    "tool_resources"{
      "code interpreter": {
          "file_ids": ["assistant-1234"]
      }
    }
  }'
```

## Create a thread

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Add a user question to the thread

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    }'
```

## Run the thread

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

## Retrieve the status of the run

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

## Retrieve the agent response

```bash
curl $AZURE_AI_AGENTS_ENDPOINT/threads/thread_abc123/messages?api-version=2024-12-01-preview \
  -H "Authorization: Bearer $AZURE_AI_AGENTS_TOKEN"
```

:::zone-end