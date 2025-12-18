---
title: Set up your development environment
titleSuffix: Microsoft Foundry
description: Instructions for installing the Microsoft Foundry SDK and the Azure CLI
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 12/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-aifnd
  - build-2025
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to install the Microsoft Foundry SDK in my development environment
---

# Prepare your development environment

Set up your development environment to use the Microsoft Foundry SDK. You also need Azure CLI for authentication so that your code can access your user credentials.


> [!IMPORTANT]  
> This article covers **general prerequisites** only, such as language runtimes, global tools, and VS Code and extension setup.  
> It doesn't cover scenario-specific steps like SDK installation or authentication.  
> When your environment is ready, continue to the [quickstart](../../quickstarts/get-started-code.md) for those instructions.


## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- Download, install, and configure Visual Studio Code, or the IDE of your choice. For more information, see [Download Visual Studio Code](https://code.visualstudio.com/Download).
- Set the appropriate RBAC permissions to create and manage Microsoft Foundry resources in the Visual Studio Code extension. For more information, see [Role-based access control for Foundry](/azure/ai-foundry/concepts/rbac-azure-ai-foundry).


## Install your programming language

::: zone pivot="programming-language-python"

In Visual Studio Code, create a new folder for your project. Open a terminal window in that folder.

[!INCLUDE [Install Python](../../includes/install-python.md)]

### Install the Python extension for Visual Studio Code

The Python extension for Visual Studio Code supports Python with IntelliSense, debugging, formatting, linting, code navigation, refactoring, variable explorer, test explorer, and environment management.

[Install the Python Extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Install Java](../../includes/install-java.md)]

### Install the Visual Studio Code Extension Pack for Java

The Extension Pack for Java is a collection of popular extensions that can help you write, test, and debug Java applications in Visual Studio Code. 

[Install the Visual Studio Code Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack).

::: zone-end

::: zone pivot="programming-language-javascript"

Install [Node.js](https://nodejs.org/).

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [install-csharp](../../includes/install-csharp.md)]

::: zone-end



##  Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../../includes/install-cli.md)]

Keep this terminal open to run scripts after signing in.

## Install the Azure Developer CLI

The Azure Developer CLI (azd) is an open-source tool that helps you set up and deploy app resources on Azure. It provides simple commands for key stages of development, whether you use a terminal, IDE, or CI/CD pipelines.
[Install the Azure Developer CLI for your platform](/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows).

The Azure Developer CLI allows you to quickly deploy many of the [AI solution templates](ai-template-get-started.md).

## Install The Foundry VS Code Extension

The Foundry extension for Visual Studio Code lets you deploy models, build AI apps, and work with Agents directly from the VS Code interface. [Install The Foundry VS Code Extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

## Install Git

Many of the Microsoft Foundry SDK samples use Git for version control. If you don't have Git installed, [follow the instructions for your platform](https://git-scm.com/downloads) and select your operating system.

## Next step

* [Get started in Foundry](../../quickstarts/get-started-code.md)
