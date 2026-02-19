---
title: 'How to upload files using the file search tool'
titleSuffix: Microsoft Foundry
description: Find code samples and instructions for uploading files to Foundry Agent Service.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/18/2025
author: alvinashcraft
ms.author: aashcraft
zone_pivot_groups: selection-bing-grounding-code
ms.custom: azure-ai-agents-code
---

# How to upload files using the file search tool

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new file search documentation](../../../default/agents/how-to/tools/file-search.md?view=foundry&preserve-view=true).

Use this article to find step-by-step instructions and code samples for uploading files using the file search tool.

## Prerequisites 

The following prerequisites are required to complete this how-to article:

1. Complete the [agent setup](../../quickstart.md).
1. Ensure that you have the role **Storage Blob Data Contributor** on your project's storage account.
1. Ensure that you have the role **Azure AI Developer** on your project.

::: zone pivot="portal"

## Add file search to an agent using the Microsoft Foundry portal

1. Go to the [Foundry portal](https://ai.azure.com/?cid=learnDocs). In the **Agents** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media\tools\knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Foundry portal." lightbox="../../media\tools\knowledge-tools.png":::

1. Select **Files** and follow the prompts to add the tool. 

    :::image type="content" source="../../media\tools\knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Foundry portal." lightbox="../../media\tools\knowledge-tools-list.png":::

    :::image type="content" source="../../media\tools\file-upload.png" alt-text="A screenshot showing the file upload page." lightbox="../../media\tools\file-upload.png":::

::: zone-end

:::zone pivot="python"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```python
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

# Define the project endpoint
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Initialize the AIProjectClient
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)  # Use Azure Default Credential for authentication
)
```

## Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store.

```python
from azure.ai.agents.models import FilePurpose

# Define the path to the file to be uploaded
file_path = "./data/product_info_1.md"

# Upload the file
file = project_client.agents.files.upload_and_poll(file_path=file_path, purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

# Create a vector store with the uploaded file
vector_store = project_client.agents.vector_stores.create_and_poll(file_ids=[file.id], name="my_vectorstore")
print(f"Created vector store, vector store ID: {vector_store.id}")
```

## Create an agent and enable file search

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

## Create a thread

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

## Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```python
# Create and process an agent run in the thread
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
print(f"Run finished with status: {run.status}")

if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Cleanup resources
project_client.agents.vector_stores.delete(vector_store.id)
print("Deleted vector store")

project_client.agents.files.delete(file_id=file.id)
print("Deleted file")

project_client.agents.delete_agent(agent.id)
print("Deleted agent")

# Fetch and log all messages from the thread
messages = project_client.agents.messages.list(thread_id=thread.id)
file_name = os.path.split(file_path)[-1]
for msg in messages:
    if msg.text_messages:
        last_text = msg.text_messages[-1].text.value
        for annotation in msg.text_messages[-1].text.annotations:
            citation = (
                file_name if annotation.file_citation.file_id == file.id else annotation.file_citation.file_id
            )
            last_text = last_text.replace(annotation.text, f" [{citation}]")
        print(f"{msg.role}: {last_text}")
```
:::zone-end

:::zone pivot="csharp"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Threading;

// Get Connection information from app configuration
IConfigurationRoot configuration = new ConfigurationBuilder()
    .SetBasePath(AppContext.BaseDirectory)
    .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
    .Build();

var projectEndpoint = configuration["ProjectEndpoint"];
var modelDeploymentName = configuration["ModelDeploymentName"];

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());

```

## Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are uploaded to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

```csharp
// Create a local sample file
System.IO.File.WriteAllText(
    path: "sample_file_for_upload.txt",
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457."
);

// Upload local sample file to the agent
PersistentAgentFileInfo uploadedAgentFile = agentClient.Files.UploadFile(
    filePath: "sample_file_for_upload.txt",
    purpose: PersistentAgentFilePurpose.Agents
);

// Setup dictionary with list of File IDs for the vector store
Dictionary<string, string> fileIds = new()
{
    { uploadedAgentFile.Id, uploadedAgentFile.Filename }
};

// Create a vector store with the file and wait for it to be processed.
// If you do not specify a vector store, CreateMessage will create a vector
// store with a default expiration policy of seven days after they were last active
PersistentAgentsVectorStore vectorStore = agentClient.VectorStores.CreateVectorStore(
    fileIds: new List<string> { uploadedAgentFile.Id },
    name: "my_vector_store");

```

## Create an agent and enable file search

Create a file search tool object with the vector store ID, and attach tool and tool resources to the agent.

```csharp
// Create tool definition for File Search
FileSearchToolResource fileSearchToolResource = new FileSearchToolResource();
fileSearchToolResource.VectorStoreIds.Add(vectorStore.Id);

// Create an agent with Tools and Tool Resources
PersistentAgent agent = agentClient.Administration.CreateAgent(
        model: modelDeploymentName,
        name: "SDK Test Agent - Retrieval",
        instructions: "You are a helpful agent that can help fetch data from files you know about.",
        tools: new List<ToolDefinition> { new FileSearchToolDefinition() },
        toolResources: new ToolResources() { FileSearch = fileSearchToolResource });
```

## Create a thread and run

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```csharp
// Create the agent thread for communication
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
PersistentThreadMessage messageResponse = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "Can you give me the documented codes for 'banana' and 'orange'?");

ThreadRun run = agentClient.Runs.CreateRun(thread, agent);

```
## Wait for run completion and check status

Wait for the agent run to finish processing by polling its status. Observe that the model uses the file search tool to provide a response.

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
```

## Process messages and handle citations

Once the run is complete, retrieve the messages from the thread and process them, replacing any file citations with the actual file names.

```csharp
// Retrieve all messages from the agent client
Pageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Helper method for replacing references
static string replaceReferences(Dictionary<string, string> fileIds, string fileID, string placeholder, string text)
{
    if (fileIds.TryGetValue(fileID, out string replacement))
        return text.Replace(placeholder, $" [{replacement}]");
    else
        return text.Replace(placeholder, $" [{fileID}]");
}

// Process messages in order
foreach (PersistentThreadMessage threadMessage in messages)
{
    Console.Write($"{threadMessage.CreatedAt:yyyy-MM-dd HH:mm:ss} - {threadMessage.Role,10}: ");

    foreach (MessageContent contentItem in threadMessage.ContentItems)
    {
        if (contentItem is MessageTextContent textItem)
        {
            if (threadMessage.Role == MessageRole.Agent && textItem.Annotations.Count > 0)
            {
                string strMessage = textItem.Text;

                // If we file path or file citation annotations - rewrite the 'source' FileId with the file name
                foreach (MessageTextAnnotation annotation in textItem.Annotations)
                {
                    if (annotation is MessageTextFilePathAnnotation pathAnnotation)
                    {
                        strMessage = replaceReferences(fileIds, pathAnnotation.FileId, pathAnnotation.Text, strMessage);
                    }
                    else if (annotation is MessageTextFileCitationAnnotation citationAnnotation)
                    {
                        strMessage = replaceReferences(fileIds, citationAnnotation.FileId, citationAnnotation.Text, strMessage);
                    }
                }
                Console.Write(strMessage);
            }
            else
            {
                Console.Write(textItem.Text);
            }
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
// Clean up resources
agentClient.VectorStores.DeleteVectorStore(vectorStore.Id);
agentClient.Files.DeleteFile(uploadedAgentFile.Id);
agentClient.Threads.DeleteThread(thread.Id);
agentClient.Administration.DeleteAgent(agent.Id);

```

:::zone-end

:::zone pivot="javascript"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```javascript
const { AgentsClient, isOutputOfType, ToolUtility } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");

const fs = require("fs");
require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"];

// Create an Azure AI Client
const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```

## Upload files and add them to a Vector Store

Upload your files and create a vector store.

```javascript
// Upload file
const filePath = "./data/sampleFileForUpload.txt";
const localFileStream = fs.createReadStream(filePath);
const file = await client.files.upload(localFileStream, "assistants", {
  fileName: "sampleFileForUpload.txt",
});
console.log(`Uploaded file, file ID: ${file.id}`);

// Create vector store
const vectorStore = await client.vectorStores.create({
  fileIds: [file.id],
  name: "myVectorStore",
});
console.log(`Created vector store, vector store ID: ${vectorStore.id}`);
```

## Create an agent and enable file search

Create a `fileSearchTool` object with the vector store ID, and attach `tools` and `toolResources` to the agent.

```javascript
// Initialize file search tool
const fileSearchTool = ToolUtility.createFileSearchTool([vectorStore.id]);

// Create agent with files
const agent = await client.createAgent(modelDeploymentName, {
  name: "SDK Test Agent - Retrieval",
  instructions: "You are helpful agent that can help fetch data from files you know about.",
  tools: [fileSearchTool.definition],
  toolResources: fileSearchTool.resources,
});
console.log(`Created agent, agent ID : ${agent.id}`);
```

## Create a thread

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```javascript
// Create thread
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create message
const message = await client.messages.create(
  thread.id,
  "user",
  "Can you give me the documented codes for 'banana' and 'orange'?",
);
console.log(`Created message, message ID: ${message.id}`);
```

## Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```javascript
// Create run
let run = await client.runs.create(thread.id, agent.id);
while (["queued", "in_progress"].includes(run.status)) {
  await delay(500);
  run = await client.runs.get(thread.id, run.id);
  console.log(`Current Run status - ${run.status}, run ID: ${run.id}`);
}

console.log(`Current Run status - ${run.status}, run ID: ${run.id}`);
const messages = await client.messages.list(thread.id);
for await (const threadMessage of messages) {
  console.log(
    `Thread Message Created at  - ${threadMessage.createdAt} - Role - ${threadMessage.role}`,
  );
  threadMessage.content.forEach((content) => {
    if (isOutputOfType(content, "text")) {
      const textContent = content;
      console.log(`Text Message Content - ${textContent.text.value}`);
    } else if (isOutputOfType(content, "image_file")) {
      const imageContent = content;
      console.log(`Image Message Content - ${imageContent.imageFile.fileId}`);
    }
  });
}

// Delete agent
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);
```

:::zone-end

:::zone pivot="rest"

## Upload files and add them to a vector store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are out of the in_progress state to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

### Upload a file

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/files?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/vector_stores?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store"
  }'
```

### Attach the uploaded file to the vector store

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/vector_stores/vs_abc123/files?api-version=$API_VERSION \
    -H "Authorization: Bearer $AGENT_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
      "file_id": "assistant-abc123"
    }'
```

## Create an agent and enable file search

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Financial Analyst Assistant",
    "instructions": "You are an expert financial analyst. Use your knowledge base to answer questions about audited financial statements.",
    "tools": [{"type": "file_search"}],
    "model": "gpt-4o-mini",
    "tool_resources": {"file_search": {"vector_store_ids": ["vs_1234abcd"]}}
  }'
```


## Create a thread

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store. When you create a Run on this thread, the file search tool queries both the vector store from your agent and the vector store on the thread.

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

### Add a user question to the thread
 
```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "Which months do we have covered in the financial statements?"
    }'
```

## Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

### Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

### Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

:::zone-end

:::zone pivot="java"

## Create a project client

Create a client object that contains the endpoint for connecting to your AI project and other resources.

```java
import com.azure.ai.agents.persistent.FilesClient;
import com.azure.ai.agents.persistent.MessagesClient;
import com.azure.ai.agents.persistent.PersistentAgentsAdministrationClient;
import com.azure.ai.agents.persistent.PersistentAgentsClient;
import com.azure.ai.agents.persistent.PersistentAgentsClientBuilder;
import com.azure.ai.agents.persistent.RunsClient;
import com.azure.ai.agents.persistent.ThreadsClient;
import com.azure.ai.agents.persistent.VectorStoresClient;
import com.azure.core.util.Configuration;
import com.azure.identity.DefaultAzureCredentialBuilder;

// Get Connection information from environment variables
String projectEndpoint = Configuration.getGlobalConfiguration().get("PROJECT_ENDPOINT", "endpoint");
String modelDeploymentName = Configuration.getGlobalConfiguration().get("MODEL_DEPLOYMENT_NAME", "model");

// Create the Agent Client
PersistentAgentsClientBuilder clientBuilder = new PersistentAgentsClientBuilder()
    .endpoint(projectEndpoint)
    .credential(new DefaultAzureCredentialBuilder().build());
PersistentAgentsClient agentsClient = clientBuilder.buildClient();
PersistentAgentsAdministrationClient administrationClient = agentsClient.getPersistentAgentsAdministrationClient();
ThreadsClient threadsClient = agentsClient.getThreadsClient();
MessagesClient messagesClient = agentsClient.getMessagesClient();
RunsClient runsClient = agentsClient.getRunsClient();
FilesClient filesClient = agentsClient.getFilesClient();
VectorStoresClient vectorStoresClient = agentsClient.getVectorStoresClient();
```

## Upload files and add them to a Vector Store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are uploaded to ensure that all content is fully processed.

```java
import com.azure.ai.agents.persistent.models.FileDetails;
import com.azure.ai.agents.persistent.models.FileInfo;
import com.azure.ai.agents.persistent.models.FilePurpose;
import com.azure.ai.agents.persistent.models.UploadFileRequest;
import com.azure.ai.agents.persistent.models.VectorStore;
import com.azure.ai.agents.persistent.models.VectorStoreStatus;
import com.azure.core.util.BinaryData;
import java.util.Arrays;

// Upload file
FileInfo uploadedAgentFile = filesClient.uploadFile(
    new UploadFileRequest(
        new FileDetails(
            BinaryData.fromString("The word `apple` uses the code 442345, while the word `banana` uses the code 673457."))
            .setFilename("sample_file_for_upload.txt"),
        FilePurpose.AGENTS));
System.out.println("Uploaded file, file ID: " + uploadedAgentFile.getId());

// Create vector store
VectorStore vectorStore = vectorStoresClient.createVectorStore(
    Arrays.asList(uploadedAgentFile.getId()),
    "my_vector_store",
    null, null, null, null);
System.out.println("Created vector store, vector store ID: " + vectorStore.getId());

// Poll until vector store is ready
do {
    Thread.sleep(500);
    vectorStore = vectorStoresClient.getVectorStore(vectorStore.getId());
}
while (vectorStore.getStatus() == VectorStoreStatus.IN_PROGRESS);
```

## Create an agent and enable file search

Create a file search tool object with the vector store ID, and attach tool and tool resources to the agent.

```java
import com.azure.ai.agents.persistent.models.CreateAgentOptions;
import com.azure.ai.agents.persistent.models.FileSearchToolDefinition;
import com.azure.ai.agents.persistent.models.FileSearchToolResource;
import com.azure.ai.agents.persistent.models.PersistentAgent;
import com.azure.ai.agents.persistent.models.ToolResources;

// Create file search tool resource
FileSearchToolResource fileSearchToolResource = new FileSearchToolResource()
    .setVectorStoreIds(Arrays.asList(vectorStore.getId()));

// Create agent with file search tool
String agentName = "file_search_example";
CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelDeploymentName)
    .setName(agentName)
    .setInstructions("You are a helpful agent that can help fetch data from files you know about.")
    .setTools(Arrays.asList(new FileSearchToolDefinition()))
    .setToolResources(new ToolResources().setFileSearch(fileSearchToolResource));
PersistentAgent agent = administrationClient.createAgent(createAgentOptions);
System.out.println("Created agent, ID: " + agent.getId());
```

## Create a thread and run

You can also attach files as Message attachments on your thread. Doing so creates another vector store associated with the thread, or, if there's already a vector store attached to this thread, attaches the new files to the existing thread vector store.

```java
import com.azure.ai.agents.persistent.models.CreateRunOptions;
import com.azure.ai.agents.persistent.models.MessageRole;
import com.azure.ai.agents.persistent.models.PersistentAgentThread;
import com.azure.ai.agents.persistent.models.ThreadMessage;
import com.azure.ai.agents.persistent.models.ThreadRun;

// Create thread
PersistentAgentThread thread = threadsClient.createThread();
System.out.println("Created thread, ID: " + thread.getId());

// Create message
ThreadMessage createdMessage = messagesClient.createMessage(
    thread.getId(),
    MessageRole.USER,
    "Can you give me the documented codes for 'banana' and 'orange'?");
System.out.println("Created message, ID: " + createdMessage.getId());
```

## Create a run and check the output

Create a run and observe that the model uses the file search tool to provide a response.

```java
import com.azure.ai.agents.persistent.models.MessageContent;
import com.azure.ai.agents.persistent.models.MessageImageFileContent;
import com.azure.ai.agents.persistent.models.MessageTextContent;
import com.azure.ai.agents.persistent.models.RunStatus;
import com.azure.core.http.rest.PagedIterable;

try {
    // Run agent
    CreateRunOptions createRunOptions = new CreateRunOptions(thread.getId(), agent.getId())
        .setAdditionalInstructions("");
    ThreadRun threadRun = runsClient.createRun(createRunOptions);

    // Wait for completion
    do {
        Thread.sleep(500);
        threadRun = runsClient.getRun(thread.getId(), threadRun.getId());
    }
    while (threadRun.getStatus() == RunStatus.QUEUED
        || threadRun.getStatus() == RunStatus.IN_PROGRESS
        || threadRun.getStatus() == RunStatus.REQUIRES_ACTION);

    System.out.println("Run finished with status: " + threadRun.getStatus());

    if (threadRun.getStatus() == RunStatus.FAILED) {
        System.out.println("Run failed: " + threadRun.getLastError().getMessage());
    }

    // Print messages
    PagedIterable<ThreadMessage> runMessages = messagesClient.listMessages(thread.getId());
    for (ThreadMessage message : runMessages) {
        System.out.print(String.format("%1$s - %2$s : ", message.getCreatedAt(), message.getRole()));
        for (MessageContent contentItem : message.getContent()) {
            if (contentItem instanceof MessageTextContent) {
                System.out.print((((MessageTextContent) contentItem).getText().getValue()));
            } else if (contentItem instanceof MessageImageFileContent) {
                String imageFileId = (((MessageImageFileContent) contentItem).getImageFile().getFileId());
                System.out.print("Image from ID: " + imageFileId);
            }
            System.out.println();
        }
    }
} catch (InterruptedException e) {
    throw new RuntimeException(e);
} finally {
    // Cleanup
    threadsClient.deleteThread(thread.getId());
    System.out.println("Deleted thread");
    administrationClient.deleteAgent(agent.getId());
    System.out.println("Deleted agent");
    filesClient.deleteFile(uploadedAgentFile.getId());
    System.out.println("Deleted file");
    vectorStoresClient.deleteVectorStore(vectorStore.getId());
    System.out.println("Deleted vector store");
}
```

:::zone-end
