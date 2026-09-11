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

[!INCLUDE [preview-feature](../includes/preview-feature.md)]

This article shows how to connect to GPT-Live over WebSocket, configure a session, stream audio, and read the events GPT-Live returns. For an overview of GPT-Live and its capabilities, see [What is GPT-Live?](../concepts/gpt-live.md)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource - [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- An API key or Microsoft Entra ID credentials for authentication. For production applications, use [Microsoft Entra ID](../../../foundry-classic/openai/how-to/managed-identity.md) for enhanced security.
- A deployment of a GPT-Live model (`gpt-live-1` or `gpt-live-1-mini`).

## Connect over WebSocket

Open a WebSocket connection and select the model in the query string. Wait for the `session.started` event before treating the session as ready; the first lifecycle event is `session.started`, not `session.updated`.

```javascript
import WebSocket from "ws";

const ws = new WebSocket(
  "wss://<your-resource-name>.openai.azure.com/openai/v1/live?model=gpt-live-1",
  {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  },
);

ws.on("open", () => {
  ws.send(JSON.stringify({
    type: "session.update",
    event_id: "event_start",
    session: {
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

Don't repeat `model` inside the initial `session.update`; the model comes from the WebSocket URL.

## Session configuration

The initial `session.update` is a strict configuration object; it rejects unknown fields.

| Field | Notes |
|---|---|
| `instructions` | System instructions. Immutable after initialization. |
| `audio.output.voice` | Output voice. Defaults to `marin`. Immutable after initialization. |
| `delegation` | Either `{ type: "client" }` or `{ type: "responses", responses: {...} }`. Omitting this field or setting it to `null` selects client delegation. See [Delegate work in GPT-Live](gpt-live-delegation.md). |

After startup, later `session.update` calls are sparse: omitted fields keep their current values. A successful update produces `session.updated` with the complete public session resource. Only errors echo `event_id`.

## Stream audio

Audio input and output use raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Base64-encode the raw PCM bytes—not a WAV file or another container—and send them in `input_audio.append`. Each sample is two bytes, so the decoded payload must contain an even number of bytes. Raw audio events aren't acknowledged.

```javascript
ws.send(JSON.stringify({
  type: "input_audio.append",
  event_id: "event_audio_1",
  audio: "<base64-encoded-24khz-pcm16le-mono-audio>",
}));
```

GPT-Live streams audio output back as `output_audio.delta` events, using the same PCM16 format, with a server-assigned half-open time range (`start_ms` / `end_ms`). There's no `output_audio.done` event. A gap between output-audio ranges represents omitted silence.

## Read transcripts and turns

`input_transcript.added` and `output_transcript.added` emit complete timed transcript fragments as they become available. Fragment boundaries reflect cadence, not semantic turn boundaries.

`turn.created`, `turn.delta`, and `turn.done` group those fragments into a heuristic user/assistant turn view for applications that want one. Turn events are a projection: they aren't context items and don't change session state.

## Append general session context

Use `session.context.append` to add general text context—such as facts the model should know—to the active session without interrupting the conversation. `content` contains exactly one `input_text` part and is limited to 500 tokens.

```javascript
ws.send(JSON.stringify({
  type: "session.context.append",
  event_id: "event_context_1",
  content: [{
    type: "input_text",
    text: "The user has already accepted the terms.",
  }],
}));
```

## Observe a session with a sideband WebSocket

A trusted application server can attach a second, *sideband* WebSocket to an already-running session to observe events and send commands, without being one of the primary media endpoints. Connect to the existing session's URL; there's no separate `/sideband` path.

```http
GET /v1/live/sess_123 HTTP/1.1
Host: <your-resource-name>.openai.azure.com
Authorization: Bearer <token>
Connection: Upgrade
Upgrade: websocket
```

The sideband connection receives the same JSON server events as the primary connection, and any commands it sends enter the same session stream.

## Close a session gracefully

Send `session.close`, then keep reading events until `session.closed` arrives, and expect the transport to close after that.

```javascript
ws.send(JSON.stringify({
  type: "session.close",
  event_id: "event_close",
}));
```

On close, the service stops accepting new work, drains active delegation and output work, finalizes the current projected turn, emits `session.closed` with cumulative usage, and closes the transport. Shutdown completes when work drains, with a 10-second maximum; new commands are rejected while closing.

## Related content

- [Delegate work in GPT-Live](gpt-live-delegation.md)
- [Use GPT-Live via WebRTC](gpt-live-webrtc.md)
- [GPT-Live event API reference](../gpt-live-reference.md)
