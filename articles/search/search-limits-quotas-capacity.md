---
title: Service Limits for Tiers and SKUs
description: Service limits used for capacity planning and maximum limits on requests and responses for Azure AI Search.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.topic: limits-and-quotas
ms.date: 09/04/2026
ms.update-cycle: 180-days
ai-usage: ai-assisted
ms.custom:
  - references_regions
  - doc-kit-assisted
#customer intent: As a developer making decisions about the infrastructure we use, planning to optimize for usage need, capacity, and cost, I want to understand the limits, quotas, and capacities associated with Azure AI Search services, detailing how these factors depend on the chosen pricing tier.
---

# Service limits in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Maximum limits on storage, workloads, and quantities of indexes and other objects depend on the pricing model of your Azure AI Search service.

Azure AI Search supports two pricing models, each with associated service tiers. The tier you select impacts the service limits outlined in this guidance.

- **Dedicated**: Fixed pricing measured by Search Units (SUs). Service tier options include: Basic, Standard (S1-S3, including S3 HD), Storage Optimized (L1-L2), and a Free tier with limited search service capabilities.
- **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. The current preview tier is: Serverless Developer. Limits are defined by per-index caps, per-service object counts, and Serverless throttling behavior. 

[!INCLUDE [Serverless preview](./includes/previews/preview-serverless.md)]

To learn more, see [Choose a pricing model and service tier](search-sku-tier.md).

## Diagnose quota, capacity, or limit failures

Quota and capacity failures come from separate controls. Use the error from the completed operation to find which one applies.

If a create, scale, or upgrade operation is still running, wait for the provisioning state to become `Succeeded` or `Failed`. An operation in progress isn't evidence of a quota or capacity problem. If a scale operation fails, see [Errors during scaling](search-capacity-planning.md#errors-during-scaling).

