# GPT-Live-1 (Bidi API) — Draft Reference

> **Source materials:** (External) GPT-Live API Alpha Developer Guide; Bidi API [gpt-live-1] Model Reference Doc (updated Jul 14, 2026); KT for Usage Questions re: gpt-live-1 [OMP-1606] (Aug 20, 2026)
>
> **Status:** Limited-access alpha — confidential. Internal testing only; no production traffic permitted.

---

## Overview

**gpt-live-1** is a bidirectional (full-duplex) voice model that lets applications listen and speak simultaneously, eliminating rigid turn-taking boundaries. It processes input continuously while generating output, enabling natural back-and-forth conversation without interruptions.

When a request needs search, deeper reasoning, or more complex work, the model can delegate to a configured Responses API model while the live interaction continues.

| | |
|---|---|
| **What is it?** | Human-like conversation where the model listens and talks simultaneously — no interruptions, no forced turns, modular and flexible |
| **Key goals** | Much stronger and more natural conversations; not yet at the same enterprise capability of tool calling, instruction following, etc. |
| **New features** | Human-like naturalness; no interruptions; simultaneous listen-and-speak; configurable frontend and backend prompts; delegation patterns without rigid turn-taking |
| **Input modalities** | Voice, Text, Image (video to follow) |
| **Output modalities** | Voice |
| **Model size** | GPT-Live-1: d64 (garlic) |
| **Deployment surface** | API only |
| **GA date** | TBD |

### Language and translation support

`gpt-live-1` and `gpt-live-1-mini` support speech input and spoken output across all languages and locales. Quality varies by language and locale, with no guarantee of uniform quality or parity with `gpt-realtime-*`.

The models also support speech translation across all source and target languages and locales. Quality varies by language pair, with no guarantee of parity with `gpt-realtime-translation`.

> **Note:** GPT-Live handles noisy input audio directly, so there's no separate noise-reduction stage. Noise reduction isn't planned for general availability.

### Alpha terms

- This product is strictly confidential.
- Use is limited to low-volume, non-production testing.
- Do not expose generated audio to end users or anyone outside the immediate alpha-testing organization.
- Traffic to the gpt-live model is not billed, but calls delegated to backend text models are billed.
- There is no scheduled date for general availability.
- The model and API shapes will change significantly before general availability.
- Service reliability and latency will not meet production-service standards.

### Early-access requirements

1. Approved customers must schedule a call with the product and research team to share evaluation feedback and results within one week.
2. Internal testing only. No production traffic is permitted.

---

## Integration values

| | |
|---|---|
| **Base namespace** | `/v1/live` |
| **Azure endpoint** | On Azure, connect to `/openai/v1/live` on the resource host—for example, `wss://<resource>.openai.azure.com/openai/v1/live` (WebSocket) and `https://<resource>.openai.azure.com/openai/v1/live` (WebRTC). The code samples in this draft use the OpenAI `api.openai.com/v1/live` host from the external guide. |
| **Required header** | `OpenAI-Alpha: quicksilver=v2` |
| **Authentication** | Project API key on trusted servers |
| **Model slug** | `gpt-live-1-boulder-alpha` — preview of flagship full-duplex voice model |

---

## Architecture: Delegation modes

The Live API supports two delegation modes:

- **Responses delegation:** The service delegates directly to a configured Responses API model. Hosted tools run server-side; client-actionable function calls are returned to the application for completion.
- **Client delegation:** The `gpt-live` model hands work to the application. The client or backend performs the work and appends the resulting context to the live session. Most flexible, but requires more upfront integration work.

Omitted or `null` delegation defaults to client delegation.

---

## Transport options

Clients can connect over **WebSocket**, **WebRTC**, or **SIP**. A trusted backend can also attach a sideband WebSocket to observe events and send commands on an existing session.

- **WebRTC:** Audio uses the negotiated media track; the data channel is for JSON events.
- **WebSocket:** Media travels in JSON audio events.

---

## Quickstart: WebSocket

A trusted WebSocket supplies configuration as its first event. The model is selected in the URL; do not repeat `model` in the initial `session.update`. Wait for `session.started` before treating the session as ready.

