---
title: "Quickstart: Full-Text Search in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to create, load, and query your first search index using an import wizard in the Azure portal. This quickstart uses a fictitious hotel dataset for sample data.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 03/04/2026
ms.custom:
  - mode-ui
  - ignite-2023
  - ignite-2024
---

# Quickstart: Full-text search in the Azure portal

> [!IMPORTANT]
> The **Import data (new)** wizard now supports keyword search, which was previously only available in the **Import data** wizard. We recommend the new wizard for an improved search experience. For more information about how we're consolidating the wizards, see [Import data wizards in the Azure portal](search-import-data-portal.md).

In this quickstart, you use the **Import data (new)** wizard and sample data about fictitious hotels to get started with [full-text search](search-lucene-query-architecture.md), also known as keyword search. The wizard requires no code to create an index, helping you write interesting queries within minutes.

The wizard creates multiple objects on your search service, including a searchable index, an indexer, and a data source connection for automated data retrieval. At the end of this quickstart, you review each object.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](search-create-service-portal.md). This quickstart requires the Basic tier or higher for managed identity support.

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage or Azure Data Lake Storage Gen2 (storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. To avoid bandwidth charges, use the same region as Azure AI Search.

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](search-import-data-portal.md).

### Check for network access

For this quickstart, all of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](search-import-data-portal.md#secure-connections).

### Check for space

Many customers start with a free search service, which is limited to three indexes, three indexers, and three data sources. This quickstart creates one of each, so before you begin, make sure you have room for extra objects.

On the **Overview** page, select **Usage** to see how many indexes, indexers, and data sources you currently have.

   :::image type="content" source="media/search-get-started-portal/overview-quota-usage.png" alt-text="Screenshot of the Overview page for an Azure AI Search service instance in the Azure portal, showing the number of indexes, indexers, and data sources." lightbox="media/search-get-started-portal/overview-quota-usage.png":::

## Configure access

Before you begin, make sure you have permissions to access content and operations. This quickstart uses Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](search-security-api-keys.md) instead.

To configure access for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com).

