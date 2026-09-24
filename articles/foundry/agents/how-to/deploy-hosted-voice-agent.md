---
title: "Deploy a hosted voice agent with the Azure Developer CLI"
description: "Use azd to deploy a hosted text agent and a managed voice wrapper with conversationEngine in Microsoft Foundry Agent Service."
author: aahill
ms.author: aahi
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: how-to
ms.date: 09/22/2026
ms.custom: preview
ai-usage: ai-assisted
#customer intent: As a developer, I want to deploy a hosted agent with a managed voice wrapper so that I can add voice without implementing an audio pipeline.
---

# Deploy a hosted voice agent with the Azure Developer CLI

Use the Azure Developer CLI (`azd`) to deploy a hosted text agent and a voice wrapper in Microsoft Foundry Agent Service. The hosted agent handles conversation logic and model calls. Voice Live handles speech recognition, turn detection, speech synthesis, and playback interruption.

This workflow uses the [Voice Live Bridge basic Python sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic). Its `azure.yaml` defines both agents. You don't need to create the wrapper separately.

[!INCLUDE [feature-preview](../../includes/feature-preview.md)]

## Prerequisites

- Azure Developer CLI version 1.32.0 or later and the [Foundry extensions](install-cli-foundry-extensions.md). Check that the extension exposes the [public-preview voice CLI options](../quickstarts/prompt-voice-agent.md#prerequisites).
- An authenticated `azd` session. Run `azd auth login` before initialization.
- The [Azure permissions needed to provision Foundry resources](install-cli-foundry-extensions.md#azure-permissions).
- Access to voice agents and hosted agents in the selected subscription and region.
- Model availability and sufficient quota for the `gpt-5.4-mini` deployment declared in the sample.
- A voice client, such as the Foundry voice playground where available, and a microphone and speakers to test a spoken conversation.

## Initialize the sample

This walkthrough creates a new Foundry project. To reuse an existing project and model deployment, follow the sample's [existing-project instructions](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic#deploy-to-an-existing-foundry-project) instead. Don't apply the new-project provisioning steps below to a shared project.

In PowerShell, create an empty directory and initialize from the public sample manifest:

```powershell
mkdir hosted-voice-quickstart
cd hosted-voice-quickstart

$sample = "https://github.com/microsoft-foundry/foundry-samples/" +
    "blob/main/samples/python/hosted-agents/bring-your-own/" +
    "voice-agent-target-agent/basic/azure.yaml"
azd ai agent init -m $sample
```

When prompted, select your tenant and subscription, create a new Foundry project, and select a supported region. Review the sample's model selection before continuing.

Change to the generated directory that contains `azure.yaml`:

```powershell
cd voice-live-bridge-basic-python
```

## Review the target and voice wrapper

The sample declares two `azure.ai.agent` services:

| Service | Responsibility |
| --- | --- |
| `voice-live-bridge-basic-python` | The `kind: hosted` target. It receives text and control events through Voice Live Bridge Protocol 1.0 over `invocations_ws`, then streams model responses as text. |
| `voice-live-bridge-basic-python-voice` | The `kind: voice` wrapper. It configures the managed audio experience and references the hosted target through `conversationEngine`. |

The wrapper includes these fields under `services` in `azure.yaml`:

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

The `uses` dependency deploys the target before the wrapper. `conversationEngine.name` is the hosted target's service name in `azure.yaml`. The optional `conversationEngine.version` defaults to `deployed`, which selects the target version deployed by the current `azd` environment.

The wrapper and hosted target must have different Foundry agent names. Keep their `name` values distinct even if you rename the sample's services.

Keep model calls, instructions, and tools in the hosted target. Configure audio, voice output, and the greeting on the wrapper. Don't use the older `modelType: hosted_agent` or `targetAgent` settings.

The target must declare `invocations_ws` version `1.0.0`, with `voiceLiveCompatible: "true"` and `bridgeProtocolVersion: "1.0"` in its metadata. The sample already supplies these settings.

This wrapper workflow doesn't replace [custom audio pipelines hosted through `invocations_ws`](build-voice-agent.md). In this sample, the hosted target exchanges text and control events with Voice Live rather than processing caller audio itself.

For field details, see the [voice service configuration reference](../concepts/azure-yaml-reference.md#voice-services).

## Provision and deploy both agents

From the generated project directory, provision the Foundry project and the model declared in `azure.yaml`:

```powershell
azd provision
```

Set the model deployment name that the hosted target reads at runtime:

```powershell
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME gpt-5.4-mini
```

This variable selects the deployment used by the hosted target. It doesn't create or rename a model deployment.

Deploy all services so that `azd` deploys both the target and the wrapper:

```powershell
azd deploy
```

Inspect both agents and confirm that their deployed versions are active:

```powershell
azd ai agent show voice-live-bridge-basic-python
azd ai agent show voice-live-bridge-basic-python-voice
```

For model-backed turns, confirm that the hosted agent's identity has the **Cognitive Services OpenAI User** role, or equivalent inherited model-inference permissions, on the parent Foundry resource.

## Test the voice wrapper

Connect your voice client to `voice-live-bridge-basic-python-voice`, not to the hosted target. The caller uses the wrapper's voice endpoint; Voice Live exchanges Bridge Protocol events with the hosted target.

Use the Foundry voice playground where available. To use the SDK client, adapt the quickstart's storage-enabled example as described in this section.

### Adapt the SDK client for storage-disabled sessions

Complete the Python SDK [package installation](../quickstarts/prompt-voice-agent.md?pivots=python#install-the-packages) and [environment setup](../quickstarts/prompt-voice-agent.md?pivots=python#set-environment-variables). Set `FOUNDRY_PROJECT_ENDPOINT` to your deployed project's endpoint and `FOUNDRY_VOICE_AGENT_NAME` to `voice-live-bridge-basic-python-voice`. Use the existing wrapper; don't run the quickstart's agent-creation examples.

Copy `talk_to_voice_agent.py` from [Talk to the agent](../quickstarts/prompt-voice-agent.md?pivots=python#talk-to-the-agent). The wrapper uses `store: false`, so a persisted conversation ID isn't required for a successful voice response. Remove this storage-only check from the copied script:

```python
if not conversation_id:
    raise RuntimeError("No persisted conversation ID was returned.")
```

Keep the response-status check, the `audio_chunks` check, and the code that writes `reply.wav`. Remove the final `print(f"Conversation id: {conversation_id}")` line. Skip the quickstart's **Read the conversation back** section. Don't enable `store: true` just to satisfy the example's storage checks. The adapted script still saves response audio locally in `reply.wav`.

### Check text and audio

For the `/help` check in the copied SDK script, set the outgoing message's `text` value to `/help`.

1. Send `/help` as a text turn. Confirm that the response contains `Commands:`. This checks the sample's command path without making a model call.
1. Ask a short question to exercise the target's model deployment.
1. Send a spoken turn. Confirm that input transcription, response text, and audible output are present.
1. Speak while the agent responds, and check interruption behavior.

An active agent or a successful text response alone doesn't establish that the audio path works.

`azd ai agent invoke` doesn't generate Voice Live conversations. Selecting the voice wrapper returns [portal guidance](invoke-hosted-agent.md#voice-agent-limitations), not a voice session. For local Bridge Protocol checks, use the sample's [protocol smoke client](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/voice-agent-target-agent/basic#local-protocol-smoke-test).

## Troubleshoot

| Symptom | Action |
| --- | --- |
| Initialization reports `not logged in`. | Sign in with `azd auth login`, and run initialization again. |
| The extension doesn't recognize the voice options or `conversationEngine`. | Check the installed extension's voice support before continuing. |
| Wrapper deployment can't resolve its target. | Check that `conversationEngine.name` matches the hosted service name, that `uses` includes it, and that the target is active. |
| `/help` works, but model-backed turns fail. | Check the target's `AZURE_AI_MODEL_DEPLOYMENT_NAME`, model availability, and managed identity permissions for model inference. |
| The target reports `protocol_mismatch`. | Check Bridge Protocol 1.0 compatibility. The Bridge Protocol version is distinct from the `invocations_ws` transport version. |

## Clean up resources

> [!WARNING]
> `azd down` deletes the resource group and all resources created for this environment. Don't use it to clean up individual agents in a shared project.

For the new project created by this walkthrough, run:

```powershell
azd down
```

## Related content

For related configuration and development workflows, see:

- [Configure a voice agent](configure-voice-agent.md).
- [azure.yaml reference](../concepts/azure-yaml-reference.md).
- [Build a custom voice pipeline with hosted agents](build-voice-agent.md).
