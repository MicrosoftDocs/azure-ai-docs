---
title: Use Scoring Profiles with Semantic Ranking
titleSuffix: Azure AI Search
description: Learn how to combine scoring profiles with semantic ranking in Azure AI Search to optimize final document relevance.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/10/2025
---

# Use scoring profiles with semantic ranker in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Integrating [scoring profiles](index-add-scoring-profiles.md) with [semantic ranker](semantic-search-overview.md) is supported in newer Azure AI Search API versions and Azure SDK packages. Semantic ranker adds a new field, `@search.rerankerBoostedScore`, to help you maintain consistent relevance and greater control over final ranking outcomes in your search pipeline.

Before this integration, scoring profiles only influenced the initial L1 ranking phase of [BM25-ranked](index-similarity-and-scoring.md) and [RRF-ranked](hybrid-search-ranking.md) search results. However, once the semantic L2 ranker re-ranked the results, those boosts no longer had any effect. The semantic reranking process ignored scoring profiles entirely.

Integrating scoring profiles with semantic ranker addresses this behavior by applying scoring profiles to L2-ranked results, ensuring that the boosts are taken into account.

## Prerequisites

- [Azure AI Search](search-create-service-portal.md), Basic pricing tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

- REST API version `2025-05-01-preview` or a prerelease Azure SDK package that provides the new APIs. For all preview features, we recommend reviewing the Azure SDK change logs for feature availability: [Python SDK change log](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET SDK change log](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [Java SDK change log](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [JavaScript SDK change log](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md).

## How does semantic configuration with scoring profiles work?

When you execute a semantic query associated with a scoring profile, a third search score, `@search.rerankerBoostedScore` value, is generated for every document in your search results. This boosted score, calculated by applying the scoring profile to the existing reranker score, doesn't have a guaranteed range (0–4) like a normal reranker score, and scores can be significantly higher than 4.

Starting in API version `2025-05-01-preview`, semantic results are sorted by `@search.rerankerBoostedScore` by default. If the `rankingOrder` property isn't specified, then `boostedReRankerScore` is the default value in the semantic configuration.

When this capability is enabled, the scoring profile defined in your index applies during the initial ranking phase.
It boosts results from:

- Text-based queries (BM25 or RRF)
- The text portion of vector queries
- Hybrid queries that combine both types

The semantic ranker then reprocesses the top 50 results. It also reapplies the scoring profile after reranking, so your boosts influence the final order of results.

## Enable scoring profiles in semantic configuration

To enable scoring profiles with semantic ranking, use preview API version `2025-05-01-preview` to update an index by setting the `rankingOrder` property of its semantic configuration. Use the PUT method to update the index with your revisions. No index rebuild is required.

```json
PUT https://{service-name}.search.windows.com/indexes/{index-name}?api-version=2025-05-01-Preview
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

## Disable scoring profiles in semantic configuration

To opt out of sorting by semantic reranker boosted score, set the `rankingOrder` field to `reRankerScore` value in the semantic configuration.

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

Even if you opt out of sorting by `@search.rerankerBoostedScore`, the `boostedReRankerScore` field is still produced in the response, but it's no longer used to sort results. 

## Example query and response

Start with a [semantic query](semantic-how-to-query-request.md) that specifies a scoring profile. The query uses the new preview REST API, and it targets a search index that has `rankingOrder` set to `boostedReRankerScore`.

```json
POST https://{service-name}.search.windows.com/indexes/{index-name}/docs/search?api-version=2025-05-01-Preview
{
  "search": "my query to be boosted",
  "scoringProfile": "myScoringProfile",
  "queryType": "semantic"
}
```

The response includes the new `rerankerBoostedScore`, alongside the L1 `@search.score` and the L2 `@search.rerankerSocre`. Results are ordered by `@search.rerankerBoostedScore`.

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
