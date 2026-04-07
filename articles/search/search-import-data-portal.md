---
title: Import Wizard in the Azure portal
titleSuffix: Azure AI Search
description: Learn about the Import data wizard in the Azure portal. The wizard creates an indexing pipeline for keyword search, RAG, and multimodal RAG scenarios, with support for data chunking, vectorization, and AI enrichment.
ms.date: 03/13/2026
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - ignite-2024
  - build-2025
  - sfi-image-nochange
---

# Import data wizard in the Azure portal

The **Import data** wizard in the Azure portal provides a no-code path to a queryable search index. It connects to a supported data source, configures optional AI enrichment and vectorization, infers an index schema, and loads content into the index. You can use the wizard for keyword search, RAG, and multimodal RAG.

The wizard supports:

- Indexer pipeline creation, including an index, indexer, data source, and skillset.
- Built-in indexers and Azure Logic Apps connectors.
- Skills-based AI enrichment.
- Data chunking and integrated vectorization, including multimodal embeddings.
- Semantic ranking configuration.
- Knowledge store creation.

## What the wizard supports

This section describes the capabilities available in the wizard.

### Built-in sample data

Built-in sample data for the hotels-sample index is no longer available. However, you can create an identical index by following [Quickstart: Full-text search in the Azure portal](search-get-started-portal.md).

### Data sources

