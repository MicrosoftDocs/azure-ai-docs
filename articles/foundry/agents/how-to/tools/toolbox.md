---
title: "Curate intent-based toolbox in Foundry (preview)"
description: "Use Microsoft toolbox in Foundry to add MCP servers, web search, Azure AI Search, file search, code interpreter tool and more to hosted agents through a single managed endpoint."
author: zhuoqunli
ms.author: zhuoqunli
ms.date: 04/03/2026
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

Toolbox in Foundry gives your agent access to tools through a unified MCP-compatible endpoint. Instead of wiring authentication and invocation separately for each tool type and framework, you configure a toolbox once in Microsoft Foundry and point your agent to it. The platform handles credential injection, token refresh, and enterprise policy enforcement at runtime.

In this article, you learn how to:

- Create a toolbox with one or more tools.
- Configure authentication using project connections.
- Get the toolbox MCP endpoint.
- Verify that tools load correctly.
- Integrate a toolbox into your hosted agent.
- Manage toolbox versions and promote a version to default.

## Feature support

| Feature | Python SDK | REST API | .NET SDK | 
|---------|-----------|----------|----------|
| Toolbox update / list / get / delete | ✔️  | ✔️ | ✔️ |
| Toolbox version create / list / get / delete | ✔️  | ✔️ | ✔️ |
| [MCP tool](model-context-protocol.md) | ✔️  | ✔️  | ✔️ |
| [Web Search tool](web-search.md) | ✔️  | ✔️  | ✔️ |
| [Azure AI Search tool](ai-search.md) | ✔️  | ✔️  | ✔️ |
| [Code Interpreter tool](code-interpreter.md) | ✔️  | ✔️  | ✔️ |
| [File Search tool](file-search.md) | ✔️  | ✔️  | ✔️ |
| [OpenAPI tool](openapi.md) | ✔️  | ✔️  | ✔️ |
| [Agent-to-Agent (A2A) tool](agent-to-agent.md) | ✔️  | ✔️  | ✔️ |

## Prerequisites

