---
title: Create a Knowledge Base
description: Learn how to create a knowledge base for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/14/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create a knowledge base in Azure AI Search

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In Azure AI Search, a *knowledge base* is a top-level object that orchestrates [agentic retrieval](agentic-retrieval-overview.md). It defines which knowledge sources to query and the default behavior for retrieval operations. At query time, the [retrieve method](agentic-retrieval-how-to-retrieve.md) targets the knowledge base to run the configured retrieval pipeline.

You can create a knowledge base in a [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) workload in the Microsoft Foundry (new) portal. You also need a knowledge base in any agentic solutions that you create using the Azure AI Search APIs.

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.
+ An optional LLM that provides reasoning capabilities for query planning and answer formulation.
+ A retrieval reasoning effort that determines whether an LLM is invoked and manages cost, latency, and quality.
+ Custom properties that control routing, source selection, output format, and object encryption.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

> [!IMPORTANT]
> 2025-11-01-preview renames the 2025-08-01-preview "knowledge agent" to "knowledge base." This is a breaking change. We recommend [migrating existing code](agentic-retrieval-how-to-migrate.md) to the new APIs as soon as possible.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-bases?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md). If you're using a [managed identity](search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic pricing tier or higher.

+ One or more [knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources) on your search service.

+ Azure OpenAI with a [supported LLM](#supported-models) deployment.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md). **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries. Alternatively, you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents` preview package](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1): `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents` preview package](https://pypi.org/project/azure-search-documents/11.7.0b2/): `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

### Supported models

Use one of the following LLMs from Azure OpenAI in Foundry Models. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

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

::: zone pivot="csharp"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

```csharp
    using Azure.Search.Documents.Indexes;
    using Azure.Identity;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
    ```

::: zone-end

::: zone pivot="python"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

```python
    # Authenticate using roles
    from azure.identity import DefaultAzureCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = DefaultAzureCredential())
    ```

::: zone-end

::: zone pivot="rest"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, such as Foundry Models, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token for a specific subscription and tenant. Specify your access token in each request, which should look similar to the following example:

```http
    # List indexes using roles
    GET https://{{search-url}}/indexes?api-version=2025-11-01-preview
    Content-Type: application/json
    Authorization: Bearer {{access-token}}
    ```

::: zone-end

### [**Use keys**](#tab/keys)

::: zone pivot="csharp"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request. Your code should look similar to the following example:

```csharp
    using Azure.Search.Documents.Indexes;
    using Azure;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));
    ```

::: zone-end

::: zone pivot="python"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request. Your code should look similar to the following example:

```python
    # Authenticate using keys
    from azure.core.credentials import AzureKeyCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
    ```

::: zone-end

::: zone pivot="rest"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Specify the API key in each request. The key should look similar to the following example:

```http
   # List indexes using keys
   GET {{search-url}}/indexes?api-version=2025-11-01-preview
   Content-Type: application/json
   api-key: {{search-api-key}}
   ```

::: zone-end

---

> [!IMPORTANT]
> Code snippets in this article use API keys. If you use role-based authentication, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

## Check for existing knowledge bases

A knowledge base is a top-level, reusable object. Knowing about existing knowledge bases is helpful for either reuse or naming new objects. Any 2025-08-01-preview knowledge agents are returned in the knowledge bases collection.

::: zone pivot="csharp"

Run the following code to list existing knowledge bases by name.

```csharp
// List knowledge bases by name
  using Azure.Search.Documents.Indexes;
  
  var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);
  var knowledgeBases = indexClient.GetKnowledgeBasesAsync();
  
  Console.WriteLine("Knowledge Bases:");
  
  await foreach (var kb in knowledgeBases)
  {
      Console.WriteLine($"  - {kb.Name}");
  }
```

::: zone-end

::: zone pivot="python"

Run the following code to list existing knowledge bases by name.

```python
# List knowledge bases by name
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

for kb in index_client.list_knowledge_bases():
    print(f"  - {kb.name}")
```

::: zone-end

::: zone pivot="rest"

Use [Knowledge Bases - List (REST API)](/rest/api/searchservice/knowledge-bases/list?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to list knowledge bases by name and type.

```http
# List knowledge bases
GET {{search-url}}/knowledgebases?api-version=2025-11-01-preview&$select=name
Content-Type: application/json
api-key: {{search-api-key}}
```

::: zone-end

You can also return a single knowledge base by name to review its JSON definition.

::: zone pivot="csharp"

```csharp
using Azure.Search.Documents.Indexes;
using System.Text.Json;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

// Specify the knowledge base name to retrieve
string kbNameToGet = "earth-knowledge-base";

// Get a specific knowledge base definition
var knowledgeBaseResponse = await indexClient.GetKnowledgeBaseAsync(kbNameToGet);
var kb = knowledgeBaseResponse.Value;

// Serialize to JSON for display
string json = JsonSerializer.Serialize(kb, new JsonSerializerOptions { WriteIndented = true });
Console.WriteLine(json);
```

::: zone-end

::: zone pivot="python"

```python
# Get a knowledge base definition
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

kb = index_client.get_knowledge_base("knowledge_base_name")
print(json.dumps(kb.as_dict(), indent = 2))
```

::: zone-end

::: zone pivot="rest"

```http
# Get knowledge base
GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{search-api-key}}
```

::: zone-end

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

::: zone pivot="csharp"

Run the following code to create a knowledge base.

```csharp
// Create a knowledge base
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var aoaiParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel
};

var knowledgeBase = new KnowledgeBase(
    name: "my-kb",
    knowledgeSources: new KnowledgeSourceReference[] 
    { 
        new KnowledgeSourceReference("hotels-ks"),
        new KnowledgeSourceReference("earth-at-night-ks")
    }
)
{
    Description = "This knowledge base handles questions directed at two unrelated sample indexes.",
    RetrievalInstructions = "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    AnswerInstructions = "Provide a two sentence concise and informative answer based on the retrieved documents.",
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis,
    Models = { new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: aoaiParams) },
    RetrievalReasoningEffort = new KnowledgeRetrievalLowReasoningEffort()
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBase.Name}' created or updated successfully.");
```

::: zone-end

::: zone pivot="python"

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
    retrieval_reasoning_effort = KnowledgeRetrievalLowReasoningEffort(),
)

index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base.name}' created or updated successfully.")
```

::: zone-end

::: zone pivot="rest"

Use [Knowledge Bases - Create or Update (REST API)](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a knowledge base.

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

::: zone-end

### Knowledge base properties

Pass the following properties to create a knowledge base.

::: zone pivot="csharp"

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `knowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `Description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `RetrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `AnswerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `OutputMode` | Valid values are `AnswerSynthesis` for an LLM-formulated answer or `ExtractedData` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `Models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `Models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. Provide the parameters by using the [KnowledgeBaseAzureOpenAIModel class](/dotnet/api/azure.search.documents.indexes.models.knowledgebaseazureopenaimodel?view=azure-dotnet-preview&preserve-view=true). You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Object | No |
| `RetrievalReasoningEffort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrieval_instructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Pass instructions directly to the LLM. It's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `answer_instructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `output_mode` | Valid values are `answer_synthesis` for an LLM-formulated answer or `extracted_data` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `knowledge_sources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Object | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrieval_reasoning_effort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. You pass instructions directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `answerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `outputMode` | Valid values are `answerSynthesis` for an LLM-formulated answer or `extractedData` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `knowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | A connection to a [supported LLM](#supported-models) used for answer formulation or query planning. In this preview, `models` can contain just one model, and the model provider must be Azure OpenAI. Obtain model information from the Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Object | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrievalReasoningEffort.kind` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

::: zone-end

## Query a knowledge base

After you create a knowledge base, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query it and verify the LLM connection.

## Delete a knowledge base

If you no longer need the knowledge base or need to rebuild it on your search service, run the following code to delete the object.

::: zone pivot="csharp"

```csharp
using Azure.Search.Documents.Indexes;
var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

await indexClient.DeleteKnowledgeBaseAsync(knowledgeBaseName);
System.Console.WriteLine($"Knowledge base '{knowledgeBaseName}' deleted successfully.");
```

::: zone-end

::: zone pivot="python"

```python
# Delete a knowledge base
from azure.core.credentials import AzureKeyCredential 
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
index_client.delete_knowledge_base("knowledge_base_name")
print(f"Knowledge base deleted successfully.")
```

::: zone-end

::: zone pivot="rest"

```http
# Delete a knowledge base
DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2025-11-01-preview
api-key: {{search-api-key}}
```

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
