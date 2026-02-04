---
title: "Quickstart: Full-Text Search in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to create, load, and query your first search index using an import wizard in the Azure portal. This quickstart uses a fictitious hotel dataset for sample data.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 12/05/2025
ms.custom:
  - mode-ui
  - ignite-2023
  - ignite-2024
---

# Quickstart: Full-text search in the Azure portal

[!INCLUDE [Import data (new) instructions](includes/quickstarts/search-get-started-portal-new-wizard.md)]

<!-- Removed this from metadata. Remove the the zone pivot entry on next PR
zone_pivot_groups: azure-portal-wizards -->

<!-- ::: zone pivot="import-data-new"
[!INCLUDE [Import data (new) instructions](includes/quickstarts/search-get-started-portal-new-wizard.md)]
::: zone-end

::: zone pivot="import-data"
[!INCLUDE [Import data instructions](includes/quickstarts/search-get-started-portal-old-wizard.md)]
::: zone-end -->

## Monitor indexer progress

You can monitor the creation of the indexer and index in the Azure portal. The **Overview** page provides links to the objects created on your search service.

To monitor the progress of the indexer:

1. From the left pane, select **Indexers**.

1. Find **hotels-sample-indexer** in the list.

   :::image type="content" source="media/search-get-started-portal/indexers-status.png" alt-text="Screenshot that shows the creation of the indexer in progress in the Azure portal." lightbox="media/search-get-started-portal/indexers-status.png":::

   It can take a few minutes for the results to update. You should see the newly created indexer with a status of **In progress** or **Success**. The list also shows the number of documents indexed.

## Check search index results

1. From the left pane, select **Indexes**.

1. Select **hotels-sample-index**. If the index has zero documents or storage, wait for the Azure portal to refresh.

   :::image type="content" source="media/search-get-started-portal/indexes-list.png" alt-text="Screenshot of the Indexes list on the Azure AI Search service dashboard in the Azure portal." lightbox="media/search-get-started-portal/indexes-list.png":::

1. Select the **Fields** tab to view the index schema.

1. Check which fields are **Filterable** or **Sortable** so that you know what queries to write.

   :::image type="content" source="media/search-get-started-portal/index-schema-definition.png" alt-text="Screenshot that shows the schema definition for an index in the Azure AI Search service in the Azure portal." lightbox="media/search-get-started-portal/index-schema-definition.png":::

## Add or change fields

On the **Fields** tab, you can create a field by selecting **Add field** and specifying a name, [supported data type](/rest/api/searchservice/supported-data-types), and attributes.

Changing existing fields is more difficult. Existing fields have a physical representation in the search index, so they aren't modifiable, not even in code. To fundamentally change an existing field, you must create a new field to replace the original. You can add other constructs, such as scoring profiles and CORS options, to an index at any time.

Review the index definition options to understand what you can and can't edit during index design. If an option appears dimmed, you can't modify or delete it.

## Query with Search explorer

You now have a search index that can be queried using [**Search explorer**](search-explorer.md), which sends REST calls that conform to [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-11-01-preview&preserve-view=true). This tool supports [simple query syntax](/rest/api/searchservice/simple-query-syntax-in-azure-search) and [full Lucene query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search) for keyword search.

To query your search index:

1. On the **Search explorer** tab, enter text to search on.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-string.png" alt-text="Screenshot that shows how to enter and run a query in the  Search Explorer tool." lightbox="media/search-get-started-portal/search-explorer-query-string.png":::

1. To jump to nonvisible areas of the output, use the mini map.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-results.png" alt-text="Screenshot that shows long results for a query in the Search Explorer tool and the mini-map." lightbox="media/search-get-started-portal/search-explorer-query-results.png":::

1. To specify syntax, switch to the JSON view.

   :::image type="content" source="media/search-get-started-portal/search-explorer-change-view.png" alt-text="Screenshot of the JSON view selector." lightbox="media/search-get-started-portal/search-explorer-change-view.png":::

## Example queries for hotels-sample index

The following examples assume the JSON view and the latest preview REST API version.

> [!TIP]
> The JSON view supports intellisense for parameter name completion. Place your cursor inside the JSON view and enter a space character to see a list of all query parameters. You can also enter a letter, like `s`, to see only the query parameters that begin with that letter.
>
> Intellisense doesn't exclude invalid parameters, so use your best judgment.

### Filter examples

Parking, tags, renovation date, rating, and location are filterable.

```json
{
    "search": "beach OR spa",
    "select": "HotelId, HotelName, Description, Rating",
    "count": true,
    "top": 10,
    "filter": "Rating gt 4"
}
```

Boolean filters assume "true" by default.

```json
{
    "search": "beach OR spa",
    "select": "HotelId, HotelName, Description, Rating",
    "count": true,
    "top": 10,
    "filter": "ParkingIncluded"
}
```

Geospatial search is filter based. The `geo.distance` function filters all results for positional data based on the specified `Location` and `geography'POINT` coordinates. The query seeks hotels within five kilometers of the latitude and longitude coordinates `-122.12 47.67`, which is "Redmond, Washington, USA." The query displays the total number of matches `&$count=true` with the hotel names and address locations.

```json
{
    "search": "*",
    "select": "HotelName, Address/City, Address/StateProvince",
    "count": true,
    "top": 10,
    "filter": "geo.distance(Location, geography'POINT(-122.12 47.67)') le 5"
}
```

### Full Lucene syntax examples

The default syntax is [simple syntax](query-simple-syntax.md), but if you want fuzzy search, term boosting, or regular expressions, specify the [full syntax](query-lucene-syntax.md).

```json
{
    "queryType": "full",
    "search": "seatle~",
    "select": "HotelId, HotelName,Address/City, Address/StateProvince",
    "count": true
}
```

Misspelled query terms, like `seatle` instead of `Seattle`, don't return matches in a typical search. The `queryType=full` parameter invokes the full Lucene query parser, which supports the tilde (`~`) operand. When you use these parameters, the query performs a fuzzy search for the specified keyword and matches on terms that are similar but not an exact match.

Take a minute to try these example queries on your index. For more information, see [Querying in Azure AI Search](search-query-overview.md).

## Clean up resources

When you work in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

In the Azure portal, you can find and manage resources by selecting **All resources** or **Resource groups** from the left pane.

> [!NOTE]
> If you're using a free search service, remember that the limit is three indexes, three indexers, and three data sources. You can delete individual objects in the Azure portal to stay under the limit.

## Next step

Try an Azure portal wizard to generate a ready-to-use web app that runs in a browser. Use this wizard on the small index you created in this quickstart, or use [sample data](https://github.com/Azure-Samples/azure-search-sample-data) for a richer search experience.

> [!div class="nextstepaction"]
> [Quickstart: Create a demo search app in the Azure portal](search-create-app-portal.md)
