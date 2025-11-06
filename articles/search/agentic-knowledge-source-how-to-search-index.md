---
title: Create a Search Index Knowledge Source
titleSuffix: Azure AI Search
description: A search index knowledge source specifies an index used by a knowledge base for agentic retrieval workloads.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 11/03/2025
---

# Create a search index knowledge source

[!INCLUDE [Feature preview](./includes/previews/preview-generic.md)]

A *search index knowledge source* specifies a connection to an Azure AI Search index that provides searchable content in an agentic retrieval pipeline. [Knowledge sources](agentic-knowledge-source-overview.md) are created independently, referenced in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md), and used as grounding data when an agent or chatbot calls a [retrieve](/rest/api/searchservice/knowledge-retrieval/retrieve?view=rest-searchservice-2025-11-01-preview&preserve-view=true) action at query time.

## Prerequisites

+ Azure AI Search, in any [region that provides agentic retrieval](search-region-support.md). You must have [semantic ranker enabled](semantic-how-to-enable-disable.md). 

+ A search index containing plain text or vector content with a semantic configuration. [Review the index criteria for agentic retrieval](agentic-retrieval-how-to-create-index.md#criteria-for-agentic-retrieval). The index must be on the same search service as the knowledge base.

To try the examples in this article, we recommend [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for sending preview REST API calls to Azure AI Search.

> [!NOTE]
> Although you can use the Azure portal to create search index knowledge sources, the portal uses the 2025-08-01-preview, which uses the previous "knowledge agent" terminology and doesn't support all 2025-11-01-preview features. For help with breaking changes, see [Migrate your agentic retrieval code](agentic-retrieval-how-to-migrate.md).

## Check for existing knowledge sources

[!INCLUDE [Check for existing knowledge sources](includes/how-tos/knowledge-source-check-rest.md)]

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

To create a search index knowledge source:

1. Set environment variables at the top of your file.

    ```http
    @search-url = <YOUR SEARCH SERVICE URL>
    @api-key = <YOUR ADMIN API KEY>
    ```

1. Use the 2025-11-01-preview of [Knowledge Sources - Create or Update (REST API)](/rest/api/searchservice/knowledge-sources/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) or an Azure SDK preview package that provides equivalent functionality to formulate the request.

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

1. Select **Send Request**.

### Source-specific properties

You can pass the following properties to create a search index knowledge source.

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

## Assign to a knowledge base

If you're satisfied with the index, continue to the next step: specifying the knowledge source in a [knowledge base](agentic-retrieval-how-to-create-knowledge-base.md).

After the knowledge base is configured, use the [retrieve action](agentic-retrieval-how-to-retrieve.md) to query the knowledge source.

## Delete a knowledge source

[!INCLUDE [Delete knowledge source](includes/how-tos/knowledge-source-delete-rest.md)]

## Related content

+ [Agentic retrieval in Azure AI Search](agentic-retrieval-overview.md)

+ [Agentic RAG: build a reasoning retrieval engine with Azure AI Search (YouTube video)](https://www.youtube.com/watch?v=PeTmOidqHM8)

+ [Azure OpenAI Demo featuring agentic retrieval](https://github.com/Azure-Samples/azure-search-openai-demo)
