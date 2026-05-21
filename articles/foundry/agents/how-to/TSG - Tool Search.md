---
title: "Troubleshoot Tool Search (preview)"
description: "Diagnose and resolve common issues with intent-based tool routing using Tool Search in a Foundry Toolbox, including configuration, MCP session, and tool selection problems."
manager: nitinme
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: troubleshooting
ms.date: 05/20/2026
author: zhuoqunli
ms.author: zhuoqunli
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
---

# Troubleshoot Tool Search (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

This article helps you diagnose and resolve common issues with [Tool Search](tools/toolbox.md#tool-search) in a Foundry Toolbox. Tool Search (`tool_search_preview`) is an intent-based routing directive that selects the most relevant tools for each request without exposing all tools to the model at once.

> [!NOTE]
> `tool_search_preview` is a routing directive, not a callable tool. It doesn't appear in `tools/list` responses and doesn't count toward the unnamed-tool-per-type limit.

## Configuration issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| Tool Search doesn't select any tools | Toolbox has no other tools besides the routing directive | `tool_search_preview` selects among the other tools in the toolbox. Add at least one additional tool type. |
| `tools/list` returns 0 tools | Toolbox not fully provisioned, or `tool_search_preview` is the only entry | `tool_search_preview` is invisible to `tools/list`. Wait 10 seconds and retry. If the count remains 0, verify that other tools are configured in the toolbox. |
| Tool Search selects the wrong tool | Missing or vague tool descriptions | Add clear `description` fields to each tool. Tool Search uses these descriptions to match the user's intent to the right tool. |
| `400 Multiple tools without identifiers` | Two unnamed instances of the same built-in tool type | Include at most one unnamed instance of each type (`web_search`, `azure_ai_search`, `code_interpreter`, `file_search`) per toolbox. To use multiple instances, add a unique `name` to each. |
| Consumer endpoint returns an error | `default_version` not set on the toolbox | Before pointing agents to the consumer endpoint (`/toolboxes/{name}/mcp`), promote a version to default. See [Promote a version to default](toolbox.md#promote-a-version-to-default). |
| `401` on toolbox MCP calls | Expired or wrong-scope token | Use token scope `https://ai.azure.com/.default` and refresh the credential. |
| `500` on `tools/list` | Transient server error | Retry after a few seconds. If the error persists, verify the toolbox version exists and use the version-specific developer endpoint to isolate the issue. |

## MCP session issues

| Symptom | Likely cause | Resolution |
|---|---|---|
| `CONSENT_REQUIRED` (error code `-32006`) on MCP call | OAuth-based MCP tool requires first-use consent | Open the `consent_url` in the error message in a browser and complete the OAuth authorization flow. Subsequent calls succeed without re-prompting. |
| Tool names not matching expected format | MCP tool names are prefixed with `server_label` | Tools exposed by an MCP server in a toolbox are named `{server_label}.{tool_name}`. Use the full prefixed name when calling the tool. |
| MCP session errors on second call | `mcp-session-id` header not sent | After initialization, include the `mcp-session-id` header returned in the `initialize` response on all subsequent requests to the same session. |

> [!IMPORTANT]
> The `Foundry-Features: Toolboxes=V1Preview` header is required on all toolbox API calls during preview. A missing header returns a `404` or unexpected response.

## Related content

- [Curate intent-based toolbox in Foundry](tools/toolbox.md)
- [Connect agents to Model Context Protocol servers](tools/model-context-protocol.md)
- [MCP server authentication](mcp-authentication.md)
- [Troubleshoot connectors and managed MCP servers](TSG%20-%20Connectors.md)
