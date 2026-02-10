---
title: Service Limits for Tiers and SKUs
titleSuffix: Azure AI Search
description: Service limits used for capacity planning and maximum limits on requests and responses for Azure AI Search.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: limits-and-quotas
ms.date: 01/26/2026
ms.update-cycle: 180-days
ms.custom:
  - references_regions
  - build-2024
  - ignite-2024
---

# Service limits in Azure AI Search

Maximum limits on storage, workloads, and quantities of indexes and other objects depend on the [pricing tier](search-sku-tier.md) of your Azure AI Search service:

+ **Free** is a multitenant shared service that comes with your Azure subscription.

+ **Basic** provides dedicated computing resources for production workloads at a smaller scale.

+ **Standard** runs on dedicated machines with more storage and processing capacity at every level. Standard comes in four levels: S1, S2, S3, and S3 HD. S3 High Density (S3 HD) is engineered for [multi-tenancy](search-modeling-multitenant-saas-applications.md) and large quantities of small indexes (3,000 indexes per service). S3 HD doesn't support [indexers](search-indexer-overview.md), so data ingestion must use APIs that push data from the source to the index.

+ **Storage Optimized** runs on dedicated machines with more total storage, storage bandwidth, and memory than **Standard**. This tier targets large, slow-changing indexes. Storage Optimized comes in two levels: L1 and L2.

## Subscription limits

[!INCLUDE [azure-search-limits-per-subscription](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-subscription.md)]

## Service limits

[!INCLUDE [azure-search-limits-per-service](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-service.md)]

## Index limits

| Resource | Free | Basic&nbsp;<sup>1</sup>  | S1 | S2 | S3 | S3&nbsp;HD | L1 | L2 |
|----------|------|--------|----|----|----|------------|----|----|
| Maximum indexes |3 |5 or 15 |50 |200 |200 |1000 per partition or 3000 per service |10 |10 |
| Maximum simple fields per index&nbsp;<sup>2</sup> |1000 |100 |1000 |1000 |1000 |1000 |1000 |1000 |
| Maximum dimensions per vector field | 4096|4096|4096|4096|4096|4096|4096|4096|
| Maximum complex collections per index |40 |40 |40 |40 |40 |40 |40 |40 |
| Maximum elements across all complex collections per document&nbsp;<sup>3</sup> |3000 |3000 |3000 |3000 |3000 |3000 |3000 |3000 |
| Maximum depth of complex fields |10 |10 |10 |10 |10 |10 |10 |10 |
| Maximum [suggesters](/rest/api/searchservice/suggesters) per index |1 |1 |1 |1 |1 |1 |1 |1 |
| Maximum [scoring profiles](/rest/api/searchservice/add-scoring-profiles-to-a-search-index) per index |100 |100 |100 |100 |100 |100 |100 |100 |
| Maximum [semantic configurations](semantic-how-to-configure.md) per index |100 |100 |100 |100 |100 |100 |100 |100 |
| Maximum functions per profile |8 |8 |8 |8 |8 |8 |8 |8 |
| Maximum index size&nbsp;<sup>4</sup> | N/A | N/A | N/A | 1.88&nbsp;TB | 2.34&nbsp;TB | 100 GB| N/A | N/A |

<sup>1</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexes. Basic tier is the only tier with a lower limit of 100 fields per index.

