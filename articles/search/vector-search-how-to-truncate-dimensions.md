---
title: Truncate dimensions
titleSuffix: Azure AI Search
description: Truncate dimensions on text-embedding-3 models using Matryoshka Representation Learning (MRL) compression

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 11/19/2024
---

# Truncate dimensions using MRL compression (preview)

> [!IMPORTANT]
> This feature is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). The [preview REST API](/rest/api/searchservice/search-service-api-versions#preview-versions) supports this feature.

Exercise the ability to use fewer dimensions on text-embedding-3 models. On Azure OpenAI, text-embedding-3 models are retrained on the [Matryoshka Representation Learning (MRL)](https://arxiv.org/abs/2205.13147) technique that produces multiple vector representations at different levels of compression. This approach produces faster searches and reduced storage costs, with minimal loss of semantic information. 

In Azure AI Search, MRL support supplements [scalar and binary quantization](vector-search-how-to-quantization.md). When you use either quantization method, you can also specify a `truncationDimension` property on your vector fields to reduce the dimensionality of text embeddings. 

MRL multilevel compression saves on vector storage and improves query response times for vector queries based on text embeddings. In Azure AI Search, MRL support is only offered together with another method of quantization. Using binary quantization with MRL provides the maximum vector index size reduction. To achieve maximum storage reduction, use binary quantization with MRL, and `stored` set to false.

This feature is in preview. It's available in `2024-09-01-preview` and in beta SDK packages targeting that preview API version.

## Prerequisites

- Text-embedding-3 models such as Text-embedding-3-small or Text-embedding-3-large (text content only).

- [New vector fields](vector-search-how-to-create-index.md) of type `Edm.Half` or `Edm.Single` (you can't add MRL compression to an existing field).

- [Hierarchical Navigable Small World (HNSW)algorithm](vector-search-ranking.md) (no support for exhaustive KNN in this preview).

- [Scalar or binary quantization](vector-search-how-to-quantization.md). Truncated dimensions can be set only when scalar or binary quantization is configured. We recommend binary quantization for MRL compression.

## Supported clients

You can use the REST APIs or Azure SDK beta packages to implement MRL compression.

- [REST API 2024-09-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true) or [REST API 2024-11-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true)

- Check the change logs for each Azure SDK beta package: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [Java](https://github.com/Azure/azure-sdk-for-java/blob/azure-search-documents_11.1.3/sdk/search/azure-search-documents/CHANGELOG.md), [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md).

There's no Azure portal or Azure AI Foundry support at this time.

## How to use MRL-extended text embeddings

MRL is a capability that's built into the text embedding model you're already using. To benefit from those capabilities in Azure AI Search, follow these steps.

1. Use the [Create or Update index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true) or equivalent API to specify the index schema.

1. [Add vector fields](vector-search-how-to-create-index.md) to the index definition.

1. Specify a `vectorSearch.compressions` object in your index definition.

1. Include a quantization method, either scalar or binary (recommended).

1. Include the `truncationDimension` parameter set to 512, or as low as 256 if you use the text-embedding-3-large model.

1. Specify a vector profile that specifies the HNSW algorithm and the vector compression object.

1. Assign the vector profile to a vector field of type `Edm.Half` or `Edm.Single` in the fields collection.

There are no query-side modifications for using an MRL-capable text embedding model. Integrated vectorization, text-to-query conversions at query time, semantic ranking and other relevance enhancement features such as reranking with original vectors and oversampling are unaffected by MRL support.

Indexing is slower due to the extra steps, but queries are faster.

## Example of a vector search configuration that supports MRL

The following example illustrates a vector search configuration that meets the requirements and recommendations of MRL.

`truncationDimension` is a compression property. It specifies how much to shrink the vector graph in memory together with a compression method like scalar or binary compression. We recommend 1,024 or higher for `truncationDimension` with binary quantization. A dimensionality of less than 1,000 degrades the quality of search results when using MRL and binary compression.

```json
{ 
  "vectorSearch": { 
    "profiles": [ 
      { 
        "name": "use-bq-with-mrl", 
        "compression": "use-mrl,use-bq", 
        "algorithm": "use-hnsw" 
      } 
    ],
    "algorithms": [
       {
          "name": "use-hnsw",
          "kind": "hnsw",
          "hnswParameters": {
             "m": 4,
             "efConstruction": 400,
             "efSearch": 500,
             "metric": "cosine"
          }
       }
    ],
    "compressions": [ 
      { 
        "name": "use-mrl", 
        "kind": "truncation", 
        "rerankWithOriginalVectors": true, 
        "defaultOversampling": 10, 
        "truncationDimension": 1024
      }, 
      { 
        "name": "use-bq", 
        "kind": "binaryQuantization", 
        "rerankWithOriginalVectors": true,
        "defaultOversampling": 10
       } 
    ] 
  } 
} 
```

Here's an example of a [fully specified vector field definition](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true#searchfield) that satisfies the requirements for MRL.

Recall that vector fields must be of type `Edm.Half` or `Edm.Single`. Vector fields must have a `vectorSearchProfile` property that determines the algorithm and compression settings. Vector fields have a `dimensions` property used for specifying the number of dimensions for scoring and ranking results. Its value should be dimensions limit of the model you're using (1,536 for text-embedding-3-small).

```json
{
    "name": "text_vector",
    "type": "Collection(Edm.Single)",
    "searchable": true,
    "filterable": false,
    "retrievable": false,
    "stored": false,
    "sortable": false,
    "facetable": false,
    "key": false,
    "indexAnalyzer": null,
    "searchAnalyzer": null,
    "analyzer": null,
    "normalizer": null,
    "dimensions": 1536,
    "vectorSearchProfile": "use-bq-with-mrl",
    "vectorEncoding": null,
    "synonymMaps": []
}
```
