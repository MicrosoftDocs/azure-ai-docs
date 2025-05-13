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

Azure AI Agents supports using the Code Interpreter tool, which allows an agent to write and run code within a secure, sandboxed execution environment. This enables the agent to perform tasks such as data analysis, mathematical calculations, or file manipulation based on user requests. This article provides step-by-step instructions and code samples for enabling and utilizing the Code Interpreter tool with your Azure AI Agent.

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

## Initialization
The code begins by setting up the necessary imports and initializing the AI Project client:

```python
import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import CodeInterpreterTool
from azure.ai.projects.models import FilePurpose, MessageRole
from azure.identity import DefaultAzureCredential
from pathlib import Path

project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(), 
    conn_str=os.environ["PROJECT_CONNECTION_STRING"]
)
```

## File Upload
The sample uploads a data file for analysis:

```python
file = project_client.agents.upload_file_and_poll(
    file_path="nifty_500_quarterly_results.csv", 
    purpose=FilePurpose.AGENTS
)
```


## Code Interpreter Setup
The Code Interpreter tool is initialized with the uploaded file:

```python
code_interpreter = CodeInterpreterTool(file_ids=[file.id])
```

## Agent Creation
An agent is created with the Code Interpreter capabilities:

```python
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-assistant",
    instructions="You are helpful assistant",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

## Thread Management
The code creates a conversation thread and initial message:

```python
thread = project_client.agents.create_thread()
message = project_client.agents.create_message(
    thread_id=thread.id,
    role="user",
    content="Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
)
```

## Message Processing
A run is created to process the message and execute code:

```python
run = project_client.agents.create_and_process_run(thread_id=thread.id, agent_id=agent.id)
```

## File Handling
The code handles the output files and annotations:

```python
messages = project_client.agents.list_messages(thread_id=thread.id)

# Save generated image files
for image_content in messages.image_contents:
    file_id = image_content.image_file.file_id
    file_name = f"{file_id}_image_file.png"
    project_client.agents.save_file(file_id=file_id, file_name=file_name)

# Process file path annotations
for file_path_annotation in messages.file_path_annotations:
    print(f"File Paths:")
    print(f"Type: {file_path_annotation.type}")
    print(f"Text: {file_path_annotation.text}")
    print(f"File ID: {file_path_annotation.file_path.file_id}")
```

## Cleanup
After completing the interaction, the code properly cleans up resources:

```python
project_client.agents.delete_file(file.id)
project_client.agents.delete_agent(agent.id)
```

This ensures proper resource management and prevents unnecessary resource consumption.

:::zone-end

:::zone pivot="csharp" 

## Create a client and agent

First, set up the configuration using `appsettings.json`, create a `PersistentAgentsClient`, and then create a `PersistentAgent` with the Code Interpreter tool enabled.

```csharp
    using Azure;
    using Azure.AI.Agents.Persistent;
    using Azure.Identity;
    using Microsoft.Extensions.Configuration;
    using System.Diagnostics;
    
    IConfigurationRoot configuration = new ConfigurationBuilder()
        .SetBasePath(AppContext.BaseDirectory)
        .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
        .Build();
    
    var projectEndpoint = configuration["ProjectEndpoint"];
    var modelDeploymentName = configuration["ModelDeploymentName"];
    
    PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());
    
    PersistentAgent agent = client.Administration.CreateAgent(
        model: modelDeploymentName,
        name: "My Friendly Test Agent",
        instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
        tools: [new CodeInterpreterToolDefinition()]
    );
```

## Create a thread and add a message

Next, create a `PersistentAgentThread` for the conversation and add the initial user message.

```csharp
    PersistentAgentThread thread = client.Threads.CreateThread();
    
    client.Messages.CreateMessage(
        thread.Id,
        MessageRole.User,
        "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9.");
```

## Create and monitor a run

Then, create a `ThreadRun` for the thread and agent. Poll the run's status until it completes or requires action.

```csharp
    ThreadRun run = client.Runs.CreateRun(
        thread.Id,
        agent.Id,
        additionalInstructions: "Please address the user as Jane Doe. The user has a premium account.");
    
    do
    {
        Thread.Sleep(TimeSpan.FromMilliseconds(500));
        run = client.Runs.GetRun(thread.Id, run.Id);
    }
    while (run.Status == RunStatus.Queued
        || run.Status == RunStatus.InProgress
        || run.Status == RunStatus.RequiresAction);
```

## Process the results and handle files

Once the run is finished, retrieve all messages from the thread. Iterate through the messages to display text content and handle any generated image files by saving them locally and opening them.

```csharp
    Pageable<ThreadMessage> messages = client.Messages.GetMessages(
        threadId: thread.Id,
        order: ListSortOrder.Ascending);
    
    foreach (ThreadMessage threadMessage in messages)
    {
        foreach (MessageContent content in threadMessage.ContentItems)
        {
            switch (content)
            {
                case MessageTextContent textItem:
                    Console.WriteLine($"[{threadMessage.Role}]: {textItem.Text}");
                    break;
                case MessageImageFileContent imageFileContent:
                    Console.WriteLine($"[{threadMessage.Role}]: Image content file ID = {imageFileContent.FileId}");
                    BinaryData imageContent = client.Files.GetFileContent(imageFileContent.FileId);
                    string tempFilePath = Path.Combine(AppContext.BaseDirectory, $"{Guid.NewGuid()}.png");
                    File.WriteAllBytes(tempFilePath, imageContent.ToArray());
                    client.Files.DeleteFile(imageFileContent.FileId);
    
                    ProcessStartInfo psi = new()
                    {
                        FileName = tempFilePath,
                        UseShellExecute = true
                    };
                    Process.Start(psi);
                    break;
            }
        }
    }
```

## Clean up resources

Finally, delete the thread and the agent to clean up the resources created in this sample.

```csharp
    client.Threads.DeleteThread(threadId: thread.Id);
    client.Administration.DeleteAgent(agentId: agent.Id);
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
