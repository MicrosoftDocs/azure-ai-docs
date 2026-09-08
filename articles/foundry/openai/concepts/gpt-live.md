---
title: "What is GPT-Live?"
titleSuffix: Microsoft Foundry
description: Learn about GPT-Live, a full-duplex voice model that enables natural, bidirectional, phone-call-like conversations instead of turn-based voice interactions.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: concept-article
ms.date: 09/04/2026
ai-usage: ai-assisted
# Customer intent: As a developer, I want to understand what GPT-Live is and when to use it for real-time voice agents.
---

# What is GPT-Live?

GPT-Live is a full-duplex voice API for building agents that listen and speak at the same time, rather than waiting for one party to finish before the other responds.

[!INCLUDE [preview-feature](../includes/preview-feature.md)]

*Full-duplex* means the audio channel carries data in both directions at once, similar to a telephone call: the agent keeps listening while it's speaking, and the user can talk without waiting for a pause. This is in contrast to *half-duplex* systems, like a walkie-talkie or turn-based speech-to-speech models such as the [GPT Realtime API](../how-to/realtime-audio.md), where only one party can transmit at a time and the other must wait to respond.

GPT-Live marks a shift away from turn-based voice interactions toward natural, bidirectional, phone-call-like conversations. It enables higher-quality, real-time communication that feels as natural as talking to another person.

## Why use GPT-Live?

The turn-based pattern of earlier speech-to-speech models can feel unnatural, especially when a user wants to interject, acknowledge, or redirect the conversation mid-response. GPT-Live's goal is a more natural, bidirectional, phone-call-like conversation instead of a turn-based interaction. See [Capabilities](#capabilities) for details.

## Capabilities

| Capability | Description |
|---|---|
| Full-duplex conversation | Listens and generates a response at the same time, without rigid turn-taking. |
| Natural interruptions | Adapts when a user interrupts, instead of finishing a queued response. |
| Delegation | Hands off requests that need search, tool use, or deeper reasoning to a configured backend model or to your own application, while the live session continues. See [Delegate work in GPT-Live](../how-to/gpt-live-delegation.md). |
| Multimodal input | Accepts voice, text, and image input. |
| Speech translation | Translates speech across source and target languages and locales. Quality varies by language pair. |
| Output | Voice only. |

## Supported models

| Model | Description |
|---|---|
| `gpt-live-1` | The flagship full-duplex voice model. |
| `gpt-live-1-mini` | A smaller, lower-latency variant intended for higher-volume deployments. |

## Language and translation support

`gpt-live-1` and `gpt-live-1-mini` support speech input and spoken output across all languages and locales. Quality varies by language and locale, with no guarantee of uniform quality or parity with `gpt-realtime-*`.

The models also support speech translation across all source and target languages and locales. Quality varies by language pair, with no guarantee of parity with `gpt-realtime-translation`.

## Connect to GPT-Live

GPT-Live supports three transports:

- **WebSocket**: A trusted backend or middle-tier service connects directly and streams audio as base64-encoded PCM16 events. See [Use GPT-Live for real-time voice](../how-to/gpt-live.md).
- **WebRTC**: Browser or native clients connect with low-latency, negotiated media tracks. See [Use GPT-Live via WebRTC](../how-to/gpt-live-webrtc.md).
- **SIP**: SIP is a supported connection transport. Detailed GPT-Live SIP procedures aren't included yet.

## Related content

- [Use GPT-Live for real-time voice](../how-to/gpt-live.md)
- [Delegate work in GPT-Live](../how-to/gpt-live-delegation.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
- [GPT Realtime API for speech and audio](../how-to/realtime-audio.md)
