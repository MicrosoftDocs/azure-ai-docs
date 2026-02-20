---
title: Manage and increase quotas for resources
titleSuffix: Microsoft Foundry
description: Learn how to view, manage, and request increases for model deployment quotas in Microsoft Foundry, including token-per-minute and provisioned throughput allocations.
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
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
---

# Manage and increase quotas for resources with Microsoft Foundry (Foundry projects)

[!INCLUDE [version-banner](../includes/version-banner.md)]

::: moniker range="foundry-classic"

> [!TIP]
> An alternate hub-focused quota article is available: [Manage and increase quotas for hub resources](hub-quota.md).

::: moniker-end

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. Azure assigns quota per subscription, per region, and per model in units of tokens per minute (TPM). Different deployment types, such as Standard and Provisioned, have different quota mechanics. For full details on default limits and quota tiers, see [Azure OpenAI quotas and limits](../openai/quotas-limits.md).

This article walks through the process of managing quota for your Microsoft Foundry Models deployed in a Foundry project, including how to view current allocations and request increases.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- A [Foundry project](../how-to/create-projects.md).
- **Cognitive Services Usages Reader** role at the subscription level, to view quota allocations.
- **Owner** or **Contributor** role on the subscription, to request quota increases.
- **Cognitive Services Contributor** role combined with **Cognitive Services Usages Reader**, to edit quota allocations in the Foundry portal.

## Foundry shared quota 

Foundry provides a pool of shared quota that different users across various regions can use concurrently. Depending on availability, users can temporarily access quota from the shared pool and use the quota to perform testing for a limited amount of time. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload. 

You can use the shared quota pool for testing inferencing for Foundry Models from the model catalog. Use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, you should [request dedicated quota](#view-and-request-quotas-in-foundry-portal). Billing for shared quota is usage-based. 

## View and request quotas in Foundry portal

Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../includes/fdp-project-name.md)]s in the same subscription.

::: moniker range="foundry-classic"

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

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
 
1. Projects help organize your work. The project you're working on appears in the upper-left corner. If you want to create a new project, select the project name, then **Create new project**.

1. Select **Operate** from the upper-right navigation.

1. Select **Quota** from the left pane to land on the **Quota** pane. The quota view has two tabs:

    - **Token per minute** — View and manage token-per-minute (TPM) quota allocations for standard deployments.
    - **Provisioned throughput unit** — View and manage provisioned throughput unit (PTU) allocations for provisioned deployments, including capacity estimation tools.

1. Select any of the deployments in the list to open its details pane on the right side. The details pane shows the deployment's current quota allocation, usage, and affiliated deployments.

1. On the deployment's details pane, go to the **Affiliated deployments using shared quota** section. Select the pencil icon in the **Actions** column of the table to edit quota allocation for the deployment and free up unused quota or increase allocation as needed.

1. Select the **Request quota** button in the upper-right corner to request increases in quota for the standard deployment type.

> [!NOTE]
> After you edit a quota allocation or submit a request, allow up to 15 minutes for changes to propagate. Refresh the **Quota** page to verify the updated allocation.

::: moniker-end

## Troubleshooting

If you encounter issues when viewing or requesting quotas, try these solutions:

| Issue | Solution |
| ----- | -------- |
| Quota page is empty or shows no allocations | Verify that you have **Cognitive Services Usages Reader** role at the subscription level. Check that you're viewing the correct subscription in the portal. |
| **Request quota** button is disabled | Verify that you have **Owner** or **Contributor** role on the subscription. Some model and region combinations might not support quota increases. |
| Quota change not reflected after approval | Quota changes can take up to 15 minutes to propagate. Refresh the **Quota** page. If the issue persists after 24 hours, contact [Azure support](https://azure.microsoft.com/support/options/). |
| Receiving 429 (Too Many Requests) errors despite having quota | Your deployment's allocated quota might be lower than the subscription-level quota. Edit the deployment's quota allocation by using the pencil icon. For rate-limit details, see [Azure OpenAI quotas and limits](../openai/quotas-limits.md). |
| Can't find quota for a specific model | Check regional availability. Not all models are available in all regions. See [Region support](../reference/region-support.md). |

## Related content

::: moniker range="foundry-classic"

- [Microsoft Foundry Models quotas and limits](../foundry-models/quotas-limits.md)
- [Azure OpenAI quotas and limits](../openai/quotas-limits.md)
- [Manage Azure OpenAI Service quota](../openai/how-to/quota.md)
- [Manage and increase quotas for hub resources](hub-quota.md)
- [Plan to manage costs](./costs-plan-manage.md)
- [Create a project](../how-to/create-projects.md)

::: moniker-end

::: moniker range="foundry"

- [Microsoft Foundry Models quotas and limits](../foundry-models/quotas-limits.md)
- [Azure OpenAI quotas and limits](../openai/quotas-limits.md)
- [Manage Azure OpenAI Service quota](../openai/how-to/quota.md)
- [Plan to manage costs](./costs-plan-manage.md)
- [Create a project](../how-to/create-projects.md)

::: moniker-end