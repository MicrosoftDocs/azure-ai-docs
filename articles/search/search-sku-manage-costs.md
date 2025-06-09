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
ms.topic: how-to
ms.date: 06/09/2025
---

# Plan and manage costs of an Azure AI Search service

This article explains how Azure AI Search is billed and provides tips for estimating, planning, monitoring, and minimizing costs. The cost of running a search service varies based on capacity and the features used. After you create a search service, optimize its capacity so that you only pay for what you need.

> [!NOTE]
> Higher-capacity partitions are available at the same billing rate on newer services created after April and May 2024. For more information about partition size upgrades, see [Service limits](search-limits-quotas-capacity.md#service-limits).

<a name="billable-events"></a>

## Understand the billing model

Azure AI Search runs on Azure infrastructure that accrues costs when you deploy new resources. Other infrastructure costs might also accrue.

### How you're charged for Azure AI Search

When you create or use search resources, you're charged for:

+ The [pricing tier](search-sku-tier.md) of your search service. This is a prorated hourly rate.

+ The number of [search units](search-capacity-planning.md) (SUs) allocated to your search service. SUs are units of capacity that equal the product of replicas and partitions (R × P = SU) used by your service.

### How you're charged for premium features

The following table lists premium features and their billing units. All of these features are optional, and you can choose to enable them as needed.

| Feature | Unit |
|-------|------|
| Image extraction (AI enrichment) <sup>1</sup> | Per 1,000 images. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Custom Entity Lookup skill](cognitive-search-skill-custom-entity-lookup.md) (AI enrichment) | Per 1,000 text records. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing) |
| [Built-in skills](cognitive-search-predefined-skills.md)  (AI enrichment) | Number of transactions. Billed at the same rate as calling Azure AI services directly. You can process 20 documents per indexer per day for free. Larger or more frequent workloads require an Azure AI services multi-service resource key. |
| [Semantic ranker](semantic-search-overview.md) | Number of queries of `queryType=semantic`. Billed at a progressive rate. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Shared private link](search-indexer-howto-access-private.md) | [Billed for bandwidth](https://azure.microsoft.com/pricing/details/private-link/) as long as the shared private link exists and is used. |

<sup>1</sup> Refers to images extracted from a file within the indexer pipeline. Text extraction is free. Image extraction is billed when you [enable the `indexAction` parameter](cognitive-search-concept-image-scenarios.md#configure-indexers-for-image-processing) for document cracking or when you call the [Document Extraction skill](cognitive-search-skill-document-extraction.md).

### How you're otherwise charged

+ Data traffic might incur networking costs. See the [Bandwidth pricing](https://azure.microsoft.com/pricing/details/bandwidth/).

+ Several premium features, such as [knowledge store](knowledge-store-concept-intro.md), [debug sessions](cognitive-search-debug-session.md), and [enrichment cache](cognitive-search-incremental-indexing-conceptual.md), depend on Azure Storage and incur storage costs. Meters for using these features are included in the Azure Storage bill.

+ [Customer-managed keys](search-security-manage-encryption-keys.md), which provide double encryption of sensitive content, require a billable [Azure Key Vault](https://azure.microsoft.com/pricing/details/key-vault/).

+ A skillset can include [billable built-in skills](cognitive-search-predefined-skills.md), nonbillable built-in utility skills, and custom skills. Nonbillable utility skills include [Conditional](cognitive-search-skill-conditional.md), [Shaper](cognitive-search-skill-shaper.md), [Text Merge](cognitive-search-skill-textmerger.md), and [Text Split](cognitive-search-skill-textsplit.md). They don't have an API key requirement or 20-document limit.

+ A custom skill is functionality you provide. Custom skills are only billable if they call other billable services. They don't have an API key requirement or 20-document limit.

> [!NOTE]
> You aren't billed for the number of full-text or vector queries, query responses, or documents ingested, but [service limits](search-limits-quotas-capacity.md) apply to each pricing tier.

## Estimate and plan costs

Effective cost planning starts before you create an Azure AI Search service. Use the [pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate your baseline costs. You can also compare the features and costs of each tier on the [Select a pricing tier](search-create-service-portal.md#choose-a-tier) page during service creation.

For initial testing, we reccomend that you index 1–5% of your representative content. Include any OCR, embeddings, or enrichment skills you plan to use. Measure the resulting index size, throughput, and costs, and then extrapolate them to estimate full-scale requirements. This approach helps you understand the index-to-source ratio and the impact of enrichment or vector features on both [capacity](search-capacity-planning.md) and cost.

<!-- If you're using [skillsets](cognitive-search-working-with-skillsets.md) with AI enrichment, computer vision, embedding requests, custom skills, or any other transformation or external service, each skill runs on a separate meter and has its own pricing. Review the pricing for each skill you plan to use. Enable incremental enrichment so unchanged skills are skipped after the first run, when applicable.

When planning, consider:

+ Indexing and enrichment volume. Estimate the frequency and volume of data ingestion and enrichment, as these drive both compute and potential AI service charges.

+ Data transfer and storage. Account for networking and storage costs, especially if your solution spans multiple regions or uses additional Azure resources.

+ Service limits. Review [service limits](search-limits-quotas-capacity.md) for your chosen tier to avoid unplanned scale-ups or throttling.

+ Skillset and enrichment metering. If you are using AI enrichment, image extraction, computer vision, embedding requests, custom skills, or any other transformation or external service, be aware that each skill runs on a separate meter and may have its own pricing. Review the pricing for each skill you plan to use. Enable incremental enrichment so unchanged skills are skipped after the first run, when applicable. -->

## Monitor costs

At the Azure AI Search level, you can [monitor built-in metrics](search-monitor-queries.md) for queries per second (QPS), search latency, throttled queries, and index size. You can then [create an Azure Monitor dashboard](/azure-monitor/visualize/tutorial-logs-dashboards) that overlays QPS, latency, and cost data to determine when to add or remove replicas.

At the subscription or resource group level, [Cost Management](/azure/cost-management-billing/costs/overview-cost-management) provides tools to track, analyze, and control your costs. You can use Cost Management to:

+ [Create budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets) that define and track progress against spending limits. For more granular monitoring, customize your budgets using [filters](/azure/cost-management-billing/costs/group-filter) for specific Azure resources or services. Filters prevent you from accidentally creating resources that incur extra costs.

+ [Create alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending) that automatically notify stakeholders of spending anomalies or overspending risks. Alerts are based on spending compared to budget and cost thresholds. Both budgets and alerts are created for subscriptions and resource groups, making them useful for monitoring overall costs.

+ [Export cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data) to an Azure Storage account. This is helpful when you or others need to perform additional cost analysis. For example, a finance team can analyze the data using Excel or Power BI. You can export your costs on a daily, weekly, or monthly schedule and set a custom date range. Exporting cost data is the recommended method for retrieving cost datasets.

## Minimize costs

To minimize the costs of your Azure AI Search solution, use the following strategies across the service lifecycle.

### Deployment and configuration

+ Create a search service in a [region with more storage per partition](search-limits-quotas-capacity.md#service-limits).

+ Create all related Azure resources in the same region (or as few regions as possible) to minimize or eliminate bandwidth charges.

+ Choose the lightest [pricing tier](search-sku-tier.md) that meets your needs. Basic and S1 offer full access to the modern API at the lowest hourly rate per SU.

+ Use [Azure Web App](/azure/app-service/overview) for your front-end application to keep requests and responses within the data center boundary.

### Scaling

+ [Add partitions](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when the index size or ingestion throughput requires it.

+ [Add replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when your queries per second increase, when complex queries are throttling your service, or when high availability is required.

+ Scale up for resource-intensive operations, such as indexing, and then readjust downwards for regular query workloads.

+ Write code to automate scaling for predictable workload patterns.

+ Remember that capacity and pricing aren't linear. Doubling capacity more than doubles costs on the same tier. For better performance at a similar price, consider [switching to a higher tier](search-performance-tips.md#tip-switch-to-a-standard-s2-tier).

### Indexing and enrichment

+ Use [incremental indexing](search-howto-reindex.md) to process only new or changed data.

+ Enable [enrichment caching](cognitive-search-incremental-indexing-conceptual.md) to reduce [AI enrichment](cognitive-search-concept-intro.md) costs. Although caching incurs a charge for Azure Blob Storage, it lowers the cumulative enrichment cost because storage is cheaper than image extraction and AI processing.

+ Keep vector payloads compact. For vector search, see the [vector  compression best practices](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/azure-ai-search-cut-vector-costs-up-to-92-5-with-new-compression-techniques/4404866).

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
