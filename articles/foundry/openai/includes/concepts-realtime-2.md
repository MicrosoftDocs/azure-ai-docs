---
title: GPT Realtime 2.x (preview)
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 05/05/2026
ms.custom: include
ai-usage: ai-assisted
---

The GPT Realtime 2.x series models are speech-to-speech models with built-in reasoning. They accept audio input and produce audio output. They're designed for low-latency, interactive voice experiences where you need stronger instruction following and reasoning than earlier realtime models.

[!INCLUDE [preview-feature](preview-feature.md)]

## What's new in GPT Realtime 2.x

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

Preambles can reduce perceived latency. For example, the model might say, "Let me think about that..." They can also be used for tool announcements or silence fillers. If the model is interrupted during thinking, it discards the current chain of thought and starts a new turn.

### Instruction following

Instruction following is stricter than in earlier realtime models. If your system prompt contains narrow wording (for example, distinguishing "order ID" from "confirmation code"), you might need to broaden or rephrase instructions to match real user phrasing.

## Get started

The connection and usage patterns for GPT Realtime 2.x are the same as for earlier versions. Deploy the new model and point your existing code to it. Choose the transport that fits your scenario:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)
- [Use the GPT Realtime API via SIP](../how-to/realtime-audio-sip.md)

