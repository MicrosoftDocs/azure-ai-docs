---
title: GPT Realtime Translate
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/07/2026
ms.custom: include
ai-usage: ai-assisted
---

GPT Realtime Translate is a purpose-built model for continuous, real-time audio translation. Unlike pipeline-based approaches that chunk audio into segments before translating, this model processes audio streams continuously and produces translated output as speech unfolds. Use it in scenarios where audio is flowing live and latency must be minimal.

## Key capabilities

- **Continuous stream processing**: Translates live audio without segmenting or buffering, producing output that tracks the cadence of the original speech.
- **Speech and text output**: Produces both translated speech (audio) and a translated transcript in the target language.
- **Low-latency translation**: Keeps pace with real-time conversation, reducing the gap between the original speech and translated output.

## When to use GPT Realtime Translate

Use GPT Realtime Translate when you need:

- Live streaming events, conferences, and broadcasts requiring real-time multilingual output.
- Cross-language customer support calls.
- Multilingual voice interfaces and applications.
- Live media localization.
- International real-time meetings and collaboration.


## Example use cases

- **Live multilingual events**: Translate conference talks, webinars, or broadcasts in real time so audiences can listen in their preferred language. Pair with GPT Realtime Whisper to simultaneously provide source-language captions.
- **Global customer support**: Route inbound calls through GPT Realtime Translate to bridge language gaps between customers and agents. The translated transcript gives agents a written record in their language for follow-up.
- **International voice assistants**: Build once and deploy across languages. GPT Realtime Translate enables multilingual voice interactions without requiring per-language model deployments.

## Get started

GPT Realtime Translate is available through the Realtime API. The connection and usage patterns are the same as for other realtime models:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)

## Deployment and availability

GPT Realtime Translate is available as a Global Standard (pay-as-you-go) deployment in Microsoft Foundry. Deploy the model from the [model catalog](https://ai.azure.com).

