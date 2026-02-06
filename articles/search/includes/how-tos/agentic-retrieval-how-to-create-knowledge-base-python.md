---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/15/2026
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

+ The latest preview version of the [`azure-search-documents` client library](https://pypi.org/project/azure-search-documents/11.7.0b2/) for Python.

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

Azure AI Search needs access to the LLM from Azure OpenAI. We recommend Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner or User Access Administrator** to assign roles. If roles aren't feasible, use key-based authentication instead.

### [**Use roles**](#tab/rbac)

1. [Configure Azure AI Search to use a managed identity](../../search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](../../search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

    ```python
    # Authenticate using roles
    from azure.identity import DefaultAzureCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = DefaultAzureCredential())
    ```
    
### [**Use keys**](#tab/keys)

1. [Copy an Azure AI Search admin API key](../../search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request. Your code should look similar to the following example:

    ```python
    # Authenticate using keys
    from azure.core.credentials import AzureKeyCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
    ```
    
---

> [!IMPORTANT]
> Code snippets in this article use API keys. If you use role-based authentication, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

## Check for existing knowledge bases

Knowing about existing knowledge bases is helpful for either reuse or naming new objects. Any 2025-08-01-preview knowledge agents are returned in the knowledge bases collection.

Run the following code to list existing knowledge bases by name.

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

A knowledge base drives the agentic retrieval pipeline. In application code, other agents or chatbots call it.

A knowledge base connects knowledge sources (searchable content) to an LLM deployment from Azure OpenAI. Properties on the LLM establish the connection, while properties on the knowledge source establish defaults that inform query execution and the response.

Run the following code to create a knowledge base.

```python
# Create a knowledge base
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeBaseAzureOpenAIModel, KnowledgeSourceReference, AzureOpenAIVectorizerParameters, KnowledgeRetrievalOutputMode, KnowledgeRetrievalLowReasoningEffort

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url = "aoai_endpoint",
    api_key="aoai_api_key",
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

Pass the following properties to create a knowledge base.

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrieval_instructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Pass instructions directly to the LLM. It's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | Yes |
| `answer_instructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](../../agentic-retrieval-how-to-answer-synthesis.md). | String | Yes |
| `output_mode` | Valid values are `answer_synthesis` for an LLM-formulated answer or `extracted_data` for full search results that you can pass to an LLM as a downstream step. | String | Yes |
| `knowledge_sources` | One or more [supported knowledge sources](../../agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. For more information, see [How to deploy Azure OpenAI models with Foundry](/azure/ai-foundry/how-to/deploy-models-openai). | Object | No |
| `encryption_key` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrieval_reasoning_effort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](../../agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

## Query a knowledge base

Call the `retrieve` action on the knowledge base to verify the LLM connection and return results. For more information about the `retrieve` request and response schema, see [Retrieve data using a knowledge base in Azure AI Search](../../agentic-retrieval-how-to-retrieve.md).

Replace "Where does the ocean look green?" with a query string that's valid for your knowledge sources.

```python
# Send grounding request
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.knowledgebases import KnowledgeBaseRetrievalClient
from azure.search.documents.knowledgebases.models import KnowledgeBaseMessage, KnowledgeBaseMessageTextContent, KnowledgeBaseRetrievalRequest, SearchIndexKnowledgeSourceParams

kb_client = KnowledgeBaseRetrievalClient(endpoint = "search_url", knowledge_base_name = "knowledge_base_name", credential = AzureKeyCredential("api_key"))

request = KnowledgeBaseRetrievalRequest(
    messages=[
        KnowledgeBaseMessage(
            role = "assistant",
            content = [KnowledgeBaseMessageTextContent(text = "Use the earth at night index to answer the question. If you can't find relevant content, say you don't know.")]
        ),
        KnowledgeBaseMessage(
            role = "user",
            content = [KnowledgeBaseMessageTextContent(text = "Where does the ocean look green?")]
        ),
    ],
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name = "earth-at-night-ks",
            include_references = True,
            include_reference_source_data = True,
            always_query_source = False,
        )
    ],
    include_activity = True,
)

result = kb_client.retrieve(request)
print(result.response[0].content[0].text)
```

**Key points:**

+ [`messages`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#knowledgeagentmessage&preserve-view=true) is required, but you can run this example by using just the `user` role that provides the query.

+ [`knowledge_source_params`](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview#searchindexknowledgesourceparams&preserve-view=true) specifies one or more query targets. For each knowledge source, you can specify how much information to include in the output.

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

```python
# Delete a knowledge base
from azure.core.credentials import AzureKeyCredential 
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
index_client.delete_knowledge_base("knowledge_base_name")
print(f"Knowledge base deleted successfully.")
```
