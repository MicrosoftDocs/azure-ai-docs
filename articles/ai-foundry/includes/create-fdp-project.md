---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: deeikele
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/09/2025
ms.custom: include, build-2024, ignite-2024
---

To create a [!INCLUDE [fdp-project-name](fdp-project-name.md)] in [Azure AI Foundry](https://ai.azure.com), follow these steps:

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Go to [Azure AI Foundry](https://ai.azure.com). If you are in a project, select **Azure AI Foundry** at the top left of the page to go to the **Home** page.
1. In the middle of the page, select **Start building**. Or select **+ Create project** in the top right corner of the page if you have existing projects.
1. Enter a name for the project.
1. Select **Create**. Or, if you want to customize your settings, follow the steps in the next section.

### Advanced options

A [!INCLUDE [fdp-project-name](fdp-project-name.md)] is created on an `AIServices` resource. This resource is created for you automatically when you create the project. 

To customize the settings for your project, follow these steps:

1. In the **Create a project** form, select **Advanced options**.

1. Select an existing **Resource group** you want to use, or leave the default to create a new resource group.

    > [!TIP]
    > Especially for getting started we recommend you create a new resource group for your project. The resource group allows you to easily manage the project and all of its resources together. 

1. Select a **Location** or use the default. The location is the region where the hub is hosted. Azure AI services availability differs per region. For example, certain models might not be available in certain regions.

1. Select **Create**. You see progress of resource creation and the project is created when the process is complete.

## Create multiple projects on the same resource

You can create other projects on an existing `AIServices` resource.

Your first project (default project) plays a special role and has access to more features:

| Feature | Default project | Nondefault project |
|--|--|--|
| Model inference | ✓ | ✓ |
| Playgrounds | ✓ | ✓ |
| Agents | ✓ | ✓ |
| Evaluations | ✓ | ✓ |
| Connections | ✓ | ✓ |
| AI Foundry API that works with agents and across models | ✓ | ✓ |
| Project-level isolation of files and outputs | ✓ | ✓ |
| Azure OpenAI with Batch, StoredCompletions, Fine-tuning | ✓ |  |
| Backwards compatible with project-less {account}.cognitiveservices.com data plane API | ✓ |  |
| Content safety | ✓ |  |

To add a nondefault project to a resource:

1. In [Azure AI Foundry](https://ai.azure.com), select either the [!INCLUDE [fdp-project-name](fdp-project-name.md)] or its associated resource.
1. In the left pane, select **Management center**.
1. In the resource section, select  **Overview**.
1. Select **New project** and provide a name.

    :::image type="content" source="../media/how-to/projects/second-project.png" alt-text="Screenshot shows how to create a second project on an existing resource.":::