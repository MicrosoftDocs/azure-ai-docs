---
title: "File search tool for Microsoft Foundry agents"
description: "Configure the file search tool for Microsoft Foundry agents. Upload files, create vector stores, and query documents with Python, C#, and REST examples."
services: cognitive-services
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 08/05/2026
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.custom: azure-ai-agents, references_regions, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-file-search-upload-new
---

# File search tool for agents

Use the file search tool to ground Microsoft Foundry agents in your own data. With file search, agents can retrieve relevant information from your documents and use it to generate more accurate, context-aware responses, augmenting agents with knowledge such as proprietary product information or user-provided documents.

In this article, you learn how to:

- Upload files and create a vector store
- Configure an agent with file search enabled
- Query your documents through the agent

By using the standard agent setup, the file search tool ensures your files remain in your own storage. Your Azure AI Search resource ingests the files, so you maintain complete control over your data.

> [!IMPORTANT]
> File search has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token-based fees for model usage.

## Prerequisites

- A [basic or standard agent environment](../../../agents/environment-setup.md)
- The SDK package for your language:
  - **Python**: `azure-ai-projects` (latest)
  - **.NET**: `Azure.AI.Extensions.OpenAI`
  - **TypeScript**: `@azure/ai-projects` (latest)
  - **Java**: `azure-ai-agents`
- **Storage Blob Data Contributor** role on your project's storage account (required for uploading files to your project's storage)
- **Foundry User** role on the Foundry project to create and run agents.

  [!INCLUDE [role-rename-note](../../../includes/role-rename-note.md)]
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Your Foundry project endpoint URL and model deployment name.

## Upload and query a file

For the shortest path to a grounded response, complete these actions in order:

1. Create or select a file that contains a fact you can test.
1. Upload the file and add it to a vector store.
1. Wait for ingestion to finish.
1. Attach file search to an agent, and ask a question that only the file can answer.
1. Verify that the response uses the uploaded content, and then delete the resources you created.

The Python and TypeScript examples show the upload-and-query flow in one program. Cleanup requirements vary by example, so follow the cleanup instructions in the selected language section.

## Usage support

The following table shows SDK and setup support.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Code examples

The following examples show how to upload a file, create a vector store, configure an agent with file search enabled, and query the agent.

### Prepare your sample

- **Hosted C#**: Install `Microsoft.Agents.AI.Foundry.Hosting` and use `AddFoundryToolboxes`. See the [maintained hosted toolbox sample](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox).
- **REST**: Use a Bash-compatible shell with Azure CLI, Azure Developer CLI, and `curl`. Set `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL_DEPLOYMENT_NAME`, obtain an `AGENT_TOKEN`, and capture the returned file, vector store, and toolbox version IDs. The toolbox requests remain authenticated with the bearer token.
- **Java**: Install JDK 17 or later and Maven 3.8 or later. Before running the Java code, use another language sample, REST, or the Foundry portal to upload the file, create the vector store and toolbox, and create the remote-tool project connection. For maintained Java client examples, see the [Azure AI Agents Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/).

> [!TIP]
> You can customize file search behavior at runtime, such as specifying which vector store to use per request, by using [structured inputs](../structured-inputs.md).

:::zone pivot="python"
## Create an agent with the file search tool

The following code sample shows how to add the file search tool to a toolbox and attach the toolbox to an agent. You need to upload files and create a vector store before running this code. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Agent Framework [`FoundryChatClient`](../../quickstarts/responses-api.md) to build an ephemeral, in-process agent.

### Prompt agents

```python
from pathlib import Path

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential

# Format: "https://resource_name.ai.azure.com/api/projects/project_name"
PROJECT_ENDPOINT = "your_project_endpoint"

# Load the file to be indexed for search.
asset_file_path = (Path(__file__).parent / "../assets/product_info.md").resolve()

# Create clients to call Foundry API
project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)
openai = project.get_openai_client()
# The openai client uses {PROJECT_ENDPOINT}/openai/v1 for file and vector store operations

# Create vector store and upload file
vector_store = openai.vector_stores.create(name="ProductInfoStore")

with asset_file_path.open("rb") as file_handle:
    vector_store_file = openai.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store.id,
        file=file_handle,
    )

# Create agent with file search tool
agent = project.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
        model="gpt-5-mini",
        instructions=(
            "You are a helpful agent that can search through product information. "
            "Use file search to answer questions from the uploaded files."
        ),
        tools=[FileSearchTool(vector_store_ids=[vector_store.id])],
    ),
    description="File search agent for product information queries.",
)

# Create conversation and generate response
conversation = openai.conversations.create()

response = openai.responses.create(
    conversation=conversation.id,
    input="Tell me about Contoso products",
    extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
)
print(response.output_text)

# Clean up resources
project.agents.delete_version(
    agent_name=agent.name,
    agent_version=agent.version,
)
openai.vector_stores.delete(vector_store.id)
```

### Expected output

