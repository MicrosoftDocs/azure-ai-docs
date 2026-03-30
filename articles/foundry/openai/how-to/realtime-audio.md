---
title: "Use the GPT Realtime API for speech and audio with Azure OpenAI"
description: "Learn how to use the GPT Realtime API for speech and audio with Azure OpenAI."
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
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
zone_pivot_groups: openai-portal-js-python-ts-cs
---

# Use the GPT Realtime API for speech and audio

[!INCLUDE [realtime-audio 1](../includes/how-to-realtime-audio-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal) in one of the [supported regions](#supported-models).
- An API key or Microsoft Entra ID credentials for authentication. For production applications, we recommend using [Microsoft Entra ID](../../../foundry-classic/openai/how-to/managed-identity.md) for enhanced security.
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article.
    - In the Microsoft Foundry portal, load your project. Select **Build** in the upper right menu, then select the **Models** tab on the left pane, and **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.

Here are some of the ways you can get started with the GPT Realtime API for speech and audio:
- For steps to deploy and use a GPT realtime model, see [the real-time audio quickstart](../how-to/realtime-audio.md#quickstart).
- Try the [WebRTC via HTML and JavaScript example](./realtime-audio-webrtc.md#step-3-optional-create-a-websocket-observercontroller) to get started with the Realtime API via WebRTC.
- [The Azure-Samples/aisearch-openai-rag-audio repo](https://github.com/Azure-Samples/aisearch-openai-rag-audio) contains an example of how to implement RAG support in applications that use voice as their user interface, powered by the GPT realtime API for audio.

## Quickstart

Follow the instructions in this section to get started with the Realtime API via WebSockets. Use the Realtime API via WebSockets in server-to-server scenarios where low latency isn't a requirement.

::: zone pivot="programming-language-javascript"

[!INCLUDE [JavaScript quickstart](../includes/realtime-javascript.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python quickstart](../includes/realtime-python.md)]

::: zone-end

::: zone pivot="programming-language-typescript"

[!INCLUDE [TypeScript quickstart](../includes/realtime-typescript.md)]

::: zone-end

::: zone pivot="ai-foundry-portal"

[!INCLUDE [Microsoft Foundry portal quickstart](../includes/realtime-portal.md)]

::: zone-end

::: zone pivot="programming-language-csharp"

[!INCLUDE [C# quickstart](../includes/realtime-csharp.md)]

::: zone-end

[!INCLUDE [realtime-audio 2](../includes/how-to-realtime-audio-2.md)]