The wizard connects to the following data sources through [built-in indexers](search-indexer-overview.md#supported-data-sources) or [Logic Apps connectors](search-how-to-index-logic-apps.md#supported-connectors) (preview).

| Data source | Supported | Connection |
|--|--|--|
| [ADLS Gen2](search-how-to-index-azure-data-lake-storage.md) | ✅ | Built-in indexer |
| [Azure Blob Storage](search-how-to-index-azure-blob-storage.md) | ✅ | Built-in indexer |
| [Azure File Storage](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [Azure Queues](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [Azure Table Storage](search-how-to-index-azure-tables.md) | ✅ | Built-in indexer |
| [Azure SQL Database and Managed Instance](search-how-to-index-sql-database.md) | ✅ | Built-in indexer |
| [Cosmos DB for NoSQL](search-how-to-index-cosmosdb-sql.md) | ✅ | Built-in indexer |
| [Cosmos DB for MongoDB](search-how-to-index-cosmosdb-mongodb.md) | ✅ | Built-in indexer |
| [Cosmos DB for Apache Gremlin](search-how-to-index-cosmosdb-gremlin.md) | ✅ | Built-in indexer |
| [MySQL](search-how-to-index-mysql.md) | ❌ | Not applicable |
| [OneDrive](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [OneDrive for Business](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [OneLake](search-how-to-index-onelake-files.md) | ✅ | Built-in indexer |
| [Service Bus](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [SharePoint](search-how-to-index-logic-apps.md#supported-connectors) | ✅ | Logic Apps connector |
| [SQL Server on virtual machines](search-how-to-index-sql-server.md) | ✅ | Built-in indexer |

> [!TIP]
> Instead of using a Logic Apps connector for Azure File Storage or SharePoint, you can use the Search Service REST APIs to programmatically index data from these sources. For more information, see [Index data from Azure Files](search-file-storage-integration.md) and [Index data from SharePoint document libraries](search-how-to-index-sharepoint-online.md).

### Skills

The following skills might appear in a wizard-generated skillset. After the skillset is created, you can modify its JSON definition to add or remove skills.

| Skill | Supported | Description |
|--|--|--|
| [AML](cognitive-search-aml-skill.md) | ✅ | Available for RAG and multimodal RAG only. |
| [Azure Vision multimodal embedding](cognitive-search-skill-vision-vectorize.md) | ✅ | Available for RAG and multimodal RAG only. |
| [Azure OpenAI embedding](cognitive-search-skill-azure-openai-embedding.md) | ✅ | Available for RAG and multimodal RAG only. |
| [Document Layout](cognitive-search-skill-document-intelligence-layout.md) | ✅ | Available for RAG and multimodal RAG only. |
| [Entity Recognition](cognitive-search-skill-entity-recognition-v3.md) | ✅ | Available for keyword search only. |
| [Image Analysis](cognitive-search-skill-image-analysis.md) | ✅ | Available for Azure Storage blobs and Microsoft OneLake files, assuming the default parsing mode. Use an image content type, such as PNG or JPG, or an embedded image in an application file, such as PDF. |
| [Key Phrase Extraction](cognitive-search-skill-keyphrases.md) | ✅ | Available for keyword search only. |
| [Language Detection](cognitive-search-skill-language-detection.md) | ✅ | Available for keyword search only. Automatically added when the skillset includes Entity Recognition, Key Phrase Extraction, or Text Split. Not user configurable. |
| [Text Translation](cognitive-search-skill-text-translation.md) | ❌ | Not applicable. |
| [OCR](cognitive-search-skill-ocr.md) | ✅ | Available for Azure Storage blobs and Microsoft OneLake files, assuming the default parsing mode. Use an image content type, such as PNG or JPG, or an embedded image in an application file, such as PDF. |
| [PII Detection](cognitive-search-skill-pii-detection.md) | ❌ | Not applicable. |
| [Sentiment](cognitive-search-skill-sentiment.md) | ❌ | Not applicable. |
| [Shaper](cognitive-search-skill-shaper.md) | ❌ | Not applicable. |
| [Text Split](cognitive-search-skill-textsplit.md) | ✅ | Added for data chunking when you choose an embedding model. For nonembedding skills, it's added when you set the source field granularity to pages or sentences. |
| [Text Merge](cognitive-search-skill-textmerger.md) | ✅ | Added for data chunking when you choose an embedding model. For nonembedding skills, it's added when you set the source field granularity to pages or sentences. |

### Semantic ranking

Semantic ranking is available for all wizard scenarios: keyword search, RAG, and multimodal RAG. If you enable it, the wizard adds a [semantic configuration](semantic-how-to-configure.md) to the index.

### Knowledge stores

[Knowledge store](knowledge-store-concept-intro.md) creation is available only for the multimodal RAG scenario. The wizard extracts images from your documents and stores them as blobs in an Azure Storage container that you specify.

## What the wizard creates

When you finish the wizard, it creates several objects on your search service. The exact objects depend on the options you select. For example, if you apply skills-based enrichment, a skillset is created.

| Object | Description |
|--|--|
| [Data source](search-data-sources-gallery.md) | Stores connection information for a supported Microsoft or Azure data source. |
| [Index](search-what-is-an-index.md) | Physical data structure for full-text search, vector search, and other queries. Can include a semantic configuration if you enable semantic ranking. |
| [Indexer](search-indexer-overview.md) | Drives data import by pulling from a data source into a target index on an optional schedule. Can also reference a skillset. |
| [Skillset](cognitive-search-working-with-skillsets.md) | (Optional) Set of instructions for AI enrichment, data chunking, and integrated vectorization during indexing. |
| [Knowledge store](knowledge-store-concept-intro.md) | (Optional) Secondary storage in Azure Storage for skillset output, such as extracted images. |

To view these objects after the wizard runs:

1. Go to your search service in the [Azure portal](https://portal.azure.com).
1. From the left pane, select **Search management** to find pages for indexes, indexers, data sources, and skillsets.

## Benefits and limitations

This section discusses the pros and cons of the wizard experience. Use this information to decide when to use the wizard and when to consider alternatives, such as programmatic approaches using REST APIs or Azure SDKs.

### Benefits 

Before you write any code, you can use the wizard for prototyping and proof-of-concept testing. The wizard connects to external data sources, samples the data to create an initial index, and then imports and optionally vectorizes the data as JSON documents into an index on Azure AI Search.

If you're evaluating skillsets, the wizard handles output field mappings and adds helper functions to create usable objects. [Text Split](cognitive-search-skill-textsplit.md) is added when you specify a parsing mode. [Text Merge](cognitive-search-skill-textmerger.md) is added when you choose image analysis so that the wizard can reunite text descriptions with image content. All of these tasks come with a learning curve. If you're new to enrichment, having these steps handled for you allows you to measure the value of a skill without investing much time and effort.

Sampling is the process by which an index schema is inferred, which has some limitations. When the data source is created, the wizard picks a random sample of documents to decide what columns are part of the data source. Not all files are read, as doing so could take hours for large data sources. Given a selection of documents, source metadata (such as field name or type) is used to create a fields collection in an index schema. Based on the complexity of the source data, you might need to edit the initial schema for accuracy or extend it for completeness. You can make your changes inline on the index definition page.

Overall, the advantages of the wizard are clear: as long as requirements are met, you can create a queryable index within minutes. The wizard handles some of the complexities of indexing, such as serializing data as JSON documents.

### Limitations

- The wizard doesn't support iteration or reuse. Each pass through the wizard creates an index, skillset, and indexer configuration. After you finish the wizard, you can edit the created objects by using other portal tools, the REST APIs, or the Azure SDKs.

- Source content must reside in a [supported data source](search-indexer-overview.md#supported-data-sources).

- Sampling, used to infer a preliminary index schema, occurs over a subset of source data. For large data sources, it's possible for the wizard to miss fields. If sampling is insufficient, you might need to manually add fields to the index or correct the inferred data types.

- [AI enrichment](cognitive-search-concept-intro.md) and [integrated vectorization](vector-search-integrated-vectorization.md), as exposed in the wizard, is limited to a subset of built-in skills.

## Secure connections

Network protections affect the portal-to-endpoint connection and also the endpoint-to-external-resource connections during portal operations.

### Portal connections to a search service

Portal connections to a network-protected endpoint are made using your client IP address.

+ For a firewall-protected search service, [add your client IP address to an inbound rule](service-configure-firewall.md#configure-network-access-and-firewall-rules-for-azure-ai-search).

+ For a search service configured for a [private endpoint](service-create-private-endpoint.md), use a browser on an allow-listed virtual machine to open portal pages and run the wizard.

+ For a search service joined to a network security perimeter, [add your client IP address to an inbound rule](search-security-network-security-perimeter.md#add-an-inbound-access-rule).

> [!TIP]
> The portal detects your client IP address and prompts you add it to the search service firewall.

### Portal connections to external resources

The wizard connects to external resources for:

+ Data retrieval during indexing.
+ AI processing for [enrichment](cognitive-search-concept-intro.md) and [integrated vectorization](vector-search-integrated-vectorization.md) performed by a Microsoft Foundry resource or model.

From the wizard, almost every outbound request for network-protected data and AI processing is made using the IP address of your client.

This section explains connection requirements for outbound requests.

#### Configure portal access to external resources

+ **IP-protected resources**: Add your client IP address to the external resource's `allowList`. If supported, list `Microsoft.Search/searchServices` as a trusted service. For example, in Azure Storage, you can list `Microsoft.Search/searchServices` as a trusted service.

+ **Private connections**: The wizard uses [shared private links](search-indexer-howto-access-private.md). Verify your search service meets tier and region requirements. Verify your external data source is supported for shared private links.

If the wizard can't connect, you'll see `"Access denied due to Virtual Network/Firewall rules"`. Consider scripted or programmatic approaches as an alternative.

## Workflow

The wizard follows a high-level workflow:

1. Connect to a supported Azure data source.

1. (Optional) Add skills to extract or generate content and structure.

1. Create an index schema, inferred by sampling source data.

1. Run the wizard to create objects, optionally vectorize data, load data into an index, set a schedule, and configure other options.

The workflow is a one-way pipeline. You can't use the wizard to edit any of the objects that were created, but you can use other portal tools, such as the index designer or JSON editors, to make allowed updates.

### Start the wizard

1. Go to your search service in the [Azure portal](https://portal.azure.com).

1. On the **Overview** page, select **Import data**.

    :::image type="content" source="media/search-import-data-portal/import-data-button.png" alt-text="Screenshot of the import wizard options." border="true":::

    The wizard opens fully expanded in the browser window, giving you more room to work.

1. Select a scenario: **Keyword search**, **RAG**, or **Multimodal RAG**.

    The scenario you select determines the available data sources and skills, as well as the index schema and indexer configuration that are created by the wizard.

1. Follow the remaining steps to create the index, indexer, and other applicable objects.

<a name="data-source-inputs"></a>

### Configure a data source

The wizard connects to an external [supported data source](search-indexer-overview.md#supported-data-sources) using the internal logic provided by indexers, which are equipped to sample the source, read metadata, crack documents to read content and structure, and serialize contents as JSON for subsequent import to Azure AI Search.

Not all preview data sources are guaranteed to be available in the wizard. Because each data source has the potential to introduce changes downstream, a preview data source is only added when it fully supports all of the wizard's experiences, such as skillset definition and index schema inference.

You can only import from a single table, database view, or equivalent data structure. However, the structure can include hierarchical or nested substructures. For more information, see [How to model complex types](search-howto-complex-data-types.md).

### Configure a skillset

Skillset configuration occurs after the data source definition because the type of data source informs the availability of certain built-in skills. For example, if you're indexing files from Azure Blob Storage, the parsing mode you choose for those files determines whether sentiment analysis is available.

The wizard adds not only skills you choose but also skills that are necessary for a successful outcome.

Skillsets are optional, and there's a button at the bottom of the page to skip ahead if you don't want AI enrichment.

<a name="index-definition"></a>

### Configure an index schema

The wizard samples your data source to detect the fields and field types. Depending on the data source, it might also offer fields for indexing metadata.

Because sampling is an imprecise exercise, review the index for the following considerations:

1. Is the field list accurate? If your data source contains fields that weren't picked up in sampling, you can manually add the missed fields. You can also remove fields that don't add value to the search experience or won't be used in a [filter expression](search-query-odata-filter.md) or [scoring profile](index-add-scoring-profiles.md).

1. Is the data type appropriate for the incoming data? Azure AI Search supports the [entity data model (EDM) data types](/rest/api/searchservice/supported-data-types). For Azure SQL data, there's a [mapping chart](search-how-to-index-sql-database.md#TypeMapping) that lays out equivalent values. For more information, see [Field mappings and transformations](search-indexer-field-mappings.md).

1. Do you have one field that can serve as the *key*? This field must be an Edm.String that uniquely identifies a document. For relational data, it might be mapped to a primary key. For blobs, it might be the `metadata-storage-path`. If field values include spaces or dashes, you must set the **Base-64 Encode Key** option in the **Create an indexer** step, under **Advanced options**, to suppress the validation check for these characters.

1. Set attributes to determine how that field is used in an index.

   Take your time with this step because attributes determine the physical expression of fields in the index. If you want to change attributes later, even programmatically, you almost always need to drop and rebuild the index. Core attributes like **Searchable** and **Retrievable** have a [negligible effect on storage](search-what-is-an-index.md#index-size). Enabling filters and using suggesters increase storage requirements.

   + **Searchable** enables full-text search. Every field used in free-form queries or in query expressions must have this attribute. Inverted indexes are created for each field that you mark as **Searchable**.

   + **Retrievable** returns the field in search results. Every field that provides content to search results must have this attribute. Setting this field doesn't appreciably affect index size.

   + **Filterable** allows the field to be referenced in filter expressions. Every field used in a **$filter** expression must have this attribute. Filter expressions are for exact matches. Because text strings remain intact, more storage is required to accommodate the verbatim content.

   + **Facetable** enables the field for faceted navigation. Only fields also marked as **Filterable** can be marked as **Facetable**.

   + **Sortable** allows the field to be used in a sort. Every field used in an **$Orderby** expression must have this attribute.

1. Do you need [lexical analysis](search-lucene-query-architecture.md#stage-2-lexical-analysis)? For Edm.String fields that are **Searchable**, you can set an **Analyzer** if you want language-enhanced indexing and querying.

   The default is *Standard Lucene*, but you can choose *Microsoft English* if you wanted to use Microsoft's analyzer for advanced lexical processing, such as resolving irregular noun and verb forms. Only language analyzers can be specified in the Azure portal. If you want to use a custom analyzer or non-language analyzer, such as Keyword or Pattern, you must create it programmatically. For more information, see [Add language analyzers](search-language-support.md).

1. Do you need typeahead functionality in the form of autocomplete or suggested results? Select the **Suggester** checkbox to enable [typeahead query suggestions and autocomplete](index-add-suggesters.md) on selected fields. Suggesters add to the number of tokenized terms in your index and thus consume more storage.

### Configure an indexer

The last page of the wizard collects user inputs for indexer configuration. You can [specify a schedule](search-howto-schedule-indexers.md) and set other options that vary by the data source type.

Internally, the wizard sets up the following definitions, which aren't visible in the indexer until after it's created.

+ [Field mappings](search-indexer-field-mappings.md) between the data source and index.
+ [Output field mappings](cognitive-search-output-field-mapping.md) between the skill output and an index.

## Try the wizard

The best way to understand the benefits and limitations of the **Import data** wizard is to step through it. The following quickstarts are based on the wizard.

+ [Quickstart: Full-text search in the Azure portal](search-get-started-portal.md)
+ [Quickstart: Vector search in the Azure portal](search-get-started-portal-import-vectors.md)
+ [Quickstart: Multimodal search in the Azure portal](search-get-started-portal-image-search.md)
+ [Quickstart: Create a skillset in the Azure portal](search-get-started-skillset.md)
