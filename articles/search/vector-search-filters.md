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
ms.date: 08/28/2025
---

# Add a filter to a vector query in Azure AI Search

> [!NOTE]
> `strictPostFilter` is currently in public preview. This preview is provided without a service-level agreement and isn't recommended for production workloads. Certain features might not be supported or might have constrained capabilities. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> `prefilter` and `postfilter` are generally available in the [latest stable REST API version](/rest/api/searchservice/search-service-api-versions).

In Azure AI Search, you can use a [filter expression](search-filters.md) to add inclusion or exclusion criteria to a vector query. You can also specify a filtering mode that applies the filter:

+ Before query execution, known as *prefiltering*.
+ After query execution, known as *postfiltering*.
+ After the global top-`k` results are identified, known as *strict postfiltering* (preview).

This article uses REST for illustration. For code samples in other languages and end-to-end solutions that include vector queries, see the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) GitHub repository.

You can also use [Search Explorer](search-get-started-portal-import-vectors.md#check-results) in the Azure portal to query vector content. If you use the JSON view, you can add filters and specify the filter mode.

## How filtering works in vector queries

When performing Approximate Nearest Neighbor (ANN) search using **Hierarchical Navigable Small World (HNSW)** algorithm, Azure AI Search stores HNSW graphs across multiple shards. Each shard contains a portion of the entire index. The different filtering options control where filter operations are applied within the stages of search, which will affect how the results are filtered down to a subset of items (e.g., by category, tag, or other attributes) and impact latency, recall, and throughput.

Filters apply to `filterable` *nonvector* fields, either string or numeric, to include or exclude search documents based on filter criteria. Although vector fields themselves aren't filterable, you can use filters on nonvector fields in the same index to include or exclude documents that contain vector fields you're searching on.

If your index lacks suitable text or numeric fields, check for document metadata that might be useful in filtering, such as `LastModified` or `CreatedBy` properties.

The `vectorFilterMode` parameter controls when the filter is applied in the vector search process, with `k` setting the maximum number of nearest neighbors to return. Depending on the filter mode and how selective your filter is, fewer than `k` results might be returned.

Azure AI Search supports three types of filtering during vector search: `preFilter` (default), `postFilter`, and `strictPostFilter`. 

> [!NOTE]
> On older indexes created before approximately October 15, 2023, `preFilter` is not available. For these indexes, `postFilter` will be the default. In order to use `preFilter` and other advanced vector features, such as vector compression, you will need to recreate your index. You can test compatibility by sending a vector query with `vectorFilterMode: preFilter` on API version later than `2023-10-01-preview` and observe whether it fails.

In summary, the three approaches are described below:
* **Pre-filter:** apply the predicate *during* HNSW traversal on each shard. Highest recall for filtered queries, but may traverse more of the graph (higher CPU/latency) when the filter has high selectivity.
* **Post-filter:** run the HNSW traversal and the filtering independently on each shard, then intersect results at shard level, and aggregate top-k from each shard into a global top-k. For higher selectivity filters or small `k`, this can create false negatives.
* **Strict post-filter:** run HNSW traversal to find the unfiltered global top-k, then apply the filter. Highest chance of returning false negatives when `k` is small or the filter has high selectivity.

For both *post-filtering* options, instead of controlling the number of results only using `k`, it is recommended to control it using `top` and increase `k`, because this reduces the likelihood of false negatives. It is also recommended to avoid both post-filtering options for high-selectivity filters (which match very few documents) because the initial set of candidates may not surface enough documents which satisfy the filter.

## Define a filter

Filters determine the scope of vector queries and are defined using [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post). Unless you want to use a preview feature, use the latest stable version of the [Search Service REST APIs](/rest/api/searchservice/search-service-api-versions) to formulate the request.

This REST API provides:

+ `filter` for the criteria.
+ `vectorFilterMode` for pre-query or post-query filtering. For supported modes, see the [next section](#set-the-filter-mode).

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
                "exhaustive": true,
                "fields": "contentVector",
                "k": 5
            }
        ]
    }