<sup>2</sup> The upper limit on fields includes both first-level fields and nested subfields in a complex collection. For example, if an index contains 15 fields and has two complex collections with five subfields each, the field count of your index is 25. Indexes with a very large fields collection can be slow. [Limit fields and attributes](search-what-is-an-index.md#physical-structure-and-size) to just those you need, and run indexing and query test to ensure performance is acceptable.

<sup>3</sup> An upper limit exists for elements because having a large number of them significantly increases the storage required for your index. An element of a complex collection is defined as a member of that collection. For example, assume a [Hotel document with a Rooms complex collection](search-howto-complex-data-types.md#complex-collection-limits). Each room in the Rooms collection is considered an element. During indexing, the indexing engine can safely process a maximum of 3,000 elements across the document as a whole. [This limit](search-api-migration.md#upgrade-to-2019-05-06) was introduced in `api-version=2019-05-06` and applies to complex collections only, and not to string collections or to complex fields.

<sup>4</sup> For most tiers, the maximum index size is the total available storage on your search service. For S2, S3, and S3 HD services with multiple partitions, and therefore more storage, the maximum size of a single index is provided in the table. Applies to search services created after April 3, 2024.

You might find some variation in maximum limits if your service happens to be provisioned on a more powerful cluster. The limits here represent the common denominator. Indexes built to the above specifications are portable across equivalent service tiers in any region.

## Document limits

Maximum number of documents per index are:

+ 24 billion on Basic, S1, S2, S3
+ 2 billion on S3 HD
+ 288 billion on L1
+ 576 billion on L2

Maximum size of each document is approximately 16 megabytes. Document size is actually a limit on the size of the indexing API request payload, which is 16 megabytes. That payload can be a single document, or a batch of documents. For a batch with a single document, the maximum document size is 16 MB of JSON.

Document size applies to *push mode* indexing that uploads documents to a search service. If you're using an indexer for *pull mode* indexing, your source files can be any file size, subject to [indexer limits](#indexer-limits). For the blob indexer, file size limits are larger for higher tiers. For example, the S1 limit is 128 megabytes, S2 limit is 256 megabytes, and so forth.

When you estimate document size, remember to index only the fields that add value to your search scenarios. Exclude source fields that have no purpose in the queries you intend to run.

## Vector index size limits

When you index documents with vector fields, Azure AI Search constructs internal vector indexes using the algorithm parameters you provide. The size of these vector indexes is restricted by the memory reserved for vector search for your service's tier (or `SKU`). For guidance on managing and maximizing vector storage, see [Vector index size and staying under limits](vector-search-index-size.md).

Vector limits vary by:

+ [Service creation date](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date)
+ [Region](search-region-support.md)

Higher vector limits from April 2024 onwards exist on *new search services* in regions providing the extra capacity, which is most of them. If you have an older service in a supported region, check if you can [upgrade your service](search-how-to-upgrade.md) to the higher vector limits.

This table shows the progression of vector quota increases in GB over time. The quota is per partition, so if you scale a new Standard (S1) service to 6 partitions, the total vector quota is 35 multiplied by 6.

| Service creation date |Basic | S1| S2 | S3/HD | L1 | L2 |
|-----------------------|------|---|----|----|----|----|
|**Before July 1, 2023** <sup>1</sup> | 0.5 | 1 | 6 | 12 | 12 | 36 |
| **July 1, 2023 through April 3, 2024** <sup>2</sup>| 1  | 3 | 12 | 36 | 12 | 36 |
|**April 3, 2024 through May 17, 2024** <sup>3</sup> | **5**  | **35** | **150** | **300** | 12 | 36 |
|**After May 17, 2024** <sup>4</sup> | 5  | 35 | 150 | 300 | **150** | **300** |

<sup>1</sup> Initial vector limits during early preview.

<sup>2</sup> Vector limits during the later preview period. Three regions didn't have the higher limits: Germany West Central, West India, Qatar Central.

<sup>3</sup> Higher vector quota based on the larger partitions for supported tiers and regions.

<sup>4</sup> Higher vector quota for more tiers and regions based on partition size updates.

The service enforces a vector index size quota *for every partition* in your search service. Each extra partition increases the available vector index size quota. This quota is a hard limit to ensure your service remains healthy, which means that further indexing attempts once the limit is exceeded results in failure. You can resume indexing once you free up available quota by either deleting some vector documents or by scaling up in partitions.

> [!IMPORTANT]
> Higher vector limits are tied to [larger partition sizes](#partition-storage-gb). Currently, higher vector limits aren't available in the following regions, which are subject to the July–April limits.
> 
> + Israel Central
> + Qatar Central
> + ⁠Spain Central
> + South India

## Indexer limits

Maximum running times exist to provide balance and stability to the service as a whole, but larger data sets might need more indexing time than the maximum allows. If an indexing job can't complete within the maximum time allowed, try running it on a schedule. The scheduler keeps track of indexing status. If a scheduled indexing job is interrupted for any reason, the indexer can pick up where it last left off at the next scheduled run.

| Resource | Free&nbsp;<sup>1</sup> | Basic&nbsp;<sup>2</sup>| S1 | S2 | S3 | S3&nbsp;HD&nbsp;<sup>3</sup>|L1 |L2 |
|----------|------|--------|----|----|----|------------|----|----|
| Maximum indexers |3 |5 or 15|50 |200 |200 |N/A |10 |10 |
| Maximum datasources |3 |5 or 15 |50 |200 |200 |N/A |10 |10 |
| Maximum skillsets <sup>4</sup> |3 |5 or 15 |50 |200 |200 |N/A |10 |10 |
| Maximum indexing load per invocation |10,000 documents |Limited only by maximum documents |Limited only by maximum documents |Limited only by maximum documents |Limited only by maximum documents |N/A |No limit |No limit |
| Minimum schedule | 5 minutes |5 minutes |5 minutes |5 minutes |5 minutes |5 minutes |5 minutes | 5 minutes |
| Maximum running time <sup>5</sup>| 1-3 or 3-10 minutes |2 or 24 hours |2 or 24 hours |2 or 24 hours |2 or 24 hours |N/A  |2 or 24 hours |2 or 24 hours |
| Blob indexer <sup>7</sup>: maximum blob size, MB |16 |16 |128 |256 |256 |N/A  |256 |256 |
| Blob indexer: maximum characters of content extracted from a blob <sup>6</sup> <sup>8</sup> |256,000 |512,000 |4&nbsp;million |8&nbsp;million |16&nbsp;million |N/A |4&nbsp;million |4&nbsp;million |

<sup>1</sup> Free services have indexer maximum execution time of 3 minutes for blob sources and 1 minute for all other data sources. Indexer invocation is once every 180 seconds. For AI indexing that calls Foundry Tools, free services are limited to 20 free transactions per indexer per day, where a transaction is defined as a document that successfully passes through the enrichment pipeline. (Tip: You can reset an indexer to reset its count.)

<sup>2</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexers, data sources, and skillsets.

<sup>3</sup> S3 HD services don't include indexer support.

<sup>4</sup> Maximum of 30 skills per skillset.

<sup>5</sup> Regarding the 2 or 24 hour maximum duration for indexers: a 2-hour maximum is the most common and it's what you should plan for. It refers to indexers that run in the [public environment](search-howto-run-reset-indexers.md#indexer-execution-environment), which offloads computationally intensive processing and leaves more resources for queries. The 24-hour limit applies if you configure the indexer to run in a private environment using only the infrastructure that's allocated to your search service. Some older indexers are incapable of running in the public environment, and those indexers always have a 24-hour processing range. If you have unscheduled indexers that run continuously for 24 hours, you can assume those indexers couldn't be migrated to the newer infrastructure. As a general rule, for indexing jobs that can't finish within two hours, put the indexer on a [5-minute schedule](search-howto-schedule-indexers.md) so that the indexer can quickly pick up where it left off. On the Free tier, the 3-10 minute maximum running time is for indexers with skillsets.

<sup>6</sup> The maximum number of characters is based on Unicode code units, specifically UTF-16.

<sup>7</sup> When using `delimitedText` parsing mode for CSV files, a buffer size limit of 10MB per file row applies.

<sup>8</sup> When using `delimitedText` parsing mode for CSV files, the “maximum extracted content size” limit doesn't apply.

> [!NOTE]
> As stated in [Index limits](#index-limits), indexers also enforce the upper limit of 3,000 elements across all complex collections per document starting with the latest GA API version that supports complex types (`2019-05-06`) onwards. This means that if you created your indexer with a prior API version, you won't be subject to this limit. To preserve maximum compatibility, an indexer that was created with a prior API version and then updated with an API version `2019-05-06` or later, will still be **excluded** from the limits. Customers should be aware of the adverse impact of having very large complex collections (as stated previously) and we highly recommend creating any new indexers with the latest GA API version.

## Shared private link resource limits

Indexers can access other Azure resources [over private endpoints](search-indexer-howto-access-private.md) managed via the [shared private link resource API](/rest/api/searchmanagement/shared-private-link-resources). This section describes the limits associated with this capability.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Private endpoint indexer support | No | Yes | Yes | Yes | Yes | No | Yes | Yes |
| Private endpoint support for indexers with a skillset <sup>1</sup> | No | No | Yes | Yes | Yes | No | Yes | Yes |
| Private endpoint support for skillsets with an embedding skill <sup>2</sup> | No | Yes | Yes | Yes | Yes | No | Yes | Yes |
| Maximum private endpoints | N/A | 10 or 30 | 100 | 400 | 400 | N/A | 20 | 20 |
| Maximum distinct resource types <sup>3</sup> | N/A | 4 | 7 | 15 | 15 | N/A | 4 | 4 |

<sup>1</sup> AI enrichment and image analysis are computationally intensive and consume disproportionate amounts of available processing power. For this reason, private connections are disabled on lower tiers to ensure the performance and stability of the search service itself. On Basic services, private connections to a Microsoft Foundry resource are unsupported to preserve service stability. For the S1 tier, make sure the service was created with [higher limits](search-limits-quotas-capacity.md#partition-storage-gb) after April 3, 2024. Indexers with more than 2 Azure OpenAI Embedding or Azure Vision multimodal embeddings skills are restricted from running in private environment, and private connections aren't available.

<sup>2</sup> Private connections to an embedding model are supported on Basic and S1 high-capacity search services created after April 3, 2024, with the [higher limits](search-limits-quotas-capacity.md#partition-storage-gb) for storage and computational processing.

<sup>3</sup> The number of distinct resource types are computed as the number of unique `groupId` values used across all shared private link resources for a given search service, irrespective of the status of the resource.

## Synonym limits

Maximum number of synonym maps varies by tier. Each rule can have up to 20 expansions, where an expansion is an equivalent term. For example, given "cat", association with "kitty", "feline", and "felis" (the genus for cats) would count as 3 expansions.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD |L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Maximum synonym maps |3 |3|5 |10 |20 |20 | 10 | 10 |
| Maximum number of rules per map |5000 |20000|20000 |20000 |20000 |20000 | 20000 | 20000  |

## Index alias limits

Maximum number of [index aliases](search-how-to-alias.md) varies by tier and [service creation date](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date). On all tiers, if the service was created after October 2022, the maximum number of aliases is double the maximum number of indexes allowed. If the service was created before October 2022, the limit is the number of indexes allowed.

| Service creation date | Free | Basic | S1 | S2 | S3 | S3 HD |L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Before October 2022 | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 1000 per partition or 3000 per service | 10 | 10 |
| After October 2022 | 6 | 30 | 100 | 400 | 400 | 2000 per partition or 6000 per service | 20 | 20 |

<sup>1</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexes.

## Agentic retrieval limits

A [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) specifies one or more [knowledge sources](agentic-knowledge-source-overview.md) and a [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) that controls the level of large language model (LLM) processing for [agentic retrieval](agentic-retrieval-overview.md). Limits vary by pricing tier and reasoning effort level.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 |
|--|--|--|--|--|--|--|--|--|
| Maximum knowledge sources per service | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 0 | 10 | 10 |
| Maximum knowledge bases per service | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 0 | 10 | 10 |
| Maximum knowledge sources per knowledge base (`minimal`) <sup>2</sup> | 3 | 5 or 10 <sup>1</sup> | 10 | 10 | 10 | 0 | 10 | 10 |
| Maximum knowledge sources per knowledge base  (`low`) | 3 | 3 | 3 | 3 | 3 | 0 | 3 | 3 |
| Maximum knowledge sources per knowledge base  (`medium`) | 3 | 5 | 5 | 5 | 5 | 0 | 5 | 5 |

<sup>1</sup> Basic services created before April 3, 2024 have lower limits (5) on knowledge sources and knowledge bases.

<sup>2</sup> The `minimal` reasoning effort supports more knowledge sources than `low` or `medium` because it bypasses LLM-based query planning.

## Data limits (AI enrichment)

Data limits apply to an [AI enrichment pipeline](cognitive-search-concept-intro.md) that makes calls to Azure Language in Foundry Tools for [entity recognition](cognitive-search-skill-entity-recognition-v3.md), [entity linking](cognitive-search-skill-entity-linking-v3.md), [key phrase extraction](cognitive-search-skill-keyphrases.md), [sentiment analysis](cognitive-search-skill-sentiment-v3.md), [language detection](cognitive-search-skill-language-detection.md), and [personal-information detection](cognitive-search-skill-pii-detection.md). The maximum size of a record should be 50,000 characters as measured by [`String.Length`](/dotnet/api/system.string.length). If you need to break up your data before sending it to the sentiment analyzer, use the [Text Split skill](cognitive-search-skill-textsplit.md).

## Throttling limits

API requests are throttled as the system approaches peak capacity. Throttling behaves differently for different APIs. Query APIs (Search/Suggest/Autocomplete) and indexing APIs throttle dynamically based on the load on the service. Index APIs and service operations API have static request rate limits.

Static rate request limits for operations related to an index:

+ List Indexes (GET /indexes): 3 per second per search unit
+ Get Index (GET /indexes/myindex): 10 per second per search unit
+ Create Index (POST /indexes): 12 per minute per search unit
+ Create or Update Index (PUT /indexes/myindex): 6 per second per search unit
+ Delete Index (DELETE /indexes/myindex): 12 per minute per search unit

Static rate request limits for operations related to a service:

+ Service Statistics (GET /servicestats): 4 per second per search unit

### Semantic ranker throttling limits

[Semantic ranker](search-get-started-semantic.md) uses a queuing system to manage concurrent requests. This system allows search services get the highest number of queries per second possible. When the limit of concurrent requests is reached, additional requests are placed in a queue. If the queue is full, further requests are rejected and must be retried.

Total semantic ranker queries per second varies based on the following factors:

+ The tier of the search service. Both queue capacity and concurrent request limits vary by tier.
+ The number of search units in the search service. The simplest way to increase the maximum number of concurrent semantic ranker queries is to [add more search units to your search service](search-capacity-planning.md#how-to-change-capacity).
+ The total available semantic ranker capacity in the region.
+ The amount of time it takes to serve a query using semantic ranker. This varies based on how busy the search service is.

The following table describes the semantic ranker throttling limits by tier, subject to available capacity in the region. You can contact Microsoft support to request a limit increase.

| Resource | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 |
|----------|-------|----|----|----|-------|----|----|
| Maximum concurrent requests (per search unit) | 2 | 3 | 4 | 4 | 4 | 4 | 4 |
| Maximum request queue size (per search unit) | 4 | 6 | 8 | 8 | 8 | 8 | 8 |

## API request limits

Limits on queries exist because unbounded queries can destabilize your search service. Typically, such queries are created programmatically. If your application generates search queries programmatically, we recommend designing it in such a way that it doesn't generate queries of unbounded size.

Limits on payloads exist for similar reasons, ensuring the stability of your search service. The limit applies to the entire request, inclusive of all its components. For example, if the request batches several documents or commands, the entire request must fit within the supported limit.

If you must exceed a supported limit, you should [test your workload](search-performance-analysis.md#develop-baseline-numbers) so that you know what to expect.

Except where noted, the following API requests apply to all programmable interfaces, including the Azure SDKs.

General:

+ Supported maximum payload limit is 16 MB for indexing and query request via REST API and SDKs.
+ Maximum 8-KB URL length (applies to REST APIs only).

Indexing APIs:

+ Supported maximum 1,000 documents per batch of index uploads, merges, or deletes.
+ Each request supports between 1 and 32,000 indexing actions.

Query APIs:

+ Maximum 10 fields in a vector query
+ Maximum 32 fields in $orderby clause.
+ Maximum 100,000 characters in a search clause.
+ Maximum number of clauses in search is 3,000.
+ Maximum limits on [wildcard](query-lucene-syntax.md#bkmk_wildcard) and [regular expression](query-lucene-syntax.md#bkmk_regex) queries, as enforced by [Lucene](https://lucene.apache.org/core/7_0_1/core/org/apache/lucene/util/automaton/RegExp.html). It caps the number of patterns, variations, or matches to 1,000 instances. This limit is in place to avoid engine overload.

Search terms:

+ Supported maximum search term size is 32,766 bytes (32 KB minus 2 bytes) of UTF-8 encoded text. Applies to keyword search and the text property of vector search.
+ Supported maximum search term size is 1,000 characters for [prefix search](query-simple-syntax.md#prefix-queries) and [regex search](query-lucene-syntax.md#bkmk_regex).

## API response limits

+ Maximum 1,000 documents returned per page of search results
+ Maximum 100 suggestions returned per Suggest API request

The search engine returns 50 results by default, but you can [override this parameter](search-pagination-page-layout.md#number-of-results-in-the-response) up to the maximum limit.

## API key limits

API keys are used for service authentication. There are two types. Admin keys are specified in the request header and grant full read-write access to the service. Query keys are read-only, specified on the URL, and typically distributed to client applications.

+ Maximum of 2 admin keys per service
+ Maximum of 50 query keys per service
