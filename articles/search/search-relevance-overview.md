---
title: Relevance
titleSuffix: Azure AI Search
description: Describe strategies for producing relevant results  in Azure AI Search and explain how the scoring and ranking algorithms work and how to use them together.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 12/08/2025
ms.update-cycle: 180-days
---

# Relevance in Azure AI Search

The true measure of relevance is *how well* a retrieved set of results meets your customer and user information needs. In this article, learn about:

+ The main strategies for producing relevant results in Azure AI Search
+ The mechanics of how relevance is measured
+ The actions you can take to improve relevance

## Strategies for highly relevant results

In Azure AI Search, two main strategies have emerged as the best approaches for producing highly relevant results.

+ Hybrid search with semantic reranker
+ Agentic retrieval (preview) with LLM-assisted query planning and answer formulation

[Hybrid search (classic)](hybrid-search-overview.md) delivers on relevance by combining the precision of keyword queries and the semantic similarity of vector queries in a search request targeting a single index. Keyword search operates over a verbatim query. Vector search runs an identical query using a vectorized version of the same string. The queries execute in parallel, looking for precise and semantically similar matches. Results are merged, ranked, and then rescored using a semantic ranker that promotes the most relevant matches. Using keyword and vector search *together* offsets the weaknesses of each approach as a standalone solution. Semantic reranker is an extra component that contributes to a better outcome.

[Agentic retrieval (preview)](agentic-retrieval-overview.md) delivers on relevance through smart integration with LLMs and a knowledge base that defines an entire search domain. The LLM can analyze and transform queries for more effective retrieval. It can decompose complex questions into targeted subqueries, refine vague requests, or generalize narrow ones for broader scope. In a typical agentic retrieval workload, the LLM answers the question using its reasoning power, context from chat history, and retrieval instructions to identify the very best content and use it to best advantage. This combination of LLM-assisted query planning, multi-source knowledge base search, and LLM reasoning is how agentic retrieval returns highly relevant results.

Relevance also depends on having grounding data of sufficient quantity and quality. In agentic retrieval, you can list multiple knowledge sources to expand the scope of what's searchable and provide logic for selecting specific ones.

## How relevance is measured

Regardless of how content is retrieved, the relevance of any given result is determined by a ranking algorithm that evaluates the strength of a match based on how closely the query corresponds to content in the search corpus. When a match is found, an algorithm assigns a score, and results are ranked by that score and the topmost results are returned in the response. 

Ranking occurs whenever the query request is for agentic retrieval and classic search for keyword, vector, and hybrid queries. It doesn't occur if the query invokes strict pattern matching, such as a filter-only query or a specialized query form like autocomplete, suggestions, geospatial search, fuzzy search, or regular expression search. A uniform search score of 1.0 indicates the absence of a ranking algorithm.

## Levels of ranking

The query engine in Azure AI Search supports a multi-level approach to rank search results, where there's a built-in ranking modality for each query type, plus extra ranking capabilities for extended relevance tuning.

