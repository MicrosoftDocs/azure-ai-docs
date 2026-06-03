---
title: Create a Search Index Knowledge Source
description: Learn how to create a search index knowledge source, which specifies an index used by a knowledge base for agentic retrieval workloads.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/02/2026
ai-usage: ai-assisted
zone_pivot_groups: search-csharp-python-rest
---

# Create a search index knowledge source

[!INCLUDE [GA feature](./includes/previews/agentic-retrieval-ga-feature.md)]

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> It's your responsibility to manage whether your data will flow outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

A *search index knowledge source* connects an existing Azure AI Search index, including its indexed text and vectors, to an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when the knowledge base is [queried at runtime](agentic-retrieval-how-to-retrieve.md).

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ An Azure AI Search service in any [region that provides agentic retrieval](search-region-support.md).

+ A search index containing plain text or vector content with a semantic configuration. [Review the index criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge base.

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

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check.md)]

The following JSON is an example response for a search index knowledge source. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json
{
  "name": "my-search-index-ks",
  "kind": "searchIndex",
  "description": "A sample search index knowledge source.",
  "encryptionKey": null,
  "searchIndexParameters": {
    "searchIndexName": "my-search-index",
    "semanticConfigurationName": null,
    "sourceDataFields": [],
    "searchFields": []
  }
}
```

## Create a knowledge source

Run the following code to create a search index knowledge source.

::: zone pivot="csharp"

# [2026-05-01-preview](#tab/2026-05-01-preview)

```csharp
// Create a search index knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var indexKnowledgeSource = new SearchIndexKnowledgeSource(
    name: knowledgeSourceName,
    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: indexName)
    {
        SearchFields = { new SearchIndexFieldReference(name: "page_chunk") },
        SourceDataFields = { new SearchIndexFieldReference(name: "id"), new SearchIndexFieldReference(name: "page_chunk"), new SearchIndexFieldReference(name: "page_number") }
    }
);

