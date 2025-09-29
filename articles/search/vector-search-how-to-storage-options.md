---
title: Eliminate optional vector instances
titleSuffix: Azure AI Search
description: In vector search, configure storage to exclude optional copies of vector fields, reducing the storage requirements of vector data.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 09/29/2025
---

# Eliminate optional vector instances from storage

Azure AI Search stores multiple copies of vector fields that are used in specific workloads. If your search scenarios don't require all of these copies, you can omit storage for that workload. 

Use cases where an extra copy is used include:

- Returning raw vectors in a query response or supporting incremental updates to vector content.
- Rescoring compressed (quantized) vectors as a query optimization technique.

Removing storage is irreversible and requires reindexing if you want it back.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md), with a `vectorSearch` configuration specifying either the Hierarchical Navigable Small Worlds (HNSW) or exhaustive K-Nearest Neighbor (KNN) algorithm, and a new vector profile.

## How vector fields are stored

| Instance | Usage | Required for search | How removed |
|----------|-------|---------------------|-------------|
| Vectors in the [HNSW graph for Approximate Nearest Neighbors (ANN) search](vector-search-overview.md) (HNSW graph) or vectors for exhaustive K-Nearest Neighbors (eKNN index) | Used for query execution. Consists of either full-precision vectors (when no compression is applied) or quantized vectors. | Essential | There are no parameters for removing this instance. |
| Source vectors received during document indexing (JSON data) | Used for incremental data refresh with `merge` or `mergeOrUpload` indexing actions. Also used to return "retrievable" vectors in the query response. | No | Set `stored` property to false. |
| Original full-precision vectors (binary data) <sup>1</sup> | For compressed vectors, it's used for `preserveOriginals` rescoring on an oversampled candidate set of results from ANN search. This applies to vector fields that undergo [scalar or binary quantization](vector-search-how-to-quantization.md), and it applies to queries using the HNSW graph. If you're using eKNN, all vectors are in scope for the query, so rescoring has no effect and thus not supported. | No | Set `rescoringOptions.rescoreStorageMethod` property to `discardOriginals` in `vectorSearch.compressions`. |

<sup>1</sup> This copy is also for internal index operations and for exhaustive KNN search in older API versions, on indexes created using the 2023 APIs. On newer indexes, an eKNN-configured field consists of full-precision vectors so no extra copy is needed.

## Remove source vectors (JSON data)

In a vector field definition, `stored` is a boolean property that determines whether storage is allocated for retrievable vector content obtained during indexing (the source instance). By default, `stored` is set to `true`. If you don't need raw vector content in a query response, changing `stored` to `false` can save up to 50% storage per field.

Considerations for setting `"stored": false`:

- Because vectors aren't human readable, you can generally omit them from results sent to LLMs in RAG scenarios or from results rendered on a search page. However, you should keep them if you're using vectors in a downstream process that consumes vector content.

