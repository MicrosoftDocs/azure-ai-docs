---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 07/03/2025
---

After you [create an index](search-how-to-create-search-index.md), you can use the [Azure AI Search REST APIs](/rest/api/searchservice/) to access its statistics and definition or remove it from your search service.

This article describes how to manage an index without affecting its content. For guidance on modifying an index definition, see [Update or rebuild an index in Azure AI Search](search-howto-reindex.md).

## Limitations

The pricing tier of your search service determines the maximum number and size of your indexes, fields, and documents. For more information, see [Service limits in Azure AI Search](search-limits-quotas-capacity.md).

Otherwise, the following limitations apply to index management:

+ You can't take an index offline for maintenance. Indexes are always available for search operations.

+ You can't directly copy or duplicate an index within or across search services. However, you can use the backup and restore sample for [.NET](https://github.com/Azure-Samples/azure-search-dotnet-utilities/blob/main/index-backup-restore) or [Python](https://github.com/Azure/azure-search-vector-samples/tree/main/demo-python/code/utilities/index-backup-restore) to achieve similar functionality.

## View all indexes

Use [Indexes - List (REST API)](/rest/api/searchservice/indexes/list) to retrieve all indexes on your search service.

```http
### List all indexes
GET https://[service name].search.windows.net/indexes?api-version=[api version]
    Content-Type: application/json
    api-key: [admin key]
```

## View an index's statistics

Use [Indexes - Get Statistics (REST API)](/rest/api/searchservice/indexes/get-statistics) to retrieve the document count, storage usage, and vector storage usage of an index.

```http
### Get index statistics
GET https://[service name].search.windows.net/indexes/[index name]/stats?api-version=[api version]
    Content-Type: application/json
    api-key: [admin key]
```

## View an index's definition

Use [Indexes - Get (REST API)](https://docs.microsoft.com/rest/api/searchservice/get-index) to retrieve the JSON definition of an index.

```http
### Get index definition
GET https://[service name].search.windows.net/indexes/[index name]?api-version=[api version]
    Content-Type: application/json
    api-key: [admin key]
```

## Delete an index

> [!WARNING]
> You can't undo an index deletion. Before you proceed, make sure that you want to permanently remove the index and its documents from your search service. We recommend that you test this operation in a nonproduction environment.

Use [Indexes - Delete (REST API)](https://docs.microsoft.com/rest/api/searchservice/delete-index) to permanently delete an index.

```http
### Delete an index
DELETE https://[service name].search.windows.net/indexes/[index name]?api-version=[api version]
    Content-Type: application/json
    api-key: [admin key]
```

If the index was deleted successfully, you should receive an `HTTP/1.1 204 No Content` response.
