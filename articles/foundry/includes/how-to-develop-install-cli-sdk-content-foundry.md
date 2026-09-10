---
title: include file
description: include file
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/18/2026
ms.custom: include
ai-usage: ai-assisted
---

Prepare your development environment to build with Microsoft Foundry. You need a supported
programming language, Git, and the Foundry developer tools that fit your workflow.

> [!TIP]
> Foundry DevPack is the recommended way to install the developer tools in one command. You can
> also install each tool separately.

> [!IMPORTANT]
> This article covers general prerequisites and developer tools. It doesn't cover
> scenario-specific SDK packages or authentication code. When your environment is ready, continue
> to the [quickstart](../tutorials/quickstart-create-foundry-resources.md).

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]
- Access to the Foundry resource or project that you plan to use. For setup guidance, see
  [Minimum role assignments to get started](../concepts/rbac-foundry.md#minimum-role-assignments-to-get-started).

## Install Foundry DevPack

Foundry DevPack installs the Foundry developer tools for your terminal, editor, and coding agent.
Select your operating system.

# [Windows](#tab/windows)

```powershell
winget install Microsoft.FoundryDevPack
```

# [macOS](#tab/macos)

```bash
brew install --cask microsoft/foundry/devpack && foundry-devpack install
```

# [Linux](#tab/linux)

```bash
curl -fsSL https://aka.ms/foundry-devpack-install.sh | bash
```

---

DevPack installs its core tools and adds host extensions only when their apps are present:

| Tool | What you can do |
| --- | --- |
| [`azd` and `azd ai`](../agents/concepts/cli-agent-development.md) | Scaffold, deploy, evaluate, and automate from the terminal. |
| [Microsoft Foundry Skill](../how-to/develop/use-microsoft-foundry-skill.md) | Give coding agents reusable guidance for Foundry workflows. |
| [Microsoft Foundry Toolkit for Visual Studio Code](../how-to/develop/get-started-projects-visual-studio-code.md) | Installed only when Visual Studio Code is present. Build, test, evaluate, and deploy from the editor. |
| [Foundry Canvas (preview)](../agents/concepts/foundry-canvas.md) | Installed only when GitHub Copilot App is present. Design and deploy hosted agents from a guided canvas. |

DevPack doesn't install Visual Studio Code or GitHub Copilot App.

Continue with the following sections to set up your programming language and install Git.

## Work with a programming language

Use the language that your application requires. Select a tab to install its runtime or Visual
Studio Code extension.

# [Python](#tab/python)

Install [Python 3.10 or later](https://www.python.org/downloads/). Python 3.9 is the minimum
supported version. Create a virtual environment for your project instead of installing packages
globally.

**Windows**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS and Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

For editor support, install the
[Python extension for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

# [C#](#tab/csharp)

Install the latest Long-Term Support version of the
[.NET SDK](https://dotnet.microsoft.com/download). For editor support, install
[C# Dev Kit for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit).

# [JavaScript/TypeScript](#tab/javascript)

Install [Node.js](https://nodejs.org/). Version 20 or later is recommended.

# [Java](#tab/java)

Install JDK 17 or later. The
[Microsoft Build of OpenJDK](/java/openjdk/download) is a free Long-Term Support distribution.
For editor support, install the
[Visual Studio Code Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack).

---

## Install Git

To clone Foundry SDK samples, you need Git. If you don't have Git installed, download and
install it from the [Git website](https://git-scm.com/downloads).

## Install developer tools separately

If you don't use Foundry DevPack, select a tab to install only the tooling that you need.

# [`azd` and `azd ai`](#tab/azd-ai)

1. [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd).
1. Install the Foundry extensions:

   ```bash
   azd ext install microsoft.foundry
   ```

To install individual extensions instead of the full bundle, see
[Install the Azure Developer CLI Foundry extensions](../agents/how-to/install-cli-foundry-extensions.md).

For direct, granular management of individual Azure resources, use the Azure CLI (`az`). See
[Azure Developer CLI vs Azure CLI](/azure/developer/azure-developer-cli/azure-developer-cli-vs-azure-cli).

# [Microsoft Foundry Skill](#tab/foundry-skill)

Install the [Microsoft Foundry Skill](../how-to/develop/use-microsoft-foundry-skill.md) in your
coding agent. The installation steps vary by coding-agent host.

# [Microsoft Foundry Toolkit](#tab/foundry-toolkit)

If you use Visual Studio Code, [install Microsoft Foundry Toolkit](https://code.visualstudio.com/docs/intelligentapps/overview#_install-and-setup).

# [Foundry Canvas](#tab/foundry-canvas)

If you use GitHub Copilot App, [install Foundry Canvas](../agents/concepts/foundry-canvas.md) to
design and deploy hosted agents from a guided canvas.

---

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Command not found after installation | Close and reopen your terminal. If you use Visual Studio Code, restart it so that PATH changes take effect. |
| Python isn't found | Use `python3` instead of `python` on macOS or Linux, or install Python 3.9 or later. |
| Permission denied during Python package installation | On macOS or Linux, don't use `sudo pip install`. Use a virtual environment instead. |

## Related content

- [Create Foundry resources with the Microsoft Foundry SDK](../tutorials/quickstart-create-foundry-resources.md)
- [Get started with Foundry](../quickstarts/get-started-code.md)
- [Microsoft Foundry SDK reference for Python](/python/api/overview/azure/ai-projects-readme)
- [Microsoft Foundry SDK reference for .NET](/dotnet/api/overview/azure/ai.projects-readme)
- [Microsoft Foundry SDK reference for JavaScript and TypeScript](/javascript/api/overview/azure/ai-projects-readme)
- [Microsoft Foundry SDK reference for Java](/java/api/overview/azure/ai-projects-readme)
