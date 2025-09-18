---
title: Vector Query Filters
titleSuffix: Azure AI Search
description: Learn how to add filter expressions to vector queries in Azure AI Search. Configure prefilter, postfilter, and strict postfilter (preview) modes to optimize query performance and improve search results.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  + ignite-2023
ms.topic: how-to
ms.date: 09/16/2025
---

# Add a filter to a vector query in Azure AI Search

> [!NOTE]
> `strictPostFilter` is currently in public preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> `prefilter` and `postfilter` are generally available in the [latest stable REST API version](/rest/api/searchservice/search-service-api-versions).

In Azure AI Search, you can use a [filter expression](search-filters.md) to add inclusion or exclusion criteria to a [vector query](vector-search-how-to-query.md). You can also specify a filtering mode that applies the filter:

+ Before query execution, known as *prefiltering*.
+ After query execution, known as *postfiltering*.
+ After the global top-`k` results are identified, known as *strict postfiltering* (preview).

This article uses REST for illustration. For code samples in other languages and end-to-end solutions that include vector queries, see the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) GitHub repository.

You can also use [Search Explorer](search-get-started-portal-import-vectors.md#check-results) in the Azure portal to query vector content. In the JSON view, you can add filters and specify the filter mode.

## How filtering works in vector queries

Azure AI Search uses the Hierarchical Navigable Small World (HNSW) algorithm for Approximate Nearest Neighbor (ANN) search, storing HNSW graphs across multiple shards. Each shard contains a portion of the entire index.

Filters apply to `filterable` *nonvector* fields, either string or numeric, to include or exclude search documents based on filter criteria. Vector fields themselves aren't filterable, but you can use filters on other fields in the same index to narrow the documents considered for vector search. If your index lacks suitable text or numeric fields, check for document metadata that might help with filtering, such as `LastModified` or `CreatedBy` properties.

The `vectorFilterMode` parameter controls where filter operations are applied during the stages of search, which affects how the results are filtered to a subset of items (such as by category, tag, or other attributes) and impacts latency, recall, and throughput. There are three modes:

+ `preFilter` applies the filter *during* HNSW traversal on each shard. This mode maximizes recall but can traverse more of the graph, increasing CPU and latency for highly selective filters.

+ `postFilter` runs HNSW traversal and filtering on each shard independently, intersects results at the shard level, and then aggregates the top `k` from each shard into a global top `k`. This mode can create false negatives for highly selective filters or small `k` values.

+ `strictPostFilter` (preview) finds the unfiltered global top `k` *before* applying the filter. This mode has the highest risk of returning false negatives for highly selective filters and small `k` values.

For more information about these modes, see [Set the filter mode](#set-the-filter-mode).

## Define a filter

Filters determine the scope of vector queries and are defined using [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post). Unless you want to use a preview feature, use the latest stable version of the [Search Service REST APIs](/rest/api/searchservice/search-service-api-versions) to formulate the request.

This REST API provides:

+ `filter` for the criteria.
+ `vectorFilterMode` to specify when the filter is applied during the vector query. For supported modes, see [Set the filter mode](#set-the-filter-mode).

```http
POST https://{search-endpoint}/indexes/{index-name}/docs/search?api-version={api-version}
Content-Type: application/json
api-key: {admin-api-key}
    
{
    "count": true,
    "select": "title, content, category",
    "filter": "category eq 'Databases'",
    "vectorFilterMode": "preFilter",
    "vectorQueries": [
        {
            "kind": "vector",
            "vector": [
                -0.009154141,
                0.018708462,
                . . . // Trimmed for readability
                -0.02178128,
                -0.00086512347
            ],
            "fields": "contentVector",
            "k": 50
        }
    ]
}
```

In this example, the vector embedding targets the `contentVector` field, and the filter criteria apply to `category`, a filterable text field. Because the `preFilter` mode is used, the filter is applied before the search engine runs the query, so only documents in the `Databases` category are considered during the vector search.

## Set the filter mode

The `vectorFilterMode` parameter determines when and how the filter is applied relative to vector query execution. You can use the following modes:

+ `preFilter` (recommended)
+ `postFilter`
+ `strictPostFilter` (preview)

> [!NOTE]
> `preFilter` is the default for indexes created after approximately October 15, 2023. For indexes created before this date, `postFilter` is the default. To use `preFilter` and other advanced vector features, such as vector compression, you must recreate your index.
>
> You can test compatibility by sending a vector query with `"vectorFilterMode": "preFilter"` on the `2023-10-01-preview` REST API version or later. If the query fails, your index doesn't support `preFilter`.

### [preFilter](#tab/prefilter-mode)

Prefiltering applies filters before query execution, which reduces the candidate set for the vector search algorithm. The top-`k` results are then selected from this filtered set.

In a vector query, `preFilter` is the default mode because it favors recall and quality over latency.

#### How this mode works

1. On each shard, apply the filter predicate *during* HNSW traversal, expanding the graph until `k` candidates are found.

1. Produce the prefiltered local top-`k` results per shard.

1. Aggregate the filtered results into a global top-`k` result set.

#### Effect of this mode

Traversal expands the search surface to find more filtered candidates, especially if the filter is selective. This produces the most similar top-`k` results across all shards. Each shard identifies the `k` results that satisfy the filter predicate.

Prefiltering guarantees that `k` results are returned if they exist in the index. For highly selective filters, this can cause a significant portion of the graph to be traversed, increasing computation cost and latency while reducing throughput. If your filter is highly selective (has very few matches), consider using `exhaustive: true` to perform exhaustive search.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-prefilter.svg" alt-text="Diagram of prefilters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-prefilter.png":::

### [postFilter](#tab/postfilter-mode)

Postfiltering applies filters after query execution, which narrows the search results. This mode processes results within each shard and then merges the filtered results from all shards to produce the top-`k` results. As a result, you might receive documents that match the filter but aren't among the global top-`k` results.

To use this mode in a vector query, use `"vectorFilterMode": "postFilter"`.

> [!TIP]
> For both postfiltering modes, use a higher `k` and the `top` parameter to reduce false negatives. Avoid postfiltering with highly selective filters, as it might not return enough matching documents.

#### How this mode works

1. On each shard, run HNSW traversal *without considering the filter* to identify the unfiltered local top-`k` results.

1. Apply the filter predicate on the unfiltered top-`k` results for each shard. This reduces the contribution from each shard to be potentially fewer than `k` results.

1. Aggregate the filtered results into the global top-`k` results.

#### Effect of this mode

Traversal occurs independently of the filter expression. However, because the intersection happens *after* the top-`k` results are identified, some matching documents that are less similar than the top-`k` unfiltered documents never appear in the search results.

For highly selective filters, postfiltering can reduce recall and produce false negatives, meaning fewer matching documents are returned than are in the index. However, latency and throughput are more predictable because the traversal cost isn't correlated with filter selectivity, but rather with filter execution cost.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-postfilter.svg" alt-text="Diagram of postfilters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-postfilter.png":::

### [strictPostFilter (preview)](#tab/strictpostfilter-mode)

Strict postfiltering applies filters after identifying the global top-`k` results. This mode guarantees that the filtered results are always a subset of the unfiltered top `k`.

With strict postfiltering, highly selective filters or small `k` values can return zero results (even if matches exist) because only documents that match the filter within the global top `k` are returned. Don't use this mode if missing relevant results could have serious consequences, such as in healthcare or patent searches.

To use this mode in a vector query, use `"vectorFilterMode": "strictPostFilter"` with the latest preview version of the [Search Service REST APIs](/rest/api/searchservice/search-service-api-versions).

> [!TIP]
> For both postfiltering modes, use a higher `k` and the `top` parameter to reduce false negatives. Avoid postfiltering with highly selective filters, as it might not return enough matching documents.

#### How this mode works

1. On each shard, run HNSW traversal *without considering the filter* to identify the unfiltered local top-`k` results.

1. Aggregate the local top-`k` results per shard into an unfiltered global top-`k` result set.

1. Apply the filter to the global top-`k` result set.

1. Return the subset that satisfies the filter predicate.

#### Effect of this mode

Applying a filter *always* reduces the set of results to be fewer than `k` if some documents don't satisfy the filter. If qualifying items aren't present in the global top-`k` results, this mode never surfaces them.

Strict postfiltering is useful for faceted navigation because it ensures that applying more selective filters never increases the number of results. This increases the consistency of facet bucket counts and search counts. However, it can result in false negatives or zero results.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-strictpostfilter.svg" alt-text="Diagram of strict postfilters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-strictpostfilter.png":::

---

### Comparison table

| Mode | Recall (filtered results) | Computational cost | Risk of false negatives | When to use |
|--|--|--|--|--|
| `preFilter` | Very high | Higher (increases with filter selectivity and complexity) | No risk | **Recommended default for all scenarios**, especially when recall is critical (sensitive search domains), when using selective filters, or when using small `k`. |
| `postFilter` | Medium to high (decreases with filter selectivity) | Similar to unfiltered but increases with filter complexity | Moderate (can miss matches per shard) | An option for filters that aren't too selective and for higher-`k` queries. |
| `strictPostFilter` | Lowest (decreases most quickly with filter selectivity) | Similar to unfiltered | Highest (can return zero results for selective filters or small `k`) | An option for faceted search applications where surfacing more results after filter application impacts the user experience more than the risk of false negatives. Don't use with small `k`. |

### Benchmark testing of prefiltering and postfiltering

> [!IMPORTANT]
> This section applies to prefiltering and postfiltering, not strict postfiltering.

To understand the conditions under which one filter mode performs better than the other, we ran a series of tests to evaluate query outcomes over small, medium, and large indexes.

+ Small (100,000 documents, 2.5-GB index, 1,536 dimensions)
+ Medium (1 million documents, 25-GB index, 1,536 dimensions)
+ Large (1 billion documents, 1.9-TB index, 96 dimensions)

For the small and medium workloads, we used a Standard 2 (S2) service with one partition and one replica. For the large workload, we used a Standard 3 (S3) service with 12 partitions and one replica.

Indexes had an identical construction: one key field, one vector field, one text field, and one numeric filterable field. The following index is defined using the `2023-11-03` syntax.

```python
def get_index_schema(self, index_name, dimensions):
    return {
        "name": index_name,
        "fields": [
            {"name": "id", "type": "Edm.String", "key": True, "searchable": True},
            {"name": "content_vector", "type": "Collection(Edm.Single)", "dimensions": dimensions,
              "searchable": True, "retrievable": True, "filterable": False, "facetable": False, "sortable": False,
              "vectorSearchProfile": "defaulthnsw"},
            {"name": "text", "type": "Edm.String", "searchable": True, "filterable": False, "retrievable": True,
              "sortable": False, "facetable": False},
            {"name": "score", "type": "Edm.Double", "searchable": False, "filterable": True,
              "retrievable": True, "sortable": True, "facetable": True}
        ],
      "vectorSearch": {
        "algorithms": [
            {
              "name": "defaulthnsw",
              "kind": "hnsw",
              "hnswParameters": { "metric": "euclidean" }
            }
          ],
          "profiles": [
            {
              "name": "defaulthnsw",
              "algorithm": "defaulthnsw"
            }
        ]
      }
    }
```

In queries, we used an identical filter for both prefilter and postfilter operations. We used a simple filter to ensure that variations in performance were due to filtering mode, not filter complexity.

Outcomes were measured in queries per second (QPS).

### Takeaways

+ Prefiltering is almost always slower than postfiltering, except on small indexes where performance is approximately equal.

+ On larger datasets, prefiltering is orders of magnitude slower.

+ Why is prefilter the default if it's almost always slower? Prefiltering guarantees that `k` results are returned if they exist in the index, where the bias favors recall and precision over speed.

+ Use postfiltering if you:

  + Value speed over selection (postfiltering can return fewer than `k` results).

  + Use filters that aren't overly selective.

  + Have indexes of sufficient size such that prefiltering performance is unacceptable.

### Details

+ Given a dataset with 100,000 vectors at 1,536 dimensions:

  + When filtering more than 30% of the dataset, prefiltering and postfiltering were comparable.

  + When filtering less than 0.1% of the dataset, prefiltering was about 50% slower than postfiltering.

+ Given a dataset with 1 million vectors at 1,536 dimensions:

  + When filtering more than 30% of the dataset, prefiltering was about 30% slower.

  + When filtering less than 2% of the dataset, prefiltering was about seven times slower.

+ Given a dataset with 1 billion vectors at 96 dimensions:

  + When filtering more than 5% of the dataset, prefiltering was about 50% slower.

  + When filtering less than 10% of the dataset, prefiltering was about seven times slower.

The following graph shows prefilter relative QPS, computed as prefilter QPS divided by postfilter QPS.

:::image type="content" source="media/vector-search-filters/chart.svg" alt-text="Chart showing QPS performance for small, medium, and large indexes for relative QPS." border="true" lightbox="media/vector-search-filters/chart.png":::

The vertical axis represents the relative performance of prefiltering compared to postfiltering, expressed as a ratio of QPS (queries per second). For example:

+ A value of `0.0` means prefiltering is 100% slower than postfiltering.
+ A value of `0.5` means prefiltering is 50% slower.
+ A value of `1.0` means prefiltering and post filtering are equivalent.

The horizontal axis represents the filtering rate, or the percentage of candidate documents after applying the filter. For example, a rate of `1.00%` means the filter criteria selected one percent of the search corpus.

## Related content

+ [Vector search in Azure AI Search](vector-search-overview.md)
+ [Create a vector index](vector-search-how-to-create-index.md)
+ [Create a vector query](vector-search-how-to-query.md)
