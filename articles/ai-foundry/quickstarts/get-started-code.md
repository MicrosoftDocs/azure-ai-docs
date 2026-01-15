---
title: "Microsoft Foundry Quickstart"
titleSuffix: Microsoft Foundry
description: Get started with Microsoft Foundry SDK to build AI applications. 
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 12/16/2025
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - build-2024
  - devx-track-azurecli
  - devx-track-python
  - ignite-2024
  - update-code7
  - build-aifnd
  - build-2025
  - peer-review-program
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
# customer intent: As a developer, I want to start using the Microsoft Foundry portal and client libraries.
---

# Microsoft Foundry Quickstart

[!INCLUDE [version-banner](../includes/version-banner.md)]

:::moniker range="foundry-classic"
[!INCLUDE [get-started-code-classic](../includes/get-started-code-classic.md)]
:::moniker-end

:::moniker range="foundry"
In this quickstart, you use [!INCLUDE [foundry-link](../default/includes/foundry-link.md)] to interact with a Foundry model, create and chat with an agent.

The Microsoft Foundry SDK is available in multiple languages, including Python, Java, TypeScript, and C#. This quickstart provides instructions for each of these languages.

## Prerequisites

* A model deployed in Microsoft Foundry. If you don't have this, jump to [What you need to run this code](#what-you-need-to-run-this-code) to create them. The code in this quickstart
* The [endpoint for the model](#find-your-endpoint).
  


## Set environment variables

Store the endpoint as an environment variable.  Also set these values for use in your scripts.


Set these environment variables to use in your scripts:

    ```plaintext
    PROJECT_ENDPOINT=<endpoint copied from welcome screen>
    AGENT_NAME="MyAgent"
    MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"
    ```
## Install and authenticate


[!INCLUDE [quickstart-v2-install](../default/includes/quickstart-v2-install.md)]

## Chat with a model

[!INCLUDE [quickstart-v2-chat](../default/includes/quickstart-v2-chat.md)]

## Create an agent

[!INCLUDE [quickstart-v2-create-agent](../default/includes/quickstart-v2-create-agent.md)]

## Chat with an agent

[!INCLUDE [quickstart-v2-agent-chat](../default/includes/quickstart-v2-agent-chat.md)]

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## What you need to run this code

The preceeding code uses a model in a project.  If you don't have one, start here first.  You need:

- [!INCLUDE [azure-subscription](../includes/azure-subscription.md)]
- [!INCLUDE [rbac-create](../includes/rbac-create.md)]
- Install the required language runtimes, global tools, and VS Code extensions as described in [Prepare your development environment](../how-to/develop/install-cli-sdk.md).

> [!IMPORTANT]
> Before starting, make sure your development environment is ready.  
> This Quickstart focuses on **scenario-specific steps** like SDK installation, authentication, and running sample code.
>

[!INCLUDE [first-run](../includes/first-run-experience.md)]

## Find your endpoint 

[!INCLUDE [find-endpoint](../default/includes/find-endpoint.md)]

Your prerequisites are all complete.  Jump back to [Set environment variables](#set-environment-variables) to begin.

## Next step
 
> [!div class="nextstepaction"]
> [Idea to prototype - Build and evaluate an enterprise agent](../default/tutorials/developer-journey-idea-to-prototype.md)

:::moniker-end
