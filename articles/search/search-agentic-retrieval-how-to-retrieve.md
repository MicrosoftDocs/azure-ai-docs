---
title: Use an agent to retrieve data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 05/05/2025
---

# Retrieve data using an agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query architecture that uses a conversational large language model (LLM) for query planning, generating subqueries that broaden the scope of what's searchable and relevant.

This article explains how to use the [**retrieve** method](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-05-01-preview&preserve-view=true) that invokes an agent and parallel query processing. This article also explains the three components of the retrieval response: 

+ *extracted response for the LLM*
+ *referenced results*
+ *query activity*

> [!NOTE]
> Currently, there's no model-generated "answer" in the response. Instead, the response provides grounding data that you can use to generate an answer from an LLM. For an end-to-end example, see [Build an agent-to-agent retrieval solution ](search-agentic-retrieval-how-to-pipeline.md) or [Azure OpenAI Demo](https://github.com/Azure-Samples/azure-search-openai-demo).

## Prerequisites

+ An [agent definition](search-agentic-retrieval-how-to-create.md) that represents a conversational language model.

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md), on basic tier and above. Your search service must have a [managed identity](search-howto-managed-identities-data-sources.md) for role-based access to a chat model.

+ API requirements. Use 2025-05-01-preview data plane REST API or a prerelease package of an Azure SDK that provides Agent APIs.

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search. There's no portal support at this time.

## Call the retrieve action

Call the **retrieve** action on the agent object to invoke retrieval and return a response. Use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

The input for the retrieval route is chat conversation history in natural language, where the `messages` array contains the conversation.

```http
# Send Grounding Request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-05-01-preview
api-key: {{search-api-key}}
Content-Type: application/json

{
    "messages" : [
            {
                "role" : "system",
                "content" : [
                  { "type" : "text", "text" : "You are a helpful assistant for Contoso Human Resources. You have access to a search index containing guidelines about health care coverage for Washington state. If you can't find the answer in the search, say you don't know." }
                ]
            },
            {
                "role" : "user",
                "content" : [
                  { "type" : "text", "text" : "What are my vision benefits?" }
                ]
            }
        ],
    "targetIndexParams" :  [
        { 
            "indexName" : "{{index-name}}",
            "filterAddOn" : "State eq 'WA'",
            "IncludeReferenceSourceData": true, 
            "rerankerThreshold " : 2.5,
            "maxDocsForReranker": 250
        } 
    ]
}
```

**Key points**:

+ `messages` articulates the messages sent to the model. The message format is similar to Azure OpenAI APIs.

  + `role` defines where the message came from, for example either `system` or `user`. The model you use determines which roles are valid.

  + `content` is the message sent to the LLM. It must be text in this preview.

+ `targetIndexParams` provide instructions on the retrieval. Currently in this preview, you can only target a single index. 

  + `filterAddOn` lets you set an [OData filter expression](search-filters.md) for keyword or hybrid search.

  + `IncludeReferenceSourceData` is initially set in the agent definition. You can override that setting in the retrieve action to return grounding data in the [references section](#review-the-references-array) of the response.

  + `rerankerThreshold` and `maxDocsForReranker` are also initially set in the agent definition as defaults. You can override them in the retrieve action to configure [semantic reranker](semantic-how-to-configure.md), setting minimum thresholds and the maximum number of inputs sent to the reranker.

    `rerankerThreshold` is the minimum semantic reranker score that's acceptable for inclusion in a response. [Reranker scores](semantic-search-overview.md#how-ranking-is-scored) range from 1 to 4. Plan on revising this value based on testing and what works for your content.

    `maxDocsForReranker` dictates the maximum number of documents to consider for the final response string. Semantic reranker accepts 50 documents. If the maximum is 200, four more subqueries are added to the query plan to ensure all 200 documents are semantically ranked. for semantic ranking. If the number isn't evenly divisible by 50, the query plan rounds up to nearest whole number.

## Review the extracted response

The *extracted response* is single unified string that's typically passed to an LLM that consumes it as grounding data, using it to formulate a response. Your API call to the LLM includes the unified string and instructions for model, such as whether to use the grounding exclusively or as a supplement.

The body of the response is also structured in the chat message style format. Currently in this preview release, the content is serialized JSON.

```http
"response": [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "[{\"ref_id\":0,\"title\":\"Vision benefits\",\"terms\":\"exams, frames, contacts\",\"content\":\"<content chunk>\"}]"
            }
        ]
    }
]
```

`content` is a JSON array. It's a single string composed of the most relevant documents (or chunks) found in the search index, given the query and chat history inputs. This array is your grounding data that a conversational language model uses to formulate a response to the user's question.

The `maxOutputSize` property on the agent determines the length of the string. We recommend 5,000 tokens.

Fields in the content `text` response string include the ref_id and semantic configuration fields: `title`, `terms`, `terms`.

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
      "inputTokens": 1308,
      "outputTokens": 141
    },
    {
      "type": "AzureSearchQuery",
      "id": 1,
      "targetIndex": "myindex",
      "query": {
        "search": "hello world programming",
        "filter": null
      },
      "queryTime": "2025-04-25T16:40:08.811Z",
      "count": 2,
      "elapsedMs": 867
    },
    {
      "type": "AzureSearchQuery",
      "id": 2,
      "targetIndex": "myindex",
      "query": {
        "search": "hello world meaning",
        "filter": null
      },
      "queryTime": "2025-04-25T16:40:08.955Z",
      "count": 2,
      "elapsedMs": 136
    }
  ],
```

## Review the references array

The `references` array is a direct reference from the underlying grounding data and includes the `sourceData` used to generate the response. It consists of every single document that was found and semantically ranked by the search engine. Fields in the `sourceData` include an `id` and semantic fields: `title`, `terms`, `content`.

The purpose of this array is to provide a chat message style structure for easy integration. For example, if you want to serialize the results into a different structure or you require some programmatic manipulation of the data before you returned it to the user.

You can also get the structured data from the source data object in the references array to manipulate it however you see fit.

Here's an example of the references array.

```json
  "references": [
    {
      "type": "AzureSearchDoc",
      "id": "0",
      "activitySource": 2,
      "docKey": "2",
      "sourceData": {
        "id": "2",
        "parent": {
          "title": null,
          "content": "good by cruel world"
        }
      }
    },
    {
      "type": "AzureSearchDoc",
      "id": "1",
      "activitySource": 2,
      "docKey": "4",
      "sourceData": {
        "id": "4",
        "parent": {
          "title": "zzzzzzz",
          "content": "zzzzzzz"
        }
      }
    }
  ]
```

<!-- Create H2s for the main patterns. -->
<!-- This section is in progress. It needs a code sample for the simple case showing how to pipeline ground data to chat completions and responses -->
## Use data for grounding

The `includeReferenceSourceData` parameter tells the search engine to provide grounding data to the search agent.

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
