---
title: "Quickstart: Create a voice-based prompt agent"
description: "Create a managed voice-based prompt agent in Foundry Agent Service by using the Microsoft Foundry portal, the Microsoft Foundry SDK, or the Azure Developer CLI."
author: PatrickFarley
ms.author: pafarley
ms.date: 09/22/2026
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: quickstart
ms.custom: preview
ai-usage: ai-assisted
zone_pivot_groups: voice-agent-quickstart-tools
# customer intent: As a developer, I want to create and connect to a voice-based prompt agent so that I can build a real-time spoken experience.
---

# Quickstart: Create a voice-based prompt agent

In this quickstart, you create a voice-based prompt agent, open a live session, complete a spoken turn, and read the conversation back. Foundry Agent Service manages the voice orchestration, so you don't host a speech pipeline of your own.

Choose your development tool. The **Foundry portal** path creates and tests the agent in the browser with no code. The **Python SDK** and **JavaScript/TypeScript SDK** paths install the Microsoft Foundry SDK, create the agent in code, and connect to a live session over a WebSocket. The **Azure Developer CLI** path uses `azd` to scaffold, provision, deploy, and test the agent without writing runtime code. All paths create the same kind of managed prompt-based voice agent, which uses a managed real-time model.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Prerequisites

- A [Foundry project](../../how-to/create-projects.md).
- [Foundry User role](../../concepts/rbac-foundry.md) on the project, to create and invoke agents.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]
- A voice model available to your project, such as `gpt-realtime`. Confirm model availability on the **Models** page of your Foundry project.
- Access to the prompt voice agent preview in your Azure subscription. Confirm that the preview is available in your project's region before you start.

::: zone pivot="portal"

- A supported browser with microphone and speaker access.
- A microphone and speaker or headset for testing.

::: zone-end

::: zone pivot="python"

- Python 3.10 or later.
- The Azure CLI, signed in with `az login`.

::: zone-end

::: zone pivot="javascript"

- Node.js 22 or later.
- The Azure CLI, signed in with `az login`.

::: zone-end

::: zone pivot="azd"

