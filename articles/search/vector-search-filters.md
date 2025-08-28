---
title: Vector Query Filters
titleSuffix: Azure AI Search
description: Learn how to add filter expressions to vector queries in Azure AI Search. Configure prefiltering and postfiltering modes to optimize query performance and improve search results.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  + ignite-2023
ms.topic: how-to
ms.date: 07/11/2025
---

# Add a filter to a vector query in Azure AI Search

In Azure AI Search, you can define a vector query request that includes a [filter expression](search-filters.md) to add inclusion or exclusion criteria to your queries. This article explains how to:

> [!div class="checklist"]
> + [Define a `filter` expression](#define-a-filter)
> + [Set the `vectorFilterMode` for pre-query or post-query filtering](#set-the-vectorfiltermode)

This article uses REST for illustration. For code samples in other languages and end-to-end solutions that include vector queries, see the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) GitHub repository.

You can also use [Search Explorer](search-get-started-portal-import-vectors.md#check-results) in the Azure portal to query vector content. If you use the JSON view, you can add filters and specify the filter mode.

## How filtering works in a vector query

Filters apply to `filterable` *nonvector* fields, either string or numeric, to include or exclude search documents based on filter criteria. Although a vector field isn't filterable itself, you can add filters to nonvector fields in the same index to include or exclude documents that also contain vector fields you're searching on.

Filters are applied before or after query execution based on the `vectorFilterMode` parameter.

## Define a filter

Filters determine the scope of a vector query. They're set on and iterate over nonvector string and numeric fields marked as `filterable` in the index. The purpose of a filter determines *what* the vector query executes over: the entire searchable space (prefiltering) or the contents of a search result (postfiltering).

If you don't have source fields with text or numeric values, check for document metadata, such as `LastModified` or `CreatedBy` properties, that might be useful in a metadata filter.

### [**2024-07-01**](#tab/filter-2024-07-01)

[**2024-07-01**](/rest/api/searchservice/search-service-api-versions#2024-07-01) is the stable version of this API. This version has:

+ `vectorFilterMode` for prefilter (default) or postfilter filtering modes.
+ `filter` for the criteria.

In the following example, the vector is a representation of this query string: "what Azure services support full text search". The query targets the `contentVector` field. The actual vector has 1,536 embeddings, so it's trimmed for readability.

The filter criteria are applied to a filterable text field (`category` in this example) before the search engine executes the vector query.

```http
POST https://{{search-service-name}}.search.windows.net/indexes/{{index-name}}/docs/search?api-version=2024-07-01
Content-Type: application/json
api-key: {{admin-api-key}}
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
                . . . 
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

### [**2024-05-01-preview**](#tab/filter-2024-05-01-preview)

[**2024-05-01-preview**](/rest/api/searchservice/search-service-api-versions#2024-05-01-preview) introduces filter options. This version adds:

+ `vectorFilterMode` for prefilter (default) or postfilter filtering modes.
+ `filter` for the criteria.

In the following example, the vector is a representation of this query string: "what Azure services support full text search". The query targets the `contentVector` field. The actual vector has 1,536 embeddings, so it's trimmed for readability.

The filter criteria are applied to a filterable text field (`category` in this example) before the search engine executes the vector query.

```http
POST https://{{search-service-name}}.search.windows.net/indexes/{{index-name}}/docs/search?api-version=2024-05-01-preview
Content-Type: application/json
api-key: {{admin-api-key}}
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
                . . . 
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

---

## Set the vectorFilterMode

The `vectorFilterMode` query parameter determines whether the filter is applied before or after vector query execution.

### [Prefilter mode](#tab/prefilter-mode)

Prefiltering applies filters before query execution, reducing the search surface area over which the vector search algorithm looks for similar content.

In a vector query, `preFilter` is the default.

:::image type="content" source="media/vector-search-filters/pre-filter.svg" alt-text="Diagram of prefilters." border="true" lightbox="media/vector-search-filters/pre-filter.png":::

### [Postfilter mode](#tab/postfilter-mode)

Postfiltering applies filters after query execution, narrowing the search results.

In a vector query, use `postFilter` for this task.

:::image type="content" source="media/vector-search-filters/post-filter.svg" alt-text="Diagram of post-filters." border="true" lightbox="media/vector-search-filters/post-filter.png":::

---

### Benchmark testing of vector filter modes

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
