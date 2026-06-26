---
title: "Build a voice agent with hosted agents (preview)"
description: "Build and deploy a real-time voice agent on Foundry Agent Service using the invocations_ws WebSocket protocol."
author: aahill
ms.author: aahi
ms.date: 05/18/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: references_regions
ai-usage: ai-assisted
---

# Build a voice agent with hosted agents (preview)

Hosted agents in Foundry Agent Service support real-time voice workloads through the **`invocations_ws`** WebSocket protocol. This article shows you how to choose a voice framework, expose the WebSocket endpoint from your container, and connect a client.

For background on hosted agents and the available protocols, see [What are hosted agents?](../concepts/hosted-agents.md). For general container packaging and deployment steps, see [Deploy a hosted agent](deploy-hosted-agent.md).

> [!IMPORTANT]
> The `invocations_ws` protocol is in public preview. The `invocations_ws` protocol is currently available only in **North Central US**. Features and limits can change.

## When to use the WebSocket protocol

Real-time voice agents need bidirectional streaming: the client and the agent send and receive audio simultaneously over a persistent connection. The `invocations_ws` protocol provides a single full-duplex WebSocket between the caller and your container, with text and binary frames relayed end-to-end.

Use `invocations_ws` when you need to:

- Stream microphone audio (for example, 20 ms PCM frames at 16 kHz) to the agent and stream synthesized speech back.
- Run a speech-to-speech or cascaded speech pipeline (STT → LLM → TTS) inside the container.
- Carry interleaved control messages (JSON) and media (binary) on the same connection.
- Use WebSocket signaling to set up a WebRTC media connection that your application manages.
- Bridge a telephony provider (for example, Twilio) that streams call audio over WebSocket.

