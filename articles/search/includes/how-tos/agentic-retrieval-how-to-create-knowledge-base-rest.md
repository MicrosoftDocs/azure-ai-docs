---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/23/2026
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In Azure AI Search, a *knowledge base* is a top-level object that orchestrates [agentic retrieval](../../agentic-retrieval-overview.md). It defines which knowledge sources to query and the default behavior for retrieval operations. At query time, the [retrieve method](../../agentic-retrieval-how-to-retrieve.md) targets the knowledge base to run the configured retrieval pipeline.

You can create a knowledge base in a [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) workload in the Microsoft Foundry (new) portal. You also need a knowledge base in any agentic solutions that you create using the Azure AI Search APIs.

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.
+ An optional LLM that provides reasoning capabilities for query planning and answer formulation.
+ A retrieval reasoning effort that determines whether an LLM is invoked and manages cost, latency, and quality.
+ Custom properties that control routing, source selection, output format, and object encryption.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

> [!IMPORTANT]
> 2025-11-01-preview renames the 2025-08-01-preview "knowledge agent" to "knowledge base." This is a breaking change. We recommend [migrating existing code](../../agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-bases?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). If you're using a [managed identity](../../search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic pricing tier or higher.

+ Azure OpenAI with a [supported LLM](#supported-models) deployment.

+ One or more [knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources) on your search service.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md). **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries. Alternatively, you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

### Supported models

Use one of the following LLMs from Azure OpenAI in Foundry Models or an equivalent open-source model. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

## Configure access

Azure AI Search needs access to the LLM from Azure OpenAI. We recommend Microsoft Entra ID for authentication and role-based access for authorization. To assign roles, you must be an **Owner or User Access Administrator**. If you can't use roles, use key-based authentication instead.

### [**Use roles**](#tab/rbac)

1. [Configure Azure AI Search to use a managed identity](../../search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](../../search-get-started-rbac.md) to get a personal access token for a specific subscription and tenant. Specify your access token in each request, which should look similar to the following example:

    ```http
    # List indexes using roles
    GET https://{{search-url}}/indexes?api-version=2025-11-01-preview
    Content-Type: application/json
    Authorization: Bearer {{access-token}}
    ```

### [**Use keys**](#tab/keys)

