---
title: Manage projects and resources
titleSuffix: Azure AI Foundry
description: "The management center in Azure AI Foundry portal provides a centralized hub for governance and management activities."
ms.author: sgilley
author: sdgilley
ms.reviewer: aashishb
ms.service: azure-ai-foundry
ms.custom:
  - ignite-2024
ms.topic: how-to
ms.date: 10/31/2025
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
#customer intent: As an admin, I want a central location where I can perform governance and management activities.
---

# Manage projects and resources

[!INCLUDE [version-banner](../includes/version-banner.md)]

:::moniker range="foundry-classic"

The management center is part of the Azure AI Foundry portal that streamlines governance and management activities. From the management center, you can manage:

- Azure AI Foundry hubs and [!INCLUDE [hub](../includes/hub-project-name.md)]s
- Azure AI [!INCLUDE [FDP](../includes/fdp-project-name.md)]s
- Quotas for models and virtual machines (VMs)

    > [!NOTE]
    > VMs and VM quotas are only available for [!INCLUDE [hub](../includes/hub-project-name.md)]s.

- User management and role assignment

To access the management center, sign in to [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs), select a project, then select **Management center** from the bottom of left menu. (You might have to scroll down to find it.)

:::image type="content" source="../media/management-center/management-center.png" alt-text="Screenshot of the left menu of Azure AI Foundry with the management center selected." :::


## Manage Foundry projects

Use the management center to create and configure [!INCLUDE [FDP](../includes/fdp-project-name.md)]s. Use **All resources** to view all [!INCLUDE [FDP](../includes/fdp-project-name.md)]s that you have access to, or to create new projects. Use the **Project** section of the left menu to manage and create individual [!INCLUDE [FDP](../includes/fdp-project-name.md)] on the AI Foundry resource.

:::image type="content" source="../media/management-center/project-management.png" alt-text="Screenshot of the all resources, hub, and project sections of the management studio selected." lightbox="../media/management-center/project-management.png":::

For more information, see [Create a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)]](../how-to/create-projects.md).


### Manage Azure AI Foundry hubs and hub-based projects

You can also manage [!INCLUDE [hub](../includes/hub-project-name.md)]s from the management center. The management center lists them in the **All resources** section. When you select a hub, the portal displays it in the left menu.

For more information, see [Create a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]](../how-to/hub-create-projects.md).

## Manage resource utilization

View and manage quotas and usage metrics across multiple projects and Azure subscriptions. Use the **Quota** link from the left menu to view and manage quotas.

:::image type="content" source="../media/management-center/quotas.png" alt-text="Screenshot of the quotas section of the management center." lightbox="../media/management-center/quotas.png":::

For more information, see [Manage and increase quotas for resources](../how-to/quota.md).

:::moniker-end

:::moniker range="foundry"

[!INCLUDE [foundry-link](../default/includes/foundry-link.md)] provides project management capabilities that streamline how you work with Foundry projects. You can switch between projects, manage project settings, and govern access to resources. 

## Prerequisites

* One or more [Foundry projects](../how-to/create-projects.md).

## Switch projects

In the Azure AI Foundry (new) portal, the project you're working with appears in the upper-left corner.  
1. [!INCLUDE [foundry-sign-in](../default/includes/foundry-sign-in.md)]
1. To switch to another recently used project, select the project name in the upper-left corner, then select the other project. 
1. To see all of your Foundry projects, select **View all projects**. Then select one of them to switch to that project.

## Find other resources

The Azure AI Foundry (new) portal displays only Foundry projects, not other resources or hub-based projects you might have created in [!INCLUDE [classic-link](../includes/classic-link.md)]. 

To find these other resources, select **View all resources**.  A new browser tab opens the Azure AI Foundry (classic) portal.  [Switch to Azure AI Foundry (classic) documentation](?view=foundry-classic&preserve-view=true) to work with these other resources in the Azure AI Foundry (classic) portal.

## Manage projects

Most of your work in the Azure AI Foundry (new) portal is performed in the context of the project shown in the upper-left corner. But when you navigate to the **Operate** section, the project name disappears. This section allows you to view and manage all of your Foundry projects.

1. [!INCLUDE [foundry-sign-in](../default/includes/foundry-sign-in.md)]
1. Select **Operate** in the upper-right navigation.
1. Select **Admin** in the left pane.

The **All projects** tab lists all of your Foundry projects.  From here you can:

* View quick information about a project by selecting the radio button next to a row in the table.  
* Add users or connected resources to a project by selecting the project link in the first column. 
* Add users or connected resources to a parent resource by selecting the parent resource link in the second column. 

## Manage in Azure portal

To delete a resource or project, or for more management activities, open the Azure portal from the parent resource:

1. [!INCLUDE [foundry-sign-in](../default/includes/foundry-sign-in.md)]
1. Select **Operate** in the upper-right navigation.
1. Select **Admin** in the left pane.
1. Select the parent resource link for your project in the second column.
1. Select the link **Manage this resource in the Azure portal** to open the Azure portal for the resource.


::: moniker-end

## Govern access

:::moniker range="foundry-classic"

With a project selected, use the __Users__ entry in the left menu to view and manage users and their roles.

:::moniker-end
:::moniker range="foundry"

After you select a project or parent resource link, use the __Users__ tab to view and manage users and their roles.

:::moniker-end

> [!NOTE]
> You can only assign built-in roles for Azure AI Foundry here.

For more information, see [Role-based access control](rbac-azure-ai-foundry.md#azure-ai-foundry-project-roles).

## Connect resources

For more information about connections, see [Add a new connection to your project](../how-to/connections-add.md).

## Related content

- [Security baseline](/security/benchmark/azure/baselines/azure-ai-foundry-security-baseline)
- [Built-in policy to allow specific models](../how-to/built-in-policy-model-deployment.md)
- [Custom policy to allow specific models](../model-inference/how-to/configure-deployment-policies.md)
