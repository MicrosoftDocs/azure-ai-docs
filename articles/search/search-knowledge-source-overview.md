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

+ Reference one or more knowledge sources in a knowledge agent. In an agentic retrieval pipeline, it's possible to query against multiple knowledge sources in single request. Subqueries are generated for each knowledge sources. Top results are returned in the retrieval response.

Make sure you have at least one knowledge source before creating a knowledge agent.

## Key points about a knowledge source

+ A knowledge source, its index, and the knowledge agent must all exist on the same search service.

+ Each knowledge source points to exactly one index, and that index must [meet the criteria for agentic retrieval](search-agentic-retrieval-how-to-index.md).

+ Each one specifies extra properties for query execution. The full specification is in the [REST API reference](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true). Besides the knowledge source definition itself, there are [KnowledgeSourceReference properties](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview#knowledgesourcereference&preserve-view-true) in the knowledge agent.

## Supported knowledge sources

Here are the knowledge sources you can create in this preview:

+ [Search index knowledge source (any existing index)](search-knowledge-source-how-to-index.md)
+ [Blob knowledge source](search-knowledge-source-how-to-blob.md)

A platform-specific knowledge source like the blob knowledge source includes specifications for generating an entire indexing pipeline that provides all extraction, enrichment and transformations over blob content, and a viable index. You can modify the pipeline and rerun the indexer, but you can't rename the objects.

> [!NOTE]
> `WebKnowledgeSource` (also referred to as `WebParameters` in REST APIs) isn't currently available in the 2025-08-01-preview.

## Control knowledge source usage

Properties on the knowledge agent determine whether and how the knowledge source is used. 

### Use multiple knowledge sources simultaneously

When you have multiple knowledge sources, set the following properties to bias query planning to a specific knowledge source.

+ Setting `alwaysQuerySource` forces query planning to always include the knowledge source.
+ Setting `retrievalInstructions` provides guidance that includes or excludes a knowledge source. 

Retrieval instructions are sent as a prompt to the large language model (LLM) used for query planning. This prompt is helpful when you have multiple knowledge sources and want to provide guidance on when to use each one. For example, if you have separate indexes for product information, job postings, and technical support, the retrieval instructions might say "use the jobs index only if the question is about a job application."

The `alwaysQuerySource` property overrides `retrievalInstructions`. You should set `alwaysQuerySource` to false when providing retrieval instructions.

### Attempt fast path processing

Fast path is opportunistic query processing that approaches the millisecond query performance of regular search. If you enable it, the search engine attempts fast path under the following conditions:

+ `attemptFastPath` is set to true in `knowledgeSourceReferences`.

+ The query input is a single message that's fewer than 512 characters.

+ The query target is one or more knowledge sources and each one has `alwaysQuerySource` set to true.

The small query, which executes in parallel on all compliant knowledge sources listed in the knowledge agent, returns a result if its scored 1.9 or higher. The highest scoring result is returned in the response. If no results satisfy this criteria, fast path is abandoned and query execution resumes with query planning and the usual agentic retrieval pipeline.

Under fast path, the response omits query planning information (`type": "modelQueryPlanning"`) and "activitySource" is set to 0 for each reference citation.

Under fast path, `retrievalInstructions` are ignored. In general, `alwaysQuerySource` overrides `retrievalInstructions`.

To achieve the fastest possible response times, follow these best practices:

+ Set `modality` to `answerSynthesis` to get a response framed as an LLM-formulated answer. It takes a few extra seconds, but it improves the quality of the response and saves time overall if the answer is usable without further LLM processing.

+ Retain `includeActivity` set to true (default setting) for insights about query execution and elapsed time.

+ Retain `includeReferences` set to true (default setting) for details about each individually scored result.

+ Set `includeReferenceSourceData` to false if you don't need the verbatim content from the index. Omitting this information simplifies the response and makes it more readable.