```

In this example, the vector embedding targets the `contentVector` field, and the filter criteria apply to `category`, a filterable text field. Because the `preFilter` mode is used, the filter is applied before the search engine runs the query, so only documents in the `Databases` category are considered during the vector search.

## Understanding Pre-Filter, Post-Filter, and Strict Post-Filter in HNSW Vector Search

The `vectorFilterMode` parameter determines when and how the filter is applied relative to vector query execution. There are three modes:

+ `preFilter` (default for indexes created after approximately October 15, 2023) - **recommended**
+ `postFilter` (default for indexes created before approximately October 15, 2023)
+ `strictPostFilter` (preview)

### Pre-filter

Prefiltering applies filters before query execution, which reduces the candidate set for the vector search algorithm. The top-`k` results are then selected from this filtered set. In a vector query, `preFilter` is the default mode because it favors recall and quality over latency.

1. On each shard, during HNSW traversal, apply the filter predicate when considering candidates, expanding the graph traversal until `k` candidates are found.
1. Pre-filtered local top-k results are produced per shard, which are aggregated into the global top-k. 

**Effect:** Traversal expands the search surface to find more filtered candidates (especially if filter is selective), producing the most similar top-k results across all shards. Each shard will identify `k` number of results which satisfy the filter predicate. Pre-filter guarantees `k` results are returned if they exist in the index. For high selectivity filters, this could cause a significant portion of the graph to be traversed, increasing computation cost and latency and reducing throughput. If your filter has a very high selectivity (very few matches), consider using `exhaustive: true` to perform exhaustive search.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-prefilter.svg" alt-text="Diagram of prefilters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-prefilter.png":::

### Post-filter

Postfiltering applies filters after query execution, which narrows the search results. This mode processes results within each shard and then merges the filtered results from all shards to produce the top-`k` results. As a result, you might receive documents that match the filter but aren't among the global top-`k` results.

To use this option in a vector query, use `"vectorFilterMode": "postFilter"`.

1. On each shard, run HNSW traversal *without considering the filter* to identify the unfiltered local top-k.
1. Apply the filter predicate on the unfiltered top-k result for each shard. Note this will reduce the contribution from each shard to be potentially fewer than `k` results.
1. Aggregate into the global top-k results.

**Effect:** Traversal is performed independently of the filter expression, but because the intersection happens *after* the top-k results are identified, some matching documents that are less similar than the best unfiltered top-k documents will never surface in the search results. For highly selective filters, this can reduce recall or produce false negatives (fewer matching documents returned than actually exist within the index). Latency and throughput is more predictable because traversal cost is not correlated to filter selectivity but rather filter execution cost.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-postfilter.svg" alt-text="Diagram of post-filters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-postfilter.png":::

### Strict Post-filter (preview)

Strict postfiltering applies filters after identifying the global top-`k` results. This mode guarantees that the filtered results are always a subset of the unfiltered top `k`.

With strict postfiltering, highly selective filters or small `k` values can return zero results (even if matches exist) because only documents that match the filter within the global top `k` are returned. Don't use this mode if missing relevant results could have serious consequences, such as in healthcare or patent searches.

To use this option in a vector query, use `"vectorFilterMode": "strictPostFilter"` with the latest preview version of the [Search Service REST APIs](/rest/api/searchservice/search-service-api-versions).

1. On each shard, run HNSW traversal *without considering the filter* to identify the unfiltered local top-k.
1. Aggregate the local top-k results per shard into an unfiltered global top-k result set.
1. Apply the filter to this global top-k. Return the subset that satisfies the filter predicate.

**Effect:** Applying a filter will *always* reduce the set of results to be fewer than `k` if some documents don't satisfy the filter. If qualifying items are not present in the global top-k, this mode will never surface them. This option can be useful when building a facet and filter navigation experience to prevent additional results from surfacing after applying increasingly selective filters and increase consistency of facet bucket counts and search counts, at the expense of potential false negatives or zero results.

:::image type="content" source="media/vector-search-filters/vector-filter-modes-strictpostfilter.svg" alt-text="Diagram of strict post-filters." border="true" lightbox="media/vector-search-filters/vector-filter-modes-strictpostfilter.png":::

## Comparison table

| Mode | Recall (filtered results) | Computational cost | Risk of false negatives | When to use |
| -------- | -------------: | ------------: | ---------------------: | ----------------------------------- |
| Pre-filter  |  Very high | Higher (increases with filter selectivity and complexity) | No false negatives | **(recommended as the default in order to favor recall over speed)** Especially when recall for filtered queries is critical (sensitive search domains), filter is selective, or k is small |
| Post-filter |  Medium-high, reduces with filter selectivity | Similar to unfiltered but increases with filter complexity | Moderate (per-shard misses possible) | Can be an option for higher `k` queries and filters which are not too selective |
| Strict post-filter | Lowest (degrades the fastest with filter selectivity) | Similar to unfiltered | Highest - can return zero results for small k or selective filters | For faceted search applications where surfacing additional results after applying a filter impacts the user experience. Do not use with small `k`. | 

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
