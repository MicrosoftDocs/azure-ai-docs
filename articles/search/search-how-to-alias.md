---
title: Create an index alias
titleSuffix: Azure AI Search
description: Create an alias to define a secondary name that can be used to refer to an index for querying, indexing, and other operations.
author: gmndrg
ms.author: gimondra
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 05/29/2025
---

# Create an index alias in Azure AI Search

> [!IMPORTANT]
> Index aliases are currently in public preview and available under [supplemental terms of use](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

An index alias in Azure AI Search is an alternate name for an index. You can use the alias instead of the index name in your application, which minimizes future updates to production code. If you need to switch to a newer index, you can update the alias mapping.

Before using an alias, your application sends requests directly to `hotel-samples-index`.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2025-05-01-preview
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

After using an alias, your application sends requests to `my-alias`, which maps to `hotel-samples-index`.

```http
POST /indexes/my-alias/docs/search?api-version=2025-05-01-preview
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Supported scenarios

You can only use an alias with document operations or to get and update an index definition. 

Aliases can't be used to [delete an index](/rest/api/searchservice/indexes/delete), or [test text tokenization](/rest/api/searchservice/indexes/analyze), or referenced as the `targetIndexName` on an [indexer](/rest/api/searchservice/indexers/create-or-update).

## Create an index alias

You can create an alias using the preview REST API, the preview SDKs, or through the [Azure portal](https://portal.azure.com). An alias consists of the `name` of the alias and the name of the search index that the alias is mapped to. Only one index name can be specified in the `indexes` array.

### [**REST API**](#tab/rest)

You can use the [Create or Update Alias (REST preview)](/rest/api/searchservice/aliases/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true) to create an index alias.

```http
POST /aliases?api-version=2025-05-01-preview
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


Using one of the beta packages from the [Azure SDK for .NET](https://www.nuget.org/packages/Azure.Search.Documents/), you can use the following syntax to create an index alias. 

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
POST /indexes/my-alias/docs/search?api-version=2025-05-01-preview
{
    "search": "pool spa +airport",
    "searchMode": any,
    "queryType": "simple",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Update an alias

PUT is required for alias updates as described in [Create or Update Alias (REST preview)](/rest/api/searchservice/aliases/create-or-update?view=rest-searchservice-2025-05-01-preview&preserve-view=true).

```http
PUT /aliases/my-alias?api-version=2025-05-01-preview
{
    "name": "my-alias",
    "indexes": ["hotel-samples-index2"]
}
```

An update to an alias may take up to 10 seconds to propagate through the system so you should wait at least 10 seconds before deleting the index that the alias was previously mapped to.

## See also

+ [Drop and rebuild an index in Azure AI Search](search-howto-reindex.md)