```javascript
import WebSocket from "ws";

const ws = new WebSocket(
  "wss://api.openai.com/v1/live?model=gpt-live-1-boulder-alpha",
  {
    headers: {
      Authorization: `Bearer ${process.env.OPENAI_API_KEY}`,
      "OpenAI-Alpha": "quicksilver=v2",
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

### Audio format

WebSocket input and output use raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Base64-encode the raw PCM bytes — not a WAV file or another container — and place them in `input_audio.append.audio`. Each sample is two bytes, so the decoded payload must contain an even number of bytes. The `audio` field in `output_audio.delta` uses the same format.

```javascript
ws.send(JSON.stringify({
  type: "input_audio.append",
  event_id: "event_audio_1",
  audio: "<base64-encoded-24khz-pcm16le-mono-audio>",
}));
```

### Graceful close

```javascript
ws.send(JSON.stringify({
  type: "session.close",
  event_id: "event_close",
}));
```

Send `session.close`, keep reading until `session.closed`, then expect the transport to close.

---

## Connect to the API

### WebSocket connection

```http
GET /v1/live?model=gpt-live-1-boulder-alpha HTTP/1.1
Host: api.openai.com
Authorization: Bearer sk_proj_...
OpenAI-Alpha: quicksilver=v2
Connection: Upgrade
Upgrade: websocket
```

The first lifecycle event is `session.started`, not `session.updated`.

### Unified WebRTC creation

Sends the SDP offer and the canonical session object together. The HTTP response body is the SDP answer and includes `OpenAI-Session-ID`. Audio uses the negotiated media track; the data channel is for JSON events.

```javascript
const pc = new RTCPeerConnection();
pc.addTransceiver("audio", { direction: "sendrecv" });
const dataChannel = pc.createDataChannel("oai-events");

const offer = await pc.createOffer();
await pc.setLocalDescription(offer);

const form = new FormData();
form.set("sdp", offer.sdp);
form.set("session", JSON.stringify({
  model: "gpt-live-1-boulder-alpha",
  instructions: "Be concise.",
  delegation: { type: "client" },
}));

const response = await fetch("https://api.openai.com/v1/live", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${token}`,
    "OpenAI-Alpha": "quicksilver=v2",
    Accept: "application/sdp",
  },
  body: form,
});

const sessionId = response.headers.get("OpenAI-Session-ID");
await pc.setRemoteDescription({
  type: "answer",
  sdp: await response.text(),
});

dataChannel.addEventListener("message", ({ data }) => {
  const event = JSON.parse(data);
  console.log(sessionId, event.type, event);
});
```

> **Note:** Do not set `Content-Type` manually when using `FormData`; the client must include the multipart boundary. Do not send `input_audio.append` on the WebRTC data channel and do not expect `output_audio.delta` there.

### Sideband WebSocket

A trusted application server attaches a sideband WebSocket at the existing session URL; there is no separate `/sideband` path. Sideband receives the same JSON server events as the primary data channel, and its commands enter the same session stream. The alpha selector must exactly match the session.

```http
GET /v1/live/sess_123 HTTP/1.1
Host: api.openai.com
Authorization: Bearer sk_proj_...
OpenAI-Alpha: quicksilver=v2
Connection: Upgrade
Upgrade: websocket
```

---

## Session configuration

Initial configuration is a strict Live API session object — unknown fields are rejected. WebSocket takes `model` from the query string; HTTP creation supplies `model` in the session object.

### Full configuration example

```json
{
  "model": "gpt-live-1-boulder-alpha",
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

### Configuration fields

| Field | Notes |
|---|---|
| `model` | Required when a transport is created. WebSocket uses the query-string value. |
| `instructions` | System instructions. Immutable after initialization. |
| `audio.output.voice` | Output voice. Defaults to `marin`. Immutable after initialization. |
| `delegation` | Either `{ type: "client" }` or `{ type: "responses", responses: {...} }`. Omitted or `null` selects client delegation. |
| `delegation.responses.service_tier` | Accepts `auto`, `default`, `flex`, or `priority`. |
| `delegation.responses.tools` | Function and hosted tools, including `web_search`, configured as ordinary tool entries. |

### Updating a live session

After startup, `session.update.session` is sparse — omitted fields retain their values. Delegation is replaced as one complete object; nested delegation fields are not patched independently. Set `delegation` to `null` to reset to client delegation. `model` and `include` are not update fields.

```json
{
  "type": "session.update",
  "event_id": "event_update",
  "session": {
    "delegation": {
      "type": "responses",
      "responses": {
        "model": "gpt-5.5",
        "tools": [{ "type": "web_search" }],
        "tool_choice": "auto"
      }
    }
  }
}
```

A successful update produces `session.updated` with the complete public session resource. Successful acknowledgments do not echo `event_id`; only errors use `event_id` for correlation.

---

## Delegation: Client

With client delegation, `delegation.created` contains the unit of work and a client-targeted item ID. Use that `id` as `delegation_item_id` when returning context. Each append contains exactly one `input_text` part and is limited to 500 tokens. Repeated appends continue the same delegation stream; they do not create independently addressable context items.

```json
// Server: the gpt-live model delegates work to the application.
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_123",
    "type": "delegation",
    "target": "client",
    "content": [{
      "type": "input_text",
      "text": "What is the weather?"
    }]
  }
}

