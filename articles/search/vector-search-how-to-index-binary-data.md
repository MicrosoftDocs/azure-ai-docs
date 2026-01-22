---
title: Index Binary Vectors for Vector Search
titleSuffix: Azure AI Search
description: Learn how to configure fields for binary vectors and the vector search configuration for querying the fields.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 01/16/2026
---

# Index binary vectors for vector search

Azure AI Search supports the `Collection(Edm.Byte)` packed binary type to further reduce the storage and memory footprint of vector data. You can use this data type for the output of models such as [Cohere's Embed v3 binary embedding models](https://cohere.com/blog/int8-binary-embeddings) or any other embedding model or process that outputs vectors as binary bytes.

There are three steps to configuring an index for binary vectors:

> [!div class="checklist"]
> + Add a vector search algorithm that specifies Hamming distance for binary vector comparison
> + Add a vector profile that points to the algorithm
> + Add a vector field of type `Collection(Edm.Byte)` and assign the Hamming distance

This article uses the REST APIs for illustration, but you can also use an Azure SDK or the Azure portal to add a binary field to an index. You assign the binary data type to fields by using the [Indexes - Create](/rest/api/searchservice/indexes/create) or [Indexes - Create Or Update](/rest/api/searchservice/indexes/create-or-update) REST APIs.

> [!TIP]
> If you're investigating binary vector support for its smaller footprint, you might also consider the vector quantization and storage reduction features in Azure AI Search. Inputs are float32 or float16 embeddings. Output is stored data in a much smaller format. For more information, see [Compress using binary or scalar quantization](vector-search-how-to-quantization.md) and [Assign narrow data types](vector-search-how-to-assign-narrow-data-types.md).

## Prerequisites

+ Familiarity with [creating an index](search-how-to-create-search-index.md) and [adding vector fields](vector-search-how-to-create-index.md).

+ Binary vectors, with one bit per dimension, packaged in uint8 values with eight bits per value. You can get these vectors by using models that directly generate *packaged binary* vectors or by quantizing vectors into binary vectors in your client application during indexing and retrieval.

## Limitations

+ No Azure portal support in the **Import data (new)** wizard.

+ No support for binary fields in the [AML skill](cognitive-search-aml-skill.md) that's used for integrated vectorization of models from the Microsoft Foundry model catalog.

## Add a vector search algorithm and vector profile

Vector search algorithms create the query navigation structures during indexing. For binary vector fields, the system uses the Hamming distance metric to perform vector comparisons. 

To configure vector search for binary vectors:

1. Set up an [Indexes - Create or Update](/rest/api/searchservice/indexes/create-or-update) (REST API) request.

1. In the index schema, add a `vectorSearch` section that specifies profiles and algorithms.

1. Add one or more [vector search algorithms](vector-search-ranking.md) that use a similarity metric of `hamming`. The Hierarchical Navigable Small Worlds (HNSW) algorithm is common, but you can also use Hamming distance with exhaustive K-Nearest Neighbors (KNN).

1. Add one or more vector profiles that specify the algorithm.

The following example shows a basic `vectorSearch` configuration.

```json
  "vectorSearch": { 
    "profiles": [ 
      { 
        "name": "myHnswProfile", 
        "algorithm": "myHnsw", 
        "compression": null, 
        "vectorizer": null 
      } 
    ], 
    "algorithms": [ 
      { 
        "name": "myHnsw", 
        "kind": "hnsw", 
        "hnswParameters": { 
          "metric": "hamming" 
        } 
      }, 
      { 
        "name": "myExhaustiveKnn", 
        "kind": "exhaustiveKnn", 
        "exhaustiveKnnParameters": { 
          "metric": "hamming" 
        } 
      } 
    ] 
  }
```

## Add a binary field to an index

The fields collection of an index must include a field for the document key, vector fields, and any other fields you need for hybrid search scenarios.

Binary fields use the `Collection(Edm.Byte)` type and contain embeddings in packed form. For example, if the original embedding dimension is `1024`, the packed binary vector length is `ceiling(1024 / 8) = 128`. You get the packed form by setting the `vectorEncoding` property on the field.

To add a binary vector field to an index:

1. Add a field to the fields collection and give it a name.

1. Set the data type to `Collection(Edm.Byte)`.

1. Set `vectorEncoding` to `packedBit` for binary encoding.

1. Set `dimensions` to `1024`. Specify the original (unpacked) vector dimension.

1. Set `vectorSearchProfile` to a profile you defined in the previous step.

1. Set `searchable` to `true`.

The following field definition is an example of a binary vector field in an index schema.

```json
  "fields": [ 
    . . . 
    { 
      "name": "my-binary-vector-field", 
      "type": "Collection(Edm.Byte)", 
      "vectorEncoding": "packedBit", 
      "dimensions": 1024, 
      "vectorSearchProfile": "myHnswProfile",
      "searchable": true
    },
   . . . 
  ]
```

## Related content

+ Review the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repository for end-to-end workflows that include schema definition, vectorization, indexing, and queries.

+ Review the vector search demo code for [C#](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-dotnet), [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python), and [JavaScript](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-javascript).
