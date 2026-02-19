---
title: File search tool for Microsoft Foundry agents
titleSuffix: Microsoft Foundry
description: Configure the file search tool for Microsoft Foundry agents. Upload files, create vector stores, and query documents with Python, C#, and REST examples.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/04/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions, dev-focus, pilot-ai-workflow-jan-2026
ai-usage: ai-assisted
zone_pivot_groups: selection-file-search-upload-new
---

# File search tool for agents

Use the file search tool to enable Microsoft Foundry agents to search through your documents and retrieve relevant information. File search augments agents with knowledge from outside their model, such as proprietary product information or user-provided documents.

In this article, you learn how to:

- Upload files and create a vector store
- Configure an agent with file search enabled
- Query your documents through the agent

> [!NOTE]
> By using the standard agent setup, the improved file search tool ensures your files remain in your own storage. Your Azure AI Search resource ingests the files, so you maintain complete control over your data.

> [!IMPORTANT]
> File search has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token-based fees for model usage.

## Usage support

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ | ✔️ | ✔️ | - | ✔️ | ✔️ | ✔️ |

Java SDK samples are not yet available.

## Prerequisites

- A [basic or standard agent environment](../../../../agents/environment-setup.md)
- The latest prerelease SDK package:
  - **Python**: `pip install azure-ai-projects azure-identity python-dotenv --pre`
  - **C#**: `dotnet add package Azure.AI.Projects.OpenAI --prerelease`
  - **TypeScript**: `npm install @azure/ai-projects @azure/identity dotenv`
- **Storage Blob Data Contributor** role on your project's storage account (required for uploading files to your project's storage)
- **Azure AI Owner** role on your Foundry resource (required for creating agent resources)
- Environment variables configured: `FOUNDRY_PROJECT_ENDPOINT`, `MODEL_DEPLOYMENT_NAME`

## Create an agent with file search

:::zone pivot="python"
## Create an agent with the file search tool

The following code sample shows how to create an agent with the file search tool enabled. You need to upload files and create a vector store before running this code. See the sections below for details.

```python
import os
from pathlib import Path

from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, PromptAgentDefinition
from azure.identity import DefaultAzureCredential

load_dotenv()

# Load the file to be indexed for search.
asset_file_path = (Path(__file__).parent / "../assets/product_info.md").resolve()

with (
  DefaultAzureCredential() as credential,
  AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=credential,
  ) as project_client,
  project_client.get_openai_client() as openai_client,
):
  print("Creating vector store...")
  vector_store = openai_client.vector_stores.create(name="ProductInfoStore")
  print(f"Vector store created (id: {vector_store.id})")

  print("Uploading file to vector store...")
  with asset_file_path.open("rb") as file_handle:
    vector_store_file = openai_client.vector_stores.files.upload_and_poll(
      vector_store_id=vector_store.id,
      file=file_handle,
    )
  print(f"File uploaded to vector store (id: {vector_store_file.id})")

  print("Creating agent with the file search tool...")
  agent = project_client.agents.create_version(
    agent_name="MyAgent",
    definition=PromptAgentDefinition(
      model=os.environ["MODEL_DEPLOYMENT_NAME"],
      instructions=(
        "You are a helpful agent that can search through product information. "
        "Use file search to answer questions from the uploaded files."
      ),
      tools=[FileSearchTool(vector_store_ids=[vector_store.id])],
    ),
    description="File search agent for product information queries.",
  )
  print(
    "Agent created "
    f"(id: {agent.id}, name: {agent.name}, version: {agent.version})"
  )

  print("Creating conversation...")
  conversation = openai_client.conversations.create()
  print(f"Created conversation (id: {conversation.id})")

  print("Creating response...")
  response = openai_client.responses.create(
    conversation=conversation.id,
    input="Tell me about Contoso products",
    extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
  )
  print(response.output_text)

  print("Cleaning up...")
  project_client.agents.delete_version(
    agent_name=agent.name,
    agent_version=agent.version,
  )
  openai_client.vector_stores.delete(vector_store.id)
```

### Expected output

The following output comes from the preceding code sample:

```console
Creating vector store...
Vector store created (id: vs_abc123)
Uploading file to vector store...
File uploaded to vector store (id: file-xyz789)
Creating agent with the file search tool...
Agent created (id: agent_001, name: MyAgent, version: 1)
Creating conversation...
Created conversation (id: conv_456)
Creating response...
[Response text grounded in your uploaded document content]
Cleaning up...
```

### References

- Reference: [Azure SDK for Python sample: file search](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search_in_stream.py)
- Reference: [Agents REST API (preview)](../../../../reference/foundry-project-rest-preview.md)
:::zone-end
:::zone pivot="csharp"
## File search sample with agent

In this example, you create a local file, upload it to Azure, and use it in the newly created `VectorStore` for file search.  The code in this example is synchronous and streaming. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample8_FileSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
// Create project client and read the environment variables, which is used in the next steps.
var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

