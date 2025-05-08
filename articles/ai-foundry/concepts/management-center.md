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
ms.date: 05/07/2025
#customer intent: As an admin, I want a central location where I can perform governance and management activities.
---

# Management center overview

The management center is a part of the Azure AI Foundry portal that streamlines governance and management activities. From the management center, you can manage:

- Azure AI Foundry hubs and [!INCLUDE [hub](../includes/hub-project-name.md)]s
- Azure AI [!INCLUDE [FDP](../includes/fdp-project-name.md)]s
- Quotas for models and virtual machines (VMs)

    > [!NOTE]
    > VM quotas are only available for [!INCLUDE [hub](../includes/hub-project-name.md)]s.

- User management and role assignment

To access the management center, sign in to [Azure AI Foundry](https://ai.azure.com), select a project, and then select **Management center** from the bottom of left menu.

:::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the left menu of Azure AI Foundry with the management center selected." lightbox="../media/management-center/management-center.png":::

## Manage Foundry projects

You can use the management center to create and configure [!INCLUDE [FDP](../includes/fdp-project-name.md)]s. Use __All resources__ to view all [!INCLUDE [FDP](../includes/fdp-project-name.md)]s that you have access to, or to create new projects. Use the __Project__ section of the left menu to manage individual [!INCLUDE [FDP](../includes/fdp-project-name.md)].

:::image type="content" source="../media/management-center/project-management.png" alt-text="Screenshot of the all resources, hub, and project sections of the management studio selected." lightbox="../media/management-center/project-management.png":::

### Manage Azure AI Foundry hubs and hub based projects

You can also manage [!INCLUDE [hub](../includes/hub-project-name.md)]s from the management center. They're listed in the __All resources__ section, and when selected are displayed in the left menu.

For more information, see the following articles:

- [Create a project in Azure AI Foundry](../how-to/create-projects.md?pivots=fdp-project)
- [Create a hub based project](../how-to/create-projects.md?pivots=hub-project)

## Manage resource utilization

You can view and manage quotas and usage metrics across multiple projects and Azure subscriptions. Use the __Quota__ link from the left menu to view and manage quotas.

:::image type="content" source="../media/management-center/quotas.png" alt-text="Screenshot of the quotas section of the management center." lightbox="../media/management-center/quotas.png":::

For more information, see [Manage and increase quotas for resources](../how-to/quota.md).

## Govern access

With a project selected, you can use the __Users__ entry in the left menu to view and manage users and their roles.

> [!NOTE]
> You can only assign built-in roles for Azure AI Foundry in the management center.

For more information, see [Role-based access control](rbac-azure-ai-foundry.md#assigning-roles-in-azure-ai-foundry-portal).

## Related content

- [Security baseline](/security/benchmark/azure/baselines/azure-ai-studio-security-baseline)
- [Built-in policy to allow specific models](../how-to/built-in-policy-model-deployment.md)
- [Custom policy to allow specific models](../model-inference/how-to/configure-deployment-policies.md)
