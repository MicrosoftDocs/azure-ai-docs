---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
ai-usage: ai-assisted
---

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for JavaScript. This article extends the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) with more details on the features and integration options.

[!INCLUDE [Header](../../common/voice-live-javascript.md)] 

[!INCLUDE [Introduction](intro.md)]

> [!NOTE]
> The JavaScript Voice Live SDK is designed for browser-based applications with built-in WebSocket and Web Audio support. This how-to guide uses Node.js with `node-record-lpcm16` and `speaker` for a console experience. For a full browser-based voice UI, see the [Voice Live universal assistant sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/voice-live-universal-assistant).

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [Node.js](https://nodejs.org/) version 18 or later.
- [SoX](https://sox.sourceforge.io/) installed on your system (required by `node-record-lpcm16` for microphone capture).
- The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
<!-- - A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](../../../../../ai-foundry/quickstarts/get-started-code.md). -->
- Assign the `Azure AI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment and create the agent

Complete the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) to prepare the environment, set up the agent with Voice Live settings, and run the first test with the Voice Live service to talk to your agent.

## Agent integration concepts

Use these concepts to understand how Voice Live and Foundry Agent Service work together in the JavaScript sample.

### Agent configuration contract

Set the `agent` property with an `AgentSessionConfig` object in your `createSession(...)` call to identify the target agent and project. At minimum, include `agentName` and `projectName`. Add `agentVersion` when you want to pin behavior to a specific version.

### Authentication model for agent mode

Use Microsoft Entra ID credentials for agent mode. Agent invocation in this flow doesn't support key-based authentication, so configure `DefaultAzureCredential` (or another Entra token credential) for local development and deployment.

### API version pinning

Use a consistent SDK version (`@azure/ai-voicelive@1.0.0-beta.3`) in your `package.json` to keep behavior predictable across preview updates. Use the same version consistently across quickstart and how-to samples to avoid schema drift.

### Conversation and trace alignment

Treat agent thread and trace records as text-turn history, not exact playback history. If your app allows interruption or truncation, enable truncation-aware handling so persisted history better matches what the user actually heard.

## Connecting to a specific agent version

Voice Live supports connecting to a specific version of your agent, enabling controlled deployments where production uses a stable version while development tests newer iterations.

To connect to a specific agent version, set the `AGENT_VERSION` environment variable or pass the `agentVersion` property when initializing the assistant:

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="135-163,356-397" highlight="9,22,39,59":::

In this sample, the version configuration is applied in three places:

- In `main()`, `AGENT_VERSION` is read from `process.env`.
- In the `BasicVoiceAssistant` constructor, `agentVersion` is spread into the `agentConfig` object.
- The config is passed to `client.createSession({ agent: this.agentConfig })`, which sends it to Voice Live.

The `agentVersion` value corresponds to the version string returned when you create or update an agent using the Foundry Agent SDK. If not specified, Voice Live connects to the latest version of the agent.

## Connecting to an agent on a different Foundry resource

You can configure Voice Live to connect to an agent hosted on a different Foundry resource than the one used for audio processing. This is useful when:
- The agent is deployed in a region that has different feature availability
- You want to separate development/staging environments from production
- Your organization uses different resources for different workloads

To connect to an agent on a different resource, configure two additional environment variables:

- `FOUNDRY_RESOURCE_OVERRIDE`: The Foundry resource name hosting the agent project (for example, `my-agent-resource`).
- `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID`: The managed identity client ID of the Voice Live resource, required for cross-resource authentication.

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="135-163,356-397" highlight="11-14,25-28,43-44,61-62":::

This configuration is resolved in `main()` and then applied when the assistant is created:

- `FOUNDRY_RESOURCE_OVERRIDE` and `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` are read from `process.env`.
- Both values are spread into the constructor options.
- In the constructor, the values are conditionally set on the `agentConfig` object, which is sent in `client.createSession({ agent: this.agentConfig })`.

> [!IMPORTANT]
> Cross-resource connections require proper role assignments. Ensure the Voice Live resource's managed identity has the `Azure AI User` role on the target agent resource.

## Add a proactive message at session start

Voice Live can initiate the conversation by sending a proactive message as soon as the session is ready. In this sample, the assistant checks a one-time flag in the `onSessionUpdated` handler, sends a greeting prompt, and then triggers a response.

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="206-222" highlight="2-17":::

In this sample, proactive messaging is applied in three steps:

- `_greetingSent` is a `boolean` initialized to `false` to track one-time greeting state.
- In the `onSessionUpdated` handler, `if (!this._greetingSent)` gates proactive execution to run once per session.
- `session.addConversationItem(...)` adds the greeting instruction to conversation context, and `session.sendEvent({ type: "response.create" })` generates spoken output.

## Improving tool calling and latency wait times

Voice Live provides a feature called `interimResponse` to bridge wait times when tool calling is required or a high latency is experienced to generate an agent response.

The voice assistant created with the quickstart shows the required code additions to configure this feature as follows:

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="334-350" highlight="3-16":::

In this sample, the interim response setup is applied inside `_setupSession()`:

- `interimResponse` defines when interim responses trigger and what style they use.
- `session.updateSession(...)` sends the session configuration to Voice Live, including the interim response settings.

## Use auto truncation for interrupted responses

When users interrupt agent audio, conversation text can drift from what users actually heard. Auto truncation helps keep session context aligned with delivered audio, which improves follow-up response quality after barge-in and keeps voice conversation history logging more accurate.

This sample currently shows interruption handling with `response.cancel` during speech start, but it doesn't configure `auto_truncate` in `turn_detection`.

> [!NOTE]
> In Foundry Agent Service, thread messages and tracing agent threads are based on text content in the thread. Without auto truncation, those records can differ from the exact portion of audio the user actually heard before interruption.

For setup details and supported options, see [Handle voice interruptions in chat history (preview)](../../../how-to-voice-live-auto-truncation.md).

## Reconnect to a previous agent conversation

Voice Live enables you to reconnect to a previous conversation by specifying the conversation ID. This preserves the conversation history and context, allowing users to continue where they left off.

When a session connects successfully, Voice Live returns session metadata in the `onSessionUpdated` handler. The sample extracts the session ID from the context and logs it to the conversation file:

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="186-201":::

In this event handler, the session ID is extracted from `context.sessionId` and written to the conversation log along with agent metadata.

The sample code writes session details to a conversation log file in the `logs/` folder (for example, `logs/conversation_20260219_143000.log`).

To reconnect to that conversation, pass the conversation ID as the `CONVERSATION_ID` environment variable (or the `conversationId` property):

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="361,393-394":::

In this sample, conversation reconnect is applied in three places:

- In `main()`, `CONVERSATION_ID` is read from `process.env` (line 361).
- The value is passed to the `BasicVoiceAssistant` constructor.
- In the constructor, `conversationId` is conditionally spread into the `agentConfig` object.

When a valid `conversationId` is provided, the agent retrieves the previous conversation context and can reference earlier exchanges in its responses.

> [!NOTE]
> Conversation IDs are tied to the agent and project. Attempting to use a conversation ID with a different agent results in a new conversation being created.

## Log session metadata for continuity and diagnostics

The sample logs key session metadata, including the session ID, to a timestamped conversation log file under `logs/`. This helps you:

- Identify the session for debugging and support scenarios.
- Correlate user-reported behavior with session metadata.
- Track runs over time by preserving per-session log files.

The following code creates the log filename and writes session metadata when `onSessionUpdated` is received:

:::code language="javascript" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.js" range="21-33,186-201" highlight="1-2,9,14-15":::

In this sample, session metadata logging is applied in three places:

- A `logs/` directory is created if it doesn't exist, and a timestamped conversation log file (`conversation_YYYYMMDD_HHmmss.log`) is created per run (lines 21–29).
- On `onSessionUpdated`, the handler extracts the session ID from `context.sessionId` and writes it along with agent metadata to the log (lines 190–191).
- `writeConversationLog(...)` appends entries to the same log file throughout the conversation lifecycle (lines 31–33).

Use the logged session metadata with `CONVERSATION_ID` to resume the same agent conversation in a later session.

Use the session ID value alongside your conversation ID for diagnostics and reconnect scenarios.
