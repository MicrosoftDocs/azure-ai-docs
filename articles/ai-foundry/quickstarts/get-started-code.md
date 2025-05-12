---
title: Get started with the Azure AI Foundry
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to start using the Azure AI Foundry portal and the Azure AI Foundry SDK.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom: build-2024, devx-track-azurecli, devx-track-python, ignite-2024
ms.topic: how-to
ms.date: 05/12/2025
ms.reviewer: dantaylo
ms.author: sgilley
author: sdgilley
zone_pivot_groups: project-type
# customer intent: As a developer, I want to build a custom chat app using the Azure AI SDK.
---


# Get started with the Azure AI Foundry

::: zone pivot="hub-project"

In this quickstart, we walk you through setting up your local development environment with the [Azure AI Foundry](https://ai.azure.com) SDK. We write a prompt, run it as part of your app code, trace the LLM calls being made, and run a basic evaluation on the outputs of the LLM.

> [!TIP]
> The rest of this article shows how to use a **[!INCLUDE [hub](../includes/hub-project-name.md)]**.  Select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article if you want to use a [!INCLUDE [fdp](../includes/fdp-project-name.md)] instead.

## Prerequisites

- An [Azure subscription](https://azure.microsoft.com/free/). If you don't have an Azure subscription, create a free account before you begin.
- A [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. If you're new to Azure AI Foundry and don't have a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)], select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article to use a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)] instead.

## Set up your development environment

1. [Set up your development environment](../how-to/develop/install-cli-sdk.md?pivots=programming-language-python)

1. Make sure you install these packages:

    ```bash
    pip install azure-ai-projects azure-ai-inference azure-identity 
    ```

## Deploy a model

[!INCLUDE [tip-left-pane](../includes/tip-left-pane.md)]

1. Sign in to [Azure AI Foundry](https://ai.azure.com).
1. Select a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)]. If you don't have a [!INCLUDE [hub-project-name](../includes/hub-project-name.md)], select **[!INCLUDE [fdp](../includes/fdp-project-name.md)]** at the top of this article to use a [!INCLUDE [fdp-project-name](../includes/fdp-project-name.md)] instead.

1. Select **Model catalog** from the left pane.

1. Select the **gpt-4o-mini** model from the list of models. You can use the search bar to find it. 

1. On the model details page, select **Deploy**.

    :::image type="content" source="../media/tutorials/chat/deploy-model.png" alt-text="Screenshot of the model details page with a button to deploy the model." lightbox="../media/tutorials/chat/deploy-model.png":::


1. Leave the default **Deployment name**. Select **Deploy**.

1. Once the model is deployed, select **Open in playground** to test your model.

## Build your chat app

Create a file named **chat.py**.  Copy and paste the following code into it.

:::code language="python" source="~/azureai-samples-main/scenarios/projects/basic/chat-simple.py":::

## Insert your connection string

Your project connection string is required to call the Azure OpenAI in Azure AI Foundry Models from your code. 

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
> [Add data and use retrieval augmented generation (RAG) to build a custom chat app](../tutorials/copilot-sdk-create-resources.md)

::: zone-end

::: zone pivot="fdp-project"

[!INCLUDE [get-started-fdp](../includes/get-started-fdp.md)]

::: zone-end
