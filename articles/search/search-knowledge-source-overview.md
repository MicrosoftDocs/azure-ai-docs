---
title: Create a knowledge source
titleSuffix: Azure AI Search
description: Learn how to create a knowledge source for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/29/2025
---

# Create a knowledge source

A knowledge source wraps a search index with extra properties for agentic retrieval. It's a required definition in a knowledge agent. We provide guidance on how to create specific knowledge sources, but generally, you can:

+ Create multiple knowledge sources as top-level resources on your search service.
+ Reference one or more knowledge sources in a knowledge agent. In an agentic retrieval pipeline, it's possible to query against multiple indexes in single request. Subqueries are generated for each knowledge sources. Top results are returned in the retrieval response.

Key points about a knowledge source:

+ It must exist on the same search service as the index and knowledge agent.
+ Each one points to a specific index that [meets the criteria for agentic retrieval](search-agentic-retrieval-how-to-index.md).
+ Each one specifies extra properties for query execution. The full specification is in the [REST API reference](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true).
+ A platform-specific knowledge source like the blob knowledge source includes specifications for generating an entire indexing pipeline that provides all extraction, enrichment and transformations, and a viable index.

Here are the knowledge sources you can create in this preview:

+ [Search index knowledge source](search-knowledge-source-how-to-index.md)
+ [Blob knowledge source](search-knowledge-source-how-to-blob.md)

> [!NOTE]
> `WebKnowledgeSource` (also referred to as `WebParameters` in REST APIs) isn't currently available in the 2025-08-01-preview.

Make sure you have at least one knowledge source before creating a knowledge agent.