---
title: "Use a subagent in a Voice-based agent"
description: "Learn how to add, configure, and test a subagent that handles a focused task for a Voice-based agent in Microsoft Foundry."
#customer intent: As an agent developer, I want to use a subagent in a Voice-based agent so that it can delegate a focused task.
author: PatrickFarley
ms.author: pafarley
ms.date: 09/22/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: preview
ai-usage: ai-assisted
---

# Use a subagent in a Voice-based agent

In this article, you use a subagent in a Voice-based agent, define when the agent delegates work to the subagent, and test the resulting voice experience.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Introduction

When creating a Voice-based agent, you can add one or more subagents that handle specific tasks. The main agent delegates requests to the subagent when the request
matches the subagent's defined capabilities.

The subagent can be Foundry prompt agents, or Foundry hosted agents.

The following section shows how to create a prompt agent, and use it as a subagent for a Voice-based agent. You can also apply similar steps to a hosted agent.

> Note: Subagents aren't supported for voice-based agents in projects configured with virtual network (VNet) isolation.

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with access to voice-based agents.
- [Foundry User role](../../concepts/rbac-foundry.md) on the project.
  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- Python 3.10 or later.
- The Azure CLI, signed in with `az login`.
- A voice model and a text model available to your project.
- A microphone and speakers or headphones.

## Install the packages

Install the Microsoft Foundry SDK version 2.7.0 or later with the `voice` extra,
Azure Identity client library, and PyAudio in the same Python environment.
The `voice` extra supplies `aiohttp` for asynchronous connections.
PyAudio handles microphone capture and speaker playback.

```bash
python -m pip install "azure-ai-projects[voice]>=2.7.0" azure-identity pyaudio
```

For Python SDK setup details, see [Install the packages](../quickstarts/prompt-voice-agent.md?pivots=python#install-the-packages).

## Set environment variables

Set the project endpoint and model deployment names. In Bash:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_SUBAGENT_MODEL="<text-model-deployment-name>"
export FOUNDRY_VOICE_MODEL="gpt-realtime"
```

In PowerShell:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_SUBAGENT_MODEL = "<text-model-deployment-name>"
$env:FOUNDRY_VOICE_MODEL = "gpt-realtime"
```

Find the project endpoint on the **Overview** page of your project in the
Foundry portal.

## Create a subagent

Create a prompt agent with one focused responsibility. The following example
creates a subagent that writes poems based on a user's requested topic and
style.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model = os.environ["FOUNDRY_SUBAGENT_MODEL"]

definition = PromptAgentDefinition(
    model=model,
    instructions=(
        "You are a poetry-writing agent. Write an original poem that "
        "matches the user's requested topic, style, tone, and length. "
        "When the request doesn't specify these details, write a short "
        "poem in free verse. Return only the poem."
    ),
)

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    poetry_agent = project_client.agents.create_version(
        agent_name="poetry-agent",
        definition=definition,
    )
    print(
        f"Created subagent '{poetry_agent.name}', "
        f"version {poetry_agent.version}"
    )
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

You can also create a subagent in the Microsoft Foundry portal or deploy a code-based hosted agent.

## Use the subagent in the Voice-based agent

Create the Voice-based agent by using the project endpoint. In
`subagent_config`, identify the poetry agent by name and describe when the
Voice-based agent delegates a request to it.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RealtimeAudioFormatsAudioPcm,
    VoiceAgentAudioConfig,
    VoiceAgentAudioInputConfig,
    VoiceAgentAudioOutputConfig,
    VoiceAgentDefinition,
    VoiceAgentInputTranscription,
    VoiceAgentServerVadTurnDetection,
    VoiceAgentSubagent,
    VoiceAgentSubagentConfig,
    VoiceAgentSubagentResponsePolicy,
)
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
model = os.environ.get("FOUNDRY_VOICE_MODEL", "gpt-realtime")

definition = VoiceAgentDefinition(
    model_type="managed",
    model=model,
    instructions=(
        "Answer ordinary questions yourself. When the user asks for a poem, "
        "always call forward_to_subagent for the configured poetry agent. "
        "After the poetry agent returns, read the poem exactly as written."
    ),
    store=True,
    output_modalities=["audio"],
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
            voice_type="azure-standard",
        ),
    ),
    subagent_config=VoiceAgentSubagentConfig(
        subagents=[
            VoiceAgentSubagent(
                agent_name="poetry-agent",
                agent_capabilities=(
                    "Writes original poems based on the requested topic, "
                    "style, tone, and length."
                ),
                response_policy=VoiceAgentSubagentResponsePolicy(
                    immediate_ack=True,
                ),
            )
        ],
    ),
)

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint,
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    voice_agent = project_client.agents.create_version(
        agent_name="poetry-voice-agent",
        definition=definition,
        description="Voice agent that delegates poetry requests",
    )
    print(
        f"Created voice agent '{voice_agent.name}', "
        f"version {voice_agent.version}"
    )
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

## Talk to the voice agent

Connect to the voice agent with the Microsoft Foundry SDK. The client streams
microphone audio to the agent and plays the spoken response as it arrives. Use
headphones to prevent the speaker output from feeding back into the microphone.
Run the package installation command with the same Python environment that you
use to run the client.

