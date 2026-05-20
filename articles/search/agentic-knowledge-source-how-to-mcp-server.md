---
title: Create an MCP Server Knowledge Source
description: Learn how to create an MCP Server knowledge source for agentic retrieval in Azure AI Search, which connects to any external Model Context Protocol server.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create an MCP Server knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API version. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> These 2026-05-01-preview features and functionality support connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.

An *MCP Server knowledge source* (preview) connects your agentic retrieval pipeline to any external system that exposes a [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP)–compatible endpoint. Use this knowledge source to reach internal tools, third-party APIs, or custom backends that Azure AI Search doesn't natively support.

Unlike indexed knowledge sources, MCP Server knowledge sources query live data directly at retrieval time. No ingestion pipeline is needed. You provide the MCP server URL and specify which tools to allow, and Azure AI Search calls those tools on each query.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ An MCP server with one or more tools. The server must be reachable from Azure AI Search over HTTPS. For testing, you can use the public Microsoft Learn MCP server at `https://learn.microsoft.com/api/mcp`.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Limitations and considerations

+ The `minimal` [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) isn't supported. Use `low` or `medium` instead.

+ `alwaysQuerySource` isn't supported on retrieve requests that reference an MCP Server knowledge source.

+ MCP server tool calls involve external network requests and can take longer than typical search queries. Set `maxRuntimeInSeconds` on retrieve requests to give all configured tools sufficient time to respond.

## Check for existing knowledge sources

