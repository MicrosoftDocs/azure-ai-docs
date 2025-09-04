---
title: Import Wizards in the Azure Portal
titleSuffix: Azure AI Search
description: Learn about the import wizards in the Azure portal used to create and load an index, and optionally invoke applied AI for vectorization, natural language processing, language translation, OCR, and image analysis.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 09/04/2025
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - ignite-2024
  - build-2025
  - sfi-image-nochange
---

# Import data wizards in the Azure portal

> [!IMPORTANT]
> The **Import and vectorize data** wizard now supports keyword search, which was previously exclusive to the **Import data** wizard. Both wizards are currently available in the Azure portal, but we recommend the **Import and vectorize data** wizard for an improved search experience.
>
> The **Import and vectorize data** wizard isn't a direct replacement for the **Import data** wizard. Certain skills and functionality are only available in the classic wizard. For more information about their similarities and differences, continue reading this article.

Azure AI Search provides two wizards that automate indexing, enrichment, and object creation for various search scenarios:

+ The **Import data** wizard supports keyword (nonvector) search. You can extract text and numbers from raw documents. You can also configure applied AI and built-in skills to infer structure and generate searchable text from image files and unstructured data.

+ The **Import and vectorize data** wizard supports keyword search, RAG, and multimodal RAG. For keyword search, it modernizes the **Import data** experience but lacks some functionality, such as automatic metadata field creation. For RAG and multimodal RAG, it connects to your embedding model deployment, sends requests, and generates vectors from text or images.

