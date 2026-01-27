---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/20/2025
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

+ The latest preview version of the [`Azure.Search.Documents` client library](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1) for the .NET SDK.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using C#](knowledge-source-check-csharp.md)]

The following JSON is an example response for a Web Knowledge Source resource.

```json
{
  "WebParameters": {
    "Domains": null
  },
  "Name": "my-web-ks",
  "Description": "A sample Web Knowledge Source.",
  "EncryptionKey": null,
}
```

## Create a knowledge source

Run the following code to create a Web Knowledge Source resource.

```csharp
// Create Web Knowledge Source
// Create a Web knowledge source
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

### Source-specific properties

You can pass the following properties to create a Web Knowledge Source resource.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | Yes | Yes |
| `Description` | A description of the knowledge source. When unspecified, Azure AI Search applies a default description. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in the knowledge source. | Object | Yes | No |
| `WebParameters` | Parameters specific to Web Knowledge Source. Currently, this is only `Domains`. | Object | Yes | No |
| `Domains` | Domains to allow or block from the search space. By default, the knowledge source uses [Grounding with Bing Search](/azure/ai-foundry/agents/how-to/tools/bing-grounding) to search the entire public internet. When you specify domains, the knowledge source uses [Grounding with Bing Custom Search](/azure/ai-foundry/agents/how-to/tools/bing-custom-search) to restrict results to the specified domains. In both cases, Bing Custom Search is the search provider. | Object | Yes | No |
| `AllowedDomains` | Domains to include in the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `IncludeSubpages` to `true` or `false`. | Array | Yes | No |
| `BlockedDomains` | Domains to exclude from the search space. For each domain, you must specify its `address` in the `website.com` format. You can also specify whether to include the domain's subpages by setting `IncludeSubpages` to `true` or `false`. | Array | Yes | No |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using C#](knowledge-source-delete-csharp.md)]