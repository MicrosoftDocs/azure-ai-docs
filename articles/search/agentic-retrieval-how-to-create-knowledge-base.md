---
title: Create a Knowledge Base
description: Learn how to create a knowledge base for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/24/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a knowledge base in Azure AI Search

<!-- build26-sdk-migration-note -->
> [!NOTE]
> For 2026-05-01-preview SDK migration work, align code samples with the current preview SDK surface before publishing. Python and .NET support the message-based retrieve path used for answer synthesis. The tested Java, JavaScript, and TypeScript alpha packages currently use semantic intents for retrieve until their public models expose the full message-based REST contract. For the detailed migration checklist, see [Migrate agentic retrieval code](agentic-retrieval-how-to-migrate.md).

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

In Azure AI Search, a *knowledge base* is a top-level object that orchestrates [agentic retrieval](agentic-retrieval-overview.md). It defines which knowledge sources to query and the default behavior for retrieval operations. At query time, the [retrieve method](agentic-retrieval-how-to-retrieve.md) targets the knowledge base to run the configured retrieval pipeline.

You can create a knowledge base in a [Foundry IQ](/azure/ai-foundry/agents/concepts/what-is-foundry-iq) workload in the Microsoft Foundry (new) portal. You also need a knowledge base in any agentic solutions that you create using the Azure AI Search APIs.

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.
+ An optional LLM for query planning, answer synthesis, or web content summarization. Supported tasks vary by API version and knowledge source type.
+ Custom properties that control routing, source selection, and object encryption.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-bases) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). If you're using a [managed identity](search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic pricing tier or higher.

+ One or more [knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). If you plan to use the 2026-04-01 API version to create your knowledge base, your knowledge sources must be generally available. Otherwise, you can use preview knowledge source types.

