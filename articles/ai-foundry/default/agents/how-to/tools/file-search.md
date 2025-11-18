---
title: 'How to use the file search tool for Microsoft Foundry agents'
titleSuffix: Microsoft Foundry
description: Learn how to use Agents file search tool for agents.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 09/24/2025
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents, references_regions
zone_pivot_groups: selection-file-search-upload-new
---

# File search tool for agents

File search augments agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.  

> [!NOTE]
> Using the standard agent setup, the improved file search tool ensures your files remain in your own storage, and your Azure AI Search resource is used to ingest them, ensuring you maintain complete control over your data.   

<!-- 
> [!IMPORTANT]
> * File search has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for model usage.
-->
## Prerequisites

- A [basic or standard agent environment](../../../../agents/environment-setup.md).
- The latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.
- Ensure that you have the role **Storage Blob Data Contributor** on your project's storage account.
- Ensure that you have the role **Azure AI Developer** on your project.


## Code example
> [!NOTE]
> You will need the latest prerelease package. See the [quickstart](../../../../quickstarts/get-started-code.md?view=foundry&preserve-view=true#install-and-authenticate) for details.

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, FileSearchTool

load_dotenv()

# Load the file to be indexed for search
asset_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/product_info.md"))

project_client = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()
```

## Creating vector stores and adding files 
Adding files to vector stores is an async operation. To ensure the operation is complete, we recommend that you use the 'create and poll' helpers in our official SDKs. If you're not using the SDKs, you can retrieve the `vector_store` object and monitor its `file_counts` property to see the result of the file ingestion operation.

Files can also be added to a vector store after it's created by creating vector store files.

```python

# Create vector store for file search
vector_store = openai_client.vector_stores.create(name="ProductInfoStore")
print(f"Vector store created (id: {vector_store.id})")

# Upload file to vector store
file = openai_client.vector_stores.files.upload_and_poll(
    vector_store_id=vector_store.id, file=open(asset_file_path, "rb")
)
print(f"File uploaded to vector store (id: {file.id})")
```
## Add the File Search tool to your prompt agent
```python
with project_client:
    # Create agent with file search tool
    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
            instructions="You are a helpful agent that can search through product information.",
            tools=[FileSearchTool(vector_store_ids=[vector_store.id])],
        ),
        description="File search agent for product information queries.",
    )
    print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

    # Create a conversation for the agent interaction
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")
```
### Create a conversation 
```python
# Create a conversation for the agent interaction
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Send a query to search through the uploaded file
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="Tell me about Contoso products",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    print(f"Response: {response.output_text}")
```

### Basic agent setup: Deleting files from vector stores
Files can be removed from a vector store by either:

* Deleting the vector store file object or,
* Deleting the underlying file object, which removes the file from all vector_store and code_interpreter configurations across all agents and threads in your organization

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


### Clean up

```python
    print("\nCleaning up...")

openai_client.vector_stores.delete(vector_store.id)
print("Deleted vector store")
```

## Managing costs with expiration policies

For basic agent setup, the `file_search` tool uses the `vector_stores`  object as its resource and you're billed based on the size of the vector_store objects created. The size of the vector store object is the sum of all the parsed chunks from your files and their corresponding embeddings.

To help you manage the costs associated with these vector_store objects, we added support for expiration policies in the `vector_store` object. You can set these policies when creating or updating the `vector_store` object.

```python
vector_store = openai_client.vector_stores.create_and_poll(
  name="Product Documentation",
  file_ids=[file_1.id],
  expires_after={
      "anchor": "last_active_at",
      "days": 7
  }
)
```

::: zone-end

:::zone pivot="rest"
## Upload files and add them to a vector store

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store. After creating the vector store, poll its status until all files are out of the in_progress state to ensure that all content is fully processed. The SDK provides helpers for uploading and polling.

### Upload a file

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/files?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -F purpose="assistants" \
  -F file="@c:\\path_to_file\\sample_file_for_upload.txt"
```