// Client: return the result as context.
{
  "type": "delegation.context.append",
  "event_id": "event_delegation_context_1",
  "delegation_item_id": "item_delegation_123",
  "content": [{
    "type": "input_text",
    "text": "It is 62 degrees and raining in Seattle."
  }]
}

// Server: acknowledge the placement range.
{
  "type": "delegation.context.appended",
  "delegation_item_id": "item_delegation_123",
  "start_ms": 1200,
  "end_ms": 1600
}
```

`delegation.context.appended` intentionally has no separate context-item ID. The delegation item ID is the stable correlation handle.

---

## Delegation: Responses

With Responses delegation, `delegation.created` identifies the semantic delegation item, `target: "responses"`, and the `response_id` that binds it to the Responses lifecycle. The service emits `delegation.created` immediately before the matching top-level `response.created` event. Do not send `response.create` into the Live API stream.

```json
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_456",
    "type": "delegation",
    "target": "responses",
    "response_id": "resp_123",
    "content": [{
      "type": "input_text",
      "text": "What is the weather?"
    }]
  }
}

{
  "type": "response.created",
  "response": {
    "id": "resp_123",
    "status": "in_progress",
    "model": "gpt-5.5"
  }
}
```

Responses events are passed through at the top level without a `channel.event` wrapper. Dispatch on the complete event type string and tolerate new `response.*` lifecycle events. Delegated output text is also injected into the Live API and can surface as normal transcript, turn, and audio output.

### Complete a client-actionable function call

When `response.function_call_arguments.done` identifies an actionable call, send one `delegation.function_call_output.create` event for that `call_id`. Unknown and already-resolved IDs are rejected; parallel calls require one result event per call.

```json
// Server
{
  "type": "response.function_call_arguments.done",
  "response_id": "resp_123",
  "item_id": "fc_123",
  "output_index": 0,
  "call_id": "call_123",
  "name": "get_weather",
  "arguments": "{\"location\":\"Seattle\"}"
}

