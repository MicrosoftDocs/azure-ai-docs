---
title: Use Knowledge Base to Retrieve Data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 02/12/2026
ai-usage: ai-assisted
---

# Use a knowledge base to retrieve data in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In an agentic retrieval pipeline, the [retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) invokes parallel query processing from a knowledge base. This article explains how to call the retrieve action and interpret the three-pronged response.

You can call the retrieve action directly using the Search Service REST APIs or an Azure SDK that provides equivalent functionality. Each knowledge base also exposes a Model Context Protocol (MCP) endpoint for consumption by MCP-compatible agents.

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ Permissions to query the knowledge base. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Index Data Reader** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

+ The [2025-11-01-preview](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) REST API or an equivalent Azure SDK preview package: [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

## Call the retrieve action

You specify the retrieve action on a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md). The input is chat conversation history in natural language, where the `messages` array contains the conversation. The agentic retrieval engine supports messages only if the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) is low or medium.

Here's an example using [Knowledge Retrieval - Retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) (REST API):

```http
@search-url=<YOUR SEARCH SERVICE URL>
@accessToken=<YOUR PERSONAL ID>

# Send grounding request
POST https://{{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview
    Content-Type: application/json
    Authorization: Bearer {{accessToken}}

{
    "messages" : [
            {
                "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "You can answer questions about the Earth at night.
                    Sources have a JSON format with a ref_id that must be cited in the answer.
                    If you do not have the answer, respond with 'I do not know'." }
                ]
            },
            {
                "role" : "user",
                "content" : [
                  { "type" : "text", "text" : "Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?" }
                ]
            }
        ],
  "knowledgeSourceParams": [
    {
      "filterAddOn": null,
      "knowledgeSourceName": "earth-at-night-blob-ks",
      "kind": "searchIndex"
    }
  ]
}
```

### Request parameters