| Failure | Likely cause | First action |
| --- | --- | --- |
| Service creation blocked in a subscription and region | Subscription quota | In the **Quotas** service, check the limit for your tier and region, then [request more services](search-create-service-portal.md#add-more-services-to-your-subscription). |
| Create, scale, or upgrade fails even though quota is available | Regional capacity constraint | Check the footnotes in [region support](search-region-support.md) for constrained tiers, then [choose another region](search-region-capacity.md#capacity-constraint-options). |
| Replica, partition, tier, or object request rejected | Service or index limit | Compare your configuration and object counts with [service limits](#service-limits) and [index limits](#index-limits). |
| The search service returns throttling responses under load | Throttling | Reduce the request rate or add search units. See [Throttling limits](#throttling-limits). |
| Indexing fails near a storage or vector limit | Storage or vector quota | Compare `storageSize` with [partition storage](#partition-storage-gb) for disk and `vectorIndexSize` with [vector index size limits](#vector-index-size-limits) for memory. |
| Indexer, skill, or vectorizer reports a 429 from another service | Azure OpenAI or other service quota | Follow the quota guidance for the service that issued the error, such as [Azure OpenAI](/azure/ai-services/openai/quotas-limits). |

Available subscription quota doesn't guarantee regional capacity, and requesting more quota doesn't resolve a capacity constraint. If the failure persists, open an Azure support request that includes the subscription, region, tier, requested configuration, full error text, UTC time, and any correlation or operation ID.

## Subscription limits
<!-- [!INCLUDE [azure-search-limits-per-subscription](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-subscription.md)] -->

You can create multiple *billable* search services (Basic and higher), up to the maximum number of services allowed at each tier, per region. For example, you can create up to 16 services at the Basic tier and another 16 services at the S1 tier within the same subscription and region. You can then create an additional 16 Basic services in another region for a combined total of 32 Basic services under the same subscription. For more information about service tiers, see [Choose a pricing model and service tier](/azure/search/search-sku-tier).

You can raise maximum service limits by request. If you need more services within the same subscription, [file a support request](/azure/search/search-create-service-portal#add-more-services-to-a-subscription).

| Resource | Free <sup>1</sup> | Basic | S1 | S2 | S3 | S3&nbsp;HD | L1 | L2 | Serverless Developer |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Maximum services per region | 1 | 16 | 16 | 8 | 6 | 6 | 6 | 6 | 5 |
| Maximum search units (SU)<sup>2</sup> | N/A | 3 SU | 36 SU | 36 SU | 36 SU | 36 SU | 36 SU | 36 SU | N/A |

<sup>1</sup> You can have one free search service per Azure subscription. The free tier is based on infrastructure shared with other customers. Because the hardware isn't dedicated, scale-up isn't supported, and storage is limited to 50 MB. A free search service might be deleted after extended periods of inactivity to make room for more services.

<sup>2</sup> Search units (SU) are billing units, allocated as either a *replica* or a *partition*. You need both. To learn more about SU combinations, see [Estimate and manage capacity of a search service](/azure/search/search-capacity-planning). 
<!-- End include -->

## Service limits
<!-- [!INCLUDE [azure-search-limits-per-service](~/reusable-content/ce-skilling/azure/includes/azure-search-limits-per-service.md)] -->

In the Dedicated pricing model, plan capacity by multiplying replicas by partitions (search units).

| Resource | Free | Basic | S1 | S2 | S3 | S3&nbsp;HD | L1 | L2 | Serverless Developer |
| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |
| Partitions | N/A | 3 <sup>1</sup> | 12 | 12 | 12 | 3 | 12 | 12 | N/A |
| Replicas | N/A | 3 | 12 | 12 | 12 | 12 | 12 | 12 | N/A |

<sup>1</sup> The Basic tier supports three partitions and three replicas, for a total of nine search units (SU) on [new search services](/azure/search/search-create-service-portal) created after April 3, 2024. Older Basic services are limited to one partition and three replicas.

A search service is subject to a maximum storage limit (partition size multiplied by the number of partitions) or a hard limit on the [maximum number of indexes](/azure/search/search-limits-quotas-capacity#index-limits) or [indexers](/azure/search/search-limits-quotas-capacity#indexer-limits), whichever limit comes first.

Service-level agreements (SLAs) apply to billable services that have two or more replicas for query workloads, or three or more replicas for query and indexing workloads. The number of partitions isn't an SLA consideration. For more information, see [Reliability in Azure AI Search](/azure/search/search-reliability#high-availability).

Free services don't have fixed partitions or replicas and share resources with other subscribers.

### Partition storage (GB)

Per-service storage limits vary based on two factors: [service creation date](/azure/search/search-how-to-upgrade#check-your-service-creation-or-upgrade-date) and [region](/azure/search/search-region-support). Most supported regions offer higher limits for [newer services](/azure/search/search-create-service-portal).

This table shows the progression of storage quota increases in GB over time. Starting in April 2024, higher capacity partitions came online in the regions listed in the footnotes. If you have an older service in a supported region, check if you can [upgrade your service](/azure/search/search-how-to-upgrade) to get higher storage limits.

| Service creation date |Basic | S1| S2 | S3/HD | L1 | L2 | Serverless Developer |
|---|---|---|---|---|---|---|---|
| Before April 3, 2024 | 2  | 25 | 100 | 200 | 1,024 | 2,048 | N/A |
| April 3, 2024 through May 17, 2024 <sup>1</sup> | **15**   | **160**  | **512**  | **1,024**  | 1,024 | 2,048 | N/A |
| After May 17, 2024 <sup>2</sup> | 15  | 160 | 512 | 1,024 | **2,048**  | **4,096**  | N/A |
| After February 10, 2025 <sup>3</sup> | 15  | 160 | 512 | 1,024 | 2,048  | 4,096  | N/A |

<sup>1</sup> Higher capacity storage for Basic, S1, S2, and S3 in these regions. **Americas**: Brazil South, Canada Central, Canada East, East US, East US 2, Central US, North Central US, South Central US, West US, West US 2, West US 3, West Central US. **Europe**: France Central. Italy North, North Europe, Norway East, Poland Central, Switzerland North, Sweden Central, UK South, UK West. **Middle East**:  UAE North. **Africa**: South Africa North. **Asia Pacific**: Australia East, Australia Southeast, Central India, Jio India West, East Asia, Southeast Asia, Japan East, Japan West, Korea Central, Korea South.

<sup>2</sup> Higher capacity storage for L1 and L2. More regions provide higher capacity at every billable tier. **Americas:** East US 2 EUAP. **Europe**: Germany North, Germany West Central, Switzerland West. **Azure Government**: Texas, Arizona, Virginia. **Africa**: South Africa North. **Asia Pacific**: China North 3, China East 3.

<sup>3</sup> Higher capacity storage is available in West Europe.

> [!IMPORTANT]
> Currently, higher storage limits aren't available in the following regions, which are subject to the pre-April 3 limits.
>
> + Israel Central
> + Qatar Central
> + Spain Central
> + South India

<!-- End include -->

## Index limits

| Resource | Free | Basic <sup>1</sup> | S1 | S2 | S3 | S3 HD | L1 | L2 | Serverless Developer |
|----------|------|--------------------|----|----|----|--------|----|----|------------|
| Maximum indexes | 3 | 5 or 15 | 50 | 200 | 200 | 1000 per partition or 3000 per service | 10 | 10 | 30 |
| Maximum simple fields per index <sup>2</sup> | 1000 | 100 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| Maximum dimensions per vector field | 4096 | 4096 | 4096 | 4096 | 4096 | 4096 | 4096 | 4096 | 4096 |
| Maximum complex collections per index | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 | 40 |
| Maximum elements across all complex collections per document <sup>3</sup> | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 | 3000 |
| Maximum depth of complex fields | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 | 10 |
| Maximum suggesters per index | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Maximum scoring profiles per index | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| Maximum semantic configurations per index | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 |
| Maximum functions per profile | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| Maximum index size <sup>4</sup> | N/A | N/A | N/A | 1.88 TB | 2.34 TB | 100 GB | N/A | N/A | 1 GB |

<sup>1</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexes. Basic tier is the only tier with a lower limit of 100 fields per index.

<sup>2</sup> The upper limit on fields includes both first-level fields and nested subfields in a complex collection. For example, if an index contains 15 fields and has two complex collections with five subfields each, the field count of your index is 25. Indexes with a very large fields collection can be slow. [Limit fields and attributes](search-what-is-an-index.md#physical-structure-and-size) to just those you need, and run indexing and query test to ensure performance is acceptable.

<sup>3</sup> An upper limit exists for elements because having a large number of them significantly increases the storage required for your index. An element of a complex collection is defined as a member of that collection. For example, assume a [Hotel document with a Rooms complex collection](search-howto-complex-data-types.md#complex-collection-limits). Each room in the Rooms collection is considered an element. During indexing, the indexing engine can safely process a maximum of 3,000 elements across the document as a whole. [This limit](search-api-migration.md#upgrade-to-2019-05-06) was introduced in `api-version=2019-05-06` and applies to complex collections only, and not to string collections or to complex fields.

<sup>4</sup> For most tiers, the maximum index size is the total available storage on your search service. For S2, S3, and S3 HD services with multiple partitions, and therefore more storage, the maximum size of a single index is provided in the table. Applies to search services created after April 3, 2024. Indexes for services set up with the Serverless model (Preview) have a set maximum size provided in the table.

You might find some variation in maximum limits if your service happens to be provisioned on a more powerful cluster. The limits here represent the common denominator. Indexes built to the above specifications are portable across equivalent service tiers in any region.

## Document limits

Each index supports up to the following number of documents:

+ 24 billion on Basic, S1, S2, and S3
+ 2 billion on S3 HD
+ 288 billion on L1
+ 576 billion on L2

Each document can be up to approximately 16 MB in size. The document size limit actually applies to the size of the indexing API request payload, which is 16 MB. That payload can be a single document or a batch of documents. For a batch with a single document, the maximum document size is 16 MB of JSON.

The document size limit applies to *push mode* indexing that uploads documents to a search service. If you're using an indexer for *pull mode* indexing, your source files can be any file size, subject to [indexer limits](#indexer-limits). For the blob indexer, file size limits are larger for higher tiers. For example, the S1 limit is 128 MB, and the S2 limit is 256 MB.

When you estimate document size, remember to index only the fields that add value to your search scenarios. Exclude source fields that have no purpose in the queries you intend to run.

## Vector index size limits

When you index documents with vector fields, Azure AI Search constructs internal vector indexes using the algorithm parameters you provide.

The size of these vector indexes is restricted by:
- The memory reserved for vector search for your service's tier (or `SKU`) in the Dedicated pricing model. 
- Per-index storage limits in the Serverless pricing model.

For guidance on managing and maximizing vector storage, see [Vector index size and staying under limits](vector-search-index-size.md).

Vector limits vary by:

- [Service creation date](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date)
- [Region](search-region-support.md)
- [Pricing model and service tier selected](search-sku-tier.md)

Higher vector limits from April 2024 onwards exist on *new search services* in regions providing the extra capacity, which is most of them. If you have an older service in a supported region, check if you can [upgrade your service](search-how-to-upgrade.md) to the higher vector limits.


In the Serverless pricing model, vector limits are defined per index rather than per partition.

- **Maximum vector index size per index (Serverless):** 300 MB  
  - This size represents approximately **30% of total index storage**, consistent with the vector-to-storage ratio used in Dedicated service tiers.
  - This size is a hard limit per index. Attempts to exceed this limit during indexing fail.

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


The service enforces a vector index size quota:
- **Dedicated:** Per partition in your search service  
- **Serverless:** Per index

This quota is a hard limit to ensure your service remains healthy. Further indexing attempts once the limit is exceeded result in failure. You can resume indexing once you free up available quota by:
- Deleting vector documents
- Reducing vector size or dimensionality
- (Dedicated only) Scaling out partitions

> [!IMPORTANT]
> Higher vector limits are tied to [larger partition sizes](#partition-storage-gb). Currently, higher vector limits aren't available in the following regions, which are subject to the July–April limits.
> 
> + Israel Central
> + Qatar Central
> + ⁠Spain Central
> + South India

## Indexer limits

Maximum running times exist to provide balance and stability to the service as a whole, but larger data sets might need more indexing time than the maximum allows. If an indexing job can't complete within the maximum time allowed, try running it on a schedule. The scheduler keeps track of indexing status. If a scheduled indexing job is interrupted for any reason, the indexer can pick up where it last left off at the next scheduled run.

> [!NOTE]
> In the Serverless pricing model, indexer behavior differs from Dedicated services. Capacity isn't defined by replicas or partitions. Instead, per-service object limits, per-index storage caps, and service-level throttling govern indexing limits. The maximum running time per Serverless Developer indexer run is two hours.

### Indexer object and throughput limits

| Resource | Free&nbsp;<sup>1</sup> | Basic&nbsp;<sup>2</sup> | S1 | S2 | S3 | S3&nbsp;HD&nbsp;<sup>3</sup> | L1 | L2 | Serverless Developer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maximum indexers | 3 | 5 or 15 | 50 | 200 | 200 | N/A | 10 | 10 | 30 |
| Maximum datasources | 3 | 5 or 15 | 50 | 200 | 200 | N/A | 10 | 10 | 30 per service |
| Maximum skillsets <sup>4</sup> | 3 | 5 or 15 | 50 | 200 | 200 | N/A | 10 | 10 | 30 |
| Maximum indexing load per invocation | 10,000 docs | Limited only by max docs | Limited only by max docs | Limited only by max docs | Limited only by max docs | N/A | No limit | No limit | Limited only by max docs |
| Minimum schedule | 5 min | 5 min | 5 min | 5 min | 5 min | 5 min | 5 min | 5 min | 5 min |
| Maximum running time per indexer run <sup>5</sup> | 1-3 or 3-10 min | 2 or 24 hours | 2 or 24 hours | 2 or 24 hours | 2 or 24 hours | 2 hours | 2 or 24 hours | 2 or 24 hours | 2 hours |
| Cumulative indexer runtime per service <sup>6</sup> | N/A | N/A | N/A | N/A | N/A | 24 hours | N/A | N/A | 24 hours |

<sup>1</sup> Free services have indexer maximum execution time of 3 minutes for blob sources and 1 minute for all other data sources. Indexer invocation is once every 180 seconds. For AI indexing that calls Foundry Tools, free services are limited to 20 free transactions per indexer per day, where a transaction is defined as a document that successfully passes through the enrichment pipeline. (Tip: You can reset an indexer to reset its count.)

<sup>2</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexers, data sources, and skillsets.

<sup>3</sup> S3 HD indexer support is in preview and requires the `2025-11-01-preview` REST API version or later. S3 HD indexers run only in the [multitenant execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment) and don't support [shared private link resources](search-indexer-howto-access-private.md). During the preview, S3 HD indexer support is best suited for small workloads (approximately 1 GB index size) with no or minimal skillsets. For aggregate behavior, monitoring, and planning guidance, see [Indexer execution on Serverless and S3 HD](search-indexer-high-density-serverless-overview.md).

<sup>4</sup> Maximum of 30 skills per skillset.

<sup>5</sup> Regarding the 2 or 24 hour maximum duration for indexers: a 2-hour maximum is the most common and it's what you should plan for. It refers to indexers that run in the [public environment](search-howto-run-reset-indexers.md#indexer-execution-environment), which offloads computationally intensive processing and leaves more resources for queries. The 24-hour limit applies if you configure the indexer to run in a private environment using only the infrastructure that's allocated to your search service. Some older indexers are incapable of running in the public environment, and those indexers always have a 24-hour processing range. If you have unscheduled indexers that run continuously for 24 hours, you can assume those indexers couldn't be migrated to the newer infrastructure. As a general rule, for indexing jobs that can't finish within two hours, put the indexer on a [5-minute schedule](search-howto-schedule-indexers.md) so that the indexer can quickly pick up where it left off. On the Free tier, the 3-10 minute maximum running time is for indexers with skillsets.

<sup>6</sup> On S3 HD and Serverless services, all indexers share 24 hours of cumulative runtime per service in each 24-hour UTC window. For quota behavior, monitoring, and planning guidance, see [Indexer execution on Serverless and S3 HD](search-indexer-high-density-serverless-overview.md).

### Source-file limits for blob-like indexers

File processing happens in stages, and each stage has its own limits:

1. A data source connector downloads a source item, subject to source-specific connector limits.
1. Azure AI Search extracts the item's content, subject to the maximum source-file size and extracted-character limits in the following table.
1. Optionally, a skillset sends that content to downstream services, where an individual skill's input limit can be smaller than what the indexer extracts.

The maximum source-file size and extracted-character limits in the following table apply to the Azure Blob Storage, ADLS Gen2, SharePoint in Microsoft 365, OneLake, and Azure Files indexers. For per-skill limits, check the [reference article for each skill](cognitive-search-predefined-skills.md) in your skillset.

| Resource | Free | Basic | S1 | S2 | S3 | S3&nbsp;HD | L1 | L2 | Serverless Developer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maximum source-file size, MB <sup>2</sup> <sup>4</sup> | 16 | 16 | 128 | 256 | 256 | N/A | 256 | 256 | 256 |
| Maximum characters extracted from a source file <sup>1</sup> <sup>3</sup> <sup>4</sup> | 256,000 | 512,000 | 4&nbsp;mil | 8&nbsp;mil | 16&nbsp;mil | N/A | 4&nbsp;mil | 4&nbsp;mil | 16&nbsp;mil |

<sup>1</sup> The maximum number of characters is based on Unicode code units, specifically UTF-16.

<sup>2</sup> When using `delimitedText` parsing mode for CSV files, a buffer size limit of 10MB per file row applies.

<sup>3</sup> When using `delimitedText` parsing mode for CSV files, the “maximum extracted content size” limit doesn't apply.

<sup>4</sup> Blob-like indexers include the Azure Blob Storage indexer (blob indexer), ADLS Gen2 indexer, SharePoint in Microsoft 365 indexer, OneLake indexer, and Azure Files indexer. The direct-upload file knowledge source doesn't use an indexer and has [separate limits](agentic-knowledge-source-how-to-file.md#file-support-and-limits).

## Shared private link resource limits

Indexers can access other Azure resources [over private endpoints](search-indexer-howto-access-private.md) managed via the [shared private link resource API](/rest/api/searchmanagement/shared-private-link-resources). This section describes the limits associated with this capability.

> [!NOTE]
> The Serverless pricing model Developer tier doesn't support shared private links or network security perimeter (NSP) to data sources. Private Endpoints and IP firewall rules for a private connection to a Serverless Developer tier service are supported.


| Resource | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 | Serverless Developer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Private endpoint indexer support | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No |
| Private endpoint support for indexers with a skillset <sup>1</sup> | No | No | Yes | Yes | Yes | No | Yes | Yes | No |
| Private endpoint support for skillsets with an embedding skill <sup>2</sup> | No | Yes | Yes | Yes | Yes | No | Yes | Yes | No |
| Maximum private endpoints | N/A | 10 or 30 | 100 | 400 | 400 | N/A | 20 | 20 | N/A |
| Maximum distinct resource types <sup>3</sup> | N/A | 4 | 7 | 15 | 15 | N/A | 4 | 4 | N/A |

<sup>1</sup> AI enrichment and image analysis are computationally intensive and consume disproportionate amounts of available processing power. For this reason, private connections are disabled on lower tiers to ensure the performance and stability of the search service itself. On Basic services, private connections to a Microsoft Foundry resource are unsupported to preserve service stability. For the S1 tier, make sure the service was created with [higher limits](search-limits-quotas-capacity.md#partition-storage-gb) after April 3, 2024. Indexers with more than 2 Azure OpenAI Embedding or Azure Vision multimodal embeddings skills are restricted from running in private environment, and private connections aren't available.

<sup>2</sup> Private connections to an embedding model are supported on Basic and S1 high-capacity search services created after April 3, 2024, with the [higher limits](search-limits-quotas-capacity.md#partition-storage-gb) for storage and computational processing.

<sup>3</sup> The number of distinct resource types are computed as the number of unique `groupId` values used across all shared private link resources for a given search service, irrespective of the status of the resource.

## Synonym limits

The maximum number of synonym maps varies by tier. Each rule can have up to 20 expansions, where an expansion is an equivalent term. For example, given "cat", association with "kitty", "feline", and "felis" (the genus for cats) counts as three expansions.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD |L1 | L2 | Serverless Developer |
|---|---|---|----|----|----|-------|----|----| --- |
| Maximum synonym maps |3 |3|5 |10 |20 |20 | 10 | 10 | 20 per service |
| Maximum number of rules per map |5000 |20000|20000 |20000 |20000 |20000 | 20000 | 20000  | 20000 |

## Index alias limits

The maximum number of [index aliases](search-how-to-alias.md) varies by tier and [service creation date](search-how-to-upgrade.md#check-your-service-creation-or-upgrade-date). On all tiers, if the service was created after October 2022, the maximum number of aliases is double the maximum number of indexes allowed. If the service was created before October 2022, the limit is the number of indexes allowed.

> [!NOTE]
> The Serverless model Developer tier doesn't support index aliases.

| Service creation date | Free | Basic | S1 | S2 | S3 | S3 HD |L1 | L2 | Serverless Developer |
|----------|------|-------|----|----|----|-------|----|----| --- |
| Before October 2022 | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 1000 per partition or 3000 per service | 10 | 10 | N/A |
| After October 2022 | 6 | 30 | 100 | 400 | 400 | 2000 per partition or 6000 per service | 20 | 20 | N/A |

<sup>1</sup> Basic services created before December 2017 have lower limits (5 instead of 15) on indexes.

## Agentic retrieval limits

A [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) specifies one or more [knowledge sources](agentic-knowledge-source-overview.md) and a [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) that controls the level of large language model (LLM) processing for [agentic retrieval](agentic-retrieval-overview.md). Limits vary by pricing tier, API version, and reasoning effort level.

| Resource | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 | Serverless Developer |
|--|--|--|--|--|--|--|--|--|--|
| Maximum knowledge sources per service | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 0 | 10 | 10 | 30 |
| Maximum knowledge bases per service | 3 | 5 or 15 <sup>1</sup> | 50 | 200 | 200 | 0 | 10 | 10 | 30 |
| Maximum knowledge sources per knowledge base | 3 | 5 or 10 <sup>1</sup> | 10 | 10 | 10 | 0 | 10 | 10 | 10 |

<sup>1</sup> Basic services created before April 3, 2024 have lower limits (5) on knowledge sources and knowledge bases.

### Knowledge source selection during retrieval

A knowledge base can contain up to the tier-specific maximum shown above, regardless of the API version or retrieval reasoning effort. The API version and reasoning effort instead affect how many knowledge sources can be selected during retrieval.

| API version | Retrieval reasoning effort | Free | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 |
|--|--|--|--|--|--|--|--|--|--|
| `2026-05-01-preview` and later | `minimal`, `low`, `medium` | 3 | 5 or 10 <sup>1</sup> | 10 | 10 | 10 | 0 | 10 | 10 |
| `2026-04-01`, `2025-11-01-preview` | `minimal` <sup>2</sup> | 3 | 5 or 10 <sup>1</sup> | 10 | 10 | 10 | 0 | 10 | 10 |
| `2025-11-01-preview` | `low` | 3 | 3 | 3 | 3 | 3 | 0 | 3 | 3 |
| `2025-11-01-preview` | `medium` | 3 | 5 | 5 | 5 | 5 | 0 | 5 | 5 |

The `2025-08-01-preview` uses the legacy knowledge agent contract and doesn't support `retrievalReasoningEffort`.

<sup>2</sup> The `minimal` reasoning effort uses all knowledge sources in the knowledge base because it bypasses LLM-based query planning.

### Retrieve request runtime

The `maxRuntimeInSeconds` limit is the same across supported tiers.

| Minimum | Default | Maximum |
|--|--|--|
| 10 seconds | 90 seconds | 600 seconds (10 minutes) |

The maximum applies only to the Azure AI Search retrieve request. For configuration examples, see [Override default reasoning effort and set request limits](agentic-retrieval-how-to-retrieve.md#override-default-reasoning-effort-and-set-request-limits).

## Data limits (AI enrichment)

Data limits apply to an [AI enrichment pipeline](cognitive-search-concept-intro.md) that calls Azure Language in Foundry Tools. The maximum input is 50,000 characters, as measured by [`String.Length`](/dotnet/api/system.string.length), for the [Entity Recognition skill](cognitive-search-skill-entity-recognition-v3.md#data-limits), [Entity Linking skill](cognitive-search-skill-entity-linking-v3.md#data-limits), [Key Phrase Extraction skill](cognitive-search-skill-keyphrases.md#data-limits), [Language Detection skill](cognitive-search-skill-language-detection.md#data-limits), and [PII Detection skill](cognitive-search-skill-pii-detection.md#data-limits). The [Sentiment skill](cognitive-search-skill-sentiment-v3.md#data-limits) has a 5,000-character maximum.

Use the [Text Split skill](cognitive-search-skill-textsplit.md) when you need to divide larger text before downstream processing.

These limits apply to both Dedicated and Serverless pricing models.

## Throttling limits

Throttling limits help ensure service stability by controlling the rate of API requests.


In the Dedicated pricing model, throttling is based on search units (replicas × partitions).  

In the Serverless pricing model, throttling isn't based on search units. Instead, service-level operation limits and overall consumption behavior govern throughput. Usage and service limits manage capacity, not the configuration of replicas and partitions.



| Operation | Dedicated (per search unit) | Serverless (per service or per index) |
|-----------|----------------------------|--------------------------------------|
| List indexes (GET /indexes) | 3 requests/sec/SU | 3 requests/sec |
| Get index (GET /indexes/{index}) | 10 requests/sec/SU | 10 requests/sec |
| Create index (POST /indexes) | 12 requests/min/SU | 12 requests/min |
| Create or update index (PUT /indexes/{index}) | 6 requests/sec/SU | 6 requests/sec |
| Delete index (DELETE /indexes/{index}) | 12 requests/min/SU | 12 requests/min |
| Service statistics (GET /servicestats) | 4 requests/sec/SU | 4 requests/sec |
| Search queries (POST /indexes/{index}/docs/search) | Varies by SU count and query complexity | 50 queries/sec (aggregate read throttle per index) |
| Index documents (POST /indexes/{index}/docs/index) | Varies by SU count and indexing workload | 5 requests/sec per index |
| Suggest (POST /indexes/{index}/docs/suggest) | Varies by SU count | Not explicitly defined |
| Autocomplete (POST /indexes/{index}/docs/autocomplete) | Varies by SU count | Not explicitly defined |


#### Semantic ranker throttling limits

[Semantic ranker](search-get-started-semantic.md) uses a queuing system to manage concurrent requests. This system allows search services to get the highest number of queries per second possible. When the limit of concurrent requests is reached, the system places additional requests in a queue. If the queue is full, the system rejects further requests and they must be retried.

Total semantic ranker queries per second vary based on the following factors:

+ The tier of the search service. Both queue capacity and concurrent request limits vary by tier.
+ The number of search units in the search service. The simplest way to increase the maximum number of concurrent semantic ranker queries is to [add more search units to your search service](search-capacity-planning.md).
+ The total available semantic ranker capacity in the region.
+ The amount of time it takes to serve a query using semantic ranker. This time varies based on how busy the search service is.

The following table describes the semantic ranker throttling limits by tier, subject to available capacity in the region. You can contact Microsoft support to request a limit increase.

| Resource | Basic | S1 | S2 | S3 | S3 HD | L1 | L2 | Serverless Developer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Maximum concurrent requests (per search unit) | 2 | 3 | 4 | 4 | 4 | 4 | 4 | 4 (per service) |
| Maximum request queue size (per search unit) | 4 | 6 | 8 | 8 | 8 | 8 | 8 | 8 (per service) |

## API request limits

Limits on queries exist because unbounded queries can destabilize your search service. Typically, such queries are created programmatically. If your application generates search queries programmatically, design it so it doesn't generate queries of unbounded size.

Limits on payloads exist for similar reasons, ensuring the stability of your search service. The limit applies to the entire request, inclusive of all its components. For example, if the request batches several documents or commands, the entire request must fit within the supported limit.

If you must exceed a supported limit, [test your workload](search-performance-analysis.md#develop-baseline-numbers) so that you know what to expect.

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

+ Each page of search results returns up to 1,000 documents.
+ Each Suggest API request returns up to 100 suggestions.

The search engine returns 50 results by default, but you can [override this parameter](search-pagination-page-layout.md#number-of-results-in-the-response) up to the maximum limit.

## API key limits

Use API keys for service authentication. Two types of API keys exist. Admin keys, which you specify in the request header, provide full read-write access to the service. Query keys, which you specify on the URL, are read-only and typically distributed to client applications.

+ Each service supports up to two admin keys.
+ Each service supports up to 50 query keys.
