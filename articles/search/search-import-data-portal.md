---
title: Import Wizards in the Azure portal
titleSuffix: Azure AI Search
description: Learn about the Azure portal wizards that create and load an index and optionally invoke applied AI for vectorization, natural-language processing, language translation, OCR, and image analysis.
author: HeidiSteen
ms.author: heidist
manager: nitinme
ms.date: 01/29/2026
ms.service: azure-ai-search
ms.topic: concept-article
ms.custom:
  - ignite-2024
  - build-2025
  - sfi-image-nochange
---

# Import data wizards in the Azure portal

> [!IMPORTANT]
> We're consolidating the Azure AI Search wizards. Key changes include:
>
> + The **Import and vectorize data** wizard is now called **Import data (new)**.
> + The **Import data** workflow is now available in **Import data (new)**.
>
> The **Import data** wizard will be deprecated soon. For now, you can still use this wizard, but we recommend the new wizard for an improved search experience that uses the latest frameworks.
>
> The wizards don't have identical keyword search workflows. Certain skills and capabilities are only available in the old wizard. For more information about their similarities and differences, continue reading this article.

Azure AI Search has two wizards that automate indexing, enrichment, and object creation for various search scenarios:

+ The **Import data** wizard supports keyword (nonvector) search. You can extract text and numbers from raw documents. You can also configure applied AI and built-in skills to infer structure and generate searchable text from image files and unstructured data.

+ The **Import data (new)** wizard supports keyword search, RAG, and multimodal RAG. For keyword search, it modernizes the **Import data** workflow but lacks some functionality, such as automatic metadata field creation. For RAG and multimodal RAG, it connects to your embedding model deployment, sends requests, and generates vectors from text or images.

Despite their differences, the wizards follow similar workflows for content ingestion and indexing. The following table summarizes their capabilities.

| Capability | Import data wizard | Import data (new) wizard |
|--|--|--|
| Index creation | ✅ | ✅ |
| Indexer pipeline creation | ✅ | ✅ |
| Azure Logic Apps connectors | ❌ | ✅ |
| Built-in sample data | ❌ | ❌ |
| Skills-based enrichment | ✅ | ✅ |
| Vector and multimodal support | ❌ | ✅ |
| Semantic ranking support | ❌ | ✅ |
| Knowledge store support | ✅ | ❌ |

Built-in sample data for the hotels sample index is no longer provided, but you can create an identical index by following the [Quickstart: Create an index for keyword search](search-get-started-portal.md).