+ (Conditional) Azure OpenAI with a [supported LLM](#supported-models) deployment. For both the 2025-11-01-preview and 2026-04-01 API versions, the LLM is required if your knowledge base includes a web knowledge source. For the 2025-11-01-preview only, the LLM is optional for all other knowledge source types. 2026-04-01 doesn't support an LLM for non-web knowledge sources. 

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md). **Search Service Contributor** can create and manage a knowledge base. **Search Index Data Reader** can run queries. Alternatively, you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ Required [Azure.Search.Documents](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2025-11-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [azure-search-documents](https://pypi.org/project/azure-search-documents/) package:

  + For 2025-11-01-preview features, the latest preview package: `pip install azure-search-documents --pre`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

### Supported models

Use one of the following LLMs from Azure OpenAI in Foundry Models. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

+ `gpt-4o`
+ `gpt-4o-mini`
+ `gpt-4.1`
+ `gpt-4.1-mini`
+ `gpt-4.1-nano`
+ `gpt-5`
+ `gpt-5-mini`
+ `gpt-5-nano`
+ `gpt-5.1`
+ `gpt-5.2`
+ `gpt-5.4`
+ `gpt-5.4-mini`
+ `gpt-5.4-nano`

The `2026-05-01-preview` API expands the supported model catalog through the
existing model allowlist, but the knowledge base schema is unchanged. You
update the model deployment and `modelName` values, not the structure of the
knowledge base request. The preview adds the listed GPT-5.1, GPT-5.2, and
GPT-5.4 family names to the supported set; it doesn't add chat, codex, or pro
model variants. Regional availability is determined by Azure OpenAI in Foundry
Models for the deployment you select.

## Configure access

Azure AI Search needs access to the LLM from Azure OpenAI in Foundry Models. We recommend Microsoft Entra ID for authentication and role-based access for authorization. To assign roles, you must be an **Owner or User Access Administrator**. If you can't use roles, use key-based authentication instead.

### [**Use roles**](#tab/rbac)

::: zone pivot="csharp"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

    ```csharp
    // Authenticate using roles
    using Azure.Search.Documents.Indexes;
    using Azure.Identity;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
    ```

::: zone-end

::: zone pivot="python"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should look similar to the following example:

    ```python
    # Authenticate using roles
    from azure.identity import DefaultAzureCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = DefaultAzureCredential())
    ```

::: zone-end

::: zone pivot="rest"

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token for a specific subscription and tenant. Specify your access token in each request, which should look similar to the following example:

    ```http
    # List indexes using roles
    GET https://{{search-url}}/indexes?api-version=2026-04-01
    Content-Type: application/json
    Authorization: Bearer {{access-token}}
    ```

::: zone-end

### [**Use keys**](#tab/keys)

::: zone pivot="csharp"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request, which should look similar to the following example:

    ```csharp
    // Authenticate using keys
    using Azure.Search.Documents.Indexes;
    using Azure;
    
    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));
    ```

::: zone-end

::: zone pivot="python"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request, which should look similar to the following example:

    ```python
    # Authenticate using keys
    from azure.core.credentials import AzureKeyCredential
    index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))
    ```

::: zone-end

::: zone pivot="rest"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Specify the API key in each request, which should look similar to the following example:

   ```http
   # List indexes using keys
   GET {{search-url}}/indexes?api-version=2026-04-01
   Content-Type: application/json
   api-key: {{search-api-key}}
   ```

::: zone-end

---

> [!IMPORTANT]
> Code snippets in this article use API keys. If you use role-based authentication, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

## Check for existing knowledge bases

A knowledge base is a top-level, reusable object. Knowing about existing knowledge bases is helpful for either reuse or naming new objects.

Run the following code to list existing knowledge bases by name. The list includes all knowledge bases on your search service, regardless of which API version you used to create them.

::: zone pivot="csharp"

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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="python"

```python
# List knowledge bases by name
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

for kb in index_client.list_knowledge_bases():
    print(f"  - {kb.name}")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# List knowledge bases
GET {{search-url}}/knowledgebases?api-version={{api-version}}&$select=name
Content-Type: application/json
api-key: {{search-api-key}}
```

**Reference:** [Knowledge Bases - List](/rest/api/searchservice/knowledge-bases/list)

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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient)

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

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# Get knowledge base
GET {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
Content-Type: application/json
api-key: {{search-api-key}}
```

**Reference:** [Knowledge Bases - Get](/rest/api/searchservice/knowledge-bases/get)

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

> [!NOTE]
> The response schema reflects the API version you used to create the knowledge base. A knowledge base created with the generally available 2026-04-01 API version returns a narrower definition than the 2025-11-01-preview. For more information about which properties each version supports, see the next section.

## Create a knowledge base

A knowledge base connects one or more knowledge sources (searchable content) to an optional LLM from Azure OpenAI in Foundry Models. The properties you set establish defaults for query execution and the retrieval response.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

::: zone pivot="csharp"

# [2025-11-01-preview](#tab/2025-11-01-preview)

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
    ModelName = aoaiGptModel,
    ApiKey = aoaiApiKey
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

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
// Create a knowledge base
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var knowledgeBase = new KnowledgeBase(
    name: "my-kb",
    knowledgeSources: new KnowledgeSourceReference[] 
    { 
        new KnowledgeSourceReference("hotels-ks"),
        new KnowledgeSourceReference("earth-at-night-ks")
    }
)
{
    Description = "This knowledge base handles questions directed at two unrelated sample indexes."
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
Console.WriteLine($"Knowledge base '{knowledgeBase.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet&preserve-view=true)

---

::: zone-end

::: zone pivot="python"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```python
# Create a knowledge base
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference,
)
from azure.search.documents.knowledgebases.models import KnowledgeRetrievalLowReasoningEffort

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
    output_mode = "answerSynthesis",
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

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

# [2026-04-01](#tab/2026-04-01)

```python
# Create a knowledge base
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeSourceReference

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_base = KnowledgeBase(
    name = "my-kb",
    description = "This knowledge base handles questions directed at two unrelated sample indexes.",
    knowledge_sources = [
        KnowledgeSourceReference(name = "hotels-ks"),
        KnowledgeSourceReference(name = "earth-at-night-ks"),
    ],
    encryption_key = None,
)

index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

---

::: zone-end

::: zone pivot="rest"

# [2025-11-01-preview](#tab/2025-11-01-preview)

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
                "deploymentId": "gpt-5.4-mini",
                "modelName": "gpt-5.4-mini"
            }
        }
    ],
    "encryptionKey": null,
    "retrievalReasoningEffort": {
        "kind": "low"
    }
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
# Create a knowledge base
PUT {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version=2026-04-01
Content-Type: application/json
api-key: {{search-api-key}}

{
    "name" : "my-kb",
    "description": "This knowledge base handles questions directed at two unrelated sample indexes.",
    "knowledgeSources": [
        {
            "name": "hotels-ks"
        },
        {
            "name": "earth-at-night-ks"
        }
    ],
    "encryptionKey": null
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true)

---

::: zone-end

> [!IMPORTANT]
> The 2026-04-01 API version only accepts generally available knowledge source types and supports minimal, extractive retrieval. Preview-only capabilities, such as query planning, answer synthesis, and configurable reasoning effort, aren't supported. For full functionality, use the 2025-11-01-preview.

### Configure CORS for browser-based retrieve calls

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

In the `2026-05-01-preview` API, a knowledge base can define `corsOptions`
for browser-based applications that call the retrieve action directly from
JavaScript. The CORS policy identifies which browser origins can send retrieve
requests to the knowledge base.

The following REST example allows retrieve requests from one browser origin:

```http
PUT {{search-url}}/knowledgebases/browser-chat-kb?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{search-api-key}}

