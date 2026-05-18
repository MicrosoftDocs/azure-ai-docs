---
title: "Enable tool search in a toolbox (preview)"
description: "Use tool search in Microsoft Foundry to help agents dynamically discover relevant tools from a large toolbox, reducing context overhead and improving tool selection accuracy."
author: zhuoqunli
ms.author: zhuoqunli
ms.reviewer: shpeng
ms.date: 05/10/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-foundry-tool-search
---

# Enable tool search in a toolbox (preview)

[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

When a toolbox contains many tools, listing all of them at once in `tools/list` can overwhelm the model's context window and reduce the quality of tool selection. Tool search solves this by giving the model a built-in search function that dynamically discovers the right tools for the current task.

When tool search is enabled, the model receives a built-in `tool_search` function it can call with a natural-language query. Foundry evaluates the query against the full set of tools in the toolbox and returns only the ones that match, keeping the active context focused and relevant.

Use tool search when:

- Your toolbox has more than 10–15 tools and you want to avoid context bloat.
- Different agent tasks need different subsets of tools, and you want the model to pick the right subset dynamically.

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- An existing or new toolbox with at least one tool. See [Curate intent-based toolbox in Foundry](toolbox.md).
- **RBAC**: Grant the **Foundry User** role on the Foundry project to each relevant identity (developer, agent managed identity, and end users in OAuth flows).
- **Python SDK**: `pip install azure-ai-projects azure-identity`

## How tool search works

When you include `ToolboxSearchPreviewTool` in a toolbox, all tools in the toolbox are hidden from the initial `tools/list` response. Instead, Foundry injects a single `tool_search` function. The model calls `tool_search` with a natural-language description of the capability it needs. Foundry evaluates the query against every tool in the toolbox and returns the matching tool definitions, making them immediately callable by the model.

The `tool_search` function accepts the following parameters:

| Parameter | Type | Required | Description |
| --------- | ---- | -------- | ----------- |
| `query` | string | Yes | Natural-language description of the capability or task you need a tool for. |
| `top_k` | integer | No | Maximum number of tools to return. Defaults to a platform value when omitted. |

The model can call `tool_search` as many times as needed during a single turn. Each call returns only the tools that match the query, so the active context stays focused on what's relevant to the current step. Tools returned by `tool_search` remain callable for the rest of the turn without repeated searching.

> [!NOTE]
> `ToolboxSearchPreviewTool` is a configuration directive that activates tool search. It doesn't appear in `tools/list` itself and doesn't count toward the unnamed-tool-per-type limit.

## Enable tool search

Add `ToolboxSearchPreviewTool` to your toolbox version. All other tools in the toolbox are available through tool search — they aren't exposed in the initial tool list the model sees.

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    MCPTool,
    ToolboxSearchPreviewTool,
)

client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# Define the MCP tools for the toolbox
github_mcp = MCPTool(
    server_label="github",
    server_url="https://api.githubcopilot.com/mcp",
    require_approval="never",
    project_connection_id="github-mcp-conn",
)

calendar_mcp = MCPTool(
    server_label="calendar",
    server_url="https://your-calendar-mcp.example.com",
    require_approval="never",
    description="Read and write calendar events",
)

# ToolboxSearchPreviewTool enables tool search — other tools are discovered on demand via tool_search
toolbox_version = client.beta.toolboxes.create_version(
    name="my-toolbox",
    description="Large toolbox with tool search enabled",
    tools=[github_mcp, calendar_mcp, ToolboxSearchPreviewTool()],
)
print(f"Created toolbox `{toolbox_version.name}` (version {toolbox_version.version})")
```

:::zone-end


:::zone pivot="rest-api"

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "Large toolbox with tool search enabled",
  "tools": [
    {
      "type": "tool_search_preview"
    },
    {
      "type": "mcp",
      "server_label": "github",
      "server_url": "https://api.githubcopilot.com/mcp",
      "require_approval": "never",
      "project_connection_id": "github-mcp-conn",
    },
    {
      "type": "mcp",
      "server_label": "calendar",
      "server_url": "https://your-calendar-mcp.example.com",
      "require_approval": "never",
    }
  ]
}
```

> [!NOTE]
> Use token scope `https://ai.azure.com/.default` when getting the bearer token.

:::zone-end


:::zone pivot="azd"

In `agent.yaml`, add `type: tool_search_preview` to your toolbox version's tools list:

```yaml
resources:
  - kind: toolbox
    name: my-toolbox
    tools:
      - type: tool_search_preview
      - type: mcp
        server_label: github
        server_url: https://api.githubcopilot.com/mcp
        require_approval: never
        project_connection_id: github-mcp-conn
        description: Access GitHub repositories, issues, and pull requests
```

