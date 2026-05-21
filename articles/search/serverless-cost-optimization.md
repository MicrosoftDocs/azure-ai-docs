---
title: Optimize costs for Azure AI Search Serverless
description: Learn how to reduce costs for the Serverless pricing model in Azure AI Search costs by tuning compute usage, managing on-disk index storage, and tracking separately billed features.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 06/02/2026
ai-usage: ai-assisted
# customer intent: As a developer or product engineer, I want to understand the details behind how the Azure AI Search Serverless pricing model works so that I can optimize my search service to use the most efficient pricing model suited to my needs and only pay for what I use.
---

# Optimize costs for the Serverless pricing model in Azure AI Search

Azure AI Search supports two pricing models, each designed for different workload patterns:

- **Dedicated**: Fixed pricing measured by Search Units (SUs). You select a service tier, and you're billed hourly based on provisioned units.

- **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage.

> [!IMPORTANT]
> The Serverless pricing model is currently available to try at no cost during this early preview period. Usage-based billing will begin prior to the end of the public preview with details provided at least 30-days in advance.

For more information about pricing model and service tier differences, see [Choose a pricing model and service tier](search-sku-tier.md).

## How cost is determined in the Serverless model

In the Serverless model, **performance optimization directly affects cost**. Cost is directly tied to workload execution:

- Queries and indexing consume compute, measured in Compute Units per hour (CU/h).
- Storage is billed separately based on index size on disk.
- When the service is idle with no active queries or indexing, compute usage is zero. There's no reserved or minimum capacity charge.

The Serverless pricing model is most cost-effective for workloads with variable, intermittent, or unpredictable traffic, where provisioned capacity would be underutilized.

> [!IMPORTANT]
> Your Compute Unit per hour (CU/h) charges don't include semantic ranker, agentic retrieval, image extraction and skill exectuion. These capabilities are billed separately.

## Understand Compute Units (CUs)

A Compute Unit (CU) represents the measured system resources required to perform search and indexing operations in the Serverless model. CU cost is driven primarily by CPU, memory, and IO utilization and secondarily by Index size and document payload size with usage being billed as Compute Unit per hour (CU/h).

Compute cost scales with:

- Query complexity
- Index size (GB) and structure
- Document payload size (KB)
- Number of fields and retrieved results

Different operations have different cost profiles:

- **Lookup**: Low cost. Retrieving a single document by its ID is the most efficient operation.
- **Keyword search**: Low cost. Text search uses inverted indexes, which are optimized for speed and low compute usage.
- **Vector search**: High cost. Vector queries are computationally expensive because they require similarity calculations across high-dimensional embeddings. Compared to keyword search, they consume significantly more compute.
- **Hybrid search**: Combines the cost of keyword and vector search, as both pipelines run for each query, plus a small additional overhead for Reciprocal Rank Fusion (RRF) to merge results.

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

This value represents the compute consumed by the request and can be used to identify high-cost query patterns. In this example, the query consumed 12.45 mCU per minute.

