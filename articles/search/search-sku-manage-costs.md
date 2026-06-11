---
title: Plan and Manage Costs
description: Learn about billable events, the billing model, and tips for cost control when running an Azure AI Search service.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 06/02/2026
---

# Plan and manage costs of an Azure AI Search service

Azure AI Search is available in two pricing models:

- **Dedicated**: Provisioned capacity with fixed pricing. You select a service tier and you're billed per hour based on Search Units (SUs). Best for steady, predictable, high-utilization workloads.

- **Serverless (Preview)**: Consumption-based pricing measured by Compute Units per hour (CU/hr) and per-GB/month for indexed storage. Best for infrequent, bursty, or highly variable workloads.

This article explains how billing works under each model and provides guidance for cost estimation, minimization, and monitoring.

## Understand the pricing model

Azure AI Search has two primary pricing models: Dedicated and Serverless. Both models incur separate charges for premium features such as semantic ranker, agentic retrieval, and AI enrichment.

Azure AI Search charges are one component of your overall Azure bill. You’re billed for all Azure services and resources used in your subscription, including services outside of Azure AI Search.

For Dedicated services, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate costs based on your planned [capacity](search-capacity-planning.md) and features. A capacity-planning worksheet can help you model expected index size, indexing throughput, and indexing costs.

As your search workload evolves, follow these tips to minimize costs during both deployment and operation. You can also use built-in metrics to monitor query requests and [Cost Management](/azure/cost-management-billing/costs/overview-cost-management) to create budgets, alerts, and data exports.

### Dedicated pricing model

When you create or use a Dedicated search service, you pay for the minimum required replica and partition combination (R × P) at the prorated hourly rate of the service tier that you select. Each replica and partition combination represents a unit of dedicated capacity.

For more details on the service tiers available, see [Choose a pricing model and service tier](search-sku-tier.md).

