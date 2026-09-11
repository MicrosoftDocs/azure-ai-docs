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


This article is the full event reference for GPT-Live. For task-based guidance, see [Use GPT-Live for real-time voice](how-to/gpt-live.md) and [Delegate work in GPT-Live](how-to/gpt-live-delegation.md).

## Base namespace

GPT-Live sessions live under `/openai/v1/live` on your Foundry resource endpoint. A WebSocket client connects to `/openai/v1/live` and sends `session.start`. WebRTC sessions are created with `POST /openai/v1/live/sessions`. A server attaches a sideband connection at `/openai/v1/live/sessions/{session_id}/attach`.

## Session configuration

A session begins with a strict configuration object that rejects unknown fields. A WebSocket client sends it in `session.start`; WebRTC session creation sends it as the `session` field of the creation request. Both supply `model` in the session object.

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
| `model` | Required. Set in the session object for both WebSocket `session.start` and WebRTC creation. Immutable after startup. |
| `instructions` | System instructions. Immutable after startup; add more with `session.instructions.append`. |
| `audio.output.voice` | Output voice. Defaults to `marin` and is immutable after startup. |
| `delegation` | Either `{ type: "client" }` or `{ type: "responses", responses: {...} }`. Omitted or `null` selects client delegation. |
| `delegation.responses.service_tier` | Accepts `auto`, `default`, `flex`, or `priority`. |
| `delegation.responses.tools` | Function and hosted tools, including `web_search`, configured as ordinary tool entries. |

### Update a live session

After startup, `session.update` is sparse: omitted fields retain their current values, and only `delegation.responses` settings can change. Delegation is replaced as one complete object—nested delegation fields aren't patched independently. The startup fields `model`, `instructions`, `input`, and `audio` aren't update fields.

A successful update produces `session.updated` with the complete public session resource. Successful acknowledgments don't echo `event_id`; only errors use `client_event_id` for correlation.

## Audio format

WebSocket input and output use raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Base64-encode the raw PCM bytes—not a WAV file or another audio container. Each sample is two bytes, so the decoded payload must contain an even number of bytes.

On WebRTC, audio uses the negotiated media track instead of JSON audio events, and doesn't carry JSON timing fields.

## Client events

| Event | Transport | Description |
|---|---|---|
| `session.start` | WebSocket | Sends the initial session configuration and produces `session.started`. |
| `session.update` | Any JSON stream | Applies a sparse update to `delegation.responses` and produces `session.updated`. |
| `session.input_audio.append` | WebSocket only | Appends non-empty base64 PCM16 mono audio. Not acknowledged. |
| `session.input_audio.mute` / `session.input_audio.unmute` | Any JSON stream | Mutes or unmutes caller input and produces `session.input_audio.muted` / `session.input_audio.unmuted`. |
| `session.instructions.append` | Any JSON stream | Appends trusted instructions and produces `session.instructions.appended`. |
| `session.thinking.append` | Any JSON stream | Appends quiet context and produces `session.thinking.appended`. |
| `session.commentary.append` | Any JSON stream | Appends content for the model to speak and produces `session.commentary.appended`. |
| `response.item.create` | Any JSON stream | With Responses delegation, submits a function result or user message for the backend. |
| `response.create` | Any JSON stream | With Responses delegation, runs or continues the backend response. |
| `session.close` | Any JSON stream | Begins graceful shutdown, produces `session.closed`, then closes the transport. |

The `session.instructions.append`, `session.thinking.append`, and `session.commentary.append` events each take a plain-string `content` of up to 500 tokens and a required `delegation_id`. Use `null` for general session context, or a client delegation ID to update that task.

## Server events

