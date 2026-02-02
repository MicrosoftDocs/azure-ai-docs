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
ms.devlang: cpp
---
# Quickstart: text to speech avatar

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you need to create a project, see [Create a Microsoft Foundry project](../../../ai-foundry/how-to/create-projects.md).
- For the current list of regions that support text to speech avatar, see the [Speech service regions table](../regions.md?tabs=ttsavatar).

  ## Try  text to speech avatar video generation

Try text to speech avatar in the Foundry portal by following these steps:

#### [Foundry (new) portal](#tab/new-foundry)


1. [!INCLUDE [foundry-sign-in](../../../ai-foundry/default/includes/foundry-sign-in.md)]
2. Select **Build** from the top right menu.
3. Select **Models** on the left pane.
4. The **AI Services** tab shows the Azure AI models that can be used out of the box in the Foundry portal. Select **Azure Speech - Text to Speech Avatar** to open the Text to Speech Avatar playground.
5. Choose a standard avatar from the Avatar list, and select background and voice.
6. Enter your sample text in the text box.
7. Select **Play audio** to hear the synthetic voice read your text without generating avatar video.
8. Select **Generate** to view the synthetic avatar video.

## Other Foundry (new) features

[!INCLUDE [speech-features-foundry](../../../ai-foundry/default/includes/speech-features-foundry.md)]

#### [Foundry (classic) portal](#tab/classic-foundry)

1. [!INCLUDE [classic-sign-in](../../../ai-foundry/includes/classic-sign-in.md)]
2. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.
3. Select **Text to speech avatar**.
4. Select an avatar from the avatar list, and select backgound, language and voice.
5. Enter your sample text in the text box.
6. Select **Play audio** to hear the synthetic voice read your text without generating avatar video.
7. Select **Generate video** to view the synthetic avatar video.

  ## Try interactive text to speech avatar 
Try realtime interactive avatar using voice live in the Foundry portal.

1. Open [voice live](../voice-live-quickstart.md)
2. In voice live, after configuring the parameters, turn on the avatar toggle button.
3. Select an avatar from the avatar list.
4. Apply changes and select **Start** to start chatting with the avatar.
