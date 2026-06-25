---
title: Create Web Knowledge Source for Agentic Retrieval
description: Learn how to create a Web Knowledge Source resource for agentic retrieval workloads in Azure AI Search.
ms.service: azure-ai-search
ms.custom:
  - ignite-2025
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a Web Knowledge Source resource

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary. This also means use of Web Knowledge Source waives all elevated Government Community Cloud security and compliance commitments to include data sovereignty and screened/citizenship-based support, as applicable.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis).
>
> + Learn more about how Azure admins can [manage access to use of Web Knowledge Source](agentic-knowledge-source-how-to-web-manage.md).

*Web Knowledge Source* enables retrieval of real-time web data from Microsoft Bing in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

Bing Custom Search is always the search provider for Web Knowledge Source. Although you can't specify alternative search providers or engines, you can include or exclude specific *domains*, such as https://learn.microsoft.com. When no domains are specified, Web Knowledge Source has unrestricted access to the entire public internet.

Web Knowledge Source works best alongside other knowledge sources. Use it when your proprietary content doesn't provide complete, up-to-date answers or when you want to supplement results with information from a commercial search engine.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure subscription with [access to Web Knowledge Source](agentic-knowledge-source-how-to-web-manage.md). By default, access is enabled. Contact your admin if access is disabled.

+ An Azure AI Search service in any [public region that provides agentic retrieval](search-region-support.md). Web Knowledge Source isn't supported in private or sovereign clouds.

+ Permissions to create knowledge sources. Configure [keyless authentication](search-get-started-rbac.md) with the **Search Service Contributor** role assigned to your user account (recommended) or use an [API key](search-security-api-keys.md).

::: zone pivot="csharp"

+ Required [`Azure.Search.Documents`](https://www.nuget.org/packages/Azure.Search.Documents) package:

  + For 2026-05-01-preview features, the latest preview package: `dotnet add package Azure.Search.Documents --prerelease`

  + For 2026-04-01 features, the latest stable package: `dotnet add package Azure.Search.Documents`

::: zone-end

::: zone pivot="python"

+ Required [`azure-search-documents`](https://pypi.org/project/azure-search-documents/#history) package:

  + For 2026-05-01-preview features, the latest preview package: `pip install --pre azure-search-documents`

  + For 2026-04-01 features, the latest stable package: `pip install azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ Required REST API version:

  + For preview features: [Search Service 2026-05-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

  + For generally available features: [Search Service 2026-04-01](/rest/api/searchservice/operation-groups?view=rest-searchservice-2026-04-01&preserve-view=true)

::: zone-end

## Limitations and considerations

+ Web content is always summarized by an LLM before it's included in retrieval results. Results are cited summaries, not verbatim web text.

+ For the 2026-04-01 API version, the knowledge base must include a model reference to provide the LLM for web content summarization. Retrieval is always extractive (cited summaries). Answer synthesis and configurable reasoning effort aren't available in this version.

+ For the 2026-05-01-preview API version, the knowledge base model reference also enables [answer synthesis](agentic-retrieval-how-to-answer-synthesis.md), which produces a single LLM-formulated response instead of extracted citations.

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

# [2026-05-01-preview](#tab/2026-05-01-preview)

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

# [2026-05-01-preview](#tab/2026-05-01-preview)

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

# [2026-05-01-preview](#tab/2026-05-01-preview)

```http
### Create Web Knowledge Source
PUT {{search-url}}/knowledgesources/my-web-ks?api-version=2026-05-01-preview
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

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

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

For the complete knowledge source request schema, see [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true).

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

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
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
