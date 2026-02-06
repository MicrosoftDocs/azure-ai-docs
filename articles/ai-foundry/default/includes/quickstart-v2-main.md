---
title: Include file
description: Include file
author: sdgilley
ms.reviewer: sgilley
ms.author: sgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 01/19/2026
ms.custom: include
---


In this quickstart, you use [!INCLUDE [foundry-link](../includes/foundry-link.md)] to interact with a Foundry model, create, and chat with an agent.


## Prerequisites

* A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../tutorials/quickstart-create-foundry-resources.md).
* The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).

## Set environment variables and get the code

Store [your project endpoint](../tutorials/quickstart-create-foundry-resources.md#get-your-project-connection-details) as an environment variable. Also set these values for use in your scripts.

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

## Create an agent

[!INCLUDE [quickstart-v2-create-agent](../includes/quickstart-v2-create-agent.md)]

## Chat with an agent

[!INCLUDE [quickstart-v2-agent-chat](../includes/quickstart-v2-agent-chat.md)]

## Clean up resources

[!INCLUDE [clean-up-resources](../includes/clean-up-resources.md)]


## Next steps

> [!div class="nextstepaction"]
> [Idea to prototype - Build and evaluate an enterprise agent](../tutorials/developer-journey-idea-to-prototype.md)

> [!div class="nextstepaction"]
> [Evaluate your agent for quality and safety](../../how-to/develop/evaluate-agent.md)

