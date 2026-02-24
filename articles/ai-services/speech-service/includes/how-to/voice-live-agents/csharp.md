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

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for C#. This article extends the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) with more details on the features and integration options.

[!INCLUDE [Header](../../common/voice-live-csharp.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later.
- The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
<!-- - A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](../../../../../ai-foundry/quickstarts/get-started-code.md). -->
- Assign the `Azure AI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment and create the agent

Complete the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) to prepare the environment, set up the agent with Voice Live settings, and run the first test with the Voice Live service to talk to your agent.

## Agent integration concepts

Use these concepts to understand how Voice Live and Foundry Agent Service work together in the C# sample.

### Agent configuration contract

Set `AgentSessionConfig` in your session setup to identify the target agent and project. At minimum, include `agentName` and `projectName`. Add `AgentVersion` when you want to pin behavior to a specific version.

### Authentication model for agent mode

Use Microsoft Entra ID credentials for agent mode. Agent invocation in this flow doesn't support key-based authentication, so configure `AzureCliCredential` (or another Entra token credential) for local development and deployment.

### API version pinning

Use a consistent SDK version (`Azure.AI.VoiceLive` 1.1.0-beta.2) in the project file to keep behavior predictable across preview updates. Use the same version consistently across quickstart and how-to samples to avoid schema drift.

### Conversation and trace alignment

Treat agent thread and trace records as text-turn history, not exact playback history. If your app allows interruption or truncation, enable truncation-aware handling so persisted history better matches what the user actually heard.

## Connecting to a specific agent version

Voice Live supports connecting to a specific version of your agent, enabling controlled deployments where production uses a stable version while development tests newer iterations.

To connect to a specific agent version, set the `AGENT_VERSION` environment variable or pass the `agentVersion` parameter when initializing the assistant:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="190-217,455-513" highlight="9,27,35-38":::

In this sample, the version configuration is applied in three places:

- In `Main()`, `AGENT_VERSION` is read from the environment.
- In the `BasicVoiceAssistant(...)` constructor, `agentVersion` is passed in.
- In the constructor, the value is set on `AgentSessionConfig` via `config.AgentVersion`, and then sent to Voice Live via `StartSessionAsync(SessionTarget.FromAgent(agentConfig))`.

The `agentVersion` value corresponds to the version string returned when you create or update an agent using the Foundry Agent SDK. If not specified, Voice Live connects to the latest version of the agent.

## Connecting to an agent on a different Foundry resource

You can configure Voice Live to connect to an agent hosted on a different Foundry resource than the one used for audio processing. This is useful when:
- The agent is deployed in a region that has different feature availability
- You want to separate development/staging environments from production
- Your organization uses different resources for different workloads

To connect to an agent on a different resource, configure two additional environment variables:

- `FOUNDRY_RESOURCE_OVERRIDE`: The Foundry resource name hosting the agent project (for example, `my-agent-resource`).
- `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID`: The managed identity client ID of the Voice Live resource, required for cross-resource authentication.

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="190-217,455-513" highlight="14-18,29-30,37-38":::

This configuration is resolved in `Main()` and then applied when the assistant is created:

- `FOUNDRY_RESOURCE_OVERRIDE` and `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` are read from environment variables.
- Both values are passed to the `BasicVoiceAssistant(...)` constructor.
- In the constructor, the values are set on `AgentSessionConfig` via `config.FoundryResourceOverride` and `config.AuthenticationIdentityClientId`, which is sent in `StartSessionAsync(SessionTarget.FromAgent(agentConfig))`.

> [!IMPORTANT]
> Cross-resource connections require proper role assignments. Ensure the Voice Live resource's managed identity has the `Azure AI User` role on the target agent resource.

## Add a proactive message at session start

Voice Live can initiate the conversation by sending a proactive message as soon as the session is ready. In this sample, the assistant checks a one-time flag in the `SessionUpdateSessionUpdated` event handler, sends a greeting prompt, and then triggers a response.

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="399-431" highlight="3-32":::

In this sample, proactive messaging is applied in three steps:

- `_greetingSent` is a `bool` initialized to `false` to track one-time greeting state.
- In the `SessionUpdateSessionUpdated` branch, `if (!_greetingSent)` gates proactive execution to run once per session.
- `SendCommandAsync(...)` with a `conversation.item.create` payload adds the greeting instruction to conversation context, and a `response.create` command generates spoken output.

## Improving tool calling and latency wait times

Voice Live provides a feature called `InterimResponse` to bridge wait times when tool calling is required or a high latency is experienced to generate an agent response.

The feature supports the following two modes:
- `LlmInterimResponseConfig`: LLM-generated interim response - best for dynamic and adaptive starts
- `InterimResponseTrigger`: Pre-generated interim response - best for deterministic or branded messaging

The voice assistant created with the quickstart shows the required code additions to configure this feature as follows:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="261-295" highlight="3-13,19-20":::

In this sample, the interim response setup is applied inside `SetupSessionAsync()`:

- `ConfigureSessionAsync(options)` sends the base session configuration (audio formats) to Voice Live.
- A raw `session.update` command with `interim_response` settings is sent via `SendCommandAsync` because `VoiceLiveSessionOptions` doesn't expose the `InterimResponse` property in this SDK version.
- The `llm_interim_response` type configuration defines when interim responses trigger and what style they use.

## Use auto truncation for interrupted responses

When users interrupt agent audio, conversation text can drift from what users actually heard. Auto truncation helps keep session context aligned with delivered audio, which improves follow-up response quality after barge-in and keeps voice conversation history logging more accurate.

This sample currently shows interruption handling with `CancelResponseAsync()` during speech start, but it doesn't configure `auto_truncate` in `turn_detection`.

> [!NOTE]
> In Foundry Agent Service, thread messages and tracing agent threads are based on text content in the thread. Without auto truncation, those records can differ from the exact portion of audio the user actually heard before interruption.

For setup details and supported options, see [Handle voice interruptions in chat history (preview)](../../../how-to-voice-live-auto-truncation.md).

## Reconnect to a previous agent conversation

Voice Live enables you to reconnect to a previous conversation by specifying the conversation (thread) ID. This preserves the conversation history and context, allowing users to continue where they left off.

When a session connects successfully, Voice Live returns session metadata in the `SessionUpdateSessionUpdated` event. The sample extracts the session ID and logs it to the conversation file:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="307-327":::

In this event handler, the session ID is extracted from `sessionUpdated.Session?.Id` and written to the conversation log.

> [!NOTE]
> The C# SDK (1.1.0-beta.2) doesn't expose the agent `thread_id` in session events. To reconnect, use the conversation ID you provided when creating the session, or retrieve the thread ID through the Foundry Agent Service API.

The sample code writes session details to a conversation log file in the `logs/` folder (for example, `logs/conversation_20260219_143000.log`).

To reconnect to that conversation, pass the conversation ID as the `CONVERSATION_ID` environment variable (or the `conversationId` parameter):

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="464,489-492":::

In this sample, conversation reconnect is applied in three places:

- In `Main()`, `CONVERSATION_ID` is read from the environment (line 464).
- The value is passed to the `BasicVoiceAssistant(...)` constructor (lines 489-492).
- In the constructor, the value is set on `AgentSessionConfig` via `config.ConversationId`.

When a valid `conversationId` is provided, the agent retrieves the previous conversation context and can reference earlier exchanges in its responses.

> [!NOTE]
> Conversation IDs are tied to the agent and project. Attempting to use a conversation ID with a different agent results in a new conversation being created.

## Log session metadata for continuity and diagnostics

The sample logs key session metadata, including the session ID, to a timestamped conversation log file under `logs/`. This helps you:

- Identify the session for debugging and support scenarios.
- Correlate user-reported behavior with session metadata.
- Track runs over time by preserving per-session log files.

The following code creates the log filename and writes session metadata when `SessionUpdateSessionUpdated` is received:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="188-189,307-327,433-445" highlight="1-2,7-8,28-39":::

In this sample, session metadata logging is applied in three places:

- A timestamped conversation log file (`conversation_YYYYMMDD_HHmmss.log`) is created per run (lines 188–189).
- On `SessionUpdateSessionUpdated`, the handler extracts the session ID and writes it to the log (lines 315–316).
- `WriteLog(...)` appends entries to the same log file throughout the conversation lifecycle (lines 433–445).

Use the session ID value alongside your conversation ID for diagnostics and reconnect scenarios.
