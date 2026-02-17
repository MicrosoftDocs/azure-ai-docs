---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/03/2025
ms.custom: include, build-2024, ignite-2024
---

[!INCLUDE [create-hub-project-simple](create-hub-project-simple.md)]

Or, if you want to customize a new hub, follow the steps in the next section before you select **Create**.

### Customize the hub

A [!INCLUDE [hub-project-name](hub-project-name.md)] exists inside a hub. A hub allows you to share configurations like data connections with all projects, and to centrally manage security settings and spend. If you're part of a team, hubs are shared across other team members in your subscription. For more information about the relationship between hubs and projects, see the [hubs and projects overview](../concepts/ai-resources.md) documentation.

When you create a new hub, you must have **Owner** or **Contributor** permissions on the selected resource group. If you're part of a team and don't have these permissions, your administrator should create a hub for you.

> [!TIP]
> While you can create a hub as part of the project creation, you have more control and can set more advanced settings for the hub if you create it separately. For example, you can customize network security or the underlying Azure Storage account. For more information, see [How to create and manage a Microsoft Foundry hub](../how-to/create-azure-ai-resource.md).

When you create a new hub as part of the project creation, default settings are provided. If you want to customize these settings, do so before you create the project:

1. In the **Create a project** form, select the arrow on the right side.

    :::image type="content" source="../media/how-to/projects/projects-customize-hub.png" alt-text="Screenshot of the customize button within the create project dialog." lightbox="../media/how-to/projects/projects-customize-hub.png":::

1. Select an existing **Resource group** you want to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started we recommend you create a new resource group for your project. The resource group allows you to easily manage the project and all of its resources together. When you create a project, several resources are created in the resource group, including a hub, a container registry, and a storage account.

1. Select a **Location** or use the default. The location is the region where the hub is hosted. The location of the hub is also the location of the project. Foundry Tools availability differs per region. For example, certain models might not be available in certain regions.

1. Select **Create a project**. You see progress of the resource creation. The project is created when the process is complete.