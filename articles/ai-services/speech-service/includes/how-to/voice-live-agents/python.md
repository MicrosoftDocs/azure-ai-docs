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

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for python. This article extends the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) with more details on the features and integration options.

[!INCLUDE [Header](../../common/voice-live-python.md)] 

[!INCLUDE [Introduction](intro.md)]

## Prerequisites

> [!NOTE]
> This document refers to the [Microsoft Foundry (new)](../../../../../ai-foundry/what-is-foundry.md#microsoft-foundry-portals) portal and the latest Foundry Agent Service version.

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- The required language runtimes, global tools, and Visual Studio Code extensions as described in [Prepare your development environment](../../../../../ai-foundry/how-to/develop/install-cli-sdk.md).
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- A model deployed in Microsoft Foundry. If you don't have a model, first complete [Quickstart: Set up Microsoft Foundry resources](../../../../../ai-foundry/default/tutorials/quickstart-create-foundry-resources.md).
<!-- - A Microsoft Foundry agent created in the [Microsoft Foundry portal](https://ai.azure.com/?cid=learnDocs). For more information about creating an agent, see the [Create an agent quickstart](../../../../../ai-foundry/quickstarts/get-started-code.md). -->
- Assign the `Azure AI User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Prepare the environment and create the agent

Please complete the [Quickstart: Create a Voice Agent with Foundry Agent Service and Voice Live](../../../voice-live-agents-quickstart.md) to prepare the environment and setup the agent with Voice Live settings and run the first test with the Voice Live service to talk to your agent.

## Connecting to a specific agent version

Voice Live supports connecting to a specific version of your agent, enabling controlled deployments where production uses a stable version while development tests newer iterations.

To connect to a specific agent version, set the `AGENT_VERSION` environment variable or pass the `agent_version` parameter when initializing the assistant:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="247-270,292-298,483-519" highlight="8,19,30,37,66":::

In this sample, the version configuration is applied in three places:

- In `main()`, `AGENT_VERSION` is read from the environment.
- In the `BasicVoiceAssistant(...)` call, `agent_version` is passed into the class constructor.
- In `BasicVoiceAssistant.__init__`, the value is added to `self.agent_config`, and then sent to Voice Live via `connect(..., agent_config=self.agent_config)`.

The `agent_version` value corresponds to the version string returned when you create or update an agent using the Foundry Agent SDK. If not specified, Voice Live connects to the latest version of the agent.

## Connecting to an agent on a different Foundry resource

You can configure Voice Live to connect to an agent hosted on a different Foundry resource than the one used for audio processing. This is useful when:
- The agent is deployed in a region that has different feature availability
- You want to separate development/staging environments from production
- Your organization uses different resources for different workloads

To connect to an agent on a different resource, configure two additional environment variables:

| Variable | Description |
|----------|-------------|
| `FOUNDRY_RESOURCE_OVERRIDE` | The Foundry resource name hosting the agent project (for example, `my-agent-resource`) |
| `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` | The managed identity client ID of the Voice Live resource, required for cross-resource authentication |

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="255-270,490-521,292-298" highlight="2-3,14-15,18-19,28-29,47,54":::

This configuration is resolved in `main()` and then applied when the assistant is created:

- `FOUNDRY_RESOURCE_OVERRIDE` and `AGENT_AUTHENTICATION_IDENTITY_CLIENT_ID` are read from environment variables.
- Both values are passed to `BasicVoiceAssistant(...)`.
- In `BasicVoiceAssistant.__init__`, the values are added to `self.agent_config`, which is sent in `connect(..., agent_config=self.agent_config)`.

> [!IMPORTANT]
> Cross-resource connections require proper role assignments. Ensure the Voice Live resource's managed identity has the `Azure AI User` role on the target agent resource.

## Add a proactive message at session start

Voice Live can initiate the conversation by sending a proactive message as soon as the session is ready. In this sample, the assistant checks a one-time flag in the `SESSION_UPDATED` event handler, sends a greeting prompt, and then triggers a response.

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="275,376-407" highlight="1,14-15,18-23,28":::

In this sample, proactive messaging is applied in three steps:

- `self.greeting_sent = False` initializes one-time greeting state.
- In the `SESSION_UPDATED` branch, `if not self.greeting_sent:` gates proactive execution to run once per session.
- `conn.conversation.item.create(...)` adds the greeting instruction to conversation context, and `conn.response.create()` generates spoken output.

## Improving tool calling and latency wait times

Voice Live provides a feature called `interim_response` to bridge wait times when tool calling is required or a high latency is experienced to generate an agent response.

The feature supports the following two modes:
- LlmInterimResponseConfig: LLM-generated interim response - best for dynamic and adaptive starts
- InterimResponseTrigger: Pre-generated interim response - best for deterministic or branded messaging

The `voice-live-agents-quickstart.py` created with the quickstart shows the required code additions to configure this feature as follows:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="17-31,325-348" highlight="9-10,20-26,33":::

In this sample, the interim response setup is applied inside `BasicVoiceAssistant._setup_session()`:

- `LlmInterimResponseConfig(...)` defines when interim responses trigger and what style they use.
- `RequestSession(...)` attaches that config through the `interim_response` field.
- `conn.session.update(session=session_config)` sends the session configuration to Voice Live.

## Use auto truncation for interrupted responses

When users interrupt agent audio, conversation text can drift from what users actually heard. Auto truncation helps keep session context aligned with delivered audio, which improves follow-up response quality after barge-in and keeps voice conversation history logging more accurate.

This sample currently shows interruption handling with `response.cancel()` during speech start, but it doesn't configure `auto_truncate` in `turn_detection`.

> [!NOTE]
> In Foundry Agent Service, thread messages and tracing agent threads are based on text content in the thread. Without auto truncation, those records can differ from the exact portion of audio the user actually heard before interruption.

For setup details and supported options, see [Handle voice interruptions in chat history (preview)](../../../how-to-voice-live-auto-truncation.md).

## Reconnect to a previous agent conversation

Voice Live enables you to reconnect to a previous conversation by specifying the conversation (thread) ID. This preserves the conversation history and context, allowing users to continue where they left off.

When a session connects successfully, Voice Live returns the thread ID in the `SESSION_UPDATED` event:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="377-386" highlight="7":::

In this event handler, the thread ID is available as `event.session.agent.thread_id` when the session is ready.

The sample code automatically writes the thread ID to a conversation log file in the `logs/` folder (for example, `logs/2026-02-19_14-30-00_conversation.log`). You can retrieve the thread ID from this file after running a session.

To reconnect to that conversation, pass the thread ID as the `CONVERSATION_ID` environment variable (or the `conversation_id` parameter):

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="255,267,490":::

In this sample, conversation reconnect is applied in three places:

- In `main()`, `CONVERSATION_ID` is read from the environment.
- In the `BasicVoiceAssistant(...)` call, `conversation_id` is passed into the class constructor.
- In `BasicVoiceAssistant.__init__`, the value is assigned into `self.agent_config` as `conversation_id`.

When a valid `conversation_id` is provided, the agent retrieves the previous conversation context and can reference earlier exchanges in its responses.

> [!NOTE]
> Conversation IDs are tied to the agent and project. Attempting to use a conversation ID with a different agent results in a new conversation being created.
