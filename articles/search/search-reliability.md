---
title: Reliability in Azure AI Search
titleSuffix: Azure AI Search
description: Find out about reliability in Azure AI Search, including availability zones and multi-region deployments.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: reliability-article
ms.date: 06/26/2025
ms.custom:
  - subject-reliability
  - ignite-2023
---

# Reliability in Azure AI Search

This article describes reliability support in Azure AI Search, covering intra-regional resiliency via [availability zones](#availability-zone-support) and [multi-region deployments](#multi-region-support).

Reliability is a shared responsibility between you and Microsoft, so this article also covers ways for you to create a resilient solution that meets your needs.

In Azure AI Search, you can achieve reliability by:

+ **Scaling a single search service**. Add multiple [replicas](search-capacity-planning.md#concepts-search-units-replicas-partitions) to increase availability and handle higher indexing and query workloads. If your region supports availability zones, replicas are automatically provisioned in different physical data centers for extra resiliency.

+ **Deploying multiple search services across different regions**. Each service operates independently within its region. However, in a multi-service scenario, you have options for synchronizing content across all services. You can also use a load-balancing solution to redistribute requests or fail over if there's a service outage.

## Production deployment recommendations

For production workloads, we recommend using a [billable tier](search-sku-tier.md) with at least [two replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas). This configuration makes your search service more resilient to transient faults and maintenance operations. It also meets the [service-level agreement](#service-level-agreement) for Azure AI Search, which requires two replicas for read-only workloads and three or more replicas for read-write workloads.

Azure AI Search doesn't provide a service-level agreement for the Free tier, which is strongly discouraged for production use.

## Transient faults

Transient faults are short, intermittent failures in components. They occur frequently in a distributed environment like the cloud, and they're a normal part of operations. They correct themselves after a short period of time. It's important that your applications handle transient faults, usually by retrying affected requests.

All cloud-hosted applications should follow the Azure transient fault handling guidance when communicating with any cloud-hosted APIs, databases, and other components. For more information, see [Recommendations for handing transient faults](/azure/well-architected/design-guides/handle-transient-faults).

Search services with one replica might experience transient faults due to regular maintenance operations. Azure AI Search minimizes these disruptions as much as possible, but they can still affect single-replica services. To ensure resiliency against transient faults, we recommend that you use two or more replicas.

## Availability zone support

Availability zones are physically separate groups of datacenters within each Azure region. When one zone fails, services can fail over to one of the remaining zones. For more information, see [What are availability zones?](/azure/reliability/availability-zones-overview)

Azure AI Search is a zone-redundant service that spreads your replicas across availability zones. A search service runs in one region, while its replicas run in zones within that region.

When you add two or more replicas to your service, Azure AI Search automatically places each replica in a different availability zone. If your service has more than three replicas, they're distributed across zones as evenly as possible.

### Region support

Support for availability zones depends on infrastructure and storage. For a list of supported regions, see [Choose a region for Azure AI Search](search-region-support.md).

### Requirements

Zone redundancy is automatically enabled when your search service:

+ Is in a [region that has availability zones](search-region-support.md).
+ Is on the [Basic tier or higher](search-sku-tier.md).
+ Has [multiple replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas): two for read-only workloads and three or more for read-write workloads.

### Considerations

Zone redundancy doesn't change the terms of the [service-level agreement](#service-level-agreement) for Azure AI Search. For high availability of read-write workloads, you still need at least three replicas.

### Cost

Each search service starts with one replica. Zone redundancy requires two or more replicas, which increases the cost of running the service. To understand the billing implications of replicas, use the [pricing calculator](https://azure.microsoft.com/pricing/calculator/).

### Configure availability zone support

If your search service meets the [requirements for zone redundancy](#requirements), no extra configuration is necessary. Azure AI Search automatically places your replicas in different availability zones.

### Zone-down experience

When an availability zone experiences an outage, your search service continues to operate using replicas in the surviving zones. The following points summarize the expected behavior:

+ **Detection and response**: Azure AI Search is responsible for detecting a failure in an availability zone. You don't need to do anything to initiate a zone failover.

+ **Notification**: Azure AI Search doesn't notify you when a zone is down.

+ **Active requests**: Any active requests are dropped and should be retried by the client.

+ **Expected data loss**: A zone failure isn't expected to cause data loss.

+ **Expected downtime**: A zone failure isn't expected to cause downtime to your search service, but it can temporarily reduce your service's overall capacity. To maintain optimal performance, consider provisioning more replicas than you typically need.

+ **Traffic rerouting**: When a zone fails, Azure AI Search detects the failure and routes requests to active replicas in the surviving zones.

### Failback

When the availability zone recovers, Azure AI Search automatically restores normal operations and begins routing traffic to available replicas across all zones, including the recovered zone.

### Testing for zone failures

Azure AI Search manages traffic routing, failover, and failback for zone-redundant services. You don't need to initiate anything or validate zone failure processes.

## Multi-region support

Azure AI Search is a single-region service. If the region becomes unavailable, your search service also becomes unavailable.

### Alternative multi-region approaches

To use Azure AI Search in multiple regions, you must deploy separate services in each region. If you create an identical deployment in a secondary Azure region using a multi-region geography architecture, your application becomes less susceptible to a single-region disaster.

When you follow this approach, you must synchronize indexes across regions to recover the last application state. You must also configure load balancing and failover policies. For more information, see [Multi-region deployments in Azure AI Search](search-multi-region.md).

## Backups

A business continuity strategy for the data layer usually involves restoring from a backup. Azure AI Search isn't a primary data storage solution, so Microsoft doesn't formally offer self-service backup and restore. However, you can use the `index-backup-restore` sample for [.NET](https://github.com/Azure-Samples/azure-search-dotnet-utilities/tree/main/index-backup-restore) or [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) to back up your index definition and its documents to a series of JSON files, which are then used to restore the index.

Otherwise, if you accidentally delete an index, the application code used to create and populate the index is the de facto restore option. To [rebuild an index](search-howto-reindex.md), you must:

1. Delete the index, assuming it exists.
1. Recreate the index in your search service.
1. Reload the index by retrieving data from your primary data store.

## Service-level agreement

The service-level agreement (SLA) for Azure AI Search describes the expected availability of the service and the conditions that must be met to achieve that availability expectation. For more information, see the [SLA for Azure AI Search](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

SLA coverage applies to search services on billable tiers with at least two replicas. In Azure AI Search, a replica is a copy of your index. Each service can have between 1 and 12 replicas. [Adding replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas) allows Azure AI Search to perform maintenance on one replica while queries continue executing on other replicas.

Microsoft guarantees at least 99.9% availability of:

+ Read-only workloads (queries) for search services with two replicas.
+ Read-write workloads (queries and indexing) for search services with three or more replicas.

## Related content

+ [Reliability in Azure](/azure/reliability/overview)
+ [Service limits in Azure AI Search](search-limits-quotas-capacity.md)
+ [Choose a region for Azure AI Search](search-region-support.md)
+ [Choose a pricing tier for Azure AI Search](search-sku-tier.md)
+ [Plan or add capacity in Azure AI Search](search-capacity-planning.md)