This section describes the levels of scoring operations. For an illustration of how they work together, see the [diagram](#diagram-of-ranking-algorithms) in this article. A [comparison of all search score types and ranges](#types-of-search-scores) is also provided in this article.

| Level | Description |
|-------|-------------|
| Level&nbsp;1&nbsp;(L1) | Initial search score (`@search.score`). <br>For text queries matching on tokenized strings, results are always initially ranked using the [BM25 ranking algorithm](index-similarity-and-scoring.md). <br>For vector queries, results are ranked using either [Hierarchical Navigable Small World (HNSW) or exhaustive K-nearest neighbor (KNN)](vector-search-ranking.md). Image search or multimodal searches are based on vector queries and scored using the L1 vector ranking algorithms. |
| Fused&nbsp;L1 | Scoring from multiple queries using the [Reciprocal Ranking Fusion (RRF) algorithm](hybrid-search-ranking.md). RRF is used for hybrid queries that include text and vector components. RRF is also used when multiple vector queries execute in parallel. A search score from RRF is reflected in `@search.score` [over a different range](#types-of-search-scores).|
| Level&nbsp;2&nbsp;(L2) | [Semantic ranking score (`@search.reRankerScore`)](semantic-search-overview.md) applies machine reading comprehension to the textual content retrieved by L1 ranking, rescoring the L1 results to better match the semantic intent of the query. L2 reranks L1 results because doing so saves time and money; it would be prohibitive to use semantic ranking as an L1 ranking system. Semantic ranking is a premium feature that bills for usage of the semantic ranking models. It's optional for text queries and vector queries that contain text, but required for [agentic retrieval (preview)](agentic-retrieval-overview.md). Although agentic retrieval sends multiple queries to the query engine, the ranking algorithm for agentic retrieval is the semantic ranker. |
| Level&nbsp;3&nbsp;(L3) | Applies to [agentic retrieval (preview)](agentic-retrieval-overview.md) and a `medium` retrieval reasoning effort. L3 ranking refers to *iterative search* and it's invoked when the agentic retrieval engine and LLM agree that a second query pass is needed to return a more relevant result. For more information, see [Iterative search for medium retrieval](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md#iterative-search-for-medium-retrieval). |

## Relevance tuning

***Relevance tuning*** is a technique for boosting search scores based on extra criteria such as weighted fields, freshness, or proximity. In Azure AI Search, relevance tuning options vary based on query type:

+ For textual and numeric (nonvector) content in keyword or hybrid search, you can tune relevance through [scoring profiles](#custom-boosting-logic-using-scoring-profiles) or invoking the [semantic ranker](semantic-search-overview.md).

+ For vector content in a hybrid query, you can [weight a vector field](hybrid-search-ranking.md#weighted-scores) to boost the importance of the vector component relative to the text component of the hybrid query.

+ For pure vector queries, you can experiment between Hierarchical Navigable Small World (HNSW) and exhaustive K-nearest neighbors (KNN) to see if one algorithm outperforms the other for your scenario. HNSW graphing with an exhaustive KNN override at query time is the most flexible approach for comparison testing. You can also experiment with various embedding models to see which ones produce higher quality results. Finally, remember that a hybrid query or a vector query on documents that include nonvector fields are in-scope for relevance tuning, so it's just the vector fields themselves that can't participate in a relevance tuning effort.

## Custom boosting logic using scoring profiles

[Scoring profiles](index-add-scoring-profiles.md) are an optional feature for boosting scores based on extra user-defined criteria. Criteria can include weighted fields where a match found in a specific field is given more weight than the same match found in a different field. Criteria can also be defined through functions that boost by freshness, proximity, magnitude, or range. There's no extra costs associated with scoring profiles. To use a scoring profile, you define it in an index and then specify it on a query. 

Scoring logic applies to text and numeric nonvector content. You can use scoring profiles with:

+ [Text (keyword) search](search-query-create.md)
+ [Pure vector queries](vector-search-how-to-query.md)
+ [Hybrid queries](hybrid-search-how-to-query.md), where text and vector subqueries execute in parallel
+ [Semantically ranked queries](semantic-how-to-query-request.md)

For standalone text queries, scoring profiles identify the top 1,000 matches in a [BM25-ranked search](index-similarity-and-scoring.md), with the top 50 matches returned in the response.

For pure vectors, the query is vector-only, but if the [*k*-matching documents](vector-search-ranking.md) include nonvector fields with human-readable content, a scoring profile is applied to nonvector fields in `k` documents. 

For the text component of a hybrid query, scoring profiles identify the top 1,000 matches in a BM25-ranked search. However, once those 1,000 results are identified, they're restored to their original BM25 order so that they can be rescored alongside vectors results in the final [Reciprocal Ranking Function (RRF)](hybrid-search-ranking.md) ordering, where the scoring profile (identified as "final document boosting adjustment" in the illustration) is applied to the merged results, along with [vector weighting](vector-search-how-to-query.md#vector-weighting), and [semantic ranking](semantic-search-overview.md) as the last step.

For semantically ranked queries (not shown in the diagram), assuming you use the latest preview REST API or a preview Azure SDK package, scoring profiles can be applied over an L2 ranked result set, generating a new `@search.rerankerBoostedScore` that determines the final ranking.

## Types of search scores

Scored results are indicated for each match in the query response. This table lists all of the search scores with an associated range. Range varies by algorithm.

| Score | Range | Algorithm|
|-------|-------|-------------|
| `@search.score` | 0 through unlimited | [BM25 ranking algorithm](index-similarity-and-scoring.md#scores-in-a-text-results) for text search |
| `@search.score` | 0.333 - 1.00 | [HNSW or exhaustive KNN algorithm](vector-search-ranking.md#scores-in-a-vector-search-results) for vector search |
| `@search.score` | 0 through an upper limit determined by the number of queries | [RRF algorithm](hybrid-search-ranking.md#scores-in-hybrid-search-results) |
| `@search.rerankerScore` | 0.00 - 4.00 | [Semantic ranking algorithm](semantic-search-overview.md#how-results-are-scored) for L2 ranking |
| `@search.rerankerBoostedScore` | 0 through unlimited  | [Semantic ranking with scoring profile boosting](semantic-how-to-enable-scoring-profiles.md) (scores can be significantly higher than 4) |

## Diagram of ranking algorithms

The following diagram illustrates how the ranking algorithms work together.

:::image type="content" source="media/scoring-profiles/scoring-over-ranked-results.png" alt-text="Diagram showing which fields have a scoring profile and when ranking occurs.":::

> [!NOTE]
> If you use semantic ranking, the [rankingOrder](/rest/api/searchservice/indexes/create-or-update#rankingorder) property determines whether results are the semantically scored results (`@search.rerankerScore`) or the boosted scores ( `@search.rerankerBoostedScore`) that are created after the scoring profile is applied.

## Example query inclusive of all ranking algorithms

A query that generates the previous workflow might look like the following example. This hybrid semantic query is scored using RRF (based on L1 scores for text and vectors), and semantic ranking.

```http
POST https://{{search-service-name}}.search.windows.net/indexes/{{index-name}}/docs/search?api-version=2025-11-01-preview

{
  "search": "cloud formation over water",
  "count": true,
  "vectorQueries": [
    {
      "kind": "text",
      "text": "cloud formation over water",
      "fields": "text_vector,image_vector"
    }
  ],
  "queryType": "semantic",
  "semanticConfiguration": "my-semantic-configuration",
  "select": "title,chunk",
  "top": 5
}
```

A response for the previous query includes the original RRF `@search.core` and the `@search.rerankerScore`.

```json
  "value": [
    {
      "@search.score": 0.03177805617451668,
      "@search.rerankerScore": 2.6919238567352295,
      "chunk": "A\nT\n\nM\nO\n\nS\nP\n\nH\nE\n\nR\nE\n\nE\nA\n\nR\nT\n\nH\n\n32\n\nFraming an Iceberg\nSouth Atlantic Ocean\n\nIn June 2016, the Suomi NPP satellite captured this image of various cloud formations in the South Atlantic Ocean. Note how low \n\nstratus clouds framed a hole over iceberg A-56 as it drifted across the sea. \n\nThe exact reason for the hole in the clouds is somewhat of a mystery. It could have formed by chance, although imagery from the \n\ndays before and after this date suggest something else was at work. It could be that the relatively unobstructed path of the clouds \n\nover the ocean surface was interrupted by thermal instability created by the iceberg. In other words, if an obstacle is big enough,  \n\nit can divert the low-level atmospheric flow of air around it, a phenomenon often caused by islands.",
      "title": "page-39.pdf",
    },
    {
      "@search.score": 0.030621785670518875,
      "@search.rerankerScore": 2.557225465774536,
      "chunk": "A\nT\n\nM\nO\n\nS\nP\n\nH\nE\n\nR\nE\n\nE\nA\n\nR\nT\n\nH\n\n24\n\nMaking Tracks\nPacific Ocean\n\nShips steaming across the Pacific Ocean left this cluster of bright cloud trails lingering in the atmosphere in February 2012. The \n\nnarrow clouds, known as ship tracks, form when water vapor condenses around tiny particles of pollution from ship exhaust. The \n\ncrisscrossing clouds off the coast of California stretched for many hundreds of kilometers from end to end. The narrow ends of the \n\nclouds are youngest, while the broader, wavier ends are older.\n\nSome of the pollution particles generated by ships (especially sulfates) are soluble in water and can serve as the seeds around which \n\ncloud droplets form. Clouds infused with ship exhaust have more and smaller droplets than unpolluted clouds. As a result, light \n\nhitting the ship tracks scatters in many directions, often making them appear brighter than other types of marine clouds, which are \n\nusually seeded by larger, naturally occurring particles like sea salt.",
      "title": "page-31.pdf",
    },
    {
      "@search.score": 0.013698630034923553,
      "@search.rerankerScore": 2.515575408935547,
      "chunk": "A\nT\n\nM\nO\n\nS\nP\n\nH\nE\n\nR\nE\n\nE\nA\n\nR\nT\n\nH\n\n16\n\nRiding the Waves\nMauritania\n\nYou cannot see it directly, but air masses from Africa and the Atlantic Ocean are colliding in this Landsat 8 image from August 2016. \n\nThe collision off the coast of Mauritania produces a wave structure in the atmosphere. \n\nCalled an undular bore or solitary wave, this cloud formation was created by the interaction between cool, dry air coming off the \n\ncontinent and running into warm, moist air over the ocean. The winds blowing out from the land push a wave of air ahead like a  \n\nbow wave moving ahead of a boat. \n\nParts of these waves are favorable for cloud formation, while other parts are not. The dust blowing out from Africa appears to be \n\nriding these waves. Dust has been known to affect cloud growth, but it probably has little to do with the cloud pattern observed here.",
      "title": "page-23.pdf",
    },
    {
      "@search.score": 0.028949543833732605,
      "@search.rerankerScore": 2.4990925788879395,
      "chunk": "A\nT\n\nM\nO\n\nS\nP\n\nH\nE\n\nR\nE\n\nE\nA\n\nR\nT\n\nH\n\n14\n\nBering Streets\nArctic Ocean\n\nWinds from the northeast pushed sea ice southward and formed cloud streets—parallel rows of clouds—over the Bering Strait in \n\nJanuary 2010. The easternmost reaches of Russia, blanketed in snow and ice, appear in the upper left. To the east, sea ice spans \n\nthe Bering Strait. Along the southern edge of the ice, wavy tendrils of newly formed, thin sea ice predominate.\n\nThe cloud streets run in the direction of the northerly wind that helps form them. When wind blows out from a cold surface like sea \n\nice over the warmer, moister air near the open ocean, cylinders of spinning air may develop. Clouds form along the upward cycle in \n\nthe cylinders, where air is rising, and skies remain clear along the downward cycle, where air is falling. The cloud streets run toward \n\nthe southwest in this image from the Terra satellite.",
      "title": "page-21.pdf",
    },
    {
      "@search.score": 0.027637723833322525,
      "@search.rerankerScore": 2.4686081409454346,
      "chunk": "A\nT\n\nM\nO\n\nS\nP\n\nH\nE\n\nR\nE\n\nE\nA\n\nR\nT\n\nH\n\n38\n\nLofted Over Land\nMadagascar\n\nAlong the muddy Mania River, midday clouds form over the forested land but not the water. In the tropical rainforests of Madagascar, \n\nthere is ample moisture for cloud formation. Sunlight heats the land all day, warming that moist air and causing it to rise high into the \n\natmosphere until it cools and condenses into water droplets. Clouds generally form where air is ascending (over land in this case), \n\nbut not where it is descending (over the river). Landsat 8 acquired this image in January 2015.",
      "title": "page-45.pdf",
    }
  ]
```
