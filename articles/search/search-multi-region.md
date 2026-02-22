---
title: Multi-Region Solutions in Azure AI Search
titleSuffix: Azure AI Search
description: Learn about multi-region deployments in Azure AI Search, including data synchronization and request failover.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 08/08/2025
ms.update-cycle: 365-days
---

# Multi-region deployments in Azure AI Search

Although Azure AI Search is a single-region service, you can achieve higher reliability by deploying multiple search services with identical configurations and content across multiple regions.

This article describes the components of a multi-region solution, which relies on your custom script or code to handle failover if a service becomes unavailable.

For more information about the reliability features of Azure AI Search, including intra-regional resiliency via availability zones, see [Reliability in Azure AI Search](/azure/reliability/reliability-ai-search).

## Why use multiple regions?

If you need two or more search services, creating them in different regions can meet the following operational requirements:

+ **Resiliency to region outages**. If there's an outage, Azure AI Search doesn't provide instant failover to another region.

+ **Fast performance for a globally distributed application**. If indexing and query requests come from around the world, users who are closest to the host data center experience faster performance. Creating more services in regions with close proximity to these users can equalize performance for everyone.

## Multi-region architecture

In a multi-region setup, two or more search services are located in different regions and have synchronized indexes. Users are automatically routed to the service with the lowest latency.

Azure AI Search doesn't provide an automated method of index replication across regions. However, you can synchronize data using [push or pull model indexing](search-what-is-data-import.md), both of which are described in the following section. You can also add Azure Traffic Manager or another load balancer for [request redirection](#request-failover-and-redirection).

The following diagram illustrates a geo-distributed set of search services:

:::image type="content" source="media/search-multi-region/geo-redundancy.png" alt-text="Diagram that shows a cross-tab view of services by region." border="true" lightbox="media/search-multi-region/geo-redundancy.png":::

> [!TIP]
> For a complete implementation, see the [Bicep sample](https://github.com/Azure-Samples/azure-search-multiple-regions) on GitHub. The sample deploys a fully configured, multi-region search solution that can be modified to your regions and indexing strategies.

## Data synchronization

To synchronize two or more distinct search services, you can either:

+ Push content into an index using [Documents - Index (REST API)](/rest/api/searchservice/documents/) or an equivalent API in the Azure SDKs.
+ Pull content into an index using an [indexer](search-indexer-overview.md).

### [Push APIs](#tab/push-apis)

If you use the REST APIs to [push content into your index](search-what-is-data-import.md#pushing-data-to-an-index), you can synchronize multiple search services by sending updates to each service whenever changes occur. Ensure that your code handles cases in which an update fails for one service but succeeds for other services.

### [Pull APIs (Indexers)](#tab/pull-apis)

If you have an indexer on one search service, you can create a second indexer on a second service to reference the same data source. Each service in each region has its own indexer and target index. Although the indexes are independent and store their own copies of the data, they remain synchronized because the indexers pull from the same source.

The following diagram illustrates this architecture:

:::image type="content" source="media/search-multi-region/scale-indexers.png" alt-text="Diagram of a single data source with distributed indexer and service combinations." border="true" lightbox="media/search-multi-region/scale-indexers.png":::

---

## Data residency

When you create multiple search services in different regions, your content is stored in the region you chose for each service.

Azure AI Search doesn't store data outside of your specified region without your authorization. Authorization is implicit when you use features that write to Azure Storage, for which you provide a storage account in your preferred region. These features include:

+ [Enrichment cache](cognitive-search-incremental-indexing-conceptual.md)
+ [Debug sessions](cognitive-search-debug-session.md)
+ [Knowledge store](knowledge-store-concept-intro.md)

If your search service and storage account are in the same region, network traffic uses private IP addresses over the Microsoft backbone network, so you can't configure IP firewalls or private endpoints for network security. As an alternative, use the [trusted service exception](search-indexer-howto-access-trusted-service-exception.md).

## Request failover and redirection

For redundancy at the request level, Azure provides several [load-balancing options](/azure/architecture/guide/technology-choices/load-balancing-overview):

### [Azure Application Gateway](#tab/application-gateway)

Use [Azure Application Gateway](/azure/application-gateway/overview) to load balance between servers in a region at the application layer.

By default, service endpoints are accessed through a public internet connection. Use Application Gateway if you set up a private endpoint for client connections that originate from within a virtual network.

### [Azure Front Door](#tab/front-door)

Use [Azure Front Door](/azure/frontdoor/front-door-overview) to optimize global routing of web traffic and provide global failover.

### [Azure Load Balancer](#tab/load-balancer)

Use [Azure Load Balancer](/azure/load-balancer/load-balancer-overview) to load balance between search services in a backend pool.

To use [health probes](/azure/load-balancer/load-balancer-custom-probe-overview) on a search service, you must use an HTTPS probe with `/ping` as the path.

### [Azure Traffic Manager](#tab/traffic-manager)

Use [Azure Traffic Manager](/azure/traffic-manager/traffic-manager-overview) to route requests to multiple geo-located websites backed by multiple search services.

Traffic Manager doesn't provide an endpoint for a direct connection to Azure AI Search. Instead, requests are assumed to flow from Traffic Manager to a search-enabled web client to a search service on the backend. In this scenario, the service and client are in the same region. If one service goes down, the client fails, and Traffic Manager redirects to the remaining client.

The following diagram illustrates search apps connecting through Traffic Manager:

:::image type="content" source="media/search-multi-region/azure-function-search-traffic-mgr.png" alt-text="Diagram of search apps connecting through Azure Traffic Manager." border="true" lightbox="media/search-multi-region/azure-function-search-traffic-mgr.png":::

> [!TIP]
> Azure AI Search provides a [multi-region Bicep sample](https://github.com/Azure-Samples/azure-search-multiple-regions) that uses Traffic Manager for request redirection when the primary endpoint fails. This solution is useful for routing to a search-enabled client that only calls a search service in the same region.

---

As you evaluate these load-balancing options, consider the following points:

+ Azure AI Search is a backend service that accepts indexing and query requests from a client.

+ By default, service endpoints are accessed through a public internet connection. We recommend [Azure Application Gateway](/azure/application-gateway/overview) for private endpoints that originate from within a virtual network.

+ Azure AI Search accepts requests addressed to the `<your-search-service-name>.search.windows.net` endpoint. If you reach the same endpoint using a different DNS name in the host header, such as a CNAME, the request is rejected.

+ Requests from the client to a search service must be authenticated. To access search operations, the caller must have [role-based permissions](search-security-rbac.md) or provide an [API key](search-security-api-keys.md) with the request.

## Related content

+ [Reliability in Azure AI Search](/azure/reliability/reliability-ai-search)
+ [Design reliable Azure applications](/azure/well-architected/reliability/checklist)