await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet-preview&preserve-view=true), [SearchIndexKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.searchindexknowledgesource?view=azure-dotnet-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```csharp
// Create a search index knowledge source
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure;

var indexClient = new SearchIndexClient(new Uri(searchEndpoint), new AzureKeyCredential(apiKey));

var indexKnowledgeSource = new SearchIndexKnowledgeSource(
    name: knowledgeSourceName,
    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: indexName)
    {
        SemanticConfigurationName = "semantic_config",
        SearchFields = { new SearchIndexFieldReference(name: "page_chunk") },
        SourceDataFields = { new SearchIndexFieldReference(name: "id"), new SearchIndexFieldReference(name: "page_chunk"), new SearchIndexFieldReference(name: "page_number") }
    }
);

await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
```

**Reference:** [SearchIndexClient](/dotnet/api/azure.search.documents.indexes.searchindexclient?view=azure-dotnet&preserve-view=true), [SearchIndexKnowledgeSource](/dotnet/api/azure.search.documents.indexes.models.searchindexknowledgesource?view=azure-dotnet&preserve-view=true)

---

::: zone-end

::: zone pivot="python"

# [2026-05-01-preview](#tab/2026-05-01-preview)

```python
# Create a search index knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters, SearchIndexFieldReference

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = SearchIndexKnowledgeSource(
    name = "my-search-index-ks",
    description= "This knowledge source pulls from an existing index designed for agentic retrieval.",
    encryption_key = None,
    search_index_parameters = SearchIndexKnowledgeSourceParameters(
        search_index_name = "search_index_name",
        semantic_configuration_name = "semantic_configuration_name",
        source_data_fields = [
            SearchIndexFieldReference(name="description"),
            SearchIndexFieldReference(name="category"),
        ],
        search_fields = [
            SearchIndexFieldReference(name="id")
        ],
    )
)

index_client.create_or_update_knowledge_source(knowledge_source)
print(f"Knowledge source '{knowledge_source.name}' created or updated successfully.")
```

**Reference:** [SearchIndexClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexclient)

# [2026-04-01](#tab/2026-04-01)

```python
# Create a search index knowledge source
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters, SearchIndexFieldReference

index_client = SearchIndexClient(endpoint = "search_url", credential = AzureKeyCredential("api_key"))

knowledge_source = SearchIndexKnowledgeSource(
    name = "my-search-index-ks",
    description= "This knowledge source pulls from an existing index designed for agentic retrieval.",
    encryption_key = None,
    search_index_parameters = SearchIndexKnowledgeSourceParameters(
        search_index_name = "search_index_name",
        semantic_configuration_name = "semantic_configuration_name",
        source_data_fields = [
            SearchIndexFieldReference(name="description"),
            SearchIndexFieldReference(name="category"),
        ],
        search_fields = [
            SearchIndexFieldReference(name="id")
        ],
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
### Create a search index knowledge source
PUT {{search-url}}/knowledgesources/my-search-index-ks?api-version=2026-05-01-preview
api-key: {{api-key}}
Content-Type: application/json

{
    "name": "my-search-index-ks",
    "kind": "searchIndex",
    "description": "This knowledge source pulls from an existing index designed for agentic retrieval.",
    "encryptionKey": null,
    "searchIndexParameters": {
        "searchIndexName": "<YOUR INDEX NAME>",
        "semanticConfigurationName": "my-semantic-config",
        "sourceDataFields": [
          { "name": "description" },
          { "name": "category" }
        ]
    }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

# [2026-04-01](#tab/2026-04-01)

```http
### Create a search index knowledge source
PUT {{search-url}}/knowledgesources/my-search-index-ks?api-version=2026-04-01
api-key: {{api-key}}
Content-Type: application/json

{
    "name": "my-search-index-ks",
    "kind": "searchIndex",
    "description": "This knowledge source pulls from an existing index designed for agentic retrieval.",
    "encryptionKey": null,
    "searchIndexParameters": {
        "searchIndexName": "<YOUR INDEX NAME>",
        "semanticConfigurationName": "my-semantic-config",
        "sourceDataFields": [
          { "name": "description" },
          { "name": "category" }
        ]
    }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true)

---

::: zone-end

### Source-specific properties

The following properties apply to search index knowledge sources.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `SearchIndexParameters` | Parameters specific to search index knowledge sources: `SearchIndexName`, `SemanticConfigurationName`, `SourceDataFields`, `SearchFields`, and `BaseFilter` (2026-05-01-preview only). | Object | Yes | Yes |
| `SearchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `SemanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `SourceDataFields` | The index fields returned when you specify `IncludeReferenceSourceData` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `SearchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |
| `BaseFilter` | A default filter expression persisted on the knowledge source that applies to every retrieve request. At retrieve time, the value is AND-composed with the request's `FilterAddOn`. Available in the 2026-05-01-preview API only. | String | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `search_index_parameters` | Parameters specific to search index knowledge sources: `search_index_name`, `semantic_configuration_name`, `source_data_fields`, `search_fields`, and `base_filter` (2026-05-01-preview only). | Object | Yes | Yes |
| `search_index_name` | The name of the existing search index. | String | Yes | Yes |
| `semantic_configuration_name` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `source_data_fields` | The index fields returned when you specify `include_reference_source_data` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `search_fields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |
| `base_filter` | A default filter expression persisted on the knowledge source that applies to every retrieve request. At retrieve time, the value is AND-composed with the request's `filter_add_on`. Available in the 2026-05-01-preview API only. | String | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `searchIndex` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `searchIndexParameters` | Parameters specific to search index knowledge sources: `searchIndexName`, `semanticConfigurationName`, `sourceDataFields`, `searchFields`, and `baseFilter` (2026-05-01-preview only). | Object | Yes | Yes |
| `searchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `semanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `sourceDataFields` | The index fields returned when you specify `includeReferenceSourceData` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `searchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |
| `baseFilter` | A default filter expression persisted on the knowledge source that applies to every retrieve request. At retrieve time, the value is AND-composed with the request's `filterAddOn`. Available in the 2026-05-01-preview API only. | String | Yes | No |

::: zone-end

### Persist a base filter on a knowledge source (preview)

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

In the `2026-05-01-preview` API, a search index knowledge source can persist a default filter through the `baseFilter` property. Use `baseFilter` when the same filter expression should apply to every retrieve request that uses the knowledge source, so callers don't have to repeat the filter on every call.

> [!NOTE]
> Starting with `2026-05-01-preview`, `semanticConfigurationName` is optional on search index knowledge sources. The examples in this section omit it. Earlier API versions still require `semanticConfigurationName`. If your knowledge source needs to support both the older and newer API versions, keep specifying it.

The following example stores a base filter on a search index knowledge source:

::: zone pivot="csharp"

```csharp
var knowledgeSource = new SearchIndexKnowledgeSource(
    name: "public-docs-ks",
    searchIndexParameters: new SearchIndexKnowledgeSourceParameters(searchIndexName: "public-docs-index")
    {
        BaseFilter = "isPublished eq true and accessScope eq 'public'"
    }
);

await indexClient.CreateOrUpdateKnowledgeSourceAsync(knowledgeSource);
```

**Reference:** [SearchIndexKnowledgeSourceParameters](/dotnet/api/azure.search.documents.indexes.models.searchindexknowledgesourceparameters?view=azure-dotnet-preview&preserve-view=true)

::: zone-end

::: zone pivot="python"

```python
knowledge_source = SearchIndexKnowledgeSource(
    name="public-docs-ks",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name="public-docs-index",
        base_filter="isPublished eq true and accessScope eq 'public'",
    ),
)

