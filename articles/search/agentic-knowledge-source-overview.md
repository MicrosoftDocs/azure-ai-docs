---
title: Create a knowledge source
titleSuffix: Azure AI Search
description: Learn how to create a knowledge source for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/09/2025
---

# Create a knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A knowledge source wraps a search index with extra properties for agentic retrieval. It's a required definition in a knowledge agent. We provide guidance on how to create specific knowledge sources, but generally, you can:

+ Create a knowledge source as top-level resources on your search service. Each knowledge source points to exactly one index, and that index must [meet the criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md).

+ Reference one or more knowledge sources in a knowledge agent. In an agentic retrieval pipeline, it's possible to query against multiple knowledge sources in single request. Subqueries are generated for each knowledge source. Top results are returned in the retrieval response.

+ Use a knowledge source definition to generate a full indexer pipeline (data source, skillset, indexer, and index) that works for agentic retrieval. Instead of creating multiple objects manually, information in the knowledge source is used to generate all objects, including a populated and searchable index.

Make sure you have at least one knowledge source before creating a knowledge agent. The full specification of a knowledge source and a knowledge agent is in the [REST API reference](/rest/api/searchservice). 

## Working with a knowledge source

+ Creation path: first create a knowledge source, then create a knowledge agent. 

+ Deletion path: update or delete knowledge agents to remove references to a knowledge source, and then delete knowledge sources last.

+ A knowledge source, its index, and the knowledge agent must all exist on the same search service.

