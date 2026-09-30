---
title: "Migrate from Voice Live with Foundry Agent Service to Microsoft Foundry voice agents"
description: "Compare model support, hosting, and voice experiences in Voice Live with Foundry Agent Service and Microsoft Foundry voice agents, then plan your migration."
author: yulin-li
ms.author: yulili
ms.date: 09/30/2026
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: preview
ai-usage: ai-assisted
#customer intent: As a developer using Voice Live with a Foundry text agent, I want to compare and migrate to a managed voice agent while preserving my application's behavior.
---

# Migrate from Voice Live with Foundry Agent Service to Microsoft Foundry voice agents

In this article, you compare [Voice Live with Foundry Agent Service](../../../ai-services/speech-service/voice-live-agents-quickstart.md) with voice-based prompt agents in Microsoft Foundry. Then you migrate your voice experience while keeping the existing text agent available.

Here, *Voice Live integration* means Voice Live connected to an existing Foundry text agent. A *Foundry voice agent* is a separate agent with `kind: voice`. It still uses Voice Live for the voice runtime, but you manage its model, instructions, audio, and tools as an agent definition.

Migration creates a new agent alongside the original. You can't change an existing text agent's interaction mode to voice. This process is separate from [migrating Agent Service (classic) to the new Agent Service](migrate.md).

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- A working Voice Live integration with a Foundry text agent, including access to its configuration and client code.
- A [Foundry project](../../how-to/create-projects.md) with access to the voice-agent preview and a supported model in the project's region.
- [Foundry User role](../../concepts/rbac-foundry.md) on the target project, with permission to create and invoke agents.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- Access to the tool connections and data resources that the migrated agent needs. Have a resource owner grant any required permissions.
- A microphone and speakers or a headset for testing spoken conversations.
- For the Python connection example, Python 3.10 or later and the Azure CLI, signed in with `az login`.

## Compare the two approaches

Compare the models you can use, who manages them, and how you operate the voice experience. Both approaches provide configurable voices, turn detection, and interruption handling through Voice Live.

The Voice Live column refers only to the Foundry text-agent integration. [Voice Live used directly](../../../ai-services/speech-service/voice-live.md) also supports speech-to-speech models.

| Customer consideration | Voice Live with Foundry Agent Service | Foundry voice agent |
| --- | --- | --- |
| Supported models | Text models supported by the connected Foundry agent. | Both speech-to-speech models, such as `gpt-realtime`, and supported text models. |
| Model hosting and capacity | Uses the model deployment selected for your Foundry text agent. | For either model family, choose a self-deployed model or a voice-agent service-managed model. Service-managed models don't require you to maintain a model deployment. |
| Conversational experience | Voice Live converts speech to text for the agent and synthesizes its text response. | Choose native speech-to-speech interaction or a text-model pipeline with speech recognition and synthesis. Latency depends on the selected model, prompts, tools, and channel. |
| Existing tools and knowledge | Keep the business logic, tools, and knowledge configured on your text agent. | Provides the same tool and knowledge coverage as Foundry text agents. Configure them for the voice agent, or reuse an existing text agent as a specialist subagent. |
| Configure voice behavior | Tune speech through Voice Live and manage the text agent's instructions and tools separately. | Manage the model, instructions, voice, greeting, and turn-taking together in Foundry. Save and test changes as agent versions. |
| Connect phone callers | Integrate your application with a telephony provider, using provider APIs or a [solution accelerator](../../../ai-services/speech-service/voice-live-telephony.md). You manage the integration. | Built-in [telephony integration](voice-agent-telephony-channels.md) supports inbound and outbound calls through Teams Phone extensibility and Twilio. Configure the provider connection and, for inbound calls, bind a phone number in Foundry. |
| Review customer conversations | Review text-agent conversation history and the logs your application captures. Text history might differ from what a caller heard before an interruption. | Opt in to persisted transcripts, conversation events, and audio for review. Recording is off by default. |
| Diagnose delays and failures | View traces of the text-model interaction. Turn detection, audio input, and audio output aren't included in the agent trace. | Trace the voice pipeline, including turn detection, audio input, model and tool calls, and audio output. |
| Plan costs | Account for your Voice Live usage, the text agent's model deployment, and dependent tools and services. | Model hosting, audio usage, tools, and optional recordings or avatars affect cost. Compare service-managed model usage with the cost of your own supported deployment. |

Choose a Foundry voice agent for speech-to-speech models, service-managed model hosting, built-in telephony, or integrated voice configuration and call review. You can also keep a supported text-model approach; migration doesn't require switching to `gpt-realtime`.

Model, region, network, and transport restrictions still apply. Measure conversation quality, latency, and cost with your workload before switching.

## Choose how to reuse your existing agent

Choose the conversation design before copying configuration. Reusing a text agent as a specialist is different from forwarding every spoken turn to it.

