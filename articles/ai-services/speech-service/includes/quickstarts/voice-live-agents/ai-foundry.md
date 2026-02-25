---
title: include file
description: include file
author: PatrickFarley
ms.author: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
ms.custom: references_regions
ai-usage: ai-assisted

---

Learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) and [Azure Speech in Foundry Tools](/azure/ai-services/speech-service/overview) in the Microsoft Foundry portal.

[!INCLUDE [Introduction](intro.md)]

<!-- #### [Foundry (new) portal](#tab/foundry-new) -->

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A Foundry agent created in [!INCLUDE [foundry-link](../../../../../ai-foundry/default/includes/foundry-link.md)]. For more information about creating an agent, see the [Create an agent quickstart](/azure/ai-foundry/agents/quickstart).

## Try out Voice Live in the playground

To try out the Voice Live demo, follow these steps:

1. [!INCLUDE [foundry-sign-in](../../../../../ai-foundry/default/includes/foundry-sign-in.md)]

1. Select **Build** in the upper right menu, and select **Agents** from the left pane. 

1. Select the agent you created previously to go to the **Agent playground**.

1. Switch the **Enable Voice Live for this agent** toggle **On**. Your agent now connects to Voice Live.

1. Expand the right pane, which contains the Voice Live settings. Optionally choose a voice, adjust the VAD settings, set the voice temperature and speed, and other settings to configure voice behavior.
 
1. Select **Start** to start speaking and select **End** to end the chat session.

<!-- #### [Foundry (classic) portal](#tab/foundry-classic)

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (classic)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal.
>
> 🔄 [Switch to the Microsoft Foundry (new) documentation](?view=foundry&preserve-view=true) if you're using the new portal.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](/azure/ai-foundry/agents/quickstart).

## Try out Voice Live in the playground

To try out the Voice Live demo, follow these steps:

1. [!INCLUDE [classic-sign-in](../../../../../ai-foundry/includes/classic-sign-in.md)] 
1. Select **Playgrounds** from the left pane.
1. In the **Speech playground** tile, select **Try the Speech playground**.
1. Select **Speech capabilities by scenario** > **Voice Live**.

   :::image type="content" source="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png" alt-text="Screenshot of filtering Speech service capabilities by scenario." lightbox="../../../media/voice-live/foundry-portal/capabilities-by-scenario.png":::

1. Select an agent that you configured in the **Agents** playground.

   :::image type="content" source="../../../media/voice-live/foundry-portal/casual-chat-bring-agent-select.png" alt-text="Screenshot of the option to bring an agent for Voice Live in the speech playground." lightbox="../../../media/voice-live/foundry-portal/casual-chat-bring-agent-select.png":::

1. Edit other settings as needed, such as the **Voice**, **Speaking rate**, and **Voice activity detection (VAD)**.

1. Select **Start** to start speaking and select **End** to end the chat session. 

---

-->
