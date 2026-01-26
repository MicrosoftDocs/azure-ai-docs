---
author: PatrickFarley
ms.service: azure-ai-speech
ms.custom:
  - ignite-2025
ms.topic: include
ms.date: 11/05/2025
ms.author: pafarley
---

In this quickstart, try out the text to speech model from Azure Speech in Foundry Tools, using [!INCLUDE [foundry-link](../../../../../ai-foundry/default/includes/foundry-link.md)]. 

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Foundry project. If you need to create a project, see [Create a Microsoft Foundry project](../../../../../ai-foundry/how-to/create-projects.md).

## Try text to speech

Try text to speech in the Foundry portal by following these steps:

#### [Foundry (new) portal](#tab/new-foundry)


1. [!INCLUDE [foundry-sign-in](../../../../../ai-foundry/default/includes/foundry-sign-in.md)] 
1. Select **Build** from the top right menu.
1. Select **Models** on the left pane. 
1. The **AI Services** tab shows the Azure AI models that can be used out of the box in the Foundry portal. Select **Azure Speech - Text to Speech** to open the Text to Speech playground.
1. Choose a prebuilt voice from the dropdown menu, and optionally tune it with the provider parameter sliders.
1. Enter your sample text in the text box.
1. Select **Play** to hear the synthetic voice read your text.

## Other Foundry (new) features

[!INCLUDE [speech-features-foundry](../../../../../ai-foundry/default/includes/speech-features-foundry.md)]

#### [Foundry (classic) portal](#tab/classic-foundry)

1. [!INCLUDE [classic-sign-in](../../../../../ai-foundry/includes/classic-sign-in.md)]
1. Select **Playgrounds** from the left pane and then select a playground to use. In this example, select **Try the Speech playground**.

1. Select **Voice gallery**.
1. Select a voice from the gallery. Optionally filter voices by keyword or supported languages.

1. On the right pane, select the **Try it out** tab. Enter sample text in the text box and select **Play** to hear the selected synthetic voice read your text.

1. You can select **View code** to see an SDK code sample in your preferred language for calling the text to speech model.

---