- Azure Developer CLI version 1.32.0 or later and the Microsoft Foundry extensions. For the individual installation steps, see [Install the Azure Developer CLI Foundry extensions](../how-to/install-cli-foundry-extensions.md). To install the complete developer toolset, see [Prepare your development environment](../../how-to/develop/install-cli-sdk.md).
- An authenticated `azd` session. Run `azd auth login` after you install the extensions.
- The Azure permissions listed in [Install the Azure Developer CLI Foundry extensions](../how-to/install-cli-foundry-extensions.md#azure-permissions).

Check the installed agent extension version and its initialization options:

```azurecli
azd ai agent version
azd ai agent init --help
```

The initialization help must list `prompt-voice` under `--kind` and expose the `--voice` option. If `--voice` isn't listed, use an extension release that includes public-preview voice support before continuing. Public-preview CLI voice options don't require a private-preview environment variable.

::: zone-end

::: zone pivot="portal"

## Create the agent

1. Sign in to the [Microsoft Foundry portal](https://ai.azure.com/).
1. Open the project where you want to create the agent.
1. Go to the **Agents** page.
1. Select **Build an agent**. The **Create an agent** dialog opens.
1. In **Agent name**, enter a unique name for the agent.
1. Under **Interaction mode**, select **Voice**:

   - **Text**: Users type messages and receive text responses.
   - **Voice**: Users speak naturally and receive spoken responses in real time.

    > [!IMPORTANT]
    > You can't change the interaction mode after you create the agent. If you create a text agent and later need a voice agent, create another agent and select **Voice**.
1. Then select a use case to optimize for. This affects the default instructions for the agent.

Use a stable, recognizable name. The name appears in agent versions, traces and monitoring queries, evaluation target selection, phone-number bindings, and application and SDK references. The name must meet the validation rules shown in the dialog.

<!-- Screenshot: Create an agent dialog showing the agent-name field and the Text and Voice interaction modes. Alt text: "Create an agent dialog with a voice-based-agent name and Text and Voice interaction mode choices." -->

### Create and open the agent

Select **Create agent and open playground**. Foundry creates the voice agent and opens it in the agent playground.

Enter the agent instructions directly in the playground, and then review and customize them before testing.

The initial managed voice configuration is designed to start a session immediately and can include a managed realtime model, 24-kHz PCM audio input and output, automatic turn detection, transcription with Azure Speech in Foundry Tools, and a compatible Azure standard voice. The exact defaults can change. Treat the values shown in the portal as authoritative.

## Review the build page

Before testing, identify these areas:

- **Instructions**: Defines the agent's behavior.
- **AI model**: Selects a native speech or text model.
- **Speech recognition** and **Language**: Appear when required by the selected model.
- **Voice**: Selects the spoken output.
- **Avatar**: Adds visual output for supported browser experiences.
- **Tools**: Adds actions and external capabilities.
- **Knowledge bases**: Grounds answers in approved content.
- **Advanced settings**: Configures input audio, transcription, turn detection, and conversational behavior.
- **Playground**: Starts a live browser session.

<!-- Screenshot: Complete voice-agent build page with the configuration pane and playground labeled. Alt text: "Voice agent build page showing instructions, model, voice settings, advanced settings, and the session playground." -->

## Add initial instructions

Replace generic instructions with a small, testable first version. Include:

1. Who the agent is.
1. What tasks it can complete.
1. Who the intended caller is.
1. The required speaking style.
1. What information it must confirm.
1. What it must never disclose or do.
1. When it must transfer or refer the caller to a person.
1. What it says when a tool fails.

Example:

```text
You are a concise appointment assistant.

- Speak in short sentences and ask one question at a time.
- Confirm the caller's name and appointment time before making a change.
- Never read a full account identifier aloud.
- If the caller asks for medical advice, explain that you can only help with scheduling and offer the approved human-support path.
- If a tool fails, apologize, do not claim the change succeeded, and provide the approved next step.
```

For detailed configuration guidance, see [Configure a voice agent](../how-to/configure-voice-agent.md).

## Save and start a browser session

1. Select **Save**.
1. Select **Start session**.
1. Allow microphone access when the browser prompts you.
1. Say a short greeting and complete a simple scenario.
1. Interrupt the agent while it's speaking to test barge-in behavior.
1. Pause during a sentence to test turn detection.
1. Select **End** when the test is complete.

> [!NOTE]
> Configuration controls are disabled during an active voice session. End the session before changing the model, voice, avatar, tools, knowledge, or advanced settings.

<!-- Screenshot: Active voice session showing the transcript, session controls, and avatar if enabled. Alt text: "Voice-agent playground during an active microphone session." -->

## Validate the first session

Confirm that:

- The agent follows its instructions.
- The transcript recognizes your words.
- The voice language and pronunciation are correct.
- The response is short enough to understand by listening.
- The agent waits long enough for natural pauses.
- Interruption stops or redirects the response as expected.
- The agent doesn't claim a tool action succeeded when it didn't.
- The session ends cleanly.

## Troubleshoot creation and first-run issues

| Symptom | Resolution |
| --- | --- |
| **Voice** isn't available as an interaction mode | Confirm the preview is available for the project, resource, subscription, and region. |
| The agent name is rejected | Follow the name validation shown in the dialog and choose a unique name in the project. |
| The model list is empty | Confirm resource access, supported region, and model availability. Refresh after permissions or deployment changes. |
| The browser can't use the microphone | Allow microphone access for the portal origin and confirm the device isn't exclusively used by another app. |
| The session starts but no audio is heard | Confirm the browser output device, system volume, selected voice compatibility, and that the session isn't muted. |
| The start button remains unavailable | Save required configuration and resolve validation messages in the configuration pane. |

::: zone-end

::: zone pivot="python"

## Install the packages

These examples target version 2.7.0 or later of the Azure AI Projects client library.

Install the `voice` extra, which supplies `websockets` for synchronous connections and `aiohttp` for asynchronous connections.

```bash
python -m pip install "azure-ai-projects[voice]>=2.7.0" azure-identity
```

Voice session and conversation operations use `project_client.beta.voice_agents`. Creating voice definitions through the standard `.agents` methods still requires `allow_preview=True` on `AIProjectClient`. 

## Set environment variables

In Bash:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_VOICE_AGENT_NAME="my-voice-agent"
export FOUNDRY_VOICE_AGENT_MODEL="gpt-realtime"
```

In PowerShell:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_VOICE_AGENT_NAME = "my-voice-agent"
$env:FOUNDRY_VOICE_AGENT_MODEL = "gpt-realtime"
```

Find the project endpoint on the **Overview** page of your project in the Foundry portal.

`FOUNDRY_VOICE_AGENT_MODEL` applies only to the explicit-definition example. The generation example lets the service choose the model.

## Create the voice agent

A voice agent is an agent whose `kind` is `voice`. Its definition holds the model, instructions, and voice configuration. Both examples enable conversation storage by setting `store` to `true`, so you can read back the transcript and audio later.

Choose one of the following creation methods, and use a unique agent name. Save the complete example, and then run it as described after the examples.

### Generate from natural language

Describe what the agent should do in `goal`. Foundry uses this natural-language description to generate instructions and creates the agent with a complete voice configuration.

The following script lets the service choose the model and prints the generated instructions for review. It then enables storage in a new version, preserving the generated audio, greeting, tools, and other settings.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentKind,
    GenerateVoiceAgentRequest,
    VoiceAgentDefinition,
)
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    generated = project_client.beta.agents.create_from_prompt(
        GenerateVoiceAgentRequest(
            kind=AgentKind.VOICE,
            name=agent_name,
            goal=(
                "Create a friendly voice assistant that answers general "
                "questions. Keep replies to one or two sentences."
            ),
        )
    )
    definition = generated.versions.latest.definition
    if not isinstance(definition, VoiceAgentDefinition):
        raise TypeError("The generated agent must have a voice definition.")

    print(f"Generated instructions:\n{definition.instructions}")
    definition.store = True
    created = project_client.agents.create_version(
        agent_name=agent_name, definition=definition
    )
    print(f"Created voice agent '{agent_name}', version {created.version}")
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Review the printed instructions before talking to the agent. To customize the generated configuration, edit fields on its definition, such as `instructions`, and save another version.

### Create from an explicit definition

Use `VoiceAgentDefinition` when you want to specify the instructions, model, and voice yourself. The following script creates an agent version with an Azure standard voice and conversation storage enabled.

```python
import os

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    VoiceAgentAudioConfig,
    VoiceAgentAudioOutputConfig,
    VoiceAgentDefinition,
    VoiceModelType,
    VoiceOutputModality,
    VoiceType,
)
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]
model = os.environ.get("FOUNDRY_VOICE_AGENT_MODEL", "gpt-realtime")

definition = VoiceAgentDefinition(
    model_type=VoiceModelType.MANAGED,
    model=model,
    instructions=(
        "You are a friendly voice assistant. "
        "Keep replies to one or two sentences."
    ),
    audio=VoiceAgentAudioConfig(
        output=VoiceAgentAudioOutputConfig(
            voice="en-US-AvaNeural",
            voice_type=VoiceType.AZURE_STANDARD,
        ),
    ),
    output_modalities=[VoiceOutputModality.AUDIO],
    store=True,
)

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

### Run your chosen example

Run the file that contains your chosen example.

Save the example as `create_voice_agent.py`.

```bash
python create_voice_agent.py
```

The explicit-definition example sets the model type to `managed` to use a service-hosted model. To use your own deployment instead, set the model type to `self_deployed` and set the model to the deployment name.

Every create or update produces a new immutable version. The agent's endpoint is live as soon as the first version exists, with no separate deployment step. Continue with the same talk, read-back, and cleanup steps for either creation method.

## Talk to the agent

Connect to the agent's realtime session, send a turn, and collect the spoken reply. This script types the turn so it runs without audio hardware, and it saves the agent's spoken response to a WAV file.

If the agent has a startup greeting, the script receives that response before sending the user turn. Only the reply to the user turn is saved in `reply.wav`.

Create the Python file:

```python
import os
import wave

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    RealtimeConversationItemMessageUser,
    RealtimeConversationItemMessageUserContent,
    RealtimeConversationItemType,
    RealtimeServerEventError,
    RealtimeServerEventResponseAudioDelta,
    RealtimeServerEventResponseAudioTranscriptDone,
    RealtimeServerEventResponseDone,
    RealtimeServerEventSessionCreated,
    VoiceAgentDefinition,
)
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]

