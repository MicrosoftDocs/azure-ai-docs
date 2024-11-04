---
title: Quantize vector fields
titleSuffix: Azure AI Search
description: Configure built-in scalar or quantization for compressing vectors on disk and in memory.

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/04/2024
---

# Use scalar or binary quantization to compress vector size

Quantization is recommended for reducing vector size because it lowers both memory and disk storage requirements for float16 and float32 embeddings. To offset the effects of a smaller index, you can add oversampling and reranking over uncompressed vectors.

Quantization applies to vector fields receiving float-type vectors. In the examples in this article, the field's data type is `Collection(Edm.Single)` for incoming float32 embeddings, but float16 is also supported. When the vectors are received on a field with compression configured, the engine automatically performs quantization to reduce the footprint of the vector data in memory and on disk.

Two types of quantization are supported:

- Scalar quantization compresses float values into narrower data types. AI Search currently supports int8, which is 8 bits, reducing vector index size fourfold.

- Binary quantization converts floats into binary bits, which takes up 1 bit. This results in up to 28 times reduced vector index size.

To use built-in quantization, follow these steps:

> [!div class="checklist"]
> - Use [Create Index](/rest/api/searchservice/indexes/create) or [Create Or Update Index](/rest/api/searchservice/indexes/create-or-update) to specify vector compression
> - Add `vectorSearch.compressions` to a search index
> - Add a `scalarQuantization` or `binaryQuantization` configuration and give it a name
> - Set optional properties to mitigate the effects of lossy indexing
> - Create a new vector profile that uses the named configuration
> - Create a new vector field having the new vector profile
> - Load the index with float32 or float16 data that's quantized during indexing with the configuration you defined
> - Optionally, [query quantized data](#) using the oversampling parameter if you want to override the default

## Add "compressions" to a search index

The following example shows a partial index definition with a fields collection that includes a vector field, and a `vectorSearch.compressions` section.

This example includes both `scalarQuantization` or `binaryQuantization`. You can specify as many compression configurations as you need, and then assign the ones you want to a vector profile.

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
        "profiles": [ ],
        "algorithms": [ ],
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

- `kind` must be set to `scalarQuantization` or `binaryQuantization`

- `rerankWithOriginalVectors` uses the original, uncompressed vectors to recalculate similarity and rerank the top results returned by the initial search query. The uncompressed vectors exist in the search index even if `stored` is false. This property is optional. Default is true.

- `defaultOversampling` considers a broader set of potential results to offset the reduction in information from quantization. The formula for potential results consists of the `k` in the query, with an oversampling multiplier. For example, if the query specifies a `k` of 5, and oversampling is 20, then the query effectively requests 100 documents for use in reranking, using the original uncompressed vector for that purpose. Only the top `k` reranked results are returned. This property is optional. Default is 4.

- `quantizedDataType` is optional and applies to scalar quantization only. If you add it, it must be set to `int8`. This is the only primitive data type supported for scalar quantization at this time. Default is `int8`.

## Add the HNSW algorithm

Make sure your index has the Hierarchical Navigable Small Worlds (HNSW) algorithm. Built-in quantization isn't supported with exhaustive KNN.

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

## How  binary quantization works in Azure AI Search

Binary quantization compresses high-dimensional vectors by representing each component as a single bit, either 0 or 1. This method drastically reduces the memory footprint and accelerates vector comparison operations, which are crucial for search and retrieval tasks. Benchmark tests show up to 96% reduction in vector index size.

It's particularly effective for embeddings with dimensions greater than 1024. For smaller dimensions, we recommend testing the quality of binary quantization, or trying scalar instead. Additionally, we’ve found BQ performs very well when embeddings are centered around zero. Most popular embedding models such as OpenAI, Cohere, and Mistral are centered around zero.

## Example: vector compression techniques

Here's Python code that demonstrates quantization, [narrow data types](vector-search-how-to-assign-narrow-data-types.md), and use of the [stored property](vector-search-how-to-storage-options.md). 

This code is borrowed from [Code sample: Vector quantization and storage options using Python](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/vector-quantization-and-storage/README.md).

This code creates and compares storage and vector index size for each option.

```bash
****************************************
Index Name: compressiontest-baseline
Storage Size: 21.3613MB
Vector Size: 4.8277MB
****************************************
Index Name: compressiontest-compression
Storage Size: 17.7604MB
Vector Size: 1.2242MB
****************************************
Index Name: compressiontest-narrow
Storage Size: 16.5567MB
Vector Size: 2.4254MB
****************************************
Index Name: compressiontest-no-stored
Storage Size: 10.9224MB
Vector Size: 4.8277MB
****************************************
Index Name: compressiontest-all-options
Storage Size: 4.9192MB
Vector Size: 1.2242MB
```

Search APIs report storage and vector size at the index level, so indexes and not fields must be the basis of comparison. Use the [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics) or an equivalent API in the Azure SDKs to obtain vector size.

## Query a quantized vector field using oversampling

Query syntax for a compressed or quantized vector field is the same as for noncompressed vector fields, unless you want to override parameters associated with oversampling or reranking with original vectors.

Recall that the [vector compression definition](vector-search-how-to-quantization.md) in the index has settings for `rerankWithOriginalVectors` and `defaultOversampling` to mitigate the effects of a smaller vector index. You can override the default values to vary the behavior at query time. For example, if `defaultOversampling` is 10.0, you can change it to something else in the query request.

You can set the oversampling parameter even if the index doesn't explicitly have a `rerankWithOriginalVectors` or `defaultOversampling` definition. Providing `oversampling` at query time overrides the index settings for that query and executes the query with an effective `rerankWithOriginalVectors` as true.

```http
POST https://[service-name].search.windows.net/indexes/demo-index/docs/search?api-version=2024-07-01   
  Content-Type: application/json   
  api-key: [admin key]   

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
