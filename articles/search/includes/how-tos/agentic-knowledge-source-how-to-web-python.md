---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

> [!IMPORTANT]
> + Web Knowledge Source, which uses Grounding with Bing Search and/or Grounding with Bing Custom Search, is a [First Party Consumption Service](https://www.microsoft.com/licensing/terms/product/ForOnlineServices/EAEAS) governed by the [Grounding with Bing terms of use](https://www.microsoft.com/en-us/bing/apis/grounding-legal-enterprise) and the [Microsoft Privacy Statement](https://www.microsoft.com/en-us/privacy/privacystatement).
>
> + The [Microsoft Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) doesn't apply to data sent to Web Knowledge Source. When Customer uses Web Knowledge Source, Customer Data flows outside the Azure compliance and Geo boundary. This also means use of Web Knowledge Source waives all elevated Government Community Cloud security and compliance commitments to include data sovereignty and screened/citizenship-based support, as applicable.
>
> + Use of Web Knowledge Source incurs costs; learn more about [pricing](https://www.microsoft.com/en-us/bing/apis/grounding-pricing).
>
> + Learn more about how Azure admins can [manage access to use of Web Knowledge Source](../../agentic-knowledge-source-how-to-web-manage.md).

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

*Web Knowledge Source* enables retrieval of real-time web data from Microsoft Bing in an agentic retrieval pipeline. [Knowledge sources](../../agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

Bing Custom Search is always the search provider for Web Knowledge Source. Although you can't specify alternative search providers or engines, you can include or exclude specific *domains*, such as https://learn.microsoft.com. When no domains are specified, Web Knowledge Source has unrestricted access to the entire public internet.

Web Knowledge Source works best alongside other knowledge sources. Use Web Knowledge Source when your proprietary content doesn't provide complete, up-to-date answers or when you want to supplement results with information from a commercial search engine.

When you use Web Knowledge Source, keep the following in mind:

+ The response is always a single, formulated answer to the query instead of raw search results from the web.

+ Because Web Knowledge Source doesn't support extractive data, your knowledge base must use [answer synthesis](../../agentic-retrieval-how-to-answer-synthesis.md) and [low or medium reasoning effort](../../agentic-retrieval-how-to-create-knowledge-base.md#create-a-knowledge-base). You also can't define answer instructions.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ❌ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure subscription with [access to Web Knowledge Source](../../agentic-knowledge-source-how-to-web-manage.md). By default, access is enabled. Contact your admin if access is disabled.

+ An Azure AI Search service in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). The service must also be in an [Azure public region](../../search-region-support.md#azure-public-regions), as Web Knowledge Source isn't supported in private or sovereign clouds.

+ The latest preview version of the [`azure-search-documents` client library](https://pypi.org/project/azure-search-documents/11.7.0b2/) for Python.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using Python](knowledge-source-check-python.md)]

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

Run the following code to create a Web Knowledge Source resource.

```python
# Create Web Knowledge Source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import WebKnowledgeSource, WebKnowledgeSourceParameters, WebKnowledgeSourceDomains

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = WebKnowledgeSource(
    name = "my-web-ks",
    description = "A sample Web Knowledge Source.",
    encryption_key = None,
    web_parameters = WebKnowledgeSourceParameters(
        domains = WebKnowledgeSourceDomains(
            allowed_domains = [ { "address": "learn.microsoft.com", "include_subpages": True } ],
            blocked_domains = [ { "address": "bing.com", "include_subpages": False } ]
        )
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

### Source-specific properties

You can pass the following properties to create a Web Knowledge Source resource.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes | Yes |
| `description` | A description of the knowledge source. When unspecified, Azure AI Search applies a default description. | String | Yes | No |
| `encryption_key` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `web_parameters` | Parameters specific to Web Knowledge Source. Currently, this is only `domains`. | Object | Yes | No |
| `domains` | Domains to allow or block from the search space. By default, the knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) to search the entire public internet. When you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search) to restrict results to the specified domains. In both cases, Bing Custom Search is the search provider. | Object | Yes | No |
| `allowed_domains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `include_subpages` to `true` or `false`. | Array | Yes | No |
| `blocked_domains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `include_subpages` to `true` or `false`. | Array | Yes | No |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using Python](knowledge-source-delete-python.md)]