conversation_id = None

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    agent = project_client.agents.get(agent_name=agent_name)
    latest = agent.versions.latest
    definition = latest.definition
    if not isinstance(definition, VoiceAgentDefinition):
        raise TypeError("The agent must have a voice definition.")

    with project_client.beta.voice_agents.realtime.connect(
        agent_name=agent_name
    ) as conn:

        def receive_response() -> tuple[str | None, list[bytes]]:
            session_conversation_id: str | None = None
            chunks: list[bytes] = []
            while True:
                event = conn.recv(timeout=45)
                if isinstance(event, RealtimeServerEventSessionCreated):
                    session_conversation_id = event.conversation_id
                elif isinstance(event, RealtimeServerEventResponseAudioDelta):
                    chunks.append(event.delta)
                elif isinstance(
                    event, RealtimeServerEventResponseAudioTranscriptDone
                ):
                    print(f"Agent: {event.transcript}")
                elif isinstance(event, RealtimeServerEventError):
                    raise RuntimeError(event.error.message)
                elif isinstance(event, RealtimeServerEventResponseDone):
                    if event.response.status != "completed":
                        raise RuntimeError(
                            f"Response status: {event.response.status}"
                        )
                    return session_conversation_id, chunks

        if definition.greeting is not None:
            # A greeting has its own response.done, before the user's reply.
            conversation_id, _ = receive_response()

        conn.conversation.item.create(
            item=RealtimeConversationItemMessageUser(
                type=RealtimeConversationItemType.MESSAGE,
                content=[
                    RealtimeConversationItemMessageUserContent(
                        type="input_text",
                        text="Hi. In one sentence, what can you help me with?",
                    )
                ]
            )
        )
        conn.response.create()
        response_conversation_id, audio_chunks = receive_response()
        conversation_id = response_conversation_id or conversation_id

