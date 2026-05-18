---
title: Estimate Capacity for Query and Index Workloads
description: Learn how capacity is structured and used in Azure AI Search, and how to estimate the resources needed for indexing and query workloads.
author: mattwojo
ms.author: mattwoj
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
  - ignite-2024
ms.topic: how-to
ms.date: 06/02/2026
ms.update-cycle: 180-days
ai-usage: ai-assisted
---

# Estimate and manage capacity of a search service

Azure AI Search offers two pricing models that handle capacity differently:

- **Dedicated**: Plan capacity by sizing replicas and partitions. See: [Plan capacity for the Dedicated model](#plan-capacity-for-the-dedicated-model).
    - You pre-provision capacity directly using replicas and partitions.
    - Estimate: Required storage (partitions) and required throughput (replicas). 
    - [Choose a pricing tier](./search-sku-tier.md) based on expected peak demand.
    - Once capacity is configured upfront, you pay an hourly rate, regardless of usage. 

- **Serverless (Preview)**: Plan capacity by optimizing workload efficiency and cost drivers. See: [Plan capacity for the Serverless model](#plan-capacity-for-the-serverless-model).
    - Capacity is managed automatically based on usage and service limits. No capacity pre-provisioning required.
    - Capacity automatically scales with demand (can scale to zero when idle).
    - You’re billed for [compute (CUs)](./serverless-cost-optimization.md) and storage based on actual usage.
    - Rather than infrastructure, planning focuses on these cost drivers: Query patterns, Index size and growth, and Data ingestion patterns.


Both pricing models provide the same Azure AI Search features and APIs.

| Dimension | Dedicated | Serverless |
| --- | --- | --- |
| Capacity model | Provisioned (replicas × partitions) | Consumption-based |
| Scaling | Manual | Automatic |
| User control | Explicit (configure replicas and partitions) | Indirect (influenced by workload characteristics) |
| Billing | Fixed hourly rate per SU | Pay for compute (CUs) and storage |
| Idle cost | Always incurred (minimum provisioned capacity) | Scales to zero when idle |
| Optimization focus | Infrastructure sizing | Workload efficiency |
| Best for | Predictable, steady workloads | Variable, bursty, or multi-tenant workloads, including agent-driven scenarios |
| Capacity planning approach | Size and scale infrastructure (replicas and partitions) | Optimize workload efficiency and usage patterns |
| Inefficiency impact | Latency and scaling pressure | Direct cost increase |


> [!NOTE]
> If your service was created before April or May 2024 with the Dedicated pricing model, a one-time upgrade to higher storage limits might be available at no extra cost. For more information, see [Upgrade your search service](search-how-to-upgrade.md).

Learn more about how to:

- [Plan and manage costs](search-sku-manage-costs.md)
- [Optimize costs with the Serverless pricing model](serverless-cost-optimization.md)
- [Choose a service tier for the Dedicated pricing model](search-sku-tier.md)

## Plan capacity for the Dedicated model

In the Dedicated model, you provision capacity using **search units (SU)**:

- **Search unit (SU)** = replicas × partitions
- **Replica**: Copies of the search engine. Provides query throughput and high availability.
- **Partition**: Units of storage. Provides storage and indexing throughput.

Each service starts with 1 replica × 1 partition (1 SU). You can add or remove replicas and partitions independently to accommodate fluctuating workloads. Adding capacity increases the [cost of running a search service](search-sku-manage-costs.md#billable-events).

| Concept  | Definition|
|----------|-----------|
|*Search unit* | A single increment of total available capacity. A minimum of one search unit is required to run the service. Depending on your pricing tier, the maximum ranges from one to 36 units.<br><br>The number of search units equals the number of replicas multiplied by the number of partitions: R × P = SU. Each service starts with one replica and one partition, which consumes one unit: 1 × 1 = 1. Adding a second replica consumes two units: 2 × 1 = 2.<br><br>A search unit is also the billing unit for a search service. |
|*Replica* | Instances of the search service, used primarily to load balance query operations. Each replica hosts one copy of an index. If you allocate three replicas, you have three copies of an index available for servicing query requests.|
|*Partition* | Physical storage and I/O for read/write operations (for example, when rebuilding or refreshing an index). Each partition has a slice of the total index. If you allocate three partitions, your index is divided into thirds. |

Review the [partitions and replicas table](#partition-and-replica-combinations-for-the-dedicated-model) for possible combinations that stay under the 36 unit limit.

The physical characteristics of replicas and partitions, such as processing speed and disk IO, vary by [pricing tier](search-sku-tier.md). On a standard search service, the replicas and partitions are faster and larger than those of a basic service.

### When to add capacity for the Dedicated model

Consider adding replicas or partitions when:

- Query latency increases or service-level agreement criteria aren't being met.
- The frequency of HTTP 503 (Service unavailable) errors is increasing.
- The frequency of HTTP 429 (Too many requests) errors is increasing, an indication of request throttling.
- Large query volumes are expected.
- Indexing jobs are slow or falling behind.
- Storage or indexing throughput is insufficient.

Scaling guidance:

- Add **replicas** to increase query throughput and availability.
- Add **partitions** to increase storage and indexing performance.
- Query-heavy workloads typically require more replicas.
- Large indexes may require additional replicas to maintain performance.

> [!IMPORTANT]
> Scaling operations can take time to complete and increase cost. Always validate changes using performance testing and pricing estimates.

The [tier you choose](search-sku-tier.md) determines partition size and speed, and each tier is optimized around a set of characteristics that fit various scenarios. If you choose a higher-end tier, you might [need fewer partitions](search-performance-tips.md#service-capacity) than if you go with S1. One of the questions you need to answer through self-directed testing is whether a larger and more expensive partition yields better performance than two cheaper partitions on a service provisioned at a lower tier.

A single service must have sufficient resources to handle all workloads (indexing and queries). Neither workload runs in the background. You can schedule indexing for times when query requests are naturally less frequent, but the service doesn't otherwise prioritize one task over another. Additionally, a certain amount of redundancy smooths out query performance when services or nodes are updated internally.

As a general rule, search applications tend to need more replicas than partitions, particularly when the service operations are biased toward query workloads. Each replica is a copy of your index, allowing the service to load balance requests against multiple copies. Azure AI Search manages all load balancing and replication of an index, and you can alter the number of replicas allocated for your service at any time. You can allocate up to 12 replicas in a Standard search service and 3 replicas in a Basic search service. Replica allocation can be made either from the [Azure portal](search-create-service-portal.md) or one of the programmatic options.

Extra partitions are helpful for intensive indexing workloads. Extra partitions spread read/write operations across a larger number of compute resources.

Finally, larger indexes take longer to query. As such, you might find that every incremental increase in partitions requires a smaller but proportional increase in replicas. The complexity of your queries and query volume factors into how quickly query execution is turned around.

For service limits and valid scaling ranges, see:
- [Service limits for tiers and SKUs](search-limits-quotas-capacity.md)
- [Choose a service tier](search-sku-tier.md)

> [!NOTE]
> Adding more replicas or partitions increases the cost of running the service, and can introduce slight variations in how results are ordered. Be sure to check the [pricing calculator](https://azure.microsoft.com/pricing/calculator/) to understand the billing implications of adding more nodes. The [partition and replica combinations table](#partition-and-replica-combinations-for-the-dedicated-model) can help you cross-reference the number of search units required for a specific configuration. For more information on how extra replicas affect query processing, see [Ordering results](search-pagination-page-layout.md#ordering-results).

### How to manage and adjust capacity for the Dedicated model

Changing capacity isn't instantaneous. Depending on data volume and operation type, scaling can take from minutes to several hours.

When scaling a search service, you can choose from the following tools and approaches:

- [Azure portal](#add-or-remove-partitions-and-replicas-for-the-dedicated-model)
- [Azure PowerShell](search-manage-powershell.md#scale-replicas-and-partitions)
- [Azure CLI](/cli/azure/search/service#az-search-service-create-optional-parameters)
- [Management REST API](/rest/api/searchmanagement/services/create-or-update)

> [!NOTE]
> If your search service was created before April or May 2024, it might be eligible for a one-time upgrade to newer infrastructure with larger partition sizes at no extra cost. This upgrade can increase available storage per partition and reduce the number of partitions required for your workload. For more information, see [Upgrade your search service](search-how-to-upgrade.md).

To increase or decrease the capacity of your service, you have two options:

- [Add or remove partitions and replicas](#add-or-remove-partitions-and-replicas-for-the-dedicated-model)
- [Change your pricing tier](#change-your-pricing-tier-for-the-dedicated-model)

#### Add or remove partitions and replicas for the Dedicated model

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. From the left pane, select **Settings** > **Scale**.

   The following screenshot shows a Standard service provisioned with one replica and partition. The formula at the bottom indicates how many search units are being used (1). If the unit price was $100 (not a real price), the monthly cost of running this service would be $100 on average.

   :::image type="content" source="media/search-capacity-planning/initial-values.png" alt-text="Screenshot of the Scale page showing the current replica and partition values." border="true" lightbox="media/search-capacity-planning/initial-values.png":::

1. Use the slider to increase or decrease the number of partitions, and then select **Save**.

   This example adds a second replica and partition. Notice the search unit count; it's now four because the billing formula is replicas multiplied by partitions (2 x 2). Doubling capacity more than doubles the cost of running the service. If the search unit cost was $100, the new monthly bill would now be $400.

   For the current per unit costs of each tier, visit the [pricing page](https://azure.microsoft.com/pricing/details/search/).

   :::image type="content" source="media/search-capacity-planning/add-two-each.png" alt-text="Screenshot of the Scale page with added replicas and partitions." border="true" lightbox="media/search-capacity-planning/add-two-each.png":::

1. Check your notifications to confirm that the operation started.

   :::image type="content" source="media/search-capacity-planning/portal-notifications.png" alt-text="Screenshot of the notification of the scaling operation in the Azure portal." border="true" lightbox="media/search-capacity-planning/portal-notifications.png":::

   This operation can take several hours to complete. It occurs in the background, so your search service remains fully operational and available for read and write operations.

   You can't cancel the operation or monitor its progress. However, the following message displays while changes are underway.

   :::image type="content" source="media/search-capacity-planning/updating-message.png" alt-text="Screenshot of the Updating message in the Azure portal." border="true" lightbox="media/search-capacity-planning/updating-message.png":::

### Change your pricing tier for the Dedicated model

> [!NOTE]
> The Azure portal and [Services - Update (REST API)](/rest/api/searchmanagement/services/update) support changes between Basic and Standard (S1, S2, and S3) tiers. You can upgrade or downgrade tiers, provided your current service configuration doesn't exceed the [limits of the target tier](search-limits-quotas-capacity.md). Your region also can't have [capacity constraints on the target tier](search-region-support.md).

Your pricing tier determines the maximum storage of your search service. If you need more or less capacity, you can switch to a different pricing tier that accommodates your storage needs.

In addition to capacity, pricing tiers determine limits on indexes, indexers, and other search objects. Compare the [service limits](search-limits-quotas-capacity.md) of your current tier and your desired tier before you proceed. Generally, switching to a higher tier increases your [storage limit](search-limits-quotas-capacity.md#service-limits) and [vector limit](search-limits-quotas-capacity.md#vector-index-size-limits), increases request throughput, and decreases latency, while switching to a lower tier has the opposite effect.

Switching to a higher pricing tier also increases the cost of running your search service. For more information, see the [pricing page](https://azure.microsoft.com/pricing/details/search/).

To change your pricing tier:

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. From the left pane, select **Settings** > **Scale**.

1. Under your current tier, select **Change Pricing Tier**.

   :::image type="content" source="media/search-capacity-planning/change-pricing-tier.png" alt-text="Screenshot of the Change Pricing Tier button in the Azure portal." border="true" lightbox="media/search-capacity-planning/change-pricing-tier.png":::

1. On the **Select Pricing Tier** page, choose a different tier from the list.

   You can switch between Basic, S1, S2, and S3, but you can't switch to or from Free, S3HD, L1, or L2. These tiers aren't selectable and appear dimmed.

   :::image type="content" source="media/search-capacity-planning/pricing-tier-list.png" alt-text="Screenshot of the Select Pricing Tier page and the list of available tiers in the Azure portal." border="true" lightbox="media/search-capacity-planning/pricing-tier-list.png":::

1. To start the scale operation, select **Save**.

   :::image type="content" source="media/search-capacity-planning/save-button.png" alt-text="Screenshot of the Save button in the Azure portal." border="true" lightbox="media/search-capacity-planning/save-button.png":::

   This operation can take several hours to complete. It occurs in the background, so your search service remains fully operational and available for read and write operations.

   You can't cancel the operation or monitor its progress. However, the following message displays while changes are underway.

   :::image type="content" source="media/search-capacity-planning/updating-message.png" alt-text="Screenshot of the Updating message in the Azure portal." border="true" lightbox="media/search-capacity-planning/updating-message.png":::

### How scale requests are handled for the Dedicated model

Upon receipt of a scale request, the search service:

1. Checks whether the request is valid.
1. Starts backing up data and system information.
1. Checks whether the service is already in a provisioning state (currently adding or eliminating either replicas or partitions).
1. Starts provisioning.

Scaling a service can take from several minutes to several hours, depending on the size of the service and the scope of the request. Backup duration also varies based on the amount of data and number of partitions and replicas.

The above steps aren't entirely consecutive. For example, the system starts provisioning when it can safely do so, which could be while backup is winding down.

#### Errors during scaling

The following table lists causes and solutions for errors that can occur during scaling operations.

| Error message | Cause | Solution |
| --- | --- | --- |
| "Service update operations aren't allowed at this time because we're processing a previous request." | Another scaling operation is in progress. | Check the **Overview** page in the Azure portal or use the [Search Management REST API](/rest/api/searchmanagement/services/get), [Azure PowerShell](search-manage-powershell.md#get-search-service-information), or [Azure CLI](search-manage-azure-cli.md#get-search-service-information) to get the status of your search service. If the status is "Provisioning," wait until it becomes "Succeeded" or "Failed" before you try again. <sup>1, 2</sup> |
| "Failed to scale search service *servicename*. Error: *Object* count *ActualCount* exceeds allowable limit: *MaximumCount*." | Your current service configuration exceeds the limits of the target pricing tier. | Check that your storage usage, vector usage, indexes, indexers, and other objects fit within the lower tier's [service limits](search-limits-quotas-capacity.md). For example, the Basic tier supports up to 15 indexes, so you can't switch from S1 to Basic if you have 16 indexes. Adjust your resources before you try again. |

<sup>1</sup> There's no status for backups, which are internal operations that are unlikely to disrupt a scaling exercise.

<sup>2</sup> If your search service appears to be stalled in a provisioning state, check for orphaned indexes that are unusable, with zero query volumes and no index updates. An unusable index can block changes to service capacity. In particular, look for [CMK-encrypted](search-security-manage-encryption-keys.md) indexes whose keys are no longer valid. Either delete the index or restore the keys to bring the index back online and unblock your scaling operation.

### Partition and replica combinations for the Dedicated model

The following chart applies to Standard tier and higher. It shows all possible combinations of partitions and replicas, subject to the 36 search unit maximum per service. 

|   | **1 partition** | **2 partitions** | **3 partitions** | **4 partitions** | **6 partitions** | **12 partitions** |
| --- | --- | --- | --- | --- | --- | --- |
| **1 replica** |1 SU |2 SU |3 SU |4 SU |6 SU |12 SU |
| **2 replicas** |2 SU |4 SU |6 SU |8 SU |12 SU |24 SU |
| **3 replicas** |3 SU |6 SU |9 SU |12 SU |18 SU |36 SU |
| **4 replicas** |4 SU |8 SU |12 SU |16 SU |24 SU |N/A |
| **5 replicas** |5 SU |10 SU |15 SU |20 SU |30 SU |N/A |
| **6 replicas** |6 SU |12 SU |18 SU |24 SU |36 SU |N/A |
| **12 replicas** |12 SU |24 SU |36 SU |N/A |N/A |N/A |

Basic search services have lower search unit counts.

- On search services created before April 3, 2024, Basic services can have exactly one partition and up to three replicas for a maximum limit of three SUs. The only adjustable resource is replicas. However, you might be able to increase your partition count by [upgrading your service](search-how-to-upgrade.md).

- On search services created after April 3, 2024 in [supported regions](search-limits-quotas-capacity.md#service-limits), Basic services can have up to three partitions and three replicas. The maximum SU limit is nine to support a full complement of partitions and replicas.

For search services on any billable tier, regardless of creation date, you need a minimum of two replicas for high availability on queries.

For billing rates per tier and currency, see the [Azure AI Search pricing page](https://azure.microsoft.com/pricing/details/search/).

### Estimate capacity using a Dedicated pricing model tier

The size of the indexes you expect to build determines storage needs. There are no solid heuristics or generalities that help with estimates. The only way to determine the size of an index is [build one](search-what-is-an-index.md). Its size is based on tokenization and embeddings, and whether you enable suggesters, filtering, and sorting, or can take advantage of [vector compression](vector-search-how-to-quantization.md).

We recommend estimating on a billable tier, Basic or higher. The Free tier runs on physical resources shared by multiple customers and is subject to factors beyond your control. Only the dedicated resources of a billable search service can accommodate larger sampling and processing times for more realistic estimates of index quantity, size, and query volumes during development. 

1. [Review service limits at each tier](search-limits-quotas-capacity.md#service-limits) to determine whether lower tiers can support the number of indexes you need. Consider whether you need multiple copies of an index for active development, testing, and production. 

   A search service is subject to object limits (maximum number of indexes, indexers, skillsets, etc.) and storage limits. Whichever limit is reached first is the effective limit. 

1. [Create a service at a billable tier](search-create-service-portal.md). Tiers are optimized for certain workloads. For example, the Storage Optimized tier has a limit of 10 indexes because it's designed to support a low number of large indexes.

    - Start low, at Basic or S1, if you're not sure about the projected load.

    - Start high, at S2 or even S3, if testing includes large-scale indexing and query loads.

    - Start with Storage Optimized, at L1 or L2, if you're indexing a large amount of data and query load is relatively low, as with an internal business application.

1. [Build an initial index](search-what-is-an-index.md) to determine how source data translates to an index. This is the only way to estimate index size. Attributes on the field definitions affect physical storage requirements:

   - For keyword search, marking fields as filterable and sortable [increases index size](search-what-is-an-index.md#physical-structure-and-size).

   - For vector search, you can [set parameters to reduce vector size](vector-search-how-to-configure-compression-storage.md).

1. [Monitor storage, service limits, query volume, and latency](monitor-azure-cognitive-search.md) in the Azure portal. The Azure portal shows queries per second, throttled queries, and search latency. These values can help you decide if you selected the right tier.

1. Add replicas for high availability or to mitigate slow query performance.

   There are no guidelines on how many replicas are needed to accommodate query loads. Query performance depends on the complexity of the query and competing workloads. Although adding replicas clearly results in better performance, the result isn't strictly linear: adding three replicas doesn't guarantee triple throughput. For guidance in estimating QPS for your solution, see [Analyze performance](search-performance-analysis.md) and [Monitor queries](search-monitor-queries.md).

For an [inverted index](https://en.wikipedia.org/wiki/Inverted_index), size and complexity are determined by content, not necessarily by the amount of data that you feed into it. A large data source with high redundancy could result in a smaller index than a smaller dataset that contains highly variable content. So it's rarely possible to infer index size based on the size of the original dataset.

Storage requirements can be inflated if you include data that will never be searched. Ideally, documents contain only the data that you need for the search experience.

### Service-level agreement considerations

The Free tier and preview features aren't covered by [service-level agreements (SLAs)](https://azure.microsoft.com/support/legal/sla/search/v1_0/). For all billable tiers, SLAs take effect when you provision sufficient redundancy for your service.

- Two or more replicas satisfy query (read) SLAs.

- Three or more replicas satisfy query and indexing (read-write) SLAs.

The number of partitions doesn't affect SLAs.

## Plan capacity for the Serverless model

In the Serverless pricing model:

- Capacity is automatically managed by the service.
- There are no replicas, partitions, or search units to configure.
- Compute scales dynamically based on the workload (query and indexing demand) and can scale to zero when idle. 

Billing is based on two dimensions:
- **Compute usage (CUs):** Charged based on query and indexing operations.
- **Indexed storage:** Charged per GB per month.

Because billing is consumption-based, cost is directly tied to usage:
- Complex queries consume more compute.
- Inefficient schema design increases both indexing and query costs.
- Poor query patterns with large or frequently updated indexes increase storage and compute usage.

### Optimize workload efficiency

Because inefficiency manifests as cost in the Serverless model, you will pay more for the same work if you don't practice workload-aware design. The best way to control Serverless spend is to design your indexes and queries efficiently from the start.

To design workloads for efficiency when using the Serverless pricing model, consider:

**Index design**
- Include only fields used in queries.
- Reduce vector dimensions where possible.
- Avoid unnecessary filterable, sortable, or facetable attributes.

**Query patterns**
- Use `$select` to limit returned fields.
- Apply filters early to reduce result sets.
- Avoid deep paging (`$skip`).
- Prefer targeted queries over broad full-text queries.
- Use hybrid search carefully due to higher compute cost.

**Monitoring**
- Monitor **CU consumption** to identify expensive queries.
- Track storage growth and remove unused data.

In Serverless, improving performance (faster, more targeted queries) typically reduces cost.

Learn more: [Optimize costs with the Serverless pricing model in Azure AI Search](serverless-cost-optimization.md)

## Regional capacity considerations

Capacity and availability can vary by the [supported region](search-region-support.md). Some regions may have constraints on provisioning new services or scaling existing ones.

If your preferred Azure AI Search region is unavailable due to capacity constraints, see [How to handle regional capacity constraints in Azure AI Search](search-region-capacity.md).

## Next steps

> [!div class="nextstepaction"]
> [Plan and manage costs](search-sku-manage-costs.md)