The following output comes from the preceding code sample:

```console
[Response text grounded in your uploaded document content]
```

### References

- Reference: [Azure SDK for Python sample: file search](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search_in_stream.py)
- Reference: [Microsoft Foundry REST API](https://ai.azure.com/api-reference)

### Hosted agents

This sample creates the file-search toolbox with the Azure AI Projects SDK, then uses [`FoundryChatClient`](../../quickstarts/responses-api.md) from the Microsoft Agent Framework and connects to the toolbox MCP endpoint by using [`FoundryToolbox`](https://aka.ms/foundry-toolbox-maf). Set the `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_MODEL` environment variables, and sign in by using `az login`.

```python
import asyncio
from pathlib import Path

from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient, FoundryToolbox
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchToolboxTool
from azure.identity import AzureCliCredential

PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"

async def main() -> None:
    credential = AzureCliCredential()

    # Load the file to be indexed for search.
    asset_file_path = (Path(__file__).parent / "../assets/product_info.md").resolve()

    # Create vector store and upload file.
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    openai = project.get_openai_client()
    vector_store = openai.vector_stores.create(name="ProductInfoStore")

    with asset_file_path.open("rb") as file_handle:
        vector_store_file = openai.vector_stores.files.upload_and_poll(
            vector_store_id=vector_store.id,
            file=file_handle,
        )

    # 1. Add the file search tool to a toolbox. Using a toolbox is the recommended way
    #    to give agents tools: you curate tools once and reuse the toolbox across agents.
    #    See /azure/foundry/agents/concepts/toolbox-overview
    toolbox = project.toolboxes.create_version(
        name="file-search-toolbox",
        description="Toolbox with the file search tool",
        tools=[FileSearchToolboxTool(vector_store_ids=[vector_store.id])],
    )

    # 2. The toolbox exposes an MCP-compatible endpoint.
    TOOLBOX_MCP_URL = (
        f"{PROJECT_ENDPOINT}/toolboxes/{toolbox.name}"
        f"/versions/{toolbox.version}/mcp?api-version=v1"
    )

    # 3. Attach the toolbox to the hosted agent as an MCP tool.
,
        timeout=120.0,
    )
    toolbox_tool = FoundryToolbox(credential, url=TOOLBOX_MCP_URL)

agent = Agent(
        client=FoundryChatClient(credential=credential),
        instructions="You are a helpful assistant that can search through files to find information.",
        tools=[toolbox_tool],
    )

    result = await agent.run("What is the weather today? Do a file search to find the answer.")
    print(f"Agent: {result.text}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Expected output

The agent searches the indexed file content from the vector store and returns a grounded response. Console output shows the final response text containing the answer derived from the uploaded file.

```console
Agent: The weather today is sunny with a high of 75F.
```

For the full sample, see [foundry_chat_client_with_file_search.py](https://github.com/microsoft/agent-framework/blob/main/python/samples/02-agents/providers/foundry/foundry_chat_client_with_file_search.py).

---

:::zone-end

:::zone pivot="csharp"
## File search sample with agent

In this example, you create a local file, upload it to Azure, and use it in the newly created `VectorStore` for file search. Select **Prompt Agents** to use the Azure AI Projects SDK to create a server-side prompt agent, or **Hosted Agents** to use the Microsoft Agent Framework to build an ephemeral, in-process agent.

### Prompt agents

The code in this example is synchronous and streaming. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample8_FileSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using System.IO;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Files;
using OpenAI.VectorStores;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create a toy example file and upload it using OpenAI mechanism.
string filePath = "sample_file_for_upload.txt";
File.WriteAllText(
    path: filePath,
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
OpenAIFileClient fileClient = projectClient.ProjectOpenAIClient.GetOpenAIFileClient();
OpenAIFile uploadedFile = fileClient.UploadFile(filePath: filePath, purpose: FileUploadPurpose.Assistants);
File.Delete(filePath);

// Create the VectorStore and provide it with uploaded file ID.
VectorStoreClient vctStoreClient = projectClient.ProjectOpenAIClient.GetVectorStoreClient();
VectorStoreCreationOptions options = new()
{
    Name = "MySampleStore",
    FileIds = { uploadedFile.Id }
};
VectorStore vectorStore = vctStoreClient.CreateVectorStore(options: options);

// Create an Agent capable of using File search.
DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
{
    Instructions = "You are a helpful agent that can help fetch data from files you know about.",
    Tools = { ResponseTool.CreateFileSearchTool(vectorStoreIds: new[] { vectorStore.Id }), }
};
AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Ask a question about the file's contents.
ProjectResponsesClient responseClient = projectClient.ProjectOpenAIClient.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseResult response = responseClient.CreateResponse("Can you give me the documented codes for 'banana' and 'orange'?");

Console.WriteLine(response.GetOutputText());

// Remove all the resources created in this sample.
projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
vctStoreClient.DeleteVectorStore(vectorStoreId: vectorStore.Id);
fileClient.DeleteFile(uploadedFile.Id);
```

### Expected output

The following output comes from the preceding code sample:

```console
The code for 'banana' is 673457. I couldn't find any documented code for 'orange' in the files I have access to.
```

### Hosted agents

The following code is an integration fragment. It creates the file-search toolbox with the Azure AI Projects SDK, then uses the Microsoft Agent Framework `AddFoundryToolboxes` integration. For the required packages, imports, and maintained helper implementation, see [Connect a hosted agent to a toolbox](use-toolbox-hosted-agent.md#connect-the-hosted-agent) and the [public hosted toolbox sample](https://github.com/microsoft/agent-framework/tree/main/dotnet/samples/04-hosting/FoundryHostedAgents/responses/Hosted-Toolbox). Set the `AZURE_AI_PROJECT_ENDPOINT`, `AZURE_OPENAI_ENDPOINT`, and `AZURE_AI_MODEL_DEPLOYMENT_NAME` environment variables, and sign in with `az login`.

**Helper-dependent integration fragment:**

```csharp
using System;
using System.IO;
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.AI;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;
using OpenAI.Files;
using OpenAI.VectorStores;

const string AgentInstructions = "You are a helpful assistant that can search through uploaded files to answer questions.";
const string AgentName = "FileSearchAgent";

string projectEndpoint = Environment.GetEnvironmentVariable("AZURE_AI_PROJECT_ENDPOINT")
    ?? "https://<account>.services.ai.azure.com/api/projects/<project>";
string openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT is not set.");
string deploymentName = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-5-mini";

DefaultAzureCredential credential = new();

// 1. Create the file search tool and add it to a toolbox. Using a toolbox is the
//    recommended way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);

// Create a toy example file and upload it using OpenAI mechanism.
string filePath = "sample_file_for_upload.txt";
File.WriteAllText(
    path: filePath,
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
OpenAIFileClient fileClient = projectClient.ProjectOpenAIClient.GetOpenAIFileClient();
OpenAIFile uploadedFile = fileClient.UploadFile(filePath: filePath, purpose: FileUploadPurpose.Assistants);
File.Delete(filePath);

// Create the VectorStore and provide it with uploaded file ID.
VectorStoreClient vctStoreClient = projectClient.ProjectOpenAIClient.GetVectorStoreClient();
VectorStoreCreationOptions options = new()
{
    Name = "MySampleStore",
    FileIds = { uploadedFile.Id }
};
VectorStore vectorStore = vctStoreClient.CreateVectorStore(options: options);

ProjectsAgentTool fileSearchTool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateFileSearchTool(vectorStoreIds: new[] { vectorStore.Id }));

ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
    .GetAgentToolboxes().CreateToolboxVersion(
        toolboxName: "file-search-toolbox",
        tools: [fileSearchTool],
        description: "Toolbox with the file search tool");

// Create the hosted agent and register the toolbox integration.
AIAgent agent = projectClient.AsAIAgent(
    model: deploymentName,
    instructions: "You are a helpful assistant with access to the toolbox tools.",
    name: "hosted-toolbox-agent");

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.Services.AddFoundryToolboxes(credential, toolboxVersion.Name);

var app = builder.Build();
app.MapFoundryResponses();
app.Run();
```

### Expected output

The hosted agent uses the toolbox MCP endpoint to search the vector store configured in the file-search toolbox and answers with grounded content.

```console
Response: The youngest employee is Alice Johnson, who is 28 years old.
File Citation - File Id: file-abc123
```

For a maintained .NET Agent Framework integration, see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md).

---

## File search sample with agent in streaming scenarios

In this example, you create a local file, upload it to Azure, and use it in the newly created `VectorStore` for file search. The code in this example is synchronous and streaming. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/ai/Azure.AI.Extensions.OpenAI/samples/Sample11_FileSearch_Streaming.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using System.IO;
using Azure.AI.Projects;
using Azure.AI.Extensions.OpenAI;
using Azure.Identity;
using OpenAI.Files;
using OpenAI.VectorStores;

class FileSearchStreamingDemo
{
    // Create a helper method ParseResponse to format streaming response output.
    // If the stream ends up in error state, it will throw an error. 
    private static void ParseResponse(StreamingResponseUpdate streamResponse)
    {
        if (streamResponse is StreamingResponseCreatedUpdate createUpdate)
        {
            Console.WriteLine($"Stream response created with ID: {createUpdate.Response.Id}");
        }
        else if (streamResponse is StreamingResponseOutputTextDeltaUpdate textDelta)
        {
            Console.WriteLine($"Delta: {textDelta.Delta}");
        }
        else if (streamResponse is StreamingResponseOutputTextDoneUpdate textDoneUpdate)
        {
            Console.WriteLine($"Response done with full message: {textDoneUpdate.Text}");
        }
        else if (streamResponse is StreamingResponseOutputItemDoneUpdate itemDoneUpdate)
        {
            if (itemDoneUpdate.Item is MessageResponseItem messageItem)
            {
                foreach (ResponseContentPart part in messageItem.Content)
                {
                    foreach (ResponseMessageAnnotation annotation in part.OutputTextAnnotations)
                    {
                        if (annotation is FileCitationMessageAnnotation fileAnnotation)
                        {
                            // Note fileAnnotation.Filename will be available in OpenAI package versions
                            // greater then 2.6.0.
                            Console.WriteLine($"File Citation - File ID: {fileAnnotation.FileId}");
                        }
                    }
                }
            }
        }
        else if (streamResponse is StreamingResponseErrorUpdate errorUpdate)
        {
            throw new InvalidOperationException($"The stream has failed with the error: {errorUpdate.Message}");
        }
    }
    public static void Main()
    {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        var projectEndpoint = "your_project_endpoint";

        // Create project client to call Foundry API
        AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

        // Create a toy example file and upload it using OpenAI mechanism.
        string filePath = "sample_file_for_upload.txt";
        File.WriteAllText(
            path: filePath,
            contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
        OpenAIFile uploadedFile = projectClient.ProjectOpenAIClient.GetProjectFilesClient().UploadFile(filePath: filePath, purpose: FileUploadPurpose.Assistants);
        File.Delete(filePath);

        // Create the `VectorStore` and provide it with uploaded file ID.
        VectorStoreCreationOptions options = new()
        {
            Name = "MySampleStore",
            FileIds = { uploadedFile.Id }
        };
        VectorStore vectorStore = projectClient.ProjectOpenAIClient.GetProjectVectorStoresClient().CreateVectorStore(options);

        // 1. Add the file search tool to a toolbox. Using a toolbox is the recommended
        //    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
        AgentToolboxes toolboxClient = projectClient.AgentAdministrationClient.GetAgentToolboxes();

        ProjectsAgentTool fileSearchTool = ProjectsAgentTool.AsProjectTool(
            ResponseTool.CreateFileSearchTool(vectorStoreIds: new[] { vectorStore.Id }));

        ToolboxVersion toolboxVersion = projectClient.AgentAdministrationClient
            .GetAgentToolboxes().CreateToolboxVersion(
                toolboxName: "file-search-toolbox",
                tools: [fileSearchTool],
                description: "Toolbox with the file search tool");

        // 2. The toolbox exposes an MCP-compatible endpoint.
        var toolboxMcpUrl = new Uri(
            $"{projectEndpoint}/toolboxes/{toolboxVersion.Name}" +
            $"/versions/{toolboxVersion.Version}/mcp?api-version=v1");

        // 3. Create a remote-tool project connection that points at the toolbox endpoint.
        //    Use a user Entra token so the caller's identity is passed through
        //    (audience https://ai.azure.com). Create the connection once, for example
        //    with the Azure Developer CLI:
        //
        //    azd ai connection create file-search-toolbox-conn \
        //      --kind remote-tool \
        //      --target "<toolboxMcpUrl>" \
        //      --auth-type user-entra-token \
        //      --audience https://ai.azure.com
        var toolboxConnectionName = "file-search-toolbox-conn";

        // 4. Attach the toolbox to the prompt agent as an MCP tool.
        McpTool toolboxTool = ResponseTool.CreateMcpTool(
            serverLabel: "toolbox",
            serverUri: toolboxMcpUrl,
            toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
                GlobalMcpToolCallApprovalPolicy.NeverRequireApproval));
        toolboxTool.ProjectConnectionId = toolboxConnectionName;

        DeclarativeAgentDefinition agentDefinition = new(model: "gpt-5-mini")
        {
            Instructions = "You are a helpful agent that can help fetch data from files you know about.",
            Tools = { toolboxTool }
        };
        AgentVersion agentVersion = projectClient.AgentAdministrationClient.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition)
        );

        // Create the conversation to store responses.
        ProjectConversation conversation = projectClient.ProjectOpenAIClient.GetProjectConversationsClient().CreateProjectConversation();
        CreateResponseOptions responseOptions = new()
        {
            Agent = agentVersion,
            AgentConversationId = conversation.Id,
            StreamingEnabled = true,
        };
        // Wait for the stream to complete.
        responseOptions.InputItems.Clear();
        responseOptions.InputItems.Add(ResponseItem.CreateUserMessageItem("Can you give me the documented codes for 'banana' and 'orange'?"));
        foreach (StreamingResponseUpdate streamResponse in projectClient.ProjectOpenAIClient.Responses.CreateResponseStreaming(responseOptions))
        {
            ParseResponse(streamResponse);
        }

        // Ask follow up question and start a new stream.
        Console.WriteLine("Demonstrating follow-up query with streaming...");
        responseOptions.InputItems.Clear();
        responseOptions.InputItems.Add(ResponseItem.CreateUserMessageItem("What was my previous question about?"));
        foreach (StreamingResponseUpdate streamResponse in projectClient.ProjectOpenAIClient.Responses.CreateResponseStreaming(responseOptions))
        {
            ParseResponse(streamResponse);
        }

        // Remove all the resources created in this sample.
        projectClient.AgentAdministrationClient.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
        projectClient.ProjectOpenAIClient.GetProjectVectorStoresClient().DeleteVectorStore(vectorStoreId: vectorStore.Id);
        projectClient.ProjectOpenAIClient.GetProjectFilesClient().DeleteFile(uploadedFile.Id);
    }
}
```

### Expected output

The following output comes from the preceding code sample:

```console
Stream response created with ID: <response-id>
Delta: The code for 'banana' is 673457. I couldn't find any documented code for 'orange' in the files I have access to.
Response done with full message: The code for 'banana' is 673457. I couldn't find any documented code for 'orange' in the files I have access to.
File Citation - File ID: <file-id>
Demonstrating follow-up query with streaming...
Stream response created with ID: <response-id>
Delta: Your previous question was about the documented codes for 'banana' and 'orange'.
Response done with full message: Your previous question was about the documented codes for 'banana' and
'orange'.
```
:::zone-end

:::zone pivot="typescript"
## Sample file search with agent

The following TypeScript sample shows how to add the file search tool to a toolbox and attach the toolbox to an agent. You need to upload files and create a vector store before running this code. See the [File search behavior by agent setup type](#file-search-behavior-by-agent-setup-type) section below for details. For a JavaScript example, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentFileSearch.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  // Load the file to be indexed for search
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const assetFilePath = path.join(__dirname, "../assets/product_info.md");

  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  // The openai client uses {PROJECT_ENDPOINT}/openai/v1 for file and vector store operations
  const openai = project.getOpenAIClient();

  // Create vector store and upload file
  const vectorStore = await openai.vectorStores.create({
    name: "ProductInfoStore",
  });

  const fileStream = fs.createReadStream(assetFilePath);
  const file = await openai.vectorStores.files.uploadAndPoll(vectorStore.id, fileStream);

  console.log("Creating a toolbox with the file search tool...");

  // 1. Add the file search tool to a toolbox. Using a toolbox is the recommended
  //    way to give agents tools. See /azure/foundry/agents/concepts/toolbox-overview
  const toolbox = await project.toolboxes.createVersion(
    "file-search-toolbox",
    [
      {
        type: "file_search",
        file_search: {
          vector_store_ids: [vectorStore.id],
        },
      },
    ],
    { description: "Toolbox with the file search tool" },
  );

  // 2. The toolbox exposes an MCP-compatible endpoint.
  const toolboxMcpUrl =
    `${PROJECT_ENDPOINT}/toolboxes/${toolbox.name}` +
    `/versions/${toolbox.version}/mcp?api-version=v1`;

  // 3. Create a remote-tool project connection that points at the toolbox endpoint.
  //    Use a user Entra token so the caller's identity is passed through
  //    (audience https://ai.azure.com). Create the connection once, for example
  //    with the Azure Developer CLI:
  //
  //    azd ai connection create file-search-toolbox-conn \
  //      --kind remote-tool \
  //      --target "<toolboxMcpUrl>" \
  //      --auth-type user-entra-token \
  //      --audience https://ai.azure.com
  const toolboxConnectionName = "file-search-toolbox-conn";

  // 4. Attach the toolbox to a prompt agent as an MCP tool.
  const agent = await project.agents.createVersion("agent-file-search", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant that can search through product information.",
    tools: [
      {
        type: "mcp",
        server_label: "toolbox",
        server_url: toolboxMcpUrl,
        require_approval: "never",
        project_connection_id: toolboxConnectionName,
      },
    ],
  });

  // Create conversation and generate response
  const conversation = await openai.conversations.create();

  const response = await openai.responses.create(
    {
      conversation: conversation.id,
      input: "Tell me about Contoso products",
    },
    {
      body: { agent_reference: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(response.output_text);

  // Clean up resources
  await project.agents.deleteVersion(agent.name, agent.version);
  await openai.vectorStores.delete(vectorStore.id);
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### Expected output

```output
[Response text grounded in your uploaded document content]
```

### References

- Reference: [Azure SDK for JavaScript sample: file search](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2/javascript/agents/tools/agentFileSearch.js)
- Reference: [Microsoft Foundry REST API](https://ai.azure.com/api-reference)

:::zone-end

:::zone pivot="java"

## Use file search in a Java agent

> [!TIP]
> Most agents use a [toolbox](../../concepts/toolbox-overview.md) to add the file search tool and attach the toolbox to your agent as an MCP tool. If you use the Java SDK, an API for creating toolboxes isn't yet available. Create a toolbox by using the Python, REST API, C#, TypeScript, or the [Foundry portal](../../how-to/tools/toolbox.md), then reference its MCP endpoint from your Java agent as an `McpTool`.

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.2.0</version>
</dependency>
```

