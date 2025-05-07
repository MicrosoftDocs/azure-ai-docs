---
title: Use the chat playground in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: Use this article to learn how to deploy a chat model and use it in the chat playground in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 04/10/2025
ms.reviewer: zuramir
ms.author: sgilley
author: sdgilley
# customer intent: As a developer, I want use the chat playground in Azure AI Foundry portal so I can work with generative AI.
---

# Quickstart: Use the chat playground in Azure AI Foundry portal

In this quickstart, you use [Azure AI Foundry](https://ai.azure.com) to deploy a chat model and use it in the chat playground in Azure AI Foundry portal.

For this quickstart, you can use either a [!INCLUDE [hub](../includes/hub-project-name.md)] or a [!INCLUDE [fdp](../includes/fdp-project-name.md)]. For more information about the differences between these two project types, see [Project types](../what-is-azure-ai-foundry.md#project-types).


If you don't have an Azure subscription, <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">create one for free</a>.

## Prerequisites

- A subscription below the [quota limit](../how-to/quota.md) to [deploy a new model in this tutorial](#deploy-a-chat-model). Otherwise you already need to have a [deployed chat model](../how-to/deploy-models-openai.md).


## Deploy a chat model

[!INCLUDE [deploy-model](../includes/deploy-model.md)]

7. Once the model is deployed, select **Open in playground** to test your model.

You're now in a project, with a deployed model. You can use the chat playground to interact with your model.

For more information about deploying models, see [how to deploy models](../how-to/deploy-models-openai.md).

## Chat in the playground without your data

In the [Azure AI Foundry](https://ai.azure.com) playground, you can observe how your model responds with and without your data. In this quickstart, you test your model without your data.

To chat with your deployed model in the chat playground, follow these steps:

1. In the **System message** text box, provide this prompt to guide the assistant: "You're an AI assistant that helps people find information." You can tailor the prompt for your scenario.
1. Optionally, add a safety system message by selecting the **Add section** button, then **Safety system messages**. Choose from the prebuilt messages, and then edit them to your needs.

1. Select **Apply changes** to save your changes, and when prompted to see if you want to update the system message, select **Continue**. 
1. In the chat session pane, enter the following question: "How much do the TrailWalker hiking shoes cost?"
1. Select the right arrow icon to send.

    :::image type="content" source="../media/tutorials/chat/chat-without-data.png" alt-text="Screenshot of the first chat question without grounding data." lightbox="../media/tutorials/chat/chat-without-data.png":::

1. The assistant either replies that it doesn't know the answer or provides a generic response. For example, the assistant might say, "The price of TrailWalker hiking shoes can vary depending on the brand, model, and where you purchase them." The model doesn't have access to current product information about the TrailWalker hiking shoes. 

Next, you can add your data to the model to help it answer questions about your products. Try the [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md) tutorial to learn more.

## Related content

- [Build a custom chat app in Python using the Azure AI Foundry SDK](./get-started-code.md).
- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md).
