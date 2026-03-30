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

The GPT Realtime API is designed to handle real-time, low-latency conversational interactions. It's a great fit for use cases involving live interactions between a user and a model, such as customer support agents, voice assistants, and real-time translators.

Most users of the Realtime API, including applications that use WebRTC or a telephony system, need to deliver and receive audio from an end-user in real time. The Realtime API isn't designed to connect directly to end user devices. It relies on client integrations to terminate end user audio streams.

## Connection methods

You can use the Realtime API via WebRTC, session initiation protocol (SIP), or WebSocket to send audio input to the model and receive audio responses in real time. In most cases, we recommend using the WebRTC API for low-latency real-time audio streaming.

| Connection method | Use case | Latency | Best for |
|-------------------|----------|---------|----------|
| **WebRTC** | Client-side applications | ~100ms | Web apps, mobile apps, browser-based experiences |
| **WebSocket** | Server-to-server | ~200ms | Backend services, batch processing, custom middleware |
| **SIP** | Telephony integration | Varies | Call centers, IVR systems, phone-based applications |

For more information, see:
- [Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)
- [Realtime API via SIP](../how-to/realtime-audio-sip.md)
- [Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)

## Supported models

The GPT real-time models are available for global deployments.
- `gpt-4o-realtime-preview` (version `2024-12-17`)
- `gpt-4o-mini-realtime-preview` (version `2024-12-17`)
- `gpt-realtime` (version `2025-08-28`)
- `gpt-realtime-mini` (version `2025-10-06`)
- `gpt-realtime-mini` (version `2025-12-15`)
- `gpt-realtime-1.5` (`2026-02-23`)

For more information, see the [models and versions documentation](/azure/ai-foundry/foundry-models/concepts/models-sold-directly-by-azure?tabs=global-standard-aoai%2Cstandard-chat-completions%2Cglobal-standard&pivots=azure-openai#audio-models).

The Realtime API supports up to 32,000 input tokens and 4,096 output tokens.

For all Realtime API models, use the GA endpoint format with `/openai/v1` in the URL.
