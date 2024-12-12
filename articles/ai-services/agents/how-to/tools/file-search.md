---
title: 'How to use Azure AI Agents file search'
titleSuffix: Azure OpenAI
description: Learn how to use Agents file search.
services: cognitive-services
manager: nitinme
ms.service: azure
ms.topic: how-to
ms.date: 11/20/2024
author: fosteramanda
ms.author: aahi
recommendations: false
zone_pivot_groups: selection-file-search
---

# Azure AI Agent Service file search tool

::: zone pivot="overview"

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


## Dependency on agent setup

### Basic agent setup
The file search tool has the same functionality as Azure OpenAI Assistants. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage 
- A vector store is created using a Microsoft managed search resource 

### Standard agent setup
The file search tool uses the Azure AI Search and Azure Blob Storage resources you connected during agent setup. 
- Uploaded files get stored in your connected Azure Blob Storage account 
- Vector stores get created using your connected Azure AI Search resource 
<br> </br>

For both agent setups, OpenAI handles the entire ingestion process, including automatically parsing and chunking documents, generating and storing embeddings, and utilizing both vector and keyword searches to retrieve relevant content for user queries. 

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
* By deleting the underlying file object (which removes the file it from all vector_store and code_interpreter configurations across all agents and threads in your organization)

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector_store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the vector store object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the thread's vector store contains files that are still being processed. This is to ensure that any files your users upload in a thread a fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

::: zone-end

::: zone pivot="upload-files-code-examples"

[!INCLUDE [upload-files-code-examples](../../includes/file-search/upload-files-code-examples.md)]

::: zone-end

::: zone pivot="azure-blob-storage-code-examples"

[!INCLUDE [azure-blob-storage-code-examples](../../includes/file-search/azure-blob-storage-code-examples.md)]

::: zone-end

::: zone pivot="supported-filetypes"

### Supported file types

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

::: zone-end

::: zone pivot="deep-dive"
## Creating vector stores and adding files

You can create a vector store and add files to it in a single API call:

```python
vector_store = client.beta.vector_stores.create(
  name="Product Documentation",
  file_ids=['file_1', 'file_2', 'file_3', 'file_4', 'file_5']
)
```

Adding files to vector stores is an async operation. To ensure the operation is complete, we recommend that you use the 'create and poll' helpers in our official SDKs. If you're not using the SDKs, you can retrieve the `vector_store` object and monitor its `file_counts` property to see the result of the file ingestion operation.

Files can also be added to a vector store after it's created by creating vector store files.

```python
file = client.beta.vector_stores.files.create_and_poll(
  vector_store_id="vs_abc123",
  file_id="file-abc123"
)
```

Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

```python
batch = client.beta.vector_stores.file_batches.create_and_poll(
  vector_store_id="vs_abc123",
  file_ids=['file_1', 'file_2', 'file_3', 'file_4', 'file_5']
)
```

Similarly, these files can be removed from a vector store by either:

* Deleting the vector store file object or,
* By deleting the underlying file object (which removes the file it from all vector_store and code_interpreter configurations across all agents and threads in your organization)

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Attaching vector stores

You can attach vector stores to your agent or thread using the tool_resources parameter.

```python
assistant = client.beta.assistants.create(
  instructions="You are a helpful product support assistant and you answer questions based on the files provided to you.",
  model="gpt-4-turbo",
  tools=[{"type": "file_search"}],
  tool_resources={
    "file_search": {
      "vector_store_ids": ["vs_1"]
    }
  }
)

thread = client.beta.threads.create(
  messages=[ { "role": "user", "content": "How do I cancel my subscription?"} ],
  tool_resources={
    "file_search": {
      "vector_store_ids": ["vs_2"]
    }
  }
)
```

You can also attach a vector store to Threads or Assistants after they're created by updating them with the right `tool_resources`.


## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector_store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the `vector_store` object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the thread's vector store contains files that are still being processed. This is to ensure that any files your users upload in a thread a fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

## Managing costs with expiration policies

The `file_search` tool uses the `vector_stores` object as its resource and you will be billed based on the size of the vector_store objects created. The size of the vector store object is the sum of all the parsed chunks from your files and their corresponding embeddings.

In order to help you manage the costs associated with these vector_store objects, we have added support for expiration policies in the `vector_store` object. You can set these policies when creating or updating the `vector_store` object.

```python
vector_store = client.beta.vector_stores.create_and_poll(
  name="Product Documentation",
  file_ids=['file_1', 'file_2', 'file_3', 'file_4', 'file_5'],
  expires_after={
      "anchor": "last_active_at",
      "days": 7
  }
)
```

### Thread vector stores have default expiration policies

Vector stores created using thread helpers (like `tool_resources.file_search.vector_stores` in Threads or `message.attachments` in Messages) have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run).

When a vector store expires, the runs on that thread fail. To fix this, you can recreate a new vector_store with the same files and reattach it to the thread.

```python
all_files = list(client.beta.vector_stores.files.list("vs_expired"))

vector_store = client.beta.vector_stores.create(name="rag-store")
client.beta.threads.update(
    "thread_abc123",
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
)

for file_batch in chunked(all_files, 100):
    client.beta.vector_stores.file_batches.create_and_poll(
        vector_store_id=vector_store.id, file_ids=[file.id for file in file_batch]
    )
```
::: zone-end

