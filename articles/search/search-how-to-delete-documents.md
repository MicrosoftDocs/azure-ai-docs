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
ms.date: 01/13/2026
---

# Delete documents in a search index

This article explains how to delete whole documents in a search index on Azure AI Search. It covers these tasks:

+ Understand when manual deletion is required
+ Identify specific documents to delete
+ Delete a single document or an orphaned document
+ Delete documents in bulk
+ Confirm deletion

You can use the REST APIs or an Azure SDK client library to delete documents. There's currently no support for deleting documents in the Azure portal.

For more information about deleting or updating a specific field within a document, see [Update or rebuild an index](search-howto-reindex.md).

## Prerequisites

+ You must be a Search Index Data Contributor or have 
`Microsoft.Search/searchServices/indexes/documents/delete` permissions to remove content from an index.

## Understand when manual deletion is required

Manual document deletion is necessary when you use the [push mode approach to indexing](search-what-is-data-import.md#pushing-data-to-an-index), where application code handles data import and drives indexing.

You also need manual document deletion if you use [Logic Apps to load an index (preview)](search-how-to-index-logic-apps.md#limitations).

In contrast, if you use indexers to pull content into an index, data synchronization is built in via the change and deletion detection features of the target data source. All of the supported data sources provide some level change or deletion detection. The following links provide more information:

+ [Azure Storage]()
+ [Azure SQL]()
+ [Azure Cosmos DB]()
+ [Azure Database for MySQL (preview)]()
+ [SharePoint indexer]()
+ [OneLake indexer]()

## Identify specific documents for deletion

Documents might be well-structured, with a collection of fields that map to individual fields in a data source. An example is the hotels-sample-index that has fields for hotel names, descriptions, location, and so forth. Documents might also be chunks of a parent document, such as paragraphs or sections of a PDF. Indexes built for RAG scenarios typically contain chunked documents.

All documents are identified by a [document key](search-how-to-create-search-index.md#document-keys) that uniquely identifies each document in a search index. A document key is a string that's generated during indexing or pulled from a data source if a unique key exists for the record or row you're importing. The index schema identifies the name of the document key field.A document key is an attribute on a field (key equal to true), and there's one key per field collection. It's always `retrievable` so that you can return it in a query.

If you're working with chunked documents, we recommend using the push model (indexers) for change and deletion detection. Alternatively, you might consider deleting all chunks related to single parent and then reindex the parent document if there are partial updates to the source content.

To find the document key, run a query that returns the document and include the document key in the search results. In this example, the HotelId is the document key.

```http
POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/search?api-version=2025-09-01
{
    "search": "this query has terms that pertain to the document I want to delete",
    "select": "HotelName, HotelId",
    "count": true
}
```

Results for this keyword search are the top 50 by default. If the document in question meets the search criteria, you should see it in the results. Have the query select the document key and any descriptive fields that help you confirm you have the correct document.

Once you have the document key, run a [look up query](/rest/api/searchservice/documents/get) that retrieves the document by it's ID to see all of its fields. If the document is a chunk, you should see the ID of the parent document. This example returns the hotel having a document key value of `20`.

```http
GET https://[service name].search.windows.net/indexes/hotels-sample-index/docs('20')&api-version=2025-09-01
```

Use a [REST client](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=rest#query-the-index), an Azure SDK client library, or a [command line tool](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=powershell#query-the-index) to run a look up query. The Azure portal doesn't support GET requests for a query.

## Delete orphan documents

Azure AI Search supports document-level operations so that you can look up, update, and delete a specific document in isolation. The following example shows how to delete a document. 

1. Identify which field is the document key. In the Azure portal, you can view the fields of each index. Document keys are string fields and are denoted with a key icon to make them easier to spot.

1. Check the values of the document key field: `search=*&$select=HotelId`. A simple string is straightforward, but if the index uses a base-64 encoded field, or if search documents were generated from a `parsingMode` setting, you might be working with values that you aren't familiar with.

1. [Look up the document](/rest/api/searchservice/documents/get) to verify the value of the document ID and to review its content before deleting it. Specify the key or document ID in the request. The following examples illustrate a simple string for the [Hotels sample index](search-get-started-portal.md) and a base-64 encoded string for the metadata_storage_path key of the [cog-search-demo index](tutorial-skillset.md).

    ```http
    GET https://[service name].search.windows.net/indexes/hotel-sample-index/docs/1111?api-version=2025-09-01
    ```

    ```http
    GET https://[service name].search.windows.net/indexes/cog-search-demo/docs/aHR0cHM6Ly9oZWlkaWJsb2JzdG9yYWdlMi5ibG9iLmNvcmUud2luZG93cy5uZXQvY29nLXNlYXJjaC1kZW1vL2d1dGhyaWUuanBn0?api-version=2025-09-01
    ```

1. [Delete the document](/rest/api/searchservice/documents) using a delete `@search.action` to remove it from the search index.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key] 
    {  
      "value": [  
        {  
          "@search.action": "delete",  
          "id": "1111"  
        }  
      ]  
    }
    ```

## Delete a single document

### [**REST**](#tab/rest)

[Documents - Index](/rest/api/searchservice/documents) is the REST API for importing data into a search index. 

The body of the request contains one or more documents to be indexed. Documents are uniquely identified through a case-sensitive key. Each document is associated with an action: "upload", "delete", "merge", or "mergeOrUpload". Upload requests must include the document data as a set of key/value pairs.

REST APIs are useful for initial proof-of-concept testing, where you can test indexing workflows without having to write much code. The `@search.action` parameter determines whether documents are added in full, or partially in terms of new or replacement values for specific fields.

[**Quickstart: Full-text search using REST**](search-get-started-text.md) explains the steps. The following example is a modified version of the example. The value is trimmed for brevity and the first HotelId value is altered to avoid overwriting an existing document.

1. Formulate a POST call specifying the index name, the "docs/index" endpoint, and a request body that includes the `@search.action` parameter.

    ```http
    POST https://[service name].search.windows.net/indexes/hotels-sample-index/docs/index?api-version=2025-09-01
    Content-Type: application/json   
    api-key: [admin key] 
    {
        "value": [
        {
        "@search.action": "upload",
        "HotelId": "1111",
        "HotelName": "Stay-Kay City Hotel",
        "Description": "The hotel is ideally located on the main commercial artery of the city in the heart of New York. A few minutes away is Time's Square and the historic centre of the city, as well as other places of interest that make New York one of America's most attractive and cosmopolitan cities.",
        "Category": "Boutique",
        "Tags": [ "pool", "air conditioning", "concierge" ]
        },
        {
        "@search.action": "mergeOrUpload",
        "HotelId": "2",
        "HotelName": "Old Century Hotel",
        "Description": "This is description is replacing the original one for this hotel. New and changed values overwrite the previous ones. In a comma-delimited list like Tags, be sure to provide the full list because there is no merging of values within the field itself.",
        "Category": "Boutique",
        "Tags": [ "pool", "free wifi", "concierge", "my first new tag", "my second new tag" ]
        }
      ]
    }
    ```

1. Set the `@search.action` parameter to `upload` to create or overwrite a document. Set it to `merge` or `uploadOrMerge` if you're targeting updates to specific fields within the document. The previous example shows both actions. 

   | Action | Effect |
   |--------|--------|
   | upload | Similar to an "upsert" where the document is inserted if it's new, and updated or replaced if it exists. If the document is missing values that the index requires, the document field's value is set to null. |
   | merge | Updates a document that already exists, and fails a document that can't be found. Merge replaces existing values. For this reason, be sure to check for collection fields that contain multiple values, such as fields of type `Collection(Edm.String)`. For example, if a `tags` field starts with a value of `["budget"]` and you execute a merge with `["economy", "pool"]`, the final value of the `tags` field is `["economy", "pool"]`. It isn't `["budget", "economy", "pool"]`. |
   | mergeOrUpload | Behaves like merge if the document exists, and upload if the document is new. This is the most common action for incremental updates. |
   | delete | Delete removes the specified document from the index. Any field you specify in a delete operation, other than the key field, is ignored. If you want to remove an individual field from a document, use merge instead and set the field explicitly to null.|

   There are no ordering guarantees for which action in the request body is executed first. It's not recommended to have multiple "merge" actions associated with the same document in a single request body. If there are multiple "merge" actions required for the same document, perform the merging client-side before updating the document in the search index.

   In primitive collections, if the document contains a Tags field of type `Collection(Edm.String)` with a value of ["budget"], and you execute a merge with a value of ["economy", "pool"] for Tag, the final value of the Tags field will be ["economy", "pool"]. It isn't ["budget", "economy", "pool"].

   In complex collections, if the document contains a complex collection field named Rooms with a value of [{ "Type": "Budget Room", "BaseRate": 75.0 }], and you execute a merge with a value of [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }], the final value of the Rooms field will be [{ "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }]. It won't be either of the following:

   + [{ "Type": "Budget Room", "BaseRate": 75.0 }, { "Type": "Standard Room" }, { "Type": "Budget Room", "BaseRate": 60.5 }] (append elements)

   + [{ "Type": "Standard Room", "BaseRate": 75.0 }, { "Type": "Budget Room", "BaseRate": 60.5 }] (merge elements in order, then append any extras)

   > [!NOTE]
   > When you upload DateTimeOffset values with time zone information to your index, Azure AI Search normalizes these values to UTC. For example, 2025-01-13T14:03:00-08:00 will be stored as 2025-01-13T22:03:00Z. If you need to store time zone information, add an extra column to your index.

1. Send the request.

   The following table explains the various per-document [status codes](/rest/api/searchservice/http-status-codes) that can be returned in the response. Some status codes indicate problems with the request itself, while others indicate temporary error conditions. The latter you should retry after a delay.

   |Status code|Meaning|Retryable|Notes|
   |-----------|-------|---------|-----| 
   |200|Document was successfully modified or deleted.|n/a|Delete operations are [idempotent](https://en.wikipedia.org/wiki/Idempotence). That is, even if a document key doesn't exist in the index, attempting a delete operation with that key results in a 200 status code.|
   |201|Document was successfully created.|n/a||
   |400|There was an error in the document that prevented it from being indexed.|No|The error message in the response indicates what is wrong with the document.|
   |404|The document couldn't be merged because the given key doesn't exist in the index.|No|This error doesn't occur for uploads since they create new documents, and it doesn't occur for deletes because they're [idempotent](https://en.wikipedia.org/wiki/Idempotence).|
   |409|A version conflict was detected when attempting to index a document.|Yes|This can happen when you're trying to index the same document more than once concurrently.|
   |422|The index is temporarily unavailable because it was updated with the 'allowIndexDowntime' flag set to 'true'.|Yes||
   |429|Indicates that you have exceeded your quota on the number of documents per index. |No | You must either create a new index or upgrade for higher capacity limits.|
   |503|Your search service is temporarily unavailable, possibly due to heavy load.|Yes|Your code should wait before retrying in this case or you risk prolonging the service unavailability.|

   > [!NOTE]  
   > If your client code frequently encounters a 207 response, one possible reason is that the system is under load. You can confirm this by checking the `statusCode` property for 503. If this is the case, we recommend throttling indexing requests. Otherwise, if indexing traffic doesn't subside, the system could start rejecting all requests with 503 errors.  

1. [Look up the documents](/rest/api/searchservice/documents/get) you just added as a validation step:

    ```http
    GET https://[service name].search.windows.net/indexes/hotel-sample-index/docs/1111?api-version=2025-09-01
    ```

When the document key or ID is new, **null** becomes the value for any field that's unspecified in the document. For actions on an existing document, updated values replace the previous values. Any fields that weren't specified in a "merge" or "mergeUpload" are left intact in the search index.

### [**.NET**](#tab/sdk-dotnet)

The Azure SDK for .NET provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsAsync](/dotnet/api/azure.search.documents.searchclient.indexdocumentsasync)
+ [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1)

There are several samples that illustrate indexing in context of simple and large-scale indexing:

+ [**"Load an index"**](search-howto-dotnet-sdk.md#load-an-index) explains basic steps.

+ [**Azure.Search.Documents Samples - Indexing Documents**](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/search/Azure.Search.Documents/samples/Sample05_IndexingDocuments.md) from the Azure SDK team adds [SearchIndexingBufferedSender](/dotnet/api/azure.search.documents.searchindexingbufferedsender-1).

+ [**Tutorial: Index any data**](tutorial-optimize-indexing-push-api.md) couples batch indexing with testing strategies for determining an optimum size.

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**Python**](#tab/sdk-python)

The Azure SDK for Python provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBatch](/python/api/azure-search-documents/azure.search.documents.indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/python/api/azure-search-documents/azure.search.documents.searchindexingbufferedsender)

Code samples include:

+ [sample_crud_operations.py](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/samples/sample_crud_operations.py)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**JavaScript**](#tab/sdk-javascript)

The Azure SDK for JavaScript/TypeScript provides the following APIs for simple and bulk document uploads into an index:

+ [IndexDocumentsBath](/javascript/api/%40azure/search-documents/indexdocumentsbatch)
+ [SearchIndexingBufferedSender](/javascript/api/%40azure/search-documents/searchindexingbufferedsender)

Code samples include:

+ See this quickstart for basic steps: [Quickstart: Full-text search](search-get-started-text.md?tabs=keyless%2Cwindows&pivots=javascript)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

### [**Java**](#tab/sdk-java)

The Azure SDK for Java provides the following APIs for simple and bulk document uploads into an index:

+ [indexactiontype enumerator](/java/api/com.azure.search.documents.models.indexactiontype)
+ [SearchIndexingBufferedSender](/java/api/com.azure.search.documents.searchclientbuilder.searchindexingbufferedsenderbuilder)

Code samples include:

+ [IndexContentManagementExample.java](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/search/azure-search-documents/src/samples/java/com/azure/search/documents/IndexContentManagementExample.java)

+ Be sure to check the [azure-search-vector-samples](https://github.com/Azure/azure-search-vector-samples) repo for code examples showing how to index vector fields.

---

## Delete documents in bulk

TBD

## Confirm document deletion

Deleting a document doesn't immediately free up space in the index. Every few minutes, a background process performs the physical deletion. Whether you use the Azure portal or an API to return index statistics, you can expect a small delay before the deletion is reflected in the Azure portal and API metrics.

## See also

+ [Search indexes overview](search-what-is-an-index.md)
+ [Data import overview](search-what-is-data-import.md)
+ [Import data wizard overview](search-import-data-portal.md)
+ [Indexers overview](search-indexer-overview.md)
