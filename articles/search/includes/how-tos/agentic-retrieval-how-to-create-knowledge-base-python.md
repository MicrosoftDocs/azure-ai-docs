---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/13/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

In Azure AI Search, a *knowledge base* is a top-level resource in agentic retrieval workloads. It specifies the knowledge sources used for retrieval and, if applicable, represents a connection to a large language model (LLM). A knowledge base is used by the [retrieve method](../../agentic-retrieval-how-to-retrieve.md) in an LLM-powered information retrieval pipeline.

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.
+ An LLM that provides reasoning capabilities for query planning and answer formulation.
+ A default retrieval reasoning effort to control the cost, latency, and quality of the final response.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

> [!IMPORTANT]
> 2025-11-01-preview renames the 2025-08-01-preview *knowledge agent* to *knowledge base*. This is a breaking change. We recommend [migrating existing code](../../agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

## Prerequisites

+ Familiarity with [agentic retrieval concepts](../../agentic-retrieval-overview.md).

+ Azure AI Search, in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). If you're using a [managed identity](../../search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic pricing tier or higher.

+ Azure OpenAI with a [supported LLM](#supported-models).

+ One or more [knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources) on your search service.

+ Permissions on your search service. **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries.

+ The latest preview package of the [Azure SDK for Python](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md).

> [!NOTE]
> Although you can use the Azure portal to create knowledge bases, the portal uses the 2025-08-01-preview, which uses the previous "knowledge agent" terminology and doesn't support all 2025-11-01-preview features. For help with breaking changes, see [Migrate your agentic retrieval code](../../agentic-retrieval-how-to-migrate.md).

### Supported models

Use one of the following LLMs from Azure OpenAI or an equivalent open-source model. For deployment instructions, see [Deploy Azure OpenAI models with Microsoft Foundry](/azure/ai-foundry/how-to/deploy-models-openai).

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-nano`
+ `gpt-4.1-mini`
+ `gpt-5`
+ `gpt-5-nano`
+ `gpt-5-mini`

## Configure access

Azure AI Search needs access to the LLM. We recommend Microsoft Entra ID for authentication and role-based access for authorization, but you can also use keys.

### [**Use roles**](#tab/rbac)

1. [Configure Azure AI Search to use a managed identity](../../search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, ensure you have **Owner** or **User Access Administrator** permissions. This is required to assign roles.

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](../../search-get-started-rbac.md) to get a personal access token for a specific subscription and tenant. Paste your token into an `@access-token` variable in requests. A request that connects using your personal identity should look similar to the following example:

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @access-token = <YOUR PERSONAL ID>
    
    # List indexes
    GET https://{{search-url}}/indexes?api-version=2025-11-01-preview
    Authorization: Bearer {{access-token}}
    ```

### [**Use keys**](#tab/keys)

1. [Copy an Azure AI Search admin API key](../../search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Paste your key into an `@api-key` variable in requests.

1. Specify an API key on each request. A request that connects using an API key should look similar to the following example:

   ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @search-api-key = <YOUR SEARCH SERVICE ADMIN API KEY>

   # List indexes
   GET {{search-url}}/indexes?api-version=2025-11-01-preview
   Content-Type: application/json
   @api-key: {{search-api-key}}
   ```

---

> [!IMPORTANT]
> If you use role-based authentication, be sure to remove all references to the API key in your requests. In a request that specifies both approaches, the API key is used instead of roles.

## Check for existing knowledge bases

All knowledge bases must be uniquely named within the knowledge bases collection. Knowing about existing knowledge bases is helpful for either reuse or naming new objects.

Any 2025-08-01-preview knowledge agents are also returned in the knowledge bases collection.

List knowledge bases by name.

```python
# List knowledge bases by name
import requests
import json

endpoint = "{search_url}/knowledgebases"
params = {"api-version": "2025-11-01-preview", "$select": "name"}
headers = {"api-key": "{api_key}"}

response = requests.get(endpoint, params = params, headers = headers)
print(json.dumps(response.json(), indent = 2))
```

You can also return a single knowledge base by name to review its JSON definition.

```python
# Get a knowledge base definition
import requests
import json

endpoint = "{search_url}/knowledgebases/{knowledge_base_name}"
params = {"api-version": "2025-11-01-preview"}
headers = {"api-key": "{api_key}"}

response = requests.get(endpoint, params = params, headers = headers)
print(json.dumps(response.json(), indent = 2))
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

A knowledge base drives the agentic retrieval pipeline. In application code, it's called by other agents or chat bots.

Its composition consists of connections between *knowledge sources* (searchable content) and LLMs that you've deployed in Azure OpenAI. Properties on the model establish the connection. Properties on the knowledge source establish defaults that inform query execution and the response.

To create a knowledge base, use the 2025-11-01-preview data plane REST API or an Azure SDK preview package that provides equivalent functionality.

Recall that you must have an existing [knowledge source](../../agentic-knowledge-source-overview.md) to assign to the knowledge base.

```python
# Create a knowledge base
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeBaseAzureOpenAIModel, KnowledgeSourceReference, AzureOpenAIVectorizerParameters, KnowledgeRetrievalOutputMode, KnowledgeRetrievalLowReasoningEffort

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url = "aoai_endpoint",
    deployment_name = "aoai_gpt_deployment",
    model_name = "aoai_gpt_model",
)

knowledge_base = KnowledgeBase(
    name = "my-kb",
    description = "This knowledge base handles questions directed at two unrelated sample indexes.",
    retrieval_instructions = "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    answer_instructions = "Provide a two sentence concise and informative answer based on the retrieved documents.",
    output_mode = KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    knowledge_sources = [
        KnowledgeSourceReference(name = "hotels-ks"),
        KnowledgeSourceReference(name = "earth-at-night-ks"),
    ],
    models = [KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters = aoai_params)],
    encryption_key = None,
    retrieval_reasoning_effort = KnowledgeRetrievalLowReasoningEffort,
)

index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base.name}' created or updated successfully.")
```

### Knowledge base properties

You can pass the following properties to create a knowledge base.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base, which must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrieval_instructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query, which is recommended when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | Yes |
| `answer_instructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](../../agentic-retrieval-how-to-answer-synthesis.md). | String | Yes |
| `output_mode` | Valid values are `answer_synthesis` for an LLM-formulated answer or `extracted_data` for full search results that you can pass to an LLM as a downstream step. | String | Yes |
| `knowledge_sources` | One or more [supported knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Foundry](/azure/ai-foundry/how-to/deploy-models-openai). | Object | No |
| `encryption_key` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrieval_reasoning_effort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](../../agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

## Query the knowledge base

Call the **retrieve** action on the knowledge base object to confirm the model connection and return a response. Use the [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) data plane REST API or an Azure SDK preview package that provides equivalent functionality for this task. For more information about the **retrieve** API and the shape of the response, see [Retrieve data using a knowledge base in Azure AI Search](../../agentic-retrieval-how-to-retrieve.md).

Replace "where does the ocean look green?" with a query string that's valid for your search index.

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
# Send grounding request
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient; from azure.search.documents.knowledgebases.models import KnowledgeBaseRetrievalRequest, KnowledgeBaseMessage, KnowledgeBaseMessageTextContent, SearchIndexKnowledgeSourceParams

kb_client = KnowledgeBaseRetrievalClient(endpoint = "search_url", knowledge_base_name = "knowledge_base_name", credential = AzureKeyCredential("api_key"))
                                         
query_1 = """
Where does the ocean look green?
"""

messages.append({
    "role": "user",
    "content": query_1
})

request = KnowledgeBaseRetrievalRequest(
    messages = [
        KnowledgeBaseMessage(
            role = m["role"],
            content = [KnowledgeBaseMessageTextContent(text=m["content"])]
        ) for m in messages if m["role"] != "system"
    ],
    knowledge_source_params = [
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name = "knowledge_source_name",
            include_references = True,
            include_reference_source_data = True,
            always_query_source = True
        )
    ],
    include_activity = True,
    retrieval_reasoning_effort = KnowledgeRetrievalLowReasoningEffort
)

result = kb_client.retrieve(request)
print(f"Retrieved content from '{knowledge_base_name}' successfully.")
```

## Delete a knowledge base

If you no longer need the knowledge base, or if you need to rebuild it on the search service, use this request to delete the current object.

```python
# Delete a knowledge base
from azure.core.credentials import AzureKeyCredential 
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
index_client.delete_knowledge_base("knowledge_base_name")
print(f"Knowledge base deleted successfully.")
```