if not conversation_id:
    raise RuntimeError("No persisted conversation ID was returned.")
if not audio_chunks:
    raise RuntimeError("No audio was returned for the user turn.")

# The reply arrives as PCM16, mono, 24 kHz.
with wave.open("reply.wav", "wb") as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(24000)
    wav.writeframes(b"".join(audio_chunks))

print(f"Saved reply.wav ({len(audio_chunks)} audio chunks)")
print(f"Conversation id: {conversation_id}")
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Run the file, and then play `reply.wav`.

```bash
python talk_to_voice_agent.py
```

A few things to note about the session:

- The agent owns the model, instructions, voice, turn detection, and noise suppression on the server, so the client doesn't send a `session.update` event.
- The persisted conversation ID arrives on the `session.created` event, not at the end of the response.
- The reply streams as a series of audio deltas. A production client plays each delta as it arrives instead of buffering the whole response.

For a hands-free version that streams microphone audio and supports interruptions, see the [Python live-audio conversation sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/voice/sample_voice_agent_live_audio_conversation_async.py). It uses server-side turn detection to decide when you finish speaking.

## Read the conversation back

Because you set `store` to `true`, the transcript and audio are saved. Use the conversation ID that the previous script printed to read the transcript in chronological order.

Create the Python file:

```python
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]
conversation_id = sys.argv[1]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    conversations = project_client.beta.voice_agents.conversations

    conversation = conversations.get(agent_name, conversation_id)
    print(f"Conversation {conversation.id}: status={conversation.status}")

    for item in conversations.list_items(
        agent_name, conversation_id, order="asc"
    ):
        parts = [
            (part.get("transcript") or part.get("text") or "").strip()
            for part in (item.get("content") or [])
        ]
        transcript = " ".join(part for part in parts if part)
        if transcript:
            print(f"  {item.get('role')}: {transcript}")
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Run the file with the conversation ID.

```bash
python read_conversation.py <conversation-id>
```

You can also download the merged call recording, with the caller on the left channel and the agent on the right. See [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Clean up resources

Delete the stored conversation and agent when you're finished. Deleting them doesn't delete your project.

```python
import os
import sys

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
agent_name = os.environ["FOUNDRY_VOICE_AGENT_NAME"]
conversation_id = sys.argv[1]

with (
    DefaultAzureCredential() as credential,
    AIProjectClient(
        endpoint=endpoint, credential=credential, allow_preview=True
    ) as project_client,
):
    project_client.beta.voice_agents.conversations.delete(
        agent_name, conversation_id
    )
    project_client.agents.delete(agent_name=agent_name)
