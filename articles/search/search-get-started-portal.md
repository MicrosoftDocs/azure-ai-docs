---
title: "Quickstart: Keyword Search in the Azure Portal"
titleSuffix: Azure AI Search
description: Learn how to create, load, and query your first search index using the Import Data wizard in the Azure portal. This quickstart uses a fictitious hotel dataset for sample data.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 03/04/2025
ms.custom:
  - mode-ui
  - ignite-2023
  - ignite-2024
---

# Quickstart: Create a search index in the Azure portal

In this quickstart, you create your first Azure AI Search index using the [**Import data** wizard](search-import-data-portal.md) and a built-in sample of fictitious hotel data hosted by Microsoft. The wizard requires no code to create an index, helping you write interesting queries within minutes.

The wizard creates multiple objects on your search service, including a [searchable index](search-what-is-an-index.md), an [indexer](search-indexer-overview.md), and a data source connection for automated data retrieval. At the end of this quickstart, we review each object.

> [!NOTE]
> The **Import data** wizard includes options for OCR, text translation, and other AI enrichments that aren't covered in this quickstart. For a similar walkthrough that focuses on applied AI, see [Quickstart: Create a skillset in the Azure portal](search-get-started-skillset.md).

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. You can use a free service for this quickstart.

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](search-import-data-portal.md).

### Check for network access

For this quickstart, which uses built-in sample data, make sure your search service doesn't have [network access controls](service-configure-firewall.md). The Azure portal controller uses a public endpoint to retrieve data and metadata from the Microsoft-hosted data source. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

### Check for space

Many customers start with a free search service, which is limited to three indexes, three indexers, and three data sources. This quickstart creates one of each, so before you begin, make sure you have room for extra objects.

On the **Overview** tab, select **Usage** to see how many indexes, indexers, and data sources you currently have.

   :::image type="content" source="media/search-get-started-portal/overview-quota-usage.png" alt-text="Screenshot of the Overview page for an Azure AI Search service instance in the Azure portal, showing the number of indexes, indexers, and data sources." lightbox="media/search-get-started-portal/overview-quota-usage.png":::

## Start the wizard

