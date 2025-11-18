---
title: Create a knowledge base
titleSuffix: Azure AI Search
description: Learn how to create a knowledge base for agentic retrieval workloads in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/10/2025
---

# Create a knowledge base in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, a *knowledge base* is a top-level resource in agentic retrieval workloads. It specifies the various knowledge sources used for retrieval, and if applicable, it represents a connection to a chat completion model . A knowledge base is used by the [retrieve method](agentic-retrieval-how-to-retrieve.md) in an LLM-powered information retrieval pipeline.

A knowledge base specifies:

+ A [knowledge source](agentic-knowledge-source-overview.md#supported-knowledge-sources) (one or more) that points to a searchable content
+ A chat completion model that provides reasoning capabilities for query planning and answer formulation
+ A default [retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md) to control the cost, latency, and quality of the final response

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

> [!IMPORTANT]
> 2025-11-01-preview renames the 2025-08-01-preview *knowledge agent* to *knowledge base*. This is a breaking change. We recommend [migrating existing code](agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

## Prerequisites

+ Familiarity with [agentic retrieval concepts and workflow](agentic-retrieval-overview.md).

+ Azure AI Search, in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md). Your search service must be basic pricing tier or higher if you're using [managed identity](search-how-to-managed-identities.md) for role-based access to deployed models.

+ A [supported chat completion model](#supported-models) on Azure OpenAI.

+ Permission requirements. **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries. Instructions are provided in this article. [Quickstart: Connect to a search service](/azure/search/search-get-started-rbac?pivots=rest) explains how to configure roles and get a personal access token for REST calls.

+ Content requirements. A [knowledge source](agentic-knowledge-source-overview.md#supported-knowledge-sources) that identifies searchable content used by the knowledge base.

+ API requirements. To create or use a knowledge base, use the [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) data plane REST API. Or, use a preview package of an Azure SDK that provides knowledge base APIs: [Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md), [.NET](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md#1170-beta3-2025-03-25), [Java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

To follow the steps in this guide, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with a [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search or the [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Jupyter package](https://pypi.org/project/jupyter/).

> [!NOTE]
> Although you can use the Azure portal to create knowledge bases, the portal uses the 2025-08-01-preview, which uses the previous "knowledge agent" terminology and doesn't support all 2025-11-01-preview features. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

## Deploy a model for agentic retrieval

Make sure you have a supported model that Azure AI Search can access. The following instructions assume Foundry Models as the provider.

1. Sign in to [Foundry portal](https://ai.azure.com/?cid=learnDocs).

1. Deploy a supported model using [these instructions](/azure/ai-foundry/how-to/deploy-models-openai).

1. Verify the search service managed identity has **Cognitive Services User** permissions on the Azure OpenAI resource. 

   If you're testing locally, you also need **Cognitive Services User** permissions.

### Supported models

Use Azure OpenAI or an equivalent open-source model:

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

## Configure access

Azure AI Search needs access to the chat completion model. You can use key-based or role-based authentication (recommended).

### [**Use roles**](#tab/rbac)

If you're using role-based authentication, on your Azure OpenAI resource, assign the **Cognitive Services User** role to a search service managed identity.

In Azure, you must have **Owner** or **User Access Administrator** permissions on the model provider to assign roles.

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, create a role assignment that gives the search service managed identity **Cognitive Services User** permissions. If you're testing locally, assign yourself to the same role. 

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token and to ensure you're logged in to a specific subscription and tenant. Paste your personal identity token into the `@accessToken` variable. A request that connects using your personal identity should look similar to the following example:

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @accessToken=<YOUR PERSONAL ID>
    
    # List Indexes
    GET https://{{search-url}}/indexes?api-version=2025-11-01-preview
    Authorization: Bearer {{accessToken}}
    ```

> [!IMPORTANT]
> If you use role-based authentication, be sure to remove all references to the API key in your requests. In a request that specifies both approaches, the API key is used instead of roles.

### [**Use keys**](#tab/keys)

You can use API keys if you don't have permission to create role assignments.

1. [Copy a Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) and paste it as an `api-key` variable into your HTTP or REST file: `@api-key`.

1. Specify an API key on each request. A request that connects using an API key should look similar to the following example:

   ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @search-api-key=<YOUR SEARCH SERVICE ADMIN API KEY>

   # List Indexes
   GET {{search-url}}/indexes?api-version=2025-11-01-preview
      Content-Type: application/json
      @api-key: {{search-api-key}}
   ```

---

## Check for existing knowledge bases

The following request lists knowledge bases by name. Within the knowledge bases collection, all knowledge bases must be uniquely named. It's helpful to know about existing knowledge bases for reuse or for naming new bases.

Any 2025-08-01-preview knowledge agents are also returned in the knowledge bases collection.

### [**Python**](#tab/python-get-agents)

The Python code snippets in this article assume you installed necessary libraries and have environment variables for endpoints and object names. For more information about these tasks, see [Quickstart: Use agentic retrieval](search-get-started-agentic-retrieval.md?pivots=programming-language-python).

```python
# List existing knowledge bases on the search service
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)

try:
    knowledgebases = {kb.name: kb for kb in index_client.list_knowledge_bases(api_version=search_api_version)}
    print(f"\nKnowledge bases on search service '{search_endpoint}':")

    if knowledgebases:
        print(f"Found {len(knowledgebases)} knowledge base(s):")
        for i, (name, knowledgebases) in enumerate(sorted(knowledgebases.items()), 1):
            print(f"{i}. Name: {name}")
            if knowledgebases.knowledge_sources:
                ks_names = [ks.name for ks in knowledgebases.knowledge_sources]
                print(f"   Knowledge Sources: {', '.join(ks_names)}")
            print()
    else:
        print("No knowledge bases found.")
        
except Exception as e:
    print(f"Error listing knowledge bases: {str(e)}")
```

You can also return a single knowledge base by name to review its JSON definition.

```python
# Get a specific knowledge base definition
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)

try:
    knowledgebase = index_client.get_knowledge_base(knowledge_base_name, api_version=search_api_version)
    
    print(f"Knowledge base: '{knowledge_base_name}'")
    print(f"Name: {knowledgebase.name}")
    
    if knowledgebase.description:
        print(f"Description: {knowledgebase.description}")
    
    if knowledgebase.models:
        print(f"\nModels ({len(knowledgebase.models)}):")
        for i, model in enumerate(knowledgebase.models, 1):
            print(f"  {i}. {type(model).__name__}")
            if hasattr(model, 'azure_open_ai_parameters'):
                params = model.azure_open_ai_parameters
                print(f"     Resource: {params.resource_url}")
                print(f"     Deployment: {params.deployment_name}")
                print(f"     Model: {params.model_name}")
    
    if knowledgebase.knowledge_sources:
        print(f"\nKnowledge Sources ({len(knowledgebase.knowledge_sources)}):")
        for i, ks in enumerate(knowledgebase.knowledge_sources, 1):
            print(f"  {i}. {ks.name}")
    
    if knowledgebase.output_mode:
        print(f"\nOutput Mode: {knowledgebase.output_mode}")
    
    # Full JSON definition
    print(f"\n{'='*60}")
    print("JSON Definition:")
    print('='*60)
    print(json.dumps(knowledgebase.as_dict(), indent=2))
    
except Exception as e:
    print(f"Error: {str(e)}")
    
    # Show available knowledge bases
    try:
        knowledgebase = {kb.name: kb for kb in index_client.knowledge_bases(api_version=search_api_version)}
        print(f"\nAvailable bases: {list(knowledgebase.keys())}")
    except Exception:
        print("Could not list available bases.")
```

### [**REST**](#tab/rest-get-agents)

```http
# List knowledge bases
GET {{search-url}}/knowledgebases?api-version=2025-11-01-preview&$select=name
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

You can also return a single knowledge base by name to review its JSON definition.

```http
# Get knowledge base
GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}
```

A response might look like the following example:

```json
{

  "name": "my-knowledge-base",
  "description": "This knowledge source uses a search index and omits a completion model for query planning and answer generation.",
  "retrievalInstructions": null,
  "answerInstructions": null,
  "outputMode": null,
  "knowledgeSources": [
    {
      "name": "my-knowledge-source"
    }
  ],
  "models": [],
  "encryptionKey": null,
  "retrievalReasoningEffort": {
    "kind": "minimal"
  }
}
```

---

## Create a knowledge base

A knowledge base drives the agentic retrieval pipeline. In application code, it's called by other agents or chat bots. 

Its composition consists of connections between *knowledge sources* (searchable content) and chat completion models that you've deployed in Azure OpenAI. Properties on the model establish the connection. Properties on the knowledge source establish defaults that inform query execution and the response.

To create a knowledge base, use the 2025-11-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

Recall that you must have an existing [knowledge source](agentic-knowledge-source-overview.md) to assign to the knowledge base.

### [**Python**](#tab/python-create-agent)

```python
from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeBaseAzureOpenAIModel, KnowledgeSourceReference, AzureOpenAIVectorizerParameters, KnowledgeRetrievalOutputMode, KnowledgeRetrievalLowReasoningEffort
from azure.search.documents.indexes import SearchIndexClient

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url=aoai_endpoint,
    deployment_name=aoai_gpt_deployment,
    model_name=aoai_gpt_model,
)

knowledge_base = KnowledgeBase(
    name=knowledge_base_name,
    models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
    knowledge_sources=[
        KnowledgeSourceReference(
            name=knowledge_source_name
        )
    ],
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    answer_instructions="Provide a 2 sentence concise and informative answer based on the retrieved documents."
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base_name}' created or updated successfully.")
```

### [**REST**](#tab/rest-create-kb)

To create a knowledge base:

1. Set environment variables at the top of your file.

    ```http
    @search-url=<YOUR SEARCH SERVICE URL>
    @knowledge-base-name=<YOUR KNOWLEDGE BASE NAME>
    @model-provider-url=<YOUR AZURE OPENAI RESOURCE URI>
    @model-api-key=<YOUR AZURE OPENAI API KEY>
    @accessToken = <a long GUID>
    ```

1. Use the 2025-11-01-preview of [Knowledge Bases - Create or Update (REST API)](/rest/api/searchservice/knowledgebases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

    ```http
    # Create knowledge base
    PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
       Content-Type: application/json
       Authorization: Bearer {{accessToken}}
    
    {
        "name" : "{{knowledge-base-name}}",
        "description": "This knowledge base handles questions directed at two unrelated sample indexes."
        "retrievalInstructions": "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
        "answerInstructions": null,
        "outputMode": "answerSynthesis",
        "knowledgeSources": [
            {
                "name": "earth-at-night-blob-ks"
            },
            {
                "name": "hotels-index-ks"
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

1. Select **Send Request**.

### Knowledge base properties

You can pass the following properties to create a knowledge base.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base, which must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrievalInstructions` | A prompt to the LLM to determine whether a knowledge source should be in scope for a query, recommended for query planning when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning (for example, if instructions resulted in bypassing an essential knowledge source). | String | Yes |
| `answerInstructions` | Use for shaping answers (see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md)). The default is null. | String | Yes |
| `outputMode` | Valid values are `answerSynthesis` for an LLM-formulated answer, or `extractedData` if you want full search results that you can pass to an LLM as a downstream step. | String | Yes |
| `knowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported chat completion model](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or from a command line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Foundry](/azure/ai-foundry/how-to/deploy-models-openai). | Object | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrievalReasoningEffort.kind` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium` (see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md)). | Object | No |

---

## Query the knowledge base

Call the **retrieve** action on the knowledge base object to confirm the model connection and return a response. Use the [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) data plane REST API or an Azure SDK preview package that provides equivalent functionality for this task. For more information about the **retrieve** API and the shape of the response, see [Retrieve data using a knowledge base in Azure AI Search](agentic-retrieval-how-to-retrieve.md).

Replace "where does the ocean look green?" with a query string that's valid for your search index.

### [**Python**](#tab/python-query-agent)

Start with instructions.

```python
instructions = """
A Q&A agent that can answer questions about the Earth at night.
If you don't have the answer, respond with "I don't know".
"""

messages = [
    {
        "role": "system",
        "content": instructions
    }
]
```

Then send the query.

```python
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import KnowledgeBaseRetrievalRequest, KnowledgeBaseMessage, KnowledgeBaseMessageTextContent, SearchIndexKnowledgeSourceParams

kb_client = KnowledgeBaseRetrievalClient(endpoint=search_endpoint, knowledge_base_name=knowledge_base_name, credential=credential)
query_1 = """
    Where does the ocean look green?
    """

messages.append({
    "role": "user",
    "content": query_1
})

req = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role=m["role"],
            content=[KnowledgeBaseMessageTextContent(text=m["content"])]
        ) for m in messages if m["role"] != "system"
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name=knowledge_source_name,
            include_references=True,
            include_reference_source_data=True,
            always_query_source=True
        )
    ],
    include_activity=True,
    retrieval_reasoning_effort=KnowledgeRetrievalLowReasoningEffort
)

result = kb_client.retrieve(retrieval_request=req)
print(f"Retrieved content from '{knowledge_base_name}' successfully.")
```

### [**REST**](#tab/rest-query-kb)

```http
# Send grounding request
POST {{search-url}}/knowledgebases/{{knowledge-base-name}}/retrieve?api-version=2025-11-01-preview
   Content-Type: application/json
   Authorization: Bearer {{accessToken}}

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
                    "text" : "where does the ocean look green?",
                    "type" : "text"
                }
            ]
        }
    ],
    "includeActivity": true,
    "knowledgeSourceParams": [
        {
            "knowledgeSourceName": "earth-at-night-blob-ks",
            "kind": "searchIndex"
            "includeReferences": true,
            "includeReferenceSourceData": true,
            "alwaysQuerySource": false
        }
  ]
}
```

[messages](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#knowledgeagentmessage&preserve-view=true) is required, but you can run this example using just the "user" role that provides the query.

[knowledgeSourceParams](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#searchindexknowledgesourceparams&preserve-view=true) specifies one or more query targets. For each knowledge source, you can specify how much information to include in the output.

The response to the previous query might look like this:

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

---

## Delete a knowledge base

If you no longer need the knowledge base, or if you need to rebuild it on the search service, use this request to delete the current object.

### [**Python**](#tab/python-delete-kb)

```python
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_base(knowledge_base_name)
print(f"Knowledge base '{knowledge_base_name}' deleted successfully.")
```

### [**REST**](#tab/rest-delete-kb)
```http
# Delete knowledge base
DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
   Authorization: Bearer {{accessToken}}
```

---

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