For request/response style invocations, continue to use the HTTP [`/invocations`](deploy-hosted-agent.md#protocol-libraries) or `/responses` routes. A single container can expose all three protocols at the same time.

## Endpoint and frame semantics

The container exposes one WebSocket route:

```
GET /invocations_ws
Upgrade: websocket
Connection: Upgrade
```

Public endpoint (single literal path; `project_name`, `agent_name`, and `agent_session_id` are passed as query string parameters):

```
wss://<account>.services.ai.azure.com/api/projects/agents/endpoint/protocols/invocations_ws
    ?project_name=<project>
    &agent_name=<agent>
    &agent_session_id=<session-id>
    &foundry_features=HostedAgents=V1Preview
```

The platform consumes `project_name`, `agent_name`, and `foundry_features` at the APIM and Agents-service layers to route the upgrade and gate the preview. They don't appear on the upgrade the container receives. Any other query parameters you add are forwarded unchanged.

The preview flag is required while the protocol is in preview. You can supply it either as the `foundry_features=HostedAgents=V1Preview` query parameter (shown above) or as the `Foundry-Features: HostedAgents=V1Preview` request header on the upgrade, which is the same flag used by HTTP `/invocations`.

The platform proxies the WebSocket upgrade transparently. Frames flow between the caller and your container as raw bytes—the platform doesn't parse, transform, or buffer them at the application layer.

| Frame type | Supported | Typical use |
|------------|-----------|-------------|
| Text (UTF-8) | Yes | JSON control messages |
| Binary | Yes | Audio (PCM/Opus), images, other non-text payloads |
| Continuation | Yes | RFC 6455 fragmented messages relayed unchanged |
| Ping / Pong | Yes | Keep-alive (your container sends Pings; the proxy doesn't generate its own) |
| Close | Yes | Standard RFC 6455 close codes |

**Frame size limit.** The platform proxy enforces a **1 MB maximum frame size**. Frames larger than 1 MB are rejected with WebSocket close code `1009`. For audio, 20 ms PCM frames at 16 kHz mono (~640 bytes) are well under the limit.

**Session resolution.** The caller can pass `?agent_session_id=<id>` on the upgrade URL. Inside the container, read `FOUNDRY_AGENT_SESSION_ID` from the environment, or fall back to the query parameter. If neither is set, generate your own UUID.

**Authentication.** Callers present a Microsoft Entra bearer token on the `Authorization` header during the upgrade. APIM and the Agents service validate the token; the container does **not** see it. Don't depend on an `Authorization` header reaching `/invocations_ws`, and don't accept an `authorization` query parameter.

## Connection lifecycle

```
Caller  ──Upgrade──▶  Agents service (proxy)  ──Upgrade──▶  Container /invocations_ws
        ◀─── 101 ─────────────────────────────────── 101 ───
        ◀══ frames (bidirectional, raw byte relay) ══▶
        ── Close ────────────────────────────────── Close ──▶
```

1. **Open.** The caller sends `GET /invocations_ws` with WebSocket upgrade headers. The platform resolves the session and version, proxies the upgrade, and the container responds `101 Switching Protocols`.
1. **Exchange.** Frames flow in both directions until either side initiates close.
1. **Close.** Either side sends a Close frame; the peer echoes a Close frame and shuts down its send side.
1. **Abnormal close.** If the underlying TCP connection drops, the peer observes close code `1006` with no Close frame.

### Maximum connection duration (preview)

The platform recycles infrastructure on a rolling basis with a shutdown grace period of **10 minutes**. Individual WebSocket connections in preview are capped at approximately **10 minutes**. When the platform initiates shutdown, it sends close code `1001` (going away). Clients must be prepared to reconnect with the same `agent_session_id`—the sandbox (and any in-process container state) persists across reconnects. The platform doesn't replay missed frames; your container is responsible for any application-level resume protocol.

### Close codes

| Close code | Meaning | Source |
|------------|---------|--------|
| `1000` | Normal closure | Either side |
| `1001` | Going away | Platform shutdown drain |
| `1002` | Protocol error | Either side |
| `1003` | Unsupported data | Either side |
| `1006` | Abnormal closure (no Close frame) | TCP drop |
| `1008` | Policy violation | Container |
| `1009` | Message too big | Platform proxy (frame exceeded 1 MB) |
| `1011` | Internal server error | Container |

## Implement the WebSocket handler

Add the `/invocations_ws` route to your container using the same `azure-ai-agentserver-invocations` host that serves the HTTP `/invocations` route. The host exposes two decorators:

| Decorator | Route | Purpose |
|-----------|-------|---------| 
| `@app.invocation_handler` | `POST /invocations` | Request/response (existing Invocations protocol) |
| `@app.ws_handler` | `GET /invocations_ws` (WebSocket upgrade) | Bidirectional streaming (this article) |

You can register one or both on the same `app` object. The host calls `await websocket.accept()` before invoking your `@app.ws_handler`, runs Ping/Pong keep-alive (default 30 s), maps uncaught exceptions to close code `1011`, and emits the structured close event and metrics listed in [Observability](#observability).

```python
from azure.ai.agentserver.invocations import InvocationsAgentServerHost
from starlette.websockets import WebSocket

app = InvocationsAgentServerHost()

@app.invocation_handler            # POST /invocations
async def invoke(payload: dict) -> dict:
    return {"echo": payload}

@app.ws_handler                    # GET /invocations_ws (WebSocket upgrade)
async def ws(websocket: WebSocket) -> None:
    async for message in websocket.iter_text():
        # JSON control message
        await websocket.send_text(message)

app.run()
```

For binary audio, read frames as bytes and pass them through your STT/LLM/TTS pipeline:

```python
@app.ws_handler
async def ws(websocket: WebSocket) -> None:
    async for chunk in websocket.iter_bytes():
        # chunk = e.g., 20 ms PCM @ 16 kHz mono = 640 bytes
        response_audio = await process_audio(chunk)
        await websocket.send_bytes(response_audio)
```

For mixed control + media, dispatch on the frame kind:

```python
import json

@app.ws_handler
async def ws(websocket: WebSocket) -> None:
    while True:
        message = await websocket.receive()
        if "text" in message:
            event = json.loads(message["text"])
            await handle_control(event, websocket)
        elif "bytes" in message:
            response = await process_audio(message["bytes"])
            await websocket.send_bytes(response)
```

The `/readiness` endpoint, OTLP export, graceful shutdown, and the `x-platform-server` identity header are inherited from `azure-ai-agentserver-core`—you don't need to wire them up yourself.

Your container should:

- Handle text and binary frames; honor continuation frames per RFC 6455.
- Keep frames at or below 1 MB.
- Persist session-relevant state so a client can reattach via the same `agent_session_id`.
- Propagate `traceparent`, `tracestate`, and `baggage` from the upgrade request as the parent context for any spans the connection emits.

For end-to-end voice samples that include a browser portal, see the [`invocations_ws` voice agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations_ws).

## Choose a voice framework

Hosted agents support any containerized voice framework. The following frameworks have validated samples:

| Framework | Description |
|-----------|-------------|
| [Microsoft Voice Live](/azure/ai-services/speech-service/voice-live) | Real-time voice interaction with built-in STT, LLM, and TTS. Supports cascaded pipelines and speech-to-speech models such as GPT-4o Realtime. |
| [Pipecat](https://www.pipecat.ai/) | Open-source modular pipeline framework for real-time voice AI. Compose processors for STT, LLMs, and TTS. |
| [LiveKit Agents](https://docs.livekit.io/agents/) | Open-source platform for real-time audio and video with room-based session management. |

### Voice pipeline architectures

You can run either pipeline style inside your container:

- **Cascaded (STT → LLM → TTS).** Separate models for each stage. Use any text model from the Foundry model catalog and any TTS voice. Best for multilingual support and custom voices.
- **Speech-to-speech.** Realtime models such as GPT-4o Realtime handle audio in and audio out in a single model. Best for natural conversational dynamics (interruptions, backchanneling) where latency is critical.

## Deploy a voice agent

Voice agents follow the same deployment flow as any hosted agent. The only difference is declaring the `invocations_ws` protocol on the agent version.

### Declare the protocol

When you create the agent version, include `invocations_ws` in `container_protocol_versions`. You can declare it alone or alongside `responses` and `invocations`.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentProtocol,
    HostedAgentDefinition,
    ProtocolVersionRecord,
)
from azure.identity import DefaultAzureCredential

project = AIProjectClient(
    endpoint="https://<resource>.services.ai.azure.com/api/projects/<project>",
    credential=DefaultAzureCredential(),
    allow_preview=True,
)

agent = project.agents.create_version(
    agent_name="my-voice-agent",
    definition=HostedAgentDefinition(
        container_protocol_versions=[
            ProtocolVersionRecord(protocol=AgentProtocol.INVOCATIONS_WS, version="1.0.0"),
        ],
        cpu="1",
        memory="2Gi",
        image="your-registry.azurecr.io/your-voice-agent:v1",
        environment_variables={
            "MODEL_DEPLOYMENT_NAME": "gpt-realtime",
        },
    ),
)
```

For the full deployment flow (build, push, RBAC, polling for status), see [Deploy a hosted agent](deploy-hosted-agent.md).

> [!TIP]
> For voice workloads, we recommend at least **1 vCPU / 2 GiB** for smooth audio processing and model inference. Sandbox sizes up to 2 vCPU / 4 GiB are available; choose what fits your pipeline.

### Connect a client

Browser clients use the W3C [WebSocket API](https://developer.mozilla.org/docs/Web/API/WebSocket/WebSocket). Other callers use standard libraries such as Python `websockets` or `aiohttp`. There's no separate client SDK.

```python
import asyncio
import websockets
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
token = credential.get_token("https://ai.azure.com/.default").token

uri = (
    "wss://<account>.services.ai.azure.com/api/projects/agents"
    "/endpoint/protocols/invocations_ws"
    "?project_name=<project>"
    "&agent_name=my-voice-agent"
    "&agent_session_id=demo-session-1"
    "&foundry_features=HostedAgents=V1Preview"
)

async def main():
    headers = {"Authorization": f"Bearer {token}"}
    async with websockets.connect(uri, additional_headers=headers) as ws:
        await ws.send("hello")
        print(await ws.recv())

asyncio.run(main())
```

### Use WebRTC media with WebSocket signaling

Some voice agents use WebRTC for browser-to-agent audio media because WebRTC handles packet loss, jitter buffering, and real-time audio transport well. Hosted agents don't provide a managed WebRTC media service, TURN service, SFU, or WebRTC signaling protocol. Instead, use `invocations_ws` as the authenticated signaling channel, and implement the WebRTC media path in your client and container.

A typical WebRTC pattern works like this:

1. The browser opens an authenticated `invocations_ws` connection to the hosted agent.
1. The browser sends signaling messages as text frames, such as an ICE configuration request, SDP offer, and ICE candidates.
1. The container creates or updates its WebRTC peer connection and responds with an SDP answer and candidate status messages.
1. Audio media flows over the WebRTC peer connection. The WebSocket remains available for signaling, lifecycle events, and application control messages.
1. Your application provides the TURN relay configuration and handles any WebRTC-specific reconnection or resume behavior.

The reference WebRTC samples use JSON text frames on `/invocations_ws` for actions such as `ice_config`, `offer`, `ice_candidate`, and `disconnect`. Audio media doesn't use the WebSocket in that pattern; it flows over the WebRTC peer connection negotiated through the WebSocket.

Use this pattern when you want WebRTC media behavior in a browser or mobile client and are prepared to operate the client-side and server-side WebRTC stack. Use direct WebSocket audio streaming when you want a simpler transport, especially for prototypes, telephony bridges, or controlled networks.

For a complete implementation, see the [Pipecat WebRTC sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations_ws/pipecat-webrtc).

## Use Foundry models and tools

Voice agents have native access to the Foundry ecosystem. The agent container authenticates with its dedicated Microsoft Entra agent identity—no API keys or connection strings in your code.

- **Realtime models.** GPT-4o Realtime and GPT Realtime for speech-to-speech pipelines.
- **Text models.** GPT-4o, GPT-4.1, and the GPT-5 series for cascaded pipelines.
- **Speech models.** Azure AI Speech for STT and TTS.
- **Tools.** Access Foundry-managed tools (Web Search, File Search, Code Interpreter, Azure AI Search, custom MCP servers, A2A) through the Toolbox MCP endpoint in your Foundry project. See [Curate intent-based toolbox in Foundry](tools/toolbox.md).

## Observability

The `/invocations_ws` upgrade and per-connection lifecycle should be instrumented with distributed trace spans, following the [OpenTelemetry GenAI conventions](../../observability/concepts/trace-agent-concept.md) used by the HTTP `/invocations` protocol.

Propagate `traceparent`, `tracestate`, and `baggage` from the upgrade request as the parent context for any spans emitted during the connection's lifetime.

Recommended metrics to emit:

| Metric | Type | Description |
|--------|------|-------------|
| `websocket.connection.duration_ms` | Histogram | Connection duration from upgrade to close. |
| `websocket.connection.close_code` | Counter | Distribution of close codes. |
| `websocket.frames.sent` / `websocket.frames.received` | Counter | Frame counts (text + binary). |
| `websocket.frames.bytes_sent` / `websocket.frames.bytes_received` | Counter | Byte volume per direction. |
| `websocket.active_connections` | Gauge | Concurrent active connections. |

Traces and metrics appear in the linked Application Insights resource alongside model and tool invocation traces.

## Limits and considerations

| Limit | Value | Notes |
|-------|-------|-------|
| Maximum WebSocket frame size | 1 MB | Enforced by the platform proxy (close code `1009`). |
| Maximum connection duration | ~10 minutes (preview) | Platform sends close code `1001` on shutdown drain. Reconnect with the same `agent_session_id`. |
| Sandbox resources | Up to 2 vCPU / 4 GiB | At least 1 vCPU / 2 GiB recommended for voice. |
| Maximum concurrent sessions | 50 per subscription per region | Adjustable through a quota request. |
| Session idle timeout | 15 minutes | Compute is deprovisioned; session state is persisted. |

The platform doesn't replay missed frames. Your container is responsible for any application-level resume protocol.

## Telephony integration

To connect a traditional phone-based agent, use a telephony provider (for example, Azure Communication Services or Twilio) that bridges PSTN calls to your hosted agent's `invocations_ws` endpoint. The telephony provider handles SIP signaling, media transcoding, and DTMF processing.

## Next steps

> [!div class="nextstepaction"]
> [Deploy a hosted agent](deploy-hosted-agent.md)

## Related content

- [What are hosted agents?](../concepts/hosted-agents.md)
- [Manage hosted agent sessions](manage-hosted-sessions.md)
- [Configure virtual networks](virtual-networks.md)
- [Hosted voice agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/invocations_ws)
