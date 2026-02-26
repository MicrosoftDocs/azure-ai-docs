---
title: Create an indexer
titleSuffix: Azure AI Search
description: Configure an indexer to automate data import and indexing from Azure data sources into a search index in Azure AI Search.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.topic: how-to
ms.date: 06/17/2025
ms.update-cycle: 180-days
ms.custom:
  - ignite-2023
  - sfi-ropc-nochange
---

# Create an indexer in Azure AI Search

This article focuses on the basic steps of creating an indexer that's used to automate data ingestion for supported data sources. Depending on the data source and your workflow, more configuration might be necessary.

You can use an indexer to automate data import and indexing in Azure AI Search. An indexer is a named object on a search service that connects to an external Azure data source, reads and serializes the data, and passes it to a search engine for indexing. Using indexers significantly reduces the quantity and complexity of the code you need to write if you're using a supported data source.

Indexers support two workflows:

+ **Raw content indexing (plain text or vectors)**: Extract strings and metadata from textual content used for full text search scenarios. Extracts raw vector content used for vector search (for example, vectors in an Azure SQL database or Azure Cosmos DB collection). In this workflow, indexing occurs only over existing content that you provide.

+ **Skills-based indexing**: Extends indexing through built-in or custom skills that create or generate new searchable content. For example, you can add integrated machine learning for analysis over images and unstructured text, extracting or inferring text and structure. Or, use skills to chunk and vectorize content from text and images. Skills-based indexing creates or generates new content that doesn't exist in your external data source. New content becomes part of your index when you add fields to the index schema that accepts the incoming data. To learn more, see [AI enrichment in Azure AI Search](cognitive-search-concept-intro.md).

## Prerequisites

