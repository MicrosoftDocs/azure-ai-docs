---
title: Create an index alias
titleSuffix: Azure AI Search
description: Create an alias to define a secondary name that can be used to refer to an index for querying, indexing, and other operations.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 10/01/2025
ms.update-cycle: 365-days
ms.custom:
  - ignite-2023
  - sfi-image-nochange
---

# Create an index alias in Azure AI Search

> [!IMPORTANT]
> Index aliases are currently in public preview and available under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

In Azure AI Search, an index alias is a secondary name for a search index. You can create an alias that maps to a search index and substitute the alias name in places where you would otherwise reference an index name. This gives you flexibility if you ever need to change which index your application is pointing to. Instead of updating the references to the index name in your production code, you can just update the mapping for your alias.

You can create and manage aliases in Azure AI Search service via HTTP requests (POST, GET, PUT, DELETE) against a given alias resource. Aliases are service level resources and maintained independently from search indexes. Once a search index is created, you can create an alias that maps to that search index.

Before using an alias, your application sends requests directly to `hotel-samples-index`.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-11-01-preview
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

After using an alias, your application sends requests to `my-alias`, which maps to `hotel-samples-index`.

```http
POST /indexes/my-alias/docs/search?api-version=2025-11-01-preview
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Supported scenarios

You can only use an alias with document operations or to get and update an index definition. 

Aliases can't be used to [delete an index](/rest/api/searchservice/indexes/delete), or [test text tokenization](/rest/api/searchservice/indexes/analyze), or be referenced as the `targetIndexName` on an [indexer](/rest/api/searchservice/indexers/create-or-update) or [knowledge source](agentic-knowledge-source-how-to-search-index.md).

## Create an index alias

Creating an alias establishes a mapping between an alias name and an index name. If the request is successful, the alias can be used for indexing, querying, and other operations.

Updating an alias allows you to map that alias to a different search index. When you update an existing alias, the entire definition is replaced with the contents of the request body. In general, the best pattern to use for updates is to retrieve the alias definition with a GET, modify it, and then update it with PUT.

You can create an alias using the preview REST API, the preview SDKs, or through the [Azure portal](https://portal.azure.com). An alias consists of the `name` of the alias and the name of the search index that the alias is mapped to. Only one index name can be specified in the `indexes` array.

The maximum number of aliases that you can create varies by pricing tier. For more information, see [Service limits](search-limits-quotas-capacity.md).

### [**REST API**](#tab/rest)

You can use the [Create or Update Alias (REST preview)](/rest/api/searchservice/aliases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true) to create an index alias.

```http
POST /aliases?api-version=2025-11-01-preview
{
    "name": "my-alias",
    "indexes": ["hotel-samples-index"]
}
```

### [**Azure portal**](#tab/portal)

Follow the steps below to create an index alias in the Azure portal.

1. Navigate to your search service in the [Azure portal](https://portal.azure.com).
1. Find and select **Aliases**.
1. Select **+ Add Alias**.
1. Give your index alias a name and select the search index you want to map the alias to. Then, select **Save**.

:::image type="content" source="media/search-howto-alias/create-alias-portal.png" alt-text="Screenshot creating an alias in the Azure portal." border="true":::

### [**.NET SDK**](#tab/sdk)

Using one of the preview packages from the [Azure SDK for .NET](https://www.nuget.org/packages/Azure.Search.Documents/), you can use the following syntax to create an index alias. 

```csharp
// Create a SearchIndexClient
SearchIndexClient adminClient = new SearchIndexClient(serviceEndpoint, credential);

// Create an index alias
SearchAlias myAlias = new SearchAlias("my-alias", "hotel-quickstart-index");
adminClient.CreateAlias(myAlias);
```

Index aliases are also supported in the latest preview SDKs for [Java](https://central.sonatype.com/artifact/com.azure/azure-search-documents/versions), [Python](https://pypi.org/project/azure-search-documents/#history), and [JavaScript](https://www.npmjs.com/package/@azure/search-documents?activeTab=versions).

---

## Send requests to an index alias

Aliases can be used for all document operations including querying, indexing, suggestions, and autocomplete.

This query sends the request to `my-alias`, which is mapped to an actual index on your search service. 

```http
POST /indexes/my-alias/docs/search?api-version=2025-11-01-preview
{
    "search": "pool spa +airport",
    "searchMode": any,
    "queryType": "simple",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Get an alias definition

This request returns a list of existing alias objects by name.

```http
GET https://[service name].search.windows.net/aliases?api-version=[api-version]&$select=name
api-key: [admin key]  
```

This request returns an alias definition

```http
GET https://[service name].search.windows.net/aliases/my-alias?api-version=[api-version]
api-key: [admin key]  
```

## Update an alias

The most common update to an alias is changing the index name when the underlying index is replaced with a newer version.

PUT is required for alias updates as described in [Create or Update Alias (REST preview)](/rest/api/searchservice/aliases/create-or-update?view=rest-searchservice-2025-11-01-preview&preserve-view=true).

```http
PUT /aliases/my-alias?api-version=2025-11-01-preview
{
    "name": "my-alias",
    "indexes": ["hotel-samples-index2"]
}
```

An update to an alias may take up to 10 seconds to propagate through the system so you should wait at least 10 seconds before deleting the index that the alias was previously mapped to.

If you attempt to delete an index that is currently mapped to an alias, the operation will fail with 400 (Bad Request) and an error message stating that the alias(es) that's mapped to that index must be deleted or mapped to a different index before the index can be deleted.

## See also

+ [Drop and rebuild an index in Azure AI Search](search-howto-reindex.md)
