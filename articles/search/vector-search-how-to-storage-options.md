---
title: Eliminate optional vector instances
titleSuffix: Azure AI Search
description: In vector search, configure storage to exclude optional copies of vector fields, reducing the storage requirements of vector data.

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 03/31/2025
---

# Eliminate optional vector instances from storage

Azure AI Search stores multiple copies of vector fields that are used in specific workloads. If you don't need to support a specific behavior, like returning raw vectors in a query response, you can set properties in the index that omit storage for that workload.

Removing storage is irreversible and requires reindexing if you want it back.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md), with a `vectorSearch` configuration specifying either the Hierarchical Navigable Small Worlds (HNSW) or exhaustive K-nearest neighbor (KNN) algorithm, and a new vector profile.

## How vector fields are stored

For every vector field, there are up to three copies of the vectors, each serving a different purpose:

| Instance | Usage | Controlled using |
|----------|-------|------------------|
| Source vectors received during document indexing (JSON data) | Used for incremental data refresh with `merge` or `mergeOrUpload` indexing action. Also used to return "retrievable" vectors in the query response. | `stored` property on vector fields |
| Original full-precision vectors (binary data) | Used for internal index operations and for exhaustive KNN search in older API versions. For compressed vectors, it's also used for `preserveOriginals` rescoring on an oversampled candidate set of results from ANN search. This applies to vector fields that undergo [scalar or binary quantization](vector-search-how-to-quantization.md). | `rescoringOptions.rescoreStorageMethod` property in `vectorSearch.compressions`. |
| Vectors in the [HNSW graph for Approximate Nearest Neighbors (ANN) search](vector-search-overview.md) (HNSW graph) or vectors for exhaustive K Nearest Neighbors (eKNN index) | Used for query execution. Consists of either full-precision vectors (when no compression is applied) or quantized vectors. | Essential. There are no parameters for removing this instance. |

You can set properties that permanently discard the first two instances (JSON data and binary data) from vector storage, but not the last instance.

To offset lossy compression for HNSW, you can keep the second instance (binary data) for rescoring purposes to improve ANN search quality. For eKNN, only scalar quantization is supported, and rescoring isn't an option. In newer API versions like the latest preview, the second instance isn't kept for eKNN because the third instance provides full-precision vectors in an eKNN index.

### Indexes created with 2024-11-01-preview or later API versions

For indexes created with the 2024-11-01-preview or a later API with uncompressed vector fields, the second and third instances (binary data and HNSW graph) are combined as part of our cost reduction investments, reducing overall storage. A newer generation index with consolidated vectors is functionally equivalent to older indexes, but uses less storage. Physical data structures are established on a Create Index request, so you must delete and recreate the index to realize the storage reductions.

If you choose [vector compression](vector-search-how-to-configure-compression-storage.md), AI Search compresses (quantizes) the in-memory portion of the vector index. Since memory is often a primary constraint for vector indexes, this practice allows you to store more vectors within the same search service. However, lossy compression equates to less information in the index, which can affect search quality.

