---
title: GPT Realtime Audio 2.0
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/10/2026
ms.custom: include
ai-usage: ai-assisted
---

## What's new in GPT Realtime Audio 2.0

GPT Realtime Audio 2.0 introduces reasoning capabilities and behavioral changes compared to version 1.5. This article describes the key differences to help you plan your migration and take advantage of new features.

## Reasoning controls

GPT Realtime Audio 2.0 adds built-in reasoning to the speech-to-speech audio model. You can control how much reasoning effort the model applies before generating a response by using the new `reasoning.effort` session parameter.

### The reasoning.effort parameter

Set `reasoning.effort` in your [`session.update`](../realtime-audio-reference.md#realtimeclienteventsessionupdate) event to one of the following levels:

| Value | Description |
|---|---|
| `minimal` | Least reasoning effort; fastest response time |
| `low` | Light reasoning effort |
| `medium` | Balanced reasoning and speed (default) [TO VERIFY before GA] |
| `high` | Maximum reasoning depth; slower but more thorough responses |

```json
{
  "type": "session.update",
  "session": {
    "reasoning": {
      "effort": "medium"
    }
  }
}
```

### Reasoning preambles

When the model reasons through a problem, it can surface that process as a *preamble*—an optional audio and text segment that precedes the final spoken response. A single turn can produce multiple preambles; for example, one preamble per tool call in a multi-tool scenario.

Preamble behavior is prompt-controllable. You can adjust your system prompt to encourage or suppress the narration of reasoning.

If a user interrupts the model while it's mid-reasoning, the reasoning chain is discarded and the model restarts from the interruption point.

## Instruction following

GPT Realtime Audio 2.0 is stricter about following instructions than version 1.5. System prompts that performed reliably in version 1.5 might produce different results in version 2.0 and might require reconfiguring for your scenario.

## Expanded context length

The model supports a context window of 256,000 tokens, which is larger than version 1.5. This allows for longer conversations and richer input context without hitting length limits.

## Voice and audio quality

GPT Realtime Audio 2.0 targets several audio quality improvements over version 1.5:

- More natural-sounding synthesized speech
- Higher overall audio output fidelity
