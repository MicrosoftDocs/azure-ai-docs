---
title: Create an MCP Server knowledge source
description: Learn how to create an MCP Server knowledge source for agentic retrieval in Azure AI Search, which connects to any external Model Context Protocol server.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/06/2026
ai-usage: ai-assisted
---

# Create an MCP Server knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

An *MCP Server knowledge source* connects your agentic retrieval pipeline to any external system through the open-source [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP) standard. Use this knowledge source when your data lives in internal tools, third-party APIs, or custom backends that Azure AI Search doesn't natively cover as a first-party knowledge source.

You register an MCP server endpoint and specify which tools to expose. At query time, Azure AI Search calls those tools to fetch live results from the external system and incorporates them in the retrieval response.

## Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2026-05-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

<!-- TO-DO (PM): Confirm portal and SDK support for Build and update this table as needed. -->

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ An external MCP server with one or more tools. The server must be reachable from Azure AI Search over HTTPS. For testing, you can use the public Microsoft Learn MCP server at `https://learn.microsoft.com/api/mcp`.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

+ The [2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true) version of the Search Service REST APIs.

## Check for existing knowledge sources

<!-- TO-DO (writer): Replace with [!INCLUDE [Check for existing knowledge sources using REST](includes/how-tos/knowledge-source-check-rest.md)] when C# and Python are added to this article. -->

A knowledge source is a top-level, reusable object. Knowing about existing knowledge sources is helpful for either reuse or naming new objects.

Run the following code to list knowledge sources by name and type.