| Migration approach | Use it when | What to change |
| --- | --- | --- |
| Create a model-backed voice agent | You want the voice agent to handle the conversation and call tools directly. | Adapt the instructions, select a supported model, and reconfigure tools for the voice agent. |
| Keep the text agent as a subagent | You want to retain specialist reasoning, retrieval, or business logic in an existing prompt or hosted agent. | Configure `subagent_config` and describe when to delegate. The voice agent handles the conversation and consults the specialist as needed. |
| Use a hosted conversation engine | Your hosted code must own the conversation logic for every turn. | Follow the separate [hosted conversation engine guide](../../how-to/voice-first-with-hosted-agent.md). The target needs the required `invocations_ws` Bridge Protocol implementation; a text endpoint alone isn't sufficient. |

For the subagent approach, the subagent must be in the same project as the voice agent. Subagents aren't supported in VNet-isolated projects. Follow [Use a subagent in a voice-based agent](use-subagent-voice-first-agent.md) and test delegation, follow-up questions, and failure behavior.

The remaining steps focus on a model-backed voice agent, with optional subagents. A custom hosted voice application that exposes `invocations_ws` is a different integration; see [Build a voice agent with hosted agents](build-voice-agent.md).

## Inventory the source and create a new agent

Capture the effective configuration, not just the values stored on the text agent.

1. Record the source agent name and version, model deployment, instructions, tools, and project connections.
1. Export the Voice Live settings. If you used the integration sample, reassemble `microsoft.voice-live.configuration` and its numbered metadata entries, such as `.1` and `.2`, in order.
1. Record any client-side `session.update` overrides, proactive greeting code, audio formats, interruption handling, and channel configuration.
1. Record authentication and cross-resource dependencies, including any `foundry_resource_override` and managed identity settings. Don't copy credentials into the new agent definition.
1. Follow [Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md) to create an agent with a **new name**. In the portal, select **Voice** as the interaction mode. In code, use `VoiceAgentDefinition` instead of `PromptAgentDefinition`.
1. Choose a supported speech-to-speech model, such as `gpt-realtime`, or a supported text model. Both model families support service-managed and self-deployed options.
1. Set `model_type` to `managed` for a service-managed model, or `self_deployed` for your own supported deployment. Don't treat a deployment name as a managed model name.
1. Adapt the instructions for spoken interaction: short answers, one question at a time, and explicit confirmation before consequential actions. Preserve the source agent's business rules and escalation requirements.
1. Save the new agent version and record its name and version for testing. Keep the original text agent and client configuration unchanged until the new path is ready.