This article explains how the wizards work to help you with proof-of-concept testing. For step-by-step instructions, see [Try the wizards](#try-the-wizards).

## Supported data sources and scenarios

This section describes the available options in each wizard.

### Data sources

The wizards support the following data sources, most of which use [built-in indexers](search-indexer-overview.md#supported-data-sources). Exceptions are noted in the table's footnotes.

| Data source | Import data wizard | Import data (new) wizard |
|--|--|--|
| [ADLS Gen2](search-how-to-index-azure-data-lake-storage.md) | ✅ | ✅ |
| [Azure Blob Storage](search-how-to-index-azure-blob-storage.md) | ✅ | ✅ |
| [Azure File Storage](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1, 2</sup> |
| [Azure Queues](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [Azure Table Storage](search-how-to-index-azure-tables.md) | ✅ | ✅ |
| [Azure SQL Database and Managed Instance](search-how-to-index-sql-database.md) | ✅ | ✅ |
| [Cosmos DB for NoSQL](search-how-to-index-cosmosdb-sql.md) | ✅ | ✅ |
| [Cosmos DB for MongoDB](search-how-to-index-cosmosdb-mongodb.md) | ✅ | ✅ |
| [Cosmos DB for Apache Gremlin](search-how-to-index-cosmosdb-gremlin.md) | ✅ | ✅ |
| [MySQL](search-how-to-index-mysql.md)  | ❌ | ❌ |
| [OneDrive](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [OneDrive for Business](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [OneLake](search-how-to-index-onelake-files.md) | ✅ | ✅ |
| [Service Bus](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1</sup> |
| [SharePoint](search-how-to-index-logic-apps.md#supported-connectors) | ❌ | ✅ <sup>1, 2</sup> |
| [SQL Server on virtual machines](search-how-to-index-sql-server.md) | ✅ | ✅ |

<sup>1</sup> This data source uses an [Azure Logic Apps connector (preview)](search-how-to-index-logic-apps.md#supported-connectors) instead of a built-in indexer.

<sup>2</sup> Instead of using a Logic Apps connector, you can use the Search Service REST APIs to programmatically index data from [Azure File Storage](search-file-storage-integration.md) or [SharePoint](search-how-to-index-sharepoint-online.md).

### Skills

Each wizard generates a skillset and outputs field mappings based on options you select. After the skillset is created, you can modify its JSON definition to add or remove skills.

The following skills might appear in a wizard-generated skillset.

| Skill | Import data wizard | Import data (new) wizard |
|--|--|--|
| [Azure Vision multimodal](cognitive-search-skill-vision-vectorize.md)  | ❌ | ✅ <sup>1</sup> |
| [Azure OpenAI embedding](cognitive-search-skill-azure-openai-embedding.md)  | ❌ | ✅ <sup>1</sup> |
| [Azure Machine Learning (Microsoft Foundry model catalog)](cognitive-search-aml-skill.md)  | ❌ | ✅ <sup>1</sup> |
| [Document layout](cognitive-search-skill-document-intelligence-layout.md)  | ❌ | ✅ <sup>1</sup> |
| [Entity recognition](cognitive-search-skill-entity-recognition-v3.md)  | ✅ | ✅ |
| [Image analysis](cognitive-search-skill-image-analysis.md) <sup>2</sup> | ✅ | ✅ |
| [Key phrase extraction](cognitive-search-skill-keyphrases.md)  | ✅ | ✅ |
| [Language detection](cognitive-search-skill-language-detection.md)  | ✅ | ✅ |
| [Text translation](cognitive-search-skill-text-translation.md)  | ✅ | ❌ |
| [OCR](cognitive-search-skill-ocr.md) <sup>2</sup> | ✅ | ✅ |
| [PII detection](cognitive-search-skill-pii-detection.md)  | ✅ | ❌ |
| [Sentiment analysis](cognitive-search-skill-sentiment.md)  | ✅ | ❌ |
| [Shaper](cognitive-search-skill-shaper.md) <sup>3</sup> | ✅ | ❌ |
| [Text Split](cognitive-search-skill-textsplit.md) <sup>4</sup> | ✅ | ✅ |
| [Text Merge](cognitive-search-skill-textmerger.md) <sup>4</sup> | ✅ | ✅ |

<sup>1</sup> This skill is available for RAG and multimodal RAG workflows only. Keyword search isn't supported.

<sup>2</sup> This skill is available for Azure Storage blobs and Microsoft OneLake files, assuming the default parsing mode. Images can be an image content type (such as PNG or JPG) or an embedded image in an application file (such as PDF).

<sup>3</sup> This skill is added when you configure a knowledge store.

<sup>4</sup> This skill is added for data chunking when you choose an embedding model. For nonembedding skills, it's added when you set the source field granularity to pages or sentences.

### Semantic ranker

You can [configure semantic ranking](semantic-how-to-configure.md) to improve the relevance of search results.

| Capability | Import data wizard | Import data (new) wizard |
|--|--|--|
| Semantic ranker | ❌ | ✅ |

### Knowledge store

You can [generate a knowledge store](knowledge-store-create-portal.md) for secondary storage of enriched (skills-generated) content. A knowledge store is useful for information retrieval workflows that don't require a search engine.

| Capability | Import data wizard | Import data (new) wizard |
|--|--|--|
| Knowledge store | ✅ | ❌ |

## What the wizards create

The following table lists the objects created by the wizards. After the objects are created, you can review their JSON definitions in the Azure portal or call them from code.

| Object | Description |
|--|--|
| [Indexer](/rest/api/searchservice/indexers/create) | Configuration object that specifies a data source, target index, optional skillset, optional schedule, and optional configuration settings for error handling and base-64 encoding. |
| [Data source](/rest/api/searchservice/data-sources/create)  | Persists connection information to a [supported data source](search-indexer-overview.md#supported-data-sources) on Azure. A data source object is used exclusively with indexers. |
| [Index](/rest/api/searchservice/indexes/create) | Physical data structure for full-text search, vector search, and other queries. |
| [Skillset](/rest/api/searchservice/skillsets/create) | (Optional) Complete set of instructions for manipulating, transforming, and shaping content, including analyzing and extracting information from image files. Skillsets are also used for integrated vectorization. If the volume of work exceeds 20 transactions per indexer per day, the skillset must include a reference to a Foundry resource that provides enrichment. For integrated vectorization, you can use either Azure Vision or an embedding model in the Foundry model catalog. |
| [Knowledge store](knowledge-store-concept-intro.md) | (Optional) Stores enriched skillset output from tables and blobs in Azure Storage for independent analysis or downstream processing in nonsearch scenarios. Available only in the **Import data** wizard. |

To view these objects after the wizards run:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.
1. From the left pane, select **Search management** to find pages for indexes, indexers, data sources, and skillsets.

## Benefits

Before you write any code, you can use the wizards for prototyping and proof-of-concept testing. The wizards connect to external data sources, sample the data to create an initial index, and then import and optionally vectorize the data as JSON documents into an index on Azure AI Search.

If you're evaluating skillsets, the wizards handle output field mappings and add helper functions to create usable objects. [Text Split](cognitive-search-skill-textsplit.md) is added when you specify a parsing mode. [Text Merge](cognitive-search-skill-textmerger.md) is added when you choose image analysis so that the wizards can reunite text descriptions with image content. [Shaper](cognitive-search-skill-shaper.md) is added to support valid projections when you choose the knowledge store option. All of these tasks come with a learning curve. If you're new to enrichment, having these steps handled for you allows you to measure the value of a skill without investing much time and effort.

Sampling is the process by which an index schema is inferred, which has some limitations. When the data source is created, the wizards pick a random sample of documents to decide what columns are part of the data source. Not all files are read, as doing so could potentially take hours for large data sources. Given a selection of documents, source metadata (such as field name or type) is used to create a fields collection in an index schema. Based on the complexity of the source data, you might need to edit the initial schema for accuracy or extend it for completeness. You can make your changes inline on the index definition page.

Overall, the advantages of the wizards are clear: as long as requirements are met, you can create a queryable index within minutes. The wizards handle some of the complexities of indexing, such as serializing data as JSON documents.

## Limitations

The wizards have the following limitations:

+ The wizards don't support iteration or reuse. Each pass through the wizards creates an index, skillset, and indexer configuration. You can reuse data sources only in the **Import data** wizard. After you finish the wizards, you can edit the created objects by using other portal tools, the REST APIs, or the Azure SDKs.

+ Source content must reside in a [supported data source](search-indexer-overview.md#supported-data-sources).

+ Sampling, used to infer a preliminary index schema, occurs over a subset of source data. For large data sources, it's possible for the wizards to miss fields. If sampling is insufficient, you might need to manually add fields to the index or correct the inferred data types.

+ [AI enrichment](cognitive-search-concept-intro.md) and [integrated vectorization](vector-search-integrated-vectorization.md), as exposed in the wizards, is limited to a subset of built-in skills.

+ A [knowledge store](knowledge-store-concept-intro.md), which is only available through the legacy **Import data** wizard, is limited to a few default projections and uses a default naming convention. To customize projections and names, you must create the knowledge store through the REST APIs or Azure SDKs.

## Secure connections

Network protections affect the portal-to-endpoint connection and also the endpoint-to-external-resource connections during portal operations.

### Portal connections to a search service

Portal connections to a network-protected endpoint are made using your client IP address.

+ For a firewall-protected search service, [add your client IP address to an inbound rule](service-configure-firewall.md#configure-network-access-and-firewall-rules-for-azure-ai-search).

+ For a search service configured for a [private endpoint](service-create-private-endpoint.md), use a browser on an allow-listed virtual machine to open portal pages and run wizards.

+ For a search service joined to a network security perimeter, [add your client IP address to an inbound rule](search-security-network-security-perimeter.md#add-an-inbound-access-rule).

> [!TIP]
> The portal detects your client IP address and prompts you add it to the search service firewall.

### Portal connections to external resources

The portal wizards connect to external resources for:

+ Data retrieval during indexing
+ AI processing for [enrichment](cognitive-search-concept-intro.md) and [integrated vectorization](vector-search-integrated-vectorization.md) performed by a Foundry resource or model

From the portal wizards, almost every outbound request for network-protected data and AI processing is made using the IP address of your client, with the exception of:

+ The legacy Import data wizard
+ Connecting to either Azure Cosmos DB or Azure SQL

This section explains connection requirements for outbound requests, and how to handle the exception.

#### Configuring portal access to external resources

+ **IP-protected resources**: Add your client IP address to the external resource's `allowList`. If supported, list `Microsoft.Search/searchServices` as a trusted service. For example, in Azure Storage, you can list `Microsoft.Search/searchServices` as a trusted service.

+ **Private connections**: The wizards use [shared private links](search-indexer-howto-access-private.md). Verify your search service meets tier and region requirements. Verify your external data source is supported for shared private links.

#### Exception: Legacy wizard with Cosmos DB and Azure SQL

The legacy wizard connects through a portal controller with its own IP address. You must use a public endpoint (no private link support) and [add the portal controller IP to inbound rules](service-configure-firewall.md#allow-access-from-the-azure-portal-ip-address).

You can avoid this restriction by using the **Import data (new)** wizard.

If the wizards can't connect, you'll see `"Access denied due to Virtual Network/Firewall rules"` in the new wizard, or the skillset silently fails to create in the legacy wizard. Consider scripted or programmatic approaches as an alternative.

## Workflow

Both wizards follow a similar high-level workflow:

1. Connect to a supported Azure data source.

1. (Optional) Add skills to extract or generate content and structure.

1. Create an index schema, inferred by sampling source data.

1. Run the wizard to create objects, optionally vectorize data, load data into an index, set a schedule, and configure other options.

The workflow is a one-way pipeline. You can't use the wizard to edit any of the objects that were created, but you can use other portal tools, such as the index designer or JSON editors, to make allowed updates.

### Starting the wizards

To start the wizards:

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. On the **Overview** page, select **Import data** or **Import data (new)**.

    :::image type="content" source="media/search-import-data-portal/import-wizards.png" alt-text="Screenshot of the import wizard options." border="true":::

    The wizards open fully expanded in the browser window, giving you more room to work.

1. Follow the remaining steps to create the index, indexer, and other applicable objects.

You can also launch **Import data** from other Azure services, including Azure Cosmos DB, Azure SQL Database, SQL Managed Instance, and Azure Blob Storage. Look for **Add Azure AI Search** in the left pane on the service overview page.

<a name="data-source-inputs"></a>

### Data source configuration in the wizard

The wizards connect to an external [supported data source](search-indexer-overview.md#supported-data-sources) using the internal logic provided by indexers, which are equipped to sample the source, read metadata, crack documents to read content and structure, and serialize contents as JSON for subsequent import to Azure AI Search.

In the **Import data** wizard, you can paste a connection to a supported data source in a different subscription or region, but the **Choose an existing connection** picker is scoped to the active subscription.

:::image type="content" source="media/search-import-data-portal/choose-connection-same-subscription.png" alt-text="Screenshot of the Connect to your data tab." border="true":::

Not all preview data sources are guaranteed to be available in the wizards. Because each data source has the potential to introduce changes downstream, a preview data source is only added when it fully supports all of the wizard's experiences, such as skillset definition and index schema inference.

You can only import from a single table, database view, or equivalent data structure. However, the structure can include hierarchical or nested substructures. For more information, see [How to model complex types](search-howto-complex-data-types.md).

### Skillset configuration in the wizard

Skillset configuration occurs after the data source definition because the type of data source informs the availability of certain built-in skills. For example, if you're indexing files from Azure Blob Storage, the parsing mode you choose for those files determines whether sentiment analysis is available.

The wizards add not only skills you choose but also skills that are necessary for a successful outcome. For example, if you specify a knowledge store in the **Import data** wizard, the wizard adds a Shaper skill to support projections or physical data structures.

Skillsets are optional, and there's a button at the bottom of the page to skip ahead if you don't want AI enrichment.

<a name="index-definition"></a>

### Index schema configuration in the wizard

The wizards sample your data source to detect the fields and field types. Depending on the data source, they might also offer fields for indexing metadata.

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

### Indexer configuration in the wizard

The last page of the wizard collects user inputs for indexer configuration. You can [specify a schedule](search-howto-schedule-indexers.md) and set other options that vary by the data source type.

Internally, the wizard sets up the following definitions, which aren't visible in the indexer until after it's created.

+ [Field mappings](search-indexer-field-mappings.md) between the data source and index.
+ [Output field mappings](cognitive-search-output-field-mapping.md) between the skill output and an index.

## Try the wizards

The best way to understand the benefits and limitations of the wizards is to step through them. The following quickstarts are based on the wizards.

+ [Quickstart: Create a search index](search-get-started-portal.md)
+ [Quickstart: Create a text translation and entity skillset](search-get-started-skillset.md)
+ [Quickstart: Create a vector index](search-get-started-portal-import-vectors.md)
+ [Quickstart: Create a multimodal index](search-get-started-portal-image-search.md)
