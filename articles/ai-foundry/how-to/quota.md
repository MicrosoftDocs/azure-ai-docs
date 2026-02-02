---
title: Manage and increase quotas for resources
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to manage and increase quotas for resources with Azure AI Foundry.
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: how-to
ms.date: 09/22/2025
ms.reviewer: haakar
reviewer: haakar
ms.author: mopeakande
author: msakande 
manager: nitinme
ai-usage: ai-assisted
# Customer intent: As an Azure AI Foundry user, I want to know how to manage and increase quotas for resources with Azure AI Foundry.
---

# Manage and increase quotas for resources with Azure AI Foundry (Foundry projects)

> [!NOTE]
> An alternate hub-focused quota article is available: [Manage and increase quotas for hub resources](hub-quota.md).

Quota provides the flexibility to actively manage the allocation of rate limits across the deployments within your subscription. This article walks through the process of managing quota for your Azure AI Foundry Models (Foundry projects). Hub-level quota guidance has moved to `hub-quota.md`.

Azure uses limits and quotas to prevent budget overruns due to fraud, and to honor Azure capacity constraints. It's also a good way to control costs for admins. Consider these limits as you scale for production workloads. 

In this article, you learn about: 

- Viewing your quotas and limits 
- Requesting quota and limit increases 

## Azure AI Foundry shared quota 

Azure AI Foundry provides a pool of shared quota that is available for different users across various regions to use concurrently. Depending upon availability, users can temporarily access quota from the shared pool and use the quota to perform testing for a limited amount of time. The specific time duration depends on the use case. By temporarily using quota from the quota pool, you no longer need to file a support ticket for a short-term quota increase or wait for your quota request to be approved before you can proceed with your workload. 

Use of the shared quota pool is available for testing inferencing for Foundry Models from the model catalog. You should use the shared quota only for creating temporary test endpoints, not production endpoints. For endpoints in production, you should [request dedicated quota](#view-and-request-quotas-in-azure-ai-foundry-portal). Billing for shared quota is usage-based. 

## View and request quotas in Azure AI Foundry portal
Use quotas to manage model quota allocation between multiple [!INCLUDE [fdp](../includes/fdp-project-name.md)]s in the same subscription.

1. In Azure AI Foundry portal, select **Management center** from the bottom of the left menu.

    :::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the management center link.":::

1. Select **Quota** from the left menu to open the quota view, where you can see the quota for the models in specific Azure regions.

    :::image type="content" source="../media/cost-management/quotas.png" alt-text="Screenshot of the quota entry in the management center section." lightbox="../media/cost-management/quotas.png":::

1. To request quota from the quota view, expand any of the groupings listed in the deployment column until you see the model deployments and their associated information.
 
    :::image type="content" source="../media/cost-management/project-model-quota.png" alt-text="Screenshot of the Model quota page for a Foundry project in Azure AI Foundry portal, with one of the groupings expanded." lightbox="../media/cost-management/project-model-quota.png":::

    - Use the **Show all quota** toggle to display all quota or only the currently allocated quota.
    - Use the **Group by** dropdown to group the list by **Quota type, Region & Model**, or **Quota type, Model & Region**, or **None**. The **None** option displays a flat list of model deployments, rather than a nested list.
    - On the line entry for a given model deployment, select the **pencil icon** in the **Quota allocation** column to edit the quota allocation for the model deployment. 
    - Select **Request quota** in the **Request quota** column to request increases in quota for the standard deployment type.
    - Use the **charts** along the side of the page to view more details about quota usage. The charts are interactive; hovering over a section of the chart displays more information, and selecting the chart filters the list of models. Selecting the chart legend filters the data displayed in the chart.
    - Use the **Provisioned Throughput** link to view information about provisioned models, including a **Capacity calculator** that you can use to estimate the number of PTUs needed for your workload.

## Related content
 
- [Plan to manage costs](./costs-plan-manage.md)
- [Create a project](../how-to/create-projects.md)