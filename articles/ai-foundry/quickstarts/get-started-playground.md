---
title: Get Answers in Chat Playground - Azure AI Foundry Quickstart
titleSuffix: Azure AI Foundry
description: Get answers using the chat playground in Azure AI Foundry portal. Learn how to deploy models, ask questions, and get AI responses quickly with this step-by-step tutorial.
ms.service: azure-ai-foundry
ms.custom:
  - build-2024
  - ignite-2024
ms.topic: quickstart
ms.date: 08/25/2025
ms.reviewer: zuramir
ms.author: sgilley
monikerRange: 'foundry-classic || foundry'
author: sdgilley
ai-usage: ai-assisted
# customer intent: As a developer, I want use the chat playground in Azure AI Foundry portal so I can work with generative AI.
---

# Quickstart: Get answers in the chat playground

Learn how to get answers using the chat playground in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). This quickstart shows you how to deploy chat models and get AI-powered responses to your questions quickly and easily in the Azure AI Foundry portal.

For this quickstart, you can use either a [!INCLUDE [hub](../includes/hub-project-name.md)] or a [!INCLUDE [fdp](../includes/fdp-project-name.md)]. For more information about the differences between these two project types, see [Project types](../what-is-azure-ai-foundry.md#project-types).


If you don't have an Azure subscription, <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">create one for free</a>.

[!INCLUDE [feature-preview](../includes/first-run-experience.md)]

## Get answers in the playground

Use the [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs) playground to get answers from AI models. In this quickstart, you'll learn how to ask questions and get responses from deployed chat models.

To get answers from your deployed model in the chat playground, follow these steps:

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