You can also use the metrics in the portal to understand the historical consumption. See [Monitoring Data Reference](monitor-azure-cognitive-search-data-reference.md#supported-metrics-for-microsoftsearchsearchservices).

:::image type="content" source="media/serverless/serverless-monitor-compute-units.png" alt-text="Screenshot of monitoring Compute Unit usage in the Azure AI Search service portal." border="true":::

Additionally, you can use [Azure Monitor logs](search-monitor-queries.md) to track aggregate CU usage over time and correlate it with query volume and workload changes.

> [!NOTE]
> The Azure pricing calculator and SU-based capacity-planning worksheets don't apply to the Serverless pricing model services. To estimate Serverless costs, index a representative sample of your data, run typical queries, and inspect the `x-ms-request-charge` header to measure actual CU consumption per operation type. Extrapolate to your expected volume using telemetry and the Azure portal to estimate costs.
> The aggregate usage is measured each minute, converting from mCU to CU (divide by 1000) and from CU/min to CU/h (divide by 60), and then emitted to the meter each minute. If a minute has no usage, nothing is emitted.
> To calculate the full CU/h amount that appears on the bill, usage is measured per minute and rounded up to the nearest 0.25 CU/minute, with 60 of these per minute segments added up over the period of an hour to calculate the full CU/h amount that appears on the bill. CU costs are consistent - the same request on the same data produces similar CU consumption. The relative cost of different operation types follows this general pattern: keyword search (low) < vector search (higher) < hybrid search (combined cost of both).

## Reduce compute costs through optimization

Efficient queries and index design reduce compute consumption and lower costs.

### Optimize your schema

Your index schema determines baseline compute and storage costs:

- **Limit field attributes**: Only enable attributes (searchable, filterable, facetable, sortable) when required. Each attribute increases index size and indexing cost.
- **Flatten complex types**: Map nested JSON structures to simple fields or collections where possible.
- **Set retrievable=false for filter-only or sort-only fields**: If a field is used for filtering or sorting but doesn't need to be returned in results, keep it indexed and set `retrievable=false` to reduce on-disk storage and per-GB/month storage cost.
- **Use retrievable-only fields when possible**: For example, fields used only for display (such as image URLs) should not be searchable.
- **Reduce vector dimensions**: Higher-dimensional vectors increase storage and query cost. Use smaller embedding models or quantization when appropriate.
- **Minimize document payload size before indexing**: Larger documents cost more to index. Remove unnecessary fields, trim long text, and strip HTML before sending documents to the index.

### Optimize indexing requests

How you send data to the index affects both cost and throughput:

- **Use larger batches when possible**: Batch indexing reduces per-request overhead by amortizing network and processing costs across more documents. In general, batches of up to ~1,000 documents or ~16 MB are more CU-efficient than many small requests. However, optimal batch size depends on your workload. Test to balance throughput, latency, and reliability.

- **Index only new or changed data**: Avoid full reindexing when possible. Sending only additions and updates reduces the number of documents processed, lowering compute cost and improving ingestion speed.

- **Use change detection for incremental indexing**: Detect what changed before you reprocess content. Incremental indexing avoids repeated work on unchanged documents and keeps reprocessing costs down.

- **Skip image extraction unless you need it**: Image extraction adds extra processing work and can become a separate cost driver. Turn it on only for documents or workflows that actually need image content.

- **Target skills to relevant fields and documents**: Scope enrichment skills to the specific fields or documents they need. Avoid running skills across content that doesn't need enrichment, especially when the outputs aren't used downstream.

- **Account for index size growth**: Where possible, create smaller indexes. As an index grows, indexing costs increase because more data must be stored and maintained, and operations require more compute. For very large datasets, consider partitioning data across multiple indexes to help manage performance and costs. Although costs rise with index size, the increase is sublinear. Larger indexes cost more per operation, but not proportionally more.

For more guidance, see [Tips for better performance in Azure AI Search](./search-performance-tips.md).

### Optimize your queries

Query design is a primary driver of variable cost:

- **Use `$select` to limit returned fields**: This reduces the payload size and compute required for serialization.

    ```rest
    GET /docs?search=test&$select=id,title,url
    ```

- **Use `searchFields` to limit where text is searched**: Restrict query-time matching to the fields that matter for the scenario. Each additional searchable field increases query work and can increase CU/h.

- **Prefer exact match or simple keyword queries**: Fuzzy, wildcard, regex, and prefix-style queries can force broad index scans and consume significantly more CU/h. Use them only when you need partial matching behavior and choose exact match or simpler keyword queries wherever possible.

- **Use lookups instead of searches when possible**: Retrieving a document by ID is more efficient than running a search query. If you know the document ID, use a lookup instead of a search query. Lookups are more efficient because they retrieve a document directly by key, while search queries invoke the full query pipeline (parsing, index traversal, scoring, and ranking), which increases compute cost.

- **Avoid deep paging (`$skip`)**: Large `$skip` values increase compute because the engine must process and rank all preceding results (for example, `$skip=5000` requires scoring at least 5,000 documents that aren’t returned). This wastes compute (CUs) and increases cost. Instead, use filters to narrow results and limit the number returned with `$top`. Right-size `$top` to match your UI display. For example, `$top=10` costs less than `$top=50` because fewer results are scored and returned. Only request as many results as your application needs, and avoid patterns that require the engine to process large numbers of unused results.

- **Minimize facet count and facet scope**: Request only the facets that are displayed in your UI, and keep each facet `count` value as low as practical. Facets require per-query aggregations, and high counts increase compute cost.

- **Use `search.in` for filtering**: When filtering by a list of IDs or values, use the `search.in` function instead of multiple `or` conditions (for example, `id eq '1' or id eq '2'`). This approach is more efficient and reduces compute overhead. You should also avoid marking high-cardinality fields (those with a large number of unique values, such as unique IDs or free-text descriptions) as filterable or facetable unless required, as this increases index size and query cost.

### Optimize your administrative requests

In addition to query and indexing operations, Azure AI Search includes object-level and service-level administrative operations (such as retrieving index schemas or service statistics). These requests have a flat per-request cost. While each request is inexpensive, repeated or unnecessary calls can accumulate over time and increase overall compute usage.

- **Avoid excessive administrative requests**: Cache metadata, such as index schemas, on the client side instead of retrieving it repeatedly. For example, fetching the index schema before every write operation introduces unnecessary cost. In the Serverless model, this pattern directly increases compute charges, whereas in Dedicated services, the impact is often hidden by fixed hourly billing.

### Optimize vector costs

Vector workloads are typically the highest-cost component in search for the Serverless pricing model because they impact both Compute Units (queries and indexing) and storage (vector size on disk). To reduce cost, optimize both how vectors are stored and how they’re queried.

#### Optimize vector storage and schema

Vector fields can significantly increase index size and indexing cost. Use the following techniques to reduce storage overhead:

- **Use compression to reduce vector size**: Apply quantization to reduce storage footprint with minimal relevance impact. For example, scalar quantization can reduce vector storage by up to 4× with minimal impact on search quality.

- **Disable storage for vectors when not needed**: Set stored=false on vector fields if you only need vectors for search, not retrieval. This avoids storing the original vectors in the index, reducing storage cost without affecting query behavior.

- **Use smaller embedding dimensions when possible**: Higher-dimensional vectors increase both storage and query cost. For non-critical workloads, use smaller embedding models (for example, 384 or 768 dimensions instead of 1536) to reduce cost.

#### Optimize vector query execution

Vector queries are compute-intensive because they require similarity calculations over high-dimensional data structures.

- **Use hybrid search selectively**: Hybrid queries run both keyword and vector retrieval. Use only when necessary for relevance.

- **Apply filters before vector queries**: Narrow the candidate set before vector search to reduce the amount of data processed. See [How filtering works in vector queries](./vector-search-filters.md#how-filtering-works-in-vector-queries).

## Reduce costs by minimizing usage

The Serverless model charges only for resources consumed. When there are no requests, compute usage drops accordingly.

To minimize usage costs:

- Run queries only when needed.
- Avoid redundant or overly frequent requests.
- Monitor usage and tune workloads based on demand.

> [!TIP]
> The same query can have different latency and CU profiles depending on whether the service is warm or cold. After a period with no read or write traffic, compute usage in the Serverless pricing model drops to zero. The next request might have higher latency and consume more CUs while data paths warm up. Larger indexes generally take longer to warm than smaller indexes, so cold-start effects are often more noticeable on larger services.

## Optimize storage costs

Storage is billed per GB/month based on on-disk index size, which can exceed raw data size.
To reduce storage costs:

- Remove unused indexes.
- Minimize stored fields.
- Design schemas with storage overhead in mind.
- Use suggesters selectively because they can dramatically increase storage size.

For vector-specific techniques (compression, pruning, and storage settings), see [Optimize for vector storage and processing](./vector-search-how-to-configure-compression-storage.md).

For more guidance on storage and query performance tradeoffs, see [Tips for better performance in Azure AI Search](./search-performance-tips.md).