For SDK creation examples, use the [explicit-definition quickstart](../quickstarts/prompt-voice-agent.md?pivots=python#create-from-an-explicit-definition). Creating a voice agent version doesn't copy the source agent's tools, connections, or conversation history.

## Move voice settings into the definition

Translate the settings rather than copying the old session object into metadata. The following table uses the JSON field names from the Voice Live integration samples and the voice-agent definition.

| Existing setting | Voice-agent definition field | Migration action |
| --- | --- | --- |
| Text-agent instructions | `instructions` | Adapt the instructions for speech, or keep specialist instructions on the subagent. |
| `session.voice.name` | `audio.output.voice` | Set the voice name as a string, not a nested voice object. |
| `session.voice.type` | `audio.output.voice_type` | Set the provider type, such as `azure-standard`. |
| `session.voice.temperature` | `audio.output.voice_temperature` | Preserve the setting only for a voice type that supports it. |
| `session.input_audio_transcription` | `audio.input.transcription` | Set the transcription model explicitly and carry over supported language and vocabulary settings. |
| `session.turn_detection` | `audio.input.turn_detection` | Review pause detection, automatic response creation, interruption, and truncation settings. |
| `session.input_audio_noise_reduction` | `audio.input.noise_reduction` | Preserve the supported noise-reduction configuration. |
| `session.input_audio_echo_cancellation` | `audio.input.echo_cancellation` | Match the reference source and channel layout to your client. |
| `session.input_audio_format` and `session.output_audio_format` | `audio.input.format` and `audio.output.format` | Use format objects, such as `{"type":"audio/pcm","rate":24000}`, instead of the legacy `pcm16` string. |
| `session.modalities` | `output_modalities` | Select the supported output modalities. Audio output defaults to `["audio"]`; don't copy the old array without reviewing it. |
| `session.interim_response` | `interim_response` | Reconfigure latency or tool-wait responses on the definition. |
| Client-generated opening message | `greeting` | Choose a fixed template or an LLM-generated greeting. Remove the old startup trigger if the new greeting replaces it. |

For the complete schema and SDK examples, see [Configure a voice agent](configure-voice-agent.md). SDK and `azure.yaml` property names can differ from the JSON names in this table.

The service applies the definition when a session starts. Remove client startup code that resends the full legacy session configuration. Keep only supported per-session overrides, such as audio or avatar settings, and verify the effective configuration returned by the service.

## Reconnect tools and knowledge

Voice agents provide the same tool and knowledge coverage as text agents, but configuration and execution paths differ. Map the existing integrations to the voice-agent tool interfaces instead of copying the text agent's `tools` array unchanged. Confirm which identity accesses each dependency.

- For a native `function` tool, configure its schema on the voice agent and implement the function-call response in your live client. A schema alone doesn't execute the function.
- For an MCP tool, configure the server and the required project connection or authentication. Verify access from the target project.
- For Foundry server-side tools, such as Azure AI Search or OpenAPI tools, create or reuse a supported toolbox and reference its name and version.
- For a retained text subagent, configure its name, capabilities, and optional version. Test which requests the voice agent answers directly and which it delegates.
- Test successful calls, denied permissions, timeouts, and unavailable dependencies before moving user traffic.

See [Attach tools](configure-voice-agent.md#attach-tools) for configuration details and the [client-executed function sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/voice-agents/voice_agent_realtime_function_tool.py) for the live tool-call loop.

## Update the client connection

Use the Foundry **project endpoint**, not the Voice Live resource endpoint. The project endpoint has this form: `https://<account>.services.ai.azure.com/api/projects/<project>`.

The voice-agent API uses `api-version=v1`, but voice agents remain a preview feature. REST requests require the `Foundry-Features: VoiceAgents=V1Preview` opt-in. The Python realtime helper supplies this header automatically.

For a raw WebSocket client, use `wss://` and replace `/voice-live/realtime` with `/api/projects/<project>/agents/<agent-name>/endpoint/protocols/voice?api-version=v1`. Request a Microsoft Entra token for `https://ai.azure.com/.default`, send it in the `Authorization` header, and include the voice-agent preview opt-in.

Resource API keys aren't a substitute for agent authentication. Don't put bearer tokens in the URL or long-lived credentials in browser code.

The project and agent are now part of the endpoint path. Review any old cross-resource connection parameters separately rather than appending them to the new URL.

### Check the connection with Python

In Python, replace the `azure-ai-voicelive` live-session connection with `azure-ai-projects` and `beta.voice_agents.realtime`.

Install the Azure AI Projects client library with its voice dependencies:

```bash
python -m pip install "azure-ai-projects[voice]>=2.7.0" azure-identity
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Set these environment variables in the shell that runs the example:

| Variable | Value |
| --- | --- |
| `FOUNDRY_PROJECT_ENDPOINT` | The target Foundry project endpoint. |
| `FOUNDRY_VOICE_AGENT_NAME` | The **new voice agent's** name, not the source text agent's name. |
| `FOUNDRY_VOICE_AGENT_VERSION` | The voice-agent version you saved for testing. |

Save the following example as `check_voice_connection.py`, and run it with `python check_voice_connection.py`. It opens a session against that exact version, waits for configuration to complete, and then closes the connection. It doesn't send microphone audio.

```python
import os
import time

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RealtimeServerEventError,
    RealtimeServerEventSessionCreated,
    RealtimeServerEventSessionUpdated,
)
from azure.identity import DefaultAzureCredential

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        credential=credential,
        allow_preview=True,
    ) as project_client,
):
    with project_client.beta.voice_agents.realtime.connect(
        agent_name=os.environ["FOUNDRY_VOICE_AGENT_NAME"],
        api_version="v1",
        extra_query={
            "x-agent-version-override": os.environ[
                "FOUNDRY_VOICE_AGENT_VERSION"
            ],
        },
    ) as connection:
        deadline = time.monotonic() + 45
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("Voice session didn't become ready.")
            event = connection.recv(timeout=remaining)
            if isinstance(event, RealtimeServerEventError):
                raise RuntimeError(event.error.message)
            if isinstance(event, RealtimeServerEventSessionCreated):
                if event.conversation_id:
                    print(f"Conversation ID: {event.conversation_id}")
            elif isinstance(event, RealtimeServerEventSessionUpdated):
                print("Voice session ready.")
                break
