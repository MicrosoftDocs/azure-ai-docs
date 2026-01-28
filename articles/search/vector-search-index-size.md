---
title: Vector Index Limits
titleSuffix: Azure AI Search
description: Learn about the factors that affect the size of a vector index.
author: robertklee
ms.author: robertlee
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: concept-article
ms.date: 11/21/2025
ms.custom:
  - build-2024
  - ignite-2024
  - sfi-image-nochange
---

# Vector index size and limits

For each vector field, Azure AI Search constructs an internal vector index using the algorithm parameters specified on the field. Because Azure AI Search imposes quotas on vector index size, you should know how to estimate and monitor vector size to ensure you stay under the limits.

Internally, the physical data structures of a search index include:

+ Raw content (used for retrieval patterns requiring nontokenized content)
+ Inverted indexes (used for searchable text fields)
+ Vector indexes (used for searchable vector fields)

This article explains the limits for the internal vector indexes that back each of your vector fields.

> [!TIP]
> [Vector optimization techniques](vector-search-how-to-configure-compression-storage.md) are generally available. Use capabilities like narrow data types, scalar and binary quantization, and elimination of redundant storage to reduce your vector quota and storage quota consumption.

## Key points about quota and vector index size

+ Vector index size is measured in bytes.

+ The total storage of your service contains all of your vector index files. Azure AI Search maintains different copies of vector index files for different purposes. We offer other options to reduce the [storage overhead of vector indexes](vector-search-how-to-storage-options.md) by eliminating some of these copies.