Pass the following parameters to call the retrieve action.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| [`messages`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgebasemessage) | Articulates the messages sent to an LLM. The message format is similar to Azure OpenAI APIs. | Object | Yes | No |
| `messages.role` | Defines where the message came from, such as `assistant` or `user`. The model you use determines which roles are valid. | String | Yes | No |
| `messages.content` | The message or prompt sent to the LLM. In this preview, it must be text. | String | Yes | No |
| [`knowledgeSourceParams`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true#knowledgebaseretrievalrequest) | Overrides default retrieval settings per knowledge source. Useful for customizing the query or response at query time. | Object | Yes | No |

### Retrieval from a search index

For knowledge sources that target a search index, all `searchable` fields are in scope for query execution. The implied query type is `semantic`, and there's no search mode.

If the index includes vector fields, you need a valid [vectorizer definition](vector-search-how-to-configure-vectorizer.md) so the agentic retrieval engine can vectorize query inputs. Otherwise, vector fields are ignored.

## Call the MCP endpoint

[MCP](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI applications connect to external data sources and tools.

In Azure AI Search, each knowledge base is a standalone MCP server that exposes the `knowledge_base_retrieve` tool. Any MCP-compatible client, including [Foundry Agent Service](/azure/ai-foundry/agents/overview), [GitHub Copilot](https://github.com/features/copilot), [Claude](https://claude.ai), and [Cursor](https://cursor.com), can invoke this tool to query the knowledge base.

### MCP endpoint format

Each knowledge base has an MCP endpoint at the following URL:

```
https://<your-service-name>.search.windows.net/knowledgebases/<your-knowledge-base-name>/mcp?api-version=2025-11-01-preview
```

### Authenticate to the MCP endpoint

The MCP endpoint requires authentication via custom headers. You have two options:

+ Pass a query key (recommended) or an admin key in the `api-key` header. The key grants read-only access, so no role assignment is needed. For more information, see [Connect to Azure AI Search using API keys](search-security-api-keys.md).

+ (Recommended) Pass a bearer token in the `Authorization` header. The identity behind the token must have the **Search Index Data Reader** role assigned on the search service. This approach avoids storing keys in configuration files. For more information, see [Connect your app to Azure AI Search using identities](search-security-rbac-client-code.md).

> [!TIP]
> Each MCP client configures custom headers differently. For example:
>
> + In [Foundry Agent Service](/azure/ai-foundry/agents/how-to/foundry-iq-connect), you configure authentication via a project connection and add the MCP tool to an agent. The service automatically injects the required headers on MCP requests.
>
> + In [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/extend-copilot-chat-with-mcp), [Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop), and similar clients, you configure headers in the MCP server JSON, such as `mcp.json`.

## Review the response

Successful retrieval returns a `200 OK` status code. If the knowledge base fails to retrieve from one or more knowledge sources, a `206 Partial Content` status code returns. The response only includes results from sources that succeeded. Details about the partial response appear as errors in the activity array.

The retrieve action returns three main components:

+ [Extracted response](#extracted-response) or [synthesized answer](agentic-retrieval-how-to-answer-synthesis.md) (depending on output mode)
+ [Activity array](#activity-array)
+ [References array](#references-array)

### Extracted response

The extracted response is a single unified string that you typically pass to an LLM. The LLM consumes it as grounding data and uses it to formulate a response. Your API call to the LLM includes the unified string and instructions for the model, such as whether to use the grounding exclusively or as a supplement.

The body of the response is also structured in the chat message style format. In this preview, the content is serialized JSON.

```json
"response": [
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "[{\"ref_id\":0,\"title\":\"Urban Structure\",\"terms\":\"Location of Phoenix, Grid of City Blocks, Phoenix Metropolitan Area at Night\",\"content\":\"<content chunk redacted>\"}]"
            }
        ]
    }
]
```

Key points:

+ `content.text` is a JSON array. It's a single string composed of the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This array is your grounding data that a chat completion model uses to formulate a response to the user's question.

  This portion of the response consists of 200 chunks or fewer, excluding any results that fail to meet the minimum threshold of a 2.5 reranker score.

  The string starts with the reference ID of the chunk (used for citation purposes), and any fields specified in the semantic configuration of the target index. In this example, assume the semantic configuration in the target index has a "title" field, a "terms" field, and a "content" field.

+ In this preview, `content.type` has one valid value: `text`.

+ The `maxOutputSize` property on the [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) determines the length of the string.

### Activity array

The activity array outputs the query plan, which provides operational transparency for tracking operations, billing implications, and resource invocations. It also includes subqueries sent to the retrieval pipeline and errors for any retrieval failures, such as inaccessible knowledge sources.

The output includes the following components:

| Section | Description |
|---------|-------------|
| modelQueryPlanning | For knowledge bases that use an LLM for query planning, this section reports on the token counts used for input, and the token count for the subqueries. |
| source-specific activity | For each knowledge source included in the query, this section reports on elapsed time and which arguments were used in the query, including semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| agenticReasoning | This section reports on token consumption for agentic reasoning during retrieval, which depends on the specified [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). |
| modelAnswerSynthesis | For knowledge bases that use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), this section reports on the token count for formulating the answer, and the token count of the answer output. |

Here's an example of the activity array:

```json
  "activity": [
    {
      "type": "modelQueryPlanning",
      "id": 0,
      "inputTokens": 2302,
      "outputTokens": 109,
      "elapsedMs": 2396
    },
    {
      "type": "searchIndex",
      "id": 1,
      "knowledgeSourceName": "demo-financials-ks",
      "queryTime": "2025-11-04T19:25:23.683Z",
      "count": 26,
      "elapsedMs": 1137,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "searchIndex",
      "id": 2,
      "knowledgeSourceName": "demo-healthcare-ks",
      "queryTime": "2025-11-04T19:25:24.186Z",
      "count": 17,
      "elapsedMs": 494,
      "searchIndexArguments": {
        "search": "List of companies in the financial sector according to SEC GICS classification",
        "filter": null,
        "sourceDataFields": [ ],
        "searchFields": [ ],
        "semanticConfigurationName": "en-semantic-config"
      }
    },
    {
      "type": "agenticReasoning",
      "id": 3,
      "retrievalReasoningEffort": {
        "kind": "low"
      },
      "reasoningTokens": 103368
    },
    {
      "type": "modelAnswerSynthesis",
      "id": 4,
      "inputTokens": 5821,
      "outputTokens": 344,
      "elapsedMs": 3837
    }
  ]
```

### References array

The references array comes directly from the underlying grounding data. It includes the `sourceData` used to generate the response. It consists of every document that the agentic retrieval engine finds and semantically ranks. Fields in the `sourceData` include an `id` and semantic fields: `title`, `terms`, and `content`.

The `id` acts as a reference ID for an item within a specific response. It's not the document key in the search index. You use it for providing citations.

The purpose of this array is to provide a chat message style structure for easy integration. For example, if you want to serialize the results into a different structure or you require some programmatic manipulation of the data before you returned it to the user.

You can also get the structured data from the source data object in the references array to manipulate it however you see fit.

Here's an example of the references array:

```json
  "references": [
    {
      "type": "AzureSearchDoc",
      "id": "0",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_104_verbalized",
      "sourceData": null
    },
    {
      "type": "AzureSearchDoc",
      "id": "1",
      "activitySource": 2,
      "docKey": "earth_at_night_508_page_105_verbalized",
      "sourceData": null
    }
  ]
```

## Examples

The following examples illustrate different ways to call the retrieve action:

+ [Override default reasoning effort and set request limits](#override-default-reasoning-effort-and-set-request-limits)
+ [Set references for each knowledge source](#set-references-for-each-knowledge-source)
+ [Use minimal reasoning effort](#use-minimal-reasoning-effort)

### Override default reasoning effort and set request limits

This example specifies [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), so `retrievalReasoningEffort` must be "low" or "medium".

```http
POST {{url}}/knowledgebases/kb-override/retrieve?api-version={{api-version}}
api-key: {{key}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "retrievalReasoningEffort": { "kind": "low" },
    "outputMode": "answerSynthesis",
    "maxRuntimeInSeconds": 30,
    "maxOutputSize": 6000
}
```

### Set references for each knowledge source

This example uses the default reasoning effort specified in the knowledge base. The focus of this example is specification of how much information to include in the response.

```http
POST {{url}}/knowledgebases/kb-medium-example/retrieve?api-version={{api-version}}
api-key: {{key}}
Content-Type: application/json

{
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": "What companies are in the financial sector?" }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "demo-financials-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": true
        },
        {
            "knowledgeSourceName": "demo-communicationservices-ks",
            "kind": "searchIndex",
            "includeReferences": false,
            "includeReferenceSourceData": false
        },
        {
            "knowledgeSourceName": "demo-healthcare-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": false,
            "alwaysQuerySource": true
        }
    ]
}
```


> [!NOTE]
> For indexed OneLake or indexed SharePoint knowledge sources, set `includeReferenceSourceData` to `true` to include source document URLs in citations.

### Use minimal reasoning effort

In this example, there's no LLM for intelligent query planning or answer synthesis. The query string goes to the agentic retrieval engine for keyword search or hybrid search.

```http
POST {{url}}/knowledgebases/kb-minimal/retrieve?api-version={{api-version}}
api-key: {{key}}
Content-Type: application/json

{
    "intents": [
        {
            "type": "semantic",
            "search": "what is a brokerage"
        }
    ]
}
```

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
