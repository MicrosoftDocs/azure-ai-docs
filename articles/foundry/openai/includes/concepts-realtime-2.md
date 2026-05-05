---
title: GPT Realtime 2.0
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

GPT Realtime 2 is a speech-to-speech model with built-in reasoning. It accepts audio input and produces audio output. It's designed for low-latency, interactive voice experiences where you need stronger instruction following and reasoning than earlier realtime models.

## What's new in GPT Realtime 2

- **Reasoning support** with an adjustable `reasoning.effort` control.
- **Response phases** that distinguish preambles ("commentary") from the final answer ("final_answer").
- **Longer context window** (256,000 tokens).

## Key concepts

### Reasoning effort

Control reasoning intensity with the `reasoning.effort` session parameter. Valid values are `minimal`, `low`, `medium`, and `high`.

### Preambles and response phases

Realtime responses can include multiple output items per turn. Each item has a `phase` that indicates its role:

| Phase | Description |
|---|---|
| `commentary` | A promptable preamble, often used before longer reasoning. |
| `final_answer` | The final answer after the model completes reasoning. |

Preambles can reduce perceived latency—for example, "Let me think about that…"—and can also be used for tool announcements or silence fillers. If the model is interrupted during thinking, it discards the current chain of thought and starts a new turn.

### Instruction following

Instruction following is stricter than in earlier realtime models. If your system prompt contains narrow wording (for example, distinguishing "order ID" from "confirmation code"), you might need to broaden or rephrase instructions to match real user phrasing.

## Get started

The connection and usage patterns for GPT Realtime 2 are the same as for earlier versions—just deploy the new model and point your existing code at it. Choose the transport that fits your scenario:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)
- [Use the GPT Realtime API via SIP](../how-to/realtime-audio-sip.md)

