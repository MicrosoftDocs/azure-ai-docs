---
title: Service Upgrade in the Azure Portal
titleSuffix: Azure AI Search
description: Learn how to upgrade your existing Azure AI Search service to the version available to new services in your region.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 03/19/2025
---

# Upgrade your Azure AI Search service in the Azure portal

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In April 2024, Azure AI Search increased the [storage capacity](search-limits-quotas-capacity.md#service-limits) of newly created search services. Services created before April 2024 saw no capacity changes, so if you wanted larger and faster partitions, you had to create a new service. However, most older services can now be upgraded to benefit from the higher capacity partitions.

<a id="upgrade-eligibility"></a>

To qualify for an upgrade, your service:

> [!div class="checklist"]
> + Must have been created before April 2024. Services created after April 2024 should already have higher capacity. To see when you created your service, [check your service version](#check-your-service-version).
> + Must be in a region that supports higher capacity. Check the footnotes in the [list of supported regions](search-region-support.md).

This article describes how to upgrade your service in the [Azure portal](https://portal.azure.com/). Alternatively, you can use the Search REST APIs to upgrade your service programmatically. For more information, see [Manage your search service with REST](search-manage-rest.md).

## About service upgrades

An upgrade brings your existing search service to the same configuration as new services in your region. Unlike [upgrading your API version](search-api-migration.md), upgrading your service doesn’t introduce new features. Rather, it brings feature enhancements that are only available to new services in your region. Your service is never out of date, and regardless of your service version, you receive code and security updates every month.

In this preview, an upgrade only increases the [storage limit](#higher-storage-limits) and [vector limit](#higher-vector-limits) of your service. Expect more upgrade capabilities in the future.

> [!IMPORTANT]
> An upgrade is permanent and can’t be undone. Before you upgrade your service, carefully consider your current and future storage needs.

### Higher storage limits

For [upgrade-eligible services](#upgrade-eligibility), the following table compares the storage limit (per partition) before and after an upgrade.

| | Basic <sup>1</sup> | S1 | S2 | S3/HD | L1 | L2 |
|-|-|-|-|-|-|-|
| **Limit before upgrade** | 2 GB | 25 GB | 100 GB | 200 GB | 1 TB | 2 TB |
| **Limit after upgrade** | 15 GB | 160 GB | 512 GB | 1 TB | 2 TB | 4 TB |

<sup>1</sup> Basic services created before April 3, 2024 were originally limited to one partition, which increases to three partitions after an upgrade. [Partition counts for all other service tiers](search-limits-quotas-capacity.md#service-limits) stay the same.

### Higher vector limits

For [upgrade-eligible services](#upgrade-eligibility), the following table compares the vector index size limit (per partition) before and after an upgrade.

| | Basic | S1 | S2 | S3/HD | L1 | L2 |
|-|-|-|-|-|-|-|
| **Limit before upgrade** | 0.5 GB <sup>1</sup> or 1 GB <sup>2</sup> | 1 GB <sup>1</sup> or 3 GB <sup>2</sup> | 6 GB <sup>1</sup> or 12 GB <sup>2</sup> | 12 GB <sup>1</sup> or 36 GB <sup>2</sup> | 12 GB | 36 GB |
| **Limit after upgrade** | 5 GB | 35 GB | 150 GB | 300 GB | 150 GB | 300 GB |

<sup>1</sup> Applies to services created before July 1, 2023.

<sup>2</sup> Applies to services created between July 1, 2023 and April 3, 2024 in all regions except Germany West Central, Qatar Central, and West India, to which the <sup>1</sup> limits apply.

## Check your service version

On the **Overview** page, you can view various metadata about your search service, including the **Service Version**. This is the date you created or last upgraded your service, whichever is most recent.

If a new version is available for services in your region, the **Upgrade** button becomes available. Otherwise, the button appears dimmed.

## Upgrade your service

You can’t undo a service upgrade. Before you proceed, be sure that you want to permanently increase the [storage limit](#higher-storage-limits) and [vector limit](#higher-vector-limits) of your search service. We recommend that you test this operation in a nonproduction environment.

To upgrade your service:

1. Go to your search service in the [Azure portal](https://portal.azure.com/).

1. On the **Overview** page, select **Upgrade** from the command bar.

   If this button appears dimmed, an upgrade isn’t available for your service. Your service is either [on the current version](#check-your-service-version) or [in an unsupported region](search-region-support.md).

1. Review the upgrade details for your service, including your service name and service version.

1. To permanently upgrade your service, select **Upgrade**.

1. Check your notifications to confirm that the operation started.

   The upgrade is an asynchronous operation, so you can continue using your service. Depending on the size of your service, the upgrade can take several hours to complete.

## Next step

After you upgrade your search service, you might have more partitions or be on a higher service tier than you need. To reduce costs, consider scaling your service down:

> [!div class="nextstepaction"]
> [Estimate and manage capacity of your Azure AI Search service](search-capacity-planning.md)
