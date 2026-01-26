---
title: Choose a service tier
titleSuffix: Azure AI Search
description: 'Learn about the service tiers (or SKUs) for Azure AI Search. A search service can be provisioned at these tiers: Free, Basic, Standard, and Storage Optimized. Standard is available in various resource configurations and capacity levels.'
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 11/06/2025
---

# Choose a service tier for Azure AI Search

Part of [creating a search service](search-create-service-portal.md) is choosing a pricing tier (or SKU). In the Azure portal, tier is specified in the **Select Pricing Tier** page when you create the service. In PowerShell or Azure CLI, the tier is specified through the `-Sku` parameter.

The tier determines the:

+ Maximum number of indexes and other objects allowed on the service.
+ Size and speed of partitions (physical storage).
+ Billable rate as a fixed monthly cost, but also an incremental cost if you add capacity.
+ Workload characteristics. Some tiers are optimized for specific workloads.

In a few instances, the tier you choose determines the availability of [premium features](#feature-availability-by-tier).

Billing rates are shown in the Azure portal's **Select Pricing Tier** page. You can check the [pricing page](https://azure.microsoft.com/pricing/details/search/) for regional rates and review [Plan and manage costs](search-sku-manage-costs.md) to learn more about the billing model.

> [!NOTE]
> Search services created after April 3, 2024 have larger partitions and higher vector quotas at almost every tier. For more information, see [Service limits](search-limits-quotas-capacity.md#service-limits).

## Tier descriptions

Tiers include **Free**, **Basic**, **Standard**, and **Storage Optimized**. Standard and Storage Optimized are available with several configurations and capacities. The following screenshot from Azure portal shows the available tiers, minus pricing (which you can find in the Azure portal and on the [pricing page](https://azure.microsoft.com/pricing/details/search/)).

:::image type="content" source="media/search-sku-tier/tiers.png" lightbox="media/search-sku-tier/tiers.png" alt-text="Pricing tier chart" border="true":::

**Free** creates a [limited search service](search-limits-quotas-capacity.md#subscription-limits) for smaller projects, like running tutorials and code samples. Internally, system resources are shared among multiple subscribers. You can't scale a free service, run significant workloads, and some premium features aren't available. You can only have one free search service per Azure subscription. If the service is inactive for an extended period of time, it might be deleted to free up capacity, especially if the region is under capacity constraints.

The most commonly used billable tiers include:

+ **Basic** has the ability to meet SLA with its support for three replicas.

+ **Standard (S1, S2, S3)** is the default. It gives you more flexibility in scaling for workloads. You can scale both partitions and replicas. With dedicated resources under your control, you can deploy larger projects, optimize performance, and increase capacity.

Some tiers are designed for certain types of work:

+ **Standard 3 High Density (S3 HD)** is a *hosting mode* for S3, where the underlying hardware is optimized for a large number of smaller indexes and is intended for multitenancy scenarios. S3 HD has the same per-unit charge as S3, but the hardware is optimized for fast file reads on a large number of smaller indexes.

+ **Storage Optimized (L1, L2)** tiers offer larger storage capacity at a lower price per TB than the Standard tiers. These tiers are designed for large indexes that don't change very often. The primary tradeoff is higher query latency, which you should validate for your specific application requirements.

You can find out more about the various tiers on the [pricing page](https://azure.microsoft.com/pricing/details/search/), in the [Service limits in Azure AI Search](search-limits-quotas-capacity.md) article, and on the Azure portal page when you're provisioning a service.

## Region availability by tier

The [regions list](search-region-support.md) provides the locations where Azure AI Search is offered. Some regions might have capacity constraints for certain tiers, which prevents the creation of new search services on those tiers. The list uses footnotes to indicate constrained regions and tiers.

When you create a search service in the Azure portal, unavailable region–tier combinations are automatically excluded.

## Feature availability by tier

Most features are available on all tiers, including the Free tier. In a few cases, the tier determines the availability of a feature. The following table describes the constraints.

| Feature | Tier considerations |
|---------|---------------------|
| [indexers](search-indexer-overview.md) | Indexers aren't available on S3 HD. Indexers have [more limitations](search-limits-quotas-capacity.md#indexer-limits) on the free tier. |
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

Once you create a service, the billing rate becomes both a *fixed cost* of running the service around the clock, and an *incremental cost* if you choose to add more capacity.

Search services are allocated computing resources in the form of *partitions* (for storage), and *replicas* (instances of the query engine). Initially, a service is created with one of each, and the billing rate is inclusive of both resources. However, if you scale capacity, the costs go up or down in increments of the billable rate.

The following example provides an illustration. Assume a hypothetical billing rate of $100 per month. If you keep the search service at its initial capacity of one partition and one replica, then $100 is what you can expect to pay at the end of the month. However, if you add two more replicas to achieve high availability, the monthly bill increases to $300 ($100 for the first replica-partition pair, followed by $200 for the two replicas).

This billing model is based on the concept of applying the billing rate to the number *search units* (SU) used by a search service. All services are initially provisioned at one SU, but you can increase the SUs by adding either partitions or replicas to handle larger workloads. For more information, see [How to estimate costs of a search service](search-sku-manage-costs.md).

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
