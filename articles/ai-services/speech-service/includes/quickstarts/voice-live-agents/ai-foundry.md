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

In this article, you learn how to use voice live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) and [Azure Speech in Foundry Tools](/azure/ai-services/speech-service/overview) in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs).

[!INCLUDE [Introduction](intro.md)]

## Prerequisites
<!--
#### [Foundry (new) portal](#tab/foundry-new)

- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).
- A Foundry agent created in [!INCLUDE [foundry-link](../../../../../ai-foundry/default/includes/foundry-link.md)]. For more information about creating an agent, see the [Create an agent quickstart](/azure/ai-foundry/agents/quickstart).


#### [Foundry (classic) portal](#tab/foundry-classic)
-->
- An Azure subscription. <a href="https://azure.microsoft.com/free/ai-services" target="_blank">Create one for free</a>.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [voice live overview documentation](../../../voice-live.md).
- A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](/azure/ai-foundry/agents/quickstart).
<!--
---
-->

> [!TIP]
> To use voice live, you don't need to deploy an audio model with your Microsoft Foundry resource. Voice live is fully managed, and the model is automatically deployed for you. For more information about models availability, see the [voice live overview documentation](../../../voice-live.md).

## Try out voice live in the playground

To try out the voice live demo, follow these steps:

<!--
#### [Foundry (new) portal](#tab/foundry-new)

1. [!INCLUDE [foundry-sign-in](../../../../../ai-foundry/default/includes/foundry-sign-in.md)]

1. Select **Build** in the upper right menu, and select **Agents** from the left pane. 

1. Select the agent you created previously to go to the **Agent playground**.

1. Switch the **Enable voice live for this agent** toggle **On**. Now your agent is connected voice live.

1. Expand the right pane, which contains the voice live settings. Optionally choose a voice, adjust the VAD settings, set the voice temperature and speed, and other settings to configure voice behavior. The **Proactive engagement** toggle allows the agent to speak first in the conversation.
 
1. Select **Start** to start speaking and select **End** to end the chat session.

#### [Foundry (classic) portal](#tab/foundry-classic)
-->
1. [!INCLUDE [classic-sign-in](../../../../../ai-foundry/includes/classic-sign-in.md)] 
1. Select **Playgrounds** from the left pane.
1. In the **Speech playground** tile, select **Try the Speech playground**.
1. Select **Speech capabilities by scenario** > **Voice live**.

   :::image type="content" source="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png" alt-text="Screenshot of filtering Speech service capabilities by scenario." lightbox="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png":::

1. Select an agent that you configured in the **Agents** playground.

   :::image type="content" source="../../../media/voice-live/foundry-portal/casual-chat-bring-agent-select.png" alt-text="Screenshot of the option to bring an agent for voice live in the speech playground." lightbox="../../../media/voice-live/foundry-portal/casual-chat-bring-agent-select.png":::

1. Edit other settings as needed, such as the **Voice**, **Speaking rate**, and **Voice activity detection (VAD)**. The **Proactive engagement** toggle allows the agent to speak first in the conversation.

1. Select **Start** to start speaking and select **End** to end the chat session.

<!--
---
-->