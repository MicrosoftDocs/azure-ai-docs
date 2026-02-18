---
title: Prepare your development environment
titleSuffix: Microsoft Foundry
description: Set up your development environment with language runtimes, Azure CLI, and tools for Microsoft Foundry development.
keywords: foundry sdk, azure cli, development environment, visual studio code
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 12/18/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-aifnd
  - build-2025
  - dev-focus
ai-usage: ai-assisted
zone_pivot_groups: foundry-sdk-overview-languages
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to install the Microsoft Foundry SDK in my development environment
---

# Prepare your development environment

Set up your development environment to use the Microsoft Foundry SDK. You also need Azure CLI for authentication so that your code can access your user credentials.

In this article, you install language runtimes, Azure CLI, Azure Developer CLI, the Foundry VS Code extension, and Git.

:::moniker range="foundry-classic"

> [!IMPORTANT]  
> This article covers **general prerequisites** only, such as language runtimes, global tools, and VS Code and extension setup.  
> It doesn't cover scenario-specific steps like SDK installation or authentication.  
> When your environment is ready, continue to the [quickstart](../../quickstarts/get-started-code.md) for those instructions.
:::moniker-end
:::moniker range="foundry"

> [!IMPORTANT]  
> This article covers **general prerequisites** only, such as language runtimes, global tools, and VS Code and extension setup.  
> It doesn't cover scenario-specific steps like SDK installation or authentication.  
> When your environment is ready, continue to the [quickstart](../../default/tutorials/quickstart-create-foundry-resources.md) for those instructions.
:::moniker-end

## Prerequisites

- [!INCLUDE [azure-subscription](../../includes/azure-subscription.md)]
- Download, install, and configure Visual Studio Code, or the IDE of your choice. For more information, see [Download Visual Studio Code](https://code.visualstudio.com/Download).
- To create and manage Foundry resources, one of the following Azure RBAC roles 
  - **Azure AI Project Manager** (for managing Foundry projects)
  - **Contributor** or **Owner** (for subscription-level permissions)
- To use project but not create new resources, you need at least:
  - **Azure AI User** on the projects you use (least-privilege role for development)

  For details on each role's permissions, see [Role-based access control for Microsoft Foundry](/azure/ai-foundry/concepts/rbac-foundry).


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

Install [Node.js](https://nodejs.org/) (version 18 or later is recommended).

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

Many of the [AI solution templates](ai-template-get-started.md) include a deployment option using `azd`.

## Install the Foundry VS Code extension

The Foundry extension for Visual Studio Code lets you deploy models, build AI apps, and work with Agents directly from the VS Code interface. [Install the Foundry VS Code extension](https://marketplace.visualstudio.com/items?itemName=TeamsDevApp.vscode-ai-foundry).

## Install Git

Git is required to clone Foundry SDK samples. If you don't have Git installed, [follow the instructions for your platform](https://git-scm.com/downloads) and select your operating system.

## Troubleshooting

| Issue | Resolution |
| ----- | ---------- |
| Command not found after install | Close and reopen your terminal, or restart VS Code, so PATH changes take effect. |
| `az login` fails with a browser error | Run `az login --use-device-code` to authenticate using a device code flow instead. |
| Python not found | Use `python3` instead of `python` on macOS/Linux, or install a supported version (3.9 or later). |
| Permission denied during install | On macOS/Linux, avoid `sudo pip install`. Use a [virtual environment](#create-a-virtual-environment) instead. |

## Related content

* [Get started with Foundry](../../quickstarts/get-started-code.md)

::: zone pivot="programming-language-python"

* [Microsoft Foundry SDK Reference documentation](/python/api/overview/azure/ai-projects-readme)

::: zone-end

::: zone pivot="programming-language-csharp"

* [.NET SDK Reference documentation](/dotnet/api/overview/azure/ai.projects-readme)

::: zone-end

::: zone pivot="programming-language-javascript"

* [JavaScript/TypeScript SDK Reference documentation](/javascript/api/overview/azure/ai-projects-readme)

::: zone-end

::: zone pivot="programming-language-java"

* [Java SDK Reference documentation](/java/api/overview/azure/ai-projects-readme)

::: zone-end
