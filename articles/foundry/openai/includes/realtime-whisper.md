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

GPT Realtime Whisper is a streaming transcription model designed to convert live audio to text in real time. It can be used alongside speech-to-speech and translation models to provide continuous input transcription for audio streams.

## Key capabilities

- **Streaming transcription**: Transcribes live audio as it arrives, without waiting for the utterance to complete.
- **Low latency**: Optimized for real-time scenarios where delays are unacceptable, such as live captions or quality monitoring.
- **Parallel operation**: Runs alongside other realtime models (such as GPT Realtime Translate) to provide source-language transcription in parallel with translation.

## When to use GPT Realtime Whisper

Use GPT Realtime Whisper when you need:

- Live captions and subtitles for ongoing audio streams.
- Transcription for monitoring, moderation, or analytics workflows.
- Original-language speech captured alongside live translation experiences.
- Text visibility into spoken input while audio is being processed by other models.


## Use cases

- **Live event captioning**: Provide real-time captions in the speaker's original language during conferences, webinars, or broadcasts.
- **Compliance and quality review**: Capture the original conversation as text for regulatory compliance, quality assurance, or analytics.
- **Multilingual pipelines**: Pair with GPT Realtime Translate to deliver both translated output and a source-language transcript in a single workflow.

## Using GPT Realtime Whisper with other models

GPT Realtime Whisper, GPT Realtime Translate, and GPT Realtime 2 cover different parts of an audio architecture:

- Use **GPT Realtime Whisper** when you need streaming transcription of live audio for captions, monitoring, moderation, or analytics.
- Use **GPT Realtime Translate** when you need continuous real-time translation during live multilingual audio experiences.
- Use **GPT Realtime 2** for live conversational experiences that require streaming audio input and output, stronger instruction following, and reasoning during the interaction.

In a pipeline, GPT Realtime Translate handles live translated output, GPT Realtime Whisper captures the original speech as text for captions, monitoring, or archival purposes, and GPT Realtime 2 supports reasoning or audio generation depending on the application design. Using the models together offers advantages in scalability, flexibility, and latency management, as each model can be optimized independently for its task.

## Get started

GPT Realtime Whisper is available through the Realtime API. The connection and usage patterns are the same as for other realtime models:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)

## Deployment and availability

GPT Realtime Whisper is available as a Global Standard (pay-as-you-go) deployment in Microsoft Foundry. Deploy the model from the [model catalog](https://ai.azure.com).

- **Access**: Generally available. No gating or access request required.
- **Fine-tuning**: Not supported.
- **Model Router**: Not supported.

[TO VERIFY] Confirm supported languages, regions, and pricing details.
