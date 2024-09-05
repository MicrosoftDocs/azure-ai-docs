---
title: 'RAG Tutorial: Search using an LLM'
titleSuffix: Azure AI Search
description: Learn how to build queries and engineer prompts for LLM-enabled search on Azure AI Search. Queries used in generative search provide the inputs to an LLM chat engine.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Search your data using a chat model (RAG tutorial - Azure AI Search)

In this tutorial, learn how to send queries and prompts to a chat model for generative search.

Objective:

- Set up clients for chat model and search engine, set up a prompt, point the model to search results.

Key points:

- You can swap out models to see which one works best for your query. No reindexing or upstream modifications required.
- Basic query (takeaway is prompt, scoping to grounding data, calling two clients)
- Basic query is hybrid for the purposes of this tutorial
- Query parent-child, one index
- Query parent-child, two indexes
- Filters

Tasks:

- H2 Set up clients and configure access (to the chat model)
- H2 Query using text, with a filter
- H2 Query using vectors and text-to-vector conversion at query time (not sure what the code looks like for this)
- H2 Query parent-child two indexes (unclear how to do this, Carey said query on child, do a lookup query on parent)

<!-- 
## Old introduction

The queries that you create for a conversational search are built for prompts and the orchestration layer. The query response is fed into message prompts sent to an LLM like GPT.

In a RAG app, the query request needs to:

- Target searchable text (vector or nonvector) in the index
- Return the most relevant results
- Return any metadata necessary for citations or other client-side requirements

A query request also specifies relevance options, which can include:

- Scoring profile
- L2 semantic reranking
- Minimum thresholds

A query request can spin off multiple query executions that execute in parallel. A hybrid query can:

- do one or more vector searches
- do keyword search
- apply filters (including geospatial)

Multiple query results are merged and ranked and returned to the client as a single result set.

## Basic query for RAG

TBD

## Add relevance features

TBD

## Hybrid query with relevance features

TBD

## Customize results

Search results are passed in messages to the LLM. This section explains refining results.

### Increase or decrease quantity

Depending on the quota of your LLM, you might want to increase or decrease the amount of information passed in messages.

TBD

### Trim results based on minimum threshold

In preview APIs, you can set a "threshhold" query parameter to exlude results having low search scores. For more information about seeting this vector query parameter, see [Create a vector query](vector-search-how-to-query.md).

### Add or remove fields

Only fields marked as "retrievable" in the search index can appear in results. If a field you want isn't already retrievable, you must drop and rebuild the index to create the physical data structures for storing retrievable data. -->

## Next step

> [!div class="nextstepaction"]
> [Maximize relevance](tutorial-rag-build-solution-relevance.md)
