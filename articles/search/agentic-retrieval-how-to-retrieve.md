---
title: Use a knowledge base to retrieve data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
---

# Retrieve data using a knowledge base in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In an agentic retrieval multi-query pipeline, query execution is through the [**retrieve action**](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) on a knowledge base that invokes parallel query processing. This request structure is updated for the new 2025-11-01-preview, which introduces breaking changes from previous previews. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

This article explains how to set up a retrieve action. It also covers the three components of the retrieval response: 

+ *extracted response for the LLM*
+ *referenced results*
+ *query activity*

A retrieve request can include instructions for query processing that override the default instructions set on the knowledge base. A retrieve action has core parameters that are supported on any request, plus parameters that are specific to a knowledge source.

## Prerequisites

+ A [supported knowledge source](agentic-knowledge-source-overview.md#supported-knowledge-sources) that wraps a searchable index or points to an external source for native data retrieval.

+ A [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) represents one or more knowledge sources, plus a chat completion model if you want intelligent query planning and answer formulation.

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md).

+ Permissions on Azure AI Search. Roles for retrieving content include **Search Index Data Reader** for running queries. To support an outbound call from a search service to a chat completion model, you must configure a managed identity for the search service, and it must have **Cognitive Services User** permissions on the Azure OpenAI resource. For more information about local testing and obtaining access tokens, see [Quickstart: Connect without keys](search-get-started-rbac.md).

+ API version requirements. To create or use a knowledge base, use the [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) data plane REST API. Or, use a preview package of an Azure SDK that provides knowledge base APIs: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search.

> [!NOTE]
> Although you can use the Azure portal to retrieve data from knowledge bases, the portal uses the 2025-08-01-preview, which uses the previous "knowledge agent" terminology and doesn't support all 2025-11-01-preview features. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

## Set up the retrieve action

A retrieve action is specified on a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md). The knowledge base has one or more knowledge sources. Retrieval can return a synthesized answer in natural language or raw grounding chunks from the knowledge sources.

+ Review your knowledge base definition to understand which knowledge sources are in scope.

+ Review your knowledge sources to understand their parameters and configuration.

+ Use the [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) data plane REST API or an Azure SDK preview package to call retrieve.

For knowledge sources that have default retrieval instructions, you can override the defaults in the retrieve request.

### Retrieval from a search index

For knowledge sources that target a search index, all `searchable` fields are in-scope for query execution. If the index includes vector fields, your index should have a valid [vectorizer definition](vector-search-how-to-configure-vectorizer.md) so that the agentic retrieval engine can vectorize the query inputs. Otherwise, vector fields are ignored. The implied query type is `semantic`, and there's no search mode.

The input for the retrieval route is chat conversation history in natural language, where the `messages` array contains the conversation. Messages are only supported if the [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) is either low or medium.

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

### Responses

Successful retrieval returns a `200 OK` status code. If the knowledge base fails to retrieve from one or more knowledge sources, a `206 Partial Content` status code is returned, and the response only includes results from sources that succeeded. Details about the partial response appear as [errors in the activity array](#review-the-activity-array).

### Retrieve parameters

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `messages` | Articulates the messages sent to a chat completion model. The message format is similar to Azure OpenAI APIs. | Object | Yes | No |
| `role` | Defines where the message came from, for example either `assistant` or `user`. The model you use determines which roles are valid. | String | Yes | No |
| `content` | The message or prompt sent to the LLM. It must be text in this preview. | String | Yes | No |
| [`knowledgeSourceParams`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#searchindexknowledgesourceparams&preserve-view=true) | Specifies parameters for each knowledge source if you want to customize the query or response at query time. | Object | Yes | No |

## Examples

Retrieve requests vary depending on the knowledge sources and whether you want to override a default configuration. Here are several examples that illustrate a range of requests.

### Example: Override default reasoning effort and set request limits

This example specifies [answer formulation](agentic-retrieval-how-to-answer-synthesis.md), so `retrievalReasoningEffort` must be "low" or "medium".

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

### Example: Set references for each knowledge source

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
            "knowledgeSourceName": "demo-healthcare=ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": false,
            "alwaysQuerySource": true
        }
    ]
}
```

> [!NOTE]
> If you're retrieving content from a OneLake or indexed SharePoint knowledge source, set `includeReferenceSourceData` to `true` to include the source document URL in the citation.

### Example: minimal reasoning effort

In this example, there's no chat completion model for intelligent query planning or answer formulation. The query string is passed to the agentic retrieval engine for keyword search or hybrid search.

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

## Review the extracted response

The *extracted response* is single unified string that's typically passed to an LLM that consumes it as grounding data, using it to formulate a response. Your API call to the LLM includes the unified string and instructions for model, such as whether to use the grounding exclusively or as a supplement.

The body of the response is also structured in the chat message style format. Currently in this preview release, the content is serialized JSON.

```http
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

**Key points**:

+ `content.text` is a JSON array. It's a single string composed of the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This array is your grounding data that a chat completion model uses to formulate a response to the user's question.

  This portion of the response consists of the 200 chunks or less, excluding any results that fail to meet the minimum threshold of a 2.5 reranker score.

  The string starts with the reference ID of the chunk (used for citation purposes), and any fields specified in the semantic configuration of the target index. In this example, you should assume the semantic configuration in the target index has a "title" field, a "terms" field, and a "content" field.

+ `content.type` has one valid value in this preview: `text`. 

> [!NOTE]
> The `maxOutputSize` property on the [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) determines the length of the string.

## Review the activity array

The activity array outputs the query plan, which helps you track the operations performed when executing the request. It also provides operational transparency so you can understand the billing implications and frequency of resource invocations.

The output includes the following components.

| Section | Description |
|---------|-------------|
| modelQueryPlanning | For knowledge bases that use an LLM for query planning, this section reports on the token counts used for input, and the token count for the subqueries. |
| source-specific activity | For each knowledge source included in the query, report on elapsed time and which arguments were used in the query, including the semantic ranker. Knowledge source types include `searchIndex`, `azureBlob`, and other [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). |
| agenticReasoningEffort | For each retrieve action, you can specify the degree of LLM support. Use minimal to bypass an LLM, low for constrained LLM processing, and medium for full LLM processing. | 
| modelAnswerSynthesis | For knowledge bases that specify answer formulation, this section reports on the token count for formulating the answer, and the token count of the answer output. |

Output reports on the token consumption for agentic reasoning during retrieval at the specified [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).

Output also includes the following information:

+ Subqueries sent to the retrieval pipeline.
+ Errors for any retrieval failures, such as inaccessible knowledge sources.

Here's an example of an activity array.

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


## Review the references array

The `references` array is a direct reference from the underlying grounding data and includes the `sourceData` used to generate the response. It consists of every single document that was found and semantically ranked by the agentic retrieval engine. Fields in the `sourceData` include an `id` and semantic fields: `title`, `terms`, `content`.

The `id` is a reference ID for an item within a specific response. It's not the document key in the search index. It's used for providing citations.

The purpose of this array is to provide a chat message style structure for easy integration. For example, if you want to serialize the results into a different structure or you require some programmatic manipulation of the data before you returned it to the user.

You can also get the structured data from the source data object in the references array to manipulate it however you see fit.

Here's an example of the references array.

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

> [!NOTE]
> If you're retrieving content from a OneLake or indexed SharePoint knowledge source, set `includeReferenceSourceData` to `true` on the retrieve request to get the source document URL in the citation.

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