```

Reference: [Python realtime client and event models](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/azure/ai/projects/_realtime.py).

The expected result is `Voice session ready.`. For a complete spoken turn, follow [Talk to the agent](../quickstarts/prompt-voice-agent.md?pivots=python#talk-to-the-agent) or adapt the [live microphone sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/voice-agents/voice_agent_realtime_audio_conversation_async.py).

Use the current Projects SDK samples for the public preview. Earlier private-preview samples that use a separate `azure-ai-voiceagents` package or `/voice_agents` management route don't describe this API.

### Adapt audio and event handling

The new endpoint isn't just a URL replacement for an older Voice Live API. For raw JSON clients, update these event families, including their `delta` and `done` events:

| Older event family | Voice-agent `v1` event family |
| --- | --- |
| `response.audio.*` | `response.output_audio.*` |
| `response.audio_transcript.*` | `response.output_audio_transcript.*` |
| `response.text.*` | `response.output_text.*` |

The Projects SDK maps these events to typed models. For example, `RealtimeServerEventResponseAudioDelta` represents `response.output_audio.delta`, and its `delta` contains decoded audio bytes.

Before enabling microphone input, wait for `session.updated`. Match the input and output formats to the saved definition. Preserve local playback-buffer clearing when the caller interrupts; canceling generation alone doesn't clear audio already queued on the device.

If the definition includes a greeting, handle its response separately from the reply to the first user turn. Don't send the old proactive greeting as well.

WebRTC isn't a drop-in substitute for WebSocket. The current voice-agent WebRTC transport doesn't support self-deployed models or hosted conversation engines. Use WebSocket for those configurations and validate each required browser or telephony path separately.

## Configure history, recordings, and monitoring

Treat the new voice conversation as a new record, not as a continuation of the old text-agent conversation.

- Start a new voice conversation at cutover. Retain prior text-agent history according to your existing policy; don't pass its conversation ID expecting an automatic import.
- Decide whether to enable `store`. Its default is `false`. Setting it to `true` stores the transcript, event timeline, and raw audio together, so review notice, consent, access, and retention requirements first.
- Capture the voice conversation ID from `session.created` for correlation and, when storage is enabled, read-back through `beta.voice_agents.conversations`. Don't confuse it with a realtime session ID.
- Retrieve merged recordings after the session ends. Recording finalization isn't necessarily immediate; follow the [conversation audio sample](https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/voice-agents/voice_agent_read_conversation_audio.py).
- Configure [voice-agent tracing and monitoring](../concepts/voice-agent-observability.md). Conversation storage and sensitive-content capture in traces are separate controls.

Review [voice-agent pricing](../concepts/voice-agent-pricing.md) for the model-hosting choice, audio usage, tools, and optional features. Measure the migrated workload rather than assuming unchanged latency or cost.

## Validate and switch traffic

Test the new agent alongside the existing integration before changing production routing.

| Check | Acceptance condition |
| --- | --- |
| Business behavior | The agent follows the same business rules and handles required scenarios correctly. |
| Speech | Recognition, language, pronunciation, voice, and audio formats work on each target device. |
| Turn-taking | Pauses, interruptions, queued playback, and opening greetings behave as intended. |
| Tools and subagents | Required actions and retrieval succeed, failures are visible, and delegation preserves user intent. |
| Identity and network | Intended callers can connect and reach dependencies without broadening access. |
| History and privacy | Storage and trace-content settings match policy, and authorized users can retrieve the expected records. |
| Channels | Browser and phone integrations connect to the tested voice agent and version. |
| Performance and cost | Measured latency, reliability, and usage meet your application's acceptance criteria. |

Follow these steps in order to switch traffic:

1. Pin the tested voice-agent version and any toolbox or subagent versions your release depends on.
1. Update a test client or a limited traffic route to use the new voice endpoint.
1. Configure the required [voice-agent channels](voice-agent-channels-publish.md). Existing text-agent app publishing or phone configuration doesn't migrate merely because you create a voice agent.
1. Increase traffic only after the checks pass. Let existing calls finish on their original integration rather than changing the endpoint during a call.
1. Keep the old endpoint, agent, and client configuration available for rollback. If needed, route **new** sessions back to the original integration.
1. Retire the old path only after confirming that no applications still depend on it and that required historical records are retained.

## Troubleshoot migration issues

Use the failing stage to narrow the configuration difference.

| Symptom | What to check |
| --- | --- |
| Creation or connection rejects the agent kind | Use a new agent name with a voice definition, a supported project region, and the preview opt-in. |
| Connection works but no reply audio reaches the client | Check the configured modalities and audio format, and update legacy event handlers to the `response.output_*` names. |
| The first reply is missing or the greeting repeats | Separate the configured greeting's response from the first user response, and remove any duplicate client-side greeting trigger. |
| A migrated tool never completes | Confirm its execution model. Native functions need client implementation; MCP, toolbox, and subagent dependencies need valid configuration and permissions. |
| Stored conversation lookup returns `404` | Check the effective `store` setting, target voice agent, conversation ID, and caller access. An old text-agent conversation ID isn't the new voice conversation ID. |
| A WebRTC connection rejects the model or engine | Check the transport restrictions. Use WebSocket for self-deployed models and hosted conversation engines. |

## Related content

- [Configure a voice agent](configure-voice-agent.md).
- [Use a subagent in a voice-based agent](use-subagent-voice-first-agent.md).
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).
