---
title: Use a knowledge agent to retrieve data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/08/2025
---

# Retrieve data using a knowledge agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query architecture that uses a large language model (LLM) for query planning. It generates subqueries that broaden the scope of what's searchable and relevant. It incorporates chat history for context. The LLM studies the query and subdivides it into more targeted queries, using different phrases and terminology for subquery composition.

:::image type="content" source="media/agentic-retrieval/agentric-retrieval-example.png" alt-text="Diagram of a complex query with implied context and an intentional typo." lightbox="media/agentic-retrieval/agentric-retrieval-example.png" :::

This article explains how to use the [**retrieve method**](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-05-01-preview&preserve-view=true) that invokes a knowledge agent and parallel query processing. This article also explains the three components of the retrieval response: 

+ *extracted response for the LLM*
+ *referenced results*
+ *query activity*

The retrieve request can include instructions for query processing that override the defaults set on the knowledge agent.

> [!NOTE]
> There's no model-generated "answer" in the response. Instead, you should pass the response to an LLM that grounds its answer based on the content. For an end-to-end example that includes this step, see [Build an agent-to-agent retrieval solution ](search-agentic-retrieval-how-to-pipeline.md) or [Azure OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo).

## Prerequisites

+ A [knowledge agent](search-agentic-retrieval-how-to-create.md) that represents the chat completion model and a valid target index.

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md), on Basic pricing tier and higher. Your search service must have a [managed identity](search-howto-managed-identities-data-sources.md) for role-based access to a chat completion model.

+ Permissions on Azure AI Search. **Search Index Data Reader** can run queries on Azure AI Search, but the search service managed identity must have **Cognitive Services User** permissions on the Azure OpenAI resource. For more information about local testing and obtaining access tokens, see [Quickstart: Connect without keys](search-get-started-rbac.md).

+ API requirements. To create or use a knowledge agent, use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API. Or, use a prerelease package of an Azure SDK that provides knowledge agent APIs: [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [Azure SDK for .NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Azure SDK for Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search. There's no portal support at this time.

## Call the retrieve action

Call the **retrieve** action on the knowledge agent object to invoke retrieval and return a response. Use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

All `searchable` fields in the search index are in-scope for query execution. If the index includes vector fields, your index should have a valid [vectorizer definition](vector-search-how-to-configure-vectorizer.md) so that it can vectorize the query inputs. Otherwise, vector fields are ignored. The implied query type is `semantic`, and there's no search mode or selection of search fields.

The input for the retrieval route is chat conversation history in natural language, where the `messages` array contains the conversation.

```http
@search-url=<YOUR SEARCH SERVICE URL>
@accessToken=<YOUR PERSONAL ID>

# Send grounding request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-05-01-preview
    Content-Type: application/json
    Authorization: Bearer {{accessToken}}

{
    "messages" : [
            {
                "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "You can answer questions about the Earth at night.
                    Sources have a JSON format with a ref_id that must be cited in the answer.
                    If you do not have the answer, respond with "I don't know"." }
                ]
            },
            {
                "role" : "user",
                "content" : [
                  { "type" : "text", "text" : "Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?" }
                ]
            }
        ],
    "targetIndexParams" :  [
        { 
            "indexName" : "{{index-name}}",
            "filterAddOn" : "page_number eq '105'",
            "IncludeReferenceSourceData": true, 
            "rerankerThreshold" : 2.5,
            "maxDocsForReranker": 50
        } 
    ]
}
```

**Key points**:

+ `messages` articulates the messages sent to the model. The message format is similar to Azure OpenAI APIs.

  + `role` defines where the message came from, for example either `assistant` or `user`. The model you use determines which roles are valid.

  + `content` is the message sent to the LLM. It must be text in this preview.

+ `targetIndexParams` provide instructions on the retrieval. Currently in this preview, you can only target a single index. 

  + `filterAddOn` lets you set an [OData filter expression](search-filters.md) for keyword or hybrid search.

  + `IncludeReferenceSourceData` tells the retrieval engine to return the source content in the response. This value is initially set in the knowledge agent definition. You can override that setting in the retrieve action to return original source content in the [references section](#review-the-references-array) of the response.

  + `rerankerThreshold` and `maxDocsForReranker` are also initially set in the knowledge agent definition as defaults. You can override them in the retrieve action to configure [semantic reranker](semantic-how-to-configure.md), setting minimum thresholds and the maximum number of inputs sent to the reranker.

    `rerankerThreshold` is the minimum semantic reranker score that's acceptable for inclusion in a response. [Reranker scores](semantic-search-overview.md#how-ranking-is-scored) range from 1 to 4. Plan on revising this value based on testing and what works for your content.

    `maxDocsForReranker` dictates the maximum number of documents to consider for the final response string. Semantic reranker accepts 50 documents. If the maximum is 200, four more subqueries are added to the query plan to ensure all 200 documents are semantically ranked. for semantic ranking. If the number isn't evenly divisible by 50, the query plan rounds up to nearest whole number. 

    The `content` portion of the response consists of the 200 chunks or less, excluding any results that fail to meet the minimum threshold of a 2.5 reranker score.

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

+ `content` is a JSON array. It's a single string composed of the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This array is your grounding data that a chat completion model uses to formulate a response to the user's question.

+ "text" is the only valid value for `type`, and it consists of the reference ID of the chunk (used for citation purposes), and any fields specified in the semantic configuration of the target index. In this example, you should assume the semantic configuration in the target index has a "title" field, a "terms" field, and a "content" field. 

> [!NOTE]
> The `maxOutputSize` property on the [knowledge agent](search-agentic-retrieval-how-to-create.md) determines the length of the string. We recommend 5,000 tokens.

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

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
