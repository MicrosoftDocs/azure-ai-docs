---
title: Set the retrieval reasoning effort
titleSuffix: Azure AI Search
description: Learn how to set the level of LLM processing for agentic retrieval in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/07/2025
---

# Set the retrieval reasoning effort

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In agentic retrieval, you can specify the level of large language model (LLM) processing for query planning and answer formulation. Use the `retrievalReasoningEffort` property to determine LLM processing levels. You can set this property in a knowledge base or on a retrieve request.

Levels of reasoning effort include:

| Level | Effort |
|-------|--------|
| `minimal` | No LLM processing. |
| `low` | Runs a single pass of LLM-based query planning and knowledge source selection. This is the default. |
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. |

## Prerequisites

+ Azure AI Search, in any [region that provides agentic retrieval](search-region-support.md).

+ Familiarity with [agentic retrieval concepts and workflow](agentic-retrieval-overview.md).

+ [A knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) and a [knowledge source](agentic-knowledge-source-overview.md).

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client). You can also use a preview package of an Azure SDK that provides the latest knowledge source REST APIs.

## Set retrievalReasoningEffort in a knowledge base

To establish the default behavior, set the property in the knowledge base.

1. Use [Create or Update Knowledge Base](/rest/api/searchservice/knowledgebases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to set the `retrievalReasoningEffort`.

1. Add the `retrievalReasoningEffort` property. The following JSON shows the syntax. For more information about knowledge bases, see [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

    ```json
    "retrievalReasoningEffort": { /* no other parameters when effort is minimal */
        "kind": "low"
    }
    ```

## Set retrievalReasoningEffort in a retrieve request

To override the default on a query-by-query basis, set the property in the retrieve request.

1. Modify a [retrieve action](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to override the knowledge base `retrievalReasoningEffort` default.

1. Add the `retrievalReasoningEffort` property. A retrieve request might look similar to the following example.

    ```json
    {
        "messages": [ /* trimmed for brevity */  ],
        "retrievalReasoningEffort": { "kind": "low" },
        "outputMode": "answerSynthesis",
        "maxRuntimeInSeconds": 30,
        "maxOutputSize": 6000
    }
    ```

## Choose a retrieval reasoning effort

| Level | Description | Recommendation | Limits | 
|-|-|-|-|
| `minimal` | Disables LLM-based query planning to deliver the lowest cost and latency for agentic retrieval. It issues direct text and vector searches across the knowledge sources listed in the knowledge base, and returns the best-matching passages. Because all knowledge sources are always searched and no query expansion is performed, behavior is predictable and easy to control. It also means the `alwaysQueryKnowledgeSource` property on a retrieve request is ignored.  | Use "minimal" for migrations from the [Search API](/rest/api/searchservice/documents/search-post) or when you want to manage query planning yourself. | `outputMode` must be set to `extractiveData`. <br>[Answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) and [web knowledge](agentic-knowledge-source-how-to-web.md) aren't supported. |
| `low` | The default mode of agentic retrieval, running a single pass of LLM-based query planning and knowledge source selection. The agentic retrieval engine generates subqueries and fans them out to the selected knowledge sources, then merges the results. You can enable answer synthesis to produce a grounded natural-language response with inline citations. | Use "low" when you want a balance between minimal latency and deeper processing. | 5,000 answer tokens. <br>Maximum three subqueries from a maximum of three knowledge sources. <br>Maximum of 50 documents for semantic ranking, and 10 documents if the semantic ranker uses L3 classification. |
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. After the first search is performed, a [high-precision semantic classifier](search-relevance-overview.md) evaluates the retrieved documents for an L3 ranking. If the quality of the retrieved results is insufficient to answer the query, a follow-up iteration is performed using a revised query plan. This revised query plan takes into account the already run queries and retrieved documents by adjusting queries, broadening terms, or adding sources such as the web. It also increases resource limits compared to low and minimal effort. | Use "medium" to maximize the utility of LLM-assisted knowledge retrieval. <br><br>Medium isn't available in all agentic retrieval regions.| 10,000 answer tokens. <br>Maximum of five subqueries from a maximum of five knowledge sources. <br>Maximum of 50 documents for semantic ranking, and 20 documents if the semantic ranker uses L3 classification.  |

### Regions supporting medium retrieval reasoning effort

You can set a medium retrieval reasoning effort if your search service is in one of the following regions.

+ East US 2
+ East US
+ South Central US
+ West US 3
+ West US 2
+ West US
+ Germany West Central
+ North Europe
+ Switzerland North
+ Sweden Central
+ Spain Central
+ UK South
+ Korea Central
+ Japan East
+ Southeast Asia

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
