---
title: Hybrid search
titleSuffix: Azure AI Search
description: Describes concepts and architecture of hybrid query processing and document retrieval. Hybrid queries combine vector search and full text search.

author: robertklee
ms.author: robertlee
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 05/27/2025
---

# Hybrid search using vectors and full text in Azure AI Search

Hybrid search is a single query request, configured for full text and vector search, that executes against a search index containing both searchable plain text content and generated embeddings. For query purposes, hybrid search is:

+ A single query request that includes both `search` and `vectors` query parameters
+ Executing in parallel
+ With merged results in the query response, scored using [Reciprocal Rank Fusion (RRF)](hybrid-search-ranking.md)

This article explains the concepts, benefits, and limitations of hybrid search. Links at the end provide instructions and next steps. You can also watch this [embedded video](#why-choose-hybrid-search) for an explanation of how hybrid retrieval contributes to high quality RAG apps.

## How does hybrid search work?

In Azure AI Search, vector fields containing embeddings can live alongside textual and numerical fields, allowing you to formulate hybrid queries that execute in parallel. Hybrid queries can take advantage of existing text-based functionality like filtering, faceting, sorting, scoring profiles, and [semantic ranking](semantic-search-overview.md) on your text fields, while executing a similarity search against vectors, all in a single search request.

Hybrid search combines results from both full text and vector queries, which use different ranking functions such as BM25 for text, and Hierarchical Navigable Small World (HNSW) and exhaustive K Nearest Neighbors (eKNN) for vectors. A [Reciprocal Rank Fusion (RRF)](hybrid-search-ranking.md) algorithm merges the results. The query response provides just one result set, using RRF to rank the unified results.

## Structure of a hybrid query

Hybrid search is predicated on having a search index that contains fields of various [data types](/rest/api/searchservice/supported-data-types), including plain text and numbers, geo coordinates if you want geospatial search, and vectors for a mathematical representation of a chunk of text. You can use almost all query capabilities in Azure AI Search with a vector query, except for pure text client-side interactions such as autocomplete and suggestions.

A representative hybrid query might be as follows (notice that the vector queries have placeholder values for brevity):

```http
POST https://{{searchServiceName}}.search.windows.net/indexes/hotels-vector-quickstart/docs/search?api-version=2024-07-01
  content-type: application/JSON
{
    "count": true,
    "search": "historic hotel walk to restaurants and shopping",
    "select": "HotelId, HotelName, Category, Description, Address/City, Address/StateProvince",
    "filter": "geo.distance(Location, geography'POINT(-77.03241 38.90166)') le 300",
    "vectorFilterMode": "postFilter",
    "facets": [ "Address/StateProvince"], 
    "vectorQueries": [
        {
            "kind": "vector",
            "vector": [ <array of embeddings> ]
            "k": 50,
            "fields": "DescriptionVector",
            "exhaustive": true,
            "oversampling": 20
        },
        {
            "kind": "vector",
            "vector": [ <array of embeddings> ]
            "k": 50,
            "fields": "Description_frVector",
            "exhaustive": false,
            "oversampling": 10
        }
    ],
    "skip": 0,
    "top": 10,
    "queryType": "semantic",
    "queryLanguage": "en-us",
    "semanticConfiguration": "my-semantic-config"
}
```

Key points include:

+ `search` specifies a single full text search query.
+ `vectorQueries` for vector queries, which can be multiple, targeting multiple vector fields. If the embedding space includes multi-lingual content, vector queries can find the match with no language analyzers or translation required. If you're also using the semantic ranker, set `k` to 50 to maximize its inputs.
+ `select` specifies which fields to return in results, which should be text fields that are human readable if you're showing them to users or sending them to an LLM.
+ `filters` can specify geospatial search or other include and exclude criteria, such as whether parking is included. The geospatial query in this example finds hotels within a 300-kilometer radius of Washington D.C. You can apply the filter at the beginning or end of query processing. If you use the semantic ranker, you probably want post-filtering as the last step but you should test to confirm which behavior is best for your queries.
+ `facets` can be used to compute facet buckets over results that are returned from hybrid queries.
+ `queryType=semantic` invokes semantic ranker, applying machine reading comprehension to surface more relevant search results. Semantic ranking is optional. If you aren't using that feature, remove the last three lines of the hybrid query.

Filters and facets target data structures within the index that are distinct from the inverted indexes used for full text search and the vector indexes used for vector search. As such, when filters and faceted operations execute, the search engine can apply the operational result to the hybrid search results in the response.

Notice how there's no `orderby` in the query. Explicit sort orders override relevanced-ranked results, so if you want similarity and BM25 relevance, omit sorting in your query.

A response from the above query might look like this:

```http
{
    "@odata.count": 3,
    "@search.facets": {
        "Address/StateProvince": [
            {
                "count": 1,
                "value": "NY"
            },
            {
                "count": 1,
                "value": "VA"
            }
        ]
    },
    "value": [
        {
            "@search.score": 0.03333333507180214,
            "@search.rerankerScore": 2.5229012966156006,
            "HotelId": "49",
            "HotelName": "Swirling Currents Hotel",
            "Description": "Spacious rooms, glamorous suites and residences, rooftop pool, walking access to shopping, dining, entertainment and the city center.",
            "Category": "Luxury",
            "Address": {
                "City": "Arlington",
                "StateProvince": "VA"
            }
        },
        {
            "@search.score": 0.032522473484277725,
            "@search.rerankerScore": 2.111117362976074,
            "HotelId": "48",
            "HotelName": "Nordick's Valley Motel",
            "Description": "Only 90 miles (about 2 hours) from the nation's capital and nearby most everything the historic valley has to offer.  Hiking? Wine Tasting? Exploring the caverns?  It's all nearby and we have specially priced packages to help make our B&B your home base for fun while visiting the valley.",
            "Category": "Boutique",
            "Address": {
                "City": "Washington D.C.",
                "StateProvince": null
            }
        }
    ]
}
```

## Why choose hybrid search?

Hybrid search combines the strengths of vector search and keyword search. The advantage of vector search is finding information that's conceptually similar to your search query, even if there are no keyword matches in the inverted index. The advantage of keyword or full text search is precision, with the ability to apply optional semantic ranking that improves the quality of the initial results. Some scenarios - such as querying over product codes, highly specialized jargon, dates, and people's names - can perform better with keyword search because it can identify exact matches.

Benchmark testing on real-world and benchmark datasets indicates that hybrid retrieval with semantic ranker offers significant benefits in search relevance.

The following video explains how hybrid retrieval gives you optimal grounding data for generating useful AI responses.

> [!VIDEO https://www.youtube.com/embed/Xwx1DJ0OqCk]

## See also

+ [Create a hybrid query](hybrid-search-how-to-query.md)
+ [Relevance scoring in hybrid search](hybrid-search-ranking.md)
+ [Outperform vector search with hybrid retrieval and ranking (Tech blog)](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167)
