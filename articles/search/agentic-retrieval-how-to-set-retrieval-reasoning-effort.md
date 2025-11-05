---
title: Set the retrieval reasoning effort
titleSuffix: Azure AI Search
description: Learn how to set the level of LLM processing for agentic retrieval in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/05/2025
---

# Set the retrieval reasoning effort

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In agentic retrieval, you can specify the level of LLM processing for query planning and answer formulation. The property is `retrievalReasoningEffort`, and you can set it in a knowledge base or on a retrieve request.

Levels of effort include:

+ `minimal` (no LLM processing)
+ `low` (LLM for query processing and answer formulation)
+ `medium` (LLM for query processing and answer formulation)

## Prerequisites

+ Azure AI Search, in any [region that provides semantic ranker](search-region-support.md).

+ Familiarity with [agentic retrieval concepts and workflow](agentic-retrieval-overview.md).

+ [A knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or a preview package of an Azure SDK that provides the latest knowledge source REST APIs. Currently, there's no portal support for this knowledge source.

## Set retrievalReasoningEffort in a knowledge base

Use [Create or Update Knowledge Base](/rest/api/searchservice/knowledgebases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to set the `retrievalReasoningEffort`.

The following JSON shows the syntax. For more information about knowledge bases, see [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

```json
"retrievalReasoningEffort": { /* no other parameters when effort is minimal */
    "kind": "low"
}
```

## Set retrievalReasoningEffort in a retrieve request

You can override the knowledge base `retrievalReasoningEffort` default by specifying the property on the retrieve request.

A retrieve request might look similar to the following example.

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

| Level | Description | Limits | 
|-|-|-|-|
| `minimal` | Doesn't take a model definition. Doesn't have retrieval instructions or answer generation. Fails if the knowledge source can't be queried with simple text or vectors. Ignores the `alwaysQueryKnowledgeSource` property on a retrieve request because all knowledge sources listed in the knowledge base are in scope for the query. Recommended if you need to minimize latency and cost.  | `outputMode` must be set to `extractiveData`. |
| `low` | Makes minimal calls to the LLM.  | 5,000 answer tokens. Maximum three subqueries from a maximum of three knowledge sources. Maximum of 50 documents for semantic ranking, and 10 documents if the semantic ranker uses L3 classification. |
| `medium `| Balanced approach that provides the LLM with more inputs.  | 10,000 answer tokens. Maximum of five subqueries from a maximum of five knowledge sources. Maximum of 50 documents for semantic ranking, and 20 documents if the semantic ranker uses L3 classification. |

---

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
