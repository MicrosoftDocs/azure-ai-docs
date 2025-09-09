---
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: include
ms.date: 09/09/2025
---

> [!IMPORTANT]
> The **Import and vectorize data** wizard now supports keyword search, which was previously limited to the **Import data** wizard. We recommend the new wizard for an improved search experience. For more information, see [Import data wizards in the Azure portal](../../search-import-data-portal.md).

In this quickstart, you use the **Import and vectorize data** wizard and sample data about ficticious hotels to create your first search index. The wizard requires no code to create an index, helping you write interesting queries within minutes.

The wizard creates multiple objects on your search service, including a searchable [index](../../search-what-is-an-index.md), an [indexer](../../search-indexer-overview.md), and a data source connection for automated data retrieval. At the end of this quickstart, you review each object.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/free/).

+ An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. You can use a free service for this quickstart.

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage or Azure Data Lake Storage Gen2 (storage account with a hierarchical namespace) on a standard performance (general-purpose v2) account. Access tiers can be hot, cool, or cold.

+ Familiarity with the wizard. See [Import data wizards in the Azure portal](../../search-import-data-portal.md).

### Check for network access

For this quickstart, all of the preceding resources must have public access enabled so that the Azure portal nodes can access them. Otherwise, the wizard fails. After the wizard runs, you can enable firewalls and private endpoints on the integration components for security. For more information, see [Secure connections in the import wizards](../../search-import-data-portal.md#secure-connections).

### Check for space

Many customers start with a free search service, which is limited to three indexes, three indexers, and three data sources. This quickstart creates one of each, so before you begin, make sure you have room for extra objects.

On the **Overview** page, select **Usage** to see how many indexes, indexers, and data sources you currently have.

   :::image type="content" source="../../media/search-get-started-portal/overview-quota-usage.png" alt-text="Screenshot of the Overview page for an Azure AI Search service instance in the Azure portal, showing the number of indexes, indexers, and data sources." lightbox="../../media/search-get-started-portal/overview-quota-usage.png":::

## Prepare sample data

This quickstart uses five JSON documents about ficticious hotels, but you can also use your own files.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container named **hotels-sample**.

1. Upload the [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/hotels/hotel-json-documents) to the container.

## Start the wizard

To start the wizard for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Import and vectorize data**.

   :::image type="content" source="../../media/search-import-data-portal/import-vectorize-data-cmd.png" alt-text="Screenshot that shows how to open the Import and vectorize data wizard in the Azure portal." lightbox="../../media/search-import-data-portal/import-vectorize-data-cmd.png":::

1. Select your data source: **Azure Blob Storage** or **Azure Data Lake Storage Gen2**.

   :::image type="content" source="../../media/search-get-started-portal-images/select-data-source.png" alt-text="Screenshot of the options for selecting a data source in the wizard." border="true" lightbox="../../media/search-get-started-portal-images/select-data-source.png":::

1. Select **Keyword search**.

## Create and load a search index

In this section, you create and load an index in five steps:

1. [Connect to a data source](#connect-to-a-data-source)
1. [Skip configuration for skills](#skip-configuration-for-skills)
1. [Preview index mappings](#preview-index-mappings)
1. [Skip advanced settings](#skip-advanced-settings)
1. [Review and create objects](#review-and-create-objects)

### Connect to a data source

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is sample hotel data in your Azure Storage account.

To connect to the sample data:

1. On the **Connect to your data** page, select your Azure subscription.

1. Select your storage account, and then select the **hotels-sample** container.

1. Select **Next** to continue.

### Skip configuration for skills

Although the wizard supports skillset creation and [AI enrichment](../../cognitive-search-concept-intro.md) during indexing, skills are beyond the scope of this quickstart.

To skip this wizard step:

1. On the **Apply AI enrichments** page, ignore the configuration options.

1. Select **Next** to continue.

> [!TIP]
> For a similar walkthrough that focuses on AI enrichment, see [Quickstart: Create a skillset in the Azure portal](../../search-get-started-skillset.md).

### Preview index mappings

Based on the structure and content of the sample hotel data, the wizard infers a schema for your search index.

To preview the index mappings:

1. Review the system-generated index fields (**content**, **title**, and **id**).

1. Select **Next** to continue.

At a minimum, the index requires a name and a collection of fields. The wizard scans for unique string fields and marks one as the document key, which uniquely identifies each document in the index.

Each field has a name, a data type, and attributes that control how the field is used in the index. You can select **Configure field** to enable or disable the following attributes:

| Attribute | Description | Applicable data types |
|-----------|-------------|------------------------|
| Retrievable | Fields returned in a query response. | Strings and integers |
| Filterable | Fields that accept a filter expression. | Integers |
| Sortable | Fields that accept an orderby expression. | Integers |
| Facetable | Fields used in a faceted navigation structure. | Integers |
| Searchable | Fields used in full-text search. Strings are searchable, but numeric and Boolean fields are often marked as not searchable. | Strings |

Attributes affect storage in different ways. For example, filterable fields consume extra storage, while retrievable fields don't. For more information, see [Example demonstrating the storage implications of attributes and suggesters](../../search-what-is-an-index.md#example-demonstrating-the-storage-implications-of-attributes-and-suggesters).

If you want autocomplete or suggested queries, specify language **Analyzers** or **Suggesters**.

### Skip advanced settings

The wizard offers advanced settings for semantic ranking and index scheduling, which are beyond the scope of this quickstart. Semantic ranking is enabled by default, so you must disable it.

To skip this wizard step:

1. On the **Advanced settings** page, deselect the **Enable semantic ranker** checkbox.

1. Leave the indexing schedule as **Once**.

1. Select **Next** to continue.

### Review and create objects

The last step is to review your configuration and create the index, indexer, and data source on your search service. The indexer automates the process of extracting content from your data source and loading it into the index, enabling keyword search.

To review and create the objects:

1. Change the object name prefix to **hotels-sample**.

1. Select **Create** to simultaneously create the objects and run the indexer.