// Create a toy example file and upload it using OpenAI mechanism.
string filePath = "sample_file_for_upload.txt";
File.WriteAllText(
    path: filePath,
    contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
OpenAIFileClient fileClient = projectClient.OpenAI.GetOpenAIFileClient();
OpenAIFile uploadedFile = fileClient.UploadFile(filePath: filePath, purpose: FileUploadPurpose.Assistants);
File.Delete(filePath);

// Create the VectorStore and provide it with uploaded file ID.
VectorStoreClient vctStoreClient = projectClient.OpenAI.GetVectorStoreClient();
VectorStoreCreationOptions options = new()
{
    Name = "MySampleStore",
    FileIds = { uploadedFile.Id }
};
VectorStore vectorStore = vctStoreClient.CreateVectorStore(options: options);

// Create an Agent capable of using File search.
PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
{
    Instructions = "You are a helpful agent that can help fetch data from files you know about.",
    Tools = { ResponseTool.CreateFileSearchTool(vectorStoreIds: new[] { vectorStore.Id }), }
};
AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
    agentName: "myAgent",
    options: new(agentDefinition));

// Ask a question about the file's contents.
ProjectResponsesClient responseClient = projectClient.OpenAI.GetProjectResponsesClientForAgent(agentVersion.Name);

ResponseResult response = responseClient.CreateResponse("Can you give me the documented codes for 'banana' and 'orange'?");

// Create the response and throw an exception if the response contains the error.
Assert.That(response.Status, Is.EqualTo(ResponseStatus.Completed));
Console.WriteLine(response.GetOutputText());

// Remove all the resources created in this sample.
projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
vctStoreClient.DeleteVectorStore(vectorStoreId: vectorStore.Id);
fileClient.DeleteFile(uploadedFile.Id);
```

### Expected output

The following output comes from the preceding code sample:

```console
The code for 'banana' is 673457. I couldn't find any documented code for 'orange' in the files I have access to.
```

## File search sample with agent in streaming scenarios

In this example, you create a local file, upload it to Azure, and use it in the newly created `VectorStore` for file search. The code in this example is synchronous and streaming. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample11_FileSearch_Streaming.md) in the Azure SDK for .NET repository on GitHub.

```csharp
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
        // Create project client and read the environment variables, which will be used in the next steps.
        var projectEndpoint = System.Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
        var modelDeploymentName = System.Environment.GetEnvironmentVariable("MODEL_DEPLOYMENT_NAME");
        AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: new DefaultAzureCredential());

        // Create a toy example file and upload it using OpenAI mechanism.
        string filePath = "sample_file_for_upload.txt";
        File.WriteAllText(
            path: filePath,
            contents: "The word 'apple' uses the code 442345, while the word 'banana' uses the code 673457.");
        OpenAIFile uploadedFile = projectClient.OpenAI.Files.UploadFile(filePath: filePath, purpose: FileUploadPurpose.Assistants);
        File.Delete(filePath);

        // Create the `VectorStore` and provide it with uploaded file ID.
        VectorStoreCreationOptions options = new()
        {
            Name = "MySampleStore",
            FileIds = { uploadedFile.Id }
        };
        VectorStore vectorStore = projectClient.OpenAI.VectorStores.CreateVectorStore(options);

        // Create an agent capable of using File search.
        PromptAgentDefinition agentDefinition = new(model: modelDeploymentName)
        {
            Instructions = "You are a helpful agent that can help fetch data from files you know about.",
            Tools = { ResponseTool.CreateFileSearchTool(vectorStoreIds: new[] { vectorStore.Id }), }
        };
        AgentVersion agentVersion = projectClient.Agents.CreateAgentVersion(
            agentName: "myAgent",
            options: new(agentDefinition)
        );

        // Create the conversation to store responses.
        ProjectConversation conversation = projectClient.OpenAI.Conversations.CreateProjectConversation();
        CreateResponseOptions responseOptions = new()
        {
            Agent = agentVersion,
            AgentConversationId = conversation.Id,
            StreamingEnabled = true,
        };
        // Wait for the stream to complete.
        responseOptions.InputItems.Clear();
        responseOptions.InputItems.Add(ResponseItem.CreateUserMessageItem("Can you give me the documented codes for 'banana' and 'orange'?"));
        foreach (StreamingResponseUpdate streamResponse in projectClient.OpenAI.Responses.CreateResponseStreaming(responseOptions))
        {
            ParseResponse(streamResponse);
        }

        // Ask follow up question and start a new stream.
        Console.WriteLine("Demonstrating follow-up query with streaming...");
        responseOptions.InputItems.Clear();
        responseOptions.InputItems.Add(ResponseItem.CreateUserMessageItem("What was my previous question about?"));
        foreach (StreamingResponseUpdate streamResponse in projectClient.OpenAI.Responses.CreateResponseStreaming(responseOptions))
        {
            ParseResponse(streamResponse);
        }

        // Remove all the resources created in this sample.
        projectClient.Agents.DeleteAgentVersion(agentName: agentVersion.Name, agentVersion: agentVersion.Version);
        projectClient.OpenAI.VectorStores.DeleteVectorStore(vectorStoreId: vectorStore.Id);
        projectClient.OpenAI.Files.DeleteFile(uploadedFile.Id);
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

