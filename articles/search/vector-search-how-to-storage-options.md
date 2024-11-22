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
ms.date: 11/19/2024
---

# Eliminate optional vector instances from storage

Azure AI Search stores multiple copies of vector fields that are used in specific workloads. If you don't need to support a specific behavior, like returning raw vectors in a query response, you can set properties in the index that omit storage for that workload.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md) with a `vectorSearch` configuration, using the Hierarchical Navigable Small Worlds (HNSW) or exhaustive K-nearest neighbor (KNN) algorithms and a new vector profile.

## How vector fields are stored

For every vector field, there could be three copies of the vectors, each serving a different purpose:

| Instance | Usage | Controlled using |
|----------|-------|------------|
| Source vectors which store the JSON that was received during document indexing | Used for incremental data refresh with `merge` or `mergeOrUpload` during document indexing. Also used if you want "retrievable" vectors returned in the query response. | `stored` property on vector fields |
| Original full-precision vectors | In existing indexes, these are used for internal index operations and for exhaustive KNN search. For vectors using compression, it's also used for rescoring (if enabled) on an oversampled candidate set of results from ANN search on vector fields using [scalar or binary quantization](vector-search-how-to-quantization.md) compression. | `rescoringOptions.rescoreStorageMethod` property in `vectorSearch.compressions`. For *uncompressed* vector fields on indexes created with `2024-11-01-Preview` API versions and later, this will be omitted by default with no impact on search activities nor quality. |
| Vectors in the [HNSW graph for Approximate Nearest Neighbors (ANN) search](vector-search-overview.md) | Used for ANN query execution. Consists of either full-precision vectors (when no compression is applied) or quantized vectors (when compression is applied) | Only applies to HNSW. These data structures are required for efficient ANN search. |

You can set properties that permanently discard the first two instances from vector storage.

The last instance (vectors and graph) is required for ANN vector query execution. If any compression techniques such as [scalar or binary quantization](vector-search-how-to-quantization.md) are used, they would be applied to this set of data. If you want to offset lossy compression, you should keep the second instance for rescoring purposes to improve ANN search quality.

## Set the `stored` property

The `stored` property is a boolean property on a vector field definition that determines whether storage is allocated for retrievable vector field content (the source instance). The `stored` property is true by default. If you don't need raw vector content in a query response, you can save up to 50 percent storage per field by changing `stored` to false.

Considerations for setting `stored` to false:

- Because vectors aren't human readable, you can omit them from results sent to LLMs in RAG scenarios, and from results that are rendered on a search page. Keep them, however, if you're using vectors in a downstream process that consumes vector content.

- However, if your indexing strategy includes [partial document updates](search-howto-reindex.md#update-content), such as "merge" or "mergeOrUpload" on an existing document, setting `stored=false` prevents content updates to those fields during the merge. On each "merge" or "mergeOrUpload" operation to a search document, you must provide the vector fields in its entirety, along with the nonvector fields that you're updating, or the vector is dropped.

> [!IMPORTANT]
> Setting the `stored=false` attribution is irreversible. This property can only be set when you create the index and is only allowed on vector fields. Updating an existing index with new vector fields cannot set this property to `false`. If you want retrievable vector content later, you must drop and rebuild the index, or create and load a new field that has the new attribution.

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

## Set the `rescoreStorageMethod` property

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The `rescoreStorageMethod` property controls the storage of full-precision vectors when compression is used.

For *uncompressed* vector fields on indexes created with `2024-11-01-Preview` API versions and later, this will be omitted by default with no impact on search activities nor quality. For existing vector fields created prior to this API version, there is no in-place ability to remove this copy of data.

On a vector compression, the `rescoreStorageMethod` property is set to `preserveOriginals` by default, which retains full-precision vectors for[oversampling and rescoring capabilities](vector-search-how-to-quantization.md#add-compressions-to-a-search-index) to reduce the effect of lossy compression on the HNSW graph. If you don't use these capabilities, you can reduce vector storage by setting `rescoreStorageMethod` to `discardOriginals`.

> [!IMPORTANT]
> Setting the `rescoreStorageMethod` property is irreversible and will have different levels of search quality loss depending on the compression method. This can be set on indexes created with `2024-11-01-Preview` or later, either during index creation or adding new vector fields.

If you intend to use scalar or binary quantization, we recommend retaining `rescoreStorageMethod` set to `preserveOriginals` to maximize search quality.

To set this property:

1. Use [Create Index](/rest/api/searchservice/indexes/create?view=rest-searchservice-2024-11-01-preview&preserve-view=true) or [Create or Update Index 2024-11-01-preview](/rest/api/searchservice/indexes/create-or-update?view=rest-searchservice-2024-11-01-preview&preserve-view=true) REST APIs, or an Azure SDK beta package providing the feature.

1. Add a `vectorSearch` section to your index with profiles, algorithms, and compressions.

1. Under compressions, add `rescoringOptions` with `enableRescoring` set to true, `defaultOversampling` set to a positive integer, and `rescoreStorageMethod` set to `preserveOriginals`.

    ```http
    PUT https://[service-name].search.windows.net/indexes/demo-index?api-version=2024-11-01-preview
    
    {
        "name": "demo-index",
        "fields": [. . . ],
        . . .
        "vectorSearch": {
            "profiles": [
                {
                "name": "myVectorProfile",
                "algorithm": "myHnsw",
                "compression": "myScalarQuantization"
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
                }
            ]
        }
    }
    ```
