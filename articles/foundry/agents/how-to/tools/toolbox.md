---
title: "Curate intent-based toolbox in Foundry (preview)"
description: "Use toolbox in Microsoft Foundry to add MCP servers, web search, Azure AI Search, file search, code interpreter tool and more to hosted agents through a single managed endpoint."
author: alvinashcraft
ms.author: aashcraft
ms.reviewer: zhuoqunli
ms.date: 04/21/2026
ms.manager: nitinme
ms.topic: how-to
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.custom: dev-focus
ai-usage: ai-assisted
zone_pivot_groups: selection-foundry-toolbox
---

# Curate intent-based toolbox in Foundry (preview)
[!INCLUDE [feature-preview](../../../includes/feature-preview.md)]

A single agent can depend on multiple tools — APIs, MCP servers, connectors, and flows — each with its own authentication model and owning team. As you scale across an organization, teams re-implement the same tools independently, credentials get duplicated, governance becomes inconsistent, and there's little visibility into what tools exist or who's using them. Developers stall, not because the models aren't capable, but because tool integration has become the bottleneck.

:::image type="content" source="../../media/tools/toolbox/toolbox-before.png" alt-text="Diagram showing multiple agents each wiring their own tools with different authentication models and duplicated credentials." lightbox="../../media/tools/toolbox/toolbox-before.png":::

Enterprises already have the infrastructure: gateways, credential vaults, policies, and observability. What's been missing is a developer experience that packages this infrastructure into something reusable, discoverable, and governed by default.

Toolbox provides that experience. Define a curated set of tools once, manage them centrally in Foundry, and expose them through a single MCP-compatible endpoint that any agent can consume. The platform handles credential injection, token refresh, and enterprise policy enforcement at runtime.

Toolbox covers the full tool lifecycle through four pillars - **Build** and **Consume** are available today:

| Pillar | Status | What it enables |
| ------ | ------ | --------------- |
| **Build** | Available today | Select tools, configure authentication centrally, and publish a reusable toolbox that any team can consume. |
| **Consume** | Available today | Connect any agent to a single MCP-compatible endpoint to dynamically discover and invoke all tools in the toolbox. |

:::image type="content" source="../../media/tools/toolbox/toolbox-architecture.png" alt-text="Diagram showing Toolboxes in Foundry architecture: Build and Consume pillars consumed by LangGraph, Microsoft Agent Framework, GitHub Copilot, Claude Code, and Microsoft Copilot Studio, governed by default." lightbox="../../media/tools/toolbox/toolbox-architecture.png":::

You create toolboxes in Foundry, but the consumption surface is open. Any MCP-compatible agent runtime or client can use a toolbox — including agents built with any framework, MCP-enabled IDEs, and custom code.

Because a toolbox is a managed resource, you can add, remove, or reconfigure tools without changing code in your agent. Your agent always connects to a single endpoint. Toolbox versioning gives you explicit control over when changes take effect — create and test a new version, then promote it to default when you're ready. Every agent that points to the toolbox picks up the promoted version automatically, with no code changes and no redeployment.

In this article, you learn how to:

- Create a toolbox with one or more tools.
- Get the toolbox MCP endpoint.
- Verify that tools load correctly.
- Integrate a toolbox into your hosted agent.
- Manage toolbox versions and promote a version to default.

