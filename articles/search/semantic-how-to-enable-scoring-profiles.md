---
title: Integrate Scoring Profiles with Semantic Ranking
titleSuffix: Azure AI Search
description: Learn how to combine scoring profiles with semantic ranking in Azure AI Search to optimize final document relevance.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/07/2025
---

# Integrating scoring profiles with semantic ranker in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Integrating [scoring profiles](index-add-scoring-profiles.md) with [semantic ranker](semantic-search-overview.md) is now possible in Azure AI Search. Semantic ranker adds a new field, `@search.rerankerBoostedScore`, to help you maintain consistent relevance and greater control over final ranking outcomes in your search pipeline.

Before this integration, scoring profiles only influenced the initial ranking phase of search results. The boost values they applied affected:
- [BM25-ranked](index-similarity-and-scoring.md) or [RRF-ranked](hybrid-search-ranking.md) results for text-based queries
- The text portion of vector queries
- Hybrid queries that included both text and vector components

However, once the semantic ranker re-ranked the results, those boosts no longer had any effect. The semantic reranking process ignored scoring profiles entirely.

Integrating scoring profiles with semantic ranker addresses this behavior by allowing you to apply those profiles directly at the reranking level, ensuring that the boosts are taken into account.


## Prerequisites

- An [Azure AI Search service](search-what-is-azure-search.md) with [semantic ranker enabled](semantic-how-to-configure.md).


## How does semantic configuration with scoring profiles work?

When you execute a semantic query associated with a scoring profile, another `@search.rerankerBoostedScore` value is generated in every document in your search results. This boosted score, calculated by applying the scoring profile to the existing reranker score, doesn't have a guaranteed range (0–4) like a normal reranker score, but it can be higher than 4.

Starting in API version `2025-05-01-preview`, semantic results are sorted by `@search.rerankerBoostedScore` by default. If the `rankingOrder` property isn't specified, then `boostedReRankerScore` is the default value in the semantic configuration.

When this capability is enabled, the scoring profile defined in your index applies during the initial ranking phase.
It boosts results from:
- Text-based queries (BM25 or RRF)
- The text portion of vector queries
- Hybrid queries that combine both types

The semantic ranker then reprocesses the top 50 results. It also reapplies the scoring profile after reranking, so your boosts influence the final order of results.


## Enabling scoring profiles in semantic configuration

To integrate scoring profiles with semantic ranking, configure it using API version `2025-05-01-preview`. Use the PUT method to update the index with the semantic configuration.

### Example: Enable boosted reranker score

```json
PUT https://{service-name}.search.windows.com/indexes/{index-name}?api-version=2024-05-01-Preview
{
  "semantic": {
    "configurations": [
      {
        "name": "mySemanticConfig",
        "rankingOrder": "boostedReRankerScore"
      }
    ]
  }
}
```


## Disabling scoring profiles in semantic configuration

If you want to opt out of sorting by semantic reranker boosted score, set the `rankingOrder` field to `reRankerScore` value in the semantic configuration.

### Example: Disable boosted reranker score

```json
PUT https://{service-name}.search.windows.com/indexes/{index-name}?api-version=2024-05-01-Preview
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
Even if you opt out of sorting by `@search.rerankerBoostedScore`, the field is still produced in the response. It simply isn't used to sort results.


### Sample Request and Response
```json
POST https://{service-name}.search.windows.com/indexes/{index-name}/docs/search?api-version=2024-05-01-Preview
{
  "search": "my query to be boosted",
  "scoringProfile": "myScoringProfile",
  "queryType": "semantic"
}
```

> [!NOTE]
> For this request to apply the semantic profile, it must be enabled in the semantic configuration as shown earlier.


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