```

Reference: [Azure AI Projects client library for Python](https://aka.ms/azsdk/azure-ai-projects-v2/python/code).

Save the example as `clean_up.py`, and run it with the conversation ID:

```bash
python clean_up.py <conversation-id>
```

::: zone-end

::: zone pivot="javascript"

## Install the packages

These examples target version 2.7.0 or later of the Azure AI Projects client library.

Install `@azure/ai-projects` and `@azure/identity`. The client library includes the WebSocket dependencies that `project.beta.voiceAgents.realtime` requires.

```bash
npm init --yes
npm pkg set type=module
npm install @azure/ai-projects@2.7.0 @azure/identity
```

Voice session and conversation operations use `project.beta.voiceAgents`. When a standard `.agents` operation creates or modifies a voice agent, pass the `VoiceAgents=V1Preview` feature opt-in.

## Set environment variables

In Bash:

```bash
export FOUNDRY_PROJECT_ENDPOINT="https://<account>.services.ai.azure.com/api/projects/<project>"
export FOUNDRY_VOICE_AGENT_NAME="my-voice-agent"
export FOUNDRY_VOICE_AGENT_MODEL="gpt-realtime"
```

In PowerShell:

```powershell
$env:FOUNDRY_PROJECT_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>"
$env:FOUNDRY_VOICE_AGENT_NAME = "my-voice-agent"
$env:FOUNDRY_VOICE_AGENT_MODEL = "gpt-realtime"
```

Find the project endpoint on the **Overview** page of your project in the Foundry portal.

`FOUNDRY_VOICE_AGENT_MODEL` applies only to the explicit-definition example. The generation example lets the service choose the model.

## Create the voice agent

A voice agent is an agent whose `kind` is `voice`. Its definition holds the model, instructions, and voice configuration. Both examples enable conversation storage by setting `store` to `true`, so you can read back the transcript and audio later.

Choose one of the following creation methods, and use a unique agent name. Save the complete example, and then run it as described after the examples.

### Generate from natural language

Describe what the agent should do in `goal`. Foundry uses this natural-language description to generate instructions and creates the agent with a complete voice configuration.

The following script lets the service choose the model and prints the generated instructions for review. It then enables storage in a new version, preserving the generated audio, greeting, tools, and other settings.

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = /** @type {string} */ (
    process.env.FOUNDRY_PROJECT_ENDPOINT
);
const agentName = /** @type {string} */ (
    process.env.FOUNDRY_VOICE_AGENT_NAME
);
if (!projectEndpoint || !agentName) {
    throw new Error(
        "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_VOICE_AGENT_NAME.",
    );
}
const options = {
    requestOptions: {
        headers: { "foundry-features": "VoiceAgents=V1Preview" },
    },
};

async function main() {
    const project = new AIProjectClient(
        projectEndpoint,
        new DefaultAzureCredential(),
    );
    const generated = await project.beta.agents.createFromPrompt(
        {
            kind: "voice",
            name: agentName,
            model_type: "managed",
            use_case: "General assistance",
            goal: "Create a friendly voice assistant that answers general " +
                "questions. Keep replies to one or two sentences.",
        },
        options,
    );
    const generatedDefinition = generated.versions.latest.definition;
    if (generatedDefinition.kind !== "voice") {
        throw new Error("The generated agent must have a voice definition.");
    }
    const definition = /** @type {import("@azure/ai-projects").VoiceAgentDefinition} */ (
        generatedDefinition
    );

    console.log(`Generated instructions:\n${definition.instructions}`);
    definition.store = true;
    const created = await project.agents.createVersion(
        agentName,
        definition,
        options,
    );
    console.log(`Created voice agent '${agentName}', version ${created.version}`);
}

main().catch((error) => {
    console.error("Sample failed:", error);
    process.exitCode = 1;
});
```

Reference: [Generate a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/generate-voice-agent).

Review the printed instructions before talking to the agent. To customize the generated configuration, edit fields on its definition, such as `instructions`, and save another version.

### Create from an explicit definition

Use a voice agent definition when you want to specify the instructions, model, and voice yourself. The following script creates an agent version with an Azure standard voice and conversation storage enabled.

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = /** @type {string} */ (
    process.env.FOUNDRY_PROJECT_ENDPOINT
);
const agentName = /** @type {string} */ (
    process.env.FOUNDRY_VOICE_AGENT_NAME
);
const model = process.env.FOUNDRY_VOICE_AGENT_MODEL || "gpt-realtime";
if (!projectEndpoint || !agentName) {
    throw new Error(
        "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_VOICE_AGENT_NAME.",
    );
}
const options = {
    requestOptions: {
        headers: { "foundry-features": "VoiceAgents=V1Preview" },
    },
};

/** @type {import("@azure/ai-projects").VoiceAgentDefinition} */
const definition = {
    kind: "voice",
    model_type: "managed",
    model,
    instructions: "You are a friendly voice assistant. " +
        "Keep replies to one or two sentences.",
    audio: {
        output: {
            voice: "en-US-AvaNeural",
            voice_type: "azure-standard",
        },
    },
    output_modalities: ["audio"],
    store: true,
};

async function main() {
    const project = new AIProjectClient(
        projectEndpoint,
        new DefaultAzureCredential(),
    );
    const created = await project.agents.createVersion(
        agentName,
        definition,
        options,
    );
    console.log(`Created voice agent '${agentName}', version ${created.version}`);
}