### Create a vector store

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/vector_stores?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my_vector_store"
    "file_ids": ["{{filesUpload.id}}"]
  }'
```


## Create an agent version and enable file search

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions?api-version=$API_VERSION \
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
    "instructions": "You are a customer support chatbot. Use your knowledge base to best respond to customer queries. When a customer asks about a specific math problem, use Python to evaluate their query."
  }
}'
```

## Create Response with File Search

```bash
curl --request POST \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/responses?api-version=$API_VERSION \
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
### clean up
delete the agent version
```bash
curl --request DELETE \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/agents/$AGENTVERSION_NAME/versions/$AGENTVERSION_VERSION?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```
delete the vector store
```bash
curl --request DELETE \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/vector_stores/$VECTORSTORE_ID?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```
delete the file
```bash
curl --request DELETE \
  --url $AZURE_AI_FOUNDRY_PROJECT_ENDPOINT/openai/files/$FILE_ID?api-version=$API_VERSION \
  -H "Authorization: Bearer $AGENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```
::: zone-end

### File sources  
- Upload local files (Basic and Standard agent setup) 
- Azure Blob Storage (Standard setup only)

## Dependency on agent setup

### Basic agent setup
The file search tool has the same functionality as Azure OpenAI Responses API. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage 
- A vector store is created using a Microsoft managed search resource 

### Standard agent setup
The file search tool uses the Azure AI Search and Azure Blob Storage resources you connected during agent setup. 
- Uploaded files get stored in your connected Azure Blob Storage account 
- Vector stores get created using your connected Azure AI Search resource 

For both agent setups, the service handles the entire ingestion process, which includes:
- Automatically parsing and chunking documents
- Generating and storing embeddings
- Utilizing both vector and keyword searches to retrieve relevant content for user queries. 

There is no difference in the code between the two setups; the only variation is in where your files and created vector stores are stored. 

## How it works
The file search tool implements several retrieval best practices out of the box to help you extract the right data from your files and augment the model’s responses. The file search tool:

* Rewrites user queries to optimize them for search.
* Breaks down complex user queries into multiple searches it can run in parallel.
* Runs both keyword and semantic searches across both agent and thread vector stores.
* Reranks search results to pick the most relevant ones before generating the final response.
* By default, the file search tool uses the following settings:
    * Chunk size: 800 tokens
    * Chunk overlap: 400 tokens
    * Embedding model: text-embedding-3-large at 256 dimensions
    * Maximum number of chunks added to context: 20

## Vector stores

Vector store objects give the file search tool the ability to search your files. Adding a file to a vector store automatically parses, chunks, embeds, and stores the file in a vector database that's capable of both keyword and semantic search. Each vector store can hold up to 10,000 files. Vector stores can be attached to both agents and threads. Currently you can attach at most one vector store to an agent and at most one vector store to a thread.


Similarly, these files can be removed from a vector store by either:

* Deleting the vector store file object or,
* By deleting the underlying file object, which removes the file from all vector_store and code_interpreter configurations across all agents and threads in your organization

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector_store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the vector store object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the thread's vector store contains files that are still being processed. This is to ensure that any files your users upload in a thread are fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

### Thread vector stores have default expiration policies

Vector stores created using thread helpers (like `tool_resources.file_search.vector_stores` in Threads or `message.attachments` in Messages) have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run).

When a vector store expires, the runs on that thread fail. To fix this issue, you can recreate a new vector_store with the same files and reattach it to the thread.

## Supported file types

> [!NOTE]
> For text/ MIME types, the encoding must be either utf-8, utf-16, or ASCII.

|File format|MIME Type|
|---|---|
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
| `.tex` |`text/x-tex` |
| `.txt` | `text/plain` |
| `.css` | `text/css` |
| `.js` | `text/javascript` |
| `.sh` | `application/x-sh` |
| `.ts` | `application/typescript` |
