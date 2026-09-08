---
title: Indexer Execution on Serverless and S3 HD
description: Learn how Azure AI Search runs indexers, applies daily runtime quotas, and reports remaining capacity on Serverless and S3 HD services.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 08/17/2026
ai-usage: ai-assisted
ms.custom: doc-kit-assisted
---

# Indexer execution on Serverless and Standard 3 High Density (S3 HD)

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

This article describes the indexer execution model that Azure AI Search uses for Serverless and Standard 3 High Density (S3 HD) search services. Both options have a service-level daily runtime quota that governs how much total indexer time you can use per 24-hour UTC window.

> [!IMPORTANT]
> The capabilities described in this article are in preview under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> + Indexer support on S3 HD requires the [`2025-11-01-preview` REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or later.
> + Serverless indexer support requires the [`2026-05-01-preview` REST API](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) or later.

## Where it applies

The execution model in this article applies to:

+ [Serverless search services](serverless-cost-optimization.md) that run indexers by using the `2026-05-01-preview` REST API or later.
+ S3 HD search services that run indexers by using the `2025-11-01-preview` REST API or later.

Supported indexer definitions, data sources, skillsets, and indexer-backed knowledge sources work without modification on both options.

## Execution model

Indexers on Serverless and S3 HD have the following execution characteristics:

+ You don't provision or manage indexer infrastructure. The service handles capacity for you.

+ Indexers run only in the [multitenant execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment). The private execution environment, which is provided through [shared private link resources](search-indexer-howto-access-private.md), isn't available for indexers on these SKUs.

+ For S3 HD, if you need indexer connections to stay off the public internet, configure a [network security perimeter](search-security-network-security-perimeter.md) (NSP) on your search service to control inbound and outbound traffic through explicit access rules.

+ For Serverless, there's no support for private connections.
  
## Daily cumulative runtime quota

Indexer execution is governed by a daily runtime quota that resets at 00:00 UTC. The quota is:

+ **Service level:** It applies to the search service as a whole.
+ **Cumulative:** Runtime from every indexer in the service counts toward the same budget. The quota isn't applied per indexer.

All running indexers accrue time against one shared service budget. The service doesn't reserve runtime for individual indexers or automatically divide the quota equally among them. For example, the cumulative durations of 12 indexers that each run for two hours can consume all 24 aggregate runtime hours, whether the runs overlap or occur at different times.

The following table lists the daily quota by SKU and the minimum API version that supports it:

| SKU | Daily quota per 24-hour UTC window | Minimum API version |
|-----|------------------------------------|---------------------|
| S3 HD | 24 hours | `2025-11-01-preview` |
| Serverless | 24 hours | `2026-05-01-preview` |

When the daily quota is exhausted:

+ Indexers that are currently running stop within about five minutes.

+ New indexer runs don't process documents and immediately return a transient failure indicating that the daily quota has been exceeded.

+ Normal indexer execution resumes after the counter resets at 00:00 UTC.

### Recover from quota exhaustion

To recover from quota exhaustion and reduce the likelihood of hitting it again:

+ Wait until the next 00:00 UTC reset, or use [Get Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) (REST API) to confirm `remainingSeconds` is replenished before triggering new runs.

+ Put indexers on [staggered schedules](search-howto-schedule-indexers.md) so that work spreads across the 24-hour window instead of running concurrently.

+ You can't pause or stop active runs. Use [Get Indexer Status](/rest/api/searchservice/indexers/get-status) to monitor them, and see [Run or reset indexers](search-howto-run-reset-indexers.md#indexer-execution) for runtime control behavior.

+ If runtime remains but indexer runs fail, see [Troubleshoot indexer issues](search-indexer-troubleshooting.md).

+ Reduce skillset cost. Skills that call external services, such as the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md), and [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md), consume runtime quickly. Lower the number of skills, batch documents, or [configure an enrichment cache](enrichment-cache-how-to-configure.md) to reuse prior results instead of reprocessing.

+ Monitor `remainingSeconds` proactively at both the service and indexer level so that you can throttle workloads before they fail.

## Monitor cumulative runtime

This section explains how to track runtime usage and remaining budget using the Search Service REST APIs. There's no portal experience for cumulative runtime during the preview.

### Service-level runtime

Use [Get Service Statistics](/rest/api/searchservice/get-service-statistics/get-service-statistics) (REST API) to retrieve cumulative indexer runtime across all indexers in the service for the current 24-hour window:

```http
GET {endpoint}/servicestats?api-version=2026-08-01-preview
```

The response includes an `indexersRuntime` section. The following JSON shows a service whose 24-hour daily quota isn't used:

