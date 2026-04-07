---
manager: nitinme
author: PatrickFarley
ms.author: pafarley
reviewer: PatrickFarley
ms.reviewer: pafarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ai-usage: ai-assisted
---

Learn how to connect remote MCP servers to a Voice Live session using the VoiceLive SDK for C#. This article builds on the [Quickstart: Create a Voice Live real-time voice agent](../../../voice-live-quickstart.md) with MCP server integration.

[!INCLUDE [Header](../../common/voice-live-csharp.md)]

[!INCLUDE [Introduction](intro.md)]

Follow the how-to below or get the full sample code:

> [!div class="nextstepaction"]
> [Voice Live MCP sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/csharp/voice-live-quickstarts/MCPQuickstart)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- [.NET 8.0 SDK](https://dotnet.microsoft.com/download/dotnet/8.0) or later.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- `Azure.AI.VoiceLive` package version 1.1.0-beta.3 or later (MCP support requires API version `2026-01-01-preview`).
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

> [!TIP]
> To use Voice Live with MCP, you don't need to deploy an audio model with your Foundry resource. Voice Live is fully managed, and the model is automatically deployed for you. For more information about model availability, see the [Voice Live overview documentation](../../../voice-live.md).

## Prepare the environment

Complete the [Voice Live quickstart](../../../voice-live-quickstart.md) to set up your environment, configure authentication, and test your first Voice Live conversation.

## MCP integration concepts

### MCP server definition

Use the `VoiceLiveMcpServerDefinition` class to declare each remote MCP endpoint. At minimum, provide `ServerLabel` (a display name) and `ServerUrl` (the MCP endpoint URL). Optionally restrict available tools with `AllowedTools` and configure the approval mode.

### Approval modes

Control whether MCP tool calls require user approval before execution:

- `RequireApproval = "never"`: The tool executes automatically when the model invokes it.
- `RequireApproval = "always"` (default): The client receives an approval request and must respond before the tool runs.

### API version requirement

MCP support requires API version `2026-01-01-preview` or later.

## Define MCP servers

Define the MCP servers that Voice Live can use during the session. Each server is a `VoiceLiveMcpServerDefinition` instance added to the tools list in the session configuration.

The following code defines two MCP servers: one with automatic tool execution and one that requires user approval before running.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="define_mcp_servers":::

In this sample:

- The `deepwiki` server allows only `read_wiki_structure` and `ask_question` tools, with `RequireApproval` set to `"never"` for automatic execution.
- The `azure_doc` server allows all tools on the endpoint, with `RequireApproval` set to `"always"` so users can review each call before execution.

## Configure the session with MCP tools

Pass the MCP server definitions to the session options tools list alongside your voice, modality, and turn-detection settings.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="configure_session":::

In this sample:

- `VoiceLiveSessionOptions` bundles MCP tools with audio format, voice, and turn detection settings.
- `ConfigureSessionAsync(options)` sends the full configuration to Voice Live.
- Voice Live automatically discovers available tools from each MCP server after the session starts.

## Handle MCP events

Process MCP-specific events in the event loop. The key events include MCP tool call creation, completion, failure, and approval requests.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="handle_mcp_events":::

## Handle approval requests

When a server is configured with `RequireApproval = "always"`, client code must handle the approval flow. Instead of blocking on `Console.ReadLine()`, inject a system message so the model asks the user verbally and parse the spoken transcript for intent.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="handle_approval":::

In this sample:

- A system message instructs the model to verbally ask for permission.
- `McpApprovalResponseItem` sends the decision back to Voice Live with `Approve = true` or `Approve = false`.

## Resolve voice-based approval

Parse the user's spoken transcript to determine approval. Use word-boundary regex to avoid false positives from words like "yesterday" or "nobody".

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="voice_approval_transcription":::

In this sample:

- The transcript from `ConversationItemInputAudioTranscriptionCompleted` is matched against `\byes\b` and `\b(no|stop|cancel)\b` patterns.
- Subsequent calls to the same server within the same turn are auto-approved to avoid repeated prompts.
- After a configurable maximum (for example, 3 approvals), further calls are auto-denied and the model responds with what it has.

## Detect stalls during MCP tool calls

MCP tool calls can take several seconds. Use a repeating timer to proactively inform the user that the assistant is still waiting for results.

:::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs" id="mcp_stall_detection":::

In this sample:

- A 10-second interval timer injects system messages like "Tell the user you're still waiting" up to 3 times.
- The timer is cancelled when the MCP call completes or the user interrupts with barge-in.

## Run the sample

1. Create the **MCPQuickstart.cs** file with the following code:

    :::code language="csharp" source="~/voice-live-samples-code/csharp/voice-live-quickstarts/MCPQuickstart/MCPQuickstart.cs":::

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Build and run the application:

    ```shell
    dotnet run
    ```

1. Speak into your microphone. Try asking questions like "What tools do you have?" or "Search the Azure documentation for Voice Live API."

    - For the `deepwiki` server (`RequireApproval = "never"`), tool calls execute automatically.
    - For the `azure_doc` server (`RequireApproval = "always"`), you're prompted to approve each tool call in the console.

1. Press **Ctrl+C** to stop the session.

## MCP server configuration reference

| Parameter | Required | Description |
| --- | --- | --- |
| `ServerLabel` | Yes | Display name for the MCP server. |
| `ServerUrl` | Yes | URL of the remote MCP endpoint. |
| `AllowedTools` | No | List of tool names the model can call. If omitted, all tools are allowed. |
| `RequireApproval` | No | `"never"`, `"always"` (default), or a per-tool dictionary. |
| `Headers` | No | Extra HTTP headers to include in MCP requests. |
| `Authorization` | No | Authorization token for MCP requests. |

For the complete REST API type definition, see [MCPTool](../../../voice-live-api-reference-2026-01-01-preview.md#mcptool) in the Voice Live API reference.
