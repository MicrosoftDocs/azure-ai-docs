---
title: 'Create a search service in the Azure portal'
titleSuffix: Azure AI Search
description: Learn how to set up an Azure AI Search resource in the Azure portal. Choose resource groups, regions, and a pricing tier.

manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - references_regions
  - build-2024
ms.topic: conceptual
ms.date: 02/18/2025
---

# Create an Azure AI Search service in the Azure portal

[Azure AI Search](search-what-is-azure-search.md) is an information-retrieval platform for the enterprise. It supports traditional search and conversational, AI-driven search for "chat with your data" experiences across your proprietary content.

The easiest way to create a search service is through the [Azure portal](https://portal.azure.com/), which is covered in this article.

[![Animated GIF showing how to create an Azure AI Search service in the Azure portal.](./media/search-create-service-portal/AnimatedGif-AzureSearch-small.gif)](./media/search-create-service-portal/AnimatedGif-AzureSearch.gif#lightbox)

You can also use [Azure PowerShell](search-manage-powershell.md#create-or-delete-a-service), the [Azure CLI](search-manage-azure-cli.md#create-or-delete-a-service), the [Management REST API](search-manage-rest.md#create-or-update-a-service), an [Azure Resource Manager template](search-get-started-arm.md), a [Bicep file](search-get-started-bicep.md), or [Terraform](search-get-started-terraform.md).

## Before you start

Some properties are fixed for the lifetime of the search service. Before creating your service, decide on a name, region, and tier.

+ [Service name](#name-your-service) becomes part of the URL endpoint. The name must be unique and follow naming rules.

+ [Region](search-region-support.md) determines data residency and availability of certain features. Semantic ranker and Azure AI integration have region requirements. Make sure your region of choice supports the features you need.

+ [Service tier](search-sku-tier.md) determines infrastructure, service limits, and billing. Some features aren't available on lower or specialized tiers.

## Subscribe to Azure

Azure AI Search requires a free or paid Azure subscription. To try Azure AI Search for free, [start a trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F) and then [create your search service on the Free tier](#choose-a-tier). Each Azure subscription can have one free search service, which is intended for short-term, non-production evaluation of the product. For more information, see [Try Azure AI Search for free](search-try-for-free.md).

With the Free tier, you can complete all of the quickstarts and most of the tutorials.

> [!IMPORTANT]
> To make room for other services, Microsoft might delete free services that are inactive for an extended period of time.

## Find the Azure AI Search offering

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. In the upper-left corner, select **Create a resource**.

   :::image type="content" source="media/search-create-service-portal/find-search3.png" lightbox="media/search-create-service-portal/find-search3.png" alt-text="Screenshot of the Create a Resource page in the Azure portal." border="true":::

1. In the search box, enter **Azure AI Search**.

## Choose a subscription

If you have multiple Azure subscriptions, choose one for your search service.

If you're implementing [customer-managed encryption](search-security-manage-encryption-keys.md) or using other features that rely on managed service identities for [external data access](search-indexer-securing-resources.md), choose the same subscription you use for Azure Key Vault or other services that use managed identities.

## Set a resource group

A resource group is a container that holds related resources for an Azure solution. Use it to consolidate same-solution resources, monitor costs, and check the creation date of your search service.

:::image type="content" source="media/search-create-service-portal/new-resource-group.png" lightbox="media/search-create-service-portal/new-resource-group.png" alt-text="Screenshot of the Create a Resource Group page in the Azure portal." border="true":::

Over time, you can track current and projected costs for individual resources and for the overall resource group. The following screenshot shows the cost information that's available when you combine multiple resources into one group:

:::image type="content" source="media/search-create-service-portal/resource-group-cost-management.png" lightbox="media/search-create-service-portal/resource-group-cost-management.png" alt-text="Screenshot of the Cost Management page in the Azure portal." border="true":::

## Name your service

Enter a name for your search service. The name is part of the endpoint against which API calls are made: `https://your-service-name.search.windows.net`. For example, if you enter `myservice`, the endpoint becomes `https://myservice.search.windows.net`.

When naming your service, follow these rules:

+ Choose a name that's unique within the `search.windows.net` namespace.
+ Use between 2 and 60 characters.
+ Use only lowercase letters, digits, or dashes (-).
+ Don't use dashes as the first two characters or the last character.
+ Don't use consecutive dashes.

> [!TIP]
> If you have multiple search services, it's helpful to include the region (or location) in the service name. For example, when deciding how to combine or attach resources, the name `myservice-westus` can save you a trip to the Properties page.

## Choose a region

> [!IMPORTANT]
> Due to high demand, Azure AI Search is currently unavailable for new instances in some regions.

If you use multiple Azure services, putting all of them in the same region minimizes or voids bandwidth charges. There are no charges for data egress among same-region services.

In most cases, choose a region near you, unless any of the following apply:

+ Your nearest region is [at capacity](search-sku-tier.md#region-availability-by-tier). The Azure portal has the advantage of hiding unavailable regions and tiers during resource setup.

+ You want to use integrated data chunking and vectorization or built-in skills for AI enrichment. Integrated operations have region requirements.

+ You want to use Azure Storage for indexer-based indexing, or you want to store application data that isn't in an index. Debug session state, enrichment caches, and knowledge stores are Azure AI Search features that depend on Azure Storage. The region you choose for Azure Storage has implications for network security. If you're setting up a firewall, you should place the resources in *separate* regions. For more information, see [Outbound connections from Azure AI Search to Azure Storage](search-indexer-securing-resources.md).

### Checklist for choosing a region

1. Is Azure AI Search available in a nearby region? Check the [list of supported regions](search-region-support.md).

1. Do you have a specific tier in mind? Check [region availability by tier](search-sku-tier.md#region-availability-by-tier).

1. Do you have business continuity and disaster recovery (BCDR) requirements? Create two or more search services in [regional pairs](/azure/reliability/cross-region-replication-azure#azure-paired-regions) within [availability zones](search-reliability.md#availability-zones). For example, if you're operating in North America, you might choose East US and West US, or North Central US and South Central US, for each search service.

1. Do you need [AI enrichment](cognitive-search-concept-intro.md), [integrated data chunking and vectorization](vector-search-integrated-vectorization.md), or [multimodal image search](search-get-started-portal-image-search.md)? Azure AI Search, Azure OpenAI, and Azure AI multiservice must coexist in the same region.

   + Start with [Azure OpenAI regions](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability) because they have the most variability. Azure OpenAI provides embedding models and chat models for RAG and integrated vectorization.

   + Check [Azure AI Search regions](search-region-support.md#azure-public-regions) for a match to your Azure OpenAI region. If you're using OCR, entity recognition, or other skills backed by Azure AI, the **AI service integration** column indicates whether Azure AI multiservice is in the same region as Azure AI Search.

   + Check [multimodal embedding regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) for multimodal APIs and image search. This API is accessed through an Azure AI multiservice account, but in general, it's available in fewer regions than Azure AI multiservice.

### Regions with the most overlap

Currently, the following regions offer cross-regional availability for Azure AI Search, Azure OpenAI, and Azure AI Vision multimodal:

+ **Americas**: West US, East US
+ **Europe**: Switzerland North, Sweden Central

This list isn't definitive, and depending on your tier, you might have more choices. Region status can also change quickly, so confirm your region choice before creating your service.

## Choose a tier

Azure AI Search is offered in [multiple pricing tiers](https://azure.microsoft.com/pricing/details/search/):

+ Free
+ Basic
+ Standard
+ Storage Optimized

Each tier has its own [capacity and limits](search-limits-quotas-capacity.md), and some features are tier dependent. For detailed information about computing characteristics, feature availability, and region availability, see [Choose a service tier for Azure AI Search](search-sku-tier.md).

The Basic and Standard tiers are the most common for production workloads, but many customers start with the Free tier. The billable tiers differ primarily in partition size, partition speed, and limits on the number of objects you can create.

Search services created after April 3, 2024 have larger partitions and higher vector quotas at every billable tier.

:::image type="content" source="media/search-create-service-portal/select-pricing-tier.png" lightbox="media/search-create-service-portal/select-pricing-tier.png" alt-text="Screenshot of the Select Pricing Tier page." border="true":::

> [!NOTE]
> Remember, you can't change the pricing tier after you create your service. If you need a lower or higher tier, you must recreate the service.

## Create your service

After you provide the necessary inputs, create your search service.

:::image type="content" source="media/search-create-service-portal/new-service3.png" lightbox="media/search-create-service-portal/new-service3.png" alt-text="Screenshot of the Review and create the service page." border="true":::

Your service is deployed in minutes, and you can monitor its progress with Azure notifications. Consider pinning the service to your dashboard for easy access in the future.

:::image type="content" source="media/search-create-service-portal/monitor-notifications.png" lightbox="media/search-create-service-portal/monitor-notifications.png" alt-text="Screenshot of the Notifications tab in the Azure portal." border="true":::

## Configure authentication

If you're using the Azure portal, skip this step. The portal is linked to your Azure AI Search resource with admin rights. For a portal walkthrough, see [Quickstart: Create an Azure AI Search index in the Azure portal](search-get-started-portal.md).

If you're not using the Azure portal, programmatic access to your search service requires the URL endpoint and an authenticated connection.

1. Go to your service page.

1. From the navigation pane, select **Overview**. Note the URL endpoint, which you'll need to set up a programmatic connection.

   :::image type="content" source="media/search-create-service-portal/get-endpoint.png" lightbox="media/search-create-service-portal/get-endpoint.png" alt-text="Screenshot of the Overview tab with the URL endpoint." border="true":::

1. From the navigation pane, select **Settings** > **Keys**. You can connect to your service using [key-based authentication](search-security-api-keys.md), [role-based access](search-security-rbac.md), or both. Most quickstarts and tutorials use API keys for simplicity, but if you're setting up a service for production workloads, consider using roles.

   :::image type="content" source="media/search-create-service-portal/set-authentication-options.png" lightbox="media/search-create-service-portal/set-authentication-options.png" alt-text="Screenshot of the Keys tab with authentication options." border="true":::

## Scale your service

After you deploy your search service, you can [scale it to meet your needs](search-limits-quotas-capacity.md). Scaling is available only on billable tiers. You can scale your service in two dimensions:

+ *Partitions*, which allow your service to store and search through more documents.

+ *Replicas*, which allow your service to handle a higher load of search queries.

On the Free tier, you cannot scale your service or configure partitions and replicas.

Adding resources will increase your monthly bill. Use the [pricing calculator](https://azure.microsoft.com/pricing/calculator/) to understand the billing implications. You can adjust resources based on load, such as increasing resources for initial indexing and decreasing them later for incremental indexing.

> [!IMPORTANT]
> Your service must have [two replicas for read-only SLA and three replicas for read-write SLA](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

To scale your service in the Azure portal:

1. Go to your service page.

1. From the navigation pane, select **Settings** > **Scale**.

1. Use the slider to add resources of either type.

:::image type="content" source="media/search-create-service-portal/settings-scale.png" lightbox="media/search-create-service-portal/settings-scale.png" alt-text="Screenshot of the Scale tab." border="true":::

## When to add a second service

Most customers use just one service provisioned at a tier [sufficient for expected load](search-capacity-planning.md). One service can host multiple indexes, subject to the [maximum limits of the tier you select](search-limits-quotas-capacity.md#index-limits), with each index isolated from another. In Azure AI Search, requests can only be directed to one index, minimizing the chance of accidental or intentional data retrieval from other indexes in the same service.

Although most customers use just one service, service redundancy might be necessary if operational requirements include the following:

+ [Business continuity and disaster recovery (BCDR)](/azure/reliability/cross-region-replication-azure). Azure AI Search doesn't provide instant failover if there's an outage.

+ [Multitenant architectures](search-modeling-multitenant-saas-applications.md) sometimes call for two or more services.

+ Globally deployed applications might require search services in each geography to minimize latency.

> [!NOTE]
> In Azure AI Search, you can't segregate indexing and querying operations; thus, you would never create multiple services for segregated workloads. An index is always queried on the service in which it was created (you can't create an index in one service and copy it to another).

A second service isn't required for high availability. High availability for queries is achieved when you use two or more replicas in the same service. Replica updates are sequential, which means at least one is operational when a service update is rolled out. For more information about uptime, see [Service Level Agreements](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

## Add more services to a subscription

Azure AI Search restricts the [number of search services](search-limits-quotas-capacity.md#subscription-limits) you can initially create in a subscription. If you exhaust your maximum limit, you can request more quota.

You must have Owner or Contributor permissions on the subscription to request quota.
Depending on region and datacenter capacity, you can automatically request more quota to add services to your subscription. If the request fails, you should either decrease the number or file a support ticket. For a large increase in quota, such as more than 30 extra services, you should expect a one-month turnaround.

1. Sign in to the Azure portal, search for "quotas" in your dashboard, and then select the **Quotas** service.

   :::image type="content" source="media/search-create-service-portal/quota-search.png" lightbox="media/search-create-service-portal/quota-search.png" alt-text="Screenshot of the quota search term and Quotas service in the results.":::

1. In the Quota's Overview page, select **Search**.

   :::image type="content" source="media/search-create-service-portal/quota-overview-page.png" lightbox="media/search-create-service-portal/quota-overview-page.png" alt-text="Screenshot of the search tile in the Quota's overview page.":::

1. Set filters so that you can review existing quota for search services in the current subscription. We recommend filtering by usage.

1. Find the region and tier that needs more quota and select the **Edit** pencil icon to begin your request.

   :::image type="content" source="media/search-create-service-portal/quota-pencil-edit.png" lightbox="media/search-create-service-portal/quota-pencil-edit.png" alt-text="Screenshot of the My Quotas page with a region at maximum quota.":::

1. In **Quota details**, specify the location, tier, and a new limit for your subscription quota. None of the values can be empty. The new limit must be greater than the current limit. If regional capacity is constrained, your request won't be automatically approved. In this scenario, an incident report is generated on your behalf for investigation and resolution.

1. Submit the request.

1. Monitor notifications in the Azure portal for status updates on the new limit. Most requests are approved within 24 hours.

## Next steps

After provisioning a service, you can continue in the Azure portal to create your first index.

> [!div class="nextstepaction"]
> [Quickstart: Create an Azure AI Search index in the Azure portal](search-get-started-portal.md)

Want to optimize and save on your cloud spending?

> [!div class="nextstepaction"]
> [Start analyzing costs with Cost Management](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