- An active [Microsoft Foundry project](../../../how-to/create-projects.md).
- **RBAC**: Azure AI User role on the Foundry project.
- Your Foundry project needs to be at one of the supported [regions](../../../openai/how-to/responses.md#region-availability).
- **Python SDK**: `pip install azure-ai-projects azure-identity`

> [!IMPORTANT]
> - A toolbox supports at most **one unnamed tool per tool type** (Web Search, Azure AI Search, Code Interpreter, File Search). To include more than one instance of the same tool type, use the `name` field to differentiate tool instances. Including two unnamed tool types returns an `invalid_payload` error. For details, see [Multiple tool types](#multiple-tool-types).
> - We highly recommend adding a `description` to tools such as Azure AI Search and File Search to better inform the model.
> - Carefully review each tool's documentation to learn more about individual tool setup, limitations, and warnings.

## Step 1: Create a toolbox version

Create a toolbox version based on tools you need.

:::zone pivot="python"

```python
import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MCPTool

client = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

toolbox_version = client.beta.toolboxes.create_toolbox_version(
    toolbox_name="my-toolbox",
    description="Toolbox with an MCP server",
    tools=[
        MCPTool(
            server_label="myserver",
            server_url="https://your-mcp-server.example.com",
            require_approval="never",
            project_connection_id="my-key-auth-connection",
        )
    ],
)
print(f"Created toolbox: {toolbox_version.name}, version: {toolbox_version.version}")
```

:::zone-end

:::zone pivot="rest-api"

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{
  "description": "Toolbox with an MCP server",
  "tools": [
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
> Use token scope `https://ai.azure.com/.default` when obtaining the bearer token.

:::zone-end


## Step 2: Configure tools

Choose the tool type and authentication pattern that matches your scenario.

> [!NOTE]
> Each of the following payloads is the request body for `POST {project_endpoint}/toolboxes/{toolbox_name}/versions?api-version=v1`.

### [Model Context Protocol (MCP)](model-context-protocol.md)

**Toolbox payload**:

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

> [!IMPORTANT]
> The first time a user calls a toolbox with an OAuth based mcp in a project, the MCP endpoint returns a `CONSENT_REQUIRED` error (code `-32006`) with a consent URL:
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
> This is expected. Open the consent URL in a browser, complete the OAuth authorization flow, then retry the agent call. Subsequent calls succeed without re-prompting.

### [Web Search](web-search.md)

> [!IMPORTANT]
> - Web Search uses Grounding with Bing Search and Grounding with Bing Custom Search, which are [First Party Consumption Services](https://www.microsoft.com/licensing/terms/product/Glossary/EAEAS#:%7E:text=First-Party%20Consumption%20Services) governed by these [Grounding with Bing terms of use](https://www.microsoft.com/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://go.microsoft.com/fwlink/?LinkId=521839&clcid=0x409).
> - The Microsoft [Data Protection Addendum](https://aka.ms/dpa) doesn't apply to data sent to Grounding with Bing Search and Grounding with Bing Custom Search. When you use Grounding with Bing Search and Grounding with Bing Custom Search, data transfers occur outside compliance and geographic boundaries.
> - Use of Grounding with Bing Search and Grounding with Bing Custom Search incurs costs. See [pricing](https://www.microsoft.com/bing/apis/grounding-pricing) for details.
> - See the [management section](./web-search.md#administrator-control-for-the-web-search-tool) for information about how Azure admins can manage access to use of web search.

Use this pattern to add web search. No project connection is required for the web search with Grounding with Bing. To use a Grounding with custom Bing Search instance, add a `web_search.custom_search_configuration` object pointing to your Grounding with Bing Custom Search connection.

**Toolbox payload** :

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

**With a Grounding with custom Bing Search connection**:

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

> [!NOTE]
> When Web Search returns results over MCP, the response is a single `text` content item containing the synthesized answer with inline Markdown citations. For example:
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
>         "type": "text",
>         "text": "Here are the latest updates on Azure OpenAI Service...\n\n- **February 2026**: Microsoft launched **gpt-realtime-1.5** and **gpt-audio-1.5** ([learn.microsoft.com](https://learn.microsoft.com/...)).\n\n...",
>         "annotations": {
>           "audience": ["assistant"]
>         }
>       }
>     ],
>     "isError": false
>   }
> }
> ```

### [Azure AI Search](ai-search.md)
**Toolbox payload** :

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
#### Configure tool parameters

| Azure AI Search tool parameter | Required | Notes |
| --- | --- | --- |
| `project_connection_id` | Yes | The resource ID of the project connection to Azure AI Search. |
| `index_name` | Yes | The name of the index in your Azure AI Search resource. |
| `top_k` | No | Defaults to 5. |
| `query_type` | No | Defaults to `vector_semantic_hybrid`. Supported values: `simple`, `vector`, `semantic`, `vector_simple_hybrid`, `vector_semantic_hybrid`. |
| `filter` | No | Applies to all queries the agent makes to the index. |


Citations are returned in `result.structuredContent.documents[]`. Each document includes `title`, `url`, `id`, and `score` fields.

### [Code Interpreter](code-interpreter.md)

Use this pattern to let the agent write and execute Python code. No project connection or extra configuration is required.

**Toolbox payload** :

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

### [File Search](file-search.md)

Use this pattern to let the agent search over uploaded files stored in a vector store. Provide `vector_store_ids` referencing vector stores already created in your Foundry project.

**Toolbox payload** :

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

> [!NOTE]
> When File Search returns results over MCP, citations are embedded in the tool response content as `【index†filename†file_id】` markers. For example:
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
> The `_meta` block inside each resource item contains the `title`, `file_id`, `document_chunk_id`, and relevance `score` for the matched chunk. Use these fields in your application to render citations or deep-link back to the source file.

### [OpenAPI](openapi.md)

Use this pattern to expose any REST API described by an OpenAPI spec. Choose the `auth.type` that matches your API's security model.

> [!IMPORTANT]
> When using managed identity auth, you must assign the appropriate RBAC role to your Foundry account's managed identity on the target service. For example, assign **Reader** or higher on the target Azure resource. Without this assignment, the agent receives a `401 Unauthorized` response when calling the API. For full setup steps, see [Authenticate by using managed identity](openapi.md#authenticate-by-using-managed-identity-microsoft-entra-id).

**Anonymous auth** :

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

**Project connection auth** :

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

**Managed identity auth** :

Use this pattern when the target API authenticates via Microsoft Entra ID. The Foundry account's managed identity calls the API on behalf of the agent. Make sure the managed identity has the required RBAC role on the target service before using this pattern.

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

### [Agent-to-Agent (A2A)](agent-to-agent.md)

Use this pattern to call another agent as a tool. Provide the base URL of the remote agent and, if it requires authentication, a project connection.

**Toolbox payload** :

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
> Each unnamed tool type (`web_search`, `azure_ai_search`, `code_interpreter`, `file_search`) can appear at most once without a `name`. If you want two instances of the same type, add a unique `name` to each — see the next example.

#### Multi-tool restrictions

You can include at most one unnamed instance of each built-in tool type in a toolbox. If you include two unnamed instances of the same type, the API returns:

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

## Step 3: Get the toolbox MCP endpoint

There are two endpoint patterns depending on your role:

| Role | Endpoint | When to use |
|------|----------|-------------|
| **Toolbox developer** | `{project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1` | Test or validate a specific version before promoting it to default. |
| **Toolbox consumer** | `{project_endpoint}/toolboxes/{toolbox_name}/mcp?api-version=v1` | Connect agents to the toolbox. Always serves the `default_version`. Requires `default_version` to be set on the toolbox. |

> [!IMPORTANT]
> The consumer endpoint returns an error if the toolbox has no `default_version` set. Before you share the toolbox broadly, [promote a version to default](#promote-a-version-to-default) before pointing agents to the consumer endpoint.

## Step 4: Verify tool availability

Before running the full agent, confirm that the toolbox loads the expected tools by using MCP JSON-RPC calls against the endpoint. Use the **version-specific endpoint** to validate a version before promoting it to default.

:::zone pivot="python"

#### Step 1: Acquire a token and build headers

```python
from azure.identity import DefaultAzureCredential

token = DefaultAzureCredential().get_token("https://ai.azure.com/.default").token
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}",
    "Foundry-Features": "Toolboxes=V1Preview",
}
```

#### Step 2: Initialize the MCP session

```python
import httpx

url = "https://<account>.services.ai.azure.com/api/projects/<proj>/toolboxes/<name>/versions/<version>/mcp?api-version=v1"

with httpx.Client(timeout=30.0) as http:
    resp = http.post(url, headers=headers, json={
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1"},
        },
    })
    resp.raise_for_status()
    session_id = resp.headers.get("mcp-session-id")
    headers["mcp-session-id"] = session_id

    http.post(url, headers=headers, json={
        "jsonrpc": "2.0", "method": "notifications/initialized"
    })
```

#### Step 3: `tools/list`

```python
    resp = http.post(url, headers=headers, json={
        "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}
    })
    tools = resp.json().get("result", {}).get("tools", [])
    print(f"Tools found: {len(tools)}")
    for t in tools:
        print(f"  - {t['name']}: {t.get('description', '')[:80]}")
```

#### Step 4: `tools/call`

Pick a tool name from the list and call it with matching arguments:

```python
    resp = http.post(url, headers=headers, json={
        "jsonrpc": "2.0", "id": 3, "method": "tools/call",
        "params": {
            "name": "<tool_name>",
            "arguments": {}  # replace with actual tool arguments
        },
    })
    result = resp.json()
```

:::zone-end

:::zone pivot="rest-api"

Use the version-specific endpoint (`/versions/{version}/mcp`) to validate a version before promoting it.

**1. Initialize the MCP session**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

**2. Send the initialized notification**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{"jsonrpc":"2.0","method":"notifications/initialized"}
```

**3. List available tools**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

**4. Call a tool**:

```http
POST {project_endpoint}/toolboxes/{toolbox_name}/versions/{version}/mcp?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"<TOOL_NAME>","arguments":{}}}
```

:::zone-end

**Check — initialize**: HTTP 200 and a non-empty `mcp-session-id` header. If you skip the initialize step, subsequent calls will fail.

**Check — `tools/list`**:
- `len(tools) > 0` — empty means the toolbox version was not provisioned correctly.
- Each tool has `name`, `description`, and `inputSchema`.
- `inputSchema` has a `properties` field (some MCP servers omit this, which breaks OpenAI).
- For MCP tools, names are prefixed with the `server_label` — for example, `myserver.some_tool`. For all other tool types, the name is the `name` field value or the default tool name.
- Note the exact parameter names for the call step (for example `query` vs `queries`).

**Check — `tools/call`**:
- No top-level `error` field. If present, inspect `error.code`:
  - `-32006` → OAuth consent required (extract URL from `error.message`).
  - Other codes → server-side failure.
- `result.content[]` contains entries with `"type": "text"` — this is the tool output.
- For AI Search, also check `result.structuredContent.documents[]` for citations.
- Watch for `"ServerError"` in text content — the tool executed but hit an internal error.

Tool-specific `tools/call` argument examples:

| Tool type | Arguments |
|-----------|-----------|
| AI Search | `{"query": "search text"}` |
| File Search | `{"queries": ["search text"]}` |
| Code Interpreter | `{"code": "print(2 ** 100)"}` |
| Web Search | `{"search_query": "weather in seattle"}` |
| A2A | `{"message": {"parts": [{"type": "text", "text": "Hello"}]}}` |
| MCP | `{"query": "what is agent service"}` |

## Step 5: Integrate the toolbox into your agent

### LangGraph

Set the `FOUNDRY_TOOLBOX_ENDPOINT` environment variable. The template picks up the endpoint automatically and connects to the toolbox on startup.

**`.env` file**:

```
FOUNDRY_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<toolbox-name>/mcp?api-version=v1
```

**`main.py`** (key pattern):

```python
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from azure.identity import DefaultAzureCredential

TOOLBOX_ENDPOINT = os.getenv("FOUNDRY_TOOLBOX_ENDPOINT")

def _get_toolbox_token() -> str:
    credential = DefaultAzureCredential()
    return credential.get_token("https://ai.azure.com/.default").token

async def build_agent():
    token = _get_toolbox_token()
    client = MultiServerMCPClient({
        "toolbox": {
            "url": TOOLBOX_ENDPOINT,
            "transport": "streamable_http",
            "headers": {
                "Authorization": f"Bearer {token}",
                "Foundry-Features": "Toolboxes=V1Preview",
            },
        }
    })
    tools = await client.get_tools()
    return tools
```

**`requirements.txt`**:

```
langchain-mcp-adapters==0.1.11
```

### Microsoft Agent Framework

Use `MCPStreamableHTTPTool` from the Agent Framework SDK to connect directly to the toolbox MCP endpoint without LangChain or LangGraph.

**`.env` file**:

```
AZURE_AI_PROJECT_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>
FOUNDRY_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<name>/mcp?api-version=v1
MODEL_DEPLOYMENT_NAME=gpt-4o
```

**`main.py`** (key pattern):

```python
import os
from urllib.parse import urlparse
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from azure.ai.agentserver.agentframework import from_agent_framework
from agent_framework import MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIChatClient

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o")
TOOLBOX_ENDPOINT = os.getenv("FOUNDRY_TOOLBOX_ENDPOINT")

_parsed = urlparse(PROJECT_ENDPOINT)
OPENAI_ENDPOINT = f"{_parsed.scheme}://{_parsed.netloc}"

def _get_toolbox_token() -> str:
    credential = DefaultAzureCredential()
    return credential.get_token("https://ai.azure.com/.default").token

def _get_toolbox_headers(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}",
        "Foundry-Features": "Toolboxes=V1Preview",
    }

credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    credential, "https://ai.azure.com/.default"
)

chat_client = AzureOpenAIChatClient(
    endpoint=OPENAI_ENDPOINT,
    deployment_name=MODEL_DEPLOYMENT_NAME,
    ad_token_provider=token_provider,
)

tools = []
if TOOLBOX_ENDPOINT:
    token = _get_toolbox_token()
    tools.append(MCPStreamableHTTPTool(
        name="toolbox",
        url=TOOLBOX_ENDPOINT,
        headers=_get_toolbox_headers(token),
    ))

agent = chat_client.create_agent(
    name="my-toolbox-agent",
    instructions="You are a helpful assistant with access to Foundry toolbox tools.",
    tools=tools,
)

from_agent_framework(agent).run()
```

**`requirements.txt`**:

```
--extra-index-url https://pkgs.dev.azure.com/azure-sdk/public/_packaging/azure-sdk-for-python/pypi/simple/
agent-framework>=0.1.0
azure-ai-agentserver-agentframework==1.0.0b14
azure-identity>=1.19.0
python-dotenv==1.1.1
```

### Copilot SDK

Use the GitHub Copilot SDK to build a toolbox-powered agent that bridges Copilot's tool invocation to the Foundry toolbox MCP endpoint.

> [!NOTE]
> The Copilot SDK rejects tool names containing dots. The bridge automatically replaces `.` with `_` in tool names — for example, `myserver.get_info` becomes `myserver_get_info`.

**`.env` file**:

```
GITHUB_TOKEN=<your-github-token>
FOUNDRY_TOOLBOX_ENDPOINT=https://<account>.services.ai.azure.com/api/projects/<project>/toolboxes/<name>/mcp?api-version=v1
```

**`agent.py`** (key pattern — MCP bridge):

```python
import httpx
from azure.identity import DefaultAzureCredential

def _get_toolbox_token() -> str:
    credential = DefaultAzureCredential()
    return credential.get_token("https://ai.azure.com/.default").token

def _get_toolbox_headers(token: str) -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "Foundry-Features": "Toolboxes=V1Preview",
    }

class McpBridge:
    """HTTP-based MCP client that bridges Foundry toolbox tools to the Copilot SDK."""

    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.headers = _get_toolbox_headers(token)
        self._session_id = None
        self._client = httpx.AsyncClient(timeout=60.0)
        self._req_id = 0

    def _next_id(self) -> int:
        self._req_id += 1
        return self._req_id

    async def initialize(self) -> str:
        resp = await self._client.post(
            self.endpoint, headers=self.headers,
            json={
                "jsonrpc": "2.0", "id": self._next_id(), "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "copilot-toolbox-bridge", "version": "1.0.0"},
                },
            },
        )
        resp.raise_for_status()
        self._session_id = resp.headers.get("mcp-session-id")
        headers = {**self.headers, **({"mcp-session-id": self._session_id} if self._session_id else {})}
        await self._client.post(
            self.endpoint, headers=headers,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
        )

    async def list_tools(self) -> list[dict]:
        headers = {**self.headers, **({"mcp-session-id": self._session_id} if self._session_id else {})}
        resp = await self._client.post(
            self.endpoint, headers=headers,
            json={"jsonrpc": "2.0", "id": self._next_id(), "method": "tools/list", "params": {}},
        )
        resp.raise_for_status()
        return resp.json().get("result", {}).get("tools", [])

    async def call_tool(self, name: str, arguments: dict) -> str:
        headers = {**self.headers, **({"mcp-session-id": self._session_id} if self._session_id else {})}
        resp = await self._client.post(
            self.endpoint, headers=headers,
            json={
                "jsonrpc": "2.0", "id": self._next_id(), "method": "tools/call",
                "params": {"name": name, "arguments": arguments},
            },
        )
        resp.raise_for_status()
        content = resp.json().get("result", {}).get("content", [])
        return "\n".join(c.get("text", "") for c in content if c.get("type") == "text")


async def run_agent(user_message: str) -> str:
    """Wire McpBridge into the Copilot SDK agent and run a single turn."""
    import os
    from copilot_sdk import Agent, Message

    endpoint = os.environ["FOUNDRY_TOOLBOX_ENDPOINT"]
    token = _get_toolbox_token()

    bridge = McpBridge(endpoint=endpoint, token=token)
    await bridge.initialize()
    mcp_tools = await bridge.list_tools()

    # Build Copilot SDK tool definitions from MCP tool list
    # Tool names with dots are replaced with underscores automatically by McpBridge
    copilot_tools = [
        {
            "name": t["name"].replace(".", "_"),
            "description": t.get("description", ""),
            "parameters": t.get("inputSchema", {}),
        }
        for t in mcp_tools
    ]

    async def tool_handler(name: str, arguments: dict) -> str:
        # Map underscored name back to dotted name for MCP call
        mcp_name = name.replace("_", ".", 1)
        return await bridge.call_tool(mcp_name, arguments)

    agent = Agent(
        tools=copilot_tools,
        tool_handler=tool_handler,
        token=os.environ["GITHUB_TOKEN"],
    )
    response = await agent.run(Message(role="user", content=user_message))
    return response.content
```

**`requirements.txt`**:

```
github-copilot-sdk>=0.1.29
azure-identity>=1.19.0
httpx
python-dotenv==1.1.1
```

## Step 6: Manage toolbox versions

Toolbox versions are immutable snapshots of a toolbox's tool configuration. Every call to the create endpoint produces a new `ToolboxVersionObject`. The parent `ToolboxObject` has a `default_version` field that controls which version the MCP endpoint serves. Creating a new version doesn't automatically promote it — you decide when to update `default_version`. This lets you stage changes, test a new version independently, and promote it to production on your own schedule.

| Object | Key fields | Description |
|--------|-----------|-------------|
| `ToolboxObject` | `id`, `name`, `default_version` | The toolbox container. `default_version` points to the active version. |
| `ToolboxVersionObject` | `id`, `name`, `version`, `description`, `created_at`, `tools[]`, `policies` | An immutable snapshot of the toolbox's tool list at a point in time. |

### Create a new version

Each create call produces a new version. If the toolbox doesn't exist yet, it's automatically created.

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

:::zone pivot="rest-api"

```http
POST {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{
  "description": "Updated tools v2",
  "tools": [...]
}
```

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

:::zone pivot="rest-api"

```http
GET {project_endpoint}/toolboxes/my-toolbox/versions?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
```

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

:::zone pivot="rest-api"

```http
GET {project_endpoint}/toolboxes/my-toolbox/versions/{version}?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
```

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

:::zone pivot="rest-api"

```http
PATCH {project_endpoint}/toolboxes/my-toolbox?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
Content-Type: application/json

{
  "default_version": "<version_id>"
}
```

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

:::zone pivot="rest-api"

```http
DELETE {project_endpoint}/toolboxes/my-toolbox/versions/{version}?api-version=v1
Authorization: Bearer {token}
Foundry-Features: Toolboxes=V1Preview
```

:::zone-end

## Troubleshoot

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `tools/list` returns 0 tools | Toolbox not fully provisioned or tool type unsupported in region | Wait 10 seconds and retry |
| `400 Multiple tools without identifiers` | Two unnamed tool types in one toolbox | Keep at most one unnamed type; add `server_label` to all MCP tools |
| `CONSENT_REQUIRED` (code `-32006`) | OAuth connection requires user consent | Open the consent URL in a browser and complete the OAuth flow, then retry |
| `401` on MCP calls | Expired token or wrong scope | Use scope `https://ai.azure.com/.default` and refresh the token |
| Tool names not matching | MCP tool names are prefixed with `server_label` | Use `{server_label}.{tool_name}` format (for example, `myserver.get_info`) |
| `500` on `tools/list` | Transient server error | Retry after a few seconds |

## Related content

- [Connect agents to Model Context Protocol servers](model-context-protocol.md)
- [Add MCP server authentication](../mcp-authentication.md)
- [Web search tool](web-search.md)
- [Azure AI Search tool](ai-search.md)
- [Deploy a hosted agent](../deploy-hosted-agent.md)
- [Add a connection to your project](../../../how-to/connections-add.md)
