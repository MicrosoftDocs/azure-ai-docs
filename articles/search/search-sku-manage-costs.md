---
title: Plan and Manage Costs
titleSuffix: Azure AI Search
description: Learn about billable events, the billing model, and tips for cost control when running an Azure AI Search service.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 06/10/2025
---

# Plan and manage costs of an Azure AI Search service

This article explains how Azure AI Search is billed, including base and potential charges, and provides guidance for cost management.

Before you create a search service, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs based on your planned [capacity](search-capacity-planning.md) and features. Another resource is a capacity-planning worksheet that models your expected index size, indexing throughput, and indexing costs.

As your search workload evolves, follow our tips to minimize costs during both deployment and operation. You can also use built-in metrics to monitor query requests and [Cost Management](/azure/cost-management-billing/costs/overview-cost-management) to create budgets, alerts, and data exports.

> [!NOTE]
> Higher-capacity partitions are available at the same billing rate on services created after April and May 2024. For more information about partition-size upgrades, see [Service limits](search-limits-quotas-capacity.md#service-limits).

<a name="billable-events"></a>

## Understand the billing model

Azure AI Search runs on Azure infrastructure that accrues costs when you deploy new resources. Other infrastructure costs might also accrue.

Costs for Azure AI Search are only a portion of the monthly costs in your Azure bill. Although this article focuses on planning and managing Azure AI Search costs, you're billed for all Azure services and resources used in your Azure subscription, including non-Microsoft services.

### How you're charged for Azure AI Search

When you create or use search resources, you're charged for:

+ The [pricing tier](search-sku-tier.md) of your search service. This is a prorated hourly rate.

+ The number of [search units](search-capacity-planning.md) (SUs) allocated to your search service. SUs are units of capacity that equal the product of replicas and partitions (R × P = SU) used by your service.

### How you're charged for premium features

Premium features are charged in addition to the base cost of your search service. The following table lists premium features and their billing units. All of these features are optional, so if you don't use them, you don't incur any charges.

| Feature | Billing unit |
|-------|------|
| Image extraction (AI enrichment) <sup>1</sup> | Per 1,000 images. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Custom Entity Lookup skill](cognitive-search-skill-custom-entity-lookup.md) (AI enrichment) | Per 1,000 text records. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing) |
| [Built-in skills](cognitive-search-predefined-skills.md)  (AI enrichment) | Number of transactions. Billed at the same rate as calling Azure AI services directly. You can process 20 documents per indexer per day for free. Larger or more frequent workloads require an Azure AI services multi-service resource key. |
| [Semantic ranker](semantic-search-overview.md) | Number of queries of `queryType=semantic`. Billed at a progressive rate. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Shared private link](search-indexer-howto-access-private.md) | [Billed for bandwidth](https://azure.microsoft.com/pricing/details/private-link/) as long as the shared private link exists and is used. |

<sup>1</sup> Refers to images extracted from a file within the indexer pipeline. Text extraction is free. Image extraction is billed when you [enable the `indexAction` parameter](cognitive-search-concept-image-scenarios.md#configure-indexers-for-image-processing) or when you call the [Document Extraction skill](cognitive-search-skill-document-extraction.md).

### How you're otherwise charged

Depending on your configuration and usage, the following charges might apply:

+ Data traffic might incur networking costs. See the [bandwidth pricing](https://azure.microsoft.com/pricing/details/bandwidth/).

+ Several premium features, such as [knowledge stores](knowledge-store-concept-intro.md), [debug sessions](cognitive-search-debug-session.md), and [enrichment caches](cognitive-search-incremental-indexing-conceptual.md), depend on Azure Storage and incur storage costs. Meters for these features are included in the Azure Storage bill.

+ [Customer-managed keys](search-security-manage-encryption-keys.md), which provide double encryption of sensitive content, require a billable [Azure Key Vault](https://azure.microsoft.com/pricing/details/key-vault/).

+ A skillset can include [billable built-in skills](cognitive-search-predefined-skills.md), nonbillable built-in utility skills, and custom skills. Nonbillable utility skills include [Conditional](cognitive-search-skill-conditional.md), [Shaper](cognitive-search-skill-shaper.md), [Text Merge](cognitive-search-skill-textmerger.md), and [Text Split](cognitive-search-skill-textsplit.md). They don't have an API key requirement or 20-document limit.

+ A custom skill is functionality you provide. Custom skills are billable only if they call other billable services. They don't have an API key requirement or 20-document limit.

> [!NOTE]
> You aren't billed for the number of full-text or vector queries, query responses, or documents ingested. However, [service limits](search-limits-quotas-capacity.md) apply to each pricing tier.

## Estimate and plan costs

Use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate your baseline costs for Azure AI Search. You can also  find estimated costs and tier comparisons on the [Select Pricing Tier](search-create-service-portal.md#choose-a-tier) page during service creation.

For initial testing, we recommend that you create a capacity-planning worksheet. The worksheet helps you understand the index-to-source ratio and the effect of enrichment or vector features on both capacity and cost.

To create a capacity-planning worksheet:

1. Index a small sample (1–5%) of your data. Include any [OCR](cognitive-search-skill-ocr.md), enrichment, or embedding skills you plan to use.

1. Measure the index size, indexing throughput, and indexing costs.

1. Extrapolate the results to estimate the full-scale requirements for your data.

## Minimize costs

To minimize the costs of your Azure AI Search solution, use the following strategies:

### Deployment and configuration

+ Create a search service in a [region with more storage per partition](search-limits-quotas-capacity.md#service-limits).

+ Create all related Azure resources in the same region (or as few regions as possible) to minimize or eliminate bandwidth charges.

+ Choose the lightest [pricing tier](search-sku-tier.md) that meets your needs. Basic and S1 offer full access to the modern API at the lowest hourly rate per SU.

+ Use [Azure Web Apps](/azure/app-service/overview) for your front-end application to keep requests and responses within the data center boundary.

### Scaling

+ [Add partitions](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when the index size or ingestion throughput requires it.

+ [Add replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when your queries per second increase, when complex queries are throttling your service, or when high availability is required.

+ Scale up for resource-intensive operations, such as indexing, and then readjust downwards for regular query workloads.

+ Write code to automate scaling for predictable workload patterns.

+ Remember that capacity and pricing aren't linear. Doubling capacity more than doubles costs on the same tier. For better performance at a similar price, consider [switching to a higher tier](search-performance-tips.md#tip-switch-to-a-standard-s2-tier).

### Indexing and enrichment

+ Use [incremental indexing](search-howto-reindex.md) to process only new or changed data.

+ Use [enrichment caching](cognitive-search-incremental-indexing-conceptual.md) and a [knowledge store](knowledge-store-concept-intro.md) to reuse previously enriched content. Although caching incurs a storage charge, it lowers the cumulative cost of [AI enrichment](cognitive-search-concept-intro.md).

+ Keep vector payloads compact. For vector search, see the [vector  compression best practices](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/azure-ai-search-cut-vector-costs-up-to-92-5-with-new-compression-techniques/4404866).

## Monitor costs

At the service level, you can [monitor built-in metrics](search-monitor-queries.md) for your queries per second (QPS), search latency, throttled queries, and index size. You can then [create an Azure Monitor dashboard](/azure/azure-monitor/visualize/tutorial-logs-dashboards) that overlays QPS, latency, and cost data to determine when to add or remove replicas.

At the subscription or resource group level, [Cost Management](/azure/cost-management-billing/costs/overview-cost-management) provides tools to track, analyze, and control costs. You can use Cost Management to:

+ [Create budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that define and track progress against spending limits. For more granular monitoring, customize your budgets using [filters](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) for specific Azure resources or services. Filters prevent you from accidentally creating resources that incur extra costs.

+ [Create alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that automatically notify stakeholders of spending anomalies or overspending risks. Alerts are based on spending compared to budget and cost thresholds. Both budgets and alerts are created for subscriptions and resource groups, making them useful for monitoring overall costs.

+ [Export cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account. This is helpful when you or others need to perform more cost analysis. For example, a finance team can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended method for retrieving cost datasets.

## FAQ

**Can I temporarily shut down a search service to save on costs?**

Search runs as a continuous service. Dedicated resources are always operational and allocated for your exclusive use for the lifetime of your service. To stop billing entirely, you must delete the service. Deleting a service is permanent and also deletes its associated data.

**Can I change the billing rate (tier) of an existing search service?**

Existing services can be switched between Basic and Standard (S1, S2, and S3) tiers. Currently, you can only switch from a lower tier to a higher tier, such as going from Basic to S1. For more information, see [Change your pricing tier](search-capacity-planning.md#change-your-pricing-tier).

## Related content

+ [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/)
+ [Choose a pricing tier for Azure AI Search](search-sku-tier.md)
+ [Optimize your cloud investment with Cost Management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
+ [Quickstart: Start using Cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
