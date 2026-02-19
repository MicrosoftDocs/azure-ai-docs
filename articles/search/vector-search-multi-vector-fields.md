---
title: Multi-Vector Field Support
titleSuffix: Azure AI Search
description: Learn how Azure AI Search enables multi-vector field support for better search experiences with long-form or multimodal content.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: concept-article
ms.date: 08/27/2025
---

# Multi-vector field support in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The multi-vector field support feature in Azure AI Search enables you to index multiple child vectors within a single document field. This feature is valuable for use cases like multimodal data or long-form documents, where representing the content with a single vector would lead to loss of important detail.

## Limitations

- Semantic ranker isn't supported for nested chunks within a complex field. Therefore, the semantic ranker doesn't support nested vectors in multi-vector fields.

## Understand multi-vector field support

Traditionally, vector types, for example `Collection(Edm.Single)` could only be used in top-level fields. With the introduction of multi-vector field support, you can now use vector types in nested fields of complex collections, effectively allowing multiple vectors to be associated with a single document.

A single document can include up to 100 vectors in total, across all complex collection fields. Vector fields can only be nested one level deep.

### Index definition with multi-vector field

No new index properties are needed for this feature. Here's a sample index definition:

```json
{
  "name": "multivector-index",
  "fields": [
    {
      "name": "id",
      "type": "Edm.String",
      "key": true,
      "searchable": true
    },
    {
      "name": "title",
      "type": "Edm.String",
      "searchable": true
    },
    {
      "name": "description",
      "type": "Edm.String",
      "searchable": true
    },
    {
      "name": "descriptionEmbedding",
      "type": "Collection(Edm.Single)",
      "dimensions": 3,
      "searchable": true,
      "retrievable": true,
      "vectorSearchProfile": "hnsw"
    },
    {
      "name": "scenes",
      "type": "Collection(Edm.ComplexType)",
      "fields": [
        {
          "name": "embedding",
          "type": "Collection(Edm.Single)",
          "dimensions": 3,
          "searchable": true,
          "retrievable": true,
          "vectorSearchProfile": "hnsw"
        },
        {
          "name": "timestamp",
          "type": "Edm.Int32",
          "retrievable": true
        },
        {
          "name": "description",
          "type": "Edm.String",
          "searchable": true,
          "retrievable": true
        },
        {
          "name": "framePath",
          "type": "Edm.String",
          "retrievable": true
        }
      ]
    }
  ]
}
```

### Sample ingest document

Here's a sample document that illustrates how you might use multi-vector fields in practice:

```json
{
  "id": "123",
  "title": "Non-Existent Movie",
  "description": "A fictional movie for demonstration purposes.",
  "descriptionEmbedding": [1, 2, 3],
  "releaseDate": "2025-08-01",
  "scenes": [
    {
      "embedding": [4, 5, 6],
      "timestamp": 120,
      "description": "A character is introduced.",
      "framePath": "nonexistentmovie\\scenes\\scene120.png"
    },
    {
      "embedding": [7, 8, 9],
      "timestamp": 2400,
      "description": "The climax of the movie.",
      "framePath": "nonexistentmovie\\scenes\\scene2400.png"
    }
  ]
}
```

In this example, the scenes field is a complex collection containing multiple vectors (the embedding fields), along with other associated data. Each vector represents a scene from the movie and could be used to find similar scenes in other movies, among other potential use cases.

## Query with multi-vector field support

The multi-vector field support feature introduces some changes to the query mechanism in Azure AI Search. However, the main querying process remains largely the same.
Previously, `vectorQueries` could only target vector fields defined as top-level index fields. With this feature, we're relaxing this restriction and allowing vectorQueries to target fields that are nested within a collection of complex types (up to one level deep).
Additionally, a new query time parameter is available: `perDocumentVectorLimit`.

- Setting `perDocumentVectorLimit` to `1` ensures that at most one vector per document is matched, guaranteeing that results come from distinct documents.
- Setting `perDocumentVectorLimit` to `0` (unlimited) allows multiple relevant vectors from the same document to be matched.

```json
{
  "vectorQueries": [
    {
      "kind": "text",
      "text": "whales swimming",
      "K": 50,
      "fields": "scenes/embedding",
      "perDocumentVectorLimit": 0
    }
  ],
  "select": "title, scenes/timestamp, scenes/framePath"
}
```

## Rank across multiple vectors in a single field

When multiple vectors are associated with a single document, Azure AI Search uses the maximum score among them for ranking. The system uses the most relevant vector to score each document, which prevents dilution by less relevant ones.

## Retrieve relevant elements in a collection

When a collection of complex types is included in the `$select` parameter, only the elements that matched the vector query are returned. This is useful for retrieving associated metadata such as timestamps, text descriptions, or image paths.

> [!NOTE]
> To reduce payload size, avoid including the vector values themselves in the `$select` parameter. Consider omitting vector storage entirely if unnecessary.

## Debug multi-vector queries (preview)

When a document includes multiple embedded vectors, such as text and image embeddings in different subfields, the system uses the highest vector score across all elements to rank the document.

To debug how each vector contributed, use the `innerHits` debug mode (available in the latest preview REST API).

```json
POST /indexes/my-index/docs/search?api-version=2025-11-01-preview
{
  "vectorQueries": [
    {
      "kind": "vector",
      "field": "keyframes.imageEmbedding",
      "kNearestNeighborsCount": 5,
      "vector": [ /* query vector */ ]
    }
  ],
  "debug": "innerHits"
}
```

### Example response shape

```json
"@search.documentDebugInfo": {
  "innerHits": {
    "keyframes": [
      {
        "ordinal": 0,
        "vectors": [
          {
            "imageEmbedding": {
              "searchScore": 0.958,
              "vectorSimilarity": 0.956
            },
            "textEmbedding": {
              "searchScore": 0.958,
              "vectorSimilarity": 0.956
            }
          }
        ]
      },
      {
        "ordinal": 1,
        "vectors": [
          {
            "imageEmbedding": null,
            "textEmbedding": {
              "searchScore": 0.872,
              "vectorSimilarity": 0.869
            }
          }
        ]
      }
    ]
  }
}
```

### Field descriptions

| Field              | Description                                                              |
|-------------------|---------------------------------------------------------------------------|
| `ordinal`         | Zero-based index of the element inside the collection.                   |
| `vectors`         | One entry per searchable vector field contained in the element.          |
| `searchScore`     | Final score for that field, after any rescoring and boosts.             |
| `vectorSimilarity`| Raw similarity returned by the distance function.                        |

> [!NOTE]
> `innerHits` currently reports only vector fields.

### Relationship to debug=vector

Here are some facts about this property:

- The existing `debug=vector` switch remains unchanged.

- When used with multi-vector fields, `@search.document` `DebugInfo.vector.subscore` shows the maximum score used to rank the parent document, but not per-element detail.

- Use `innerHits` to gain insight into how individual elements contributed to the score.
