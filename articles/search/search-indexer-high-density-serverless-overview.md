---
title: About Indexer Execution on Serverless and S3 HD
description: Learn how Azure AI Search runs indexers on serverless indexes and S3 High Density (S3 HD) search services.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 05/18/2026
ms.custom:
  - references_regions
  - build-2026
ai-usage: ai-assisted
---

# Indexer execution on serverless and Standard 3 High Density (S3 HD)

This article describes the indexer execution model that Azure AI Search uses for serverless indexes and Standard 3 High Density (S3 HD) search services. Both options have a service-level daily runtime quota that governs how much total indexer time you can use per 24-hour UTC window.

> [!IMPORTANT]
> The capabilities described in this article are in preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> + Indexer support on S3 HD requires the [`2025-11-01-preview` REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or later.
> + Serverless indexer support requires the [`2026-05-01-preview` REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or later.

## Where it applies

The execution model in this article applies to:

+ Serverless indexes that run indexers using the `2026-05-01-preview` REST API or later.
+ S3 HD search services that run indexers using the `2025-11-01-preview` REST API or later.

Existing indexer definitions, data sources, skillsets, and [knowledge sources](agentic-knowledge-source-overview.md) work without modification on both options.

## Execution model

Indexers on serverless and S3 HD have the following execution characteristics:

+ You don't provision or manage indexer infrastructure. The service handles capacity for you.
+ Indexers run only in the [public execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). The private execution environment, which is provided through [shared private link resources](search-indexer-howto-access-private.md), isn't available for indexers on these SKUs. If you need indexer connections to stay off the public internet, configure a [network security perimeter (NSP)](search-security-network-security-perimeter.md) on your search service to control inbound and outbound traffic through explicit access rules.

## Daily cumulative runtime quota

Indexer execution is governed by a daily runtime quota that resets at 00:00 UTC. The quota is:

+ **Service-level.** It applies to the search service as a whole.
+ **Cumulative.** Runtime from every indexer in the service counts toward the same budget. The quota isn't applied per indexer.

The following table lists the daily quota by SKU and the minimum API version that supports it:

| SKU | Daily quota per 24-hour UTC window | Minimum API version |
|-----|------------------------------------|---------------------|
| S3 HD | 6 hours | `2025-11-01-preview` |
| Serverless | 6 hours | `2026-05-01-preview` |

When the daily quota is exhausted:

+ Indexers that are currently running stop within about 5 minutes.
+ New indexer runs don't process documents and immediately return a transient failure indicating that the daily quota has been exceeded.
+ Normal indexer execution resumes after the counter resets at 00:00 UTC.

### Recover from quota exhaustion

To recover from quota exhaustion and reduce the likelihood of hitting it again:

+ Wait until the next 00:00 UTC reset, or use [Get Service Statistics](/rest/api/searchservice/get-service-statistics) to confirm `remainingSeconds` is replenished before triggering new runs.
+ Put indexers on [staggered schedules](search-howto-schedule-indexers.md) so that work spreads across the 24-hour window instead of running concurrently.
+ Reduce skillset cost. Skills that call external services—such as Azure OpenAI embeddings, chat completions, and the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md)—consume runtime quickly. Lower the number of skills, batch documents, or [configure an enrichment cache](enrichment-cache-how-to-configure.md) to reuse prior results instead of reprocessing.
+ Monitor `remainingSeconds` proactively at both the service and indexer level so that you can throttle workloads before they fail.

## Monitor cumulative runtime

Use the REST APIs in this section to track runtime usage and remaining budget. There's no portal experience for cumulative runtime at preview.

### Service-level runtime

Use [Get Service Statistics](/rest/api/searchservice/get-service-statistics) to retrieve cumulative indexer runtime across all indexers in the service for the current 24-hour window:

```http
GET {endpoint}/servicestats?api-version=2025-11-01-preview
```

The response includes an `indexersRuntime` section. The following sample shows a service whose 6-hour daily quota hasn't been used:

```json
"indexersRuntime": {
    "usedSeconds": 0,
    "remainingSeconds": 21600,
    "beginningTime": "2026-05-16T00:00:00.000Z",
    "endingTime": "2026-05-17T00:00:00.000Z"
}
```

+ `usedSeconds`: total seconds that all indexers in the service have run during the current window.
+ `remainingSeconds`: seconds still available before the daily quota is reached. Present when a tier-specific limit applies.
+ `beginningTime` and `endingTime`: start and end of the current 24-hour UTC counting window.

### Indexer-level runtime

Use [Get Indexer Status](/rest/api/searchservice/indexers/get-status) to retrieve cumulative runtime for an individual indexer:

```http
GET {endpoint}/indexers('{indexerName}')/search.status?api-version=2025-11-01-preview
```

The response includes a `runtime` section. The following sample shows an indexer on a service whose 6-hour daily quota hasn't been used:

```json
"runtime": {
    "usedSeconds": 0,
    "remainingSeconds": 21600,
    "beginningTime": "2026-05-16T00:00:00.000Z",
    "endingTime": "2026-05-17T00:00:00.000Z"
}
```

+ `usedSeconds`: total seconds the indexer has run during the current window.
+ `remainingSeconds`: seconds still available to *all indexers in the service*, not just this indexer. Present when a tier-specific limit applies.
+ `beginningTime` and `endingTime`: start and end of the current 24-hour UTC counting window.

## Best practice guidance

Indexer support on S3 HD and serverless is in preview. Follow this guidance to size workloads appropriately and to plan for billing for serverless to be introduced at a later date.

### S3 High Density

During preview, S3 HD indexer support is designed for workloads with no skillsets or small skillsets. To stay within the daily quota:

+ Plan for small indexes of about **1 GB** in size.
+ Size skillset usage carefully. Skills that call external services—such as Azure OpenAI embeddings, chat completions, and the [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md)—significantly increase runtime and can consume the daily quota quickly, especially in multi-tenant scenarios.
+ Expect limited parallelism at preview. Use scheduled, staggered runs for large indexer fleets so that work spreads across the 24-hour window rather than competing for the same budget.

### Serverless

During preview, serverless indexers are designed to simplify ingestion for retrieval-augmented generation (RAG) and knowledge base scenarios:

+ Indexer execution (excluding skills) is currently free. Pricing will be introduced at a later date.
+ **Skillset execution** is billed the same way as on dedicated indexers. Calls to external services—such as Azure OpenAI embeddings, chat completions, and the Azure Content Understanding skill—are billed through the attached [Foundry or Azure AI services resource](cognitive-search-attach-cognitive-services.md).

## Limits and quotas

For indexer limits on serverless and S3 HD, see [Indexer limits](search-limits-quotas-capacity.md#indexer-limits).

## Related content

+ [Indexers in Azure AI Search](search-indexer-overview.md)
+ [Run or reset indexers](search-howto-run-reset-indexers.md)
+ [Monitor indexer status and results](search-howto-monitor-indexers.md)
+ [Knowledge sources](agentic-knowledge-source-overview.md)
+ [Service limits in Azure AI Search](search-limits-quotas-capacity.md)