### Create an agent with file search

Before running this sample, create a file and vector store using the `{projectEndpoint}/openai/v1/files` and `{projectEndpoint}/openai/v1/vector_stores` REST endpoints. Then create a file-search toolbox out of band by using the Python, REST, C#, or TypeScript example, or the Foundry portal. Create the remote-tool project connection for the toolbox MCP endpoint before you attach it to the Java agent.

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.AzureCreateResponseOptions;
import com.azure.ai.agents.models.McpTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Collections;

public class FileSearchExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String toolboxMcpUrl = projectEndpoint
            + "/toolboxes/file-search-toolbox/versions/1/mcp?api-version=v1";
        String toolboxConnectionName = "file-search-toolbox-conn";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // The Java SDK doesn't yet expose a toolbox creation API. Create the
        // toolbox with Python, REST, C#, TypeScript, or the Foundry portal, then
        // attach its MCP endpoint as an MCP tool.
        McpTool toolboxTool = new McpTool("toolbox")
            .setServerUrl(toolboxMcpUrl)
            .setProjectConnectionId(toolboxConnectionName)
            .setRequireApproval("never");

        // Create agent with the toolbox MCP tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a helpful assistant that can search through files to answer questions.")
            .setTools(Collections.singletonList(toolboxTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("file-search-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createAzureResponse(
            new AzureCreateResponseOptions().setAgentReference(agentReference),
            ResponseCreateParams.builder()
                .input("What information is in the uploaded files?"));

        System.out.println("Response: " + response.output());

        // Clean up
        agentsClient.deleteAgentVersion(agent.getName(), agent.getVersion());
    }
}
```

### Expected output

```output
Agent created: file-search-agent (version 1)
Response: [ResponseOutputItem containing file search results ...]
```

For more examples including file upload and vector store creation, see the [Azure AI Agents Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/ai/azure-ai-agents/src/samples/).

:::zone-end

:::zone pivot="rest"
## Upload files and add them to a vector store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. Then poll the store's status until all files are out of the `in_progress` state to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

Set the following environment variable before running the examples:

```bash
AGENT_TOKEN=$(az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv)
```

### Upload a file

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/v1/files \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/v1/vector_stores \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store",
    "file_ids": ["'$FILE_ID'"]
  }'
```

