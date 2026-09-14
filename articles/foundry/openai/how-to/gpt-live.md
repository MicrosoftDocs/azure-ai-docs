---
title: "Use GPT-Live for real-time voice"
titleSuffix: Microsoft Foundry
description: Learn how to connect to GPT-Live over WebSocket, configure a session, stream audio, and read transcripts and turns.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 09/04/2026
author: PatrickFarley
ms.author: pafarley
recommendations: false
ai-usage: ai-assisted
---

# Use GPT-Live for real-time voice


This article shows how to connect to GPT-Live over WebSocket, configure a session, stream audio, and read the events GPT-Live returns. For an overview of GPT-Live and its capabilities, see [What is GPT-Live?](../concepts/gpt-live.md)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- An API key or Microsoft Entra ID credentials for authentication. For production applications, use [Microsoft Entra ID](../../../foundry-classic/openai/how-to/managed-identity.md) for enhanced security.
- A deployment of the `gpt-live-1` model.

## Connect over WebSocket

Open a WebSocket connection to the live endpoint, then send a `session.start` event with your session configuration. Wait for the `session.started` event before treating the session as ready.

```javascript
import WebSocket from "ws";

const ws = new WebSocket(
  "wss://<your-resource-name>.openai.azure.com/openai/v1/live",
  {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  },
);

ws.on("open", () => {
  ws.send(JSON.stringify({
    type: "session.start",
    event_id: "event_start",
    session: {
      model: "gpt-live-1",
      instructions: "Be concise and ask before taking an external action.",
      audio: { output: { voice: "marin" } },
      delegation: { type: "client" },
    },
  }));
});

ws.on("message", (data) => {
  const event = JSON.parse(data.toString());
  console.log(event.type, event);
});
```

Set `model` in the `session` object of the `session.start` event.

## Session configuration

The `session` object in `session.start` is a strict configuration object; it rejects unknown fields.

| Field | Notes |
|---|---|
| `model` | Required. The GPT-Live model to run, such as `gpt-live-1`. Immutable after startup. |
| `instructions` | System instructions. Immutable after startup; add more with `session.instructions.append`. |
| `audio.output.voice` | Output voice. Defaults to `marin`. Immutable after startup. |
| `delegation` | Either `{ type: "client" }` or `{ type: "responses", responses: {...} }`. Omitting this field or setting it to `null` selects client delegation. See [Delegate work in GPT-Live](gpt-live-delegation.md). |

After startup, later `session.update` calls are sparse: omitted fields keep their current values, and only `delegation.responses` settings can change. A successful update produces `session.updated` with the complete public session resource. Only errors echo `event_id`.

## Stream audio

Audio input and output use raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Base64-encode the raw PCM bytes - not a WAV file or another container - and send them in `session.input_audio.append`. Each sample is two bytes, so the decoded payload must contain an even number of bytes. Raw audio events aren't acknowledged.

```javascript
ws.send(JSON.stringify({
  type: "session.input_audio.append",
  event_id: "event_audio_1",
  audio: "<base64-encoded-24khz-pcm16le-mono-audio>",
}));
```

GPT-Live streams audio output back as `session.output_audio.delta` events, using the same PCM16 format, with a server-assigned half-open time range (`start_ms` / `end_ms`). There's no output-audio-done event. A gap between output-audio ranges represents omitted silence.

## Read transcripts

`session.input_transcript.delta` and `session.output_transcript.delta` emit timed transcript fragments as they become available. Each event contains a `delta` text fragment with a `start_ms` / `end_ms` range on the session timeline. Fragment boundaries reflect audio cadence, not semantic turn boundaries.

Append fragments in order for each speaker. Because listening and speaking can overlap, user and assistant fragments can interleave, a fragment isn't a complete turn, and transcripts can contain mistakes. GPT-Live doesn't emit an authoritative turn-completed event; group fragments into turns in your application if you need that view.

## Add context during the conversation

Feed text into a running session with one of three append events. Each event takes a plain-string `content` of up to 500 tokens and a required `delegation_id`. Use `null` for general session context, or a client delegation ID to update that task.

| Event | Use it for | Acknowledgment |
|---|---|---|
| `session.instructions.append` | Trusted application instructions that change behavior or speech. | `session.instructions.appended` |
| `session.thinking.append` | Quiet context the model can use, but doesn't say on append. | `session.thinking.appended` |
| `session.commentary.append` | Information the model should say aloud, which it may paraphrase. | `session.commentary.appended` |

```javascript
ws.send(JSON.stringify({
  type: "session.thinking.append",
  event_id: "event_context_1",
  delegation_id: null,
  content: "The user has already accepted the terms.",
}));
```

An acknowledgment confirms that context was accepted for injection. It doesn't confirm that the model consumed the update, spoke it, or that any external action succeeded. Quiet context can still influence later speech, so it isn't a place for secrets.

## Observe a session with a sideband WebSocket

A trusted application server can attach a second *sideband* WebSocket to an already running session to observe events and send commands, without being one of the primary media endpoints. Attach to the running session by its ID:

```text
wss://<your-resource-name>.openai.azure.com/openai/v1/live/sessions/{session_id}/attach
```

The session is already running, so don't send `session.start` again. The sideband connection receives the same JSON server events as the primary connection, and any commands it sends enter the same session stream. This is how a server monitors a browser-owned WebRTC session while audio stays on the media track.

## Close a session gracefully

Send `session.close`, then keep reading events until `session.closed` arrives, and expect the transport to close after that.

```javascript
ws.send(JSON.stringify({
  type: "session.close",
  event_id: "event_close",
}));
```

On close, the service stops accepting new work, drains active delegation and output work, and emits `session.closed` with the final cumulative usage and a `reason`. New commands are rejected while closing. Read the final `usage` from `session.closed`; a transport close without that event leaves final usage unconfirmed.

## Related content

- [Delegate work in GPT-Live](gpt-live-delegation.md)
- [Use GPT-Live via WebRTC](gpt-live-webrtc.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
