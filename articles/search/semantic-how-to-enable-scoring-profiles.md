---
title: Integrate Scoring Profiles with Semantic Ranking
titleSuffix: Azure AI Search
description: Learn how to combine scoring profiles with semantic ranking in Azure AI Search to optimize final document relevance.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/06/2025
---

# Integrating scoring profiles with semantic ranker in Azure AI Search

## Overview

Integrating [scoring profiles](index-add-scoring-profiles.md) with [semantic ranker](semantic-search-overview.md) is now possible in Azure AI Search. Semantic ranker adds a new field, `@search.rerankerBoostedScore`, to help you maintain consistent relevance and greater control over final ranking outcomes in your search pipeline.

Prior to this integration, scoring profiles only had an effect on the initial search results. The boosts introduced by these scoring profiles were applied to the initial BM25-ranked or RRF-ranked search result for text-based queries, the text portion of vector queries, and hybrid queries that were served to the ranker, but were overlooked once semantic ranking came into play.

Integrating scoring profiles with semantic ranker addresses this by allowing you to apply those profiles directly at the reranking level, ensuring that the boosts are taken into account.


## Prerequisites

- An [Azure AI Search service](search-what-is-azure-search.md) with [semantic ranker enabled](semantic-how-to-configure.md).


## How does semantic configuration with scoring profiles work?

When you execute a semantic query associated with a scoring profile, an additional `@search.rerankerBoostedScore` is generated in every document in your search results. This boosted score, calculated by applying the scoring profile to the existing reranker score, does not have a guaranteed range (0–4) like a normal reranker score, but it can be higher than 4.

Starting in API version `2025-05-01-preview`, semantic results are sorted by `@search.rerankerBoostedScore` by default. If the `rankingOrder` property is not specified, then `boostedReRankerScore` is the default value in the semantic configuration.

Enabling this capability means that your scoring profile defined in your index will first be applied in the initial BM25-ranked or RRF-ranked search result for text-based queries, the text portion of vector queries, and hybrid queries. Then, the top 50 results will be used as inputs by your semantic ranker and also apply the scoring profile after the reranking operation has occurred.


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
