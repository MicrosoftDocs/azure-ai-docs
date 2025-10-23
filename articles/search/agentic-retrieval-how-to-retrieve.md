---
title: Use a knowledge agent to retrieve data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/29/2025
---

# Retrieve data using a knowledge agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query architecture that uses a large language model (LLM) for query planning. It generates subqueries that broaden the scope of what's searchable and relevant. It incorporates chat history for context. The LLM studies the query and subdivides it into more targeted queries, using different phrases and terminology for subquery composition.

This article explains how to use the [**retrieve action**](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) that invokes a knowledge agent and parallel query processing. It's updated for the new 2025-08-01-preview, which introduces breaking changes from the 2025-05-01-preview. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

This article also explains the three components of the retrieval response: 

+ *extracted response for the LLM*
+ *referenced results*
+ *query activity*

The retrieve request can include instructions for query processing that override the defaults set on the knowledge agent.

> [!NOTE]
> By default, there's no model-generated "answer" in the response and you should pass the extracted response to an LLM so that it can ground its answer based on the search results. For an end-to-end example that includes this step, see [Tutorial: Build an agent-to-agent retrieval solution ](agentic-retrieval-how-to-create-pipeline.md) or [Azure OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo).
>
>Alternatively, you can use [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) to bring answer formulation into the agentic pipeline. In this workflow, the retriever response consists of LLM-formulated answers instead of the raw search results.

## Prerequisites

+ A *knowledge source* that wraps a searchable index. It's either a [search index knowledge source](agentic-knowledge-source-how-to-search-index.md) or a [blob knowledge source](agentic-knowledge-source-how-to-blob.md).

+ A [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md) that represents the chat completion model and one or more knowledge sources.

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md), on Basic pricing tier and higher. Your search service must have a [managed identity](search-how-to-managed-identities.md) for role-based access to a chat completion model.

+ Permissions on Azure AI Search. **Search Index Data Reader** can run queries on Azure AI Search, but the search service managed identity must have **Cognitive Services User** permissions on the Azure OpenAI resource. For more information about local testing and obtaining access tokens, see [Quickstart: Connect without keys](search-get-started-rbac.md).

+ API requirements. To create or use a knowledge agent, use the [2025-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) data plane REST API. Or, use a prerelease package of an Azure SDK that provides knowledge agent APIs: [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Azure SDK for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search. There's no portal support at this time.

## Call the retrieve action

Call the **retrieve** action on the knowledge agent object to invoke retrieval and return a response. Use the [2025-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-08-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

All `searchable` fields in the search index are in-scope for query execution. If the index includes vector fields, your index should have a valid [vectorizer definition](vector-search-how-to-configure-vectorizer.md) so that it can vectorize the query inputs. Otherwise, vector fields are ignored. The implied query type is `semantic`, and there's no search mode or selection of search fields.

The input for the retrieval route is chat conversation history in natural language, where the `messages` array contains the conversation.

```http
@search-url=<YOUR SEARCH SERVICE URL>
@accessToken=<YOUR PERSONAL ID>

# Send grounding request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-08-01-preview
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

**Key points**:

+ The retrieve action targets a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md). The knowledge agent specifies one or more knowledge sources and a knowledge source configuration. Review your knowledge agent definition for output and semantic ranking configuration.

+ `messages` articulates the messages sent to the model. The message format is similar to Azure OpenAI APIs.

  + `role` defines where the message came from, for example either `assistant` or `user`. The model you use determines which roles are valid.

  + `content` is the message or prompt sent to the LLM. It must be text in this preview.

+ [`knowledgeSourceParams`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview#searchindexknowledgesourceparams&preserve-view=true) is optional. Specify a knowledge source if the agent has more than one, and you want to focus the retrieve action on just one knowledge source. If the knowledge agent has just one knowledge source with the configuration you want, you can omit this section.

  A knowledge source specification on the retrieve action describes the target search index on the search service. So even if the knowledge source "kind" is Azure blob, the valid value here is `searchIndex`. In this first public preview release, `knowledgeSourceParams.kind` is always `searchIndex`.

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
> The `maxOutputSize` property on the [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md) determines the length of the string. We recommend 5,000 tokens.

## Review the activity array

The activity array outputs the query plan and it helps you keep track of the operations performed when executing the request. It provides transparency of operations so that you can understand billing implications and the frequency of resource invocations.

Output includes:

+ Token used for input
+ Token counts for output
+ Subqueries sent to the retrieval pipeline
+ Result count per subquery
+ Filters on the subquery, if applicable
+ Token counts used for ranking and extraction

Here's an example of an activity array.

```json
"activity": [
    {
      "type": "ModelQueryPlanning",
      "id": 0,
      "inputTokens": 1261,
      "outputTokens": 270
    },
    {
      "type": "AzureSearchQuery",
      "id": 1,
      "targetIndex": "earth_at_night",
      "query": {
        "search": "suburban belts December brightening urban cores comparison",
        "filter": null
      },
      "queryTime": "2025-05-30T21:23:25.944Z",
      "count": 0,
      "elapsedMs": 600
    },
    {
      "type": "AzureSearchQuery",
      "id": 2,
      "targetIndex": "earth_at_night",
      "query": {
        "search": "Phoenix nighttime street grid visibility from space",
        "filter": null
      },
      "queryTime": "2025-05-30T21:23:26.128Z",
      "count": 2,
      "elapsedMs": 161
    },
    {
      "type": "AzureSearchQuery",
      "id": 3,
      "targetIndex": "earth_at_night",
      "query": {
        "search": "interstate visibility from space midwestern cities",
        "filter": null
      },
      "queryTime": "2025-05-30T21:23:26.277Z",
      "count": 0,
      "elapsedMs": 147
    },
    {
      "type": "AzureSearchSemanticRanker",
      "id": 4,
      "inputTokens": 2622
    }
  ],
```

## Review the references array

The `references` array is a direct reference from the underlying grounding data and includes the `sourceData` used to generate the response. It consists of every single document that was found and semantically ranked by the search engine. Fields in the `sourceData` include an `id` and semantic fields: `title`, `terms`, `content`.

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

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