As you increase or decrease the number of replicas or partitions, your total search units change, and costs scale accordingly. For more information and examples, see [Billing rates](search-sku-tier.md#billing-rates).

### Serverless pricing model (Preview)

[!INCLUDE [Serverless preview](./includes/previews/preview-serverless.md)]

The Serverless pricing model charges based on usage, with no pre-provisioned or idle capacity. You pay only for the compute resources consumed by operations and the storage used by your indexes.

Unlike the Dedicated model, you don't configure replicas or partitions. The service automatically manages capacity based on workload demand and service limits.

Serverless billing has two independent dimensions:

- **Compute (Compute Units, CU):**  
  Compute usage is measured in Compute Units per hour (CUs/hr). Compute cost is driven by factors such as query complexity, index size, data volume, and operation type (querying, indexing, or enrichment).

- **Indexed storage:**  
  Storage is billed per GB per month based on the on-disk size of your indexes. This size includes indexed content and supporting data structures used for retrieval.

### How you're charged for premium features

Premium features incur charges in addition to the compute and storage charges for your search service, regardless of whether you use the Dedicated or Serverless pricing model.

The following table lists premium features and their billing units. All of these features are optional, so if you don't use them, you don't incur any charges.

| Feature | Billing unit |
| --- | --- |
| Image extraction (AI enrichment) <sup>1</sup> | Per 1,000 images. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Custom Entity Lookup skill](cognitive-search-skill-custom-entity-lookup.md) (AI enrichment) | Per 1,000 text records. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing) |
| [Built-in or custom skills](cognitive-search-predefined-skills.md) (AI enrichment) <sup>2</sup> | Number of transactions. Billed at the rate of the model provider: Microsoft Foundry or Azure-hosted models or resources. |
| [Vectorizers](vector-search-how-to-configure-vectorizer.md) <sup>2</sup> | Number of vectorization operations. Billed at the rate of the model provider: Azure Vision in Foundry Tools, Azure OpenAI, or Foundry. |
| [Semantic ranker](semantic-search-overview.md) | Number of queries of `queryType=semantic`. Billed at a progressive rate. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Agentic retrieval](agentic-retrieval-overview.md) | Number of agentic reasoning tokens, plus number of tokens used in query planning and answer formulation. See the [pricing page](https://azure.microsoft.com/pricing/details/search/#pricing). |
| [Shared private link](search-indexer-howto-access-private.md) | [Billed for bandwidth](https://azure.microsoft.com/pricing/details/private-link/) as long as the shared private link exists and is used. |


<sup>1</sup> Refers to images extracted from a file within the indexer pipeline. Text extraction is free. Image extraction is billed when you [enable the `indexAction` parameter](cognitive-search-concept-image-scenarios.md#configure-indexers-for-image-processing) or when you call the [Document Extraction skill](cognitive-search-skill-document-extraction.md).

<sup>2</sup> Charges for Azure OpenAI models and Foundry models appear on your bill for those services.

### How you're otherwise charged

Depending on your configuration and usage, the following charges might apply:

+ Data traffic might incur networking costs. See the [bandwidth pricing](https://azure.microsoft.com/pricing/details/bandwidth/).

+ Several premium features, such as [knowledge stores](knowledge-store-concept-intro.md), [debug sessions](cognitive-search-debug-session.md)<sup>1</sup> , and [enrichment caches](enrichment-cache-how-to-configure.md), depend on Azure Storage and incur storage costs. Charges for these features appear on your Azure Storage bill.

+ [Customer-managed keys](search-security-manage-encryption-keys.md), which provide double encryption of sensitive content, require a billable [Azure Key Vault](https://azure.microsoft.com/pricing/details/key-vault/).

+ A skillset can include [billable built-in skills](cognitive-search-predefined-skills.md), nonbillable built-in utility skills, and custom skills. Nonbillable utility skills include [Conditional](cognitive-search-skill-conditional.md), [Shaper](cognitive-search-skill-shaper.md), [Text Merge](cognitive-search-skill-textmerger.md), and [Text Split](cognitive-search-skill-textsplit.md). They don't have an API key requirement or 20-document limit.

+ A custom skill is functionality you provide. Custom skills are billable only if they call other billable services. They don't have an API key requirement or 20-document limit.

<sup>1</sup> Debug sessions are available only in the Dedicated pricing model services.

> [!NOTE]
> On Dedicated services, you aren't billed per query. However, [service limits](search-limits-quotas-capacity.md) apply to each pricing tier. On Serverless, queries consume CU/hr based on complexity and index size. 

## Estimate and plan costs for the Dedicated pricing model

To estimate costs for the Dedicated pricing model, use the [Azure pricing calculator](https://azure.microsoft.com/pricing/calculator/) to estimate your baseline costs for Azure AI Search. You can also find estimated costs and tier comparisons on the [Select Pricing Tier](search-create-service-portal.md#choose-a-tier) page during service creation. 

For initial testing of the Dedicated pricing model, create a capacity-planning worksheet. The worksheet helps you understand the index-to-source ratio and the effect of enrichment or vector features on both capacity and cost.

To create a capacity-planning worksheet:

1. Index a small sample (1–5%) of your data. Include any [OCR](cognitive-search-skill-ocr.md), enrichment, or embedding skills you plan to use.

1. Measure the index size, indexing throughput, and indexing costs.

1. Extrapolate the results to estimate the full-scale requirements for your data.

## Estimate and plan costs for Serverless pricing model

To estimate and manage costs in Serverless, monitor both compute consumption and index size, and optimize queries and schema design to reduce resource usage.

First index a representative sample, then run typical queries and measure CU consumption via `x-ms-request-charge`. Once you have a consumption average, extrapolate costs based on that average. For guidance on monitoring compute usage, see [Optimize costs with the Serverless pricing model](serverless-cost-optimization.md#monitor-compute-usage).

## Minimize costs for the Dedicated pricing model

To minimize costs for the Dedicated pricing model, use the following strategies:

### Deployment and configuration

+ Create a search service in a [region with more storage per partition](search-limits-quotas-capacity.md#service-limits).

+ Create all related Azure resources in the same region (or as few regions as possible) to minimize or eliminate bandwidth charges.

+ Choose the lightest [service tier](search-sku-tier.md) that meets your needs. Basic and S1 offer full access to the modern API at the lowest hourly rate per SU. **For workloads with variable or bursty traffic, the Serverless pricing model might be more cost-effective than a continuously provisioned Basic or S1 service.*

+ Use [Azure Web Apps](/azure/app-service/overview) for your front-end application to keep requests and responses within the data center boundary.

### Scaling

+ [Add partitions](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when the index size or ingestion throughput requires it.

+ [Add replicas](search-capacity-planning.md#add-or-remove-partitions-and-replicas) only when your queries per second increase, when complex queries are throttling your service, or when high availability is required.

+ Scale up for resource-intensive operations, such as indexing, and then readjust downwards for regular query workloads.

+ Write code to automate scaling for predictable workload patterns.

+ Remember that capacity and pricing aren't linear. Doubling capacity more than doubles costs on the same tier. For better performance at a similar price, consider [switching to a higher tier](search-performance-tips.md#tip-switch-to-a-standard-s2-tier).

### Indexing and enrichment

+ Use [incremental indexing](search-howto-reindex.md) to process only new or changed data.

+ Use [enrichment caching](enrichment-cache-how-to-configure.md) and a [knowledge store](knowledge-store-concept-intro.md) to reuse previously enriched content. Although caching incurs a storage charge, it lowers the cumulative cost of [AI enrichment](cognitive-search-concept-intro.md).

+ Keep vector payloads compact. For vector search, see the [vector  compression best practices](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-ai-search-cut-vector-costs-up-to-92-5-with-new-compression-techniques/4404866).

## Minimize costs for the Serverless pricing model

To minimize costs for the Dedicated pricing model, use the following strategies:

- Monitor CU/hr telemetry to identify expensive queries.
- Use the simplest query type that meets relevance needs.
- Remove unused indexes to reduce storage costs.

Learn more: [Optimize costs with the Serverless pricing model](serverless-cost-optimization.md#monitor-compute-usage).


## Monitor costs

At the service level, you can [monitor built-in metrics](search-monitor-queries.md) for queries per second (QPS), search latency, throttled queries, and index size. 

How you use these metrics depends on your pricing model:

- **Dedicated pricing model:**  
  Use QPS, latency, and throttling metrics to determine when to add or remove replicas or partitions. Scaling capacity directly affects both performance and cost, so monitoring these signals helps you optimize your search units.

- **Serverless pricing model:**  
  Use these metrics to understand workload patterns and identify cost drivers. Because Serverless capacity is managed automatically, you don't scale by adding replicas or partitions. Instead, focus on monitoring compute consumption and optimizing usage.

For Serverless, you can monitor compute usage per request by using the `x-ms-request-charge` response header and analyze query patterns by using Azure Monitor logs. Tracking CU consumption by query type or workload helps identify opportunities to reduce cost through query optimization, schema design, or workload distribution.

At the subscription or resource group level, [Cost Management](/azure/cost-management-billing/costs/overview-cost-management) provides tools to track, analyze, and control costs. Use Cost Management to:

+ [Create budgets](/azure/cost-management-billing/costs/tutorial-acm-create-budgets?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that define and track progress against spending limits. For more granular monitoring, customize your budgets by using [filters](/azure/cost-management-billing/costs/group-filter?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) for specific Azure resources or services. Filters help ensure that cost tracking aligns to specific workloads or deployments.

+ [Create alerts](/azure/cost-management-billing/costs/cost-mgt-alerts-monitor-usage-spending?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) that automatically notify stakeholders of spending anomalies or overspending risks. Alerts are based on spending compared to budget and cost thresholds, and apply at the subscription or resource group level.

+ [Export cost data](/azure/cost-management-billing/costs/tutorial-export-acm-data?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn) to a storage account for deeper analysis. For example, finance teams can analyze exported data by using Excel or Power BI. Exporting cost data on a schedule is the recommended method for retrieving cost datasets.

## FAQ

**Can I temporarily shut down a search service to save on costs?**

Search runs as a continuous service. Dedicated resources are always operational and allocated for your exclusive use for the lifetime of your service.

In the Dedicated pricing model, to stop billing entirely, you must delete the service. Deleting a service is permanent and also deletes its associated data.

In the Serverless pricing model, there's no compute charge when idle. You pay only for indexed storage while the service isn't processing requests.

**Can I change the pricing model or billing rate (tier) of an existing search service?**

After you choose the Dedicated or Serverless pricing model, you can't convert your AI Search services between the two.

If you choose the Dedicated pricing model, your existing services can switch between Basic and Standard (S1, S2, and S3) tiers. Your current service configuration can't exceed the limits of the target tier, and your region can't have capacity constraints on the target tier. For more information, see [Change your pricing tier](search-capacity-planning.md#change-your-pricing-tier).

## Related content

- [Azure AI Search pricing](https://azure.microsoft.com/pricing/details/search/)
- [Optimize costs with the Serverless pricing model](serverless-cost-optimization.md#monitor-compute-usage)
- [Choose a pricing model and service tier](search-sku-tier.md)
- [Optimize your cloud investment with Cost Management](/azure/cost-management-billing/costs/cost-mgt-best-practices?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
- [Quickstart: Start using Cost analysis](/azure/cost-management-billing/costs/quick-acm-cost-analysis?WT.mc_id=costmanagementcontent_docsacmhorizontal_-inproduct-learn)
