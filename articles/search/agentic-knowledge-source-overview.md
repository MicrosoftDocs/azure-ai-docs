---
title: What is a knowledge source
titleSuffix: Azure AI Search
description: Learn about the knowledge source object used for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 11/10/2025
---

# What is a knowledge source?

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A knowledge source specifies the content used for agentic retrieval. It encapsulates a search index which may be populated by an external data source, or a direct connection to a remote source such as Bing or Sharepoint that is queried directly. A knowledge source is a required definition in a knowledge base.

+ Create a knowledge source as a top-level resource on your search service. Each knowledge source points to exactly one data structure, either a search index that [meets the criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md) or a supported external resource.

+ Reference one or more knowledge sources in a knowledge base. In an agentic retrieval pipeline, it's possible to query against multiple knowledge sources in a single request. Subqueries are generated for each knowledge source. Top results are returned in the retrieval response.

+ For certain knowledge sources, you can use a knowledge source definition to generate a full indexer pipeline (data source, skillset, indexer, and index) that works for agentic retrieval. Instead of creating multiple objects manually, information in the knowledge source is used to generate all objects, including a populated, chunked, and searchable index.

Make sure you have at least one knowledge source before creating a knowledge base. The full specification of a knowledge source and a knowledge base is in the [preview REST API reference](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

## Working with a knowledge source

+ Creation path: first create a knowledge source, then create a knowledge base.

+ Deletion path: update or delete knowledge bases to remove references to a knowledge source, and then delete the knowledge source last.

+ A knowledge source, its index, and the knowledge base must all exist on the same search service. External content is either accessed over the public internet (Bing) or in a Microsoft tenant (remote SharePoint).

## Supported knowledge sources

Here are the knowledge sources you can create in this preview:

+ [`"searchIndex"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchindexknowledgesource) wraps an existing index.
+ [`"azureBlob"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#azureblobknowledgesource) generates an indexer pipeline that pulls from a blob container.
+ [`"indexedOneLake"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#indexedonelakeknowledgesource) generates an indexer pipeline that pulls from a lakehouse.
+ [`"indexedSharePoint"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#indexedsharepointknowledgesource) generates an indexer pipeline that pulls from a SharePoint site.
+ [`"remoteSharePoint"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#remotesharepointknowledgesource) retrieves content directly from SharePoint.
+ [`"webParameters"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#webknowledgesource) retrieves real-time grounding data from Microsoft Bing.

## Creating knowledge sources

You must have [**Search Service Contributor** permissions](search-security-rbac.md) to create objects on a search service.  You also need **Search Index Data Contributor** permissions to load an index if you're using a knowledge source that creates an indexer pipeline. Alternatively, you can [use an API admin key](search-security-api-keys.md) instead of roles.

You can use the REST API or an Azure SDK preview package to create a knowledge source. Azure portal support is available for select knowledge sources. The following links provide instructions for creating a knowledge source:

+ [How to create a search index knowledge source (wraps an existing index)](agentic-knowledge-source-how-to-search-index.md)
+ [How to create a blob knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-blob.md)
+ [How to create a OneLake knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-onelake.md)
+ [How to create a SharePoint (indexed) knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-sharepoint-indexed.md)
+ [How to create a SharePoint (remote) knowledge source (queries SharePoint directly)](agentic-knowledge-source-how-to-sharepoint-remote.md)
+ [How to create a Web Knowledge Source resource (connects to Bing's public endpoint)](agentic-knowledge-source-how-to-web.md)

After the knowledge source is created, you can reference it in a knowledge base.

## Using knowledge sources

Properties on the [*knowledge base*](agentic-retrieval-how-to-create-knowledge-base.md) determine which knowledge sources are used.

+ ["knowledgeSources" REST](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgesourcereference) array specifies the knowledge sources available to the knowledge base.

+ ["retrievalReasoningEffort" REST](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgeretrievalreasoningeffortkind) properties determine the amount of effort put into a retrieval. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

+ ["outputMode" REST](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgeretrievaloutputmode) affects query output and what goes in the response.

The knowledge base uses the [retrieve action](agentic-retrieval-how-to-retrieve.md) to send queries to the index specified in the knowledge source. In the retrieve action, some knowledge base and source defaults can be overridden at retrieval time.

### Use multiple knowledge sources simultaneously

When you have multiple knowledge sources, set the following properties to bias query planning to a specific knowledge source.

+ Setting `alwaysQuerySource` forces query planning to always include the knowledge source.
+ Setting `retrievalInstructions` provides guidance that includes or excludes a knowledge source. 

Retrieval instructions are sent as a user-defined prompt to the large language model (LLM) used for query planning. This prompt is helpful when you have multiple knowledge sources and want to provide guidance on when to use each one. For example, if you have separate indexes for product information, job postings, and technical support, the retrieval instructions might say "use the jobs index only if the question is about a job application."

The `alwaysQuerySource` property overrides `retrievalInstructions`. Set `alwaysQuerySource` to false when providing retrieval instructions.

### Use a retrieval reasoning effort to control LLM usage

Not all solutions benefit from LLM query planning and execution. If simplicity and speed outweigh the benefits the LLM query planning and context engineering provide, you can omit the LLM from your pipeline.

The retrieval reasoning effort determines the level of processing that goes into a retrieval action. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

> [!NOTE]
> If you used `attemptFastPath` in the previous preview, that approach is now replaced with `retrievalReasoningEffort` set to `minimal`.
