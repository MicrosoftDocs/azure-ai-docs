---
title: What is GPT-Live for real-time voice agents?
titleSuffix: Foundry Tools
description: Learn about GPT-Live, a full-duplex voice service that enables natural, bidirectional, phone-call-like conversations instead of turn-based voice interactions.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: overview
ms.date: 08/14/2026
ai-usage: ai-assisted
# Customer intent: As a developer, I want to understand what GPT-Live is and when to use it for real-time voice agents.
---

# What is GPT-Live?

GPT-Live is a full-duplex voice service for building agents that listen and speak at the same time, rather than waiting for one party to finish before the other responds. It's built on the [Voice Live](./voice-live.md) platform, so it inherits Voice Live's fully managed connection model while adding a new conversational experience.

*Full-duplex* means the audio channel carries data in both directions at once, similar to a telephone call: the agent keeps listening while it's speaking, and the user can talk without waiting for a pause. This is in contrast to *half-duplex* systems, like a walkie-talkie or earlier turn-based speech-to-speech models, where only one party can transmit at a time and the other must wait to respond.

GPT-Live marks a shift away from turn-based voice interactions toward natural, bidirectional, phone-call-like conversations. It enables higher-quality, real-time communication that feels as natural as talking to another person.

> [!IMPORTANT]
> GPT-Live is in public preview. Capabilities, APIs, and availability described in this article are subject to change before general availability.

## Why use GPT-Live?

The turn-based pattern of earlier speech-to-speech models can feel unnatural, especially when a user wants to interject, acknowledge, or redirect the conversation mid-response. GPT-Live's goal is a more natural, bidirectional, phone-call-like conversation instead of a turn-based interaction. See [Capabilities](#capabilities) for details.

## GPT-Live and Voice Live

GPT-Live uses Voice Live's fully managed session and connection infrastructure. You don't provision or manage the underlying generative AI model yourself.

## Capabilities

| Capability | Description |
|---|---|
| Full-duplex conversation | Listens and generates a response at the same time, without rigid turn-taking. |
| Natural interruptions | Adapts when a user interrupts, instead of finishing a queued response. |
| Backchanneling | Produces brief listening cues during the user's turn. |
| Delegation | Hands off requests that need search, tool use, or deeper reasoning to a configured backend model while the live session continues. |
| Memory | Maintains context across a conversation for coherent, multi-turn exchanges. |
| Multimodal input | Accepts voice, text, and image input. [TO VERIFY: video input support and timeline.] |
| Output | Voice only. |

## Supported models

| Model | Description |
|---|---|
| `gpt-live-1` | The flagship full-duplex voice model. |
| `gpt-live-1-mini` | A smaller, lower-latency variant intended for higher-volume deployments. |

<!--
## Language support

[TO VERIFY: confirm supported languages/locales and link to a language support page once evaluated, similar to [Voice Live language support](./voice-live-language-support.md).]

## Regions and availability

[TO VERIFY: confirm supported regions.]

## Pricing

[TO VERIFY: confirm pricing and billing model. No pricing is published as of this writing.]

-->

## Related content

- [What is the Voice Live API?](./voice-live.md)
- [Voice Live language support](./voice-live-language-support.md)
