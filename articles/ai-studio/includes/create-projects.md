---
title: include file
description: include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-studio
ms.topic: include
ms.date: 5/21/2024
ms.custom: include, build-2024
---

To create a project in [Azure AI Studio](https://ai.azure.com), follow these steps:

1. Go to the **Home** page of [Azure AI Studio](https://ai.azure.com). If you are in a project, select **Azure AI Studio** at the top left of the page to go to the **Home** page.
1. Select **+ New project**.
1. Enter a name for the project.
1. Select a hub if you have one, or select **Create new hub** and supply a name.

    :::image type="content" source="../media/how-to/projects/projects-create-details.png" alt-text="Screenshot of the project details page within the create project dialog." lightbox="../media/how-to/projects/projects-create-details.png":::

1. Select **Create a project**.  Or, if you want to customize the hub, follow the steps in the next section.

### Customize the hub

Projects live inside a hub. A hub allows you to share configurations like data connections with all projects, and centrally manage security settings and spend. If you're part of a team, hubs are shared across other team members in your subscription. For more information about the relationship between hubs and projects, see the [hubs and projects overview](../concepts/ai-resources.md) documentation.

When you create a new hub, you must have **Owner** or **Contributor** permissions on the selected resource group. If you're part of a team and don't have these permissions, your administrator should create a hub for you.

When you create a new hub, default settings are provided.  If you want to customize the settings, do so before you create the project:

1. In the **Create a project** form, select **Customize**.
    
    :::image type="content" source="../media/how-to/projects/projects-customize-hub.png" alt-text="Screenshot of the customize button within the create project dialog." lightbox="../media/how-to/projects/projects-customize-hub.png":::


1. Select an existing **Resource group** you want to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started it's recommended to create a new resource group for your project. This allows you to easily manage the project and all of its resources together. When you create a project, several resources are created in the resource group, including a hub, a container registry, and a storage account.

1. Select a **Location** or use the defailt. The location is the region where the hub is hosted. The location of the hub is also the location of the project. Azure AI services availability differs per region. For example, certain models might not be available in certain regions.
1. Select an existing Azure AI services resource (including Azure OpenAI) from the dropdown if you have one, or use the default to create a new resource.

    :::image type="content" source="../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../media/how-to/projects/projects-create-resource.png":::

1. On the **Review and finish** page, you see the Azure AI services resource name and other settings to review.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish.png" alt-text="Screenshot of the review and finish page within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish.png":::

1. Review the project details and then select **Create a project**. You see progress of resource creation and the project is created when the process is complete.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish-progress.png" alt-text="Screenshot of the resource creation progress within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish-progress.png":::
