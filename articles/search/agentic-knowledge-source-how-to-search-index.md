---
title: Create a Search Index Knowledge Source
description: Learn how to create a search index knowledge source, which specifies an index used by a knowledge base for agentic retrieval workloads.
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/14/2026
zone_pivot_groups: search-csharp-python-rest
---

# Create a search index knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to an Azure AI Search index that provides searchable content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md).

+ A search index containing plain text or vector content with a semantic configuration. [Review the index criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge base.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](search-security-rbac.md), but you can use [API keys](search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](search-get-started-rbac.md).

::: zone pivot="csharp"

+ The latest [`Azure.Search.Documents` preview package](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1): `dotnet add package Azure.Search.Documents --prerelease`

::: zone-end

::: zone pivot="python"

+ The latest [`azure-search-documents` preview package](https://pypi.org/project/azure-search-documents/11.7.0b2/): `pip install --pre azure-search-documents`

::: zone-end

::: zone pivot="rest"

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

::: zone-end

## Check for existing knowledge sources

::: zone pivot="csharp"

[!INCLUDE [Check for existing knowledge sources using C#](includes/how-tos/knowledge-source-check-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Check for existing knowledge sources using Python](includes/how-tos/knowledge-source-check-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [Check for existing knowledge sources using REST](includes/how-tos/knowledge-source-check-rest.md)]

::: zone-end

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

::: zone pivot="csharp"

Run the following code to create a search index knowledge source.

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
        SourceDataFields = { new SearchIndexFieldReference(name: "id"), new SearchIndexFieldReference(name: "page_chunk"), new SearchIndexFieldReference(name: "page_number") }
    }
);

await indexClient.CreateOrUpdateKnowledgeSourceAsync(indexKnowledgeSource);
Console.WriteLine($"Knowledge source '{knowledgeSourceName}' created or updated successfully.");
```

::: zone-end

::: zone pivot="python"

Run the following code to create a search index knowledge source.

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

::: zone-end

::: zone pivot="rest"

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a search index knowledge source.

```http
PUT {{search-url}}/knowledgesources/my-search-index-ks?api-version=2025-11-01-preview
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

::: zone-end

### Source-specific properties

You can pass the following properties to create a search index knowledge source.

::: zone pivot="csharp"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `SearchIndexParameters` | Parameters specific to search index knowledge sources: `search_index_name`, `SemanticConfigurationName`, `SourceDataFields`, and `SearchFields`. | Object | Yes | Yes |
| `SearchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `SemanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `SourceDataFields` | The index fields returned when you specify `include_reference_source_data` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `SearchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |

::: zone-end

::: zone pivot="python"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryption_key` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `search_index_parameters` | Parameters specific to search index knowledge sources: `search_index_name`, `semantic_configuration_name`, `source_data_fields`, and `search_fields`. | Object | Yes | Yes |
| `search_index_name` | The name of the existing search index. | String | Yes | Yes |
| `semantic_configuration_name` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `source_data_fields` | The index fields returned when you specify `include_reference_source_data` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `search_fields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |

::: zone-end

::: zone pivot="rest"

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `searchIndex` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `searchIndexParameters` | Parameters specific to search index knowledge sources: `searchIndexName`, `semanticConfigurationName`, `sourceDataFields`, and `searchFields`. | Object | Yes | Yes |
| `searchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `semanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `sourceDataFields` | The index fields returned when you specify `includeReferenceSourceData` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `searchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |

::: zone-end

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

::: zone pivot="csharp"

[!INCLUDE [Delete knowledge source using C#](includes/how-tos/knowledge-source-delete-csharp.md)]

::: zone-end

::: zone pivot="python"

[!INCLUDE [Delete knowledge source using Python](includes/how-tos/knowledge-source-delete-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [Delete knowledge source using REST](includes/how-tos/knowledge-source-delete-rest.md)]

::: zone-end

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)
+ [Agentic RAG: Build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)
+ [Azure OpenAI demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
