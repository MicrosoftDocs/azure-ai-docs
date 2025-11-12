---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 08/29/2024
ms.custom: include, ignite-2024
---

You install the [Azure CLI](/cli/azure/what-is-azure-cli) and sign in from your local development environment, so that you can use your user credentials to call Azure OpenAI in Microsoft Foundry Models.

In most cases you can install Azure CLI from your terminal using the following command: 

# [Windows](#tab/windows)

```powershell 
winget install -e --id Microsoft.AzureCLI
```

# [Linux](#tab/linux)

```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

# [macOS](#tab/macos)

```bash
brew update && brew install azure-cli
```

---

You can follow instructions [How to install the Azure CLI](/cli/azure/install-azure-cli) if these commands don't work for your particular operating system or setup.

After you install the Azure CLI, sign in using the ``az login`` command and sign-in using the browser:

```
az login
```

Alternatively, you can sign in manually via the browser with a device code.

```
az login --use-device-code
```
