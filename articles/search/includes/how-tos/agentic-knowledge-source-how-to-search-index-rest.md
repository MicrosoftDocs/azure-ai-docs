---
manager: nitinme
author: heidisteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: include
ms.date: 11/14/2025
---

[!INCLUDE [Feature preview](../previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to an Azure AI Search index that provides searchable content in an agentic retrieval pipeline. [Knowledge sources](../../agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve action](../../agentic-retrieval-how-to-retrieve.md) at query time.

### Usage support

| [Azure portal](../../get-started-portal-agentic-retrieval.md) | [Microsoft Foundry portal](/azure/ai-foundry/agents/concepts/what-is-foundry-iq#workflow) | [.NET SDK](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/CHANGELOG.md) | [Python SDK](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [Java SDK](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/CHANGELOG.md) | [JavaScript SDK](https://github.com/Azure/azure-sdk-for-js/blob/main/sdk/search/search-documents/CHANGELOG.md) | [REST API](/rest/api/searchservice/knowledge-sources?view=rest-searchservice-2025-11-01-preview&preserve-view=true) |
|--|--|--|--|--|--|--|
| ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ |

## Prerequisites

+ Azure AI Search in any [region that provides agentic retrieval](../../search-region-support.md). You must have [semantic ranker enabled](../../semantic-how-to-enable-disable.md). 

+ A search index containing plain text or vector content with a semantic configuration. Review the [index criteria for agentic retrieval](../../agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge base.

+ The [2025-11-01-preview](/rest/api/searchservice/operation-groups?view=rest-searchservice-2025-11-01-preview&preserve-view=true) version of the Search Service REST APIs.

+ Permission to create and use objects on Azure AI Search. We recommend [role-based access](../../search-security-rbac.md), but you can use [API keys](../../search-security-api-keys.md) if a role assignment isn't feasible. For more information, see [Connect to a search service](../../search-get-started-rbac.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources using REST](knowledge-source-check-rest.md)]

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

Use [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create a search index knowledge source.

```http
POST {{search-url}}/knowledgesources/my-search-index-ks?api-version=2025-11-01-preview
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
        ],
        "searchFields": [
          { "name": "*" }
        ]
    }
}
```

### Source-specific properties

You can pass the following properties to create a search index knowledge source.

| Name | Description | Type | Editable | Required |
|--|--|--|--|--|
| `name` | The name of the knowledge source, which must be unique within the knowledge sources collection and follow the [naming guidelines](/rest/api/searchservice/naming-rules) for objects in Azure AI Search. | String | No | Yes |
| `kind` | The kind of knowledge source, which is `searchIndex` in this case. | String | No | Yes |
| `description` | A description of the knowledge source. | String | Yes | No |
| `encryptionKey` | A [customer-managed key](../../search-security-manage-encryption-keys.md) to encrypt sensitive information in both the knowledge source and the generated objects. | Object | Yes | No |
| `searchIndexParameters` | Parameters specific to search index knowledge sources: `searchIndexName`, `semanticConfigurationName`, `sourceDataFields`, and `searchFields`. | Object | Yes | Yes |
| `searchIndexName` | The name of the existing search index. | String | Yes | Yes |
| `semanticConfigurationName` | Overrides the default semantic configuration for the search index. | String | Yes | No |
| `sourceDataFields` | The index fields returned when you specify `includeReferenceSourceData` in the knowledge base definition. These fields are used for citations and should be `retrievable`. Examples include the document name, file name, page numbers, or chapter numbers. | Array | Yes | No |
| `searchFields` | The index fields to specifically search against. When unspecified, all fields are searched. | Array | Yes | No |

---

## Assign to a knowledge base

If you're satisfied with the knowledge source, continue to the next step: specify the knowledge source in a [knowledge base](../../agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](../../agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source using REST](knowledge-source-delete-rest.md)]