- If your indexing strategy uses [partial document updates](search-howto-reindex.md#update-content), such as `merge` or `mergeOrUpload` on an existing document, setting `"stored": false` prevents content updates to those fields during the merge. You must include the entire vector field (and nonvector fields you're updating) in each reindexing operation. Otherwise, the vector data is lost without an error or warning. To avoid this risk altogether, set `"stored": true`.

> [!IMPORTANT]
> Setting the `"stored": false` attribution is irreversible. This property can only be set when you create the index and is only allowed on vector fields. Updating an existing index with new vector fields can't set this property to `false`. If you want retrievable vector content later, you must drop and rebuild the index or create and load a new field that has the new attribution.

For new vector fields in a search index, set `"stored": false` to permanently remove retrievable storage for the vector field. The following example shows a vector field definition with the `stored` property.

```http
PUT https://[service-name].search.windows.net/indexes/demo-index?api-version=2025-09-01@search.rerankerBoostedScore 
  Content-Type: application/json  
  api-key: [admin key]  

    { 
      "name": "demo-index", 
      "fields": [ 
        { 
          "name": "vectorContent", 
          "type": "Collection(Edm.Single)", 
          "retrievable": false, 
          "stored": false, 
          "dimensions": 1536, 
          "vectorSearchProfile": "vectorProfile" 
        } 
      ] 
    } 
```

### Summary of key points

- Applies to fields that have a [vector data type](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields).

- Affects storage on disk, not memory, and has no effect on queries. Query execution uses a separate vector index that's unaffected by the `stored` property because that copy of the vector is always stored.

- The `stored` property is set during index creation on vector fields and is irreversible. If you want retrievable content later, you must drop and rebuild the index or create and load a new field that has the new attribution.

- Defaults are `"stored": true` and `"retrievable": false`. In a default configuration, a retrievable copy is stored but isn't automatically returned in results. When `stored` is `true`, you can toggle `retrievable` between `true` and `false` at any time without having to rebuild an index. When `stored` is `false`, `retrievable` must be `false` and can't be changed.

## Remove full-precision vectors

Original full-precision vectors are used in rescoring operations over compressed (quantized) vectors. The intent of rescoring is to mitigate the loss in information due to compression. The effect of rescoring is retrieval of a larger set of candidate documents from the compressed index, with recomputation of similarity scores using the original vectors or the dot product. For rescoring to work, original vectors must be retained in storage for certain scenarios. As a result, while quantization reduces memory usage (vector index size usage), it slightly increases storage requirements since both compressed and original vectors are stored. The extra storage is approximately equal to the size of the compressed index.

Rescoring requirements by quantization approach:

- Rescoring of scalar quantized vectors requires retention of the original full-precision vectors.

- Rescoring of binary quantized vectors can use either the original full-precision vectors, or the dot product of the binary embedding, which produces high quality search results, without having to reference full-precision vectors in the index.

Rescoring recommendations:

- For scalar quantization, preserve original full-precision vectors in the index because they're required for rescore.

- For binary quantization, either preserve original full-precision vectors for the highest quality of rescoring, or discard full-precision vectors if you want to rescore based on the dot product of the binary embeddings.

The `rescoreStorageMethod` property controls whether full-precision vectors are stored. In `vectorSearch.compressions`, the `rescoreStorageMethod` property is set to `preserveOriginals` by default, which retains full-precision vectors for [oversampling and rescoring capabilities](vector-search-how-to-quantization.md#add-compressions-to-a-search-index) to reduce the effect of lossy compression on the HNSW graph. If you don't need rescoring, of if you used binary quantization and the dot product for rescoring, you can reduce vector storage by setting `rescoreStorageMethod` to `discardOriginals`.

> [!IMPORTANT]
> Setting the `rescoreStorageMethod` property is irreversible and can adversely affect search quality, although the degree depends on the compression method and any mitigations you apply.

To set this property:

1. Use [Create Index](/rest/api/searchservice/indexes/create) or [Create or Update Index](/rest/api/searchservice/indexes/create-or-update) REST APIs, or an Azure SDK.

1. Add a `vectorSearch` section to your index with profiles, algorithms, and compressions.

1. Under `vectorSearch.compressions`, add `rescoringOptions` with `enableRescoring` set to true, `defaultOversampling` set to a positive integer, and `rescoreStorageMethod` set to `discardOriginals` for binary quantization and `preserveOriginals` for scalar quantization.

    ```http
    PUT https://[service-name].search.windows.net/indexes/demo-index?api-version=2025-09-01
    
    {
        "name": "demo-index",
        "fields": [. . . ],
        . . .
        "vectorSearch": {
            "profiles": [
                {
                "name": "myVectorProfile-1",
                "algorithm": "myHnsw",
                "compression": "myScalarQuantization"
                },
                {
                "name": "myVectorProfile-2",
                "algorithm": "myHnsw",
                "compression": "myBinaryQuantization"
                }
            ],
            "algorithms": [
              {
                "name": "myHnsw",
                "kind": "hnsw",
                "hnswParameters": {
                  "metric": "cosine",
                  "m": 4,
                  "efConstruction": 400,
                  "efSearch": 500
                },
                "exhaustiveKnnParameters": null
              }
            ],
            "compressions": [
                {
                    "name": "myScalarQuantization",
                    "kind": "scalarQuantization",
                    "rescoringOptions": {
                        "enableRescoring": true,
                        "defaultOversampling": 10,
                        "rescoreStorageMethod": "preserveOriginals"
                    },
                    "scalarQuantizationParameters": {
                        "quantizedDataType": "int8"
                    },
                    "truncationDimension": null
                },
                {
                    "name": "myBinaryQuantization",
                    "kind": "binaryQuantization",
                    "rescoringOptions": {
                        "enableRescoring": true,
                        "defaultOversampling": 10,
                        "rescoreStorageMethod": "discardOriginals"
                    },
                    "truncationDimension": null
                }
            ]
        }
    }
    ```
> [!NOTE]
> Vector storage strategies have been evolving over the last several releases. Index creation date and API version determine your storage options. For example, in the 2024-11-01-preview, if you set `discardOriginals` to remove full-precision vectors, there was no rescoring for binary quantization because the dot product approach wasn't available. We recommend using the latest APIs for the best mitigation options.
