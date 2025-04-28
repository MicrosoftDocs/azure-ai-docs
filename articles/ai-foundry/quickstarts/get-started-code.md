---
title: Get started building a chat app
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to build a custom chat app in Python using the Azure AI SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2024, devx-track-azurecli, devx-track-python, ignite-2024
ms.topic: how-to
ms.date: 04/26/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
zone_pivot_groups: project-type
# customer intent: As a developer, I want to build a custom chat app using the Azure AI SDK.
---


# Get started with the Azure AI Foundry SDK

::: zone pivot="hub-project"

In this quickstart, we walk you through setting up your local development environment with the [Azure AI Foundry](https://ai.azure.com) SDK. We write a prompt, run it as part of your app code, trace the LLM calls being made, and run a basic evaluation on the outputs of the LLM.

> [!TIP]
> The rest of this article shows how to create a **[!INCLUDE [hub](../includes/hub-project-name.md)]**.  Select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article if you want to create a [!INCLUDE [fdp](../includes/fdp-project-name.md)] instead.

## Prerequisites

[!INCLUDE [hub-only-tutorial](../includes/hub-only-tutorial.md)]

* Before you can follow this quickstart, complete the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md) to deploy a **gpt-4o-mini** model into your [!INCLUDE [hub-project-name](../includes/hub-project-name.md)].

### Set up your development environmant

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?tab-python)

1. Make sure you install these packages:

    ```bash
    pip install azure-ai-projects azure-ai-inference azure-identity 
    ```

## Deploy a model

[!INCLUDE [deploy-model](../includes/deploy-model.md)]

7. Once the model is deployed, select **Open in playground** to test your model.

## Build your chat app

Create a file named **chat.py**.  Copy and paste the following code into it.

:::code language="python" source="~/azureai-samples-main/scenarios/projects/basic/chat-simple.py":::

## Insert your connection string

Your project connection string is required to call the Azure OpenAI service from your code. 

Find your connection string in the Azure AI Foundry project you created in the [Azure AI Foundry playground quickstart](../quickstarts/get-started-playground.md).  Open the project, then find the connection string on the **Overview** page.  

:::image type="content" source="../media/quickstarts/azure-ai-sdk/connection-string.png" alt-text="Screenshot shows the overview page of a project and the location of the connection string.":::

Copy the connection string and replace `<your-connection-string-goes-here>` in the **chat.py** file.

## Run your chat script

Run the script to see the response from the model.

```bash
python chat.py
```

## Generate prompt from user input and a prompt template

The script uses hardcoded input and output messages. In a real app you'd take input from a client application, generate a system message with internal instructions to the model, and then call the LLM with all of the messages.

Let's change the script to take input from a client application and generate a system message using a prompt template.

1. Remove the last line of the script that prints a response.

1. Now define a `get_chat_response` function that takes messages and context, generates a system message using a prompt template, and calls a model.  Add this code to your  existing **chat.py** file:

    :::code language="python" source="~/azureai-samples-main/scenarios/projects/basic/chat-template.py" id="chat_function":::

    > [!NOTE]
    > The prompt template uses mustache format.

    The get_chat_response function could be easily added as a route to a FastAPI or Flask app to enable calling this function from a front-end web application.

1. Now simulate passing information from a frontend application to this function.  Add the following code to the end of your **chat.py** file.  Feel free to play with the message and add your own name.

    :::code language="python" source="~/azureai-samples-main/scenarios/projects/basic/chat-template.py" id="create_response":::

Run the revised script to see the response from the model with this new input.

```bash
python chat.py
```


## Next step

> [!div class="nextstepaction"]
> [Add data and use retrieval augmented generation (RAG) to build a custom chat app](../tutorials/copilot-sdk-create-resources.md?pivots=hub-project)

::: zone-end

::: zone pivot="fdp-project"

[!INCLUDE [get-started-fdp](../includes/get-started-fdp.md)]

::: zone-end