1. On your Azure AI Search service:

    1. [Enable role-based access](search-security-enable-roles.md).

    1. [Create a system-assigned managed identity](search-how-to-managed-identities.md#create-a-system-managed-identity).

    1. [Assign the following roles](search-security-rbac.md) to your user account: **Search Service Contributor**, **Search Index Data Contributor**, and **Search Index Data Reader**.

1. On your Azure Storage account, assign **Storage Blob Data Reader** to the managed identity of your search service.

## Prepare sample data

This quickstart uses a sample JSON document that contains metadata for 50 fictitious hotels, but you can also use your own files.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container named **hotels-sample-data**.

1. Upload the [sample JSON document](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/hotels/HotelsData_toAzureBlobs.json) to the container.

## Start the wizard

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Import data (new)**.

   :::image type="content" source="media/search-import-data-portal/import-data-new-button.png" alt-text="Screenshot that shows how to open the new import wizard in the Azure portal.":::

1. Select your data source: **Azure Blob Storage** or **Azure Data Lake Storage Gen2**.

   :::image type="content" source="media/search-get-started-portal-images/select-data-source.png" alt-text="Screenshot of the options for selecting a data source in the wizard." border="true" lightbox="media/search-get-started-portal-images/select-data-source.png":::

1. Select **Keyword search**.

   :::image type="content" source="media/search-get-started-portal/keyword-search-tile.png" alt-text="Screenshot of the keyword search tile in the Azure portal." border="true" lightbox="media/search-get-started-portal/keyword-search-tile.png":::

## Run the wizard

The wizard walks you through several configuration steps. This section covers each step in sequence.

### Connect to a data source

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is your Azure Storage account.

To connect to the sample data:

1. On the **Connect to your data** page, select your Azure subscription.

1. Select your storage account, and then select the **hotels-sample-data** container.

1. Select **JSON array** for the parsing mode.

1. Select the **Authenticate using managed identity** checkbox. Leave the identity type as **System-assigned**.

   :::image type="content" source="media/search-get-started-portal/connect-to-your-data.png" alt-text="Screenshot of the Connect to your data page in the Azure portal." lightbox="media/search-get-started-portal/connect-to-your-data.png":::

1. Select **Next**.

### Skip AI enrichment

The wizard supports skillset creation and [AI enrichment](cognitive-search-concept-intro.md) during indexing, which are beyond the scope of this quickstart. Skip this step by selecting **Next**.

> [!TIP]
> For a similar walkthrough that focuses on AI enrichment, see [Quickstart: Create a skillset in the Azure portal](search-get-started-skillset.md).

### Configure the index

The wizard infers a schema for your search index based on the sample data. At a minimum, the index requires a name and a collection of fields. The wizard scans for unique string fields and marks one as the document key, which uniquely identifies each document in the index.

Each field has a name, [data type](/rest/api/searchservice/supported-data-types), and attributes that control how it's used. For example, **Filterable** fields support filter expressions in queries, while **Searchable** fields support keyword search. For more information, see [Configure field definitions](/azure/search/search-how-to-create-search-index#configure-field-definitions).

To configure the index for the query examples in this quickstart:

1. For each of the following fields, select **Configure field**, and then set the respective attributes.

   | Fields | Attributes |
   |-------|------------|
   | `HotelId` | Key, Retrievable, Filterable, Sortable, Searchable |
   | `HotelName`, `Category` | Retrievable, Filterable, Sortable, Searchable |
   | `Description`, `Description_fr` | Retrievable, Searchable |
   | `Tags` | Retrievable, Filterable, Searchable |
   | `ParkingIncluded`, `IsDeleted` | Retrievable, Filterable, Facetable |
   | `LastRenovationDate`, `Rating`, `Location` | Retrievable, Filterable, Sortable |
   | `Address.StreetAddress`, `Rooms.Description`, `Rooms.Description_fr` | Retrievable, Searchable |
   | `Address.City`, `Address.StateProvince`, `Address.PostalCode`, `Address.Country` | Retrievable, Filterable, Facetable, Searchable, Sortable|
   | `Rooms.Type`, `Rooms.BedOptions`, `Rooms.Tags` | Retrievable, Filterable, Facetable, Searchable |
   | `Rooms.BaseRate`, `Rooms.SleepsCount`, `Rooms.SmokingAllowed` | Retrievable, Filterable, Facetable |

   :::image type="content" source="media/search-get-started-portal/configure-index.gif" alt-text="GIF that shows how to configure attributes for fields in the index." lightbox="media/search-get-started-portal/configure-index.gif":::

1. Select **Next**.

### Skip advanced settings

The wizard offers advanced settings for semantic ranking and index scheduling, which are beyond the scope of this quickstart. Skip this step by selecting **Next**.

## Finish the wizard

The final step is to review your configuration and create the index, indexer, and data source on your search service. The indexer automates the process of extracting content from your data source and loading it into the index, enabling keyword search.

To finish the wizard:

1. Change the object name prefix to **hotels-sample**.

1. Review the object configurations.

   :::image type="content" source="media/search-get-started-portal/review-and-create.png" alt-text="Screenshot of the object configuration page in the Azure portal." lightbox="media/search-get-started-portal/review-and-create.png":::

   AI enrichment, semantic ranker, and indexer scheduling are either disabled or set to their default values because you skipped their wizard steps.

1. Select **Create** to simultaneously create the objects and run the indexer.

## Check indexer status

1. From the left pane, select **Search management** > **Indexers**.

1. Find **hotels-sample-indexer** in the list.

   :::image type="content" source="media/search-get-started-portal/indexers-status.png" alt-text="Screenshot that shows the creation of the indexer in progress in the Azure portal." lightbox="media/search-get-started-portal/indexers-status.png":::

   It can take a few minutes for the results to update. You should see the newly created indexer with a status of **In progress** or **Success**. The list also shows the number of documents indexed.

## Check index results

1. From the left pane, select **Search management** > **Indexes**.

1. Select **hotels-sample**. If the index has zero documents or storage, wait for the Azure portal to refresh.

   :::image type="content" source="media/search-get-started-portal/indexes-list.png" alt-text="Screenshot of the Indexes list on the Azure AI Search service dashboard in the Azure portal." lightbox="media/search-get-started-portal/indexes-list.png":::

1. Select the **Fields** tab to view the index schema.

   :::image type="content" source="media/search-get-started-portal/index-schema-definition.png" alt-text="Screenshot that shows the schema definition for an index in the Azure AI Search service in the Azure portal." lightbox="media/search-get-started-portal/index-schema-definition.png":::

### Add or change index fields

On the **Fields** tab, you can create a field by selecting **Add field** and specifying a name, supported data type, and attributes.

Changing existing fields is more difficult. Existing fields have a physical representation in the search index, so they aren't modifiable, not even in code. To fundamentally change an existing field, you must create a new field to replace the original. You can add other constructs, such as scoring profiles and a semantic configuration, to an index at any time.

Review the index definition options to understand what you can and can't edit during index design. If an option appears dimmed, you can't modify or delete it.

## Query the index

You now have a search index that can be queried using [**Search explorer**](search-explorer.md), which sends REST calls that conform to [Documents - Search Post (REST API)](/rest/api/searchservice/documents/search-post?view=rest-searchservice-2025-11-01-preview&preserve-view=true). This tool supports [simple query syntax](/rest/api/searchservice/simple-query-syntax-in-azure-search) and [full Lucene query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search) for keyword search.

To query your search index:

1. On the **Search explorer** tab, enter a query term or string, such as `new york hotel with pool or gym`.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-string.png" alt-text="Screenshot that shows how to enter and run a query in the  Search Explorer tool." lightbox="media/search-get-started-portal/search-explorer-query-string.png":::

1. To jump to nonvisible areas of the output, use the mini map.

   :::image type="content" source="media/search-get-started-portal/search-explorer-query-results.png" alt-text="Screenshot that shows long results for a query in the Search Explorer tool and the mini-map." lightbox="media/search-get-started-portal/search-explorer-query-results.png":::

1. To specify syntax, switch to the JSON view.

   :::image type="content" source="media/search-get-started-portal/search-explorer-change-view.png" alt-text="Screenshot of the JSON view selector." lightbox="media/search-get-started-portal/search-explorer-change-view.png":::

1. Run the following query examples to see how filtering and query syntax work.

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

For more information about these examples, see [Querying in Azure AI Search](search-query-overview.md).

## Clean up resources

[!INCLUDE [clean up resources (free)](includes/resource-cleanup-free.md)]

## Next step

Try an Azure portal wizard to generate a ready-to-use web app that runs in a browser. Use this wizard on the small index you created in this quickstart, or use [sample data](https://github.com/Azure-Samples/azure-search-sample-data) for a richer search experience.

> [!div class="nextstepaction"]
> [Quickstart: Create a demo search app in the Azure portal](search-create-app-portal.md)
