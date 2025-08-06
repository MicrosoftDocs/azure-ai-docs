---
title: "Code interpreter code samples"
titleSuffix: Azure AI Foundry
description: Find code samples to enable code interpreter for Azure AI Agents.
author: aahill
ms.author: aahi
manager: nitinme
ms.date: 06/30/2025
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.custom:
  - azure-ai-agents-code
  - build-2025
zone_pivot_groups: selection-code-interpreter
---

# How to use the code interpreter tool

Azure AI Agents supports using the Code Interpreter tool, which allows an agent to write and run code within a secure, sandboxed execution environment. This enables the agent to perform tasks such as data analysis, mathematical calculations, or file manipulation based on user requests. This article provides step-by-step instructions and code samples for enabling and utilizing the Code Interpreter tool with your Azure AI Agent.

:::zone pivot="portal"

## Using the code interpreter tool with an agent

You can add the code interpreter tool to an agent programmatically using the code examples listed at the top of this article, or the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs). If you want to use the portal:

1. In the **Agents** screen for your agent, scroll down the **Setup** pane on the right to **action**. Then select **Add**.

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
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool


# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
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
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

## Thread Management
The code creates a conversation thread and initial message:

```python
thread = project_client.agents.threads.create()
message = project_client.agents.messages.create(
    thread_id=thread.id,
    role=MessageRole.USER,
    content="Could you please create bar chart in TRANSPORTATION sector for the operating profit from the uploaded csv file and provide file to me?",
)
```

## Message Processing
A run is created to process the message and execute code:

```python
run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
```

## File Handling
The code handles the output files and annotations:

```python
messages = project_client.agents.messages.list(thread_id=thread.id)

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

## Create a project client

Create a client object, which will contain the project endpoint for connecting to your AI project and other resources.

```csharp
using Azure;
using Azure.AI.Agents.Persistent;
using Azure.Identity;

var projectEndpoint = System.Environment.GetEnvironmentVariable("ProjectEndpoint");
var projectEndpoint = System.Environment.GetEnvironmentVariable("ModelDeploymentName");
var projectEndpoint = System.Environment.GetEnvironmentVariable("BingConnectionId");

// Create the Agent Client
PersistentAgentsClient agentClient = new(projectEndpoint, new DefaultAzureCredential());
```

## Create an Agent with the Grounding with Bing search tool enabled

To make the Grounding with Bing search tool available to your agent, use a connection to initialize the tool and attach it to the agent. You can find your connection in the **connected resources** section of your project in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

```csharp

BingGroundingToolDefinition bingGroundingTool = new(
    new BingGroundingSearchToolParameters(
        [new BingGroundingSearchConfiguration(bingConnectionId)]
    )
);

// Create the Agent
PersistentAgent agent = agentClient.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "my-agent",
    instructions: "Use the bing grounding tool to answer questions.",
    tools: [bingGroundingTool]
);
```

## Create a thread and run

```csharp
PersistentAgentThread thread = agentClient.Threads.CreateThread();

// Create message and run the agent
PersistentThreadMessage message = agentClient.Messages.CreateMessage(
    thread.Id,
    MessageRole.User,
    "How does wikipedia explain Euler's Identity?");
ThreadRun run = agentClient.Runs.CreateRun(thread, agent);

```

## Wait for the agent to complete and print the output

First, wait for the agent to complete the run by polling its status. Observe that the model uses the Grounding with Bing Search tool to provide a response to the user's question.

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

Then, retrieve and process the messages from the completed run.

```csharp
// Retrieve all messages from the agent client
Pageable<PersistentThreadMessage> messages = agentClient.Messages.GetMessages(
    threadId: thread.Id,
    order: ListSortOrder.Ascending
);

