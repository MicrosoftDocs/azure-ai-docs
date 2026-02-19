---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/19/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to an Azure AI Search index that provides searchable content in an agentic retrieval pipeline. [Knowledge sources](../../agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). 

+ A search index containing plain text or vector content with a semantic configuration. [Review the index criteria for agentic retrieval](../../agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge base.

+ The latest preview version of the [`Azure.Search.Documents` client library](https://www.nuget.org/packages/Azure.Search.Documents/11.8.0-beta.1) for the .NET SDK.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using C#](knowledge-source-check-csharp.md)]

The following JSON is an example response for a search index knowledge source. Notice that the knowledge source specifies a single index name and which fields in the index to include in the query.

```json
{
  "SearchIndexParameters": {
    "SearchIndexName": "earth-at-night",
    "SourceDataFields": [
      {
        "Name": "id"
      },
      {
        "Name": "page_chunk"
      },
      {
        "Name": "page_number"
      }
    ],
    "SearchFields": [],
    "SemanticConfigurationName": "semantic-config"
  },
  "Name": "earth-knowledge-source",
  "Description": null,
  "EncryptionKey": null,
  "ETag": "<redacted>"
}
```

## Create a knowledge source

Run the following code to create a search index knowledge source.

```csharp
using Azure.Search.Documents.Indexes.Models;

// Create the knowledge source
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

### Source-specific properties

You can pass the following properties to create a search index knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `Name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `Description` | A description of the knowledge source. | String | Yes | No |
| `EncryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `SearchIndexParameters` | Parameters specific to search index knowledge sources: `search_index_name`, `SemanticConfigurationName`, `SourceDataFields`, and `SearchFields`. | Object | Yes | Yes |
| `SearchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `SemanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `SourceDataFields` | The index fields returned when you specify `include_reference_source_data` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `SearchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using Python](knowledge-source-delete-python.md)]
