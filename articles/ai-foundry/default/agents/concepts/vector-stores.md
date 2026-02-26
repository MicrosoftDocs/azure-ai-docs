---
title: Vector stores for file search in Microsoft Foundry Agent Service
titleSuffix: Microsoft Foundry
description: "Learn how vector stores enable file search for agents, including ingestion (chunking and embeddings), readiness, limits, and expiration policies."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 02/04/2026
author: aahill
ms.author: aahi
ai-usage: ai-assisted
---

# Vector stores for file search

Vector store objects give the [file search](../how-to/tools/file-search.md) tool the ability to search your files. When you add a file to a vector store, the service parses, chunks, embeds, and indexes it so the tool can run both keyword and semantic search.

Vector stores can be attached to both agents and conversations. Currently, you can attach at most one vector store to an agent and at most one vector store to a conversation. For a conceptual overview of conversations, see [Agent runtime components](runtime-components.md).

In the current agents developer experience, response generation uses **responses** and **conversations**. Some SDKs and older samples use the term *run*. If you see both terms, treat *run* as response generation. For migration guidance, see [How to migrate to the new agent service](../how-to/migrate.md).

For a list of limits for vector search (such as maximum allowable file sizes), see the [quotas and limits](../concepts/limits-quotas-regions.md) article.

## Prerequisites

- A [Microsoft Foundry project](../../../how-to/create-projects.md).
- An agent or conversation that uses the [file search](../how-to/tools/file-search.md) tool.
- If you use standard agent setup, connect Azure Blob Storage and Azure AI Search during setup so your files remain in your storage. See [Agent environment setup](../../../agents/environment-setup.md).
- Roles and permissions vary by task (for example, creating projects, assigning roles for standard setup, or creating and editing agents). See the required permissions table in [Agent environment setup](../../../agents/environment-setup.md).
- Feature availability can vary by region. For current coverage, see [Microsoft Foundry feature availability across cloud regions](../../../reference/region-support.md).

## Key limits and defaults

Vector stores are often the first place retrieval workflows fail in production, so it helps to know the defaults and hard limits.

- **Files per vector store**: Each vector store can hold up to 10,000 files.
- **Attachments**: You can attach at most one vector store to an agent and at most one vector store to a conversation.
- **Default retrieval settings** (file search):
	- Chunk size: 800 tokens
	- Chunk overlap: 400 tokens
	- Embedding model: text-embedding-3-large at 256 dimensions
	- Maximum number of chunks added to context: 20

For file size and token limits, see [quotas and limits](../concepts/limits-quotas-regions.md).

## Key concepts

| Term | Meaning |
| --- | --- |
| Vector store | A container for searchable file content (chunks and embeddings) used by the file search tool. |
| Ingestion | The asynchronous process that parses, chunks, embeds, and indexes a file for search. |
| Readiness | Whether ingestion has completed and the vector store is searchable. |
| Expiration policy | A lifecycle policy that expires a vector store after a period of inactivity. |

## How vector stores work with file search

File search applies retrieval best practices to help your agent find the right content from your files. Depending on the query and your data, the tool can:

- Rewrite user queries to improve retrieval.
- Break down complex queries into multiple searches.
- Run both keyword and semantic searches across agent and conversation vector stores.
- Rerank results before adding them to the model context.

