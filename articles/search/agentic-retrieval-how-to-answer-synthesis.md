---
title: Enable Answer Synthesis
titleSuffix: Azure AI Search
description: Learn how to enable answer synthesis in a knowledge base or retrieve request in Azure AI Search. At query time, the knowledge base uses your deployed LLM to produce natural-language answers with citations to your knowledge sources.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
---

# Use answer synthesis for citation-backed responses in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

By default, a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) in Azure AI Search performs *data extraction*, which returns raw grounding chunks from your knowledge sources. Data extraction is useful for retrieving specific information but lacks the context and reasoning necessary for complex queries.

You can instead enable *answer synthesis*, which uses the LLM specified in your knowledge base to answer queries in natural language. Each answer includes citations to the retrieved sources and follows any instructions you provide, such as using bulleted lists.

You can enable answer synthesis in two ways:

+ On the knowledge base (becomes the default for all queries)
+ On individual retrieval requests (overrides the default)

> [!IMPORTANT]
> + The `minimal` retrieval reasoning effort disables LLM processing, so it's incompatible with answer synthesis in both knowledge base definitions and retrieval requests. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md).
>
> + Answer synthesis incurs pay-as-you-go charges from Azure OpenAI, which is based on the number of input and output tokens. Charges appear under the LLM assigned to the knowledge base. For more information, see [Availability and pricing of agentic retrieval](agentic-retrieval-overview.md#availability-and-pricing).

## Prerequisites

+ An Azure AI Search service with a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md) that specifies an LLM.

+ Permissions to update the knowledge base. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

+ For outbound calls to the LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

+ The [2025-11-01-preview](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) REST API or an equivalent Azure SDK preview package: [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

## Enable answer synthesis in a knowledge base

This section explains how to enable answer synthesis in an existing knowledge base. Although you can use this configuration for new knowledge bases, knowledge base creation is beyond the scope of this article.

To enable answer synthesis in a knowledge base:

1. Use the 2025-11-01-preview of [Knowledge Base - Create or Update (REST API)](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to formulate the request.

1. In the body of the request, set `outputMode` to `answerSynthesis`.

1. (Optional) Use `answerInstructions` to customize the answer output. Our example instructs the knowledge base to `Use concise bulleted lists`.

```http
@search-url = <YOUR SEARCH SERVICE URL>
@api-key = <YOUR API KEY>
@knowledge-base-name = <YOUR KNOWLEDGE BASE NAME>

### Enable answer synthesis in a knowledge base
PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview  HTTP/1.1
Content-Type: application/json
api-key: {{api-key}}

{
    "name": "{{knowledge-base-name}}",
    "knowledgeSources": [ ... // OMITTED FOR BREVITY ],
    "models": [ ... // OMITTED FOR BREVITY ],
    "outputMode": "answerSynthesis",
    "answerInstructions": "Use concise bulleted lists"
}
```

> [!NOTE]
> This example assumes that you're using key-based authentication for local proof-of-concept testing. We recommend role-based access control for production workloads. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Enable answer synthesis in a retrieve request

For per-query control over the response format, you can enable answer synthesis at query time. This approach overrides the default output mode specified in the knowledge base.

To enable answer synthesis in a retrieve request:

1. Use the 2025-11-01-preview of [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to formulate the request.

1. In the body of the request, set `outputMode` to `answerSynthesis`.

```http
@search-url = <YOUR SEARCH SERVICE URL>
@api-key = <YOUR API KEY>
@knowledge-base-name = <YOUR KNOWLEDGE BASE NAME>

### Enable answer synthesis in a retrieve request
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview  HTTP/1.1
Content-Type: application/json
api-key: {{api-key}}
        
{
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is healthcare?"
                }
            ]
        }
    ],
    "outputMode": "answerSynthesis"
}
```

> [!NOTE]
> This example assumes that you're using key-based authentication for local proof-of-concept testing. We recommend role-based access control for production workloads. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md).

## Get a synthesized answer

When answer synthesis is enabled, [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) returns a natural-language answer based on the instructions you optionally specified in the knowledge base. Citations to your knowledge sources are formatted as `[ref_id:<number>]`.

For example, if your instructions are `Use concise bulleted lists` and your query is `What is healthcare?`, the response might look like this:

```json
{
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "- Healthcare encompasses various services provided to patients and the general population ... // TRIMMED FOR BREVITY"
        }
      ]
    }
  ]
}
```

The full `text` output is as follows:

```
"- Healthcare encompasses various services provided to patients and the general population, including primary health services, hospital care, dental care, mental health services, and alternative health services [ref_id:1].\n- It involves the delivery of safe, effective, patient-centered care through different modalities, such as in-person encounters, shared medical appointments, and group education sessions [ref_id:0].\n- Behavioral health is a significant aspect of healthcare, focusing on the connection between behavior and overall health, including mental health and substance use [ref_id:2].\n- The healthcare system aims to ensure quality of care, access to providers, and accountability for positive outcomes while managing costs effectively [ref_id:2].\n- The global health system is evolving to address complex health needs, emphasizing the importance of cross-sectoral collaboration and addressing social determinants of health [ref_id:4]."
```

Depending on your knowledge base's configuration, the response might include other information, such as activity logs and reference arrays. For more information, see [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Related content

+ [Quickstart: Agentic retrieval in Azure AI Search (uses answer synthesis)](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb)
+ [Azure AI Search Blob knowledge source Python sample (uses answer synthesis)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md)
+ [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md)
