---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 09/16/2025
---

> [!IMPORTANT]
> The **Import data** wizard will eventually be deprecated. Most of its functionality is available in the **Import data (new)** wizard, which we recommend for most search scenarios. For more information, see [Import data wizards in the Azure portal](../../search-import-data-portal.md).

In this quickstart, you use the **Import data** wizard and a built-in sample of fictitious hotel data to create your first search index. The wizard requires no code to create an index, helping you write interesting queries within minutes.

The wizard creates multiple objects on your search service, including a searchable [index](../../search-what-is-an-index.md), an [indexer](../../search-indexer-overview.md), and a data source connection for automated data retrieval. At the end of this quickstart, you review each object.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. You can use a free service for this quickstart.

### Check for network access

For this quickstart, which uses built-in sample data, make sure your search service doesn't have [network access controls](../../service-configure-firewall.md). The Azure portal controller uses a public endpoint to retrieve data and metadata from the Microsoft-hosted data source. For more information, see [Secure connections in the import wizards](../../search-import-data-portal.md#secure-connections).

### Check for space

Many customers start with a free search service, which is limited to three indexes, three indexers, and three data sources. This quickstart creates one of each, so before you begin, make sure you have room for extra objects.

On the **Overview** page, select **Usage** to see how many indexes, indexers, and data sources you currently have.

   :::image type="content" source="../../media/search-get-started-portal/overview-quota-usage.png" alt-text="Screenshot of the Overview page for an Azure AI Search service instance in the Azure portal, showing the number of indexes, indexers, and data sources." lightbox="../../media/search-get-started-portal/overview-quota-usage.png":::

## Start the wizard

To start the wizard for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Import data**.

   :::image type="content" source="../../media/search-import-data-portal/import-data-button.png" alt-text="Screenshot that shows how to open the Import data wizard in the Azure portal.":::

## Create and load a search index

In this section, you create and load an index in four steps.

### Connect to a data source

The wizard creates a data source connection to sample data that Microsoft hosts on Azure Cosmos DB. The sample data is accessed through a public endpoint, so you don't need an Azure Cosmos DB account or source files for this step.

To connect to the sample data:

1. On the **Connect to your data** page, select the **Data Source** dropdown list, and then select **Samples**.

1. Select **hotels-sample** from the list of built-in samples.

1. Select **Next: Add cognitive skills (Optional)**.

   :::image type="content" source="../../media/search-get-started-portal/import-hotels-sample.png" alt-text="Screenshot that shows how to select the hotels-sample data source in the Import data wizard." lightbox="../../media/search-get-started-portal/import-hotels-sample.png":::

### Skip configuration for skills

The wizard supports skillset creation and [AI enrichment](../../cognitive-search-concept-intro.md) during indexing, which are beyond the scope of this quickstart. Skip this step by selecting **Next: Customize target index**.

> [!TIP]
> For a similar walkthrough that focuses on AI enrichment, see [Quickstart: Create a skillset in the Azure portal](../../search-get-started-skillset.md).

### Configure the index

Based on the structure and content of the sample hotel data, the wizard infers a schema for your search index.

To configure the index:

1. Accept the system-generated values for the index name (**hotels-sample-index**) and key (**HotelId**).

1. Accept the system-generated values for all field attributes.

1. Select **Next: Create an indexer**.

   :::image type="content" source="../../media/search-get-started-portal/hotels-sample-generated-index.png" alt-text="Screenshot that shows the generated index definition for the hotels-sample data source in the Import data wizard." lightbox="../../media/search-get-started-portal/hotels-sample-generated-index.png":::

At a minimum, the index requires a name and a collection of fields. The wizard scans for unique string fields and marks one as the document key, which uniquely identifies each document in the index.

Each field has a name, data type, and attributes that control how the field is used in the index. You can use the checkboxes to enable or disable the following attributes:

| Attribute | Description | Applicable data types |
|-----------|-------------|------------------------|
| Retrievable | Fields returned in a query response. | Strings and integers |
| Filterable | Fields that accept a filter expression. | Integers |
| Sortable | Fields that accept an orderby expression. | Integers |
| Facetable | Fields used in a faceted navigation structure. | Integers |
| Searchable | Fields used in full-text search. Strings are searchable, but numeric and Boolean fields are often marked as not searchable. | Strings |

Attributes affect storage in different ways. For example, filterable fields consume extra storage, while retrievable fields don't.

If you want autocomplete or suggested queries, specify language **Analyzers** or **Suggesters**.

### Configure and run the indexer

The last step is to configure and run the indexer, which automates the process of extracting content from your data source and loading it into your index. This step also creates the data source and index objects on your search service.

To configure and run the indexer:

1. Accept the system-generated value for the indexer name (**hotels-sample-indexer**).

1. Accept the default schedule option to run the indexer once and immediately. The sample data is static, so you can't enable change tracking.

1. Select **Submit** to simultaneously create and run the indexer.

   :::image type="content" source="../../media/search-get-started-portal/hotels-sample-indexer.png" alt-text="Screenshot that shows how to configure the indexer for the hotels-sample data source in the Import data wizard." lightbox="../../media/search-get-started-portal/hotels-sample-indexer.png":::
