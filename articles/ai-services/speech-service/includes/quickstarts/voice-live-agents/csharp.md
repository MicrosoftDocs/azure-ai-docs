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

In this article, you learn how to use Voice Live with [Microsoft Foundry Agent Service](/azure/ai-foundry/agents/overview) using the VoiceLive SDK for C#.

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

## Prepare the environment

1. Create a new folder `voice-live-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir voice-live-quickstart && cd voice-live-quickstart
    ```

1. Create a **.csproj** file with the following project configuration:

    :::code language="xml" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgent.csproj":::

1. Restore NuGet packages:

    ```shell
    dotnet restore
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!NOTE]
> The C# Foundry Agent SDK (`Azure.AI.Projects`) uses a connection string instead of an endpoint URL. Set `PROJECT_CONNECTION_STRING` to your project connection string (found in the Foundry portal under **Project settings** > **Connected resources**).

## Create an agent with Voice Live settings

The agent creation script is a separate utility. Create a temporary console project to run it:

1. Create a separate folder for the agent creation utility:

    ```shell
    mkdir create-agent && cd create-agent
    dotnet new console --framework net8.0
    ```

1. Add the required NuGet packages:

    ```shell
    dotnet add package Azure.AI.Projects --prerelease
    dotnet add package Azure.Identity
    ```

1. Replace the contents of **Program.cs** with the following code:

    :::code language="csharp" source="..\..\code-samples\voice-live-agents\CreateAgentWithVoiceLive.cs":::

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Build and run the agent creation script:

    ```shell
    dotnet run
    ```

1. Return to the quickstart folder:

    ```shell
    cd ..
    ```

## Talk with a voice agent

The sample code in this quickstart uses Microsoft Entra ID for authentication as the current integration only supports this authentication method.

The sample connects to Foundry Agent Service by passing `AgentSessionConfig` to `StartSessionAsync(SessionTarget.FromAgent(...))` using these properties:

- `agentName`: The agent name to invoke.
- `projectName`: The Foundry project containing the agent.
- `AgentVersion`: Optional pinned version for controlled rollouts. If omitted, the latest version is used.
- `ConversationId`: Optional conversation ID to continue prior conversation context.
- `FoundryResourceOverride`: Optional resource name when the agent is hosted on a different Foundry resource.
- `AuthenticationIdentityClientId`: Optional managed identity client ID used with cross-resource agent connections.

> [!NOTE]
> Agent mode in Voice Live doesn't support key-based authentication for agent invocation. Use Microsoft Entra ID (for example, `AzureCliCredential`) for agent access. Voice Live resource configuration might still include API keys for non-agent scenarios.

1. Create the **VoiceLiveWithAgentV2.cs** file with the following code:

    :::code language="csharp" source="..\..\code-samples\voice-live-agents\VoiceLiveWithAgentV2.cs":::

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Build and run the voice assistant:

    ```shell
    dotnet run
    ```

1. You can start speaking with the agent and hear responses. You can interrupt the model by speaking. Enter "Ctrl+C" to quit the conversation.

## Output

The output of the script is printed to the console. You see messages indicating the status of the connection, audio stream, and playback. The audio is played back through your speakers or headphones.

```text
🎙️  Basic Foundry Voice Agent with Azure VoiceLive SDK (Agent Mode)
=================================================================

=================================================================
🎤 VOICE ASSISTANT READY
Start speaking to begin conversation
Press Ctrl+C to exit
=================================================================

🎤 Listening...
🤔 Processing...
👤 You said:	Hello.
🎤 Ready for next input...
🤖 Agent responded:	Hello! I'm Tobi the agent. How can I assist you today?
🎤 Listening...
🤔 Processing...
👤 You said:	What are the opening hours of the Eiffel Tower?
🎤 Ready for next input...
🤖 Agent responded:	The Eiffel Tower's opening hours can vary depending on the season and any special events or maintenance. Generally, the Eiffel Tower is open every day of the year, with the following typical hours:

- Mid-June to early September: 9:00 AM to 12:45 AM (last elevator ride up at 12:00 AM)
- Rest of the year: 9:30 AM to 11:45 PM (last elevator ride up at 11:00 PM)

These times can sometimes change, so it's always best to check the official Eiffel Tower website or contact them directly for the most up-to-date information before your visit.

Would you like me to help you find the official website or any other details about visiting the Eiffel Tower?

👋 Voice assistant shut down. Goodbye!
```

A conversation log file is created in the `logs` folder with the name `conversation_YYYYMMDD_HHmmss.log`. This file contains session metadata and the conversation transcript, including user inputs and agent responses.

```text
SessionID: sess_1m1zrSLJSPjJpzbEOyQpTL

User Input:	Hello.
Agent Audio Response:	Hello! I'm Tobi the agent. How can I assist you today?
User Input:	What are the opening hours of the Eiffel Tower?
Agent Audio Response:	The Eiffel Tower's opening hours can vary depending on the season...
```

Here are the key differences between the [technical log](#technical-log) and the [conversation log](#conversation-log):

| Aspect | Conversation Log | Technical Log |
|--------|-------------|---------------|
| **Audience** | Business users, content reviewers | Developers, IT operations |
| **Content** | What was said in conversations | How the system is working |
| **Level** | Application/conversation level | System/infrastructure level |
| **Troubleshooting** | "What did the agent say?" | "Why did the connection fail?" |

**Example**: If your agent wasn't responding, you'd check:
- **Console log** → "WebSocket connection failed" or "Audio stream error"
- **conversation log** → "Did the user actually say anything?"

Both logs are complementary - conversation logs for conversation analysis and testing, technical logs for system diagnostics!

### Technical log
**Purpose**: Technical debugging and system monitoring

**Contents**:
- WebSocket connection events
- Audio stream status
- Error messages and stack traces
- System-level events (session.created, response.done, etc.)
- Network connectivity issues
- Audio processing diagnostics

**Format**: Structured logging with timestamps, log levels, and technical details

**Use Cases**:
- Debugging connection problems
- Monitoring system performance
- Troubleshooting audio issues
- Developer/operations analysis

### Conversation log
**Purpose**: Conversation transcript and user experience tracking

**Contents**:
- Agent and project identification
- Session configuration details
- **User transcripts**: "Tell me a story", "Stop"
- **Agent responses**: Full story text and follow-up responses
- Conversation flow and interactions

**Format**: Plain text, human-readable conversation format

**Use Cases**:
- Analyzing conversation quality
- Reviewing what was actually said
- Understanding user interactions and agent responses
- Business/content analysis
