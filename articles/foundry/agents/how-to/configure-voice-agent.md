---
title: "Configure a voice agent"
description: "Configure the model, instructions, greeting, audio, and tools for a voice-based agent in Microsoft Foundry."
author: sdgilley
ms.author: sgilley
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/22/2026
ms.custom: preview
ai-usage: ai-assisted
zone_pivot_groups: voice-agent-config-method
#customer intent: As a developer, I want to configure the model, voice, turn detection, and tools of a voice-based agent so that spoken conversations behave the way my scenario needs.
---

# Configure a voice agent

A voice-based agent in Microsoft Foundry Agent Service is an agent whose `kind` is `voice`. Its definition holds everything the service needs to run a spoken conversation: which model serves the session, what the agent says first, how it listens, how it sounds, and which tools it can call.

This article shows you how to set each part of that definition. Every **create** or **update** action produces a new immutable agent version, so you can change configuration and roll back without changing the agent's endpoint. You can set these values with the Azure AI Projects client library, with `azure.yaml` and the Azure Developer CLI (`azd`), or visually in the Foundry portal playground. Select a configuration method to see the steps for that surface.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md) with access to voice-based agents.
- [Foundry User role](../../concepts/rbac-foundry.md) on the project scope, or permission to create and update agents.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- A voice-based agent to configure. To create one, see [Quickstart: Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md).
- A voice model that's available to your project. Use a service-managed model such as `gpt-realtime`, or your own Foundry model deployment. This corresponds to `modelType: managed` or, where supported, `modelType: self_deployed` with a bring-your-own-model (BYOM) deployment.
- A client that supports the audio input and output formats you configure.
- A microphone to test a live conversation in the playground.

::: zone pivot="python"

