---
title: 'How to use Azure AI Agents file search'
titleSuffix: Azure OpenAI
description: Learn how to use Agents file search.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 12/11/2024
author: aahill
ms.author: aahi
ms.custom: azure-ai-agents
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

### Usage support

|Azure AI foundry support  | Python SDK |	C# SDK | JavaScript SDK | REST API | Basic agent setup | Standard agent setup |
|---------|---------|---------|---------|---------|---------|---------|
| ✔️  | ✔️ | ✔️ | ✔️ | ✔️ | File upload only | File upload and using  BYO blob storage | 

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

For both agent setups, Azure OpenAI handles the entire ingestion process, which includes:
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
* By deleting the underlying file object, which removes the file it from all vector_store and code_interpreter configurations across all agents and threads in your organization

The maximum file size is 512 MB. Each file should contain no more than 5,000,000 tokens per file (computed automatically when you attach a file).


## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector_store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the vector store object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the thread's vector store contains files that are still being processed. This is to ensure that any files your users upload in a thread are fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

## Add file search to an agent using the Azure AI Foundry portal

You can add the File Search tool to an agent programatically using the code examples listed at the top of this article, or the [Azure AI Foundry portal](https://ai.azure.com/). If you want to use the portal:

1. In the **Create and debug** screen for your agent, scroll down the **Setup** pane on the right to **knowledge**. Then select **Add**.

    :::image type="content" source="../../media/tools/knowledge-tools.png" alt-text="A screenshot showing the available tool categories in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools.png":::

1. Select **Files** and follow the prompts to add the tool. 

    :::image type="content" source="../../media/tools/knowledge-tools-list.png" alt-text="A screenshot showing the available knowledge tools in the Azure AI Foundry portal." lightbox="../../media/tools/knowledge-tools-list.png":::

    :::image type="content" source="../../media/tools/file-upload.png" alt-text="A screenshot showing the file upload page." lightbox="../../media/tools/file-upload.png":::

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

[!INCLUDE [deep-dive](../../includes/file-search/deep-dive.md)]

::: zone-end

