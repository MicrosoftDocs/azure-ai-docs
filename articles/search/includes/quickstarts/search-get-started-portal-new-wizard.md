---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 01/15/2026
---

> [!IMPORTANT]
> The **Import data (new)** wizard now supports keyword search, which was previously only available in the **Import data** wizard. We recommend the new wizard for an improved search experience. For more information about how we're consolidating the wizards, see [Import data wizards in the Azure portal](../../search-import-data-portal.md).

In this quickstart, you use the **Import data (new)** wizard and sample data about fictitious hotels to get started with [full-text search](../../search-lucene-query-architecture.md), also known as keyword search. The wizard requires no code to create an index, helping you write interesting queries within minutes.

The wizard creates multiple objects on your search service, including a searchable index, an indexer, and a data source connection for automated data retrieval. At the end of this quickstart, you review each object.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An [Azure AI Search service](../../search-create-service-portal.md). You can use the Free tier for this quickstart.

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage or Azure Data Lake Storage Gen2 (storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. To avoid bandwidth charges, use the same region as Azure AI Search.

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](../../search-import-data-portal.md).

### Check for network access

For this quickstart, all of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](../../search-import-data-portal.md#secure-connections).

### Check for space

Many customers start with a free search service, which is limited to three indexes, three indexers, and three data sources. This quickstart creates one of each, so before you begin, make sure you have room for extra objects.

On the **Overview** page, select **Usage** to see how many indexes, indexers, and data sources you currently have.

   :::image type="content" source="../../media/search-get-started-portal/overview-quota-usage.png" alt-text="Screenshot of the Overview page for an Azure AI Search service instance in the Azure portal, showing the number of indexes, indexers, and data sources." lightbox="../../media/search-get-started-portal/overview-quota-usage.png":::

## Prepare sample data

This quickstart uses a JSON document that contains metadata for 50 fictitious hotels, but you can also use your own files.

To prepare the sample data for this quickstart:

1. Download the `HotelsData_toAzureBlobs.json` file from the [azure-search-sample-data](https://github.com/Azure-Samples/azure-search-sample-data/blob/main/hotels/HotelsData_toAzureBlobs.json) repo.

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container named **hotels-sample**.

1. Upload the `HotelsData_toAzureBlobs.json` file to the container.

## Run the wizard

The wizard walks you through several configuration steps. This section covers each step in sequence.

### Start the wizard

To start the wizard for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Import data (new)**.

   :::image type="content" source="../../media/search-import-data-portal/import-data-new-button.png" alt-text="Screenshot that shows how to open the new import wizard in the Azure portal.":::

1. Select your data source: **Azure Blob Storage** or **Azure Data Lake Storage Gen2**.

   :::image type="content" source="../../media/search-get-started-portal-images/select-data-source.png" alt-text="Screenshot of the options for selecting a data source in the wizard." border="true" lightbox="../../media/search-get-started-portal-images/select-data-source.png":::

1. Select **Keyword search**.

   :::image type="content" source="../../media/search-get-started-portal/keyword-search-tile.png" alt-text="Screenshot of the keyword search tile in the Azure portal." border="true" lightbox="../../media/search-get-started-portal/keyword-search-tile.png":::

### Connect to a data source

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is your Azure Storage account.

To connect to the sample data:

1. On the **Connect to your data** page, select your Azure subscription.

1. Select your storage account, and then select the **hotels-sample** container.

1. Select **JSON array** for the parsing mode.

   :::image type="content" source="../../media/search-get-started-portal/connect-to-your-data.png" alt-text="Screenshot of the Connect to your data page in the Azure portal." lightbox="../../media/search-get-started-portal/connect-to-your-data.png":::

1. Select **Next**.

### Skip AI enrichment

The wizard supports skillset creation and [AI enrichment](../../cognitive-search-concept-intro.md) during indexing, which are beyond the scope of this quickstart. Skip this step by selecting **Next**.

> [!TIP]
> For a similar walkthrough that focuses on AI enrichment, see [Quickstart: Create a skillset in the Azure portal](../../search-get-started-skillset.md).

### Configure the index

Based on the structure and content of the sample hotel data, the wizard infers a schema for your search index.

To configure the index:

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

   :::image type="content" source="../../media/search-get-started-portal/configure-index.gif" alt-text="GIF that shows how to configure attributes for fields in the index." lightbox="../../media/search-get-started-portal/configure-index.gif":::

1. Select **Next**.

At a minimum, the index requires a name and a collection of fields. The wizard scans for unique string fields and marks one as the document key, which uniquely identifies each document in the index.

Each field has a name, [data type](/rest/api/searchservice/supported-data-types), and attributes that control how the field is used in the index. You can enable or disable the following attributes:

| Attribute | Description | Applicable data types |
|-----------|-------------|------------------------|
| Retrievable | Fields returned in a query response. | Strings and integers |
| Filterable | Fields that accept a filter expression. | Strings and integers |
| Sortable | Fields that accept an orderby expression. | Strings and integers |
| Facetable | Fields used in a faceted navigation structure. | Strings and integers |
| Searchable | Fields used in full-text search. Strings are searchable, but numeric and Boolean fields are often marked as not searchable. | Strings |

Attributes affect storage in different ways. For example, filterable fields consume extra storage, while retrievable fields don't. For more information about attributes and data types, see [Configure field definitions](/azure/search/search-how-to-create-search-index#configure-field-definitions).

If you want autocomplete or suggested queries, specify **Suggesters**.

### Skip advanced settings

The wizard offers advanced settings for semantic ranking and index scheduling, which are beyond the scope of this quickstart. Skip this step by selecting **Next**.

### Finish the wizard

The last step is to review your configuration and create the index, indexer, and data source on your search service. The indexer automates the process of extracting content from your data source and loading it into the index, enabling keyword search.

To finish the wizard:

1. Change the object name prefix to **hotels-sample**.

1. Review the object configurations.

   :::image type="content" source="../../media/search-get-started-portal/review-and-create.png" alt-text="Screenshot of the object configuration page in the Azure portal." lightbox="../../media/search-get-started-portal/review-and-create.png":::

   AI enrichment, semantic ranker, and indexer scheduling are either disabled or set to their default values because you skipped their wizard steps.

1. Select **Create** to simultaneously create the objects and run the indexer.