Create a file named `talk_to_voice_agent.py`:

```python
import asyncio
import os

import pyaudio
from azure.ai.projects import models
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.aio.operations import AsyncBetaRealtimeConnection
from azure.identity.aio import DefaultAzureCredential

RATE = 24000
CHUNK = 2400


async def wait_until_ready(
    connection: AsyncBetaRealtimeConnection,
) -> None:
    while True:
        event = await connection.recv()
        if isinstance(event, models.RealtimeServerEventSessionCreated):
            return
        if isinstance(event, models.RealtimeServerEventError):
            raise RuntimeError(event.error.message)


async def send_microphone(
    connection: AsyncBetaRealtimeConnection, stream: pyaudio.Stream
) -> None:
    while True:
        audio = await asyncio.to_thread(
            stream.read,
            CHUNK,
            exception_on_overflow=False,
        )
        await connection.input_audio_buffer.append(audio=audio)


async def receive_audio(
    connection: AsyncBetaRealtimeConnection, stream: pyaudio.Stream
) -> None:
    async for event in connection:
        if isinstance(
            event,
            models.RealtimeServerEventResponseAudioDelta,
        ):
            await asyncio.to_thread(stream.write, event.delta)
        elif isinstance(
            event,
            models.RealtimeServerEventResponseAudioTranscriptDone,
        ):
            print(f"Agent: {event.transcript}")
        elif isinstance(event, models.RealtimeServerEventError):
            raise RuntimeError(event.error.message)


async def talk() -> None:
    endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
    audio = pyaudio.PyAudio()
    microphone = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )
    speaker = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )

    try:
        async with (
            DefaultAzureCredential() as credential,
            AIProjectClient(
                endpoint=endpoint,
                credential=credential,
                allow_preview=True,
            ) as project_client,
            project_client.beta.voice_agents.realtime.connect(
                agent_name="poetry-voice-agent",
            ) as connection,
        ):
            await asyncio.wait_for(wait_until_ready(connection), timeout=30)
            print("Connected. Ask the agent to write a poem.")
            await asyncio.gather(
                send_microphone(connection, microphone),
                receive_audio(connection, speaker),
            )
    finally:
        microphone.close()
        speaker.close()
        audio.terminate()


asyncio.run(talk())
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

The client waits for `session.created` before streaming microphone audio.
It uses the agent's saved configuration, so it doesn't send `session.update`
or wait for `session.updated`.

Run the client:

```bash
python talk_to_voice_agent.py
```

After the client connects, ask it to write a short poem about the sea. The
voice agent delegates the request to `poetry-agent` and speaks the returned
poem. Press `Ctrl+C` to disconnect.


## Use the voice agent in the Foundry portal

Open the voice agent in the playground to have a spoken conversation:

1. Sign in to the [Foundry portal](https://ai.azure.com).
1. Open the project that contains the voice agent and subagent.
1. Select **Build** > **Agents**.
1. Select **poetry-voice-agent**, and then select **Open in playground**.
1. Start a voice session.
1. Ask the agent to write a short poem about the sea.

The voice agent delegates the request to `poetry-agent` and speaks the returned
poem.

## Configure subagent behavior

The `subagent_config` object identifies the text agents that the Voice-based
agent can consult. Each subagent must belong to the same Foundry project as the
Voice-based agent. Configure at least one entry in the `subagents` array.

| Property | Required | Description |
|---|---|---|
| `agent_name` | Yes | Specifies the name of the subagent. |
| `agent_version` | No | Pins a specific subagent version. If you omit this property, the voice agent uses the active version. |
| `agent_capabilities` | Yes | Describes the subagent's specialization. The voice agent uses this description to decide whether to forward a request. |
| `invoke_timeout_seconds` | No | Sets the invocation timeout from 5 through 1,200 seconds. If you omit this property, the service timeout applies. |

Use the optional `response_policy` object to control what the voice agent says
while it waits for a subagent:

| Property | Description |
|---|---|
| `immediate_ack` | Specifies whether the voice agent immediately acknowledges that it forwarded the request. |
| `ack_instructions` | Provides instructions for generating the immediate acknowledgment. |
| `enable_delta_progress` | Emits progress incrementally instead of waiting for the subagent invocation to finish. The default is `false`. |
| `gap_filling_interval` | Sets the period without subagent content or user input before a gap-filling response. Use a value from 5 through 120 seconds. |
| `gap_filling_instructions` | Provides instructions for speech generated while the voice agent waits for progress. |
| `progress_instructions` | Provides instructions for summarizing streamed subagent progress as speech. |
| `progress_update_interval` | Sets the minimum time between spoken progress updates. Use a value from 5 through 300 seconds. |

In Python, use `datetime.timedelta` for `invoke_timeout_seconds`,
`gap_filling_interval`, and `progress_update_interval`.
The SDK serializes these values as seconds.

## Apply subagent best practices

- Give each subagent one clearly defined capability.
- Tune the agent's instructions to delegate requests to the subagent when appropriate.

## Related content

- [Configure a voice agent](configure-voice-agent.md)
- [Optimize voice agent instructions](optimize-voice-agent-instructions.md)
- [Integrate telephony channels with a voice agent](voice-agent-telephony-channels.md)
