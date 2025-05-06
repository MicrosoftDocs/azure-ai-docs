---
title: Management center overview
titleSuffix: Azure AI Foundry
description: "The management center in Azure AI Foundry portal provides a centralized hub for governance and management activities."
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: concept-article #Don't change.
ms.date: 02/13/2025
zone_pivot_groups: project-type
#customer intent: As an admin, I want a central location where I can perform governance and management activities.
---

# Management center overview

::: zone pivot="hub-project"

The management center is a part of the Azure AI Foundry portal that streamlines governance and management activities. From the management center, you can manage Azure AI Foundry hubs, [!INCLUDE [hub](../includes/hub-project-name.md)], resources, and settings. To visit the management center, open the [Azure AI Foundry](https://ai.azure.com) and (while in a hub or [!INCLUDE [hub](../includes/hub-project-name.md)]) select the __Management center__ link from the bottom of the left menu.

::: zone-end

::: zone pivot="fdp-project"

The management center is a part of the Azure AI Foundry portal that streamlines governance and management activities. From the management center, you can manage Azure AI Foundry [!INCLUDE [FDP](../includes/fdp-project-name.md)], resources, and settings. To visit the management center, open the [Azure AI Foundry](https://ai.azure.com) and (while in a [!INCLUDE [FDP](../includes/fdp-project-name.md)]) select the __Management center__ link from the bottom of the left menu.

::: zone-end

:::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the left menu of Azure AI Foundry with the management center selected." lightbox="../media/management-center/management-center.png":::

::: zone pivot="hub-project"

## Manage hubs and hub based projects

You can use the management center to configure hubs and hub based projects. Use __All resources__ to view all hubs and projects that you have access to. Use the __Hub__ and __Project__ sections of the left menu to manage individual hubs and projects.

:::image type="content" source="../media/management-center/manage-hub-project.png" alt-text="Screenshot of the all resources, hub, and project sections of the management studio selected." lightbox="../media/management-center/manage-hub-project.png":::

For more information, see the articles on creating a [hub](../how-to/create-azure-ai-resource.md#create-a-hub-in-azure-ai-foundry-portal) and [hub based project](../how-to/create-projects.md?pivots=hub-project).

::: zone-end

::: zone pivot="fdp-project"

## Manage Foundry projects

You can use the management center to create and configure [!INCLUDE [FDP](../includes/fdp-project-name.md)]s. Use __All resources__ to view all [!INCLUDE [FDP](../includes/fdp-project-name.md)] that you have access to. Use the __Project__ section of the left menu to manage individual [!INCLUDE [FDP](../includes/fdp-project-name.md)].

For more information, see the [Create a project in Azure AI Foundry](../how-to/create-projects.md?pivots=fdp-project) article.

::: zone-end

## Manage resource utilization

You can view and manage quotas and usage metrics across multiple projects and Azure subscriptions. Use the __Quota__ link from the left menu to view and manage quotas.

:::image type="content" source="../media/management-center/quotas.png" alt-text="Screenshot of the quotas section of the management center." lightbox="../media/management-center/quotas.png":::

For more information, see [Manage and increase quotas for resources](../how-to/quota.md).

## Govern access

Assign roles, manage users, and ensure that all settings comply with organizational standards.

:::image type="content" source="../media/management-center/user-management.png" alt-text="Screenshot of the user management section of the management center." lightbox="../media/management-center/user-management.png":::

For more information, see [Role-based access control](rbac-azure-ai-foundry.md#assigning-roles-in-azure-ai-foundry-portal).

## Related content

- [Security baseline](/security/benchmark/azure/baselines/azure-ai-studio-security-baseline)
- [Built-in policy to allow specific models](../how-to/built-in-policy-model-deployment.md)
- [Custom policy to allow specific models](../model-inference/how-to/configure-deployment-policies.md)
