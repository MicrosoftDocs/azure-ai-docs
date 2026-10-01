---
title: Use MAI-Transcribe-2-Streaming with the Realtime API - Speech Service
titleSuffix: Foundry Tools
description: Learn how to transcribe streaming audio with MAI-Transcribe-2-Streaming by using the Realtime API.
manager: mcleans
author: PatrickFarley
ms.author: pafarley
ms.service: azure-speech-foundry-tools
ms.topic: how-to
ms.date: 09/30/2026
ms.custom: references_regions
ai-usage: ai-assisted

# Customer intent: As a developer, I want to transcribe live audio with MAI-Transcribe-2-Streaming by using the Realtime API.
---

# Use MAI-Transcribe-2-Streaming with the Realtime API

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

MAI-Transcribe-2-Streaming is a low-latency, speech-to-text model for real-time transcription. Send audio as a continuous stream and receive incremental transcripts while the speaker talks. Intermediate results update the current transcription, and final results confirm each segment.

The model supports live audio workloads such as call centers, voice assistants, meeting and lecture captioning, voice-driven interfaces, and real-time note taking.

For the managed client-library integration, see [Use MAI-Transcribe-2-Streaming with Azure Speech SDK](mai-transcribe-2-streaming-speech-sdk.md).

## Prerequisites

