---
title: Set up your development environment
titleSuffix: Azure AI Foundry
description:  Instructions for installing the Azure AI Foundry SDK and the Azure CLI 
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 04/22/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley

#customer intent: As a developer, I want to install the Azure AI Foundry SDK in my development environment
---

# Set up your development environment

Set up your development environment to use the [Azure AI Foundry](https://ai.azure.com) SDK. You also need Azure CLI for authentication so that your code can access your user credentials.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).


## Create a new environment

# [Python SDK](#tab/python)

In the IDE of your choice, create a new folder for your project. Open a terminal window in that folder.

[!INCLUDE [Install Python](../../includes/install-python.md)]

# [Java](#tab/java)

[!INCLUDE [Install Jave](../../includes/install-java.md)]

# [JavaScript](#tab/javascript)

Install Javascript.

# [C#](#tab/csharp)

[!INCLUDE [install-csharp](../../includes/install-csharp.md)]

---



## <a name="installs"></a> Install the Azure CLI and sign in 

[!INCLUDE [Install the Azure CLI](../../includes/install-cli.md)]

Keep this terminal window open to run your scripts from here as well, now that you've signed in.

## Next step

* [Get started in Azure AI Foundry](../../quickstarts/get-started-code.md)