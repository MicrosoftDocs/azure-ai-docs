---
title: Use an agent to retrieve data
titleSuffix: Azure AI Search
description: Set up a retrieval route for agentic retrieval workloads in Azure AI Search.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/30/2025
---

# Retrieve data using an agent in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, *agentic retrieval* is a new parallel query processing architecture that uses a chat completion model for query planning and execution. 

This article explains how to use the **retrieve** method that invokes an agent and parallel query processing. This article also unpacks the response. Currently, there's no "answer" in the response, but you can evaluate the component parts to determine whether further processing is required to make it suitable for your app.

## Prerequisites

+ An [agent definition](search-agentic-retrieval-how-to-create.md) that represents a chat completion model, used during query planning and execution.

+ Azure AI Search with a managed identity for role-based access to a chat model.

+ Region requirements. Azure AI Search and your model should be in the same region.

+ API requirements. Use 2025-05-01-preview data plane REST API or a prerelease package of an Azure SDK that provides Agent APIs.

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending REST API calls to Azure AI Search.

## Call retrieve

Call the **retrieve** action on the agent object to return a response. Use the [2025-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-05-01-preview&preserve-view=true) data plane REST API or an Azure SDK prerelease package that provides equivalent functionality for this task.

The input for the retrieval route is natural language, where the `messages` array captures the inputs needed for calling a chat completion model.

```http
# Send Grounding Request
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-05-01-preview
api-key: {{search-api-key}}
Content-Type: application/json

{
    "messages" : [
            {
                "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "How can I help you?" }
                ]
            },
            {
                "role" : "visual interpreter",
                "content" : [
                  { "type" : "text", "text" : "What do you see in this image?" },
                  { "type" : "image", "image" : {"url": "<base64-encoded URI>"} }
                ]
            }
        ],
    "targetIndexParams" :  [
        { 
            "indexName" : "{{index-name}}",
            "filterAddOn" : "State eq WA,
            "IncludeReferenceSourceData": true, 
            "rerankerThreshold" : 2.5,
            "maxDocsForReranker": 250
        } 
    ]
}
```

**Key points**:

+ `messages` articulates the messages sent to the model.

+ `targetIndexParams` provide instructions on the retrieval. Currently in this preview, you can only target a single index. 

   You can provide a [filter expression](search-filters.md) for keyword or hybrid search. 

   You can return grounding data in the [references section](#review-the-references-array) of the response.

   You can set parameters for the [semantic reranker](semantic-how-to-configure.md) including minimum thresholds and the maximum number of inputs sent to the reranker.

## Review the response

The body of the response is also structured in the chat message style format. Currently in this preview release, the content is serialized JSON.

```http
"response": [
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": [ {
                     'azs/ref': '000000',
                     'title': 'Chapter 4',
                     'keywords': 'cloud formation,  wind speed, humidity'.
                     'content': '<content chunk>'
                
                }]
            }
        ]
    }
]
```

## Review the activity array

The activity array keeps track of the operations performed when executing the request, providing transparency of operations so that you can understand billing implications and the frequency of resource invocations.

Output includes:

+ Token used for input
+ Token counts for output
+ Result count per subquery
+ Token counts used for ranking and extraction

## Review the references array

The `references` array is a direct reference from the underlying grounding data and includes the `sourceData` used to generate the response.

The purpose of this array is to provide a chat message style structure for easy integration. For example, if you want to serialize the results into a different structure or you require some programmatic manipulation of the data before you returned it to the user.

You can also get the structured data from the source data object in the references array to manipulate it however you see fit.

## Provide grounding data

The `includeReferenceSourceData` parameter tells the search engine to provide grounding data to the search agent.

## Related content

+ [Agentic retrieval in Azure AI Search](search-agentic-retrieval-concept.md)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
