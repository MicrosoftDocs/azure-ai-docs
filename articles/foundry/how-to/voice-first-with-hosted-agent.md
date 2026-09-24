---
title: "Use a hosted agent as the conversation engine in a Voice-based agent"
description: "Learn how to create a Voice-based agent that uses a hosted text agent as its conversation engine in Microsoft Foundry."
#customer intent: As an agent developer, I want to use my hosted text agent as the conversation engine for a Voice-based agent.
author: PatrickFarley
ms.author: pafarley
ms.date: 09/09/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ai-usage: ai-assisted
---

# Use a hosted agent as the conversation engine in a Voice-based agent

In this article, you create a Voice-based agent that uses a hosted text agent as its conversation engine. Voice Live provides speech recognition, turn-taking, speech synthesis, and interruption handling, while your hosted agent processes text input and produces text responses.

> [!IMPORTANT]
> Voice-based agents are in preview. Requests to create a Voice-based agent must include the `Foundry-Features: VoiceAgents=V1Preview` header.

A Voice-based agent can use an existing hosted text agent for its conversation logic. The resulting voice experience follows this flow:

```text
caller audio -> 
Voice Live speech recognition -> 
hosted text agent -> 
Voice Live speech synthesis -> 
caller audio
```

## Prerequisites

- Access to a Microsoft Foundry project.
- A hosted text agent deployed in the Foundry project. The hosted agent must expose the `invocations_ws` protocol and implement Bridge Protocol version 1.0. For an implementation example, see the [basic Voice-based target agent sample](https://github.com/microsoft-foundry/foundry-samples-pr/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic).
- The name of the hosted agent and, optionally, a specific version to use.

## Create the voice-based agent

Create the voice-based agent by using the project endpoint. Set `conversation_engine.type` to `hosted_agent`, and use `name` to identify the hosted agent that handles the conversation.

Replace the project endpoint, hosted agent name, and optional hosted agent version with your project values.

```python
import requests

from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)
HOSTED_AGENT_NAME = "<hosted-agent-name>"
HOSTED_AGENT_VERSION = "<hosted-agent-version>"

credential = DefaultAzureCredential()
token = credential.get_token("https://ai.azure.com/.default").token

conversation_engine = {
	"type": "hosted_agent",
	"name": HOSTED_AGENT_NAME,
}

if HOSTED_AGENT_VERSION:
	conversation_engine["version"] = HOSTED_AGENT_VERSION

voice_definition = {
	"kind": "voice",
	"conversation_engine": conversation_engine,
	"greeting": {
		"type": "template",
		"text": "Hello! How can I help you today?",
	},
	"store": True,
	"output_modalities": ["audio"],
	"audio": {
		"input": {
			"format": {"type": "audio/pcm", "rate": 24000},
			"turn_detection": {
				"type": "server_vad",
				"threshold": 0.5,
				"prefix_padding_ms": 300,
				"silence_duration_ms": 1000,
			},
			"transcription": {"model": "azure-speech"},
		},
		"output": {
			"format": {"type": "audio/pcm", "rate": 24000},
			"voice": {
				"type": "azure-standard",
				"name": "en-US-JennyNeural",
			},
		},
	},
}

response = requests.post(
	f"{PROJECT_ENDPOINT}/agents?api-version=v1",
	headers={
		"Authorization": f"Bearer {token}",
		"Content-Type": "application/json",
		"Foundry-Features": "VoiceAgents=V1Preview",
	},
	json={
		"name": "hosted-conversation-voice-agent",
		"description": (
			"Voice agent that uses a hosted agent as its conversation engine"
		),
		"definition": voice_definition,
	},
	timeout=30,
)
response.raise_for_status()

voice_agent = response.json()
print(f"Voice agent created: {voice_agent['name']}")
```

To use the hosted agent's latest version instead of pinning a version, set `HOSTED_AGENT_VERSION` to an empty string or remove `version` from the `conversation_engine` object.

The `conversation_engine` object supports the following properties:

| Property | Required | Description |
|---|---|---|
| `type` | Yes | Selects the conversation engine. Set this property to `hosted_agent`. |
| `name` | Yes | Specifies the name of a hosted text agent in the same Foundry project. |
| `version` | No | Pins a hosted-agent version. If you omit this property, the service selects the latest version when the hosted-agent connection is established. |

For this type of voice-based agent, don't specify `model_type` or `model`. Exactly one conversation selection form is allowed: a model-backed definition or an engine-backed definition. The presence of `conversation_engine` selects the engine-backed form.

The hosted agent owns the conversation logic. Therefore, don't configure `instructions`, `reasoning_effort`, `tools`, `tool_choice`, `subagent_config`, or `handoff` on the voice wrapper. You can configure voice-surface properties, including `audio`, `avatar`, `output_modalities`, `greeting`, `structured_inputs`, `store`, and `rai_config`.

The `create` operation validates the conversation engine configuration but doesn't verify the referenced hosted agent. The service resolves the target agent and checks its Voice Live and Bridge Protocol compatibility when a voice session starts.

## Use the voice-based agent

Connect to the voice-based agent's voice WebSocket endpoint to have an interactive conversation. The following Python sample captures 24-kHz PCM audio from your microphone, sends it to the agent, and plays the agent's audio responses.

Install the required packages:

```console
pip install azure-identity "websockets>=14" pyaudio
```

> [!NOTE]
> PyAudio requires PortAudio. If the `pyaudio` installation fails, install the PortAudio development package for your operating system, and then run the `pip install` command again.

Replace the project endpoint and Voice-based agent name with your values:

```python
import asyncio
import base64
import json
import queue
import threading
import uuid

import pyaudio
import websockets
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)
VOICE_AGENT_NAME = "hosted-conversation-voice-agent"

SAMPLE_RATE = 24000
CHANNELS = 1
SAMPLE_WIDTH = 2
CHUNK_FRAMES = 1200


class AudioIO:
	def __init__(self, loop: asyncio.AbstractEventLoop):
		self.loop = loop
		self.audio = pyaudio.PyAudio()
		self.capture_queue: asyncio.Queue[bytes] = asyncio.Queue()
		self.playback_queue: queue.Queue[bytes] = queue.Queue()
		self.remaining_audio = b""
		self.playback_enabled = True
		self.playback_lock = threading.Lock()

		self.input_stream = self.audio.open(
			format=pyaudio.paInt16,
			channels=CHANNELS,
			rate=SAMPLE_RATE,
			input=True,
			frames_per_buffer=CHUNK_FRAMES,
			stream_callback=self._capture,
			start=False,
		)
		self.output_stream = self.audio.open(
			format=pyaudio.paInt16,
			channels=CHANNELS,
			rate=SAMPLE_RATE,
			output=True,
			frames_per_buffer=CHUNK_FRAMES,
			stream_callback=self._playback,
		)

	def _capture(self, audio, _frame_count, _time_info, _status):
		self.loop.call_soon_threadsafe(self.capture_queue.put_nowait, audio)
		return (None, pyaudio.paContinue)

	def _playback(self, _audio, frame_count, _time_info, _status):
		required_bytes = frame_count * SAMPLE_WIDTH
		with self.playback_lock:
			output = self.remaining_audio
			self.remaining_audio = b""

			while len(output) < required_bytes:
				try:
					output += self.playback_queue.get_nowait()
				except queue.Empty:
					output += bytes(required_bytes - len(output))

			self.remaining_audio = output[required_bytes:]
		return (output[:required_bytes], pyaudio.paContinue)

	def start_capture(self):
		self.input_stream.start_stream()

	def play(self, audio):
		with self.playback_lock:
			if self.playback_enabled:
				self.playback_queue.put(audio)

	def start_response(self):
		with self.playback_lock:
			self.playback_enabled = True

	def stop_playback(self):
		with self.playback_lock:
			self.playback_enabled = False
			self.remaining_audio = b""
			while True:
				try:
					self.playback_queue.get_nowait()
				except queue.Empty:
					break

	def close(self):
		if self.input_stream.is_active():
			self.input_stream.stop_stream()
		self.input_stream.close()
		self.output_stream.stop_stream()
		self.output_stream.close()
		self.audio.terminate()


async def send_microphone_audio(websocket, audio_io):
	while True:
		audio = await audio_io.capture_queue.get()
		await websocket.send(
			json.dumps(
				{
					"type": "input_audio_buffer.append",
					"audio": base64.b64encode(audio).decode("ascii"),
				}
			)
		)


async def receive_events(websocket, audio_io, session_ready):
	async for message in websocket:
		if isinstance(message, bytes):
			audio_io.play(message)
			continue

		event = json.loads(message)
		event_type = event.get("type")

		if event_type == "session.updated":
			session_ready.set()
		elif event_type == "input_audio_buffer.speech_started":
			audio_io.stop_playback()
		elif event_type == "response.created":
			audio_io.start_response()
		elif event_type == "conversation.item.input_audio_transcription.completed":
			print(f"You: {event.get('transcript', '')}")
		elif event_type in {
			"response.audio.delta",
			"response.output_audio.delta",
		}:
			audio_io.play(base64.b64decode(event["delta"]))
		elif event_type in {
			"response.audio_transcript.done",
			"response.output_audio_transcript.done",
		}:
			print(f"Agent: {event.get('transcript', '')}")
		elif event_type == "error":
			raise RuntimeError(json.dumps(event, indent=2))


async def talk_to_agent():
	token = DefaultAzureCredential().get_token(
		"https://ai.azure.com/.default"
	).token
	websocket_endpoint = PROJECT_ENDPOINT.replace("https://", "wss://", 1)
	session_id = uuid.uuid4().hex
	url = (
		f"{websocket_endpoint}/agents/{VOICE_AGENT_NAME}"
		f"/endpoint/protocols/voice?api-version=v1"
		f"&agent_session_id={session_id}"
	)

	async with websockets.connect(
		url,
		additional_headers={
			"Authorization": f"Bearer {token}",
			"Foundry-Features": "VoiceAgents=V1Preview",
		},
	) as websocket:
		session_ready = asyncio.Event()
		audio_io = AudioIO(asyncio.get_running_loop())
		receive_task = asyncio.create_task(
			receive_events(websocket, audio_io, session_ready)
		)
		ready_task = asyncio.create_task(session_ready.wait())
		send_task = None

		try:
			done, _ = await asyncio.wait(
				{ready_task, receive_task},
				timeout=10,
				return_when=asyncio.FIRST_COMPLETED,
			)
			if receive_task in done:
				receive_task.result()
				raise ConnectionError("Connection closed before the session was ready.")
			if ready_task not in done:
				raise TimeoutError("The voice session wasn't ready within 10 seconds.")

			print("Connected. Start speaking. Press Ctrl+C to stop.")
			audio_io.start_capture()
			send_task = asyncio.create_task(
				send_microphone_audio(websocket, audio_io)
			)
			done, _ = await asyncio.wait(
				{send_task, receive_task},
				return_when=asyncio.FIRST_COMPLETED,
			)
			for task in done:
				task.result()
		finally:
			tasks = [ready_task, receive_task]
			if send_task is not None:
				tasks.append(send_task)
			for task in tasks:
				task.cancel()
			await asyncio.gather(*tasks, return_exceptions=True)
			audio_io.close()


try:
	asyncio.run(talk_to_agent())
except KeyboardInterrupt:
	print("Conversation ended.")
```

Run the script, start speaking after the connection message appears, and listen for the agent's response through your speakers or headphones. The server-side voice activity detector identifies the end of each turn and starts the agent's response automatically. Press Ctrl+C to end the conversation.
