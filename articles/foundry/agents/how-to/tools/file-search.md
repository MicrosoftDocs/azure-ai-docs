---
title: "File search tool for Microsoft Foundry agents"
description: "Configure the file search tool for Microsoft Foundry agents. Upload files, create vector stores, and query documents with Python, C#, and REST examples."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 03/06/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions, dev-focus, pilot-ai-workflow-jan-2026, doc-kit-assisted
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

✔️ (GA) indicates general availability, ✔️ (Preview) indicates public preview, and a dash (-) indicates the feature isn't available.

| Microsoft Foundry support | Python SDK | C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ✔️ | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ (Preview) | ✔️ (GA) | ✔️ | ✔️ |

## Prerequisites

- A [basic or standard agent environment](../../../agents/environment-setup.md)
- The SDK package for your language:
  - **Python**: `azure-ai-projects` (latest)
  - **.NET**: `Azure.AI.Projects.OpenAI` (prerelease)
  - **TypeScript**: `@azure/ai-projects` (latest)
  - **Java**: `azure-ai-agents` (prerelease)
- **Storage Blob Data Contributor** role on your project's storage account (required for uploading files to your project's storage)
- **Azure AI Owner** role on your Foundry resource (required for creating agent resources)
- Azure credentials configured for authentication (such as `DefaultAzureCredential`).
- Your Foundry project endpoint URL and model deployment name.

## Code examples

The following examples show how to upload a file, create a vector store, configure an agent with file search enabled, and query the agent.

:::zone pivot="python"
## Create an agent with the file search tool

The following code sample shows how to create an agent with the file search tool enabled. You need to upload files and create a vector store before running this code. See the sections below for details.

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
- Reference: [Agents REST API (preview)](../../../reference/foundry-project-rest-preview.md)
:::zone-end

:::zone pivot="csharp"
## File search sample with agent

In this example, you create a local file, upload it to Azure, and use it in the newly created `VectorStore` for file search.  The code in this example is synchronous and streaming. For asynchronous usage, see the [sample code](https://github.com/Azure/azure-sdk-for-net/blob/feature/ai-foundry/agents-v2/sdk/ai/Azure.AI.Projects.OpenAI/samples/Sample8_FileSearch.md) in the Azure SDK for .NET repository on GitHub.

```csharp
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
using Azure.Identity;

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
var projectEndpoint = "your_project_endpoint";

// Create project client to call Foundry API
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
PromptAgentDefinition agentDefinition = new(model: "gpt-5-mini")
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
using System;
using Azure.AI.Projects;
using Azure.AI.Projects.OpenAI;
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
        PromptAgentDefinition agentDefinition = new(model: "gpt-5-mini")
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

// Format: "https://resource_name.ai.azure.com/api/projects/project_name"
const PROJECT_ENDPOINT = "your_project_endpoint";

export async function main(): Promise<void> {
  // Load the file to be indexed for search
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = path.dirname(__filename);
  const assetFilePath = path.join(__dirname, "../assets/product_info.md");

  // Create clients to call Foundry API
  const project = new AIProjectClient(PROJECT_ENDPOINT, new DefaultAzureCredential());
  const openai = project.getOpenAIClient();

  // Create vector store and upload file
  const vectorStore = await openai.vectorStores.create({
    name: "ProductInfoStore",
  });

  const fileStream = fs.createReadStream(assetFilePath);
  const file = await openai.vectorStores.files.uploadAndPoll(vectorStore.id, fileStream);

  // Create agent with file search tool
  const agent = await project.agents.createVersion("agent-file-search", {
    kind: "prompt",
    model: "gpt-5-mini",
    instructions: "You are a helpful assistant that can search through product information.",
    tools: [
      {
        type: "file_search",
        vector_store_ids: [vectorStore.id],
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
      body: { agent: { name: agent.name, type: "agent_reference" } },
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

- Reference: [Azure SDK for JavaScript sample: file search](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/ai/ai-projects/samples/v2-beta/javascript/agents/tools/agentFileSearch.js)
- Reference: [Agents REST API (preview)](../../../reference/foundry-project-rest-preview.md)

:::zone-end

:::zone pivot="java"

## Use file search in a Java agent

Add the dependency to your `pom.xml`:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-agents</artifactId>
    <version>2.0.0-beta.1</version>
</dependency>
```

### Create an agent with file search

```java
import com.azure.ai.agents.AgentsClient;
import com.azure.ai.agents.AgentsClientBuilder;
import com.azure.ai.agents.ResponsesClient;
import com.azure.ai.agents.models.AgentReference;
import com.azure.ai.agents.models.AgentVersionDetails;
import com.azure.ai.agents.models.FileSearchTool;
import com.azure.ai.agents.models.PromptAgentDefinition;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

import java.util.Arrays;
import java.util.Collections;

public class FileSearchExample {
    public static void main(String[] args) {
        // Format: "https://resource_name.ai.azure.com/api/projects/project_name"
        String projectEndpoint = "your_project_endpoint";
        String vectorStoreId = "your_vector_store_id";

        AgentsClientBuilder builder = new AgentsClientBuilder()
            .credential(new DefaultAzureCredentialBuilder().build())
            .endpoint(projectEndpoint);

        AgentsClient agentsClient = builder.buildAgentsClient();
        ResponsesClient responsesClient = builder.buildResponsesClient();

        // Create file search tool with vector store IDs
        FileSearchTool fileSearchTool = new FileSearchTool(
            Arrays.asList(vectorStoreId)
        );

        // Create agent with file search tool
        PromptAgentDefinition agentDefinition = new PromptAgentDefinition("gpt-5-mini")
            .setInstructions("You are a helpful assistant that can search through files to answer questions.")
            .setTools(Collections.singletonList(fileSearchTool));

        AgentVersionDetails agent = agentsClient.createAgentVersion("file-search-agent", agentDefinition);
        System.out.printf("Agent created: %s (version %s)%n", agent.getName(), agent.getVersion());

        // Create a response
        AgentReference agentReference = new AgentReference(agent.getName())
            .setVersion(agent.getVersion());

        Response response = responsesClient.createWithAgent(
            agentReference,
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
export AGENT_TOKEN=$(az account get-access-token --scope "https://ai.azure.com/.default" --query accessToken -o tsv)
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

## Create an agent with the file search tool

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
          "type": "file_search",
          "vector_store_ids": ["'$VECTOR_STORE_ID'"],
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
```

### References

- Reference: [Agents REST API (preview)](../../../reference/foundry-project-rest-preview.md)
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
- Features and availability vary by region. See [Azure AI Foundry region support](../../../reference/region-support.md).

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
