---
title: Choose vector optimization
titleSuffix: Azure AI Search
description: Learn about the vector compression options in Azure AI Search, and how to reduce storage through narrow data types, built-in scalar or quantization, truncated dimensions, and elimination of redundant storage.

author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2024
ms.topic: concept-article
ms.date: 11/19/2024
---

# Choose an approach for optimizing vector storage and processing

Embeddings, or the numerical representation of heterogeneous content, are the basis of vector search workloads, but the sizes of embeddings make them hard to scale and expensive to process. Significant research and productization have produced multiple solutions for improving scale and reducing processing times. Azure AI Search taps into a number these capabilities for faster and cheaper vector workloads.

This article enumerates all of optimization techniques in Azure AI Search that can help you reduce vector size and query processing times. 

Vector optimization settings are specified in vector field definitions in a search index. Most of the features described in this article are generally available in [2024-07-01 REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-07-01&preserve-view=true) and in the Azure SDK packages targeting that version. The [latest preview version](/rest/api/searchservice/operation-groups?view=rest-searchservice-2024-09-01-preview&preserve-view=true) adds support for truncated dimensions if you're using text-embedding-3-large or text-embedding-3-small for vectorization.

## Evaluate the options

Review the approaches in Azure AI Search for reducing the amount of storage used by vector fields. These approaches aren't mutually exclusive and can be combined for [maximum reduction in vector size](#example-vector-size-by-vector-compression-technique).

We recommend built-in quantization because it compresses vector size in memory *and* on disk with minimal effort, and that tends to provide the most benefit in most scenarios. In contrast, narrow types (except for float16) require a special effort into making them, and `stored` saves on disk storage, which isn't as expensive as memory.

| Approach | Why use this option |
|----------|---------------------|
| [Add scalar or binary quantization](vector-search-how-to-quantization.md) | Use quantization to compress native float32 or float16  embeddings to  int8  (scalar) or Byte (binary). This option reduces storage in memory and on disk with no degradation of query performance. Smaller data types like int8 or Byte produce vector indexes that are less content-rich than those with larger embeddings. To offset information loss, built-in compression includes options for post-query processing using uncompressed embeddings and oversampling to return more relevant results. Reranking and oversampling are specific features of built-in quantization of float32 or float16 fields and can't be used on embeddings that undergo custom quantization. |
| [Truncate dimensions for MRL-capable text-embedding-3 models (preview)](vector-search-how-to-truncate-dimensions.md) | Exercise the option to use fewer dimensions on text-embedding-3 models. On Azure OpenAI, these models have been retrained on the [Matryoshka Representation Learning (MRL)](https://arxiv.org/abs/2205.13147) technique that produces multiple vector representations at different levels of compression. This approach produces faster searches and reduced storage costs, with minimal loss of semantic information. In Azure AI Search, MRL support supplements scalar and binary quantization. When you use either quantization method, you can also specify a `truncateDimension` property on your vector fields to reduce the dimensionality of text embeddings. |
| [Assign smaller primitive data types to vector fields](vector-search-how-to-assign-narrow-data-types.md) | Narrow data types, such as float16, int16,  int8, and Byte (binary) consume less space in memory and on disk, but you must have an embedding model that outputs vectors in a narrow data format. Or, you must have custom quantization logic that outputs small data. A third use case that requires less effort is recasting native float32 embeddings produced by most models to float16. See [Index binary vectors](vector-search-how-to-index-binary-data.md) for details about binary vectors. |
| [Eliminate optional storage of retrievable vectors](vector-search-how-to-storage-options.md) | Vectors returned in a query response are stored separately from vectors used during query execution. If you don't need to return vectors, you can turn off retrievable storage, reducing overall per-field disk storage by up to 50 percent. |

All of these options are defined on an empty index. To implement any of them, use the Azure portal, REST APIs, or an Azure SDK package targeting that API version.

After the index is defined, you can load and index documents as a separate step.

## Example: vector size by vector compression technique

[Code sample: Vector quantization and storage options using Python](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/vector-quantization-and-storage/README.md) is a Python code sample that creates multiple search indexes that vary by their use of vector storage quantization, [narrow data types](vector-search-how-to-assign-narrow-data-types.md), and [storage properties](vector-search-how-to-storage-options.md).

This code creates and compares storage and vector index size for each vector storage optimization option. From these results, you can see that [quantization](vector-search-how-to-quantization.md) reduces vector size the most, but the greatest storage savings are achieved if you use multiple options.

| Index name | Storage size | Vector size |
|------------|--------------|-------------|
| compressiontest-baseline | 21.3613MB | 4.8277MB |
| compressiontest-scalar-compression | 17.7604MB | 1.2242MB |
| compressiontest-narrow | 16.5567MB | 2.4254MB |
| compressiontest-no-stored | 10.9224MB | 4.8277MB  |
| compressiontest-all-options | 4.9192MB | 1.2242MB |

Search APIs report storage and vector size at the index level, so indexes and not fields must be the basis of comparison. Use the [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics) or an equivalent API in the Azure SDKs to obtain vector size.

## See also

- [Get started with REST](search-get-started-rest.md)
- [Supported data types](/rest/api/searchservice/supported-data-types)
- [Search REST APIs](/rest/api/searchservice/)