## Add file search to a toolbox and create an agent

The recommended way to add file search is through a toolbox, then attach the toolbox to your agent as an MCP tool. See [What is a toolbox?](../../concepts/toolbox-overview.md)

### Upload files for toolbox use

To create a file and vector store for use with a toolbox, upload the file at the **resource-level** Files endpoint with the `x-aml-project-id` header. Use the project GUID from `properties.amlWorkspace.internalId`.

1. Upload your file: `POST {account_endpoint}/openai/v1/files` with `purpose=assistants` and header `x-aml-project-id: {project-guid}`.
1. Create a vector store: `POST {account_endpoint}/openai/v1/vector_stores` with the returned file ID and the same `x-aml-project-id` header.

The resulting vector store ID is the value you supply as `<VECTOR_STORE_ID>`.

1. Create a toolbox that contains the file search tool:

    ```bash
    curl --request POST \
      --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/file-search-toolbox/versions?api-version=v1" \
      -H "Authorization: Bearer $AGENT_TOKEN" \
      -H "Content-Type: application/json" \
      --data '{
        "description": "Toolbox with the file search tool",
        "tools": [
          {
            "type": "file_search",
            "file_search": {
              "vector_store_ids": ["'$VECTOR_STORE_ID'"]
            },
            "max_num_results": 20
          }
        ]
      }'
    ```

   The toolbox exposes an MCP-compatible endpoint at `$FOUNDRY_PROJECT_ENDPOINT/toolboxes/file-search-toolbox/versions/<version>/mcp?api-version=v1`, where `<version>` is the version returned by the previous call.

