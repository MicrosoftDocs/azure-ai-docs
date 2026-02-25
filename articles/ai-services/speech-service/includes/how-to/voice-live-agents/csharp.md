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

In this article, you'll learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for C#. This article extends the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) with more details on features and integration options.

[!INCLUDE [Header](../../common/voice-live-csharp.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

> [!NOTE]
> This guide refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later.
- The required language runtimes, global tools, and Visual Studio Code extensions. See [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in a supported region. See [Voice Live overview documentation](../../../voice-live.md) for region availability.
- A deployed model in Microsoft Foundry. If you don't have one, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
- The `Azure AI User` role assigned to your user account. Assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment and create the agent

Complete the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) to prepare your environment, set up the agent with Voice Live settings, and run your first test.

## Agent integration concepts

These concepts help you understand how Voice Live and Foundry Agent Service work together in the C# sample.

### Agent configuration contract

Set `AgentSessionConfig` in your session setup to identify the target agent and project. Include at minimum `agentName` and `projectName`. Add `AgentVersion` when you want to pin behavior to a specific version.

### Authentication for agent mode

Use Microsoft Entra ID credentials for agent mode. Agent invocation doesn't support key-based authentication, so configure `AzureCliCredential` (or another Entra token credential) for local development and deployment.

### API version pinning

Use a consistent SDK version (`Azure.AI.VoiceLive` 1.1.0-beta.2) in your project file. Consistent versioning keeps behavior predictable across preview updates and avoids schema drift.

### Conversation and trace alignment

Treat agent thread and trace records as text-turn history, not exact playback history. If your app allows interruption or truncation, enable truncation-aware handling. This ensures persisted history better matches what users actually heard.

## Connect to a specific agent version

Voice Live lets you connect to a specific version of your agent. This enables controlled deployments where production uses a stable version while development tests newer iterations.

To connect to a specific agent version, set the `AGENT_VERSION` environment variable or pass the `agentVersion` parameter when initializing the assistant:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="190-217,455-513" highlight="9,27,35-38":::

The version configuration is applied in three places:

- In `Main()`, read `AGENT_VERSION` from the environment.
- Pass `agentVersion` to the `BasicVoiceAssistant(...)` constructor.
- In the constructor, set the value on `AgentSessionConfig` via `config.AgentVersion`. Send it to Voice Live via `StartSessionAsync(SessionTarget.FromAgent(agentConfig))`.

The `agentVersion` value corresponds to the version string returned when you create or update an agent using the Foundry Agent SDK. If not specified, Voice Live connects to the latest agent version.

## Connect to an agent on a different Foundry resource

Configure Voice Live to connect to an agent hosted on a different Foundry resource than the one used for audio processing.

This is useful in these scenarios:

- The agent is deployed in a region with different feature availability.
- You want to separate development and staging from production.
- Your organization uses different resources for different workloads.

To connect to an agent on a different resource, configure two environment variables:

- `FOUNDRY_RESOURCE_OVERRIDE`: The Foundry resource name hosting the agent project (for example, `my-agent-resource`).
- `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID`: The managed identity client ID of the Voice Live resource, required for cross-resource authentication.

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="190-217,455-513" highlight="14-18,29-30,37-38":::

The configuration is resolved in `Main()` and applied when the assistant is created:

- Read `FOUNDRY_RESOURCE_OVERRIDE` and `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` from environment variables.
- Pass both values to the `BasicVoiceAssistant(...)` constructor.
- In the constructor, set both values on `AgentSessionConfig` via `config.FoundryResourceOverride` and `config.AuthenticationIdentityClientId`. Send them in `StartSessionAsync(SessionTarget.FromAgent(agentConfig))`.

> [!IMPORTANT]
> Cross-resource connections require proper role assignments. Ensure the Voice Live resource's managed identity has the `Azure AI User` role on the target agent resource.

## Add a proactive message at session start

Voice Live can initiate conversations by sending a proactive message when the session is ready. The assistant checks a one-time flag in the `SessionUpdateSessionUpdated` event handler, sends a greeting prompt, and then triggers a response.

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="399-431" highlight="3-32":::

Proactive messaging is applied in three steps:

- `_greetingSent` is a `bool` initialized to `false` to track one-time greeting state.
- In the `SessionUpdateSessionUpdated` branch, `if (!_greetingSent)` gates execution to run once per session.
- `SendCommandAsync(...)` with a `conversation.item.create` payload adds the greeting to conversation context. A `response.create` command generates spoken output.

## Improve tool calling and latency wait times

Voice Live offers `InterimResponse` to bridge wait times during tool calling or when generating responses with high latency.

The feature supports two modes:

- `LlmInterimResponseConfig`: LLM-generated interim response—best for dynamic starts.
- `InterimResponseTrigger`: Pre-generated interim response—best for deterministic or branded messaging.

The quickstart voice assistant shows the required code additions:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="261-295" highlight="3-13,19-20":::

The interim response setup is applied inside `SetupSessionAsync()`:

- `ConfigureSessionAsync(options)` sends the base session configuration to Voice Live.
- A raw `session.update` command with `interim_response` settings is sent via `SendCommandAsync`. This is necessary because `VoiceLiveSessionOptions` doesn't expose the `InterimResponse` property in this SDK version.
- The `llm_interim_response` configuration defines when interim responses trigger and what style they use.

## Use auto truncation for interrupted responses

When users interrupt agent audio, conversation text can drift from what users actually heard. Auto truncation keeps session context aligned with delivered audio. This improves follow-up responses after barge-in and keeps conversation logging more accurate.

The sample currently shows interruption handling with `CancelResponseAsync()` during speech start, but it doesn't configure `auto_truncate` in `turn_detection`.

> [!NOTE]
> In Foundry Agent Service, thread messages and trace records are based on text content. Without auto truncation, these records can differ from the exact portion of audio users heard before interruption.

See [Handle voice interruptions in chat history (preview)](../../../how-to-voice-live-auto-truncation.md) for setup details and supported options.

## Reconnect to a previous agent conversation

Voice Live lets you reconnect to a previous conversation by specifying the conversation ID. This preserves conversation history and context, allowing users to continue where they left off.

When a session connects successfully, Voice Live returns session metadata in the `SessionUpdateSessionUpdated` event. Extract the session ID and log it to the conversation file:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="307-327":::

In this event handler, the session ID is extracted from `sessionUpdated.Session?.Id` and written to the conversation log.

The sample writes session details to a conversation log file in the `logs/` folder (for example, `logs/conversation_20260219_143000.log`).

To reconnect, pass the conversation ID as the `CONVERSATION_ID` environment variable or the `conversationId` parameter:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="464,489-492":::

Conversation reconnect is applied in three places:

- In `Main()`, read `CONVERSATION_ID` from the environment (line 464).
- Pass the value to the `BasicVoiceAssistant(...)` constructor (lines 489-492).
- In the constructor, set the value on `AgentSessionConfig` via `config.ConversationId`.

When a valid `conversationId` is provided, the agent retrieves the previous conversation context and can reference earlier exchanges.

> [!NOTE]
> Conversation IDs are tied to the agent and project. Using a conversation ID with a different agent creates a new conversation.

## Log session metadata for continuity and diagnostics

The sample logs key session metadata, including the session ID, to a timestamped conversation log file under `logs/`. This helps you:

- Identify the session for debugging and support.
- Correlate user-reported behavior with session metadata.
- Track runs over time by preserving per-session log files.

The following code creates the log filename and writes session metadata when `SessionUpdateSessionUpdated` fires:

:::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs" range="188-189,307-327,433-445" highlight="1-2,7-8,28-39":::

Session metadata logging is applied in three places:

- A timestamped conversation log file (`conversation_YYYYMMDD_HHmmss.log`) is created per run (lines 188–189).
- On `SessionUpdateSessionUpdated`, the handler extracts the session ID and writes it to the log (lines 315–316).
- `WriteLog(...)` appends entries throughout the conversation lifecycle (lines 433–445).

Use the logged session metadata with `CONVERSATION_ID` to resume the same agent conversation later. Use the session ID alongside your conversation ID for diagnostics and reconnect scenarios.
