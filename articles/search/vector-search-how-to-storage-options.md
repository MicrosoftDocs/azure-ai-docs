---
title: Omit vectors from search results
titleSuffix: Azure AI Search
description: In vector search, configure storage to exclude optional copies of vector fields, reducing the storage requirements of vector data.

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/04/2024
---

# Omit vectors from search results

Azure AI Search stores multiple copies of field content that are used in specific workloads. If you don't need to support a specific behavior, like returning raw vectors in a query response, you can set properties that omit storage for that workload.

## Prerequisites

- [Vector fields in a search index](vector-search-how-to-create-index.md).

## Set the stored property

The `stored` property is a boolean on a vector field definition that determines whether storage is allocated for retrievable vector field content. The `stored` property is true by default. If you don't need raw vector content in a query response, you can save up to 50 percent storage per field by setting `stored` to false.

Considerations for setting `stored` to false:

- Because vectors aren't human readable, you can omit them from results sent to LLMs in RAG scenarios, and from results that are rendered on a search page. Keep them, however, if you're using vectors in a downstream process that consumes vector content.

- However, if your indexing strategy includes [partial document updates](search-howto-reindex.md#update-content), such as "merge" or "mergeOrUpload" on a document, remember that setting `stored=false` bypasses content updates to those fields during the merge. On each "merge" or "mergeOrUpload" operation, you must provide the vector fields in addition to other nonvector fields that you're updating, or the vector will be dropped.

Remember that the `stored` attribution is irreversible. It's set during index creation on vector fields when physical data structures are created. If you want retrievable vector content later, you must drop and rebuild the index, or create and load a new field that has the new attribution.

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

## 