---
title: Service limits for tiers and skus
titleSuffix: Azure AI Search
description: Service limits used for capacity planning and maximum limits on requests and responses for Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: cognitive-search
ms.topic: conceptual
ms.date: 06/13/2024
ms.custom:
  - references_regions
  - build-2024
---

# Service limits in Azure AI Search

Maximum limits on storage, workloads, and quantities of indexes and other objects depend on whether you [create Azure AI Search](search-create-service-portal.md) at **Free**, **Basic**, **Standard**, or **Storage Optimized** pricing tiers.

+ **Free** is a multitenant shared service that comes with your Azure subscription. 

+ **Basic** provides dedicated computing resources for production workloads at a smaller scale, but shares some networking infrastructure with other tenants.

+ **Standard** runs on dedicated machines with more storage and processing capacity at every level. Standard comes in four levels: S1, S2, S3, and S3 HD. S3 High Density (S3 HD) is engineered for [multi-tenancy](search-modeling-multitenant-saas-applications.md) and large quantities of small indexes (3,000 indexes per service). S3 HD doesn't provide the [indexer feature](search-indexer-overview.md) and data ingestion must use APIs that push data from source to index. 

+ **Storage Optimized** runs on dedicated machines with more total storage, storage bandwidth, and memory than **Standard**. This tier targets large, slow-changing indexes. Storage Optimized comes in two levels: L1 and L2.

## Subscription limits
[!INCLUDE [azure-search-limits-per-subscription](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-subscription.md)]

## Service limits
[!INCLUDE [azure-search-limits-per-service](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-service.md)]

<a name="index-limits"></a>

## Index limits

| Resource | Free | Basic&nbsp;<sup>1</sup>  | S1 | S2 | S3 | S3&nbsp;HD | L1 | L2 |
|----------|------|--------|----|----|----|------------|----|----|
| Maximum indexes |3 |5 or 15 |50 |200 |200 |1000 per partition or 3000 per service |10 |10 |
| Maximum simple fields per index&nbsp;<sup>2</sup> |1000 |100 |1000 |1000 |1000 |1000 |1000 |1000 |
| Maximum dimensions per vector field | 4098|4098|4098|4098|4098|4098|4098|4098|
| Maximum complex collections per index |40 |40 |40 |40 |40 |40 |40 |40 |
| Maximum elements across all complex collections per document&nbsp;<sup>3</sup> |3000 |3000 |3000 |3000 |3000 |3000 |3000 |3000 |
| Maximum depth of complex fields |10 |10 |10 |10 |10 |10 |10 |10 |
| Maximum [suggesters](/rest/api/searchservice/suggesters) per index |1 |1 |1 |1 |1 |1 |1 |1 |
| Maximum [scoring profiles](/rest/api/searchservice/add-scoring-profiles-to-a-search-index) per index |100 |100 |100 |100 |100 |100 |100 |100 |
| Maximum functions per profile |8 |8 |8 |8 |8 |8 |8 |8 |
| Maximum index size&nbsp;<sup>4</sup> | N/A | N/A | N/A | 1.88&nbsp;TB | 2.34&nbsp;TB | 100 GB| N/A | N/A |

<sup>1</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexes. Basic tier is the only tier with a lower limit of 100 fields per index. 

