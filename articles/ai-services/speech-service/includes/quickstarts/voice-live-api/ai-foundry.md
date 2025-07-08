---
title: include file
description: include file
author: eric-urban
ms.author: eur
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/1/2025
ms.custom: references_regions
---

In this article, you learn how to use voice live with generative AI and Azure AI Speech in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- <a href="https://www.python.org/" target="_blank">Python 3.8 or later version</a>. We recommend using Python 3.10 or later, but having at least Python 3.8 is required. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- An [Azure AI Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live API overview documentation](../../../voice-live.md).

> [!TIP]
> To use the Voice Live API, you don't need to deploy an audio model with your Azure AI Foundry resource. The Voice Live API is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [Voice Live API overview documentation](../../../voice-live.md).

## Try out voice live in the Speech playground

To try out the voice live demo, follow these steps:

1. Go to your project in [Azure AI Foundry](https://ai.azure.com/?cid=learnDocs). 
1. Select **Playgrounds** from the left pane.
1. In the **Speech playground** tile, select **Try the Speech playground**.
1. Select **Speech capabilities by scenario** > **Voice live**.

   :::image type="content" source="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png" alt-text="Screenshot of filtering Speech service capabilities by scenario." lightbox="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png":::

1. Select a sample scenario, such as **Casual chat**.

   :::image type="content" source="../../../media/voice-live/foundry-portal/casual-chat-start.png" alt-text="Screenshot of selecting the casual chat example scenario in the Speech playground." lightbox="../../../media/voice-live/foundry-portal/casual-chat-start.png":::

1. Select **Start** to start chatting with the chat agent.

1. Select **End** to end the chat session.

1. Select a new generative AI model from the drop-down list via **Configuration** > **GenAI** > **Generative AI model**. 

   > [!NOTE]
   > You can also select an agent that you configured in the **Agents** playground.

   :::image type="content" source="../../../media/voice-live/foundry-portal/casual-chat-generative-ai-select.png" alt-text="Screenshot of the casual chat example scenario in the Speech playground." lightbox="../../../media/voice-live/foundry-portal/casual-chat-generative-ai-select.png":::

1. Edit other settings as needed, such as the **Response instructions**, **Voice**, and **Speaking rate**.

1. Select **Start** to start speaking again and select **End** to end the chat session.
