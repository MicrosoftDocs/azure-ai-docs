---
title: include file
description: include file
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include
ai-usage: ai-assisted
---

Prepare your development environment to build with the Microsoft Foundry. You need a
supported programming language, the Azure CLI for authentication, Git, and Foundry developer
tools.

> [!TIP]
> Foundry DevPack is the recommended way to install the developer tools in one command. You can
> also install each tool separately.

> [!IMPORTANT]
> This article covers general prerequisites, global tools, and Visual Studio Code setup. It
> doesn't cover scenario-specific SDK packages or authentication code. When your environment is
> ready, continue to the [quickstart](../tutorials/quickstart-create-foundry-resources.md).

## Prerequisites

- [!INCLUDE [azure-subscription](azure-subscription.md)]
- Download, install, and configure [Visual Studio Code](https://code.visualstudio.com/Download),
  or use the IDE of your choice.
- To create and manage Foundry resources, use one of these Azure RBAC roles:
    - **Foundry Project Manager** to manage Foundry projects.

    [!INCLUDE [role-rename-note](./role-rename-note.md)]
    - **Owner** for subscription-level permissions and role assignments required by some
    scenarios.
- To use an existing project without creating resources, you need at least **Foundry User** on
  the project.

For details about each role, see
[Role-based access control for Microsoft Foundry](../concepts/rbac-foundry.md).

## Install Foundry DevPack

Foundry DevPack installs the Foundry developer tools for your editor, terminal, and coding agent.
Run the command for your operating system.

### Windows

```powershell
winget install Microsoft.FoundryDevPack
```

### macOS

```bash
brew install --cask microsoft/foundry/devpack && foundry-devpack install
```

### Linux

```bash
curl -fsSL https://aka.ms/foundry-devpack-install.sh | bash
```

DevPack installs these tools:

| Tool | What you can do |
| --- | --- |
| [Microsoft Foundry Toolkit for Visual Studio Code](../how-to/develop/get-started-projects-vs-code.md) | Build, test, evaluate, and deploy from Visual Studio Code. |
| [`azd` and `azd ai`](../agents/concepts/cli-agent-development.md) | Scaffold, deploy, evaluate, and automate from the terminal. |
| [Foundry Canvas (preview)](../agents/concepts/foundry-canvas.md) | Design and deploy hosted agents with a guided Copilot canvas. |
| [Microsoft Foundry Skill](../how-to/develop/use-microsoft-foundry-skill.md) | Give coding agents reusable guidance for Foundry workflows. |

Continue with the following sections to set up your programming language, sign in with the Azure
CLI, and install Git.

## Work with a programming language

Use the language that your application requires. Expand a section if you need to install its
runtime or Visual Studio Code extension.

<details>
<summary>Python</summary>

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

</details>

<details>
<summary>Java</summary>

Install JDK 17 or later. The
[Microsoft Build of OpenJDK](/java/openjdk/download) is a free Long-Term Support distribution.
For editor support, install the
[Visual Studio Code Extension Pack for Java](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack).

</details>

<details>
<summary>JavaScript/TypeScript</summary>

Install [Node.js](https://nodejs.org/). Version 20 or later is recommended.

</details>

<details>
<summary>C#</summary>

Install the latest Long-Term Support version of the
[.NET SDK](https://dotnet.microsoft.com/download). For editor support, install
[C# Dev Kit for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit).

</details>

## Install the Azure CLI and sign in

[!INCLUDE [Install the Azure CLI](install-cli.md)]

Keep this terminal open to run scripts after you sign in.

## Install Git

To clone Foundry SDK samples, you need Git. If you don't have Git installed, download and
install it from the [Git website](https://git-scm.com/downloads).

## Install developer tools individually

If you don't use Foundry DevPack, install each developer tool separately:

1. [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd?tabs=winget-windows%2Cbrew-mac%2Cscript-linux&pivots=os-windows).
1. Install all Foundry extensions for `azd`:
   ```bash
   azd ext install microsoft.foundry
   ```
   To install individual extensions instead, see
   [Install the Azure Developer CLI Foundry extensions](../agents/how-to/install-cli-foundry-extensions.md).
1. Install the editor and coding-agent tools:
   - [Install and set up the Microsoft Foundry Toolkit for Visual Studio Code](https://code.visualstudio.com/docs/intelligentapps/overview#_install-and-setup).
   - [Use Foundry Canvas](../agents/concepts/foundry-canvas.md) to design and deploy hosted agents.
   - [Use the Microsoft Foundry Skill](../how-to/develop/use-microsoft-foundry-skill.md) in your
     coding agent.

Many [AI solution templates](../how-to/develop/ai-template-get-started.md) support deployment with
`azd`.

## Troubleshooting

| Issue | Resolution |
| --- | --- |
| Command not found after installation | Close and reopen your terminal, or restart Visual Studio Code, so that PATH changes take effect. |
| `az login` fails with a browser error | Run `az login --use-device-code` to authenticate with a device code. |
| Python isn't found | Use `python3` instead of `python` on macOS or Linux, or install Python 3.9 or later. |
| Permission denied during Python package installation | On macOS or Linux, don't use `sudo pip install`. Use a virtual environment instead. |

## Related content

- [Create Foundry resources with the Microsoft Foundry SDK](../tutorials/quickstart-create-foundry-resources.md)
- [Get started with Foundry](../quickstarts/get-started-code.md)
- [Microsoft Foundry SDK reference for Python](/python/api/overview/azure/ai-projects-readme)
- [Microsoft Foundry SDK reference for .NET](/dotnet/api/overview/azure/ai.projects-readme)
- [Microsoft Foundry SDK reference for JavaScript and TypeScript](/javascript/api/overview/azure/ai-projects-readme)
- [Microsoft Foundry SDK reference for Java](/java/api/overview/azure/ai-projects-readme)
