---
title: Data import and data ingestion
titleSuffix: Azure AI Search
description: Populate and upload data to an index in Azure AI Search from external data sources.

manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.custom:
  - ignite-2023
ms.topic: concept-article
ms.date: 09/17/2024
---

# Data import in Azure AI Search

In Azure AI Search, queries execute over user-owned content that's loaded into a [search index](search-what-is-an-index.md). This article describes the two basic workflows for populating an index: *push* your data into the index programmatically, or *pull* in the data using a [search indexer](search-indexer-overview.md).

Both approaches load documents from an external data source. Although you can create an empty index, it's not queryable until you add the content.

> [!NOTE]
> If [AI enrichment](cognitive-search-concept-intro.md) or [integrated vectorization](vector-search-integrated-vectorization.md) are solution requirements, you must use the pull model (indexers) to load an index. Skillsets are attached to indexers and don't run independently.

## Pushing data to an index

Push model is an approach that uses APIs to upload documents into an existing search index. You can upload documents individually or in batches up to 1000 per batch, or 16 MB per batch, whichever limit comes first.

Key benefits include:

+ No restrictions on data source type. The payload must be composed of JSON documents that map to your index schema, but the data can be sourced from anywhere. 

+ No restrictions on frequency of execution. You can push changes to an index as often as you like. For applications having low latency requirements (for example, when the index needs to be in sync with product inventory fluctuations), the push model is your only option.

+ Connectivity and the secure retrieval of documents are fully under your control. In contrast, indexer connections are authenticated using the security features provided in Azure AI Search.

### How to push data to an Azure AI Search index

Use the following APIs to load single or multiple documents into an index:

+ [Index Documents (REST API)](/rest/api/searchservice/documents)
+ [IndexDocumentsAsync (Azure SDK for .NET)](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync) or [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)
+ [IndexDocumentsBatch (Azure SDK for Python)](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch) or [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)
+ [IndexDocumentsBatch (Azure SDK for Java)](/java/api/com.azure.search.documents.indexes.models.indexdocumentsbatch) or [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchindexingbufferedasyncsender)
+ [IndexDocumentsBatch (Azure SDK for JavaScript](/javascript/api/@azure/search-documents/indexdocumentsbatch) or [SearchIndexingBufferedSender](/javascript/api/@azure/search-documents/searchindexingbufferedsender)

There's no support for pushing data via the Azure portal.

For an introduction to the push APIs, see:

+ [Quickstart: Full text search using the Azure SDKs](search-get-started-text.md)
+ [C# Tutorial: Optimize indexing with the push API](tutorial-optimize-indexing-push-api.md)
+ [REST Quickstart: Create an Azure AI Search index using PowerShell](search-get-started-powershell.md)

<a name="indexing-actions"></a>

### Indexing actions: upload, merge, mergeOrUpload, delete

You can control the type of indexing action on a per-document basis, specifying whether the document should be uploaded in full, merged with existing document content, or deleted.

Whether you use the REST API or an Azure SDK, the following document operations are supported for data import:

+ **Upload**, similar to an "upsert" where the document is inserted if it's new, and updated or replaced if it exists. If the document is missing values that the index requires, the document field's value is set to null.

+ **merge** updates a document that already exists, and fails a document that can't be found. Merge replaces existing values. For this reason, be sure to check for collection fields that contain multiple values, such as fields of type `Collection(Edm.String)`. For example, if a `tags` field starts with a value of `["budget"]` and you execute a merge with `["economy", "pool"]`, the final value of the `tags` field is `["economy", "pool"]`. It won't be `["budget", "economy", "pool"]`.

+ **mergeOrUpload** behaves like **merge** if the document exists, and **upload** if the document is new.

+ **delete** removes the entire document from the index. If you want to remove an individual field, use **merge** instead, setting the field in question to null.

## Pulling data into an index

The pull model uses *indexers* connecting to a supported data source, automatically uploading the data into your index. Indexers from Microsoft are available for these platforms:

+ [Azure Blob storage](search-howto-indexing-azure-blob-storage.md)
+ [Azure Table storage](search-howto-indexing-azure-tables.md)
+ [Azure Data Lake Storage Gen2](search-howto-index-azure-data-lake-storage.md)
+ [Azure Files (preview)](search-file-storage-integration.md)
+ [Azure Cosmos DB](search-howto-index-cosmosdb.md)
+ [Azure SQL Database, SQL Managed Instance, and SQL Server on Azure VMs](search-how-to-index-sql-database.md)
+ [OneLake files and shortcuts](search-how-to-index-onelake-files.md)
+ [SharePoint Online (preview)](search-howto-index-sharepoint-online.md)

You can use third-party connectors, developed and maintained by Microsoft partners. For more information and links, see [Data source gallery](search-data-sources-gallery.md).

Indexers connect an index to a data source (usually a table, view, or equivalent structure), and map source fields to equivalent fields in the index. During execution, the rowset is automatically transformed to JSON and loaded into the specified index. All indexers support schedules so that you can specify how frequently the data is to be refreshed. Most indexers provide change tracking if the data source supports it. By tracking changes and deletes to existing documents in addition to recognizing new documents, indexers remove the need to actively manage the data in your index.

### How to pull data into an Azure AI Search index

Use the following tools and APIs for indexer-based indexing:

+ [Import data wizard or Import and vectorize data wizard](search-import-data-portal.md)
+ REST APIs: [Create Indexer (REST)](/rest/api/searchservice/indexers/create), [Create Data Source (REST)](/rest/api/searchservice/data-sources/create), [Create Index (REST)](/rest/api/searchservice/indexes/create)
+ Azure SDK for .NET: [SearchIndexer](/dotnet/api/azure.search.documents.indexes.models.searchindexer), [SearchIndexerDataSourceConnection](/dotnet/api/azure.search.documents.indexes.models.searchindexerdatasourceconnection), [SearchIndex](/dotnet/api/azure.search.documents.indexes.models.searchindex),
+ Azure SDK for Python: [SearchIndexer](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindexer), [SearchIndexerDataSourceConnection](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindexerdatasourceconnection), [SearchIndex](/python/api/azure-search-documents/azure.search.documents.indexes.models.searchindex),
+ Azure SDK for Java: [SearchIndexer](/java/api/com.azure.search.documents.indexes.models.searchindexer), [SearchIndexerDataSourceConnection](/java/api/com.azure.search.documents.indexes.models.searchindexerdatasourceconnection), [SearchIndex](/java/api/com.azure.search.documents.indexes.models.searchindex),
+ Azure SDK for JavaScript: [SearchIndexer](/javascript/api/@azure/search-documents/searchindexer), [SearchIndexerDataSourceConnection](/javascript/api/@azure/search-documents/searchindexerdatasourceconnection), [SearchIndex](/javascript/api/@azure/search-documents/searchindex),

Indexer functionality is exposed in the [Azure portal], the [REST API](/rest/api/searchservice/indexers/create), and the [.NET SDK](/dotnet/api/azure.search.documents.indexes.searchindexerclient).

An advantage to using the Azure portal is that Azure AI Search can usually generate a default index schema by reading the metadata of the source dataset. 

## Verify data import with Search explorer

A quick way to perform a preliminary check on the document upload is to use [**Search explorer**](search-explorer.md) in the Azure portal.

:::image type="content" source="media/search-explorer/search-explorer-cmd2.png" alt-text="Screenshot of Search Explorer command in the Azure portal." border="true":::

The explorer lets you query an index without having to write any code. The search experience is based on default settings, such as the [simple syntax](/rest/api/searchservice/simple-query-syntax-in-azure-search) and default [searchMode query parameter](/rest/api/searchservice/documents/search-post). Results are returned in JSON so that you can inspect the entire document.

Here's an example query that you can run in Search Explorer in JSON view. The "HotelId" is the document key of the hotels-sample-index. The filter provides the document ID of a specific document:

```JSON
{
  "search": "*",
  "filter": "HotelId eq '50'"
}
```

If you're using REST, this [Look up query](search-query-simple-examples.md#example-2-look-up-by-id) achieves the same purpose.

## See also

+ [Indexer overview](search-indexer-overview.md)
+ [Portal quickstart: create, load, query an index](search-get-started-portal.md)
