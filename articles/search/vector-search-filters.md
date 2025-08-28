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

Filters apply to `filterable` *nonvector* fields, either string or numeric, to include or exclude search documents based on filter criteria. Although vector fields aren't filterable, you can use filters on nonvector fields in the same index to include or exclude documents that contain vector fields you're searching on.

If your index lacks suitable text or numeric fields, check for document metadata that might be useful in filtering, such as `LastModified` or `CreatedBy` properties.

The `vectorFilterMode` parameter controls when the filter is applied in the vector search process, with `k` setting the maximum number of nearest neighbors to return. Depending on the filter mode and how selective your filter is, more than `k` results might be returned.

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

In this example, the vector is a numeric representation of the following query string: "what Azure services support full text search". The query targets the `contentVector` field.

The filter criteria apply to `category`, a filterable text field. Because the `preFilter` mode is used, the filter is applied before the search engine runs the query, so only documents in the `Databases` category are considered during the vector search.

## Set the filter mode

The `vectorFilterMode` parameter determines when and how the filter is applied relative to vector query execution. There are three modes:

+ `preFilter` (default)
+ `postFilter`
+ `strictPostFilter` (preview)

### [preFilter](#tab/prefilter-mode)

Prefiltering applies filters before query execution, which reduces the candidate set for the vector search algorithm. The top-`k` results are then selected from this filtered set.

In a vector query, `preFilter` is the default mode.

:::image type="content" source="media/vector-search-filters/pre-filter.svg" alt-text="Diagram of prefilters." border="true" lightbox="media/vector-search-filters/pre-filter.png":::

### [postFilter](#tab/postfilter-mode)

Postfiltering applies filters after query execution, which narrows the search results. This mode processes results within each segment and then merges the filtered results from all segments to produce the top-`k` results. As a result, you might receive documents that match the filter but aren't among the global top-`k` results.

In a vector query, use `postFilter` for this task.

:::image type="content" source="media/vector-search-filters/post-filter.svg" alt-text="Diagram of post-filters." border="true" lightbox="media/vector-search-filters/post-filter.png":::

### [strictPostFilter (preview)](#tab/strictpostfilter-mode)

Strict postfiltering applies filters after identifying the global top-`k` results. This mode guarantees that the filtered results are always a subset of the unfiltered top `k`.

With strict postfiltering, highly selective filters or small `k` values can return zero results (even if matches exist) because only documents that match the filter within the global top `k` are returned. Don't use this mode if missing relevant results could have serious consequences, such as in healthcare or patent searches.

In a vector query, use `strictPostFilter` and the latest preview version of the [Search Service REST APIs](/rest/api/searchservice/search-service-api-versions) for this task.

---

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