The following TypeScript sample shows how to create an agent with the file search tool enabled. You need to upload files and create a vector store before running this code. See the [File search behavior by agent setup type](#file-search-behavior-by-agent-setup-type) section below for details. For a JavaScript example, see the [sample code](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFileSearch.js) in the Azure SDK for JavaScript repository on GitHub.

```typescript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import "dotenv/config";

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";
const deploymentName = process.env["MODEL_DEPLOYMENT_NAME"] || "<model deployment name>";

export async function main(): Promise<void> {
  // Load the file to be indexed for search
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const assetFilePath = path.join(__dirname, "../assets/product_info.md");

  // Create AI Project client
  const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());
  const openAIClient = await project.getOpenAIClient();

  // Create vector store for file search
  console.log("Creating vector store...");
  const vectorStore = await openAIClient.vectorStores.create({
    name: "ProductInfoStore",
  });
  console.log(`Vector store created (id: ${vectorStore.id})`);

  // Upload file to vector store
  console.log("\nUploading file to vector store...");
  const fileStream = fs.createReadStream(assetFilePath);
  const file = await openAIClient.vectorStores.files.uploadAndPoll(vectorStore.id, fileStream);
  console.log(`File uploaded to vector store (id: ${file.id})`);

  // Create agent with file search tool
  console.log("\nCreating agent with file search tool...");
  const agent = await project.agents.createVersion("agent-file-search", {
    kind: "prompt",
    model: deploymentName,
    instructions: "You are a helpful assistant that can search through product information.",
    tools: [
      {
        type: "file_search",
        vector_store_ids: [vectorStore.id],
      },
    ],
  });
  console.log(`Agent created (id: ${agent.id}, name: ${agent.name}, version: ${agent.version})`);

  // Create a conversation for the agent interaction
  console.log("\nCreating conversation...");
  const conversation = await openAIClient.conversations.create();
  console.log(`Created conversation (id: ${conversation.id})`);

  // Send a query to search through the uploaded file
  console.log("\nGenerating response...");
  const response = await openAIClient.responses.create(
    {
      conversation: conversation.id,
      input: "Tell me about Contoso products",
    },
    {
      body: { agent: { name: agent.name, type: "agent_reference" } },
    },
  );
  console.log(`Response: ${response.output_text}`);

  // Clean up
  console.log("\nCleaning up resources...");
  await project.agents.deleteVersion(agent.name, agent.version);
  console.log("Agent deleted");

  await openAIClient.vectorStores.delete(vectorStore.id);
  console.log("Vector store deleted");
}

main().catch((err) => {
  console.error("The sample encountered an error:", err);
});
```

### References

- Reference: [Azure SDK for JavaScript sample: file search](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFileSearch.js)
- Reference: [Agents REST API (preview)](../../../../reference/foundry-project-rest-preview.md)

:::zone-end

:::zone pivot="rest"
## Upload files and add them to a vector store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. Then poll the store's status until all files are out of the `in_progress` state to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

### Upload a file

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/files?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/vector_stores?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store",
    "file_ids": ["{{filesUpload.id}}"]
  }'
```

## Create an agent version and enable file search

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Test agent version description",
  "definition": {
    "kind": "prompt",
    "model": "{{model}}",
    "tools": [
      {
        "type": "file_search",
        "vector_store_ids": ["{{vectorStore.id}}"],
        "max_num_results": 20
      }
    ],
    "instructions": "You are a customer support chatbot. Use file search results from the vector store to answer questions based on the uploaded files."
  }
}'
```

## Create response with file search

```bash
curl --request POST \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
  "agent": {
    "type": "agent_reference",
    "name": "{{agentVersion.name}}",
    "version": "{{agentVersion.version}}"
  },
  "metadata": {
    "test_response": "file_search_enabled",
    "vector_store_id": "{{vectorStore.id}}"
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

Delete the agent version.

```bash
curl --request DELETE \
  --url $FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions/$AGENTVERSION_VERSION?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Delete the vector store.

```bash
curl --request DELETE \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/vector_stores/$VECTORSTORE_ID?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

Delete the file.

```bash
curl --request DELETE \
  --url $FOUNDRY_PROJECT_ENDPOINT/openai/files/$FILE_ID?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### References

- Reference: [Agents REST API (preview)](../../../../reference/foundry-project-rest-preview.md)
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
- Features and availability vary by region. See [Azure AI Foundry region support](../../../../reference/region-support.md).

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
