---
title: Optimize costs for Azure AI Search serverless
description: Learn how to reduce Azure AI Search serverless costs by tuning compute usage, managing on-disk index storage, and tracking separately billed features.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 06/02/2026
ai-usage: ai-assisted
# customer intent: As a developer or product engineer, I want to understand the details behind how the Azure AI Search Serverless pricing model works so that I can optimize my search service to use the most efficient pricing model suited to my needs and only pay for what I use.

---

# Optimize costs with the Serverless pricing model in Azure AI Search

Azure AI Search supports two pricing models, each designed for different workload patterns:

- **Dedicated (provisioned capacity)**: Fixed pricing based on search units. You select a pricing tier, and you're billed hourly based on provisioned units. For more information, see [Choose a service tier](search-sku-tier.md).

- **Serverless (consumption-based)**: Metered pricing based on actual usage. *This model is currently in preview.* You're billed for:

    - Compute (measured in compute units, or CUs/hr)
    - Indexed storage (billed per GB/month based on on-disk index size)

## How cost is determined in the serverless model

In the serverless model, **performance optimization directly affects cost**. Cost is directly tied to workload execution:

- Queries and indexing consume compute, measured in compute units per hour (CUs/hr).
- Storage is billed separately based on index size on disk.
- When the service is idle with no active queries or indexing, compute usage is zero. There is no reserved or minimum capacity charge.

> [!IMPORTANT]
> CUs/hr don't include all optional capabilities. Semantic ranker, agentic retrieval, image extraction, and skill execution are billed separately.

## Understand compute units (CUs)

A compute unit (CU) represents the measured system resources required to perform search and indexing operations in the serverless model. CU cost is primarily driven by CPU utilization first, memory second, and storage I/O third. Index size (GB) and document payload size (KB) are close secondary drivers because they increase how much data each operation must process. Usage is billed per hour (CU/hr).

Compute cost scales with:

- Query complexity
- CPU, memory, and storage I/O utilization
- Index size (GB) and structure
- Document payload size (KB)
- Number of fields and retrieved results

Different operations have different cost profiles:

- **Lookup**: Low cost. Retrieving a single document by its ID is the most efficient operation.
- **Keyword search**: Low cost. Text search uses inverted indexes, which are optimized for speed and low compute usage.
- **Vector search**: High cost. Vector queries are computationally expensive because they require similarity calculations across high-dimensional embeddings. Compared to keyword search, they consume significantly more compute.
- **Hybrid search**: Creates an average cost between the Keyword and Vector searches, plus a small overhead for Reciprocal Rank Fusion (RRF) to merge results.

### Monitor compute usage

The Compute Unit (CU) cost of every request is returned in the `x-ms-request-charge` HTTP response header as a floating-point number. Use this header to identify expensive operations and optimize query patterns. You can track the CU cost of every request by inspecting the HTTP response headers and operation events in [Azure Monitor](/azure/azure-monitor/fundamentals/overview).

- **Header**: `x-ms-request-charge: <value>`
- **Value**: A floating-point number representing the CUs consumed.

Example:

```http
Status: 200 OK
Content-Type: application/json
x-ms-request-charge: 12.45
```

This value represents the compute consumed by the request and can be used to identify high-cost query patterns. In this example, the query consumed 12.45 CUs.

You can also use [Azure Monitor logs](search-monitor-queries.md) to track aggregate CU usage over time and correlate it with query volume and workload changes.

> [!NOTE]
> The Azure pricing calculator and SU-based capacity-planning worksheets don't apply to Serverless services. To estimate Serverless costs, index a representative sample of your data, run typical queries, and inspect the `x-ms-request-charge` header to measure actual CU consumption per operation type. Extrapolate to your expected volume, then apply current rates from the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/).
> Usage is measured per minute and rounded up to the nearest 0.25 CU/minute, with 60 of these per minute segments added up over the period of an hour to calculate the full CU/hr amount that appears on the bill. CU costs are consistent - the same request on the same data produces similar CU consumption. The relative cost of different operation types follows this general pattern: keyword search (low) < vector search (higher) < hybrid search (combined cost of both).

## Reduce compute costs through optimization

Efficient queries and index design reduce compute consumption and lower costs.

### Optimize your schema

Your index schema determines baseline compute and storage costs:

- **Limit field attributes**: Only enable attributes (searchable, filterable, facetable, sortable) when required. Each attribute increases index size and indexing cost.
- **Flatten complex types**: Map nested JSON structures to simple fields or collections where possible.
- **Set retrievable=false for filter-only or sort-only fields**: If a field is used for filtering or sorting but doesn't need to be returned in results, keep it indexed and set `retrievable=false` to reduce on-disk storage and per-GB/month storage cost.
- **Use retrievable-only fields when possible**: For example, fields used only for display (such as image URLs) should not be searchable.
- **Reduce vector dimensions**: Higher-dimensional vectors increase storage and query cost. Use smaller embedding models or quantization when appropriate.
- **Minimize document payload size before indexing**: In the serverless model, indexing cost is influenced by how much data the system processes. Indexing cost includes a `payload_KB` factor. The `payload_KB` factor refers to the size of each document (in kilobytes) sent to the index during indexing. Larger payloads require more compute to process, increasing indexing cost. To reduce cost, remove unnecessary fields, trim long text, and strip HTML or other formatting before indexing so that each document contains only the data required for search.

### Optimize indexing requests

How you send data to the index affects both cost and throughput. More efficient indexing patterns reduce compute (CUs) and improve ingestion performance. Larger payloads and more frequent indexing requests both increase compute consumption, so batching and incremental updates are key optimization strategies.

- **Use larger batches when possible**: Batch indexing reduces per-request overhead by amortizing network and processing costs across more documents. In general, batches of up to ~1,000 documents or ~16 MB are more CU-efficient than many small requests. However, optimal batch size depends on your workload—test to balance throughput, latency, and reliability.

