---
title: Reliability in Azure AI Search
titleSuffix: Azure AI Search
description: Find out about reliability in Azure AI Search, including availability zones and multi-region deployments.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: reliability-article
ms.date: 06/20/2025
ms.custom:
  - subject-reliability
  - references_regions
  - ignite-2023
---

# Reliability in Azure AI Search

This article describes reliability support in Azure AI Search, covering intra-regional resiliency via [availability zones](#availability-zone-support) and [multi-region deployments](#multi-region-support).

Resiliency is a shared responsibility between you and Microsoft, so this article also covers ways for you to create a resilient solution that meets your needs.

## Production deployment recommendations

To ensure reliability and high availability, your production search service should be on a paid [pricing tier](search-sku-tier.md):

+ Basic
+ Standard
+ Storage Optimized

Azure AI Search doesn't provide a service-level agreement (SLA) for the Free tier, which is strongly discouraged for production use.

The number of replicas deployed to your search service also affects your SLA coverage. Services with one replica don't receive SLA protection. Use two replicas for high availability of read-only workloads and three or more replicas for high availability of read-write workloads. For more information, see [Service-level agreement](#service-level-agreement).

## Reliability architecture overview

<!-- TO DO -->

## Transient faults

Transient faults are short, intermittent failures in components. They occur frequently in a distributed environment like the cloud, and they're a normal part of operations. They correct themselves after a short period of time. It's important that your applications handle transient faults, usually by retrying affected requests.

All cloud-hosted applications should follow the Azure transient fault handling guidance when communicating with any cloud-hosted APIs, databases, and other components. For more information, see [Recommendations for handing transient faults](/azure/well-architected/design-guides/handle-transient-faults).

A single-replica search service might experience transient faults due to regular maintenance operations. Azure AI Search minimizes these disruptions as much as possible, but they can still affect single-replica services. To ensure resiliency against transient faults, we recommend that you use two or more replicas.

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
+ Have at least [two replicas](search-capacity-planning.d#add-or-remove-partitions-and-replicas).

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

+ **Expected downtime**: A zone failure isn't expected to cause downtime to the overall search service. However, replicas in the failed zone might be unavailable for a period of time.

+ **Traffic rerouting**: When a zone fails, Azure AI Search detects the failure and routes requests to active replicas in the surviving zones.

### Failback

When the availability zone recovers, Azure AI Search automatically restores normal operations and begins routing traffic to available replicas across all zones, including the recovered zone.

### Testing for zone failures

Azure AI Search manages traffic routing, failover, and failback for zone-redundant services. You don't need to initiate anything or validate zone failure processes.

## Multi-region support

Azure AI Search is a single-region service. If the region is unavailable, your search service is also unavailable. However, you can follow the guidance in this section to implement a multi-region architecture that provides redundancy and failover capabilities.

### Why use multiple regions?

If you need two or more search services, creating them in different regions can meet the following operational requirements:

+ [Business continuity and disaster recovery (BCDR)](/azure/reliability/disaster-recovery-overview). Azure AI Search doesn't provide instant failover if there's an outage.

+ Fast performance for a globally distributed application. If query and indexing requests come from all over the world, users who are closest to the host data center experience faster performance. Creating more services in regions with close proximity to these users can equalize performance for everyone.

### Multi-region architecture

In a multi-region setup, two or more search services are located in different regions and have synchronized indexes. Users are automatically routed to the service with the lowest latency.

Azure AI Search doesn't provide automated index replication across regions, but you can [synchronize data](#synchronize-data) using indexers or REST APIs. You can also add Azure Traffic Manager for intelligent request routing.

The following diagram illustrates the multi-region architecture with three search services, each in a different region:

![Diagram showing cross-tab view of services by region.][1]

> [!TIP]
> For a complete implementation, see the [multi-region Bicep sample](https://github.com/Azure-Samples/azure-search-multiple-regions) on GitHub. The sample deploys a fully configured, multi-regional search solution and provides two options for index synchronization and request redirection using Azure Traffic Manager.

### Synchronize data

To keep two or more distinct search services in sync, you can either:

+ Pull content updates into an index using an indexer.
+ Push content into an index using the [Documents - Index REST API](/rest/api/searchservice/documents/) or an equivalent API in the Azure SDKs.

#### Option 1: Use indexers

<!-- TO DO -->

#### Option 2: Use REST APIs

<!-- TO DO -->

### Load balancing and failover

<!-- TO DO -->

### Data residency in a multi-region deployment

When you deploy multiple search services in various geographic regions, your content is stored in the region you chose for each search service.

Azure AI Search doesn't store data outside of your specified region without your authorization. Authorization is implicit when you use features that write to an Azure Storage resource:

+ [Enrichment cache](cognitive-search-incremental-indexing-conceptual.md)
+ [Debug sessions](cognitive-search-debug-session.md)
+ [Knowledge store](knowledge-store-concept-intro.md)

For these features, you provide the storage account in your preferred region.

> [!NOTE]
> When both the search service and storage account are in the same region, network traffic uses private IP addresses over the Microsoft backbone. IP firewalls and private endpoints aren't supported in this configuration. Use the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md) instead.

<!-- Across Azure, [reliability](/azure/reliability/overview) means resiliency and availability if there's a service outage or degradation. In Azure AI Search, reliability can be achieved within a single service or through multiple search services in separate regions.

+ Deploy a single search service and scale up for high availability. You can add multiple replicas to handle higher indexing and query workloads. If your search service [supports availability zones](#availability-zone-support), replicas are automatically provisioned in different physical data centers for extra resiliency.

+ Deploy multiple search services across different geographic regions. All search workloads are fully contained within a single service that runs in a single geographic region, but in a multi-service scenario, you have options for synchronizing content so that it's the same across all services. You can also set up a load balancing solution to redistribute requests or fail over if there's a service outage.

For business continuity and recovery from disasters at a regional level, plan on a cross-regional topology, consisting of multiple search services having identical configuration and content. Your custom script or code provides the *failover* mechanism to an alternate search service if one suddenly becomes unavailable.

<a name="scale-for-availability"></a>

## High availability

In Azure AI Search, replicas are copies of your index. A search service is commissioned with at least one replica, and can have up to 12 replicas. [Adding replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas) allows Azure AI Search to do machine reboots and maintenance against one replica, while query execution continues on other replicas.

For each individual search service, Microsoft guarantees at least 99.9% availability for configurations that meet these criteria:

+ Two replicas for high availability of *read-only* workloads (queries)

+ Three or more replicas for high availability of *read-write* workloads (queries and indexing) 

The system has internal mechanisms for monitoring replica health and partition integrity. If you provision a specific combination of replicas and partitions, the system ensures that level of capacity for your service.

No Service Level Agreement (SLA) is provided for the *Free* tier. For more information, see the [SLA for Azure AI Search](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

## Multiple services in separate geographic regions

Service redundancy is necessary if your operational requirements include:

+ [Business continuity and disaster recovery (BCDR) requirements](/azure/reliability/disaster-recovery-overview). Azure AI Search doesn't provide instant failover if there's an outage.

+ Fast performance for a globally distributed application. If query and indexing requests come from all over the world, users who are closest to the host data center experience faster performance. Creating more services in regions with close proximity to these users can equalize performance for all users.

If you need two or more search services, creating them in different regions can meet application requirements for continuity and recovery, and faster response times for a global user base.

Azure AI Search doesn't provide an automated method of replicating search indexes across geographic regions, but there are some techniques that can make this process simple to implement and manage. These techniques are outlined in the next few sections.

The goal of a geo-distributed set of search services is to have two or more indexes available in two or more regions, where a user is routed to the Azure AI Search service that provides the lowest latency:

   ![Diagram showing cross-tab view of services by region.][1]

You can implement this architecture by creating multiple services and designing a strategy for data synchronization. Optionally, you can include a resource like Azure Traffic Manager for routing requests. 

> [!TIP]
> For help with deploying multiple search services across multiple regions, see this [Bicep sample on GitHub](https://github.com/Azure-Samples/azure-search-multiple-regions) that deploys a fully configured, multi-regional search solution. The sample gives you two options for index synchronization, and request redirection using Traffic Manager.

<a name="data-sync"></a>

### Synchronize data across multiple services

There are two options for keeping two or more distinct search services in sync:

+ Pull content updates into a search index by using an [indexer](search-indexer-overview.md).
+ Push content into an index using the [Add or Update Documents (REST)](/rest/api/searchservice/documents) API or an Azure SDK equivalent API.

To configure either option, we recommend using the [sample Bicep script in the azure-search-multiple-region](https://github.com/Azure-Samples/azure-search-multiple-regions) repository, modified to your regions and indexing strategies.

#### Option 1: Use indexers for updating content on multiple services

If you're already using indexer on one service, you can configure a second indexer on a second service to use the same data source object, pulling data from the same location. Each service in each region has its own indexer and a target index (your search index isn't shared, which means each index has its own copy of the data), but each indexer references the same data source.

Here's a high-level visual of what that architecture would look like.

![Diagram showing a single data source with distributed indexer and service combinations.][2]

#### Option 2: Use REST APIs for pushing content updates on multiple services

If you're using the Azure AI Search REST API to [push content to your search index](tutorial-optimize-indexing-push-api.md), you can keep your various search services in sync by pushing changes to all search services whenever an update is required. In your code, make sure to handle cases where an update to one search service fails but succeeds for other search services.

### Fail over or redirect query requests

If you need redundancy at the request level, Azure provides several [load balancing options](/azure/architecture/guide/technology-choices/load-balancing-overview):

+ [Azure Traffic Manager](/azure/traffic-manager/traffic-manager-overview), used to route requests to multiple geo-located websites that are then backed by multiple search services. 
+ [Application Gateway](/azure/application-gateway/overview), used to load balance between servers in a region at the application layer.
+ [Azure Front Door](/azure/frontdoor/front-door-overview), used to optimize global routing of web traffic and provide global failover.
+ [Azure Load Balancer](/azure/load-balancer/load-balancer-overview), used to load balance between services in a backend pool.

Some points to keep in mind when evaluating load balancing options:

+ Search is a backend service that accepts query and indexing requests from a client. 

+ Requests from the client to a search service must be authenticated. For access to search operations, the caller must have role-based permissions or provide an API key on the request.

+ Service endpoints are reached through a public internet connection by default. If you set up a private endpoint for client connections that originate from within a virtual network, use [Application Gateway](/azure/application-gateway/overview).

+ Azure AI Search accepts requests addressed to the `<your-search-service-name>.search.windows.net` endpoint. If you reach the same endpoint using a different DNS name in the host header, such as a CNAME, the request is rejected.

Azure AI Search provides a [multi-region deployment sample](https://github.com/Azure-Samples/azure-search-multiple-regions) that uses Azure Traffic Manager for request redirection if the primary endpoint fails. This solution is useful when you route to a search-enabled client that only calls a search service in the same region.

Azure Traffic Manager is primarily used for routing network traffic across different endpoints based on specific routing methods (such as priority, performance, or geographic location). It acts at the DNS level to direct incoming requests to the appropriate endpoint. If an endpoint that Traffic Manager is servicing begins refusing requests, traffic is routed to another endpoint.

Traffic Manager doesn't provide an endpoint for a direct connection to Azure AI Search, which means you can't put a search service directly behind Traffic Manager. Instead, the assumption is that requests flow to Traffic Manager, then to a search-enabled web client, and finally to a search service on the backend. The client and service are located in the same region. If one search service goes down, the search client starts failing, and Traffic Manager redirects to the remaining client.

> [!NOTE]
> If you are using Azure Load Balancer [health probes](/azure/load-balancer/load-balancer-custom-probe-overview) on a search service, you must use an HTTPS probe with `/ping` as the path.

![Diagram of search apps connecting through Azure Traffic Manager.][4]

## Data residency in a multi-region deployment

When you deploy multiple search services in various geographic regions, your content is stored in the region you chose for each search service.

Azure AI Search doesn't store data outside of your specified region without your authorization. Authorization is implicit when you use features that write to an Azure Storage resource: [enrichment cache](cognitive-search-incremental-indexing-conceptual.md), [debug session](cognitive-search-debug-session.md), [knowledge store](knowledge-store-concept-intro.md). In all cases, the storage account is one that you provide, in the region of your choice. 

> [!NOTE]
> If both the storage account and the search service are in the same region, network traffic between search and storage uses a private IP address and occurs over the Microsoft backbone network. Because private IP addresses are used, you can't configure IP firewalls or a private endpoint for network security. Instead, use the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md) as an alternative when both services are in the same region. 

## About service outages and catastrophic events

As stated in the [SLA](https://azure.microsoft.com/support/legal/sla/search/v1_0/), Microsoft guarantees a high level of availability for index query requests when an Azure AI Search service instance is configured with two or more replicas, and index update requests when an Azure AI Search service instance is configured with three or more replicas. However, there's no built-in mechanism for disaster recovery. If continuous service is required in the event of a catastrophic failure outside of Microsoft’s control, we recommend provisioning a second service in a different region and implementing a geo-replication strategy to ensure indexes are fully redundant across all services.

Customers who use [indexers](search-indexer-overview.md) to populate and refresh indexes can handle disaster recovery through geo-specific indexers that retrieve data from the same data source. Two services in different regions, each running an indexer, could index the same data source to achieve geo-redundancy. If you're indexing from data sources that are also geo-redundant, remember that Azure AI Search indexers can only perform incremental indexing (merging updates from new, modified, or deleted documents) from primary replicas. In a failover event, be sure to redirect the indexer to the new primary replica. 

If you don't use indexers, you would use your application code to push objects and data to different search services in parallel. For more information, see [Synchronize data across multiple services](#data-sync).

## Back up and restore alternatives

A business continuity strategy for the data layer usually includes a restore-from-backup step. Because Azure AI Search isn't a primary data storage solution, Microsoft doesn't provide a formal mechanism for self-service backup and restore. However, you can use the **index-backup-restore** sample code in this [Azure AI Search .NET sample repo](https://github.com/Azure-Samples/azure-search-dotnet-utilities)  or in this [Python sample repository](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/utilities/index-backup-restore/azure-search-backup-and-restore.ipynb) to back up your index definition and snapshot to a series of JSON files, and then use these files to restore the index, if needed. This tool can also move indexes between service tiers.

Otherwise, your application code used for creating and populating an index is the de facto restore option if you delete an index by mistake. To rebuild an index, you would delete it (assuming it exists), recreate the index in the service, and reload by retrieving data from your primary data store.

## Related content

+ Review [Service limits](search-limits-quotas-capacity.md) to learn more about the pricing tiers and service limits.
+ Review [Plan for capacity](search-capacity-planning.md) to learn more about partition and replica combinations.
+ Review [Case Study: Use Cognitive Search to Support Complex AI Scenarios](https://techcommunity.microsoft.com/t5/azure-ai/case-study-effectively-using-cognitive-search-to-support-complex/ba-p/2804078) for more configuration guidance.

<!--Image references-->
[1]: ./media/search-reliability/geo-redundancy.png
[2]: ./media/search-reliability/scale-indexers.png
[4]: ./media/search-reliability/azure-function-search-traffic-mgr.png