+ For each knowledge source, the knowledge agent provides extra properties for query execution. [KnowledgeSourceReference](/rest/api/searchservice/knowledge-agents/create-or-update#knowledgesourcereference?view=rest-searchservice-2025-08-01-preview&preserve-view=true) properties affect query planning. [KnowledgeAgentOutputConfiguration](/rest/api/searchservice/knowledge-agents/create-or-update#knowledgeagentoutputconfiguration?view=rest-searchservice-2025-08-01-preview&preserve-view=true) properties affect query output.

## Supported knowledge sources

Here are the knowledge sources you can create in this preview:

+ [`"searchIndex"`](/rest/api/searchservice/knowledge-sources/create-or-update#searchindexknowledgesource?view=rest-searchservice-2025-08-01-preview&preserve-view=true) wraps an existing index
+ [`"azureBlob"`](/rest/api/searchservice/knowledge-sources/create-or-update#azureblobknowledgesource?view=rest-searchservice-2025-08-01-preview&preserve-view=true) generates an indexer pipeline that pulls from a blob container

A platform-specific knowledge source like the blob knowledge source includes specifications for generating an entire indexing pipeline that provides all extraction, enrichment and transformations over blob content, and a viable index. You can modify the pipeline and rerun the indexer, but you can't rename the objects.

> [!NOTE]
> `WebKnowledgeSource` (also referred to as `WebParameters` in REST APIs) isn't currently available in the 2025-08-01-preview.

## Create a knowledge source

You must have [permissions](search-security-rbac.md) to create objects on a search service (**Search Service Contributor**), and also permissions to load an index if you're using a knowledge source (**Search Index Data Contributor**) that creates an indexer pipeline. Alternatively, you can also [use an API admin key](search-security-api-keys.md) to create and load objects.

You must use the REST API or an Azure SDK preview package to create a knowledge source. There's no portal support at this time. The following links provide instructions for creating a knowledge source:

+ [Search index knowledge source (wraps an existing index)](agentic-knowledge-source-how-to-search-index.md)
+ [Blob knowledge source (generates an indexer pipeline)](agentic-knowledge-source-how-to-blob.md)

After the knowledge source is created, you can reference it in a knowledge agent.

## Use a knowledge source.

Properties on the *knowledge agent* determine whether and how the knowledge source is used. The [KnowledgeSourceReference](/rest/api/searchservice/knowledge-agents/create-or-update#knowledgesourcereference?view=rest-searchservice-2025-08-01-preview&preserve-view=true) array specifies the knowledge sources available to the knowledge agent.

The knowledge agent uses the [retrieve action](agentic-retrieval-how-to-retrieve.md) to send queries to the index specified in the knowledge source.

### Use multiple knowledge sources simultaneously

When you have multiple knowledge sources, set the following properties to bias query planning to a specific knowledge source.

+ Setting `alwaysQuerySource` forces query planning to always include the knowledge source.
+ Setting `retrievalInstructions` provides guidance that includes or excludes a knowledge source. 

Retrieval instructions are sent as a user-defined prompt to the large language model (LLM) used for query planning. This prompt is helpful when you have multiple knowledge sources and want to provide guidance on when to use each one. For example, if you have separate indexes for product information, job postings, and technical support, the retrieval instructions might say "use the jobs index only if the question is about a job application."

The `alwaysQuerySource` property overrides `retrievalInstructions`. Set `alwaysQuerySource` to false when providing retrieval instructions.

### Attempt fast path processing

Fast path is opportunistic query processing that approaches the millisecond query performance of regular search. If you enable it, the search engine attempts fast path under the following conditions:

+ `attemptFastPath` is set to true in `outputConfiguration`.

+ The query input is a single message that's fewer than 512 characters.

+ The query targets are the knowledge sources specified in the agent that have `alwaysQuerySource` set to true.

The small query, which executes in parallel on all compliant knowledge sources listed in the knowledge agent, returns a result if its scored 1.9 or higher. The highest scoring result is returned in the response. If no results satisfy this criteria, fast path is abandoned and query execution resumes with query planning and the usual agentic retrieval pipeline.

Under fast path, the response omits query planning information (`type": "modelQueryPlanning"`) and "activitySource" is set to 0 for each reference citation.

Under fast path, `retrievalInstructions` are ignored. In general, `alwaysQuerySource` overrides `retrievalInstructions`.

To achieve the fastest possible response times, follow these best practices:

1. In the knowledge agent:

   + Set `outputConfiguration.attemptFastPath` to true.

   + Set `outputConfiguration.modality` to `answerSynthesis` to get a response framed as an LLM-formulated answer. It takes a few extra seconds, but it improves the quality of the response and saves time overall if the answer is usable without further LLM processing.

   + Retain `outputConfiguration.includeActivity` set to true (default setting) for insights about query execution and elapsed time.

   + Retain `knowledgeSource.includeReferences` set to true (default setting) for details about each individually scored result.

   + Set `knowledgeSources.alwaysQuerySource` to true.

   + Set `knowledgeSources.retrievalInstructions` to false.

   + Set `knowledgeSources.includeReferenceSourceData` to false if you don't need the verbatim content from the index. Omitting this information simplifies the response and makes it more readable.

1. In the [retrieve action](agentic-retrieval-how-to-retrieve.md), provide a single message query that's fewer than 512 characters.

## Delete a knowledge source

Before you can delete a knowledge source, you must delete or update any knowledge agent that references it. The associated index is a standalone object in Azure AI Search and doesn't need to be deleted or updated in tandem with the knowledge source, but no references to the knowledge source can exist if you want to delete it.

If you try to delete a knowledge source that's in use, the action fails and a list of affected knowledge agents is returned.

1. Get the knowledge agent definition to confirm knowledge source references.

    ```http
    ### Get the knowledge agent
    GET {{search-endpoint}}/agents/hotels-index-ka?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

1. Either update the knowledge agent by removing the knowledge source, or delete the knowledge agent. This example shows deletion.

    ```http
    ### Delete knowledge agent
    DELETE {{search-endpoint}}/agents/hotels-index-ka?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source definition
    GET {{search-endpoint}}/knowledgeSources/hotels-index-ks?api-version=2025-08-01-preview
    api-key: {{api-key}}
    Content-Type: application/json
    ```