- **Index only new or changed data**: Avoid full reindexing when possible. Sending only additions and updates reduces the number of documents processed, lowering compute cost and improving ingestion speed.

- **Use change detection for incremental indexing**: Detect what changed before you reprocess content. Incremental indexing avoids repeated work on unchanged documents and keeps reprocessing costs down.

- **Skip image extraction unless you need it**: Image extraction adds extra processing work and can become a separate cost driver. Turn it on only for documents or workflows that actually need image content.

- **Target skills to relevant fields and documents**: Scope enrichment skills to the specific fields or documents they need. Avoid running skills across content that doesn't need enrichment, especially when the outputs aren't used downstream.

- **Account for index size growth**: Indexing cost increases as the index grows, because more data must be maintained and updated. While the increase isn’t strictly linear, larger indexes require more compute per operation. For very large datasets, consider partitioning data across multiple indexes to improve performance and control costs.

For more guidance, see [Tips for better performance in Azure AI Search](./search-performance-tips.md).

### Optimize your queries

Query design is a primary driver of variable cost:

- **Use `$select` to limit returned fields**: This reduces the payload size and compute required for serialization.

    ```rest
    GET /docs?search=test&$select=id,title,url
    ```

- **Use `searchFields` to limit where text is searched**: Restrict query-time matching to the fields that matter for the scenario. Each additional searchable field increases query work and can increase CUs/hr.

- **Prefer exact match or simple keyword queries**: Fuzzy, wildcard, regex, and prefix-style queries can force broad index scans and consume significantly more CUs/hr. Use them only when you need partial matching behavior and choose exact match or simpler keyword queries wherever possible.

- **Use lookups instead of searches when possible**: Retrieving a document by ID is more efficient than running a search query. If you know the document ID, use a lookup instead of a search query. Lookups are more efficient because they retrieve a document directly by key, while search queries invoke the full query pipeline (parsing, index traversal, scoring, and ranking), which increases compute cost.

- **Avoid deep paging (`$skip`)**: Large `$skip` values increase compute because the engine must process and rank all preceding results (for example, `$skip=5000` requires scoring at least 5,000 documents that aren’t returned). This wastes compute (CUs) and increases cost. Instead, use filters to narrow results and limit the number returned with `$top`. Right-size `$top` to match your UI display. For example, `$top=10` costs less than `$top=50` because fewer results are scored and returned. Only request as many results as your application needs, and avoid patterns that require the engine to process large numbers of unused results.

- **Minimize facet count and facet scope**: Request only the facets that are displayed in your UI, and keep each facet `count` value as low as practical. Facets require per-query aggregations, and high counts increase compute cost.

- **Use `search.in` for filtering**: When filtering by a list of IDs or values, use the `search.in` function instead of multiple `or` conditions (for example, `id eq '1' or id eq '2'`). This approach is more efficient and reduces compute overhead. You should also avoid marking high-cardinality fields (those with a large number of unique values, such as unique IDs or free-text descriptions) as filterable or facetable unless required, as this increases index size and query cost.

## Optimize vector costs

Vector workloads are typically the highest-cost component in serverless search because they impact both compute (queries and indexing) and storage (vector size on disk). To reduce cost, optimize both how vectors are stored and how they’re queried.

### Optimize vector storage and schema

Vector fields can significantly increase index size and indexing cost. Use the following techniques to reduce storage overhead:

- **Use compression to reduce vector size**: Apply quantization to reduce storage footprint with minimal relevance impact. For example, scalar quantization can reduce vector storage by up to 4× with minimal impact on search quality.

- **Disable storage for vectors when not needed**: Set stored=false on vector fields if you only need vectors for search, not retrieval. This avoids storing the original vectors in the index, reducing storage cost without affecting query behavior.

- **Use smaller embedding dimensions when possible**: Higher-dimensional vectors increase both storage and query cost. For non-critical workloads, use smaller embedding models (for example, 384 or 768 dimensions instead of 1536) to reduce cost.

### Optimize vector query execution

Vector queries are compute-intensive because they require similarity calculations over high-dimensional data structures.

- **Use hybrid search selectively**: Hybrid queries run both keyword and vector retrieval. Use only when necessary for relevance.

- **Apply filters before vector queries**: Narrow the candidate set before vector search to reduce the amount of data processed. See [How filtering works in vector queries](./vector-search-filters.md#how-filtering-works-in-vector-queries).

## Reduce costs by minimizing usage

The serverless model charges only for resources consumed. When there are no requests, compute usage drops accordingly.

To minimize usage costs:

- Run queries only when needed.
- Avoid redundant or overly frequent requests.
- Monitor usage and tune workloads based on demand.

> [!TIP]
> The same query can have different latency and CU profiles depending on whether the service is warm or cold. After a period with no read or write traffic, serverless compute usage drops to zero. The next request might have higher latency and consume more CUs while data paths warm up. Larger indexes generally take longer to warm than smaller indexes, so cold-start effects are often more noticeable on larger services.

Serverless is most cost-effective for workloads with variable, intermittent, or unpredictable traffic, where provisioned capacity would be underutilized.

## Optimize storage costs

Storage is billed per GB/month based on on-disk index size, which can exceed raw data size.
To reduce storage costs:

- Remove unused indexes.
- Minimize stored fields.
- Design schemas with storage overhead in mind.
- Use suggesters selectively because they can dramatically increase storage size.

For vector-specific techniques (compression, pruning, and storage settings), see [Optimize for vector storage and processing](./vector-search-how-to-configure-compression-storage.md).

For more guidance on storage and query performance tradeoffs, see [Tips for better performance in Azure AI Search](./search-performance-tips.md).
