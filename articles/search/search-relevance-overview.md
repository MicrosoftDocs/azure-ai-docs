---
title: How scoring works
titleSuffix: Azure AI Search
description: Describes the ranking algorithms in Azure AI Search and how to use them together.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 07/23/2025
---

# How scoring works in Azure AI Search

The query engine in Azure AI Search supports a multi-level approach to ranking search results where there's a built-in ranking modality for each query type, plus extra ranking capabilities for more relevance tuning.

Ranking occurs whenever the query request includes full text or vector queries. It doesn't occur if the query invokes strict pattern matching, such as a filter-only query or a specialized query form like autocomplete, suggestions, geospatial search, fuzzy search, or regular expression search. A uniform search score of 1.0 indicates the absence of a ranking algorithm.

## Levels of ranking

### Initial ranking

Assuming the query engine performs a scoring operation, the initial scoring for level 1 (L1) ranking varies by query type.

+ Text queries, which match on tokenized strings, are always initially ranked using the [BM25 ranking algorithm](index-similarity-and-scoring.md).

+ Vector query L1 ranking is either Hierarchical Navigable Small World (HNSW) or exhaustive K-nearest neighbor (KNN). Image search or multimodal searches are based on vector queries and scored using the vector L2 ranking algorithms.

### Fused ranking

Hybrid queries that include text and vector components are ranked using the Reciprocal Ranking Fusion (RRF) algorithm that's used for merging the results of multiple queries. RRF is also used if multiple vector queries execute in parallel.

### Level 2 (L2) ranking

The L2 ranking feature in Azure AI Search is the [semantic ranker](semantic-search-overview.md) that applies machine reading comprehension to textual content. Semantic ranking is a premium feature that incurs extra charges for use of the semantic ranking models. 

It's optional for text queries and vector queries that contain text, but required for [agentic retrieval (preview)](search-agentic-retrieval-concept.md). Although agentic retrieval sends multiple queries to the query engine, the ranking algorithm for agentic retrieval is the L2 ranker.

## Custom boosting logic using scoring profiles

Scoring profiles supplement a scoring algorithm by boosting the scores of matches that meet user-defined criteria. Criteria can include weighted fields, or functions that boost by freshness, proximity, magnitude, or range. There's no extra charge for using a scoring profile. To use a scoring profile, you define it in an index and then specify it on a query. 

Scoring logic applies to text and numeric nonvector content. You can use scoring profiles with:

+ [Text (keyword) search](search-query-create.md)
+ [Pure vector queries](vector-search-how-to-query.md)
+ [Hybrid queries](hybrid-search-how-to-query.md), with text and vector subqueries execute in parallel
+ [Semantically ranked queries](semantic-how-to-query-request.md)

For standalone text queries, scoring profiles identify the top 1,000 matches in a [BM25-ranked search](index-similarity-and-scoring.md), with the top 50 matches returned in the response.

For pure vectors, the query is vector-only, but if the [*k*-matching documents](vector-search-ranking.md) include nonvector fields with human-readable content, a scoring profile is applied to nonvector fields in `k` documents. 

For the text component of a hybrid query, scoring profiles identify the top 1,000 matches in a BM25-ranked search. However, once those 1,000 results are identified, they're restored to their original BM25 order so that they can be rescored alongside vectors results in the final [Reciprocal Ranking Function (RRF)](hybrid-search-ranking.md) ordering, where the scoring profile (identified as "final document boosting adjustment" in the illustration) is applied to the merged results, along with [vector weighting](vector-search-how-to-query.md#vector-weighting), and [semantic ranking](semantic-search-overview.md) as the last step.

For semantically ranked queries (not shown in the diagram), assuming you use the latest preview REST API or a preview Azure SDK package, scoring profiles can be applied over an L2 ranked result set, generating a new `@search.rerankerBoostedScore` that determines the final ranking.

## Types of search scores

Scored results are indicated for each match in the query response. This table lists all of the search scores with an associated range. Range varies by algorithm.

| Score | Range | Algorithm|
|-------|-------|-------------|
| @search.score | 0 through unlimited | [BM25 ranking algorithm](index-similarity-and-scoring.md#scores-in-a-text-results) for text search |
| @search.score | 0.333 - 1.00 | [HNSW or exhaustive KNN algorithm](vector-search-ranking.md#scores-in-a-vector-search-results) for vector search |
| @search.score | 0 through an upper limit determined by the number of queries | [RRF algorithm](hybrid-search-ranking.md#scores-in-a-hybrid-search-results) |
| @search.rerankerScore | 0.00 - 4.00 | [Semantic ranking algorithm](semantic-search-overview.md#how-ranking-is-scored) for L2 ranking |
| @search.rerankerScoreBoosted | 0.00 - 4.00 | Semantic ranking algorithm for L2 ranking and custom boosting through a scoring profile |

## Diagram of ranking algorithms

The following diagram illustrates how the ranking algorithms are used together.

:::image type="content" source="media/scoring-profiles/scoring-over-ranked-results.png" alt-text="Diagram showing which fields have a scoring profile and when ranking occurs.":::

> [!NOTE]
> This workflow diagram currently omits `@search.rerankerScoreBoosted` and a step for semantic ranking with boosting from a scoring profile. If you use semantic ranking with scoring profile, the scoring profile is applied after L2 ranking, and the final score is based on `@search.rerankerScoreBoosted`.

A query that generates the previous workflow might look like the following example.

```http
POST https://{{search-service-name}}.search.windows.net/indexes/{{index-name}}/docs/search?api-version=2025-05-01-preview
Content-Type: application/json
api-key: {{admin-api-key}}
{
   "queryType":"semantic",
   "search":"what is a hello world application",
   "searchFields":"field_a, field_b",
   "vectorQueries": [
       {
           "kind":"vector",
           "vector": [1.0, 2.0, 3.0],
           "fields": "field_c, field_d"
       },
       {
           "kind":"vector",
           "vector": [4.0, 5.0, 6.0],
           "fields": "field_d, field_e"
       }
   ],
   "scoringProfile":"my_scoring_profile"
}
```