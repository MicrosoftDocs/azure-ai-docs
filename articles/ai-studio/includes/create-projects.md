---
title: include file
description: include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 11/19/2024
ms.custom: include, build-2024, ignite-2024
---

To create a project in [Azure AI Foundry](https://ai.azure.com), follow these steps:

1. Go to [Azure AI Foundry](https://ai.azure.com). If you are in a project, select **Azure AI Foundry** at the top left of the page to go to the **Home** page.
1. Select **+ Create project**.
1. Enter a name for the project.
1. If you have a hub, you'll see the one you most recently used selected.  
    * If you have access to more than one hub, you can select a different hub from the dropdown.
    * If you want to create a new one, select **Create new hub** and supply a  name.  If you want to customize the default values, see the next section.

        :::image type="content" source="../media/how-to/projects/projects-create-details.png" alt-text="Screenshot of the project details page within the create project dialog." lightbox="../media/how-to/projects/projects-create-details.png":::

1. If you don't have a hub, a default one is created for you.  If you want to customize the default values, see the next section.

1. Select **Create a project**.  Or, if you want to customize a new hub, follow the steps in the next section.

### Customize the hub

Projects live inside a hub. A hub allows you to share configurations like data connections with all projects, and to centrally manage security settings and spend. If you're part of a team, hubs are shared across other team members in your subscription. For more information about the relationship between hubs and projects, see the [hubs and projects overview](../concepts/ai-resources.md) documentation.

When you create a new hub, you must have **Owner** or **Contributor** permissions on the selected resource group. If you're part of a team and don't have these permissions, your administrator should create a hub for you.

While you can create a hub as part of the project creation, you have more control and can set more advanced settings for the hub if you create it separately. For example, you can customize network security or the underlying Azure Storage account. For more information, see [How to create and manage an Azure AI Foundry hub](../how-to/create-azure-ai-resource.md).

When you create a new hub as part of the project creation, default settings are provided. If you want to customize these settings, do so before you create the project:

1. In the **Create a project** form, select **Customize**.

    :::image type="content" source="../media/how-to/projects/projects-customize-hub.png" alt-text="Screenshot of the customize button within the create project dialog." lightbox="../media/how-to/projects/projects-customize-hub.png":::

1. Select an existing **Resource group** you want to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started it's recommended to create a new resource group for your project. This allows you to easily manage the project and all of its resources together. When you create a project, several resources are created in the resource group, including a hub, a container registry, and a storage account.

1. Select a **Location** or use the default. The location is the region where the hub is hosted. The location of the hub is also the location of the project. Azure AI services availability differs per region. For example, certain models might not be available in certain regions.
1. Select an existing Azure AI services resource (including Azure OpenAI) from the dropdown if you have one, or use the default to create a new resource.

    :::image type="content" source="../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../media/how-to/projects/projects-create-resource.png":::

1. Select **Create a project**. You see progress of resource creation and the project is created when the process is complete.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish-progress.png" alt-text="Screenshot of the resource creation progress within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish-progress.png":::
