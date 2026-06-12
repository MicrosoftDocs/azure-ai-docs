---
title: Create an Index Alias
description: Create an alias to define a secondary name that can be used to refer to an index for querying, indexing, and other operations.
ms.reviewer: gimondra
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 04/27/2026
ms.update-cycle: 365-days
ms.custom:
  - ignite-2023
  - sfi-image-nochange
  - ai-usage: ai-assisted
---

# Create an index alias in Azure AI Search

In Azure AI Search, an index alias is a secondary name for a search index. You can create an alias that maps to a search index and substitute the alias name in places where you'd otherwise reference an index name. This feature provides flexibility if you need to change the index to which your application points. Instead of updating references to the index name in your production code, you can simply update the alias mapping.

You can create and manage aliases on a search service via HTTP requests (POST, GET, PUT, or DELETE) against a given alias resource. Aliases are service-level resources that are maintained independently from search indexes. After you create a search index, you can create an alias that maps to it.

Before using an alias, your application sends requests directly to `hotel-samples-index`.

```http
POST /indexes/hotel-samples-index/docs/search?api-version=2026-04-01
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

After using an alias, your application sends requests to `my-alias`, which maps to `hotel-samples-index`.

```http
POST /indexes/my-alias/docs/search?api-version=2026-04-01
{
    "search": "pool spa +airport",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Prerequisites

+ An [Azure AI Search service](search-create-service-portal.md) in any region and pricing tier.
+ An existing [search index](search-how-to-create-search-index.md) to which you want to map the alias.
+ Permissions to create an alias:
  + For key-based authentication, an [admin API key](search-security-api-keys.md) for your search service.
  + For role-based authentication, the [Search Service Contributor](search-security-rbac.md) role.

## Limitations and considerations

+ You can only use an alias with document operations or to get and update an index definition.
+ You can't use an alias to [delete an index](/rest/api/searchservice/indexes/delete) or [test text tokenization](/rest/api/searchservice/indexes/analyze).
+ You can't reference an alias as the `targetIndexName` on an [indexer](/rest/api/searchservice/indexers/create-or-update) or [knowledge source](agentic-knowledge-source-how-to-search-index.md).

## Create an index alias

Creating an alias establishes a mapping between an alias name and an index name. If the request is successful, you can use the alias for indexing, querying, and other operations.

You can create an alias by using the REST API, Azure SDKs, or the Azure portal. An alias consists of the `name` of the alias and the name of the search index to which the alias maps. You can specify only one index name in the `indexes` array.

The maximum number of aliases that you can create varies by pricing tier. For more information, see [Index alias limits](search-limits-quotas-capacity.md#index-alias-limits).

### [**REST API**](#tab/rest)

Use the latest stable version of [Aliases - Create](/rest/api/searchservice/aliases/create?view=rest-searchservice-2026-04-01&preserve-view=true) (REST API) to create an index alias.

```http
POST /aliases?api-version=2026-04-01
{
    "name": "my-alias",
    "indexes": ["hotel-samples-index"]
}
```

### [**Azure SDKs**](#tab/sdk)

Index aliases are supported in the latest stable Azure SDKs for [.NET](https://www.nuget.org/packages/Azure.Search.Documents/), [Java](https://central.sonatype.com/artifact/com.azure/azure-search-documents/versions), [JavaScript](https://www.npmjs.com/package/@azure/search-documents?activeTab=versions), and [Python](https://pypi.org/project/azure-search-documents/#history).

The following example shows how to create an alias with the Azure SDK for .NET.

```csharp
// Create a SearchIndexClient
SearchIndexClient adminClient = new SearchIndexClient(serviceEndpoint, credential);

// Create an index alias
SearchAlias myAlias = new SearchAlias("my-alias", "hotel-samples-index");
adminClient.CreateAlias(myAlias);
```

### [**Azure portal**](#tab/portal)

1. Go to your search service in the [Azure portal](https://portal.azure.com).
1. From the left pane, select **Search management** > **Aliases**.
1. Select **Add alias**.
1. Enter a name for your index alias.
1. Select the search index to which you want to map your alias.
1. Select **Save**.

    :::image type="content" source="media/search-howto-alias/create-alias-portal.png" lightbox="media/search-howto-alias/create-alias-portal.png" alt-text="Screenshot showing how to create an index alias in the Azure portal." border="true":::

---

## Send requests to an index alias

You can use an alias for all document operations, including querying, indexing, suggestions, and autocomplete.

The following query sends the request to `my-alias`, which is mapped to an actual index on your search service.

```http
POST /indexes/my-alias/docs/search?api-version=2026-04-01
{
    "search": "pool spa +airport",
    "searchMode": "any",
    "queryType": "simple",
    "select": "HotelId, HotelName, Category, Description",
    "count": true
}
```

## Get an alias definition

Use [Aliases - List](/rest/api/searchservice/aliases/list?view=rest-searchservice-2026-04-01&preserve-view=true) (REST API) to return a list of existing alias objects by name.

```http
GET /aliases?api-version=2026-04-01&$select=name
```

Use [Aliases - Get](/rest/api/searchservice/aliases/get?view=rest-searchservice-2026-04-01&preserve-view=true) (REST API) to return the definition of a specific alias.

```http
GET /aliases/my-alias?api-version=2026-04-01
```

## Update an alias

The most common update to an alias is changing the index name when the underlying index is replaced with a newer version.

Use [Aliases - Create or Update](/rest/api/searchservice/aliases/create-or-update?view=rest-searchservice-2026-04-01&preserve-view=true) (REST API) to update an alias. The following example shows how to update `my-alias` to point to `hotel-samples-index2` instead of `hotel-samples-index`.

```http
PUT /aliases/my-alias?api-version=2026-04-01
{
    "name": "my-alias",
    "indexes": ["hotel-samples-index2"]
}
```

An update to an alias might take up to 10 seconds to propagate through the system, so wait at least 10 seconds before you delete the index to which the alias previously mapped.

If you attempt to delete an index that's currently mapped to an alias, the operation fails with 400 (Bad Request) and an error message stating that the alias(es) that's mapped to that index must be deleted or mapped to a different index before the index can be deleted.

## Related content

+ [Drop and rebuild an index in Azure AI Search](search-howto-reindex.md)