```http
### List knowledge sources by name and type
GET {{search-url}}/knowledgesources?api-version=2026-05-01-preview&$select=name,kind
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - List](/rest/api/searchservice/knowledge-sources/list?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

You can also return a single knowledge source by name to review its JSON definition.

```http
### Get a knowledge source definition
GET {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
api-key: {{api-key}}
```

**Reference:** [Knowledge Sources - Get](/rest/api/searchservice/knowledge-sources/get?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

The following JSON is an example response for an MCP Server knowledge source.

```json
{
  "name": "my-mcp-server-ks",
  "kind": "mcpServer",
  "description": "An MCP server knowledge source.",
  "encryptionKey": null,
  "mcpServerParameters": {
    "serverURL": "https://learn.microsoft.com/api/mcp",
    "tools": [
      {
        "name": "microsoft_docs_search",
        "outputParsing": {
          "kind": "auto"
        }
      }
    ]
  }
}
```

## Create a knowledge source

Run the following code to create an MCP Server knowledge source.

```http
### Create an MCP Server knowledge source
PUT {{search-url}}/knowledgesources/my-mcp-server-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json
Prefer: return=representation

{
  "name": "my-mcp-server-ks",
  "kind": "mcpServer",
  "description": "An MCP server knowledge source.",
  "encryptionKey": null,
  "mcpServerParameters": {
    "serverURL": "https://learn.microsoft.com/api/mcp",
    "authentication": {
      "kind": "foundryConnection",
      "foundryConnectionParameters": {
        "connectionId": "<your-foundry-connection-id>"
      }
    },
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

### Source-specific properties

The following properties apply to MCP Server knowledge sources.

<!-- TO-DO (PM): Confirm all property descriptions, Editable values, and Required values in this table before publish. -->

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `mcpServer` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `mcpServerParameters` | Parameters specific to MCP Server knowledge sources: `serverURL`, `authentication`, and `tools`. | Object | No | Yes |
| `serverURL` | The URL of the MCP server endpoint. Must be a valid URI. | String | No | Yes |
| `authentication` | Authentication credentials for the MCP server. If omitted, requests are sent without authentication. For supported authentication options, see [Authentication options](#authentication-options). | Object | Yes | No |
| `tools` | An array of tools to allow from the MCP server. Must contain at least one entry. Each tool name must be unique within the list and must match a tool exposed by the MCP server. Dynamic tool discovery isn't supported in this preview, so you must specify each tool explicitly. For supported tool properties, see [Tool properties](#tool-properties). | Array | No | Yes |

### Authentication options

If your MCP server requires authentication, use one of the following options.

# [foundryConnection](#tab/foundry-connection)

Authenticates using credentials managed by Microsoft Foundry. Foundry handles the full authentication lifecycle, including OAuth flows, API key storage, and token refresh, and injects the required headers at query time. This approach is recommended for production scenarios.

```json
"authentication": {
  "kind": "foundryConnection",
  "foundryConnectionParameters": {
    "connectionId": "<your-foundry-connection-id>"
  }
}
```

# [storedHeaders](#tab/stored-headers)

Sends static HTTP headers with every MCP request. The `headers` object must contain at least one entry. This approach is suitable for long-lived, non-rotating credentials, such as API keys. Stored headers aren't intended for per-user credentials or rotating tokens.

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

Each entry in the `tools` array is a `McpServerTool` object with the following properties.

<!-- TO-DO (PM): Confirm all property descriptions, Editable values, and Required values in this table before publish. Also confirm whether `inclusionMode` and `maxOutputTokens` are part of the feature spec — they appear in the TypeSpec but aren't covered in the 1-pager. -->

| Property | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the MCP tool to invoke. Must match a tool name exposed by the MCP server. | String | No | Yes |
| `outputParsing` | Controls how the tool's raw output is parsed into rankable documents. Defaults to `auto`. For supported output parsing modes, see [Output parsing modes](#output-parsing-modes). | Object | No | No |
| `inclusionMode` | Controls whether the tool's results are included only when ranked highly (`reranked`, default) or always regardless of relevance score (`always`). | String | No | No |
| `maxOutputTokens` | Maximum number of tokens to retain from the tool output before ranking. | Integer | No | No |

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

<!-- TO-DO (PM): Confirm property descriptions and Required values for `jsonParameters`. -->

| Property | Description | Type | Required |
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

> [!IMPORTANT]
> MCP Server knowledge sources don't support the `minimal` retrieval reasoning effort or extractive data. Your knowledge base must use the `low` or `medium` [reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) and [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md).

## Query a knowledge base

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query MCP server content. MCP Server knowledge sources have source-specific retrieval behavior and response fields.

### How MCP server retrieval works

At query time, the retrieval engine discovers tool manifests from the MCP server. The model configured in the knowledge base selects which tools to call and generates the tool inputs based on those manifests and the user query. Results are merged with any other knowledge sources in the knowledge base, reranked, and returned.

> [!TIP]
> MCP tool calls involve external network requests that can take longer than typical search queries. Set `maxRuntimeInSeconds` on the retrieve request to a value that gives all configured tools sufficient time to respond.

### MCP server–specific response fields

MCP Server knowledge sources return per-document citations in the `references` array and per-invocation diagnostics in the `activity` array. If the knowledge source lists multiple tools and the model selects more than one, a separate activity record appears for each invocation.

<!-- TO-DO (PM): Confirm the exact JSON serialization names for all fields in the mcpServer reference object and activity record before publish. The structure below is sourced from the feature 1-pager. Specifically confirm whether `toolOutput` is a valid references field and whether `includeReferenceSourceData` causes it to be returned. -->

The following example shows a retrieve response containing an MCP Server knowledge source reference and its corresponding activity record.

```json
{
  "response": ["..."],
  "references": [
    {
      "type": "mcpServer",
      "id": "ref-01",
      "activitySource": 1,
      "toolName": "microsoft_docs_search",
      "rerankerScore": 0.92
    }
  ],
  "activity": [
    {
      "id": 1,
      "type": "mcpServer",
      "knowledgeSourceName": "my-mcp-server-ks",
      "elapsedMs": 1250,
      "count": 4,
      "mcpServerArguments": {
        "toolName": "microsoft_docs_search",
        "toolArguments": {
          "query": "Azure AI Search features"
        }
      }
    }
  ]
}
```

<!-- TO-DO (PM): Confirm the field name for raw tool output in mcpServer references when `includeReferenceSourceData` is set to `true`. For searchIndex, the spec uses `sourceData`; for mcpServer it may be `sourceData` or a different field. -->

> [!TIP]
> To receive raw tool output in the response, set `includeReferenceSourceData` to `true` in `knowledgeSourceParams` of the retrieve request.

## Delete a knowledge source

<!-- TO-DO (writer): Replace with [!INCLUDE [Delete knowledge source using REST](includes/how-tos/knowledge-source-delete-rest.md)] when C# and Python are added to this article. -->

Before you can delete a knowledge source, you must delete any knowledge base that references it or update the knowledge base definition to remove the reference.

If you try to delete a knowledge source that's in use, the action fails and returns a list of affected knowledge bases.

To delete a knowledge source:

1. Get a list of all knowledge bases on your search service.

    ```http
    ### Get knowledge bases
    GET {{search-url}}/knowledgebases?api-version=2026-05-01-preview&$select=name
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

   An example response might look like the following:

   ```json
    {
        "@odata.context": "https://my-search-service.search.windows.net/$metadata#knowledgebases(name)",
        "value": [
          {
            "name": "my-kb"
          },
          {
            "name": "my-kb-2"
          }
        ]
    }
   ```

1. Get an individual knowledge base definition to check for knowledge source references.

    ```http
    ### Get a knowledge base definition
    GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

   An example response might look like the following:

   ```json
    {
      "name": "my-kb",
      "description": null,
      "retrievalInstructions": null,
      "answerInstructions": null,
      "outputMode": "answerSynthesis",
      "knowledgeSources": [
        {
          "name": "my-mcp-server-ks"
        }
      ],
      "models": [],
      "encryptionKey": null,
      "retrievalReasoningEffort": {
        "kind": "low"
      }
    }
   ```

1. Either delete the knowledge base or, if you have multiple knowledge sources, update the knowledge base to remove the reference. This example shows deletion.

    ```http
    ### Delete a knowledge base
    DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

1. Delete the knowledge source.

    ```http
    ### Delete a knowledge source
    DELETE {{search-url}}/knowledgesources/{{knowledge-source-name}}?api-version=2026-05-01-preview
    api-key: {{api-key}}
    ```

   **Reference:** [Knowledge Sources - Delete](/rest/api/searchservice/knowledge-sources/delete?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

## Related content

+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
