---
title: Eliminate optional vector instances
titleSuffix: Azure AI Search
description: In vector search, configure storage to exclude optional copies of vector fields, reducing the storage requirements of vector data.

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/19/2024
---

# Eliminate optional vector instances from storage

Azure AI Search stores multiple copies of vector fields that are used in specific workloads. If you don't need to support a specific behavior, like returning raw vectors in a query response, you can set properties in the index that omit storage for that workload.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md) with a `vectorSearch` configuration, using the Hierarchical Navigable Small Worlds (HNSW) algorithm and a new vector profile.

## How vector fields are stored

For every vector field, there are three copies of the vectors:

| Instance | Usage |
|----------|-------|
| Source vectors (in JSON) as received from an embedding model or push request to the index | Used for incremental data refresh, and if you want "retrievable" vectors returned in the query response. |
| Original full-precision vectors | Used for scoring if vectors are uncompressed, or optional rescoring if query results obtained over compressed vectors. Rescoring applies only if vector fields undergo [scalar or binary quantization](vector-search-how-to-quantization.md). |
| Vectors in the [HNSW graph for Approximate Nearest Neighbors (ANN) search](vector-search-overview.md) | Used for query execution. |

The last instance (vectors and graph) is required for ANN vector query execution. The first two instances can be discarded if you don't need them. Compression techniques like scalar or binary quantization are applied to the vectors used during query execution.

## Set the `stored` property

The `stored` property is a boolean on a vector field definition that determines whether storage is allocated for retrievable vector field content (the source instance). The `stored` property is true by default. If you don't need raw vector content in a query response, you can save up to 50 percent storage per field by changing `stored` to false.

Considerations for setting `stored` to false:

- Because vectors aren't human readable, you can omit them from results sent to LLMs in RAG scenarios, and from results that are rendered on a search page. Keep them, however, if you're using vectors in a downstream process that consumes vector content.

- However, if your indexing strategy includes [partial document updates](search-howto-reindex.md#update-content), such as "merge" or "mergeOrUpload" on an existing document, setting `stored=false` prevents content updates to those fields during the merge. On each "merge" or "mergeOrUpload" operation to a search document, you must provide the vector fields in its entirety, along with the nonvector fields that you're updating, or the vector is dropped.

Setting the `stored=false` attribution is irreversible. It's set during index creation on vector fields when physical data structures are created. If you want retrievable vector content later, you must drop and rebuild the index, or create and load a new field that has the new attribution.

The following example shows the fields collection of a search index. Set `stored` to false to permanently remove retrievable storage for the vector field.

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

The `rescoreStorageMethod` property on a vector field definition determines whether storage is allocated for original full-precision vectors. The `rescoreStorageMethod` property is set to `preserveOriginals` by default. If you aren't using the [oversampling and rescoring mitigations](vector-search-how-to-quantization.md#add-compressions-to-a-search-index) provided for querying compressed vectors, you can save on vector storage by changing `rescoreStorageMethod` to `discardOriginals`.

If you intend to use scalar or binary quantization, we recommend retaining `rescoreStorageMethod` set to `preserveOriginals`.

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
