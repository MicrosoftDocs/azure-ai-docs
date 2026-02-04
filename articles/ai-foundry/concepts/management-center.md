---
title: Management center overview
titleSuffix: Microsoft Foundry
description: "The management center in Microsoft Foundry portal provides a centralized hub for governance and management activities."
ms.author: sgilley
author: sdgilley
ms.reviewer: aashishb
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
  - dev-focus
ms.topic: concept-article
ms.date: 01/23/2026
ai-usage: ai-assisted
#customer intent: As an admin, I want a central location where I can perform governance and management activities.
---

# Management center overview

[!INCLUDE [classic-banner](../includes/classic-banner.md)]

The management center is part of the Microsoft Foundry portal that streamlines governance and management activities. From the management center, you can manage:

- Foundry hubs and [!INCLUDE [hub](../includes/hub-project-name.md)]s
- Azure AI [!INCLUDE [FDP](../includes/fdp-project-name.md)]s
- Quotas for models and virtual machines (VMs)

    > [!NOTE]
    > VMs and VM quotas are only available for [!INCLUDE [hub](../includes/hub-project-name.md)]s.

- User management and role assignment

To access the management center, sign in to [Foundry](https://ai.azure.com/?cid=learnDocs), select a project, and then select **Management center** from the bottom of the left menu. (You might have to scroll down to find it.)

:::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the left menu of Foundry with the management center selected." :::


## Manage Foundry projects

Use the management center to create and configure [!INCLUDE [FDP](../includes/fdp-project-name.md)]s. Use **All resources** to view all [!INCLUDE [FDP](../includes/fdp-project-name.md)]s that you have access to, or to create new projects. Use the **Project** section (Project = Foundry project) of the left menu to manage and create individual [!INCLUDE [FDP](../includes/fdp-project-name.md)]s on the Foundry resource.

:::image type="content" source="../media/management-center/project-management.png" alt-text="Screenshot of the all resources, hub, and project sections of the management studio selected." lightbox="../media/management-center/project-management.png":::

For more information, see [Create a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]](../how-to/create-projects.md).


### Manage Foundry hubs and hub-based projects

You can also manage [!INCLUDE [hub](../includes/hub-project-name.md)]s from the management center. The management center lists them in the **All resources** section. When you select a hub, the portal displays it in the left menu.

For more information, see [Create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]](../how-to/hub-create-projects.md).

## Manage resource utilization

View and manage quotas and usage metrics across multiple projects and Azure subscriptions. Use the **Quota** link from the left menu to view and manage quotas. VM quotas apply to hub-based projects only.

:::image type="content" source="../media/management-center/quotas.png" alt-text="Screenshot of the quotas section of the management center." lightbox="../media/management-center/quotas.png":::

For more information, see [Manage and increase quotas for resources](../how-to/quota.md).

## Govern access

With a project selected, use the __Users__ entry in the left menu to view and manage users and their roles.

> [!NOTE]
> You can only assign built-in roles for Foundry here.

For more information, see [Role-based access control](rbac-foundry.md#built-in-roles).

## Related content

- [Add a new connection to your project](../how-to/connections-add.md)
- [Security baseline](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)
- [Built-in policy to allow specific models](../how-to/built-in-policy-model-deployment.md)
- [Custom policy to allow specific models](../foundry-models/how-to/configure-deployment-policies.md)