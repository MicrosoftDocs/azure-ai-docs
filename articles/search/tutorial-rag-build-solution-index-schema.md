---
title: 'RAG Tutorial: Design an index'
titleSuffix: Azure AI Search
description: Design an index for RAG patterns in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: tutorial
ms.date: 09/12/2024

---

# Design an index (RAG tutorial - Azure AI Search)

In this tutorial, you create an index that's designed for conversational search. 

Key points:

- index contains searchable vector and text content, plus configurations
- schema for rag is designed for producing chunks of content
- schema should be flat (no complex types or structures)
- schema determines what queries you can create (be generous in attribute assignments)
- schema must cover all the queries you want to run. You can only query one index at a time (no joins), but you can create indexes that preserve parent-child relationship, and then use nested queries or parallel queries in your search logic to pull from both.
- schema has impact on storage/size. Consider narrow data types, attribution, vector configuration.
- show schemas for parent-child all-up and paired indexes via index projections
- note metadata for filters
- TBD: add fields for location and use entity recognition to pull this values out of the PDFs? Not sure how it will query, but goal would be to add some structure to the schema.

<!-- 

ps: We have another physical resource limit for our services: vector index size. HNSW requires vector indices to reside entirely in memory. "Vector index size" is our customer-facing resource limit that governs the memory consumed by their vector data. (and this is a big reason why the beefiest VMs have 512 GB of RAM). Increasing partitions also increases the amount of vector quota for customers as well. 


## Old introduction

For those of you who are already familiar with Azure AI Search, an index for RAG looks different from one designed for a "classic" search experience that returns structured results on a web page.

In conversational search, LLMs compose the response that the user sees, not the search engine, so you don't need to think about what fields to show in your search results, and whether the representation of a matching search document is coherent to the user. Depending on the question, the LLM might return verbatim content from your index, or more likely, repackage the content for a better answer.

To generate a response, LLMs operate on chunks of content, and while they need to know where the chunk came from for citation purposes, what matters most is the quality of message inputs and its relevance to the user's question. Whether the chunks come from one document or a thousand, the LLM ingests the information or *grounding data*, and formulates the response using instructions provided in a system prompt. 

A minimal index for LLM is designed to store chunks of content. It includes vector fields if you want similarity search, and nonvector fields for results. Nonvector content in the results becomes the grounding data sent to the LLM.

`sidenote: the following applies to the non-basic index, which might be out of scope`.
*A richer index has more fields and configurations, and is often better because extra fields support richer queries and more opportunities for relevance tuning. Filters and scoring profiles for boosting apply to nonvector fields. If you have content that should be matched precisely and not similarly, such as a name or employee number, then create fields to contain that information.*

## Prerequisites

TBD

## Create a basic index

1. Create an index definition with required elements. The index requires a key field ("id"). It includes vector and nonvector chunks of text. Vector content is used for similarity search. Nonvector content is returned in results and will be passed in messages to the LLM. The vector search configuration defines the algorithms used for a vector query.

```http
### Create an index for RAG scenarios
POST {{baseUrl}}/indexes?api-version=2024-05-01-preview  HTTP/1.1
  Content-Type: application/json
  Authorization: Bearer {{token}}

    {
      "name": "demo-rag-index",
      "fields": [
        { "name": "id", "type": "Edm.String", "key": true },
        { "name": "chunked_content", "type": "Edm.String", "searchable": true, "retrievable": true },
        { "name": "chunked_content_vectorized", "type": "Edm.Single", "dimensions": 1536, "vectorSearchProfile": "my-vector-profile", "searchable": true, "retrievable": false, "stored": false },
        { "name": "metadata", "type": "Edm.String", "retrievable": true, "searchable": true }
      ],
      "vectorSearch": {
         "algorithms": [
             { "name": "my-algo-config", "kind": "hnsw", "hnswParameters": { }  }
         ],
         "profiles": [ 
            { "name": "my-vector-profile", "algorithm": "my-algo-config" }
         ]
     }
    }
```

## BLOCKED: Index for hybrid queries and relevance tuning

Per Carey, you would want a couple indexes for this scenario - parent index, chunked/child index linked to parent - with queries that include lookup to access fields at the parent level. You would need index projections to "project" to coordiate the indexing of the two indexes simultaneously.

child index:
- id
- chunk
- chunkVectcor
- parentId

parent index (everything that you want "one of"):
- fields for verbatim matching (name, title, category)
- fields for filters or boosting (dates, geo coordates)

This is probably out of scope for this tutorial, but could be an extension. -->

## Next step

> [!div class="nextstepaction"]
> TBD