index_client.create_or_update_knowledge_source(knowledge_source)
```

**Reference:** [SearchIndexKnowledgeSourceParameters](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindexknowledgesourceparameters)

::: zone-end

::: zone pivot="rest"

```http
PUT {{search-url}}/knowledgesources/public-docs-ks?api-version=2026-05-01-preview
Content-Type: application/json
api-key: {{search-api-key}}

{
  "name": "public-docs-ks",
  "kind": "searchIndex",
  "searchIndexParameters": {
    "searchIndexName": "public-docs-index",
    "baseFilter": "isPublished eq true and accessScope eq 'public'"
  }
}
```

**Reference:** [Knowledge Sources - Create or Update](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2026-05-01-preview&preserve-view=true)

::: zone-end

At retrieve time, `knowledgeSourceParams.filterAddOn` adds request-specific constraints to the stored base filter:

::: zone pivot="csharp"

```csharp
var retrievalRequest = new KnowledgeBaseRetrievalRequest();
retrievalRequest.KnowledgeSourceParams.Add(
    new SearchIndexKnowledgeSourceParams("public-docs-ks")
    {
        FilterAddOn = "category eq 'Benefits'"
    }
);
```

::: zone-end

::: zone pivot="python"

```python
request = KnowledgeBaseRetrievalRequest(
    knowledge_source_params=[
        SearchIndexKnowledgeSourceParams(
            knowledge_source_name="public-docs-ks",
            filter_add_on="category eq 'Benefits'",
        ),
    ],
)
```

::: zone-end

::: zone pivot="rest"

```json
{
  "knowledgeSourceParams": [
    {
      "knowledgeSourceName": "public-docs-ks",
      "kind": "searchIndex",
      "filterAddOn": "category eq 'Benefits'"
    }
  ]
}
```

::: zone-end

The effective filter is composed as:

```text
baseFilter AND filterAddOn
```

Because the filters are combined with `AND`, `filterAddOn` can only narrow the persisted base filter. It can't replace or broaden it.

## Assign to a knowledge base

If you're satisfied with the knowledge source, [add it to a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

## Query a knowledge base

After the knowledge base is configured, [call the retrieve action or MCP endpoint](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete a knowledge source](includes/how-tos/knowledge-source-delete.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [What is a knowledge source?](agentic-knowledge-source-overview.md)
+ [Create a knowledge base](agentic-retrieval-how-to-create-knowledge-base.md)
+ [Query a knowledge base](agentic-retrieval-how-to-retrieve.md)
