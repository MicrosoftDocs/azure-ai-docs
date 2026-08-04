---
title: "Create and manage a toolbox in Foundry"
description: "Use toolbox in Microsoft Foundry to add MCP servers, web search, Azure AI Search, file search, code interpreter tool and more to hosted agents through a single managed endpoint."
author: mattwojo
reviewer: lindazqli
ms.author: mattwoj
ms.reviewer: zhuoqunli
ms.date: 07/20/2026
ms.manager: mcleans
ms.topic: how-to
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: selection-foundry-toolbox
---

# Create and manage a toolbox in Foundry

> [!WARNING]
> When you connect to non-Foundry tools, you might incur costs and data might be sent outside Foundry's compliance boundary and processed according to the applicable terms and data handling policies. See the tool's documentation to learn how to manage access to the tool.

This article shows you how to create a toolbox, add and configure tools, verify that they load, integrate the toolbox into a hosted agent, and manage toolbox versions. For a conceptual introduction to toolboxes, see [What is Toolbox in Foundry?](../../concepts/toolbox-overview.md). For tool configuration syntax and authentication options for each tool type, see [Configure tools](#configure-tools).

## Feature support

Toolbox management operations are available across the SDKs and tooling as shown here.

| Operation | Python SDK | REST API | .NET SDK | JavaScript SDK | Azure Developer CLI | Foundry Toolkit |
| --------- | ---------- | -------- | -------- | -------------- | --- | --------------- |
| Toolbox update, list, get, and delete | ✔️ | ✔️ | ✔️ | ✔️ | N/A | ✔️ |
| Toolbox version create | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Toolbox version list, get, and delete | ✔️ | ✔️ | ✔️ | ✔️ | N/A | No. UI shows the latest version only. |
| Guardrail (RAI policy) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

The following tools can be added to a toolbox. This table shows SDK and tooling support for each tool, whether the tool can also be attached directly to an agent (outside a toolbox), and whether the tool works when your project uses [network isolation (private link)](../../../how-to/configure-private-link.md). The **VNet support** column notes how traffic flows in a network-isolated environment.

| Tool | In a toolbox | Direct tool integration | Python SDK | REST API | .NET SDK | JavaScript SDK | Azure Developer CLI | Foundry Toolkit | VNet support (traffic flow) |
| ---- | ------------ | ----------------------- | ---------- | -------- | -------- | -------------- | --- | --------------- | --------------------------- |
| [Model Context Protocol (MCP)](model-context-protocol.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✅ Supported (through your VNet subnet) |
| [Web search](web-search.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✅ Supported (public endpoint) |
| [Azure AI Search](ai-search.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✅ Supported (through private endpoint) |
| [Code interpreter](code-interpreter.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✅ Supported (Microsoft backbone network) |
| [File search](file-search.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ❌ Not supported |
| [OpenAPI](openapi.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | No | ✅ Supported (depends on target API network configuration) |
| [Agent-to-agent (A2A)](agent-to-agent.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | No | ✅ Supported (through private endpoint) |
| [Browser automation](browser-automation.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | No | ❌ Not supported |
| [Fabric IQ](fabric-iq.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ❌ Not supported |
| [Work IQ](work-iq.md) | ✅ Yes | ✅ Yes | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ❌ Not supported |
| [Tool search](tool-search.md) | ✅ Yes | ❌ No | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | N/A |
| [Skills](skills.md) | ✅ Yes | ❌ No | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | No | N/A |

Tool availability also depends on your project's region and model. Before you deploy a toolbox, verify that your target region supports the tool types you plan to use. See [Tool support by region and model](../../concepts/limits-quotas-regions.md#tool-support-by-region-and-model).

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Grant the **Foundry User** role on the Foundry project to each identity that applies to your scenario:
  - **Developer** (always required) — the identity that creates, updates, and manages toolbox versions.
  - **Agent identity** (required if using a prompt agent) — the agent's managed identity that calls tools at runtime.
  - **End user** (required only for OAuth flows) — any user whose identity is proxied through OAuth or UserEntraToken connections (for example, OAuth-based MCP or user Entra token (managed user identity passthrough) flows).

  For step-by-step instructions to assign the **Foundry User** role to an agent identity, see [Assign permissions to the agent identity](../../concepts/agent-identity.md#assign-permissions-to-the-agent-identity).
- Your Foundry project needs to be at one of the supported [regions](../../concepts/limits-quotas-regions.md#supported-regions). Individual tool types within a toolbox are further limited by region and model – not all tool types are available in every region or with every model. See [Region and model compatibility](#region-and-model-compatibility).
- [Visual Studio Code (VS Code)](https://code.visualstudio.com/).
- Install the [Microsoft Foundry Toolkit for Visual Studio Code extension](https://aka.ms/foundrytk) from the Visual Studio Code Marketplace.
- **Python SDK**: `pip install azure-ai-projects azure-identity`
- **.NET SDK**: `dotnet add package Azure.AI.Projects --prerelease` and `dotnet add package Azure.Identity`
- **JavaScript SDK**: `npm install @azure/ai-projects @azure/identity`
- **Azure Developer CLI**: [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) (`azd`, 1.25 or later) and the unified Foundry CLI extension bundle:

  ```bash
  # Install the unified bundle (provides azd ai agent, connection, inspector,
  # project, routine, skill, and toolbox).
  azd ext install microsoft.foundry
  ```

> [!IMPORTANT]
> - A toolbox supports at most **one tool without a `name` field** (Web Search, Azure AI Search, Code Interpreter, File Search). To include more than one instance of the same tool type, set a unique `name` on each instance to differentiate them. Including two instances of the same type without a `name` returns an `invalid_payload` error. For details, see [Multiple tool types](#multiple-tool-types).
> - Add a `description` to every tool in your toolbox to help the model select the right tool for each request.
> - Carefully review each tool's documentation to learn more about individual tool setup, limitations, and warnings.

> [!TIP]
> If you're using GitHub Copilot for Azure to scaffold a hosted agent that consumes the toolbox, the following skill references describe the same endpoint contract (env var, headers, MCP protocol, citation patterns, and troubleshooting) that the agent must implement:
>
> - [Toolbox reference](https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/foundry-agent/create/references/toolbox-reference.md) — endpoint format, MCP protocol, OAuth consent handling, citation patterns, and troubleshooting.
> - [Use toolbox in a hosted agent](https://github.com/microsoft/GitHub-Copilot-for-Azure/blob/main/plugin/skills/microsoft-foundry/foundry-agent/create/references/use-toolbox-in-hosted-agent.md) — endpoint resolution, env-var contract, payload shape, code integration patterns, and tracing.

## Step 1: Create a toolbox version

Create a toolbox version based on the tools you need.

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, ToolSearchToolboxTool, WebSearchTool

# Create Foundry project client
endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"
project = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

# Create toolbox version with web search and MCP tools
toolbox_version = project.toolboxes.create_toolbox_version(
    name="my-toolbox",
    description="Toolbox with web search and an MCP server",
    tools=[
        WebSearchTool(),
        MCPTool(
            server_label="myserver",
            server_url="https://your-mcp-server.example.com",
            require_approval="never",
            project_connection_id="my-key-auth-connection",
        ),
        ToolSearchToolboxTool(),
    ],
)
print(f"Created toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
using Azure.Identity;
using Azure.AI.Projects;

// Create Foundry project client
var projectEndpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>";
AIProjectClient projectClient = new(new Uri(projectEndpoint), new DefaultAzureCredential());
AgentToolboxes toolboxClient = projectClient.AgentAdministrationClient.GetAgentToolboxes();

ProjectsAgentTool webTool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateWebSearchTool());

ProjectsAgentTool mcpTool = ProjectsAgentTool.AsProjectTool(ResponseTool.CreateMcpTool(
    serverLabel: "myserver",
    serverUri: new Uri("https://your-mcp-server.example.com"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.NeverRequireApproval
    )
));

ToolSearchToolboxTool searchTool = new() { Name = "ToolBoxSearch" };

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [webTool, mcpTool, searchTool],
    description: "Toolbox with web search, MCP, and tool search"
);
Console.WriteLine($"Created toolbox: {toolboxVersion.Name}, version: {toolboxVersion.Version}");
```

:::zone-end

:::zone pivot="rest-api"

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "Toolbox with web search, MCP, and tool search",
  "tools": [
    {
      "type": "web_search",
      "description": "Search the web for current information"
    },
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com",
      "require_approval": "never",
      "project_connection_id": "my-key-auth-connection"
    },
    {
      "type": "toolbox_search"
    }
  ]
}
```

> [!NOTE]
> Use token scope `https://ai.azure.com/.default` when getting the bearer token.

:::zone-end

:::zone pivot="javascript"

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { AIProjectClient } from "@azure/ai-projects";

// Create Foundry project client
const projectEndpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>";

const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());

const toolboxVersion = await project.toolboxes.createVersion(
  "my-toolbox",
  [
    {
      type: "web_search",
      description: "Search the web for current information",
    },
    {
      type: "mcp",
      server_label: "myserver",
      server_url: "https://your-mcp-server.example.com",
      require_approval: "never",
      project_connection_id: "my-key-auth-connection",
    },
    { type: "toolbox_search" },
  ],
  {
    description: "Toolbox with web search, MCP, and tool search",
  },
);
console.log(`Created toolbox: ${toolboxVersion.name}, version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Microsoft Foundry Toolkit for Visual Studio Code extension to create and publish a toolbox from the **Tools** view.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. Select the **+ Add Toolbox** icon.
1. On the **Build a Custom Toolbox** tab, enter the toolbox name and description, and add the tools you want.
1. To enable intent-based tool routing, select **Tool search**.
1. Select **Publish**.

Publishing a new toolbox creates its first version. That version becomes the default version automatically.

:::image type="content" source="../../media/tools/toolbox/toolbox-vscode-create.png" alt-text="Screenshot of the Microsoft Foundry Toolkit for Visual Studio Code extension showing the Build a Custom Toolbox view with fields for the toolbox name, description, and tools, plus the Publish action." lightbox="../../media/tools/toolbox/toolbox-vscode-create.png":::

:::zone-end

:::zone pivot="azd"

With the unified `microsoft.foundry` extension bundle (see [Prerequisites](#prerequisites)), create a toolbox in two steps:

1. Use `azd ai connection create` to register each project connection that the toolbox references (one call per credential record).
1. Use `azd ai toolbox create --from-file <toolbox.yaml>` to create the toolbox. The YAML references connections by name and never embeds credentials.

The pattern is the same for every connection kind and auth type:

1. Set the active project once per shell:

   ```bash
   azd ai project set $PROJECT_ENDPOINT
   ```

1. Create a connection with `azd ai connection create`. The flags differ per auth type, but the command shape is always:

   ```bash
   azd ai connection create <name> \
     --kind <remote-tool|remote-a2a|cognitive-search|GroundingWithCustomSearch> \
     --target <endpoint-url> \
     --auth-type <none|custom-keys|api-key|oauth2|user-entra-token|project-managed-identity|agentic-identity> \
     [--custom-key "Header=Value" | --key <key> | --client-id ... --client-secret ... --authorization-url ... --token-url ... | --audience <aad-resource-uri>]
   ```

   Use `azd ai connection list` and `azd ai connection show <name>` to inspect connections, and `azd ai connection delete <name> --force` to remove them.

3. Author a toolbox YAML that references one or more existing connections by name. The YAML never embeds credentials:

   ```yaml
   # my-toolbox.yaml
   description: <human-readable description>
   connections:
     - name: <project-connection-name>   # must already exist in the project
   # Optional: add connectionless built-in tools and policies.
   tools:
     - type: web_search
       name: web
     - type: code_interpreter
       container: { type: auto }
       name: code
     # Tool search is connectionless.
     - type: toolbox_search
     # For Azure AI Search, set the index in the tool entry:
     # - type: azure_ai_search
     #   name: search
     #   azure_ai_search:
     #     indexes:
     #       - project_connection_id: <azure-ai-search-connection-name>
     #         index_name: <search-index-name>
     # For Bing Custom Search, set the instance in the tool entry:
     # - type: bing_custom_search
     #   name: bing
     #   custom_search_configuration:
     #     project_connection_id: <bing-connection-name>
     #     instance_name: <bing-instance-name>
   # Optional: attach existing project skills as MCP resources.
   skills:
     - name: <skill-name>          # uses the skill's default version
     - name: <other-skill>
       version: "2"               # pin to a specific skill version (string)
   policies:
     rai_config:
       rai_policy_name: <policy-name>    # must already exist on the project
   ```

   At least one of `connections`, `skills`, or `tools` must be non-empty. Skill references must point to skills that already exist in the same Foundry project; see [Use skills in Foundry](skills.md) to create them with `azd ai skill create`. For end-to-end Tool Search setup details, see [Use tool search](tool-search.md).

4. Create the toolbox from that file:

   ```bash
   azd ai toolbox create <toolbox-name> --from-file ./my-toolbox.yaml
   ```

   The first version becomes the default automatically. Use `azd ai toolbox list`, `azd ai toolbox show <name>`, `azd ai toolbox version list <name>`, and `azd ai toolbox delete <name> --force` to manage toolboxes.

**Example: MCP server with key-based auth**

```bash
# 1. Create the connection
azd ai connection create my-gh-conn \
  --kind remote-tool \
  --target https://api.githubcopilot.com/mcp/ \
  --auth-type custom-keys \
  --custom-key "Authorization=Bearer $GITHUB_PAT"

# 2. Create the toolbox
azd ai toolbox create my-toolbox \
  --from-file ./my-toolbox.yaml \
  --no-prompt
```

```yaml
# my-toolbox.yaml
description: GitHub MCP toolbox
connections:
  - name: my-gh-conn
```

:::zone-end

## Step 2: Get the toolbox MCP endpoint

Two endpoint patterns exist depending on your role:

| Role | Endpoint | When to use |
| ---- | -------- | ----------- |
| **Toolbox developer** | `{project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1` | Test or validate a specific version before promoting it to default. |
| **Toolbox consumer** | `{project_endpoint}/toolboxes/{toolbox_name}/mcp?api-version=v1` | Connect agents to the toolbox. Always serves the `default_version`. The first version you create is automatically set as the default. |

Replace the placeholders with your own values:

- `{project_endpoint}` is your Foundry project endpoint, in the form `https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>`. Copy it from the **Overview** page of your project in the [Foundry portal](https://ai.azure.com), or from the **Endpoint URL** column in the **Toolboxes** view of the Microsoft Foundry Toolkit for Visual Studio Code.
- `{toolbox_name}` and `{version}` are the toolbox name and version you created in [Step 1](#step-1-create-a-toolbox-version).

> [!TIP]
> Connect agents to the **toolbox consumer** endpoint. It always serves the `default_version`, so you can promote new versions without changing agent code or redeploying. Reserve the **toolbox developer** (version-specific) endpoint for testing a version before you promote it.

> [!NOTE]
> The first version of a new toolbox is automatically promoted to `default_version` (v1). If you need to change the default later, see [Promote a version to default](#promote-a-version-to-default).

:::zone pivot="vscode"

In the Microsoft Foundry Toolkit for Visual Studio Code extension, copy the toolbox consumer endpoint from the **Toolboxes** view.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. On the **Toolboxes** tab, locate your toolbox.
1. In the **Endpoint URL** column, copy the endpoint.

The **Endpoint URL** value is the toolbox consumer endpoint. To construct a version-specific endpoint, use the developer pattern shown in the previous table.

:::image type="content" source="../../media/tools/toolbox/toolbox-vscode-list.png" alt-text="Screenshot of the Microsoft Foundry Toolkit for Visual Studio Code extension showing the Toolboxes view with the toolbox endpoint URL and the Scaffold code template action." lightbox="../../media/tools/toolbox/toolbox-vscode-list.png":::

:::zone-end

## Step 3: Verify tool availability

Before running the full agent, confirm that the toolbox loads the expected tools by using an MCP client SDK against the endpoint. Use the **version-specific endpoint** to validate a version before promoting it to default.

:::zone pivot="python"

Install the MCP client SDK:

```bash
pip install mcp
```

#### Connect to the toolbox and list tools

```python
import asyncio
from azure.identity import DefaultAzureCredential
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

url = "https://<account>.services.ai.azure.com/api/projects/<proj>/toolboxes/<name>/versions/<version>/mcp?api-version=v1"

token = DefaultAzureCredential().get_token("https://ai.azure.com/.default").token
headers = {
    "Authorization": f"Bearer {token}",
}

async def verify_toolbox():
    async with streamablehttp_client(url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print(f"Tools found: {len(tools_result.tools)}")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {(tool.description or '')[:80]}")

            # Call a tool (replace with actual tool name and arguments)
            result = await session.call_tool("<tool_name>", arguments={})
            print(result)

asyncio.run(verify_toolbox())
```

:::zone-end

:::zone pivot="dotnet"

> [!NOTE]
> Use the REST API tab to verify tool availability from .NET, or use the Python MCP client SDK.

:::zone-end

:::zone pivot="rest-api"

Use the version-specific endpoint (`/versions/{version}/mcp`) to validate a version before promoting it.

**1. Initialize the MCP session**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

**2. Send the initialized notification**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{"jsonrpc":"2.0","method":"notifications/initialized"}
```

**3. List available tools**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

**4. Call a tool**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"<TOOL_NAME>","arguments":{}}}
```

:::zone-end

:::zone pivot="javascript"

Install the MCP client SDK:

```bash
npm install @modelcontextprotocol/sdk
```

#### Connect to the toolbox and list tools

```javascript
import { DefaultAzureCredential } from "@azure/identity";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

const url = "https://<account>.services.ai.azure.com/api/projects/<proj>/toolboxes/<name>/versions/<version>/mcp?api-version=v1";

const credential = new DefaultAzureCredential();
const token = await credential.getToken("https://ai.azure.com/.default");

const transport = new StreamableHTTPClientTransport(
  new URL(url),
  {
    requestInit: {
      headers: {
        Authorization: `Bearer ${token.token}`,
      },
    },
  },
);

const client = new Client({ name: "test", version: "1.0" });
await client.connect(transport);

// List available tools
const toolsResult = await client.listTools();
console.log(`Tools found: ${toolsResult.tools.length}`);
for (const tool of toolsResult.tools) {
  console.log(`  - ${tool.name}: ${(tool.description || "").slice(0, 80)}`);
}

// Call a tool (replace with actual tool name and arguments)
const result = await client.callTool({ name: "<tool_name>", arguments: {} });
console.log(result);

await client.close();
```

:::zone-end

:::zone pivot="vscode"

Use the endpoint from Step 2 together with a scaffolded hosted agent sample to validate toolbox loading in VS Code.

1. In **Foundry Toolkit**, under **My Resources** > **Your project name** > **Tools**, locate the toolbox you want to test.
1. Select **Scaffold code template**.
1. Choose a project folder when prompted.
1. Follow the generated `README.md` to install dependencies, configure environment variables, and run the sample locally.
1. Use **Agent Inspector** or run `python main.py` to confirm the toolbox tools load and respond.

For version-specific validation before you promote a new toolbox version, use the Python or REST API tab in this step.

:::zone-end

:::zone pivot="azd"

> [!NOTE]
> Use the REST API tab to verify tool availability, or use the Python MCP client SDK.

:::zone-end


**Check — initialize**: HTTP 200. If you skip the initialize step, subsequent calls fail.

**Check — `tools/list`**:

- `len(tools) > 0` — empty means the toolbox version wasn't provisioned correctly.
- Each tool has `name`, `description`, and `inputSchema`. For tool naming conventions, see the [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/server/tools).
- `inputSchema` has a `properties` field (some MCP servers omit this field, which breaks OpenAI).
- Tool names are namespaced by tool type:

  | Tool type | Tool name format | Example |
  | --------- | ---------------- | ------- |
  | MCP | `{server_label}.{tool_name}` | `myserver.some_tool` |
  | OpenAPI | `{openapi_name}.{operationId}` | `weatherapi.getForecast` |
  | A2A | The tool's `name` (agent name), or the connection name if `name` is omitted | `myagent` |
  | All other tool types | The `name` field value or the default tool name | `web_search` |

- MCP tools include a `_meta.tool_configuration` block containing runtime settings such as `require_approval`. See [Enforce tool approval](use-toolbox-hosted-agent.md#enforce-tool-approval).
- Note the exact parameter names for the call step (for example `query` vs `queries`).

**Check - `tools/call`**:

- No top-level `error` field. If present, inspect `error.code`. For standard MCP error codes, see the [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/server/tools#error-handling):
  - `-32006` → OAuth consent required (extract URL from `error.message`).
  - Other codes → server-side failure.
- `result.content[]` contains entries with `"type": "text"` - this is the tool output.
- For AI Search, check `result.structuredContent.documents[]` for chunk metadata (`title`, `url`, `id`, `score`).
- For File Search, check `result.content[].resource._meta` for chunk metadata (`title`, `file_id`, `document_chunk_id`, `score`).
- For Web Search, check `result.content[].resource._meta.annotations[]` for URL citations (`type`, `url`, `title`, `start_index`, `end_index`).
- For Fabric IQ, check `result.structuredContent.documents[]` for citation chunks. Each document includes `title` and `url` fields pointing back to the Fabric item (Ontology, data agent, or Power BI semantic model) used to ground the response.
- Watch for `"ServerError"` in text content - the tool executed but hit an internal error.

Tool-specific `tools/call` argument examples:

| Tool type | Arguments |
| --------- | --------- |
| AI Search | `{"query": "search text"}` |
| File Search | `{"queries": ["search text"]}` — or `{"queries": ["search text"], "vector_store_ids": ["<VECTOR_STORE_ID>"]}` when vector store is passed dynamically |
| Code Interpreter | `{"code": "print(2 ** 100)"}` |
| Web Search | `{"search_query": "weather in seattle"}` |
| A2A | `{"message": {"parts": [{"type": "text", "text": "Hello"}]}}` |
| Fabric IQ | Varies by exposed tool — typically `{"query": "..."}` for query tools |
| Work IQ | `{"message": {"parts": [{"type": "text", "text": "Hello"}]}}` |
| MCP | `{"query": "what is agent service"}` |

## Step 4: Integrate the toolbox into your agent

:::zone pivot="python"

### LangGraph

See the [full sample](https://aka.ms/foundry-toolbox-langgraph) for the complete implementation.

**`.env` file**:

```
FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
TOOLBOX_NAME=agent-tools
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

**`main.py`** (key pattern):

```python
from langchain_azure_ai.tools import AzureAIProjectToolbox

toolbox = AzureAIProjectToolbox(toolbox_name=TOOLBOX_NAME)
tools = await toolbox.get_tools()
```


> [!IMPORTANT]
> Class `langchain_azure_ai.tools.AzureAIProjectToolbox` requires `langchain-azure-ai[tools]>1.2.3`.

### Microsoft Agent Framework

Use `MCPStreamableHTTPTool` from the Agent Framework SDK to connect directly to the toolbox MCP endpoint.

**`.env` file**:

```
FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

**`main.py`** (key pattern):

```python
# Auth: wrap token provider in an httpx.Auth subclass
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
http_client = httpx.AsyncClient(
    auth=_ToolboxAuth(token_provider),
    timeout=120.0,
)

# Toolbox MCP endpoint (platform-injected at runtime via TOOLBOX_ENDPOINT)
TOOLBOX_ENDPOINT = "https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1"

# Connect MCPStreamableHTTPTool to the toolbox endpoint
mcp_tool = MCPStreamableHTTPTool(
    name="toolbox",
    url=TOOLBOX_ENDPOINT,
    http_client=http_client,
    load_prompts=False,
)

agent = chat_client.as_agent(
    name="my-toolbox-agent",
    instructions="You are a helpful assistant with access to Foundry toolbox tools.",
    tools=[mcp_tool],
)
ResponsesAgentServerHost().run()
```

See the [full sample](https://aka.ms/foundry-toolbox-maf) for the complete implementation.

### Copilot SDK

Use the GitHub Copilot SDK to build a toolbox-powered agent that bridges Copilot's tool invocation to the Foundry toolbox MCP endpoint.

> [!NOTE]
> The Copilot SDK rejects tool names containing dots. The bridge automatically replaces `.` with `_` in tool names. For example, `myserver.get_info` becomes `myserver_get_info`.

**`.env` file**:

```
GITHUB_TOKEN=<your-github-token>
TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
```

**`agent.py`** (key pattern — MCP bridge):

```python
# 1. Open an MCP session to the toolbox endpoint
bridge = McpBridge(endpoint=TOOLBOX_ENDPOINT, token=_get_toolbox_token())
await bridge.initialize()
mcp_tools = await bridge.list_tools()

# 2. Map MCP tool list to Copilot SDK tool definitions
#    Dots in tool names are replaced with underscores (Copilot SDK requirement)
copilot_tools = [
    {
        "name": t["name"].replace(".", "_"),
        "description": t.get("description", ""),
        "parameters": t.get("inputSchema", {}),
    }
    for t in mcp_tools
]

# 3. Wire tool calls back to the MCP session
async def tool_handler(name: str, arguments: dict) -> str:
    return await bridge.call_tool(name.replace("_", ".", 1), arguments)

# 4. Run the Copilot SDK agent
agent = Agent(
    tools=copilot_tools,
    tool_handler=tool_handler,
    token=os.environ["GITHUB_TOKEN"],
)
```

<!-- TODO: Add link to full Copilot SDK sample when aka.ms/foundry-toolbox-copilotsdk is published -->

:::zone-end

:::zone pivot="dotnet"

### Microsoft Agent Framework

Use `ResponsesServer` from the Agent Framework SDK with a custom `ToolboxMcpClient` to discover and invoke toolbox tools through the MCP endpoint.

**Environment variables**:

```
AZURE_OPENAI_ENDPOINT=https://<account>.services.ai.azure.com
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
TOOLBOX_MCP_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
```

**`Program.cs`** (key pattern):

```csharp
using Azure.AI.AgentServer.Responses;
using Azure.AI.AgentServer.Responses.Models;
using Azure.AI.OpenAI;
using Azure.Identity;
using Microsoft.Extensions.DependencyInjection;
using OpenAI.Chat;

// Azure OpenAI endpoint and model deployment
var openAiEndpoint = "https://<account>.services.ai.azure.com";
var deployment = "gpt-4o";  // supports all toolbox tool types

// Toolbox MCP endpoint (platform-injected at runtime via TOOLBOX_MCP_ENDPOINT)
var toolboxEndpoint = "https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1";

// Azure OpenAI client
var credential = new DefaultAzureCredential();
var openAIClient = new AzureOpenAIClient(new Uri(openAiEndpoint), credential);
var chatClient = openAIClient.GetChatClient(deployment);

// Toolbox MCP client — discovers tools via tools/list, calls them via tools/call
var toolboxClient = new ToolboxMcpClient(toolboxEndpoint, credential);

ResponsesServer.Run<ToolboxHandler>(configure: builder =>
{
    builder.Services.AddSingleton(new AgentConfig(chatClient, toolboxClient));
});
```

`ToolboxMcpClient` wraps direct JSON-RPC calls to the MCP endpoint. `ToolboxHandler` connects LLM tool calls back to the MCP client by using a standard tool-calling loop. For the complete implementation of both classes, see the [full sample](https://github.com/microsoft/hosted-agents-vnext-private-preview/tree/main/samples/dotnet/toolbox/maf).

:::zone-end

:::zone pivot="rest-api"

> [!NOTE]
> Integration samples for this step are available for Python and .NET only.

:::zone-end

:::zone pivot="javascript"

> [!NOTE]
> Integration samples for this step are available for Python and .NET only.

:::zone-end

:::zone pivot="vscode"

Use the Microsoft Foundry Toolkit for Visual Studio Code extension to scaffold a Hosted agent sample that's already wired to your toolbox.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. On the **Toolboxes** tab, locate the toolbox you want to consume, and then select **Scaffold code template**.
1. In the Command Palette, choose a project folder when prompted.
1. Open the generated `README.md` and follow the setup, local run, and deployment steps for the scaffold.

The generated project includes the Hosted agent entry point, deployment files, and a `README.md` with the exact setup, run, and deployment steps.

If you want to integrate a toolbox into an existing hosted agent project instead of generating a new sample, use the copied endpoint from Step 2 with the Python or .NET patterns in this section.

:::zone-end

:::zone pivot="azd"

### Pass the toolbox endpoint to your agent

After you create the toolbox in [Step 1](#step-1-create-a-toolbox-version), retrieve its MCP endpoint by using `azd ai toolbox show` and pass that endpoint to your agent code as an environment variable. The agent reads the variable at startup and uses it to connect to the toolbox.

1. Get the toolbox endpoint:

   ```bash
   azd ai toolbox show <toolbox-name> --output json
   ```

    The `endpoint` field in the response identifies the selected version. Use it to test that version before promotion. For an agent that should follow `default_version`, construct the unversioned consumer endpoint shown in [Step 2](#step-2-get-the-toolbox-mcp-endpoint).    

1. Set the endpoint as an environment variable that your agent reads at startup:

   ```bash
   # .env (or however your runtime loads environment variables)
   TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/mcp?api-version=v1
   ```

1. In your agent code, read `TOOLBOX_ENDPOINT` and connect to it with an MCP client. Use the Python or .NET integration patterns earlier in this section as a reference for the client setup, and the Entra token (`https://ai.azure.com/.default` scope).

:::zone-end

### Handle tool approval requirements

The toolbox returns a `_meta.tool_configuration` object into every tool entry returned by `tools/list`. When a tool has `require_approval` set to `"always"`, the agent runtime must present the pending action to the user and wait for confirmation before invoking the tool. The MCP endpoint doesn't block `tools/call`. Enforcement is entirely the agent runtime's responsibility.

After your toolbox is created and tested, connect it to an agent. The integration pattern depends on the agent type:

- **Hosted agent** (your own code running in Foundry Agent Service): see [Use a toolbox with a hosted agent](use-toolbox-hosted-agent.md) for Agent Framework, LangGraph, Visual Studio Code, and Azure Developer CLI integration patterns and runtime approval requirements.

## Configure `require_approval` on a tool

Set `require_approval` when you create a toolbox version. The MCP tool examples in [Step 1](#step-1-create-a-toolbox-version) show both `"always"` and `"never"` values. You can also set it through the SDK:

:::zone pivot="python"

```python
from azure.ai.projects.models import MCPTool

# Set require_approval on an MCP tool
toolbox_version = project.toolboxes.create_toolbox_version(
    name="my-toolbox",
    tools=[
        MCPTool(
            server_label="myserver",
            server_url="https://your-mcp-server.example.com",
            require_approval="always",  # "always" | "never"
            project_connection_id="my-connection",
        )
    ],
)
```

:::zone-end

:::zone pivot="rest-api"

```json
{
  "tools": [
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com",
      "require_approval": "always",
      "project_connection_id": "my-connection"
    }
  ]
}
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool mcpTool = ProjectsAgentTool.AsProjectTool(ResponseTool.CreateMcpTool(
    serverLabel: "myserver",
    serverUri: new Uri("https://your-mcp-server.example.com"),
    toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
        GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval
    )
));
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "mcp",
    server_label: "myserver",
    server_url: "https://your-mcp-server.example.com",
    require_approval: "always",
    project_connection_id: "my-connection",
  },
];
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, REST API, or Azure Developer CLI tab to configure `require_approval` in your toolbox definition. The Microsoft Foundry Toolkit for Visual Studio Code extension workflow in this article focuses on creating and consuming the toolbox in Visual Studio Code.

:::zone-end

:::zone pivot="azd"

```yaml
resources:
  - kind: toolbox
    name: my-toolbox
    tools:
      - type: mcp
        server_label: myserver
        server_url: https://your-mcp-server.example.com
        require_approval: always
        project_connection_id: my-connection
```

:::zone-end

## Step 5: Manage toolbox versions

> [!NOTE]
> You can delete toolbox versions only through the Python SDK, .NET SDK, JavaScript SDK, and REST API. The Azure Developer CLI supports list, get, and publish (default-version promotion) operations.

Toolbox versions are immutable snapshots of a toolbox's tool configuration. Every call to the create endpoint produces a new `ToolboxVersionObject`. The parent `ToolboxObject` has a `default_version` field that controls which version the MCP endpoint serves. Creating a new version doesn't automatically promote it - you decide when to update `default_version`. This process lets you stage changes, test a new version independently, and promote it to production on your own schedule.

> [!NOTE]
> For the Azure Developer CLI, every mutating operation that targets the current default version &mdash; `azd ai toolbox connection add/remove` and `azd ai toolbox skill add/remove` &mdash; creates a **new** toolbox version that carries forward all previously attached connections and skills with the requested change applied. None of these commands automatically change `default_version`; run `azd ai toolbox publish <toolbox-name> <version>` when you're ready to make the new version active. To inspect a pending (non-default) version, use `azd ai toolbox show <name> --version <n>`.

| Object | Key fields | Description |
|--------|-----------|-------------|
| `ToolboxObject` | `id`, `name`, `default_version` | The toolbox container. `default_version` points to the active version. |
| `ToolboxVersionObject` | `id`, `name`, `version`, `description`, `created_at`, `tools[]`, `policies` | An immutable snapshot of the toolbox's tool list at a point in time. `policies.rai_config.rai_policy_name` specifies the optional guardrail applied to this version. |

### Create a new version

Each create call produces a new version. If the toolbox doesn't exist yet, the process automatically creates it. When you create the first version of a new toolbox, the default version is `v1` until you **manually** update to another version.

:::zone pivot="python"

```python
# Create a new toolbox version
toolbox_version = project.toolboxes.create_toolbox_version(
    name="my-toolbox",
    description="Updated tools v2",
    tools=[...],
)
print(f"Created version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "<toolbox-name>",
    tools: [tool],
    description: "Updated tools v2"
);
Console.WriteLine($"Created version: {toolboxVersion.Version}");
```

:::zone-end

:::zone pivot="rest-api"

```

POST {project_endpoint}/toolboxes/<toolbox-name>/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "Updated tools v2",
  "tools": [...]
}
```

:::zone-end

:::zone pivot="javascript"

```javascript
const toolboxVersion = await project.toolboxes.createVersion(
  "<toolbox-name>",
  [/* tools array */],
  { description: "Updated tools v2" },
);
console.log(`Created version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to create a new toolbox version. The Microsoft Foundry Toolkit for Visual Studio Code extension workflow in this article focuses on creating a toolbox and scaffolding a Hosted agent that consumes it.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with the Azure Developer CLI. To create a toolbox version, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end

The response is a `ToolboxVersionObject` containing the new `version` identifier.

### List versions

:::zone pivot="python"

```python
# List all toolbox versions
versions = list(project.toolboxes.list_toolbox_versions(name="<toolbox-name>"))
for v in versions:
    print(f"{v.version} — created {v.created_at}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
List<ToolboxVersion> versions = await toolboxClient
    .GetToolboxVersionsAsync("<toolbox-name>")
    .ToListAsync();
Console.WriteLine($"Found {versions.Count} toolbox version(s).");
foreach (ToolboxVersion v in versions)
{
    Console.WriteLine($"  - {v.Name} ({v.Version})");
}
```

:::zone-end

:::zone pivot="rest-api"

```http
GET {project_endpoint}/toolboxes/<toolbox-name>/versions?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
const versions = project.toolboxes.listVersions("<toolbox-name>");
for await (const v of versions) {
  console.log(`${v.version} — created ${v.created_at}`);
}
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to list toolbox versions.

:::zone-end

:::zone pivot="azd"

```bash
# The current default version is marked with *
azd ai toolbox version list <toolbox-name>
```

:::zone-end

### Get a specific version

:::zone pivot="python"

```python
# Get a specific toolbox version
version_obj = project.toolboxes.get_toolbox_version(
    toolbox_name="<toolbox-name>",
    version="<version_id>",
)
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxVersion versionObj = await toolboxClient.GetToolboxVersionAsync(
    "<toolbox-name>",
    "<version_id>"
);
Console.WriteLine($"Retrieved toolbox: {versionObj.Name} ({versionObj.Id})");
```

:::zone-end

:::zone pivot="rest-api"

```http
GET {project_endpoint}/toolboxes/<toolbox-name>/versions/{version}?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
const versionObj = await project.toolboxes.getVersion(
  "<toolbox-name>",
  "<version_id>",
);
console.log(`Retrieved version: ${versionObj.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to get a specific toolbox version.

:::zone-end

:::zone pivot="azd"

```bash
azd ai toolbox version get <toolbox-name> <version_id>
```

:::zone-end

### Promote a version to default

The MCP endpoint always serves the `default_version`. To switch which version is active, update the toolbox:

:::zone pivot="python"

```python
# Promote a version to default
toolbox = project.toolboxes.update(
    toolbox_name="<toolbox-name>",
    default_version="<version_id>",
)
print(f"Active version: {toolbox.default_version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxRecord record = await toolboxClient.UpdateToolboxAsync(
    "<toolbox-name>",
    "<version_id>"
);
Console.WriteLine($"Active version: {record.DefaultVersion}");
```

:::zone-end

:::zone pivot="rest-api"

```http
PATCH {project_endpoint}/toolboxes/<toolbox-name>?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "default_version": "<version_id>"
}
```

`default_version` can't be empty. Replace it with a new version. 
:::zone-end

:::zone pivot="javascript"

```javascript
const toolbox = await project.toolboxes.update(
  "<toolbox-name>",
  "<version_id>",
);
console.log(`Active version: ${toolbox.default_version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to promote a toolbox version to default.

:::zone-end

:::zone pivot="azd"

Toolbox versions are immutable. Use `publish` to make any existing version the new default:

```bash
# Roll back or forward to a specific version
azd ai toolbox publish <toolbox-name> <version_id> --no-prompt
```

`publish` is the only path that changes `default_version` from the CLI; mutating verbs (`connection add/remove`, `skill add/remove`) always create a new version without promoting it.

:::zone-end

### Delete a version

:::zone pivot="python"

```python
# Delete a toolbox version
project.toolboxes.delete_toolbox_version(
    toolbox_name="<toolbox-name>",
    version="<version_id>",
)
```

:::zone-end

:::zone pivot="dotnet"

```csharp
await toolboxClient.DeleteToolboxVersionAsync(
    "<toolbox-name>",
    "<version_id>"
);
```

:::zone-end

:::zone pivot="rest-api"

```http
DELETE {project_endpoint}/toolboxes/<toolbox-name>/versions/{version}?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
await project.toolboxes.deleteVersion(
  "<toolbox-name>",
  "<version_id>",
);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to delete a toolbox version.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with the Azure Developer CLI. To delete a toolbox version, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end


## Configure tools

Choose the tool type and authentication pattern that match your scenario. Select the tab for your preferred SDK or deployment method.

Each tool's **azd** tab below shows declarative toolbox YAML. To create a toolbox imperatively without an agent project, use the [generic four-step `azd ai toolbox create --from-file` workflow](#step-1-create-a-toolbox-version) and apply the per-tool data shown in the following sections. To deploy a toolbox with a hosted agent, model it as an `azure.ai.toolbox` service in `azure.yaml` and wire the agent to it with `uses:` or `toolboxes:`.

### Multiple tool types

A single toolbox can bundle different tool types. The following example combines Web Search, Azure AI Search, and an MCP server in one toolbox:

```json
{
  "description": "Web search, knowledge base search, and custom MCP server",
  "tools": [
    {
      "type": "web_search",
      "description": "Search the web for current information"
    },
    {
      "type": "azure_ai_search",
      "name": "my_aisearch",
      "description": "Search internal product documentation",
      "azure_ai_search": {
        "indexes": [
          {
            "index_name": "<INDEX_NAME>",
            "project_connection_id": "<CONNECTION_NAME>"
          }
        ]
      }
    },
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com",
      "require_approval": "never",
      "project_connection_id": "my-key-auth-connection"
    }
  ]
}
```

> [!NOTE]
> Each tool type (`web_search`, `azure_ai_search`, `code_interpreter`, `file_search`) can appear at most once without a `name` field. To include multiple instances of the same type, set a unique `name` on each instance - see the next example.

#### Multi-tool restrictions

You can include at most one instance of each built-in tool type without a `name` field in a toolbox. If you include two instances of the same type without a `name`, the API returns:

```
400 invalid_payload: Multiple tools without identifiers found...
```

### Two instances of the same tool type

Use the `name` field to include multiple instances of the same tool type in one toolbox. Each named instance is treated as a separate tool and must have a unique name.

```json
{
  "description": "Two Azure AI Search indexes in a single toolbox",
  "tools": [
    {
      "type": "azure_ai_search",
      "name": "product-search",
      "description": "Search product catalog and specifications",
      "azure_ai_search": {
        "indexes": [
          {
            "index_name": "<PRODUCT_INDEX_NAME>",
            "project_connection_id": "<PRODUCT_CONNECTION_NAME>"
          }
        ]
      }
    },
    {
      "type": "azure_ai_search",
      "name": "support-search",
      "description": "Search support tickets and troubleshooting guides",
      "azure_ai_search": {
        "indexes": [
          {
            "index_name": "<SUPPORT_INDEX_NAME>",
            "project_connection_id": "<SUPPORT_CONNECTION_NAME>"
          }
        ]
      }
    }
  ]
}
```

Each tool type has its own toolbox configuration - connection authentication types, per-language SDK snippets, and any toolbox-specific behavior. Those details live in each tool's reference article. See the [Feature support](#feature-support) table for a link to each tool.

For toolbox-specific behavior - such as File Search dynamic vector store (parameter override) or resource-level file uploads for Code Interpreter and File Search - see the linked article for each tool.


## Troubleshoot

| Symptom | Likely cause | Fix |
| ------- | ------------ | --- |
| `tools/list` returns zero tools for MCP or A2A tools | Invalid or missing connection credentials for the remote MCP server or A2A agent. The toolbox can't retrieve tool manifests from the remote endpoint without valid auth. | Verify the `project_connection_id` exists in your Foundry project and the credentials are correct. Try connecting to the MCP server directly to test the auth setup. If using managed identity (PMI, agent identity, or MI), verify the correct RBAC role assignments for the caller on the target resource. |
| `tools/list` returns zero tools for OpenAPI tools | Invalid OpenAPI spec. The toolbox constructs the tool manifest from the spec, which fails if the spec is malformed. | Validate your OpenAPI spec content. Check that it conforms to OpenAPI 3.0 or 3.1 and includes valid `paths`, `operationId` values, and parameter schemas. If using managed identity auth, also verify RBAC role assignments on the target service. |
| `tools/list` returns fewer tools than expected | The `allowed_tools` filter contains incorrect or misspelled tool names. Tool names are case-sensitive and must follow the [MCP specification for tool names](https://modelcontextprotocol.io/specification/2025-03-26/server/tools) (no whitespace or special characters). | Remove `allowed_tools` temporarily and call `tools/list` to get the full tool list. Use the exact names from the response to set values for `allowed_tools`. |
| `tools/list` returns zero tools (other tool types) | Toolbox not fully provisioned or tool type unsupported in region. For built-in tools (Web Search, AI Search, Code Interpreter, File Search), tool manifests are constructed server-side and don't require auth — if they return empty, the toolbox version might not be provisioned yet. | Wait 10 seconds and retry. |
| `400 Multiple tools without identifiers` | Two unnamed tool types in one toolbox | Keep at most one unnamed type; add `server_label` to all MCP tools. |
| `CONSENT_REQUIRED` (code `-32006`) | OAuth connection requires user consent | Open the consent URL in a browser and complete the OAuth flow, then retry. |
| `401` on MCP calls | Expired token or wrong scope | Use scope `https://ai.azure.com/.default` and refresh the token. |
| Tool names not matching | MCP tool names are prefixed with `server_label` | Use `{server_label}.{tool_name}` format (for example, `myserver.get_info`). |
| `500` on `send_ping()` | Toolbox MCP server doesn't implement the MCP `ping` method. | Don't call `send_ping()`. If your framework calls it automatically (for example, Microsoft Agent Framework's `MCPStreamableHTTPTool._ensure_connected()`), disable the ping check or override the method with a no-op. |
| `500` on `prompts/list` | The Foundry MCP server doesn't implement `prompts/list`. | Pass `load_prompts=False` (or equivalent) to your MCP client constructor. |
| `500` with non-streaming `tools/call` | Non-streaming mode (`stream=False`) isn't supported for toolbox MCP endpoints. | Always use `stream=True` when calling toolbox MCP tools. |
| `500` on `tools/list` | Transient server error | Retry after a few seconds. |
| Environment variables overwritten at runtime | The platform reserves all environment variables prefixed with `FOUNDRY_` and might silently overwrite user-defined values. | Rename custom environment variables to avoid the `FOUNDRY_` prefix (for example, use `TOOLBOX_MCP_ENDPOINT` instead of `FOUNDRY_TOOLBOX_ENDPOINT`). |

## Configure guardrails

Apply a named [guardrail policy](../../../guardrails/guardrails-overview.md) to a toolbox version to enforce responsible AI content filtering on tool inputs and outputs. The guardrail runs at the toolbox layer, independently of any model-level content filter.

Reference a guardrail by its policy name, which you configure in the Foundry portal under **Guardrails**. Set `policies.rai_config.rai_policy_name` to the name of the policy when creating a toolbox version.

:::zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import WebSearchTool

endpoint = "https://<your-foundry-account>.services.ai.azure.com/api/projects/<your-project>"
project = AIProjectClient(endpoint=endpoint, credential=DefaultAzureCredential())

toolbox_version = project.beta.toolboxes.create_version(
    name="my-toolbox",
    description="Toolbox with guardrail",
    tools=[WebSearchTool()],
    policies={
        "rai_config": {
            "rai_policy_name": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/raiPolicies/<policy-name>"
        }
    },
)
print(f"Created version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="rest-api"

```http
POST {endpoint}/toolboxes/{toolbox_name}/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "Toolbox with guardrail",
  "tools": [{ "type": "web_search" }],
  "policies": {
    "rai_config": {
      "rai_policy_name": "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/raiPolicies/<policy-name>"
    }
  }
}
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
using Azure.AI.Projects;
using Azure.AI.Projects.Agents;
using Azure.Identity;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
DefaultAzureCredential credential = new();
AIProjectClient projectClient = new(endpoint: new Uri(projectEndpoint), tokenProvider: credential);
AgentToolboxes toolboxClient = projectClient.AgentAdministrationClient.GetAgentToolboxes();

var toolboxVersion = toolboxClient.CreateToolboxVersion(
    toolboxName: "my-toolbox",
    description: "Toolbox with guardrail",
    tools: [new WebSearchTool()],
    policies: new ToolboxPolicies
    {
        RaiConfig = new RaiConfig { RaiPolicyName = "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/raiPolicies/<policy-name>" }
    });
Console.WriteLine($"Created version: {toolboxVersion.Version}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const toolboxVersion = await project.beta.toolboxes.createVersion(
  "my-toolbox",
  [{ type: "web_search" }],
  {
    description: "Toolbox with guardrail",
    policies: {
      rai_config: {
        rai_policy_name: "/subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/raiPolicies/<policy-name>",
      },
    },
  },
);
console.log(`Created version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="azd"

```yaml
name: my-toolbox
description: Toolbox with guardrail
policies:
  rai_config:
    rai_policy_name: /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<account-name>/raiPolicies/<policy-name>
tools:
  - type: web_search
```

:::zone-end

:::zone pivot="vscode"

Guardrail configuration isn't yet available in the VS Code extension. Use the REST API, SDK, or Azure Developer CLI to configure guardrails.

:::zone-end

## Attach skills to a toolbox

Attach [skills](skills.md) to a toolbox version to make them available to agents through the toolbox MCP endpoint. Each skill reference specifies the skill name and an optional version. Omit `version` to use the skill's `default_version`; pin a `version` string to use an immutable snapshot.

A toolbox version can contain tools, skills, or both. The following examples create a toolbox version that contains a single skill reference. To add skills to a toolbox that already has tools, include the same `tools` you used in [Step 1](#step-1-create-a-toolbox-version) along with the `skills` array.

> [!IMPORTANT]
> Skills attached to a toolbox must exist in the same Foundry project. Cross-project references aren't supported.

When an agent or MCP client connects to the toolbox endpoint, skills are exposed as [MCP Resources](https://modelcontextprotocol.io/docs/concepts/resources). The MCP client or agent framework must support the MCP Resources protocol to auto-discover and load skills. To verify that skills are discoverable, call `resources/list` on the toolbox MCP endpoint and confirm your skill names appear in the response.

:::zone pivot="rest-api"

```http
POST {endpoint}/toolboxes/{toolbox_name}/versions?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Accept: application/json
Foundry-Features: Skills=V1Preview

{
  "description": "Toolbox with a skill reference",
  "tools": [],
  "skills": [
    {
      "type": "skill_reference",
      "name": "greeting"
    }
  ]
}
```

To pin a specific version:

```json
{
  "skills": [
    {
      "type": "skill_reference",
      "name": "greeting",
      "version": "v1"
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import ToolboxSkillReference

toolbox_version = project.beta.toolboxes.create_version(
    name="my-toolbox",
    description="Toolbox with a skill reference",
    tools=[],
    skills=[
        ToolboxSkillReference(name="greeting"),              # use default version
        # ToolboxSkillReference(name="greeting", version="v1"),  # pin to v1
    ],
)
print(f"Created toolbox version: {toolbox_version.id}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
#pragma warning disable AAIP001
// Reuse the AgentToolboxes client (toolboxClient) from Step 1.
ToolboxSkillReference skillRef = new("greeting");
// To pin a version: new ToolboxSkillReference("greeting") { Version = "v1" }

ToolboxVersion toolboxVersion = toolboxClient.CreateToolboxVersion(
    name: "my-toolbox",
    tools: [],
    skills: [skillRef],
    description: "Toolbox with a skill reference"
);
Console.WriteLine($"Created toolbox version: {toolboxVersion.Id}");
```

:::zone-end

:::zone pivot="javascript"

```javascript
const toolboxVersion = await project.beta.toolboxes.createVersion(
  "my-toolbox",
  [],
  {
    description: "Toolbox with a skill reference",
    skills: [
      { type: "skill_reference", name: "greeting" },
      // { type: "skill_reference", name: "greeting", version: "v1" },  // pin to v1
    ],
  },
);
console.log(`Created toolbox version: ${toolboxVersion.id}`);
```

:::zone-end

:::zone pivot="azd"

The Azure Developer CLI supports skill references in two places: declaratively as a top-level `skills:` block in the `azd ai toolbox create --from-file` YAML, and imperatively with the `azd ai toolbox skill add/list/remove` verbs. Each reference takes a `name` (required) and an optional `version` (string). Omit `version` to follow the skill's `default_version`; pin a version string to lock the toolbox to an immutable snapshot.

**Declare skills when you create the toolbox**

```yaml
# my-toolbox.yaml
description: Toolbox with skill references
connections:
  - name: my-gh-conn
skills:
  - name: greeting              # follows the skill's default version
  - name: review-checklist
    version: "2"               # pin to skill version 2
```

```bash
azd ai toolbox create my-toolbox --from-file ./my-toolbox.yaml --no-prompt
```

**Add, list, and remove skills on an existing toolbox**

```bash
# Add a skill (follows default version)
azd ai toolbox skill add my-toolbox greeting

# Add a skill pinned to a specific version
azd ai toolbox skill add my-toolbox review-checklist@2

# Add multiple skills from a file (same shape as the create YAML's skills block)
azd ai toolbox skill add my-toolbox --from-file ./skills.yaml

# List skill references on the current default version
azd ai toolbox skill list my-toolbox --output table

# Remove a skill (--force skips the confirmation prompt; multiple names allowed)
azd ai toolbox skill remove my-toolbox greeting --force
```

`skill list` shows only the default version. Pinned skills show their version; unpinned skills show `(default)`. To inspect skills on a pending version, run `azd ai toolbox show <toolbox> --version <n> --output json` and read the `skills` array.

> [!IMPORTANT]
> `skill add` and `skill remove` each create a new toolbox version that carries forward every previously attached connection and skill with the requested change applied. **They don't promote the new version to default**, so changes aren't visible to MCP clients until you run `azd ai toolbox publish <toolbox> <version>`. To change the pinned version of a skill that's already attached &mdash; for example, upgrade `greeting` from v1 to v2 &mdash; run three commands in order: `skill remove`, `publish` the new version, then `skill add <name>@<new-version>` (`skill add` blocks duplicates when checked against the current default version).

Skill names must match `^[a-z0-9]([a-z0-9\-]*[a-z0-9])?$` (lowercase letters, digits, and hyphens; max 64 characters; no leading or trailing hyphen). A trailing `@` in `<name>@<version>` (an empty version) is rejected.

:::zone-end

:::zone pivot="vscode"

Skill references aren't currently configurable through the VS Code extension. Use the REST API or SDK to configure skills.

:::zone-end

:::zone pivot="python"

### Validate skill discovery

After attaching skills to a toolbox version, verify that you can discover them through the toolbox MCP endpoint by using the MCP Python SDK:

```python
import asyncio
from azure.identity import DefaultAzureCredential
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def list_skills():
    credential = DefaultAzureCredential()
    token = credential.get_token("https://ai.azure.com/.default").token
    toolbox_url = "{endpoint}/toolboxes/my-toolbox/mcp?api-version=v1"
    headers = {
        "Authorization": f"Bearer {token}",
    }
    async with streamablehttp_client(toolbox_url, headers=headers) as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"Skill: {resource.uri} - {resource.name}")

asyncio.run(list_skills())
```

Skills appear as MCP resources with URIs in the format `skill://{name}`.

:::zone-end

:::zone pivot="dotnet"

### Consume skills from an agent (Microsoft Agent Framework, .NET)

In .NET, use `AgentSkillsProviderBuilder().UseMcpSkills(mcpClient)` from the Microsoft Agent Framework SDK to discover MCP-based skills from a toolbox endpoint and inject them as `AIContextProviders` on the agent. The agent then loads each skill's instructions at runtime when the model decides it's relevant. The following `Program.cs` hosts the agent with the Responses hosting layer (`AddFoundryResponses` and `MapFoundryResponses`).

```csharp
using System.Net.Http.Headers;
using Azure.AI.Projects;
using Azure.Core;
using Azure.Identity;
using DotNetEnv;
using Microsoft.Agents.AI;
using Microsoft.Agents.AI.Foundry.Hosting;
using Microsoft.Extensions.AI;
using ModelContextProtocol.Client;

// Load .env file if present (for local development).
Env.TraversePath().Load();

string projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT")
    ?? throw new InvalidOperationException("FOUNDRY_PROJECT_ENDPOINT environment variable is not set.");

string deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("AZURE_AI_MODEL_DEPLOYMENT_NAME environment variable is not set.");

string toolboxName = Environment.GetEnvironmentVariable("TOOLBOX_NAME")
    ?? throw new InvalidOperationException("TOOLBOX_NAME environment variable is not set.");

// Build the Foundry Toolbox MCP URL from the project endpoint and toolbox name.
string toolboxMcpServerUrl = $"{projectEndpoint.TrimEnd('/')}/toolboxes/{toolboxName}/mcp?api-version=v1";

TokenCredential credential = new DefaultAzureCredential();

// HttpClient that attaches a fresh Foundry bearer token to every request.
// CheckCertificateRevocationList = true satisfies CA5399.
using var httpClient = new HttpClient(
    new BearerTokenHandler(credential, "https://ai.azure.com/.default")
    {
        CheckCertificateRevocationList = true,
    });

Console.WriteLine($"Connecting to Foundry Toolbox '{toolboxName}' MCP server...");

// Connect to the Foundry Toolbox MCP endpoint.
// The Foundry-Features: Toolboxes=V1Preview opt-in header is required while the
// toolbox MCP surface is in preview.
await using var mcpClient = await McpClient.CreateAsync(
    new HttpClientTransport(
        new HttpClientTransportOptions
        {
            Endpoint = new Uri(toolboxMcpServerUrl),
            Name = toolboxName,
            TransportMode = HttpTransportMode.StreamableHttp,
        },
        httpClient));

// AgentSkillsProvider implements progressive disclosure over the MCP-discovered skills:
// names and descriptions are advertised in the system prompt, and the full skill body
// (and any supplementary resources) is loaded on demand when the model decides it is
// relevant.
var skillsProvider = new AgentSkillsProviderBuilder()
    .UseMcpSkills(mcpClient)
    .Build();

AIAgent agent = new AIProjectClient(new Uri(projectEndpoint), credential)
    .AsAIAgent(new ChatClientAgentOptions
    {
        Name = "foundry-toolbox-mcp-skills",
        Description = "Agent that discovers MCP-based skills from a Foundry Toolbox and exposes them via AgentSkillsProvider.",
        ChatOptions = new ChatOptions
        {
            ModelId = deployment,
            Instructions = "You are a helpful assistant.",
        },
        AIContextProviders = [skillsProvider],
    });

var builder = AgentHost.CreateBuilder(args);
builder.Services.AddFoundryResponses(agent);
builder.RegisterProtocol("responses", endpoints => endpoints.MapFoundryResponses());

var app = builder.Build();
app.Run();

// HttpClientHandler that attaches a fresh Foundry bearer token to every outgoing request.
internal sealed class BearerTokenHandler(TokenCredential credential, string scope) : HttpClientHandler
{
    private readonly TokenRequestContext _tokenContext = new([scope]);

    protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        AccessToken token = await credential.GetTokenAsync(this._tokenContext, cancellationToken).ConfigureAwait(false);
        request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token.Token);
        return await base.SendAsync(request, cancellationToken).ConfigureAwait(false);
    }
}
```

For the complete sample, including project files and deployment steps, see the [Skills in Toolbox sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/csharp/hosted-agents/agent-framework/foundry-toolbox-mcp-skills).

:::zone-end

### Reminder

The `reminder_preview` tool enables a hosted agent to schedule *itself* to run again at a future time. When the agent calls this tool, it specifies a delay in minutes. After that delay, Foundry re-invokes the same agent on the same conversation.

:::image type="content" source="../../media/routines/toolbox-reminder-tool.png" alt-text="Screenshot showing the reminder_preview tool in a toolbox in the Foundry portal.":::

> [!NOTE]
> The reminder tool is available only for hosted agents. You can't use the reminder tool with prompt agents.

For full setup instructions, usage examples, and limitations, see [Reminder tool for self-scheduling agents](reminder-tool.md).

## Region and model compatibility

Toolbox availability depends on two factors beyond the project region:

- **Region**: Some tool types aren't available in every region that supports the agent service. For example, a region that supports the toolbox endpoint might not support all built-in tool types.

Before deploying a toolbox, verify that your target region supports the tool types you plan to use. For the full compatibility tables, see [Tool support by region and model](../../concepts/limits-quotas-regions.md#tool-support-by-region-and-model).

## Related content

- [Connect agents to Model Context Protocol servers](model-context-protocol.md)
- [Add MCP server authentication](../mcp-authentication.md)
- [Web search tool](web-search.md)
- [Azure AI Search tool](ai-search.md)
- [Guardrails overview](../../../guardrails/guardrails-overview.md)
- [Manage skills](skills.md)
- [Deploy a Hosted agent](../deploy-hosted-agent.md)
- [Add a connection to your project](../../../how-to/connections-add.md)
- [Configure network isolation for Microsoft Foundry](../../../how-to/configure-private-link.md)
