---
title: Manage and increase quotas for hub resources
titleSuffix: Microsoft Foundry
description: Manage and increase quotas for hub-level resources in Microsoft Foundry.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
  - hub-only
ms.topic: how-to
ms.date: 09/22/2025
ms.reviewer: haakar
ms.author: mopeakande
author: msakande 
manager: nitinme
ai-usage: ai-assisted
# Hub-focused copy of quota article. Project (fdp) version remains in quota.md
---
# Manage and increase quotas for hub resources

> [!TIP]
> An alternate Foundry project-focused quota article is available: [Manage and increase quotas for resources with Microsoft Foundry](quota.md).

Quota provides flexibility to manage rate limits across deployments within your subscription. This article focuses on hub-level quotas (virtual machines and models) and how to view and request increases.

## Special considerations 

Quotas apply per subscription. Request increases separately for each subscription.

A quota is a credit limit, not a capacity guarantee. For large capacity needs, contact support.

> [!NOTE]
> Foundry compute has a separate quota from the core compute quota.

Default limits vary by offer category (free trial, serverless API deployment, VM series).

## Foundry quota 

The following actions in the portal consume quota: 

- Creating a compute instance.
- Building a vector index.
- Deploying open models from model catalog.

## Foundry compute 

[Foundry compute](./create-manage-compute.md) has default limits on cores and unique compute resources per region.

- Core quota split by VM family and cumulative total cores.
- Unique compute resources quota is separate.

To raise limits, [request a quota increase](#view-and-request-quotas-in-foundry-portal).

Available resources include:
- Dedicated cores per region default 24–300 (depends on subscription). Specialized GPU families may default to 0.
- Total compute limit per region default 500; increase up to 2500. Shared between compute instances and managed online endpoint deployments.

Support request steps to increase total compute limit:
1. Issue type: **Technical**.
1. Select subscription.
1. Service type: **Machine Learning**.
1. Select resource.
1. Summary: "Increase total compute limits".
1. Problem type: **Compute instance**; subtype: **Other features (Setup scripts, shutdown, Identity etc.)**.
1. Provide additional details and submit.

:::image type="content" source="../media/cost-management/quota-azure-portal-support.png" alt-text="Screenshot of the page to submit compute quota requests in Azure portal." lightbox="../media/cost-management/quota-azure-portal-support.png":::

## Foundry shared quota 

Shared quota provides a regional pool for temporary testing (for Foundry Models). Use only for temporary test endpoints; request dedicated quota for production. Billing is usage-based.

## Container Instances 

See [Container Instances limits](/azure/azure-resource-manager/management/azure-subscription-service-limits#container-instances-limits).

## Storage

Azure Storage limit: 250 storage accounts per region per subscription (Standard + Premium).

## View and request quotas in Foundry portal

Use quotas to manage compute and model quota across hubs in the same subscription. All hubs share subscription-level VM family quota by default. You can set max quota per VM family for granular governance.

1. In Foundry portal, select **Management center**.
1. Select **Quota**.

   :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Expand groupings to view model deployments and details.

:::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the quota entry in the management center section." lightbox="../media/cost-management/quotas.png":::

:::image type="content" source="../media/cost-management/model-quota.png" alt-text="Screenshot of the Model quota page in Foundry portal, with one of the groupings expanded." lightbox="../media/cost-management/model-quota.png":::
 
- **Show all quota** toggle displays all or allocated quota.
- **Group by** changes nesting (Quota type / Region / Model or flat view).
- Pencil icon edits allocation.
- **Request quota** link requests increases (standard deployments).
- Charts are interactive for usage insights.
- **Provisioned Throughput** link opens PTU info and capacity calculator.

**VM Quota** link: View per-region VM family quota and usage. Select a family then **Request quota** to ask for more.

> [!TIP]
> If the VM quota link is missing you were in a Foundry project view. Use **All resources** then select a hub-type project and return to **Management center**.

:::image type="content" source="../media/cost-management/vm-quota.png" alt-text="Screenshot of the VM quota page in Foundry portal." lightbox="../media/cost-management/vm-quota.png":::

## Related content

- [Manage and increase quotas for Foundry projects](./quota.md)
- [Plan to manage costs](./costs-plan-manage.md)
- [How to create compute](./create-manage-compute.md)