| Event | Description |
|---|---|
| `session.started` | Startup configuration. |
| `session.updated` | A later sparse update was applied; includes the complete public session resource. |
| `session.output_audio.delta` | Timed base64-encoded raw mono 24 kHz signed PCM16 little-endian output audio (WebSocket only). |
| `session.input_transcript.delta` / `session.output_transcript.delta` | A timed input or output transcript fragment. |
| `session.instructions.appended` / `session.thinking.appended` / `session.commentary.appended` | A context append was accepted for injection. |
| `session.input_audio.muted` / `session.input_audio.unmuted` | A mute or unmute command was applied. |
| `session.delegation.created` | GPT-Live created a client- or Responses-targeted unit of delegated work. |
| `response.event` | An envelope carrying a nested Responses delegation event; dispatch on the nested `event.type` and preserve the outer `delegation_id`. |
| `session.usage.updated` | Cumulative session usage, emitted approximately once per minute. |
| `session.closed` | Graceful close completed, including final cumulative usage and a `reason`. |
| `error` | Startup, validation, command, or delegated Responses error; `error.client_event_id` correlates to the failed command. |

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
    "delegation": { "type": "client" }
  }
}
```

### session.output_audio.delta

`start_ms` and `end_ms` use the server timeline, so a gap between ranges represents omitted silence. There's no output-audio-done event.

```json
{
  "type": "session.output_audio.delta",
  "delta": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}
```

### session.input_transcript.delta / session.output_transcript.delta

Each event carries a `delta` fragment with a `start_ms` / `end_ms` range on the session timeline. Fragment boundaries reflect audio cadence, not semantic turn boundaries, and user and assistant fragments can interleave.

```json
{
  "type": "session.input_transcript.delta",
  "delta": "What is the",
  "start_ms": 600,
  "end_ms": 800
}
```

### session.delegation.created

The `delegation` object carries `id`, `type`, and `target`. For client delegation, use `delegation.id` as the `delegation_id` on later `session.commentary.append` or `session.thinking.append` events. For Responses delegation, `response_id` binds the delegation to the Responses lifecycle that follows in `response.event` envelopes. See [Delegate work in GPT-Live](how-to/gpt-live-delegation.md) for the full flow.

```json
{
  "type": "session.delegation.created",
  "offset_ms": 1000,
  "delegation": {
    "id": "item_delegation_123",
    "type": "delegation",
    "target": "client"
  }
}
```

### session.usage.updated / session.closed

`session.usage.updated` reports cumulative voice duration in seconds, along with the context-window usage ratio. These are running snapshots, not increments to sum. `session.closed` carries the final usage and a `reason`.

```json
{
  "type": "session.usage.updated",
  "usage": { "seconds": 12 },
  "context_window": { "usage_ratio": 0.42 }
}
```

```json
{
  "type": "session.closed",
  "reason": "close_requested",
  "usage": { "seconds": 128 }
}
```

The `reason` field explains why the session ended: `close_requested`, `expired`, `content`, `remote_hangup`, or `connection_lost`. Backend token usage is separate; read it from nested `response.completed` events delivered in `response.event`.

## Error handling

All GPT-Live errors use one error envelope. `error.client_event_id` is present only when the error can be correlated to a client command; `param` is omitted when no specific field caused the failure. A startup error prevents `session.started`. A command error doesn't necessarily close an already-started session.

```json
{
  "type": "error",
  "error": {
    "type": "invalid_request_error",
    "code": "invalid_audio",
    "message": "PCM16 audio must contain an even number of bytes",
    "param": "audio",
    "client_event_id": "event_audio_1"
  }
}
```

## Complete WebSocket lifecycle

```text
// 1. Client startup
{ "type": "session.start",
  "session": {
    "model": "gpt-live-1",
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
{ "type": "session.input_audio.append",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>"
}

// 4. Server events may interleave
{ "type": "session.input_transcript.delta",
  "delta": "Hello",
  "start_ms": 600,
  "end_ms": 800
}
{ "type": "session.output_audio.delta",
  "delta": "<base64-encoded-24khz-pcm16le-mono-audio>",
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
