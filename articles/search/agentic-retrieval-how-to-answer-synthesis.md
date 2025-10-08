---
title: Configure Answer Synthesis
titleSuffix: Azure AI Search
description: Learn how to configure a knowledge agent to use answer synthesis in Azure AI Search. At query time, the agent uses your deployed chat completion model to produce natural-language answers with citations to your knowledge sources.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/26/2025
---

# Use answer synthesis for citation-backed responses in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

By default, a [knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md) in Azure AI Search performs *data extraction*, which returns raw grounding chunks from your knowledge sources. Data extraction is useful for retrieving specific information, but it lacks the context and reasoning necessary for complex queries.

You can configure the agent to perform *answer synthesis*, which uses your deployed chat completion model to respond to queries in natural language. Each answer includes citations to the retrieved sources and follows any instructions you provide, such as using bulleted lists.

This article explains how to configure and test answer synthesis for an existing agent. Although you can use this configuration for new agents, agent creation is beyond the scope of this article.

> [!IMPORTANT]
> Answer synthesis incurs pay-as-you-go charges from Azure OpenAI, which is based on the number of input and output tokens. Charges appear under the chat completion model assigned to the agent. For more information, see [Availability and pricing of agentic retrieval](agentic-retrieval-overview.md#availability-and-pricing).

## Prerequisites

+ A knowledge agent that uses the 2025-08-01-preview syntax, which requires `knowledgeSources` instead of `targetIndexes`.

+ [Visual Studio Code](https://code.visualstudio.com/) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) or a prerelease package of an Azure SDK that provides the knowledge agent REST APIs. Currently, there's no portal support.

## Configure answer synthesis

To configure your knowledge agent for answer synthesis, use the 2025-08-01-preview of [Knowledge Agent - Create or Update (REST API)](/rest/api/searchservice/knowledge-agents/create-or-update?view=rest-searchservice-2025-08-01-preview&preserve-view=true).

In the `outputConfiguration` section:

1. Set `modality` to `answerSynthesis`.

1. (Optional) Use `answerInstructions` to customize the answer output. Our example instructs the agent to `Use concise bulleted lists`.

```http
@search-url = <YourSearchServiceUrl>
@agent-name = <YourAgentName>
@api-key = <YourApiKey>

### Configure answer synthesis
PUT https://{{search-url}}/knowledgeAgents/{{agent-name}}?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}

    {
        "name": "{{agent-name}}",
        "models": [
            ... // Redacted for brevity
        ],
        "knowledgeSources": [
            ... // Redacted for brevity
        ],
        "outputConfiguration": {
            "modality": "answerSynthesis",
            "answerInstructions": "Use concise bulleted lists"
        }
    }
```

> [!IMPORTANT]
> This example assumes that you're using key-based authentication for local proof-of-concept testing. We recommend role-based access control for production workloads. For more information, see [Connect to Azure AI Search using roles](search-security-rbac.md).

<!--
1. (Optional) Set the `includeReferences` property to `true` or `false`.

    ```http
          "knowledgeSources" : [
              {
                  "name" : "<YourKnowledgeSource>", 
                  "includeReferences" : true,
                  "includeReferenceSourceData" : true
              }
          ]
    ```

1. (Optional) Set the `includeActivity` property to `true` to include an activity log in answers.

    ```http
        	"outputConfiguration": {
        		"modality": "answerSynthesis",
        		"answerInstructions": "Use concise bulleted lists",
        		"includeActivity": true
        	}
    ```
-->

## Get a synthesized answer

After your knowledge agent is configured for answer synthesis, use the 2025-08-01-preview of [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-08-01-preview&preserve-view=true) to test its output.

```http
### Send a query to the agent
POST https://{{search-url}}/agents/{{agent-name}}/retrieve?api-version=2025-08-01-preview  HTTP/1.1
    Content-Type: application/json
    api-key: {{api-key}}
        
    {
      "messages": [
            {
                "role": "user",
                "content" : [
                    {
                        "text": "<YourQueryText>",
                        "type": "text"
                    }
                ]
            }
        ]
    }
```

The response should include a natural-language answer based on your instructions, with citations to your knowledge sources formatted as `[ref_id:<number>]`. For example, if your instructions are `Use concise bulleted lists` and your query is `What is healthcare?`, the response might look like this:

```json
{
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "- Healthcare encompasses various services provided to patients and the general population ... // Trimmed for brevity
        }
      ]
    }
  ],
  ... // Redacted for brevity
}
```

The full `text` output is as follows:

```
"- Healthcare encompasses various services provided to patients and the general population, including primary health services, hospital care, dental care, mental health services, and alternative health services [ref_id:1].\n- It involves the delivery of safe, effective, patient-centered care through different modalities, such as in-person encounters, shared medical appointments, and group education sessions [ref_id:0].\n- Behavioral health is a significant aspect of healthcare, focusing on the connection between behavior and overall health, including mental health and substance use [ref_id:2].\n- The healthcare system aims to ensure quality of care, access to providers, and accountability for positive outcomes while managing costs effectively [ref_id:2].\n- The global health system is evolving to address complex health needs, emphasizing the importance of cross-sectoral collaboration and addressing social determinants of health [ref_id:4]."
```

Depending on your agent's configuration, the response might include other information, such as activity logs and reference arrays. For more information, see [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md).

## Related content

+ [Quickstart: Agentic retrieval in Azure AI Search (uses answer synthesis)](https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb)
+ [Azure AI Search Blob knowledge source Python sample (uses answer synthesis)](https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/knowledge/blob-knowledge-source.ipynb)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Create a knowledge agent](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Create a search index knowledge source](agentic-knowledge-source-how-to-search-index.md)
+ [Create a blob knowledge source](agentic-knowledge-source-how-to-blob.md)
