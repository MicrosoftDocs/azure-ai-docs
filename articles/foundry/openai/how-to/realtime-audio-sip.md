---
title: "Use the GPT Realtime API via SIP"
description: "Learn how to use the GPT Realtime API for speech and audio via SIP."
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/12/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
---

# Use the GPT Realtime API via SIP

[!INCLUDE [realtime-audio-sip 1](../includes/how-to-realtime-audio-sip-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Microsoft Foundry portal, load your project. Select **Build** in the upper right menu, then select the **Models** tab on the left pane, and **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
- Azure role assignment: **Cognitive Services User** or **Cognitive Services Contributor** on your resource.

For the code samples in this article, you also need:

- Python 3.8 or later.
- The following Python packages installed:
  - `openai>=1.0.0` (includes webhook support)
  - `flask>=2.0.0`
  - `websockets>=10.0`
  - `requests`
- An account with a SIP trunking provider (for example, Twilio, Vonage, or Bandwidth).
- A phone number purchased from your SIP provider.

[!INCLUDE [realtime-audio-sip 2](../includes/how-to-realtime-audio-sip-2.md)]
