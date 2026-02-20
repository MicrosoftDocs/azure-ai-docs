---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: patrickfarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 2/20/2026
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

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="254-265,487-489" highlight="2,10":::

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

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="256-258,263-270" highlight="3-4,10-12":::

> [!IMPORTANT]
> Cross-resource connections require proper role assignments. Ensure the Voice Live resource's managed identity has the `Azure AI User` role on the target agent resource.

## Improving tool calling and latency wait times

Voice Live provides a feature called `interim_response` to bridge wait times when tool calling is required or a high latency is experienced to generate an agent response.

The feature supports the following two modes:
- LlmInterimResponseConfig: LLM-generated interim response - best for dynamic and adaptive starts
- InterimResponseTrigger: Pre-generated interim response - best for deterministic or branded messaging

The `voice-live-agents-quickstart.py` created with the quickstart shows the required code additions to configure this feature as follows:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="17-31,325-348" highlight="9-10,20-26,33":::

## Reconnect to a previous agent conversation

Voice Live enables you to reconnect to a previous conversation by specifying the conversation (thread) ID. This preserves the conversation history and context, allowing users to continue where they left off.

When a session connects successfully, Voice Live returns the thread ID in the `SESSION_UPDATED` event:

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="376-386" highlight="6":::

The sample code automatically writes the thread ID to a conversation log file in the `logs/` folder (for example, `logs/2026-02-19_14-30-00_conversation.log`). You can retrieve the thread ID from this file after running a session.

To reconnect to that conversation, pass the thread ID as the `CONVERSATION_ID` environment variable (or the `conversation_id` parameter):

:::code language="python" source="..\..\code-samples\voice-live-agents\voice-live-with-agent-v2.py" range="255,267,490" highlight="1-3":::

When a valid `conversation_id` is provided, the agent retrieves the previous conversation context and can reference earlier exchanges in its responses.

> [!NOTE]
> Conversation IDs are tied to the agent and project. Attempting to use a conversation ID with a different agent results in a new conversation being created.