main().catch((error) => {
    console.error("Sample failed:", error);
    process.exitCode = 1;
});
```

Reference: [Configure a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/configure-voice-agent).

### Run your chosen example

Run the file that contains your chosen example.

Save the example as `create_voice_agent.js`, and run it with Node.js:

```bash
node create_voice_agent.js
```

The explicit-definition example sets the model type to `managed` to use a service-hosted model. To use your own deployment instead, set the model type to `self_deployed` and set the model to the deployment name.

Every create or update produces a new immutable version. The agent's endpoint is live as soon as the first version exists, with no separate deployment step. Continue with the same talk, read-back, and cleanup steps for either creation method.

## Talk to the agent

Connect to the agent's realtime session, send a turn, and collect the spoken reply. This script types the turn so it runs without audio hardware, and it saves the agent's spoken response as raw PCM audio.

If the agent has a startup greeting, the script receives that response before sending the user turn. Only the reply to the user turn is saved in `reply.pcm`.

Create a file named `talk_to_voice_agent.js`:

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";
import { once } from "node:events";
import { createWriteStream } from "node:fs";
import { finished } from "node:stream/promises";

const projectEndpoint = /** @type {string} */ (
    process.env.FOUNDRY_PROJECT_ENDPOINT
);
const agentName = /** @type {string} */ (
    process.env.FOUNDRY_VOICE_AGENT_NAME
);
if (!projectEndpoint || !agentName) {
    throw new Error(
        "Set FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_VOICE_AGENT_NAME.",
    );
}
const options = {
    requestOptions: {
        headers: { "foundry-features": "VoiceAgents=V1Preview" },
    },
};
const pcmSampleRate = 24_000;

/**
 * @param {import("node:fs").WriteStream} output
 * @param {Uint8Array} audio
 */
async function writeAudio(output, audio) {
    if (!output.write(audio)) {
        await once(output, "drain");
    }
}

/**
 * @param {import("@azure/ai-projects").AgentDefinitionUnion} definition
 * @returns {definition is import("@azure/ai-projects").VoiceAgentDefinition}
 */
function isVoiceAgentDefinition(definition) {
    return definition.kind === "voice" &&
        "model_type" in definition &&
        (definition.model_type === "managed" ||
            definition.model_type === "self_deployed") &&
        "model" in definition &&
        typeof definition.model === "string";
}

async function main() {
    const project = new AIProjectClient(
        projectEndpoint,
        new DefaultAzureCredential(),
    );
    const agent = await project.agents.get(agentName, options);
    const definition = agent.versions.latest.definition;
    if (!isVoiceAgentDefinition(definition)) {
        throw new Error("The agent must have a voice definition.");
    }

    const connection = await project.beta.voiceAgents.realtime.connect(
        agentName,
        { store: true },
    );
    const audioOutput = createWriteStream("reply.pcm");
    let audioByteCount = 0;
    let conversationId;
    let userTurnSent = !definition.greeting;

    try {
        await connection.configureSession({
            type: "realtime",
            output_modalities: ["text", "audio"],
            audio: {
                output: {
                    format: { type: "audio/pcm", rate: pcmSampleRate },
                },
            },
        });
        if (userTurnSent) {
            await connection.sendText(
                "Hi. In one sentence, what can you help me with?",
            );
        }

        for await (const event of connection) {
            if (event.type === "session.created") {
                conversationId = event.conversation_id;
            } else if (event.type === "response.output_audio.delta" &&
                userTurnSent) {
                audioByteCount += event.delta.byteLength;
                await writeAudio(audioOutput, event.delta);
            } else if (event.type === "response.output_audio_transcript.done" &&
                userTurnSent) {
                console.log(`Agent: ${event.transcript}`);
            } else if (event.type === "error") {
                throw new Error(
                    `${event.error.code ?? "voice_agent_error"}: ` +
                        event.error.message,
                );
            } else if (event.type === "response.done") {
                if (event.response.status !== "completed") {
                    throw new Error(`Response status: ${event.response.status}`);
                }
                if (!userTurnSent) {
                    userTurnSent = true;
                    await connection.sendText(
                        "Hi. In one sentence, what can you help me with?",
                    );
                } else {
                    await connection.close();
                }
            }
        }
    } finally {
        audioOutput.end();
        try {
            await finished(audioOutput);
        } finally {
            await connection.dispose();
        }
    }

    if (!conversationId) {
        throw new Error("No persisted conversation ID was returned.");
    }
    if (audioByteCount === 0) {
        throw new Error("No audio was returned for the user turn.");
    }
    console.log(`Saved reply.pcm (${audioByteCount} bytes)`);
    console.log(`Audio format: PCM16, ${pcmSampleRate} Hz, mono.`);
    console.log(`Conversation id: ${conversationId}`);
}

main().catch((error) => {
    console.error("Sample failed:", error);
    process.exitCode = 1;
});
```