[!INCLUDE [](./includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for an MCP Server knowledge source.

```json
{
  "name": "my-mcp-server-ks",
  "kind": "mcpServer",
  "description": "An MCP Server knowledge source.",
  "encryptionKey": null,
  "mcpServerParameters": {
    "serverURL": "https://learn.microsoft.com/api/mcp",
    "authentication": null,
    "tools": [
      {
        "name": "microsoft_docs_search",
        "inclusionMode": null,
        "maxOutputTokens": null,
        "outputParsing": {
          "kind": "auto",
          "jsonParameters": null,
          "splitParameters": null
        }
      }
    ]
  }
}
```

## Create a knowledge source

Run the following code to create an MCP Server knowledge source.

::: zone pivot="csharp"

```csharp
using Azure;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

Uri searchEndpoint = new Uri("<search-service-url>");
AzureKeyCredential credential = new AzureKeyCredential("<api-key>");
var indexClient = new SearchIndexClient(searchEndpoint, credential);

var knowledgeSource = new McpServerKnowledgeSource("<knowledge-source-name>")
{
    Description = "An MCP Server knowledge source.",
    McpServerParameters = new McpServerParameters(
        serverUrl: "https://learn.microsoft.com/api/mcp",
        tools: new[]
        {
            new McpServerTool("microsoft_docs_search")
            {
                OutputParsing = new McpServerToolOutputParsing { Kind = McpServerToolOutputParsingKind.Auto },
                InclusionMode = McpServerToolInclusionMode.Reranked,
                MaxOutputTokens = 1000
            }
        })
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    McpServerKnowledgeSource,
    McpServerParameters,
    McpServerTool,
    McpServerToolOutputParsing,
)

index_client = SearchIndexClient(
    endpoint="<search-service-url>",
    credential=AzureKeyCredential("<api-key>")
)

knowledge_source = McpServerKnowledgeSource(
    name="<knowledge-source-name>",
    description="An MCP Server knowledge source.",
    mcp_server_parameters=McpServerParameters(
        server_url="https://learn.microsoft.com/api/mcp",
        tools=[
            McpServerTool(
                name="microsoft_docs_search",
                output_parsing=McpServerToolOutputParsing(kind="auto"),
                inclusion_mode="reranked",
                max_output_tokens=1000
            )
        ]
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient?view=azure-python-preview&preserve-view=true)

::: zone-end

::: zone pivot="rest"

```http
### Create an MCP Server knowledge source
PUT {{search-url}}/knowledgesources/my-mcp-server-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json
Prefer: return=representation

{
  "name": "my-mcp-server-ks",
  "kind": "mcpServer",
  "description": "An MCP Server knowledge source.",
  "encryptionKey": null,
  "mcpServerParameters": {
    "serverURL": "https://learn.microsoft.com/api/mcp",
    "tools": [
      {
        "name": "microsoft_docs_search",
        "outputParsing": {
          "kind": "auto"
        },
        "inclusionMode": "reranked",
        "maxOutputTokens": 1000
      }
    ]
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

### Source-specific properties

The following properties apply to MCP Server knowledge sources.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `mcpServer` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `mcpServerParameters` | Parameters specific to MCP Server knowledge sources: `serverURL`, `authentication`, and `tools`. | Object | No | Yes |
| `serverURL` | The URL of the MCP server. | String | No | Yes |
| `authentication` | Authentication credentials for the MCP server. If omitted, requests are sent without authentication. For supported authentication options, see [Authentication options](#authentication-options). | Object | Yes | No |
| `tools` | An array of tools to allow from the MCP server. Must contain at least one entry. Each tool name must be unique within the list and must match a tool exposed by the MCP server. The knowledge source doesn't automatically allow all MCP server tools, so you must explicitly list each tool that is allowed. For supported tool properties, see [Tool properties](#tool-properties). | Array | Yes | Yes |

### Authentication options

If your MCP server requires authentication, use one of the following options.

# [foundryConnection](#tab/foundry-connection)

Use `foundryConnection` to authenticate with credentials managed by Microsoft Foundry, which manages the full authentication lifecycle and injects the required credentials at query time. We recommend this option for production scenarios.

```json
"authentication": {
  "kind": "foundryConnection",
  "foundryConnectionParameters": {
    "connectionId": "<your-foundry-connection-id>"
  }
}
```

# [storedHeaders](#tab/stored-headers)

Use `storedHeaders` to send static HTTP headers with every MCP request. We recommend this option for static, long-lived credentials, such as API keys. Stored headers aren't intended for per-user credentials or rotating tokens.

```json
"authentication": {
  "kind": "storedHeaders",
  "storedHeadersParameters": {
    "headers": {
      "x-api-key": "<your-api-key>"
    }
  }
}
```

> [!NOTE]
> Header values are write-only. When you retrieve the knowledge source definition, header values appear masked in the response.

---

### Tool properties

Each entry in the `tools` array is an `McpServerTool` object with the following properties.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the MCP tool to invoke. Must match a tool name exposed by the MCP server. | String | No | Yes |
| `outputParsing` | Controls how the tool's raw output is parsed into rankable documents. Defaults to `auto`. For supported output parsing modes, see [Output parsing modes](#output-parsing-modes). | Object | No | No |
| `inclusionMode` | Controls whether the tool's results are included only when ranked highly (`reranked`) or always regardless of relevance score (`always`). Defaults to `reranked`. | String | Yes | No |
| `maxOutputTokens` | Maximum number of tokens to retain from the tool output before ranking. Defaults to 10,000. | Integer | No | No |

### Output parsing modes

By default, the retrieval engine applies automatic heuristics (`auto`) to convert raw MCP tool output into rankable documents. You can override this behavior per tool using the `outputParsing` property.

# [auto](#tab/auto)

The `auto` mode requires no configuration. The retrieval engine applies heuristics to parse the tool output.

# [json](#tab/json)

The `json` mode extracts documents from a specific location in the JSON output using a JSONPath expression. Use this mode when your tool returns a structured JSON response with a predictable array field.

```json
"outputParsing": {
  "kind": "json",
  "jsonParameters": {
    "documentsPath": "$.results[*]",
    "includeContext": false
  }
}
```

| Name | Description | Type | Required |
|--|--|--|--|
| `documentsPath` | A [JSONPath](https://goessner.net/articles/JsonPath/) expression that resolves to an array in the tool output. Each element in the array becomes a rankable document. | String | Yes |
| `includeContext` | Whether to include the full JSON response alongside each extracted document as additional context. Defaults to `false`. | Boolean | No |

# [split](#tab/split)

The `split` mode chunks large text, HTML, or Markdown output into smaller segments. Use this mode when a tool returns long-form content. This mode supports the same parameters as the [Text Split skill](cognitive-search-skill-textsplit.md#skill-parameters).

```json
"outputParsing": {
  "kind": "split",
  "splitParameters": {
    "textSplitMode": "pages",
    "maximumPageLength": 2000,
    "pageOverlapLength": 200
  }
}
```

# [none](#tab/none)

The `none` mode requires no configuration. The entire tool output is treated as a single document. Use this mode when the raw output doesn't require splitting or structured extraction.

---

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query MCP server content. MCP Server knowledge sources have source-specific retrieval behavior and response fields.

### How retrieval works for MCP Server knowledge sources

At query time, the large language model (LLM) configured in the knowledge base reviews the configured tools, selects which ones to call based on the user query, and generates the arguments for each call. Azure AI Search then invokes the selected tools on the MCP server and returns the results as ranked references.

### MCP Server–specific response fields

MCP Server knowledge sources return per-document citations in the `references` array and per-invocation diagnostics in the `activity` array. If the knowledge source lists multiple tools and the model selects more than one, a separate activity record appears for each invocation.

The following example shows a retrieve response containing an MCP Server knowledge source reference and its corresponding activity record. For broader guidance on interpreting retrieve responses, see [Review the response](agentic-retrieval-how-to-retrieve.md#review-the-response).

> [!TIP]
> To receive `sourceData` for references, set `includeReferenceSourceData` to `true` on the knowledge source entry within `knowledgeSourceParams` on the retrieve request.

```json
{
  "response": [
      // ... Response omitted for brevity
  ],
  "activity": [
    {
      "type": "mcpServer",
      "id": 1,
      "knowledgeSourceName": "my-mcp-server-ks",
      "queryTime": "2026-05-11T15:42:33.0888894Z",
      "count": 10,
      "elapsedMs": 768,
      "mcpServerArguments": {
        "toolName": "microsoft_docs_search",
        "toolArguments": {
          "query": "Azure AI Search features"
        }
      }
    },
    {
      // ... Additional activity records omitted for brevity
    }
  ],
  "references": [
    {
      "type": "mcpServer",
      "id": "0",
      "activitySource": 1,
      "sourceData": {
        "title": "What is a knowledge source?",
        "content": "..."
      },
      "rerankerScore": 2.96,
      "toolName": "microsoft_docs_search",
      "title": "my-mcp-server-ks microsoft_docs_search 1"
    },
    {
      // ... Additional references omitted for brevity
    }
  ]
}
```

## Delete a knowledge source

[!INCLUDE [](./includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
