---
title: Vector stores for file search in Azure AI Agent Service
titleSuffix: Microsoft Foundry
description: "Discover how vector stores in Azure AI Agent Service enable file search capabilities with automatic chunking, embedding, and semantic search for your AI agents." 
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: conceptual
ms.date: 11/18/2025
author: aahill
ms.author: aahi
---

# Vector stores for file search

Vector store objects give the [file search](../../../agents/how-to/tools/file-search.md) tool the ability to search your files. Adding a file to a vector store automatically parses, chunks, embeds, and stores the file in a vector database that's capable of both keyword and semantic search. Vector stores can be attached to both agents and conversations. Currently you can attach at most one vector store to an agent and at most one vector store to a conversation.

For a list of limits for vector search (such as maximum allowable file sizes), see the [quotas and limits](../../../agents/quotas-limits.md) article.

## Ensuring vector store readiness before creating runs

We highly recommend that you ensure all files in a vector store are fully processed before you create a run. This ensures that all the data in your vector store is searchable. You can check for vector store readiness by using the polling helpers in the SDKs, or by manually polling the vector store object to ensure the status is completed.

As a fallback, there's a 60-second maximum wait in the run object when the conversation's vector store contains files that are still being processed. This is to ensure that any files your users upload in a conversation are fully searchable before the run proceeds. This fallback wait does not apply to the agent's vector store.

## Creating vector stores and adding files

Adding files to vector stores is an async operation. To ensure the operation is complete, we recommend that you use the "create and poll" helpers in our official SDKs. If you're not using the SDKs, you can retrieve the vector store object and monitor its file counts property to see the result of the file ingestion operation.

Files can also be added to a vector store after it's created by creating vector store files. Alternatively, you can add several files to a vector store by creating batches of up to 500 files.

When you upload a file to create a vector store, the system automatically:

1. **Chunks your content** into manageable pieces
2. **Converts each chunk** into high-dimensional vectors using embedding models
3. **Stores these vectors** in an optimized search index
4. **Creates associations** between the vectors and your original content

## Basic agent setup: Deleting files from vector stores

If you're using a basic agent setup, files can be removed from a vector store by either:

* Deleting the vector store file object or,
* Deleting the underlying file object, which removes the file from all vector store configurations across all agents and conversations in your organization.

### Managing costs with expiration policies

For the basic agent setup, the Azure AI Agent Service uses vector store objects as a resource and you're billed based on the size of the vector store objects created. The size of the vector store object is the sum of all the parsed chunks from your files and their corresponding embeddings.

To help you manage the costs associated with these vector store objects, you can use expiration policies. You can set these policies when creating or updating the vector store object.

### conversation vector stores have default expiration policies

Vector stores created using helper functions have a default expiration policy of seven days after they were last active (defined as the last time the vector store was part of a run).
When a vector store expires, the runs on that conversation fail. To fix this issue, you can recreate a new vector_store with the same files and reattach it to the conversation.

## Next steps

* Learn more about the [file search tool](../../../agents/how-to/tools/file-search.md)
