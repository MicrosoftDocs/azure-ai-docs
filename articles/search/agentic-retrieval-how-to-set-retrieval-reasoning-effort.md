---
title: Set the Retrieval Reasoning Effort
titleSuffix: Azure AI Search
description: Learn how to set the level of LLM processing for agentic retrieval in Azure AI Search.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 01/26/2026
ms.custom: references_regions
---

# Set the retrieval reasoning effort

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In agentic retrieval, you can specify the level of large language model (LLM) processing for query planning and answer formulation. Use the `retrievalReasoningEffort` property to set LLM processing levels that affect costs and latency. Extra LLM processing improves relevancy, but it also takes longer and uses billable LLM resources. You can set this property in a knowledge base or on a retrieve request.

Levels of reasoning effort include:

| Level | Effort |
|-------|--------|
| `minimal` | No LLM processing. You provide the query.|
| `low` | Runs a single pass of LLM-based query planning and knowledge source selection. This is the default. The LLM analyzes the query and breaks it into component parts as needed.|
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. |

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ Permissions to update the knowledge base. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) REST API or a preview Azure SDK package: [.NET](/dotnet/api/azure.search.documents?view=azure-dotnet-preview&preserve-view=true) | [Java](/java/api/com.azure.search.documents?view=azure-java-preview&preserve-view=true) | [JavaScript](/javascript/api/@azure/search-documents?view=azure-node-preview&preserve-view=true) | [Python](/python/api/azure-search-documents?view=azure-python-preview&preserve-view=true).


## Choose a reasoning effort

This section describes:

+ [Reasoning effort levels](#reasoning-effort-levels)
+ [Iterative search for medium retrieval](#iterative-search-for-medium-retrieval)
+ [Region support for medium retrieval](#region-support-for-medium-retrieval)

### Reasoning effort levels

| Level | Description | Recommendation | Limits | 
|-|-|-|-|
| `minimal` | Disables LLM-based query planning to deliver the lowest cost and latency for agentic retrieval. It issues direct text and vector searches across the knowledge sources listed in the knowledge base, and returns the best-matching passages. Because all knowledge sources in the knowledge base are always searched and no query expansion is performed, behavior is predictable and easy to control. It also means the `alwaysQueryKnowledgeSource` property on a retrieve request is ignored.  | Use "minimal" for migrations from the [Search API](/rest/api/searchservice/documents/search-post) or when you want to manage query planning yourself. | <ul><li>`outputMode` must be set to `extractiveData`.</li><li>[Answer synthesis](agentic-retrieval-how-to-answer-synthesis.md) and [web knowledge](agentic-knowledge-source-how-to-web.md) aren't supported.</li><li>Maximum of [10 knowledge sources per knowledge base](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li></ul> |
| `low` | The default mode of agentic retrieval, running a single pass of LLM-based query planning and knowledge source selection. The agentic retrieval engine generates subqueries and fans them out to the selected knowledge sources, then merges the results. You can enable answer synthesis to produce a grounded natural-language response with inline citations. | Use "low" when you want a balance between minimal latency and deeper processing. | <ul><li>5,000 answer tokens.</li><li>Maximum of three subqueries from [three knowledge sources per knowledge base](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li><li>Maximum of 50 documents for semantic ranking, and 10 documents if the semantic ranker uses L3 classification.</li></ul> |
| `medium` | Adds deeper search and an enhanced retrieval stack to agentic retrieval to maximize completeness. After the first search is performed, a [high-precision semantic classifier](search-relevance-overview.md) evaluates the retrieved documents to determine whether further processing and L3 ranking is required. If the initial results from the first pass are insufficiently relevant to the query, a follow-up iteration is performed using a revised query plan. This revised query plan takes the previous results into account and iterates by fine-tuning queries, broadening terms, or adding other knowledge sources such as the web. It also increases resource limits compared to low and minimal effort. This reasoning level optimizes for relevance rather than exhaustive recall. | Use "medium" to maximize the utility of LLM-assisted knowledge retrieval. | <ul><li>10,000 answer tokens.</li><li>Maximum of five subqueries from [five knowledge sources per knowledge base](search-limits-quotas-capacity.md#agentic-retrieval-limits).</li><li>Maximum of 50 documents for semantic ranking, and 20 documents if the semantic ranker uses L3 classification.</li><li>Available in [select regions](#region-support-for-medium-retrieval).</li></ul> |

### Iterative search for medium retrieval

A medium retrieval reasoning effort provides iterative search if initial results aren't sufficiently relevant. An extra *semantic classifier model* is called to determine if a second iteration is necessary.

The semantic classifier performs the following:

+ Recognizes when there's enough context to answer the question.

+ Retries on insufficient results, using existing information for context. New queries might drill down for more focused detail, or broaden the search. The activity log in the response shows the generated queries used for a more comprehensive answer.

+ Rescores using L3 classification. The range is identical to L2 ranking, an absolute range of zero through 4.0.

There's only one retry. Each iteration adds latency and cost, so the system constrains retry to one pass. A second iteration adds input tokens to the query pipeline, which adds to the overall billable input token count.

Iteration can reuse or choose different sources. The second pass selects the most promising knowledge resource to provide the missing information.

### Region support for medium retrieval

You can set a medium retrieval reasoning effort if your search service is in one of the following regions:

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

## Set the reasoning effort in a knowledge base

To establish the default behavior, set the property in the knowledge base.

1. Use [Create or Update Knowledge Base](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to set the `retrievalReasoningEffort`.

1. Add the `retrievalReasoningEffort` property. The following JSON shows the syntax. For more information about knowledge bases, see [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

    ```json
    "retrievalReasoningEffort": { /* no other parameters when effort is minimal */
        "kind": "low"
    }
    ```

## Set the reasoning effort in a retrieve request

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

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