This article explains how the wizards work to help you with proof-of-concept testing. For step-by-step instructions using sample data, see [Try the wizards](#try-the-wizards).

## Supported data sources and scenarios

This section describes the available options in each wizard, including supported data sources and skills.

### Data sources

The wizards support the following data sources, most of which use [built-in indexers](search-indexer-overview.md#supported-data-sources). Exceptions are noted in the table's footnotes.

| Data source | Import data wizard | Import and vectorize data wizard |
|------|--------------------|----------------------------------|
| [ADLS Gen2](search-howto-index-azure-data-lake-storage.md) | ✅ | ✅ |
| [Azure Blob Storage](search-howto-indexing-azure-blob-storage.md) | ✅ | ✅ |
| [Azure File Storage](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1, 2</sup> |
| [Azure Queues](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [Azure Table Storage](search-howto-indexing-azure-tables.md) | ✅ | ✅ |
| [Azure SQL Database and Managed Instance](search-how-to-index-sql-database.md) | ✅ | ✅ |
| [Cosmos DB for NoSQL](search-howto-index-cosmosdb.md) | ✅ | ✅ |
| [Cosmos DB for MongoDB](search-howto-index-cosmosdb-mongodb.md) | ✅ | ✅ |
| [Cosmos DB for Apache Gremlin](search-howto-index-cosmosdb-gremlin.md) | ✅ | ✅ |
| [MySQL](search-howto-index-mysql.md)  | ❌ | ❌ |
| [OneDrive](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [OneDrive for Business](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [OneLake](search-how-to-index-onelake-files.md) | ✅ | ✅ |
| [Service Bus](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [SharePoint Online](search-how-to-index-logic-apps-indexers.md#supported-connectors) | ❌ | ✅ <sup>1, 2</sup> |
| [SQL Server on virtual machines](search-how-to-index-sql-server.md) | ✅ | ✅ |

<sup>1</sup> This data source uses an [Azure Logic Apps connectors (preview)](search-how-to-index-logic-apps-indexers.md#supported-connectors) instead of a built-in indexer.

<sup>2</sup> Instead of using a connector, you can use the Search Service REST APIs to programmatically index data from [Azure File Storage](search-file-storage-integration.md) or [SharePoint Online](search-howto-index-sharepoint-online.md).

### Sample data

The wizards support the following Microsoft-hosted sample data, which bypasses the data source configuration step.

| Sample data | Import data wizard | Import and vectorize data wizard |
|-------------|--------------------|----------------------------------|
| Hotels      | ✅                 | ❌                              |
| Real estate | ✅                 | ❌                              |

### Skills

Each wizard generates a skillset and outputs field mappings based on options you select. After the skillset is created, you can modify its JSON definition to add or remove skills.

The following skills might appear in a wizard-generated skillset.

| Skill | Import data wizard | Import and vectorize data wizard |
|------|--------------------|----------------------------------|
| [Azure AI Vision multimodal](cognitive-search-skill-vision-vectorize.md)  | ❌ | ✅ <sup>1</sup> |
| [Azure OpenAI embedding](cognitive-search-skill-azure-openai-embedding.md)  | ❌ | ✅ <sup>1</sup> |
| [Azure Machine Learning (Azure AI Foundry model catalog)](cognitive-search-aml-skill.md)  | ❌ | ✅ <sup>1</sup> |
| [Document layout](cognitive-search-skill-document-intelligence-layout.md)  | ❌ | ✅ <sup>1</sup> |
| [Entity recognition](cognitive-search-skill-entity-recognition-v3.md)  | ✅ | ✅ |
| [Image analysis](cognitive-search-skill-image-analysis.md) <sup>2</sup> | ✅ | ❌ |
| [Keyword extraction](cognitive-search-skill-keyphrases.md)  | ✅ | ❌ |
| [Language detection](cognitive-search-skill-language-detection.md)  | ✅ | ❌ |
| [Text translation](cognitive-search-skill-text-translation.md)  | ✅ | ❌ |
| [OCR](cognitive-search-skill-ocr.md) <sup>2</sup> | ✅ | ✅ |
| [PII detection](cognitive-search-skill-pii-detection.md)  | ✅ | ❌ |
| [Sentiment analysis](cognitive-search-skill-sentiment.md)  | ✅ | ❌ |
| [Shaper](cognitive-search-skill-shaper.md) <sup>3</sup> | ✅ | ❌ |
| [Text Split](cognitive-search-skill-textsplit.md) <sup>4</sup> | ✅ | ✅ |
| [Text Merge](cognitive-search-skill-textmerger.md) <sup>4</sup> | ✅ | ✅ |

<sup>1</sup> This skill is available for RAG and multimodal RAG workflows only. Keyword search isn't supported.

<sup>2</sup> This skill is available for Azure Storage blobs and OneLake files, assuming the default parsing mode. Images can be an image content type (such as PNG or JPG) or an embedded image in an application file (such as PDF).

<sup>3</sup> This skill is added when you configure a knowledge store.

<sup>4</sup> This skill is added for data chunking when you choose an embedding model. For nonembedding skills, it's added when you set the source field granularity to pages or sentences.

### Knowledge store

You can [generate a knowledge store](knowledge-store-create-portal.md) for secondary storage of enriched (skills-generated) content. A knowledge store is useful for information retrieval workflows that don't require a search engine.

| Knowledge store | Import data wizard | Import and vectorize data wizard |
|-----------------|--------------------|----------------------------------|
| Storage | ✅ | ❌ |

## What the wizards create

The following table lists the objects created by the wizards. After the objects are created, you can review their JSON definitions in the Azure portal or call them from code.

| Object | Description |
|--------|-------------|
| [Indexer](/rest/api/searchservice/indexers/create) | Configuration object that specifies a data source, target index, optional skillset, optional schedule, and optional configuration settings for error handling and base-64 encoding. |
| [Data source](/rest/api/searchservice/data-sources/create)  | Persists connection information to a [supported data source](search-indexer-overview.md#supported-data-sources) on Azure. A data source object is used exclusively with indexers. |
| [Index](/rest/api/searchservice/indexes/create) | Physical data structure for full-text search, vector search, and other queries. |
| [Skillset](/rest/api/searchservice/skillsets/create) | (Optional) Complete set of instructions for manipulating, transforming, and shaping content, including analyzing and extracting information from image files. Skillsets are also used for integrated vectorization. If the volume of work exceeds 20 transactions per indexer per day, the skillset must include a reference to an Azure AI services multi-service resource that provides enrichment. For integrated vectorization, you can use either Azure AI Vision or an embedding model in the Azure AI Foundry model catalog. |
| [Knowledge store](knowledge-store-concept-intro.md) | (Optional) Stores enriched skillset output from in tables and blobs in Azure Storage for independent analysis or downstream processing in nonsearch scenarios. Available only in the **Import data** wizard. |

To view these objects after the wizard runs:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.
1. From the left pane, select **Search management** to find pages for indexes, indexers, data sources, and skillsets.

## Benefits

Before writing any code, you can use the wizards for prototyping and proof-of-concept testing. The wizards connect to external data sources, sample the data to create an initial index, and then import and optionally vectorize the data as JSON documents into an index on Azure AI Search. 

If you're evaluating skillsets, the wizard handles output field mappings and adds helper functions to create usable objects. Text split is added if you specify a parsing mode. Text merge is added if you chose image analysis so that the wizard can reunite text descriptions with image content. Shaper skills are added to support valid projections if you chose the knowledge store option. All of the above tasks come with a learning curve. If you're new to enrichment, the ability to have these steps handled for you allows you to measure the value of a skill without having to invest much time and effort.

Sampling is the process by which an index schema is inferred, and it has some limitations. When the data source is created, the wizard picks a random sample of documents to decide what columns are part of the data source. Not all files are read, as this could potentially take hours for very large data sources. Given a selection of documents, source metadata, such as field name or type, is used to create a fields collection in an index schema. Depending on the complexity of source data, you might need to edit the initial schema for accuracy, or extend it for completeness. You can make your changes inline on the index definition page.

Overall, the advantages of using the wizard are clear: as long as requirements are met, you can create a queryable index within minutes. Some of the complexities of indexing, such as serializing data as JSON documents, are handled by the wizards.

## Limitations

The import wizards aren't without limitations. Constraints are summarized as follows:

+ The wizards don't support iteration or reuse. Each pass through the wizard creates a new index, skillset, and indexer configuration. Only data sources can be persisted and reused within the wizard. To edit or refine other objects, either delete the objects and start over, or use the REST APIs or .NET SDK to modify the structures.

+ Source content must reside in a [supported data source](search-indexer-overview.md#supported-data-sources).

+ Sampling is over a subset of source data. For large data sources, it's possible for the wizard to miss fields. You might need to extend the schema, or correct the inferred data types, if sampling is insufficient.

+ AI enrichment, as exposed in the Azure portal, is limited to a subset of built-in skills. 

+ A [knowledge store](knowledge-store-concept-intro.md), which can be created by the **Import data** wizard, is limited to a few default projections and uses a default naming convention. If you want to customize names or projections, you'll need to create the knowledge store through REST API or the SDKs.

## Secure connections

The import wizards make outbound connections using the Azure portal controller and public endpoints. You can't use the wizards if Azure resources are accessed over a private connection or through a shared private link.

You can use the wizards over restricted public connections, but not all functionality is available.

+ On a search service, importing the built-in sample data requires a public endpoint and no firewall rules.

  Sample data is hosted by Microsoft on specific Azure resources. The Azure portal controller connects to those resources over a public endpoint. If you put your search service behind a firewall, you get this error when attempting to retrieve the builtin sample data: `Import configuration failed, error creating Data Source`, followed by `"An error has occured."`.

+ On supported Azure data sources protected by firewalls, you can retrieve data if you have the right firewall rules in place.

  The Azure resource must admit network requests from the IP address of the device used on the connection. You should also list Azure AI Search as a trusted service on the resource's network configuration. For example, in Azure Storage, you can list `Microsoft.Search/searchServices` as a trusted service.

+ On connections to an Azure AI services multi-service account that you provide, or on connections to embedding models deployed in [Azure AI Foundry portal](https://ai.azure.com/?cid=learnDocs) or Azure OpenAI, public internet access must be enabled unless your search service meets the creation date, tier, and region requirements for private connections. For more information about these requirements, see [Make outbound connections through a shared private link](search-indexer-howto-access-private.md).

  Connections to Azure AI services multi-service are for [billing purposes](cognitive-search-attach-cognitive-services.md). Billing occurs when API calls exceed the free transaction count (20 per indexer run) for built-in skills called by the **Import data** wizard or integrated vectorization in the **Import and vectorize data wizard**.

  If Azure AI Search can't connect:

  + In the **Import and vectorize data wizard**, the error is `"Access denied due to Virtual Network/Firewall rules."`

  + In the **Import data** wizard, there's no error, but the skillset won't be created.

If firewall settings prevent your wizard workflows from succeeding, consider scripted or programmatic approaches instead.

## Workflow

Both wizards follow a similar high-level workflow:

1. Connect to a supported Azure data source.

1. Create an index schema, inferred by sampling source data.

1. (Optional) Add skills to extract or generate content and structure.

1. Run the wizard to create objects, optionally vectorize data, load data into an index, set a schedule, and configure other options.

The workflow is a pipeline, so it's one way. You can't use the wizard to edit any of the objects that were created, but you can use other portal tools, such as the index or indexer designer or the JSON editors, for allowed updates.

### Starting the wizards

Here's how you start the wizards.

1. In the [Azure portal](https://portal.azure.com), open the search service page from the dashboard or [find your service](https://portal.azure.com/#blade/HubsExtension/BrowseResourceBlade/resourceType/Microsoft.Search%2FsearchServices) in the service list.

1. On the **Overview** page, select **Import data** or **Import and vectorize data wizard**.

    :::image type="content" source="media/search-import-data-portal/import-data-cmd.png" alt-text="Screenshot of the import wizard options." border="true":::

    The wizards open fully expanded in the browser window so that you have more room to work.

1. If you selected **Import data**, you can select the **Samples** option to index a Microsoft-hosted dataset from a supported data source.

    :::image type="content" source="media/search-what-is-an-index/add-index-import-samples.png" alt-text="Screenshot of the import data page with the samples option selected." border="true":::

1. Follow the remaining steps in the wizard to create the index and indexer.

You can also launch **Import data** from other Azure services, including Azure Cosmos DB, Azure SQL Database, SQL Managed Instance, and Azure Blob Storage. Look for **Add Azure AI Search** in the left-navigation pane on the service overview page.

<a name="data-source-inputs"></a>

### Data source configuration in the wizard

The wizards connect to an external [supported data source](search-indexer-overview.md#supported-data-sources) using the internal logic provided by Azure AI Search indexers, which are equipped to sample the source, read metadata, crack documents to read content and structure, and serialize contents as JSON for subsequent import to Azure AI Search.

You can paste in a connection to a supported data source in a different subscription or region, but the **Choose an existing connection** picker is scoped to the active subscription.

:::image type="content" source="media/search-import-data-portal/choose-connection-same-subscription.png" alt-text="Screenshot of the Connect to your data tab." border="true":::

Not all preview data sources are guaranteed to be available in the wizard. Because each data source has the potential for introducing other changes downstream, a preview data source will only be added to the data sources list if it fully supports all of the experiences in the wizard, such as skillset definition and index schema inference.

You can only import from a single table, database view, or equivalent data structure, however the structure can include hierarchical or nested substructures. For more information, see [How to model complex types](search-howto-complex-data-types.md).

### Skillset configuration in the wizard

Skillset configuration occurs after the data source definition because the type of data source informs the availability of certain built-in skills. In particular, if you're indexing files from Blob storage, your choice of parsing mode of those files determine whether sentiment analysis is available.

The wizard adds the skills you choose. It also adds other skills that are necessary for achieving a successful outcome. For example, if you specify a knowledge store, the wizard adds a Shaper skill to support projections (or physical data structures).

Skillsets are optional and there's a button at the bottom of the page to skip ahead if you don't want AI enrichment.

<a name="index-definition"></a>

### Index schema configuration in the wizard

The wizards sample your data source to detect the fields and field type. Depending on the data source, it might also offer fields for indexing metadata.

Because sampling is an imprecise exercise, review the index for the following considerations:

1. Is the field list accurate? If your data source contains fields that weren't picked up in sampling, you can manually add any new fields that sampling missed, and remove any that don't add value to a search experience or that won't be used in a [filter expression](search-query-odata-filter.md) or [scoring profile](index-add-scoring-profiles.md).

1. Is the data type appropriate for the incoming data? Azure AI Search supports the [entity data model (EDM) data types](/rest/api/searchservice/supported-data-types). For Azure SQL data, there's [mapping chart](search-how-to-index-sql-database.md#TypeMapping) that lays out equivalent values. For more background, see [Field mappings and transformations](search-indexer-field-mappings.md).

1. Do you have one field that can serve as the *key*? This field must be Edm.string and it must uniquely identify a document. For relational data, it might be mapped to a primary key. For blobs, it might be the `metadata-storage-path`. If field values include spaces or dashes, you must set the **Base-64 Encode Key** option in the **Create an Indexer** step, under **Advanced options**, to suppress the validation check for these characters.

1. Set attributes to determine how that field is used in an index.

   Take your time with this step because attributes determine the physical expression of fields in the index. If you want to change attributes later, even programmatically, you'll almost always need to drop and rebuild the index. Core attributes like **Searchable** and **Retrievable** have a [negligible effect on storage](search-what-is-an-index.md#index-size). Enabling filters and using suggesters increase storage requirements.

   + **Searchable** enables full-text search. Every field used in free form queries or in query expressions must have this attribute. Inverted indexes are created for each field that you mark as **Searchable**.

   + **Retrievable** returns the field in search results. Every field that provides content to search results must have this attribute. Setting this field doesn't appreciably affect index size.

   + **Filterable** allows the field to be referenced in filter expressions. Every field used in a **$filter**  expression must have this attribute. Filter expressions are for exact matches. Because text strings remain intact, more storage is required to accommodate the verbatim content.

   + **Facetable** enables the field for faceted navigation. Only fields also marked as **Filterable** can be marked as **Facetable**.

   + **Sortable** allows the field to be used in a sort. Every field used in an **$Orderby** expression must have this attribute.

1. Do you need [lexical analysis](search-lucene-query-architecture.md#stage-2-lexical-analysis)? For Edm.string fields that are **Searchable**, you can set an **Analyzer** if you want language-enhanced indexing and querying.

   The default is *Standard Lucene* but you could choose *Microsoft English* if you wanted to use Microsoft's analyzer for advanced lexical processing, such as resolving irregular noun and verb forms. Only language analyzers can be specified in the Azure portal. If you use a custom analyzer or a non-language analyzer like Keyword, Pattern, and so forth, you must create it programmatically. For more information about analyzers, see [Add language analyzers](search-language-support.md).

1. Do you need typeahead functionality in the form of autocomplete or suggested results? Select the **Suggester** the checkbox to enable [typeahead query suggestions and autocomplete](index-add-suggesters.md) on selected fields. Suggesters add to the number of tokenized terms in your index, and thus consume more storage.

### Indexer configuration in the wizard

The last page of the wizard collects user inputs for indexer configuration. You can [specify a schedule](search-howto-schedule-indexers.md) and set other options that will vary by the data source type.

Internally, the wizard also sets up the following definitions, which aren't visible in the indexer until after it's created:

+ [field mappings](search-indexer-field-mappings.md) between the data source and index
+ [output field mappings](cognitive-search-output-field-mapping.md) between skill output and an index

## Try the wizards

The best way to understand the benefits and limitations of the wizard is to step through it. Here are some quickstarts that are based on the wizard.

+ [Quickstart: Create a search index](search-get-started-portal.md)
+ [Quickstart: Create a text translation and entity skillset](search-get-started-skillset.md)
+ [Quickstart: Create a vector index](search-get-started-portal-import-vectors.md)
+ [Quickstart: Image search (vectors)](search-get-started-portal-image-search.md)
