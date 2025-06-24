---
title: Truncate dimensions
titleSuffix: Azure AI Search
description: Truncate dimensions on text-embedding-3 models using Matryoshka Representation Learning (MRL) compression.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 06/12/2025
---

# Truncate dimensions using MRL compression (preview)

> [!IMPORTANT]
> This feature is in public preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/). We recommend the latest [preview REST API version](/rest/api/searchservice/search-service-api-versions#preview-versions) for this feature.

Exercise the ability to use fewer dimensions on text-embedding-3 models. On Azure OpenAI, text-embedding-3 models are retrained on the [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147) (MRL) technique that produces multiple vector representations at different levels of compression. This approach produces faster searches and reduced storage costs with minimal loss of semantic information.

In Azure AI Search, MRL support supplements [scalar and binary quantization](vector-search-how-to-quantization.md). When you use either quantization method, you can specify a `truncationDimension` property on your vector fields to reduce the dimensionality of text embeddings.

MRL multilevel compression saves on vector storage and improves query response times for vector queries based on text embeddings. In Azure AI Search, MRL support is only offered together with another method of quantization. Using binary quantization with MRL provides the maximum vector index size reduction. To achieve maximum storage reduction, use binary quantization with MRL and set `stored` to false.

## Prerequisites

- A text-embedding-3 model, such as text-embedding-3-small or text-embedding-3-large.

- A [supported client](#supported-clients).

- [New vector fields](vector-search-how-to-create-index.md) of type `Edm.Half` or `Edm.Single`. You can't add MRL compression to an existing field.

- [Hierarchical Navigable Small World (HNSW) algorithm](vector-search-ranking.md). This preview doesn't support exhaustive KNN.

- [Scalar or binary quantization](vector-search-how-to-quantization.md). Truncated dimensions can be set only when scalar or binary quantization is configured. We recommend binary quantization for MRL compression.

### Supported clients

You can use the REST APIs or Azure SDK beta packages to implement MRL compression. At this time, there's no Azure portal or Azure AI Foundry support.

- [REST API 2024-09-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true) or later. We recommend the latest preview API.

- Check the change logs for each Azure SDK beta package: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [Java](https://github.com/Azure/azure-sdk-for-java/blob/azure-search-documents_11.1.3/sdk/search/azure-search-documents/CHANGELOG.md), [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md).

## Use MRL-extended text embeddings

MRL is built into the text embedding model you're already using. To use MRL capabilities in Azure AI Search:

1. Use [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true) or an equivalent API to specify the index schema.

1. [Add vector fields](vector-search-how-to-create-index.md) to the index definition.

1. Specify a `vectorSearch.compressions` object in your index definition.

1. Include a quantization method, either scalar or binary (recommended).

1. Include the `truncationDimension` parameter and set it to 512. If you're using the text-embedding-3-large model, you can set it as low as 256.

1. Include a vector profile that specifies the HNSW algorithm and the vector compression object.

1. Assign the vector profile to a vector field of type `Edm.Half` or `Edm.Single` in the fields collection.

There are no query-side modifications for using an MRL-capable text embedding model. MRL support doesn't affect integrated vectorization, text-to-query conversions at query time, semantic ranking, and other relevance-enhancement features, such as reranking with original vectors and oversampling.

Although indexing is slower due to the extra steps, queries are faster.

## Example: Vector search configuration that supports MRL

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

Here's an example of a [fully specified vector field definition](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-09-01-preview&preserve-view=true#searchfield) that satisfies the requirements for MRL. Recall that vector fields must:

- Be of type `Edm.Half` or `Edm.Single`.

- Have a `vectorSearchProfile` property that specifies the algorithm and compression settings.

- Have a `dimensions` property that specifies the number of dimensions for scoring and ranking results. Its value should be the dimensions limit of the model you're using (1,536 for text-embedding-3-small).

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