```json
"indexersRuntime": {
    "usedSeconds": 0,
    "remainingSeconds": 86400,
    "beginningTime": "2026-05-16T00:00:00.000Z",
    "endingTime": "2026-05-17T00:00:00.000Z"
}
```

**Key points:**

+ `usedSeconds`: Total seconds that all indexers in the service have run during the current window.
+ `remainingSeconds`: Seconds still available before the daily quota is reached. Present when a tier-specific limit applies.
+ `beginningTime` and `endingTime`: Start and end of the current 24-hour UTC counting window.

### Indexer-level runtime

Use [Get Indexer Status](/rest/api/searchservice/indexers/get-status) (REST API) to retrieve cumulative runtime for an individual indexer:

```http
GET {endpoint}/indexers('{indexerName}')/search.status?api-version=2026-08-01-preview
```

The response includes a `runtime` section. The following JSON shows an indexer on a service whose 24-hour daily quota isn't used:

```json
"runtime": {
    "usedSeconds": 0,
    "remainingSeconds": 86400,
    "beginningTime": "2026-05-16T00:00:00.000Z",
    "endingTime": "2026-05-17T00:00:00.000Z"
}
```

**Key points:**

+ `usedSeconds`: Total seconds the indexer has run during the current window.
+ `remainingSeconds`: Seconds still available to *all indexers in the service*, not just this indexer. Present when a tier-specific limit applies.
+ `beginningTime` and `endingTime`: Start and end of the current 24-hour UTC counting window.

## Best practices

Indexer support on S3 HD and Serverless is in preview. Follow this guidance to size workloads appropriately and to plan for billing for Serverless to be introduced at a later date.

### S3 HD

During the preview, S3 HD indexer support is designed for workloads with no skillsets or small skillsets. To stay within the daily quota:

+ Plan for small indexes of about 1 GB in size.

+ Size skillset usage carefully. Skills that call external services, such as the [Azure OpenAI Embedding skill](cognitive-search-skill-azure-openai-embedding.md), [GenAI Prompt skill](cognitive-search-skill-genai-prompt.md), and [Azure Content Understanding skill](cognitive-search-skill-content-understanding.md), significantly increase runtime and can consume the daily quota quickly, especially in multitenant scenarios.

+ Expect limited parallelism during the preview. Use scheduled, staggered runs for large indexer fleets so that work spreads across the 24-hour window rather than competing for the same budget.

#### Illustrative split-and-embed workload

In one controlled S3 HD test, a Split skill and one Azure OpenAI Embedding skill generated chunks and embeddings. The workload produced approximately 2.5 chunks per source document, and approximately 22,000 source documents were observed in this test during one 24-hour S3 HD test window.

The following values are rounded, illustrative fair-share arithmetic based on the aggregate observation. They aren't measured per-indexer results.

| Indexer count | Illustrative source documents per indexer per day |
|---------------|---------------------------------------------------|
| 100 | About 200 |
| 500 | About 40 |
| 1,000 | About 20 |

The service doesn't reserve capacity or guarantee equal distribution, execution order, or throughput for these indexer counts.

> [!NOTE]
> This result was observed in one controlled test. It isn't a performance target, service guarantee, capacity commitment, sizing formula, or substitute for testing your workload.

Throughput can vary materially with document complexity and profile, chunking, the number and type of skills and vector outputs, model latency, capacity, and quota, source and target performance, concurrency, scheduling order, throttling, region, failures and retries, document cracking or optical character recognition (OCR), and uneven tenant volumes. Test with representative production inputs before you plan capacity.

### Serverless

During the preview, Serverless indexers are designed to simplify ingestion for retrieval-augmented generation (RAG) and knowledge base scenarios:

+ Indexer execution (excluding skills) is currently free. Writing documents to an index incurs a cost.

+ Skillset execution is billed the same way as on dedicated indexers. Calls to external services, such as the Azure OpenAI Embedding skill, GenAI Prompt skill, and Azure Content Understanding skill, are billed through the attached [Foundry or Azure AI services resource](cognitive-search-attach-cognitive-services.md).

## Limits and quotas

For indexer limits on Serverless and S3 HD, see [Indexer limits](search-limits-quotas-capacity.md#indexer-limits).

The service-level runtime quota and indexer limits don't replace the input, request, or processing limits of skills and external services in a skillset. Check each skill reference separately when you size an enrichment pipeline.

## Related content

+ [Indexers in Azure AI Search](search-indexer-overview.md)
+ [Run or reset indexers](search-howto-run-reset-indexers.md)
+ [Monitor indexer status and results](search-monitor-indexers.md)
+ [Knowledge sources](agentic-knowledge-source-overview.md)
+ [Service limits in Azure AI Search](search-limits-quotas-capacity.md)
