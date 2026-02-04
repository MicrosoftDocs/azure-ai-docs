---
title: Vector stores for file search in Microsoft Foundry Agent Service
titleSuffix: Microsoft Foundry
description: "Learn how vector stores enable file search for agents, including ingestion (chunking and embeddings), readiness, limits, and expiration policies."
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: concept-article
ms.date: 01/20/2026
author: aahill
ms.author: aahi
ai-usage: ai-assisted
---

# Vector stores for file search

Vector store objects give the [file search](../how-to/tools/file-search.md) tool the ability to search your files. When you add a file to a vector store, the service parses, chunks, embeds, and indexes it so the tool can run both keyword and semantic search.

Vector stores can be attached to both agents and conversations. Currently, you can attach at most one vector store to an agent and at most one vector store to a conversation. For a conceptual overview of conversations, see [Agent runtime components](runtime-components.md).

In the current agents developer experience, response generation uses **responses** and **conversations**. Some SDKs and older samples use the term *run*. If you see both terms, treat *run* as response generation. For background and migration guidance, see [How to migrate to the new agent service](../how-to/migrate.md).

For a list of limits for vector search (such as maximum allowable file sizes), see the [quotas and limits](../../../agents/quotas-limits.md) article.

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

As a fallback, response generation includes a 60-second maximum wait when the conversation's vector store contains files that are still being processed. This fallback wait doesn't apply to the agent's vector store.

## Add files and manage vector stores

Adding files to vector stores is an asynchronous operation. To ensure ingestion completes, use the create-and-poll helpers in the official SDKs. If you aren't using an SDK, retrieve the vector store object and monitor its file counts to confirm ingestion.

Files can also be added to a vector store after it's created by creating vector store files. Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

When you upload a file to create a vector store, the system automatically:

1. **Chunks your content** into manageable pieces.
1. **Converts each chunk** into high-dimensional vectors using embedding models.
1. **Stores these vectors** in an optimized search index.
1. **Creates associations** between the vectors and your original content.

## Basic agent setup: Deleting files from vector stores

If you're using a basic agent setup, files can be removed from a vector store by either:

- Deleting the vector store file object.
- Deleting the underlying file object, which removes the file from all vector store configurations across all agents and conversations in your organization.

### Managing costs with expiration policies

For the basic agent setup, Microsoft Foundry Agent Service uses vector store objects as a resource and you're billed based on the size of the vector store objects you create. The size of a vector store is the sum of all the parsed chunks from your files and their corresponding embeddings.

To help you manage the costs associated with these vector store objects, you can use expiration policies. You can set these policies when creating or updating the vector store object.

### Conversation vector stores have default expiration policies

Vector stores created using conversation helpers have a default expiration policy of seven days after they were last active (defined as the last time the vector store was used during response generation).

When a vector store expires, response generation for that conversation fails. To fix the issue, recreate a new vector store with the same files and reattach it to the conversation. For more detail, see [Conversation vector stores have default expiration policies](../how-to/tools/file-search.md#conversation-vector-stores-have-default-expiration-policies).

## Supported file types and key limits

For the supported file types list and encoding requirements, see [Supported file types](../how-to/tools/file-search.md#supported-file-types).

Key limits to keep in mind:

- You can attach at most one vector store to an agent and at most one vector store to a conversation.
- File size and token limits vary by feature. See [Quotas and limits](../../../agents/quotas-limits.md).

## Troubleshooting

- **Your vector store isn't searchable yet**: Wait for ingestion to finish. Use SDK polling helpers or poll the vector store until its status is **completed**.
- **Response generation fails after a few days**: Your conversation vector store might have expired. Recreate a new vector store with the same files and reattach it.
- **A file disappeared from multiple agents or conversations**: You might have deleted the underlying file object, which removes the file from all vector store configurations across your organization.
- **Uploads or ingestion fail**: Check file size and token limits in [Quotas and limits](../../../agents/quotas-limits.md).

## Next steps

- Learn more about the [file search tool](../how-to/tools/file-search.md)
- Review [tool best practices](tool-best-practice.md) for guidance on reliability and security
- Learn about [agent runtime components](runtime-components.md)
