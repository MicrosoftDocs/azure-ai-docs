---
title: Choose a Service Tier
description: 'Learn about the service tiers (or SKUs) for Azure AI Search. A search service can be provisioned at these tiers: Free, Basic, Standard, and Storage Optimized. Standard is available in various resource configurations and capacity levels.'
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 03/25/2026
---

# Choose a pricing model and service tier in Azure AI Search

When you [create a search service](search-create-service-portal.md), you must choose a pricing model. Azure AI Search offers two pricing models, each suited to different workload patterns:

| Pricing model | Best for | How you're billed |
| --- | --- | --- |
| Dedicated | Steady, predictable, high-utilization workloads | Fixed capacity via Search Units (SUs); hourly rate based on selection of a [service tier](#choose-a-service-tier) |
| Serverless | Infrequent, bursty, or highly variable workloads | Consumption-based: measured by [Compute Units](./serverless-cost-optimization.md) and indexed storage (GB/month) |

> [!NOTE] 
> Dedicated model Search Units (SUs) and Serverless model Compute Units (CUs) are not the same and cannot be used interchangeably. Don't use SU-based pricing calculators or estimates for Serverless workloads.

Both models provide the same core search features (with a few minor exceptions for the Serverless preview noted below). The primary difference is pricing and scale behavior, not capabilities.

Selecting the Dedicated pricing model requires estimating your workload needs and then [choosing a service tier](#dedicated-pricing-model---choose-a-service-tier) with the appropriate pre-provisioned capacity.

Selecting the Serverless pricing model does not require selecting a pre-provisioned service tier, but uses consumption-based pricing, so [performance optimization](./serverless-cost-optimization.md) will directly affect cost.

## Serverless pricing model (preview)

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

The Serverless pricing model is a consumption-based offering that automatically scales compute and storage based on your workload. It eliminates the need to provision capacity upfront, allowing you to pay only for the resources you use.

With the Serverless model, you don’t configure replicas, partitions, or search units. Instead, the service manages capacity dynamically in response to query volume, indexing activity, and workload complexity.

Billing is based on two primary dimensions:

- **Compute usage**: Measured in compute units per hour (CU/h) and charged based on the work performed (queries, indexing, and other operations).
- **Indexed storage**: Charged per GB per month based on the size of your indexes.

This model is designed for workloads with variable or unpredictable demand, including bursty traffic, multi-tenant applications, and agent-driven scenarios. It supports the same core search features and APIs as Dedicated services, so you can build and run search applications without rewriting code.

In its current (Public Preview) state, the Serverless pricing model does not support certain features available in Dedicated pricing model. Known limitations include:

- Index aliases: Not supported
- Debug sessions: Not supported
- Private networking for indexers: Not supported
- File Knowledge Service (Preview): Not supported
- Shared Private Link resources: No planned support for the Serverless model
- Service-level agreement (SLA): Not available during Public Preview

Additional capabilities (such as certain networking or security features) might be limited or introduced later as the service evolves.

To learn more, see [Optimize costs with the Serverless pricing model](./serverless-cost-optimization.md).

## Dedicated pricing model

The Dedicated pricing model is a provisioned-capacity offering that provides predictable performance and cost by allocating fixed infrastructure to your workload. You configure capacity upfront, allowing the service to handle consistent indexing and query demands with guaranteed resources.

With the Dedicated model, you explicitly configure replicas, partitions, and search units (SUs). Replicas provide query throughput and high availability, while partitions define storage and indexing capacity. Together, they determine the total capacity and performance characteristics of your search service.

Billing is based on:

- **[Service tier](#choose-a-service-tier)**: The pre-selected provisioned capacity.
- **Search units (SUs)**: The billing unit for Dedicated services, calculated as replicas × partitions. You’re billed at a fixed hourly rate based on the number of search units and selected service tier.

This model is designed for workloads with steady, predictable demand, where consistent performance, low latency, and controlled scaling are important. It’s commonly used for production applications with sustained query volumes or large indexing workloads.

In the Dedicated pricing model, the selected service tier determines:

- Maximum number of indexes and other objects allowed on the service.
- Size and speed of partitions (physical storage).
- Billable rate as a fixed monthly cost, but also an incremental cost if you add capacity.
- Workload characteristics. Some tiers are optimized for specific workloads.

In some cases, the tier also determines the availability of [premium features](#feature-availability-by-tier).

### Choose a service tier

**Free** creates a [limited search service](search-limits-quotas-capacity.md#subscription-limits) for small projects, such as tutorials and development. Resources are shared across tenants, and scaling is not supported. Some premium features are unavailable, and the service may be deleted after periods of inactivity. You can only have one free search service per Azure subscription.

The most commonly used billable tiers include:

- **Basic** supports production workloads and can meet SLA requirements with up to three replicas.

- **Standard (S1, S2, S3)** is the default tier. It supports scaling partitions and replicas, enabling larger workloads and improved performance.

Some tiers are designed for certain types of work:

- **Standard 3 High Density (S3 HD)** is a *hosting mode* for S3 optimized for multitenancy. S3 HD has the same per-unit charge as S3, but supports a large number of smaller indexes and uses hardware optimized for fast file reads and high-density storage scenarios.

- **Storage Optimized (L1, L2)** tiers provide lower-cost storage per TB and are designed for large, less frequently updated indexes. These tiers typically have higher query latency.

Billing rates are shown in the [Azure portal](https://portal.azure.com/auth/login/) when you're creating a new AI Search service in the **Select Pricing Tier** page. 

:::image type="content" source="media/search-sku-tier/tiers.png" lightbox="media/search-sku-tier/tiers.png" alt-text="Pricing tier chart" border="true":::

You can check the [pricing page](https://azure.microsoft.com/pricing/details/search/) for regional rates.

Review [Plan and manage costs](search-sku-manage-costs.md) to learn more about the Dedicated pricing model and how it compares to the Serverless model.

Check [Service limits in Azure AI Search](search-limits-quotas-capacity.md) 
or limits on storage, workloads, and object counts by tier.

## How to select a tier

In the Azure portal, the service tiers are specified in the **Select Pricing Tier** page when you create the service. 

In PowerShell or Azure CLI, the tier is specified through the `-Sku` parameter.

## Region availability by tier

The [regions list](search-region-support.md) provides the locations where Azure AI Search is offered. Some regions might have capacity constraints for certain tiers, which prevents the creation of new search services on those tiers. The list uses footnotes to indicate constrained regions and tiers.

When you create a search service in the Azure portal, unavailable region–tier combinations are automatically excluded.

## Feature availability by tier

Most features are available across all tiers. In some cases, feature availability depends on the selected tier:

| Feature | Tier considerations |
| ------- | ------------------- |
| [indexers](search-indexer-overview.md) | Indexers have [more limitations](search-limits-quotas-capacity.md#indexer-limits) on the free tier. |
| [indexer `executionEnvironment` configuration parameter](search-how-to-create-indexers.md?tabs=indexer-rest#create-an-indexer) | The ability to pin all indexer processing to just the search clusters allocated to your search service requires S2 and higher. |
| [AI enrichment](cognitive-search-concept-intro.md) | Runs on the Free tier but not recommended for large workloads. |
| [Managed or trusted identities for outbound (indexer) access](search-how-to-managed-identities.md) | Not available on the Free tier.|
| [Customer-managed encryption keys](search-security-manage-encryption-keys.md) | Not available on the Free tier. |
| [IP firewall access](service-configure-firewall.md) | Not available on the Free tier. |
| [Private endpoint (integration with Azure Private Link)](service-create-private-endpoint.md) | For inbound connections to a search service, not available on the Free tier. <br>For outbound connections by indexers to other Azure resources, not available on Free or S3 HD. <br>For indexers that use skillsets, not available on Free, Basic, S1, or S3 HD.|
| [Availability zones](/azure/reliability/reliability-ai-search#availability-zone-support) | Not available on the Free tier. |
| [Semantic ranker](semantic-search-overview.md) | Runs on the Free tier but not recommended for large workloads. |

Resource-intensive features might not work well unless you give it sufficient capacity. For example, [AI enrichment](cognitive-search-concept-intro.md) has long-running skills that time out on a Free service unless the dataset is small.

## Upper limits

Tiers determine the  maximum storage of the service itself, plus the maximum number of indexes, indexers, data sources, skillsets, and synonym maps that you can create. For a full break out of all limits, see [Service limits in Azure AI Search](search-limits-quotas-capacity.md).

## Partition size and speed

Tier pricing includes details about per-partition storage that ranges from 15 GB for Basic, up to 2 TB for Storage Optimized (L2) tiers. Other hardware characteristics, such as speed of operations, latency, and transfer rates, aren't published, but tiers that are designed for specific solution architectures are built on hardware that has the features to support those scenarios. For more information about partitions, see [Estimate and manage capacity](search-capacity-planning.md) and [Reliability in Azure AI Search](/azure/reliability/reliability-ai-search).

> [!NOTE]
> Higher-capacity partitions became available in select regions in April 2024. A second wave of higher-capacity partitions was released in May 2024. If you have an older search service, you might be able to [upgrade your service](search-how-to-upgrade.md) to benefit from more capacity at the same billing rate.

## Billing rates

Tiers have different billing rates, with higher rates for tiers that run on more expensive hardware or provide more expensive features. The tier billing rate can be found in the [Azure pricing pages](https://azure.microsoft.com/pricing/details/search/) for Azure AI Search.

After you create a service, the billing rate becomes both a *fixed cost* of running the service around the clock, and an *incremental cost* if you choose to add more capacity.


In the Dedicated model, billing is based on Search Units (SUs), which combine partitions (storage) and replicas (query capacity).

- A service starts with one partition and one replica (one SU)
- Adding partitions or replicas increases cost linearly with the number of SUs

For example, adding replicas to improve availability or throughput increases the monthly cost proportionally.

For more information, see [Plan and manage costs](search-sku-manage-costs.md).

### Billing rate example

The following example provides an illustration. Assume a hypothetical billing rate of $100 per month. If you keep the search service at its initial capacity of one partition and one replica, then $100 is what you can expect to pay at the end of the month. However, if you add two more replicas to achieve high availability, the monthly bill increases to $300 ($100 for the first replica-partition pair, followed by $200 for the two replicas).

## Tier changes

> [!NOTE]
> Existing search services can switch between Basic and Standard (S1, S2, and S3) tiers. Your current service configuration can't exceed the limits of the target tier, and your region can't have capacity constraints on the target tier. For more information, see [Change your pricing tier](search-capacity-planning.md#change-your-pricing-tier).

To switch to a different tier than those previously listed:

1. [Create a search service](search-create-service-portal.md) on the new tier.
1. Deploy your search content onto the new service. [Follow this checklist](search-howto-move-across-regions.md#prepare-and-move) to ensure you have all the content.
1. Delete the old service when you're sure it's no longer needed.

For large indexes that you don't want to rebuild from scratch, use one of the following backup and restore samples:

+ [Backup and restore sample (C#)](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore/README.md)
+ [Backup and restore sample (Python)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/utilities/index-backup-restore/azure-search-backup-and-restore.ipynb)
+ [Backup and restore sample for very large indexes (Python)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/utilities/resumable-index-backup-restore/backup-and-restore.ipynb)

## Next steps

The best way to choose a pricing tier is to start with a least-cost tier, and then allow experience and testing to inform your decision to keep the service or switch to a higher tier.

For next steps, we recommend that you create a search service at a tier that can accommodate the level of testing you propose to do, and then review the following guidance on estimating cost and capacity:

+ [Create a search service](search-create-service-portal.md)
+ [Estimate costs](search-sku-manage-costs.md)
+ [Estimate capacity](search-capacity-planning.md)
