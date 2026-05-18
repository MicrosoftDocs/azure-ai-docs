---
title: GPT Audio 2.0
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/05/2026
ms.custom: include
ai-usage: ai-assisted
---

GPT Audio 2 is an audio-focused model designed for generating, processing, and transforming speech. Unlike realtime models, which operate in a continuous streaming session, GPT Audio 2 is optimized for request/response scenarios.

## When to use GPT Audio 2

Use GPT Audio 2 when you need:

- High-quality audio generation without maintaining a realtime session.
- Lower latency for text-to-speech scenarios.
- Stateless audio APIs for scalable architectures.
- A clean separation between reasoning (handled elsewhere) and speech output.

## How GPT Audio 2 differs from GPT Realtime 2

| Feature | GPT Audio 2 | GPT Realtime 2 |
|---|---|---|
| Interaction type | Request/response (stateless) | Streaming session (stateful) |
| Primary use | Audio generation / TTS | Conversational speech-in/speech-out |
| Reasoning | Not primary | Built-in reasoning |

## Supported modalities

- **Input**: Text
- **Output**: Audio


## Get started

The connection and usage patterns for GPT Realtime Audio 2 are the same as for earlier versions—just deploy the new model and point your existing code at it. Choose the transport that fits your scenario:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)
- [Use the GPT Realtime API via SIP](../how-to/realtime-audio-sip.md)

