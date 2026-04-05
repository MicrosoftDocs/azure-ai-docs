---
title: "Use the GPT Realtime API for speech and audio with Azure OpenAI (classic)"
description: "Learn how to use the GPT Realtime API for speech and audio with Azure OpenAI. (classic)"
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.date: 02/11/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
recommendations: false
ai-usage: ai-assisted
zone_pivot_groups: openai-portal-js-python-ts
ROBOTS: NOINDEX, NOFOLLOW
---

# Use the GPT Realtime API for speech and audio (classic)

**Currently viewing:** :::image type="icon" source="../../../foundry/media/yes-icon.svg" border="false"::: **Foundry (classic) portal version** - [Switch to version for the new Foundry portal](../../../foundry/openai/how-to/realtime-audio.md)

[!INCLUDE [realtime-audio 1](../../../foundry/openai/includes/how-to-realtime-audio-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- An Azure OpenAI resource created in a [supported region](#supported-models). For more information, see [Create a resource and deploy a model with Azure OpenAI](create-resource.md).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article. You can deploy the model from the [Foundry model catalog](../../concepts/foundry-models-overview.md) or from your project in Microsoft Foundry portal. 
Here are some of the ways you can get started with the GPT Realtime API for speech and audio:
- For steps to deploy and use a GPT realtime model, see [the real-time audio quickstart](../how-to/realtime-audio.md#quickstart).
- Try the [WebRTC via HTML and JavaScript example](./realtime-audio-webrtc.md#step-3-optional-create-a-websocket-observercontroller) to get started with the Realtime API via WebRTC.
- [The Azure-Samples/aisearch-openai-rag-audio repo](https://github.com/Azure-Samples/aisearch-openai-rag-audio) contains an example of how to implement RAG support in applications that use voice as their user interface, powered by the GPT realtime API for audio.

## Quickstart

Follow the instructions in this section to get started with the Realtime API via WebSockets. Use the Realtime API via WebSockets in server-to-server scenarios where low latency isn't a requirement.

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](../../../foundry/openai/includes/realtime-javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](../../../foundry/openai/includes/realtime-python.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](../../../foundry/openai/includes/realtime-typescript.md)]

::: zone-end

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Microsoft Foundry portal quickstart](../../../foundry/openai/includes/realtime-portal.md)]

::: zone-end

[!INCLUDE [realtime-audio 2](../../../foundry/openai/includes/how-to-realtime-audio-2.md)]
