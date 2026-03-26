---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: erichen
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/free/).
- [Visual Studio Code](https://code.visualstudio.com/Download) installed.
- Your subscription needs to be below your [quota limit](../how-to/quota.md) to [deploy a new model in this article](#deploy-a-model-from-the-model-catalog). If you already reached your quota limit, you need to have a [deployed chat model](../foundry-models/how-to/deploy-foundry-models.md).
- Appropriate RBAC permissions to create and manage Foundry resources. For more information, see [Role-based access control for Foundry](../concepts/rbac-foundry.md).

## Install the extension

To use Foundry capabilities in VS Code, install the Foundry for Visual Studio Code extension. Install from the Visual Studio Code Marketplace or directly from within VS Code.

### Install from the Visual Studio Code Marketplace

Use the marketplace to install the extension without opening VS Code first.

1. Open the [Foundry for Visual Studio Code extension page](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).
1. Select the **Install** button.
1. Follow the prompts to install the extension in Visual Studio Code.
1. After installation, open Visual Studio Code and verify the extension is installed successfully from the status messages.
1. The Foundry icon appears in the primary navigation bar on the left side of VS Code.

### Install from within Visual Studio Code

Alternatively, search for the extension directly from the VS Code extensions view.

1. Open VS Code.

1. Select **Extensions** from the left pane.

1. Select the **Settings** icon from the top-right on the extensions pane.

1. Search for and select **Foundry**.

1. Select **Install**.

1. After installation completes, a status message confirms the extension is installed. The Foundry icon appears in the left navigation bar.