// Process messages in order
foreach (PersistentThreadMessage threadMessage in messages)
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
                    if (annotation is MessageTextUriCitationAnnotation urlAnnotation)
                    {
                        response = response.Replace(urlAnnotation.Text, $" [{urlAnnotation.UriCitation.Title}]({urlAnnotation.UriCitation.Uri})");
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

## Optionally output the run steps used by the agent

```csharp
// Retrieve the run steps used by the agent and print those to the console
Console.WriteLine("Run Steps used by Agent:");
Pageable<RunStep> runSteps = agentClient.Runs.GetRunSteps(run);

foreach (var step in runSteps)
{
    Console.WriteLine($"Step ID: {step.Id}, Total Tokens: {step.Usage.TotalTokens}, Status: {step.Status}, Type: {step.Type}");

    if (step.StepDetails is RunStepMessageCreationDetails messageCreationDetails)
    {
        Console.WriteLine($"   Message Creation Id: {messageCreationDetails.MessageCreation.MessageId}");
    }
    else if (step.StepDetails is RunStepToolCallDetails toolCallDetails)
    {
        // We know this agent only has the Bing Grounding tool, so we can cast it directly
        foreach (RunStepBingGroundingToolCall toolCall in toolCallDetails.ToolCalls)
        {
            Console.WriteLine($"   Tool Call Details: {toolCall.GetType()}");

            foreach (var result in toolCall.BingGrounding)
            {
                Console.WriteLine($"      {result.Key}: {result.Value}");
            }
        }
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

To use code interpreter, first you need to create a project client, which will contain an endpoint to your AI project, and will be used to authenticate API calls.

```javascript
const { AgentsClient, isOutputOfType, ToolUtility } = require("@azure/ai-agents");
const { delay } = require("@azure/core-util");
const { DefaultAzureCredential } = require("@azure/identity");
const fs = require("fs");
const path = require("node:path");
require("dotenv/config");

const projectEndpoint = process.env["PROJECT_ENDPOINT"];

// Create an Azure AI Client
const client = new AgentsClient(projectEndpoint, new DefaultAzureCredential());
```

## Upload a File

Files can be uploaded and then referenced by agents or messages. Once it's uploaded it can be added to the tool utility for referencing.

```javascript
// Upload file and wait for it to be processed
const filePath = "./data/nifty500QuarterlyResults.csv";
const localFileStream = fs.createReadStream(filePath);
const localFile = await client.files.upload(localFileStream, "assistants", {
  fileName: "localFile",
});

console.log(`Uploaded local file, file ID : ${localFile.id}`);
```

## Create an Agent with the Code Interpreter Tool

```javascript
// Create code interpreter tool
const codeInterpreterTool = ToolUtility.createCodeInterpreterTool([localFile.id]);

// Notice that CodeInterpreter must be enabled in the agent creation, otherwise the agent will not be able to see the file attachment
const agent = await client.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [codeInterpreterTool.definition],
  toolResources: codeInterpreterTool.resources,
});
console.log(`Created agent, agent ID: ${agent.id}`);
```

## Create a thread, message, and get the agent response

```javascript
// Create a thread
const thread = await client.threads.create();
console.log(`Created thread, thread ID: ${thread.id}`);

// Create a message
const message = await client.messages.create(
  thread.id,
  "user",
  "Could you please create a bar chart in the TRANSPORTATION sector for the operating profit from the uploaded CSV file and provide the file to me?",
  {
    attachments: [
      {
        fileId: localFile.id,
        tools: [codeInterpreterTool.definition],
      },
    ],
  },
);

console.log(`Created message, message ID: ${message.id}`);

// Create and execute a run
let run = await client.runs.create(thread.id, agent.id);
while (run.status === "queued" || run.status === "in_progress") {
  await delay(1000);
  run = await client.runs.get(thread.id, run.id);
}
if (run.status === "failed") {
  // Check if you got "Rate limit is exceeded.", then you want to get more quota
  console.log(`Run failed: ${run.lastError}`);
}
console.log(`Run finished with status: ${run.status}`);

// Delete the original file from the agent to free up space (note: this does not delete your version of the file)
await client.files.delete(localFile.id);
console.log(`Deleted file, file ID: ${localFile.id}`);

// Print the messages from the agent
const messagesIterator = client.messages.list(thread.id);
const allMessages = [];
for await (const m of messagesIterator) {
  allMessages.push(m);
}
console.log("Messages:", allMessages);

// Get most recent message from the assistant
const assistantMessage = allMessages.find((msg) => msg.role === "assistant");
if (assistantMessage) {
  const textContent = assistantMessage.content.find((content) => isOutputOfType(content, "text"));
  if (textContent) {
    console.log(`Last message: ${textContent.text.value}`);
  }
}

// Save the newly created file
console.log(`Saving new files...`);
const imageFile = allMessages[0].content[0].imageFile;
console.log(`Image file ID : ${imageFile.fileId}`);
const imageFileName = path.resolve(
  "./data/" + (await client.files.get(imageFile.fileId)).filename + "ImageFile.png",
);

const fileContent = await (await client.files.getContent(imageFile.fileId).asNodeStream()).body;
if (fileContent) {
  const chunks = [];
  for await (const chunk of fileContent) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  const buffer = Buffer.concat(chunks);
  fs.writeFileSync(imageFileName, buffer);
} else {
  console.error("Failed to retrieve file content: fileContent is undefined");
}
console.log(`Saved image file to: ${imageFileName}`);

// Iterate through messages and print details for each annotation
console.log(`Message Details:`);
allMessages.forEach((m) => {
  console.log(`File Paths:`);
  console.log(`Type: ${m.content[0].type}`);
  if (isOutputOfType(m.content[0], "text")) {
    const textContent = m.content[0];
    console.log(`Text: ${textContent.text.value}`);
  }
  console.log(`File ID: ${m.id}`);
});

// Delete the agent once done
await client.deleteAgent(agent.id);
console.log(`Deleted agent, agent ID: ${agent.id}`);
```

<!--
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
-->
:::zone-end


:::zone pivot="rest-api" 

Follow the [REST API Quickstart](../../quickstart.md?pivots=rest-api#api-call-information) to set the right values for the environment variables `AGENT_TOKEN`, `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` and `API_VERSION`.

## Upload a file 

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/files?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\file.csv"
```

## Create an agent with the code interpreter tool

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/assistants?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
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
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d ''
```

## Add a user question to the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
      "role": "user",
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    }'
```

## Run the thread

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "asst_abc123",
  }'
```

## Retrieve the status of the run

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/runs/run_abc123?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

## Retrieve the agent response

```bash
curl --request GET \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/threads/thread_abc123/messages?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

:::zone-end
