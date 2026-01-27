---
title: Assign Narrow Data Types
titleSuffix: Azure AI Search
description: Learn how to assign narrow data types to vector fields to reduce the storage requirements of vector indexes.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 01/16/2026
---

# Assign narrow data types to vector fields in Azure AI Search

An easy way to reduce vector size is to store embeddings in a smaller data format. Most embedding models output 32-bit floating point numbers. However, if you quantize your vectors or use an embedding model that natively supports quantization, the output might be float16, int16, or int8, which are significantly smaller than float32. You can accommodate these smaller vector sizes by assigning a narrow data type to a vector field. In the vector index, narrow data types consume less storage.

You assign data types to fields in an index definition. Use the Azure portal, the [Search Service REST APIs](/rest/api/searchservice/indexes/create), or an Azure SDK package that provides the feature.

## Prerequisites

- An embedding model that outputs small data formats, such as text-embedding-3 or Cohere V3 embedding models.

## Supported narrow data types

1. Review the [data types used for vector fields](/rest/api/searchservice/supported-data-types#edm-data-types-for-vector-fields) for recommended usage:

   - `Collection(Edm.Single)`: 32-bit floating point (default)
   - `Collection(Edm.Half)`: 16-bit floating point (narrow)
   - `Collection(Edm.Int16)`: 16-bit signed integer (narrow)
   - `Collection(Edm.SByte)`: 8-bit signed integer (narrow)
   - `Collection(Edm.Byte)`: 8-bit unsigned integer (only allowed with packed binary data types)
1. From that list, determine which data type is valid for your embedding model's output or for vectors that undergo custom quantization.

   The following table provides links to several embedding models that can use a narrow data type, `Collection(Edm.Half)`, without extra quantization. You can cast from float32 to float16 using `Collection(Edm.Half)` with no extra work.

   | Embedding model | Native output | Assign this type in Azure AI Search |
   |------------------------|---------------|--------------------------------|
   | [text-embedding-ada-002](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#embeddings) | `Float32` | `Collection(Edm.Single)` or `Collection(Edm.Half)` |
   | [text-embedding-3-small](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#embeddings) | `Float32` | `Collection(Edm.Single)` or `Collection(Edm.Half)` |
   | [text-embedding-3-large](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure#embeddings) | `Float32` | `Collection(Edm.Single)` or `Collection(Edm.Half)` |
   | [Cohere V3 embedding models with int8 embedding_type](https://docs.cohere.com/reference/embed) | `Int8` | `Collection(Edm.SByte)` |

   You can use other narrow data types if your model emits embeddings in the smaller data format or if you have custom quantization that converts vectors to a smaller format.

1. Understand the tradeoffs of a narrow data type. `Collection(Edm.Half)` has less information, which results in lower resolution. If your data is homogeneous or dense, losing extra detail or nuance could lead to unacceptable results at query time because there's less detail that can be used to distinguish nearby vectors apart.

## Assign the data type

[Define and build an index](vector-search-how-to-create-index.md). You can use the Azure portal, [Indexes - Create Or Update](/rest/api/searchservice/indexes/create-or-update) (REST API), or an Azure SDK package for this step.

This field definition uses a narrow data type, `Collection(Edm.Half)`, that accepts a float32 embedding stored as a float16 value. As is true for all vector fields, set the `dimensions` and `vectorSearchProfile` properties. The specifics of the `vectorSearchProfile` are immaterial to the datatype.

Set `retrievable` and `stored` to true if you want to visually check the values of the field. On a subsequent rebuild, you can change these properties to false for reduced storage requirements.

```json
{
    "name": "nameEmbedding",
    "type": "Collection(Edm.Half)",
    "searchable": true,
    "filterable": false,
    "retrievable": true,
    "sortable": false,
    "facetable": false,
    "key": false,
    "indexAnalyzer": null,
    "searchAnalyzer": null,
    "analyzer": null,
    "synonymMaps": [],
    "dimensions": 1536,
    "vectorSearchProfile": "myHnswProfile"
}
```

Recall that vector fields aren't filterable, sortable, or facetable. They can't be used as keys and don't use analyzers or synonym maps.

### Working with a production index

You assign data types on new fields when they're created. You can't change the data type of an existing field, and you can't drop a field without [rebuilding the index](search-howto-reindex.md). For established indexes already in production, a common workaround is to create new fields with the desired revisions and then remove obsolete fields during a planned index rebuild.

## Check results

1. Verify the field content matches the data type. Assuming the vector field is marked as `retrievable`, use [Search explorer](search-explorer.md) or [Search - POST](/rest/api/searchservice/documents/search-post?) (REST API) to return vector field content.

1. To check vector index size, refer to the vector index size column on the **Search management > Indexes** page in the [Azure portal](https://portal.azure.com). You can also use [Indexes - Get Statistics](/rest/api/searchservice/indexes/get-statistics) (REST API) or an equivalent Azure SDK method.

> [!NOTE]
> The field's data type creates the physical data structure. To change a data type later, either [drop and rebuild the index](search-howto-reindex.md) or create a second field with the new definition.