For current default retrieval settings (chunk size and overlap, embedding model, and the maximum number of chunks added to context), see [How it works](../how-to/tools/file-search.md#how-file-search-works).

## Where your data lives (basic vs standard agent setup)

Where files and search resources live depends on your agent setup:

- **Basic agent setup**: File search uses Microsoft-managed storage and search resources.
- **Standard agent setup**: File search uses the Azure Blob Storage and Azure AI Search resources you connect during setup, so your files remain in your storage.

To set up your environment, see [Agent environment setup](../../../agents/environment-setup.md). For more detail, see [Dependency on agent setup](../how-to/tools/file-search.md#file-search-behavior-by-agent-setup-type).

## Ensure vector store readiness before creating responses

Ensure all files in a vector store are fully processed before you create a response. This step ensures that all the data in your vector store is searchable.

To check readiness, use the SDK polling helpers (for example, *create-and-poll* and *upload-and-poll*) or poll the vector store object until its status is **completed**. For code examples, see [File search tool for agents](../how-to/tools/file-search.md).

During ingestion, a vector store can be in **in_progress** status. When ingestion completes, the status changes to **completed**.

As a fallback, response generation includes a 60-second maximum wait when the conversation's vector store contains files that are still being processed. This fallback wait doesn't apply to the agent's vector store.

## End-to-end workflow checklist

Use this checklist to validate a working vector-store workflow from ingestion to lifecycle management.

1. Decide whether you use basic agent setup or standard agent setup, based on where you want your files and search resources to live. See [Where your data lives (basic vs standard agent setup)](#where-your-data-lives-basic-vs-standard-agent-setup).
1. Upload your files and create a vector store. For a step-by-step example, see [Upload files and add them to a vector store](../how-to/tools/file-search.md#upload-files-and-add-them-to-a-vector-store).
1. Wait for ingestion to finish before you generate responses. Use SDK polling helpers or poll the vector store until its status is **completed** and no files remain in **in_progress**. See [Ensuring vector store readiness before creating responses](../how-to/tools/file-search.md#ensuring-vector-store-readiness-before-creating-runs).
1. Attach the vector store to the agent or conversation that you use for file search. Keep the attachment limits in mind. See [Vector stores](../how-to/tools/file-search.md#vector-stores).
1. Create a response that uses file search and verify that the tool is retrieving from the expected sources. See [Create response with file search](../how-to/tools/file-search.md#create-response-with-file-search) and [Verify results](../how-to/tools/file-search.md#verify-file-search-results).
1. Manage lifecycle: remove files you no longer need, and plan for expiration policies (especially for vector stores created by conversation helpers). See [Vector stores](../how-to/tools/file-search.md#vector-stores) and [Conversation vector stores have default expiration policies](../how-to/tools/file-search.md#conversation-vector-stores-have-default-expiration-policies).

## Add files and manage vector stores

Adding files to vector stores is an asynchronous operation. To ensure ingestion completes, use the create-and-poll helpers in the official SDKs. If you aren't using an SDK, poll the vector store until its status is **completed** and no files remain in **in_progress**.

Files can also be added to a vector store after it's created by creating vector store files. Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

When you upload a file to create a vector store, the system automatically:

1. **Chunks your content** into manageable pieces.
1. **Converts each chunk** into high-dimensional vectors using embedding models.
1. **Stores these vectors** in an optimized search index.
1. **Creates associations** between the vectors and your original content.

## Remove files from vector stores

You can remove files from a vector store in two different ways:

- Delete the vector store file object.
- Delete the underlying file object. This removes the file from all vector store configurations across all agents and conversations in your organization.

### Manage lifecycle with expiration policies

Expiration policies help you manage vector store lifecycle. You can set these policies when creating or updating the vector store object.



### Conversation vector stores have default expiration policies

Vector stores created using conversation helpers have a default expiration policy of seven days after they were last active (defined as the last time the vector store was used during response generation).

When a vector store expires, response generation for that conversation fails. To fix the issue, recreate a new vector store with the same files and reattach it to the conversation. For more detail, see [Conversation vector stores have default expiration policies](../how-to/tools/file-search.md#conversation-vector-stores-have-default-expiration-policies).

## Supported file types and key limits

For the supported file types list and encoding requirements, see [Supported file types](../how-to/tools/file-search.md#supported-file-types).

Key limits to keep in mind:

- You can attach at most one vector store to an agent and at most one vector store to a conversation.
- File size and token limits vary by feature. See [Quotas and limits](../concepts/limits-quotas-regions.md).

## Troubleshooting

- **Your vector store isn't searchable yet**: Wait for ingestion to finish. Use SDK polling helpers or poll the vector store until its status is **completed**.
- **Response generation fails after a few days**: Your conversation vector store might have expired. Recreate a new vector store with the same files and reattach it.
- **A file disappeared from multiple agents or conversations**: You might have deleted the underlying file object, which removes the file from all vector store configurations across your organization.
- **Uploads or ingestion fail**: Check file size and token limits in [Quotas and limits](../concepts/limits-quotas-regions.md).

## Next steps

- Learn more about the [file search tool](../how-to/tools/file-search.md)
- Review [tool best practices](tool-best-practice.md) for guidance on reliability and security
- Learn about [agent runtime components](runtime-components.md)
