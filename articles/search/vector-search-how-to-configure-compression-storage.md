---
title: Choose Vector Optimization
titleSuffix: Azure AI Search
description: Learn about the vector compression options in Azure AI Search, and how to reduce storage through narrow data types, built-in scalar or quantization, truncated dimensions, and elimination of redundant storage.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 01/16/2026
---

# Choose an approach for optimizing vector storage and processing

Embeddings, or the numerical representation of heterogeneous content, are the basis of vector search workloads. However, the sizes of embeddings make them hard to scale and expensive to process. Significant research and productization have produced multiple solutions for improving scale and reducing processing times. Azure AI Search taps into a number of these capabilities for faster and cheaper vector workloads.

This article covers all of the optimization techniques in Azure AI Search that can help you reduce vector size and query processing times.

You specify vector optimization settings in vector field definitions in a search index. Most of the features described in this article are generally available in the [latest stable REST API version](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-09-01&preserve-view=true) and Azure SDK packages targeting that version.

## Evaluate the options

Review the approaches in Azure AI Search for reducing the amount of storage used by vector fields. These approaches aren't mutually exclusive, so you can combine them for [maximum reduction in vector size](#example-vector-size-by-vector-compression-technique).

We recommend built-in quantization because it compresses vector size in memory *and* on disk with minimal effort. This approach tends to provide the most benefit in most scenarios. In contrast, narrow types (except for float16) require special effort to create them, and `stored` saves on disk storage, which isn't as expensive as memory.

| Approach | Why use this approach |
|----------|---------------------|
| [Add scalar or binary quantization](vector-search-how-to-quantization.md) | Compress native float32 or float16 embeddings to int8 (scalar) or byte (binary). This option reduces storage in memory and on disk with no degradation of query performance. Smaller data types, such as int8 or byte, produce vector indexes that are less content-rich than those with larger embeddings. To offset information loss, built-in compression includes options for post-query processing by using uncompressed embeddings and oversampling to return more relevant results. Reranking and oversampling are specific features of built-in quantization of float32 or float16 fields and can't be used on embeddings that undergo custom quantization. |
| [Truncate dimensions for MRL-capable text-embedding-3 models](vector-search-how-to-truncate-dimensions.md) | Use fewer dimensions on text-embedding-3 models. On Azure OpenAI, these models are retrained on the [Matryoshka Representation Learning](https://arxiv.org/abs/2205.13147) (MRL) technique that produces multiple vector representations at different levels of compression. This approach produces faster searches and reduced storage costs with minimal loss of semantic information. In Azure AI Search, MRL support supplements scalar and binary quantization. When you use either quantization method, you can also specify a `truncateDimension` property on your vector fields to reduce the dimensionality of text embeddings. |
| [Assign smaller primitive data types to vector fields](vector-search-how-to-assign-narrow-data-types.md) | Narrow data types, such as float16, int16, int8, and byte (binary), consume less space in memory and on disk. However, you must have an embedding model that outputs vectors in a narrow data format. Alternatively, you must have custom quantization logic that outputs small data. A third use case that requires less effort is recasting native float32 embeddings produced by most models to float16. For information about binary vectors, see [Index binary vectors](vector-search-how-to-index-binary-data.md). |
| [Eliminate optional storage of retrievable vectors](vector-search-how-to-storage-options.md) | Vectors returned in a query response are stored separately from vectors used during query execution. If you don't need to return vectors, you can turn off retrievable storage to reduce overall per-field disk storage by up to 50 percent. |

Define all of these options on an empty index. To implement any of them, use the Azure portal, REST APIs, or an Azure SDK package targeting that API version.

After you define the index, you can load and index documents as a separate step.

## Example: Vector size by vector compression technique

[Vector quantization and storage options using Python](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/vector-quantization-and-storage/README.md) is a Python code sample that creates multiple search indexes that vary by their use of vector storage quantization, [narrow data types](vector-search-how-to-assign-narrow-data-types.md), and [storage properties](vector-search-how-to-storage-options.md).

This code creates and compares storage and vector index size for each vector storage optimization option. From these results, you can see that [quantization](vector-search-how-to-quantization.md) reduces vector size the most, but the greatest storage savings are achieved if you use multiple options.

| Index name | Storage size | Vector size |
|------------|--------------|-------------|
| compressiontest-baseline | 21.3613 MB | 4.8277 MB |
| compressiontest-scalar-compression | 17.7604 MB | 1.2242 MB |
| compressiontest-narrow | 16.5567 MB | 2.4254 MB |
| compressiontest-no-stored | 10.9224 MB | 4.8277 MB |
| compressiontest-all-options | 4.9192 MB | 1.2242 MB |

The Search Service REST APIs report storage and vector size at the index level, so you must compare indexes, not fields. Use [Indexes - Get Statistics](/rest/api/searchservice/indexes/get-statistics) (REST API) or an equivalent API in the Azure SDKs to get vector size.

## Related content

- [Vector search in Azure AI Search](vector-search-overview.md)
- [Create a vector index](vector-search-how-to-create-index.md)
- [Supported data types](/rest/api/searchservice/supported-data-types)
