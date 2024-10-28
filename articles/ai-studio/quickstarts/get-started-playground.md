---
title: Use the chat playground in Azure AI Studio
titleSuffix: Azure AI Studio
description: Use this article to learn how to deploy a chat model and use it in the chat playground in Azure AI Studio.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - build-2024
ms.topic: quickstart
ms.date: 10/22/2024
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
# customer intent: As a developer, I want use the chat playground in Azure AI Studio so I can work with generative AI.
---

# Quickstart: Use the chat playground in Azure AI Studio

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

In this quickstart, you use [Azure AI Studio](https://ai.azure.com) to deploy a chat model and use it in the chat playground in Azure AI Studio.

If you don't have an Azure subscription, <a href="https://azure.microsoft.com/free/cognitive-services" target="_blank">create one for free</a>.

## Prerequisites

- You need permissions to create an Azure AI Studio hub or have one created for you.
    - If your role is **Contributor** or **Owner**, you can follow the steps in this tutorial.
    - If your role is **Azure AI Developer**, the hub must already be created before you can complete this tutorial. Your user role must be **Azure AI Developer**, **Contributor**, or **Owner** on the hub. For more information, see [hubs](../concepts/ai-resources.md) and [Azure AI roles](../concepts/rbac-ai-studio.md).

- Your subscription needs to be below your [quota limit](../how-to/quota.md) to [deploy a new model in this tutorial](#deploy-a-chat-model). Otherwise you already need to have a [deployed chat model](../how-to/deploy-models-openai.md).

## Deploy a chat model

Follow these steps to deploy an Azure OpenAI chat model.

1. Sign in to [Azure AI Studio](https://ai.azure.com) and go to the **Home** page.

1. From the left pane, select **Model catalog**.
    
    :::image type="content" source="../media/tutorials/chat/deploy-create.png" alt-text="Screenshot of the deployments page with a button to create a new deployment." lightbox="../media/tutorials/chat/deploy-create.png":::

1. Select the model you want to deploy from the list of models. For example, select **gpt-4o-mini**. Then select **Confirm**.

    :::image type="content" source="../media/tutorials/chat/deploy-gpt-35-turbo-16k.png" alt-text="Screenshot of the model selection page." lightbox="../media/tutorials/chat/deploy-gpt-35-turbo-16k.png":::

1. On the **Deploy model** page, enter a name for your deployment. 

    * If you're signed in to your project, the model is deployed to that project.  
    * If you aren't in a project, select the project you want to use.  
    * If you don't yet have a project, create one here by assigning a name.

1. Select **Deploy**.
1. Once the model is deployed, select **Open in playground** to test your model.

For more information about deploying models, see [how to deploy models](../how-to/deploy-models-openai.md).

## Chat in the playground without your data

In the [Azure AI Studio](https://ai.azure.com) playground, you can observe how your model responds with and without your data. In this quickstart, you test your model without your data.

To chat with your deployed model in the chat playground, follow these steps:

1. In the **System message** text box, provide this prompt to guide the assistant: "You're an AI assistant that helps people find information." You can tailor the prompt for your scenario. For more information, see [the prompt catalog](../what-is-ai-studio.md#prompt-catalog).
1. Optionally, add a safety system message by selecting the **Add section** button, then **Safety system messages**. Choose from the prebuilt messages, and then edit them to your needs.

1. Select **Apply changes** to save your changes, and when prompted to see if you want to update the system message, select **Continue**. 
1. In the chat session pane, enter the following question: "How much do the TrailWalker hiking shoes cost?"
1. Select the right arrow icon to send.

    :::image type="content" source="../media/tutorials/chat/chat-without-data.png" alt-text="Screenshot of the first chat question without grounding data." lightbox="../media/tutorials/chat/chat-without-data.png":::

1. The assistant either replies that it doesn't know the answer or provides a generic response. For example, the assistant might say, "The price of TrailWalker hiking shoes can vary depending on the brand, model, and where you purchase them." The model doesn't have access to current product information about the TrailWalker hiking shoes. 

    :::image type="content" source="../media/tutorials/chat/assistant-reply-not-grounded.png" alt-text="Screenshot of the assistant's reply without grounding data." lightbox="../media/tutorials/chat/assistant-reply-not-grounded.png":::

Next, you can add your data to the model to help it answer questions about your products. Try the [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md) tutorial to learn more.

## Related content

- [Build a custom chat app in Python using the prompt flow SDK](./get-started-code.md).
- [Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md).
