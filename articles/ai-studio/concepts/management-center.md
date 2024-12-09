---
title: Management center overview
titleSuffix: Azure AI Foundry
description: "The management center in Azure AI Foundry portal provides a centralized hub for governance and management activities."
author: Blackmist
ms.author: larryfr
ms.service: azure-ai-studio
ms.custom:
  - ignite-2024
ms.topic: concept-article #Don't change.
ms.date: 11/18/2024
#customer intent: As an admin, I want a central location where I can perform governance and management activities.
---

# Management center overview

The management center is a part of the Azure AI Foundry portal that streamlines governance and management activities. From the management center, you can manage Azure AI Foundry hubs, projects, resources, and settings. To visit the management center, open the [Azure AI Foundry](https://ai.azure.com) and (while in a project) select the __Management center__ link from the left menu.

:::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the left menu of Azure AI Foundry with the management center selected." lightbox="../media/management-center/management-center.png":::

## Manage hubs and projects

You can use the management center to create and configure hubs and projects within those hubs. Use __All resources__ to view all hubs and projects that you have access to. Use the __Hub__ and __Project__ sections of the left menu to manage individual hubs and projects.

:::image type="content" source="../media/management-center/manage-hub-project.png" alt-text="Screenshot of the all resources, hub, and project sections of the management studio selected." lightbox="../media/management-center/manage-hub-project.png":::

For more information, see the articles on creating a [hub](../how-to/create-azure-ai-resource.md#create-a-hub-in-ai-foundry-portal) and [project](../how-to/create-projects.md).

## Manage resource utilization

You can view and manage quotas and usage metrics across multiple hubs and Azure subscriptions. Use the __Quota__ link from the left menu to view and manage quotas.

:::image type="content" source="../media/management-center/quotas.png" alt-text="Screenshot of the quotas section of the management center." lightbox="../media/management-center/quotas.png":::

For more information, see [Manage and increase quotas for resources](../how-to/quota.md).

## Govern access

Assign roles, manage users, and ensure that all settings comply with organizational standards.

:::image type="content" source="../media/management-center/user-management.png" alt-text="Screenshot of the user management section of the management center." lightbox="../media/management-center/user-management.png":::

For more information, see [Role-based access control](rbac-ai-studio.md#assigning-roles-in-ai-foundry-portal).

## Related content

- [Security baseline](/security/benchmark/azure/baselines/azure-ai-studio-security-baseline)
- [Built-in policy to allow specific models](../how-to/built-in-policy-model-deployment.md)
- [Custom policy to allow specific models](../how-to/custom-policy-model-deployment.md)