<sup>2</sup> The upper limit on fields includes both first-level fields and nested subfields in a complex collection. For example, if an index contains 15 fields and has two complex collections with five subfields each, the field count of your index is 25. Indexes with a very large fields collection can be slow. [Limit fields and attributes](search-what-is-an-index.md#physical-structure-and-size) to just those you need, and run indexing and query test to ensure performance is acceptable.

<sup>3</sup> An upper limit exists for elements because having a large number of them significantly increases the storage required for your index. An element of a complex collection is defined as a member of that collection. For example, assume a [Hotel document with a Rooms complex collection](search-howto-complex-data-types.md#indexing-complex-types), each room in the Rooms collection is considered an element. During indexing, the indexing engine can safely process a maximum of 3,000 elements across the document as a whole. [This limit](search-api-migration.md#upgrade-to-2019-05-06) was introduced in `api-version=2019-05-06` and applies to complex collections only, and not to string collections or to complex fields.

<sup>4</sup> On most tiers, maximum index size is all available storage on your search service. For S2, S3, and S3 HD, the maximum size of any index is the number provided in the table. Applies to search services created after April 3, 2024.

You might find some variation in maximum limits if your service happens to be provisioned on a more powerful cluster. The limits here represent the common denominator. Indexes built to the above specifications are portable across equivalent service tiers in any region.

<a name="document-limits"></a>

## Document limits 

You can have approximately 24 billion documents per index on Basic, S1, S2, S3, L1, and L2 search services. For S3 HD, the limit is 2 billion documents per index. Each instance of a complex collection counts as a separate document in terms of these limits.

### Document size limits per API call

The maximum document size when calling an Index API is approximately 16 megabytes.

Document size is actually a limit on the size of the Index API request body. Since you can pass a batch of multiple documents to the Index API at once, the size limit realistically depends on how many documents are in the batch. For a batch with a single document, the maximum document size is 16 MB of JSON.

When estimating document size, remember to consider only those fields that add value to your search scenarios, and exclude any source fields that have no purpose in the queries you intend to run.

## Vector index size limits

When you index documents with vector fields, Azure AI Search constructs internal vector indexes using the algorithm parameters you provide. The size of these vector indexes is restricted by the memory reserved for vector search for your service's tier (or `SKU`).

The service enforces a vector index size quota **for every partition** in your search service. Each extra partition increases the available vector index size quota. This quota is a hard limit to ensure your service remains healthy, which means that further indexing attempts once the limit is exceeded results in failure. You can resume indexing once you free up available quota by either deleting some vector documents or by scaling up in partitions.

The table describes the vector index size quota per partition across the service tiers. For context, it includes:

+ [Partition storage limits](#service-limits) for each tier, repeated here for context.
+ Amount of each partition (in GB) available for vector indexes (created when you add vector fields to an index).
+ Approximate number of embeddings (floating point values) per partition.

Use the [GET Service Statistics](/rest/api/searchservice/get-service-statistics) to retrieve your vector index size quota or review the **Indexes** page or **Usage** tab in the Azure portal.

Vector limits vary by service creation date and tier. To check the age of your search service and learn more about vector indexes, see [Vector index size and staying under limits](vector-search-index-size.md).

### Vector limits on services created after May 17, 2024

The highest vector limits are available on search services created after May 17, 2024 in a [supported region](#supported-regions-with-higher-storage-limits).

| Tier   | Storage quota (GB) | Vector quota per partition (GB) | 
|--------|--------------------|---------------------------------|
| Basic | 15                  | 5      |
| S1    | 160                 | 35     |
| S2    | 512                 | 150    |
| S3    | 1,024               | 300    |
| L1    | 2,048               | 150    |
| L2    | 4,096               | 300    |

### Vector limits on services created between April 3, 2024 and May 17, 2024

The following vector limits are available on search services created after April 3, 2024 in a [supported region](#supported-regions-with-higher-storage-limits).

| Tier   | Storage quota (GB) | Vector quota per partition (GB) |
|--------|--------------------|---------|
| Basic | 15                  | 5       |
| S1    | 160                 | 35      |
| S2    | 350                 | 100     |
| S3    | 700                 | 200     |
| L1    | 1,000               | 12      |
| L2    | 2,000               | 36      |

Notice that L1 and L2 limits are unchanged in the April 3 rollout.

### Vector limits on services created between July 1, 2023 and April 3, 2024

The following limits applied to new services created between July 1 and April 3, 2024, except for the following regions, which have the original limits from before July 1, 2023:

+ Germany West Central
+ West India
+ Qatar Central

All other regions have these limits:

| Tier   | Storage quota (GB) | Vector quota per partition (GB) |
|--------|--------------------|---------------|
| Basic | 2                  | 1              |
| S1    | 25                 | 3              |
| S2    | 100                | 12             |
| S3    | 200                | 36             |
| L1    | 1,000              | 12             |
| L2    | 2,000              | 36             |

### Vector limits on services created before July 1, 2023

| Tier   | Storage quota (GB) | Vector quota per partition (GB) |
|--------|--------------------|--------------|
| Basic | 2                  | 0.5           |
| S1    | 25                 | 1             |
| S2    | 100                | 6             |
| S3    | 200                | 12            |
| L1    | 1,000              | 12            |
| L2    | 2,000              | 36            |

## Indexer limits

Maximum running times exist to provide balance and stability to the service as a whole, but larger data sets might need more indexing time than the maximum allows. If an indexing job can't complete within the maximum time allowed, try running it on a schedule. The scheduler keeps track of indexing status. If a scheduled indexing job is interrupted for any reason, the indexer can pick up where it last left off at the next scheduled run.

| Resource | Free&nbsp;<sup>1</sup> | Basic&nbsp;<sup>2</sup>| S1 | S2 | S3 | S3&nbsp;HD&nbsp;<sup>3</sup>|L1 |L2 |
|----------|------|--------|----|----|----|------------|----|----|
| Maximum indexers |3 |5 or 15|50 |200 |200 |N/A |10 |10 |
| Maximum datasources |3 |5 or 15 |50 |200 |200 |N/A |10 |10 |
| Maximum skillsets <sup>4</sup> |3 |5 or 15 |50 |200 |200 |N/A |10 |10 |
| Maximum indexing load per invocation |10,000 documents |Limited only by maximum documents |Limited only by maximum documents |Limited only by maximum documents |Limited only by maximum documents |N/A |No limit |No limit |
| Minimum schedule | 5 minutes |5 minutes |5 minutes |5 minutes |5 minutes |5 minutes |5 minutes | 5 minutes |
| Maximum running time <sup>5</sup>| 1-3 minutes |2 or 24 hours |2 or 24 hours |2 or 24 hours |2 or 24 hours |N/A  |2 or 24 hours |2 or 24 hours |
| Maximum running time for indexers with a skillset <sup>6</sup> | 3-10 minutes |2 hours |2 hours |2 hours |2 hours |N/A  |2 hours |2 hours |
| Blob indexer: maximum blob size, MB |16 |16 |128 |256 |256 |N/A  |256 |256 |
| Blob indexer: maximum characters of content extracted from a blob |32,000 |64,000 |4&nbsp;million |8&nbsp;million |16&nbsp;million |N/A |4&nbsp;million |4&nbsp;million |

<sup>1</sup> Free services have indexer maximum execution time of 3 minutes for blob sources and 1 minute for all other data sources. Indexer invocation is once every 180 seconds. For AI indexing that calls into Azure AI services, free services are limited to 20 free transactions per indexer per day, where a transaction is defined as a document that successfully passes through the enrichment pipeline (tip: you can reset an indexer to reset its count).

<sup>2</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexers, data sources, and skillsets.

<sup>3</sup> S3 HD services don't include indexer support.

<sup>4</sup> Maximum of 30 skills per skillset.

<sup>5</sup> Regarding the 2 or 24 hour maximum duration for indexers: a 2-hour maximum is the most common and it's what you should plan for. The 24-hour limit is from an older indexer implementation. If you have unscheduled indexers that run continuously for 24 hours, it's because those indexers couldn't be migrated to the newer infrastructure. As a general rule, for indexing jobs that can't finish within two hours, put the indexer on a [2-hour schedule](search-howto-schedule-indexers.md). When the first 2-hour interval is complete, the indexer picks up where it left off when starting the next 2-hour interval.

<sup>6</sup> Skillset execution, and image analysis in particular, are computationally intensive and consume disproportionate amounts of available processing power. Running time for these workloads is shorter so that other jobs in the queue have more opportunity to run.

> [!NOTE]
> As stated in the [Index limits](#index-limits), indexers will also enforce the upper limit of 3000 elements across all complex collections per document starting with the latest GA API version that supports complex types (`2019-05-06`) onwards. This means that if you've created your indexer with a prior API version, you will not be subject to this limit. To preserve maximum compatibility, an indexer that was created with a prior API version and then updated with an API version `2019-05-06` or later, will still be **excluded** from the limits. Customers should be aware of the adverse impact of having very large complex collections (as stated previously) and we highly recommend creating any new indexers with the latest GA API version.

## Shared private link resource limits

Indexers can access other Azure resources [over private endpoints](search-indexer-howto-access-private.md) managed via the [shared private link resource API](/rest/api/searchmanagement/shared-private-link-resources). This section describes the limits associated with this capability.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Private endpoint indexer support | No | Yes | Yes | Yes | Yes | No | Yes | Yes |
| Private endpoint support for indexers with a skillset<sup>1</sup> | No | No | No | Yes | Yes | No | Yes | Yes |
| Maximum private endpoints | N/A | 10 or 30 | 100 | 400 | 400 | N/A | 20 | 20 |
| Maximum distinct resource types<sup>2</sup> | N/A | 4 | 7 | 15 | 15 | N/A | 4 | 4 |

<sup>1</sup> AI enrichment and image analysis are computationally intensive and consume disproportionate amounts of available processing power. For this reason, private connections are disabled on lower tiers to ensure the performance and stability of the search service itself.

<sup>2</sup> The number of distinct resource types are computed as the number of unique `groupId` values used across all shared private link resources for a given search service, irrespective of the status of the resource.

## Synonym limits

Maximum number of synonym maps varies by tier. Each rule can have up to 20 expansions, where an expansion is an equivalent term. For example, given "cat", association with "kitty", "feline", and "felis" (the genus for cats) would count as 3 expansions.

| Resource | Free | Basic | S1 | S2 | S3 | S3-HD |L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Maximum synonym maps |3 |3|5 |10 |20 |20 | 10 | 10 |
| Maximum number of rules per map |5000 |20000|20000 |20000 |20000 |20000 | 20000 | 20000  |

## Index alias limits

Maximum number of [index aliases](search-how-to-alias.md) varies by tier. In all tiers, the maximum number of aliases is double the maximum number of indexes allowed.

| Resource | Free | Basic | S1 | S2 | S3 | S3-HD |L1 | L2 |
|----------|------|-------|----|----|----|-------|----|----|
| Maximum aliases |6 |10 or 30 |100 |400 |400 |2000 per partition or 6000 per service |20 |20 |

## Data limits (AI enrichment)

An [AI enrichment pipeline](cognitive-search-concept-intro.md) that makes calls to an Azure AI Language resource for [entity recognition](cognitive-search-skill-entity-recognition-v3.md), [entity linking](cognitive-search-skill-entity-linking-v3.md), [key phrase extraction](cognitive-search-skill-keyphrases.md), [sentiment analysis](cognitive-search-skill-sentiment-v3.md), [language detection](cognitive-search-skill-language-detection.md), and [personal-information detection](cognitive-search-skill-pii-detection.md) is subject to data limits. The maximum size of a record should be 50,000 characters as measured by [`String.Length`](/dotnet/api/system.string.length). If you need to break up your data before sending it to the sentiment analyzer, use the [Text Split skill](cognitive-search-skill-textsplit.md).

## Throttling limits

API requests are throttled as the system approaches peak capacity. Throttling behaves differently for different APIs. Query APIs (Search/Suggest/Autocomplete) and indexing APIs throttle dynamically based on the load on the service. Index APIs and service operations API have static request rate limits. 

Static rate request limits for operations related to an index:

+ List Indexes (GET /indexes): 3 per second per search unit
+ Get Index (GET /indexes/myindex): 10 per second per search unit
+ Create Index (POST /indexes): 12 per second per search unit
+ Create or Update Index (PUT /indexes/myindex): 6 per second per search unit
+ Delete Index (DELETE /indexes/myindex): 12 per second per search unit 

Static rate request limits for operations related to a service:

+ Service Statistics (GET /servicestats): 4 per second per search unit

L2 reranking using the semantic reranker has an expected volume:

+ Up to 10 concurrent queries per replica. If you anticipate consistent throughput requirements near, at, or higher than this level, please file a support ticket so that we can provision for your workload.

## API request limits

* Maximum of 16 MB per request <sup>1</sup>
* Maximum 8-KB URL length
* Maximum 1,000 documents per batch of index uploads, merges, or deletes
* Maximum 32 fields in $orderby clause
* Maximum 100,000 characters in a search clause
* The maximum number of clauses in `search` (expressions separated by AND or OR) is 1024
* Maximum search term size is 32,766 bytes (32 KB minus 2 bytes) of UTF-8 encoded text
* Maximum search term size is 1,000 characters for [prefix search](query-simple-syntax.md#prefix-queries) and [regex search](query-lucene-syntax.md#bkmk_regex)
* [Wildcard search](query-lucene-syntax.md#bkmk_wildcard) and [Regular expression search](query-lucene-syntax.md#bkmk_regex) are limited to a maximum of 1,000 states when processed by [Lucene](https://lucene.apache.org/core/7_0_1/core/org/apache/lucene/util/automaton/RegExp.html). 

<sup>1</sup> In Azure AI Search, the body of a request is subject to an upper limit of 16 MB, imposing a practical limit on the contents of individual fields or collections that aren't otherwise constrained by theoretical limits (see [Supported data types](/rest/api/searchservice/supported-data-types) for more information about field composition and restrictions).

Limits on query size and composition exist because unbounded queries can destabilize your search service. Typically, such queries are created programmatically. If your application generates search queries programmatically, we recommend designing it in such a way that it doesn't generate queries of unbounded size.

## API response limits

* Maximum 1,000 documents returned per page of search results
* Maximum 100 suggestions returned per Suggest API request

## API key limits

API keys are used for service authentication. There are two types. Admin keys are specified in the request header and grant full read-write access to the service. Query keys are read-only, specified on the URL, and typically distributed to client applications.

* Maximum of 2 admin keys per service
* Maximum of 50 query keys per service
