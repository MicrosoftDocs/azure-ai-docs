---
title: Service Upgrade in the Azure portal
titleSuffix: Azure AI Search
description: Learn how to upgrade your existing Azure AI Search service to high-capacity storage and processors in your region.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.custom: references_regions
ms.date: 08/08/2025
ms.update-cycle: 180-days
---

# Upgrade your Azure AI Search service in the Azure portal

An upgrade brings older search services to the capabilities of new services created in the same region. Specifically, it upgrades the computing power of the underlying service. This one-time operation doesn't introduce breaking changes to your application, and you shouldn't need to change any code.

For [eligible services](#upgrade-eligibility), an upgrade increases the [partition storage](#higher-storage-limits) and [vector index size](#higher-vector-limits) on the same pricing tier at no extra cost.

This article describes how to upgrade your service in the [Azure portal](https://portal.azure.com/). Alternatively, you can use the [Search Management REST APIs](/rest/api/searchmanagement/) to upgrade your service programmatically. For more information, see [Manage your search service using REST](search-manage-rest.md#upgrade-a-service).

> [!TIP]
> Looking to [change your pricing tier](search-capacity-planning.md#change-your-pricing-tier)? You can switch between Basic and Standard (S1, S2, and S3) tiers.

## About service upgrades

In April 2024, Azure AI Search increased the [storage capacity](search-limits-quotas-capacity.md#service-limits) of newly created search services. Services created before April 2024 saw no capacity changes, so if you wanted larger and faster partitions, you had to create a new service. However, some older services can now be upgraded to benefit from the higher-capacity partitions.

Currently, an upgrade only increases the [storage limit](#higher-storage-limits) and [vector index size](#higher-vector-limits) of [eligible services](#upgrade-eligibility).

### Upgrade eligibility

To qualify for an upgrade, your service must:

> [!div class="checklist"]
> + Have been [created before April 3, 2024](#check-your-service-creation-or-upgrade-date). Services created after this date should already have higher capacity.
> + Be in a [region where higher capacity is enabled](search-limits-quotas-capacity.md#partition-storage-gb). Most regions provide higher-capacity partitions, as noted in the table's footnotes.
> + Be in a [region that doesn't have capacity constraints on your pricing tier](search-region-support.md). Constrained regions and tiers are noted in the footnotes of each table.

> [!IMPORTANT]
> Some search services created before January 1, 2019 don't support upgrades. In this situation, you must create a new service in a [high-capacity region](search-limits-quotas-capacity.md#partition-storage-gb) to get increased storage and vector limits.

### Higher storage limits

For [eligible services](#upgrade-eligibility), the following table compares the storage limit (per partition) before and after an upgrade.

| | Basic <sup>1</sup> | S1 | S2 | S3/HD | L1 | L2 |
|-|-|-|-|-|-|-|
| **Limit before upgrade** | 2 GB | 25 GB | 100 GB | 200 GB | 1 TB | 2 TB |
| **Limit after upgrade** | 15 GB | 160 GB | 512 GB | 1 TB | 2 TB | 4 TB |

<sup>1</sup> Basic services created before April 3, 2024 were originally limited to one partition, which increases to three partitions after an upgrade. [Partition counts for all other pricing tiers](search-limits-quotas-capacity.md#service-limits) stay the same.

### Higher vector limits

For [eligible services](#upgrade-eligibility), the following table compares the vector index size (per partition) before and after an upgrade.

| | Basic | S1 | S2 | S3/HD | L1 | L2 |
|-|-|-|-|-|-|-|
| **Limit before upgrade** | 0.5 GB <sup>1</sup> or 1 GB <sup>2</sup> | 1 GB <sup>1</sup> or 3 GB <sup>2</sup> | 6 GB <sup>1</sup> or 12 GB <sup>2</sup> | 12 GB <sup>1</sup> or 36 GB <sup>2</sup> | 12 GB | 36 GB |
| **Limit after upgrade** | 5 GB | 35 GB | 150 GB | 300 GB | 150 GB | 300 GB |

<sup>1</sup> Applies to services created before July 1, 2023.

<sup>2</sup> Applies to services created between July 1, 2023 and April 3, 2024 in all regions except Germany West Central, Qatar Central, and West India, to which the <sup>1</sup> limits apply.

## Check your service creation or upgrade date

On the **Overview** page, you can view various metadata about your search service, including **Date created** and **Date upgraded**.

:::image type="content" source="media/search-how-to-upgrade/service-created-upgraded-metadata.png" alt-text="Screenshot of the service creation and service upgrade dates in the Azure portal." border="true" lightbox="media/search-how-to-upgrade/service-created-upgraded-metadata.png":::

The date you created your service partially determines its [upgrade eligibility](#upgrade-eligibility). If your service has never been upgraded, **Date upgraded** doesn't appear.

## Upgrade your service

You can't undo a service upgrade. Before you proceed, make sure that you want to permanently increase the [storage limit](#higher-storage-limits) and [vector index size](#higher-vector-limits) of your search service. We recommend that you test this operation in a nonproduction environment.

The availability of your search service during an upgrade depends on how many replicas you've provisioned. With two or more replicas, your service remains available while one replica is updated. For more information, see [Reliability in Azure AI Search](/azure/reliability/reliability-ai-search).

To upgrade your service:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Upgrade** from the command bar.

   :::image type="content" source="media/search-how-to-upgrade/upgrade-button.png" alt-text="Screenshot of the Upgrade button on the command bar in the Azure portal." border="true" lightbox="media/search-how-to-upgrade/upgrade-button.png":::

   If this button appears dimmed, an upgrade isn’t available for your service. Your service either [has the latest upgrade](#check-your-service-creation-or-upgrade-date) or [doesn't qualify for an upgrade](#upgrade-eligibility).

1. Review the upgrade details for your service, and then select **Upgrade**.

   :::image type="content" source="media/search-how-to-upgrade/upgrade-panel.png" alt-text="Screenshot of your service upgrade details in the Azure portal." border="true" lightbox="media/search-how-to-upgrade/upgrade-panel.png":::

   A confirmation appears reminding you that the upgrade can't be undone.

1. To permanently upgrade your service, select **Upgrade**.

   :::image type="content" source="media/search-how-to-upgrade/upgrade-confirmation.png" alt-text="Screenshot of the upgrade confirmation in the Azure portal." border="true" lightbox="media/search-how-to-upgrade/upgrade-confirmation.png":::

1. Check your notifications to confirm that the operation started.

   Depending on the size of your service, this operation can take several hours to complete. If the upgrade fails, your service returns to its original state.

## Next step

After you upgrade your search service, you might want to reconsider your scale configuration:

> [!div class="nextstepaction"]
> [Estimate and manage capacity of an Azure AI Search service](search-capacity-planning.md)
