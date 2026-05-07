---
title: GPT Realtime Whisper
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

GPT Realtime Whisper is a low-latency streaming transcription model designed for live audio workflows. It produces transcriptions of the original audio in real time, making it suitable for captioning, monitoring, compliance, and archival scenarios.

## Key capabilities

- **Streaming transcription**: Transcribes live audio as it arrives, without waiting for the utterance to complete.
- **Low latency**: Optimized for real-time scenarios where delays are unacceptable—such as live captions or quality monitoring.
- **Parallel operation**: Runs alongside other realtime models (such as GPT Realtime Translate) to provide source-language transcription in parallel with translation.

## When to use GPT Realtime Whisper

Use GPT Realtime Whisper when you need:

- Real-time captions of live audio in the original spoken language.
- A compliance or quality-review transcript alongside a translated conversation.
- Archival records of the source speech in multilingual workflows.
- Low-latency monitoring of live audio streams.

## How GPT Realtime Whisper differs from GPT Realtime Translate

| Feature | GPT Realtime Whisper | GPT Realtime Translate |
|---|---|---|
| Primary function | Source-language transcription | Cross-language translation |
| Output | Text transcript in the source language | Translated speech and text in the target language |
| Use with other models | Often paired with GPT Realtime Translate | Often paired with GPT Realtime Whisper |

## Use cases

- **Live event captioning**: Provide real-time captions in the speaker's original language during conferences, webinars, or broadcasts.
- **Compliance and quality review**: Capture the original conversation as text for regulatory compliance, quality assurance, or analytics.
- **Multilingual pipelines**: Pair with GPT Realtime Translate to deliver both translated output and a source-language transcript in a single workflow.

## Get started

GPT Realtime Whisper is available through the Realtime API. The connection and usage patterns are the same as for other realtime models:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)

## Deployment

GPT Realtime Whisper is available through Microsoft Foundry. Deploy the model from the [model catalog](https://ai.azure.com).

[TO VERIFY] Confirm supported regions, deployment types, and pricing details.
