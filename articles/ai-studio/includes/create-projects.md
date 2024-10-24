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

1. Go to [Azure AI Studio](https://ai.azure.com) and select **Azure AI Studio** in the upper left corner. From the welcome page, select **+ Create project**.
1. Enter a name for the project.
1. Select a hub from the dropdown to host your project. If you don't yet have a hub, select **Create a new hub**. For information about the relationship between hubs and projects, see the [hubs and projects overview](../concepts/ai-resources.md) documentation.

    :::image type="content" source="../media/how-to/projects/projects-create-details.png" alt-text="Screenshot of the project details page within the create project dialog." lightbox="../media/how-to/projects/projects-create-details.png":::

    > [!NOTE]
    > To create a hub, you must have **Owner** or **Contributor** permissions on the selected resource group. It's recommended to share a hub with your team. This lets you share configurations like data connections with all projects, and centrally manage security settings and spend. For more options to create a hub, see [how to create and manage an Azure AI Studio hub](../how-to/create-azure-ai-resource.md). A project name must be unique between projects that share the same hub.

1. If you're creating a new hub, enter a name and select **Create**. You can now use the **Customize** button from the **Create a project** dialog to customize the hub settings. For example, you can select your Azure subscription, resource group, location, and connected Azure AI Services or Azure OpenAI. When finished customizing, select **Next** to review changes.

    :::image type="content" source="../media/how-to/projects/projects-create-resource.png" alt-text="Screenshot of the create resource page within the create project dialog." lightbox="../media/how-to/projects/projects-create-resource.png":::

1. Select **Create a project**. You see progress of resource creation and the project is created when the process is complete.

    :::image type="content" source="../media/how-to/projects/projects-create-review-finish-progress.png" alt-text="Screenshot of the resource creation progress within the create project dialog." lightbox="../media/how-to/projects/projects-create-review-finish-progress.png":::

Once a project is created, you can access the playground, tools, and other assets in the left navigation panel.
