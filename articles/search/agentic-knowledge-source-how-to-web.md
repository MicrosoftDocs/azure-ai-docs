---
title: Create Web Knowledge Source for Agentic Retrieval
description: Learn how to create a Web Knowledge Source resource for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 04/28/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create a Web Knowledge Source resource

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary. This also means use of Web Knowledge Source waives all elevated Government Community Cloud security and compliance commitments to include data sovereignty and screened/citizenship-based support, as applicable.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis/grounding-pricing).
>
> + Learn more about how Azure admins can [manage access to use of Web Knowledge Source](agentic-knowledge-source-how-to-web-manage.md).

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

*Web Knowledge Source* enables retrieval of real-time web data from Microsoft Bing in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

Bing Custom Search is always the search provider for Web Knowledge Source. Although you can't specify alternative search providers or engines, you can include or exclude specific *domains*, such as https://learn.microsoft.com. When no domains are specified, Web Knowledge Source has unrestricted access to the entire public internet.

Web Knowledge Source works best alongside other knowledge sources. Use Web Knowledge Source when your proprietary content doesn't provide complete, up-to-date answers or when you want to supplement results with information from a commercial search engine.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure subscription with [access to Web Knowledge Source](agentic-knowledge-source-how-to-web-manage.md). By default, access is enabled. Contact your admin if access is disabled.

+ An Azure AI Search service in any [public region that provides agentic retrieval](search-region-support.md). Web Knowledge Source isn't supported in private or sovereign clouds.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

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

## Limitations and considerations

+ Web content is always summarized by an LLM before it's included in retrieval results. Results are cited summaries, not verbatim web text.

+ For the 2026-04-01 API version, the knowledge base must include a model reference to provide the LLM for web content summarization. Retrieval is always extractive (cited summaries). Answer synthesis and configurable reasoning effort aren't available in this version.

+ For the 2025-11-01-preview API version, the knowledge base model reference also enables [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), which produces a single LLM-formulated response instead of extracted citations.

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a Web Knowledge Source resource.

```json
{
  "name": "my-web-ks",
  "kind": "web",
  "description": "A sample Web Knowledge Source.",
  "encryptionKey": null,
  "webParameters": {
    "domains": null
  }
}
```

## Create a knowledge source

Run the following code to create a web knowledge source.

