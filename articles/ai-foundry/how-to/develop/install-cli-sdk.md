---
title: Set up your development environment
titleSuffix: Azure AI Foundry
description: Instructions for installing the Azure AI Foundry SDK and the Azure CLI
author: sdgilley
ms.author: sgilley
manager: scottpolly
ms.reviewer: dantaylo
ms.date: 04/22/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-aifnd
  - build-2025
zone_pivot_groups: foundry-sdk-overview-languages
# customer intent: As a developer, I want to install the Azure AI Foundry SDK in my development environment
---

# Set up your development environment

Set up your development environment to use the [Azure AI Foundry](https://ai.azure.com) SDK. You also need Azure CLI for authentication so that your code can access your user credentials.

## Prerequisites

- An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).


## Install your programming language 

::: zone pivot="programming-language-python"

In the IDE of your choice, create a new folder for your project. Open a terminal window in that folder.

[!INCLUDE [Install Python](../../includes/install-python.md)]

::: zone-end

::: zone pivot="programming-language-java"

[!INCLUDE [Install Jave](../../includes/install-java.md)]

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

Keep this terminal window open to run your scripts from here as well, now that you've signed in.

## Next step

* [Get started in Azure AI Foundry](../../quickstarts/get-started-code.md)