1. Create a remote-tool project connection that points at the toolbox endpoint, using a user Entra token so the caller's identity is passed through (audience `https://ai.azure.com`).

    ```bash
    azd ai connection create file-search-toolbox-conn \
      --kind remote-tool \
      --target "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/file-search-toolbox/versions/<version>/mcp?api-version=v1" \
      --auth-type user-entra-token \
      --audience https://ai.azure.com
    ```

1. Create an agent that uses the toolbox by attaching it as an MCP tool.

    ```bash
    curl -X POST "$FOUNDRY_PROJECT_ENDPOINT/agents?api-version=v1" \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $AGENT_TOKEN" \
      -d '{
        "name": "<AGENT_NAME>-file-search",
        "description": "Agent with file search",
        "definition": {
          "kind": "prompt",
          "model": "'$FOUNDRY_MODEL_DEPLOYMENT_NAME'",
          "tools": [
            {
              "type": "mcp",
              "server_label": "toolbox",
              "server_url": "'$FOUNDRY_PROJECT_ENDPOINT'/toolboxes/file-search-toolbox/versions/<version>/mcp?api-version=v1",
              "require_approval": "never",
              "project_connection_id": "file-search-toolbox-conn"
            }
          ],
          "instructions": "You are a customer support chatbot. Use file search results from the vector store to answer questions based on the uploaded files."
        }
      }'
    ```