Install version 2.7.0 or later of the Azure AI Projects client library as shown in [Install the packages](../quickstarts/prompt-voice-agent.md?pivots=python#install-the-packages).

Use Python 3.10 or later. Set `allow_preview=True` on `AIProjectClient` when you use `.agents` methods with voice definitions.

Sign in with `az login`. Set `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_VOICE_AGENT_NAME` as shown in the [quickstart](../quickstarts/prompt-voice-agent.md?pivots=python#set-environment-variables).

::: zone-end

::: zone pivot="javascript"

Install version 2.7.0 or later of the Azure AI Projects client library as shown in [Install the packages](../quickstarts/prompt-voice-agent.md?pivots=javascript#install-the-packages).

Use Node.js 22 or later. Configure the project as an ECMAScript module and install the packages:

```bash
npm init --yes
npm pkg set type=module
npm install @azure/ai-projects@2.7.0 @azure/identity
```

Reference: [Voice Agents JavaScript samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents).

Pass the `VoiceAgents=V1Preview` feature option when an `.agents` operation creates or modifies a voice agent.

Sign in with `az login`. Set `FOUNDRY_PROJECT_ENDPOINT` and `FOUNDRY_VOICE_AGENT_NAME` as shown in the [quickstart](../quickstarts/prompt-voice-agent.md?pivots=javascript#set-environment-variables).

::: zone-end

::: zone pivot="azure-cli"

To configure the agent with `azure.yaml`, you also need an authenticated Azure Developer CLI (`azd`) session.

::: zone-end

## Understand the voice agent definition

A voice agent definition includes these parts:

| Part | Property | Purpose |
|---|---|---|
| Model | `model_type`, `model` | Selects which model serves the session. |
| Behavior | `instructions`, `greeting`, `structured_inputs` | Tells the agent what to do and what to say first. |
| Listening | `audio.input` | Sets input format, turn detection, noise reduction, and transcription. |
| Speaking | `audio.output`, `output_modalities` | Sets the voice, locale, speed, and what the agent emits. |
| Actions | `tools`, `tool_choice`, `parallel_tool_calls` | Defines what the agent can do during a call. |
| Latency | `interim_response` | Fills silence while the agent thinks or waits on a tool. |
| Data | `store` | Controls whether conversations are persisted. |

The values in `audio` and `avatar` are session defaults. A client can override supported fields with a `session.update` event when it connects.

::: zone pivot="python"

## Choose the model

The SDK examples build a single definition. Start with this example, add the configuration snippets you need in the same script, and finish with [Save and test the agent](#save-and-test-the-agent). Run the input-audio example before the transcription and output-audio examples, which reuse its configuration objects.

Set `model_type` and `model` together. `model_type` selects how the model is served, and `model` names it:

- `managed`: the service hosts the model. Set `model` to a service-managed model name, such as `gpt-realtime-2.1`.
- `self_deployed`: the service uses your own deployment. Set `model` to the Foundry deployment name.

The service derives the architecture, real-time or cascaded, from the model you select. You don't configure it separately.

```python
from azure.ai.projects.models import VoiceAgentDefinition, VoiceModelType

definition = VoiceAgentDefinition(
    model_type=VoiceModelType.MANAGED,
    model="gpt-realtime-2.1",
    instructions=(
        "You are a friendly voice assistant. Keep replies short and natural."
    ),
)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

## Write instructions and a greeting

`instructions` is the system message inserted into the model's context. Write it for speech: short sentences, no markdown, and no lists that a caller can't hear. For detailed guidance, see [Optimize voice agent instructions](optimize-voice-agent-instructions.md).

### Configure a session-start greeting

Set `definition.greeting` to make the agent speak when a session starts, before the caller sends a turn. Choose one of two modes:

- `template`: the agent speaks the exact rendered `text`. Use this mode when the opening line must be predictable or preapproved.
- `llm_generated`: the session model authors the opening turn from a `prompt`. Its `tool_choice` defaults to `none`.

Both modes accept Handlebars placeholders that resolve against `structured_inputs`. Declare one `structured_inputs` entry for every placeholder you use. If a placeholder has no matching entry, the session fails to start.

```python
from azure.ai.projects.models import (
    StructuredInputDefinition,
    VoiceAgentTemplateGreetingConfig,
)

definition.greeting = VoiceAgentTemplateGreetingConfig(
    text=(
        "Welcome to {{company_name}}. I can help with orders and returns. "
        "What do you need today?"
    )
)
definition.structured_inputs = {
    "company_name": StructuredInputDefinition(
        description="The company name spoken in the greeting.",
        schema={"type": "string"},
        default_value="Contoso",
    )
}
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Templates render once per session, before the live session starts.

To let the session model write the opening line instead, replace the greeting with a scoped prompt:

```python
from azure.ai.projects.models import VoiceAgentLlmGeneratedGreetingConfig

definition.greeting = VoiceAgentLlmGeneratedGreetingConfig(
    prompt="Greet the caller warmly in one sentence and ask how you can help.",
    tool_choice="none",
)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Set `definition.greeting` to `None` if the agent should wait for the caller instead. After changing the greeting, [save and test a new agent version](#save-and-test-the-agent).

The greeting streams through the normal response events; don't send a user message or `response.create` to trigger it. Receive the greeting's response before sending the first user turn, as shown in the [quickstart](../quickstarts/prompt-voice-agent.md?pivots=python#talk-to-the-agent).

## Configure input audio

`audio.input` controls how the agent listens.

### Set turn detection

Turn detection decides when the caller stops speaking. Server-side turn detection is on by default. Set `turn_detection` to `None` to disable it, in which case your client must trigger each response.

| Type | Use it when |
|---|---|
| `server_vad` | You want straightforward silence-based detection. This type suits most business scenarios. |
| `semantic_vad` | You want the OpenAI semantic end-of-turn model. |
| `azure_semantic_vad` | You want Azure semantic detection with an explicit `languages` list. |
| `azure_semantic_vad_en` | Your callers speak English only. |
| `azure_semantic_vad_multilingual` | Your callers switch languages within a call. |

The Azure semantic types share these options:

| Option | Effect |
|---|---|
| `threshold` | Activation sensitivity, from 0 to 1. Raise it in noisy environments. |
| `prefix_padding_ms` | Audio kept before detected speech. |
| `silence_duration_ms` | Silence required before the turn ends. Increase it when callers pause often. |
| `idle_timeout_ms` | Maximum idle time before the detector ends the turn. |
| `speech_duration_ms` | Minimum speech needed to trigger detection. |
| `remove_filler_words` | Drops filler words from transcription. Defaults to `False`. |
| `create_response` | Creates a response automatically when speech stops. Defaults to `True`. |
| `interrupt_response` | Lets caller speech interrupt the agent. Defaults to `True`. |
| `end_of_utterance_detection` | Adds a semantic end-of-utterance model. Set to `None` to disable. |

Set `auto_truncate` to `True` to truncate the input audio buffer automatically when speech stops.

```python
from azure.ai.projects.models import (
    RealtimeAudioFormatsAudioPcm,
    VoiceAgentAudioConfig,
    VoiceAgentAudioInputConfig,
    VoiceAgentServerVadTurnDetection,
)

input_audio = VoiceAgentAudioInputConfig(
    format=RealtimeAudioFormatsAudioPcm(rate=24000),
    turn_detection=VoiceAgentServerVadTurnDetection(
        threshold=0.5,
        prefix_padding_ms=300,
        silence_duration_ms=500,
    ),
)
audio_config = VoiceAgentAudioConfig(input=input_audio)
definition.audio = audio_config
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

### Reduce noise and echo

Set `noise_reduction.type` to `near_field` for headsets and handsets, `far_field` for speakerphones and rooms, or `azure_deep_noise_suppression` for noisy environments such as contact centers. Set `noise_reduction` to `None` to disable it.

Set `echo_cancellation` when the agent's own output can be picked up by the caller's microphone. `reference_source` defaults to `server`. Use `client` with two interleaved input channels when your client supplies the reference signal.

### Transcribe caller speech

`transcription` runs asynchronous transcription of input audio. Set it to `None` to disable transcription.

Set `model` to a transcription model name, such as `azure-speech`, `whisper-1`, `gpt-4o-transcribe`, or `gpt-4o-mini-transcribe`. This value is a model name, not a Foundry deployment name.

Two Foundry extensions help with domain vocabulary:

- `phrase_list`: phrase hints that bias recognition toward domain terms, such as product names.
- `custom_speech`: your custom speech deployments, keyed by locale.

```python
from azure.ai.projects.models import (
    VoiceAgentInputTranscription,
    VoiceAgentInputTranscriptionModel,
)

input_audio.transcription = VoiceAgentInputTranscription(
    model=VoiceAgentInputTranscriptionModel.AZURE_SPEECH,
    phrase_list=["Contoso Aurora", "SKU 4471"],
)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

## Configure output audio

The `audio.output` setting controls how the agent sounds. The `voice_type` setting selects the voice implementation, and it determines which other fields apply:

| `voice_type` | Applicable fields |
|---|---|
| `openai` | `voice`, `speed` |
| `azure-standard` | `voice`, `voice_locale`, `speed`, `voice_temperature`, `custom_lexicon_url`, `custom_text_normalization_url`, `prefer_locales`, `style`, `pitch`, `volume` |
| `azure-custom` | The `azure-standard` fields except `style`, plus `custom_voice_endpoint_id` |
| `azure-personal` | The `azure-standard` fields except `style`, plus `personal_voice_model` |
| `avatar-voice-sync` | The `azure-standard` fields except `voice` and `style`, plus `personal_voice_model`. The voice name comes from the avatar. |
| `azure-realtime-native` | `voice`, `speed` |

The `format` and `output_audio_timestamp_types` settings apply to every voice type. Output defaults to 24-kHz PCM. The `speed` setting accepts values from 0.25 through 1.5 and defaults to 1. Set `output_audio_timestamp_types` to `["word"]` when your client needs word-level timing, for example to highlight text as the agent speaks.

```python
from azure.ai.projects.models import VoiceAgentAudioOutputConfig, VoiceType

audio_config.output = VoiceAgentAudioOutputConfig(
    voice="en-US-AvaNeural",
    voice_type=VoiceType.AZURE_STANDARD,
    speed=1.0,
)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

The `output_modalities` setting defaults to `["audio"]`. Add `text` when your client also renders the transcript. Use `animation` and `avatar` only when you configure an avatar.

## Attach tools

The `tools` list defines what the agent can do during a call. The service supports four kinds of tools:

| Kind | Executed by | Notes |
|---|---|---|
| `function` | Your client | The service forwards the call over the live session, and your app returns the result. |
| `mcp` | The service | Points at a remote MCP server. |
| `toolbox` | The service | References a versioned Foundry toolbox by `toolbox_name` and `toolbox_version`. |
| `system` | The service | Session controls that need no code or external credentials. `end_conversation` lets the agent end the call. |

Attach server-side tools such as web search, Azure AI Search, and OpenAPI tools through a toolbox rather than declaring them directly. See [Create and manage a toolbox in Foundry](tools/toolbox.md).

For `mcp` and `toolbox` tools, `response_scheduling` decides when the result turns into speech:

| Value | Behavior |
|---|---|
| `when_idle` | Responds when the conversation is idle. This value is the default. |
| `interrupt` | Interrupts the active response. |
| `skip_if_busy` | Responds only when no response is active. |
| `silent` | Doesn't create a follow-up response. |

`tool_choice` defaults to `auto`. Set it to `none` to block tool calls, `required` to force at least one, or name a specific function or MCP tool.

```python
from azure.ai.projects.models import (
    RealtimeFunctionToolParameters,
    VoiceAgentEndConversationSystemTool,
    VoiceAgentFunctionTool,
)

get_order_status = VoiceAgentFunctionTool(
    name="get_order_status",
    description="Look up the status of a customer order.",
    parameters=RealtimeFunctionToolParameters(
        {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order number.",
                }
            },
            "required": ["order_id"],
        }
    ),
)

definition.tools = [
    get_order_status,
    VoiceAgentEndConversationSystemTool(),
]
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

This example registers the function schema. Your realtime client must implement `get_order_status` and return its result when the agent calls it.

## Cover tool latency with interim responses

Silence during a tool call sounds like a dropped call. By using `interim_response`, the agent can speak while it waits.

Set `triggers` to `latency`, `tool`, or both. The default value for `latency_threshold_ms` is 2,000 milliseconds. Choose one of two modes:

- `static_interim_response`: the service picks from your `texts` list. This mode adds no model latency.
- `llm_interim_response`: a model authors the filler from `instructions`. The default value for `max_completion_tokens` is 50.

```python
from datetime import timedelta

from azure.ai.projects.models import VoiceAgentStaticInterimResponseConfig

definition.interim_response = VoiceAgentStaticInterimResponseConfig(
    triggers=["latency", "tool"],
    texts=["Let me check that for you.", "One moment while I look that up."],
    latency_threshold_ms=timedelta(milliseconds=1500),
)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

In Python, `latency_threshold_ms` takes a `datetime.timedelta`. The SDK serializes it as milliseconds.

## Persist conversations

The default value for `store` is `False`, so nothing is persisted. Set it to `True` to persist the conversation, which includes the transcript, the event timeline, and raw audio. There's no separate audio-logging switch: audio is persisted only as part of `store`.

A client can override `store` for a single session by using the `store` query parameter in the connect request. For information about what you can read back afterward, see [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Limit response length

Set `max_output_tokens` to a token count to cap each response, or to `inf` for no cap. Capping output is an effective way to keep spoken replies short.

Use `include` to add optional fields to service output, such as `item.input_audio_transcription.logprobs` or `item.input_audio_transcription.phrases`.

## Save and test the agent

After applying your selected configuration snippets, create a version for the agent named in `FOUNDRY_VOICE_AGENT_NAME`. The following code uses your project endpoint and credentials, with `allow_preview=True`:

```python
import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    created = project_client.agents.create_version(
        agent_name=agent_name, definition=definition
    )
    print(f"Created voice agent '{agent_name}', version {created.version}")
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

The agent endpoint is live as soon as the version exists. Connect to it over the voice protocol WebSocket route:

```text
wss://{project-endpoint}/agents/{agent-name}/endpoint/protocols/voice?api-version=v1
```

Authenticate the upgrade with a Microsoft Entra bearer token. To test a version that isn't the active one, pass the version override on the connect request instead of changing the active version.

For an end-to-end walkthrough, see [Quickstart: Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md).

::: zone-end

::: zone pivot="javascript"

## Choose the model

The SDK examples build a single definition. Start with this example, add the configuration snippets you need in the same script, and finish with [Save and test the agent](#save-and-test-the-agent). Run the input-audio example before the transcription and output-audio examples, which reuse its configuration objects.

Set `model_type` and `model` together. `model_type` selects how the model is served, and `model` names it:

- `managed`: the service hosts the model. Set `model` to a service-managed model name, such as `gpt-realtime-2.1`.
- `self_deployed`: the service uses your own deployment. Set `model` to the Foundry deployment name.

The service derives the architecture, real-time or cascaded, from the model you select. You don't configure it separately.

```javascript
/** @type {import("@azure/ai-projects").VoiceAgentDefinition} */
const definition = {
    kind: "voice",
    model_type: "managed",
    model: "gpt-realtime-2.1",
    instructions: "You are a friendly voice assistant. " +
        "Keep replies short and natural.",
};
```

Reference: [Configure a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/configure-voice-agent).

## Write instructions and a greeting

`instructions` is the system message inserted into the model's context. Write it for speech: short sentences, no markdown, and no lists that a caller can't hear. For detailed guidance, see [Optimize voice agent instructions](optimize-voice-agent-instructions.md).

### Configure a session-start greeting

Set `definition.greeting` to make the agent speak when a session starts, before the caller sends a turn. Choose one of two modes:

- `template`: the agent speaks the exact rendered `text`. Use this mode when the opening line must be predictable or preapproved.
- `llm_generated`: the session model authors the opening turn from a `prompt`. Its `tool_choice` defaults to `none`.

Both modes accept Handlebars placeholders that resolve against `structured_inputs`. Declare one `structured_inputs` entry for every placeholder you use. If a placeholder has no matching entry, the session fails to start.

```javascript
definition.greeting = {
    type: "template",
    text: "Welcome to {{company_name}}. I can help with orders and " +
        "returns. What do you need today?",
};
definition.structured_inputs = {
    company_name: {
        description: "The company name spoken in the greeting.",
        schema: { type: "string" },
        default_value: "Contoso",
    },
};
```

Reference: [Manage a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/manage-voice-agent).

Templates render once per session, before the live session starts.

To let the session model write the opening line instead, replace the greeting with a scoped prompt:

```javascript
definition.greeting = {
    type: "llm_generated",
    prompt: "Greet the caller warmly in one sentence and ask how you can help.",
    tool_choice: "none",
};
```

Reference: [Azure AI Projects client library for JavaScript](https://aka.ms/azsdk/azure-ai-projects-v2/javascript/code).

Set `definition.greeting` to `undefined` if the agent should wait for the caller instead. After changing the greeting, [save and test a new agent version](#save-and-test-the-agent).

The greeting streams through the normal response events; don't send a user message or `response.create` to trigger it. Receive the greeting's response before sending the first user turn, as shown in the [quickstart](../quickstarts/prompt-voice-agent.md?pivots=javascript#talk-to-the-agent).

## Configure input audio

`audio.input` controls how the agent listens.

### Set turn detection

Turn detection decides when the caller stops speaking. Server-side turn detection is on by default. Set `turn_detection` to `undefined` to disable it, in which case your client must trigger each response.

| Type | Use it when |
|---|---|
| `server_vad` | You want straightforward silence-based detection. This type suits most business scenarios. |
| `semantic_vad` | You want the OpenAI semantic end-of-turn model. |
| `azure_semantic_vad` | You want Azure semantic detection with an explicit `languages` list. |
| `azure_semantic_vad_en` | Your callers speak English only. |
| `azure_semantic_vad_multilingual` | Your callers switch languages within a call. |

The Azure semantic types share these options:

| Option | Effect |
|---|---|
| `threshold` | Activation sensitivity, from 0 to 1. Raise it in noisy environments. |
| `prefix_padding_ms` | Audio kept before detected speech. |
| `silence_duration_ms` | Silence required before the turn ends. Increase it when callers pause often. |
| `idle_timeout_ms` | Maximum idle time before the detector ends the turn. |
| `speech_duration_ms` | Minimum speech needed to trigger detection. |
| `remove_filler_words` | Drops filler words from transcription. Defaults to `false`. |
| `create_response` | Creates a response automatically when speech stops. Defaults to `true`. |
| `interrupt_response` | Lets caller speech interrupt the agent. Defaults to `true`. |
| `end_of_utterance_detection` | Adds a semantic end-of-utterance model. Set to `undefined` to disable. |

Set `auto_truncate` to `true` to truncate the input audio buffer automatically when speech stops.

```javascript
/** @type {import("@azure/ai-projects").VoiceAgentAudioInputConfig} */
const inputAudio = {
    format: { type: "audio/pcm", rate: 24000 },
    turn_detection: {
        type: "server_vad",
        threshold: 0.5,
        prefix_padding_ms: 300,
        silence_duration_ms: 500,
    },
};
/** @type {import("@azure/ai-projects").VoiceAgentAudioConfig} */
const audioConfig = { input: inputAudio };
definition.audio = audioConfig;
```

Reference: [Realtime audio JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/realtime-audio).

### Reduce noise and echo

Set `noise_reduction.type` to `near_field` for headsets and handsets, `far_field` for speakerphones and rooms, or `azure_deep_noise_suppression` for noisy environments such as contact centers. Set `noise_reduction` to `undefined` to disable it.

Set `echo_cancellation` when the agent's own output can be picked up by the caller's microphone. `reference_source` defaults to `server`. Use `client` with two interleaved input channels when your client supplies the reference signal.

### Transcribe caller speech

`transcription` runs asynchronous transcription of input audio. Set it to `undefined` to disable transcription.

Set `model` to a transcription model name, such as `azure-speech`, `whisper-1`, `gpt-4o-transcribe`, or `gpt-4o-mini-transcribe`. This value is a model name, not a Foundry deployment name.

Two Foundry extensions help with domain vocabulary:

- `phrase_list`: phrase hints that bias recognition toward domain terms, such as product names.
- `custom_speech`: your custom speech deployments, keyed by locale.

```javascript
inputAudio.transcription = {
    model: "azure-speech",
    phrase_list: ["Contoso Aurora", "SKU 4471"],
};
```

Reference: [Azure AI Projects client library for JavaScript](https://aka.ms/azsdk/azure-ai-projects-v2/javascript/code).

## Configure output audio

The `audio.output` setting controls how the agent sounds. The `voice_type` setting selects the voice implementation, and it determines which other fields apply:

| `voice_type` | Applicable fields |
|---|---|
| `openai` | `voice`, `speed` |
| `azure-standard` | `voice`, `voice_locale`, `speed`, `voice_temperature`, `custom_lexicon_url`, `custom_text_normalization_url`, `prefer_locales`, `style`, `pitch`, `volume` |
| `azure-custom` | The `azure-standard` fields except `style`, plus `custom_voice_endpoint_id` |
| `azure-personal` | The `azure-standard` fields except `style`, plus `personal_voice_model` |
| `avatar-voice-sync` | The `azure-standard` fields except `voice` and `style`, plus `personal_voice_model`. The voice name comes from the avatar. |
| `azure-realtime-native` | `voice`, `speed` |

The `format` and `output_audio_timestamp_types` settings apply to every voice type. Output defaults to 24-kHz PCM. The `speed` setting accepts values from 0.25 through 1.5 and defaults to 1. Set `output_audio_timestamp_types` to `["word"]` when your client needs word-level timing, for example to highlight text as the agent speaks.

```javascript
audioConfig.output = {
    voice: "en-US-AvaNeural",
    voice_type: "azure-standard",
    speed: 1.0,
};
```

Reference: [Configure a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/configure-voice-agent).

The `output_modalities` setting defaults to `["audio"]`. Add `text` when your client also renders the transcript. Use `animation` and `avatar` only when you configure an avatar.

## Attach tools

The `tools` list defines what the agent can do during a call. The service supports four kinds of tools:

| Kind | Executed by | Notes |
|---|---|---|
| `function` | Your client | The service forwards the call over the live session, and your app returns the result. |
| `mcp` | The service | Points at a remote MCP server. |
| `toolbox` | The service | References a versioned Foundry toolbox by `toolbox_name` and `toolbox_version`. |
| `system` | The service | Session controls that need no code or external credentials. `end_conversation` lets the agent end the call. |

Attach server-side tools such as web search, Azure AI Search, and OpenAPI tools through a toolbox rather than declaring them directly. See [Create and manage a toolbox in Foundry](tools/toolbox.md).

For `mcp` and `toolbox` tools, `response_scheduling` decides when the result turns into speech:

| Value | Behavior |
|---|---|
| `when_idle` | Responds when the conversation is idle. This value is the default. |
| `interrupt` | Interrupts the active response. |
| `skip_if_busy` | Responds only when no response is active. |
| `silent` | Doesn't create a follow-up response. |

`tool_choice` defaults to `auto`. Set it to `none` to block tool calls, `required` to force at least one, or name a specific function or MCP tool.

```javascript
const getOrderStatus = {
    type: "function",
    name: "get_order_status",
    description: "Look up the status of a customer order.",
    parameters: {
        type: "object",
        properties: {
            order_id: {
                type: "string",
                description: "The order number.",
            },
        },
        required: ["order_id"],
    },
};

definition.tools = [
    getOrderStatus,
    { type: "system", name: "end_conversation" },
];
```

Reference: [Realtime text and tools JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/realtime-text-and-tools).

This example registers the function schema. Your realtime client must implement `get_order_status` and return its result when the agent calls it.

## Cover tool latency with interim responses

Silence during a tool call sounds like a dropped call. By using `interim_response`, the agent can speak while it waits.

Set `triggers` to `latency`, `tool`, or both. The default value for `latency_threshold_ms` is 2,000 milliseconds. Choose one of two modes:

- `static_interim_response`: the service picks from your `texts` list. This mode adds no model latency.
- `llm_interim_response`: a model authors the filler from `instructions`. The default value for `max_completion_tokens` is 50.

```javascript
definition.interim_response = {
    type: "static_interim_response",
    triggers: ["latency", "tool"],
    texts: [
        "Let me check that for you.",
        "One moment while I look that up.",
    ],
    latency_threshold_ms: 1500,
};
```

Reference: [Azure AI Projects client library for JavaScript](https://aka.ms/azsdk/azure-ai-projects-v2/javascript/code).

In JavaScript, `latency_threshold_ms` takes a numeric value in milliseconds.

## Persist conversations

The default value for `store` is `false`, so nothing is persisted. Set it to `true` to persist the conversation, which includes the transcript, the event timeline, and raw audio. There's no separate audio-logging switch: audio is persisted only as part of `store`.

A client can override `store` for a single session by using the `store` query parameter in the connect request. For information about what you can read back afterward, see [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Limit response length

Set `max_output_tokens` to a token count to cap each response, or to `inf` for no cap. Capping output is an effective way to keep spoken replies short.

Use `include` to add optional fields to service output, such as `item.input_audio_transcription.logprobs` or `item.input_audio_transcription.phrases`.

## Save and test the agent

After applying your selected configuration snippets, create a version for the agent named in `FOUNDRY_VOICE_AGENT_NAME`. The following code uses your project endpoint and credentials, with the `VoiceAgents=V1Preview` feature option enabled:

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = process.env.FOUNDRY_PROJECT_ENDPOINT;
const agentName = process.env.FOUNDRY_VOICE_AGENT_NAME;
if (!projectEndpoint || !agentName) {
    throw new Error(
        "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_VOICE_AGENT_NAME.",
    );
}

const project = new AIProjectClient(
    projectEndpoint,
    new DefaultAzureCredential(),
);
const created = await project.agents.createVersion(
    agentName,
    definition,
    {
        requestOptions: {
            headers: { "foundry-features": "VoiceAgents=V1Preview" },
        },
    },
);
console.log(`Created voice agent '${agentName}', version ${created.version}`);
```

Reference: [Configure a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/configure-voice-agent).

The agent endpoint is live as soon as the version exists. Connect to it over the voice protocol WebSocket route:

```text
wss://{project-endpoint}/agents/{agent-name}/endpoint/protocols/voice?api-version=v1
```

Authenticate the upgrade with a Microsoft Entra bearer token. To test a version that isn't the active one, pass the version override on the connect request instead of changing the active version.

For an end-to-end walkthrough, see [Quickstart: Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md).

::: zone-end

::: zone pivot="azure-cli"

## Configure with azure.yaml and the Azure Developer CLI

Advanced settings are optional for a prompt voice agent. Use them when you need to control the agent's instructions, audio formats, turn detection, transcription, voice, greeting, or tool behavior. Configure these settings in the agent service in `azure.yaml`, and then deploy a new agent version with the Azure Developer CLI (`azd`).

For an existing voice service, edit `azure.yaml` rather than running initialization again to change the voice. The `--voice` initialization option is limited to creating a new prompt voice agent. Other initialization flows reject it.

### Choose a managed or self-deployed model

Set `modelType` and `model.id` together on the voice agent service. The service accepts both `kind: voice` and the compatibility alias `kind: prompt-voice`.

| Model type | `model.id` value | Deployment requirement |
| --- | --- | --- |
| `managed` | A service-managed model name, such as `gpt-realtime`. | No separate model deployment is needed. |
| `self_deployed` | The name of a compatible model deployment in your Foundry resource. | The deployment must exist before you deploy the voice agent. |

For a managed model, use:

```yaml
modelType: managed
model:
  id: gpt-realtime
```

For bring-your-own-model (BYOM), replace these fields with:

```yaml
modelType: self_deployed
model:
  id: <existing-model-deployment-name>
```

Replace `<existing-model-deployment-name>` with the deployment name, which can differ from the model name. BYOM can use a compatible realtime or cascaded text model deployment. Confirm model availability and compatibility for your project.

New prompt voice initialization rejects `--model-deployment`. Configure BYOM through `modelType` and `model.id` in `azure.yaml` instead.

Changing `modelType` and `model.id` doesn't create the BYOM deployment. Create or confirm it in the Foundry resource before running `azd deploy`. For model deployment steps, see [Deploy models](../../how-to/deploy-models-managed.md).

Keep the existing audio and advanced settings compatible with the selected model. For a voice wrapper that delegates conversation logic to a hosted agent, use `conversationEngine` instead of these model fields. See [Deploy a hosted voice agent with azd](deploy-hosted-voice-agent.md).

### Add the advanced settings

Add the following properties to the prompt voice agent service in `azure.yaml`. Place them at the same indentation level as `kind`, `model`, `modelType`, and `name`.

```yaml
instructions: You are {{persona}}, a concise voice assistant.
structuredInputs:
  persona:
    description: Assistant persona
    defaultValue: Ada
    schema:
      type: string
audio:
  input:
    format:
      type: audio/pcm
      rate: 24000
    noiseReduction:
      type: near_field
    turnDetection:
      type: azure_semantic_vad
      threshold: 0.6
      speechDurationMs: 120
      removeFillerWords: true
      createResponse: true
      interruptResponse: true
      languages: [en-US]
      autoTruncate: true
    transcription:
      model: azure-speech
      language: en-US
  output:
    format:
      type: audio/pcm
      rate: 24000
    voice:
      type: azure_standard
      name: en-US-AvaNeural
      locale: en-US
      style: cheerful
    speed: 1
outputModalities: [audio, text]
tools:
  - type: system
    name: end_conversation
greeting:
  type: template
  text: Hello {{persona}}
toolChoice: auto
maxOutputTokens: "inf"
include:
  - item.input_audio_transcription.phrases
```

> [!IMPORTANT]
> Prompt voice agents currently don't support `parallelToolCalls`. Don't add
> this property to the agent definition.

The following example configures these behaviors:

| Setting | Behavior |
| --- | --- |
| `instructions` and `structuredInputs` | Define a reusable `persona` input with the default value `Ada`. The instructions and greeting reference it as `{{persona}}`. |
| `audio.input.format` | Accept 24-kHz pulse-code modulation (PCM) audio, which works with browser microphone clients that send this format. |
| `audio.input.noiseReduction` | Optimize input processing for a near-field microphone. |
| `audio.input.turnDetection` | Use Azure semantic voice activity detection (VAD), automatically respond when a turn ends, and let user speech interrupt an in-progress response. |
| `audio.input.transcription` | Transcribe `en-US` input with Azure Speech in Foundry Tools. |
| `audio.output` | Return 24-kHz PCM audio with the `en-US-AvaNeural` voice and the `cheerful` style. |
| `outputModalities` | Return both audio and text. |
| `tools` and `toolChoice` | Make the `end_conversation` system tool available and let the service choose when to call it. |
| `greeting` | Start the session with a templated greeting that uses the `persona` input. |
| `maxOutputTokens` | Set the response output token limit to a positive `int32` value, or use the exact string `"inf"`. |
| `include` | Include input-audio transcription phrases in service responses. The `item.input_audio_transcription.phrases` value requires the `azure-speech` or `azure-fast-transcription` transcription model. |

The audio format must match the format that your client sends and receives. Support for advanced settings and combinations can vary by model.

For more information about audio formats and turn detection, see [How to use the Voice Live API](/azure/ai-services/speech-service/voice-live-how-to).

### Add a telephony binding

A prompt voice service can declare Foundry-side phone bindings in `azure.yaml`. Before adding a binding, configure the phone provider account or resource, the phone number, and a Foundry project connection for that provider. Configure provider-side delivery, such as a Twilio webhook or an Azure Communication Services Event Grid subscription, separately.

Add `telephony` at the same indentation level as `kind`, `model`, and `name`:

```yaml
telephony:
  bindings:
    - provider: twilio
      identifier: "+14255550123"
      connection: telephony-twilio
```

Replace the example number with your own Twilio number in E.164 format, and replace `telephony-twilio` with your existing Foundry project connection name. These fields are `azd` configuration fields, not a REST request body.

The `acs` provider is also supported, with different identifier formats. See the [telephony configuration reference](../concepts/azure-yaml-reference.md#telephony-bindings) for the provider values and required fields.

The agent deployment creates a missing binding or accepts an existing matching binding. Bindings are create-only in this preview: if the existing configuration differs, deployment fails with remediation guidance rather than updating it.

After deployment, make a controlled inbound test call and confirm two-way audio. A deployed binding alone doesn't establish that provider routing and audio work. Delete test bindings before deleting their agents; removing a binding from `azure.yaml` isn't a remote deletion. For conditional cleanup, follow [Remove a telephony binding](#remove-a-telephony-binding).

### Deploy the updated agent

Deploy the agent service after you save `azure.yaml`:

```azurecli
azd deploy voice-guide-managed
```

Before deployment, `azd` validates the agent definition locally. The service then performs final validation of the advanced setting values and combinations. If either validation fails, the command returns a validation error. Update the affected setting, and deploy again.

### Test the advanced settings

Use the Foundry playground to test the voice, greeting, interruption, and transcription behavior.

1. Open the [Foundry portal](https://ai.azure.com) and sign in.
1. Select the Foundry project that contains your agent.
1. In the left navigation, select **Build** > **Agents**.
1. Select **voice-guide-managed**, and then select **Open in playground**.
1. Start a voice session, and confirm that the agent uses the configured greeting and voice.
1. Speak while the agent responds, and confirm that the agent stops speaking and listens to the new input.
1. Review the transcript, and confirm that the session includes both text and audio responses.

### Remove a telephony binding

This PowerShell example removes the Twilio binding configured in this section. It uses azd's telephony route, `/agents/{agentName}/telephony/{bindingId}`, with `api-version=2025-11-15-preview`. Don't substitute the `/telephony/bindings` routes or `api-version=v1` from the separate Teams Phone REST examples.

Install the [Azure CLI](/cli/azure/install-azure-cli) and sign in with `az login` to the project's Microsoft Entra tenant. Replace `<project-endpoint>`, `<agent-name>`, and the example phone number with the values for your binding. Read the binding and review the returned provider, identifier, and connection before deleting it:

```powershell
$projectEndpoint = "<project-endpoint>"
$agentName = "<agent-name>"
$phoneNumber = "+14255550123"
$bindingId = "twilio:" + [uri]::EscapeDataString($phoneNumber)
$uri = $projectEndpoint.TrimEnd("/") + "/agents/" +
    [uri]::EscapeDataString($agentName) + "/telephony/" +
    $bindingId + "?api-version=2025-11-15-preview"

$token = az account get-access-token `
    --scope https://ai.azure.com/.default --query accessToken -o tsv
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($token)) {
    throw "No access token returned. Sign in to Azure CLI and try again."
}
$headers = @{
    Authorization = "Bearer $token"
    "Foundry-Features" = "VoiceAgents=V1Preview"
}
$response = Invoke-WebRequest -Method Get -Uri $uri -Headers $headers `
    -ErrorAction Stop
$binding = $response.Content | ConvertFrom-Json -ErrorAction Stop
$binding
```

After confirming that this is the intended binding, continue in the same PowerShell session. Read the `ETag` from the HTTP response headers, with a fallback to the JSON body's `etag` property. Preserve the returned value, including its quotes, and send it in `If-Match`:

```powershell
$etag = [string]($response.Headers["ETag"] | Select-Object -First 1)
if ([string]::IsNullOrWhiteSpace($etag)) {
    $etag = [string]$binding.etag
}
if ([string]::IsNullOrWhiteSpace($etag)) {
    throw "No ETag returned. Stop without deleting the binding."
}
$headers["If-Match"] = $etag
Invoke-WebRequest -Method Delete -Uri $uri -Headers $headers `
    -ErrorAction Stop | Out-Null
```

If deletion returns `412 Precondition Failed`, read and review the binding again before retrying with its current ETag. Don't use `If-Match: *` to bypass the check. After deletion succeeds, remove the binding from `azure.yaml` to prevent a later deployment from recreating it. Then delete the test agent if you no longer need it.

::: zone-end

::: zone pivot="foundry-portal"

## Configure in the agent playground

After you create a voice-based agent, Foundry opens the agent playground. Use this page to configure how the agent reasons, listens, speaks, calls tools, and appears in a visual session.

### Get familiar with the agent playground

The agent page includes these tabs:

- **Playground**: Configure and test the agent.
- **Details**: Review agent details and saved version information.
- **Traces**: Inspect recorded agent conversations and operations.
- **Monitor**: Review usage, latency, duration, and conversation metrics.
- **Evaluation**: Evaluate saved voice conversations.
- **Channels**: Publish or connect the agent to a supported experience.

The playground contains a configuration panel on the left and a test surface on the right.

| Playground control | What it does |
| --- | --- |
| Version selector | Opens a saved version of the agent. |
| **Save** | Saves the current configuration as the latest agent version. |
| **Publish** | Opens the publishing flow for a saved agent. |
| **Instructions** | Defines the agent's role, goals, speaking behavior, limits, and escalation rules. |
| **Optimize** | Helps refine the instructions for the intended scenario. |
| **AI model** | Selects the model that reasons over the conversation and creates responses. |
| **Voice** | Selects and previews the voice that users hear. |
| **Advanced settings** | Configures transcription, incoming audio, turn detection, and conversational behavior. |
| **Tools** | Adds one or more individual MCP tools or attaches one toolbox. |
| **Avatar** | Adds a visual speaker to supported browser experiences. |
| **Chat** | Starts an interactive test conversation in the browser. |
| **YAML** | Displays the agent configuration in YAML. |
| **Call agent** | Provides code and endpoint guidance for calling the saved agent. |
| **Metrics** | Opens live measurements for the current test session. |
| Microphone menu | Selects the browser audio-input device. |
| Avatar video control | Shows or hides the visual avatar during a supported session. |
| **Start** | Starts the voice session with the latest saved settings. |

> [!IMPORTANT]
> Voice sessions use the latest saved agent settings. Select **Save** before selecting **Start**. Configuration controls are disabled while a session is active, so stop the session before making another change.

<!-- Screenshot: Voice-based agent playground showing the left configuration panel, Chat, YAML, Call agent, Metrics, microphone menu, avatar video control, and Start. -->

### Review and optimize the instructions

If you select **Optimize instructions for your use case** during agent creation, the portal generates use-case instructions as the starting preset in the playground.

Review the preset before testing. Instructions for a spoken experience should tell the agent to:

- Use short sentences and ask one question at a time.
- Confirm important names, numbers, dates, and actions.
- Avoid reading long URLs, tables, or code aloud.
- Explain when it's checking information or performing an action.
- Ask for clarification instead of guessing when speech is unclear.
- Explain escalation, transfer, and failure behavior in plain language.

Select **Optimize** to refine the instructions further. Optimization gives you a starting point; it doesn't replace testing with realistic users and audio.

### Choose an AI model

Open **AI model**. Foundry groups the available models into **Native speech-to-speech models** and **Native text models**.

<!-- Screenshot: AI model menu grouped into Native speech-to-speech models and Native text models. -->

#### Native speech-to-speech models

These models process speech input and generate speech output directly. They're designed for responsive, natural spoken interaction.

Current portal options include:

| Model | Approximate latency | Tier |
| --- | ---: | --- |
| `gpt-realtime-2.1` | 800 ms | Pro |
| `azure-realtime` | 500 ms | Pro |
| `gpt-realtime-1.5` | 700 ms | Pro |
| `gpt-realtime-2.1-mini` | 1,100 ms | Standard |
| `gpt-realtime-mini` | 400 ms | Standard |

#### Native text models

These models use a composed speech pipeline:

1. A transcription model converts your speech to text.
1. The selected text model reviews the transcript and generates text.
1. Speech synthesis converts the response to the selected voice.

This separation provides more direct control over transcription and synthesized voice settings.

Current portal options include:

| Model | Approximate latency | Tier |
| --- | ---: | --- |
| `gpt-5.4` | 1,500 ms | Pro |
| `gpt-5.3-chat` | Not shown | Pro |
| `gpt-5-mini` | 1,400 ms | Standard |
| `gpt-5-nano` | Not shown | Lite |

> [!NOTE]
> Model availability and metadata are loaded for your Foundry resource and can change by region and release stage. The portal is the source of truth.

#### Understand the model indicators

Each model row can display:

- **Preview**, when the model is offered as a preview capability.
- An approximate model latency, such as `~500 ms` or `~1.5 s`.
- A **Pro**, **Standard**, or **Lite** tier.

Latency in the menu is a comparison aid, not a guaranteed end-to-end response time. Transcription, speech synthesis, tool calls, network conditions, and avatar rendering can add time.

#### Understand what changes with the model

Changing the model can change:

- Which voices are compatible.
- Whether a separate **User transcript model** appears.
- Which advanced speech and conversation settings are available.
- Whether interim responses are available.
- Whether the model supports tools.

If the selected voice isn't compatible with the new model, Foundry selects a compatible default. Review **Voice** and **Advanced settings** after every model change.

### Choose and tune the voice

In **Voice**, preview and select the voice that users hear. Depending on the model and resource, **Browse all voices** can include:

- **Realtime native** voices.
- **Azure standard** voices.
- Eligible **Azure custom** voices.

Use the language and capability filters to narrow the list. Choose a voice that's clear over the intended channel and correctly pronounces important names and terms.

Select the advanced options icon next to **Voice** to configure supported output controls.

| Setting | What it changes | Guidance |
| --- | --- | --- |
| **Voice temperature** | Controls output variation for supported Neural HD voices from 0 through 1. | Use lower values for predictable transactional speech and higher values for more variation. |
| **Playback speed** | Controls speaking rate from 0.5 through 1.5. | Test comprehension with realistic users and telephone-quality audio. |
| **Custom lexicon** | Uses a lexicon URL to define pronunciation. | Add brand names, medical terms, abbreviations, and other commonly mispronounced words. |

Changing the voice resets advanced voice options to defaults supported by the new voice. Voice temperature appears only for supported Neural HD voices.

For lexicon authoring guidance, see [Improve synthesis with the Speech Synthesis Markup Language](/azure/ai-services/speech-service/speech-synthesis-markup).

### Configure every advanced setting

Select **Advanced settings**. The drawer organizes the controls into **Input**, **Automatic turn detection**, and, when supported, **Conversational behavior**.

<!-- Screenshot: Advanced settings drawer showing Input, Automatic turn detection, and Conversational behavior. -->

Select **Select** in the drawer to apply the settings to the agent draft. Then select the main **Save** action to persist the agent version. **Reset** restores the drawer defaults.

#### Input settings

##### User transcript model

For supported native speech-to-speech models, this setting selects the model that creates the readable transcript of what the user says. Options depend on the selected real-time model and can include:

- **Azure Speech**
- **Whisper**
- **GPT-4o Transcribe**
- **GPT-4o Mini Transcribe**
- **GPT-4o Transcribe Diarize**

The transcript model creates the conversation transcript. It doesn't replace the speech-to-speech model's direct audio processing.

##### Language

Select **Auto-detect** when you don't know the spoken language before the session. Otherwise, select up to 10 expected languages. A short, accurate list reduces the set of languages the recognizer must distinguish.

Test accents and code-switching that are common for your users.

##### Phrase list

Turn on **Phrase list**, and enter values separated by commas or semicolons. Use it to improve recognition of:

- Product and organization names.
- People and locations.
- Industry terminology.
- Alphanumeric identifiers.

Phrase lists aren't supported by every real-time model combination. The portal hides or ignores controls that the selected model doesn't support.

##### Audio enhancement

**Audio enhancement** is on by default. It reduces background noise and improves incoming-audio clarity. When enabled, you can independently configure:

- **Noise suppression**, on by default, to reduce background noise.
- **Echo cancellation**, on by default, to reduce speaker feedback.

Keep both enabled for typical browser speakerphone use. Test carefully with contact-center equipment or devices that already apply their own audio processing.

#### Automatic turn detection

Turn detection decides when the user finishes speaking. Tune it to avoid interrupting users or leaving unexplained silence.

##### Azure semantic

**Azure semantic** is the default. It uses semantic understanding of spoken content to detect the start and end of speech.

| Setting | Default | What it does |
| --- | --- | --- |
| **Type** | Multilingual | Selects **Multilingual** or **English** semantic detection. |
| **Remove user filler words** | On | Removes filler words such as "um" and "uh" from the transcript. |
| **End of utterance (EOU)** | Off, when available | Uses a model to determine whether the user completed a thought instead of relying only on silence. |

Use Azure semantic for conversational scenarios in which users pause while thinking or speak in complete phrases.

##### Basic

**Basic** detects speech from audio volume and exposes direct tuning controls.

| Setting | Default | Range | What it does |
| --- | ---: | ---: | --- |
| **Threshold** | 0.8 | 0 through 1 | Higher values require louder audio to trigger speech detection. |
| **Prefix padding** | 0.8 seconds | 0 through 1 second | Preserves audio immediately before detection so the beginning of a word isn't lost. |
| **Speech duration** | 0.8 seconds | 0 through 1 second | Sets the minimum speech duration treated as a user turn. |
| **Silence duration** | 0.8 seconds | 0 through 1 second | Sets how much silence ends the user's turn. |
| **End of utterance (EOU)** | Off, when available | On or off | Adds model-based end-of-thought detection. |

Lower **Threshold** for quiet speakers. Increase **Silence duration** if the agent interrupts users who pause. Decrease it if the agent waits too long.

#### Conversational behavior

Conversational behavior appears only for supported model and voice combinations. It isn't shown for realtime-native output voices.

##### Interim response

Turn on **Interim response** to play a brief spoken acknowledgment when a response takes longer to prepare. Choose:

- **LLM-generated messages** for a context-aware acknowledgment.
- **Static messages** for up to three controlled phrases. You must provide at least one phrase.

**Response threshold** specifies how long Foundry waits before playing the interim response. The default is 500 milliseconds; valid values are 10 through 10,000 milliseconds.

Use static messages when you need to control the wording. Don't use wording that implies a tool action succeeded before the tool result is available.

### Add an MCP tool or a toolbox

The **Tools** section provides **Add a MCP tool** and **Add a toolbox**. For a voice-based agent, a toolbox is the preferred way to provide tools because it supports reuse, versioning, centralized governance, and tool search. **Add a MCP tool** is the only way to attach a standalone tool directly to the agent. Use it when a required remote MCP server isn't managed through a toolbox.

<!-- Screenshot: Tools section showing Add a MCP tool and the Add a toolbox menu. -->

#### Add a MCP tool

Select **Add a MCP tool** to connect the agent directly to a remote Model Context Protocol (MCP) server. Enter a unique **Name**, the **Remote MCP Server endpoint**, an **Authentication** method, and the required credential key-value pairs. Then select **Connect**.

Use least-privilege credentials and review approval requirements for write or irreversible actions. During a conversation, the agent waits for the MCP result before responding, so tool latency becomes conversation latency.

#### Add a toolbox

A toolbox is a reusable, versioned collection of tools and policies presented through one MCP-compatible interface. Open **Add a toolbox** to select an existing project toolbox, or select **Create a toolbox**.

<!-- Screenshot: Tools section with an attached toolbox and the Add a MCP tool and Add a toolbox actions. -->

Use a toolbox when:

- Multiple agents should share the same governed capabilities.
- A central owner manages authentication, policies, and tool definitions.
- The collection contains many tools and tool search can reduce unnecessary tool definitions in model input.
- Changes need controlled, auditable versions.

> [!IMPORTANT]
> A voice-based agent can have individual tools or one toolbox, but not both. Attaching a toolbox replaces the agent's individual tools list.

##### Attach an existing toolbox

1. In **Tools**, select **Add a toolbox**.
1. Select a toolbox from the project list.
1. Confirm that the toolbox name and endpoint appear in the **Tools** section.
1. Select the main **Save** action before starting a voice session.

Selecting another toolbox replaces the currently attached toolbox. Use the toolbox row's actions menu to manage the attachment when those actions are available.

##### Create a toolbox and add an information source

The following example adds an Azure AI Search index so the agent can retrieve information from indexed customer content.

1. Select **Add a toolbox** > **Create a toolbox**.
1. Under **Basic info**, enter a unique **Name** and a description that tells project members what information or operations the toolbox provides.
1. Under **Included**, select **Add** > **Add tool**.
1. Find and select **Azure AI Search**.
1. In **Description**, explain what the selected index contains and when the agent should search it. For example: "Search the approved product support articles for setup requirements and troubleshooting steps."
1. Select an existing **Azure AI Search connection**. If none is available, select **Connect to new resource** and create the project connection.
1. Select one search index from the list. The list shows each index name and its available fields. If necessary, select **Create a new index** first.
1. Select **Add**.
1. If the toolbox contains many capabilities, turn on **Tool search**. Tool search lets the agent find the relevant tool during execution instead of placing every tool definition in the model input.
1. Review any toolbox guardrail policy, and then select **Publish**.

You need at least one tool or skill before you can publish the toolbox. The toolbox creation flow uses project permissions; a user without permission to create or update toolboxes must ask an administrator for the **Foundry User** role.

After you publish the toolbox from the playground, Foundry attaches the newly created toolbox to the agent. Confirm that it appears in **Tools**, and then select the main **Save** action to save the agent configuration.

> [!NOTE]
> To read an Azure AI Search index, the Foundry project managed identity needs the **Search Index Data Reader** role on the search resource. Creating an index also requires **Search Service Contributor**.

##### Help the agent use the information correctly

The tool description helps the model decide whether the tool is relevant. The agent instructions should define the broader response behavior. For example, tell the agent to:

- Search the toolbox before answering questions covered by the indexed source.
- Base the answer on the returned information instead of guessing.
- Say that the information wasn't found when the search returns no relevant result.
- Ask a clarifying question when the request is too broad for a reliable search.
- Never describe a lookup or action as successful before the tool returns.

Azure AI Search starts with **Simple** query type and returns up to five results by default. When supported by the index, use the tool's settings to select another search type or change the number of returned results from 1 through 50. More results can improve recall but add content, processing, and latency to the spoken turn.

##### Test retrieval in the playground

1. Select **Save**, and then start a new voice session.
1. Ask a question whose answer is present in the selected index.
1. Confirm that the agent invokes the toolbox and answers from the returned information.
1. Ask a question that isn't covered by the index. Confirm that the agent doesn't invent an answer.
1. Open the conversation in **Traces** and verify the tool-call span, tool arguments, returned result, status, and duration.

Also test unclear requests, denied access, empty results, timeouts, and tool failures. Tool execution adds conversation latency, so consider an interim response for lookups that commonly take longer.

Toolbox versions are immutable. Adding, editing, or removing a tool publishes a new version. Verify which version the agent uses after a toolbox update.

For more information, see [Model Context Protocol (MCP) tools](/azure/foundry/agents/how-to/tools/model-context-protocol).

### Configure an avatar

Turn on **Enable avatar** to add a visual speaker to supported browser experiences.

<!-- Screenshot: Avatar section with Enable avatar turned on, Lisa selected, Browse all avatars, and the save-before-start warning. -->

To select an avatar:

1. Turn on **Enable avatar**.
1. Select a suggested full-length or portrait avatar, such as **Lisa**, or select **Browse all avatars**.
1. In the browser, filter by **Portrait** or **Full-length**.
1. Select the avatar, and then select **Select**.
1. Select the main **Save** action.
1. Start a new voice session.

The selected avatar appears in the visual session and speaks with the agent's configured voice. Availability can depend on region, and photo avatars might not be available in every region.

> [!IMPORTANT]
> If the playground displays **Save the agent before starting**, save the agent before you select **Start**. A running session doesn't receive an unsaved avatar, voice, model, or advanced-setting change.

Selecting an avatar can incur separate charges. Review [Speech pricing](https://azure.microsoft.com/pricing/details/cognitive-services/speech-services/) before enabling it.

Avatars apply to supported visual browser or WebRTC experiences. Telephone callers receive audio only, even when an avatar is configured.

For current availability and requirements, see [Use real-time text-to-speech avatar](/azure/ai-services/speech-service/text-to-speech-avatar/real-time-synthesis-avatar).

### Add knowledge

Use **Knowledge bases** for project-managed information that grounds the agent's answers. Knowledge differs from a tool:

- Knowledge supplies content for answering questions.
- Tools retrieve live information or perform actions.

Tell the agent when to use grounded knowledge, when to call a tool, and what to do when neither source can answer safely.

### Start and test a session

In **Chat**:

1. Select **Save**.
1. Select the microphone from the audio-device menu.
1. Turn avatar video on or off, if an avatar is configured.
1. Optionally open **Metrics**.
1. Select **Start** and allow browser microphone access.

Test the greeting, accents, interruptions, long pauses, background noise, tool success and failure, important pronunciations, and the experience with and without an avatar.

Stop the session before changing the configuration. Save the new version and start another session to test it.

::: zone-end

## Related content

- [Optimize voice agent instructions](optimize-voice-agent-instructions.md)
- [Best practices for voice-based agents](../concepts/voice-agent-best-practice.md)
- [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).
- [Pricing for voice-based agents](../concepts/voice-agent-pricing.md).
- [Quickstart: Create a voice-based prompt agent](../quickstarts/prompt-voice-agent.md)
- [Agent development with the Azure Developer CLI](../concepts/cli-agent-development.md)
- [How to use the Voice Live API](/azure/ai-services/speech-service/voice-live-how-to)
- [Publish and connect a voice-based agent](voice-agent-channels-publish.md)
