---
title: Manage and increase quotas for resources
titleSuffix: Microsoft Foundry
description: This article provides instructions on how to manage and increase quotas for resources with Microsoft Foundry.
monikerRange: 'foundry-classic || foundry'
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 10/30/2025
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

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Microsoft Foundry Models (Foundry projects).

::: moniker-end

::: moniker range="foundry"

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Foundry Models (Foundry projects).

::: moniker-end

Azure uses limits and quotas to prevent budget overruns due to fraud and to honor Azure capacity constraints. It's also a good way for admins to control costs. Consider these limits as you scale for production workloads. 

In this article, you learn about: 

- Viewing your quotas and limits 
- Requesting quota and limit increases 

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

::: moniker-end

::: moniker range="foundry"

1. [!INCLUDE [version-sign-in](../includes/version-sign-in.md)]
 
1. Projects help organize your work. The project you're working on appears in the upper-left corner. If you want to create a new project, select the project name, then **Create new project**.

1. Select **Operate** from the upper-right navigation.

1. Select **Quota** from the left pane to land on the **Quota** pane. Here, you can view your quota on the **Token per minute** tab and view provisioned models on the **Provisioned throughput unit** tab. 

1. Select any of the deployments in the list to open its details pane on the right side. 

1. On the deployment's details pane, go to the **Affiliated deployments using shared quota** section. Select the pencil icon in the **Actions** column of the table to edit quota allocation for the deployment and free up unused quota or increase allocation as needed.

1. Select the **Request quota** button in the upper-right corner to request increases in quota for the standard deployment type.


::: moniker-end

## Related content

::: moniker range="foundry-classic"
 
- [Plan to manage costs](./costs-plan-manage.md)
- [Create a project](../how-to/create-projects.md)

::: moniker-end

::: moniker range="foundry"
 
- [Create a project](../how-to/create-projects.md)

::: moniker-end