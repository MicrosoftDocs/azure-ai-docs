---
title: GPT Realtime Translate
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 05/07/2026
ms.custom: include
ai-usage: ai-assisted
---

GPT Realtime Translate is a continuous, real-time translation model that produces translated output as speech unfolds. Unlike segmented pipeline approaches, it processes live audio as a stream—translating without buffering or segmenting—to enable more natural multilingual interactions.

## Key capabilities

- **Continuous stream processing**: Translates live audio without segmenting or buffering, producing output that tracks the cadence of the original speech.
- **Speech and text output**: Produces both translated speech (audio) and a translated transcript in the target language.
- **Low-latency translation**: Designed to keep pace with real-time conversation, reducing the gap between the original speech and translated output.

## When to use GPT Realtime Translate

Use GPT Realtime Translate when you need:

- Live translation of conversations, meetings, or events across languages.
- Translated audio output for listeners who speak a different language.
- A translated transcript alongside the translated audio for captioning or record-keeping.
- Continuous translation that doesn't break the flow of conversation.

## How GPT Realtime Translate differs from GPT Realtime Whisper

| Feature | GPT Realtime Translate | GPT Realtime Whisper |
|---|---|---|
| Primary function | Cross-language translation | Source-language transcription |
| Output | Translated speech + target-language transcript | Text transcript in the source language |
| Use with other models | Often paired with GPT Realtime Whisper | Often paired with GPT Realtime Translate |

## Use cases

- **Live multilingual events**: Translate conference talks, webinars, or broadcasts in real time so audiences can listen in their preferred language. Pair with GPT Realtime Whisper to simultaneously provide source-language captions.
- **Global customer support**: Route inbound calls through GPT Realtime Translate to bridge language gaps between customers and agents. The translated transcript gives agents a written record in their language for follow-up.
- **International voice assistants**: Build once and deploy across languages. GPT Realtime Translate enables multilingual voice interactions without requiring per-language model deployments.

## Get started

GPT Realtime Translate is available through the Realtime API. The connection and usage patterns are the same as for other realtime models:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)

## Deployment

GPT Realtime Translate is available as a Global Standard deployment in Microsoft Foundry. Deploy the model from the [model catalog](https://ai.azure.com).

[TO VERIFY] Confirm supported languages, regions, and pricing details.
