---
title: "GPT-Live event API reference"
titleSuffix: Microsoft Foundry
description: Reference for GPT-Live client and server events, session configuration, audio format, and error handling.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: reference
ms.date: 09/04/2026
author: PatrickFarley
ms.author: pafarley
recommendations: false
ai-usage: ai-assisted
---

# GPT-Live event API reference

[!INCLUDE [preview-feature](../includes/preview-feature.md)]

This article is the full event reference for GPT-Live. For task-based guidance, see [Use GPT-Live for real-time voice](how-to/gpt-live.md) and [Delegate work in GPT-Live](how-to/gpt-live-delegation.md).

## Base namespace

GPT-Live sessions are created under `/openai/v1/live` on your Foundry resource endpoint.

## Session configuration

The initial `session.update` is a strict configuration object: unknown fields are rejected. WebSocket takes `model` from the query string; WebRTC session creation supplies `model` in the session object.

```json
{
  "model": "gpt-live-1",
  "instructions": "Answer briefly and ask before taking an external action.",
  "audio": {
    "output": { "voice": "marin" }
  },
  "delegation": {
    "type": "responses",
    "responses": {
      "model": "gpt-5.5",
      "instructions": "Use tools when current information is required.",
      "max_output_tokens": 2048,
      "service_tier": "priority",
      "reasoning": { "effort": "medium", "summary": "auto" },
      "text": { "verbosity": "low" },
      "tools": [
        { "type": "web_search" },
        {
          "type": "function",
          "name": "get_weather",
          "description": "Get current weather for a location.",
          "parameters": {
            "type": "object",
            "properties": { "location": { "type": "string" } },
            "required": ["location"],
            "additionalProperties": false
          }
        }
      ],
      "tool_choice": "auto",
      "parallel_tool_calls": true
    }
  }
}
```

| Field | Notes |
|---|---|
| `model` | Required when a transport is created. WebSocket uses the query-string value. |
| `instructions` | System instructions. Immutable after initialization. |
| `audio.output.voice` | Output voice. Defaults to `marin` and is immutable after initialization. |
| `delegation` | Either `{ type: "client" }` or `{ type: "responses", responses: {...} }`. Omitted or `null` selects client delegation. |
| `delegation.responses.service_tier` | Accepts `auto`, `default`, `flex`, or `priority`. |
| `delegation.responses.tools` | Function and hosted tools, including `web_search`, configured as ordinary tool entries. |

### Update a live session

After startup, `session.update.session` is sparse: omitted fields retain their current values. Delegation is replaced as one complete object—nested delegation fields aren't patched independently. Set `delegation` to `null` to reset to client delegation. `model` and `include` aren't update fields.

A successful update produces `session.updated` with the complete public session resource. Successful acknowledgments don't echo `event_id`; only errors use `event_id` for correlation.

## Audio format

WebSocket input and output use raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Base64-encode the raw PCM bytes—not a WAV file or another audio container. Each sample is two bytes, so the decoded payload must contain an even number of bytes.

On WebRTC, audio uses the negotiated media track instead of JSON audio events, and doesn't carry JSON timing fields.

## Client events

| Event | Transport | Description |
|---|---|---|
| `session.update` | Any JSON stream | Initial configuration produces `session.started`; later sparse updates produce `session.updated`. |
| `input_audio.append` | WebSocket only | Appends non-empty base64 PCM16 mono audio. Not acknowledged. |
| `session.context.append` | Any JSON stream | Appends general text context and produces `session.context.appended`. |
| `delegation.context.append` | Any JSON stream | Appends text for a prior client-targeted delegation and produces `delegation.context.appended`. |
| `delegation.function_call_output.create` | Any JSON stream | Returns one actionable function result and produces `delegation.function_call_output.created`. |
| `session.close` | Any JSON stream | Begins graceful shutdown, produces `session.closed`, then closes the transport. |

## Server events

