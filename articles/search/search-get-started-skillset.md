---
title: "Quickstart: Create a Skillset in the Azure portal"
titleSuffix: Azure AI Search
description: Learn how to use an import wizard to generate searchable text from images and unstructured documents. Skills in this quickstart include optical character recognition (OCR), image analysis, and natural-language processing.
manager: nitinme
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
ms.topic: quickstart
ms.date: 12/11/2025
---

# Quickstart: Create a skillset in the Azure portal

> [!IMPORTANT]
> The **Import data (new)** wizard now supports keyword search, which was previously only available in the **Import data** wizard. We recommend the new wizard for an improved search experience. For more information about how we're consolidating the wizards, see [Import data wizards in the Azure portal](search-import-data-portal.md).

In this quickstart, you learn how a skillset in Azure AI Search adds optical character recognition (OCR), image analysis, language detection, text merging, and entity recognition to generate text-searchable content in an index.

You can run the **Import data (new)** wizard in the Azure portal to apply skills that create and transform textual content during indexing. The input is your raw data, usually blobs in Azure Storage. The output is a searchable index containing AI-generated image text, captions, and entities. You can then query generated content in the Azure portal using [**Search explorer**](search-explorer.md).

Before you run the wizard, you create a few resources and upload sample files.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An Azure AI Search service. [Create a service](search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. You can use a free service for this quickstart.

+ An [Azure Storage account](/azure/storage/common/storage-account-create). Use Azure Blob Storage on a standard performance (general-purpose v2) account. To avoid bandwidth charges, use the same region as Azure AI Search.

> [!NOTE]
> This quickstart uses [Foundry Tools](https://azure.microsoft.com/services/cognitive-services/) for AI enrichment. Because the workload is small, Foundry Tools is tapped behind the scenes for free processing up to 20 transactions. Therefore, you don't need to create a Microsoft Foundry resource.

## Prepare sample data

In this section, you create an Azure Storage container to store sample data consisting of various file types, including images and application files that aren't full-text searchable in their native formats.

To prepare the sample data for this quickstart:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your Azure Storage account.

1. From the left pane, select **Data storage** > **Containers**.

1. Create a container, and then upload the [sample data](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/ai-enrichment-mixed-media) to the container.

## Run the wizard

To run the wizard:

1. Sign in to the [Azure portal](https://portal.azure.com/) and select your search service.

1. On the **Overview** page, select **Import data (new)**.

   :::image type="content" source="media/search-import-data-portal/import-data-new-button.png" alt-text="Screenshot that shows how to open the new import wizard in the Azure portal.":::

1. Select **Azure Blob Storage** for the data source.

   :::image type="content" source="media/search-get-started-skillset/choose-data-source.png" alt-text="Screenshot of the Azure Blob Storage data source option in the Azure portal." border="true" lightbox="media/search-get-started-skillset/choose-data-source.png":::

1. Select **Keyword search**.

   :::image type="content" source="media/search-get-started-portal/keyword-search-tile.png" alt-text="Screenshot of the keyword search tile in the Azure portal." border="true" lightbox="media/search-get-started-portal/keyword-search-tile.png":::

### Step 1: Create a data source

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is your Azure Storage account.

To create the data source:

1. On the **Connect to your data** page, select your Azure subscription.

1. Select your storage account, and then select the container you created.

   :::image type="content" source="media/search-get-started-skillset/connect-to-your-data.png" alt-text="Screenshot of the Connect to your data page in the Azure portal." border="true" lightbox="media/search-get-started-skillset/connect-to-your-data.png":::

1. Select **Next**.

If you get `Error detecting index schema from data source`, the indexer that powers the wizard can't connect to your data source. The data source most likely has security protections. Try the following solutions, and then rerun the wizard.

| Security feature | Solution |
|--------------------|----------|
| Resource requires Azure roles, or its access keys are disabled. | [Connect as a trusted service](search-indexer-howto-access-trusted-service-exception.md) or [connect using a managed identity](search-how-to-managed-identities.md). |
| Resource is behind an IP firewall. | [Create an inbound rule for Azure AI Search and the Azure portal](search-indexer-howto-access-ip-restricted.md). |
| Resource requires a private endpoint connection. | [Connect over a private endpoint](search-indexer-howto-access-private.md). |

### Step 2: Add cognitive skills

The next step is to configure AI enrichment to invoke OCR, image analysis, and entity recognition.

OCR and image analysis are available for blobs in Azure Blob Storage and Azure Data Lake Storage (ADLS) Gen2 and for image content in Microsoft OneLake. Images can be standalone files or embedded images in a PDF or other files.

To add the skills:

1. Select **Extract entities**, and then select the gear icon.

1. Select and save the following checkboxes:

   + **Persons**

   + **Locations**

   + **Organizations**

   :::image type="content" source="media/search-get-started-skillset/extract-entities.png" alt-text="Screenshot of the Extract entities options in the Azure portal." lightbox="media/search-get-started-skillset/extract-entities.png":::

1. Select **Extract text from images**, and then select the gear icon.

1. Select and save the following checkboxes:

   + **Generate tags**

   + **Categorize content**

   :::image type="content" source="media/search-get-started-skillset/extract-text.png" alt-text="Screenshot of the Extract text from images options in the Azure portal." lightbox="media/search-get-started-skillset/extract-text.png":::

1. Leave the **Use a free AI service (limited enrichments)** checkbox selected.

   The sample data consists of 14 files, so the free allotment of 20 transactions on Foundry Tools is sufficient.

1. Select **Next**.

### Step 3: Configure the index

An index contains your searchable content. The wizard can usually create the schema by sampling the data source. In this step, you review the generated schema and potentially revise any settings.

For this quickstart, the wizard sets reasonable defaults:  

+ Default fields are based on metadata properties of existing blobs and new fields for the enrichment output, such as `persons`, `locations`, and `organizations`. Data types are inferred from metadata and by data sampling.

  :::image type="content" source="media/search-get-started-skillset/index-fields-new-wizard.png" alt-text="Screenshot of the index definition page." border="true" lightbox="media/search-get-started-skillset/index-fields-new-wizard.png":::

+ Default document key is `metadata_storage_path`, which is selected because the field contains unique values.

+ Default field attributes are based on the skills you selected. For example, fields created by the Entity Recognition skill (`persons`, `locations`, and `organizations`) are **Retrievable**, **Filterable**, **Facetable**, and **Searchable**. To view and change these attributes, select a field, and then select **Configure field**.

  **Retrievable** fields can be returned in results, while **Searchable** fields support full-text search. Use **Filterable** if you want to use fields in a filter expression.
  
  Marking a field as **Retrievable** doesn't mean that the field *must* appear in search results. You can control which fields are returned by using the `select` query parameter.

After you review the index schema, select **Next**.

### Step 4: Skip advanced settings

The wizard offers advanced settings for semantic ranking and index scheduling, which are beyond the scope of this quickstart. Skip this step by selecting **Next**.

### Step 5: Review and create objects

The last step is to review your configuration and create the index, indexer, and data source on your search service. The indexer automates the process of extracting content from your data source, loading the index, and driving skillset execution.

To review and create the objects:

1. Accept the default **Objects name prefix**.

1. Review the object configurations.

   :::image type="content" source="media/search-get-started-skillset/review-and-create.png" alt-text="Screenshot of the object configuration page in the Azure portal." border="true" lightbox="media/search-get-started-skillset/review-and-create.png":::

   AI enrichment, semantic ranker, and indexer scheduling are either disabled or set to their default values because you skipped their wizard steps.

1. Select **Create** to simultaneously create the objects and run the indexer.

## Monitor status

You can monitor the creation of the indexer in the Azure portal. Skills-based indexing takes longer than text-based indexing, especially OCR and image analysis.

To monitor the progress of the indexer:

1. From the left pane, select **Indexers**.

1. Select your indexer from the list.

1. Select **Success** (or **Failed**) to view execution details.

   :::image type="content" source="media/search-get-started-skillset/indexer-notification.png" alt-text="Screenshot of the indexer status page." border="true" lightbox="media/search-get-started-skillset/indexer-notification.png":::

  In this quickstart, there are a few warnings, including `Could not execute skill because one or more skill input was invalid.` This warning tells you that a PNG file in the data source doesn't provide a text input to Entity Recognition. It occurs because the upstream OCR skill didn't recognize any text in the image and couldn't provide a text input to the downstream Entity Recognition skill.

  Warnings are common in skillset execution. As you become familiar with how skills iterate over your data, you might begin to notice patterns and learn which warnings are safe to ignore.

## Query in Search explorer

To query your index:

1. From the left pane, select **Indexes**.

1. Select your index from the list. If the index has zero documents or storage, wait for the Azure portal to refresh.

1. On the **Search explorer** tab, enter a search string, such as `satya nadella`.

The search bar accepts keywords, quote-enclosed phrases, and operators. For example: `"Satya Nadella" +"Bill Gates" +"Steve Ballmer"`

Results are returned as verbose JSON, which can be hard to read, especially in large documents. Here are tips for searching in this tool:
    
   + Switch to the JSON view to specify parameters that shape results.
   + Add `select` to limit the fields in results.
   + Add `count` to show the number of matches.
   + Use Ctrl-F to search within the JSON for specific properties or terms.

:::image type="content" source="media/search-get-started-skillset/search-explorer-new-wizard.png" alt-text="Screenshot of the Search explorer page." border="true" lightbox="media/search-get-started-skillset/search-explorer-new-wizard.png":::

Here's some JSON you can paste into the view:
    
```json
{
"search": "\"Satya Nadella\" +\"Bill Gates\" +\"Steve Ballmer\"",
"count": true,
"select": "merged_content, persons"
}
```

> [!TIP]
> Query strings are case sensitive, so if you get an "unknown field" message, check **Fields** or **Index Definition (JSON)** to verify the name and case.

## Takeaways

You've created your first skillset and learned the basic steps of skills-based indexing.

Some key concepts that we hope you picked up include the dependencies. A skillset is bound to an indexer, and indexers are Azure and source-specific. Although this quickstart uses Azure Blob Storage, other Azure data sources are available. For more information, see [Indexers in Azure AI Search](search-indexer-overview.md). 

Another important concept is that skills operate over content types, and when you use heterogeneous content, some inputs are skipped. Also, large files or fields might exceed the indexer limits of your service tier. It's normal to see warnings when these events occur. 

The output is routed to a search index, and there's a mapping between name-value pairs created during indexing and individual fields in your index. Internally, the wizard sets up [an enrichment tree](cognitive-search-concept-annotations-syntax.md) and defines a [skillset](cognitive-search-defining-skillset.md), establishing the order of operations and general flow. These steps are hidden in the wizard, but when you start writing code, these concepts become important.

Finally, you learned that you can verify content by querying the index. Ultimately, Azure AI Search provides a searchable index that you can query using either [simple](/rest/api/searchservice/simple-query-syntax-in-azure-search) or [fully extended query syntax](/rest/api/searchservice/lucene-query-syntax-in-azure-search). An index containing enriched fields is like any other. You can incorporate standard or [custom analyzers](search-analyzers.md), [scoring profiles](/rest/api/searchservice/add-scoring-profiles-to-a-search-index), [synonyms](search-synonyms.md), [faceted navigation](search-faceted-navigation.md), geo-search, and other Azure AI Search features.

## Clean up resources

[!INCLUDE [clean up resources (free)](includes/resource-cleanup-free.md)]

## Next step

You can use the Azure portal, REST APIs, or an Azure SDK to create skillsets. Try the REST APIs by using a REST client and more sample data:

> [!div class="nextstepaction"]
> [Tutorial: Use skillsets to generate searchable content in Azure AI Search](tutorial-skillset.md)