Reference: [Realtime text and tools JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/realtime-text-and-tools).

Run the file. The output is PCM16, 24-kHz, mono audio.

```bash
node talk_to_voice_agent.js
```

A few things to note about the session:

- The agent owns the model, instructions, voice, turn detection, and noise suppression on the server. The client uses `configureSession` only to request text and 24-kHz PCM audio output.
- The persisted conversation ID arrives on the `session.created` event, not at the end of the response.
- The reply streams as a series of audio deltas. A production client plays each delta as it arrives instead of buffering the whole response.

For a hands-free version that streams microphone audio and supports interruptions, see the [JavaScript realtime-audio sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/realtime-audio). This sample uses server-side turn detection to decide when you finish speaking.

## Read the conversation back

Because you set `store` to `true`, the transcript and audio are saved. Use the conversation ID that the previous script printed to read the transcript in chronological order.

Create a file named `read_conversation.js`:

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = /** @type {string} */ (
    process.env.FOUNDRY_PROJECT_ENDPOINT
);
const agentName = /** @type {string} */ (
    process.env.FOUNDRY_VOICE_AGENT_NAME
);
const conversationId = /** @type {string} */ (process.argv[2]);
if (!projectEndpoint || !agentName || !conversationId) {
    throw new Error(
        "Set the project endpoint and agent name, then pass a conversation ID.",
    );
}
const options = {
    requestOptions: {
        headers: { "foundry-features": "VoiceAgents=V1Preview" },
    },
};

/** @param {import("@azure/ai-projects").RealtimeConversationItemUnion} item */
function summarizeItem(item) {
    if (item.type !== "message" || !("content" in item)) {
        return `[${item.type}]`;
    }
    const text = item.content
        .map((part) => part.text ??
            ("transcript" in part ? part.transcript : undefined) ?? "")
        .filter(Boolean)
        .join(" ");
    return `[${item.role}] ${text || "(no text content)"}`;
}

async function main() {
    const project = new AIProjectClient(
        projectEndpoint,
        new DefaultAzureCredential(),
    );
    const conversations = project.beta.voiceAgents.conversations;
    const conversation = await conversations.get(
        agentName,
        conversationId,
        options,
    );
    console.log(`Conversation ${conversation.id}: status=${conversation.status}`);

    for await (const item of conversations.listItems(
        agentName,
        conversationId,
        { ...options, order: "asc" },
    )) {
        console.log(`  ${summarizeItem(item)}`);
    }
}

main().catch((error) => {
    console.error("Sample failed:", error);
    process.exitCode = 1;
});
```

Reference: [Voice agent conversation JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/voice-agent-conversations).

Run the file with the conversation ID.

```bash
node read_conversation.js <conversation-id>
```

You can also download the merged call recording, with the caller on the left channel and the agent on the right. See [Voice agent tracing, monitoring, and evaluation](../concepts/voice-agent-observability.md).

## Clean up resources

Delete the stored conversation and agent when you're finished. Deleting them doesn't delete your project.

```javascript
import { AIProjectClient } from "@azure/ai-projects";
import { DefaultAzureCredential } from "@azure/identity";

const projectEndpoint = /** @type {string} */ (
    process.env.FOUNDRY_PROJECT_ENDPOINT
);
const agentName = /** @type {string} */ (
    process.env.FOUNDRY_VOICE_AGENT_NAME
);
const conversationId = /** @type {string} */ (process.argv[2]);
if (!projectEndpoint || !agentName || !conversationId) {
    throw new Error(
        "Set the project endpoint and agent name, then pass a conversation ID.",
    );
}
const options = {
    requestOptions: {
        headers: { "foundry-features": "VoiceAgents=V1Preview" },
    },
};

async function main() {
    const project = new AIProjectClient(
        projectEndpoint,
        new DefaultAzureCredential(),
    );
    await project.beta.voiceAgents.conversations.delete(
        agentName,
        conversationId,
        options,
    );
    console.log(`Deleted conversation: ${conversationId}`);
    const deleted = await project.agents.delete(agentName, options);
    console.log(`Deleted: ${deleted.deleted}`);
}

