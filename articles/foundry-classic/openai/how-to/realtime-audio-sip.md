---
title: "Use the GPT Realtime API via SIP (classic)"
description: "Learn how to use the GPT Realtime API for speech and audio via SIP. (classic)"
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
recommendations: false
ai-usage: ai-assisted

ROBOTS: NOINDEX, NOFOLLOW
---

# Use the GPT Realtime API via SIP (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/realtime-audio-sip.md)

[!INCLUDE [realtime-audio-sip 1](../../../foundry/openai/includes/how-to-realtime-audio-sip-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../concepts/foundry-models-overview.md) or from your project in Microsoft Foundry portal.
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

[!INCLUDE [realtime-audio-sip 2](../../../foundry/openai/includes/how-to-realtime-audio-sip-2.md)]