For tool configuration syntax and authentication options for each tool type, see [Configure tools](#configure-tools).

## Feature support

| Feature | Python SDK | REST API | .NET SDK | JavaScript SDK | azd (deploy) |
| ------- | ---------- | -------- | -------- | -------------- | ------------ |
| Toolbox update, list, get, and delete | ✔️ | ✔️ | ✔️ | ✔️ | N/A |
| Toolbox version create | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| Toolbox version list, get, and delete | ✔️ | ✔️ | ✔️ | ✔️ | N/A |
| [MCP tool](model-context-protocol.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [Web Search tool](web-search.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [Azure AI Search tool](ai-search.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [Code Interpreter tool](code-interpreter.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [File Search tool](file-search.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [OpenAPI tool](openapi.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |
| [Agent-to-Agent (A2A) tool](agent-to-agent.md) | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Grant the **Azure AI User** role on the Foundry project to each identity that applies to your scenario:
  - **Developer** (always required) — the identity that creates, updates, and manages toolbox versions.
  - **Agent identity** (required if using a hosted agent) — the agent's managed identity that calls tools at runtime.
  - **End user** (required only for OAuth flows) — any user whose identity is proxied through OAuth or UserEntraToken connections (for example, OAuth-based MCP or 1P OBO flows).
- Your Foundry project needs to be at one of the supported [regions](../../concepts/limits-quotas-regions.md#supported-regions).
- [Visual Studio Code](https://code.visualstudio.com/).
- [Microsoft Foundry Toolkit for Visual Studio Code extension](https://aka.ms/foundrytk) and the pre-release **Foundry** extension. Toolbox support in Foundry Toolkit is currently in preview and is only available in pre-release versions.
- **Python SDK**: `pip install azure-ai-projects azure-identity`
- **.NET SDK**: `dotnet add package Azure.AI.Projects --prerelease` and `dotnet add package Azure.Identity`
- **JavaScript SDK**: `npm install @azure/ai-projects @azure/identity`
- **azd (deploy)**: [Install the Azure Developer CLI](/azure/developer/azure-developer-cli/install-azd) and the agent extension: `azd extension install azure.ai.agents`

> [!IMPORTANT]
> - A toolbox supports at most **one tool without a `name` field per tool type** (Web Search, Azure AI Search, Code Interpreter, File Search). To include more than one instance of the same tool type, set a unique `name` on each instance to differentiate them. Including two instances of the same type without a `name` returns an `invalid_payload` error. For details, see [Multiple tool types](#multiple-tool-types).
> - Add a `description` to every tool in your toolbox to help the model select the right tool for each request.
> - Carefully review each tool's documentation to learn more about individual tool setup, limitations, and warnings.

## Step 1: Create a toolbox version

Create a toolbox version based on the tools you need.

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool, WebSearchTool

client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

toolbox_version = client.beta.toolboxes.create_toolbox_version(
    toolbox_name="my-toolbox",
    description="Toolbox with web search and an MCP server",
    tools=[
        WebSearchTool(),
        MCPTool(
            server_label="myserver",
            server_url="https://your-mcp-server.example.com",
            require_approval="never",
            project_connection_id="my-key-auth-connection",
        ),
    ],
)
print(f"Created toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
using Azure.Identity;
using Azure.AI.Projects;

var projectEndpoint = Environment.GetEnvironmentVariable("FOUNDRY_PROJECT_ENDPOINT");
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

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [webTool, mcpTool],
    description: "Toolbox with web search and an MCP server"
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
  "description": "Toolbox with web search and an MCP server",
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

const projectEndpoint = process.env["FOUNDRY_PROJECT_ENDPOINT"] || "<project endpoint>";

const project = new AIProjectClient(projectEndpoint, new DefaultAzureCredential());

const toolboxVersion = await project.beta.toolboxes.createVersion(
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
  ],
  {
    description: "Toolbox with web search and an MCP server",
  },
);
console.log(`Created toolbox: ${toolboxVersion.name}, version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use Foundry Toolkit in Visual Studio Code to create and publish a toolbox
from the **Tools** view.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. Select the **+ Add Toolbox** icon.
1. On the **Build a Custom Toolbox** tab, enter the toolbox name and
  description, add the tools you want, and then select **Publish**.

Publishing a new toolbox creates its first version. That version becomes
the default version automatically.

:::image type="content" source="../../media/tools/toolbox/toolbox-vscode-create.png" alt-text="Screenshot of Foundry Toolkit in Visual Studio Code showing the Build a Custom Toolbox view with fields for the toolbox name, description, and tools, plus the Publish action." lightbox="../../media/tools/toolbox/toolbox-vscode-create.png":::

:::zone-end

:::zone pivot="azd"

By using `azd`, you declare toolbox resources in an `agent.yaml` file instead of calling the SDK. Define your tools in the `resources` section and deploy by using `azd ai agent init`. For `agent.yaml` examples for each tool type, see [Configure tools](#configure-tools). For the full deployment workflow, see [Deploy with azd](#deploy-with-azd).

> [!IMPORTANT] 
> The `-m` (or `--manifest`) flag is **required** for `azd ai agent init`.
> It tells the command where to find your agent definition and source files.
>
> `-m` can point to either:
> - **A specific `agent.yaml` file** — init copies all files from the same directory as the manifest
> - **A folder containing `agent.yaml`** — init copies all files from that folder
>
> All files in the manifest directory (main.py, Dockerfile, requirements.txt, setup.py, and so on)
> are copied into the scaffolded project under `src/<agent-name>/`.

```powershell
# 1. Create a manifest directory with your agent.yaml + source files
mkdir my-agent/manifest
# Copy agent.yaml, main.py, Dockerfile, requirements.txt into my-agent/manifest/

# 2. Initialize the azd project (note: -m is REQUIRED)
cd my-agent
$PROJECT_ID = "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
azd ai agent init -m https://github.com/microsoft/hosted-agents-vnext-private-preview/main/samples/python/toolbox/azd/agent.yaml --project-id $PROJECT_ID -e my-env
# Or equivalently: azd ai agent init -m manifest/ --project-id $PROJECT_ID -e my-env
# ↑ If your agent.yaml declares {{ param }} secrets (e.g., github_pat), you will be prompted to enter
#   them interactively HERE — before init completes. This is the only safe time to supply credentials.
# NOTE: Do NOT use --no-prompt here — it skips the prompt and leaves {{ param }} credentials empty (see Troubleshooting: Credentials Empty with --no-prompt)

# 3. CRITICAL post-init fixes (see "Post-Init Checklist" below)
azd env set enableHostedAgentVNext "true" -e my-env
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "gpt-4o" -e my-env  # must match the deployment name in azure.yaml

# 4. Provision infrastructure (creates connections via Bicep)
azd provision -e my-env

# 5. Deploy agent (creates toolboxes, container image, agent version)
azd deploy -e my-env

# 6. Invoke the agent (MUST run from the scaffolded project directory)
azd ai agent invoke --new-session "tell me about the latest news in Microsoft Foundry" --timeout 120
```

Agent.yaml:
```yaml
kind: hosted
name: toolbox-azd-test
description: LangGraph agent wired for toolbox MCP.
metadata:
  tags:
    - AI Agent Hosting
    - LangGraph

# template: contains the ContainerAgent definition (kind: hosted).
# These fields are used to generate src/<agent>/agent.yaml during init.
template:
  kind: hosted
  protocols:
    - protocol: responses
      version: 1.0.0
  environment_variables:
    # FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_AGENT_TOOLBOX_* are injected
    # automatically by the platform at runtime — do NOT declare them here.
    - name: AZURE_OPENAI_ENDPOINT
      value: ${AZURE_OPENAI_ENDPOINT}
    - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
      value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o}
    - name: TOOLBOX_NAME
      value: ${TOOLBOX_NAME=agent-tools}

# parameters: secret values prompted at init time (or set via azd env).
# azd uppercases the param name to find the env var: github_pat → GITHUB_PAT.
parameters:
  github_pat:
    secret: true
    description: GitHub Personal Access Token (classic ghp_... or fine-grained github_pat_...)

# resources: connections and toolboxes scaffolded into azure.yaml by azd ai agent init.
resources:
  - kind: connection
    name: github-mcp-conn
    target: https://api.githubcopilot.com/mcp
    category: remoteTool
    credentials:
      type: CustomKeys
      keys:
        Authorization: "Bearer {{ github_pat }}"

  - kind: toolbox
    name: agent-tools
    tools:
      - type: web_search
      - type: mcp
        server_label: github
        server_url: https://api.githubcopilot.com/mcp
        project_connection_id: github-mcp-conn
```

:::zone-end

## Step 2: Get the toolbox MCP endpoint

Two endpoint patterns exist depending on your role:

| Role | Endpoint | When to use |
| ---- | -------- | ----------- |
| **Toolbox developer** | `{project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1` | Test or validate a specific version before promoting it to default. |
| **Toolbox consumer** | `{project_endpoint}/toolboxes/{toolbox_name}/mcp?api-version=v1` | Connect agents to the toolbox. Always serves the `default_version`. The first version you create is automatically set as the default. |

> [!IMPORTANT]
> Every request to the toolbox MCP endpoint must include the header `Foundry-Features: Toolboxes=V1Preview`. Calls that omit this header fail. Include it in all HTTP clients, MCP transports, and SDK wrappers that call the toolbox endpoint.

> [!NOTE]
> The first version of a new toolbox is automatically promoted to `default_version` (v1). If you need to change the default later, see [Promote a version to default](#promote-a-version-to-default).

:::zone pivot="vscode"

In Foundry Toolkit for Visual Studio Code, copy the toolbox consumer
endpoint from the **Toolboxes** view.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. On the **Toolboxes** tab, locate your toolbox.
1. In the **Endpoint URL** column, copy the endpoint.

The **Endpoint URL** value is the toolbox consumer endpoint. To
construct a version-specific endpoint, use the developer pattern shown
in the table above.

:::image type="content" source="../../media/tools/toolbox/toolbox-vscode-list.png" alt-text="Screenshot of Foundry Toolkit in Visual Studio Code showing the Toolboxes view with the toolbox endpoint URL and the Scaffold code template action." lightbox="../../media/tools/toolbox/toolbox-vscode-list.png":::

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
    "Foundry-Features": "Toolboxes=V1Preview",
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
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

**2. Send the initialized notification**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","method":"notifications/initialized"}
```

**3. List available tools**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

**4. Call a tool**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Content-Type: application/json
Foundry-Features: Toolboxes=V1Preview

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
        "Foundry-Features": "Toolboxes=V1Preview",
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

Use the endpoint from Step 2 together with a scaffolded hosted agent
sample to validate toolbox loading in VS Code.

1. In **Foundry Toolkit**, under **My Resources** > **Your project
  name** > **Tools**, locate the toolbox you want to test.
1. Select **Scaffold code template**.
1. Choose a project folder when prompted.
1. Follow the generated `README.md` to install dependencies, configure
  environment variables, and run the sample locally.
1. Use **Agent Inspector** or run `python main.py` to confirm the
  toolbox tools load and respond.

For version-specific validation before you promote a new toolbox version,
use the Python or REST API tab in this step.

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
- For MCP tools, names are prefixed with the `server_label` - for example, `myserver.some_tool`. For all other tool types, the name is the `name` field value or the default tool name.
- Note the exact parameter names for the call step (for example `query` vs `queries`).

**Check - `tools/call`**:

- No top-level `error` field. If present, inspect `error.code`. For standard MCP error codes, see the [MCP specification](https://modelcontextprotocol.io/specification/2025-03-26/server/tools#error-handling):
  - `-32006` → OAuth consent required (extract URL from `error.message`).
  - Other codes → server-side failure.
- `result.content[]` contains entries with `"type": "text"` - this is the tool output.
- For AI Search, check `result.structuredContent.documents[]` for chunk metadata (`title`, `url`, `id`, `score`).
- For File Search, check `result.content[].resource._meta` for chunk metadata (`title`, `file_id`, `document_chunk_id`, `score`).
- For Web Search, check `result.content[].resource._meta.annotations[]` for URL citations (`type`, `url`, `title`, `start_index`, `end_index`).
- Watch for `"ServerError"` in text content - the tool executed but hit an internal error.

Tool-specific `tools/call` argument examples:

| Tool type | Arguments |
| --------- | --------- |
| AI Search | `{"query": "search text"}` |
| File Search | `{"queries": ["search text"]}` |
| Code Interpreter | `{"code": "print(2 ** 100)"}` |
| Web Search | `{"search_query": "weather in seattle"}` |
| A2A | `{"message": {"parts": [{"type": "text", "text": "Hello"}]}}` |
| MCP | `{"query": "what is agent service"}` |

## Step 4: Integrate the toolbox into your agent

:::zone pivot="python"

### LangGraph

**`.env` file**:

```
FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
FOUNDRY_AGENT_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
FOUNDRY_AGENT_TOOLBOX_FEATURES=Toolboxes=V1Preview
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

**`main.py`** (key pattern):

```python
TOOLBOX_ENDPOINT = os.getenv("TFOUNDRY_AGENT_TOOLBOX_ENDPOINT")

# Auth: httpx.Auth subclass injects a Bearer token on every request
class _ToolboxAuth(httpx.Auth):
    def __init__(self, token_provider):
        self._get_token = token_provider
    def auth_flow(self, request):
        request.headers["Authorization"] = f"Bearer {self._get_token()}"
        yield request

# Connect LangGraph to the toolbox MCP endpoint
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
client = MultiServerMCPClient({
    "toolbox": {
        "url": TOOLBOX_ENDPOINT,
        "transport": "streamable_http",
        "headers": {"Foundry-Features": "Toolboxes=V1Preview"},
        "auth": _ToolboxAuth(token_provider),
    }
})
tools = await client.get_tools()
```

See the [full sample](https://aka.ms/foundry-toolbox-langgraph) for the complete implementation.

### Microsoft Agent Framework

Use `MCPStreamableHTTPTool` from the Agent Framework SDK to connect directly to the toolbox MCP endpoint.

**`.env` file**:

```
FOUNDRY_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
FOUNDRY_AGENT_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
FOUNDRY_AGENT_TOOLBOX_FEATURES=Toolboxes=V1Preview
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o
```

**`main.py`** (key pattern):

```python
# Auth: wrap token provider in an httpx.Auth subclass
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(credential, "https://ai.azure.com/.default")
http_client = httpx.AsyncClient(
    auth=_ToolboxAuth(token_provider),
    headers={"Foundry-Features": os.getenv("FOUNDRY_AGENT_TOOLBOX_FEATURES", "Toolboxes=V1Preview")},
    timeout=120.0,
)

TOOLBOX_ENDPOINT = os.getenv("FOUNDRY_AGENT_TOOLBOX_ENDPOINT")

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
FOUNDRY_AGENT_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/versions/<version>/mcp?api-version=v1
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

See the [full sample](https://aka.ms/foundry-toolbox-copilotsdk) for the complete implementation.

:::zone-end

:::zone pivot="dotnet"

### Microsoft Agent Framework

Use `ResponsesServer` from the Agent Framework SDK with a custom `ToolboxMcpClient` to discover and invoke toolbox tools via the MCP endpoint.

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

var openAiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("Set AZURE_OPENAI_ENDPOINT");
var deployment = Environment.GetEnvironmentVariable("AZURE_AI_MODEL_DEPLOYMENT_NAME") ?? "gpt-4o";
var toolboxEndpoint = Environment.GetEnvironmentVariable("TOOLBOX_MCP_ENDPOINT")
    ?? throw new InvalidOperationException(
        "TOOLBOX_MCP_ENDPOINT is required. Set this variable " +
        "(platform-injected at runtime) to enable toolbox integration.");

// Azure OpenAI client
var credential = new DefaultAzureCredential();
var aoaiClient = new AzureOpenAIClient(new Uri(openAiEndpoint), credential);
var chatClient = aoaiClient.GetChatClient(deployment);

// Toolbox MCP client — discovers tools via tools/list, calls them via tools/call
var toolboxClient = new ToolboxMcpClient(toolboxEndpoint, credential);

ResponsesServer.Run<ToolboxHandler>(configure: builder =>
{
    builder.Services.AddSingleton(new AgentConfig(chatClient, toolboxClient));
});
```

`ToolboxMcpClient` wraps direct JSON-RPC calls to the MCP endpoint. `ToolboxHandler` wires LLM tool calls back to the MCP client using a standard tool-calling loop. See the [full sample](https://github.com/microsoft/hosted-agents-vnext-private-preview/tree/main/samples/dotnet/toolbox/maf) for the complete implementation of both classes.

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

Use Foundry Toolkit to scaffold a hosted agent sample that is already
wired to your toolbox.

1. Select **Foundry Toolkit** in the Activity Bar.
1. Under **My Resources**, expand **Your project name** > **Tools**.
1. On the **Toolboxes** tab, locate the toolbox you want to consume,
  and then select **Scaffold code template**.
1. In the Command Palette, choose a project folder when prompted.
1. Open the generated `README.md` and follow the setup, local run, and
  deployment steps for the scaffold.

The generated project includes the hosted agent entry point, deployment
files, and a `README.md` with the exact setup, run, and deployment
steps. The scaffolded agent handles the `Foundry-Features:
Toolboxes=V1Preview` header for you.

If you want to integrate a toolbox into an existing hosted agent project
instead of generating a new sample, use the copied endpoint from Step 2
with the Python or .NET patterns in this section.

:::zone-end

:::zone pivot="azd"

### Deploy with azd

Use the Azure Developer CLI (`azd`) to declare toolbox resources directly in an `agent.yaml` file and deploy your agent with a single command. By using this approach, you don't need to create the toolbox separately through SDK or REST. `azd` provisions the toolbox, connections, and model deployment together.

> [!IMPORTANT]
> The `-m` (or `--manifest`) flag is required for `azd ai agent init`. It tells the command where to find your agent definition and source files. `-m` can point to either a specific `agent.yaml` file or a folder containing one. All files in the manifest directory (`main.py`, `Dockerfile`, `requirements.txt`, and so on) are copied verbatim into the scaffolded project under `src/<agent-name>/`.

**Folder structure**:

```
my-agent/
├── agent.yaml          # Agent, toolbox, and connection declarations
├── main.py             # LangGraph agent
├── requirements.txt    # All dependencies (Azure SDK + PyPI packages)
├── Dockerfile          # Container build
```

**`agent.yaml`** (Web Search + GitHub MCP example):

```yaml
name: my-toolbox-agent
description: LangGraph agent with Azure AI Foundry toolbox MCP.
metadata:
  tags:
    - AI Agent Hosting
    - LangGraph
template:
  name: my-toolbox-agent
  kind: hosted
  protocols:
    - protocol: responses
      version: 1.0.0
  environment_variables:
    # FOUNDRY_PROJECT_ENDPOINT and FOUNDRY_AGENT_TOOLBOX_* are injected
    # automatically by the platform at runtime — do NOT declare them here.
    - name: AZURE_AI_MODEL_DEPLOYMENT_NAME
      value: ${AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4o}
    - name: TOOLBOX_NAME
      value: ${TOOLBOX_NAME=agent-tools}
parameters:
  github_pat:
    secret: true
    description: GitHub Personal Access Token for MCP connection
resources:
  - kind: connection
    name: github-mcp-conn
    target: https://api.githubcopilot.com/mcp
    category: RemoteTool
    authType: CustomKeys
    credentials:
      keys:
        Authorization: "Bearer {{ github_pat }}"
  - kind: toolbox
    name: agent-tools
    description: Web search and GitHub MCP tools
    tools:
      - type: web_search
      - type: mcp
        server_label: github
        server_url: https://api.githubcopilot.com/mcp
        project_connection_id: github-mcp-conn
```

> [!NOTE]
> When you deploy with toolbox resources in `agent.yaml`, the platform injects `FOUNDRY_AGENT_TOOLBOX_ENDPOINT` (base URL) and `TOOLBOX_{toolbox_name}_MCP_ENDPOINT` (full per-toolbox endpoint) as environment variables. For the toolbox named `agent-tools`, the per-toolbox variable becomes `TOOLBOX_AGENT_TOOLS_MCP_ENDPOINT`. Your `main.py` reads the per-toolbox variable or constructs the URL from `FOUNDRY_AGENT_TOOLBOX_ENDPOINT` and `TOOLBOX_NAME` at runtime.

**`main.py`** follows the same LangGraph pattern shown earlier. By using `azd`, `FOUNDRY_AGENT_TOOLBOX_ENDPOINT` and `TOOLBOX_{toolbox_name}_MCP_ENDPOINT` are injected automatically - no extra endpoint configuration is needed in code.

**Deploy**:

```bash
# 1. Place agent.yaml and source files in a manifest directory
mkdir my-agent/manifest
# Copy agent.yaml, main.py, Dockerfile, requirements.txt into my-agent/manifest/

# 2. Initialize the azd project (-m is required)
cd my-agent
PROJECT_ID="/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.CognitiveServices/accounts/<account>/projects/<project>"
azd ai agent init -m manifest/ --project-id $PROJECT_ID -e my-env
# If agent.yaml declares {{ param }} secrets (for example, github_pat), you are prompted
# to enter them interactively here. Do NOT use --no-prompt — it leaves credentials empty.

# 3. Set required environment variables
azd env set enableHostedAgentVNext "true" -e my-env
azd env set AZURE_AI_MODEL_DEPLOYMENT_NAME "gpt-4o" -e my-env

# 4. Provision infrastructure (creates connections via Bicep)
azd provision -e my-env

# 5. Deploy agent (creates toolboxes, container image, agent version)
azd deploy -e my-env

# 6. Invoke the agent
azd ai agent invoke --new-session "Hello, what tools do you have?" --timeout 120
```

:::zone-end

## Step 5: Manage toolbox versions

> [!NOTE]
> You can manage toolbox versions (list, get, promote, delete) through the Python SDK, .NET SDK, JavaScript SDK, and REST API. The azd CLI only supports creating toolbox versions during deployment.

Toolbox versions are immutable snapshots of a toolbox's tool configuration. Every call to the create endpoint produces a new `ToolboxVersionObject`. The parent `ToolboxObject` has a `default_version` field that controls which version the MCP endpoint serves. Creating a new version doesn't automatically promote it - you decide when to update `default_version`. This process lets you stage changes, test a new version independently, and promote it to production on your own schedule.

| Object | Key fields | Description |
|--------|-----------|-------------|
| `ToolboxObject` | `id`, `name`, `default_version` | The toolbox container. `default_version` points to the active version. |
| `ToolboxVersionObject` | `id`, `name`, `version`, `description`, `created_at`, `tools[]`, `policies` | An immutable snapshot of the toolbox's tool list at a point in time. |

### Create a new version

Each create call produces a new version. If the toolbox doesn't exist yet, the process automatically creates it. When you create the first version of a new toolbox, the default version is `v1` until you **manually** update to another version.

:::zone pivot="python"

```python
toolbox_version = client.beta.toolboxes.create_toolbox_version(
    toolbox_name="my-toolbox",
    description="Updated tools v2",
    tools=[...],
)
print(f"Created version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Updated tools v2"
);
Console.WriteLine($"Created version: {toolboxVersion.Version}");
```

:::zone-end

:::zone pivot="rest-api"

```

POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
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
const toolboxVersion = await project.beta.toolboxes.createVersion(
  "my-toolbox",
  [/* tools array */],
  { description: "Updated tools v2" },
);
console.log(`Created version: ${toolboxVersion.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to create a new
toolbox version. The Foundry Toolkit workflow in this article focuses on
creating a toolbox and scaffolding a hosted agent that consumes it.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with azd. To create a toolbox version, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end

The response is a `ToolboxVersionObject` containing the new `version` identifier.

### List versions

:::zone pivot="python"

```python
versions = list(client.beta.toolboxes.list_toolbox_versions(toolbox_name="my-toolbox"))
for v in versions:
    print(f"{v.version} — created {v.created_at}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
List<ToolboxVersion> versions = await toolboxClient
    .GetToolboxVersionsAsync("my-toolbox")
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
GET {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
const versions = project.beta.toolboxes.listVersions("my-toolbox");
for await (const v of versions) {
  console.log(`${v.version} — created ${v.createdAt}`);
}
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to list toolbox
versions.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with azd. To list toolbox versions, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end

### Get a specific version

:::zone pivot="python"

```python
version_obj = client.beta.toolboxes.get_toolbox_version(
    toolbox_name="my-toolbox",
    version="<version_id>",
)
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxVersion versionObj = await toolboxClient.GetToolboxVersionAsync(
    "my-toolbox",
    "<version_id>"
);
Console.WriteLine($"Retrieved toolbox: {versionObj.Name} ({versionObj.Id})");
```

:::zone-end

:::zone pivot="rest-api"

```http
GET {project_endpoint}/toolboxes/my-toolbox/versions/{version}?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
const versionObj = await project.beta.toolboxes.getVersion(
  "my-toolbox",
  "<version_id>",
);
console.log(`Retrieved version: ${versionObj.version}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to get a specific
toolbox version.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with azd. To get a specific toolbox version, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end

### Promote a version to default

The MCP endpoint always serves the `default_version`. To switch which version is active, update the toolbox:

:::zone pivot="python"

```python
toolbox = client.beta.toolboxes.update(
    toolbox_name="my-toolbox",
    default_version="<version_id>",
)
print(f"Active version: {toolbox.default_version}")
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ToolboxRecord record = await toolboxClient.UpdateToolboxAsync(
    "my-toolbox",
    "<version_id>"
);
Console.WriteLine($"Active version: {record.DefaultVersion}");
```

:::zone-end

:::zone pivot="rest-api"

```http
PATCH {project_endpoint}/toolboxes/my-toolbox?api-version=v1
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
const toolbox = await project.beta.toolboxes.update(
  "my-toolbox",
  "<version_id>",
);
console.log(`Active version: ${toolbox.defaultVersion}`);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to promote a toolbox
version to default.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with azd. To promote a version to default, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end

### Delete a version

:::zone pivot="python"

```python
client.beta.toolboxes.delete_toolbox_version(
    toolbox_name="my-toolbox",
    version="<version_id>",
)
```

:::zone-end

:::zone pivot="dotnet"

```csharp
await toolboxClient.DeleteToolboxVersionAsync(
    "my-toolbox",
    "<version_id>"
);
```

:::zone-end

:::zone pivot="rest-api"

```http
DELETE {project_endpoint}/toolboxes/my-toolbox/versions/{version}?api-version=v1
Authorization: Bearer {token}
```

:::zone-end

:::zone pivot="javascript"

```javascript
await project.beta.toolboxes.deleteVersion(
  "my-toolbox",
  "<version_id>",
);
```

:::zone-end

:::zone pivot="vscode"

Use the Python, .NET, JavaScript, or REST API tab to delete a toolbox
version.

:::zone-end

:::zone pivot="azd"

This operation isn't supported with azd. To delete a toolbox version, use the **Python**, **.NET**, **REST API**, or **JavaScript** tab.

:::zone-end


## Configure tools

Choose the tool type and authentication pattern that match your scenario. Select the tab for your preferred SDK or deployment method.

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

The following sections show each tool type's configuration in detail.

### [Model Context Protocol (MCP)](model-context-protocol.md)

:::zone pivot="rest-api"

**Key-based auth:**

```json
{
  "description": "my-mcp-toolbox",
  "tools": [
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com",
      "project_connection_id": "my-mcp-connection"
    }
  ]
}
```

**No auth (public MCP server):**

```json
{
  "description": "Public MCP server",
  "tools": [
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com"
    }
  ]
}
```

**OAuth or identity-based auth:**

For OAuth (managed connector, custom app registration), agent identity, or user Entra token auth, first create the appropriate connection in your Foundry project, then reference it with `project_connection_id`:

```json
{
  "description": "MCP server with OAuth/identity auth",
  "tools": [
    {
      "type": "mcp",
      "server_label": "myserver",
      "server_url": "https://your-mcp-server.example.com",
      "project_connection_id": "<OAUTH_OR_IDENTITY_CONNECTION_NAME>"
    }
  ]
}
```

The connection's `authType` determines the authentication flow. Supported connection auth types for MCP include `CustomKeys`, `OAuth2` (managed or custom), `AgenticIdentity`, and `UserEntraToken`. See the [azd tab](#model-context-protocol-mcp) for connection configuration examples for each auth type.

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import MCPTool

tools = [
    MCPTool(
        server_label="myserver",
        server_url="https://your-mcp-server.example.com",
        project_connection_id="my-mcp-connection",
    )
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = ProjectsAgentTool.AsProjectTool(ResponseTool.CreateMcpTool(
    serverLabel: "myserver",
    serverUri: new Uri("https://your-mcp-server.example.com")
));

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "my-mcp-toolbox"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "mcp",
    server_label: "myserver",
    server_url: "https://your-mcp-server.example.com",
    project_connection_id: "my-mcp-connection",
  },
];
```

:::zone-end

:::zone pivot="azd"

**No auth:**

```yaml
resources:
  - kind: toolbox
    name: mcp-tools
    description: Public MCP server tools
    tools:
      - type: mcp
        server_label: myserver
        server_url: https://your-mcp-server.example.com
```

**Key-based auth:**

```yaml
parameters:
  mcp_api_key:
    secret: true
    description: API key for the MCP server
resources:
  - kind: connection
    name: mcp-conn
    target: https://your-mcp-server.example.com
    category: RemoteTool
    authType: CustomKeys
    credentials:
      keys:
        Authorization: "Bearer {{ mcp_api_key }}"
  - kind: toolbox
    name: mcp-tools
    description: MCP server tools with key auth
    tools:
      - type: mcp
        server_label: myserver
        server_url: https://your-mcp-server.example.com
        project_connection_id: mcp-conn
```

**OAuth — managed connector:**

Use this pattern for MCP servers that support Foundry's managed OAuth flow. The `connectorName` value must match a managed connector available in the Foundry Tools Catalog.

```yaml
resources:
  - kind: connection
    name: github-oauth-conn
    category: RemoteTool
    authType: OAuth2
    target: https://api.githubcopilot.com/mcp
    connectorName: foundrygithubmcp
  - kind: toolbox
    name: oauth-tools
    description: GitHub OAuth MCP toolbox
    tools:
      - type: mcp
        server_label: github
        project_connection_id: github-oauth-conn
```

**OAuth — custom app registration:**

Use this pattern when you bring your own OAuth app registration for the MCP server.

```yaml
parameters:
  oauth_client_id:
    secret: true
    description: OAuth client ID
  oauth_client_secret:
    secret: true
    description: OAuth client secret
resources:
  - kind: connection
    name: mcp-oauth-custom-conn
    category: RemoteTool
    authType: OAuth2
    target: https://your-mcp-server.example.com
    authorizationUrl: https://auth.example.com/authorize
    tokenUrl: https://auth.example.com/token
    refreshUrl: https://auth.example.com/token
    scopes: []
    credentials:
      clientID: "{{ oauth_client_id }}"
      clientSecret: "{{ oauth_client_secret }}"
  - kind: toolbox
    name: oauth-custom-tools
    description: MCP toolbox with custom OAuth
    tools:
      - type: mcp
        server_label: myserver
        project_connection_id: mcp-oauth-custom-conn
```

**Agent identity (Entra ID):**

Use this pattern for MCP servers that support Microsoft Entra ID authentication. The Foundry agent identity authenticates against the target resource.

```yaml
resources:
  - kind: connection
    name: language-mcp
    category: RemoteTool
    authType: AgenticIdentity
    audience: <entra-audience>
    target: https://<resource>.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview
  - kind: toolbox
    name: agent-identity-tools
    description: MCP toolbox with agent identity auth
    tools:
      - type: mcp
        server_label: language
        project_connection_id: language-mcp
```

> [!NOTE]
> You must assign your agent identity the required RBAC role on the target resource before the MCP server accepts requests.

**User Entra token (1P OBO):**

Use this pattern for MCP servers that require user identity through the On-Behalf-Of (OBO) flow. Foundry proxies the user's Entra token to the MCP server.

```yaml
resources:
  - kind: connection
    name: workiq-mail-conn
    category: RemoteTool
    authType: UserEntraToken
    audience: <entra-app-id>
    target: https://agent365.svc.cloud.microsoft/agents/servers/mcp_MailTools
  - kind: toolbox
    name: workiq-tools
    description: MCP toolbox with user Entra token auth
    tools:
      - type: mcp
        server_label: workiq
        project_connection_id: workiq-mail-conn
```

> [!NOTE]
> The `audience` field is required for `UserEntraToken` connections. Without it, `tools/list` returns 0 tools.

:::zone-end

> [!IMPORTANT]
> The first time a user calls a toolbox with an OAuth-based MCP in a project, the MCP endpoint returns a `CONSENT_REQUIRED` error (code `-32006`) with a consent URL:
>
> ```json
> {
>   "error": {
>     "code": -32006,
>     "message": "User consent is required. Please visit: https://..."
>   }
> }
> ```
>
> This error is expected. Open the consent URL in a browser, complete the OAuth authorization flow, and then retry the agent call. Subsequent calls succeed without re-prompting.

### [Web Search](web-search.md)

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](./web-search.md#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

Use this pattern to add web search. No project connection is required for the web search with Grounding with Bing. To use a Grounding with custom Bing Search instance, add a `web_search.custom_search_configuration` object pointing to your Grounding with Bing Custom Search connection.

:::zone pivot="rest-api"

```json
{
  "description": "Built-in web search",
  "tools": [
    {
      "type": "web_search",
      "name": "<OPTIONAL_TOOL_NAME>",
      "description": "<Optional description for the model>"
    }
  ]
}
```

**With a Grounding with Bing Custom Search connection:**

```json
{
  "description": "Custom Bing Search instance",
  "tools": [
    {
      "type": "web_search",
      "name": "<OPTIONAL_TOOL_NAME>",
      "description": "<Optional description for the model>",
      "web_search": {
        "custom_search_configuration": {
          "project_connection_id": "<BING_CONNECTION_NAME>",
          "instance_name": "<BING_INSTANCE_NAME>"
        }
      }
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import WebSearchTool

tools = [
    WebSearchTool()
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateWebSearchTool()
);

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Built-in web search"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "web_search",
    name: "<OPTIONAL_TOOL_NAME>",
    description: "<Optional description for the model>",
  },
];
```

:::zone-end

:::zone pivot="azd"

```yaml
resources:
  - kind: toolbox
    name: websearch-tools
    description: Web search toolbox
    tools:
      - type: web_search
```

**With Grounding with Bing Custom Search:**

```yaml
parameters:
  bing_api_key:
    secret: true
    description: Bing API key
resources:
  - kind: connection
    name: bing-custom-conn
    category: GroundingWithCustomSearch
    authType: ApiKey
    target: ""
    credentials:
      key: "{{ bing_api_key }}"
    metadata:
      ResourceId: /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Bing/accounts/<bing-account>
      type: bing_custom_search
  - kind: toolbox
    name: bing-custom-tools
    description: Bing Custom Search toolbox
    tools:
      - type: bing_custom_search
        custom_search_configuration:
          instance_name: your-bing-custom-instance
        project_connection_id: bing-custom-conn
```

:::zone-end

> [!NOTE]
> When Web Search returns results over MCP, the response is a `resource` content item containing the synthesized answer with inline Markdown source links. URL citations are in `content[].resource._meta.annotations[]`. For example:
>
> ```json
> {
>   "jsonrpc": "2.0",
>   "id": "ws-call-1",
>   "result": {
>     "_meta": {
>       "tool_configuration": {
>         "type": "web_search",
>         "name": "web-search-default"
>       }
>     },
>     "content": [
>       {
>         "type": "resource",
>         "resource": {
>           "uri": "about:web-search-answer",
>           "mimeType": "text/plain",
>           "text": "Here are the latest updates on Azure OpenAI Service...\n\n- **GPT-image-1 Release (January 7, 2026)** Microsoft introduced GPT-image-1 ([serverless-solutions.com](https://...)).\n\n..."
>         },
>         "annotations": {
>           "audience": ["assistant"]
>         },
>         "_meta": {
>           "annotations": [
>             {
>               "type": "url_citation",
>               "url": "https://www.serverless-solutions.com/blog/...",
>               "title": "Microsoft Expands Azure AI Foundry with Powerful New OpenAI Models",
>               "start_index": 741,
>               "end_index": 879
>             }
>           ],
>           "action": {
>             "type": "search",
>             "query": "Azure OpenAI service updates 2026",
>             "queries": ["Azure OpenAI service updates 2026"]
>           },
>           "response_id": "resp_001fcebcc300..."
>         }
>       }
>     ],
>     "isError": false
>   }
> }
> ```

### [Azure AI Search](ai-search.md)

:::zone pivot="rest-api"

```json
{
  "description": "Azure AI Search over my data",
  "tools": [
    {
      "type": "azure_ai_search",
      "name": "<OPTIONAL_TOOL_NAME>",
      "description": "<Optional description for the model>",
      "azure_ai_search": {
        "indexes": [
          {
            "index_name": "<INDEX_NAME>",
            "project_connection_id": "<CONNECTION_NAME>"
          }
        ]
      }
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import AzureAISearchTool

tools = [
    AzureAISearchTool(
        index_name="<INDEX_NAME>",
        project_connection_id="<CONNECTION_NAME>",
    )
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = new AzureAISearchTool(
    new AzureAISearchToolOptions(
        indexes: [
            new AzureAISearchIndexResource(
                indexName: "<INDEX_NAME>",
                projectConnectionId: "<CONNECTION_NAME>"
            )
        ]
    )
);

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Azure AI Search over my data"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "azure_ai_search",
    name: "<OPTIONAL_TOOL_NAME>",
    description: "<Optional description for the model>",
    azure_ai_search: {
      indexes: [
        {
          index_name: "<INDEX_NAME>",
          project_connection_id: "<CONNECTION_NAME>",
        },
      ],
    },
  },
];
```

:::zone-end

:::zone pivot="azd"

```yaml
parameters:
  ai_search_key:
    secret: true
    description: Azure AI Search admin key
resources:
  - kind: connection
    name: aisearch-conn
    category: CognitiveSearch
    authType: ApiKey
    target: https://your-search-service.search.windows.net/
    credentials:
      key: "{{ ai_search_key }}"
  - kind: toolbox
    name: search-tools
    description: Azure AI Search toolbox
    tools:
      - type: azure_ai_search
        index_name: your-index-name
        project_connection_id: aisearch-conn
```

:::zone-end

#### Configure tool parameters

| Azure AI Search tool parameter | Required | Notes |
| --- | --- | --- |
| `project_connection_id` | Yes | The resource ID of the project connection to Azure AI Search. |
| `index_name` | Yes | The name of the index in your Azure AI Search resource. |
| `top_k` | No | Defaults to 5. |
| `query_type` | No | Defaults to `vector_semantic_hybrid`. Supported values: `simple`, `vector`, `semantic`, `vector_simple_hybrid`, `vector_semantic_hybrid`. |
| `filter` | No | Applies to all queries the agent makes to the index. |


The search results include chunk metadata in `result.structuredContent.documents[]`. Each document includes `title`, `url`, `id`, and `score` fields that you can use to generate citation details in your application.

### [Code Interpreter](code-interpreter.md)

Use this pattern to let the agent write and execute Python code. The pattern doesn't require a project connection or extra configuration.

To upload a file for Code Interpreter to use, call `POST {project_endpoint}/openai/v1/files` with `purpose=assistants`. The returned file ID is the value you supply as `<FILE_ID>` in the tool configuration. See [Code Interpreter](code-interpreter.md) for full upload examples.

> [!IMPORTANT]
> When using Code Interpreter through a toolbox in a hosted agent, **user isolation is not supported**. All users in the same project share the same container context.

:::zone pivot="rest-api"

```json
{
  "description": "Code interpreter for data analysis",
  "tools": [
    {
      "type": "code_interpreter",
      "name": "<OPTIONAL_TOOL_NAME>",
      "description": "<Optional description for the model>",
      "container": {
            "type": "auto",
            "file_ids": ["<FILE_ID>"]
        }
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import CodeInterpreterTool

tools = [
    CodeInterpreterTool()
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateCodeInterpreterTool(
        new CodeInterpreterToolContainer()
    )
);

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Code interpreter for data analysis"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "code_interpreter",
    name: "<OPTIONAL_TOOL_NAME>",
    description: "<Optional description for the model>",
    container: {
      type: "auto",
      file_ids: ["<FILE_ID>"],
    },
  },
];
```

:::zone-end

:::zone pivot="azd"

```yaml
resources:
  - kind: toolbox
    name: codeinterp-tools
    description: Code interpreter toolbox
    tools:
      - type: code_interpreter
```

:::zone-end

#### Download output files from Code Interpreter

When Code Interpreter produces output files (for example, a generated CSV or chart), use the following steps to list and download them.

**Step 1: List files using the Container API**

Extract the `container_id` from `content[]._meta.container_id` in the `tools/call` response, then call the Container Files API to list all files in the container:

```http
GET {project_endpoint}/containers/{container_id}/files?api-version=v1
Authorization: Bearer {token}
```

The response returns a list of files with their names and IDs.

**Step 2: Download the file using the File API**

Use the file name returned from Step 1 to download the file via the [File API download endpoint](/azure/foundry/openai/latest#download-file).

### [File Search](file-search.md)

Use this pattern to let the agent search over uploaded files stored in a vector store. Provide `vector_store_ids` referencing vector stores already created in your Foundry project.

To create a file and vector store, use the `{project_endpoint}/openai/v1` API:

1. Upload your file: `POST {project_endpoint}/openai/v1/files` with `purpose=assistants`.
1. Create a vector store: `POST {project_endpoint}/openai/v1/vector_stores` with the returned file ID.

The resulting vector store ID is the value you supply as `<VECTOR_STORE_ID>`. See [File Search](file-search.md) for full examples in each language.

> [!IMPORTANT]
> When using File Search through a toolbox in a hosted agent, **user isolation is not supported**. All users in the same project share access to the same vector store.

:::zone pivot="rest-api"

```json
{
  "description": "Search over uploaded documents",
  "tools": [
    {
      "type": "file_search",
      "name": "<OPTIONAL_TOOL_NAME>",
      "description": "<Optional description for the model>",
      "file_search": {
        "vector_store_ids": ["<VECTOR_STORE_ID>"]
      }
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import FileSearchTool

tools = [
    FileSearchTool(
        vector_store_ids=["<VECTOR_STORE_ID>"]
    )
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = ProjectsAgentTool.AsProjectTool(
    ResponseTool.CreateFileSearchTool(
        vectorStoreIds: ["<VECTOR_STORE_ID>"]
    )
);

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Search over uploaded documents"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "file_search",
    name: "<OPTIONAL_TOOL_NAME>",
    description: "<Optional description for the model>",
    file_search: {
      vector_store_ids: ["<VECTOR_STORE_ID>"],
    },
  },
];
```

:::zone-end

:::zone pivot="azd"

```yaml
resources:
  - kind: toolbox
    name: filesearch-tools
    description: File search toolbox
    tools:
      - type: file_search
        vector_store_ids:
          - ${FILE_SEARCH_VECTOR_STORE_ID}
```

Set the vector store ID before deploying:

```bash
azd env set FILE_SEARCH_VECTOR_STORE_ID "vs_xxxxxxxxxxxx"
```

:::zone-end

> [!NOTE]
> When File Search returns results over MCP, chunk metadata is embedded in the tool response content as `【index†filename†file_id】` markers. For example:
>
> ```json
> {
>   "jsonrpc": "2.0",
>   "id": "fs-call-1",
>   "result": {
>     "content": [
>       {
>         "type": "resource",
>         "resource": {
>           "uri": "file://assistant-tvfqncbtruyffxkfewenyy/",
>           "_meta": {
>             "title": "mcp-test-file.txt",
>             "file_id": "assistant-TVfQnCBtRuyfFxkfeweNYY",
>             "document_chunk_id": "f7327b7f-5ed0-43c6-9bee-e8e9552afcb5",
>             "score": 0.03333333507180214
>           },
>           "text": "# 【0†mcp-test-file.txt†assistant-TVfQnCBtRuyfFxkfeweNYY】\nContent Snippet:\nAzure OpenAI Service is a cloud service..."
>         }
>       }
>     ]
>   }
> }
> ```
>
> The `_meta` block inside each resource item contains the `title`, `file_id`, `document_chunk_id`, and relevance `score` for the matched chunk. Use these metadata fields in your application to generate citation details or deep-link back to the source file.

### [OpenAPI](openapi.md)

Use this pattern to expose any REST API described by an OpenAPI spec. Choose the `auth.type` that matches your API's security model.

> [!IMPORTANT]
> When using managed identity auth, you must assign the appropriate RBAC role to your **Foundry project's** managed identity on the target service. For example, assign Reader or higher on the target Azure resource. Without this assignment, the agent receives a `401 Unauthorized` response when calling the API. For full setup steps, see [Authenticate by using managed identity](openapi.md#authenticate-by-using-managed-identity-microsoft-entra-id).

:::zone pivot="rest-api"

**Anonymous auth:**

```json
{
  "description": "REST API via OpenAPI spec",
  "tools": [
    {
      "type": "openapi",
      "openapi": {
        "name": "my-api",
        "spec": { "<paste OpenAPI spec object here>" },
        "auth": {
          "type": "anonymous"
        }
      }
    }
  ]
}
```

**Project connection auth:**

Use this pattern when the API requires a key or token stored in a Foundry project connection.

```json
{
  "description": "REST API with connection-based auth",
  "tools": [
    {
      "type": "openapi",
      "openapi": {
        "name": "my-api",
        "spec": { "<paste OpenAPI spec object here>" },
        "auth": {
          "type": "connection",
          "security_scheme": {
            "project_connection_id": "<CONNECTION_NAME>"
          }
        }
      }
    }
  ]
}
```

**Managed identity auth:**

Use this pattern when the target API authenticates via Microsoft Entra ID. The Foundry project's managed identity calls the API on behalf of the agent. Make sure the managed identity has the required RBAC role on the target service before using this pattern.

```json
{
  "description": "REST API with managed identity auth",
  "tools": [
    {
      "type": "openapi",
      "openapi": {
        "name": "my-api",
        "spec": { "<paste OpenAPI spec object here>" },
        "auth": {
          "type": "managed_identity",
          "security_scheme": {
            "audience": "<TARGET_SERVICE_AUDIENCE>"
          }
        }
      }
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import OpenAPITool

tools = [
    OpenAPITool(
        name="my-api",
        spec={"<paste OpenAPI spec object here>"},
        auth={"type": "anonymous"},
    )
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
BinaryData specBytes = BinaryData.FromString("<OpenAPI spec JSON>");
ProjectsAgentTool tool = new OpenAPITool(
    new OpenApiFunctionDefinition(
        name: "my-api",
        spec: specBytes,
        openApiAuthentication: new OpenApiAnonymousAuthDetails()
    )
);

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "REST API via OpenAPI spec"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "openapi",
    openapi: {
      name: "my-api",
      spec: { /* paste OpenAPI spec object here */ },
      auth: {
        type: "anonymous",
      },
    },
  },
];
```

:::zone-end

:::zone pivot="azd"

**Key-based auth:**

```yaml
parameters:
  api_key:
    secret: true
    description: API key for the target service
resources:
  - kind: connection
    name: api-conn
    category: CustomKeys
    authType: CustomKeys
    target: https://api.example.com
    credentials:
      keys:
        key: "{{ api_key }}"
  - kind: toolbox
    name: openapi-tools
    description: OpenAPI key-auth toolbox
    tools:
      - type: openapi
        openapi:
          name: my-api
          spec:
            openapi: "3.0.1"
            info:
              title: "My API"
              version: "1.0"
            servers:
              - url: https://api.example.com/v1
            paths:
              /search:
                get:
                  operationId: search
                  parameters:
                    - name: query
                      in: query
                      required: true
                      schema:
                        type: string
                  responses:
                    "200":
                      description: OK
          auth:
            type: connection_auth
            connection_id: api-conn
```

:::zone-end

### [Agent-to-Agent (A2A)](agent-to-agent.md)

Use this pattern to call another agent as a tool. Provide the base URL of the remote agent and, if it requires authentication, a project connection.

:::zone pivot="rest-api"

```json
{
  "description": "Delegate tasks to a specialist agent",
  "tools": [
    {
      "type": "a2a_preview",
      "name": "<AGENT_NAME>",
      "description": "<What this agent does>",
      "base_url": "<AGENT_BASE_URL>",
      "project_connection_id": "<CONNECTION_NAME>"
    }
  ]
}
```

:::zone-end

:::zone pivot="python"

```python
from azure.ai.projects.models import A2APreviewTool

tools = [
    A2APreviewTool(
        name="<AGENT_NAME>",
        description="<What this agent does>",
        base_url="<AGENT_BASE_URL>",
        project_connection_id="<CONNECTION_NAME>",
    )
]
```

:::zone-end

:::zone pivot="dotnet"

```csharp
ProjectsAgentTool tool = new A2APreviewTool()
{
    ProjectConnectionId = "<CONNECTION_NAME>",
};

ToolboxVersion toolboxVersion = await toolboxClient.CreateToolboxVersionAsync(
    toolboxName: "my-toolbox",
    tools: [tool],
    description: "Delegate tasks to a specialist agent"
);
```

:::zone-end

:::zone pivot="javascript"

```javascript
const tools = [
  {
    type: "a2a_preview",
    name: "<AGENT_NAME>",
    description: "<What this agent does>",
    base_url: "<AGENT_BASE_URL>",
    project_connection_id: "<CONNECTION_NAME>",
  },
];
```

:::zone-end

:::zone pivot="azd"

```yaml
resources:
  - kind: connection
    name: a2a-conn
    category: RemoteA2A
    authType: None
    target: https://your-remote-agent.azurecontainerapps.io
  - kind: toolbox
    name: a2a-tools
    description: Agent-to-Agent toolbox
    tools:
      - type: a2a_preview
        project_connection_id: a2a-conn
```

:::zone-end

## Troubleshoot

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `tools/list` returns 0 tools for MCP or A2A tools | Invalid or missing connection credentials for the remote MCP server or A2A agent. The toolbox can't retrieve tool manifests from the remote endpoint without valid auth. | Verify the `project_connection_id` exists in your Foundry project and the credentials are correct. Try connecting to the MCP server directly to test the auth setup. If using managed identity (PMI, agent identity, or MI), verify the correct RBAC role assignments for the caller on the target resource. |
| `tools/list` returns 0 tools for OpenAPI tools | Invalid OpenAPI spec. The toolbox constructs the tool manifest from the spec, which fails if the spec is malformed. | Validate your OpenAPI spec content. Check that it conforms to OpenAPI 3.0 or 3.1 and includes valid `paths`, `operationId` values, and parameter schemas. If using managed identity auth, also verify RBAC role assignments on the target service. |
| `tools/list` returns fewer tools than expected | The `allowed_tools` filter contains incorrect or misspelled tool names. Tool names are case-sensitive and must follow the [MCP specification for tool names](https://modelcontextprotocol.io/specification/2025-03-26/server/tools) (no whitespace or special characters). | Remove `allowed_tools` temporarily and call `tools/list` to get the full tool list. Use the exact names from the response to set values for `allowed_tools`. |
| `tools/list` returns 0 tools (other tool types) | Toolbox not fully provisioned or tool type unsupported in region. For built-in tools (Web Search, AI Search, Code Interpreter, File Search), tool manifests are constructed server-side and don't require auth — if they return empty, the toolbox version might not be provisioned yet. | Wait 10 seconds and retry. |
| `400 Multiple tools without identifiers` | Two unnamed tool types in one toolbox | Keep at most one unnamed type; add `server_label` to all MCP tools. |
| `CONSENT_REQUIRED` (code `-32006`) | OAuth connection requires user consent | Open the consent URL in a browser and complete the OAuth flow, then retry. |
| `401` on MCP calls | Expired token or wrong scope | Use scope `https://ai.azure.com/.default` and refresh the token. |
| Tool names not matching | MCP tool names are prefixed with `server_label` | Use `{server_label}.{tool_name}` format (for example, `myserver.get_info`). |
| `500` on `send_ping()` | Toolbox MCP server doesn't implement the MCP `ping` method. | Don't call `send_ping()`. If your framework calls it automatically (for example, Microsoft Agent Framework's `MCPStreamableHTTPTool._ensure_connected()`), disable the ping check or override the method with a no-op. |
| `500` on `prompts/list` | The Foundry MCP server doesn't implement `prompts/list`. | Pass `load_prompts=False` (or equivalent) to your MCP client constructor. |
| `500` with non-streaming `tools/call` | Non-streaming mode (`stream=False`) isn't supported for toolbox MCP endpoints. | Always use `stream=True` when calling toolbox MCP tools. |
| `500` on `tools/list` | Transient server error | Retry after a few seconds. |
| Environment variables overwritten at runtime | The platform reserves all environment variables prefixed with `FOUNDRY_` and might silently overwrite user-defined values. | Rename custom environment variables to avoid the `FOUNDRY_` prefix (for example, use `TOOLBOX_MCP_ENDPOINT` instead of `FOUNDRY_TOOLBOX_ENDPOINT`). |

## Virtual network support

When your Foundry project uses [network isolation (private link)](../../../how-to/configure-private-link.md), not all toolbox tool types are supported. The following table shows the support status for each tool type and how traffic flows in a network-isolated environment.

| Tool type | VNet support | Traffic flow |
|-----------|-------------|--------------|
| [MCP](model-context-protocol.md) | ✅ Supported | Through your VNet subnet |
| [Azure AI Search](ai-search.md) | ✅ Supported | Through private endpoint |
| [Code Interpreter](code-interpreter.md) | ✅ Supported | Microsoft backbone network |
| [Web Search](web-search.md) | ✅ Supported | Public endpoint |
| [OpenAPI](openapi.md) | ✅ Supported | Depends on target API network configuration |
| [File Search](file-search.md) | ❌ Not supported | Not yet available |
| [Agent-to-Agent (A2A)](agent-to-agent.md) | ❌ Not supported | Not yet available |

For full network isolation setup instructions, including VNet injection for the agent client, DNS configuration, and private endpoint requirements, see [Configure network isolation for Microsoft Foundry](../../../how-to/configure-private-link.md).

## Related content

- [Connect agents to Model Context Protocol servers](model-context-protocol.md)
- [Add MCP server authentication](../mcp-authentication.md)
- [Web search tool](web-search.md)
- [Azure AI Search tool](ai-search.md)
- [Deploy a hosted agent](../deploy-hosted-agent.md)
- [Add a connection to your project](../../../how-to/connections-add.md)
- [Configure network isolation for Microsoft Foundry](../../../how-to/configure-private-link.md)
