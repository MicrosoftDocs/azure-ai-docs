---
title: Compress vectors using quantization
titleSuffix: Azure AI Search
description: Configure built-in scalar or quantization for compressing vectors on disk and in memory.

author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 03/31/2025
---

# Compress vectors using scalar or binary quantization

Azure AI Search supports scalar and binary quantization for reducing the size of vectors in a search index. Quantization is recommended because it reduces both memory and disk storage for float16 and float32 embeddings. To offset the effects of lossy compression, you can add oversampling and rescoring.

To use built-in quantization, follow these steps:

> [!div class="checklist"]
> - Start with [vector fields and a `vectorSearch` configuration](vector-search-how-to-create-index.md) to an index
> - Add `vectorSearch.compressions`
> - Add a `scalarQuantization` or `binaryQuantization` configuration and give it a name
> - Set optional properties to mitigate the effects of lossy indexing
> - Create a new vector profile that uses the named configuration
> - Create a new vector field having the new vector profile
> - Load the index with float32 or float16 data that's quantized during indexing with the configuration you defined
> - Optionally, [query quantized data](#query-a-quantized-vector-field-using-oversampling) using the oversampling parameter. If the vector field doesn't specify oversampling in its definition, you can add it at query time.

> [!TIP]
> [Azure AI Search: Cut Vector Costs Up To 92.5% with New Compression Techniques](https://aka.ms/AISearch-cut-cost) compares compression strategies and explains savings in storage and costs. It also includes metrics for measuring relevance based on Normalized discounted cumulative gain (NDCG), demonstrating that you can compress your data without sacrificing search quality.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md), with a `vectorSearch` configuration specifying either the Hierarchical Navigable Small Worlds (HNSW) or exhaustive K-nearest neighbor (eKNN) algorithm, and a new vector profile.

## Supported quantization techniques

Quantization applies to vector fields receiving float-type vectors. In the examples in this article, the field's data type is `Collection(Edm.Single)` for incoming float32 embeddings, but float16 is also supported. When the vectors are received on a field with compression configured, the engine performs quantization to reduce the footprint of the vector data in memory and on disk.

Two types of quantization are supported:

- Scalar quantization compresses float values into narrower data types. AI Search currently supports int8, which is 8 bits, reducing vector index size fourfold.

- Binary quantization converts floats into binary bits, which takes up 1 bit. This results in up to 28 times reduced vector index size.

>[!Note]
> While free services support quantization, they don't demonstrate the full storage savings due to the limited storage quota.

## Recommended rescoring techniques

Rescoring is a technique used to offset information loss due to vector compression. It uses oversampling to pick up extra vectors, and supplemental information to rescore initial results found by the query. Supplemental information is either uncompressed original full-precision vectors - or for binary quantization only - you have the option of rescoring using the binary quantized document candidates against the query vector. Rescoring options are specified in the index, but you can invoke rescoring at query time if the index supports it.

API versions determine which rescoring behavior is operational for your code. The most recent preview API supports a new rescoring approach for binary quantization. Indexes created with `2025-03-01-preview` can use the new rescoring behaviors.

| API version | Quantization type | Rescoring properties |
|-------------|-------------------|------------------|
| [2024-07-01](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-07-01&preserve-view=true) | Scalar and binary quantization, on vector indexes built using Hierarchical Navigable Small World (HNSW) graphs for similarity search | `rerankWithOriginalVectors` |
| [2024-11-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true) | Scalar and binary quantization on HNSW graphs | `rescoringOptions.enableRescoring` and `rescoreStorageMethod.preserveOriginals` |
| [2025-03-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-03-01-preview&preserve-view=true) | Binary quantization on HNSW graphs | Previous parameter combinations are still supported but binary quantization can now be rescored if original embeddings are deleted: `rescoringOptions.enableRescoring` and `rescoringOptions.rescoreStorageMethod=discardOriginals` |

Only HNSW graphs allow rescoring. Exhaustive K Nearest Neighbors (eKNN) doesn't support rescoring.

<!-- - In version 2024-11-01-preview, set `rescoringOptions.enableRescoring` and `rescoreStorageMethod.preserveOriginals`
- In version 2025-03-01-preview, set `rescoringOptions.enableRescoring` and `rescoringOptions.rescoreStorageMethod=preserveOriginals` for scalar or binary quantization, or `rescoringOptions.enableRescoring` and `rescoringOptions.rescoreStorageMethod=discardOriginals` for binary quantization only -->

The generalized process for rescoring is:

1. The vector query executes over compressed vector fields.
1. The vector query returns the top k oversampled candidates.
1. Oversampled k candidates are rescored using either the uncompressed original vectors, or the dot product of binary quantization. 1. After rescoring, results are adjusted so that more relevant matches appear first.

## Add "compressions" to a search index

This section explains how to specify a `vectorsSearch.compressions` section in the index. The following example shows a partial index definition with a fields collection that includes a vector field.

The compression example includes both `scalarQuantization` or `binaryQuantization`. You can specify as many compression configurations as you need, and then assign the ones you want to a vector profile.

Syntax for `vectorSearch.Compressions` varies between stable and preview REST APIs, with the preview adding more options for storage optimization, plus changes to existing syntax. Backwards compatibility is preserved through internal API mappings, but we recommend adopting the newer properties in code that targets 2024-11-01-preview and future versions.

### [**2024-07-01**](#tab/2024-07-01)

Use the [Create Index](/rest/api/searchservice/indexes/create) or [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) REST API to configure compression settings.

```http
POST https://[servicename].search.windows.net/indexes?api-version=2024-07-01

{
  "name": "my-index",
  "fields": [
    { "name": "Id", "type": "Edm.String", "key": true, "retrievable": true, "searchable": true, "filterable": true },
    { "name": "content", "type": "Edm.String", "retrievable": true, "searchable": true },
    { "name": "vectorContent", "type": "Collection(Edm.Single)", "retrievable": false, "searchable": true, "dimensions": 1536,"vectorSearchProfile": "vector-profile-1"},
  ],
  "vectorSearch": {
    "profiles": [ 
      {
          "name": "vector-profile-1",
          "algorithm": "use-hnsw",
          "compression": "use-scalar"
      }
    ],
    "algorithms": [ 
      {
        "name": "use-hnsw",
        "kind": "hnsw",
        "hnswParameters": { },
        "exhaustiveKnnParameters": null
      }
    ],
    "compressions": [
      {
        "name": "use-scalar",
        "kind": "scalarQuantization",
        "scalarQuantizationParameters": {
          "quantizedDataType": "int8"
        },
        "rerankWithOriginalVectors": true,
        "defaultOversampling": 10
      },
      {
        "name": "use-binary",
        "kind": "binaryQuantization",
        "rerankWithOriginalVectors": true,
        "defaultOversampling": 10
      }
    ]
  }
}
```

**Key points**:

- `kind` must be set to `scalarQuantization` or `binaryQuantization`.

- `rerankWithOriginalVectors` uses the original uncompressed vectors to recalculate similarity and rerank the top results returned by the initial search query. The uncompressed vectors exist in the search index even if `stored` is false. This property is optional. Default is true.

- `defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, then the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

- `quantizedDataType` is optional and applies to scalar quantization only. If you add it, it must be set to `int8`. This is the only primitive data type supported for scalar quantization at this time. Default is `int8`.

### [**2024-11-01-preview**](#tab/2024-11-01-preview)

Use the [Create Index (preview)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2024-11-01-preview&preserve-view=true) or [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true) REST API to configure compression settings.

Changes in this version include new `rescoringOptions` that replace `rerankWithOriginalVectors`, and extend the API with more storage options. Notice that `defaultOversampling` is now a property of `rescoringOptions`.

Rescoring options are used to mitigate the effects of lossy comprehension. You can set `rescoringOptions` for scalar or binary quantization.

```http
POST https://[servicename].search.windows.net/indexes?api-version=2024-11-01-preview

{
  "name": "my-index",
  "fields": [
    { "name": "Id", "type": "Edm.String", "key": true, "retrievable": true, "searchable": true, "filterable": true },
    { "name": "content", "type": "Edm.String", "retrievable": true, "searchable": true },
    { "name": "vectorContent", "type": "Collection(Edm.Single)", "retrievable": false, "searchable": true, "dimensions": 1536,"vectorSearchProfile": "vector-profile-1"},
  ],
  "vectorSearch": {
        "profiles": [ 
          {
              "name": "vector-profile-1",
              "algorithm": "use-hnsw",
              "compression": "use-scalar"
          }
        ],
        "algorithms": [ 
          {
            "name": "use-hnsw",
            "kind": "hnsw",
            "hnswParameters": { },
            "exhaustiveKnnParameters": null
          }
        ],
        "compressions": [
          {
            "name": "use-scalar",
            "kind": "scalarQuantization",
            "rescoringOptions": {
                "enableRescoring": true,
                "defaultOversampling": 10,
                "rescoreStorageMethod": "preserveOriginals"
            },
            "scalarQuantizationParameters": {
              "quantizedDataType": "int8"
            },
            "truncationDimension": 1024
          },
          {
            "name": "use-binary",
            "kind": "binaryQuantization",
            "rescoringOptions": {
                "enableRescoring": true,
                "defaultOversampling": 10,
                "rescoreStorageMethod": "preserveOriginals"
            },
            "truncationDimension": 1024
          }
        ]
    }
}
```

**Key points**:

- `kind` must be set to `scalarQuantization` or `binaryQuantization`.

- `rescoringOptions` are a collection of properties used to offset lossy compression by rescoring query results using the original full-precision vectors that exist prior to quantization. For rescoring to work, you must have the vector instance that provides this content. Setting `rescoreStorageMethod` to `discardOriginals` prevents you from using `enableRescoring` or `defaultOversampling`. For more information about vector storage, see [Eliminate optional vector instances from storage](vector-search-how-to-storage-options.md).

- `"rescoreStorageMethod": "preserveOriginals"` is the API equivalent of `"rerankWithOriginalVectors": true`. Rescoring vector search results with the original full-precision vectors can result in adjustments to search score and rankings, promoting the more relevant matches as determined by the rescoring step.

- `defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, then the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

- `quantizedDataType` is optional and applies to scalar quantization only. If you add it, it must be set to `int8`. This is the only primitive data type supported for scalar quantization at this time. Default is `int8`.

- `truncationDimension` is a preview feature that taps inherent capabilities of the text-embedding-3 models to "encode information at different granularities and allows a single embedding to adapt to the computational constraints of downstream tasks" (see [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)). You can use truncated dimensions with or without rescoring options. For more information about how this feature is implemented in Azure AI Search, see [Truncate dimensions using MRL compression](vector-search-how-to-truncate-dimensions.md).

### [**2025-03-01-preview**](#tab/2025-03-01-preview)

Use the [Create Index (preview)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2025-031-01-preview&preserve-view=true) or [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-03-01-preview&preserve-view=true) REST API to configure compression settings.

Changes in this version include new guidance for *binary quantization*. If you set `enableRescoring` to true, you can set `rescoreStorageMethod` to `discardOriginals` to further reduce storage, without reducing quality. 

Azure AI Search supports a lossy rescoring option on the binary quantized document vectors, which helps close the quality gap between no rescoring and full-precision rescoring when using `binaryQuantization`.

For scalar quantization, there are no rescoring changes in this preview.

```http
POST https://[servicename].search.windows.net/indexes?api-version=2025-03-01-preview

{
  "name": "my-index",
  "fields": [
    { "name": "Id", "type": "Edm.String", "key": true, "retrievable": true, "searchable": true, "filterable": true },
    { "name": "content", "type": "Edm.String", "retrievable": true, "searchable": true },
    { "name": "vectorContent", "type": "Collection(Edm.Single)", "retrievable": false, "searchable": true, "dimensions": 1536,"vectorSearchProfile": "vector-profile-1"},
  ],
  "vectorSearch": {
        "profiles": [ 
          {
              "name": "vector-profile-1",
              "algorithm": "use-hnsw",
              "compression": "use-binary"
          }
        ],
        "algorithms": [ 
          {
            "name": "use-hnsw",
            "kind": "hnsw",
            "hnswParameters": { },
            "exhaustiveKnnParameters": null
          }
        ],
        "compressions": [
          {
            "name": "use-scalar",
            "kind": "scalarQuantization",
            "rescoringOptions": {
                "enableRescoring": true,
                "defaultOversampling": 10,
                "rescoreStorageMethod": "preserveOriginals"
            },
            "scalarQuantizationParameters": {
              "quantizedDataType": "int8"
            },
            "truncationDimension": 1024
          },
          {
            "name": "use-binary",
            "kind": "binaryQuantization",
            "rescoringOptions": {
                "enableRescoring": true,
                "defaultOversampling": 10,
                "rescoreStorageMethod": "discardOriginals"
            },
            "truncationDimension": 1024
          }
        ]
    }
}
```

**Key points**:

- `kind` must be set to `scalarQuantization` or `binaryQuantization`.

- `rescoringOptions` are a collection of properties used to offset lossy compression by rescoring query results using the original full-precision vectors that exist prior to quantization.

- `enableRescoring` rescores the initial results obtained by query execution over compressed data. For scalar quantization, rescoring uses uncompressed vectors to produce more relevant results and takes a dependency on `preserveOriginals`. For binary quantization, rescoring is the same as scalar quantization if you preserve originals, but you can also discard originals and still get rescoring. In this scenario, rescoring is calculated by the dot product of the full precision query and binary quantized data in the index.  

- `"rescoreStorageMethod": "discardOriginals"` removes original vectors. These aren't needed for binary quantization.

- `defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, then the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

- `truncationDimension` is a preview feature that taps inherent capabilities of the text-embedding-3 models to "encode information at different granularities and allows a single embedding to adapt to the computational constraints of downstream tasks" (see [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147)). You can use truncated dimensions with or without rescoring options. For more information about how this feature is implemented in Azure AI Search, see [Truncate dimensions using MRL compression](vector-search-how-to-truncate-dimensions.md).

---

## Add the vector search algorithm

You can use HNSW algorithm or exhaustive KNN in the 2024-11-01-preview REST API or later. For the stable version, use HNSW only. If you want rescoring, you must choose HNSW.

   ```json
   "vectorSearch": {
       "profiles": [ ],
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
        "compressions": [ <see previous section>] 
   }
   ```

## Create and assign a new vector profile

To use a new quantization configuration, you must create a *new* vector profile. Creation of a new vector profile is necessary for building compressed indexes in memory. Your new profile uses HNSW.

1. In the same index definition, create a new vector profile and add a compression property and an algorithm. Here are two profiles, one for each quantization approach.

   ```json
   "vectorSearch": {
       "profiles": [
          {
             "name": "vector-profile-hnsw-scalar",
             "compression": "use-scalar", 
             "algorithm": "use-hnsw",
             "vectorizer": null
          },
          {
             "name": "vector-profile-hnsw-binary",
             "compression": "use-binary", 
             "algorithm": "use-hnsw",
             "vectorizer": null
          }
        ],
        "algorithms": [  <see previous section> ],
        "compressions": [ <see previous section> ] 
   }
   ```

1. Assign a vector profile to a *new* vector field. The data type of the field is either float32 or float16.

   In Azure AI Search, the Entity Data Model (EDM) equivalents of float32 and float16 types are `Collection(Edm.Single)` and `Collection(Edm.Half)`, respectively.

   ```json
   {
      "name": "vectorContent",
      "type": "Collection(Edm.Single)",
      "searchable": true,
      "retrievable": true,
      "dimensions": 1536,
      "vectorSearchProfile": "vector-profile-hnsw-scalar",
   }
   ```

1. [Load the index](search-what-is-data-import.md) using indexers for pull model indexing, or APIs for push model indexing.

## How scalar quantization works in Azure AI Search

Scalar quantization reduces the resolution of each number within each vector embedding. Instead of describing each number as a 16-bit or 32-bit floating point number, it uses an 8-bit integer. It identifies a range of numbers (typically 99th percentile minimum and maximum) and divides them into a finite number of levels or bin, assigning each bin an identifier. In 8-bit scalar quantization, there are 2^8, or 256, possible bins.

Each component of the vector is mapped to the closest representative value within this set of quantization levels in a process akin to rounding a real number to the nearest integer. In the quantized 8-bit vector, the identifier number stands in place of the original value. After quantization, each vector is represented by an array of identifiers for the bins to which its components belong. These quantized vectors require much fewer bits to store compared to the original vector, thus reducing storage requirements and memory footprint.

## How binary quantization works in Azure AI Search

Binary quantization compresses high-dimensional vectors by representing each component as a single bit, either 0 or 1. This method drastically reduces the memory footprint and accelerates vector comparison operations, which are crucial for search and retrieval tasks. Benchmark tests show up to 96% reduction in vector index size.

It's particularly effective for embeddings with dimensions greater than 1024. For smaller dimensions, we recommend testing the quality of binary quantization, or trying scalar instead. Additionally, we’ve found binary quantization performs very well when embeddings are centered around zero. Most popular embedding models such as OpenAI, Cohere, and Mistral are centered around zero.

## Query a quantized vector field using oversampling

Query syntax for a compressed or quantized vector field is the same as for noncompressed vector fields, unless you want to override parameters associated with oversampling and rescoring. You can add an o`versampling` parameter to invoke oversampling and rescoring at query time.

### [**2024-07-01**](#tab/query-2024-07-01)

Recall that the [vector compression definition](vector-search-how-to-quantization.md) in the index has settings for `rerankWithOriginalVectors` and `defaultOversampling` to mitigate the effects of lossy compression. You can override the default values to vary the behavior at query time. For example, if `defaultOversampling` is 10.0, you can change it to something else in the query request.

You can set the oversampling parameter even if the index doesn't explicitly have a `rerankWithOriginalVectors` or `defaultOversampling` definition. Providing `oversampling` at query time overrides the index settings for that query and executes the query with an effective `rerankWithOriginalVectors` as true.

```http
POST https://[service-name].search.windows.net/indexes/demo-index/docs/search?api-version=2024-07-01

{    
    "vectorQueries": [
        {    
            "kind": "vector",    
            "vector": [8, 2, 3, 4, 3, 5, 2, 1],    
            "fields": "myvector",
            "oversampling": 12.0,
            "k": 5   
        }
  ]    
}
```

**Key points**:

- Applies to vector fields that undergo vector compression, per the vector profile assignment.

- Overrides the `defaultOversampling` value or introduces oversampling at query time, even if the index's compression configuration didn't specify oversampling or reranking options.

### [**2024-11-01-preview**](#tab/query-2024-11-01-preview)

Recall that the [vector compression definition](vector-search-how-to-quantization.md) in the index has settings for `enableRescoring`, `rescoreStorageMethod`, and `defaultOversampling` to mitigate the effects of lossy compression. You can override the default values to vary the behavior at query time. For example, if `defaultOversampling` is 10.0, you can change it to something else in the query request.

You can set the oversampling parameter even if the index doesn't explicitly have rescoring options or `defaultOversampling` definition. Providing `oversampling` at query time overrides the index settings for that query and executes the query with an effective `enableRescoring` as true.

```http
POST https://[service-name].search.windows.net/indexes/demo-index/docs/search?api-version=2024-11-01-preview

{    
    "vectorQueries": [
        {    
            "kind": "vector",    
            "vector": [8, 2, 3, 4, 3, 5, 2, 1],    
            "fields": "myvector",
            "oversampling": 12.0,
            "k": 5   
        }
  ]    
}
```

**Key points**:

- Oversampling applies to vector fields that undergo vector compression, per the vector profile assignment.

- Oversampling in the query overrides the `defaultOversampling` value in the index, or invokes oversampling and rescoring at query time, even if the index's compression configuration didn't specify oversampling or reranking options.

### [**2025-03-01-preview**](#tab/query-2025-03-01-preview)

The latest preview API is identical to the previous preview API in terms of `vectorQueries` specification. As with the previous version, we recommend oversampling as mitigation for lossy compression.

```http
POST https://[service-name].search.windows.net/indexes/demo-index/docs/search?api-version=2025-03-01-preview

{    
    "vectorQueries": [
        {    
            "kind": "vector",    
            "vector": [8, 2, 3, 4, 3, 5, 2, 1],    
            "fields": "myvector",
            "oversampling": 12.0,
            "k": 5   
        }
  ]    
}
```

**Key points**:

- Oversampling applies to vector fields that undergo vector compression, per the vector profile assignment.

- Oversampling in the query overrides the `defaultOversampling` value in the index, or invokes oversampling and rescoring at query time, even if the index's compression configuration didn't specify oversampling or reranking options.

---