main().catch((error) => {
    console.error("Sample failed:", error);
    process.exitCode = 1;
});
```

Reference: [Manage a voice agent JavaScript sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/javascript/voice-agents/manage-voice-agent).

Save the example as `clean_up.js`, and run it with the conversation ID:

```bash
node clean_up.js <conversation-id>
```

::: zone-end

::: zone pivot="azd"

## Initialize a prompt-based voice agent

Create an empty working directory, and start the interactive initialization flow:

```azurecli
mkdir voice-agent-quickstart
cd voice-agent-quickstart
azd ai agent init
```

Choose these options:

1. For **How do you want to initialize your agent?**, select **Create a prompt voice agent**.
1. Enter `voice-guide-managed` as the agent name.
1. Select **Create a new Foundry project**.
1. Select your tenant and Azure subscription.
1. Select a region where prompt-based voice agents are available.

Alternatively, specify the agent type, name, model, and output voice in the command. Run this command in the empty working directory in place of `azd ai agent init`:

```powershell
azd ai agent init --kind prompt-voice `
    --agent-name voice-guide-managed `
    --model gpt-realtime `
    --voice en-US-AvaNeural
```

Complete the Foundry project selection when prompted. The `--voice` option applies only when creating a new prompt voice agent. Don't combine this flow with hosted code options such as `--src`, `--runtime`, `--protocol`, or `--deploy-mode`.

When initialization finishes, change to the generated project directory:

```azurecli
cd voice-guide-managed
```

Open `azure.yaml`, and confirm that the agent definition contains these values:

```yaml
kind: prompt-voice
model:
  id: gpt-realtime
modelType: managed
name: voice-guide-managed
```

The `managed` model type tells Foundry to provide the real-time model for the agent. You don't need to create a model deployment separately.

The CLI generates `kind: prompt-voice` for compatibility. `kind: voice` is also accepted; you don't need to rename the generated kind to use public preview. To use your own model deployment, see [Choose a managed or self-deployed model](../how-to/configure-voice-agent.md#choose-a-managed-or-self-deployed-model).

## Provision the Foundry project

Provision the Foundry project and its required resources:

```azurecli
azd provision
```

## Deploy the voice agent

Deploy the prompt-based voice agent:

```azurecli
azd deploy voice-guide-managed
```

When deployment finishes, `azd` confirms the agent name, version, and endpoint for the active environment.

## Test the voice agent

`azd ai agent invoke` doesn't start voice conversations. When it recognizes a voice service in `azure.yaml`, it returns an error with guidance to use the Foundry portal, even if you specify `--protocol responses`. Use the playground to test the agent:

1. Open the [Foundry portal](https://ai.azure.com) and sign in.
1. Select the Foundry project that you provisioned.
1. In the left navigation, select **Build** > **Agents**.
1. Select **voice-guide-managed**, and then select **Open in playground**.
1. Start a voice session, and speak to the agent.
1. Confirm that the agent responds with synthesized speech and that the playground doesn't report a runtime error.

## Clean up resources

Run the cleanup command from the project directory:

> [!WARNING]
> If this `azd` environment created the Foundry project, `azd down` permanently deletes the project's resource group and everything in it. If you initialized the agent with an existing project, the command leaves that project and its resources in place.

```azurecli
azd down
```

::: zone-end

## Related content

::: zone pivot="portal"

- [Configure a voice agent](../how-to/configure-voice-agent.md)
- [Best practices for voice-first agents](../concepts/voice-agent-best-practice.md)
- [Integrate telephony channels with a voice agent](../how-to/voice-agent-telephony-channels.md)

::: zone-end

::: zone pivot="python"

- [Configure a voice agent](../how-to/configure-voice-agent.md)
- [Optimize voice agent instructions](../how-to/optimize-voice-agent-instructions.md)
- [Best practices for voice-based agents](../concepts/voice-agent-best-practice.md)
- [Integrate telephony channels with a voice agent](../how-to/voice-agent-telephony-channels.md)

::: zone-end

::: zone pivot="javascript"

- [Configure a voice agent](../how-to/configure-voice-agent.md)
- [Optimize voice agent instructions](../how-to/optimize-voice-agent-instructions.md)
- [Best practices for voice-based agents](../concepts/voice-agent-best-practice.md)
- [Integrate telephony channels with a voice agent](../how-to/voice-agent-telephony-channels.md)

::: zone-end

::: zone pivot="azd"

- [Agent development with the Azure Developer CLI](../concepts/cli-agent-development.md)
- [Configure a voice agent](../how-to/configure-voice-agent.md)
- [Build a voice agent with hosted agents](../how-to/build-voice-agent.md)
- [Deploy a hosted voice agent with azd](../how-to/deploy-hosted-voice-agent.md)

::: zone-end
