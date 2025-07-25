---
title: Use Scoring Profiles with Semantic Ranking
titleSuffix: Azure AI Search
description: Learn how to combine scoring profiles with semantic ranking in Azure AI Search to optimize final document relevance.
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 07/22/2025
---

# Use scoring profiles with semantic ranker in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

Integrating [scoring profiles](index-add-scoring-profiles.md) with [semantic ranker](semantic-search-overview.md) is supported in newer Azure AI Search preview REST API versions and Azure SDK preview packages. Semantic ranker adds a new response field, `@search.rerankerBoostedScore`, that applies scoring profile logic on semantically ranked results. In search results that include `@search.score` from level 1 ranking, `@search.rerankerScore` from semantic ranker, and `@search.reRankerBoostedScore`, results are sorted by `@search.reRankerBoostedScore`.

If you're using a stable API version or an earlier preview, scoring profiles are used upstream, before the semantic ranking step. For a diagram of the scoring workflow, see [Relevance in Azure AI Search](search-relevance-overview.md).

## Prerequisites

- [Azure AI Search](search-create-service-portal.md), Basic pricing tier or higher, with [semantic ranker enabled](semantic-how-to-enable-disable.md).

- [REST API version `2025-05-01-preview`](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) or a prerelease Azure SDK package that provides the new APIs. Currently, there's no Azure portal (Search Explorer) support for this feature so use a REST client or an IDE.

  For all preview features, we recommend reviewing the Azure SDK change logs to check for feature availability: [Python SDK change log](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET SDK change log](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md), [Java SDK change log](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [JavaScript SDK change log](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md).

- A search index with a semantic configuration that specifies `"rankingOrder": "boostedReRankerScore"` and a scoring profile that specifies [functions](index-add-scoring-profiles.md#use-functions).

- A semantic query includes the scoring profile.

## Limitations

Boosting of semantically ranked results applies to scoring profile functions only. There's no boosting if the scoring profile consists of just weighted text fields.

## How does semantic configuration with scoring profiles work?

When you execute a semantic query associated with a scoring profile, a third search score, `@search.rerankerBoostedScore` value, is generated for every document in your search results. This boosted score, calculated by applying the scoring profile to the existing reranker score, doesn't have a guaranteed range (0–4) like a normal reranker score, and scores can be significantly higher than 4.

Starting in API version `2025-05-01-preview`, semantic results are sorted by `@search.rerankerBoostedScore` by default if a scoring profile exists. If the `rankingOrder` property isn't specified, then `BoostedReRankerScore` is the default value in the semantic configuration.

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
PUT https://{service-name}.search.windows.com/indexes/{index-name}?api-version=2025-05-01-Preview
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