| Event | Description |
|---|---|
| `session.started` | Startup configuration. |
| `session.updated` | A later sparse update was applied; includes the complete public session resource. |
| `output_audio.delta` | Timed base64-encoded raw mono 24 kHz signed PCM16 little-endian output audio (WebSocket only). |
| `session.context.appended` | General client context was placed. |
| `delegation.context.appended` | Context for a client delegation was placed. |
| `delegation.function_call_output.created` | A delegated function result was accepted and assigned an output-item ID. |
| `input_transcript.added` / `output_transcript.added` | One complete timed input or output transcript fragment. |
| `turn.created` / `turn.delta` / `turn.done` | A projected transcript turn began, expanded, or reached its final form. |
| `delegation.created` | GPT-Live created a client- or Responses-targeted unit of delegated work. |
| `response.*` | A Responses delegation event emitted top-level without a wrapper, including `response.created`, function-call argument events, and terminal lifecycle events. |
| `session.usage.updated` | Cumulative session usage, emitted approximately once per minute. |
| `session.closed` | Graceful close completed, including final cumulative usage. |
| `error` | Startup, validation, command, or delegated Responses error. |

### session.started

```json
{
  "type": "session.started",
  "session": {
    "id": "sess_123",
    "expires_at": 1782518400,
    "model": "gpt-live-1",
    "instructions": "Be concise.",
    "audio": { "output": { "voice": "marin" } },
    "delegation": { "type": "client" },
    "include": null
  }
}
```

### output_audio.delta

`start_ms` and `end_ms` use the server timeline, so a gap between ranges represents omitted silence. There's no `output_audio.done` event.

```json
{
  "type": "output_audio.delta",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}
```

### input_transcript.added / output_transcript.added

Fragment boundaries reflect cadence, not semantic turn boundaries.

```json
{
  "type": "input_transcript.added",
  "start_ms": 600,
  "end_ms": 800,
  "item": {
    "id": "item_input_transcript_1",
    "type": "input_transcript",
    "text": "What is the"
  }
}
```

### turn.created / turn.delta / turn.done

Turn events are a projection over transcript fragments. They aren't context items and don't change session state.

```json
{
  "type": "turn.done",
  "turn": {
    "id": "turn_123",
    "role": "user",
    "start_ms": 600,
    "end_ms": 1000,
    "transcript": "What is the weather?"
  }
}
```

### delegation.created

For client delegation, the item ID becomes the `delegation_item_id` used by later context appends. For Responses delegation, `response_id` binds the delegation item to the Responses lifecycle that follows. See [Delegate work in GPT-Live](how-to/gpt-live-delegation.md) for the full delegation flow.

### session.usage.updated / session.closed

Reports cumulative token usage approximately once per minute. `session.closed` carries final cumulative usage.

```json
{
  "type": "session.closed",
  "reason": "client_request",
  "usage": {
    "total_tokens": 1640,
    "input_tokens": 960,
    "output_tokens": 680,
    "input_token_details": {
      "text_tokens": 320,
      "audio_tokens": 640,
      "image_tokens": 0,
      "cached_tokens": 100
    },
    "output_token_details": {
      "text_tokens": 280,
      "audio_tokens": 400,
      "image_tokens": 0,
      "cached_tokens": 0
    }
  }
}
```

## Error handling

All GPT-Live errors use one error envelope. `error.event_id` is present only when the error can be correlated to a client event; `param` is omitted when no specific field caused the failure. A startup error prevents `session.started`. A command error doesn't necessarily close an already-started session.

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_audio",
    "message": "PCM16 audio must contain an even number of bytes",
    "param": "audio",
    "event_id": "event_audio_1"
  }
}
```

## Complete WebSocket lifecycle

```text
// 1. Client startup
{ "type": "session.update",
  "session": {
    "instructions": "Be concise.",
    "delegation": { "type": "client" }
  }
}

// 2. Server startup acknowledgment
{ "type": "session.started",
  "session": {
    "id": "sess_123",
    "model": "gpt-live-1",
    "instructions": "Be concise.",
    "audio": { "output": { "voice": "marin" } },
    "delegation": { "type": "client" }
  }
}

// 3. Client audio, repeated as data becomes available
{ "type": "input_audio.append",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>"
}

// 4. Server events may interleave
{ "type": "input_transcript.added",
  "start_ms": 600,
  "end_ms": 800,
  "item": { "id": "item_1", "type": "input_transcript", "text": "Hello" }
}
{ "type": "output_audio.delta",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}

// 5. Client shutdown; keep reading until session.closed
{ "type": "session.close" }
```

## Related content

- [What is GPT-Live?](concepts/gpt-live.md)
- [Use GPT-Live for real-time voice](how-to/gpt-live.md)
- [Delegate work in GPT-Live](how-to/gpt-live-delegation.md)
- [Realtime API reference](realtime-audio-reference.md)