For the full `azd` workflow, see [Deploy with azd](toolbox.md#deploy-with-azd).

:::zone-end

## Verify tool search is active

After creating a toolbox version, verify that `tool_search` appears in `tools/list`.

:::zone pivot="python"

```python
import asyncio
from azure.identity import DefaultAzureCredential
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

# Use the version-specific endpoint for validation
url = (
    "https://<account>.services.ai.azure.com/api/projects/<proj>"
    "/toolboxes/<name>/versions/<version>/mcp?api-version=v1"
)
token = DefaultAzureCredential().get_token("https://ai.azure.com/.default").token
headers = {
    "Authorization": f"Bearer {token}",
    "Foundry-Features": "Toolboxes=V1Preview",
}

async def verify():
    async with streamablehttp_client(url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            names = [t.name for t in tools_result.tools]
            print("Visible tools:", names)
            # tool_search should be in the list
            assert "tool_search" in names, "tool_search not found — check ToolboxSearchPreviewTool config"

asyncio.run(verify())
```

:::zone-end

:::zone pivot="rest-api"

**List tools** and confirm `tool_search` appears:

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","method":"notifications/initialized"}
```

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

In the response, `result.tools` should include `tool_search`.

:::zone-end



:::zone pivot="azd"

> [!NOTE]
> Use the REST API tab or the Python MCP client SDK to verify tool availability after deployment.

:::zone-end

## Configuration reference

### ToolboxSearchPreviewTool

| Field | Type | Required | Description |
| ----- | ---- | -------- | ----------- |
| `type` | `"tool_search_preview"` | Yes | Activates tool search for the toolbox. No other fields are required. |

Include `ToolboxSearchPreviewTool()` in your toolbox's tools list to enable tool search. No additional configuration is required.

## Considerations

- **All toolbox tools are hidden from the initial listing.** When `ToolboxSearchPreviewTool` is in a toolbox, no other toolbox tools appear in `tools/list`. The model discovers them only through `tool_search`. Tools added directly to an agent outside the toolbox are unaffected and remain visible.
- **Tool descriptions drive match quality.** Foundry uses tool names and descriptions to evaluate search queries. A tool without a description, or with a vague one, is unlikely to be returned even for relevant queries. Write descriptions that describe what the tool does and the kinds of tasks it handles.
- **`tool_search` doesn't count toward tool limits.** It's injected by the platform and doesn't consume the unnamed-tool-per-type slot.
- **Multiple searches per turn are supported.** The model can call `tool_search` more than once in a single turn if different steps need different capabilities.
- **Returned tools persist for the turn.** Once a tool is returned by `tool_search`, the model can call it multiple times without re-searching.

## Best practices

- **Add a description to every tool.** Tool search uses descriptions to match tools to queries. A missing or vague description causes poor discovery.
- **Use tool search for large toolboxes.** This is the most effective configuration when you have 10 or more tools.
- **Use tool search together with toolbox versioning.** Test your configuration on a version-specific endpoint before promoting it to default.
- **Mention tool search in the system prompt.** Guide the model to call `tool_search` before concluding that a capability is unavailable. For example: *"If you need a tool that isn't in your current list, call `tool_search` with a description of what you need before responding that you can't help."

## Troubleshoot

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| `tool_search` is missing from `tools/list` | `ToolboxSearchPreviewTool` wasn't included in the toolbox version, or you're connected to a version that predates the change. | Add `ToolboxSearchPreviewTool()` to the tools list and create a new version. Confirm you're using the updated version's endpoint. |
| `tool_search` returns no results for a query | Tools in the toolbox have no description or descriptions don't relate to the query. | Add or improve descriptions on the tools in the toolbox. Descriptions should explain what the tool does and the kinds of tasks it handles. |
| A toolbox tool appears in the initial `tools/list` | The tool was added directly to the agent instead of, or in addition to, the toolbox definition. | Remove the tool from the agent's direct tool list and rely on the toolbox. Tools added directly to an agent are always visible, regardless of tool search. |
| The model never calls `tool_search` | The model doesn't know `tool_search` can retrieve additional tools. | Add an instruction in the system prompt telling the model to call `tool_search` when a needed capability isn't in its current tool list. |
| `tool_search` is called but the tool returned fails to execute | The underlying tool's connection or configuration is invalid. | Verify the `project_connection_id` and other fields on the returned tool. Test the tool directly through the toolbox MCP endpoint without tool search enabled. |

## Related content

- [Curate intent-based toolbox in Foundry (preview)](toolbox.md)
- [Model Context Protocol (MCP)](model-context-protocol.md)
- [Tools overview](../../concepts/tool-catalog.md)
- [Best practices for tools](../../concepts/tool-best-practice.md)
