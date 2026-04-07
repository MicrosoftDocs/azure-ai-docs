---
author: PatrickFarley
ms.service: azure-ai-speech
ms.topic: include
ms.date: 03/30/2026
ms.author: pafarley
ai-usage: ai-assisted
---

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

### Voice UX considerations

Integrating MCP servers into a voice assistant introduces UX challenges that don't exist in text-based or console-based MCP clients. MCP tool calls can take 3–60+ seconds, approval prompts must happen conversationally, and users expect continuous spoken feedback. Plan for these patterns when building a voice-enabled MCP integration.

#### Voice-native approval

Console-based MCP samples typically use blocking input (such as `input()` or `readline`) for approval. In a voice assistant, blocking the audio pipeline freezes the conversation. Instead, handle approvals conversationally:

- Inject a system message that instructs the model to **verbally ask for permission**.
- Parse the user's spoken response for clear intent (`yes`, `no`, `stop`, `cancel`).
- Allow **barge-in** so the user can say "yes" without waiting for the full approval prompt to finish.
- Use word-boundary matching (such as `\byes\b`) to avoid false positives from words like "yesterday" or "nobody".

#### System instructions for the approval flow

The model needs explicit instructions about the approval flow in its system prompt. Without them, it might paraphrase the permission request into a generic "Let me look that up," skipping the actual question. Include language like:

> *"Some tools require user approval. When you receive a system message asking you to request permission, you MUST clearly ask the user for their explicit approval. Never skip the approval question or assume permission is granted."*

Use `"Say exactly:"` phrasing in per-request system messages to prevent the model from rewording the question.

#### Handle repeated tool calls

MCP servers might require multiple searches to gather complete information. Each search triggers a separate approval if `require_approval="always"`. Rather than asking the identical question each time:

- Track the call count per server.
- Change the prompt wording for subsequent calls (for example, "I need one more search. Should I continue?").
- Consider auto-denying after a maximum number of approved calls (for example, 3) to prevent infinite loops. The model responds with what it has.
- Reset the counter when results are delivered or the user denies a request.

For approval-required servers, consider auto-approving subsequent calls to the **same server within the same turn** to avoid repeated voice prompts for what is logically a single task.

#### Fill silence during tool calls

MCP tool calls can take several seconds to complete. Without feedback, the user assumes the assistant is unresponsive. Use these complementary layers:

1. **Tool announcements** (immediate, client-side): For auto-approved servers, have the assistant say something like "Let me look that up" when the call starts. Skip this for approval-required servers since the approval prompt already communicates that a tool call is happening.
2. **Stall detection** (client-side, repeating timer): If a tool call runs longer than expected, proactively tell the user the assistant is still waiting. A 10-second interval with a maximum of 3 notifications works well for medium-latency servers (5–15 seconds). Adjust the interval based on your expected MCP server latency.

> [!NOTE]
> MCP calls can't be cancelled. Stall notifications are status updates, not actionable options. Once a call starts, it runs until the server responds or times out.

#### Handle barge-in during MCP calls

Users naturally try to interrupt or ask "Are you still there?" during long tool calls. Rather than ignoring this:

- Inject a system message so the model can acknowledge the user.
- If the original MCP call completes later, introduce its result as a late result (for example, "By the way, those results from earlier just came in...").
- Protect against response collisions: when a cancelled response's completion handler runs, skip any deferred processing (pending approval prompts, queued MCP results) so it doesn't overlap with the user's new turn.

#### Choose MCP servers for voice latency

Not all MCP servers are well-suited for voice UX. When selecting MCP servers for a voice assistant:

- **Prefer low-latency servers** — search APIs, simple lookups, and cached data sources that respond within 5 seconds work best.
- **Avoid servers that perform heavy computation** — large repository analysis, complex document retrieval, or multi-step workflows can take 30–60+ seconds, degrading the voice experience.
- **Plan for non-cancellable calls** — MCP calls can't be cancelled from the client. If the user moves on during a slow call, the result arrives out of context and must be introduced as a late result, which can feel disjointed.
- **Consider your use case** — if users expect real-time answers, long-running MCP servers frustrate them. If the interaction style is more like a research assistant, asynchronous results might be acceptable.

### Troubleshooting

#### MCP tool discovery fails (`mcp_list_tools.failed`)

Voice Live contacts each MCP server's tool listing endpoint at session start. If discovery fails, no tools from that server are available during the session.

| Cause | Resolution |
|-------|------------|
| Incorrect `server_url` | Verify the MCP server URL is reachable and includes the correct path (for example, `https://mcp.deepwiki.com/mcp`). |
| Server is unreachable | Confirm the MCP server is running and accessible from Azure's network. Check firewall rules and DNS resolution. |
| Authentication failure | If the server requires authentication, verify the `authorization` or `headers` values are correct and not expired. |
| Server returns invalid tool schema | Check the MCP server's tool listing response conforms to the MCP specification. |

#### MCP tool call fails (`response.mcp_call.failed`)

A tool call failure means Voice Live successfully discovered the tool but the call didn't complete.

| Cause | Resolution |
|-------|------------|
| Server timeout | The MCP server took too long to respond. Optimize the server-side handler or choose a lower-latency server. |
| Server returned an error | Check your MCP server logs. Common issues include missing parameters, invalid input, or downstream service failures. |
| Network interruption | Transient network errors between Voice Live and the MCP server. Retry by prompting the model again. |

> [!TIP]
> When an MCP call fails, trigger `response.create` so the model can inform the user and continue the conversation. The sample code does this automatically.

#### No MCP events received

| Cause | Resolution |
|-------|------------|
| Wrong API version | MCP requires `api_version="2026-01-01-preview"` or later. Earlier API versions silently ignore MCP server configuration. |
| MCP servers not in session config | Verify that `MCPServer` objects are included in the `tools` list passed to `configure_session` or `updateSession`. |
| `allowed_tools` mismatch | If `allowed_tools` is set, only the listed tool names are exposed. Verify the names match exactly what the MCP server advertises. |

#### Approval requests not received

| Cause | Resolution |
|-------|------------|
| `require_approval` set to `"never"` | Tool calls auto-execute without approval. Change to `"always"` or use a per-tool dictionary if you need approval for specific tools. |
| Event handler not subscribed | Ensure your code listens for `mcp_approval_request` conversation items in the event loop. |
| Duplicate handling | The approval request arrives as a conversation item creation event, not a standalone event type. Check that your `conversation.item.created` handler inspects the item type. |

#### Response collision errors during MCP flow

Voice Live doesn't allow overlapping responses. During MCP flows, `response.create` calls can collide with an in-progress response.

| Cause | Resolution |
|-------|------------|
| `"Cancellation failed: no active response"` | Non-fatal. This occurs when a cancel is issued but the response already completed. Log and ignore. |
| `"active response"` errors | A new `response.create` was attempted while another response is still generating. Track response state (`response.created` / `response.done` events) and defer actions until the active response completes. |
| Interim response errors | Some model pipelines don't support `interimResponse`. If you receive interim response errors, remove the interim response configuration or verify your model supports it. |
