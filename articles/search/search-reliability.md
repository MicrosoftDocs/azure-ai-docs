---
title: Reliability in Azure AI Search
titleSuffix: Azure AI Search
description: Find out about reliability in Azure AI Search, including availability zones and multi-region deployments.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: reliability-article
ms.date: 06/21/2025
ms.custom:
  - subject-reliability
  - references_regions
  - ignite-2023
---

# Reliability in Azure AI Search

This article describes reliability support in Azure AI Search, covering intra-regional resiliency via [availability zones](#availability-zone-support) and [multi-region deployments](#multi-region-support).

Resiliency is a shared responsibility between you and Microsoft, so this article also covers ways for you to create a resilient solution that meets your needs.

<!-- Across Azure, [reliability](/azure/reliability/overview) means resiliency and availability if there's a service outage or degradation. In Azure AI Search, reliability can be achieved within a single service or through multiple search services in separate regions.

+ Deploy a single search service and scale up for high availability. You can add multiple replicas to handle higher indexing and query workloads. If your search service [supports availability zones](#availability-zone-support), replicas are automatically provisioned in different physical data centers for extra resiliency.

+ Deploy multiple search services across different geographic regions. All search workloads are fully contained within a single service that runs in a single geographic region, but in a multi-service scenario, you have options for synchronizing content so that it's the same across all services. You can also set up a load balancing solution to redistribute requests or fail over if there's a service outage.

For business continuity and recovery from disasters at a regional level, plan on a cross-regional topology, consisting of multiple search services having identical configuration and content. Your custom script or code provides the *failover* mechanism to an alternate search service if one suddenly becomes unavailable. -->

## Production deployment recommendations

To ensure reliability and high availability for production workloads, your search service should be on a paid [pricing tier](search-sku-tier.md):

+ Basic
+ Standard
+ Storage Optimized

Azure AI Search doesn't provide a service-level agreement for the Free tier, which is strongly discouraged for production use. For more information, see [Service-level agreement](#service-level-agreement).

## Transient faults

Transient faults are short, intermittent failures in components. They occur frequently in a distributed environment like the cloud, and they're a normal part of operations. They correct themselves after a short period of time. It's important that your applications handle transient faults, usually by retrying affected requests.

All cloud-hosted applications should follow the Azure transient fault handling guidance when communicating with any cloud-hosted APIs, databases, and other components. For more information, see [Recommendations for handing transient faults](/azure/well-architected/design-guides/handle-transient-faults).

Search services with one replica might experience transient faults due to regular maintenance operations. Azure AI Search minimizes these disruptions as much as possible, but they can still affect single-replica services. To ensure resiliency against transient faults, we recommend that you use two or more replicas.

## Availability zone support

Availability zones are physically separate groups of datacenters within each Azure region. When one zone fails, services can fail over to one of the remaining zones. For more information, see [What are availability zones?](/azure/reliability/availability-zones-overview)

Azure AI Search is a zone-redundant service that spreads your replicas across availability zones. A search service runs in one region, while its replicas run in zones within that region.

When you add two or more replicas to your service, Azure AI Search automatically places each replica in a different availability zone. If your service has more than three replicas, they're distributed across zones as evenly as possible.

### Region support

Support for availability zones depends on infrastructure and storage. For a list of supported regions, see [Choose a region](search-region-support.md).

### Requirements

To enable zone redundancy, your search service must:

+ Be in a [region that has availability zones](search-region-support.md).
+ Be on the [Basic tier or higher](search-sku-tier.md).
+ Have at least [two replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas).

### Considerations

If an availability zone goes down, your application keeps running and serving traffic. However, overall throughput might decrease because replicas in the affected zone are unavailable. The remaining zones must handle all requests, so if your replicas are spread across three zones, your capacity drops by about one-third. To offset this, consider provisioning more replicas than you typically need.

Zone redundancy also doesn't change the terms of the [SLA for Azure AI Search](https://azure.microsoft.com/support/legal/sla/search/v1_0/). For high availability of read-write workloads, your search service must still have at least three replicas.

### Cost

Each search service starts with one replica. Zone redundancy requires two or more replicas, which increases the cost of running the service. To understand the billing implications of replicas, use the [pricing calculator](https://azure.microsoft.com/pricing/calculator/).

### Configure availability zone support

If your search service meets the [requirements for zone redundancy](#requirements), no extra configuration is necessary. Azure AI Search automatically places replicas in different availability zones when they're added to your service.

### Zone-down experience

When an availability zone experiences an outage, your search service continues to operate using replicas in the surviving zones. The following points summarize the expected behavior:

+ **Detection and response**: Azure AI Search is responsible for detecting a failure in an availability zone. You don't need to do anything to initiate a zone failover.

+ **Notification**: Azure AI Search doesn't notify you when a zone is down.

+ **Active requests**: Any active requests are dropped and should be retried by the client.

+ **Expected data loss**: A zone failure isn't expected to cause data loss.

+ **Expected downtime**: A zone failure isn't expected to cause downtime to the overall search service. However, replicas in the failed zone might be unavailable for some time.

+ **Traffic rerouting**: When a zone fails, Azure AI Search detects the failure and routes requests to active replicas in the surviving zones.

### Failback

When the availability zone recovers, Azure AI Search automatically restores normal operations and begins routing traffic to available replicas across all zones, including the recovered zone.

### Testing for zone failures

Azure AI Search manages traffic routing, failover, and failback for zone-redundant services. You don't need to initiate anything or validate zone failure processes.

## Multi-region support

Azure AI Search is a single-region service. If the region is unavailable, your search service is also unavailable. However, you can follow the guidance in this section to implement a multi-region architecture that provides redundancy and failover capabilities.

### Why use multiple regions?

If you need two or more search services, creating them in different regions can meet the following operational requirements:

+ [Business continuity and disaster recovery (BCDR)](/azure/reliability/disaster-recovery-overview). If there's an outage, Azure AI Search doesn't provide instant failover.

+ Fast performance for a globally distributed application. If indexing and query requests come from around the world, users who are closest to the host data center experience faster performance. Creating more services in regions with close proximity to these users can equalize performance for everyone.

### Multi-region architecture

In a multi-region setup, two or more search services are located in different regions and have synchronized indexes. Users are automatically routed to the service with the lowest latency.

Azure AI Search doesn't provide an automated method of index replication across regions. However, you can [synchronize data](#data-synchronization-in-a-multi-region-deployment) using indexers or REST APIs, both of which are described in the following section. You can also add Azure Traffic Manager for [request redirection](#request-failover-and-redirection).

The following diagram illustrates a geo-distributed set of search services:

:::image type="content" source="media/search-reliability/geo-redundancy.png" alt-text="Diagram that shows a cross-tab view of services by region." border="true" lightbox="media/search-reliability/geo-redundancy.png":::

> [!TIP]
> For a complete implementation, see the [Bicep sample](https://github.com/Azure-Samples/azure-search-multiple-regions) on GitHub. The sample deploys a fully configured, multi-region search solution that can be modified to your regions and indexing strategies.

### Data synchronization in a multi-region deployment

To synchronize two or more distinct search services, you can either:

+ Pull content into an index using an [indexer](search-indexer-overview.md).
+ Push content into an index using the [Documents - Index REST API](/rest/api/searchservice/documents/) or an equivalent API in the Azure SDKs.

#### [Indexers](#tab/indexers)

If you have an [indexer](search-indexer-overview.md) on one search service, you can create a second indexer on a second service to reference the same data source. Each service in each region has its own indexer and target index. Although the indexes are independent and store their own copies of the data, they remain synchronized because the indexers pull from the same source.

The following diagram illustrates this architecture:

:::image type="content" source="media/search-reliability/scale-indexers.png" alt-text="Diagram of a single data source with distributed indexer and service combinations." border="true" lightbox="media/search-reliability/scale-indexers.png":::

#### [REST APIs](#tab/rest-apis)

If you use the REST APIs to [push content to your search index](search-what-is-data-import.md#pushing-data-to-an-index), you can synchronize multiple search services by sending updates to each service whenever changes occur. Ensure that your code handles cases in which an update fails for one service but succeeds for other services.

---

### Data residency in a multi-region deployment

When you create multiple search services in different regions, your content is stored in the region you chose for each service.

Azure AI Search doesn't store data outside of your specified region without your authorization. Authorization is implicit when you use features that write to Azure Storage, for which you provide a storage account in your preferred region. These features include:

+ [Enrichment cache](cognitive-search-incremental-indexing-conceptual.md)
+ [Debug sessions](cognitive-search-debug-session.md)
+ [Knowledge store](knowledge-store-concept-intro.md)

If your search service and storage account are in the same region, network traffic uses private IP addresses over the Microsoft backbone network, so you can't configure IP firewalls or private endpoints for network security. As an alternative, use the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md).

### Request failover and redirection

For redundancy at the request level, Azure provides several [load-balancing options](/azure/architecture/guide/technology-choices/load-balancing-overview):

#### [Azure Application Gateway](#tab/application-gateway)

Use [Azure Application Gateway](/azure/application-gateway/overview) to load balance between servers in a region at the application layer.

By default, service endpoints are accessed through a public internet connection. Use Application Gateway if you set up a private endpoint for client connections that originate from within a virtual network.

#### [Azure Front Door](#tab/front-door)

Use [Azure Front Door](/azure/frontdoor/front-door-overview) to optimize global routing of web traffic and provide global failover.

#### [Azure Load Balancer](#tab/load-balancer)

Use [Azure Load Balancer](/azure/load-balancer/load-balancer-overview) to load balance between search services in a backend pool.

To use Azure Load Balancer [health probes](/azure/load-balancer/load-balancer-custom-probe-overview) on a search service, you must use an HTTPS probe with `/ping` as the path.

#### [Azure Traffic Manager](#tab/traffic-manager)

Use [Azure Traffic Manager](/azure/traffic-manager/traffic-manager-overview) to route requests to multiple geo-located websites backed by multiple search services.

Traffic Manager doesn't provide an endpoint for a direct connection to Azure AI Search. Instead, requests are assumed to flow from Traffic Manager to a search-enabled web client to a search service on the backend. In this scenario, the service and client are in the same region. If one service goes down, the client starts failing, and Traffic Manager redirects to the remaining client.

The following diagram illustrates search apps connecting through Traffic Manager:

:::image type="content" source="media/search-reliability/azure-function-search-traffic-mgr.png" alt-text="Diagram of search apps connecting through Azure Traffic Manager." border="true" lightbox="media/search-reliability/azure-function-search-traffic-mgr.png":::

> [!TIP]
> Azure AI Search provides a [multi-region deployment sample](https://github.com/Azure-Samples/azure-search-multiple-regions) that uses Traffic Manager for request redirection when the primary endpoint fails. This solution is useful for routing to a search-enabled client that only calls a search service in the same region.

---

As you evaluate these load-balancing options, consider the following points:

+ Azure AI Search is a backend service that accepts indexing and query requests from a client.

+ By default, service endpoints are accessed through a public internet connection. We recommend [Application Gateway](#azure-application-gateway) for private endpoints that originate from within a virtual network.

+ Azure AI Search accepts requests addressed to the `<your-search-service-name>.search.windows.net` endpoint. If you reach the same endpoint using a different DNS name in the host header, such as a CNAME, the request is rejected.

+ Requests from the client to a search service must be authenticated. To access search operations, the caller must have [role-based permissions](search-security-rbac.md) or provide an [API key](search-security-api-keys.md) with the request.

## Backups

A business continuity strategy for the data layer usually involves restoring from a backup. Azure AI Search isn't a primary data storage solution, so Microsoft doesn't formally offer self-service backup and restore. However, you can use the `index-backup-restore` sample code for [.NET](https://github.com/Azure-Samples/azure-search-dotnet-utilities/tree/main/index-backup-restore) or [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) to back up your index definition and its documents to a series of JSON files, which are then used to restore the index. You can also use the sample to move indexes between pricing tiers.

Otherwise, if you accidentally delete an index, the application code used to create and populate the index is the de facto restore option. To rebuild an index, you must:

1. Delete the index, assuming it exists.
1. Recreate the index in your search service.
1. Reload the index by retrieving data from your primary data store.

## Service-level agreement

The service-level agreement (SLA) for Azure AI Search describes the expected availability of the service and the conditions that must be met to achieve that availability expectation. For more information, see the [SLA for Azure AI Search](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

The number of [replicas](search-capacity-planning.md#concepts-search-units-replicas-partitions) deployed to your search service determines your SLA coverage. In Azure AI Search, a replica is a copy of your search index. Each service can have between 1 and 12 replicas. Having more replicas enables Azure AI Search to perform maintenance and handle failures without interrupting queries.

Single-replica services don't receive SLA protection. However, Microsoft guarantees at least 99.9% availability of:

+ Read-only workloads (queries) for search services with two replicas.
+ Read-write workloads (queries and indexing) for search services with three or more replicas.

## Related content

+ [Reliability in Azure](/azure/reliability/overview)
+ [Service limits in Azure AI Search](search-limits-quotas-capacity.md)
+ [Plan or add capacity in Azure AI Search](search-capacity-planning.md)