+ A [supported data source](search-indexer-overview.md#supported-data-sources) that contains the content you want to ingest.

+ An [indexer data source](#prepare-a-data-source) that sets up a connection to external data.

+ A [search index](search-how-to-create-search-index.md) that can accept incoming data.

+ Be under the [maximum limits](search-limits-quotas-capacity.md#indexer-limits) for your service tier. The Free tier allows three objects of each type and 1-3 minutes of indexer processing, or 3-10 minutes if there's a skillset.

## Indexer patterns

When you create an indexer, the definition is one of two patterns: *content-based indexing* or *skills-based indexing*. The patterns are the same, except that skills-based indexing has more definitions.

### Indexer example for content-based indexing

Content-based indexing for full text or vector search is the primary use case for indexers. For this workflow, an indexer looks like this example.

```json
{
  "name": (required) String that uniquely identifies the indexer,
  "description": (optional),
  "dataSourceName": (required) String indicating which existing data source to use,
  "targetIndexName": (required) String indicating which existing index to use,
  "parameters": {
    "batchSize": null,
    "maxFailedItems": 0,
    "maxFailedItemsPerBatch": 0,
    "base64EncodeKeys": false,
    "configuration": {}
  },
  "fieldMappings": (optional) unless field discrepancies need resolution,
  "disabled": null,
  "schedule": null,
  "encryptionKey": null
}
```

Indexers have the following requirements:

+ A `name` property that uniquely identifies the indexer in the indexer collection
+ A `dataSourceName` property that points to a data source object. It specifies a connection to external data
+ A `targetIndexName` property that points to the destination search index

Other parameters are optional and modify run time behaviors, such as how many errors to accept before failing the entire job. Required parameters are specified in all indexers and are documented in the [REST API reference](/rest/api/searchservice/indexers/create#request-body). 

Data source-specific indexers for blobs, SQL, and Azure Cosmos DB provide extra `configuration` parameters for source-specific behaviors. For example, if the source is Blob Storage, you can set a parameter that filters on file extensions, such as:

```json
"parameters" : { "configuration" : { "indexedFileNameExtensions" : ".pdf,.docx" } }
```

If the source is Azure SQL, you can set a query time-out parameter.

[Field mappings](search-indexer-field-mappings.md) are used to explicitly map source-to-destination fields if there are discrepancies by name or type between a field in the data source and a field in the search index.

By default, an indexer runs immediately when you create it on the search service. If you don't want indexer execution, set `disabled` to *true* when creating the indexer.

You can also [specify a schedule](search-howto-schedule-indexers.md) or set an [encryption key](search-security-manage-encryption-keys.md) for supplemental encryption of the indexer definition.

### Indexer example for skills-based indexing

Skills-based indexing uses [AI enrichment](cognitive-search-concept-intro.md) to process content that isn't searchable in its raw form. All of the above properties and parameters apply, but the following extra properties are specific to AI enrichment: `skillSetName`, `cache`, `outputFieldMappings`.

```json
{
  "name": (required) String that uniquely identifies the indexer,
  "dataSourceName": (required) String, provides raw content that will be enriched,
  "targetIndexName": (required) String, name of an existing index,
  "skillsetName" : (required for AI enrichment) String, name of an existing skillset,
  "cache":  {
    "storageConnectionString" : (required if you enable the cache) Connection string to a blob container,
    "enableReprocessing": true
    },
  "parameters": { },
  "fieldMappings": (optional) Maps fields in the underlying data source to fields in an index,
  "outputFieldMappings" : (required) Maps skill outputs to fields in an index,
}
```

AI enrichment is its own subject area and is out of scope for this article. For more information, start with [AI enrichment](cognitive-search-concept-intro.md), [Skillsets in Azure AI Search](cognitive-search-working-with-skillsets.md), [Create a skillset](cognitive-search-defining-skillset.md), [Map enriched output fields](cognitive-search-output-field-mapping.md), and [Enable caching for AI enrichment](enrichment-cache-how-to-configure.md).

## Prepare external data

Indexers work with data sets. When you run an indexer, it connects to your data source, retrieves the data from the container or folder, optionally serializes it into JSON before passing it to the search engine for indexing. This section describes the requirements of incoming data for text-based indexing.

| Source data | Tasks |
|-------------|-------|
| JSON documents | JSON documents can contain text, numbers, and vectors. Make sure the structure or shape of incoming data corresponds to the schema of your search index. Most search indexes are fairly flat, where the fields collection consists of fields at the same level. However, hierarchical or nested structures are possible through [complex fields and collections](search-howto-complex-data-types.md). |
| Relational | Provide data as a flattened row set, where each row becomes a full or partial search document in the index. <br><br> To flatten relational data into a row set, you should create a SQL view, or build a query that returns parent and child records in the same row. For example, the built-in hotels sample dataset is an SQL database that has 50 records (one for each hotel), linked to room records in a related table. The query that flattens the collective data into a row set embeds all of the room information in JSON documents in each hotel record. The embedded room information is a generated by a query that uses a **FOR JSON AUTO** clause. <br><br> You can learn more about this technique in [define a query that returns embedded JSON](index-sql-relational-data.md#define-a-query-that-returns-embedded-json). This is just one example; you can find other approaches that produce the same result. |
| Files | An indexer generally creates one search document for each file, where the search document consists of fields for content and metadata. Depending on the file type, the indexer can sometimes [parse one file into multiple search documents](search-how-to-index-azure-blob-one-to-many.md). For example, in a CSV file, each row can become a standalone search document. |

Remember that you only need to pull in searchable and filterable data:

+ Searchable data is text or vectors
+ Filterable data is text and numbers (non-vector fields)

Azure AI Search can't do a full-text search over binary data in any format, although it can extract and infer text descriptions of image files (see [AI enrichment](cognitive-search-concept-intro.md)) to create searchable content. Likewise, large text can be broken down and analyzed by natural language models to find structure or relevant information, generating new content that you can add to a search document. It can also do vector search over embeddings, including quantized embeddings in a binary format.

Given that indexers don't fix data problems, other forms of data cleansing or manipulation might be needed. For more information, you should refer to the product documentation of your [Azure database product](/azure/?product=databases).

## Prepare a data source

Indexers require a data source that specifies the type, container, and connection.

1. Make sure you're using a [supported data source type](search-indexer-overview.md#supported-data-sources).

1. [Create a data source](/rest/api/searchservice/data-sources/create) definition. The following data sources are a few of the more frequently used sources:

   + [Azure Blob Storage](search-how-to-index-azure-blob-storage.md)
   + [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md)
   + [Azure SQL Database](search-how-to-index-sql-database.md)

1. If the data source is a database, such as Azure SQL or Cosmos DB, enable change tracking. Azure Storage has built-in change tracking through the `LastModified` property on every blob, file, and table. The links for the various data sources explain which change tracking methods are supported by indexers.

## Prepare an index

Indexers also require a search index. Recall that indexers pass data off to the search engine for indexing. Just as indexers have properties that determine execution behavior, an index schema has properties that profoundly affect how strings are indexed (only strings are analyzed and tokenized). 

1. Start with [Create a search index](search-how-to-create-search-index.md).

1. Set up the fields collection and field attributes. 

   Fields are the only receptors of external content. Depending on how the fields are attributed in the schema, the values for each field are analyzed, tokenized, or stored as verbatim strings for filters, fuzzy search, and typeahead queries.

   Indexers can automatically map source fields to target index fields when the names and types are equivalent. If a field can't be implicitly mapped, remember that you can [define an explicit field mapping](search-indexer-field-mappings.md) that tells the indexer how to route the content.

1. Review the analyzer assignments on each field. Analyzers can transform strings. As such, indexed strings might be different from what you passed in. You can evaluate the effects of analyzers using [Analyze Text (REST)](/rest/api/searchservice/indexes/analyze). For more information about analyzers, see [Analyzers for text processing](search-analyzers.md).

During indexing, an indexer only checks field names and types. There's no validation step that ensures incoming content is correct for the corresponding search field in the index.

## Create an indexer

When you're ready to create an indexer on a remote search service, you need a search client. A search client can be the Azure portal, a REST client, or code that instantiates an indexer client. We recommend the Azure portal or REST APIs for early development and proof-of-concept testing.

### [**Azure portal**](#tab/portal)

1. Sign in to the [Azure portal](https://portal.azure.com) and select your search service.

1. Choose from the following options:

   + [**Import wizards**](search-import-data-portal.md): The wizards are unique in that they create all of the required elements. Other approaches require a predefined data source and index.

       :::image type="content" source="media/search-how-to-create-indexers/portal-indexer-client.png" alt-text="Screenshot that shows the Import data wizard." border="true":::

   + **Add indexer**: A visual editor for specifying an indexer definition.

       :::image type="content" source="media/search-how-to-create-indexers/portal-indexer-client-2.png" alt-text="Screenshot that shows the Add indexer button." border="true":::

### [**REST**](#tab/indexer-rest)

Visual Studio Code with a REST client can send indexer requests. Using the app, you can connect to your search service and send [Create indexer (REST)](/rest/api/searchservice/indexers/create) or [Create or Update indexer](/rest/api/searchservice/indexers/create-or-update) requests. 

```http
POST /indexers?api-version=[api-version]
{
  "name": (required) String that uniquely identifies the indexer,
  "dataSourceName": (required) String indicated which existing data source to use,
  "targetIndexName": (required) String,
  "parameters": {
    "batchSize": null,
    "maxFailedItems": null,
    "maxFailedItemsPerBatch": null,
    "configuration": {
        "executionEnvironment": "standard"
    }
  },
  "fieldMappings": [ optional unless there are field discrepancies that need resolution]
}
```

Parameters are used to set the batch size and how to handle processing failures. The [execution environment](search-howto-run-reset-indexers.md#indexer-execution-environment) determines whether indexer and skillset processing can use the multitenant capabilities provided by Microsoft or the private processing nodes allocated exclusively to your search service. If your search service is Standard2 or higher, you can set `executionEnvironment` to private to pin all indexer processing to just your search service clusters.

There are numerous tutorials and examples that demonstrate REST clients for creating objects. [Quickstart: Full-text search using REST](search-get-started-text.md) can get you started.

### [**.NET SDK**](#tab/indexer-csharp)

For Azure AI Search, the Azure SDKs implement generally available features. As such, you can use any of the SDKs to create indexer-related objects. All of them provide a `SearchIndexerClient` that has methods for creating indexers and related objects, including skillsets.

| Azure SDK | Client | Examples |
|-----------|--------|----------|
| .NET | [SearchIndexerClient](/dotnet/api/azure.search.documents.indexes.searchindexerclient) | [DotNetHowToIndexers](https://github.com/Azure-Samples/search-dotnet-getting-started/tree/master/DotNetHowToIndexers) |
| Java | [SearchIndexerClient](/java/api/com.azure.search.documents.indexes.searchindexerclient) | [CreateIndexerExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/indexes/CreateIndexerExample.java) |
| JavaScript | [SearchIndexerClient](/javascript/api/@azure/search-documents/searchindexerclient) | [Indexers](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/search/search-documents/samples/v11/javascript) |
| Python | [SearchIndexerClient](/python/api/azure-search-documents/azure.search.documents.indexes.searchindexerclient) | [sample_indexers_operations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_indexer_crud.py) |

---

## Run the indexer

By default, an indexer runs immediately when you create it on the search service. You can override this behavior by setting `disabled` to *true* in the indexer definition. Indexer execution is the moment of truth where you find out if there are problems with connections, field mappings, or skillset construction. 

There are several ways to run an indexer:

+ Run on indexer creation or update (default).

+ Run on demand when there are no changes to the definition, or precede with reset for full indexing. For more information, see [Run or reset indexers](search-howto-run-reset-indexers.md).

+ [Schedule indexer processing](search-howto-schedule-indexers.md) to invoke execution at regular intervals. 

Scheduled execution is usually implemented when you have a need for incremental indexing so that you can pick up the latest changes. As such, scheduling has a dependency on change detection.

Indexers are one of the few subsystems that make overt outbound calls to other Azure resources. In terms of Azure roles, indexers don't have separate identities; a connection from the search engine to another Azure resource is made using the [system or user-assigned managed identity](search-how-to-managed-identities.md) of a search service. If the indexer connects to an Azure resource on a virtual network, you should create a [shared private link](search-indexer-howto-access-private.md) for that connection. For more information about secure connections, see [Security in Azure AI Search](search-security-overview.md).

## Check results

[Monitor indexer status](search-monitor-indexers.md) to check for status. Successful execution can still include warning and notifications. Be sure to check both successful and failed status notifications for details about the job.

For content verification, [run queries](search-query-create.md) on the populated index that return entire documents or selected fields.

## Change detection and internal state

If your data source supports change detection, an indexer can detect underlying changes in the data and process just the new or updated documents on each indexer run, leaving unchanged content as-is. If indexer execution history says that a run was successful with *0/0* documents processed, it means that the indexer didn't find any new or changed rows or blobs in the underlying data source.

Change detection logic is built into the data platforms. How an indexer supports change detection varies by data source:

+ Azure Storage has built-in change detection, which means an indexer can recognize new and updated documents automatically. Blob Storage, Azure Table Storage, and Azure Data Lake Storage Gen2 stamp each blob or row update with a date and time. An indexer automatically uses this information to determine which documents to update in the index. For more information about deletion detection, see [Change and delete detection using indexers for Azure Storage](search-how-to-index-azure-blob-changed-deleted.md).

+ Cloud database technologies provide optional change detection features in their platforms. For these data sources, change detection isn't automatic. You need to specify in the data source definition which policy is used:

  + [Azure SQL (change detection)](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows)
  + [Azure DB for MySQL (change detection)](search-how-to-index-mysql.md#indexing-new-and-changed-rows)
  + [Azure Cosmos DB for NoSQL (change detection)](search-how-to-index-cosmosdb-sql.md#indexing-new-and-changed-documents)
  + [Azure Cosmos DB for MongoDB (change detection)](search-how-to-index-cosmosdb-mongodb.md#indexing-new-and-changed-documents)
  + [Azure Cosmos DB for Apache Gremlin (change detection)](search-how-to-index-cosmosdb-gremlin.md#indexing-new-and-changed-documents)

Indexers keep track of the last document it processed from the data source through an internal *high water mark*. The marker is never exposed in the API, but internally the indexer keeps track of where it stopped. When indexing resumes, either through a scheduled run or an on-demand invocation, the indexer references the high water mark so that it can pick up where it left off.

If you need to clear the high water mark to reindex in full, you can use [Reset Indexer](/rest/api/searchservice/indexers/reset). For more selective reindexing, use [Reset Skills](/rest/api/searchservice/skillsets/reset-skills?view=rest-searchservice-2024-05-01-preview&preserve-view=true) or [Reset Documents](/rest/api/searchservice/indexers/reset-docs?view=rest-searchservice-2024-05-01-preview&preserve-view=true). Through the reset APIs, you can clear internal state, and also flush the cache if you enabled [incremental enrichment](enrichment-cache-how-to-configure.md). For more background and comparison of each reset option, see [Run or reset indexers, skills, and documents](search-howto-run-reset-indexers.md).

## Related content

+ [Index data from Azure Blob Storage](search-how-to-index-azure-blob-storage.md)
+ [Index data from Azure SQL database](search-how-to-index-sql-database.md)
+ [Index data from Azure Data Lake Storage Gen2](search-how-to-index-azure-data-lake-storage.md)
+ [Index data from Azure Table Storage](search-how-to-index-azure-tables.md)
+ [Index data from Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md)
