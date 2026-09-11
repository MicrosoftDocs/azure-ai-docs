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

*Full-duplex* means the audio channel carries data in both directions at once, similar to a telephone call: the agent keeps listening while it's speaking, and the user can talk without waiting for a pause. This is in contrast to *half-duplex* systems, like a walkie-talkie or turn-based speech-to-speech models such as the [GPT Realtime API](../how-to/realtime-audio.md), where only one party can transmit at a time and the other must wait to respond.

GPT-Live marks a shift away from turn-based voice interactions toward natural, bidirectional, phone-call-like conversations. It enables higher-quality, real-time communication that feels as natural as talking to another person.

## Why use GPT-Live?

The turn-based pattern of earlier speech-to-speech models can feel unnatural, especially when a user wants to interject, acknowledge, or redirect the conversation mid-response. GPT-Live's goal is a more natural, bidirectional, phone-call-like conversation instead of a turn-based interaction. See [Capabilities](#capabilities) for details.

## How GPT-Live works

GPT-Live splits a voice application into two parts:

- **The live voice model** handles the spoken conversation. It listens, speaks, decides when to respond, and decides when to hand off work. You steer this behavior with a short set of session instructions that cover conversational style and when to delegate.
- **A backend** handles delegated reasoning, lookups, tool selection, and longer-running tasks. Hosted tools can run through a configured Responses API backend, while your application executes private functions and remains responsible for permissions, user confirmations, business records, and durable task state.

Your application owns everything outside the spoken exchange: permissions, confirmations, tool execution, business records, and durable task state. Because the live model can keep talking while backend work runs, interrupting speech doesn't cancel that work. Your application decides whether to finish, change, or cancel it.

For guidance on splitting instructions between the voice model and the backend, see [Delegate work in GPT-Live](../how-to/gpt-live-delegation.md).

## Capabilities

| Capability | Description |
|---|---|
| Full-duplex conversation | Listens and generates a response at the same time, without rigid turn-taking. |
| Natural interruptions | Adapts when a user interrupts, instead of finishing a queued response. |
| Delegation | Hands off requests that need search, tool use, or deeper reasoning to a configured backend model or to your own application, while the live session continues. See [Delegate work in GPT-Live](../how-to/gpt-live-delegation.md). |
| Multimodal input | Accepts voice and text input. |
| Speech translation | Translates speech across source and target languages and locales. Quality varies by language pair. |
| Output | Voice only. |

## Supported models

| Model | Description |
|---|---|
| `gpt-live-1` | The flagship full-duplex voice model. |

## Language and translation support

`gpt-live-1`supports multilingual speech and can be used for speech-translation experiences. Quality varies by language and locale, with no guarantee of uniform quality or parity with `gpt-realtime-*`.

The models also support speech translation across all source and target languages and locales. Quality varies by language pair, with no guarantee of parity with `gpt-realtime-translation`.

## Connect to GPT-Live

GPT-Live supports three transports:

- **WebSocket**: A trusted backend or middle-tier service connects directly and streams audio as base64-encoded PCM16 events. It also supports 16/24-kHz PCM, 8-kHz, G.711, μ-law, and A-law. See [Use GPT-Live for real-time voice](../how-to/gpt-live.md).
- **WebRTC**: Browser or native clients connect with low-latency, negotiated media tracks. See [Use GPT-Live via WebRTC](../how-to/gpt-live-webrtc.md).

## Choose a voice architecture

GPT-Live is one of several ways to build a voice experience. Choose based on how speech connects to reasoning and tools.

| Architecture | Best for | Why choose it |
|---|---|---|
| GPT-Live | Full-duplex conversations with a separate backend | You choose the voice model and the backend that reasons and uses tools independently, and the conversation continues while backend work runs. |
| [GPT Realtime API](../how-to/realtime-audio.md) | Speech, reasoning, and tool use in one turn-based model | One model interprets audio, decides what to do, and responds in speech. |
| Chained pipeline | Full control over each speech and text stage | Speech-to-text, your own agent, and text-to-speech run as separate stages that you can inspect or replace. |

## Context management in long conversations

GPT-Live manages conversation context automatically as a session grows; you don't set a parameter to enable it. The instructions you provide at session start are preserved for the life of the session.

As the conversation approaches the context window limit, GPT-Live summarizes older history in the background and continues within the same session. Older details can be summarized or dropped, so keep important facts, confirmed actions, and current task state in your application and supply relevant context when it's needed.

## Speech and task work run independently

Because GPT-Live is full duplex, the spoken conversation and delegated backend work proceed on separate tracks:

- Interrupting the assistant's speech stops it from talking, but doesn't cancel work already running in the backend. "Stop talking" and "Cancel my order" are different intents.
- A completed backend response doesn't mean the user heard the answer. Verify spoken confirmations against your application's authoritative state.
- Transcript fragments reflect audio cadence, not complete turns. A fragment isn't a finished user turn, user and assistant text can overlap, and transcripts can contain mistakes.

## Cost model

GPT-Live bills the voice conversation separately from the backend that reasons and uses tools:

- The **voice session** covers the spoken conversation, including silence and time when the backend is working.
- The **backend** model and tool usage is billed the same as an application without voice.

Session usage is reported as a cumulative running total, so read the latest usage value rather than adding snapshots together. For current rates, see the [Azure OpenAI pricing page](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Limits

The GPT-Live API limits the number of concurrent sessions per subscription based on your tier. For the per-tier values, see [GPT-Live concurrent session limits](../quotas-limits.md#gpt-live-concurrent-session-limits).

## Related content

- [Use GPT-Live for real-time voice](../how-to/gpt-live.md)
- [Delegate work in GPT-Live](../how-to/gpt-live-delegation.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
- [GPT Realtime API for speech and audio](../how-to/realtime-audio.md)
