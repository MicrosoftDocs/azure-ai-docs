---
title: "Text to speech avatar quickstart - Speech service"
titleSuffix: Foundry Tools
description: Learn how to create an app that converts text to avatar video, and explore supported functions and custom configuration options.
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-speech
ms.topic: quickstart
ms.date: 1/29/2026
ms.author: pafarley
ai-usage: ai-assisted
---

# Quickstart: Text to speech avatar

In this quickstart, you learn how to use text to speech avatar to generate synthetic avatar videos from text input. You can try the feature in the Foundry portal playground and explore both standard avatar video generation and interactive real-time avatars.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you need to create a project, see [Create a Microsoft Foundry project](../../../ai-foundry/how-to/create-projects.md).
- For the current list of regions that support text to speech avatar, see the [Speech service regions table](../regions.md?tabs=ttsavatar).

## Try text to speech avatar video generation

Try text to speech avatar in the Foundry portal by following these steps.

#### [Foundry (new) portal](#tab/new-foundry)

1. [!INCLUDE [foundry-sign-in](../../../ai-foundry/default/includes/foundry-sign-in.md)]
1. Select **Build** from the top right menu.
1. Select **Models** on the left pane.
1. The **AI Services** tab shows the Azure AI models that you can use out of the box in the Foundry portal. Select **Azure Speech - Text to Speech Avatar** to open the Text to Speech Avatar playground.
1. Choose a standard avatar from the Avatar list, and select background and voice.
1. Enter your sample text in the text box.
1. Select **Play audio** to hear the synthetic voice read your text without generating avatar video.
1. Select **Generate** to view the synthetic avatar video.

## Other Foundry (new) features

[!INCLUDE [speech-features-foundry](../../../ai-foundry/default/includes/speech-features-foundry.md)]

#### [Foundry (classic) portal](#tab/classic-foundry)

1. [!INCLUDE [classic-sign-in](../../../ai-foundry/includes/classic-sign-in.md)]
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.
1. Select **Text to speech avatar**.
1. Select an avatar from the avatar list, and select background, language, and voice.
1. Enter your sample text in the text box.
1. Select **Play audio** to hear the synthetic voice read your text without generating avatar video.
1. Select **Generate video** to view the synthetic avatar video.

---

## Try interactive text to speech avatar

Try real-time interactive avatar using Voice Live in the Foundry portal.

1. Open the [Voice Live quickstart](../voice-live-quickstart.md).
1. In Voice Live, after configuring the parameters, turn on the avatar toggle button.
1. Select an avatar from the avatar list.
1. Apply changes and select **Start** to start chatting with the avatar.
