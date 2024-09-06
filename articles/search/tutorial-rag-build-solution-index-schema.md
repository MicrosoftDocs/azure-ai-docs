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

An index contains searchable text and vector content, plus configurations. In a RAG pattern that uses a chat model for responses, you want an index that contains chunks of content that can be passed to an LLM at query time. 

In this tutorial, you:

> [!div class="checklist"]
> - Learn the characteristics of an index schema built for RAG
> - Create an index that accommodate vectors and hybrid queries
> - Add semantic ranking and filters
> - Add vector profiles and configurations
> - Add structured data

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

The output of this exercise is an index definition in JSON. At this point, it's not uploaded to Azure AI Search, so there are no requirements for cloud services or permissions in this exercise.

## Review schema considerations for RAG

In conversational search, LLMs compose the response that the user sees, not the search engine, so you don't need to think about what fields to show in your search results, and whether the representations of individual search documents are coherent to the user. Depending on the question, the LLM might return verbatim content from your index, or more likely, repackage the content for a better answer.

To generate a response, LLMs operate on chunks of content, and while they need to know where the chunk came from for citation purposes, what matters most is the quality of message inputs and its relevance to the user's question. Whether the chunks come from one document or a thousand, the LLM ingests the information or *grounding data*, and formulates the response using instructions provided in a system prompt. 

A minimal index for LLM is designed to store chunks of content. It includes vector fields if you want similarity search, and nonvector fields for human-readable results. Nonvector "chunked" content in the search results becomes the grounding data sent to the LLM.

A schema that works best for RAG workloads:

- Returns chunks of content in search results. 
- Search results go to an LLM, which can handle a certain level of redundancy and incomplete strings.
- Accommodates the queries you want create. You should have fields for vector and hybrid content, and those fields should be attributed to support specific query behaviors.
- Your schema should be flat (no complex types or structures).
- You can only query one index at a time (no joins), but you can create indexes that preserve parent-child relationship, and then use nested queries or parallel queries in your search logic to pull from both. This exercise includes templates for both.

Schema design has an impact on storage and costs. This exercise is focused on schema fundamentals. In the [Minimize storage and costs](tutorial-rag-build-solution-optimize.md) tutorial, we revisit schema design to consider narrow data types, attribution, and vector configurations that are more efficient.

## Create a basic index

Here's a minimal index definition for RAG solutions that supports vector and hybrid search. If you aren't using vectors, the index can be even simpler (see [Quickstart: Generative search (RAG)](search-get-started-rag.md) for an example).

1. Open Visual Studio Code and create a new file. It doesn't have to be a Python file type for this exercise.

1. Review the following example for an introduction to required elements. These elements consist of a name, key field ("id"), non-vector chunks for the LLM, vector chunks for similarity search by the search engine, and a `vectorSearch` configuration for the vector fields. 

   Vector fields have [specific types](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields) and extra attributes for embedding model dimensions and configuration. `Edm.Single` is a data type that works for the more commonly used LLMs. For more information about vector fields, see [Create a vector index](vector-search-how-to-create-index.md).

    ```json
    {
      "name": "my-demo-index",
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

1. 
<!-- Objective:

- Design an index schema that generates results in a format that works for LLMs.

Key points:

- 
- schema for rag is designed for producing chunks of content
- schema should be flat (no complex types or structures)
- schema determines what queries you can create (be generous in attribute assignments)
- schema must cover all the queries you want to run. You can only query one index at a time (no joins), but you can create indexes that preserve parent-child relationship, and then use nested queries or parallel queries in your search logic to pull from both.
- schema has impact on storage/size. Consider narrow data types, attribution, vector configuration.
- show schema patterns: one for parent-child all-up, one for paired indexes via index projections
- note metadata for filters
- TBD: add fields for location and use entity recognition to pull this values out of the PDFs? Not sure how the extraction will work on chunked documents or how it will query, but goal would be to show that you can add structured data to the schema.

Tasks:

- H2 How to create an index for chunked and vectorized data (show examples for parent-child variants)
- H2 How to define vector profiles and configuration (discuss pros and cons, shouldn't be a rehash of existing how-to)
- H2 How to add filters
- H2 How to add structured data (example is "location", top-level field, data aquisition is through the pipeline) -->

<!-- 

ps: We have another physical resource limit for our services: vector index size. HNSW requires vector indices to reside entirely in memory. "Vector index size" is our customer-facing resource limit that governs the memory consumed by their vector data. (and this is a big reason why the beefiest VMs have 512 GB of RAM). Increasing partitions also increases the amount of vector quota for customers as well. 


## Old introduction


`sidenote: the following applies to the non-basic index, which might be out of scope`.
*A richer index has more fields and configurations, and is often better because extra fields support richer queries and more opportunities for relevance tuning. Filters and scoring profiles for boosting apply to nonvector fields. If you have content that should be matched precisely and not similarly, such as a name or employee number, then create fields to contain that information.*


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
> [Create an indexing pipeline](tutorial-rag-build-solution-pipeline.md)