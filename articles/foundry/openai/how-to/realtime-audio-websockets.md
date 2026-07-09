---
title: "Use the GPT Realtime API via WebSockets"
description: "Learn how to use the GPT Realtime API for speech and audio via WebSockets."
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: how-to
ms.date: 04/01/2026
author: PatrickFarley
ms.author: pafarley
ms.custom:
  - references_regions
  - classic-and-new
  - doc-kit-assisted
recommendations: false
ai-usage: ai-assisted
---

# Use the GPT Realtime API via WebSockets

[!INCLUDE [realtime-audio-websockets 1](../includes/how-to-realtime-audio-websockets-1.md)]

## Prerequisites

Before you can use GPT real-time audio, you need:

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A Microsoft Foundry resource. Create the resource in one of the [supported regions](#supported-models). For setup steps, see [Create a Microsoft Foundry resource](/azure/ai-services/multi-service-resource?pivots=azportal).
- A deployment of a GPT realtime model in a supported region as described in the [supported models](#supported-models) section in this article.
  - In the Foundry portal, load your project. Select **Build** in the upper-right menu, then select the **Models** tab on the left pane, and select **Deploy a base model**. Search for the model you want, and select **Deploy** on the model page.
- **Required libraries**:
  - Python: `pip install websockets azure-identity`
  - JavaScript/Node.js: `npm install ws @azure/identity`

[!INCLUDE [realtime-audio-websockets 2](../includes/how-to-realtime-audio-websockets-2.md)]

## Connection and authentication

The Realtime API (via `/realtime`) is built on [the WebSockets API](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) to facilitate fully asynchronous streaming communication between the end user and model. 

The Realtime API is accessed via a secure WebSocket connection to the `/realtime` endpoint of your Azure OpenAI resource.

You can construct a full request URI by concatenating:

- The secure WebSocket (`wss://`) protocol.
- Your Azure OpenAI resource endpoint hostname, for example, `my-aoai-resource.openai.azure.com`
- The API path: `openai/v1/realtime` for GA, or `openai/realtime` for preview.
- A `model` query string parameter with the name of your `gpt-realtime`, `gpt-realtime-1.5`, or `gpt-realtime-mini` model deployment.
- **(Preview version only)** An `api-version` query string parameter for a supported API version such as `2025-04-01-preview` and a `deployment` query parameter instead of `model`.

The following example is a well-constructed `/realtime` request URI:

#### [GA version](#tab/ga)

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/v1/realtime?model=gpt-realtime-deployment-name
```

#### [Preview version](#tab/preview)

```http
wss://my-eastus2-openai-resource.openai.azure.com/openai/realtime?api-version=2025-04-01-preview&deployment=gpt-4o-mini-realtime-preview-deployment-name
```

---

> [!NOTE]
> The GA API uses the `/openai/v1/realtime` path with `model=` as the query parameter. The preview API uses `/openai/realtime` with `api-version=` and `deployment=` parameters. Using the wrong path or mixing GA/preview formats results in a 404 error.


To authenticate:
- **Microsoft Entra** (recommended): Use token-based authentication with the `/realtime` API for an Azure OpenAI resource with managed identity enabled. Apply a retrieved authentication token using a `Bearer` token with the `Authorization` header.
- **API key**: An `api-key` can be provided in one of two ways:
  - Using an `api-key` connection header on the pre-handshake connection. This option isn't available in a browser environment.
  - Using an `api-key` query string parameter on the request URI. Query string parameters are encrypted when using HTTPS/WSS.

## Transcribe audio in real-time

The following examples show how to stream microphone audio to the `gpt-realtime-whisper` model for real-time transcription.

### Prerequisites for Python

Install required packages:

```bash
pip install websockets sounddevice azure-identity
```

Set environment variables:

#### [API key](#tab/api-key)

```bash
export AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com
export AZURE_OPENAI_API_KEY=<api-key>
export AZURE_OPENAI_DEPLOYMENT_NAME=<deployment-name>
```

#### [Microsoft Entra](#tab/entra-id)

```bash
export AZURE_OPENAI_ENDPOINT=https://<resource-name>.openai.azure.com
export AZURE_OPENAI_DEPLOYMENT_NAME=<deployment-name>
```

Sign in to Azure:

```bash
az login
```

---

### Transcription example

#### [API key](#tab/api-key)

```python
import asyncio
import base64
import json
import os
import signal
from urllib.parse import urlencode

import sounddevice as sd
import websockets

# Configuration
LANGUAGE = ""  # Optional: language hint like "en"
TRANSCRIPTION_DELAY = "medium"  # Supported values: minimal, low, medium, high, xhigh
SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = "int16"
BLOCK_MS = 100
COMMIT_SECONDS = 3


def azure_realtime_url() -> str:
    """Construct WebSocket URL for transcription."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip().rstrip("/")
    if endpoint.lower().startswith("https://"):
        endpoint = "wss://" + endpoint[8:]
    endpoint_complete = f"{endpoint}/openai/v1/realtime?intent=transcription"
    return endpoint_complete


def session_update_message(language: str) -> str:
    """Create session configuration message."""
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"].strip()
    transcription = {"model": deployment}
    if TRANSCRIPTION_DELAY.strip():
        transcription["delay"] = TRANSCRIPTION_DELAY.strip()
    if language.strip():
        transcription["language"] = language.strip()

    return json.dumps({
        "type": "session.update",
        "session": {
            "type": "transcription",
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": SAMPLE_RATE,
                    },
                    "turn_detection": None,
                    "transcription": transcription,
                },
            },
        },
    })


async def transcribe_audio() -> None:
    """Stream microphone audio and transcribe in real-time."""
    headers = {"api-key": os.environ["AZURE_OPENAI_API_KEY"].strip()}
    url = azure_realtime_url()
    stop = asyncio.Event()

    async def microphone_sender(ws):
        """Send microphone audio to WebSocket."""
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue(maxsize=20)

        def enqueue_audio(audio_bytes: bytes) -> None:
            try:
                queue.put_nowait(audio_bytes)
            except asyncio.QueueFull:
                pass

        def on_audio(indata, frames, time, status):
            if status:
                print(f"Microphone warning: {status}")
            audio_bytes = bytes(indata)
            loop.call_soon_threadsafe(enqueue_audio, audio_bytes)

        blocksize = int(SAMPLE_RATE * BLOCK_MS / 1000)
        print(f"Starting transcription. Press Ctrl+C to stop.\n")
        
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=blocksize,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=on_audio,
        ):
            append_count = 0
            commit_count = 0
            chunks_since_commit = 0
            chunks_per_commit = max(1, int(COMMIT_SECONDS * 1000 / BLOCK_MS))

            while not stop.is_set():
                chunk = await queue.get()
                if stop.is_set():
                    break
                    
                append_count += 1
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "event_id": f"append_{append_count}",
                    "audio": base64.b64encode(chunk).decode("ascii"),
                }))
                
                chunks_since_commit += 1
                if chunks_since_commit >= chunks_per_commit:
                    commit_count += 1
                    await ws.send(json.dumps({
                        "type": "input_audio_buffer.commit",
                        "event_id": f"commit_{commit_count}",
                    }))
                    chunks_since_commit = 0

    async def transcription_receiver(ws):
        """Receive and print transcription results."""
        try:
            async for raw_message in ws:
                if stop.is_set():
                    break
                event = json.loads(raw_message)
                event_type = event.get("type")

                if event_type in {
                    "conversation.item.input_audio_transcription.completed",
                    "response.text.done",
                }:
                    text = event.get("text") or event.get("transcript")
                    if text:
                        print(text, flush=True)
                elif event_type == "conversation.item.input_audio_transcription.failed":
                    print(f"Transcription failed: {event.get('error', event)}")
        except asyncio.CancelledError:
            pass

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Configure session
        await ws.send(session_update_message(LANGUAGE))
        async for raw_message in ws:
            event = json.loads(raw_message)
            if event.get("type") == "session.updated":
                print("Transcription session configured.")
                break

        # Start sender and receiver tasks
        sender = asyncio.create_task(microphone_sender(ws))
        receiver = asyncio.create_task(transcription_receiver(ws))

        try:
            await asyncio.sleep(3600)  # Run for 1 hour or until Ctrl+C
        except KeyboardInterrupt:
            print("\nStopping transcription.")
        finally:
            stop.set()
            sender.cancel()
            receiver.cancel()
            await asyncio.gather(sender, receiver, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(transcribe_audio())
    except KeyboardInterrupt:
        pass
```

#### [Microsoft Entra](#tab/entra-id)

```python
import asyncio
import base64
import json
import logging
import os
import signal

import sounddevice as sd
import websockets
from azure.identity import DefaultAzureCredential

# Configuration
LANGUAGE = ""
TRANSCRIPTION_DELAY = "medium"
SAMPLE_RATE = 24000
CHANNELS = 1
DTYPE = "int16"
BLOCK_MS = 100
AZURE_OPENAI_SCOPE = "https://ai.azure.com/.default"


def azure_realtime_url() -> str:
    """Construct WebSocket URL for transcription."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip().rstrip("/")
    if endpoint.lower().startswith("https://"):
        endpoint = "wss://" + endpoint[8:]
    endpoint_complete = f"{endpoint}/openai/v1/realtime?intent=transcription"
    return endpoint_complete


def get_auth_headers() -> dict:
    """Get authorization headers using Microsoft Entra."""
    credential = DefaultAzureCredential()
    token = credential.get_token(AZURE_OPENAI_SCOPE)
    return {"Authorization": f"Bearer {token.token}"}


def session_update_message(language: str) -> str:
    """Create session configuration message."""
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"].strip()
    transcription = {"model": deployment}
    if TRANSCRIPTION_DELAY.strip():
        transcription["delay"] = TRANSCRIPTION_DELAY.strip()
    if language.strip():
        transcription["language"] = language.strip()

    return json.dumps({
        "type": "session.update",
        "session": {
            "type": "transcription",
            "audio": {
                "input": {
                    "format": {
                        "type": "audio/pcm",
                        "rate": SAMPLE_RATE,
                    },
                    "turn_detection": None,
                    "transcription": transcription,
                },
            },
        },
    })


async def transcribe_audio() -> None:
    """Stream microphone audio and transcribe in real-time."""
    headers = get_auth_headers()
    url = azure_realtime_url()
    stop = asyncio.Event()

    async def microphone_sender(ws):
        """Send microphone audio to WebSocket."""
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue(maxsize=20)

        def enqueue_audio(audio_bytes: bytes) -> None:
            try:
                queue.put_nowait(audio_bytes)
            except asyncio.QueueFull:
                pass

        def on_audio(indata, frames, time, status):
            if status:
                print(f"Microphone warning: {status}")
            audio_bytes = bytes(indata)
            loop.call_soon_threadsafe(enqueue_audio, audio_bytes)

        blocksize = int(SAMPLE_RATE * BLOCK_MS / 1000)
        print(f"Starting transcription. Press Ctrl+C to stop.\n")
        
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=blocksize,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=on_audio,
        ):
            append_count = 0
            commit_count = 0
            chunks_since_commit = 0
            chunks_per_commit = 3

            while not stop.is_set():
                chunk = await queue.get()
                if stop.is_set():
                    break
                    
                append_count += 1
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "event_id": f"append_{append_count}",
                    "audio": base64.b64encode(chunk).decode("ascii"),
                }))
                
                chunks_since_commit += 1
                if chunks_since_commit >= chunks_per_commit:
                    commit_count += 1
                    await ws.send(json.dumps({
                        "type": "input_audio_buffer.commit",
                        "event_id": f"commit_{commit_count}",
                    }))
                    chunks_since_commit = 0

    async def transcription_receiver(ws):
        """Receive and print transcription results."""
        try:
            async for raw_message in ws:
                if stop.is_set():
                    break
                event = json.loads(raw_message)
                event_type = event.get("type")

                if event_type in {
                    "conversation.item.input_audio_transcription.completed",
                    "response.text.done",
                }:
                    text = event.get("text") or event.get("transcript")
                    if text:
                        print(text, flush=True)
                elif event_type == "conversation.item.input_audio_transcription.failed":
                    print(f"Transcription failed: {event.get('error', event)}")
        except asyncio.CancelledError:
            pass

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Configure session
        await ws.send(session_update_message(LANGUAGE))
        async for raw_message in ws:
            event = json.loads(raw_message)
            if event.get("type") == "session.updated":
                print("Transcription session configured.")
                break

        # Start sender and receiver tasks
        sender = asyncio.create_task(microphone_sender(ws))
        receiver = asyncio.create_task(transcription_receiver(ws))

        try:
            await asyncio.sleep(3600)
        except KeyboardInterrupt:
            print("\nStopping transcription.")
        finally:
            stop.set()
            sender.cancel()
            receiver.cancel()
            await asyncio.gather(sender, receiver, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(transcribe_audio())
    except KeyboardInterrupt:
        pass
```

---

## Translate audio in real time

The following examples show how to stream microphone audio to the `gpt-realtime-translate` model for real-time translation.

### Translation example

#### [API key](#tab/api-key)

```python
import asyncio
import base64
import json
import os

import sounddevice as sd
import websockets

# Configuration
TARGET_LANGUAGE = "de"  # German - set to desired target language
SAMPLE_RATE = 24_000
CHANNELS = 1
DTYPE = "int16"
BLOCK_MS = 100


def azure_realtime_url() -> str:
    """Construct WebSocket URL for translation."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip().rstrip("/")
    if endpoint.lower().startswith("https://"):
        endpoint = "wss://" + endpoint[8:]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"].strip()
    endpoint_complete = f"{endpoint}/openai/v1/realtime/translations?model={deployment}"
    return endpoint_complete


def session_update_message(target_language: str) -> str:
    """Create session configuration message for translation."""
    return json.dumps({
        "type": "session.update",
        "session": {
            "audio": {
                "output": {
                    "language": target_language,
                },
            },
        },
    })


async def translate_audio() -> None:
    """Stream microphone audio and translate in real-time."""
    headers = {"api-key": os.environ["AZURE_OPENAI_API_KEY"].strip()}
    url = azure_realtime_url()
    stop = asyncio.Event()

    async def microphone_sender(ws):
        """Send microphone audio to WebSocket."""
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue(maxsize=20)

        def enqueue_audio(audio_bytes: bytes) -> None:
            try:
                queue.put_nowait(audio_bytes)
            except asyncio.QueueFull:
                pass

        def on_audio(indata, frames, time, status):
            if status:
                print(f"Microphone warning: {status}")
            audio_bytes = bytes(indata)
            loop.call_soon_threadsafe(enqueue_audio, audio_bytes)

        blocksize = int(SAMPLE_RATE * BLOCK_MS / 1000)
        print(f"Starting translation to {TARGET_LANGUAGE}. Press Ctrl+C to stop.\n")
        
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=blocksize,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=on_audio,
        ):
            while not stop.is_set():
                chunk = await queue.get()
                if stop.is_set():
                    break
                await ws.send(json.dumps({
                    "type": "session.input_audio_buffer.append",
                    "audio": base64.b64encode(chunk).decode("ascii"),
                }))

    async def translation_receiver(ws):
        """Receive and print translation results."""
        try:
            async for raw_message in ws:
                if stop.is_set():
                    break
                event = json.loads(raw_message)
                event_type = event.get("type")

                # Print translation deltas and final translations
                if event_type == "response.text.delta":
                    text = event.get("text", "")
                    if text:
                        print(text, end="", flush=True)
                elif event_type == "response.text.done":
                    print()  # Newline after translation completes
        except asyncio.CancelledError:
            pass

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Configure session
        await ws.send(session_update_message(TARGET_LANGUAGE))
        async for raw_message in ws:
            event = json.loads(raw_message)
            if event.get("type") == "session.updated":
                print("Translation session configured.")
                break

        # Start sender and receiver tasks
        sender = asyncio.create_task(microphone_sender(ws))
        receiver = asyncio.create_task(translation_receiver(ws))

        try:
            await asyncio.sleep(3600)
        except KeyboardInterrupt:
            print("\nStopping translation.")
        finally:
            stop.set()
            sender.cancel()
            receiver.cancel()
            await asyncio.gather(sender, receiver, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(translate_audio())
    except KeyboardInterrupt:
        pass
```

#### [Microsoft Entra](#tab/entra-id)

```python
import asyncio
import base64
import json
import os

import sounddevice as sd
import websockets
from azure.identity import DefaultAzureCredential

# Configuration
TARGET_LANGUAGE = "de"  # German - set to desired target language
SAMPLE_RATE = 24_000
CHANNELS = 1
DTYPE = "int16"
BLOCK_MS = 100
AZURE_OPENAI_SCOPE = "https://ai.azure.com/.default"


def azure_realtime_url() -> str:
    """Construct WebSocket URL for translation."""
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].strip().rstrip("/")
    if endpoint.lower().startswith("https://"):
        endpoint = "wss://" + endpoint[8:]
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"].strip()
    endpoint_complete = f"{endpoint}/openai/v1/realtime/translations?model={deployment}"
    return endpoint_complete


def get_auth_headers() -> dict:
    """Get authorization headers using Microsoft Entra."""
    credential = DefaultAzureCredential()
    token = credential.get_token(AZURE_OPENAI_SCOPE)
    return {"Authorization": f"Bearer {token.token}"}


def session_update_message(target_language: str) -> str:
    """Create session configuration message for translation."""
    return json.dumps({
        "type": "session.update",
        "session": {
            "audio": {
                "output": {
                    "language": target_language,
                },
            },
        },
    })


async def translate_audio() -> None:
    """Stream microphone audio and translate in real-time."""
    headers = get_auth_headers()
    url = azure_realtime_url()
    stop = asyncio.Event()

    async def microphone_sender(ws):
        """Send microphone audio to WebSocket."""
        loop = asyncio.get_running_loop()
        queue = asyncio.Queue(maxsize=20)

        def enqueue_audio(audio_bytes: bytes) -> None:
            try:
                queue.put_nowait(audio_bytes)
            except asyncio.QueueFull:
                pass

        def on_audio(indata, frames, time, status):
            if status:
                print(f"Microphone warning: {status}")
            audio_bytes = bytes(indata)
            loop.call_soon_threadsafe(enqueue_audio, audio_bytes)

        blocksize = int(SAMPLE_RATE * BLOCK_MS / 1000)
        print(f"Starting translation to {TARGET_LANGUAGE}. Press Ctrl+C to stop.\n")
        
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=blocksize,
            channels=CHANNELS,
            dtype=DTYPE,
            callback=on_audio,
        ):
            while not stop.is_set():
                chunk = await queue.get()
                if stop.is_set():
                    break
                await ws.send(json.dumps({
                    "type": "session.input_audio_buffer.append",
                    "audio": base64.b64encode(chunk).decode("ascii"),
                }))

    async def translation_receiver(ws):
        """Receive and print translation results."""
        try:
            async for raw_message in ws:
                if stop.is_set():
                    break
                event = json.loads(raw_message)
                event_type = event.get("type")

                # Print translation deltas and final translations
                if event_type == "response.text.delta":
                    text = event.get("text", "")
                    if text:
                        print(text, end="", flush=True)
                elif event_type == "response.text.done":
                    print()  # Newline after translation completes
        except asyncio.CancelledError:
            pass

    async with websockets.connect(url, additional_headers=headers) as ws:
        # Configure session
        await ws.send(session_update_message(TARGET_LANGUAGE))
        async for raw_message in ws:
            event = json.loads(raw_message)
            if event.get("type") == "session.updated":
                print("Translation session configured.")
                break

        # Start sender and receiver tasks
        sender = asyncio.create_task(microphone_sender(ws))
        receiver = asyncio.create_task(translation_receiver(ws))

        try:
            await asyncio.sleep(3600)
        except KeyboardInterrupt:
            print("\nStopping translation.")
        finally:
            stop.set()
            sender.cancel()
            receiver.cancel()
            await asyncio.gather(sender, receiver, return_exceptions=True)


if __name__ == "__main__":
    try:
        asyncio.run(translate_audio())
    except KeyboardInterrupt:
        pass
```

---

[!INCLUDE [realtime-audio-websockets 3](../includes/how-to-realtime-audio-websockets-3.md)]
