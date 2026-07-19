---
title: "Use the GPT Realtime API for speech and audio with Azure OpenAI"
description: "Learn how to use the GPT Realtime API for speech and audio with Azure OpenAI."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 07/13/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
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
- For steps to deploy and use a GPT realtime model over WebSockets, see [the WebSockets quickstart](./realtime-audio-websockets.md#voice-agent-quickstart).
- Try the [WebRTC via HTML and JavaScript example](./realtime-audio-webrtc.md#step-3-optional-create-a-websocket-observercontroller) to get started with the Realtime API via WebRTC.
- [The Azure-Samples/aisearch-openai-rag-audio repo](https://github.com/Azure-Samples/aisearch-openai-rag-audio) contains an example of how to implement RAG support in applications that use voice as their user interface, powered by the GPT realtime API for audio.

## Understand Realtime session types

OpenAI describes three Realtime session patterns:

- **Voice-agent session** (default conversation flow): Use this session for interactive, multimodal assistants that listen, reason, speak, and call tools. In practice, this session is the standard Realtime conversation lifecycle on `/openai/v1/realtime`.
- **Translation session**: Use this session for continuous speech translation. In Azure OpenAI, this session is a dedicated flow on `/openai/v1/realtime/translations`.
- **Transcription session**: Use this session for speech-to-text scenarios when you need transcript deltas from streaming audio.


When you use the GA Realtime event model, `session.update` uses `session.type` to configure conversation-style and transcription-style sessions:

- `realtime` for voice-agent speech-to-speech sessions.
- `transcription` for live transcription sessions.

For implementation guidance:

- For server-to-server setup, see [Use the GPT Realtime API via WebSockets](./realtime-audio-websockets.md).
- For browser-native, low-latency media setup, see [Use the GPT Realtime API via WebRTC](./realtime-audio-webrtc.md).

[!INCLUDE [realtime-audio 2](../includes/how-to-realtime-audio-2.md)]