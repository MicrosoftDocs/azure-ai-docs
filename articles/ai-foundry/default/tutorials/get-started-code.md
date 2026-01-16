---
title: "Quickstart: Chat with a model"
titleSuffix: Microsoft Foundry
description: Get started with Microsoft Foundry SDK building AI applications. 
author: sdgilley
ms.author: sgilley
ms.reviewer: dantaylo
ms.date: 01/16/2026
ms.service: azure-ai-foundry
ms.topic: how-to
ms.custom:
  - dev-focus
ai-usage: ai-assisted
# customer intent: As a developer, I want to start using the Microsoft Foundry portal and client libraries.
---

# Quickstart: Chat with a model

In this quickstart, you use [!INCLUDE [foundry-link](../includes/foundry-link.md)] to interact with a Foundry model, create, and chat with an agent.

## Prerequisites

* A model deployed in Microsoft Foundry. If you don't have one, first complete [Quickstart: Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md).
* The [endpoint for the model](#find-your-endpoint).
* Install the required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).

## Set environment variables and get the code

Store the endpoint as an environment variable. Also set these values for use in your scripts.

```plaintext
PROJECT_ENDPOINT=<endpoint copied from welcome screen>
AGENT_NAME="MyAgent"
MODEL_DEPLOYMENT_NAME="gpt-4.1-mini"
```

[!INCLUDE [quickstart-v2-get-code](../includes/quickstart-v2-get-code.md)]

## Install and authenticate

[!INCLUDE [quickstart-v2-install](../includes/quickstart-v2-install.md)]

## Chat with a model

[!INCLUDE [quickstart-v2-chat](../includes/quickstart-v2-chat.md)]

<!-- ## Create an agent

[!INCLUDE [quickstart-v2-create-agent](../includes/quickstart-v2-create-agent.md)]

## Chat with an agent

[!INCLUDE [quickstart-v2-agent-chat](../includes/quickstart-v2-agent-chat.md)] -->

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]

## Find your endpoint 

[!INCLUDE [find-endpoint](../includes/find-endpoint.md)]
 
Copy the endpoint to use in your [environment variable](#set-environment-variables-and-get-the-code).


## Next step
 
> [!div class="nextstepaction"]
> [Idea to prototype - Build and evaluate an enterprise agent](../tutorials/developer-journey-idea-to-prototype.md)