{
  "name": "browser-chat-kb",
  "description": "A knowledge base that allows one browser app origin.",
  "knowledgeSources": [
    {
      "name": "product-docs-ks"
    }
  ],
  "corsOptions": {
    "allowedOrigins": [
      "https://myapp.example.com"
    ],
    "maxAgeInSeconds": 300
  }
}
```

When `corsOptions` is present, `allowedOrigins` lists the origins that can call
the knowledge base from a browser. `maxAgeInSeconds` is optional and controls
how long the browser can cache the preflight response.

If `corsOptions` is omitted, the knowledge base has no CORS policy and browsers
block cross-origin retrieve requests. Set `allowedOrigins` to an explicit list
of browser origins for production applications. You can use `"*"` to allow all
origins, but this setting isn't recommended for production. If
`maxAgeInSeconds` is omitted, the preflight cache duration defaults to 300
seconds. CORS applies to knowledge base retrieve REST API calls from browsers.

### Knowledge base properties

Pass the following properties to create a knowledge base.

::: zone pivot="csharp"

# [2025-11-01-preview](#tab/2025-11-01-preview)

| Name | Description | Type | Required |
|--|--|--|--|
| `Name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `KnowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `Description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `RetrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Instructions are passed directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `AnswerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `OutputMode` | Valid values are `AnswerSynthesis` for an LLM-formulated answer or `ExtractedData` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `Models` | Required for web knowledge sources. Optional for other knowledge source types. Specifies a [supported LLM](#supported-models) for query planning or answer synthesis. Get connection details from the Microsoft Foundry portal or a command-line request, and then provide them by using the [KnowledgeBaseAzureOpenAIModel class](/dotnet/api/azure.search.documents.indexes.models.knowledgebaseazureopenaimodel?view=azure-dotnet-preview&preserve-view=true). You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `RetrievalReasoningEffort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

# [2026-04-01](#tab/2026-04-01)

| Name | Description | Type | Required |
|--|--|--|--|
| `Name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `KnowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). You must specify generally available knowledge source types. | Array | Yes |
| `Description` | A description of the knowledge base. | String | No |
| `Models` | Required for web knowledge sources. Specifies a [supported LLM](#supported-models) used to summarize and preprocess web content before it can be included in retrieval results. Get connection details from the Microsoft Foundry portal or a command-line request, and then provide them by using the [KnowledgeBaseAzureOpenAIModel class](/dotnet/api/azure.search.documents.indexes.models.knowledgebaseazureopenaimodel?view=azure-dotnet&preserve-view=true). You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |

---

::: zone-end

::: zone pivot="python"

# [2025-11-01-preview](#tab/2025-11-01-preview)

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrieval_instructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. Pass instructions directly to the LLM. It's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `answer_instructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `output_mode` | Valid values are `answerSynthesis` for an LLM-formulated answer or `extractedData` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `knowledge_sources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | Required for web knowledge sources. Optional for other knowledge source types. Specifies a [supported LLM](#supported-models) for query planning or answer synthesis. Get connection details from the Microsoft Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrieval_reasoning_effort` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

# [2026-04-01](#tab/2026-04-01)

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. | String | No |
| `knowledge_sources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). You must specify generally available knowledge source types. | Array | Yes |
| `models` | Required for web knowledge sources. Specifies a [supported LLM](#supported-models) used to summarize and preprocess web content before it can be included in retrieval results. Get connection details from the Microsoft Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |

---

::: zone-end

::: zone pivot="rest"

# [2025-11-01-preview](#tab/2025-11-01-preview)

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. The LLM uses the description to inform query planning. | String | No |
| `retrievalInstructions` | A prompt for the LLM to determine whether a knowledge source should be in scope for a query. Include this prompt when you have multiple knowledge sources. This field influences both knowledge source selection and query formulation. For example, instructions could append information or prioritize a knowledge source. You pass instructions directly to the LLM, which means it's possible to provide instructions that break query planning, such as instructions that result in bypassing an essential knowledge source. | String | No |
| `answerInstructions` | Custom instructions to shape synthesized answers. The default is null. For more information, see [Use answer synthesis for citation-backed responses](agentic-retrieval-how-to-answer-synthesis.md). | String | No |
| `outputMode` | Valid values are `answerSynthesis` for an LLM-formulated answer or `extractedData` for full search results that you can pass to an LLM as a downstream step. | String | No |
| `knowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). | Array | Yes |
| `models` | Required for web knowledge sources. Optional for other knowledge source types. Specifies a [supported LLM](#supported-models) for query planning or answer synthesis. Get connection details from the Microsoft Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |
| `retrievalReasoningEffort.kind` | Determines the level of LLM-related query processing. Valid values are `minimal`, `low` (default), and `medium`. For more information, see [Set the retrieval reasoning effort](agentic-retrieval-how-to-set-retrieval-reasoning-effort.md). | Object | No |

# [2026-04-01](#tab/2026-04-01)

| Name | Description | Type | Required |
|--|--|--|--|
| `name` | The name of the knowledge base. It must be unique within the knowledge bases collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes |
| `description` | A description of the knowledge base. | String | No |
| `knowledgeSources` | One or more [supported knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). You must specify generally available knowledge source types. | Array | Yes |
| `models` | Required for web knowledge sources. Specifies a [supported LLM](#supported-models) used to summarize and preprocess web content before it can be included in retrieval results. Get connection details from the Microsoft Foundry portal or a command-line request. You can use role-based access control instead of API keys for the Azure AI Search connection to the model. | Array | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge base and the generated objects. | Object | No |

---

::: zone-end

## Query a knowledge base

After you create a knowledge base, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query it and verify the LLM connection.

## Delete a knowledge base

If you no longer need the knowledge base or need to rebuild it on your search service, run the following code to delete the object.

::: zone pivot="csharp"

```csharp
// Delete a knowledge base
using Azure.Search.Documents.Indexes;
var indexClient = new SearchIndexClient(new Uri(searchEndpoint), credential);

await indexClient.DeleteKnowledgeBaseAsync(knowledgeBaseName);
System.Console.WriteLine($"Knowledge base '{knowledgeBaseName}' deleted successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true)

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

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# Delete a knowledge base
DELETE {{search-url}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
api-key: {{search-api-key}}
```

**Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
