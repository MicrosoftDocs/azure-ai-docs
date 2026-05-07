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

GPT Realtime Translate is a purpose-built model for continuous, real-time audio translation. Unlike pipeline-based approaches that chunk audio into segments before translating, this model processes audio streams continuously, producing translated output as speech unfolds. It's designed for scenarios where audio is flowing live and latency can't be an afterthought.

## Key capabilities

- **Continuous stream processing**: Translates live audio without segmenting or buffering, producing output that tracks the cadence of the original speech.
- **Speech and text output**: Produces both translated speech (audio) and a translated transcript in the target language.
- **Low-latency translation**: Designed to keep pace with real-time conversation, reducing the gap between the original speech and translated output.

## When to use GPT Realtime Translate

Use GPT Realtime Translate when you need:

- Live streaming events, conferences, and broadcasts requiring real-time multilingual output.
- Cross-language customer support calls.
- Multilingual voice interfaces and applications.
- Live media localization.
- International real-time meetings and collaboration.



## Use cases

- **Live multilingual events**: Translate conference talks, webinars, or broadcasts in real time so audiences can listen in their preferred language. Pair with GPT Realtime Whisper to simultaneously provide source-language captions.
- **Global customer support**: Route inbound calls through GPT Realtime Translate to bridge language gaps between customers and agents. The translated transcript gives agents a written record in their language for follow-up.
- **International voice assistants**: Build once and deploy across languages. GPT Realtime Translate enables multilingual voice interactions without requiring per-language model deployments.

## Using GPT Realtime Translate with other models

GPT Realtime Translate, GPT Realtime Whisper, and GPT Realtime 2 cover different parts of an audio architecture:

- Use **GPT Realtime Translate** when you need continuous real-time translation during live multilingual audio experiences.
- Use **GPT Realtime Whisper** when you need streaming transcription of live audio for captions, monitoring, moderation, or analytics.
- Use **GPT Realtime 2** for live conversational experiences that require streaming audio input and output, stronger instruction following, and reasoning during the interaction.

In a pipeline, GPT Realtime Translate handles live translated output, GPT Realtime Whisper captures the original speech as text for captions, monitoring, or archival purposes, and GPT Realtime 2 supports reasoning or audio generation depending on the application design. Using the models together offers advantages in scalability, flexibility, and latency management, as each model can be optimized independently for its task.

## Get started

GPT Realtime Translate is available through the Realtime API. The connection and usage patterns are the same as for other realtime models:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)

## Deployment and availability

GPT Realtime Translate is available as a Global Standard (pay-as-you-go) deployment in Microsoft Foundry. Deploy the model from the [model catalog](https://ai.azure.com).

- **Access**: Generally available. No gating or access request required.
- **Fine-tuning**: Not supported.
- **Model Router**: Not supported.

[TO VERIFY] Confirm supported languages, regions, and pricing details.
