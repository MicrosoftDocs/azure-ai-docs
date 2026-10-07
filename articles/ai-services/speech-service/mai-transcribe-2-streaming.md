---
title: MAI-Transcribe-2-Streaming overview - Speech Service
titleSuffix: Foundry Tools
description: Learn about MAI-Transcribe-2-Streaming and choose between the Realtime API and Azure Speech SDK.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: overview
ms.date: 09/30/2026
ms.custom: references_regions
ai-usage: ai-assisted

# Customer intent: As a developer, I want to choose an integration method for transcribing live audio with MAI-Transcribe-2-Streaming.
---

# MAI-Transcribe-2-Streaming overview

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Transcribe-2-Streaming is a low-latency speech-to-text model for real-time transcription. Send audio as a continuous stream and receive incremental transcripts while the speaker talks. Intermediate results update the current transcription, and final results confirm each segment.

The model supports live audio workloads such as call centers, voice assistants, meeting and lecture captioning, voice-driven interfaces, and real-time note taking.

## Choose an integration method

| Integration | Use when | Guide |
| --- | --- | --- |
| Realtime API | Your application uses an OpenAI Realtime-compatible WebSocket integration. | [Use MAI-Transcribe-2-Streaming with the Realtime API](mai-transcribe-2-streaming-realtime.md) |
| Azure Speech SDK | You want a managed client library for connection management, retries, and audio streaming. | [Use MAI-Transcribe-2-Streaming with Azure Speech SDK](mai-transcribe-2-streaming-speech-sdk.md) |

Both integration methods support the `MAI-Transcribe-2-Streaming` model and return intermediate and final transcription results.

## Availability and regions

You can access MAI-Transcribe-2-Streaming globally. Azure serves the model from the following regions and routes requests to them for each integration method.

| Region | Region identifier | Availability |
| --- | --- | --- |
| Sweden Central | `swedencentral` | Available |
| Central US | `centralus` | Available |
| East US 2 | `eastus2` | Available |
| Southeast Asia | `southeastasia` | Available |

## Language support

By default, the model operates in multilingual mode with language auto-detection. The following languages are currently supported:

[!INCLUDE [MAI Transcribe language support](includes/language-support/mai-transcribe.md)]
