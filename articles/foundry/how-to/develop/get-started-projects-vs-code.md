---
title: "Work with the Microsoft Foundry for Visual Studio Code extension"
description: "Create projects, deploy models from the model catalog, and interact with model playgrounds using the Microsoft Foundry for Visual Studio Code extension."
manager: mcleans
ms.service: azure-ai-foundry
content_well_notification: 
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 03/12/2026
ms.reviewer: erichen
ms.author: johalexander
author: ms-johnalex

# customer intent: As an AI app developer, I want to learn how to use the Microsoft Foundry for Visual Studio Code extension so that I can create projects and deploy models using Microsoft Foundry capabilities directly in VS Code.
ms.custom:
  - classic-and-new
  - doc-kit-assisted
---

# Work with the Microsoft Foundry for Visual Studio Code extension

In this article, learn how to install and use the [Microsoft Foundry](../../what-is-foundry.md) for Visual Studio Code extension. Create projects, deploy models from the Foundry model catalog, and interact with model playgrounds from within VS Code.

[!INCLUDE [get-started-projects-vs-code 1](../../includes/how-to-develop-get-started-projects-vs-code-1.md)]

## Connect to your Azure resources

After you install the extension, sign in to your Azure subscription and open a Foundry project to begin working with models, agents, and playgrounds.

> [!NOTE]
> For a full list of features available in the extension, use the Command Palette. Select <kbd>F1</kbd> to open the command palette and search **Foundry**. The following screenshot shows some of the available commands.
>     :::image type="content" source="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png" alt-text="Screenshot of the VS Code command palette showing available Foundry commands such as Open Model Catalog and Open Playground." lightbox="../../media/how-to/get-started-projects-vs-code/visual-studio-command-palette-small.png":::

### Sign in to your resources

Sign in to your Azure subscription so the extension can access your Foundry projects and deployed models.

1. Select the Azure icon on the VS Code navigation bar.

1. Select **Sign in to Azure...** in the **Azure Resources** view.

1. Under the **Resources** section, select your Azure subscription and resource group.

1. Select **Foundry** and right-click your project.

1. Select **Open in Foundry Extension**.

    Your Foundry project resources appear in the extension view, and the Foundry icon displays on the VS Code navigation bar.

### Navigate the extension interface

The Foundry extension organizes your workspace into three main sections.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/initial-view.png" alt-text="Screenshot of the Foundry extension interface showing the Resources, Tools, and Help and Feedback sections.":::

| Section | What it contains | When to use it |
| ------- | --------------- | -------------- |
| **Resources** | Deployed models, declarative agents, hosted agents, connections, and vector stores for your Foundry project. | View and manage your project resources. |
| **Tools** | Model Catalog, Model Playground, Agent Playgrounds (remote and local), Local Visualizer, and Deploy Hosted Agents. | Deploy new models, test prompts, and interact with agents. |
| **Help and Feedback** | Documentation, GitHub repository, Microsoft Privacy Statement, and community links. | Get help or provide feedback. |

[!INCLUDE [get-started-projects-vs-code 2](../../includes/how-to-develop-get-started-projects-vs-code-2.md)]

## Next steps

- [Explore Foundry models](../../concepts/foundry-models-overview.md)
- [Deploy models with Foundry](../../foundry-models/how-to/deploy-foundry-models.md)
