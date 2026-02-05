---
title: What is a Knowledge Source?
titleSuffix: Azure AI Search
description: Learn about the knowledge source object used for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 02/02/2026
---

# What is a knowledge source?

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A knowledge source specifies the content used for agentic retrieval. It either encapsulates a search index populated by external data, or it's a direct connection to a remote target such as Bing or SharePoint that's queried directly. A knowledge source is a required definition in a knowledge base.

+ Create a knowledge source as a top-level resource on your search service. Each knowledge source points to exactly one data structure, either a search index that [meets the criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md) or a supported external resource.

+ Reference one or more knowledge sources in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md). In an agentic retrieval pipeline, you can query against multiple knowledge sources in a single request. Subqueries are generated for each knowledge source. Top results are returned in the retrieval response.

+ For certain knowledge sources, you can use a knowledge source definition to generate a full indexer pipeline (data source, skillset, indexer, and index) that works for agentic retrieval. Instead of creating multiple objects manually, the information in the knowledge source is used to generate all objects, including a populated, chunked, and searchable index.

Make sure you have at least one knowledge source before creating a knowledge base. The full specification of a knowledge source and a knowledge base can be found in the [preview REST API reference](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

## Working with a knowledge source

+ Creation path: first create a knowledge source, then create a knowledge base.

+ Deletion path: update or delete knowledge bases to remove references to a knowledge source, and then delete the knowledge source last.

+ A knowledge source, its index, and the knowledge base must all exist on the same search service. External content is either accessed over the public internet (Bing) or in a Microsoft tenant (remote SharePoint).

## Supported knowledge sources

In this preview, you can create the following knowledge sources:

| Kind | Indexed or remote |
|------|-------------------|
| [`"searchIndex"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#searchindexknowledgesource) wraps an existing index. | Indexed |
| [`"azureBlob"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#azureblobknowledgesource) generates an indexer pipeline that pulls from a blob container. | Indexed |
| [`"indexedOneLake"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#indexedonelakeknowledgesource) generates an indexer pipeline that pulls from a lakehouse. | Indexed |
| [`"indexedSharePoint"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#indexedsharepointknowledgesource) generates an indexer pipeline that pulls from a SharePoint site. | Indexed |
| [`"remoteSharePoint"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#remotesharepointknowledgesource) retrieves content directly from SharePoint. | Remote |
|  [`"webParameters"` API](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#webknowledgesource) retrieves real-time grounding data from Microsoft Bing. | Remote |

Indexed knowledge sources point to a target index on Azure AI Search. Query execution is local to the search engine on your search service. Keyword (full text search), vector, and hybrid query capabilities are used for retrieving data from indexed knowledge sources.

You access remote knowledge sources at query time. The agentic retrieval engine calls the retrieval APIs that are native to the platform (Bing or SharePoint APIs).

All retrieved content, whether indexed or remote, is pulled into the ranking pipeline in Azure AI Search where it's scored for relevance, merged (assuming multiple queries), reranked, and returned in the retrieval response. 

## Creating knowledge sources

Create knowledge sources as standalone objects. Then, specify them in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) within a ["knowledgeSources" array](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgesourcereference).

To create objects on a search service, you need [**Search Service Contributor** permissions](search-security-rbac.md). If you're using a knowledge source that creates an indexer pipeline, you also need **Search Index Data Contributor** permissions to load an index. Alternatively, you can [use an API admin key](search-security-api-keys.md) instead of roles.

Use the Azure portal, REST API, or an Azure SDK preview package to create a knowledge source. The following links provide instructions for creating a knowledge source:

+ [How to create a search index knowledge source (wraps an existing index)](agentic-knowledge-source-how-to-search-index.md)
+ [How to create a blob knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-blob.md)
+ [How to create a OneLake knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-onelake.md)
+ [How to create a SharePoint (indexed) knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-sharepoint-indexed.md)
+ [How to create a SharePoint (remote) knowledge source (queries SharePoint directly)](agentic-knowledge-source-how-to-sharepoint-remote.md)
+ [How to create a Web Knowledge Source resource (connects to Bing's public endpoint)](agentic-knowledge-source-how-to-web.md)

After you create the knowledge source, reference it in a knowledge base.

## Using knowledge sources

You can explicitly control knowledge source usage by setting `alwaysQuery` on the knowledge source definition or through steering instructions used during query planning. Steering instructions refer to descriptions on an index, or explicit retrieval instructions in the knowledge source, that provide guidance on when to use the index. Query planning happens when you use a low or medium [retrieval reasoning effort from the LLM](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). For a minimal reasoning effort, all knowledge sources listed in the knowledge base are in scope for every query. For low and medium, the knowledge base and the LLM can determine at query time which knowledge sources are likely to provide the best search corpus.  

Knowledge source selection logic is based on these factors:

+ Is `alwaysQuery` set? If yes, the knowledge source is always used on every query.

+ The `name` of the knowledge source.

+ The `description` of an index, assuming an indexed knowledge source.

+ The `retrievalInstructions` specified in the [retrieve action](agentic-retrieval-how-to-retrieve.md) or in the [knowledge base definition](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) provides guidance that includes or excludes a knowledge source. It's similar to a prompt. You can specify brevity, tone, and formatting as a retrieval instruction.

+ [`outputMode`](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgeretrievaloutputmode) on a knowledge base also affects query output and what goes in the response.

### Use a retrieval reasoning effort to control LLM usage

Not all solutions benefit from LLM query planning and execution. If simplicity and speed outweigh the benefits the LLM query planning and context engineering provide, specify a minimal reasoning effort to prevent LLM processing in your pipeline.

For low and medium, the level of LLM processing is either a balanced or maximal approach that improves relevance. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

> [!NOTE]
> If you used `attemptFastPath` in the previous preview, that approach is now replaced by `retrievalReasoningEffort` set to `minimal`.