### Dynamic vector store selection (parameter override)

When you add file search to a toolbox, you can supply `vector_store_ids` in two ways:

- **Pinned at toolbox creation** — include `vector_store_ids` in the tool configuration (as shown in the previous example). The vector store is fixed for every call and can't be overridden at runtime.
- **Dynamic at runtime (parameter override)** — omit `vector_store_ids` from the tool configuration. Callers supply it in the `tools/call` arguments, so each call can target a different vector store. This enables scenarios like multitenant document stores where every request searches a different set of files.

Create the toolbox without `vector_store_ids`:

```bash
curl --request POST \
  --url "$FOUNDRY_PROJECT_ENDPOINT/toolboxes/file-search-toolbox/versions?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "description": "File search with dynamic vector store",
    "tools": [
      { "type": "file_search" }
    ]
  }'
```

When you omit `vector_store_ids`, callers pass it in the `tools/call` arguments:

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"file_search","arguments":{"queries":["search text"],"vector_store_ids":["<VECTOR_STORE_ID>"]}}}
```

> [!NOTE]
> The REST API, Python SDK, .NET SDK, JavaScript SDK, and Azure Developer CLI support dynamic `vector_store_ids`. The Foundry portal UI currently requires `vector_store_ids` when you add a File Search tool.

> [!IMPORTANT]
> When you use File Search through a toolbox in a hosted agent, **user isolation isn't supported**. All users in the same project share access to any vector stores referenced in the tool configuration or provided at runtime.

## Create response with file search

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/v1/responses \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "agent": {
    "type": "agent_reference",
    "name": "<AGENT_NAME>-file-search"
  },
  "metadata": {
    "test_response": "file_search_enabled",
    "vector_store_id": "'$VECTOR_STORE_ID'"
  },
  "input": [{
    "type": "message",
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "Can you search the uploaded file and tell me about Azure TV instructions?"
      }
    ]
  }],
  "stream": true
}'
```

