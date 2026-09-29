---
title: "Use a hosted agent as the conversation engine in a voice-based agent"
description: "Learn how to create a voice-based agent in Microsoft Foundry that uses a hosted agent as its conversation engine, including deployment and SDK setup."
#customer intent: As an agent developer, I want to create a voice-based agent that uses a hosted text agent as its conversation engine so that I can use custom conversation logic.
author: PatrickFarley
ms.author: pafarley
ms.date: 09/28/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: preview
ai-usage: ai-assisted
---

# Use a hosted agent as the conversation engine in a voice-based agent

In this article, you create a voice-based agent in Microsoft Foundry that uses a hosted text agent as its conversation engine. Voice Live provides speech recognition, turn-taking, speech synthesis, and interruption handling. The hosted agent handles conversation logic, model calls, and tools.

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Choose a path based on whether the hosted conversation engine is already deployed:

| Starting point | Path |
| --- | --- |
| You need to deploy the voice-based agent and its hosted conversation engine. | [Deploy both agents with the Azure Developer CLI](#deploy-both-agents-with-the-azure-developer-cli). The sample declares both agents, so you don't create the voice-based agent again with the SDK. |
| You already have a compatible hosted text agent in a Foundry project. | [Create the voice-based agent](#create-the-voice-based-agent) with the Python SDK. |

Both paths use the same [voice client](#use-the-voice-based-agent) and follow this flow:

```text
caller audio -> 
Voice Live speech recognition -> 
hosted text agent -> 
Voice Live speech synthesis -> 
caller audio
```

## Prerequisites

- Access to voice agents and hosted agents in the selected Azure subscription and region.
- A microphone and speakers or a headset.
- For the CLI deployment path, Azure Developer CLI version 1.32.0 or later and the [Foundry extensions](../agents/how-to/install-cli-foundry-extensions.md). Check that the extension exposes the [public-preview voice CLI options](../agents/quickstarts/prompt-voice-agent.md#prerequisites).
- For the CLI deployment path, an authenticated `azd` session. Run `azd auth login` before initialization.
- For the CLI deployment path, the [Azure permissions needed to provision Foundry resources](../agents/how-to/install-cli-foundry-extensions.md#azure-permissions). Confirm model availability and sufficient quota for the sample's `gpt-5.4-mini` deployment.
- For the SDK creation path, an existing Foundry project and a deployed hosted text agent. The target must expose `invocations_ws` and implement Voice Live Bridge Protocol 1.0. Have its agent name and, optionally, the version to use.
- For the SDK creation path, the [Foundry User role](../concepts/rbac-foundry.md) on the project, or equivalent permissions to create and invoke agents.
- For the Python SDK examples, Python 3.10 or later and the Azure CLI, signed in with `az login`.

[!INCLUDE [role-rename-note](../includes/role-rename-note.md)]

The Python examples use version 2.7.0 or later of the Azure AI Projects client library. Install the `voice` extra and the audio dependencies:

```console
python -m pip install "azure-ai-projects[voice]>=2.7.0" azure-identity pyaudio
```

Reference: [Azure AI Projects client library for Python](/python/api/overview/azure/ai-projects-readme).

The `voice` extra installs the realtime transport dependencies, including `aiohttp` for asynchronous sessions. Your code uses the SDK instead of importing the transport libraries directly.

> [!NOTE]
> PyAudio requires PortAudio. If the `pyaudio` installation fails, install the PortAudio development package for your operating system, and then run the `pip install` command again.

## Deploy both agents with the Azure Developer CLI

Use the [Voice Live Bridge basic Python sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic) to deploy the hosted target and voice wrapper together. Its `azure.yaml` defines both agents and configures a Python 3.13 runtime for the hosted target.

This path creates a new Foundry project. To reuse an existing project and model deployment, follow the sample's [existing-project instructions](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic#deploy-to-an-existing-foundry-project) instead. Don't run the new-project provisioning steps below against a shared project.

### Initialize the sample

In PowerShell, create an empty directory and initialize from the public sample manifest:

```powershell
New-Item -ItemType Directory -Path hosted-voice-quickstart
Set-Location hosted-voice-quickstart

$sample = "https://github.com/microsoft-foundry/foundry-samples/" +
    "blob/main/samples/python/hosted-agents/bring-your-own/" +
    "voice-agent-target-agent/basic/azure.yaml"
azd ai agent init -m $sample
```

Reference: [Initialize a hosted agent](../agents/how-to/deploy-hosted-agent.md).

When prompted, select your tenant and subscription, create a new Foundry project, and select a supported region. Review the sample's model selection before continuing.

Change to the generated directory that contains `azure.yaml` by running `Set-Location voice-live-bridge-basic-python`.

### Review the target and voice wrapper

The sample declares two `azure.ai.agent` services:

| Service | Responsibility |
| --- | --- |
| `voice-live-bridge-basic-python` | The `kind: hosted` target. It receives text and control events through Voice Live Bridge Protocol 1.0 over `invocations_ws`, then streams model responses as text. |
| `voice-live-bridge-basic-python-voice` | The `kind: voice` wrapper. It configures the managed audio experience and references the hosted target through `conversationEngine`. |

The wrapper includes these fields under `services` in `azure.yaml`. Keep the sample's existing audio and greeting settings:

```yaml
voice-live-bridge-basic-python-voice:
  host: azure.ai.agent
  kind: voice
  name: voice-live-bridge-basic-python-voice
  uses:
    - ai-project
    - voice-live-bridge-basic-python
  conversationEngine:
    type: hosted_agent
    name: voice-live-bridge-basic-python
  store: false
```

Reference: [Voice service configuration](../agents/concepts/azure-yaml-reference.md#voice-services).

The `uses` dependency deploys the target before the wrapper. In `azure.yaml`, `conversationEngine.name` is the hosted target's service name. The optional `conversationEngine.version` defaults to `deployed`, which pins the wrapper to the target version deployed by the current `azd` environment.

The wrapper and hosted target must have different Foundry agent names. Keep their `name` values distinct if you rename the sample's services.

Keep model calls, instructions, and tools in the hosted target. Configure audio, voice output, and the greeting on the wrapper. Don't use the older `modelType: hosted_agent` or `targetAgent` settings.

The target must declare `invocations_ws` version `1.0.0`, with `voiceLiveCompatible: "true"` and `bridgeProtocolVersion: "1.0"` in its metadata. The sample already supplies these settings. The Bridge Protocol version is distinct from the `invocations_ws` transport version.

This workflow doesn't replace [custom audio pipelines hosted through `invocations_ws`](../agents/how-to/build-voice-agent.md). The hosted target exchanges text and control events with Voice Live rather than processing caller audio itself.

### Provision and deploy both agents

From the generated project directory, provision the new Foundry project and the model declared in `azure.yaml`:

```powershell
azd provision
```

Reference: [azd provision](/azure/developer/azure-developer-cli/reference#azd-provision).

Set the model deployment name that the hosted target reads at runtime:

```powershell
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME gpt-5.4-mini
```

Reference: [azd env set](/azure/developer/azure-developer-cli/reference#azd-env-set).

This variable selects the deployment used by the hosted target. It doesn't create or rename a model deployment.

Deploy all services so that `azd` deploys both the target and the wrapper:

```powershell
azd deploy
```

Reference: [azd deploy](/azure/developer/azure-developer-cli/reference#azd-deploy).

Inspect both agents and confirm that their deployed versions are active:

```powershell
azd ai agent show voice-live-bridge-basic-python
azd ai agent show voice-live-bridge-basic-python-voice
```

Reference: [Deploy a hosted agent](../agents/how-to/deploy-hosted-agent.md) | [Manage hosted agents](../agents/how-to/manage-hosted-agent.md).

For model-backed turns, confirm that the hosted agent's identity has the **Cognitive Services OpenAI User** role on the parent Foundry resource. Equivalent inherited model-inference permissions also work.

Continue to [Use the voice-based agent](#use-the-voice-based-agent) with `voice-live-bridge-basic-python-voice`. Don't run the SDK creation example next: the CLI already created the voice wrapper.

## Create the voice-based agent

Use this alternative when you already have a compatible hosted text agent and want to create its voice wrapper with the SDK. If you deployed both agents with the CLI, skip to [Use the voice-based agent](#use-the-voice-based-agent).

Create the voice-based agent by using `AIProjectClient` and the project endpoint. Set `conversation_engine` to a `VoiceHostedAgentConversationEngine`, and use `name` to identify the deployed hosted agent in that project. The SDK sets the engine's `type` to `hosted_agent`.

Set `allow_preview=True` on `AIProjectClient` to create voice-agent definitions. The SDK adds the required `Foundry-Features: VoiceAgents=V1Preview` header.

Replace the project endpoint, hosted agent name, and optional hosted agent version with your project values. Keep `VOICE_AGENT_NAME` different from `HOSTED_AGENT_NAME`. The example enables conversation storage with `store=True`, which persists transcripts and audio. Use `store=False` if you don't need persistence.

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
	RealtimeAudioFormatsAudioPcm,
	VoiceAgentAudioConfig,
	VoiceAgentAudioInputConfig,
	VoiceAgentAudioOutputConfig,
	VoiceAgentDefinition,
	VoiceAgentInputTranscription,
	VoiceAgentServerVadTurnDetection,
	VoiceAgentTemplateGreetingConfig,
	VoiceHostedAgentConversationEngine,
	VoiceOutputModality,
	VoiceType,
)
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)
HOSTED_AGENT_NAME = "<hosted-agent-name>"
HOSTED_AGENT_VERSION = "<hosted-agent-version>"
VOICE_AGENT_NAME = "hosted-conversation-voice-agent"

conversation_engine = VoiceHostedAgentConversationEngine(
	name=HOSTED_AGENT_NAME,
)

if HOSTED_AGENT_VERSION:
	conversation_engine.version = HOSTED_AGENT_VERSION

voice_definition = VoiceAgentDefinition(
	conversation_engine=conversation_engine,
	greeting=VoiceAgentTemplateGreetingConfig(
		text="Hello! How can I help you today?",
	),
	store=True,
	output_modalities=[VoiceOutputModality.AUDIO],
	audio=VoiceAgentAudioConfig(
		input=VoiceAgentAudioInputConfig(
			format=RealtimeAudioFormatsAudioPcm(rate=24000),
			turn_detection=VoiceAgentServerVadTurnDetection(
				threshold=0.5,
				prefix_padding_ms=300,
				silence_duration_ms=1000,
			),
			transcription=VoiceAgentInputTranscription(
				model="azure-speech",
			),
		),
		output=VoiceAgentAudioOutputConfig(
			format=RealtimeAudioFormatsAudioPcm(rate=24000),
			voice="en-US-JennyNeural",
			voice_type=VoiceType.AZURE_STANDARD,
		),
	),
)

with (
	DefaultAzureCredential() as credential,
	AIProjectClient(
		endpoint=PROJECT_ENDPOINT,
		credential=credential,
		allow_preview=True,
	) as project_client,
):
	voice_agent = project_client.agents.create_version(
		agent_name=VOICE_AGENT_NAME,
		description=(
			"Voice agent that uses a hosted agent as its conversation engine"
		),
		definition=voice_definition,
	)
	print(
		f"Voice agent created: {voice_agent.name}, "
		f"version {voice_agent.version}"
	)
```

Reference: [AgentsOperations.create_version](/python/api/azure-ai-projects/azure.ai.projects.operations.agentsoperations#azure-ai-projects-operations-agentsoperations-create-version) | [VoiceAgentDefinition](/python/api/azure-ai-projects/azure.ai.projects.models.voiceagentdefinition) | [VoiceHostedAgentConversationEngine](/python/api/azure-ai-projects/azure.ai.projects.models.voicehostedagentconversationengine).

The script prints the voice agent's name and new version. Each call to `create_version` creates a new immutable version.

To use the hosted agent's latest version instead of pinning a version, set `HOSTED_AGENT_VERSION` to an empty string. The example then omits `version` from the conversation engine. Unlike the CLI's `conversationEngine.version: deployed` setting, the SDK accepts an actual agent version, not the literal value `deployed`.

The `conversation_engine` object supports the following properties:

| Property | Required | Description |
|---|---|---|
| `type` | Yes | Selects the conversation engine. `VoiceHostedAgentConversationEngine` sets this property to `hosted_agent` automatically. |
| `name` | Yes | Specifies the name of a hosted text agent in the same Foundry project. |
| `version` | No | Pins a hosted-agent version. If you omit this property, the service selects the latest version when the hosted-agent connection is established. |

For this type of voice-based agent, don't specify `model_type` or `model`. Exactly one conversation selection form is allowed: a model-backed definition or an engine-backed definition. The presence of `conversation_engine` selects the engine-backed form.

The hosted agent owns the conversation logic. Therefore, don't configure `instructions`, `reasoning_effort`, `tools`, `tool_choice`, `subagent_config`, or `handoff` on the voice wrapper. You can configure voice-surface properties, including `audio`, `avatar`, `output_modalities`, `greeting`, `structured_inputs`, `store`, and `rai_config`.

The `create_version` operation validates the conversation engine configuration but doesn't verify the referenced hosted agent. The service resolves the target agent and checks its Voice Live and Bridge Protocol compatibility when a voice session starts.

## Use the voice-based agent

Connect to the voice-based agent with `project_client.beta.voice_agents.realtime.connect()`. The SDK handles authentication, the voice WebSocket endpoint, and event serialization. The following Python sample captures 24-kHz PCM audio from your microphone, sends it to the agent, and plays the agent's audio responses.

The voice agent owns its audio configuration and turn detection, so the client doesn't send a `session.update` event. The SDK accepts raw PCM bytes for microphone input and returns decoded audio bytes in typed server events.

Connect to the voice wrapper, not to the hosted text target. Copy the project endpoint from the **Overview** page of your project in the Foundry portal. Set `VOICE_AGENT_NAME` in the following script to the wrapper you created:

| Creation path | `VOICE_AGENT_NAME` |
| --- | --- |
| Azure Developer CLI sample | `voice-live-bridge-basic-python-voice` |
| Python SDK example | `hosted-conversation-voice-agent` |

The CLI sample uses `store: false`; the SDK creation example uses `store=True`. This client works with either setting and doesn't require a persisted conversation ID.

Replace the project endpoint and voice-based agent name with your values:

```python
import asyncio
import queue
import threading
import uuid

import pyaudio
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.aio.operations import AsyncBetaRealtimeConnection
from azure.ai.projects.models import (
	RealtimeServerEventConversationItemInputAudioTranscriptionCompleted,
	RealtimeServerEventError,
	RealtimeServerEventInputAudioBufferSpeechStarted,
	RealtimeServerEventResponseAudioDelta,
	RealtimeServerEventResponseAudioTranscriptDone,
	RealtimeServerEventResponseCreated,
	RealtimeServerEventSessionCreated,
	RealtimeServerEventSessionUpdated,
)
from azure.identity.aio import DefaultAzureCredential

PROJECT_ENDPOINT = (
	"https://<resource>.services.ai.azure.com/api/projects/<project>"
)
VOICE_AGENT_NAME = "voice-live-bridge-basic-python-voice"

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


async def send_microphone_audio(
	connection: AsyncBetaRealtimeConnection, audio_io: AudioIO
):
	while True:
		audio = await audio_io.capture_queue.get()
		await connection.input_audio_buffer.append(audio=audio)


async def receive_events(
	connection: AsyncBetaRealtimeConnection,
	audio_io: AudioIO,
	session_ready: asyncio.Event,
):
	async for event in connection:
		if isinstance(
			event,
			(
				RealtimeServerEventSessionCreated,
				RealtimeServerEventSessionUpdated,
			),
		):
			session_ready.set()
		elif isinstance(
			event, RealtimeServerEventInputAudioBufferSpeechStarted
		):
			audio_io.stop_playback()
		elif isinstance(event, RealtimeServerEventResponseCreated):
			audio_io.start_response()
		elif isinstance(
			event,
			RealtimeServerEventConversationItemInputAudioTranscriptionCompleted,
		):
			print(f"You: {event.transcript}")
		elif isinstance(event, RealtimeServerEventResponseAudioDelta):
			audio_io.play(event.delta)
		elif isinstance(event, RealtimeServerEventResponseAudioTranscriptDone):
			print(f"Agent: {event.transcript}")
		elif isinstance(event, RealtimeServerEventError):
			raise RuntimeError(event.error.message)


async def talk_to_agent():
	async with (
		DefaultAzureCredential() as credential,
		AIProjectClient(
			endpoint=PROJECT_ENDPOINT,
			credential=credential,
			allow_preview=True,
		) as project_client,
		project_client.beta.voice_agents.realtime.connect(
			agent_name=VOICE_AGENT_NAME,
			agent_session_id=uuid.uuid4().hex,
		) as connection,
	):
		session_ready = asyncio.Event()
		audio_io = AudioIO(asyncio.get_running_loop())
		receive_task = asyncio.create_task(
			receive_events(connection, audio_io, session_ready)
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
				raise ConnectionError(
					"Connection closed before the session was ready."
				)
			if ready_task not in done:
				raise TimeoutError(
					"The voice session wasn't ready within 10 seconds."
				)

			print("Connected. Start speaking. Press Ctrl+C to stop.")
			audio_io.start_capture()
			send_task = asyncio.create_task(
				send_microphone_audio(connection, audio_io)
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

Reference: [AsyncBetaRealtime.connect](/python/api/azure-ai-projects/azure.ai.projects.aio.operations.asyncbetarealtime#azure-ai-projects-aio-operations-asyncbetarealtime-connect) | [AsyncBetaRealtimeConnection](/python/api/azure-ai-projects/azure.ai.projects.aio.operations.asyncbetarealtimeconnection).

Run the script, start speaking after the connection message appears, and listen for the agent's response through your speakers or headphones. The server-side voice activity detector identifies the end of each turn and starts the agent's response automatically. Press Ctrl+C to end the conversation.

For a maintained end-to-end SDK example with microphone streaming and interruption handling, see the [Python live-audio conversation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/voice/sample_voice_agent_live_audio_conversation_async.py).

### Test the voice wrapper

Use the preceding client or the Foundry voice playground where available:

1. Ask a short question to exercise the target's model deployment.
1. Confirm that the client prints your input transcription and the agent's response text, and that you hear the response.
1. Speak while the agent responds, and check that playback stops and the agent handles your new turn.

An active agent or a successful text response alone doesn't establish that the audio path works.

For a model-independent check of the sample's hosted target, use its [local protocol smoke client](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic#local-protocol-smoke-test). It sends `/help` through the Bridge Protocol without calling a model. This check verifies the target's protocol handling, not the managed voice audio path.

`azd ai agent invoke` doesn't generate Voice Live conversations. Selecting the voice wrapper returns [portal guidance](../agents/how-to/invoke-hosted-agent.md#voice-agent-limitations), not a voice session.

## Troubleshoot

| Symptom | Action |
| --- | --- |
| Initialization reports `not logged in`. | Sign in with `azd auth login`, and run initialization again. |
| The extension doesn't recognize the voice options or `conversationEngine`. | Check the installed extension's [voice support](../agents/quickstarts/prompt-voice-agent.md#prerequisites) before continuing. |
| Wrapper deployment can't resolve its target. | Check that `conversationEngine.name` matches the hosted service name, that `uses` includes it, and that the target is active. |
| `/help` works, but model-backed turns fail. | Check the target's `AZURE_AI_MODEL_DEPLOYMENT_NAME`, model availability, and managed identity permissions for model inference. |
| The target reports `protocol_mismatch`. | Check Bridge Protocol 1.0 compatibility. The Bridge Protocol version is distinct from the `invocations_ws` transport version. |
| The SDK can't find the voice wrapper. | Use the wrapper name for your chosen creation path and the endpoint of the project that contains both agents. |

## Clean up resources

For the new project created by the CLI deployment path, run the following command from its generated project directory:

> [!WARNING]
> `azd down` deletes the resource group and all resources created for this environment. Don't use it to clean up individual agents in a shared project.

```powershell
azd down
```

Reference: [azd down](/azure/developer/azure-developer-cli/reference#azd-down).

For the SDK creation path, delete only the voice wrapper you created by calling `project_client.agents.delete(agent_name=VOICE_AGENT_NAME)` with an authenticated `AIProjectClient`. Keep any pre-existing hosted target, model deployment, and shared project.

## Related content

For related configuration and development workflows, see:

- [Configure a voice agent](../agents/how-to/configure-voice-agent.md).
- [azure.yaml reference](../agents/concepts/azure-yaml-reference.md).
- [Build a custom voice pipeline with hosted agents](../agents/how-to/build-voice-agent.md).