::: zone pivot="csharp"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```csharp
// Create Web Knowledge Source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var knowledgeSource = new WebKnowledgeSource(name: "my-web-ks")
{
    Description = "A sample Web Knowledge Source.",
    WebParameters = new WebKnowledgeSourceParameters
    {
        Domains = new WebKnowledgeSourceDomains
        {
            AllowedDomains = 
            {
                new WebKnowledgeSourceDomain(address: "learn.microsoft.com") { IncludeSubpages = true }
            },
            BlockedDomains = 
            {
                new WebKnowledgeSourceDomain(address: "bing.com") { IncludeSubpages = false }
            }
        }
    }
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [WebKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.webknowledgesource?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
// Create Web Knowledge Source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var knowledgeSource = new WebKnowledgeSource(name: "my-web-ks")
{
    Description = "A sample Web Knowledge Source.",
    WebParameters = new WebKnowledgeSourceParameters
    {
        Domains = new WebKnowledgeSourceDomains
        {
            AllowedDomains = 
            {
                new WebKnowledgeSourceDomain(address: "learn.microsoft.com") { IncludeSubpages = true }
            },
            BlockedDomains = 
            {
                new WebKnowledgeSourceDomain(address: "bing.com") { IncludeSubpages = false }
            }
        }
    }
};

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSource.Name}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true), [WebKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.webknowledgesource?view=azure-dotnet&preserve-view=true)

---

::: zone-end

::: zone pivot="python"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```python
# Create Web Knowledge Source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import WebKnowledgeSource, WebKnowledgeSourceParameters, WebKnowledgeSourceDomains, WebKnowledgeSourceDomain

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = WebKnowledgeSource(
    name = "my-web-ks",
    description = "A sample Web Knowledge Source.",
    encryption_key = None,
    web_parameters = WebKnowledgeSourceParameters(
        domains = WebKnowledgeSourceDomains(
            allowed_domains = [ WebKnowledgeSourceDomain(address="learn.microsoft.com", include_subpages=True) ],
            blocked_domains = [ WebKnowledgeSourceDomain(address="bing.com", include_subpages=False) ]
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

# [2026-04-01](#tab/2026-04-01)

```python
# Create Web Knowledge Source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import WebKnowledgeSource, WebKnowledgeSourceParameters, WebKnowledgeSourceDomains, WebKnowledgeSourceDomain

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = WebKnowledgeSource(
    name = "my-web-ks",
    description = "A sample Web Knowledge Source.",
    encryption_key = None,
    web_parameters = WebKnowledgeSourceParameters(
        domains = WebKnowledgeSourceDomains(
            allowed_domains = [ WebKnowledgeSourceDomain(address="learn.microsoft.com", include_subpages=True) ],
            blocked_domains = [ WebKnowledgeSourceDomain(address="bing.com", include_subpages=False) ]
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

---

::: zone-end

::: zone pivot="rest"

# [2025-11-01-preview](#tab/2025-11-01-preview)

```http
### Create Web Knowledge Source
PUT {{search-url}}/knowledgesources/my-web-ks?api-version=2025-11-01-preview
Content-Type: application/json
api-key: {{api-key}}

{
  "name": "my-web-ks",
  "kind": "web",
  "description": "This knowledge source pulls content from the web.",
  "encryptionKey": null,
  "webParameters": {
    "domains": {
      "allowedDomains": [ { "address": "learn.microsoft.com", "includeSubpages": true } ],
      "blockedDomains": [ { "address": "bing.com", "includeSubpages": false } ]
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
### Create Web Knowledge Source
PUT {{search-url}}/knowledgesources/my-web-ks?api-version=2026-04-01
Content-Type: application/json
api-key: {{api-key}}

{
  "name": "my-web-ks",
  "kind": "web",
  "description": "This knowledge source pulls content from the web.",
  "encryptionKey": null,
  "webParameters": {
    "domains": {
      "allowedDomains": [ { "address": "learn.microsoft.com", "includeSubpages": true } ],
      "blockedDomains": [ { "address": "bing.com", "includeSubpages": false } ]
    }
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true)

---

::: zone-end

### Source-specific properties

For both the 2025-11-01-preview and 2026-04-01 API versions, you can pass the following properties to create a web knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. When unspecified, Azure AI Search applies a default description. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `WebParameters` | Parameters specific to Web Knowledge Source. Currently, this is only `Domains`. | Object | Yes | No |
| `Domains` | Domains to allow or block from the search space. By default, the knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) to search the entire public internet. When you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search) to restrict results to the specified domains. In both cases, Bing Custom Search is the search provider. | Object | Yes | No |
| `AllowedDomains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `IncludeSubpages` to `true` or `false`. | Array | Yes | No |
| `BlockedDomains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `IncludeSubpages` to `true` or `false`. | Array | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. When unspecified, Azure AI Search applies a default description. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `web_parameters` | Parameters specific to Web Knowledge Source. Currently, this is only `domains`. | Object | Yes | No |
| `domains` | Domains to allow or block from the search space. By default, the knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) to search the entire public internet. When you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search) to restrict results to the specified domains. In both cases, Bing Custom Search is the search provider. | Object | Yes | No |
| `allowed_domains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `include_subpages` to `true` or `false`. | Array | Yes | No |
| `blocked_domains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `include_subpages` to `true` or `false`. | Array | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `web` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. When unspecified, Azure AI Search applies a default description. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `webParameters` | Parameters specific to Web Knowledge Source. Currently, this is only `domains`. | Object | Yes | No |
| `domains` | Domains to allow or block from the search space. By default, the knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) to search the entire public internet. When you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search) to restrict results to the specified domains. In both cases, Bing Custom Search is the search provider. | Object | Yes | No |
| `allowedDomains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `includeSubpages` to `true` or `false`. | Array | Yes | No |
| `blockedDomains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `includeSubpages` to `true` or `false`. | Array | Yes | No |

::: zone-end

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Review retrieve output

When you query a knowledge base that includes Web Knowledge Source, the retrieve response `activity` array can contain two web-related records:

+ A `web` record that captures the runtime parameters used for the request.
+ A `modelWebSummarization` record that captures token usage for the LLM summarization step.

```json
{
  "activity": [
    {
      "id": 1,
      "type": "web",
      "knowledgeSourceName": "my-web-ks",
      "elapsedMs": 212,
      "webArguments": {
        "search": "What is the latest news about AI in education?",
        "language": "en",
        "market": "en-US",
        "count": 10,
        "freshness": "2026-03-01..2026-03-31"
      }
    },
    {
      "id": 2,
      "type": "modelWebSummarization",
      "elapsedMs": 87,
      "inputTokens": 1234,
      "outputTokens": 256
    }
  ]
}
```

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Manage access to Web Knowledge Source in your Azure subscription](agentic-knowledge-source-how-to-web-manage.md)
+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