Before you can use MAI-Transcribe-2-Streaming, you need:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource: Create the resource in one of the supported regions. For setup steps, see [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of a MAI-Transcribe-2-Streaming model in a supported region.
  - In the Foundry portal, load your project. Select **Build** in the upper-right menu, select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.


## Supported models

- `MAI-Transcribe-2-Streaming`

## Limitations

- Each session can last up to one hour.

## Availability and regions

You can access MAI-Transcribe-2-Streaming globally. Azure serves the model from the following regions, and routes requests to them:

| Region | Region identifier | Availability |
| --- | --- | --- |
| Sweden Central | `swedencentral` | Available |
| Central US | `centralus` | Available |
| East US 2 | `eastus2` | Coming soon |
| South India | `southindia` | Available |

## Quickstart
MAI-Transcribe-2-Streaming converts streamed audio into text over a WebSocket connection, using [OpenAI Realtime API-like protocol](https://developers.openai.com/api/docs/guides/realtime-transcription). Clients send audio; the server produces partial and final transcription hypotheses. Additionally, clients can explicitly request a final by sending a `commit` message, which produces `completed` transcription as soon as possible.


1. Initiate a WebSocket connection to `wss://{your_resource_name}.services.ai.azure.com/mai/v1/realtime` (`ws://` locally), and set the `Authorization` header to your Microsoft Entra bearer token (or supply an `api-key` header instead). For details, see [Connection and authentication](#connection-and-authentication).

   - On success, the server sends `session.created` containing `session.id` and current settings.

1. Configure the session **before sending audio** by sending the following message:

   ```json
   {
     "type": "session.update",
     "event_id": "configure-1",
     "session": {
       "type": "transcription",
       "audio": {
         "input": {
           "format": {"type": "audio/pcm", "rate": 16000},
           "transcription": {"model": "<deployment-name>", "language": null},
           "turn_detection": null,
           "noise_reduction": null
         }
       }
     }
   }
   ```

   | Setting under `session.audio.input` | Behavior |
   | --- | --- |
   | `format` | Raw signed little-endian PCM16, mono, 16000 or 24000 samples/second. |
   | `transcription.language` | Optional language code, such as `"en"`. The model supports 60 languages (see the table below). Initially `null`: automatic detection. The current backend treats unrecognized values as unset. |
   | `transcription.model` | The model deployment name in Foundry. |
   | `turn_detection`, `noise_reduction` | Only `null` is supported. There is no server-side speech detection or automatic commit. The service might initially create a session with turn detection enabled. When you specify the model in a `session.update` message, the service disables turn detection. |

   - On success, `session.updated` is returned with the full session object. Settings can't change after the first audio append, even after a commit.

1. Start sending audio:

   ```json
   {"type": "input_audio_buffer.append", "audio": "<base64-encoded PCM16 bytes>"}
   ```

   - `audio` must be a nonempty, valid base64 encoding of 16-bit PCM samples, without a WAV header. To minimize latency, send audio in small chunks, such as 10-20 ms. If you can accept higher latency, use larger chunks to save network overhead.

1. Receive events concurrently with sending.

   - There's no per-append acknowledgement: the server processes buffered audio independently of packet boundaries. An append can produce zero or multiple transcript events.
   - The server sends the following events:

   | Event name | Description |
   | --- | --- |
   | `conversation.item.input_audio_transcription.delta` | Contains newly finalized transcript. Append it to an accumulated string buffer. Don't insert or strip spaces. |
   | `conversation.item.input_audio_transcription.intermediate` (MAI-specific) | Contains the entire current provisional suffix, replacing the previous suffix (aka partial). The suffix is relative to the latest `delta` event, i.e. the current best hypothesis of the model is: `"".join(list_of_all_deltas_so_far) + intermediate.intermediate` |
   | `input_audio_buffer.committed` | Confirms that the service committed the current input audio buffer. Finalization can continue after this event. |
   | `conversation.item.input_audio_transcription.completed` | Contains the full final transcript for audio since the previous commit, or since the beginning of the session for the first commit. The transcript is equivalent to the accumulated `delta` events for that interval. |

   - Example:

   ```json
   {"type":"conversation.item.input_audio_transcription.delta","item_id":"item_1","content_index":0,"delta":"Hello"}
   {"type":"conversation.item.input_audio_transcription.intermediate","item_id":"item_1","content_index":0,"intermediate":" world"}
   {"type":"conversation.item.input_audio_transcription.intermediate","item_id":"item_1","content_index":0,"intermediate":" there"}
   {"type":"conversation.item.input_audio_transcription.delta","item_id":"item_1","content_index":0,"delta":" there!"}
   ```

1. Commit an item.

   - Send commit at a natural pause in speech (such as identified by a VAD model for voice activity detection), or end of recording. It requests the model to produce a final transcript for all audio sent so far as fast as possible.

   ```json
   {"type": "input_audio_buffer.commit"}
   ```

   - Example response:

   ```json
   {"type":"input_audio_buffer.committed"}
   {"type":"conversation.item.input_audio_transcription.completed", "transcript":"Hello there!"}
   ```

   The client can either accumulate `delta` events or consume the `completed` event when it needs the full final transcript after a commit.

1. Continue streaming and sending commits.


## Connection and authentication

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model.

Access the Realtime API through a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

Construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol.
- Your Azure resource endpoint hostname, for example, `my-resource.services.ai.azure.com`.
- The API path: `/mai/v1/realtime`

The following example is a well-constructed request URI:

```http
wss://my-resource.services.ai.azure.com/mai/v1/realtime?intent=transcription
```

To authenticate:

- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI resource with managed identity enabled. Apply a retrieved authentication token by using a `Bearer` token with the `Authorization` header.
- **API key**: Provide an `api-key` in one of two ways:
  - Use an `api-key` connection header on the pre-handshake connection. This option isn't available in a browser environment.
  - Use an `api-key` query string parameter on the request URI. Query string parameters are encrypted when you use HTTPS/WSS.

## Pricing

See [Microsoft Foundry Models pricing](https://azure.microsoft.com/pricing/details/ai-foundry-models/microsoft/).

## Transcribe audio in real time

The following examples show how to stream microphone audio to the `MAI-Transcribe-2-Streaming` model for real-time transcription.

### Prerequisites for Python

Install required packages:

```bash
pip install websockets sounddevice azure-identity
```

Set environment variables:

#### Microsoft Entra ID

```bash
export AZURE_MAI_ENDPOINT=https://<resource-name>.services.ai.azure.com
export AZURE_MAI_DEPLOYMENT_NAME=<deployment-name>
```

Sign in to Azure:

```bash
az login
```


#### API key

```bash
export AZURE_MAI_ENDPOINT=https://<resource-name>.services.ai.azure.com
export AZURE_MAI_API_KEY=<api-key>
export AZURE_MAI_DEPLOYMENT_NAME=<deployment-name>
```

### Transcription example

```python
"""Stream mono PCM16 microphone audio to the Azure MAI transcription endpoint."""

import asyncio
import base64
import json
import os
import signal
from typing import Any
from urllib.parse import urlsplit

from azure.identity.aio import DefaultAzureCredential
import sounddevice as sd
from websockets.asyncio.client import ClientConnection, connect

SAMPLE_RATE = 16_000
BLOCK_MS = 100
COMMIT_SECONDS = 3
LANGUAGE = ""  # Optional language hint, such as "en".
SESSION_TIMEOUT_SECONDS = 30
COMPLETION_TIMEOUT_SECONDS = 240
MAX_RECORDING_SECONDS = 3600
_TOKEN_SCOPE = "https://cognitiveservices.azure.com/.default"
_TRANSCRIPTION_EVENT = "conversation.item.input_audio_transcription."


def _realtime_url() -> str:
    endpoint = urlsplit(os.environ["AZURE_MAI_ENDPOINT"].strip())
    if (
        endpoint.scheme not in {"https", "wss"}
        or not endpoint.hostname
        or endpoint.username is not None
        or endpoint.password is not None
        or endpoint.path not in {"", "/"}
        or endpoint.query
        or endpoint.fragment
    ):
        raise ValueError("AZURE_MAI_ENDPOINT must be an HTTPS/WSS resource root URL")
    return endpoint._replace(
        scheme="wss", path="/mai/v1/realtime", query="intent=transcription"
    ).geturl()


async def _auth_headers() -> dict[str, str]:
    if api_key := os.environ.get("AZURE_MAI_API_KEY", "").strip():
        return {"api-key": api_key}
    async with DefaultAzureCredential() as credential:
        token = await credential.get_token(_TOKEN_SCOPE)
    return {"Authorization": f"Bearer {token.token}"}


async def _receive_event(ws: ClientConnection) -> dict[str, Any]:
    event = json.loads(await ws.recv())
    if event.get("type") in {"error", _TRANSCRIPTION_EVENT + "failed"}:
        raise RuntimeError(f"Transcription API error: {event.get('error', event)}")
    return event


async def _wait_for_event(ws: ClientConnection, event_type: str) -> None:
    async with asyncio.timeout(SESSION_TIMEOUT_SECONDS):
        while (await _receive_event(ws)).get("type") != event_type:
            pass


async def transcribe_audio() -> None:
    """Record until Ctrl+C or one hour, then drain audio and await all completions."""
    url = _realtime_url()
    deployment = os.environ["AZURE_MAI_DEPLOYMENT_NAME"].strip()
    if not deployment:
        raise ValueError("AZURE_MAI_DEPLOYMENT_NAME must not be empty")
    transcription = {"model": deployment}
    if LANGUAGE.strip():
        transcription["language"] = LANGUAGE.strip()
    headers = await _auth_headers()

    async with connect(url, additional_headers=headers) as ws:
        await _wait_for_event(ws, "session.created")
        await ws.send(
            json.dumps(
                {
                    "type": "session.update",
                    "session": {
                        "type": "transcription",
                        "audio": {
                            "input": {
                                "format": {"type": "audio/pcm", "rate": SAMPLE_RATE},
                                "transcription": transcription,
                                "turn_detection": None,  # This example commits manually.
                            },
                        },
                    },
                }
            )
        )
        await _wait_for_event(ws, "session.updated")

        loop = asyncio.get_running_loop()
        queue: asyncio.Queue[bytes | Exception | None] = asyncio.Queue()
        stopping = False
        pending_commits = 0
        all_completed = asyncio.Event()
        all_completed.set()

        def _stop(error: Exception | None = None) -> None:
            nonlocal stopping
            if not stopping:
                stopping = True
                queue.put_nowait(error)  # None marks a normal stop after queued audio.

        def _enqueue(chunk: bytes, warning: str) -> None:
            if stopping:
                return
            if warning:
                _stop(RuntimeError(f"Microphone error: {warning}"))
            elif queue.qsize() >= 20:
                _stop(RuntimeError("Audio sender fell behind; microphone audio was lost"))
            else:
                queue.put_nowait(chunk)

        def _on_audio(indata, frames, time, status) -> None:
            loop.call_soon_threadsafe(_enqueue, bytes(indata), str(status) if status else "")

        async def _commit() -> None:
            nonlocal pending_commits
            pending_commits += 1
            all_completed.clear()
            await ws.send(json.dumps({"type": "input_audio_buffer.commit"}))

        async def _send_microphone() -> None:
            bytes_since_commit = 0
            with sd.RawInputStream(
                samplerate=SAMPLE_RATE,
                blocksize=SAMPLE_RATE * BLOCK_MS // 1000,
                channels=1,
                dtype="int16",
                callback=_on_audio,
            ):
                print("Transcribing. Press Ctrl+C to stop.", flush=True)
                while (chunk := await queue.get()) is not None:
                    if isinstance(chunk, Exception):
                        raise chunk
                    await ws.send(
                        json.dumps(
                            {
                                "type": "input_audio_buffer.append",
                                "audio": base64.b64encode(chunk).decode("ascii"),
                            }
                        )
                    )
                    bytes_since_commit += len(chunk)
                    if bytes_since_commit >= SAMPLE_RATE * 2 * COMMIT_SECONDS:
                        await _commit()
                        bytes_since_commit = 0
            if bytes_since_commit:
                await _commit()

        async def _receive_transcripts() -> None:
            nonlocal pending_commits
            while True:
                event = await _receive_event(ws)
                event_type = event.get("type")
                if event_type == _TRANSCRIPTION_EVENT + "intermediate":
                    text = (
                        event.get("intermediate")
                    )
                    print(f"Intermediate: {text}", flush=True)
                elif event_type == _TRANSCRIPTION_EVENT + "delta":
                    print(f"Delta: {event.get('delta', '')}", flush=True)
                elif event_type == _TRANSCRIPTION_EVENT + "completed":
                    print(f"Transcript: {event.get('transcript', '')}", flush=True)
                    pending_commits -= 1
                    if pending_commits == 0:
                        all_completed.set()

        previous_handler = signal.signal(signal.SIGINT, lambda *_: loop.call_soon_threadsafe(_stop))
        deadline = loop.call_later(MAX_RECORDING_SECONDS, _stop)
        try:
            async with asyncio.TaskGroup() as tasks:
                receiver = tasks.create_task(_receive_transcripts())
                await _send_microphone()
                print("Waiting for final transcription...", flush=True)
                async with asyncio.timeout(COMPLETION_TIMEOUT_SECONDS):
                    await all_completed.wait()
                receiver.cancel()
        finally:
            stopping = True
            deadline.cancel()
            signal.signal(signal.SIGINT, previous_handler)


if __name__ == "__main__":
    try:
        asyncio.run(transcribe_audio())
    except KeyboardInterrupt:
        pass
```


## Language support

By default, the model operates in multilingual mode. The following languages are currently supported:

[!INCLUDE [MAI Transcribe language support](includes/language-support/mai-transcribe.md)]