1. Sign in to the [Azure portal](https://portal.azure.com/).

1. Go to your search service.

1. On the **Overview** tab, select **Import data** to start the wizard.

   :::image type="content" source="media/search-import-data-portal/import-data-cmd.png" alt-text="Screenshot that shows how to open the Import data wizard in the Azure portal.":::

## Create and load a search index

In this section, you create and load an index in four steps:

1. [Connect to a data source](#connect-to-a-data-source)
1. [Skip configuration for cognitive skills](#skip-configuration-for-cognitive-skills)
1. [Configure the index](#configure-the-index)
1. [Configure and run the indexer](#configure-and-run-the-indexer)

### Connect to a data source

The wizard creates a data source connection to sample data that Microsoft hosts on Azure Cosmos DB. The sample data is accessed through a public endpoint, so you don't need an Azure Cosmos DB account or source files for this step.

To connect to the sample data:

1. On **Connect to your data**, expand the **Data Source** dropdown list and select **Samples**.

1. Select **hotels-sample** from the list of built-in samples.

1. Select **Next: Add cognitive skills (Optional)** to continue.

   :::image type="content" source="media/search-get-started-portal/import-hotels-sample.png" alt-text="Screenshot that shows how to select the hotels-sample data source in the Import data wizard.":::

### Skip configuration for cognitive skills

Although the wizard supports skillset creation and [AI enrichment](cognitive-search-concept-intro.md) during indexing, cognitive skills are beyond the scope of this quickstart.

To skip this step in the wizard:

1. On **Add cognitive skills**, ignore the AI enrichment configuration options.

1. Select **Next: Customize target index** to continue.

   :::image type="content" source="media/search-get-started-portal/skip-cognitive-skills.png" alt-text="Screenshot that shows how to Skip to the Customize target index tab in the Import data wizard.":::

> [!TIP]
> To get started with AI enrichment, see [Quickstart: Create a skillset in the Azure portal](search-get-started-skillset.md).

### Configure the index

The wizard infers a schema for the hotels-sample index. To configure the index:

1. Accept the system-generated values for the **Index name** (_hotels-sample-index_) and **Key** (_HotelId_).

1. Accept the system-generated values for all field attributes.

1. Select **Next: Create an indexer** to continue.

   :::image type="content" source="media/search-get-started-portal/hotels-sample-generated-index.png" alt-text="Screenshot that shows the generated index definition for the hotels-sample data source in the Import data wizard.":::

At a minimum, the search index requires a name and a collection of fields. The wizard scans for unique string fields and marks one as the document key, which uniquely identifies each document in the index.

Each field has a name, a data type, and attributes that control how the field is used in the index. Use the checkboxes to enable or disable the following attributes:

| Attribute | Description | Applicable data types |
|-----------|-------------|------------------------|
| Retrievable | Fields returned in a query response. | Strings and integers |
| Filterable | Fields that accept a filter expression. | Integers |
| Sortable | Fields that accept an orderby expression. | Integers |
| Facetable | Fields used in a faceted navigation structure. | Integers |
| Searchable | Fields used in full text search. Strings are searchable, but numeric and Boolean fields are often marked as not searchable. | Strings |

Attributes affect storage in different ways. For example, filterable fields consume extra storage, while retrievable fields don't. For more information, see [Example demonstrating the storage implications of attributes and suggesters](search-what-is-an-index.md#example-demonstrating-the-storage-implications-of-attributes-and-suggesters).

If you want autocomplete or suggested queries, specify language **Analyzers** or **Suggesters**.

### Configure and run the indexer

Finally, you configure and run the indexer, which defines an executable process. The data source and index are also created in this step.

To configure and run the indexer:

1. Accept the system-generated value for the **Indexer name** (_hotels-sample-indexer_).

1. For this quickstart, use the default option to run the indexer immediately and only once. The sample data is static, so you can't enable change tracking.

1. Select **Submit** to simultaneously create and run the indexer.

   :::image type="content" source="media/search-get-started-portal/hotels-sample-indexer.png" alt-text="Screenshot that shows how to configure the indexer for the hotels-sample data source in the Import data wizard.":::

## Monitor indexer progress

You can monitor the creation of the indexer and index in the Azure portal. The **Overview** tab provides links to the resources created in your search service.

To monitor the progress of the indexer:

1. Go to your search service in the [Azure portal](https://portal.azure.com/).

1. From the left pane, select **Indexers**.

   :::image type="content" source="media/search-get-started-portal/indexers-status.png" alt-text="Screenshot that shows the creation of the indexer in progress in the Azure portal.":::

   It can take a few minutes for the results to update. You should see the newly created indexer with a status of **In progress** or **Success**. The list also shows the number of documents indexed.

## Check search index results

1. Go to your search service in the [Azure portal](https://portal.azure.com/).

1. From the left pane, select **Indexes**.

1. Select **hotels-sample-index**. If the index has zero documents or storage, wait for the Azure portal to refresh.

   :::image type="content" source="media/search-get-started-portal/indexes-list.png" alt-text="Screenshot of the Indexes list on the Azure AI Search service dashboard in the Azure portal.":::

1. Select the **Fields** tab to view the index schema.

1. Check which fields are **Filterable** or **Sortable** so that you know what queries to write.

   :::image type="content" source="media/search-get-started-portal/index-schema-definition.png" alt-text="Screenshot that shows the schema definition for an index in the Azure AI Search service in the Azure portal.":::

## Add or change fields

On the **Fields** tab, you can create a field by selecting **Add field** and specifying a name, [supported data type](/rest/api/searchservice/supported-data-types), and attributes.

Changing existing fields is more difficult. Existing fields have a physical representation in the search index, so they aren't modifiable, not even in code. To fundamentally change an existing field, you must create a new field to replace the original. You can add other constructs, such as scoring profiles and CORS options, to an index at any time.

Review the index definition options to understand what you can and can't edit during index design. If an option appears dimmed, you can't modify or delete it.

## Query with Search explorer

You now have a search index that can be queried using [**Search explorer**](search-explorer.md), which sends REST calls that conform to the [Search POST REST API](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2024-05-01-preview&preserve-view=true). This tool supports [simple query syntax](/rest/api/searchservice/simple-query-syntax-in-azure-search) and [full Lucene query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search).

To query your search index:

1. On the **Search explorer** tab, enter text to search on.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-string.png" alt-text="Screenshot that shows how to enter and run a query in the  Search Explorer tool.":::

1. To jump to nonvisible areas of the output, use the mini map.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-results.png" alt-text="Screenshot that shows long results for a query in the Search Explorer tool and the mini-map.":::

1. To specify syntax, switch to the JSON view.

   :::image type="content" source="media/search-get-started-portal/search-explorer-change-view.png" alt-text="Screenshot of the JSON view selector.":::

## Example queries for hotels-sample index

The following examples assume the JSON view and the 2024-05-01-preview REST API version.

> [!TIP]
> The JSON view supports intellisense for parameter name completion. Place your cursor inside the JSON view and type a space character to see a list of all query parameters. You can also type a letter, like "s," to see only the query parameters that begin with that letter. Intellisense doesn't exclude invalid parameters, so use your best judgment.

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

Take a minute to try these example queries on your index. To learn more about queries, see [Querying in Azure AI Search](search-query-overview.md).

## Clean up resources

When you work in your own subscription, it's a good idea at the end of a project to identify whether you still need the resources you created. Resources left running can cost you money. You can delete resources individually or delete the resource group to delete the entire set of resources.

In the Azure portal, you can find and manage resources for your service under **All resources** or **Resource groups** in the left pane.

> [!NOTE]
> If you're using a free search service, remember that the limit is three indexes, three indexers, and three data sources. You can delete individual objects in the Azure portal to stay under the limit.

## Next step

Try an Azure portal wizard to generate a ready-to-use web app that runs in a browser. Use this wizard on the small index you created in this quickstart, or use one of the built-in sample datasets for a richer search experience.

> [!div class="nextstepaction"]
> [Quickstart: Create a demo search app in the Azure portal](search-create-app-portal.md)