The response returns streaming output containing the agent's answer based on information retrieved from the vector store. The agent searches through your uploaded file to answer the query about Azure TV instructions.

### Clean up

Delete the agent.

```bash
curl -X DELETE "$FOUNDRY_PROJECT_ENDPOINT/agents/<AGENT_NAME>-file-search?api-version=v1" \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

Delete the vector store.

```bash
curl --request DELETE \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/v1/vector_stores/$VECTOR_STORE_ID \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

Delete the file.

```bash
curl --request DELETE \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/v1/files/$FILE_ID \
  -H "Authorization: Bearer $AGENT_TOKEN"
```

### References

- Reference: [Microsoft Foundry REST API](https://ai.azure.com/api-reference)
:::zone-end

## Verify file search results

After running a code sample in this article, verify that file search is working:

- Confirm that the vector store and file are created.
  - In the Python and TypeScript samples, the upload-and-poll helpers complete only after ingestion finishes.
- Ask a question that you can answer only from your uploaded content.
- Confirm that the response is grounded in your documents.

### File sources

- Upload local files (Basic and Standard agent setup) 
- Azure Blob Storage (Standard setup only)

## File search behavior by agent setup type

### Basic agent setup

The file search tool has the same functionality as Azure OpenAI Responses API. The tool uses Microsoft managed search and storage resources. 

- You store uploaded files in Microsoft managed storage. 
- You create a vector store by using a Microsoft managed search resource. 

### Standard agent setup

The file search tool uses the Azure AI Search and Azure Blob Storage resources you connect to during agent setup. 

- You store uploaded files in your connected Azure Blob Storage account. 
- You create vector stores by using your connected Azure AI Search resource. 

For both agent setups, the service handles the entire ingestion process, which includes:

- Automatically parsing and chunking documents.
- Generating and storing embeddings.
- Utilizing both vector and keyword searches to retrieve relevant content for user queries. 

The code is identical for both setups. The only variation is where your files and vector stores are stored. 

## When to use file search

Choose file search when you need to:

- Search through documents you upload directly (PDFs, Word docs, code files)
- Enable agents to answer questions from proprietary or confidential content
- Process files up to 512 MB without managing external search infrastructure

Consider alternatives for these scenarios:

| Scenario | Recommended tool |
| -------- | ---------------- |
| Search existing Azure AI Search indexes | [Azure AI Search tool](ai-search.md) |
| Search the public web for current information | [Web search tool](web-search.md) |
| Combine multiple data sources in one query | Use multiple tools together |

## How file search works

The file search tool uses retrieval best practices to extract relevant data from your files and improve model responses.

### Query processing

When you send a query, file search:

1. **Rewrites** your query to optimize it for search.
1. **Breaks down** complex queries into parallel searches.
1. **Runs hybrid search** combining keyword and semantic matching across vector stores.
1. **Reranks results** to select the most relevant content for the response.

### Default chunking settings

| Setting | Default value |
| ------- | ------------- |
| Chunk size | 800 tokens |
| Chunk overlap | 400 tokens |
| Embedding model | text-embedding-3-large (256 dimensions) |
| Max chunks in context | 20 |

## Vector stores

Vector store objects give the file search tool the ability to search your files. When you add a file to a vector store, the process automatically parses, chunks, embeds, and stores the file in a vector database that supports both keyword and semantic search. Each vector store can hold up to 10,000 files. You can attach vector stores to both agents and conversations. Currently, you can attach at most one vector store to an agent and at most one vector store to a conversation.

For background concepts and lifecycle guidance (readiness, deletion behavior, and expiration policies), see [Vector stores for file search](../../concepts/vector-stores.md).

Remove files from a vector store by:

- Deleting the vector store file object.
- Deleting the underlying file object. This action removes the file from all `vector_store` and `code_interpreter` configurations across all agents and conversations in your organization.

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens (computed automatically when you attach a file).

## Ensuring vector store readiness before creating runs

Ensure the system fully processes all files in a vector store before you create a run. This ensures all data in your vector store is searchable. Check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the vector store object to ensure the status is **completed**.

As a fallback, the run object includes a 60-second maximum wait when the conversation's vector store contains files that are still processing. This wait ensures that any files your users upload in a conversation are fully searchable before the run proceeds. This fallback wait doesn't apply to the agent's vector store.

### Conversation vector stores have default expiration policies

Vector stores that you create by using conversation helpers (like `tool_resources.file_search.vector_stores` in conversations or `message.attachments` in Messages) have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run).

