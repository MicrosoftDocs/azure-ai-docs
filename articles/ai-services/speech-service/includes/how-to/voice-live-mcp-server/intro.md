---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ms.author: pafarley
ai-usage: ai-assisted
---

## Introduction 

Voice Live supports connecting to remote [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) servers during a voice session. MCP integration enables the model to discover and invoke tools hosted on external services, such as documentation search, wiki lookup, or custom APIs, and incorporate tool results into spoken responses.

MCP server integration differs from [function calling](../../../how-to-voice-live-function-calling.md) in these ways:

| Aspect | Function calling | MCP server |
| --- | --- | --- |
| Tool execution | Client-side | Server-side (managed by Voice Live) |
| Tool discovery | Client defines tools explicitly | Voice Live auto-discovers tools from MCP endpoint |
| Approval model | Not applicable | Configurable: `"always"` (default), `"never"`, or [per-tool dictionary](#approval-modes) |
| API version required | `2025-10-01` | `2026-01-01-preview` or later |

### Key concepts

- **`MCPServer` definition**: Declare one or more MCP endpoints in the session configuration with `server_label`, `server_url`, and optional `allowed_tools`, `headers`, `authorization`, and `require_approval`.
- **Tool discovery**: On session start, Voice Live calls each MCP server's tool listing endpoint and emits `mcp_list_tools` events.
- **Tool invocation**: When the model decides to call an MCP tool, the service handles execution and streams `response.mcp_call` events.
- **Approval flow**: When `require_approval` is set to `"always"` (the default), the client receives an `mcp_approval_request` conversation item and must respond with an `mcp_approval_response` before the call executes. Set `require_approval` to `"never"` for automatic execution, or use a per-tool dictionary to mix modes on the same server.

### Approval modes

The `require_approval` property on each `MCPServer` controls whether tool calls need client-side approval before execution. It accepts a string or a per-tool dictionary.

| Mode | Value | Behavior |
|------|-------|----------|
| Always (default) | `"always"` | Every tool call sends an `mcp_approval_request` to the client. The call doesn't execute until the client responds with `mcp_approval_response` and `approve=true`. |
| Never | `"never"` | Tool calls execute automatically. No approval event is sent. |
| Per-tool | `{"always": ["tool_a"], "never": ["tool_b", "tool_c"]}` | Each tool is assigned an approval mode individually. Tools not listed in either key default to `"always"`. |

**When to use each mode:**

- **`"always"`** — Use for tools that perform write operations, access sensitive data, or incur costs. The voice samples auto-approve subsequent calls to the same server within the same turn to reduce repeated prompts.
- **`"never"`** — Use for read-only lookups, search APIs, or trusted internal tools where user confirmation adds latency without security benefit.
- **Per-tool dictionary** — Use when a single MCP server exposes a mix of read-only and write tools. For example, a documentation server might allow `search_docs` without approval but require approval for `submit_feedback`.

> [!NOTE]
> In voice scenarios, each approval triggers a conversational prompt. Configure `require_approval` carefully to balance security with conversation flow. See [Voice-native approval](#voice-native-approval) for implementation patterns.

For the full MCP event and type reference, see [Voice Live API reference (2026-01-01-preview)](../../../voice-live-api-reference-2026-01-01-preview.md).


