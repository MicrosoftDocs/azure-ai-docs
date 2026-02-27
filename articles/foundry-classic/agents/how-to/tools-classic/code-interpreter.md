---
title: 'How to use Foundry Agent Service Code Interpreter'
titleSuffix: Microsoft Foundry
description: Learn how to use Foundry Agent Service Code Interpreter
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 11/20/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents
zone_pivot_groups: selection-code-interpreter
---
# Foundry Agent Service Code Interpreter

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Code Interpreter documentation](../../../default/agents/how-to/tools/code-interpreter.md?view=foundry&preserve-view=true).

Code Interpreter allows the agents to write and run Python code in a sandboxed execution environment. With Code Interpreter enabled, your agent can run code iteratively to solve more challenging code, math, and data analysis problems or create graphs and charts. When your Agent writes code that fails to run, it can iterate on this code by modifying and running different code until the code execution succeeds.

> [!IMPORTANT]
> Code Interpreter has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for Azure OpenAI usage. If your Agent calls Code Interpreter simultaneously in two different threads, two code interpreter sessions are created. Each session is active by default for 1 hour with an idle timeout of 30 minutes.

## Prerequisites

- A [basic or standard agent environment](../../environment-setup.md).


## Code samples
<!--
Use the following file search tool samples to implement it in your agents. You can also add this tool to agents [using the Microsoft Foundry portal](./overview.md#add-tools-to-your-agents-in-the-azure-ai-foundry-portal).
-->

:::zone pivot="python"

### Create an agent with code interpreter
```python
code_interpreter = CodeInterpreterTool()

# An agent is created with the Code Interpreter capabilities:
agent = project_client.agents.create_agent(
    model=os.environ["MODEL_DEPLOYMENT_NAME"],
    name="my-agent",
    instructions="You are helpful agent",
    tools=code_interpreter.definitions,
    tool_resources=code_interpreter.resources,
)
```

### Attach a file for code interpreter to use

If you want a file to use with code interpreter, you can use the `upload_and_poll` function. 

```python
file = agents_client.files.upload_and_poll(file_path=asset_file_path, purpose=FilePurpose.AGENTS)
print(f"Uploaded file, file ID: {file.id}")

code_interpreter = CodeInterpreterTool(file_ids=[file.id])
```


::: zone-end

:::zone pivot="csharp"

### Create an agent with code interpreter

```csharp
var projectEndpoint = System.Environment.GetEnvironmentVariable("ProjectEndpoint");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("ModelDeploymentName");

PersistentAgentsClient client = new(projectEndpoint, new DefaultAzureCredential());

PersistentAgent agent = client.Administration.CreateAgent(
    model: modelDeploymentName,
    name: "My Friendly Test Agent",
    instructions: "You politely help with math questions. Use the code interpreter tool when asked to visualize numbers.",
    tools: [new CodeInterpreterToolDefinition()]
);
```

### Attach a file for code interpreter to use

If you want a file to use with code interpreter, you can attach it to your message. 

```csharp
PersistentAgentFileInfo uploadedAgentFile = client.Files.UploadFile(
    filePath: "sample_file_for_upload.txt",
    purpose: PersistentAgentFilePurpose.Agents);
var fileId = uploadedAgentFile.Id;

var attachment = new MessageAttachment(
    fileId: fileId,
    tools: tools
);

// attach the file to the message
PersistentThreadMessage message = client.Messages.CreateMessage(
    threadId: thread.Id,
    role: MessageRole.User,
    content: "Can you give me the documented information in this file?",
    attachments: [attachment]
);
```

::: zone-end

:::zone pivot="javascript"

### Create an agent with code interpreter

```javascript
// Create the code interpreter tool
const codeInterpreterTool = ToolUtility.createCodeInterpreterTool();

// Enable the code interpreter tool during agent creation
const agent = await client.createAgent("gpt-4o", {
  name: "my-agent",
  instructions: "You are a helpful agent",
  tools: [codeInterpreterTool.definition],
  toolResources: codeInterpreterTool.resources,
});
console.log(`Created agent, agent ID: ${agent.id}`);
```

### Attach a file for code interpreter to use

If you want a file to use with code interpreter, you can attach it to the tool. 

```javascript
// Upload file and wait for it to be processed
const filePath = "./examplefile.csv";
const localFileStream = fs.createReadStream(filePath);
const localFile = await client.files.upload(localFileStream, "assistants", {
  fileName: "localFile",
});
// Create code interpreter tool
const codeInterpreterTool = ToolUtility.createCodeInterpreterTool([localFile.id]);
```

::: zone-end

:::zone pivot="rest-api"

### Create an agent with the code interpreter tool

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
      }
    }
  }'
```

::: zone-end

:::zone pivot="java"

```java 
String agentName = "code_interpreter_agent";
CodeInterpreterToolDefinition ciTool = new CodeInterpreterToolDefinition();
CreateAgentOptions createAgentOptions = new CreateAgentOptions(modelName).setName(agentName).setInstructions("You are a helpful agent").setTools(Arrays.asList(ciTool));
PersistentAgent agent = administrationClient.createAgent(createAgentOptions);
```

### Attach a file for code interpreter to use

If you want a file to use with code interpreter, you can attach it to the tool. 

```java
FileInfo uploadedFile = filesClient.uploadFile(new UploadFileRequest(
    new FileDetails(BinaryData.fromFile(htmlFile))
    .setFilename("sample.html"), FilePurpose.AGENTS));

MessageAttachment messageAttachment = new MessageAttachment(Arrays.asList(BinaryData.fromObject(ciTool))).setFileId(uploadedFile.getId());

PersistentAgentThread thread = threadsClient.createThread();
ThreadMessage createdMessage = messagesClient.createMessage(
    thread.getId(),
    MessageRole.USER,
    "What does the attachment say?",
    Arrays.asList(messageAttachment),
    null);
```

::: zone-end
 
### Supported models

The [models page](../../quotas-limits.md) contains the most up-to-date information on regions/models where agents and code interpreter are supported.

We recommend using Agents with the latest models to take advantage of the new features, larger context windows, and more up-to-date training data.

### Supported file types

|File format|MIME Type|
|---|---|
|`.c`| `text/x-c` |
|`.cpp`|`text/x-c++` |
|`.csv`|`application/csv`|
|`.docx`|`application/vnd.openxmlformats-officedocument.wordprocessingml.document`|
|`.html`|`text/html`|
|`.java`|`text/x-java`|
|`.json`|`application/json`|
|`.md`|`text/markdown`|
|`.pdf`|`application/pdf`|
|`.php`|`text/x-php`|
|`.pptx`|`application/vnd.openxmlformats-officedocument.presentationml.presentation`|
|`.py`|`text/x-python`|
|`.py`|`text/x-script.python`|
|`.rb`|`text/x-ruby`|
|`.tex`|`text/x-tex`|
|`.txt`|`text/plain`|
|`.css`|`text/css`|
|`.jpeg`|`image/jpeg`|
|`.jpg`|`image/jpeg`|
|`.js`|`text/javascript`|
|`.gif`|`image/gif`|
|`.png`|`image/png`|
|`.tar`|`application/x-tar`|
|`.ts`|`application/typescript`|
|`.xlsx`|`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`|
|`.xml`|`application/xml` or `text/xml`|
|`.zip`|`application/zip`|