When a vector store expires, the runs on that conversation fail. To fix this problem, recreate a new vector store with the same files and reattach it to the conversation.

## Supported file types

> [!NOTE]
> For text MIME types, the encoding must be UTF-8, UTF-16, or ASCII.

| File format | MIME Type |
| --- | --- |
| `.c` | `text/x-c` |
| `.cs` | `text/x-csharp` |
| `.cpp` | `text/x-c++` |
| `.doc` | `application/msword` |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| `.html` | `text/html` |
| `.java` | `text/x-java` |
| `.json` | `application/json` |
| `.md` | `text/markdown` |
| `.pdf` | `application/pdf` |
| `.php` | `text/x-php` |
| `.pptx` | `application/vnd.openxmlformats-officedocument.presentationml.presentation` |
| `.py` | `text/x-python` |
| `.py` | `text/x-script.python` |
| `.rb` | `text/x-ruby` |
| `.tex` | `text/x-tex` |
| `.txt` | `text/plain` |
| `.css` | `text/css` |
| `.js` | `text/javascript` |
| `.sh` | `application/x-sh` |
| `.ts` | `application/typescript` |

## Limitations

Keep these limits in mind when you plan your file search integration:

- File search supports specific file formats and encodings. See [Supported file types](#supported-file-types).
- Each vector store can hold up to 10,000 files.
- You can attach at most one vector store to an agent and at most one vector store to a conversation.
- Features and availability vary by region. See [Microsoft Foundry region support](../../../reference/region-support.md).

## Troubleshooting

| Issue | Likely cause | Resolution |
| --- | --- | --- |
| 401 Unauthorized | The access token is missing, expired, or scoped incorrectly. | Get a fresh token and retry the request. For REST calls, confirm you set `AGENT_TOKEN` correctly. |
| 403 Forbidden | The signed-in identity doesn't have the required roles. | Confirm the roles in [Prerequisites](#prerequisites) and retry after role assignment finishes propagating. |
| 404 Not Found | The project endpoint or resource identifiers are incorrect. | Confirm `FOUNDRY_PROJECT_ENDPOINT` and IDs such as agent name, version, vector store ID, and file ID. |
| Responses ignore your files | The agent isn't configured with `file_search`, or the vector store isn't attached. | Confirm the agent definition includes `file_search` and the `vector_store_ids` list contains your vector store ID. |
| File upload times out | Large file or slow network connection. | Use `upload_and_poll` to handle large files. Consider chunking very large documents. |
| Vector store creation fails | Quota exceeded or invalid file format. | Check vector store limits (10,000 files per store). Verify file format is supported. |
| Search returns irrelevant results | File content not properly indexed or query too broad. | Wait for indexing to complete (check `vector_store.status`). Use more specific queries. |
| No citations in response | Model didn't use file search or content not found. | Use `tool_choice="required"` to force file search. Verify the file content matches your query topic. |

## Related content

- [Azure AI Search tool](ai-search.md) - Search existing Azure AI Search indexes from your agents
- [Web search tool](web-search.md) - Enable agents to search the public web
- [Vector stores for file search](../../concepts/vector-stores.md) - Understand vector store lifecycle and expiration
- [Structured inputs](../structured-inputs.md) - Parameterize agent definitions at runtime
