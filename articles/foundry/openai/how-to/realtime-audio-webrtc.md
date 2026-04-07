---
title: "Use the GPT Realtime API via WebRTC"
description: "Learn how to use the GPT Realtime API for speech and audio via WebRTC."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 01/29/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
---

# Use the GPT Realtime API via WebRTC

[!INCLUDE [realtime-audio-webrtc 1](../includes/how-to-realtime-audio-webrtc-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Foundry portal, load your project. Select **Build** in the upper-right menu, then select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.

[!INCLUDE [realtime-audio-webrtc 2](../includes/how-to-realtime-audio-webrtc-2.md)]
