---
title: Create a Knowledge Base
description: Learn how to create a knowledge base for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 08/12/2026
ms.custom:
  - dev-focus
  - doc-kit-assisted
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a knowledge base in Azure AI Search

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-08-01-preview REST API. The 2026-08-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-08-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

In Azure AI Search, a *knowledge base* is a top-level object that orchestrates [agentic retrieval](agentic-retrieval-overview.md). It defines which knowledge sources to query and the default behavior for retrieval operations. At query time, the [retrieve method](agentic-retrieval-how-to-retrieve.md) targets the knowledge base to run the configured retrieval pipeline.

A knowledge base specifies:

+ One or more knowledge sources that point to searchable content.

+ An optional LLM for query planning, answer synthesis, or web content summarization. Supported tasks vary by API version and knowledge source type.

+ Custom properties that control routing, source selection, and object encryption.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-bases) |
| -- | -- | -- | -- | -- | -- | -- |
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). If you're using a [managed identity](search-how-to-managed-identities.md) for role-based access to deployed models, your search service must be on the Basic tier or higher.

+ One or more [knowledge sources](agentic-knowledge-source-overview.md#supported-knowledge-sources). Use the `2026-08-01-preview` API version to access preview knowledge sources or to use an LLM with non-web knowledge sources. Use the `2026-04-01` API version for generally available knowledge sources and minimal, extractive retrieval.

+ (Conditional) Azure OpenAI with a [supported LLM](#supported-models) deployment. An LLM is required if your knowledge base includes a web knowledge source. For other knowledge sources, an LLM is optional in the `2026-08-01-preview` API version and unsupported in the `2026-04-01` API version.

+ Permission to create knowledge bases. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [admin API key](search-security-api-keys.md).

+ If the knowledge base specifies an LLM, the search service must have a [managed identity](search-how-to-managed-identities.md) with **Cognitive Services User** permissions on the Microsoft Foundry resource.

::: zone pivot="csharp"

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For `2026-08-01-preview` features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For `2026-04-01` features, the latest stable package: `dotnet add package Azure.Search.Documents`

+ For keyless authentication, the [`Azure.Identity`](https://www.nuget.org/packages/Azure.Identity) package: `dotnet add package Azure.Identity`

::: zone-end

::: zone pivot="python"

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For `2026-08-01-preview` features, the latest preview package: `pip install --pre azure-search-documents`

  + For `2026-04-01` features, the latest stable package: `pip install azure-search-documents`

+ For keyless authentication, the [`azure-identity`](https://pypi.org/project/azure-identity/) package: `pip install azure-identity`

::: zone-end

::: zone pivot="rest"

+ Required Search Service REST API version:

  + For preview features: [2026-08-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

  + For generally available features: [2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

+ For keyless authentication, include a [Microsoft Entra ID token](search-get-started-rbac.md?pivots=rest#get-token) in the `Authorization` header of each HTTP request.

::: zone-end

### Supported models

Use one of the following LLMs from Azure OpenAI in Foundry Models. Azure OpenAI determines regional availability for the deployment you select. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/ai-foundry/how-to/deploy-models-openai).

The GPT-4 family is deprecated. For model lifecycle guidance, retirement dates, and current status, see [Model retirement and deprecation](/azure/ai-foundry/openai/concepts/model-retirements) and [Model retirement schedule - Microsoft Foundry](/azure/foundry/openai/concepts/model-retirement-schedule).

| Model | Supported API versions |
| -- | -- |
| `gpt-4o` (deprecated) | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-4o-mini` (deprecated) | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-4.1` (deprecated) | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-4.1-mini` (deprecated) | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-4.1-nano` (deprecated) | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5` | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5-mini` | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5-nano` | 2025-11-01-preview, 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.1` | 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.2` | 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.4` | 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.4-mini` | 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.4-nano` | 2026-05-01-preview, 2026-08-01-preview |
| `gpt-5.5` | 2026-08-01-preview |
| `gpt-5.6-sol` | 2026-08-01-preview |
| `gpt-5.6-terra` | 2026-08-01-preview |
| `gpt-5.6-luna` | 2026-08-01-preview |

## Configure access

Azure AI Search needs access to the LLM from Azure OpenAI in Foundry Models. We recommend Microsoft Entra ID for authentication and role-based access for authorization. To assign roles, you must be an **Owner or User Access Administrator**. If you can't use roles, use key-based authentication instead.

### [**Use roles**](#tab/rbac)

::: zone pivot="csharp"

1. [Enable role-based access control on Azure AI Search](search-security-enable-roles.md).

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should be similar to the following example.

    ```csharp
    // Authenticate using roles
    using Azure.Search.Documents.Indexes;
    using Azure.Identity;

    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());
    ```

::: zone-end

::: zone pivot="python"

1. [Enable role-based access control on Azure AI Search](search-security-enable-roles.md).

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to sign in to a specific subscription and tenant. Use `DefaultAzureCredential` instead of `AzureKeyCredential` in each request, which should be similar to the following example.

    ```python
    # Authenticate using roles
    from azure.identity import DefaultAzureCredential
    index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())
    ```

::: zone-end

::: zone pivot="rest"

1. [Enable role-based access control on Azure AI Search](search-security-enable-roles.md).

1. [Configure Azure AI Search to use a managed identity](search-how-to-managed-identities.md).

1. On your model provider, assign **Cognitive Services User** to the managed identity of your search service. If you're testing locally, assign the same role to your user account.

1. For local testing, follow the steps in [Quickstart: Connect without keys](search-get-started-rbac.md) to get a personal access token for a specific subscription and tenant. Specify your access token in each request, which should be similar to the following example.

    ```http
    # List indexes using roles
    GET {{search-endpoint}}/indexes?api-version=2026-04-01
    Content-Type: application/json
    Authorization: Bearer {{search-access-token}}
    ```

::: zone-end

### [**Use keys**](#tab/keys)

::: zone pivot="csharp"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request, which should be similar to the following example.

    ```csharp
    // Authenticate using keys
    using Azure.Search.Documents.Indexes;
    using Azure;

    var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));
    ```

::: zone-end

::: zone pivot="python"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Use `AzureKeyCredential` to specify the API key in each request, which should be similar to the following example.

    ```python
    # Authenticate using keys
    from azure.core.credentials import AzureKeyCredential
    index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = AzureKeyCredential("api_key"))
    ```

::: zone-end

::: zone pivot="rest"

1. [Copy an Azure AI Search admin API key](search-security-api-keys.md#find-existing-keys) from the Azure portal.

1. Specify the API key in each request, which should be similar to the following example.

   ```http
   # List indexes using keys
   GET {{search-endpoint}}/indexes?api-version=2026-04-01
   Content-Type: application/json
   api-key: {{search-api-key}}
   ```

::: zone-end

---

> [!IMPORTANT]
> The code snippets in this article use keyless authentication. To use an API key instead, update each request accordingly. In a request that specifies both approaches, the API key takes precedence.

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
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

for kb in index_client.list_knowledge_bases():
    print(f"  - {kb.name}")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# List knowledge bases
GET {{search-endpoint}}/knowledgebases?api-version={{api-version}}&$select=name
Content-Type: application/json
Authorization: Bearer {{search-access-token}}
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
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
import json

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

kb = index_client.get_knowledge_base("<knowledge-base-name>")
print(json.dumps(kb.as_dict(), indent = 2))
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# Get knowledge base
GET {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
Content-Type: application/json
Authorization: Bearer {{search-access-token}}
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
> The response schema reflects the API version you used to create the knowledge base. A knowledge base created with the generally available `2026-04-01` API version returns a narrower definition than the `2026-08-01-preview`. For more information about which properties each version supports, see [Create a knowledge base](#create-a-knowledge-base).

## Create a knowledge base

> [!IMPORTANT]
> The `2026-04-01` API version only accepts generally available knowledge source types and supports minimal, extractive retrieval. It doesn't support preview-only capabilities, such as query planning, answer synthesis, and configurable reasoning effort. For full functionality, use the `2026-08-01-preview`.

A knowledge base connects one or more knowledge sources (searchable content) to an optional LLM from Azure OpenAI in Foundry Models. The properties you set establish defaults for query execution and the retrieval response.

After you create a knowledge base, you can update its properties at any time. If the knowledge base is in use, updates take effect on the next retrieval.

::: zone pivot="csharp"

# [2026-08-01-preview](#tab/2026-08-01-preview)

```csharp
// Create a knowledge base
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.KnowledgeBases.Models;
using Azure.Identity;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

var aoaiParams = new AzureOpenAIVectorizerParameters
{
    ResourceUri = new Uri(aoaiEndpoint),
    DeploymentName = aoaiGptDeployment,
    ModelName = aoaiGptModel,
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
    AnswerInstructions = "Answer in two concise sentences.",
    OutputMode = KnowledgeRetrievalOutputMode.AnswerSynthesis,
    Models = { new KnowledgeBaseAzureOpenAIModel(azureOpenAIParameters: aoaiParams) },
    RetrievalReasoningEffort = new KnowledgeRetrievalAutoReasoningEffort()
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
using Azure.Identity;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```python
# Create a knowledge base
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    AzureOpenAIVectorizerParameters,
    KnowledgeBase,
    KnowledgeBaseAzureOpenAIModel,
    KnowledgeSourceReference,
)
from azure.search.documents.knowledgebases.models import (
    KnowledgeRetrievalAutoReasoningEffort,
    KnowledgeRetrievalOutputMode,
)

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url = "<aoai-endpoint>",
    deployment_name = "<aoai-gpt-deployment>",
    model_name = "<aoai-gpt-model>",
)

knowledge_base = KnowledgeBase(
    name = "my-kb",
    description = "This knowledge base handles questions directed at two unrelated sample indexes.",
    retrieval_instructions = "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    answer_instructions = "Answer in two concise sentences.",
    output_mode = KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    knowledge_sources = [
        KnowledgeSourceReference(name = "hotels-ks"),
        KnowledgeSourceReference(name = "earth-at-night-ks"),
    ],
    models = [KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters = aoai_params)],
    encryption_key = None,
    retrieval_reasoning_effort = KnowledgeRetrievalAutoReasoningEffort(),
)

index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

# [2026-04-01](#tab/2026-04-01)

```python
# Create a knowledge base
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeSourceReference

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())

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

# [2026-08-01-preview](#tab/2026-08-01-preview)

```http
# Create a knowledge base
PUT {{search-endpoint}}/knowledgebases/my-kb?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
    "name" : "my-kb",
    "description": "This knowledge base handles questions directed at two unrelated sample indexes.",
    "retrievalInstructions": "Use the hotels knowledge source for queries about where to stay, otherwise use the earth at night knowledge source.",
    "answerInstructions": "Answer in two concise sentences.",
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
                "resourceUri": "{{aoai-endpoint}}",
                "deploymentId": "gpt-5.4-mini",
                "modelName": "gpt-5.4-mini"
            }
        }
    ],
    "encryptionKey": null,
    "retrievalReasoningEffort": {
        "kind": "auto"
    }
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
# Create a knowledge base
PUT {{search-endpoint}}/knowledgebases/my-kb?api-version=2026-04-01
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

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

### Configure default retrieve limits (preview)

Starting with the `2026-08-01-preview` API version, you can use the optional `retrieveDefaults` object to store request-wide defaults on a knowledge base. Each stored property applies only when a retrieve request omits the corresponding request field:

| Stored property | Retrieve request field |
| --- | --- |
| `maxRuntimeInSeconds` | `maxRuntimeInSeconds` |
| `maxOutputDocuments` | `maxOutputDocuments` |
| `maxOutputSizeInTokens` | `maxOutputSize` |

The output token budget uses different property names when stored and overridden. Set `maxOutputSizeInTokens` in `retrieveDefaults`, and use `maxOutputSize` in a retrieve request.

The effective value for each property is determined independently in this order:

1. The corresponding value on the retrieve request.
1. The value in the knowledge base `retrieveDefaults` object.
1. The service default when the property is absent at both levels.

The following example uses an existing search index knowledge source named `your-knowledge-source`. It stores a 45-second runtime budget, a maximum of eight output documents, and a 12,000-token output budget.

::: zone pivot="csharp"

```csharp
using System;
using Azure.Identity;
using Azure.Search.Documents;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;

string searchEndpoint = "<search-endpoint>";

var options = new SearchClientOptions(
    SearchClientOptions.ServiceVersion.V2026_08_01_Preview);
var indexClient = new SearchIndexClient(
    new Uri(searchEndpoint),
    new DefaultAzureCredential(),
    options);

var knowledgeBase = new KnowledgeBase(
    "your-knowledge-base",
    new[] { new KnowledgeSourceReference("your-knowledge-source") })
{
    Description = "A knowledge base for product support content.",
    RetrieveDefaults = new KnowledgeBaseRetrieveDefaults
    {
        MaxRuntimeInSeconds = 45,
        MaxOutputDocuments = 8,
        MaxOutputSizeInTokens = 12000
    }
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [SearchClientOptions.ServiceVersion](/dotnet/api/azure.search.documents.searchclientoptions.serviceversion?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    KnowledgeBase,
    KnowledgeBaseRetrieveDefaults,
    KnowledgeSourceReference,
)

search_endpoint = "<search-endpoint>"
index_client = SearchIndexClient(
    endpoint=search_endpoint,
    credential=DefaultAzureCredential(),
    api_version="2026-08-01-preview",
)

knowledge_base = KnowledgeBase(
    name="your-knowledge-base",
    description="A knowledge base for product support content.",
    knowledge_sources=[
        KnowledgeSourceReference(name="your-knowledge-source"),
    ],
    retrieve_defaults=KnowledgeBaseRetrieveDefaults(
        max_runtime_in_seconds=45,
        max_output_documents=8,
        max_output_size_in_tokens=12000,
    ),
)

index_client.create_or_update_knowledge_base(knowledge_base)
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-endpoint}}/knowledgebases/your-knowledge-base?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

{
  "name": "your-knowledge-base",
  "description": "A knowledge base for product support content.",
  "knowledgeSources": [
    {
      "name": "your-knowledge-source"
    }
  ],
  "retrieveDefaults": {
    "maxRuntimeInSeconds": 45,
    "maxOutputDocuments": 8,
    "maxOutputSizeInTokens": 12000
  }
}
```

**Reference:** [Knowledge Bases - Create or Update](/rest/api/searchservice/knowledge-bases/create-or-update?view=rest-searchservice-2026-08-01-preview&preserve-view=true)

::: zone-end

To override these stored values with 20 seconds, one document, and 5,000 tokens for one request, see [Verify knowledge base retrieve defaults](agentic-retrieval-how-to-retrieve.md#verify-knowledge-base-retrieve-defaults).

### Configure CORS for browser-based retrieve calls (preview)

> [!IMPORTANT]
> Cross-origin resource sharing (CORS) allows browser-based applications to request data directly from the service. Depending on your CORS configuration, external web pages might access or invoke the service and its data by using the user's browser context. This access can create security threats. Enabling CORS is at your own risk.

Starting with the `2026-05-01-preview` API version, a knowledge base can define `corsOptions` for browser-based applications that call the retrieve action directly from JavaScript. The CORS policy identifies which browser origins can send retrieve requests to the knowledge base.

When you omit `corsOptions`, the knowledge base has no CORS policy, and browsers block cross-origin retrieve requests.

The following example creates a knowledge base that allows retrieve requests from one browser origin.

::: zone pivot="csharp"

```csharp
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new DefaultAzureCredential());

var knowledgeBase = new KnowledgeBase(
    name: "browser-chat-kb",
    knowledgeSources: new[] { new KnowledgeSourceReference("product-docs-ks") }
)
{
    Description = "A knowledge base that allows one browser app origin.",
    CorsOptions = new CorsOptions(new[] { "https://myapp.example.com" })
    {
        MaxAgeInSeconds = 300
    }
};

await indexClient.CreateOrUpdateKnowledgeBaseAsync(knowledgeBase);
```

**Reference:** [CorsOptions](/dotnet/api/azure.search.documents.indexes.models.corsoptions?view=azure-dotnet-preview&preserve-view=true), [KnowledgeBase](/dotnet/api/azure.search.documents.indexes.models.knowledgebase?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    CorsOptions,
    KnowledgeBase,
    KnowledgeSourceReference,
)

index_client = SearchIndexClient(endpoint="<search-endpoint>", credential=DefaultAzureCredential())

knowledge_base = KnowledgeBase(
    name="browser-chat-kb",
    description="A knowledge base that allows one browser app origin.",
    knowledge_sources=[KnowledgeSourceReference(name="product-docs-ks")],
    cors_options=CorsOptions(
        allowed_origins=["https://myapp.example.com"],
        max_age_in_seconds=300,
    ),
)

index_client.create_or_update_knowledge_base(knowledge_base)
```

**Reference:** [CorsOptions](/python/api/azure-search-documents/azure.search.documents.indexes.models.corsoptions), [KnowledgeBase](/python/api/azure-search-documents/azure.search.documents.indexes.models.knowledgebase)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-endpoint}}/knowledgebases/browser-chat-kb?api-version=2026-08-01-preview
Content-Type: application/json
Authorization: Bearer {{search-access-token}}

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

::: zone-end

## Query a knowledge base

After you create a knowledge base, call the [retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query it.

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
from azure.identity import DefaultAzureCredential
from azure.search.documents.indexes import SearchIndexClient

index_client = SearchIndexClient(endpoint = "<search-endpoint>", credential = DefaultAzureCredential())
index_client.delete_knowledge_base("<knowledge-base-name>")
print(f"Knowledge base deleted successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

::: zone-end

::: zone pivot="rest"

```http
# Delete a knowledge base
DELETE {{search-endpoint}}/knowledgebases/{{knowledge-base-name}}?api-version={{api-version}}
Authorization: Bearer {{search-access-token}}
```

**Reference:** [Knowledge Bases - Delete](/rest/api/searchservice/knowledge-bases/delete?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
+ [Migrate agentic retrieval code](agentic-retrieval-how-to-migrate.md)
