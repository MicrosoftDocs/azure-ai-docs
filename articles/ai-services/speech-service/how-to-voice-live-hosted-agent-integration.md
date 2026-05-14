---
title: Use Voice Live with hosted agents
titleSuffix: Foundry Tools
description: Learn how to integrate Voice Live with Microsoft Foundry hosted agents using both the Responses and Invocations protocols.
ms.service: azure-ai-speech
ms.topic: how-to
ms.date: 05/14/2026
author: 
reviewer: 
ms.author: 
ms.reviewer: 
ai-usage: ai-assisted
# Customer intent: As a developer, I want to add real-time voice interaction to my Microsoft Foundry hosted agent so that users can speak to the agent and hear responses.
---

# Use Voice Live with hosted agents

Here's how to integrate Azure Voice Live with your [Microsoft Foundry hosted agents](../../foundry/agents/how-to/deploy-hosted-agent.md) to enable real-time voice interaction.
    
Once you deploy a hosted agent to Microsoft Foundry, you can add real-time voice interaction using the [Azure VoiceLive SDK](https://pypi.org/project/azure-ai-voicelive/). 

Hosted agents support two protocols — **Responses** and **Invocations**. Voice Live works with both with a little difference. This article covers both protocols.

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- A [Microsoft Foundry resource](../multi-service-resource.md) in a [supported region](./voice-live.md#supported-models-and-regions).
- A hosted agent deployed to Microsoft Foundry. If you don't have one, see [Deploy a hosted agent](../../foundry/agents/how-to/deploy-hosted-agent.md).
- Python 3.10 or later.
- A working microphone and speakers on your machine.
- The `Azure AI User` role assigned to your user account. Assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

Install the required packages:

```bash
pip install azure-ai-voicelive[aiohttp]==1.2.0b5 azure-identity pyaudio
```

> [!NOTE]
> On Linux, install PortAudio first: `sudo apt-get install -y portaudio19-dev libasound2-dev`

## Use Voice Live with a Responses protocol agent

For agents that use the Responses protocol, Voice Live connects directly through the `AgentSessionConfig`.

```python
agent_config: AgentSessionConfig = {
    "agent_name": "<your-agent-name>",
    "project_name": "<your-foundry-project-name>",
}
```

### Configure the session

The following example shows how to initialize a Voice Live session with a hosted agent using the `AgentSessionConfig`:

```python
from azure.ai.voicelive.aio import connect, AgentSessionConfig
from azure.ai.voicelive.models import (
    AudioEchoCancellation,
    AudioNoiseReduction,
    AzureStandardVoice,
    InputAudioFormat,
    Modality,
    OutputAudioFormat,
    RequestSession,
    ServerVad,
)
from azure.identity.aio import DefaultAzureCredential

endpoint = "https://<your-foundry-resource>.services.ai.azure.com"
credential = DefaultAzureCredential()

agent_config: AgentSessionConfig = {
    "agent_name": "<your-agent-name>",
    "project_name": "<your-foundry-project-name>",
}

async with connect(
    endpoint=endpoint,
    credential=credential,
    agent_config=agent_config,
) as connection:
    # Configure session settings
    session_config = RequestSession(
        modalities=[Modality.TEXT, Modality.AUDIO],
        voice=AzureStandardVoice(name="en-US-Ava:DragonHDLatestNeural"),
        input_audio_format=InputAudioFormat.PCM16,
        output_audio_format=OutputAudioFormat.PCM16,
        turn_detection=ServerVad(),
        input_audio_echo_cancellation=AudioEchoCancellation(),
        input_audio_noise_reduction=AudioNoiseReduction(
            type="azure_deep_noise_suppression"
        ),
    )
    await connection.session.update(session=session_config)
```

Reference: [VoiceLive SDK (azure-ai-voicelive)](https://pypi.org/project/azure-ai-voicelive/) | [AgentSessionConfig](/python/api/azure-ai-voicelive/azure.ai.voicelive)

### Process events

After configuring the session, capture microphone audio and handle events from the connection. The key events for voice interaction are:

| Event | Description |
|-------|-------------|
| `SESSION_UPDATED` | Session is ready. Start audio capture. |
| `INPUT_AUDIO_BUFFER_SPEECH_STARTED` | User started speaking. Skip any queued playback audio. |
| `INPUT_AUDIO_BUFFER_SPEECH_STOPPED` | User stopped speaking. |
| `RESPONSE_AUDIO_DELTA` | Incremental audio from the agent. Queue for playback. |
| `RESPONSE_AUDIO_DONE` | Agent finished speaking. |
| `CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED` | Transcription of user speech. |

### Sample Voice Live client

For a complete working example, see [voicelive_client.py](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/bring-your-own/voicelive/client/voicelive_client.py) on GitHub.

Use the shared Voice Live client to connect to your deployed agent. The client authenticates with `DefaultAzureCredential`, so sign in first with `az login`.

```bash
python voicelive_client.py \
  --endpoint "https://<your-foundry-resource>.services.ai.azure.com" \
  --agent-name "<your-agent-name>" \
  --project-name "<your-foundry-project-name>"
```

Speak into your microphone. The agent responds with synthesized speech. Press Ctrl+C to end the session.

## Use Voice Live with an Invocations protocol agent

For agents that use the Invocations protocol, Voice Live handles speech-to-text and text-to-speech while the agent processes structured input and returns streaming text.

### Make an Invocations agent compatible with Voice Live

An Invocations agent must meet three requirements to work with Voice Live:

1. **Accept voice transcription input**: The agent must process incoming messages in this format:

    ```json
    {"type": "input_audio.transcription", "input": "example voice input"}
    ```

1. **Return streaming text as SSE events**: The agent must return text to be spoken as server-sent events (SSE) using the `output_audio_transcription` event types. Voice Live synthesizes audio from the `delta` text:

    ```text
    data: {"type": "output_audio_transcription.delta", "delta": "The weather "}
    data: {"type": "output_audio_transcription.delta", "delta": "in Seattle "}
    data: {"type": "output_audio_transcription.delta", "delta": "is 52°F "}
    data: {"type": "output_audio_transcription.delta", "delta": "and partly cloudy."}
    data: {"type": "output_audio_transcription.done", "text": "The weather in Seattle is 52°F and partly cloudy."}
    data: {"type": "done"}
    ```

1. **Declare Voice Live compatibility in the agent manifest**: Add `voiceLiveCompatible: "true"` to the `metadata` section of your `agent.manifest.yaml`:

    ```yaml
    metadata:
      voiceLiveCompatible: "true"
    ```

For a complete Invocations agent sample compatible with Voice Live, see [hello-world-invocations-voicelive](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voicelive/hello-world-invocations-voicelive) on GitHub.

### Connect with Voice Live

Once your Invocations agent is deployed, you can start a voice conversation using the same Voice Live client, similar to a Responses protocol agent. See [Sample Voice Live client](#sample-voice-live-client) for the connection steps.



## Related content

- [Voice Live overview](./voice-live.md)
- [How to build a voice agent](./how-to-voice-agent-integration.md)
- [How to use the Voice Live API](./voice-live-how-to.md)
- [Voice Live API reference](./voice-live-api-reference-2026-04-10.md)
- [Hosted agents overview](/azure/foundry/agents/concepts/hosted-agents)
- [Microsoft Foundry hosted agent samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents)
