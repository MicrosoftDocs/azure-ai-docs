---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

Azure OpenAI GPT Realtime API for speech and audio is part of the GPT-4o model family that supports low-latency, "speech in, speech out" conversational interactions. 

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. Follow the instructions in this article to get started with the Realtime API via WebRTC.

In most cases, use the WebRTC API for real-time audio streaming. The WebRTC API is a web standard that enables real-time communication (RTC) between browsers and mobile applications. Here are some reasons why WebRTC is preferred for real-time audio streaming:
- **Lower latency**: WebRTC is designed to minimize delay, making it more suitable for audio and video communication where low latency is critical for maintaining quality and synchronization.
- **Media handling**: WebRTC has built-in support for audio and video codecs, providing optimized handling of media streams.
- **Error correction**: WebRTC includes mechanisms for handling packet loss and jitter, which are essential for maintaining the quality of audio streams over unpredictable networks.
- **Peer-to-peer communication**: WebRTC allows direct communication between clients, reducing the need for a central server to relay audio data, which can further reduce latency.

Use the [Realtime API via WebSockets](../how-to/realtime-audio-websockets.md) if you need to:
- Stream audio data from a server to a client.
- Send and receive data in real time between a client and server.

WebSockets aren't recommended for real-time audio streaming because they have higher latency than WebRTC.

## Supported models

You can access the GPT real-time models for global deployments in the [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (2024-12-17)
- `gpt-4o-realtime-preview` (2024-12-17)
- `gpt-realtime` (version 2025-08-28)
- `gpt-realtime-mini` (version 2025-10-06)
- `gpt-realtime-mini` (version 2025-12-15)
- `gpt-realtime-1.5` (version 2026-02-23)

Use the `/openai/v1` path in the request URL when calling the Realtime API.

For more information about supported models, see the [models and versions documentation](../../foundry-models/concepts/models-sold-directly-by-azure.md#audio-models).

> [!IMPORTANT]
> Use the GA protocol for WebRTC.
>
> You can still use the beta protocol, but we recommend that you start with the GA Protocol. If you're a current customer, plan to migrate to the GA Protocol. 
>
> This article describes how to use WebRTC with the GA Protocol. We preserve the legacy protocol documentation [here](/previous-versions/azure/foundry-models/realtime-audio-webrtc-legacy).
