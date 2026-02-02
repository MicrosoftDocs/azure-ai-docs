---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 7/31/2025
ms.custom: references_regions
---

In this article, you learn how to use voice live with generative AI and Azure AI Speech in the [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs).

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- An [Azure AI Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).

> [!TIP]
> To use voice live, you don't need to deploy an audio model with your Azure AI Foundry resource. Voice live is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [voice live overview documentation](../../../voice-live.md).

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
   > You can also select an agent that you configured in the **Agents** playground. For more information, see the [voice live with Foundry agents quickstart](/azure/ai-services/speech-service/voice-live-agents-quickstart).

   :::image type="content" source="../../../media/voice-live/foundry-portal/casual-chat-generative-ai-select.png" alt-text="Screenshot of the casual chat example scenario in the Speech playground." lightbox="../../../media/voice-live/foundry-portal/casual-chat-generative-ai-select.png":::

1. Edit other settings as needed, such as the **Response instructions**, **Voice**, and **Speaking rate**.

1. Select **Start** to start speaking again and select **End** to end the chat session.
