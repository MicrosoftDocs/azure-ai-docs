---
title: GPT Realtime 2.x
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 09/21/2026
ms.custom: include
ai-usage: ai-assisted
---

The generally available GPT Realtime 2.x series models are speech-to-speech models with built-in reasoning. They accept audio input and produce audio output. They're designed for low-latency, interactive voice experiences where you need stronger instruction following and reasoning than earlier realtime models.

The current models are:

- `gpt-realtime-2.1` (version `2026-07-07`) is an incremental update to `gpt-realtime-2` with improved silence and noise handling.
- `gpt-realtime-2.1-mini` (version `2026-07-07`) is a new smaller variant in the 2.x series.

Both models support Global Standard and Data Zone Standard deployments. For region-by-region availability, see [Region availability for Foundry Models sold by Azure](../../foundry-models/concepts/models-sold-directly-by-azure-region-availability.md?pivots=standard).

Azure OpenAI bills these models by input, cached input, and output tokens. Image input is billed separately. For current rates, see the **Audio Models** section on the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## GPT Realtime 2.x features

- **Reasoning support** with an adjustable `reasoning.effort` control.
- **Response phases** that distinguish preambles ("commentary") from the final answer ("final_answer").
- **Longer context window** (256,000 tokens).

## Key concepts

### API and transports

Use the GA Realtime API under `/openai/v1`. The WebSocket endpoint has the following format, where the `model` value is your deployment name:

```text
wss://<resource-name>.openai.azure.com/openai/v1/realtime?model=<deployment-name>
```

The GA endpoint doesn't use a date-based API version or an `api-version` query parameter. For complete examples, see [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md) and [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md).

### Audio and voices

For audio sent as Realtime API events, use headerless, mono PCM16 audio sampled at 24 kHz and base64-encode the bytes. WebRTC negotiates audio transport between the client and service.

The supported output voices are `alloy`, `ash`, `ballad`, `coral`, `cedar`, `echo`, `marin`, `sage`, `shimmer`, and `verse`.

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

## Known limitations

Currently, GPT Realtime 2.x models don't support the `truncation` property in the `session.update` payload. To manage token usage and costs in an ongoing conversation, consider using the `conversation.item.truncate` or `conversation.item.delete` events.

Realtime models have separate audio-token and concurrent-session quotas. Review [Azure OpenAI quotas and limits](../quotas-limits.md) before production deployment.

## Get started

The connection and usage patterns for GPT Realtime 2.x are the same as for earlier versions. Deploy the new model and point your existing code to it. Choose the transport that fits your scenario:

- [Use the GPT Realtime API via WebSockets](../how-to/realtime-audio-websockets.md)
- [Use the GPT Realtime API via WebRTC](../how-to/realtime-audio-webrtc.md)
- [Use the GPT Realtime API via SIP](../how-to/realtime-audio-sip.md)

