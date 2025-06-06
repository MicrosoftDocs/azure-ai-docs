---
title: Plan and manage costs
titleSuffix: Azure AI Search
description: Learn about billable events, the billing model, and tips for cost control when running an Azure AI Search service.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: conceptual
ms.date: 06/06/2025
---

# Plan and manage costs of an Azure AI Search service

This article explains how Azure AI Search is billed and provides tips for planning, estimating, monitoring, and minimizing costs.

As a first step, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate your baseline costs. You can also find estimated costs and tier comparisons on the [Select a pricing tier](search-create-service-portal.md#choose-a-tier) page during service creation.

Through built-in cost management that cuts across service boundaries, Azure provides inclusive cost monitoring and the ability to set budgets and define alerts. The costs of running a search service vary depending on capacity and the features used. After you create a search service, optimize capacity to pay for only what you need.

> [!NOTE]
> Higher-capacity partitions are available at the same billing rate on newer services created after April and May 2024. For more information about partition size upgrades, see [Service limits](search-limits-quotas-capacity.md#service-limits).

<a name="billable-events"></a>

## Understand the billing model

Azure AI Search runs on Azure infrastructure that accrues costs when you deploy new resources. Note that other infrastructure costs might also accrue.

### How you're charged for Azure AI Search

When you create or use search resources, you're charged for:

+ The [pricing tier](search-sku-tier.md) of your search service. This is a prorated hourly rate.

+ The number of [search units](search-capacity-planning.md) (SUs) allocated to your search service. SUs are units of capacity that equal the product of replicas and partitions (R × P = SU) used by your service.

### How you're charged for premium features

The following table lists premium features and their billing units. All of these features are optional, and you can choose to enable them as needed.

| Feature | Unit |
|-------|------|
| Image extraction (AI enrichment) <sup>1</sup> | Per 1000 images. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Custom Entity Lookup skill](cognitive-search-skill-custom-entity-lookup.md) (AI enrichment) | Per 1000 text records. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing) |
| [Built-in skills](cognitive-search-predefined-skills.md)  (AI enrichment) | Number of transactions, billed at the same rate as calling Azure AI services directly. You can process 20 documents per indexer per day for free. Larger or more frequent workloads require an Azure AI services multi-service resource key. |
| [Semantic ranker](semantic-search-overview.md) | Number of queries of `queryType=semantic`, billed at a progressive rate. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Shared private link](search-indexer-howto-access-private.md) | [Billed for bandwidth](https://azure.microsoft.com/pricing/details/private-link/) as long as the shared private link exists and is used. |

<sup>1</sup> Refers to images extracted from a file within the indexer pipeline. Text extraction is free. Image extraction is billed when you [enable the `indexAction` parameter](cognitive-search-concept-image-scenarios.md#configure-indexers-for-image-processing) for document cracking or when you call the [Document Extraction skill](cognitive-search-skill-document-extraction.md).

### How you're otherwise charged

+ Data traffic might incur networking costs. See the [Bandwidth pricing](https://azure.microsoft.com/pricing/details/bandwidth/).

+ Several premium features, such as [knowledge store](knowledge-store-concept-intro.md), [debug sessions](cognitive-search-debug-session.md), and [enrichment cache](cognitive-search-incremental-indexing-conceptual.md), depend on Azure Storage and incur storage costs. Meters for using these features are included in the Azure Storage bill.

+ [Customer-managed keys](search-security-manage-encryption-keys.md), which provide double encryption of sensitive content, require a billable [Azure Key Vault](https://azure.microsoft.com/pricing/details/key-vault/).

+ A skillset can include [billable built-in skills](cognitive-search-predefined-skills.md), non-billable built-in utility skills, and custom skills. Non-billable utility skills include [Conditional](cognitive-search-skill-conditional.md), [Shaper](cognitive-search-skill-shaper.md), [Text Merge](cognitive-search-skill-textmerger.md), and [Text Split](cognitive-search-skill-textsplit.md). They don't have an API key requirement or 20-document limit.

+ A custom skill is functionality you provide. Custom skills are only billable if they call other billable services. They don't have an API key requirement or 20-document limit.

> [!NOTE]
> You aren't billed for the number of full-text or vector queries, query responses, or documents ingested, but [service limits](search-limits-quotas-capacity.md) apply to each pricing tier.

## Monitor costs

Cost management is built into the Azure infrastructure. Review [Billing and cost management](/azure/cost-management-billing/cost-management-billing-overview) for more information about tracking costs, tools, and APIs.

## Minimize costs

Follow these guidelines to minimize costs of an Azure AI Search solution.

1. If possible, create a search service [in a region that has more storage per partition](search-limits-quotas-capacity.md#service-limits). If you're using multiple Azure resources in your solution, create them in the same region, or in as few regions as possible, to minimize or eliminate bandwidth charges.

1. [Scale up](search-capacity-planning.md) for resource-intensive operations like indexing, and then readjust downwards for regular query workloads. If there are predictable patterns to your workloads, you might be able to synchronize scale up to coincide with the expected volume (you would need to write code to automate this).

   When estimating the cost of a search solution, keep in mind that pricing and capacity aren't linear (doubling capacity more than doubles the cost on the same tier). Also, at some point, switching up to a higher tier can give you better and faster performance at roughly the same price point. For more information and an example, see [Switch to a Standard S2 tier](search-performance-tips.md#tip-switch-to-a-standard-s2-tier).

1. Consider [Azure Web App](/azure/app-service/overview) for your front-end application so that requests and responses stay within the data center boundary.

1. If you're using [AI enrichment](cognitive-search-concept-intro.md), there's an extra charge for blob storage, but the cumulative cost goes down if you enable [enrichment caching](cognitive-search-incremental-indexing-conceptual.md).

## Create budgets

You can create [budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to manage costs and create [alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that automatically notify stakeholders of spending anomalies and overspending risks. Alerts are based on spending compared to budget and cost thresholds. Budgets and alerts are created for Azure subscriptions and resource groups, so they're useful as part of an overall cost monitoring strategy. 

Budgets can be created with filters for specific resources or services in Azure if you want more granularity present in your monitoring. Filters help ensure that you don't accidentally create new resources that cost you extra money. For more information about the filter options available when you create a budget, see [Group and filter options](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).

## Export cost data

You can also [export your cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account. This is helpful when you need or others to do more data analysis for costs. For example, a finance team can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended way to retrieve cost datasets.

## FAQ

**Can I temporarily shut down a search service to save on costs?**

Search runs as a continuous service. Dedicated resources are always operational, allocated for your exclusive use for the lifetime of your service. To stop billing entirely, you must delete the service. Deleting a service is permanent and also deletes its associated data.

**Can I change the billing rate (tier) of an existing search service?**

Existing services can be switched between Basic and Standard (S1, S2, and S3) tiers. Currently, you can only switch from a lower tier to a higher tier, such as going from Basic to S1. For more information, see [Change your pricing tier](search-capacity-planning.md#change-your-pricing-tier).

## Next steps

+ Learn more on how pricing works with Azure AI Search. See [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/).
+ Learn more about [replicas and partitions](search-sku-tier.md).
+ Learn [how to optimize your cloud investment with Cost Management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
+ Learn more about managing costs with [cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
+ Learn about how to [prevent unexpected costs](/azure/cost-management-billing/cost-management-billing-overview?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn).
+ Take the [Cost Management](/training/paths/control-spending-manage-bills?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) guided learning course.
