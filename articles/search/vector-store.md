---
title: Vector store database
titleSuffix: Azure AI Search
description: Describes concepts behind vector storage in Azure AI Search.

author: robertklee
ms.author: robertlee
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 06/16/2025
---

# Vector indexes in Azure AI Search

Vectors are high-dimensional embeddings that capture the underlying meaning of content, such as text or images. Azure AI Search stores vectors at the field level, allowing vector and nonvector content to coexist within the same [search index](search-what-is-an-index.md).

A search index becomes a vector index when you define vector fields, nonvector fields, and a vector configuration. You can populate vector fields by pushing precomputed embeddings into them or by using [built-in vectorization](vector-search-integrated-vectorization.md) to generate embeddings during indexing.

When it comes to vector storage, you should:

+ Design an index schema based on your intended vector retrieval pattern.
+ Estimate your index size and check your search service's capacity.
+ Manage your vector index, including updates and monitoring.
+ Secure access to your vector index.

At query time, the vector fields in your index enable similarity search, where the system retrieves documents whose vectors are most similar to the vector query. You can use [vector search](vector-search-overview.md) for semantic matching alone, or you can use [hybrid search](hybrid-search-overview.md) for a combination of semantic and keyword matching.

## Vector retrieval patterns

In Azure AI Search, there are two vector-based patterns for working with search results:

+ **Generative search.** Language models use data from Azure AI Search to respond to user queries. An orchestration layer typically coordinates prompts and maintains context, feeding search results into chat models like GPT. This pattern is based on the [retrieval-augmented generation (RAG)](retrieval-augmented-generation-overview.md) architecture, where the search index supplies grounding data.

+ **Classic search.** Users enter queries into a search bar. At query time, your application code or the search engine vectorizes the input and performs a vector search over the vector fields in your index. The search engine returns results as a flattened row set, and you can choose which fields to include in the response. The search engine matches on vectors, but you should include human-readable, nonvector fields in your index to present results to users. For more information, see [Create a vector query](vector-search-how-to-query.md) and [Create a hybrid query](hybrid-search-how-to-query.md).

Your index schema should reflect your primary use case. The following section highlights the differences in field composition for solutions built for generative AI or classic search.

## Schema of a vector store

A vector store is just a search index with vector fields. Your schema needs a name, a key field, one or more vector fields, and a vector configuration. Non-vector fields are recommended for hybrid queries or for returning readable content.

### Basic vector field configuration

A vector field is defined by its data type and vector-specific properties. For example:

```json
{
    "name": "content_vector",
    "type": "Collection(Edm.Single)",
    "searchable": true,
    "retrievable": true,
    "dimensions": 1536,
    "vectorSearchProfile": "my-vector-profile"
}
```

A vector field must be searchable and retrievable. It cannot be filterable, facetable, or sortable, and cannot use analyzers or synonym maps. The `dimensions` property must match the output of your embedding model.

### Example: basic fields for a vector index

A typical index includes a key field, one or more vector fields, and fields for readable content or metadata:

```json
"fields": [
  { "name": "id", "type": "Edm.String", "key": true },
  { "name": "content_vector", "type": "Collection(Edm.Single)", "searchable": true, "retrievable": true, "dimensions": 1536, "vectorSearchProfile": null },
  { "name": "content", "type": "Edm.String", "searchable": true, "retrievable": true },
  { "name": "metadata", "type": "Edm.String", "searchable": true, "filterable": true, "retrievable": true }
]
```

The `content` field provides the human-readable version of the vectorized content. If you only use language models for responses, you can omit non-vector content fields. If you return results directly to users, include readable content fields.

Metadata fields are useful for filtering, especially if they include source information. You cannot filter directly on a vector field, but you can filter before or after a vector query using other fields.

## Related content

+ [Create a vector store using REST APIs (Quickstart)](search-get-started-vector.md)
+ [Create a vector store](vector-search-how-to-create-index.md)
+ [Query a vector index](vector-search-how-to-query.md)
