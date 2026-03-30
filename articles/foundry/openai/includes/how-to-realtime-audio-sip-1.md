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

You can use the Realtime API via WebRTC, SIP, or WebSocket to send audio input to the model and receive audio responses in real time. Follow the instructions in this article to get started with the Realtime API via SIP.

Session Initiation Protocol (SIP) is a signaling protocol used to establish, modify, and terminate real‑time communication sessions over IP networks, such as voice calls. With SIP support in the Realtime API, you can route inbound VoIP calls directly into an AI‑powered session for processing.

## Supported models

The GPT real-time models are available for global deployments in [East US 2 and Sweden Central regions](../../foundry-models/concepts/models-sold-directly-by-azure.md#global-standard-model-availability).
- `gpt-4o-mini-realtime-preview` (`2024-12-17`)
- `gpt-4o-realtime-preview` (`2024-12-17` and `2025-06-03`)
- `gpt-realtime` (`2025-08-28`)
- `gpt-realtime-mini` (`2025-10-06`)
- `gpt-realtime-mini` (`2025-12-15`)
- `gpt-realtime-1.5` (`2026-02-23`)
