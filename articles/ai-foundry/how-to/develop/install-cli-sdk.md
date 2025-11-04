---
title: Set up your development environment
titleSuffix: Azure AI Foundry
description: Instructions for installing the Azure AI Foundry SDK and the Azure CLI
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 11/04/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-aifnd
  - build-2025
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to install the Azure AI Foundry SDK in my development environment
---

# Prepare your development environment

Set up your development environment to use the Azure AI Foundry SDK. You also need Azure CLI for authentication so that your code can access your user credentials.


> **Important**  
> This article covers **general prerequisites** only—language runtimes, global tools, VS Code and extension setup.  
> It does **not** include scenario-specific steps like SDK installation or authentication.  
> When your environment is ready, continue to the [quickstart](../../quickstarts/get-started-code.md) for those instructions.


## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- Download, install, and configure Visual Studio Code. More information: [Download Visual Studio Code](https://code.visualstudio.com/Download)
- Set the appropriate RBAC permissions to create and manage Azure AI Foundry resources with the Visual Studio Code extension. For more information, see [Role-based access control for Azure AI Foundry](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).


## Install your programming language and VS Code extension

::: zone pivot="programming-language-python"

In Visual Studio Code, create a new folder for your project. Open a terminal window in that folder.

[!INCLUDE [Install Python](../../includes/install-python.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Install Java](../../includes/install-java.md)]

::: zone-end

::: zone pivot="programming-language-javascript"

Install [Node.js](https://nodejs.org/)

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [install-csharp](../../includes/install-csharp.md)]

::: zone-end

<a name="installs"></a>

##  Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../../includes/install-cli.md)]

Keep this terminal open to run scripts after signing in.

## Install the Azure Developer CLI

[Install the Azure Developer CLI for your platform](/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows)

## Install The AI Foundry VS Code Extension

[Install The AI Foundry VS Code Extension](https://marketplace.visualstudio.com/items?itemName=AzureAIFoundry.azure-ai-foundry-vscode)

## Install Git

Many of the Azure AI Foundry SDK samples use Git for version control. If you don't have Git installed, [follow the instructions for your platform](https://git-scm.com/downloads) and select your operating system.

## Next step

* [Get started in Azure AI Foundry](../../quickstarts/get-started-code.md)
