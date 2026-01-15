---
title: Delete Documents
titleSuffix: Azure AI Search
description: Learn how to delete documents in a search index using the REST APIs or an Azure SDK.
manager: nitinme
author: HeidiSteen
ms.author: heidist
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: how-to
ms.date: 01/15/2026
---

# Delete documents in a search index

This article explains how to delete whole documents from a search index on Azure AI Search. 

It covers these tasks:

+ Understand when manual deletion is required
+ Identify specific documents to delete
+ Get document counts and storage metrics
+ Delete a single or orphaned document
+ Delete documents in bulk
+ Confirm deletion

You can use the REST APIs or an Azure SDK client library to delete documents. There's currently no support for document deletion in the Azure portal.

For more information about deleting or updating a *specific field* within a document, see [Update or rebuild an index](search-howto-reindex.md).

## Prerequisites

+ To delete documents, you must have 
`Microsoft.Search/searchServices/indexes/documents/delete` or **Search Index Data Contributor** permissions.

## Understand when manual deletion is required

Manual document deletion is necessary when you use the [push mode approach to indexing](search-what-is-data-import.md#pushing-data-to-an-index), where application code handles data import and drives indexing.

You also need manual document deletion if you use [Logic Apps to load an index (preview)](search-how-to-index-logic-apps.md#limitations).

You might also need manual document deletion in indexer-driven workloads if search documents become "orphaned" from source documents. An important benefit of indexers is automated content retrieval and synchronization via the change and deletion detection features of the target data source. All of the supported data sources provide some level of detection. But in some cases, synchronized deletion is predicated on a soft-delete strategy where you flag a source document (or record) for deletion, run the indexer to delete the indexed content, and only after the index is updated do you physically delete the source content. If source content is deleted first, you have *orphan documents* in the search index. You must manually delete orphan documents in your index to re-establish parity between source and indexed content.

The following links provide more information about change and deletion detection for each data source in indexer-driven workloads.

+ [Azure Storage](search-how-to-index-azure-blob-changed-deleted.md)
+ [Azure SQL](search-how-to-index-sql-database.md#indexing-new-changed-and-deleted-rows)
+ [Azure Cosmos DB](search-how-to-index-cosmosdb-sql.md#indexing-deleted-documents)
+ [Azure Database for MySQL (preview)](search-how-to-index-mysql.md#indexing-deleted-rows)
+ [SharePoint indexer](search-how-to-index-sharepoint-online.md)
+ [OneLake indexer](search-how-to-index-onelake-files.md#supported-tasks)

## Identify specific documents for deletion

All documents are uniquely identified by a [document key](search-how-to-create-search-index.md#document-keys) in a search index. To delete a document, you must identify which field is the document key and provide the key on the deletion request.

In the Azure portal, you can view the fields of each index. Document keys are string fields and are denoted with a key icon to make them easier to spot.

### Find the document key

Once you know which field is the document key, you can get the key value by running a query that returns the key field in the search results.

In this example, the search string is used to find the document in the index, and the select statement determines what fields are in the results. The "HotelId" is the document key in this example. 

```http
POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "this query has terms that pertain to the document I want to delete",
    "select": "HotelName, HotelId",
    "count": true
}
```

Results for this keyword search are the top 50 by default. If the document you want to delete satisfies the search criteria, you should see it (and it's key) in the results. Make sure the query includes a descriptive field that helps you confirm you have the correct document.

```json
{
  "@odata.count": 50,
  "value": [
    {
      "@search.score": 4.5116634,
      "HotelId": "18",
      "HotelName": "Ocean Water Resort & Spa"
    }
   ...
  ]
}
```

A simple string is straightforward, but if the index uses a base-64 encoded field, or if search documents were generated from a `parsingMode` setting, you might be working with values that you aren't familiar with. If you're working with chunked documents create by an indexer, the document key is often a generated "chunked_id" composed of a long sequence of numbers and letters.

## Look up a specific document

Now that you have the document key, run a [look up query](/rest/api/searchservice/documents/get) that retrieves the entire document. If the document is a chunk, you should see the ID of the parent document. The document key is included as a query parameter.

The first example returns the hotel having a document key value of `18`.

```http
GET https://[service name].search.windows.net/indexes/hotels-sample-index/docs('18')&api-version=2025-09-01
```

The second example returns a chunk document. The "chunk_id" is the document key.

```http
GET https://[service name].search.windows.net/indexes/chunking-example-index/docs('aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb')&api-version=2025-09-01
```

The response from the second example includes all fields, which you should review to ensure you know what you're deleting. Fields that include parent information are useful if you need to manually reindex a single parent document into constituent chunked documents in the search index.

```json
{
  "chunk_id": "aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb",
  "parent_id": "bbbbbbbb-1111-2222-3333-cccccccccccc",
  "chunk": "Unpopulated Slopes of an Active Volcano\u2014Naples, Italy ... 90\n\nDazzling Coastlines\u2014Italy ... .92\n\nLiving on Fertile Land\u2014Nile River, Egypt  ... 94\n\n\n\n vii",
  "title": "earth_at_night_508.pdf",
  "text_vector": [ <omitted> ]
}
```

> [!TIP]
> Use a [REST client](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=rest#query-the-index), an Azure SDK client library, or a [command line tool](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=powershell#query-the-index) to run a lookup query. The Azure portal doesn't support GET requests for a query.

## Get document counts and storage metrics

Before you delete documents, get initial metrics for the index document count and storage so that you can confirm deletion later.

You can get document counts and index storage using:

+ The Azure portal, under **Search management** > **Indexes**.
+ The [Indexes - Get Statistics](/rest/api/searchservice/indexes/get-statistics) REST API

Here's an example response:

```json
{
  "documentCount": 12,
  "storageSize": 123456,
  "vectorIndexSize": 123456
}
```

## Delete a single document

### [**REST**](#tab/rest)

1. Use the [Documents - Index](/rest/api/searchservice/documents) REST API with a delete `@search.action` to remove it from the search index. Formulate a POST call specifying the index name and the `docs/index` endpoint. Make sure the body of the request includes the key of the document you want to delete.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key]
    
    {  
      "value": [  
        {  
          "@search.action": "delete",  
          "id": "18"  
        }  
      ]  
    }
    ```

1. Send the request.

   The following table explains the various per-document [status codes](/rest/api/searchservice/http-status-codes) that can be returned in the response. Some status codes indicate problems with the request itself, while others indicate temporary error conditions. The latter you should retry after a delay.

   |Status code|Meaning|Retryable|Notes|
   |-----------|-------|---------|-----| 
   |200|Document was successfully deleted.|n/a|Delete operations are [idempotent](https://en.wikipedia.org/wiki/Idempotence). That is, even if a document key doesn't exist in the index, attempting a delete operation with that key results in a 200 status code.|
   |400|There was an error in the document that prevented it from being deleted.|No|The error message in the response provides details.|
   |422|The index is temporarily unavailable because it was updated with the 'allowIndexDowntime' flag set to 'true'.|Yes|
   |503|Your search service is temporarily unavailable, possibly due to heavy load.|Yes|Your code should wait before retrying in this case or you risk prolonging the service unavailability.|

   > [!NOTE]  
   > If your client code frequently encounters a 207 response, one possible reason is that the system is under load. You can confirm this by checking the `statusCode` property for 503. If so, we recommend throttling indexing requests. Otherwise, if indexing traffic doesn't subside, the system could start rejecting all requests with 503 errors.  

1. You can resend the [Lookup query](/rest/api/searchservice/documents/get) to confirm the deletion. You should get a 404 document not found message. 

    ```http
    GET https://[service name].search.windows.net/indexes/hotel-sample-index/docs/18?api-version=2025-09-01
    ```

### [**.NET**](#tab/sdk-dotnet)

The Azure SDK for .NET provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync)
+ [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)

### [**Python**](#tab/sdk-python)

The Azure SDK for Python provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBatch](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)

Code sample:

+ [sample_crud_operations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_crud_operations.py)

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBath](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for simple and bulk document uploads into an index:

+ [indexactiontype enumerator](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

Code sample:

+ [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

---

## Delete documents in bulk

### [**REST**](#tab/rest)

1. Use the [Documents - Index](/rest/api/searchservice/documents) REST API with a delete `@search.action` to remove it from the search index. Formulate a POST call specifying the index name and the `docs/index` endpoint. Make sure the body of the request includes the keys of all of the documents you want to delete.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key]
    
    {
      "value": [
        {
          "@search.action": "delete",
          "id": "doc1"
        },
        {
          "@search.action": "delete",
          "id": "doc2"
        }
      ]
    }
    ```

+ **Batch limits**: It is recommended to limit batches to 1,000 documents or roughly 16 MB per request to ensure optimal performance.

+ **Idempotency**: Deletion is idempotent; if you attempt to delete a document ID that does not exist, the API will still return a 200 OK status.

+ **Latency**: Documents are not always removed instantly from storage. A background process performs the physical deletion every few minutes.

+ **Vector storage**: Deleting documents does not immediately free up vector storage quotas. It takes several minutes for physical deletion. For immediate reclamation of vector space, you may need to drop and rebuild the index.

### [**.NET**](#tab/sdk-dotnet)

The Azure SDK for .NET provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync)
+ [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)

### [**Python**](#tab/sdk-python)

The Azure SDK for Python provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBatch](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)

Code sample:

+ [sample_crud_operations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_crud_operations.py)

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBath](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for simple and bulk document uploads into an index:

+ [indexactiontype enumerator](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

Code sample:

+ [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

---

## Confirm document deletion

You can find metrics about document counts and index storage using:

+ The Azure portal, under **Search management** > **Indexes**.
+ The [Indexes - Get Statistics](/rest/api/searchservice/indexes/get-statistics) REST API

Get Statistics is the mechanism for retrieving index metrics. The portal calls Get Statistics to populate the index metrics in the portal pages.

Deleting a document doesn't immediately free up space in the index. Every few minutes, a background process performs the physical deletion. Whether you use the Azure portal or the Get Statistics API to return index statistics, you can expect a small delay before the deletion is reflected in the Azure portal and API metrics.

## See also

+ [Search indexes overview](search-what-is-an-index.md)
+ [Data import overview](search-what-is-data-import.md)
+ [Import data wizard overview](search-import-data-portal.md)
+ [Indexers overview](search-indexer-overview.md)
