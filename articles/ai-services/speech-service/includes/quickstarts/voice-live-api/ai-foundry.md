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

In this article, you learn how to use voice live with generative AI and Azure Speech in Foundry Tools in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).

> [!TIP]
> To use voice live, you don't need to deploy an audio model with your Microsoft Foundry resource. Voice live is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [voice live overview documentation](../../../voice-live.md).

## Try out voice live in the Speech playground

#### [Foundry (new) portal](#tab/foundry-new)


To try out the voice live demo, follow these steps:

1. Go to [!INCLUDE [foundry-link](../../../../../ai-foundry/default/includes/foundry-link.md)]. 
1. Select **Build** from the top right menu.
1. Select **Models** on the left pane. 
1. The **AI Services** tab shows the Azure AI models that can be used out of the box in the Foundry portal. **Select Azure Speech - Voice Live** to open the Voice Live playground.
1. Select a scenario and a voice using the dropdown menus. Optionally configure other parameters of the voice agent's behavior. The **Proactive engagement** toggle, for example, allows the agent to speak first in the conversation.
1. When you're ready, select **Start** to start chatting with the voice agent using your device's microphone and speakers.
1. Select **End** to end the chat session.

#### [Foundry (classic) portal](#tab/foundry-classic)

To try out the voice live demo, follow these steps:

1. Go to your project in [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs). 
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

1. Edit other settings as needed, such as the **Response instructions**, **Voice**, and **Speaking rate**. The **Proactive engagement** allows the agent to speak first in the conversation.

1. Select **Start** to start speaking again and select **End** to end the chat session.


---
