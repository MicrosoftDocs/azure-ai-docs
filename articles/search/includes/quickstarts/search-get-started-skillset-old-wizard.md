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

In this quickstart, you learn how a skillset in Azure AI Search adds optical character recognition (OCR), image analysis, language detection, text merging, and entity recognition to generate text-searchable content in an index.

You can run the **Import data** wizard in the Azure portal to apply skills that create and transform textual content during indexing. The input is your raw data, usually blobs in Azure Storage. The output is a searchable index containing AI-generated image text, captions, and entities. You can then query generated content in the Azure portal using [**Search explorer**](../../search-explorer.md).

Before you run the wizard, you create a few resources and upload sample files.

## Prerequisites

+ An Azure account with an active subscription. [Create an account for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

+ An Azure AI Search service. [Create a service](../../search-create-service-portal.md) or [find an existing service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in your current subscription. You can use a free service for this quickstart.

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

1. On the **Overview** page, select **Import data**.

   :::image type="content" source="../../media/search-import-data-portal/import-data-button.png" alt-text="Screenshot of the Import data command." border="true":::

### Step 1: Create a data source

Azure AI Search requires a connection to a data source for content ingestion and indexing. In this case, the data source is your Azure Storage account.

To create the data source:

1. On the **Connect to your data** page, select the **Data Source** dropdown list, and then select **Azure Blob Storage**.

1. Choose an existing connection string for your storage account, and then select the container you created.

1. Enter a name for the data source.

   :::image type="content" source="../../media/search-get-started-skillset/blob-datasource.png" alt-text="Screenshot of the data source definition page." border="true" lightbox="../../media/search-get-started-skillset/blob-datasource.png":::

1. Select **Next: Add cognitive skills (Optional)**.

If you get `Error detecting index schema from data source`, the indexer that powers the wizard can't connect to your data source. The data source most likely has security protections. Try the following solutions, and then rerun the wizard.

| Security feature | Solution |
|--------------------|----------|
| Resource requires Azure roles, or its access keys are disabled. | [Connect as a trusted service](../../search-indexer-howto-access-trusted-service-exception.md) or [connect using a managed identity](../../search-how-to-managed-identities.md). |
| Resource is behind an IP firewall. | [Create an inbound rule for Azure AI Search and the Azure portal](../../search-indexer-howto-access-ip-restricted.md). |
| Resource requires a private endpoint connection. | [Connect over a private endpoint](../../search-indexer-howto-access-private.md). |

### Step 2: Add cognitive skills

The next step is to configure AI enrichment to invoke OCR, image analysis, and natural-language processing. 

OCR and image analysis are available for blobs in Azure Blob Storage and Azure Data Lake Storage (ADLS) Gen2 and for image content in Microsoft OneLake. Images can be standalone files or embedded images in a PDF or other files.

To add the skills:

1. Expand the **Attach Cognitive Services** section.

1. Select **Free (Limited enrichments)** to use a free Foundry resource.

   :::image type="content" source="../../media/search-get-started-skillset/cog-search-attach.png" alt-text="Screenshot of the Attach Foundry tab." border="true" lightbox="../../media/search-get-started-skillset/cog-search-attach.png":::

   The sample data consists of 14 files, so the free allotment of 20 transactions on Foundry is sufficient.

1. Expand the **Add enrichments** section.

1. Select the **Enable OCR and merge all text into merged_content field** checkbox.

1. Under **Text Cognitive Skills**, select the following checkboxes:

    + **Extract people names**
    
    + **Extract organization names**
    
    + **Extract location names**

1. Under **Image Cognitive Skills**, select the following checkboxes: 

    + **Generate tags from images**
    
    + **Generate captions from images**

   :::image type="content" source="../../media/search-get-started-skillset/skillset.png" alt-text="Screenshot of the skillset definition page." border="true" lightbox="../../media/search-get-started-skillset/skillset.png":::

1. Select **Next: Customer target index**.

### Step 3: Configure the index

An index contains your searchable content. The wizard can usually create the schema by sampling the data source. In this step, you review the generated schema and potentially revise any settings. 

For this quickstart, the wizard sets reasonable defaults:  

+ Default fields are based on metadata properties of existing blobs and new fields for the enrichment output, such as `people`, `organizations`, and `locations`. Data types are inferred from metadata and by data sampling.

+ Default document key is `metadata_storage_path`, which is selected because the field contains unique values.

+ Default attributes are **Retrievable** and **Searchable**. **Retrievable** fields can be returned in results, while **Searchable** fields support full-text search. The wizard assumes you want these fields to be retrievable and searchable because you created them via a skillset. Select **Filterable** if you want to use fields in a filter expression.

  :::image type="content" source="../../media/search-get-started-skillset/index-fields-old-wizard.png" alt-text="Screenshot of the index definition page." border="true" lightbox="../../media/search-get-started-skillset/index-fields-old-wizard.png":::

  Marking a field as **Retrievable** doesn't mean that the field *must* appear in search results. You can control which fields are returned by using the `select` query parameter.
      
After you review the index schema, select **Next: Create an indexer**.

### Step 4: Configure the indexer

The indexer drives the indexing process and specifies the data source name, a target index, and frequency of execution. In this step, the wizard creates several objects, including an indexer that you can reset and run repeatedly.

To configure the indexer:

1. On the **Create an indexer** page, accept the default name.

1. Select **Once** for the schedule.

   :::image type="content" source="../../media/search-get-started-skillset/indexer-def.png" alt-text="Screenshot of the indexer definition page." border="true" lightbox="../../media/search-get-started-skillset/indexer-def.png":::

1. Select **Submit** to simultaneously create and run the indexer.

## Monitor status

You can monitor the creation of the indexer in the Azure portal. Skills-based indexing takes longer than text-based indexing, especially OCR and image analysis.

To monitor the progress of the indexer:

1. From the left pane, select **Indexers**.

1. Select your indexer from the list.

1. Select **Success** (or **Failed**) to view execution details.

   :::image type="content" source="../../media/search-get-started-skillset/indexer-notification.png" alt-text="Screenshot of the indexer status page." border="true" lightbox="../../media/search-get-started-skillset/indexer-notification.png":::

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

:::image type="content" source="../../media/search-get-started-skillset/search-explorer-old-wizard.png" alt-text="Screenshot of the Search explorer page." border="true" lightbox="../../media/search-get-started-skillset/search-explorer-old-wizard.png":::

Here's some JSON you can paste into the view:
    
```json
{
"search": "\"Satya Nadella\" +\"Bill Gates\" +\"Steve Ballmer\"",
"count": true,
"select": "content, people"
}
```

> [!TIP]
> Query strings are case sensitive, so if you get an "unknown field" message, check **Fields** or **Index Definition (JSON)** to verify the name and case.