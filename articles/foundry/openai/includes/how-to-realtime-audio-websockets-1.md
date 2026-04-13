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

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. 

Follow the instructions in this article to get started with the Realtime API via WebSockets. Use the Realtime API via WebSockets in server-to-server scenarios where low latency isn't a requirement.

> [!TIP] 
> In most cases, use the [Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md) for real-time audio streaming in client-side applications such as a web application or mobile app. WebRTC is designed for low-latency, real-time audio streaming and is the best choice for most scenarios.

Use the following table to help you choose the right protocol for your scenario:

| Protocol | Best for | Latency | Complexity |
|----------|----------|---------|------------|
| **WebRTC** | Client-side apps (web, mobile) | Lowest (~50-100ms) | Higher |
| **WebSocket** | Server-to-server, batch processing | Moderate (~100-300ms) | Lower |
| **SIP** | Telephony integration | Varies | Highest |