// Client
{
  "type": "delegation.function_call_output.create",
  "event_id": "event_function_output_1",
  "item": {
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}

// Server
{
  "type": "delegation.function_call_output.created",
  "item": {
    "id": "item_function_output_123",
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

The acknowledgment means the result was accepted, not that the Responses delegation has completed. Continue reading `response.*` events until the lifecycle reaches a terminal event such as `response.completed` or an error.

---

## Append general session context

Use `session.context.append` to add general text context to the active Live API session. `content` contains exactly one `input_text` part and is limited to 500 tokens. Do not supply an item `id`, `status`, or timing field.

```json
{
  "type": "session.context.append",
  "event_id": "event_context_1",
  "content": [{
    "type": "input_text",
    "text": "The user has already accepted the terms."
  }]
}

{
  "type": "session.context.appended",
  "start_ms": 800,
  "end_ms": 1200
}
```

---

## Output, transcripts, and timing

### Audio output

On WebSocket, `output_audio.delta` carries base64-encoded raw mono 24 kHz signed PCM16 little-endian audio with a server-assigned half-open time range. There is no `output_audio.done` event. A gap between output-audio ranges represents omitted silence; the logical timeline is not compressed when silence is removed.

```json
{
  "type": "output_audio.delta",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}
```

On WebRTC, input and output media are synchronized through RTP and do not carry JSON timing fields. Precise RTP-to-JSON correlation and preservation of logical gaps in outbound RTP timestamps remain follow-up work.

### Transcript items and projected turns

`input_transcript.added` and `output_transcript.added` emit complete timed transcript fragments. Fragment boundaries reflect cadence, not semantic turn boundaries. `turn.created`, `turn.delta`, and `turn.done` provide a heuristic grouping of those fragments for applications that want a user/assistant turn view. Turn events are a projection — they are not context items and do not change session state.

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

{
  "type": "turn.created",
  "turn": {
    "id": "turn_123",
    "role": "user",
    "start_ms": 600,
    "end_ms": 800,
    "transcript": "What is the"
  }
}

{
  "type": "turn.delta",
  "turn_id": "turn_123",
  "start_ms": 800,
  "end_ms": 1000,
  "delta": " weather?"
}

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

---

## Usage and graceful close

`session.usage.updated` reports cumulative voice session usage approximately once per minute, independently of transcript, audio, and delegation traffic. `session.closed` carries final cumulative usage.

On close, the service asks the session to stop, drains active delegation and output work, finalizes the current projected turn, emits `session.closed`, and closes the transport. Shutdown completes when work drains and has a 10-second maximum; new commands are rejected while closing.

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

---

## Event reference

### Client events

| Event | Transport | Description |
|---|---|---|
| `session.update` | Any JSON stream | Initial WebSocket configuration produces `session.started`; later sparse updates produce `session.updated`. |
| `input_audio.append` | WebSocket only | Appends non-empty base64 PCM16 mono audio; no acknowledgment. |
| `session.context.append` | Any JSON stream | Appends general text context and produces `session.context.appended`. |
| `delegation.context.append` | Any JSON stream | Appends text for a prior client-targeted delegation and produces `delegation.context.appended`. |
| `delegation.function_call_output.create` | Any JSON stream | Returns one actionable function result and produces `delegation.function_call_output.created`. |
| `session.close` | Any JSON stream | Begins graceful shutdown, produces `session.closed`, then closes the transport. |

### Server events

| Event | Description |
|---|---|
| `session.started` | Startup configuration. |
| `session.updated` | A later sparse update was applied; includes the complete public session resource. |
| `output_audio.delta` | Timed base64-encoded raw mono 24 kHz signed PCM16 little-endian output audio on WebSocket. |
| `session.context.appended` | General client context was placed. |
| `delegation.context.appended` | Context for a client delegation was placed. |
| `delegation.function_call_output.created` | A delegated function result was accepted and assigned an output-item ID. |
| `input_transcript.added` / `output_transcript.added` | One complete timed input or output transcript fragment. |
| `turn.created` / `turn.delta` / `turn.done` | A projected transcript turn began, expanded, or reached its final form. |
| `delegation.created` | The model created a client- or Responses-targeted unit of delegated work. |
| `response.*` | A Responses delegation event emitted top-level without a wrapper, including `response.created`, function-call argument events, and terminal lifecycle events. |
| `session.usage.updated` | Cumulative session usage, emitted approximately once per minute. |
| `session.closed` | Graceful close completed, including final cumulative usage. |
| `error` | Startup, validation, command, or delegated Responses error. |

---

## Error handling

All Live API and normalized Responses errors use one error envelope. `error.event_id` is present only when the error can be correlated to a client event; `param` is omitted when no specific field caused the failure. A startup error prevents `session.started`. A command error does not necessarily close an already started session.

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

---

## Complete WebSocket lifecycle

```json
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
    "model": "gpt-live-1-boulder-alpha",
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
  "item": {
    "id": "item_1",
    "type": "input_transcript",
    "text": "Hello"
  }
}
{ "type": "output_audio.delta",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}

// 5. Client shutdown; keep reading until session.closed
{ "type": "session.close" }
```

---

## Server event details

### `session.started`

```json
{
  "type": "session.started",
  "session": {
    "id": "sess_123",
    "expires_at": 1782518400,
    "model": "gpt-live-1-boulder-alpha",
    "instructions": "Be concise.",
    "audio": {
      "output": { "voice": "marin" }
    },
    "delegation": { "type": "client" },
    "include": null
  }
}
```

### `session.updated`

```json
{
  "type": "session.updated",
  "session": {
    "id": "sess_123",
    "expires_at": 1782518400,
    "model": "gpt-live-1-boulder-alpha",
    "instructions": "Be concise.",
    "audio": {
      "output": { "voice": "marin" }
    },
    "delegation": { "type": "client" },
    "include": null
  }
}
```

### `output_audio.delta`

Carries base64-encoded raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. `start_ms` and `end_ms` use the server timeline, so a gap between ranges represents omitted silence. There is no `output_audio.done` event.

```json
{
  "type": "output_audio.delta",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>",
  "start_ms": 0,
  "end_ms": 100
}
```

### `session.context.appended`

```json
{
  "type": "session.context.appended",
  "start_ms": 800,
  "end_ms": 1200
}
```

### `delegation.context.appended`

Intentionally has no separate context-item ID.

```json
{
  "type": "delegation.context.appended",
  "delegation_item_id": "item_delegation_123",
  "start_ms": 1200,
  "end_ms": 1600
}
```

### `delegation.function_call_output.created`

```json
{
  "type": "delegation.function_call_output.created",
  "item": {
    "id": "item_function_output_123",
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

### `input_transcript.added`

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

### `output_transcript.added`

Transcript fragment boundaries reflect cadence, not semantic turn boundaries.

```json
{
  "type": "output_transcript.added",
  "start_ms": 800,
  "end_ms": 1000,
  "item": {
    "id": "item_output_transcript_1",
    "type": "output_transcript",
    "text": "It is currently"
  }
}
```

### `turn.created`

```json
{
  "type": "turn.created",
  "turn": {
    "id": "turn_123",
    "role": "user",
    "start_ms": 600,
    "end_ms": 800,
    "transcript": "What is the"
  }
}
```

### `turn.delta`

```json
{
  "type": "turn.delta",
  "turn_id": "turn_123",
  "start_ms": 800,
  "end_ms": 1000,
  "delta": " weather?"
}
```

### `turn.done`

Turn events are a projection over transcript fragments. They are not context items and do not change session state.

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

### `delegation.created`

For client delegation, the item ID becomes the `delegation_item_id` used by later context appends. For Responses delegation, `response_id` binds the semantic delegation item to the Responses lifecycle that follows.

```json
// Client delegation
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_123",
    "type": "delegation",
    "target": "client",
    "content": [{
      "type": "input_text",
      "text": "What is the weather?"
    }]
  }
}

// Responses delegation
{
  "type": "delegation.created",
  "offset_ms": 1000,
  "item": {
    "id": "item_delegation_456",
    "type": "delegation",
    "target": "responses",
    "response_id": "resp_123",
    "content": [{
      "type": "input_text",
      "text": "What is the weather?"
    }]
  }
}
```

### `session.usage.updated`

```json
{
  "type": "session.usage.updated",
  "usage": {
    "total_tokens": 1500,
    "input_tokens": 900,
    "output_tokens": 600,
    "input_token_details": {
      "text_tokens": 300,
      "audio_tokens": 600,
      "image_tokens": 0,
      "cached_tokens": 100
    },
    "output_token_details": {
      "text_tokens": 250,
      "audio_tokens": 350,
      "image_tokens": 0,
      "cached_tokens": 0
    }
  }
}
```

---

## Client event details

### `session.update`

The first WebSocket event supplies startup configuration. The model comes from the WebSocket URL and must not be repeated in the session object. Later updates are sparse; omitted fields retain their values, and replacing delegation requires a complete delegation object.

```json
{
  "type": "session.update",
  "event_id": "event_start",
  "session": {
    "instructions": "Be concise.",
    "audio": {
      "output": { "voice": "marin" }
    },
    "delegation": {
      "type": "client"
    }
  }
}
```

### `input_audio.append`

Appends audio to a WebSocket session. The `audio` field contains base64-encoded raw, headerless, mono, signed 16-bit little-endian PCM sampled at 24,000 Hz. Do not send a WAV header or another container format. The decoded payload must be non-empty and contain an even number of bytes. The server does not acknowledge raw audio events.

```json
{
  "type": "input_audio.append",
  "event_id": "event_audio_1",
  "audio": "<base64-encoded-24khz-pcm16le-mono-audio>"
}
```

### `session.context.append`

Appends general text context to the active session. `content` contains exactly one `input_text` part and is limited to 500 tokens.

```json
{
  "type": "session.context.append",
  "event_id": "event_context_1",
  "content": [
    {
      "type": "input_text",
      "text": "The user has already accepted the terms."
    }
  ]
}
```

### `delegation.context.append`

Returns context for a prior client-targeted delegation. Use the item ID from `delegation.created` as `delegation_item_id`. Each event contains exactly one `input_text` part and is limited to 500 tokens.

```json
{
  "type": "delegation.context.append",
  "event_id": "event_delegation_context_1",
  "delegation_item_id": "item_delegation_123",
  "content": [
    {
      "type": "input_text",
      "text": "It is 62 degrees and raining in Seattle."
    }
  ]
}
```

### `delegation.function_call_output.create`

Returns the result for one client-actionable function call from a Responses-backed delegation. The `call_id` must identify an outstanding call. Parallel calls require one event per result.

```json
{
  "type": "delegation.function_call_output.create",
  "event_id": "event_function_output_1",
  "item": {
    "type": "function_call_output",
    "call_id": "call_123",
    "output": "{\"temperature\":62,\"conditions\":\"rain\"}"
  }
}
```

### `session.close`

Requests graceful shutdown. Continue reading until `session.closed`, then expect the transport to close.

```json
{
  "type": "session.close",
  "event_id": "event_close"
}
```

---

## Model metadata (from Bidi API Model Reference Doc)

| Field | Value |
|---|---|
| **DRI (OpenAI)** | Wenjia You (wenjia@openai.com) |
| **DRI (Microsoft)** | Dave Jacobs (davej@microsoft.com) |
| **Inference engine** | EV3 |
| **Inference code** | `chatgpt/av-app-service/av_app_service` |

### Audio encoder/decoder (alpha A/B testing)

| Component | Identifier |
|---|---|
| Audio decoder | `custom_audio_decoder_ldm_gen2_d8_v1_20260202-2026-02-03-06-17` |
| Image encoder | `custom_lpe:image_lpe_bidi_garlic_20260430-2026-04-30-07-56` |

### Model checkpoints

| Description | Format | Snapshot ID |
|---|---|---|
| Alpha (GPT-Live-1 Front End), VM: `gpt-live-1-boulder-alpha`, Engine group | Research | `az://oaidfw2/oaistrawberry3/twapi/mini/e/rithesh-bigbrain-garlic-d64-sft-20260624-no-convo2-backend-evidence-rewrite-blitz-thinking-slim-v5-wolfiv0-s750-rkld-spv2-20x-no-gate/policy/step_000060/260626163543KQZI4YTD/` |
| Alpha (GPT-Live-1 Front End) | Inference | `garlic-0705-no-vq-surgery-60-8shard-2026-07-06-01-58` (automatic) |

### Backend checkpoints (for traceability only — transferred under separate BOMs)

| Backend | VM | Engine group | Inference snapshot |
|---|---|---|---|
| Instant Free | `chat-free-ev3-gpt55-v4` | `ch-55-v4a` | `big-dipper-c2-s1150-parrot-es8-1150-8shard-2026-05-18-23-29` |
| Instant Paid | `chat-paid-ev3-gpt55-v4` | `ch-55-v4a`, `ch-b-55-v4a` | same as Instant Free |
| Instant Go | `chat-go-ev3-gpt55-v4` | `ch-55-v4a` | same as Instant Free |
| Thinking Medium (juice 16) | `bidi-be-thinking-ev3-gpt55-v1` | `bidi-be-55r-v1a` | `tristan-oseries-spud-br-0331-v1--step-690-2026-04-08-01-08` |
| Thinking High (juice 64) | `bidi-be-thinking-ev3-gpt55-v1` | `bidi-be-55r-v1a` | same as Thinking Medium |

---

*This document was compiled from confidential source materials (GPT-Live API Alpha Developer Guide and Bidi API [gpt-live-1] Model Reference Doc, updated Jul 14, 2026). Internal use only.*
