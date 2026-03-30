---
title: "Manage and increase quotas for resources (classic)"
description: "Learn how to view, manage, and request increases for model deployment quotas in Microsoft Foundry, including token-per-minute and provisioned throughput allocations. (classic)"
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - classic-and-new
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 02/20/2026
ms.reviewer: haakar
reviewer: haakar
ms.author: mopeakande
author: msakande 
manager: nitinme
ai-usage: ai-assisted
# Customer intent: As a Microsoft Foundry user, I want to know how to manage and increase quotas for resources with Microsoft Foundry.
ROBOTS: NOINDEX, NOFOLLOW
---

# Manage and increase quotas for resources with Microsoft Foundry (Foundry projects) (classic)

**Currently viewing:** :::image type="icon" source="../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../foundry/how-to/quota.md)

> [!TIP]
> An alternate hub-focused quota article is available: [Manage and increase quotas for hub resources](hub-quota.md).

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. Azure assigns quota per subscription, per region, and per model in units of tokens per minute (TPM). Different deployment types, such as Standard and Provisioned, have different quota mechanics. For full details on default limits and quota tiers, see [Azure OpenAI quotas and limits](../openai/quotas-limits.md).

This article walks through the process of managing quota for your Microsoft Foundry Models deployed in a Foundry project, including how to view current allocations and request increases.

[!INCLUDE [quota 1](../../foundry/includes/how-to-quota-1.md)]

## View and request quotas in Foundry portal

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../../foundry/includes/fdp-project-name.md)]s in the same subscription.

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]

1. Select **Management center** from the bottom of the left pane.

    :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Select **Quota** from the left pane to open the quota view, where you can see the quota for the models in specific Azure regions.

    :::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the quota entry in the management center section." lightbox="../media/cost-management/quotas.png":::

1. To request quota from the quota view, expand any of the groupings listed in the deployment column until you see the model deployments and their associated information.
 
    :::image type="content" source="../media/cost-management/project-model-quota.png" alt-text="Screenshot of the Model quota page for a Foundry project in Foundry portal, with one of the groupings expanded." lightbox="../media/cost-management/project-model-quota.png":::

    - Use the **Show all quota** toggle to display all quota or only the currently allocated quota.
    - Use the **Group by** dropdown to group the list by **Quota type, Region & Model**, or **Quota type, Model & Region**, or **None**. The **None** option displays a flat list of model deployments, rather than a nested list.
    - On the line entry for a given model deployment, select the **pencil icon** in the **Quota allocation** column to edit the quota allocation for the model deployment. 
    - Select **Request quota** in the **Request quota** column to request increases in quota for the standard deployment type.
    - Use the **charts** along the side of the page to view more details about quota usage. The charts are interactive; hovering over a section of the chart displays more information, and selecting the chart filters the list of models. Selecting the chart legend filters the data displayed in the chart.
    - Use the **Provisioned Throughput** link to view information about provisioned models, including a **Capacity calculator** that you can use to estimate the number of PTUs needed for your workload.

> [!NOTE]
> After you edit a quota allocation or submit a request, allow up to 15 minutes for changes to propagate. Refresh the **Quota** page to verify the updated allocation.

[!INCLUDE [quota 2](../../foundry/includes/how-to-quota-2.md)]

## Related content

- [Microsoft Foundry Models quotas and limits](../foundry-models/quotas-limits.md)
- [Azure OpenAI quotas and limits](../openai/quotas-limits.md)
- [Manage Azure OpenAI Service quota](../openai/how-to/quota.md)
- [Manage and increase quotas for hub resources](hub-quota.md)
- [Plan to manage costs](./costs-plan-manage.md)
- [Create a project](../how-to/create-projects.md)