+ Vector quotas are enforced on the search service as a whole, per partition. If you add partitions, vector quota also increases. Per-partition vector quotas are higher on newer services. For more information, see [Vector index size limits](search-limits-quotas-capacity.md#vector-index-size-limits).

+ Not all algorithms consume vector index size quota. Vector quotas are established based on memory requirements of Approximate Nearest Neighbor (ANN) search. Vector fields created with the Hierarchical Navigable Small World (HNSW) algorithm need to reside in memory during query execution because of the random-access nature of graph-based traversals. Vector fields using the exhaustive K-Nearest Neighbors (KNN) algorithm are loaded into memory dynamically in pages during query execution and thus don't consume vector quota.

## Check partition size and quantity

If you aren't sure what your search service limits are, here are two ways to get that information:

+ In the Azure portal, on the search service **Overview** page, both the **Properties** tab and **Usage** tab show partition size and storage, and also vector quota and vector index size.

+ In the Azure portal, on the **Scale** page, you can review the number and size of partitions.

Your vector limit varies depending on your [service creation date](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date).

## Check vector index size

A request for vector metrics is a data plane operation. You can use the Azure portal, REST APIs, or Azure SDKs to get vector usage at the service level through service statistics and for individual indexes.

### [**Portal**](#tab/portal-vector-quota)

#### Vector size per index

To get vector index size per index, select **Search management** > **Indexes** to view a list of indexes and the document count, the size of in-memory vector indexes, and total index size as stored on disk.

Recall that vector quota is based on memory constraints. For vector indexes created using the HNSW algorithm, all searchable vector indexes are permanently loaded into memory. For indexes created using the exhaustive KNN algorithm, vector indexes are loaded in chunks, sequentially, during query time. There's no memory residency requirement for exhaustive KNN indexes. The lifetime of the loaded pages in memory is similar to text search and there are no other metrics applicable to exhaustive KNN indexes other than total storage.

The following screenshot shows two versions of the same vector index. One version is created using HNSW algorithm, where the vector graph is memory resident. Another version is created using exhaustive KNN algorithm. With exhaustive KNN, there's no specialized in-memory vector index, so the portal shows 0 MB for vector index size. Those vectors still exist and are counted in overall storage size, but they don’t occupy the in-memory resource that the vector index size metric is tracking.

:::image type="content" source="media/vector-search-index-size/vector-index-size-by-algorithm.png" lightbox="media/vector-search-index-size/vector-index-size-by-algorithm.png" alt-text="Screenshot of the index portal page showing vector index size based on different algorithms.":::

#### Vector size per service

To get vector index size for the search service as a whole, select the **Overview** page's **Usage** tab. Portal pages refresh every few minutes so if you recently updated an index, wait a bit before checking results.

The following screenshot is for an older Standard 1 (S1) search service, configured for one partition and one replica.

+ Storage quota is a disk constraint, and it's inclusive of all indexes (vector and nonvector) on a search service.

+ Vector index size quota is a memory constraint. It's the amount of memory required to load all internal vector indexes created for each vector field on a search service.

The screenshot indicates that indexes (vector and nonvector) consume almost 460 megabytes of available disk storage. Vector indexes consume almost 93 megabytes of memory at the service level.

:::image type="content" source="media/vector-search-index-size/portal-vector-index-size.png" lightbox="media/vector-search-index-size/portal-vector-index-size.png" alt-text="Screenshot of the Overview page's usage tab showing vector index consumption against quota.":::

Quotas for both storage and vector index size increase or decrease as you add or remove partitions. If you change the partition count, the tile shows a corresponding change in storage and vector quota.

> [!NOTE]
> On disk, vector indexes aren't 93 megabytes. Vector indexes on disk take up about three times more space than vector indexes in memory. See [How vector fields affect disk storage](#how-vector-fields-affect-disk-storage) for details.

### [**REST**](#tab/rest-vector-quota)

Data plane REST APIs (all newer APIs provide vector usage statistics):

+ [GET Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) returns quota and usage for the search service all-up.
+ [GET Index Statistics](/rest/api/searchservice/indexes/get-statistics) returns usage for a given index.

Usage and quota are reported in bytes.

Here's GET Service Statistics:

```http
GET {{baseUrl}}/servicestats?api-version=2025-09-01  HTTP/1.1
Content-Type: application/json
api-key: {{apiKey}}
```

Response includes metrics for `storageSize`, which doesn't distinguish between vector and nonvector indexes. The `vectorIndexSize` statistic shows usage and quota at the service level.  

```json
{
    "@odata.context": "https://my-demo.search.windows.net/$metadata#Microsoft.Azure.Search.V2023_11_01.ServiceStatistics",
    "counters": {
        "documentCount": {
            "usage": 15377,
            "quota": null
        },
        "indexesCount": {
            "usage": 13,
            "quota": 15
        },
        . . .
        "storageSize": {
            "usage": 39862913,
            "quota": 2147483648
        },
        . . .
        "vectorIndexSize": {
            "usage": 2685436,
            "quota": 1073741824
        }
    },
    "limits": {
        "maxFieldsPerIndex": 1000,
        "maxFieldNestingDepthPerIndex": 10,
        "maxComplexCollectionFieldsPerIndex": 40,
        "maxComplexObjectsInCollectionsPerDocument": 3000
    }
}
```

You can also send a GET Index Statistics to get the physical size of the index on disk, plus the in-memory size of the vector fields.

```http
GET {{baseUrl}}/indexes/vector-healthplan-idx/stats?api-version=2025-09-01  HTTP/1.1
Content-Type: application/json
api-key: {{apiKey}}
```

Response includes usage information at the index level. This example is based on the index created in [Quickstart: Vector search](search-get-started-portal-import-vectors.md) that chunks and vectorizes health plan PDFs. Each chunk contributes to `documentCount`.

```json
{
    "@odata.context": "https://my-demo.search.windows.net/$metadata#Microsoft.Azure.Search.V2023_11_01.IndexStatistics",
    "documentCount": 147,
    "storageSize": 4592870,
    "vectorIndexSize": 915484
}
```

---

## Factors affecting vector index size

There are three major components that affect the size of your internal vector index:

- Raw size of the data
- Overhead from the selected algorithm
- Overhead from deleting or updating documents within the index

### Raw size of the data

Each vector is usually an array of single-precision floating-point numbers, in a field of type `Collection(Edm.Single)`.  

Vector data structures require storage, represented in the following calculation as the "raw size" of your data. Use this _raw size_ to estimate the vector index size requirements of your vector fields.

The dimensionality of one vector determines its storage size. Multiply the size of one vector by the number of documents containing that vector field to obtain the _raw size_:

`raw size = (number of documents) * (dimensions of vector field) * (size of data type)`

| EDM data type | Size of the data type |
|---------------|-----------------------|
| `Collection(Edm.Single)` | 4 bytes |
| `Collection(Edm.Half)` | 2 bytes |
| `Collection(Edm.Int16)`| 2 bytes |
| `Collection(Edm.SByte)`| 1 byte |

### Memory overhead from the selected algorithm  
  
Every ANN algorithm generates extra data structures in memory to enable efficient searching. These structures consume extra space within memory.  
  
**For the HNSW algorithm, the memory overhead ranges between 1% and 20% for uncompressed float32 (Edm.Single) vectors.**  
  
As dimensionality increases, the memory overhead percentage decreases. This occurs because the raw size of the vectors increases in size while the other data structures, which store graph connectivity information, remain a fixed size for a given `m`. As a result, the relative impact of these extra data structures diminishes in relation to the overall vector size.
  
The memory overhead increases with larger values of the HNSW parameter `m`, which specifies the number of bi-directional links created for each new vector during index construction. This happens because each link contributes approximately 8 to 10 bytes per document, and the total overhead scales proportionally with `m`.
  
The following table summarizes the overhead percentages observed in internal tests for *uncompressed* vector fields:  
  
| Dimensions | HNSW parameter (m) | Overhead percentage |  
|------------|--------------------|---------------------|
| 96         | 4                  | 20%                 |
| 200        | 4                  | 8%                  |  
| 768        | 4                  | 2%                  |  
| 1536       | 4                  | 1%                  |
| 3072       | 4                  | 0.5%                |

These results demonstrate the relationship between dimensions, HNSW parameter `m`, and memory overhead for the HNSW algorithm.

For vector fields that use compression techniques, such as [scalar or binary quantization](vector-search-how-to-quantization.md), the overhead percentage appears to consume a greater percentage of the total vector index size. As the size of the data decreases, the relative impact of the fixed-size data structures used to store graph connectivity information becomes more significant.

### Overhead from deleting or updating documents within the index

When a document with a vector field is either deleted or updated (updates are internally represented as a delete and insert operation), the underlying document is marked as deleted and skipped during subsequent queries. As new documents are indexed and the internal vector index grows, the system cleans up these deleted documents and reclaims the resources. This means you'll likely observe a lag between deleting documents and the underlying resources being freed.

We refer to this as the *deleted documents ratio*. Since the deleted documents ratio depends on the indexing characteristics of your service, there's no universal heuristic to estimate this parameter, and there's no API or script that returns the ratio in effect for your service. We observe that half of our customers have a deleted documents ratio less than 10%. If you tend to perform high-frequency deletions or updates, then you might observe a higher deleted documents ratio.

This is another factor impacting the size of your vector index. Unfortunately, we don't have a mechanism to surface your current deleted documents ratio.

## Estimate total size of data in memory

Taking the previously described factors into account, to estimate the total size of your vector index, use the following calculation:

**`(raw_size) * (1 + algorithm_overhead (in percent)) * (1 + deleted_docs_ratio (in percent))`**

For example, to calculate the **raw_size**, let's assume you're using a popular Azure OpenAI model, `text-embedding-ada-002` with 1,536 dimensions. This means one document would consume 1,536 `Edm.Single` (floats), or 6,144 bytes since each `Edm.Single` is 4 bytes. 1,000 documents with a single, 1,536-dimensional vector field would consume in total 1000 docs x 1536 floats/doc = 1,536,000 floats, or 6,144,000 bytes.

If you have multiple vector fields, you need to perform this calculation for each vector field within your index and add them all together. For example, 1,000 documents with **two** 1,536-dimensional vector fields, consume 1000 docs x **2 fields** x 1536 floats/doc x 4 bytes/float = 12,288,000 bytes.

To obtain the **vector index size**, multiply this **raw_size** by the **algorithm overhead** and **deleted document ratio**. If your algorithm overhead for your chosen HNSW parameters is 10% and your deleted document ratio is 10%, then we get: `6.144 MB * (1 + 0.10) * (1 + 0.10) = 7.434 MB`.

## How vector fields affect disk storage

Most of this article provides information about the size of vectors in memory. For information about the storage overhead of vector indexes, see [Eliminate optional vector instances from storage](vector-search-how-to-storage-options.md).

## Related content

+ [Vector search in Azure AI Search](vector-search-overview.md)
+ [Choose an approach for optimizing vector storage and processing](vector-search-how-to-configure-compression-storage.md)
