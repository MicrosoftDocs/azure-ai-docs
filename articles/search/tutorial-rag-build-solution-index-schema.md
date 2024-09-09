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
> - Add vector profiles and configurations
> - Add structured data
> - Add filters

## Prerequisites

[Visual Studio Code](https://code.visualstudio.com/download) with the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and the [Jupyter package](https://pypi.org/project/jupyter/). For more information, see [Python in Visual Studio Code](https://code.visualstudio.com/docs/languages/python).

The output of this exercise is an index definition in JSON. At this point, it's not uploaded to Azure AI Search, so there are no requirements for cloud services or permissions in this exercise.

## Review schema considerations for RAG

In conversational search, LLMs compose the response that the user sees, not the search engine, so you don't need to think about what fields to show in your search results, and whether the representations of individual search documents are coherent to the user. Depending on the question, the LLM might return verbatim content from your index, or more likely, repackage the content for a better answer.

### Focus on chunks

To generate a response, LLMs operate on chunks of content, and while they need to know where the chunk came from for citation purposes, what matters most is the quality of message inputs and its relevance to the user's question. Whether the chunks come from one document or a thousand, the LLM ingests the information or *grounding data*, and formulates the response using instructions provided in a system prompt.

Chunks are the focus of the schema, and each chunk is the definitive element of a search document in a RAG pattern. You can think of your index as a large collection of chunks, as opposed to traditional search documents that have more structure and fields containing uniform content for a name field, versus a description field, versus a category field.

A minimal index for LLM is designed to store chunks of content. It includes vector fields if you want similarity search for highly relevant results, and nonvector fields for human-readable inputs to the LLM for conversational search. Nonvector chunked content in the search results becomes the grounding data sent to the LLM.

### Checklist of schema considerations

An index that works best for RAG workloads has these qualities:

- Returns chunks that are relevant to the query and readable to the LLM. LLMs can handle a certain level of dirty data in chunks, such as mark up, redundancy, and incomplete strings. While chunks need to be readable and relevant to the query, they don't need to be pristine.

- Maintains a parent-child relationship between chunks of a document and the properties of the parent document, such as the file name, file type, title, author, and so forth. To answer a query, chunks could be pulled from anywhere in the index. Association with the parent document providing the chunk is useful for context, citations, and follow up queries.

- Accommodates the queries you want create. You should have fields for vector and hybrid content, and those fields should be attributed to support specific query behaviors. You can only query one index at a time (no joins) so your fields collection should define all of your searchable content.

- Your schema should be flat (no complex types or structures). This requirement is specific to the RAG pattern in Azure AI Search.

Although Azure AI Search can't join indexes, you can create indexes that preserve parent-child relationship, and then use sequential or parallel queries in your search logic to pull from both. This exercise includes templates for parent-child elements in the same index and in separate indexes, where information from the parent index is retrieved using a look up query.

Schema design affects storage and costs. This exercise is focused on schema fundamentals. In the [Minimize storage and costs](tutorial-rag-build-solution-optimize.md) tutorial, we revisit schema design to consider narrow data types, attribution, and vector configurations that are more efficient.

### Sample content for this tutorial

The content you're indexing informs what fields are in the index.

In this tutorial, we use PDFs and content from the NASA Earth at Night ebook. The original ebook is large, over 100 pages and 35 MB in size. We broke it up into smaller PDFs, one per page of text, to stay under the REST API payload limit of 16 MB per API call.

We omit image vectorization for this exercise.

The sample content is descriptive and informative. It also mentions places, regions, and countries across the world. We can include skills in our indexing pipeline that extracts this information and loads it into a queryable and filterable `locations` field.

Because all of the chunks of text originate from the same parent (Earth at Night ebook), we don't need a separate index dedicated to parent fields. If we were indexing from multiple parent PDFs, we would want a parent-child index pair to capture PDF-specific fields (path, title, authors, publication date, summary) and then send look up queries to the parent index to retrieve those fields relevant to each chunk. We include an example of that parent-child index template in this exercise for comparison.

## Create a basic index

1. Open Visual Studio Code and create a new file. It doesn't have to be a Python file type for this exercise.

1. Here's a minimal index definition for RAG solutions that support vector and hybrid search. Review it for an introduction to required elements: name, fields, and a `vectorSearch` configuration for the vector fields.

    ```json
    {
      "name": "example-minimal-index",
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

   Fields must include key field (`"id"`) and should include vector chunks for similarity search, and nonvector chunks for the LLM. Metadata about the source file might be file path, creation date, or content type.

   Vector fields have [specific types](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields) and extra attributes for embedding model dimensions and configuration. `Edm.Single` is a data type that works for the more commonly used LLMs. For more information about vector fields, see [Create a vector index](vector-search-how-to-create-index.md).

1. Here's the index schema for the tutorial and the NASA ebook content. It's similar to the basic schema, but adds a parent ID and metadata. It also includes fields for storing generated content that's created in the indexing pipeline.


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

ps 1: We have another physical resource limit for our services: vector index size. HNSW requires vector indices to reside entirely in memory. "Vector index size" is our customer-facing resource limit that governs the memory consumed by their vector data. (and this is a big reason why the beefiest VMs have 512 GB of RAM). Increasing partitions also increases the amount of vector quota for customers as well. 

ps 2: A richer index has more fields and configurations, and is often better because extra fields support richer queries and more opportunities for relevance tuning. Filters and scoring profiles for boosting apply to nonvector fields. If you have content that should be matched precisely and not similarly, such as a name or employee number, then create fields to contain that information.*

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