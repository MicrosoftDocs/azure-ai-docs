---
title: Use Scoring Profiles with Semantic Ranking
titleSuffix: Azure AI Search
description: Learn how to combine scoring profiles with semantic ranking in Azure AI Search to optimize final document relevance.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 09/28/2025
---

# Use scoring profiles with semantic ranker in Azure AI Search

You can apply a [scoring profile](index-add-scoring-profiles.md) over [semantically ranked search results](semantic-search-overview.md), where the scoring profile is processed last.

To ensure the scoring profile provides the determining score, the semantic ranker adds a response field, `@search.rerankerBoostedScore`, that applies scoring profile logic on semantically ranked results. In search results that include `@search.score` from level 1 ranking, `@search.rerankerScore` from semantic ranker, and `@search.reRankerBoostedScore`, results are sorted by `@search.reRankerBoostedScore`.

## Prerequisites

- [Azure AI Search](search-create-service-portal.md) in any [region that provides semantic ranking](search-region-support.md), with [semantic ranker enabled](semantic-how-to-enable-disable.md).

- A search index with a semantic configuration that specifies `"rankingOrder": "boostedRerankerScore"` and a scoring profile that specifies [functions](index-add-scoring-profiles.md#use-functions).

## Limitations

Boosting of semantically ranked results applies to scoring profile functions only. There's no boosting if the scoring profile consists only of weighted text fields.

## How does semantic configuration with scoring profiles work?

When you execute a semantic query associated with a scoring profile, a third search score, `@search.rerankerBoostedScore` value, is generated for every document in your search results. This boosted score, calculated by applying the scoring profile to the existing reranker score, doesn't have a guaranteed range (0–4) like a normal reranker score, and scores can be significantly higher than 4.

Semantic results are sorted by `@search.rerankerBoostedScore` by default if a scoring profile exists. If the `rankingOrder` property isn't specified, then `BoostedRerankerScore` is the default value in the semantic configuration.

In this scenario, a scoring profile is used twice. 

1. First, the scoring profile defined in your index is used during the initial L1 ranking phase, boosting results from:

   - Text-based queries (BM25 or RRF)
   - The text portion of vector queries
   - Hybrid queries that combine both types

1. Next, the semantic ranker rescores the top 50 results, promoting more semantically relevant matches to the top. This step can erase the benefit of the scoring profile. For example, if you boosted based on freshness, then semantic reordering replaces that boost with its own logic of what is most relevant.

1. Finally, the scoring profile is applied again, after reranking, restoring the boosts influence over the final order of results. If you boost by freshness, the semantically ranked results are rescored based on freshness.

## Enable scoring profiles in semantic configuration

To enable scoring profiles for semantically ranked results, [update an index](/rest/api/searchservice/indexes/create-or-update#rankingorder) by setting the `rankingOrder` property of its semantic configuration. Use the PUT method to update the index with your revisions. No index rebuild is required.

```json
PUT https://{service-name}.search.windows.com/indexes/{index-name}?api-version=2025-09-01
{
  "semantic": {
    "configurations": [
      {
        "name": "mySemanticConfig",
        "rankingOrder": "boostedRerankerScore"
      }
    ]
  }
}
```

## Disable scoring profiles in semantic configuration

To opt out of sorting by semantic reranker boosted score, set the `rankingOrder` field to `reRankerScore` value in the semantic configuration.

```json
PUT /indexes/{index-name}?api-version=2025-09-01
{
  "semantic": {
    "configurations": [
      {
        "name": "mySemanticConfig",
        "rankingOrder": "reRankerScore"
      }
    ]
  }
}
```

Even if you opt out of sorting by `@search.rerankerBoostedScore`, the `boostedRerankerScore` field is still produced in the response, but it's no longer used to sort results. 

## Example query and response

Start with a [semantic query](semantic-how-to-query-request.md) that specifies a scoring profile. This query targets a search index that has `rankingOrder` set to `boostedRerankerScore`.

```json
POST /indexes/{index-name}/docs/search?api-version=2025-09-01
{
  "search": "my query to be boosted",
  "scoringProfile": "myScoringProfile",
  "queryType": "semantic"
}
```

The response includes the new `rerankerBoostedScore`, alongside the L1 `@search.score` and the L2 `@search.rerankerScore`. Results are ordered by `@search.rerankerBoostedScore`.

```json
{
  "value": [
    {
      "@search.score": 0.63,
      "@search.rerankerScore": 2.98,
      "@search.rerankerBoostedScore": 7.68,
      "content": "boosted content 2"
    },
    {
      "@search.score": 1.12,
      "@search.rerankerScore": 3.12,
      "@search.rerankerBoostedScore": 5.61,
      "content": "boosted content 1"
    }
  ]
}
```