To mitigate the loss in information, you can [enable "rescoring" and "oversampling" options](vector-search-how-to-quantization.md#recommended-rescoring-techniques) to help maintain quality. The effect is retrieval of a larger set of candidate documents from the compressed index, with recomputation of similarity scores using the original vectors or the dot product. For rescoring to work, original vectors must be retained in storage for certain scenarios. As a result, while quantization reduces memory usage (vector index size usage), it slightly increases storage requirements since both compressed and original vectors are stored. The extra storage is approximately equal to the size of the compressed index.

## Remove source vectors (JSON data)

The `stored` property is a boolean property on a vector field definition that determines whether storage is allocated for retrievable vector field content obtained during indexing (the source instance). The `stored` property is true by default. If you don't need raw vector content in a query response, you can save up to 50 percent storage per field by changing `stored` to false.

Considerations for setting `stored` to false:

- Because vectors aren't human readable, you can omit them from results sent to LLMs in RAG scenarios, and from results that are rendered on a search page. Keep them, however, if you're using vectors in a downstream process that consumes vector content.

- However, if your indexing strategy includes [partial document updates](search-howto-reindex.md#update-content), such as "merge" or "mergeOrUpload" on an existing document, setting `stored=false` prevents content updates to those fields during the merge. On each "merge" or "mergeOrUpload" operation to a search document, you must provide the vector fields in its entirety, along with the nonvector fields that you're updating, or the vector is dropped.

> [!IMPORTANT]
> Setting the `stored=false` attribution is irreversible. This property can only be set when you create the index and is only allowed on vector fields. Updating an existing index with new vector fields can't set this property to `false`. If you want retrievable vector content later, you must drop and rebuild the index, or create and load a new field that has the new attribution.

For new vector fields in a search index, set `stored` to false to permanently remove retrievable storage for the vector field. The following example shows a vector field definition with the `stored` property.

```http
PUT https://[service-name].search.windows.net/indexes/demo-index?api-version=2024-07-01 
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

- Applies to fields having a [vector data type](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields).

- Affects storage on disk, not memory, and it has no effect on queries. Query execution uses a separate vector index that's unaffected by the `stored` property because that copy of the vector is always stored.

- The `stored` property is set during index creation on vector fields and is irreversible. If you want retrievable content later, you must drop and rebuild the index, or create and load a new field that has the new attribution.

- Defaults are `stored` set to true and `retrievable` set to false. In a default configuration, a retrievable copy is stored, but it's not automatically returned in results. When `stored` is true, you can toggle `retrievable` between true and false at any time without having to rebuild an index. When `stored` is false, `retrievable` must be false and can't be changed.

## Remove full-precision vectors (binary data)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

When you compress vectors using either scalar or binary quantization, query execution is over the quantized vectors. In this case, you only need the original full-precision vectors (binary data) if you want to rescore.

If you use newer preview APIs *and* binary quantization, you can safely discard full-precision vectors because rescoring strategies now use the dot product of a binary embedding, which produces high quality search results, without having to reference full-precision vectors in the index.

The `rescoreStorageMethod` property controls whether full-precision vectors are stored. The guidance for whether to retain full-precision vectors is:

- For scalar quantization, preserve original full-precision vectors in the index because they're required for rescore.
- For binary quantization, preserve original full-precision vectors for the highest quality of rescoring, or discard full-precision vectors (requires 2025-03-01-preview) if you want to rescore based on the dot product of the binary embeddings.

Vector storage strategies have been evolving over the last several releases. Index creation date and API version determine your storage options. 

| API version | Applies to | Remove full-precision vectors |
|-------------|-------------------------------|
| 2024-07-01 and earlier | Not applicable. | There's no mechanism for removing full-precision vectors. |
| 2024-11-01-preview | Binary embeddings | Use `rescoreStorageMethod.discardOriginals` to remove full-precision vectors, but doing so prevents rescoring. `enableRescoring` must be false if originals are gone.|
| 2025-03-01-preview | Binary embeddings | Use `rescoreStorageMethod.discardOriginals` to remove full-precision vectors in the index while still retaining rescore options. In this preview, rescoring is possible because the technique changed. The dot product of the binary embeddings is used on the rescore, producing high quality search results equivalent to or better than earlier techniques based on full-precision vectors. |

Notice that scalar isn't listed in the table. If you use scalar quantization, you must retain original full-precision vectors if you want to rescore.

In `vectorSearch.compressions`, the `rescoreStorageMethod` property is set to `preserveOriginals` by default, which retains full-precision vectors for [oversampling and rescoring capabilities](vector-search-how-to-quantization.md#add-compressions-to-a-search-index) to reduce the effect of lossy compression on the HNSW graph. If you don't need full-precision vectors, you can reduce vector storage by setting `rescoreStorageMethod` to `discardOriginals`.

> [!IMPORTANT]
> Setting the `rescoreStorageMethod` property is irreversible and can adversely affect search quality, although the degree depends on the compression method and any mitigations you apply.

To set this property:

1. Use [Create Index (preview)](/rest/api/searchservice/indexes/create?view=rest-searchservice-2025-03-01-preview&preserve-view=true) or [Create or Update Index (preview)](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2025-03-01-preview&preserve-view=true) REST APIs, or an Azure SDK beta package providing the feature.

1. Add a `vectorSearch` section to your index with profiles, algorithms, and compressions.

1. Under `vectorSearch.compressions`, add `rescoringOptions` with `enableRescoring` set to true, `defaultOversampling` set to a positive integer, and `rescoreStorageMethod` set to `discardOriginals` for binary quantization and `preserveOriginals` for scalar quantization.

    ```http
    PUT https://[service-name].search.windows.net/indexes/demo-index?api-version=2025-03-01-preview
    
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
