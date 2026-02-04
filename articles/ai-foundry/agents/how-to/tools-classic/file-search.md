---
title: 'How to use Azure AI Agents file search'
titleSuffix: Microsoft Foundry
description: Learn how to use Agents file search.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 02/02/2026
author: alvinashcraft
ms.author: aashcraft
ms.custom: azure-ai-agents, references_regions
---

# Foundry Agent Service file search tool

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new file search documentation](../../../default/agents/how-to/tools/file-search.md?view=foundry&preserve-view=true).


File search augments agents with knowledge from outside its model, such as proprietary product information or documents provided by your users.  

> [!NOTE]
> Using the standard agent setup, the improved file search tool ensures your files remain in your own storage, and your Azure AI Search resource is used to ingest them, ensuring you maintain complete control over your data.   

<!-- 
> [!IMPORTANT]
> * File search has [additional charges](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) beyond the token based fees for model usage.
-->

### File sources  
- Upload local files 
- Azure Blob Storage

### Usage support

> [!NOTE]
> The file search tool is currently unavailable in the following regions:
>    * Italy north
>    * Brazil south
>    * West Europe

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | Java SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|---------|
| ✔️  | ✔️ | ✔️ | ✔️ | ✔️ |  ✔️ | File upload only | File upload and using  bring-your-own blob storage | 

## Dependency on agent setup

### Basic agent setup
The file search tool has the same functionality as Azure OpenAI Assistants. Microsoft managed search and storage resources are used. 
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

## Creating vector stores and adding files 
Adding files to vector stores is an async operation. To ensure the operation is complete, we recommend that you use the 'create and poll' helpers in our official SDKs. If you're not using the SDKs, you can retrieve the `vector_store` object and monitor its `file_counts` property to see the result of the file ingestion operation.

Files can also be added to a vector store after it's created by creating vector store files.

```python

# create a vector store with no file and wait for it to be processed
vector_store = project_client.agents.vector_stores.create_and_poll(data_sources=[], name="sample_vector_store")
print(f"Created vector store, vector store ID: {vector_store.id}")

# add the file to the vector store or you can supply file ids in the vector store creation
vector_store_file_batch = project_client.agents.vector_store_file_batches.create_and_poll(
    vector_store_id=vector_store.id, file_ids=[file.id]
)
print(f"Created vector store file batch, vector store file batch ID: {vector_store_file_batch.id}")

```

Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

```python
batch = project_client.agents.vector_store_file_batches.create_and_poll(
  vector_store_id=vector_store.id,
  file_ids=[file_1.id, file_2.id, file_3.id, file_4.id, file_5.id]
)
```

### Basic agent setup: Deleting files from vector stores
Files can be removed from a vector store by either:

* Deleting the vector store file object or,
* Deleting the underlying file object, which removes the file from all vector_store and code_interpreter configurations across all agents and threads in your organization

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Remove vector store 

You can remove a vector store from the file search tool.

```python
file_search_tool.remove_vector_store(vector_store.id)
print(f"Removed vector store from file search, vector store ID: {vector_store.id}")

project_client.agents.update_agent(
    agent_id=agent.id, tools=file_search_tool.definitions, tool_resources=file_search_tool.resources
)
print(f"Updated agent, agent ID: {agent.id}")

```

## Deleting vector stores
```python
project_client.agents.vector_stores.delete(vector_store.id)
print("Deleted vector store")
```

## Managing costs with expiration policies

For basic agent setup, the `file_search` tool uses the `vector_stores`  object as its resource and you're billed based on the size of the vector_store objects created. The size of the vector store object is the sum of all the parsed chunks from your files and their corresponding embeddings.

To help you manage the costs associated with these vector_store objects, we added support for expiration policies in the `vector_store` object. You can set these policies when creating or updating the `vector_store` object.

```python
vector_store = project_client.agents.vector_stores.create_and_poll(
  name="Product Documentation",
  file_ids=[file_1.id],
  expires_after={
      "anchor": "last_active_at",
      "days": 7
  }
)
```

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