1. [Copy an Azure AI Search admin API key](../../search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Specify the API key in each request. The key should look similar to the following example:

   ```http
   # List indexes using keys
   GET {{search-url}}/indexes?api-version=2025-11-01-preview
   Content-Type: application/json
   api-key: {{search-api-key}}
   ```

---

> [!IMPORTANT]
> Code snippets in this article use API keys. If you use role-based authentication, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

## Check for existing knowledge bases

A knowledge base is a top-level, reusable object. Knowing about existing knowledge bases is helpful for either reuse or naming new objects. Any 2025-08-01-preview knowledge agents are returned in the knowledge bases collection.

Use [Knowledge Bases - List (REST API)](/rest/api/searchservice/knowledge-bases/list?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to list knowledge bases by name and type.

```http
# List knowledge bases
GET {{search-url}}/knowledgebases?api-version=2025-11-01-preview&$select=name
Content-Type: application/json
api-key: {{search-api-key}}
```

You can also return a single knowledge base by name to review its JSON definition.

```http
# Get knowledge base
GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{search-api-key}}
```

The following JSON is an example response for a knowledge base.

```json
{
  "name": "my-kb",
  "description": "A sample knowledge base.",
  "retrievalInstructions": null,
  "answerInstructions": null,
  "outputMode": null,
  "knowledgeSources": [
    {
      "name": "my-blob-ks"
    }
  ],
  "models": [],
  "encryptionKey": null,
  "retrievalReasoningEffort": {
    "kind": "low"
  }
}
```

## Create a knowledge base

A knowledge base drives the agentic retrieval pipeline. In application code, other agents or chatbots call it.

A knowledge base connects knowledge sources (searchable content) to an LLM deployment from Azure OpenAI. Properties on the LLM establish the connection, while properties on the knowledge source set defaults that guide query execution and the response.

Use [Knowledge Bases - Create or Update (REST API)](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to formulate the request.

```http
# Create a knowledge base
PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{search-api-key}}

{
    "name" : "my-kb",
    "description": "This knowledge base handles questions directed at two unrelated sample indexes.",
    "retrievalInstructions": "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    "answerInstructions": null,
    "outputMode": "answerSynthesis",
    "knowledgeSources": [
        {
            "name": "hotels-ks"
        },
        {
            "name": "earth-at-night-ks"
        }
    ],
    "models" : [ 
        {
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": "{{model-provider-url}}",
                "apiKey": "{{model-api-key}}",
                "deploymentId": "gpt-4.1-mini",
                "modelName": "gpt-4.1-mini"
            }
        }
    ],
    "encryptionKey": null,
    "retrievalReasoningEffort": {
        "kind": "low"
    }
}
```

### Knowledge base properties

Pass the following properties to create a knowledge base.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. You pass instructions directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | Yes |
| `answerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](../../agentic-retrieval-how-to-answer-synthesis.md). | String | Yes |
| `outputMode` | Valid values are `answerSynthesis` for an LLM-formulated answer or `extractedData` for full search results that you can pass to an LLM as a downstream step. | String | Yes |
| `knowledgeSources` | One or more [supported knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Foundry](/azure/ai-foundry/how-to/deploy-models-openai). | Object | No |
| `encryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrievalReasoningEffort.kind` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](../../agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

## Query a knowledge base

Call the `retrieve` action on the knowledge base to verify the LLM connection and return results. For more information about the `retrieve` request and response schema, see [Retrieve data using a knowledge base in Azure AI Search](../../agentic-retrieval-how-to-retrieve.md).

Use [Knowledge Retrieval - Retrieve (REST API)](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to formulate the request. Replace "Where does the ocean look green?" with a query string that's valid for your knowledge sources.

```http
# Send grounding request
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{search-api-key}}

{
    "messages" : [
        { "role" : "assistant",
                "content" : [
                  { "type" : "text", "text" : "Use the earth at night index to answer the question. If you can't find relevant content, say you don't know." }
                ]
        },
        {
            "role" : "user",
            "content" : [
                {
                    "text" : "Where does the ocean look green?",
                    "type" : "text"
                }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-ks",
            "kind": "searchIndex",
            "includeReferences": true,
            "includeReferenceSourceData": true,
            "alwaysQuerySource": false
        }
  ]
}
```

**Key points:**

+ [`messages`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#knowledgeagentmessage&preserve-view=true) is required, but you can run this example by using just the `user` role that provides the query.

+ [`knowledgeSourceParams`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#searchindexknowledgesourceparams&preserve-view=true) specifies one or more query targets. For each knowledge source, you can specify how much information to include in the output.

The response to the sample query might look like the following example:

```http
  "response": [
    {
      "content": [
        {
          "type": "text",
          "text": "The ocean appears green off the coast of Antarctica due to phytoplankton flourishing in the water, particularly in Granite Harbor near Antarctica’s Ross Sea, where they can grow in large quantities during spring, summer, and even autumn under the right conditions [ref_id:0]. Additionally, off the coast of Namibia, the ocean can also look green due to blooms of phytoplankton and yellow-green patches of sulfur precipitating from bacteria in oxygen-depleted waters [ref_id:1]. In the Strait of Georgia, Canada, the waters turned bright green due to a massive bloom of coccolithophores, a type of phytoplankton [ref_id:5]. Furthermore, a milky green and blue bloom was observed off the coast of Patagonia, Argentina, where nutrient-rich waters from different currents converge [ref_id:6]. Lastly, a large bloom of cyanobacteria was captured in the Baltic Sea, which can also give the water a green appearance [ref_id:9]."
        }
      ]
    }
  ]
```

## Delete a knowledge base

If you no longer need the knowledge base or need to rebuild it on your search service, use this request to delete the object.

```http
# Delete a knowledge base
DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
api-key: {{search-api-key}}
```
