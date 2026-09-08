---
title: "Install Microsoft Foundry Toolkit for Visual Studio Code"
description: "Install and verify Microsoft Foundry Toolkit for Visual Studio Code from the Visual Studio Marketplace or the Extensions view."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-sdk
content_well_notification:
  - AI-contribution
ai-usage: ai-assisted
ms.topic: how-to
ms.date: 08/20/2026
ms.reviewer: erichen
ms.author: rotabor
author: bobtabor-msft

# customer intent: As an AI app developer, I want to install Foundry Toolkit so that I can work with models and agents in VS Code.
ms.custom:
  - doc-kit-assisted
---

# Install Microsoft Foundry Toolkit for Visual Studio Code

Install Microsoft Foundry Toolkit for Visual Studio Code from the Visual Studio
Marketplace or the Extensions view. When you finish, the Foundry Toolkit view
is available in Visual Studio Code.

## Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/Download).
- The [.NET Runtime](/dotnet/core/install/). Foundry Toolkit depends on this
  runtime.

For a complete Foundry development environment, install
[Foundry DevPack](install-cli-sdk.md#install-foundry-devpack) instead of
installing Foundry Toolkit by itself. DevPack installs Foundry Toolkit,
`azd` and `azd ai`, Foundry Canvas, and Microsoft Foundry Skill to provide a
smoother workflow across your editor, terminal, and coding agent. For the full
setup, see [Prepare your development environment](install-cli-sdk.md).

## Install Foundry Toolkit

Install the extension from the Visual Studio Marketplace or from within Visual
Studio Code.

### Install from the Visual Studio Marketplace

1. Open the
   [Microsoft Foundry Toolkit for Visual Studio Code extension](https://aka.ms/foundrytk)
   page.
1. Select **Install**, and follow the prompt to open Visual Studio Code.
1. In Visual Studio Code, complete the installation. Reload the window if
   prompted.
1. Confirm that the **Foundry Toolkit** icon appears in the Activity Bar.

### Install manually from Visual Studio Code

Use the Extensions view to find and install the extension without leaving
Visual Studio Code.

:::image type="content" source="../../media/how-to/get-started-projects-vs-code/install-foundry-toolkit-marketplace.png" alt-text="Screenshot of the Visual Studio Code Extensions Marketplace showing the Foundry Toolkit for VS Code extension details." lightbox="../../media/how-to/get-started-projects-vs-code/install-foundry-toolkit-marketplace.png":::

1. In the Activity Bar, select **Extensions**.
1. Search for **Foundry Toolkit for VS Code**.
1. In the search results, select the extension published by Microsoft.
1. Select **Install**.
1. Reload the window if prompted.
1. Confirm that the **Foundry Toolkit** icon appears in the Activity Bar.

After installation, open **What's New** under **Help And Feedback** in Foundry
Toolkit to review the features and changes in the installed version.

## Confirm the installation

Confirm that the extension activated successfully.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Confirm that **My Resources**, **Developer Tools**, and **Help And Feedback**
   appear in the Foundry Toolkit view.

## Clean up

This procedure doesn't create Azure resources. If you installed Foundry
Toolkit only to evaluate it, open **Extensions**, find **Foundry Toolkit for
Visual Studio Code**, and select **Uninstall**. Uninstalling the extension
doesn't delete any Azure resources.

## Next step

> [!div class="nextstepaction"]
> [Set up a Foundry project](set-up-foundry-project-visual-studio-code.md)
