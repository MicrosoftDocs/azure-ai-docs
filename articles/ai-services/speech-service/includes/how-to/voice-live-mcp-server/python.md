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

Learn how to connect remote MCP servers to a Voice Live session using the VoiceLive SDK for Python. This article builds on the [Quickstart: Create a Voice Live real-time voice agent](../../../voice-live-quickstart.md) with MCP server integration.

[!INCLUDE [Header](../../common/voice-live-python.md)]

[!INCLUDE [Introduction](intro.md)]

Follow the how-to below or get the full sample code:

> [!div class="nextstepaction"]
> [Voice Live MCP sample](https://github.com/microsoft-foundry/voicelive-samples/tree/main/python/voice-live-quickstarts/MCPQuickstart)

## Prerequisites

- An Azure subscription. [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
- <a href="https://www.python.org/" target="_blank">Python 3.10 or later version</a>. If you don't have a suitable version of Python installed, you can follow the instructions in the [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial#_install-a-python-interpreter) for the easiest way of installing Python on your operating system.
- A [Microsoft Foundry resource](../../../../multi-service-resource.md) created in one of the supported regions. For more information about region availability, see the [Voice Live overview documentation](../../../voice-live.md).
- `azure-ai-voicelive` package version 1.0.0b5 or later (MCP support requires `api_version="2026-01-01-preview"`).
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

> [!TIP]
> To use Voice Live with MCP, you don't need to deploy an audio model with your Foundry resource. Voice Live is fully managed, and the model is automatically deployed for you. For more information about model availability, see the [Voice Live overview documentation](../../../voice-live.md).

## Prepare the environment

Complete the [Voice Live quickstart](../../../voice-live-quickstart.md) to set up your environment, configure authentication, and test your first Voice Live conversation.

## MCP integration concepts

### MCP server definition

Use the `MCPServer` class to declare each remote MCP endpoint. At minimum, provide `server_label` (a display name) and `server_url` (the MCP endpoint URL). Optionally restrict available tools with `allowed_tools` and configure the approval mode.

### Approval modes

Control whether MCP tool calls require user approval before execution:

- `require_approval="never"`: The tool executes automatically when the model invokes it.
- `require_approval="always"` (default): The client receives an `mcp_approval_request` and must respond before the tool runs.
- Per-tool dictionary: Set `require_approval={"never": ["tool_a"], "always": ["tool_b"]}` for granular control.

### API version requirement

MCP support requires `api_version="2026-01-01-preview"` or later. Pass this value in the `connect()` call.

## Define MCP servers

Define the MCP servers that Voice Live can use during the session. Each server is an `MCPServer` instance added to the tools list in the session configuration.

The following code defines two MCP servers: one with automatic tool execution and one that requires user approval before running.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="define_mcp_servers":::

In this sample:

- The `deepwiki` server allows only `read_wiki_structure` and `ask_question` tools, with `require_approval="never"` for automatic execution.
- The `azure_doc` server allows all tools on the endpoint, with `require_approval="always"` so users can review each call before execution.

## Configure the session with MCP tools

Pass the MCP server definitions to the `RequestSession` tools list alongside your voice, modality, and turn-detection settings.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="configure_session":::

In this sample:

- `RequestSession` bundles MCP tools with audio format, voice, and turn detection settings.
- `connection.session.update(session=session_config)` sends the full configuration to Voice Live.
- Voice Live automatically discovers available tools from each MCP server after the session starts.

## Handle MCP events

Process MCP-specific events in the event loop. The key events are:

- `CONVERSATION_ITEM_CREATED` with `ItemType.MCP_CALL`: An MCP tool call was triggered by the model.
- `RESPONSE_MCP_CALL_COMPLETED`: The MCP call completed successfully.
- `RESPONSE_MCP_CALL_FAILED`: The MCP call failed.
- `CONVERSATION_ITEM_CREATED` with `ItemType.MCP_APPROVAL_REQUEST`: The server is requesting approval for a tool call.
- `CONVERSATION_ITEM_CREATED` with `ItemType.MCP_LIST_TOOLS`: Tool discovery completed for a server.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="handle_mcp_events":::

In this sample:

- `_handle_mcp_call_arguments` waits for the full arguments to stream in via `RESPONSE_MCP_CALL_ARGUMENTS_DONE`, then waits for the response to complete.
- `_handle_mcp_call_completed` receives the tool output and triggers a new response so the model can incorporate the result into its next spoken reply.

## Handle approval requests

When a server is configured with `require_approval="always"`, client code must handle the approval flow. Instead of blocking on console input, inject a system message so the model asks the user verbally and parse the spoken response.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="handle_approval":::

In this sample:

- The `mcp_approval_request` event contains `server_label`, `name` (tool name), and `arguments`.
- A system message instructs the model to verbally ask for permission.
- `MCPApprovalResponseRequestItem` sends the decision back to Voice Live with `approve=True` or `approve=False`.

## Resolve voice-based approval

Parse the user's spoken transcript to determine approval. Use word-boundary regex to avoid false positives from words like "yesterday" or "nobody".

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="voice_approval_transcription":::

In this sample:

- The transcript from `CONVERSATION_ITEM_INPUT_AUDIO_TRANSCRIPTION_COMPLETED` is matched against `\byes\b` and `\b(no|stop|cancel)\b` patterns.
- Subsequent calls to the same server within the same turn are auto-approved to avoid repeated prompts.
- After a configurable maximum (for example, 3 approvals), further calls are auto-denied and the model responds with what it has.

## Detect stalls during MCP tool calls

MCP tool calls can take several seconds. Use a repeating timer to proactively inform the user that the assistant is still waiting for results.

:::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py" id="mcp_stall_detection":::

In this sample:

- A 10-second interval timer injects system messages like "Tell the user you're still waiting" up to 3 times.
- The timer is cancelled when the MCP call completes or the user interrupts with barge-in.

## Run the sample

1. Create the `mcp-quickstart.py` file with the following code:

    :::code language="python" source="~/voice-live-samples-code/python/voice-live-quickstarts/MCPQuickstart/mcp-quickstart.py":::

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the Python script:

    ```shell
    python mcp-quickstart.py
    ```

1. Speak into your microphone. Try asking questions like "What tools do you have?" or "Search the Azure documentation for Voice Live API."

    - For the `deepwiki` server (`require_approval="never"`), tool calls execute automatically.
    - For the `azure_doc` server (`require_approval="always"`), you're prompted to approve each tool call in the console.

1. Press **Ctrl+C** to stop the session.

## MCP server configuration reference

| Parameter | Required | Description |
| --- | --- | --- |
| `server_label` | Yes | Display name for the MCP server. |
| `server_url` | Yes | URL of the remote MCP endpoint. |
| `allowed_tools` | No | List of tool names the model can call. If omitted, all tools are allowed. |
| `require_approval` | No | `"never"`, `"always"` (default), or a per-tool dictionary. |
| `headers` | No | Extra HTTP headers to include in MCP requests. |
| `authorization` | No | Authorization token for MCP requests. |

For the complete REST API type definition, see [MCPTool](../../../voice-live-api-reference-2026-01-01-preview.md#mcptool) in the Voice Live API reference.
