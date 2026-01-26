---
title: 'Create a Search Service in the Azure portal'
titleSuffix: Azure AI Search
description: Learn how to set up an Azure AI Search service in the Azure portal. Choose a resource group, region, and pricing tier.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 09/25/2025
ms.custom:
  - references_regions
  - build-2024
  - sfi-image-nochange
---

# Create an Azure AI Search service in the Azure portal

[Azure AI Search](search-what-is-azure-search.md) is an information retrieval platform for the enterprise. It supports traditional search and conversational, AI-driven search for "chat with your data" experiences across your proprietary content.

The easiest way to create a search service is through the [Azure portal](https://portal.azure.com/), which is covered in this article.

[![Animated GIF showing how to create an Azure AI Search service in the Azure portal.](./media/search-create-service-portal/AnimatedGif-AzureSearch-small.gif)](./media/search-create-service-portal/AnimatedGif-AzureSearch.gif#lightbox)

You can also use:

+ [Azure PowerShell](search-manage-powershell.md#create-or-delete-a-service)
+ [Azure CLI](search-manage-azure-cli.md#create-or-delete-a-service)
+ [Management REST API](search-manage-rest.md#create-or-update-a-service)
+ [Azure Resource Manager template](search-get-started-arm.md)
+ [Bicep](search-get-started-bicep.md)
+ [Terraform](search-get-started-terraform.md)

## Before you start

Some properties are fixed for the lifetime of the search service. Before you create your service, decide on the following properties:

| Property | Description |
|--|--|
| [Name](#name-your-service) | Becomes part of the URL endpoint. The name must be unique and follow naming rules. |
| [Region](search-region-support.md) | Determines data residency and availability of certain features. For example, semantic ranker and Azure AI integration have region requirements. Choose a region that supports the features you need. |
| [Tier](search-sku-tier.md) | Determines infrastructure, service limits, and billing. Some features aren't available on lower or specialized tiers. After you create your service, you can [switch between Basic and Standard (S1, S2, and S3) tiers](search-capacity-planning.md#change-your-pricing-tier). |
| [Compute type](search-security-overview.md#data-in-use) | Determines virtualization and security model. You can choose between standard VMs (recommended) and confidential VMs, which are intended for select workloads requiring data-in-use privacy and isolation. |
## Subscribe to Azure

Azure AI Search requires a free or Standard Azure subscription.

To try Azure AI Search for free, [start a trial subscription](https://azure.microsoft.com/pricing/free-trial/?WT.mc_id=A261C142F) and then [create your search service on the Free tier](#choose-a-tier). Each Azure subscription can have one free search service, which is intended for short-term, non-production evaluation of the product. You can complete all of our quickstarts and most of our tutorials on the Free tier. For more information, see [Try Azure AI Search for free](search-try-for-free.md).

> [!IMPORTANT]
> To make room for other services, Microsoft might delete free services that are inactive for an extended period of time.

## Find the Azure AI Search offering

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. In the upper-left corner of your dashboard, select **Create a resource**.

   :::image type="content" source="media/search-create-service-portal/create-resource.png" lightbox="media/search-create-service-portal/create-resource.png" alt-text="Screenshot of the Create a Resource button in the Azure portal." border="true":::

1. Use the search box to find **Azure AI Search**.

   :::image type="content" source="media/search-create-service-portal/azure-ai-search-tile.png" lightbox="media/search-create-service-portal/azure-ai-search-tile.png" alt-text="Screenshot of the Azure AI Search tile in the Azure portal." border="true":::

## Choose a subscription

If you have multiple Azure subscriptions, choose one for your search service.

If you're implementing [customer-managed encryption](search-security-manage-encryption-keys.md) or using other features that rely on managed service identities for [external data access](search-indexer-securing-resources.md), choose the same subscription you use for Azure Key Vault or other services that use managed identities.

## Set a resource group

A resource group is a container that holds related resources for an Azure solution. Use it to consolidate same-solution resources, monitor costs, and check the creation date of your search service.

:::image type="content" source="media/search-create-service-portal/create-resource-group.png" lightbox="media/search-create-service-portal/create-resource-group.png" alt-text="Screenshot of the Create a Resource Group dialog on the Create a Search Service page." border="true":::

Over time, you can track current and projected costs for individual resources and for the overall resource group. The following screenshot shows the cost information that's available when you combine multiple resources into one group:

:::image type="content" source="media/search-create-service-portal/resource-group-cost-management.png" lightbox="media/search-create-service-portal/resource-group-cost-management.png" alt-text="Screenshot of the Cost Management page in the Azure portal." border="true":::

## Name your service

Enter a name for your search service. The name is part of the endpoint against which API calls are issued: `https://your-service-name.search.windows.net`. For example, if you enter `myservice`, the endpoint becomes `https://myservice.search.windows.net`.

When naming your service, follow these rules:

+ Use a name that's unique within the `search.windows.net` namespace.
+ Use between 2 and 60 characters.
+ Use only lowercase letters, digits, and dashes (-).
+ Don't use dashes as the first two characters or the last character.
+ Don't use consecutive dashes.

> [!TIP]
> If you have multiple search services, it's helpful to include the region in the service name. For example, when deciding how to combine or attach resources, the name `myservice-westus` might save you a trip to the Properties page.

## Choose a region

> [!IMPORTANT]
> Due to high demand, Azure AI Search is currently unavailable for new instances in some regions.

If you use multiple Azure services, putting all of them in the same region minimizes or voids bandwidth charges. There are no charges for data egress among same-region services.

In most cases, choose a region near you, unless any of the following apply:

+ Your nearest region is [at capacity](search-region-support.md), which is indicated by the footnotes of each table. The Azure portal has the advantage of hiding unavailable regions and tiers during resource setup.

+ You want to use integrated data chunking and vectorization or built-in skills for AI enrichment. Integrated operations have region requirements.

+ You want to use Azure Storage for indexer-based indexing, or you want to store application data that isn't in an index. Debug session state, enrichment caches, and knowledge stores are Azure AI Search features that depend on Azure Storage. The region you choose for Azure Storage has implications for network security. If you're setting up a firewall, you should place the resources in separate regions. For more information, see [Outbound connections from Azure AI Search to Azure Storage](search-indexer-securing-resources.md).

### Checklist for choosing a region

1. Is Azure AI Search available in a nearby region? Check the [list of supported regions](search-region-support.md).

1. Do you have a specific tier in mind? Check [region availability by tier](search-sku-tier.md#region-availability-by-tier).

1. Do you have business continuity and disaster recovery (BCDR) requirements? Create two or more search services in different Azure regions, each with two or more replicas so that they can be spread across multiple [availability zones](/azure/reliability/reliability-ai-search#availability-zone-support). For example, if you're operating in North America, you might choose East US and West US, or North Central US and South Central US, for each search service. For more information, see [Multi-region deployments in Azure AI Search](search-multi-region.md).

1. Do you need [AI enrichment](cognitive-search-concept-intro.md), [integrated data chunking and vectorization](vector-search-integrated-vectorization.md), or [multimodal search](multimodal-search-overview.md) powered by Foundry Tools? For billing purposes, you must [attach your Microsoft Foundry resource](cognitive-search-attach-cognitive-services.md) to your search service via a keyless connection (preview) or key-based connection. Key-based connections require both services to be in the same region.

   + Check [Azure AI Search regions](search-region-support.md#azure-public-regions). If you're using OCR, entity recognition, or other skills backed by Azure AI, the **AI enrichment** column indicates whether Azure AI Search and Microsoft Foundry are in the same region.

   + Check [Azure Vision in Foundry Tools regions](/azure/ai-services/computer-vision/overview-image-analysis#region-availability) for multimodal APIs that enable text and image vectorization. These APIs are powered by Azure Vision and accessed through a Microsoft Foundry resource. However, they're generally available in fewer regions than the Microsoft Foundry resource itself.

## Choose a tier

Azure AI Search is offered in multiple [pricing tiers](https://azure.microsoft.com/pricing/details/search/):

+ Free
+ Basic
+ Standard
+ Storage Optimized

Each tier has its own [capacity and limits](search-limits-quotas-capacity.md), and some features are tier dependent. For information about computing characteristics, feature availability, and region availability, see [Choose a service tier for Azure AI Search](search-sku-tier.md).

The Basic and Standard tiers are the most common for production workloads, but many customers start with the Free tier. The billable tiers differ primarily in partition size, partition speed, and limits on the number of objects you can create.

:::image type="content" source="media/search-create-service-portal/select-pricing-tier.png" lightbox="media/search-create-service-portal/select-pricing-tier.png" alt-text="Screenshot of the Select Pricing Tier page in the Azure portal." border="true":::

> [!NOTE]
> Services created after April 3, 2024 have larger partitions and higher vector quotas at every billable tier.

## Choose a compute type

The compute type determines the virtualization and security model used to deploy your search service. There are two compute types:

+ **Default** (base cost) deploys your search service on standard Azure infrastructure, encrypting data at rest and in transit but not in use. Recommended for most search workloads.

+ **Confidential** (10% surcharge) uses [Azure confidential computing](/azure/confidential-computing/use-cases-scenarios) to isolate processing in a hardware-based trusted execution environment, protecting unencrypted data in use from unauthorized access. Recommended only if you have advanced privacy, compliance, or regulatory requirements.

Confidential computing has limited regional availability, disables or restricts certain features, and increases the cost of running your search service. For a detailed comparison of both compute types, see [Data in use](search-security-overview.md#data-in-use).

## Create your service

After providing the necessary inputs, create your search service.

:::image type="content" source="media/search-create-service-portal/create-search-service.png" lightbox="media/search-create-service-portal/create-search-service.png" alt-text="Screenshot of the Review and Create button on the Create a Search Service page." border="true":::

Your service is deployed within minutes, and you can monitor its progress with Azure notifications. Consider pinning the service to your dashboard for easy access in the future.

:::image type="content" source="media/search-create-service-portal/portal-notifications.png" lightbox="media/search-create-service-portal/portal-notifications.png" alt-text="Screenshot of the Notifications tab in the Azure portal." border="true":::

## Configure authentication

When you create a search service, key-based authentication is the default, but it's not the most secure option. We recommend that you replace it with role-based access.

To enable role-based access for your service:

1. Go to your search service in the [Azure portal](https://portal.azure.com/).

1. From the left pane, select **Settings** > **Keys**. You can connect to your service using [API keys](search-security-api-keys.md), [Azure roles](search-security-rbac.md), or both. Select **Both** until you assign roles, after which you can select **Role-based access control**.

   :::image type="content" source="media/search-create-service-portal/authentication-options.png" lightbox="media/search-create-service-portal/authentication-options.png" alt-text="Screenshot of the Keys tab with authentication options." border="true":::

## Scale your service

After deploying your search service, you can [scale it to meet your needs](search-limits-quotas-capacity.md). Azure AI Search offers two scaling dimensions: *replicas* and *partitions*. Replicas allow your service to handle a higher load of search queries, while partitions allow your service to store and search through more documents.

Scaling is available only on billable tiers. On the Free tier, you can't scale your service or configure replicas and partitions.

> [!IMPORTANT]
> Your service must have [two replicas for read-only SLA and three replicas for read/write SLA](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

Adding resources will increase your monthly bill. Use the [pricing calculator](https://azure.microsoft.com/pricing/calculator/) to understand the billing implications. You can adjust resources based on load, such as increasing resources for initial indexing and decreasing them later for incremental indexing.

To scale your service:

1. Go to your search service in the [Azure portal](https://portal.azure.com/).

1. From the left pane, select **Settings** > **Scale**.

   :::image type="content" source="media/search-create-service-portal/scale-settings.png" lightbox="media/search-create-service-portal/scale-settings.png" alt-text="Screenshot of the Scale tab with sliders for adding replicas and partitions." border="true":::

1. Use the sliders to add replicas and partitions.

## When to add a second service

Most customers use a single search service at a tier [sufficient for the expected load](search-capacity-planning.md). One service can host multiple indexes, each isolated from the others, within the [maximum limits of your chosen tier](search-limits-quotas-capacity.md#index-limits). In Azure AI Search, you can direct requests to only one index, reducing the chance of retrieving data from other indexes in the same service.

However, you might need a second service for the following operational requirements:

+ Region outages. In the unlikely event of a full region outage, Azure AI Search doesn't provide instant failover. You must implement your own multi-region solution and failover approach. For more information, see [Multi-region deployments in Azure AI Search](search-multi-region.md).
+ [Multitenant architectures](search-modeling-multitenant-saas-applications.md) that require two or more services.
+ Globally deployed applications that require services in each geography to minimize latency.

> [!NOTE]
> In Azure AI Search, you can't separate indexing and querying operations, so don't create multiple services for separate workloads. An index is always queried on the service in which it was created, and you can't copy an index to another service.

A second service isn't required for high availability. You achieve high availability for queries by using two or more replicas in the same service. Because the replicas are updated sequentially, at least one is operational when a service update is rolled out. For more information about uptime, see [Service Level Agreements](https://azure.microsoft.com/support/legal/sla/search/v1_0/).

## Add more services to your subscription

Azure AI Search limits the [number of search services](search-limits-quotas-capacity.md#subscription-limits) you can initially create in a subscription. If you reach your limit, you can request more quotas.

You must have Owner or Contributor permissions for the subscription to request quota. Depending on your region and data center capacity, you might be able to automatically request quota to add services to your subscription. If the request fails, reduce the number or file a support ticket. Expect a one-month turnaround for a large quota increase, such as more than 30 extra services.

To request more subscription quota:

1. Go to your dashboard in the [Azure portal](https://portal.azure.com/).

1. Use the search box to find the **Quotas** service.

   :::image type="content" source="media/search-create-service-portal/quota-search.png" lightbox="media/search-create-service-portal/quota-search.png" alt-text="Screenshot of the Quota search term and the Quotas service in the results.":::

1. On the **Overview** tab, select the **Search** tile.

   :::image type="content" source="media/search-create-service-portal/quota-overview-page.png" lightbox="media/search-create-service-portal/quota-overview-page.png" alt-text="Screenshot of the Search tile on the Overview page.":::

1. Set filters to review the existing quota for search services in your current subscription. We recommend filtering by usage.

    :::image type="content" source="media/search-create-service-portal/usage-filter.png" lightbox="media/search-create-service-portal/usage-filter.png" alt-text="Screenshot of the Usage filter for search services in your current subscription.":::

1. Next to the tier and region that need more quotas, select **Request adjustment** <img src=media/search-create-service-portal/request-adjustment-icon.png alt="Screenshot of the Request Adjustment icon, which is the outline of a pencil." width="14">.

1. In **New Quota Request**, enter a new limit for your subscription quota. The new limit must be greater than your current limit. If regional capacity is constrained, your request won't be automatically approved, and an incident report will be generated on your behalf for investigation and resolution.

1. Submit your request.

1. Monitor notifications in the Azure portal for updates on the new limit. Most requests are approved within 24 hours.

## Next steps

Now that you've deployed your search service, continue in the Azure portal to create your first index:

> [!div class="nextstepaction"]
> [Quickstart: Create an Azure AI Search index in the Azure portal](search-get-started-portal.md)

Want to optimize and save on your cloud spending?

> [!div class="nextstepaction"]
> [Start analyzing costs with Cost Management](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
